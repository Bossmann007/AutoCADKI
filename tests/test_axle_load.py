import pytest

from src.axle_load import AxleSpec, axle_positions
from src.tank_shell import ShellSpec

A, S = AxleSpec(), ShellSpec()


def test_totals():
    assert A.total_kg == 48000.0
    assert sum(A.axle_loads_kg[1:]) == 25500.0


def test_moment_equilibrium_about_kingpin():
    r = axle_positions(A, S)
    about_kp = sum(w * (x - r["kingpin_x"]) for w, x in zip(A.axle_loads_kg, r["axle_x"]))
    assert about_kp == pytest.approx(A.total_kg * (r["cg_x"] - r["kingpin_x"]), rel=1e-9)


def test_spacings_kept_and_hand_calc():
    r = axle_positions(A, S)
    gaps = [b - a for a, b in zip(r["axle_x"], r["axle_x"][1:])]
    assert gaps == pytest.approx(list(A.spacings_mm))
    # hand calc: x_cg-from-kingpin = 5030; d1 = 48000*5030/35500 - 2657.7 = 6801.1 - 2657.7 = 4143.4
    assert r["kingpin_to_axle1"] == pytest.approx(4143.4, abs=1.0)


def test_cg_shift_moves_axles_rearward():
    base = axle_positions(A, S)["kingpin_to_axle1"]
    assert axle_positions(A, S, cg_x=axle_positions(A, S)["cg_x"] + 300)["kingpin_to_axle1"] > base
