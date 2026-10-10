import pytest

from src.tank_shell import ShellSpec, build_shell, capacidade_litros, cavity, litros_por_cm, mesh_volume_litros

S = ShellSpec()


def test_shell_is_one_valid_solid():
    shell = build_shell(S)
    assert shell.val().isValid()
    assert len(shell.solids().vals()) == 1


def test_cavity_volume_matches_analytic_capacity():
    assert mesh_volume_litros(cavity(S)) == pytest.approx(capacidade_litros(S), rel=5e-3)


def test_bbox_matches_spec():
    bb = build_shell(S).val().BoundingBox()
    assert bb.ylen == pytest.approx(S.width, rel=1e-3)
    assert bb.zlen == pytest.approx(S.height, rel=1e-3)
    assert bb.xlen == pytest.approx(S.length + 2 * S.head_depth, rel=1e-3)


def test_litros_por_cm_consistent_with_cylinder():
    assert litros_por_cm(S) * S.length / 10 < capacidade_litros(S)


@pytest.mark.parametrize("kw", [{"width": 2700}, {"thickness": 0}, {"thickness": 800}, {"length": -1}])
def test_invalid_specs_rejected(kw):
    with pytest.raises(ValueError):
        build_shell(ShellSpec(**kw))
