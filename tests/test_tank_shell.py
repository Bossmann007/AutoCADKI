import pytest

from src.tank_shell import (ShellSpec, build_parts, capacidade_litros, cavity, head_geometry,
                            litros_por_cm, mesh_volume_litros)

S = ShellSpec()


def test_parts_are_valid_single_solids():
    for name, wp in build_parts(S).items():
        assert wp.val().isValid(), name
        assert len(wp.solids().vals()) == 1, name


def test_cavity_volume_matches_numeric_capacity():
    assert mesh_volume_litros(cavity(S)) == pytest.approx(capacidade_litros(S), rel=2e-3)


def test_litros_por_cm_is_cross_section_area():
    # pi * 1095^2 mm^2 * 10 mm = 37.66 L
    assert litros_por_cm(S) == pytest.approx(37.66, rel=1e-3)
    assert litros_por_cm(S) * S.straight_length / 10 < capacidade_litros(S)


def test_torispherical_head_depth():
    # R = Di, r = 0.1 Di, Di = 2190 -> inner depth 424.4 mm (hand calc)
    assert S.head_depth_inner == pytest.approx(424.4, abs=0.1)
    g = head_geometry(S)
    assert g["knuckle_c"][0] == pytest.approx(0.0)  # knuckle centre sits on the tangent line


def test_bbox_and_thicknesses():
    parts = build_parts(S)
    bb = parts["casco"].val().BoundingBox()
    assert bb.ylen == pytest.approx(S.inner_diameter + 2 * S.shell_thickness, rel=1e-4)
    assert bb.xlen == pytest.approx(S.straight_length, rel=1e-4)
    front = parts["calota_dianteira"].val().BoundingBox()
    assert front.xmin == pytest.approx(-S.head_depth_outer, abs=0.05)  # apex outer = inner depth + 4 mm
    rear = parts["calota_traseira"].val().BoundingBox()
    assert rear.xmax == pytest.approx(S.straight_length + S.head_depth_outer, abs=0.05)


def test_shell_material_volume_matches_thickness():
    # casco ring volume = pi*(Ro^2 - Ri^2)*L, 3 mm wall
    ro, ri = S.ri + 3, S.ri
    expected = 3.141592653589793 * (ro**2 - ri**2) * S.straight_length / 1e6
    assert mesh_volume_litros(build_parts(S)["casco"]) == pytest.approx(expected, rel=2e-3)


@pytest.mark.parametrize("kw", [{"inner_diameter": 2600}, {"shell_thickness": 0}, {"straight_length": -1},
                                {"knuckle_factor": 0.9}])
def test_invalid_specs_rejected(kw):
    with pytest.raises(ValueError):
        build_parts(ShellSpec(**kw))
