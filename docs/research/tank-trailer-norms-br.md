# Brazilian norms for road tank trailers (tanque rodoviario / semirreboque tanque)

Date: 2026-10-10. English with Portuguese terms. Tags: **[V]** verified from a fetched page (URL given), **[V-sec]** verified only on a secondary aggregator or search snippet, **[U]** unverified. ABNT texts are paid; only titles seen on catalog-like pages are listed. Companion to `ai-cad-trailers.md` section 8.1.

## 0. Verdict on "INMETRO Portaria 134/2022"

**The user's memory is correct.** [V-sec: https://www.normasbrasil.com.br/norma/portaria-134-2022_429256.html, full text fetched; aggregator copy of the DOU act, not the gov.br/DOU original. Re-check the official text before relying on article numbers.]

- **What it is:** Portaria INMETRO n. 134, 24/03/2022, DOU 25/03/2022. Approves the consolidated *Requisitos de Avaliacao da Conformidade para Tanques de Carga Rodoviarios Destinados ao Transporte de Produtos Perigosos* (mandatory **certification**, with CTPP per tank).
- **Scope:** road cargo tanks for dangerous goods (produtos perigosos). Tanks not intended for dangerous goods are outside it. Applies to national manufacturers and importers.
- **In force:** effective 01/04/2022. Search found only two retifications, no substantive amendment [V-sec: normasbrasil search results]: 01/09/2022 (certification per family, item 1.1.2 Anexo I) and **28/12/2022 (corrects Anexo H tables of minimum thickness for calotas and costado)**. Amendments after 2024 not checked [U].
- **Replaces:** Portarias INMETRO 175/2006, 16/2016, 38/2018, 144/2019, 128/2021 and Anexo J of 230/2021 (art. 12) [V-sec].
- **Applies to tank trailers:** yes. A semirreboque tanque for dangerous goods carries a "tanque de carga" certified under it; the tank is certified per family, the chassis is not covered (see Portaria 127/2022).

### 0.1 "Anexo H" (the user's hint)
**Exists.** Anexo H = *Tanques de carga destinados ao transporte de liquidos* (Anexo G = gases; E = liquefied chlorine; F = cryogenic; I = PRFV/fiberglass; II = Selo de Identificacao) [V-sec, same page]. Scope: tanks for liquid products of groups 2A-2F, 4A-4E, 7A-7F, 27A1-27A6, 27B, 27C, 27G, 27J, PMTA 690 kPa, carbon steel, stainless steel or aluminium. Base: US CFR-DOT 406/407/412, or ADR if item 2.20 conditions are met. This is the annex that governs a typical fuel/chemical liquid tank trailer, so it is the main design source. What I could read of it:

| Topic (Anexo H) | Content seen | Item |
|---|---|---|
| Design code | ASME Sec. VIII or another code accepted by the OCP; memoria de calculo + memorial descritivo signed by responsavel tecnico with ART | 2.x |
| Data book | specification sheet (~26 items: serial, compartments, volumes, tank type, dimensions, min. thickness, PMTA, tare, operating temp.), material/accessory certificates, welding qualifications, NDT reports | 1.x |
| Plate (placa do fabricante) | manufacturer, serial, build date, standard ref., family, capacity, design and original thickness, tare, PMTA, operating temp., test pressure | marking |
| Materials | listed ASTM steels; Al alloys per ABNT NBR 6834 (5052, 5154, 5254, 5454, 5652, 5083) and ASTM B209 5086; tempers per ABNT NBR 6835 (O, H32, H34) | 2.2 |
| Thickness | min. design thickness must keep stresses within items 2.3.1-2.3.3; **no corrosion allowance counted** toward design; numeric tables are in item 3 and were **not readable** in the fetched text | 2.3, 3 |
| Manhole (boca de visita, BV) | >= 450 mm diameter per tank/compartment; cover withstands 250 kPa (+-2%) or tank test pressure if higher | 2.5.1 |
| Baffles (quebra-ondas) | circular passage opening >= 500 mm, no sharp edges; thickness >= head plate unless calculation justifies; ring stiffener spacing <= 1,524 mm | text |
| Relief | primary opens 120-130% PMTA, recloses >= 108%; secondary opens >= 120%; surge capacity per TTMA RP 81; device marked with maker, model, set pressure, flow, serial | 2.12 |
| Valves | automatic internal or external shut-off on loading/unloading openings; remote closure + thermal activation <= 120 C for flammable/oxidizing/toxic | 2.13 |
| Rollover (capotamento) | fittings in upper 2/3 protected or >= 1.25x as strong; devices resist normal+tangential load >= 2x loaded vehicle weight | 2.10.3 |
| Rear / bottom protection | rear collision protection mandatory; protective device >= 150 mm from protected component (rear and lower third) | 2.10.2, 2.10.4 |
| Test pressure | 2.15.1 reached but its value was not visible | 2.15 |

