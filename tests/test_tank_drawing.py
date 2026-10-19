import pytest
from ezdxf import recover

from src.tank_drawing import build_drawing
from src.tank_shell import ShellSpec

S = ShellSpec()


@pytest.fixture(scope="module")
def doc(tmp_path_factory):
    path = tmp_path_factory.mktemp("dxf") / "t.dxf"
    build_drawing(S).saveas(path)
    d, auditor = recover.readfile(path)
    assert not auditor.has_errors
    return d


def test_dimension_values_match_spec(doc):
    vals = sorted(round(e.get_measurement()) for e in doc.modelspace().query("DIMENSION"))
    expected = sorted(round(v) for v in (S.head_depth, S.length, S.head_depth,
                                          S.length + 2 * S.head_depth, S.height, S.width))
    assert vals == expected


def test_every_dimension_has_rendered_block(doc):
    for e in doc.modelspace().query("DIMENSION"):
        assert e.dxf.geometry in doc.blocks


def test_layers_and_version(doc):
    assert doc.dxfversion == "AC1032"
    assert {"OUTLINE", "HIDDEN", "CENTER", "DIM", "TEXT"} <= {l.dxf.name for l in doc.layers}


def test_hidden_wall_is_inside_outline(doc):
    def widest(layer):
        return max(e.dxf.major_axis.magnitude for e in doc.modelspace().query("ELLIPSE") if e.dxf.layer == layer)

    assert widest("HIDDEN") == pytest.approx(widest("OUTLINE") - S.thickness)
