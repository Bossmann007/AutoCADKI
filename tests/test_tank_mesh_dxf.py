import pytest
from ezdxf import recover

from src.tank_shell import ShellSpec, export_dxf_mesh


def test_3d_dxf_is_r2000_with_faces_on_three_part_layers(tmp_path):
    path = tmp_path / "m.dxf"
    export_dxf_mesh(ShellSpec(), path)
    doc, auditor = recover.readfile(path)
    assert not auditor.has_errors
    assert doc.dxfversion == "AC1015"
    faces = list(doc.modelspace().query("3DFACE"))
    assert {f.dxf.layer for f in faces} == {"CASCO", "CALOTA_DIANTEIRA", "CALOTA_TRASEIRA"}
    assert len(faces) > 300
    xs = [v.x for f in faces for v in f.wcs_vertices()]
    assert max(xs) - min(xs) == pytest.approx(ShellSpec().overall_length, rel=1e-3)
