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
    assert len(groups["TANQUE"]) == 11 + 2          # 54k: 10 x 1200 + 888 plates + 2 heads
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


def test_52k_shell_plates_10x1200_plus_400():
    from src.presets import get

    shell, axles = get("52k")
    assert shell.plate_lengths == (1200.0,) * 10 + (400.0,)
    assert shell.plate_welds == tuple(1200.0 * i for i in range(1, 11))
    g = build_trailer(shell, axles)
    plates = g["TANQUE"][:-2]
    assert [round(wp.val().BoundingBox().xlen) for wp in plates] == [1200] * 10 + [400]
    assert round(plates[0].val().BoundingBox().xmin) == 0 and round(plates[-1].val().BoundingBox().xmax) == 12400


def test_52k_baffles_and_rings_follow_photo_positions():
    from src.presets import get

    shell, axles = get("52k")
    g = build_trailer(shell, axles)
    bx = sorted(round(wp.val().BoundingBox().xmax) for wp in g["QUEBRA_ONDAS"])   # edge of each dish
    assert bx == [3200, 6450, 9000]
    assert len(g["REFORCOS_U"]) == 3 and len(g["REFORCO_VERM"]) == 2
    assert sorted(round(wp.val().Center().x) for wp in g["ANEIS"]) == [round(x) for x in shell.ring_positions]
    pos = axle_positions(axles, shell)
    assert bx[0] == round(pos["kingpin_x"] + 2500)                    # QO1 over the landing leg
    assert bx[1] == round(pos["axle_x"][0] + 500) and bx[2] == round(pos["axle_x"][1] + 600)


def test_baffles_are_dished_convex_to_the_front_with_a_passage_opening():
    from src.presets import get
    from src.tank_shell import build_baffle

    shell, _ = get("52k")
    b = build_baffle(shell, 500.0)
    bb = b.val().BoundingBox()
    assert b.val().isValid() and len(b.solids().vals()) == 1
    assert bb.xmax == pytest.approx(0, abs=0.01) and bb.xmin < -300      # edge at x=0, apex toward the front (-x)
    assert bb.ylen == pytest.approx(shell.inner_diameter, abs=0.1)       # fits the shell
    # the opening: no material on the axis at the apex
    from OCP.BRepClass3d import BRepClass3d_SolidClassifier
    from OCP.gp import gp_Pnt
    from OCP.TopAbs import TopAbs_OUT
    c = BRepClass3d_SolidClassifier(b.val().wrapped, gp_Pnt(bb.xmin + 5, 0, 0), 1e-6)
    assert c.State() == TopAbs_OUT


def test_landing_legs_2500_from_kingpin(groups):
    kp = axle_positions(A, S)["kingpin_x"]
    legs = [wp for wp in groups["CHASSI"] if abs(wp.val().Center().x - (kp + 2500)) < 1e-6]
    assert len(legs) == 4          # 2 legs + 2 foot plates, left and right


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
    assert {f.dxf.layer for f in faces} == {k for k, v in groups.items() if v}   # empty groups write no faces
    hidden = sum(bin(f.dxf.invisible_edges).count("1") for f in faces)
    assert hidden > len(faces)          # most interior edges hidden