Not readable in my fetch: item 3 (thickness values), item 2.19 (ADR conditions; was 2.20 before the 01/09/2022 retification), test pressure values, grounding for liquids [U]. Read the official text (DOU/gov.br) to get them; the retification of 28/12/2022 changes those very tables, so use the **retified** version.

Other general points from the Portaria (Anexo I RAC and others) [V-sec]:
- Certification Model 5 (type tests + SGQ audit + periodic surveillance), certificate valid 4 years, **per family** of tanks (same maker and plant), CTPP issued per tank.
- Initial request must include memorial descritivo of representative models, **projetos tecnicos (drawings)**, CAT, ART of designer/technical manager. Anexo B = memorial form; Anexo C = CTPP flow, equipment number, plates; Anexo D = CTPP layout.
- Maintenance audit every 12 months, tests/verifications every 24 months; records kept 3 years paper / 5 years digital.
- Equipment number: stainless plate, 7 characters, digits >= 8 mm high. Selo (Anexo II): stainless >= 2 mm (aluminium seal on aluminium tanks), welded all around near manufacturer's plate; externally clad tanks mount it on the side of the first cradle.
- Registration with INMETRO under Portaria INMETRO 258/2020 (or successor) before using the selo.
- ABNT cited in the Portaria: NBR 6835:2000 (aluminium tempers), NBR 6664:1992 (heavy plate steels), NBR 11767:1986 (nitric acid tanks), NBR NM-ISO 9712:2014 (NDT personnel); the text gave numbers/short names only, titles here are as fetched, not from ABNT.

