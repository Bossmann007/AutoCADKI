"""Kingpin (pino rei) and axle positions, with a static moment check. kg, mm.

Test inputs replicated from the owner's hand sketch (54,000 L, 2026-05-21?): 4 axles, spacings 2450/1250/1250,
kingpin 800 from the front, kingpin->axle 1 = 5640, loads: kingpin 13.5 t, axles 31.2 t, total 44.7 t.
Per-axle split is NOT in the sketch: ASSUMED axle 1 = 10.0 t, axles 2-4 equal (7.067 t), which reproduces the
sketch's kingpin->axle-group distance (8080) within ~1%. If kingpin_to_axle1_mm is None, axle 1 is solved from the
CG distance instead (moment balance). The real values come from the engineer.
"""
from dataclasses import dataclass

from src.tank_shell import ShellSpec


@dataclass(frozen=True)
class AxleSpec:
    axle_loads_kg: tuple = (10000.0, 7066.67, 7066.67, 7066.66)
    spacings_mm: tuple = (2450.0, 1250.0, 1250.0)
    kingpin_load_kg: float = 13500.0
    kingpin_from_front_mm: float = 800.0   # from the outer apex of the front head (assumed reference)
    kingpin_to_axle1_mm: float | None = 5640.0
    cg_from_kingpin_mm: float = 5640.0     # used only when kingpin_to_axle1_mm is None

    @property
    def total_kg(self) -> float:
        return self.kingpin_load_kg + sum(self.axle_loads_kg)


def axle_positions(axles: AxleSpec, shell: ShellSpec, cg_x: float | None = None) -> dict:
    """Positions along the tank axis (x=0 front tangent line, +x rearward), plus overhang and offsets.

    cg_x: combined centre of gravity x; default = kingpin + axles.cg_from_kingpin_mm.
    """
    kp_x = -shell.head_depth_outer + axles.kingpin_from_front_mm
    cg = kp_x + axles.cg_from_kingpin_mm if cg_x is None else cg_x
    offsets = [0.0]
    for sp in axles.spacings_mm:
        offsets.append(offsets[-1] + sp)
    group = sum(axles.axle_loads_kg)
    if axles.kingpin_to_axle1_mm is not None:
        xs = [kp_x + axles.kingpin_to_axle1_mm + o for o in offsets]
        implied_cg = sum(w * (x - kp_x) for w, x in zip(axles.axle_loads_kg, xs)) / axles.total_kg
        rear_apex = shell.straight_length + shell.head_depth_outer
        return {"kingpin_x": kp_x, "axle_x": xs, "kingpin_to_axle1": axles.kingpin_to_axle1_mm,
                "rear_overhang": rear_apex - xs[-1], "cg_x": kp_x + implied_cg,
                "cg_from_kingpin": implied_cg,
                "group_resultant_from_kingpin": sum(w * (x - kp_x) for w, x in zip(axles.axle_loads_kg, xs)) / group}
    xbar = sum(w * o for w, o in zip(axles.axle_loads_kg, offsets)) / group  # resultant, from axle 1
    # moments about the kingpin: total weight at cg == axle reactions (kingpin reaction has no moment)
    resultant_from_kp = axles.total_kg * (cg - kp_x) / group
    d1 = resultant_from_kp - xbar
    xs = [kp_x + d1 + o for o in offsets]
    rear_apex = shell.straight_length + shell.head_depth_outer
    return {"kingpin_x": kp_x, "axle_x": xs, "kingpin_to_axle1": d1, "rear_overhang": rear_apex - xs[-1],
            "cg_x": cg, "cg_from_kingpin": cg - kp_x, "group_resultant_from_kingpin": resultant_from_kp}
