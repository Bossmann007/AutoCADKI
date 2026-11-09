# AutoCADKI · Hephaestus


Hefesto, o deus ferreiro que forjava carros e máquinas. Este projeto transforma o croqui ou a foto de uma carreta em desenho técnico pronto (DWG/DXF 2D e modelo 3D), com IA.

Parte do portfólio de engenharia de IA do Enzo Bossmann: **AI models for real work**. O nome do projeto é Hephaestus; o repositório continua sendo o AutoCADKI. Contexto técnico em `PROJECT.md`, plano em `docs/PLAN.md`.

## O problema

Um engenheiro de carretas (o primeiro usuário é o avô do Enzo) desenha à mão e precisa do desenho técnico no AutoCAD. Hoje isso é trabalho manual de horas.

## Fluxo da v1

1. **Entrada:** foto do croqui, ditado ou tabela de medidas.
2. **Leitura:** um modelo de IA extrai as medidas para uma especificação estruturada (JSON validado).
3. **Conferência obrigatória:** o engenheiro confere a tabela de medidas antes de desenhar. Nada é desenhado sem esse sim.
4. **Geração:** a especificação vira geometria paramétrica (código, não imagem) e sai em DXF/DWG 2D e STEP 3D.
5. **Revisão:** o engenheiro assina; a IA nunca assina nem certifica.

## Produto

Depois do primeiro usuário, a ferramenta vira produto para fábricas de carreta (ver `docs/PLAN.md`).

## Regras

- Toda medida vem do engenheiro ou do documento; o que a IA supõe fica marcado "SUPOSTO".
- Arquivos de projeto de clientes (STEP, DWG, fotos) nunca vão para o git.
- O cálculo estrutural e as normas são responsabilidade do engenheiro.

## Fluxo de trabalho (2D → 3D → render)

1. **Tabela de medidas** com a origem de cada valor (engenheiro, documento ou SUPOSTO). O engenheiro confirma antes de qualquer desenho (gate da skill `desenho-cm`).
2. **2D:** script em `local/<projeto>/` com CADCraft gera DXF/DWG. As imagens e PDFs para o usuário saem em fundo branco com `.claude/skills/desenho-cm/scripts/white_export.py`.
3. **3D:** modelo build123d em `local/<projeto>/3d/`, gerado com `cadgen run <modelo>.py` (STEP para CAD, GLB para o Blender).
4. **Checks do modelo:** `cadgen run local/<projeto>/3d/checks/check_*.py` (medidas contra a tabela) e `checks/interference.py` (peças se atravessando). Exit 0 antes de renderizar.
5. **Render:** Blender 5.2 com o MCP oficial (`open -a /Applications/Blender.app --args --online-mode`), sempre em arquivos novos dentro de `local/`.

Quando o pedido é "deixar igual" a fotos ou renders de referência: recortar cada parte da referência, montar a tabela, ter o ok do usuário e comparar sempre com a câmera no mesmo ângulo de cada foto.

### Casar a câmera com a foto (fSpy)

Instalado em 2026-11-09 no Mac do projeto:
- **fSpy 1.0.3** (`/Applications/fSpy.app`, GPL-3.0, [stuffmatic/fSpy](https://github.com/stuffmatic/fSpy)). É um app Intel: precisa do Rosetta (`softwareupdate --install-rosetta --agree-to-license`).
- **Importador fSpy-Blender 1.0.3** ([stuffmatic/fSpy-Blender](https://github.com/stuffmatic/fSpy-Blender)), add-on `fspy_blender` ativado no Blender. Feito para o 2.8, testado no Blender 5.2.3 (câmera, campo de visão e resolução corretos).

Por foto de referência:
1. Abrir a foto no fSpy, pôr as linhas de fuga sobre arestas paralelas (comprimento e largura) e marcar uma medida conhecida em "Reference distance".
2. Salvar em `local/<projeto>/refs/<foto>.fspy` (fora do git).
3. No Blender: File → Import → fSpy, ou `bpy.ops.fspy_blender.import_project(filepath=...)`. Cria a câmera da foto com a foto de fundo.
4. Modelar e comparar por essa câmera; antes de dizer "pronto", salvar `local/<projeto>/compare/<peça>_vN.png` com o recorte da foto e o render lado a lado.

Peça comprada (lanterna, para-lama, válvula): pedir o modelo ou a ficha técnica do fabricante, ou uma foto de frente com trena, antes de modelar.

## Como verificar

- `scripts/verify`: exit 0 = os testes passaram, nenhum arquivo de cliente está versionado (exceto as normas públicas em `docs/sources/`) e, nesta máquina, todos os checks de `local/*/3d/checks/` (check_*.py e interference.py) passaram. Sem `local/`, esses checks são pulados.
