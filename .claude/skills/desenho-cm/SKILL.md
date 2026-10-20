---
name: desenho-cm
description: Make or change a trailer chassis drawing ("CM0xx", e.g. "4º eixo após adaptação") from the engineer's hand sketch and the previous CM drawing, with CADCraft. Use when the user sends a photo of an engineer's sketch or a CM drawing and asks to make, change, "alterar", "replicar" or "deixar igual" a drawing, or asks for the 3-axle / 4-axle version. Also for the 3D model, renders and presentation video of the same trailer (text-to-cad + Blender MCP).
---

# Desenho CM (carreta) a partir do croqui do engenheiro

Method approved by the engineer for CM070 (2026-10-19). Reference implementation:
`~/Projects/AutoCADKI/local/cm070/cm070_drawing.py` (copy it for a new CM; do not edit the approved one).

## Rules

- The drawing is only valid if every dimension equals the engineer's sketch. Never invent a value.
- Everything stays on this machine: work in `~/Projects/AutoCADKI/local/<cm>/` (git-ignored). Never commit or push
  chassis numbers, ARTs, engineer data or the drawings.
- Copy the layout of the previous CM drawing: overall length on top, kingpin chains above the chassis, axle chain
  below, chassis heights as vertical dimensions, title block bottom-left, code bottom-right and in the title block.

## Steps

1. Transcribe. Zoom the photos (PIL crop + resize) and write a table: value | from where | to where. Read every
   number, also the small and circled ones.
   **Gate (mandatory): show the table and STOP. Do not draw until the user explicitly confirms the table.**
   Handwriting can be misread (7 vs 1, 2,43 vs 2,44); this confirmation is the only guarantee. If the user
   corrects a value, show the corrected table again and wait for a new confirmation.
2. Check the chain. front -> kingpin + kingpin -> axle 1 + axle gaps + last axle -> rear must equal the total.
   If it does not close, ask which value is wrong. Do not hide the difference.
3. Conventions learned on CM069/CM070:
   - The small numbers at the front and rear (205/225, 445) are the chassis heights (vertical), not lengths.
   - Long dimensions start at the kingpin line (e.g. 10200 = kingpin -> ABS); 1600 = front -> kingpin.
   - ABS sits between the last two axles.
   - Axle 1 -> axle 2 cannot be less than 2400.
   - 3-axle version = the same trailer without the middle axle (the two 1225 gaps become one 2450).
4. Build with CADCraft: `~/.local/bin/cadcraft-cli run --metric --cmd 'id {json}' ... --save X.dxf --export X.png`,
   then `cadcraft-cli convert X.dxf X.dwg` and `X.pdf`. Text style Arial (`style {name, font: "arial.ttf"}`) so the
   accents render. MCP server: `cadcraft` in the project `.mcp.json` (same engine).
   When the chain closes, draw to scale with no text overrides; only use `text` overrides when the engineer says the
   drawing does not need to be proportional.
5. Title block (from the user, every time): title, CHASSI, Eng. Mec. name, CREA, ARTs, code (CMxxx).
6. Verify before sending: read the DXF back with ezdxf (`recover.readfile`, no audit errors), compare every
   dimension value with the table, render the PNG and look at it. Send PNG + PDF + DWG with SendUserFile.
7. Report what was checked and what was not (e.g. DWG not opened in AutoCAD).

## 3D model and video (same dimension table)

Tools installed 2026-10-19 (all free):
- **text-to-cad** plugin v0.7.24 (`text-to-cad@earthtojake`, MIT, telemetry off with `cadgen telemetry off`).
  Skills: `cad` (parametric build123d model -> STEP/GLB/STL), `engineering-drawing` (PDF drawing), `dxf`.
- **Blender 5.2.2** (`/Applications/Blender.app`) + official **Blender Lab MCP v1.0.3** (add-on `mcp`, server
  `blender` in the project `.mcp.json`, pinned to `git+https://projects.blender.org/lab/blender_mcp.git@v1.0.3`).
  The PyPI package named `blender-mcp` is a different, unofficial project: do not use it.

Steps:
1. Model with the `cad` skill: build the trailer in build123d from the approved dimension table (chassis profile
   with 225/445 heights and slope, kingpin, landing leg, axles at the chain positions, wheels, ABS). Real 1:1 mm.
   Save in `local/<cm>/3d/` (git-ignored). Export GLB (for Blender) and STEP.
2. Check the model numbers against the table (bounding box = total length, axle x positions) before rendering.
3. Start Blender for the MCP: `open -a /Applications/Blender.app --args --online-mode` (the add-on only opens
   localhost:9876 with online access; the flag is per session, no preference change). Check `nc -z localhost 9876`.
4. With the `blender` MCP (`execute_blender_code`): new scene, import the GLB, materials (painted steel chassis,
   rubber tyres, metal rims), lights, ground, camera. Renders: still images (`render_viewport_to_path` for quick
   previews), turntable and camera moves for video (Cycles/EEVEE, ffmpeg output to `local/<cm>/video/`).
5. Safety: the Blender MCP runs generated Python with no guard. Work only on new or copied .blend files in `local/`,
   never on the user's other files.
