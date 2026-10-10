import pytest

from src.axle_load import AxleSpec, axle_positions
from src.tank_shell import ShellSpec

A, S = AxleSpec(), ShellSpec()


def test_totals():
    assert A.total_kg == pytest.approx(44700.0)
    assert sum(A.axle_loads_kg) == pytest.approx(31200.0)


def test_spacings_kept():
    r = axle_positions(A, S)
    gaps = [b - a for a, b in zip(r["axle_x"], r["axle_x"][1:])]
    assert gaps == pytest.approx(list(A.spacings_mm))
    assert r["kingpin_to_axle1"] == 5640.0


def test_reproduces_sketch_cg_and_axle_group_distance():
    r = axle_positions(A, S)
    assert r["cg_from_kingpin"] == pytest.approx(5640, abs=60)               # sketch: 5640 (+-50)
    assert r["group_resultant_from_kingpin"] == pytest.approx(8080, abs=100)  # sketch: 8080


def test_moment_balance_mode():
    solved = AxleSpec(kingpin_to_axle1_mm=None, cg_from_kingpin_mm=5640.0)
    r = axle_positions(solved, S)
    about_kp = sum(w * (x - r["kingpin_x"]) for w, x in zip(solved.axle_loads_kg, r["axle_x"]))
    assert about_kp == pytest.approx(solved.total_kg * 5640.0, rel=1e-9)
    assert axle_positions(AxleSpec(kingpin_to_axle1_mm=None, cg_from_kingpin_mm=5940.0), S)["kingpin_to_axle1"] > r["kingpin_to_axle1"]
