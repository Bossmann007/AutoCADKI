"""Parametric tank shell: circular cylinder (casco) + two torispherical heads (calotas), as 3 separate parts.

Units: mm. Tank axis = X, x=0 at the front tangent line, x increases to the rear.
Thicknesses are INPUTS; they are not derived from Portaria INMETRO 134/2022 Anexo H.
Head type "ASME 10" is ASSUMED to mean crown radius = 1.0 x Di, knuckle radius = 0.10 x Di
(confirm with the engineer). Straight flange of the heads is not modelled.
"""
from dataclasses import dataclass
from math import atan2, cos, pi, radians, sin, sqrt

import cadquery as cq

MAX_WIDTH_MM = 2600  # CONTRAN Res. 882/2021 art. 4 (verified in docs/research/ai-cad-trailers.md)


@dataclass(frozen=True)
class ShellSpec:
    inner_diameter: float = 2290.0
    straight_length: float = 12888.0   # between head tangent lines (hand sketch: see straight_length_for_capacity)
    shell_thickness: float = 3.0
    head_thickness: float = 4.0
    crown_factor: float = 1.0          # crown radius / Di
    knuckle_factor: float = 0.10       # knuckle radius / Di
    baffle_count: int = 3
    baffle_volume_l: float = 41.0      # volume displaced by each baffle (hand sketch)
    capacity_factor: float = 1.025     # geometric net volume / nominal capacity (hand sketch)

    def check(self) -> None:
        if min(self.inner_diameter, self.straight_length, self.shell_thickness,
               self.head_thickness, self.crown_factor, self.knuckle_factor) <= 0:
            raise ValueError("all dimensions must be > 0")
        if not 0 < self.knuckle_factor <= 0.5 or self.crown_factor < 0.5 + self.knuckle_factor / 2:
            raise ValueError("invalid torispherical head proportions")
        if self.outer_diameter > MAX_WIDTH_MM:
            raise ValueError(f"outer width {self.outer_diameter} mm exceeds CONTRAN limit {MAX_WIDTH_MM} mm")

    @property
    def ri(self) -> float:
        return self.inner_diameter / 2

    @property
    def outer_diameter(self) -> float:
        return self.inner_diameter + 2 * max(self.shell_thickness, self.head_thickness)

    @property
    def crown_radius(self) -> float:
        return self.crown_factor * self.inner_diameter

    @property
    def knuckle_radius(self) -> float:
        return self.knuckle_factor * self.inner_diameter

    @property
    def head_depth_inner(self) -> float:
        """Inner depth of one head (apex to tangent line), straight flange not included."""
        R, r = self.crown_radius, self.knuckle_radius
        return R - sqrt((R - r) ** 2 - (self.ri - r) ** 2)

    @property
    def head_depth_outer(self) -> float:
        return self.head_depth_inner + self.head_thickness

    @property
    def overall_length(self) -> float:
        return self.straight_length + 2 * self.head_depth_outer


def head_geometry(spec: ShellSpec) -> dict:
    """Centres and angles of the front (left) head, inner surface. Angles in degrees, CCW from +X."""
    R, r, ri, h = spec.crown_radius, spec.knuckle_radius, spec.ri, spec.head_depth_inner
    crown_c = (R - h, 0.0)                 # crown centre on the axis
    knuckle_c = (0.0, ri - r)              # knuckle centre, on the tangent line
    dx, dy = knuckle_c[0] - crown_c[0], knuckle_c[1] - crown_c[1]
    n = sqrt(dx * dx + dy * dy)
    u = (dx / n, dy / n)                   # unit vector crown centre -> knuckle centre
    return {"crown_c": crown_c, "knuckle_c": knuckle_c, "u": u, "theta": atan2(u[1], u[0]) * 180 / pi}


def _pt(c, rad, ang_deg):
    return (c[0] + rad * cos(radians(ang_deg)), c[1] + rad * sin(radians(ang_deg)))


def litros_por_cm(spec: ShellSpec) -> float:
    """Inner volumetric capacity per cm of straight length (key input of Anexo H thickness tables)."""
    return pi * spec.ri ** 2 * 10 / 1e6  # mm^2 * 10 mm (1 cm) / 1e6 mm^3 per litre


def capacidade_litros(spec: ShellSpec, steps: int = 20000) -> float:
    """Inner capacity: cylinder + 2 heads, heads integrated numerically over the analytic profile."""
    R, r, ri, h = spec.crown_radius, spec.knuckle_radius, spec.ri, spec.head_depth_inner
    g = head_geometry(spec)
    cx = g["crown_c"][0]
    x_t = g["knuckle_c"][0] + r * g["u"][0]      # crown/knuckle tangent point, x
    dx = h / steps
    vol = 0.0
    for i in range(steps):
        x = -h + (i + 0.5) * dx
        y = sqrt(R * R - (x - cx) ** 2) if x < x_t else g["knuckle_c"][1] + sqrt(r * r - x * x)
        vol += pi * y * y * dx
    return (pi * ri ** 2 * spec.straight_length + 2 * vol) / 1e6


def _arc(wp: cq.Workplane, c, rad, a1, a2) -> cq.Workplane:
    return wp.threePointArc(_pt(c, rad, (a1 + a2) / 2), _pt(c, rad, a2))


