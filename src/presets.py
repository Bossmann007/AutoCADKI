"""Project presets. All numbers are TEST inputs taken from the owner's documents; the engineer replaces them.

52k: colour photo (52,000 L, #3 mm INOX, Di 2290, straight 12,400, kingpin 700 from the cylinder/head junction (owner confirmed), kingpin->axle 1 = 5250,
     rear chassis 1500 past the last axle) and the 52 m3 STEP assembly (tyre/chassis sizes).
54k: hand sketch (54,000 L, straight 12,888, kingpin 800 from the front junction (same convention ASSUMED), kingpin->axle 1 = 5640).
Baffles (owner rule): QO1 over the landing leg, QO2 500 mm after axle 1, QO3 600 mm after axle 2, dished ASME 10, 4 mm.
Ring (orange) and red band positions of 52k were measured on the photo (+-100 mm).
Loads per axle are not in the 52k documents: the sketch's loads are reused (ASSUMED).
"""
from dataclasses import replace

from src.axle_load import AxleSpec
from src.tank_shell import ShellSpec
from src.trailer_3d import GearSpec


def baffle_positions(axles: AxleSpec, gear: GearSpec = GearSpec()) -> tuple:
    """Owner's rule (2026-10-10), from the front junction: QO1 over the landing leg; QO2 500 mm after axle 1;
    QO3 600 mm after axle 2."""
    kp = axles.kingpin_from_tangent_mm
    a1 = kp + axles.kingpin_to_axle1_mm
    a2 = a1 + axles.spacings_mm[0]
    return (kp + gear.landing_leg_from_kingpin, a1 + 500.0, a2 + 600.0)


_A52 = AxleSpec(kingpin_from_tangent_mm=700.0, kingpin_to_axle1_mm=5250.0)
_A54 = AxleSpec()

PRESETS = {
    "52k": (ShellSpec(straight_length=12400.0,
                      red_band_positions=(2060.0, 4040.0),                # red bands in the photo (function to confirm)
                      ring_positions=(980.0, 5200.0, 7660.0, 9950.0, 11040.0)),  # orange bands in the photo
              _A52),
    "54k": (ShellSpec(), _A54),
}
# baffle positions follow the owner's rule for both presets (needs the axle positions)
PRESETS = {k: (replace(sh, baffle_positions=baffle_positions(ax)), ax) for k, (sh, ax) in PRESETS.items()}

DEFAULT = "52k"


def get(name: str = DEFAULT):
    return PRESETS[name]

