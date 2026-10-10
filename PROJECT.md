# PROJECT.md

Project brain — semi-static. Update when stack or architecture changes.

## Goal

Create 2D and 3D drawings of trailers (carretas) and their parts using AI.
Phase 1 is research: what approaches/tools exist (text-to-CAD, parametric CAD
generation via LLM code, DXF/DWG output for AutoCAD, 3D mesh/STEP generation),
what is feasible, and what output formats a trailer shop needs.

## Stack

- Language: Python 3.12
- Framework: CadQuery 2.x (OCCT B-rep), pytest
- Package manager: uv (`.venv/`, git-ignored)

## Commands

```bash
uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python cadquery pytest
.venv/bin/python -m pytest -q
mkdir -p out && .venv/bin/python -m src.tank_shell   # writes out/tank_shell.step
```

## Architecture

Research in `docs/research/`. `src/tank_shell.py`: parametric tank shell (oval section + half-ellipsoid heads, thickness as input). Next: nozzles/manholes, baffles, chassis, DXF drawings. All dimensions are placeholders until the reviewing engineer sets them.

## Conventions

- Research notes: Markdown in `docs/research/`, primary sources, dated

## Decisions

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-10-10 | Research before building | User request at setup |
| 2026-10-10 | MVP target: tank trailer (carreta tanque) | User choice |
| 2026-10-10 | Shell thickness is an input, not computed from Anexo H | Tables depend on cargo group, density, l/cm, L; engineer reviews at the end |
| 2026-10-10 | Deliverable format includes DWG (not only DXF) | User requirement; see docs/research/ai-cad-trailers.md §5 |

## Project inputs (TEST project; numbers come from the owner's documents, not absolute truths)

Two presets in `src/presets.py` (default `52k`); the engineer replaces everything when a real project starts.

- **52k** (colour photo + `TANQUE_PASTRE_52M3_asm.stp`, owner's first spoken spec): 52,000 L, shell 3 mm INOX, heads 4 mm,
  Di 2290, straight 12,400 (our capacity formula gives 52.03 m3), kingpin 700 mm from the cylinder/head junction (owner confirmed 2026-10-10; not from the apex), kingpin -> axle 1 = 5250,
  axle spacings 2450 / 1250 / 1250, chassis ends at the rear junction: 1500 from the last axle to it (700 + 5250 + 2450 + 1250 + 1250 + 1500 = 12,400). (The owner once dictated Di 2190: the photo and STEP say 2290.)
- **54k** (hand sketch, 54,000 L): straight 12,888 = (54,000 x 1.025 - 2 x 1,200 + 3 x 41) / 4.118, kingpin 800 from the front junction (same convention ASSUMED),
  kingpin -> axle 1 = 5640, loads kingpin 13.5 t / axles 31.2 t / total 44.7 t.
- Torispherical "ASME 10" heads ASSUMED R = Di, r = 0.10 Di (our head = 1,188 L vs the sketch's 1,200 L).
- Loads per axle are NOT in the 52k documents: sketch loads reused, axle 1 = 10 t, axles 2-4 equal (ASSUMED).
- Shell plates (chapas), owner 2026-10-10: counted from the weld of the front head, 10 plates of 1,200 mm + a last plate of 400 mm = 12,400 straight length (circumferential welds at 1,200 ... 12,000). The 54k preset uses the same rule (10 x 1,200 + 888, ASSUMED).
- Landing legs (pes de apoio) 2500 mm from the kingpin (owner confirmed 2026-10-10).
- Baffles (the red lines in the photo, per the owner): 52k positions measured on the photo from the front junction: 2,060 and 4,040 mm (+-100); the 3rd is not visible and is ASSUMED at axle 1 (5,950, continuing the ~2,000 mm pitch). 54k: default assumption at axle 1, axles 2-3 mid, axle 4.
- Outer orange bands in the photo (rings/straps) measured at 980 / 5,200 / 7,660 / 9,950 / 11,040 mm (+-100); the 54k preset uses 9 evenly spaced rings (ASSUMED).
- Taken from the 52 m3 STEP assembly (Creo, 282 MB, 464 products, 5,922 solids; not in the repo): tyre OD 1105 x 275, dual gap 60,
  track 1940, chassis rails 80 x 320 at 970 centres, tank bottom ~1,353-1,399 mm above ground, tank axis slopes ~0.4 deg (not modelled),
  tank built from 1,215 mm rings of 3 mm wall, two spare wheels, first axle looks like a lift axle (not modelled).
- Sketch items not modelled / unclear: overall ~18,300 mm (with tractor), 2500, 786/780, 5450, 12,640 and 248.
- An earlier Pastre 45,000 L study (10/2015) was a basis only; its numbers are not used.
- Outputs: `src/trailer_3d.py` (3D assembly -> STEP, 3D DXF with 3DFACE), `src/ga_drawing.py` (A1 1:50 general arrangement DXF).
  DXF -> DWG was done with AutoCAD 2027 for Mac from the command line (script via `-b`), worked 3 of 4 times.

## Known issues

- 

## Current work

See `.claude/state/checkpoint.json` for live task state.
