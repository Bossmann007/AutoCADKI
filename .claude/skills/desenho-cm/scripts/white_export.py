"""White-background exports of a CADCraft DXF: vector A3 PDF + 300 dpi PNG (black lines on white).

CADCraft's own PNG/PDF exports use a dark background; its SVG export is white with black lines, so this goes
DXF -> SVG (cadcraft-cli) -> PDF (svglib/reportlab) -> PNG (PyMuPDF).

Usage: uvx --with svglib --with reportlab --with pymupdf python white_export.py X.dxf [Y.dxf ...] --out DIR
"""
import argparse
import subprocess
from pathlib import Path

import fitz
from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import A3, landscape
from svglib.svglib import svg2rlg

CLI = str(Path.home() / ".local/bin/cadcraft-cli")


def export(dxf: Path, out: Path) -> list[Path]:
    out.mkdir(parents=True, exist_ok=True)
    svg, pdf, png = (out / f"{dxf.stem}.{ext}" for ext in ("svg", "pdf", "png"))
    subprocess.run([CLI, "convert", str(dxf), str(svg)], check=True, stdout=subprocess.DEVNULL)
    drawing = svg2rlg(str(svg))
    pw, ph = landscape(A3)
    s = min(pw / drawing.width, ph / drawing.height)
    drawing.scale(s, s)
    drawing.width *= s
    drawing.height *= s
    renderPDF.drawToFile(drawing, str(pdf))
    fitz.open(str(pdf))[0].get_pixmap(dpi=300, alpha=False).save(str(png))
    return [pdf, png]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("dxf", nargs="+", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    for d in a.dxf:
        print(*export(d, a.out))
