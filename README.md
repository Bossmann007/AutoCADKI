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

## Como verificar

`scripts/verify` (exit 0 = os testes passaram e nenhum arquivo de cliente está versionado (exceto as normas públicas em `docs/sources/`)).
