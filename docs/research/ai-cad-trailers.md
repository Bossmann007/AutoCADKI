# AI-generated CAD for trailers (carretas / semirreboques): feasibility research

Date: 2026-10-10. Language: English with Portuguese terms. Every claim is tagged **[V]** verified (primary source URL given) or **[U]** unverified (and why). Reference numbers in brackets point to the Sources list at the end.

## Summary

- **Feasible, with the right architecture.** The practical path is NOT "text-to-3D mesh". It is: LLM fills a parametric template or writes CadQuery/build123d code -> OCCT B-rep -> STEP (3D) + DXF (2D) -> validation loop -> human review. [U as a whole: no source shows an LLM producing a fabrication-grade trailer drawing end to end; this is an engineering judgement built from verified components below.]
- **Python CAD libs are mature and open source** (CadQuery, build123d: Apache-2.0, OpenCASCADE kernel, STEP/STL/DXF/SVG export) [V: 1,2,3,4].
- **Research on LLM/transformer text-to-CAD is real but benchmark-grade** (simple sketch-extrude parts, DeepCAD-style data), not assemblies like trailers [V: 5,6,7,8].
- **2D DXF via ezdxf is solid** (MIT, R12 to R2018). Dimensions work but need an explicit `render()` step or AutoCAD will not show them [V: 9,10].
- **Your local AutoCAD for Mac (full)** is a good DWG backend: it removes the need for ODA/LibreDWG on that machine, but NOT for headless/server use, and it cannot be driven by .NET/COM/accoreconsole on Mac [V for .NET/COM; U for accoreconsole] (see section 5).
- **Brazilian rules**: CONTRAN Res. 882/2021 (not 210/2006, which is revoked) sets width 2.60 m, height 4.40 m, tractor+semirreboque length 19.30 m since Res. 1.005/2024, axle limits, etc. [V: 24,25,26]. Selling a trailer legally also needs Senatran homologation (CAT / código marca-modelo-versão) [V partial: 28,29].
- **Main risk**: the drawing looks right but is structurally or legally wrong. A licensed engineer (ART/CREA) must sign anything structural [ART/CREA requirement mentioned in a search summary only: U].

---

## 1. LLM-generated parametric CAD code

### 1.1 Libraries

| Tool | What it is | Export | License | Notes |
|---|---|---|---|---|
| CadQuery | Python parametric CAD scripting on OCCT (OCP) | STEP, DXF, STL, VRML, AMF, 3MF listed [V:1]; also SVG, glTF (assemblies), others [V:3] | Apache-2.0 [V:1] | DXF export works only for 2D sections/sketches: use `.section()` first [V:3] |
| build123d | Python parametric B-rep framework on OCCT, derived from CadQuery, refactored | STEP, STL, 3MF, BREP, glTF, OBJ, DXF, SVG [V:4]; `ExportDXF`/`ExportSVG` with layers, colors, ISO/ANSI line types [V:4] | Apache-2.0 [V:2] | `project_to_viewport()` returns visible+hidden edges; `section()` for cross-sections [V:4]. Best fit for generating drawings from a model |
| OpenSCAD | Code-driven solid modeller (CSG) | STL, OFF, AMF, 3MF, DXF, SVG, PNG, PDF (A4 only); STEP not listed [V:11, a wikibook mirror of the user manual; not the first-party page] | not verified on page [U] | CSG/mesh oriented, weak for manufacturing B-rep. Not recommended for this project |

Why LLMs + these libs: code is text, can be diffed, tested, parametrised, and re-run. Dimensions are variables (e.g. `comprimento_chassi`, `bitola`) so the same script yields variants.

### 1.2 Research and datasets (all verified to exist)

