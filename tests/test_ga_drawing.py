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
    for v in (700 - 0, 5250, 2450, 1250, 1500, 12400, 2290, SHELL.head_depth_outer, SHELL.overall_length):
        if v == 700:
            continue  # 700 is the distance from the front apex to the kingpin: asserted below
        assert round(v) in vals, v
    assert round(pos["kingpin_x"] + SHELL.head_depth_outer) == 700
    assert 700 in vals


def test_layers_and_tables(doc):
    names = {l.dxf.name for l in doc.layers}
    assert {"ANEIS", "QUEBRA_ONDAS", "CHASSI", "RODAS", "TABELA", "MOLDURA"} <= names
    texts = " ".join(t.dxf.text for t in doc.modelspace().query("TEXT"))
    for needle in ("DIN 7168", "REACAO NO SOLO", "INOX", "QUEBRA-ONDAS"):
        assert needle in texts


def test_wheel_circles(doc):
    wheels = [c for c in doc.modelspace().query("CIRCLE") if c.dxf.layer == "RODAS" and abs(c.dxf.radius - 552.5) < 1e-6]
    assert len(wheels) == 4
