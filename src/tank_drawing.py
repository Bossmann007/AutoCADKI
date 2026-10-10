"""2D drawing (DXF R2018) of the tank: side view (outer, hidden inner wall, kingpin, axles) + end view, dimensioned.

Units mm, model space 1:1. Dimensions come from the same ShellSpec/AxleSpec as the 3D model.
Placeholder drawing for engineer review: no ABNT title block, no weld symbols, baffles not yet placed.
"""
import ezdxf

from src.axle_load import AxleSpec, axle_positions
from src.tank_shell import ShellSpec, capacidade_litros, head_geometry, litros_por_cm

DIMSTYLE = "TANK"


def _setup(doc):
    for name, color, lt in (("OUTLINE", 7, "CONTINUOUS"), ("HIDDEN", 8, "DASHED"),
                            ("CENTER", 1, "CENTER"), ("DIM", 3, "CONTINUOUS"), ("TEXT", 7, "CONTINUOUS"),
                            ("SUSPENSION", 5, "CONTINUOUS")):
        doc.layers.add(name, color=color, linetype=lt)
    doc.dimstyles.new(DIMSTYLE, dxfattribs={
        "dimtxt": 90, "dimasz": 70, "dimexe": 40, "dimexo": 30, "dimgap": 25,
        "dimtad": 1, "dimdec": 0, "dimlunit": 2,
    })
    doc.header["$LTSCALE"] = 200


def _head_arcs(spec: ShellSpec, off: float):
    """Top half of the front head surface offset by `off`: (centre, radius, start, end) CCW degrees."""
    g = head_geometry(spec)
    R, r, th = spec.crown_radius, spec.knuckle_radius, g["theta"]
    return [(g["crown_c"], R + off, th, 180.0), (g["knuckle_c"], r + off, 90.0, th)]


def _all_arcs(spec: ShellSpec, off: float):
    """Four arcs per head: front/rear x top/bottom."""
    L = spec.straight_length
    out = []
    for c, rad, a1, a2 in _head_arcs(spec, off):
        top = (c, rad, a1, a2)
        bot = ((c[0], -c[1]), rad, -a2, -a1)
        for (cc, rr, s, e) in (top, bot):
            out.append((cc, rr, s, e))                                   # front
            out.append(((L - cc[0], cc[1]), rr, 180 - e, 180 - s))       # rear (mirror in x)
    return out


def _add_arcs(msp, arcs, layer):
    for (c, rad, s, e) in arcs:
        msp.add_arc(center=c, radius=rad, start_angle=s % 360, end_angle=e % 360, dxfattribs={"layer": layer})


def build_drawing(spec: ShellSpec, axles: AxleSpec | None = None) -> ezdxf.document.Drawing:
    spec.check()
    axles = axles or AxleSpec()
    pos = axle_positions(axles, spec)
    doc = ezdxf.new("R2018", setup=True)
    _setup(doc)
    msp = doc.modelspace()
    ri, ro, L, ho = spec.ri, spec.ri + spec.shell_thickness, spec.straight_length, spec.head_depth_outer
    b = ro

    # side view: outer wall, hidden inner wall, centre line
    for y in (ro, -ro):
        msp.add_line((0, y), (L, y), dxfattribs={"layer": "OUTLINE"})
    for y in (ri, -ri):
        msp.add_line((0, y), (L, y), dxfattribs={"layer": "HIDDEN"})
    _add_arcs(msp, _all_arcs(spec, spec.head_thickness), "OUTLINE")
    _add_arcs(msp, _all_arcs(spec, 0.0), "HIDDEN")
    msp.add_line((-ho - 250, 0), (L + ho + 250, 0), dxfattribs={"layer": "CENTER"})

    # kingpin and axle centre lines
    kp = pos["kingpin_x"]
    msp.add_line((kp, -b - 150), (kp, b + 150), dxfattribs={"layer": "SUSPENSION"})
    msp.add_text("PINO REI", height=90, dxfattribs={"layer": "TEXT", "insert": (kp + 40, b + 170)})
    for i, x in enumerate(pos["axle_x"], 1):
        msp.add_line((x, -b - 150), (x, -b + 120), dxfattribs={"layer": "SUSPENSION"})
        msp.add_text(f"EIXO {i}", height=90, dxfattribs={"layer": "TEXT", "insert": (x + 40, -b - 150), "rotation": 90})

    # end view
    cx = L + ho + 400 + ro + 900
    for r_, lay in ((ro, "OUTLINE"), (ri, "HIDDEN")):
        msp.add_circle((cx, 0), r_, dxfattribs={"layer": lay})
    msp.add_line((cx - ro - 150, 0), (cx + ro + 150, 0), dxfattribs={"layer": "CENTER"})
    msp.add_line((cx, -ro - 150), (cx, ro + 150), dxfattribs={"layer": "CENTER"})

    def dim(p1, p2, base, angle=0):
        msp.add_linear_dim(base=base, p1=p1, p2=p2, angle=angle, dimstyle=DIMSTYLE,
                           dxfattribs={"layer": "DIM"}).render()

    row1, row2, row3 = (0, -b - 450), (0, -b - 800), (0, -b - 1150)
    dim((-ho, 0), (0, 0), row1)
    dim((0, 0), (L, 0), row1)
    dim((L, 0), (L + ho, 0), row1)
    xs = [kp] + pos["axle_x"]
    for p, q in zip(xs, xs[1:]):
        dim((p, 0), (q, 0), row2)
    dim((-ho, 0), (L + ho, 0), row3)
    dim((L / 2, -ri), (L / 2, ri), (L + ho + 450, 0), angle=90)
    dim((cx - ri, 0), (cx + ri, 0), (0, ro + 350))

    notes = (
        "TANQUE - PLACEHOLDER, REVISAO DE ENGENHARIA PENDENTE",
        f"Costado {spec.shell_thickness:g} mm, calotas {spec.head_thickness:g} mm (entradas, nao calculadas)",
        f"Calotas toriesfericas 'ASME 10' (ASSUMIDO: R={spec.crown_factor:g}xDi, r={spec.knuckle_factor:g}xDi)",
        f"Capacidade interna {capacidade_litros(spec):,.0f} L ({litros_por_cm(spec):.1f} L/cm)",
        f"Pino rei a {axles.kingpin_from_front_mm:g} mm da calota dianteira; cargas: pino {axles.kingpin_load_kg:g} kg, "
        f"eixos {', '.join(f'{w:g}' for w in axles.axle_loads_kg)} kg",
        "Posicao dos eixos: equilibrio de momentos com CG no centro geometrico (ASSUMIDO)",
        "Quebra-ondas: 3, posicoes a definir. Unidades: mm. Escala 1:1 no modelo.",
    )
    for i, line in enumerate(notes):
        msp.add_text(line, height=100, dxfattribs={"layer": "TEXT", "insert": (-ho, -b - 1500 - i * 190)})
    return doc


if __name__ == "__main__":
    build_drawing(ShellSpec()).saveas("out/tank_shell.dxf")
    print("wrote out/tank_shell.dxf")