- **Text2CAD** (NeurIPS 2024 Spotlight): transformer producing parametric CAD sequences from text; ~170K models, ~660K text annotations built on DeepCAD [V:5].
- **CADCodeVerify / CADPrompt** (Alrashedy et al., arXiv 2410.05340, preprint): VLM generates CAD code, checks the rendered object via generated validation questions, then self-corrects; CADPrompt = 200 prompts with expert CAD code. Reports with GPT-4: 7.30% lower point-cloud distance and 5.0% better success rate vs prior work [V:6]. Whether it uses CadQuery: the abstract page does not say [U].
- **CAD-Recode** (arXiv 2412.14042, ICCV 2025): point cloud -> Python CAD code with a small LLM decoder, trained on 1M procedurally generated sketch-extrude sequences [V:7]. Code is CadQuery format per a third-party summary [U; not stated on abstract page]. (Note: "CAD-Coder" is a different name; the paper you may be thinking of is CAD-Recode.)
- **DeepCAD** (ICCV 2021): 178,238 CAD models with construction sequences [V:8].
- **Fusion 360 Gallery**: Autodesk AI Lab; Reconstruction 8,625 sequences, Segmentation 35,680 parts, Assembly 8,251 assemblies / 154,468 parts [V:12].
- **ABC dataset**: ~1M CAD models from Onshape; STEP, Parasolid, STL, OBJ, features; CVPR 2019; licensing follows Onshape ToS (creators keep copyright) [V:13].
- Takeaway: datasets are dominated by small mechanical parts (brackets, gears). No source found for trailer/semitrailer-specific datasets [U: absence of evidence only].

### 1.3 Commercial / first-party tools

- **Zoo (zoo.dev) Text-to-CAD**: generates B-rep, exports STEP, claimed fully parametric, written in Zoo's own KCL language [V: 14 (search-result summary of Zoo research page); the main docs page now says Text-to-CAD is available in Zoo Design Studio, with the conversational agent "Zookeeper" [V:15]]. Output formats on the current page are not specified [V:15]. Independent evaluation limited [U].
- **Autodesk Project Bernini**: Autodesk Research generative model (text/image/point cloud/voxel -> 3D), research proof of concept, exports OBJ (mesh), not available publicly as of 2024 coverage [V:16 (Autodesk Research page found by search); details from secondary press: U]. Not a parametric CAD tool.
- **Onshape (PTC)**: AI Advisor (documentation assistant, shipping) and FeatureScript MCP Server in Onshape Labs (LLM writes FeatureScript, early access). PTC says "text-to-code-to-CAD". No native text-to-CAD product found [V for statements via PTC/Onshape pages: 17; the Katzman quote is reported by a trade outlet].
- Not checked: Fusion native AI features, Siemens, SolidWorks, Adam.new, etc. [U].

---

## 2. 2D output

### 2.1 ezdxf
- Python lib to read/write DXF; supports DXF R12 (AC1009) through R2018 (AC1032); MIT license [V:9].
- **Does not read/write DWG**; docs recommend ODA File Converter for DXF/DWG conversion [V:9].
- Dimensions: `add_linear_dim()`, `add_aligned_dim()` etc. return `DimStyleOverride`; **`render()` must be called** to build the anonymous block, because "AutoCAD is not willing to show a dimension line defined only by this dimension entity". ezdxf targets BricsCAD look; not all DIMSTYLE variables supported, so AutoCAD output may differ [V:10]. So: always test dimensions in real AutoCAD.
- Drawing add-on: renders DXF to PDF/SVG/PNG via Matplotlib, PyMuPDF, SVG backends; can render a paper-space layout; no 3D engine (3D is projected to XY, viewports render top view only); MTEXT is approximate [V:18]. Useful for fast preview/PDF in the validation loop, not as a plotting-accurate replacement for AutoCAD.
- Layouts/paper space/title blocks: ezdxf supports layouts (documented in ezdxf docs) [U: not fetched in this research; verify at ezdxf.readthedocs.io]. 

### 2.2 DWG options

| Option | Facts | Status |
|---|---|---|
| ODA File Converter | Free-to-download app converting between .dwg and .dxf versions; GUI + CLI; macOS 13+ (arm64/x64), Windows 10+, Linux x64 [V:19]. The page states no license; **commercial/redistribution terms unverified**. ODA SDK memberships are separate paid tiers (commercial $3,000 initial; non-commercial $375, no commercial distribution) [V partial: 20 (search snippet of pricing page)] | Use internally after reading its EULA [U] |
| LibreDWG | GPL-3.0-or-later C library; reads all DWG versions (some R2010+ objects skipped); writing partial (mainly up to R2004; R2010 to R2018 writes give CRC errors); `dxf2dwg` R2000 only (~80% coverage) [V:21] | OK for reading; weak for writing production DWG. GPL matters if you distribute |
| Autodesk AutoCAD (local) | See section 5 | Best fidelity for you |
| Autodesk APS (cloud) | Not researched: Design Automation for AutoCAD would be cloud DWG processing [U] | Skip for MVP |

