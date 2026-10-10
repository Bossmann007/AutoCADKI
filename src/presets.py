"""Project presets. All numbers are TEST inputs taken from the owner's documents; the engineer replaces them.

52k: colour photo (52,000 L, #3 mm INOX, Di 2290, straight 12,400, kingpin 700 from the cylinder/head junction (owner confirmed), kingpin->axle 1 = 5250,
     rear chassis 1500 past the last axle) and the 52 m3 STEP assembly (tyre/chassis sizes).
54k: hand sketch (54,000 L, straight 12,888, kingpin 800 from the front junction (same convention ASSUMED), kingpin->axle 1 = 5640).
Loads per axle are not in the 52k documents: the sketch's loads are reused (ASSUMED).
"""
from src.axle_load import AxleSpec
from src.tank_shell import ShellSpec

PRESETS = {
    "52k": (ShellSpec(straight_length=12400.0), AxleSpec(kingpin_from_tangent_mm=700.0, kingpin_to_axle1_mm=5250.0)),
    "54k": (ShellSpec(), AxleSpec()),
}

DEFAULT = "52k"


def get(name: str = DEFAULT):
    return PRESETS[name]