### 0.2 Check against the user-provided PDF (added after review)
Source: `docs/sources/portaria-inmetro-134-2022-retificacao-2022-09-01-legisweb.pdf` (LegisWeb print, 10/10/2026; text extracted with MarkItDown). **It is only the DOU retification of 01/09/2022** (items 1-7: Anexos I, A, D, E, F, G, H), not the full Portaria and not an official DOU copy [V-sec: LegisWeb aggregator]. What it confirms or changes:
- **Two retifications both touch Anexo H (resolved after the user asked where to find the correct text):** DOU 01/09/2022 (this PDF) and **DOU 28/12/2022** [V-sec: https://www.normasbrasil.com.br/norma/portaria-134-2022_440509.html, fetched via summarizing tool; aggregator]. The 28/12/2022 one corrects Anexo H item 1, **Tables 2, 3, 6, 7** (head/shell minimum thickness by capacity, footnote allowing 3.00 mm in place of 3.28 mm for some bands; Tables 6/7 band edges "33-39, 39-45" become "33-40, 40-45"; MS/HSLA/SS/AL definitions added), and items 3.4.1 and 3.4.3. **The 28/12/2022 values supersede the 01/09/2022 ones below: carbon steel minimum 4.75 mm (not 4.76) and design pressure not less than 175 kPa (not 176).** Stainless 4 mm in 3.4.1 was not shown in the 28/12 extract: re-check. Earlier text of this note saying 28/12 alone corrects the tables, and then that the PDF contradicts it, is superseded by this item.
- **Renumbering of Anexo H:** ADR condition item 2.20 -> **2.19**; relief systems referenced as item **2.12**; grounding **2.18**; circumferential stiffeners **2.7**; baffle spacing 2.3.1.1, 2.3.1.2 and 2.7.2. Item numbers in section 0.1 may be off by one in places: always cite the retified numbering.
- **Values found in the retified text (item 3, specific tank types; which tank type item 3.4 refers to is not visible in the extract) [V-sec]:** [01/09/2022 text, **superseded by 28/12/2022: 4.75 mm and 175 kPa**] minimum shell and head thickness 4.76 mm carbon steel, 4 mm stainless steel (3.4.1); design pressure not less than 176 kPa (3.4.3); vacuum-loading tanks per ASME III Div. 1/2 or XII (3.9.1.3); test pressure **264 kPa** (3.9.1.6, product group 27 A2).
- **Tabela 5 (minimum shell thickness after forming, mm), headers read from a user-supplied screenshot of the table [V-sec, low-resolution rotated text, partly illegible]:** columns are grouped by **volumetric capacity (litros/cm)**: up to 15; above 15 up to 21; above 21 up to 27; above 27. Within each group, sub-columns are by **product density at 15 C (kg/l)**: legible thresholds are "ate 1,2", "acima de 1,2 ate 1,56", "acima de 1,56 ate 1,82" (one cell reads "acima de 1,92", probably 1,82 or a typo in the source). Groups 1 and 2 have 4 density columns, groups 3 and 4 appear to have 3 (4+4+3+3 = 14, matching the 14 extracted values per row). Rows: L = distance between circumferential stiffeners (up to 914; 914-1,372; 1,372-1,524 mm), steel and aluminium.
  - Steel, L up to 914 mm, extracted order: 2.54 3.28 3.99 4.75 | 2.54 3.28 3.99 4.75 | 2.54 3.28 3.99 | 3.28 3.99 4.75. Other rows are in the PDF text.
  - **Exact density class of each column in groups 3 and 4 is not legible: confirm on the official DOU table before coding.** Aluminium row also has a probable typo ("5,75" amid 5.77 values) in the source text. Extracted values are identical before and after the retification, so what changed is unknown.
- Confirms: Anexos E (chlorine), F (cryogenic), G (gases), H (liquids), and ASME VIII / ADR 2021 / CFR-DOT / TTMA RP 81 as cited design bases; ABNT NBR 6835:2000, 6664:1992, 11767:1986, NM-ISO 9712:2014 listed as complementary documents.

## 1. INMETRO family around Portaria 134 (design vs inspection)

| Act | What | Status | Tag |
|---|---|---|---|
| Portaria 134/2022 | certification of the **tank** (construction/design) | in force, retified 2022 | [V-sec] |
| Portaria 127/2022 | OIA **inspection of road vehicles** (cavalo/chassi) for dangerous goods | amended by Portaria 384/2023 and 125/2024 (search snippets) | [V-sec: normasbrasil/lex search results] |
| Portaria 128/2022 | OIA **inspection of road equipment** (bulk tank) for dangerous goods, classes 1,2,3,4,5,6,8,9; ANTT decides if compulsory; Portaria 8/2025 amended its Anexo I; retification 19/09/2022 on item 7.3.4 | in force per snippets | [V-sec: normasbrasil search results; text not fetched] |
| Portaria 445/2021 | descontaminacao of equipment (also cited for tank loads) | amendment under consultation 2024 | [V-sec: snippet; U on current text] |
| Portaria 329/2012 | compulsory inspection of container-tank | pre-2022; status unknown | [U] |

Design/documentation requirements found only for 134 (above); for 127/128 the content was not read [U].

## 2. ABNT NBRs (titles seen on catalog-like pages only)

| NBR | Title as seen | Tag |
|---|---|---|
| NBR 11767 | Tanque de carga para transporte rodoviario de acido nitrico a granel, especificacao (1986) | [V-sec: search snippet + Portaria 134 cites it]; current status [U] |
| NBR 12227 | Inspecao periodica dos tanques de carga utilizados em transporte rodoviario | [V-sec: target.com.br catalog URL title: https://www.target.com.br/produtos/normas-tecnicas/30552/nbr12227-inspecao-periodica-dos-tanques-de-carga-utilizados-em-transporte-rodoviario]; edition/status [U] |
| NBR 16142 | Implementos rodoviarios: escada para veiculo tanque rodoviario | [V-sec: https://normas.com.br/visualizar/abnt-nbr-nm/32682/abnt-nbr16142-implementos-rodoviarios-escada-para-veiculo-tanque-rodoviario]; edition [U] |
| NBR 7500 | Identificacao para o transporte terrestre, manuseio, movimentacao e armazenamento de produtos (ed. 2017) | [V-sec: snippet] marking of vehicle/labels |
| NBR 9735 | Conjunto de equipamentos para emergencias no transporte terrestre de produtos perigosos (ed. 2016) | [V-sec: snippet]; equipment kit, not tank design |
| NBR 6834 / 6835 | Aluminium alloy / temper designations | [V-sec: cited in Portaria 134 Anexo H] |

Not verified, do not use as facts: NBR 14619/14620 (user's guess; unrelated or fixed-tank family, **not checked [U]**), NBR 13999. Tank design itself is by Anexo H (ASME/CFR 49), not a single ABNT construction NBR [V-sec].

## 3. ANTT

- **Res. ANTT 5.947/2021 is revoked.** It was replaced by **Res. ANTT 5.998, 03/11/2022** (DOU 04/11/2022), in force **01/06/2023**; art. 47 revokes 5.947 [V-sec: https://www.lex.com.br/resolucao-antt-no-5-998-de-3-de-novembro-de-2022/ (fetched)]. A later ANTT revision of 5.998 was reported (DOU 29/11, year/number unclear) [U: https://legismap.com.br/conteudos/artigos-e-noticias/antt-conclui-revisao-da-resolucao-sobre-transporte-de-produtos-perigosos]. Check the current ANTT act before coding.
- **Equipment rules (5.998):** bulk equipment must be **certified by an OCP** (**CTPP**) and inspected by an **OIA** (**CIPP**); bulk vehicles get a **CIV**; OCP/OIA accredited by Inmetro (art. 11); bulk products only as listed in CTPP/CIPP (art. 35 VI); signage per product (art. 6); emergency kit outside the cab (art. 8); **certified bulk equipment cannot carry food, medicines, cosmetics or inputs**, limited exception for potable ethyl alcohol (art. 13) [V-sec: lex page, summarized]. Detailed Instrucoes Complementares are on the ANTT site and were not read [U].
- **MOPP** (driver course): not mentioned in the 5.998 text fetched; legal basis (CONTRAN rule) not verified [U]. It concerns the driver, not the drawing.
- The legal chain: Decreto 96.044/1988 gives Inmetro the attestation of vehicles and equipment [V-sec: portaldotransito article in search result; U].

## 4. CONTRAN

- **Res. 882/2021** dimensions/weights and **1.005/2024** (19.30 m): already verified in `ai-cad-trailers.md` section 4.2; apply equally to the tank trailer.
- **Antispray: Res. CONTRAN 888, 13/12/2021** (DOU 22/12/2021); replaced Res. 762/2018 from 03/01/2022. Covers caminhao, caminhao-trator, reboque and semirreboque; requirements in Anexos II-IV; Anexo I defines para-lama and para-barro [V-sec: normasbrasil/legisweb search results; text not fetched]. Phase-in dates and exact wheel-coverage dimensions [U]: read the PDF at https://www.gov.br/transportes/pt-br/assuntos/transito/conteudo-contran/resolucoes/Resolucao8882021.pdf (appeared in search results; not fetched).
- Tank-specific CONTRAN marking (e.g., painel de seguranca, rotulos de risco): governed by ABNT NBR 7500 / ANTT rules, CONTRAN-specific rule not found [U].
- Registration: CAT/Senatran codes (Portaria Senatran 989/990/2022; Res. 916/2022) see `ai-cad-trailers.md` 4.3 [V partial]. Note Portaria 134 itself requires the **CAT** in the certification request [V-sec].
- UN numbers (numero ONU): relevant to **which equipment may carry which product** (CTPP/CIPP list the products), not to drawing geometry [V-sec].

## 5. By cargo

| Cargo | Norm | Effect on equipment | Tag |
|---|---|---|---|
| Dangerous chemicals / fuels (classes 2,3,...) | Portaria 134 + 127/128 + ANTT 5.998 | certified tank, CTPP, periodic inspection | [V-sec] |
| Fuel distribution (combustiveis) | ANP Res. 44/2013 (numbered seals, amostra-testemunha), ANP 898/2022 (sealed compartments, bocais, valvulas), ANP 885/2022 (samples carried in the truck toolbox) | **lacre points** on hatches/valves, toolbox | [V-sec: search snippets, not fetched] |
| Food (liquid, bulk) | ANVISA: RDC 81/2008 chapter XXXI cited in sanitary enforcement decisions; ANTT 5.998 art. 13 bars certified dangerous-goods bulk equipment from food; no approved tank cleaning method per ANVISA decisions | separate food-grade tank (stainless, sanitary design); the specific norm for food tanks **not found** | [V-sec for art. 13; U for sanitary norm] |

## 6. Summary table

| Norm | Issuer | Applies to | Affects drawing/design | Verified |
|---|---|---|---|---|
| Portaria 134/2022 (Anexos H, G, E, F, I, II) | INMETRO | tank of road tanker, dangerous goods | design code, thickness, BV 450 mm, baffle opening 500 mm, relief, valves, plates, selo, rollover/rear guards, data book | V-sec (full text, aggregator) |
| Portaria 127/2022 | INMETRO | chassis/vehicle inspection | inspection items on vehicle | V-sec snippets |
| Portaria 128/2022 | INMETRO | bulk equipment inspection (OIA) | inspection and marks | V-sec snippets |
| Res. ANTT 5.998/2022 | ANTT | transport of dangerous goods | CTPP/CIPP, signage, kit | V-sec (fetched, aggregator) |
| Res. ANTT 5.947/2021 | ANTT | revoked 01/06/2023 | none | V-sec |
| Res. CONTRAN 882/2021, 1.005/2024 | CONTRAN | all semirreboques | width 2.60, height 4.40, 19.30 m | V (see prior note) |
| Res. CONTRAN 888/2021 | CONTRAN | antispray | mudguard/flap geometry | V-sec snippets |
| ABNT NBR 12227, 16142, 7500, 9735, 11767, 6834, 6835 | ABNT | various | inspection, ladder, labels, kit, nitric tanks, Al | V-sec titles only |
| ANP 44/2013, 898/2022, 885/2022 | ANP | fuel tank trucks | seal points | V-sec snippets |
| ANVISA RDC 81/2008 | ANVISA | food transport | food-grade tank | U |

## 7. CAD spec parameters implied

Found in sources (Anexo H, aggregator text, re-check against the official retified text):
- `codigo_projeto` (ASME VIII or accepted), `PMTA_kPa` (<= 690 for Anexo H), `material` (steel grade / Al alloy per NBR 6834, temper per 6835).
- `boca_visita_dn >= 450 mm` per compartment; `bv_tampa_teste_kPa >= 250`.
- `quebra_onda_abertura_dn >= 500 mm`; `quebra_onda_espessura >= espessura_calota`; `espacamento_reforco_anel <= 1524 mm`.
- `alivio_primario_abre = 120-130% PMTA`, `reseat >= 108%`, `alivio_secundario >= 120%`.
- Valves: automatic shut-off; remote + thermal (120 C) for flammable/oxidizing/toxic.
- Protections: rollover (load >= 2x loaded weight), rear guard, lower-third protection, offsets >= 150 mm.
- Plate fields (see section 0.1) and `numero_equipamento` (7 chars, >= 8 mm digits), selo (SS >= 2 mm, welded all around).
- `familia_tanque`, data book list, ART/CAT references.
- Volume from geometry (capacidade) and CONTRAN limits from the other note.

**Needs the official text or paid NBR:** minimum shell/head thickness tables (Anexo H item 3 / Tabela 5, column headings; see 0.2 for the retification-date conflict), test pressure (2.15), ADR item 2.20, grounding, NBR 16142 ladder dimensions, NBR 12227 inspection intervals, NBR 7500 label/panel sizes, CONTRAN 888 mudguard geometry, ANTT Instrucoes Complementares sign/panel details, MOPP legal basis. Also confirm current status of 5.998 amendments and Portaria 134 after 2024.

## Sources

- https://www.normasbrasil.com.br/norma/portaria-134-2022_429256.html (fetched; text of Portaria 134 with Anexos; aggregator)
- https://www.normasbrasil.com.br/norma/portaria-128-2022_429255.html, https://www.normasbrasil.com.br/norma/portaria-127-2022_429253.html (search results only)
- https://www.lex.com.br/resolucao-antt-no-5-998-de-3-de-novembro-de-2022/ (fetched)
- https://www.normasbrasil.com.br/norma/resolucao-888-2021_424907.html (search result)
- https://www.target.com.br/produtos/normas-tecnicas/30552/nbr12227-inspecao-periodica-dos-tanques-de-carga-utilizados-em-transporte-rodoviario ; https://normas.com.br/visualizar/abnt-nbr-nm/32682/abnt-nbr16142-implementos-rodoviarios-escada-para-veiculo-tanque-rodoviario (search results)
- https://www.normasbrasil.com.br/norma/resolucao-50-2014_274427.html etc. for ANP: ANP 44/2013 PDF https://www.brasilpostos.com.br/wp-content/uploads/2014/02/RESOLUO-N-44.pdf (search result)
- ANVISA decisions: https://bibliotecadigital.anvisa.gov.br/jspui/bitstream/anvisa/15176/1/Decis%c3%a3o_2140600.pdf (search result)
- Not reached: gov.br/inmetro and in.gov.br originals; abntcatalogo.com.br (not searched directly).