Practical point: AutoCAD, BricsCAD, LibreCAD and most CAM tools read DXF directly. Many fabrication shops accept DXF (laser/plasma cutting) as the primary file. DWG is only needed if the client insists.

### 2.3 Dimensioned orthographic views from 3D
- build123d: `project_to_viewport()` (visible + hidden edges) and `section()`, then `ExportDXF`/`ExportSVG` [V:4]. Then you still must add dimensions (ezdxf) yourself: automatic dimensioning of projected views is not provided by these libs [U; not seen in docs, verify].
- CadQuery: DXF export of 2D sections/sketches only [V:3].
- OCCT hidden-line-removal (HLR) classes exist (`HLRBRep_*`) and are the usual engine behind such projections [U: not confirmed from OCCT docs here; my fetch did not reach that section].
- FreeCAD TechDraw (projection views, dimensions, DXF/SVG/PDF export) is the other route [U: wiki page blocked by bot protection; GUI-centric, scripting from headless is fiddly].
- Recommended: generate the 2D drawing **directly from the parameters** (flat plates/profiles drawn as 2D with ezdxf, dimensions placed from the same variables) rather than extracting from 3D. It is more controllable and gives clean fabrication drawings. Use 3D->2D projection only for general-arrangement views.

---

## 3. 3D output

- **STEP (ISO 10303)**: B-rep neutral exchange; written by CadQuery and build123d [V:1,3,4]. Primary deliverable for 3D.
- **STL/3MF/OBJ**: meshes (triangles); fine for viewing/3D printing, useless for editing dimensions or machining features [V: formats listed in 3,4]. IGES: not covered by sources [U].
- **Text-to-3D mesh AI (e.g. Bernini, image-to-3D)**: outputs meshes (Bernini exports OBJ) [V:16 partial]. Zoo contrasts mesh outputs, "hard to edit once imported", with its B-rep STEP [V: 14 via search summary].
- **Why parametric B-rep matters** for manufacturing: exact surfaces/edges (holes, cylinders, planes) for CNC/laser/bending, measurable dimensions, tolerances, STEP interoperability, regeneration when a parameter changes, BOM extraction from named solids. [Engineering rationale; supported in spirit by build123d description for CNC/laser/3D printing: V:2.]

---

## 4. What a trailer shop needs, and Brazilian regulation

### 4.1 Shop deliverables (engineering judgement, U as sources)
- Dimensioned fabrication drawings per part (laser/plasma plates, tubes, profiles, bent parts) with material/thickness, quantity, tolerances.
- General arrangement and assembly drawings; BOM / cut list (lista de corte); weld symbols (ISO 2553 / AWS A2.4 style) and weld sizes; surface treatment and paint notes; title block with revision.
- Structural check (longarinas, quinta roda/pino rei, eixos, suspensão) by a responsible engineer. **LLM output must not be trusted for structural sizing.**
- These were not verified from standards documents in this research [U].

### 4.2 Dimensions and weights: CONTRAN Res. 882/2021
Sources: DOU copy of Res. 882 (in.gov.br, via gov.br PDF, 2021 print) [V:24]; Res. 1.005/2024 text in DOU via gov.br PDF [V:25].

