import pytest
from ezdxf import recover

from src.axle_load import AxleSpec, axle_positions
from src.tank_shell import ShellSpec
from src.trailer_3d import build_trailer, export_dxf

S, A = ShellSpec(), AxleSpec()


@pytest.fixture(scope="module")
def groups():
    return build_trailer(S, A)


def test_all_solids_valid(groups):
    for layer, parts in groups.items():
        for wp in parts:
            assert wp.val().isValid(), layer


def test_counts(groups):
    assert len(groups["TANQUE"]) == 3
    assert len(groups["QUEBRA_ONDAS"]) == 3
    assert len(groups["ANEIS"]) == 9
    assert len(groups["PARALAMAS"]) == 8
    assert len(groups["EIXOS"]) == 4
    assert len(groups["RODAS"]) == 4 * 2 * 2 * 2  # 4 axles x 2 sides x dual x (tyre + rim)
    assert len(groups["PINO_REI"]) == 1


def test_envelope_within_contran(groups):
    zmax = max(wp.val().BoundingBox().zmax for p in groups.values() for wp in p)
    ymax = max(wp.val().BoundingBox().ymax for p in groups.values() for wp in p)
    zmin = min(wp.val().BoundingBox().zmin for p in groups.values() for wp in p)
    assert zmin == pytest.approx(0.0, abs=1e-6)       # tyres on the ground
    assert zmax <= 4400                                # CONTRAN 882 max height
    assert 2 * ymax <= 2600                            # CONTRAN 882 max width


def test_wheels_centred_on_axle_positions(groups):
    xs = sorted({round(wp.val().Center().x) for wp in groups["EIXOS"]})
    assert xs == [round(x) for x in axle_positions(A, S)["axle_x"]]


def test_dxf_has_hidden_smooth_edges_and_layers(groups, tmp_path):
    path = tmp_path / "t.dxf"
    n = export_dxf(groups, path)
    doc, aud = recover.readfile(path)
    assert not aud.has_errors
    faces = list(doc.modelspace().query("3DFACE"))
    assert len(faces) == n
    assert {f.dxf.layer for f in faces} == set(groups)
    hidden = sum(bin(f.dxf.invisible_edges).count("1") for f in faces)
    assert hidden > len(faces)          # most interior edges hidden
