"""2D drawing (DXF R2018) of the tank shell: side view with hidden inner wall + end view, dimensioned.

Units mm, model space 1:1. Dimensions come from the same ShellSpec as the 3D model.
Placeholder drawing for engineer review: no title block standard (ABNT) applied yet.
"""
from math import pi

import ezdxf

from src.tank_shell import ShellSpec, capacidade_litros

DIMSTYLE = "TANK"


def _setup(doc):
    for name, color, lt in (("OUTLINE", 7, "CONTINUOUS"), ("HIDDEN", 8, "DASHED"),
                            ("CENTER", 1, "CENTER"), ("DIM", 3, "CONTINUOUS"), ("TEXT", 7, "CONTINUOUS")):
        doc.layers.add(name, color=color, linetype=lt)
    doc.dimstyles.new(DIMSTYLE, dxfattribs={
        "dimtxt": 90, "dimasz": 70, "dimexe": 40, "dimexo": 30, "dimgap": 25,
        "dimtad": 1, "dimdec": 0, "dimlunit": 2,
    })
    doc.header["$LTSCALE"] = 200


def _side_profile(msp, a: float, b: float, h: float, length: float, layer: str):
    """Silhouette in XZ: top/bottom lines + two half-ellipse heads (centre on axis, vertical major axis b)."""
    at = {"layer": layer}
    msp.add_line((0, b), (length, b), dxfattribs=at)
    msp.add_line((0, -b), (length, -b), dxfattribs=at)
    msp.add_ellipse((0, 0), major_axis=(0, b), ratio=h / b, start_param=0, end_param=pi, dxfattribs=at)
    msp.add_ellipse((length, 0), major_axis=(0, b), ratio=h / b, start_param=pi, end_param=2 * pi, dxfattribs=at)


def build_drawing(spec: ShellSpec) -> ezdxf.document.Drawing:
    spec.check()
    doc = ezdxf.new("R2018", setup=True)
    _setup(doc)
    msp = doc.modelspace()
    a, b, h, L, t = spec.width / 2, spec.height / 2, spec.head_depth, spec.length, spec.thickness
    ia, ib, ih = spec.inner

    # side view
    _side_profile(msp, a, b, h, L, "OUTLINE")
    _side_profile(msp, ia, ib, ih, L, "HIDDEN")
    msp.add_line((-h - 250, 0), (L + h + 250, 0), dxfattribs={"layer": "CENTER"})

    # end view, to the right of the side view
    cx = L + h + 400 + a + 900
    msp.add_ellipse((cx, 0), major_axis=(a, 0), ratio=b / a, dxfattribs={"layer": "OUTLINE"})
    msp.add_ellipse((cx, 0), major_axis=(ia, 0), ratio=ib / ia, dxfattribs={"layer": "HIDDEN"})
    msp.add_line((cx - a - 150, 0), (cx + a + 150, 0), dxfattribs={"layer": "CENTER"})
    msp.add_line((cx, -b - 150), (cx, b + 150), dxfattribs={"layer": "CENTER"})

    def dim(p1, p2, base, angle=0):
        d = msp.add_linear_dim(base=base, p1=p1, p2=p2, angle=angle, dimstyle=DIMSTYLE, dxfattribs={"layer": "DIM"})
        d.render()

    row1, row2 = (0, -b - 300), (0, -b - 650)
    dim((-h, 0), (0, 0), row1)
    dim((0, 0), (L, 0), row1)
    dim((L, 0), (L + h, 0), row1)
    dim((-h, 0), (L + h, 0), row2)
    dim((L / 2, -b), (L / 2, b), (L + h + 450, 0), angle=90)
    dim((cx - a, 0), (cx + a, 0), (0, b + 350))

    for i, line in enumerate((
        "CASCO DE TANQUE - PLACEHOLDER, REVISAO DE ENGENHARIA PENDENTE",
        f"Espessura da parede: {t:g} mm (entrada, nao calculada)",
        f"Capacidade interna: {capacidade_litros(spec):,.0f} L",
        "Unidades: mm. Escala 1:1 no modelo.",
    )):
        msp.add_text(line, height=110, dxfattribs={"layer": "TEXT", "insert": (-h, -b - 1250 - i * 200)})
    return doc


if __name__ == "__main__":
    s = ShellSpec()
    d = build_drawing(s)
    d.saveas("out/tank_shell.dxf")
    print("wrote out/tank_shell.dxf")