- **Res. 210/2006 and 211/2006 are revoked** (revogadas): 210 revoked by Deliberação 250/2021 and Res. 882/2021, effective 03/01/2022 [V partial: 26 (legisweb/normasbrasil aggregator, secondary; effective date and 27 revoked resolutions also per art. 64/65 reported there)]. The official art. 64 list was not read directly [U].
- Art. 4 (no AET/AE needed): width max 2.60 m; height max 4.40 m; length: non-articulated 14.00 m; articulated passenger transport 19.80 m; caminhão-trator + semirreboque **18.60 m in the original text**; truck/bus + reboque 19.80 m; more than two units 19.80 m [V:24].
- **Res. 1.005/2024 (3 Apr 2024, DOU 08/04/2024)** approves Deliberação 270/2023 and changes art. 4, III, "e": caminhão-trator + semirreboque **max 19.30 m**; in force on publication [V:25].
- Rear overhang (balanço traseiro): reboques and semirreboques up to 3.50 m [V:24 art. 4 §2 II]. Total length is measured to the most protruding points including accessories without exception [V:24 art. 4 §1].
- Art. 6 weights (original text; some items seen via aggregator summary, the DOU text lines confirm 6 t, 10 t, 12 t, 25.5 t tridem, 45 t, 54.5 t, 17.5 m thresholds): per axle: single 2 tires 6 t; single 4 tires 10 t; tandem double axle 17 t; tridem (semirreboque) 25.5 t; PBTC caminhão-trator+semirreboque under 16 m: 45 t; 54.5 t with tridem or spaced axles above 16 m [V partial: 24 for the lines visible above; the full tables 26/27 are secondary]. **Re-read art. 6 in the consolidated current text before coding any limit.**
- Semirreboques with spaced axles (eixos distanciados) need pneumatic suspension and at least one self-steering axle (art. 15) [V:24].
- Amendments: Res. 899/2022 (references to marking per axle; reported by secondary source) [U for details]. Further later changes may exist [U].
- "Res. 211": its status as revoked is reported by the same secondary source [U].
- The task prompt mentions "Lei da Balança"; Lei 7.408/1985 (tolerância de 5% no peso por eixo) is not verified here [U]. Neither were fines/penalties.
- Local OEERs can set stricter limits (art. 61) and AET/AE is required beyond limits [V partial: 27].

### 4.3 Homologation / registration of the implement (Senatran)
- Código de marca/modelo/versão for the RENAVAM and **CAT (Certificado de Adequação à Legislação de Trânsito)** are requested from Senatran by manufacturers, importers, encarroçadores, transformadores. Portaria Senatran 990/2022 deals with homologation and RENAVAM codes; Portaria Senatran 989/2022 with cadastro of fabricantes/instaladores of equipamentos veiculares (carroçaria) and CAT [V partial: 28 (search summaries of gov.br service pages and lex.com.br)]. Portaria DENATRAN 190/2009 was the earlier regime, replaced [V partial: 28].
- Res. CONTRAN 916/2022 now consolidates código marca/modelo/versão and the modifications permitted by CTB arts. 98 and 106, replacing Res. 291/2008 and (probably) 292/2008; modifications may need CSV from an ITL (Instituição Técnica Licenciada) [V partial: 29; 292 status unconfirmed: U].
- CCT (Comprovante de Capacitação Técnica) issued by an ITL accredited by INMETRO and licensed by Senatran, in some cases [V partial: 28].
- CIRETRAN: a state-level DETRAN unit; its role in implement registration was not verified here [U].
- Whether CSV or CCT applies to YOUR industrial semirreboque type: **unverified; ask a despachante/ITL or Senatran**.
- Also seen in a Senatran consultation title: antispray requirements for caminhão, reboque, semirreboque [V that the consultation exists: 30; content U].

---

## 5. Using local AutoCAD for Mac (full version) as the DWG / 2D backend

**Release note**: today is 2026-10; Autodesk help pages for a **2027** Mac release exist (Mac developer interface table at help.autodesk.com/cloudhelp/2027) [V:31]. Your version year is unknown: run `ABOUT` in AutoCAD. Older releases (2018 to 2024) differ in details; I cite the version of each source.