def capacidade_nominal_litros(spec: ShellSpec) -> float:
    """Nominal capacity as in the hand sketch: (geometric - baffle displacement) / 1.025."""
    return (capacidade_litros(spec) - spec.baffle_count * spec.baffle_volume_l) / spec.capacity_factor


def straight_length_for_capacity(nominal_l: float, di: float, head_l: float = 1200.0, baffles: int = 3,
                                 baffle_l: float = 41.0, factor: float = 1.025) -> float:
    """Hand-sketch formula: L = (C*1.025 - 2*head + n*baffle) / (litros por metro of the section), in mm."""
    area_l_per_m = pi * (di / 2) ** 2 / 1e6
    return (nominal_l * factor - 2 * head_l + baffles * baffle_l) / area_l_per_m


def _head_shell_profile(spec: ShellSpec) -> cq.Workplane:
    """Front head as a thin shell, profile in (x, radius): outer apex -> tangent line -> inner apex."""
    g, t = head_geometry(spec), spec.head_thickness
    C, K, th = g["crown_c"], g["knuckle_c"], g["theta"]
    R, r, ri, h = spec.crown_radius, spec.knuckle_radius, spec.ri, spec.head_depth_inner
    wp = cq.Workplane("XY").moveTo(-h - t, 0)
    wp = _arc(wp, C, R + t, 180, th)
    wp = _arc(wp, K, r + t, th, 90)
    wp = wp.lineTo(0, ri)
    wp = _arc(wp, K, r, 90, th)
    wp = _arc(wp, C, R, th, 180)
    return wp.close()


def _revolve(wp: cq.Workplane) -> cq.Workplane:
    return wp.revolve(360, (0, 0, 0), (1, 0, 0))


def build_parts(spec: ShellSpec) -> dict[str, cq.Workplane]:
    """Three parts: casco (cylinder ring), calota_dianteira, calota_traseira."""
    spec.check()
    L = spec.straight_length
    casco = cq.Workplane("YZ").circle(spec.ri + spec.shell_thickness).circle(spec.ri).extrude(L)
    front = _revolve(_head_shell_profile(spec))
    rear = front.mirror("YZ").translate((L, 0, 0))
    return {"casco": casco, "calota_dianteira": front, "calota_traseira": rear}


def cavity(spec: ShellSpec) -> cq.Workplane:
    """Inner volume (fluid) as one solid, from the inner surfaces only."""
    spec.check()
    g, R, r, ri, h, L = head_geometry(spec), spec.crown_radius, spec.knuckle_radius, spec.ri, spec.head_depth_inner, spec.straight_length
    C, K, th = g["crown_c"], g["knuckle_c"], g["theta"]
    mir = lambda p: (L - p[0], p[1])  # noqa: E731
    wp = cq.Workplane("XY").moveTo(-h, 0)
    wp = _arc(wp, C, R, 180, th)
    wp = _arc(wp, K, r, th, 90)
    wp = wp.lineTo(L, ri)
    wp = wp.threePointArc(mir(_pt(K, r, (th + 90) / 2)), mir(_pt(K, r, th)))
    wp = wp.threePointArc(mir(_pt(C, R, (180 + th) / 2)), (L + h, 0))
    return _revolve(wp.close())


def mesh_volume_litros(wp: cq.Workplane) -> float:
    verts, tris = wp.val().tessellate(0.01, 0.05)
    return abs(sum(verts[i].dot(verts[j].cross(verts[k])) for i, j, k in tris)) / 6 / 1e6


def export_step(spec: ShellSpec, path: str) -> None:
    parts = build_parts(spec)
    comp = cq.Compound.makeCompound([p.val() for p in parts.values()])
    cq.exporters.export(cq.Workplane("XY").add(comp), path)


def export_dxf_mesh(spec: ShellSpec, path: str, tolerance: float = 1.0) -> None:
    """3D DXF (R2000) with 3DFACE triangles per part (layers CASCO, CALOTA_DIANTEIRA, CALOTA_TRASEIRA).

    Workaround: AutoCAD for Mac does not import STEP. 3DFACE is the most widely supported 3D entity
    (R12 and later). Faces are triangles, not B-rep solids.
    """
    import ezdxf

    doc = ezdxf.new("R2000")
    msp = doc.modelspace()
    for name, wp in build_parts(spec).items():
        doc.layers.add(name.upper())
        verts, tris = wp.val().tessellate(tolerance, 0.1)
        for i, j, k in tris:
            msp.add_3dface([verts[i].toTuple(), verts[j].toTuple(), verts[k].toTuple(), verts[k].toTuple()],
                           dxfattribs={"layer": name.upper()})
    doc.saveas(path)


if __name__ == "__main__":
    s = ShellSpec()
    export_step(s, "out/tank_shell.step")
    export_dxf_mesh(s, "out/tank_shell_3d.dxf")
    print(f"capacidade {capacidade_litros(s):.0f} L, {litros_por_cm(s):.2f} L/cm, "
          f"calota interna {s.head_depth_inner:.1f} mm, comprimento total {s.overall_length:.1f} mm")
