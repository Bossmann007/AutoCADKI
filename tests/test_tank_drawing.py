import pytest
from ezdxf import recover

from src.axle_load import AxleSpec, axle_positions
from src.tank_drawing import build_drawing
from src.tank_shell import ShellSpec

S, A = ShellSpec(), AxleSpec()


@pytest.fixture(scope="module")
def doc(tmp_path_factory):
    path = tmp_path_factory.mktemp("dxf") / "t.dxf"
    build_drawing(S, A).saveas(path)
    d, auditor = recover.readfile(path)
    assert not auditor.has_errors
    return d


def test_dimension_values_match_spec(doc):
    pos = axle_positions(A, S)
    expected = [S.head_depth_outer, S.straight_length, S.head_depth_outer, pos["kingpin_to_axle1"],
                *A.spacings_mm, S.overall_length, S.inner_diameter, S.inner_diameter]
    vals = sorted(round(e.get_measurement()) for e in doc.modelspace().query("DIMENSION"))
    assert vals == sorted(round(v) for v in expected)


def test_every_dimension_has_rendered_block(doc):
    for e in doc.modelspace().query("DIMENSION"):
        assert e.dxf.geometry in doc.blocks


def test_layers_and_version(doc):
    assert doc.dxfversion == "AC1032"
    assert {"OUTLINE", "HIDDEN", "CENTER", "DIM", "TEXT", "SUSPENSION"} <= {l.dxf.name for l in doc.layers}


def test_head_arcs_present_and_nested(doc):
    arcs = list(doc.modelspace().query("ARC"))
    assert len(arcs) == 16  # 2 arcs x (top, bottom) x (front, rear) x (outer, inner)
    outer = max(a.dxf.radius for a in arcs if a.dxf.layer == "OUTLINE")
    inner = max(a.dxf.radius for a in arcs if a.dxf.layer == "HIDDEN")
    assert outer - inner == pytest.approx(S.head_thickness)