### 5.1 Programming/automation on Mac
- Interface table (Mac, full AutoCAD, 2027 docs): **AutoLISP yes, ObjectARX yes; Managed .NET no; ActiveX Automation no; VBA no; JavaScript no** [V:31]. For AutoCAD LT on Mac: none of them [V:31] (you have full AutoCAD, so AutoLISP applies).
- AutoLISP help (2021): "AutoCAD for Mac does not support Managed .NET applications" [V:32].
- Visual LISP on Mac (the `vl-*` / `vla-*` functions): the interface table doesn't list it; ActiveX-dependent LISP is not supported (2026 Mac AutoLISP docs, via search summary) [V partial: 33]. Plain AutoLISP should be fine.
- DCL dialogs are supported on Mac, with some tile attributes missing (2026 Mac docs via search summary) [V partial: 33].
- **Script files (.scr)**: SCRIPT command runs a .scr; one command per line; no dialog commands (use hyphen versions such as `-INSERT`); `;` comments; last line blank [V:34 (AutoCAD for Mac help 2018/2019, found by search; syntax unchanged in 2025 Windows help per result list: U for Mac 2027)]. Mac Terminal startup: `AutoCAD drawing_name -b script_name` (script name last) [V:34, Mac 2018 help]. Whether this switch still works in the current Mac release and on Apple silicon: [U], test it.
- **accoreconsole.exe (Core Console)**: only seen as a Windows executable in forum posts with Windows paths [V that Windows paths are used: forum posts; official Autodesk statement about Mac: not found]. Treat as **unavailable on Mac [U, not confirmed in Autodesk docs]**. No headless batch AutoCAD on macOS. APS Design Automation (cloud) not researched [U].

### 5.2 Opening an ezdxf DXF and saving as DWG
- Plan: ezdxf writes DXF (R2018 recommended, or R2013 if compatibility problems) -> open in AutoCAD for Mac -> `SAVEAS` DWG (or Mac File > Save As). Opening DXF in AutoCAD is a core capability (ezdxf docs target BricsCAD/AutoCAD output) [V: 9,10 imply AutoCAD reading]; the exact Mac SAVEAS-by-script sequence (FILEDIA/CMDDIA, DWG version prompt) was **not verified** [U]. Test with a .scr using `-SAVEAS` style commands.
- Dimension display: run `render()` in ezdxf; check results in AutoCAD because DIMSTYLE variable coverage is incomplete [V:10].
- A low-effort automation: one .scr per drawing (or a Mac Automator/AppleScript wrapper calling the Terminal startup switch) that opens the DXF, runs `AUDIT`/`ZOOM E`, and saves as DWG [U: untested design].

### 5.3 Does it remove the need for ODA / LibreDWG?
- **For a single-user interactive workflow on your Mac: yes**, AutoCAD itself converts DXF to DWG reliably, and DWG written by AutoCAD is the reference for client acceptance.
- **Still useful**: ODA File Converter (macOS-native, CLI, batch; license terms unverified [V:19]) for **headless batch** conversion when AutoCAD cannot be automated; LibreDWG only if you need to read DWG programmatically [V:21]. If you plan a web service, AutoCAD for Mac is not a server component (single desktop app, licensed per user) [U].
- Recommended: ship DXF as the primary 2D output (works everywhere), DWG as an optional step via AutoCAD for Mac (manual or .scr); evaluate ODA only if you need unattended batches.

### 5.4 3D in full AutoCAD for Mac: opening CadQuery STEP output
- Autodesk states that importing STEP is **not possible in AutoCAD LT or AutoCAD for Mac** (support article, and a note in the 2024 AutoCAD help) [V partial: 35 (statement known via search-result summaries; page itself returned HTTP 403 to my fetch)]. Whether the current Mac release (2026/2027) added STEP is **not confirmed**; I found no "What's New" item mentioning STEP/SAT [U: negative search only].
- Mac help for IMPORT lists **ACIS (.sat)** among formats [V partial: 36 (2019 Mac IMPORT page snippet)]. Community advice: convert STEP -> SAT elsewhere (e.g. Fusion) then import [secondary, forum: U].
- OCCT/CadQuery SAT export: **not found in CadQuery docs list of formats** [V that SAT is absent from the list: 3], so STEP->SAT needs another tool [U which one].
- AutoCAD for Mac does support 3D modeling in principle, but community posts say 3D is more limited than Windows (no offline rendering, etc.) [U: forum claims, not Autodesk].
- Verdict: do **not** make AutoCAD Mac the 3D viewer in the pipeline. Use STEP in FreeCAD / Fusion / Onshape / eDrawings for 3D review, and AutoCAD for the 2D DWG. If you need 3D in AutoCAD: test the IMPORT dialog in your version first; else a mesh-based 3D DXF or SAT via another converter [U].
- Features known missing on Mac from forum posts: Express Tools, Sheet Set Manager, Action Recorder, Data Extraction [U, forum]. Check the Autodesk comparison page for your version.

