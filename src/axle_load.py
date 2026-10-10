"""Axle positions from load balance (static, moments about the kingpin / pino rei).

Inputs from the project owner (2026-10-10): 4 axles, spacings 2450 / 1250 / 1250 mm,
axle 1 carries 10,000 kg, axles 2-4 carry 25,500 kg together (assumed equal share, 8,500 kg each),
kingpin carries 12,500 kg. ASSUMPTION: combined centre of gravity 5,030 mm from the kingpin, the value in a
reference study (Pastre 45,000 L, 4E chassis, 10/2015) used only as a basis; the real CG must come from the
engineer. kg, mm.
"""
from dataclasses import dataclass

from src.tank_shell import ShellSpec


@dataclass(frozen=True)
class AxleSpec:
    axle_loads_kg: tuple = (10000.0, 8500.0, 8500.0, 8500.0)
    spacings_mm: tuple = (2450.0, 1250.0, 1250.0)
    kingpin_load_kg: float = 12500.0
    kingpin_from_front_mm: float = 750.0   # from the outer apex of the front head (assumed reference)
    cg_from_kingpin_mm: float = 5030.0     # reference-study CG, to be replaced by the engineer's value

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
    xbar = sum(w * o for w, o in zip(axles.axle_loads_kg, offsets)) / group  # resultant, from axle 1
    # moments about the kingpin: total weight at cg == axle reactions (kingpin reaction has no moment)
    resultant_from_kp = axles.total_kg * (cg - kp_x) / group
    d1 = resultant_from_kp - xbar
    xs = [kp_x + d1 + o for o in offsets]
    rear_apex = shell.straight_length + shell.head_depth_outer
    return {"kingpin_x": kp_x, "axle_x": xs, "kingpin_to_axle1": d1, "rear_overhang": rear_apex - xs[-1],
            "cg_x": cg}
