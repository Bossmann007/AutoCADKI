"""General-arrangement drawing (DXF R2018, A1 sheet at 1:50, model units mm) of the tank trailer.

Side view (tank, outer rings, baffles, chassis, kingpin, suspension, wheels, mudguards, landing legs), rear view,
dimensions, reaction table, capacity formula, DIN 7168 tolerance table and title block, in the style of the owner's photos.
TEST drawing: every number comes from src/presets.py (owner documents) and is to be replaced by the engineer.
"""
from math import pi

import ezdxf

from src.axle_load import AxleSpec, axle_positions
from src.presets import DEFAULT, get
from src.tank_drawing import _all_arcs
from src.tank_shell import ShellSpec, capacidade_litros, capacidade_nominal_litros, straight_length_for_capacity
from src.trailer_3d import GearSpec

SCALE = 50
SHEET_W, SHEET_H = 841 * SCALE, 594 * SCALE
OX, G = 5000.0, 15500.0          # sheet position of tank x=0 and of the ground line
TXT, TXT_BIG = 140, 210          # text heights (mm in model) = 2.8 / 4.2 mm on paper at 1:50
DIM = "GA"

LAYERS = (("OUTLINE", 7, "CONTINUOUS"), ("HIDDEN", 8, "DASHED"), ("CENTER", 1, "CENTER"), ("DIM", 3, "CONTINUOUS"),
          ("TEXT", 7, "CONTINUOUS"), ("ANEIS", 30, "CONTINUOUS"), ("QUEBRA_ONDAS", 1, "DASHED"),
          ("CHASSI", 94, "CONTINUOUS"), ("RODAS", 250, "CONTINUOUS"), ("SUSPENSAO", 8, "CONTINUOUS"),
          ("PINO_REI", 1, "CONTINUOUS"), ("MOLDURA", 7, "CONTINUOUS"), ("TABELA", 7, "CONTINUOUS"), ("JUNCAO", 6, "CENTER"))


def _setup(doc):
    for name, color, lt in LAYERS:
        doc.layers.add(name, color=color, linetype=lt)
    doc.dimstyles.new(DIM, dxfattribs={"dimtxt": TXT, "dimasz": 100, "dimexe": 50, "dimexo": 40, "dimgap": 30,
                                       "dimtad": 1, "dimdec": 0, "dimlunit": 2})
    doc.header["$LTSCALE"] = 250


class Sheet:
    def __init__(self, msp):
        self.msp = msp

    def line(self, p, q, layer="OUTLINE"):
        self.msp.add_line(p, q, dxfattribs={"layer": layer})

    def rect(self, x0, y0, x1, y1, layer="OUTLINE"):
        self.msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True, dxfattribs={"layer": layer})

    def circle(self, c, r, layer="OUTLINE"):
        self.msp.add_circle(c, r, dxfattribs={"layer": layer})

    def arc(self, c, r, a1, a2, layer="OUTLINE"):
        self.msp.add_arc(c, r, a1 % 360, a2 % 360, dxfattribs={"layer": layer})

    def text(self, s, p, h=TXT, layer="TEXT", rotation=0):
        self.msp.add_text(s, height=h, dxfattribs={"layer": layer, "insert": p, "rotation": rotation})

    def dim(self, p1, p2, base, angle=0):
        self.msp.add_linear_dim(base=base, p1=p1, p2=p2, angle=angle, dimstyle=DIM,
                                dxfattribs={"layer": "DIM"}).render()

    def table(self, x, y, widths, row_h, rows, header_rows=1, h=TXT):
        """Grid with top-left corner (x, y), rows going down."""
        total_w = sum(widths)
        for i in range(len(rows) + 1):
            self.line((x, y - i * row_h), (x + total_w, y - i * row_h), "TABELA")
        cx = x
        for w in [0] + list(widths):
            cx += w
            self.line((cx, y), (cx, y - len(rows) * row_h), "TABELA")
        for i, row in enumerate(rows):
            cx = x
            for w, cell in zip(widths, row):
                self.text(str(cell), (cx + 60, y - (i + 1) * row_h + (row_h - h) / 2), h)
                cx += w