---

## 6. Recommended architecture

```
 User request ("carreta graneleira 3 eixos, 12.5 m, ...")
        |
        v
 [LLM] -> structured JSON spec (validated by Pydantic/JSON Schema)   <- trust boundary
        |
        v
 Parametric templates (CadQuery/build123d functions per part & per trailer type)
   - LLM only chooses parameters / picks parts / composes
   - LLM-written free-form code only in a sandbox, optional, behind review
        |
        +--> 3D B-rep assembly -> STEP (+ STL for preview)
        +--> 2D part drawings (ezdxf direct, dims from params, render()) -> DXF R2018
        +--> BOM / cut list (CSV/XLSX) from the same part registry
        |
        v
 Validation loop (deterministic first):
   - geometry: solid valid, volume > 0, bbox vs spec, no self-intersections
   - regulatory rules as code: width <= 2.60, height <= 4.40, comprimento conjunto <= 19.30 (with a cavalo, to be modelled), balanço <= 3.50, axle config vs limits
   - drawing: ezdxf audit, dimension count, layers, ezdxf drawing add-on -> PDF preview
   - optional VLM check (CADCodeVerify-style render + questions) as a second opinion only
        |
        v
 Human review + engineer sign-off  -> release
        |
        +--> AutoCAD for Mac: open DXF, check dims, SAVEAS DWG (manual or .scr); PDF plot
```

Design choices
- Templates over free-form code generation for repeatable trailer families (CadQuery and build123d are both Apache-2.0 [V:1,2]).
- Pick one kernel lib: build123d has DXF/SVG exporters with ISO line types and viewport projection [V:4]; CadQuery has the larger ecosystem and is the code format of CAD-Recode-style research (U). I lean toward build123d for drawings; CadQuery is acceptable.
- Keep rules and limits in a versioned data file (e.g. `regs/conTRAN_882.yaml`) with article reference and date, so changes (like 1.005/2024) are a data edit.
- Single source of truth: the parameter spec produces 3D, 2D, and BOM, so they cannot disagree.
- AutoCAD for Mac is a finishing/review tool, not a pipeline component (no .NET/COM, accoreconsole not documented on Mac).

## 7. Risks
1. Wrong-but-plausible geometry/dimensions from LLM code (known weakness: research reports success rates in percent, not certainty [V:6]).
2. Structural/safety liability: needs engineer + ART; do not let AI size members.
3. Regulation drift (882 changed by 899/2022 and 1.005/2024; more may follow) [V:25; U for others].
4. AutoCAD dimension rendering differences vs ezdxf [V:10].
5. DWG licensing (ODA terms unverified; LibreDWG GPL and write gaps [V:21]).
6. STEP not importable in AutoCAD for Mac (as documented for older versions) [V partial:35].
7. Weld symbols/ISO conventions are not in ezdxf as ready-made features [U: verify; may require custom blocks].
8. Zoo/Autodesk/Onshape offerings change fast; re-check before committing [V:14-17 are dated].

## 8. Suggested MVP
- One trailer type (suggest: semirreboque **carga seca / graneleiro** or **prancha** 3-axle, whichever you build most) and 4 to 6 parts: longarina (I-beam/chassis rail), travessa, placa de quinta roda / pino rei plate, suporte de eixo, painel lateral, para-choque (traseiro).
- Input: a form or JSON (comprimento, largura, número de eixos, espessuras, material), plus LLM front-end that converts Portuguese text to the JSON.
- Output per part: DXF R2018 (dimensioned, layers, title block) + DWG via AutoCAD Mac; STEP; BOM CSV; PDF preview.
- Validators: geometry + CONTRAN dimension checks above.
- Success criteria: a shop can cut one part from the DXF without questions; dims match the spec exactly; AutoCAD opens with no dimension errors.
- Time order: (1) one part end to end by hand-written template; (2) add JSON spec + LLM; (3) validators; (4) assembly + BOM; (5) DWG via AutoCAD script.

