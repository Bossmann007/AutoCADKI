"""Parametric tank shell (casco): oval cross-section cylinder + two half-ellipsoid heads (calotas).

Units: mm. Tank axis = X, width = Y, height = Z. Geometry only: thickness is an INPUT,
it is not derived from Portaria INMETRO 134/2022 Anexo H (see docs/research/tank-trailer-norms-br.md).
Every default below is a placeholder for the reviewing engineer, not a design.
"""
from dataclasses import dataclass
from math import pi

import cadquery as cq

MAX_WIDTH_MM = 2600  # CONTRAN Res. 882/2021 art. 4 (verified in docs/research/ai-cad-trailers.md)


@dataclass(frozen=True)
class ShellSpec:
    width: float = 2200.0        # outer width, Y
    height: float = 1500.0       # outer height, Z
    length: float = 9500.0       # cylindrical part, X
    head_depth: float = 350.0    # outer depth of each head along X
    thickness: float = 4.75      # wall, shell and heads

    def check(self) -> None:
        if min(self.width, self.height, self.length, self.head_depth, self.thickness) <= 0:
            raise ValueError("all dimensions must be > 0")
        if self.thickness >= min(self.width, self.height, 2 * self.head_depth) / 2:
            raise ValueError("thickness too large for the section")
        if self.width > MAX_WIDTH_MM:
            raise ValueError(f"outer width {self.width} mm exceeds CONTRAN limit {MAX_WIDTH_MM} mm")

    @property
    def inner(self) -> tuple[float, float, float]:
        """Inner semi-axes (a: Y, b: Z, h: head depth)."""
        t = self.thickness
        return self.width / 2 - t, self.height / 2 - t, self.head_depth - t


def litros_por_cm(spec: ShellSpec) -> float:
    """Volumetric capacity per cm of cylindrical length: key for Anexo H tables."""
    a, b, _ = spec.inner
    return pi * a * b / 1e6  # mm^2 * 10 mm / 1e6 mm^3 per litre


def capacidade_litros(spec: ShellSpec) -> float:
    a, b, h = spec.inner
    cyl = pi * a * b * spec.length
    heads = 4 / 3 * pi * a * b * h  # two half-ellipsoids
    return (cyl + heads) / 1e6


def _body(a: float, b: float, h: float, length: float) -> cq.Workplane:
    """Solid of revolution (circular section radius a, half-ellipsoid heads), then scaled in Z by b/a.

    One revolve + one scale avoids boolean seams between head and cylinder (those gave invalid solids).
    """
    V = cq.Vector
    head_l = cq.Edge.makeEllipse(a, h, V(0, 0, 0), V(0, 0, 1), V(0, 1, 0), 0, 90)
    top = cq.Edge.makeLine(V(0, a, 0), V(length, a, 0))
    head_r = cq.Edge.makeEllipse(a, h, V(length, 0, 0), V(0, 0, 1), V(0, 1, 0), 270, 360)
    axis = cq.Edge.makeLine(V(-h, 0, 0), V(length + h, 0, 0))
    face = cq.Face.makeFromWires(cq.Wire.assembleEdges([head_l, top, head_r, axis]))
    solid = cq.Solid.revolve(face, 360, V(0, 0, 0), V(1, 0, 0))
    return cq.Workplane("XY").add(solid.transformGeometry(cq.Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, b / a, 0]])))


def cavity(spec: ShellSpec) -> cq.Workplane:
    spec.check()
    a, b, h = spec.inner
    return _body(a, b, h, spec.length)


def build_shell(spec: ShellSpec) -> cq.Workplane:
    spec.check()
    outer = _body(spec.width / 2, spec.height / 2, spec.head_depth, spec.length)
    return outer.cut(cavity(spec))


def mesh_volume_litros(wp: cq.Workplane) -> float:
    """Volume from a tessellation. Shape.Volume() is ~1% off after the non-uniform scale in _body."""
    verts, tris = wp.val().tessellate(0.01, 0.05)
    return abs(sum(verts[i].dot(verts[j].cross(verts[k])) for i, j, k in tris)) / 6 / 1e6


if __name__ == "__main__":
    s = ShellSpec()
    cq.exporters.export(build_shell(s), "out/tank_shell.step")
    print(f"capacidade {capacidade_litros(s):.0f} L, {litros_por_cm(s):.2f} L/cm")
