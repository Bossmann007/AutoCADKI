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

## Project inputs (TEST project, replicated from the owner's hand sketch, 54,000 L; not absolute truths)

- Tank: circular, Di 2290 mm, straight length 12,888 mm = (54,000 x 1.025 - 2 x 1,200 + 3 x 41) / 4.118 (sketch formula: 2.5% factor, two heads of 1,200 L, three baffles of 41 L, 4.118 L/mm... per m of section), shell 3 mm, heads 4 mm (from earlier owner input; not in the sketch),
  torispherical heads, ASSUMED R = Di, r = 0.10 Di (our head = 1,188 L vs the sketch's 1,200 L, which supports this), 3 baffles (positions TBD, at the suspension supports).
- Trailer: 4 axles, spacings 2450 / 1250 / 1250 mm; kingpin 800 mm from the front end; kingpin -> axle 1 = 5640 mm;
  loads: kingpin 13.5 t, axles 31.2 t, total 44.7 t (sketch). Per-axle split ASSUMED: axle 1 = 10 t, axles 2-4 equal.
  The sketch also shows CG at 5640 and kingpin -> axle group 8080 (alt. 7830) from the kingpin; the model gives 5691 and 8154 (within ~1%).
- Sketch items not modelled / unclear: overall ~18,300 mm (with tractor), 2500 (last axle to chassis end), 786/780, 5450, 12,640 and 248.
- An earlier Pastre 45,000 L study (10/2015) was supplied only as a basis; its numbers are not used.
- The engineer replaces all of this when a real project starts.

## Known issues

- 

## Current work

See `.claude/state/checkpoint.json` for live task state.
