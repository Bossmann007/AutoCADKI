import pytest
from ezdxf import recover

from src.axle_load import axle_positions
from src.ga_drawing import build_ga
from src.presets import get

SHELL, AXLES = get("52k")


@pytest.fixture(scope="module")
def doc(tmp_path_factory):
    path = tmp_path_factory.mktemp("ga") / "ga.dxf"
    build_ga(SHELL, AXLES).saveas(path)
    d, aud = recover.readfile(path)
    assert not aud.has_errors
    return d


def test_expected_dimensions_present(doc):
    pos = axle_positions(AXLES, SHELL)
    vals = {round(e.get_measurement()) for e in doc.modelspace().query("DIMENSION")}
    for v in (700, 2500, 5250, 2450, 1250, 1500, 12400, 2290, SHELL.head_depth_outer, SHELL.overall_length):
        assert round(v) in vals, v
    assert pos["kingpin_x"] == 700  # junction -> kingpin


def test_layers_and_tables(doc):
    names = {l.dxf.name for l in doc.layers}
    assert {"ANEIS", "QUEBRA_ONDAS", "CHASSI", "RODAS", "TABELA", "MOLDURA"} <= names
    texts = " ".join(t.dxf.text for t in doc.modelspace().query("TEXT"))
    for needle in ("DIN 7168", "REACAO NO SOLO", "INOX", "QUEBRA-ONDAS"):
        assert needle in texts


def test_junction_lines_on_both_sides(doc):
    xs = sorted(round(l.dxf.start.x) for l in doc.modelspace().query("LINE") if l.dxf.layer == "JUNCAO")
    assert xs == [5000, 5000 + 12400]   # OX + 0 and OX + straight length


def test_last_axle_to_rear_junction_is_1500(doc):
    pos = axle_positions(AXLES, SHELL)
    assert SHELL.straight_length - pos["axle_x"][-1] == 1500


def test_baffle_lines_and_position_dimensions(doc):
    xs = sorted(round(l.dxf.start.x - 5000) for l in doc.modelspace().query("LINE")
                if l.dxf.layer == "QUEBRA_ONDAS")
    assert xs == [2060, 4040, 5950]
    vals = {round(e.get_measurement()) for e in doc.modelspace().query("DIMENSION")}
    assert {2060, 1980, 1910} <= vals


def test_weld_seams_and_plate_dimensions(doc):
    xs = sorted(round(l.dxf.start.x - 5000) for l in doc.modelspace().query("LINE") if l.dxf.layer == "SOLDA")
    assert xs == [1200 * i for i in range(1, 11)]
    vals = [round(e.get_measurement()) for e in doc.modelspace().query("DIMENSION")]
    assert vals.count(1200) >= 10 and 400 in vals


def test_wheel_circles(doc):
    wheels = [c for c in doc.modelspace().query("CIRCLE") if c.dxf.layer == "RODAS" and abs(c.dxf.radius - 552.5) < 1e-6]
    assert len(wheels) == 4
