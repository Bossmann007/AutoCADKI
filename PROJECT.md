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
- 2D chassis drawings: CADCraft (`~/.local/bin/cadcraft-cli`, MCP `cadcraft`)
- 3D models for drawings and renders: build123d through cadgen (text-to-cad plugin), `cadgen run <model>.py`
- Presentation renders: Blender 5.2 + official Blender Lab MCP v1.0.3
- Package manager: uv (`.venv/`, git-ignored)

## Commands

```bash
uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python cadquery pytest
.venv/bin/python -m pytest -q
mkdir -p out && .venv/bin/python -m src.tank_shell   # writes out/tank_shell.step
```

## Architecture

Research in `docs/research/`. `src/tank_shell.py`: parametric tank shell (cylinder + torispherical "ASME 10" heads, thickness as input). Per-job work (CM chassis drawings, 3D models, renders) lives in `local/<project>/` (git-ignored) and follows `.claude/skills/desenho-cm/SKILL.md`. Next: nozzles/manholes, baffles, chassis, DXF drawings. All dimensions are placeholders until the reviewing engineer sets them.

## Conventions

- Research notes: Markdown in `docs/research/`, primary sources, dated

## Decisions

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-10-10 | Research before building | User request at setup |
| 2026-10-10 | MVP target: tank trailer (carreta tanque) | User choice |
| 2026-10-10 | Shell thickness is an input, not computed from Anexo H | Tables depend on cargo group, density, l/cm, L; engineer reviews at the end |
| 2026-10-10 | Deliverable format includes DWG (not only DXF) | User requirement; see docs/research/ai-cad-trailers.md §5 |
| 2026-10-19 | CM070 drawing method approved by the engineer (dimension chain kept in `local/cm070/`; 3-axle version = same trailer without the middle axle) | Engineer, via Enzo |
| 2026-10-20 | Mandatory gate: the dimension table is confirmed before drawing (PR #7); every print/render sent to Enzo on a white background | Enzo |
| 2026-11-08 | Projeto vira Hephaestus dentro do AutoCADKI: assistente do Nonno (Claude + skills), depois ML; FreeCAD + freecad-mcp para peças no Mac | Enzo; plano v2 revisado por Maria, Do Contra e Operations Planner (docs/PLAN.md) |
| 2026-11-08 | Stainless tank job from `raw/` is its own trailer, not the CM070: polished stainless tank, rear panel stainless with the logo cut out over blue, chassis blue, top guard rail folded | Enzo; all tank dimensions still SUPOSTO (no drawing) |
| 2026-11-09 | Tank logo uses the Michroma font (SIL OFL), kept in `local/` | Closest free match to the logo; Enzo approved the download |
| 2026-11-09 | The `raw/` stainless tank is the 52k preset (TANQUE_PASTRE_52M3): rows 2-12 of `local/tanque_inox/ref_crops/tabela_medidas.md` use its values; renders for this job on the dark studio background | Enzo; the full table still waits for his ok before modelling |

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
- Baffles (quebra-ondas), owner rule 2026-10-10: dished ASME 10 plates, 4 mm, **convex toward the front** so the liquid impact hits the concave side; QO1 over the landing leg (700 + 2500 = 3,200 mm from the front junction), QO2 500 mm after axle 1 (6,450), QO3 600 mm after axle 2 (9,000). Central passage opening 500 mm (Anexo H minimum; the owner gave no size). The white "U" shapes in the photo fall at the same three positions and are modelled as external U reinforcements (lower half ring).
- The two red bands in the photo (~2,060 and ~4,040 mm, +-100) are modelled as outer red bands; function unknown, to confirm.
- Details copied from the colour photo (ASSUMED, +-150 mm, see `DetailSpec`): box on top of the tank at 5,150-6,650, vertical pipe with top valve at 7,150, hazard panel at 10,075 and two diamond labels at 10,540 / 11,015, rear bumper bar with posts and lights. Not modelled: the red object near the front frame, spare wheels, front bolster frame, tank slope.
- Outer orange bands in the photo (rings/straps) measured at 980 / 5,200 / 7,660 / 9,950 / 11,040 mm (+-100); the 54k preset uses 9 evenly spaced rings (ASSUMED).
- Taken from the 52 m3 STEP assembly (Creo, 282 MB, 464 products, 5,922 solids; not in the repo): tyre OD 1105 x 275, dual gap 60,
  track 1940, chassis rails 80 x 320 at 970 centres, tank bottom ~1,353-1,399 mm above ground, tank axis slopes ~0.4 deg (not modelled),
  tank built from 1,215 mm rings of 3 mm wall, two spare wheels, first axle looks like a lift axle (not modelled).
- Sketch items not modelled / unclear: overall ~18,300 mm (with tractor), 2500, 786/780, 5450, 12,640 and 248.
- An earlier Pastre 45,000 L study (10/2015) was a basis only; its numbers are not used.
- Outputs: `src/trailer_3d.py` (3D assembly -> STEP, 3D DXF with 3DFACE), `src/ga_drawing.py` (A1 1:50 general arrangement DXF).
  DXF -> DWG was done with AutoCAD 2027 for Mac from the command line (script via `-b`), worked 3 of 4 times.

## Known issues

- cadgen (0.8.x, Python 3.13) no longer exports `cadgen.build123d` / `cadgen.srgb`: use `import build123d as bd` and a local `srgb`. Fixed in `local/cm070/3d/cm070_3d.py` on 2026-11-09 (`cadgen run` exit 0, `check_model.py` 20/20).
- Local scripts need Python 3.12+ (`str | None` fails on the system python3 3.9).
- `scripts/verify` runs every `local/*/3d/checks/check_*.py` and `interference.py` when they exist (about 2 min with the tank interference check).

## Current work

See `.claude/state/checkpoint.json` for live task state.
