"""Simplified 3D trailer assembly: tank + chassis rails + kingpin + 4 axles (suspension, dual wheels) + landing legs.

Units mm. x along the trailer (x=0 front tangent line of the tank, same as tank_shell), y lateral, z up (ground z=0).
Proportional placeholders for presentation, NOT a structural design: every dimension below is an assumption the
engineer replaces (sizes of rails, tyres, suspension, heights).
"""
from dataclasses import dataclass
from math import cos, radians

import cadquery as cq

from src.axle_load import AxleSpec, axle_positions
from src.tank_shell import ShellSpec, build_baffle, build_parts, build_plates


@dataclass(frozen=True)
class DetailSpec:
    """Details copied from the owner's colour photo. Positions from the front junction (mm), ASSUMED +-150 mm."""
    toolbox_x: float = 5150.0          # box on top of the tank (function to confirm)
    toolbox_len: float = 1500.0
    toolbox_w: float = 600.0
    toolbox_h: float = 300.0
    pipe_x: float = 7150.0             # vertical pipe/ladder on the side, valve at the top
    pipe_d: float = 76.0
    panel_x: float = 10075.0           # hazard panel (painel de seguranca) centre
    diamond_x: tuple = (10540.0, 11015.0)   # hazard labels (rotulos de risco) centres
    placard_above_bottom: float = 500.0     # height of the placards above the tank bottom
    u_width: float = 120.0             # U-shaped external reinforcement at each baffle (lower half ring)
    red_band_width: float = 40.0


@dataclass(frozen=True)
class GearSpec:
    tire_radius: float = 552.5       # sizes below from the 52 m3 STEP assembly (tyre OD 1105 x 275, dual gap 60)
    tire_width: float = 275.0
    dual_gap: float = 60.0
    track: float = 1940.0            # centre of the dual pair, left to right
    rail_spacing: float = 970.0      # centre to centre
    rail_width: float = 80.0
    rail_height: float = 320.0
    landing_leg_from_kingpin: float = 2500.0   # pe de apoio, owner confirmed 2026-10-10
    rail_top_z: float = 1380.0       # tank bottom rests here (STEP: 1353-1399 above ground, tank slopes slightly)
    ring_count: int = 9              # outer stiffening rings seen in the photo (orange bands), spacing ASSUMED
    ring_width: float = 60.0
    ring_thickness: float = 6.0
    baffle_hole: float = 500.0       # Anexo H: baffle passage opening >= 500 mm
    crossmember_pitch: float = 1500.0


def _box(x0, x1, y0, y1, z0, z1) -> cq.Workplane:
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def _cyl_y(x, y, z, r, w) -> cq.Workplane:
    """Cylinder with axis along Y, centred at (x, y, z)."""
    return cq.Workplane("XZ").circle(r).extrude(w / 2, both=True).translate((x, y, z))


