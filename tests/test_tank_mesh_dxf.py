from ezdxf import recover

from src.tank_shell import ShellSpec, export_dxf_mesh


def test_mesh_dxf_has_three_closed_part_meshes(tmp_path):
    path = tmp_path / "m.dxf"
    export_dxf_mesh(ShellSpec(), path)
    doc, auditor = recover.readfile(path)
    assert not auditor.has_errors
    meshes = list(doc.modelspace().query("MESH"))
    assert {m.dxf.layer for m in meshes} == {"CASCO", "CALOTA_DIANTEIRA", "CALOTA_TRASEIRA"}
    for m in meshes:
        assert len(m.vertices) > 100 and len(m.faces) > 100