## 9. Open questions for the user
1. Which trailer type(s) and which sizes? Brand/catalogue constraints (eixos, suspensão supplier)?
2. Do you make the trailers (shop) or draw for a client? Do you hold CAT / registration (Portaria 989/990/2022)? Who is the responsible engineer (ART/CREA)?
3. Output must be DWG or is DXF acceptable to the cutting vendors? Which CAM/nesting software?
4. AutoCAD for Mac version year (`ABOUT`) and does IMPORT list STEP in your menu? Is a Windows machine/VM available?
5. Drawing standard: ABNT NBR 10067/10126/8403 style? (NBR drawing norms not researched [U]). Units mm, sheet sizes (A3/A4), title block template?
6. Weld notation (ABNT/ISO/AWS)? Material/paint standards?
7. Is an LLM API (cloud) acceptable for proprietary designs?
8. Do you want AI to propose designs, or only to automate drafting of designs you already specify? (The latter is much more feasible.)

---

## Sources

1. https://github.com/CadQuery/cadquery (CadQuery README)
2. https://github.com/gumyr/build123d
3. https://cadquery.readthedocs.io/en/latest/importexport.html
4. https://build123d.readthedocs.io/en/latest/import_export.html
5. https://arxiv.org/abs/2409.17106 (Text2CAD)
6. https://arxiv.org/abs/2410.05340 (CADCodeVerify / CADPrompt)
7. https://arxiv.org/abs/2412.14042 (CAD-Recode)
8. https://arxiv.org/abs/2105.09492 (DeepCAD)
9. https://ezdxf.readthedocs.io/en/stable/introduction.html
10. https://ezdxf.readthedocs.io/en/stable/tutorials/linear_dimension.html
11. https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Export (third-party mirror; first-party: https://openscad.org/documentation.html, page lacked format details)
12. https://github.com/AutodeskAILab/Fusion360GalleryDataset
13. https://deep-geometry.github.io/abc-dataset/
14. https://docs.zoo.dev/research/introducing-text-to-cad and https://zoo.dev/blog/introducing-text-to-cad (seen only as search results; not fetched)
15. https://zoo.dev/text-to-cad
16. https://www.research.autodesk.com/?p=5064 (Project Bernini; seen in search results; not fetched)
17. https://www.ptc.com/en/news/2025/ptc-announces-latest-Onshape-AI-advisor-release and https://www.onshape.com/en/blog/ai-advisor-artificial-intelligence-cad-engineering-software (search results; not fetched). Secondary: https://embeddedcomputing.com/technology/software-and-os/simulation-modeling-tools/ptcs-onshape-featurescript-mcp-server-delivers-ai-text-to-code-to-cad
18. https://ezdxf.readthedocs.io/en/stable/addons/drawing.html
19. https://www.opendesign.com/guestfiles/oda_file_converter
20. https://www.opendesign.com/pricing.md (search result snippet only)
21. https://github.com/LibreDWG/libredwg
24. https://www.gov.br/transportes/pt-br/assuntos/transito/conteudo-contran/resolucoes/Resolucao8822021.pdf (Res. 882/2021, DOU copy; text extracted locally)
25. https://www.gov.br/transportes/pt-br/assuntos/transito/conteudo-contran/resolucoes/Resolucao10052024.pdf (Res. 1.005/2024; text extracted locally)
26. https://www.legisweb.com.br/legislacao/?id=104243 (Res. 210/2006 marked revoked; secondary) and https://www.legisweb.com.br/legislacao/?id=428905 (Res. 899/2022; secondary)
27. https://www.normasbrasil.com.br/norma/resolucao-882-2021_425133.html (secondary consolidated view)
28. https://www.gov.br/pt-br/servicos/homologar-portaria-989-22-equipamento-rodoviario ; https://www.gov.br/transportes/pt-br/assuntos/transito/arquivos-senatran/portarias/2022/Portaria9902022.pdf (search results; not fetched)
29. https://www.normasbrasil.com.br/norma/resolucao-916-2022_429751.html (search result; not fetched)
30. https://www.gov.br/participamaisbrasil/requisitos-para-o-sistema-antispray-para-veiculos-tipo-caminhao-caminhao-trator-reboque-e-semirreboque1
31. https://help.autodesk.com/cloudhelp/2027/ENU/AutoCAD-MAC-Customization/files/GUID-E6429154-36DF-4D84-8ABC-9FCA15B66158.htm
32. https://help.autodesk.com/cloudhelp/2021/ENU/AutoCAD-AutoLISP/files/GUID-75F19C76-78D0-443B-BC39-EB9FEB4650B1.htm
33. https://help.autodesk.com/cloudhelp/2026/FRA/AutoCAD-MAC-AutoLisp/files/GUID-7884190F-4603-4E9F-8FB3-0D683BD7C4C9.htm (search result; not fetched)
34. https://help.autodesk.com/cloudhelp/2018/ENU/AutoCAD-MAC-Core/files/GUID-DB55FE5C-6B51-40AE-AE3D-4C3A28ADC5D9.htm and https://help.autodesk.com/cloudhelp/2018/ENU/AutoCAD-MAC-Customization/files/GUID-5510017F-4656-478F-BD4C-AB6B1998BF55.htm (search results)
35. https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/Cannot-import-STEP-files-in-AutoCAD-for-Mac-2018.html and https://autodesk.com/support/technical/article/Importing-a-STEP-file-into-AutoCAD (both HTTP 403 on fetch; content from search summaries)
36. https://knowledge.autodesk.com/support/autocad-for-mac/learn-explore/caas/CloudHelp/cloudhelp/2019/ENU/AutoCAD-MAC-Core/files/GUID-083880D6-3424-4545-8BB8-6858B86C2532-htm.html (search result; not fetched)

(Numbers 22 and 23 intentionally unused.)

## Verification status

**Verified by fetching the primary page (V):** CadQuery license/formats (1,3); build123d license/formats/projection/ExportDXF (2,4); ezdxf versions, license, no DWG, dimension `render()` (9,10); ezdxf drawing add-on limits (18); ODA File Converter function and platforms (19); LibreDWG license and write limits (21); Text2CAD, CADCodeVerify, CAD-Recode, DeepCAD, Fusion 360 Gallery, ABC facts (5-8,12,13); CONTRAN 882 art. 4 values and several art. 6 lines (24); Res. 1.005/2024 19.30 m (25); Mac programming-interface table (31); "Mac does not support Managed .NET" (32); Zoo page (15, limited content).

**Verified only via search-result summaries (partial):** Zoo STEP/B-rep/KCL (14); Bernini (16); Onshape AI Advisor and FeatureScript MCP (17); ODA SDK pricing (20); revocation of Res. 210 (26); Senatran Portarias 989/990, Res. 916/2022, CAT/CSV/CCT (28,29); Mac SCRIPT command and Terminal switch (34); STEP not importable in AutoCAD for Mac, SAT import (35,36); Mac AutoLISP/ActiveX details (33).

**Unverified / not found:** ODA File Converter license/redistribution terms; commercial terms of OpenSCAD license; whether current AutoCAD for Mac (2026/2027) imports STEP; accoreconsole absence on Mac (no Autodesk statement found); Mac `-b` switch and SAVEAS scripting on current release; Visual LISP `vl-*` non-COM functions on Mac; automatic dimensioning from projections; OCCT HLR and FreeCAD TechDraw details; ezdxf paper-space/layout API details; Lei da Balança (7.408/1985) and 5% tolerance; Res. 211 status from an official source; later amendments of 882 beyond 899/2022 and 1.005/2024; Res. 292/2008 revocation; need for CSV/CCT for your trailer type; ABNT drawing standards; weld symbol and tolerance standards; ART/CREA requirement; trailer-specific AI datasets (none found).

**Caveat on regulation:** values come from the 2021 DOU print of Res. 882 plus Res. 1.005/2024. Confirm against the current consolidated text at gov.br/transportes (CONTRAN resoluções) before relying on any limit in code.