def build_trailer(shell: ShellSpec, axles: AxleSpec, gear: GearSpec = GearSpec(),
                  det: DetailSpec = DetailSpec()) -> dict[str, list[cq.Workplane]]:
    shell.check()
    pos = axle_positions(axles, shell)
    kp, axle_x = pos["kingpin_x"], pos["axle_x"]
    zc = gear.rail_top_z + shell.ri + max(shell.shell_thickness, shell.head_thickness)   # tank axis height
    x_front, x_rear = kp - 300.0, axle_x[-1] + axles.chassis_rear_overhang_mm
    half = gear.rail_spacing / 2
    rz0 = gear.rail_top_z - gear.rail_height
    g: dict[str, list] = {k: [] for k in ("TANQUE", "ANEIS", "REFORCO_VERM", "REFORCOS_U", "QUEBRA_ONDAS", "CAIXA",
                                          "TUBULACAO", "PLACAS", "CHASSI", "PARACHOQUE", "PINO_REI", "EIXOS",
                                          "SUSPENSAO", "RODAS", "PARALAMAS")}

    parts = build_parts(shell)
    g["TANQUE"] = [wp.translate((0, 0, zc)) for wp in (*build_plates(shell), parts["calota_dianteira"], parts["calota_traseira"])]

    ro = shell.ri + shell.shell_thickness
    L = shell.straight_length
    ring_x = shell.ring_positions or tuple(600 + i * (L - 1200) / (gear.ring_count - 1) for i in range(gear.ring_count))
    baffle_x = shell.baffle_positions or (axle_x[0], (axle_x[1] + axle_x[2]) / 2, axle_x[3])
    for x in ring_x:                                                  # outer rings / straps
        g["ANEIS"].append(cq.Workplane("YZ").circle(ro + gear.ring_thickness).circle(ro).extrude(gear.ring_width)
                          .translate((x - gear.ring_width / 2, 0, zc)))
    for x in baffle_x:                                                # dished baffles + external U reinforcement
        g["QUEBRA_ONDAS"].append(build_baffle(shell, gear.baffle_hole).translate((x, 0, zc)))
        u = (cq.Workplane("YZ").circle(ro + 10).circle(ro).extrude(det.u_width).translate((x - det.u_width / 2, 0, 0))
             .intersect(_box(x - det.u_width, x + det.u_width, -ro - 20, ro + 20, -ro - 20, 0)))
        g["REFORCOS_U"].append(u.translate((0, 0, zc)))
    for x in shell.red_band_positions:
        g["REFORCO_VERM"].append(cq.Workplane("YZ").circle(ro + 8).circle(ro).extrude(det.red_band_width)
                                 .translate((x - det.red_band_width / 2, 0, zc)))
    top = zc + ro
    g["CAIXA"].append(_box(det.toolbox_x, det.toolbox_x + det.toolbox_len, -det.toolbox_w / 2, det.toolbox_w / 2,
                           top - 60, top + det.toolbox_h))
    g["TUBULACAO"].append(cq.Workplane("XY").circle(det.pipe_d / 2).extrude(top - gear.rail_top_z)
                          .translate((det.pipe_x, ro + 60, gear.rail_top_z)))
    g["TUBULACAO"].append(_box(det.pipe_x - 90, det.pipe_x + 90, ro - 30, ro + 150, top - 40, top + 160))   # top valve
    pz = zc - ro + det.placard_above_bottom
    g["PLACAS"].append(_box(det.panel_x - 190, det.panel_x + 190, ro, ro + 6, pz - 150, pz + 150))
    for dx in det.diamond_x:
        sq = _box(dx - 150, dx + 150, ro, ro + 6, pz - 150, pz + 150)
        g["PLACAS"].append(sq.rotate((dx, 0, pz), (dx, 1, pz), 45))
    xb = x_rear
    g["PARACHOQUE"].append(_box(xb, xb + 100, -1100, 1100, 500, 700))                 # rear bumper bar
    for s in (-1, 1):
        g["PARACHOQUE"].append(_box(xb - 60, xb + 100, s * 1000 - 50, s * 1000 + 50, 700, rz0))   # posts
        g["PARACHOQUE"].append(_box(xb + 100, xb + 160, s * 950 - 60, s * 950 + 60, 560, 640))    # lights

    for s in (-1, 1):
        y0, y1 = sorted((s * half - gear.rail_width / 2, s * half + gear.rail_width / 2))
        g["CHASSI"].append(_box(x_front, x_rear, y0, y1, rz0, gear.rail_top_z))
    n = int((x_rear - x_front) // gear.crossmember_pitch) + 1
    for i in range(n + 1):
        x = x_front + i * (x_rear - x_front - 100) / n
        g["CHASSI"].append(_box(x, x + 100, -half, half, rz0, rz0 + 150))
    g["CHASSI"].append(_box(kp - 450, kp + 450, -500, 500, gear.rail_top_z - 70, gear.rail_top_z - 20))  # kingpin plate
    g["PINO_REI"].append(cq.Workplane("XY").circle(25.4).extrude(100).translate((kp, 0, gear.rail_top_z - 170)))
    for s in (-1, 1):                                                                                  # landing legs
        y = s * (half + 300)
        lx = kp + gear.landing_leg_from_kingpin
        g["CHASSI"].append(_box(lx - 70, lx + 70, y - 70, y + 70, 380, rz0))
        g["CHASSI"].append(_box(lx - 200, lx + 200, y - 150, y + 150, 360, 380))

    zax = gear.tire_radius
    for x in axle_x:
        g["EIXOS"].append(_box(x - 70, x + 70, -1000, 1000, zax - 70, zax + 70))
        for s in (-1, 1):
            g["SUSPENSAO"].append(_box(x - 500, x + 500, s * half - 45, s * half + 45, zax + 100, zax + 200))   # spring pack
            for dx in (-450, 450):
                g["SUSPENSAO"].append(_box(x + dx - 60, x + dx + 60, s * half - 50, s * half + 50, zax + 200, rz0))  # hangers
            for d in (-1, 1):
                y = s * gear.track / 2 + d * (gear.tire_width + gear.dual_gap) / 2
                tire = _cyl_y(x, y, zax, gear.tire_radius, gear.tire_width).edges().fillet(35)
                g["RODAS"].append(tire)
                g["RODAS"].append(_cyl_y(x, y, zax, 285, gear.tire_width + 20))
            fw = 2 * gear.tire_width + gear.dual_gap + 40            # mudguard over the dual pair
            fr = gear.tire_radius + 45
            ring = cq.Workplane("XZ").circle(fr).circle(fr - 4).extrude(fw / 2, both=True)
            upper = _box(-fr, fr, -fw / 2, fw / 2, 0, fr)
            g["PARALAMAS"].append(ring.intersect(upper).translate((x, s * gear.track / 2, zax)))
    return g


def smooth_flags(verts, tris, angle_deg: float = 15.0) -> list[int]:
    """DXF 3DFACE invisible-edge bits per triangle: hide edges shared by nearly coplanar triangles."""
    key = [(round(v.x, 2), round(v.y, 2), round(v.z, 2)) for v in verts]
    normals = []
    for i, j, k in tris:
        n = (verts[j] - verts[i]).cross(verts[k] - verts[i])
        normals.append(n.normalized() if n.Length > 1e-12 else n)
    edges: dict = {}
    for t, (i, j, k) in enumerate(tris):
        for e, (p, q) in enumerate(((i, j), (j, k), (k, i))):
            edges.setdefault(frozenset((key[p], key[q])), []).append((t, e))
    bit = (1, 2, 8)  # v0v1, v1v2, v2v0 (4th vertex repeats v2, so the 3rd edge is bit 8)
    flags = [0] * len(tris)
    cos_thr = cos(radians(angle_deg))
    for faces in edges.values():
        if len(faces) == 2 and abs(normals[faces[0][0]].dot(normals[faces[1][0]])) >= cos_thr:
            for t, e in faces:
                flags[t] |= bit[e]
    return flags


LAYER_COLORS = {"TANQUE": 254, "ANEIS": 30, "REFORCO_VERM": 1, "REFORCOS_U": 255, "CAIXA": 9, "TUBULACAO": 8,
                "PLACAS": 250, "PARACHOQUE": 94, "QUEBRA_ONDAS": 1, "CHASSI": 94, "PINO_REI": 1, "EIXOS": 3,
                "SUSPENSAO": 8, "RODAS": 250, "PARALAMAS": 94}


# (linear tolerance mm, angular tolerance rad) per layer: fine on the tank, coarse on small parts
MESH_QUALITY = {"REFORCO_VERM": (2.0, 0.15), "REFORCOS_U": (2.0, 0.15), "CAIXA": (5.0, 0.5), "TUBULACAO": (2.0, 0.3),
                "PLACAS": (5.0, 0.5), "PARACHOQUE": (5.0, 0.5), "TANQUE": (1.5, 0.1), "ANEIS": (2.0, 0.15), "QUEBRA_ONDAS": (2.0, 0.15), "RODAS": (3.0, 0.3),
                "CHASSI": (5.0, 0.5), "PINO_REI": (1.0, 0.3), "EIXOS": (5.0, 0.5), "SUSPENSAO": (5.0, 0.5),
                "PARALAMAS": (3.0, 0.3)}


def export_dxf(groups: dict, path: str) -> int:
    import ezdxf

    doc = ezdxf.new("R2000")
    msp = doc.modelspace()
    total = 0
    for layer, parts in groups.items():
        doc.layers.add(layer, color=LAYER_COLORS[layer])
        tolerance, angular = MESH_QUALITY[layer]
        for wp in parts:
            verts, tris = wp.val().tessellate(tolerance, angular)
            for (i, j, k), fl in zip(tris, smooth_flags(verts, tris)):
                f = msp.add_3dface([verts[i].toTuple(), verts[j].toTuple(), verts[k].toTuple(), verts[k].toTuple()],
                                   dxfattribs={"layer": layer})
                f.dxf.invisible_edges = fl
                total += 1
    doc.saveas(path)
    return total


def export_step(groups: dict, path: str) -> None:
    solids = [wp.val() for parts in groups.values() for wp in parts]
    cq.exporters.export(cq.Workplane("XY").add(cq.Compound.makeCompound(solids)), path)


if __name__ == "__main__":
    import sys

    from src.presets import DEFAULT, get

    name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    groups = build_trailer(*get(name))
    export_step(groups, f"out/carreta_{name}_3d.step")
    print(name, "faces:", export_dxf(groups, f"out/carreta_{name}_3d.dxf"))