def build_ga(shell: ShellSpec, axles: AxleSpec, gear: GearSpec = GearSpec(), name: str = DEFAULT) -> ezdxf.document.Drawing:
    shell.check()
    pos = axle_positions(axles, shell)
    doc = ezdxf.new("R2018", setup=True)
    _setup(doc)
    s = Sheet(doc.modelspace())
    ri, ro, L = shell.ri, shell.ri + shell.shell_thickness, shell.straight_length
    ho, kp, axle_x = shell.head_depth_outer, pos["kingpin_x"], pos["axle_x"]
    zc = gear.rail_top_z + ro + 3
    zax = gear.tire_radius
    X = lambda x: OX + x            # noqa: E731
    Y = lambda z: G + z             # noqa: E731
    x_front, x_rear = kp - 300.0, axle_x[-1] + axles.chassis_rear_overhang_mm
    rz0 = gear.rail_top_z - gear.rail_height

    # --- sheet frame
    s.rect(0, 0, SHEET_W, SHEET_H, "MOLDURA")
    s.rect(1000, 500, SHEET_W - 500, SHEET_H - 500, "MOLDURA")

    # --- ground and tank side view
    s.line((OX - 2500, G), (X(L + ho + 2500), G), "OUTLINE")
    for yy in (zc + ro, zc - ro):
        s.line((X(0), Y(yy)), (X(L), Y(yy)))
    for yy in (zc + ri, zc - ri):
        s.line((X(0), Y(yy)), (X(L), Y(yy)), "HIDDEN")
    for (c, rad, a1, a2) in _all_arcs(shell, shell.head_thickness):
        s.arc((X(c[0]), Y(zc + c[1])), rad, a1, a2)
    for (c, rad, a1, a2) in _all_arcs(shell, 0.0):
        s.arc((X(c[0]), Y(zc + c[1])), rad, a1, a2, "HIDDEN")
    s.line((X(-ho - 300), Y(zc)), (X(L + ho + 300), Y(zc)), "CENTER")
    for i in range(gear.ring_count):                                     # outer rings
        x = 600 + i * (L - 1200) / (gear.ring_count - 1)
        s.rect(X(x - 30), Y(zc - ro - 6), X(x + 30), Y(zc + ro + 6), "ANEIS")
    for x in (axle_x[0], (axle_x[1] + axle_x[2]) / 2, axle_x[3]):        # baffles (inside, dashed)
        s.line((X(x), Y(zc - ri)), (X(x), Y(zc + ri)), "QUEBRA_ONDAS")
    for xj, side in ((0, "DIANTEIRA"), (L, "TRASEIRA")):                 # cylinder/head junction, both ends
        s.line((X(xj), G - 600), (X(xj), Y(zc + ro + 350)), "JUNCAO")
        s.text(f"JUNCAO CORPO CILINDRICO / TAMPO {side}", (X(xj) + 90, Y(zc + ro + 380)), TXT, "JUNCAO", rotation=90)
    s.text(f"#{shell.shell_thickness:g} mm INOX", (X(L * 0.62), Y(zc + 500)), TXT_BIG)
    s.text(f"{round(capacidade_nominal_litros(shell), -2):.0f} L", (X(L * 0.45), Y(zc - 150)), TXT_BIG)
    s.text("QUEBRA-ONDAS (3) - POSICOES A DEFINIR", (X(axle_x[0] - 1200), Y(zc + ri + 150)), TXT, "QUEBRA_ONDAS")

    # --- chassis, kingpin, landing legs, bumper
    s.rect(X(x_front), Y(rz0), X(x_rear), Y(gear.rail_top_z), "CHASSI")
    s.rect(X(kp - 450), Y(gear.rail_top_z - 70), X(kp + 450), Y(gear.rail_top_z - 20), "CHASSI")
    s.rect(X(kp - 25.4), Y(gear.rail_top_z - 170), X(kp + 25.4), Y(gear.rail_top_z - 70), "PINO_REI")
    lx = kp + 1200
    s.rect(X(lx - 70), Y(380), X(lx + 70), Y(rz0), "CHASSI")
    s.rect(X(lx - 200), Y(360), X(lx + 200), Y(380), "CHASSI")
    s.rect(X(x_rear), Y(500), X(x_rear + 80), Y(1100), "CHASSI")                      # rear bumper bar

    # --- axles, suspension, wheels, mudguards
    for i, x in enumerate(axle_x, 1):
        s.rect(X(x - 500), Y(zax + 100), X(x + 500), Y(zax + 200), "SUSPENSAO")
        for dx in (-450, 450):
            s.rect(X(x + dx - 60), Y(zax + 200), X(x + dx + 60), Y(rz0), "SUSPENSAO")
        s.circle((X(x), Y(zax)), gear.tire_radius, "RODAS")
        s.circle((X(x), Y(zax)), 285, "RODAS")
        s.circle((X(x), Y(zax)), 70, "RODAS")
        s.arc((X(x), Y(zax)), gear.tire_radius + 45, 15, 165, "CHASSI")
        s.line((X(x), Y(0) - 300), (X(x), Y(zax + 700)), "CENTER")
        s.text(f"E{i}", (X(x) + 80, Y(zax + 760)), TXT, "TEXT")
    s.text("PINO REI", (X(kp) + 80, Y(gear.rail_top_z + 100)), TXT)
    s.line((X(kp), Y(rz0 - 300)), (X(kp), Y(gear.rail_top_z + 100)), "CENTER")

    # --- dimensions (side view)
    dy1, dy2, dy3 = G - 900, G - 1500, G - 2100
    xs = [0, kp] + axle_x + [L]           # chain from the front junction to the rear junction
    for p, q in zip(xs, xs[1:]):
        s.dim((X(p), G), (X(q), G), (0, dy1))
    s.dim((X(-ho), G), (X(0), G), (0, dy2))
    s.dim((X(0), G), (X(L), G), (0, dy2))
    s.dim((X(L), G), (X(L + ho), G), (0, dy2))
    s.dim((X(-ho), G), (X(L + ho), G), (0, dy3))
    s.dim((X(L + ho + 900), Y(zc - ri)), (X(L + ho + 900), Y(zc + ri)), (X(L + ho + 1300), 0), angle=90)
    s.dim((X(-ho - 900), G), (X(-ho - 900), Y(gear.rail_top_z)), (X(-ho - 1500), 0), angle=90)
    s.dim((X(-ho - 900), G), (X(-ho - 900), Y(zc + ro)), (X(-ho - 2200), 0), angle=90)

    # --- rear view
    rx = 30000.0
    s.line((rx - 2000, G), (rx + 2000, G))
    s.circle((rx, Y(zc)), ro)
    s.circle((rx, Y(zc)), ri, "HIDDEN")
    s.circle((rx, Y(zc)), ro + gear.ring_thickness, "ANEIS")
    s.line((rx - ro - 200, Y(zc)), (rx + ro + 200, Y(zc)), "CENTER")
    s.line((rx, Y(zc) - ro - 200), (rx, Y(zc) + ro + 200), "CENTER")
    for sgn in (-1, 1):
        s.rect(rx + sgn * gear.rail_spacing / 2 - gear.rail_width / 2, Y(rz0),
               rx + sgn * gear.rail_spacing / 2 + gear.rail_width / 2, Y(gear.rail_top_z), "CHASSI")
        for d in (-1, 1):
            yc = sgn * gear.track / 2 + d * (gear.tire_width + gear.dual_gap) / 2
            s.rect(rx + yc - gear.tire_width / 2, G, rx + yc + gear.tire_width / 2, G + 2 * gear.tire_radius, "RODAS")
    s.dim((rx - ro, Y(zc)), (rx + ro, Y(zc)), (0, Y(zc + ro) + 500))
    s.dim((rx - gear.track / 2, G), (rx + gear.track / 2, G), (0, G - 900))
    half_w = gear.track / 2 + gear.tire_width + gear.dual_gap / 2
    s.dim((rx - half_w, G), (rx + half_w, G), (0, G - 1500))
    s.text("VISTA TRASEIRA", (rx - 700, G - 2500), TXT_BIG)
    s.text("VISTA LATERAL  (ESC. 1:50)", (X(0), G - 2900), TXT_BIG)

    # --- reaction table (ground reactions, tonnes) and capacity calculation
    pr, e1 = axles.kingpin_load_kg / 1000, axles.axle_loads_kg[0] / 1000
    e234 = sum(axles.axle_loads_kg[1:]) / 1000
    d_e234 = pos["kingpin_to_axle1"] + axles.spacings_mm[0] + axles.spacings_mm[1]
    s.text("ESPECIFICACAO TECNICA", (1500, 9400), TXT_BIG)
    s.text(f"ESTUDO DE APLICACAO DE TANQUE {round(capacidade_nominal_litros(shell), -2):.0f} L EM CHASSI 4E",
           (1500, 9000), TXT)
    s.table(1500, 8600, (1400, 2600, 2000), 450, [
        ("", "REACAO NO SOLO (TON)", "DIST (mm)"),
        ("PR", f"{pr:.2f}", "0"),
        ("CG", f"{axles.total_kg / 1000:.2f}", f"{pos['cg_from_kingpin']:.0f}"),
        ("E1", f"{e1:.2f}", f"{pos['kingpin_to_axle1']:.0f}"),
        ("E234", f"{e234:.2f}", f"{d_e234:.0f}"),
    ])
    s.text("Distancias a partir do pino rei. Reacao no chassi: nao informada.", (1500, 6200), TXT)
    s.text("Distribuicao por eixo ASSUMIDA (E1 = 10 t). CG calculado.", (1500, 5900), TXT)
    Lc = straight_length_for_capacity(capacidade_nominal_litros(shell), shell.inner_diameter, 1200.0,
                                      shell.baffle_count, shell.baffle_volume_l, shell.capacity_factor)
    area = pi * shell.ri ** 2 / 1e6
    s.text("CALCULO DO COMPRIMENTO DA PARTE RETA", (1500, 5300), TXT_BIG)
    s.text(f"L = ({capacidade_nominal_litros(shell):.0f} x {shell.capacity_factor:g} - 2 x 1200 + "
           f"{shell.baffle_count} x {shell.baffle_volume_l:g}) / {area:.3f} = {Lc:.0f} mm", (1500, 4900), TXT)
    s.text(f"Adotado: {L:.0f} mm.  Di {shell.inner_diameter:g}; costado {shell.shell_thickness:g} mm INOX; "
           f"calotas {shell.head_thickness:g} mm toriesfericas 'ASME 10' (R=Di, r=0,1 Di, ASSUMIDO).", (1500, 4500), TXT)
    s.text(f"Capacidade geometrica {capacidade_litros(shell):,.0f} L; fator {shell.capacity_factor:g}; "
           f"{shell.baffle_count} quebra-ondas x {shell.baffle_volume_l:g} L.".replace(",", ""), (1500, 4100), TXT)
    s.text("TANQUE DE TESTE - VALORES PARA REVISAO DA ENGENHARIA (nao e projeto aprovado).", (1500, 3300), TXT, "TEXT")

    # --- tolerance table (DIN 7168, from the reference documents) top right
    tx, ty = SHEET_W - 500 - 11500, SHEET_H - 500 - 400
    s.text("TOLERANCIAS QUANDO NAO ESPECIFICADAS SAO CONFORME DIN 7168", (tx, ty + 150), TXT)
    s.table(tx, ty, (1500,) + (1428,) * 7, 450, [
        ("FINO", "0-6", "6-30", "30-120", "120-400", "400-1000", "1000-2000", "2000-4000"),
        ("", "+-0,05", "+-0,1", "+-0,15", "+-0,2", "+-0,3", "+-0,5", "+-0,8"),
    ])

    # --- title block bottom right
    bx, by = SHEET_W - 500 - 12000, 500
    s.rect(bx, by, bx + 12000, by + 4400, "TABELA")
    s.text(f"TANQUE {round(capacidade_nominal_litros(shell), -2):.0f} L RODOVIARIO EM CHASSI 4E",
           (bx + 300, by + 3500), TXT_BIG)
    s.text("PROJETO TESTE - GERADO POR IA (AutoCADKI) - REVISAO DE ENGENHARIA PENDENTE", (bx + 300, by + 3100), TXT)
    s.table(bx, by + 2700, (2400, 2400, 2400, 2400, 2400), 450, [
        ("PROJETADO", "DESENHADO", "APROVADO", "VISTO", "DATA"),
        ("", "AutoCADKI", "", "", "2026-10-10"),
    ])
    s.table(bx, by + 1500, (4000, 4000, 4000), 450, [
        ("ESCALA", "UNIDADES", "FOLHA"),
        ("1:50", "mm", "A1   1/1"),
    ])
    s.text(f"CODIGO: TESTE-{name.upper()}   REV. 0   ANTE-PROJETO", (bx + 300, by + 300), TXT)
    return doc


if __name__ == "__main__":
    import sys

    n = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    build_ga(*get(n), name=n).saveas(f"out/ga_{n}.dxf")
    print(f"wrote out/ga_{n}.dxf")
