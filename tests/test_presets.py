import pytest

from src.axle_load import axle_positions
from src.presets import get
from src.tank_shell import capacidade_nominal_litros


def test_52k_preset_reproduces_52000_litres():
    shell, _ = get("52k")
    assert capacidade_nominal_litros(shell) == pytest.approx(52000, rel=3e-3)


def test_52k_axle_dimensions_from_photo():
    shell, axles = get("52k")
    r = axle_positions(axles, shell)
    assert r["kingpin_x"] == 700  # from the cylinder/head junction
    assert r["kingpin_to_axle1"] == 5250
    gaps = [b - a for a, b in zip(r["axle_x"], r["axle_x"][1:])]
    assert gaps == pytest.approx([2450, 1250, 1250])
