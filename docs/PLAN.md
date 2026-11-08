# Plano v2 (08/11/2026)

Projeto Hephaestus, no repositório AutoCADKI (decisão do Enzo, 08/11/2026: continuar no AutoCADKI).

Revisado por Maria (CEO), Do Contra e Operations Planner em 08/11. A v1 anterior está no histórico do git.

## Objetivo

O Nonno (engenheiro de carretas) faz o trabalho dele com o próprio Claude; o Enzo fica só como suporte. Série de portfólio "AI for real work".

## Prova de que funciona (critério do Do Contra)

Um desenho real, do tipo de carreta que ele mais faz, de ponta a ponta e assinado por ele, em até 3 semanas depois do início, com o tempo dele medido antes e depois.

## v1: só a Camada 1 (assistente)

Fluxo:
1. **Gatilho:** chega pedido ou croqui (Gmail/WhatsApp) e ele pede ao Claude.
2. **Tabela:** o Claude monta a tabela (campo | valor | origem: engenheiro, documento ou SUPOSTO). Ilegível vira "?" e pergunta; nunca chuta. SUPOSTO bloqueia o desenho.
3. **Conferência:** ele aprova ou corrige; nada é desenhado sem o "ok" dele.
4. **Saída:** DXF 2D + 3D (STEP e prévia GLB/imagens) + lista de materiais, com carimbo "NÃO ASSINADO". Ele assina. DWG nativo fica fora da v1 (ODA US$ 3.000/ano).
5. **Fora da v1:** tipo de carreta diferente do escolhido gera aviso e recusa.

Skills (no máximo 5, cada uma com critério de pronto):
- `receber-pedido`: anexo salvo na pasta do projeto, nada enviado; pronto = arquivo na pasta + resumo do pedido.
- `ler-croqui`: croqui → tabela; pronto = todo campo com origem, testado em 10 croquis com medidas conhecidas, acerto por campo medido.
- `conferir-tabela`: pronto = "ok" registrado + diff original × corrigido + pergunta de consentimento.
- `gerar-desenho`: tabela aprovada → DXF 2D + 3D de 1 tipo. O 3D sai em STEP (para CAD) e em prévia visual (imagem em 4 vistas e arquivo GLB que abre no navegador e no celular), como já fazia a skill desenho-cm do AutoCADKI. Pronto = o DXF abre no AutoCAD, cada cota bate com a tabela e a prévia 3D mostra a mesma carreta. Reaproveita os presets e o núcleo do AutoCADKI (não recomeça do zero).
- `lista-materiais`: pronto = a soma bate com a tabela.

Suporte sem gargalo: o Enzo fica fora do caminho do pedido. Um canal só para travas e revisão do log de falhas uma vez por semana (domingo, 30 min a 1 h). Se o Enzo estiver fora, o Nonno trabalha como hoje.

## Dados e consentimento (antes de tudo)

- O Nonno e a fábrica concordam sobre o que vai para a nuvem do Claude; os desenhos antigos podem ser da fábrica, não dele.
- Cada correção vira um par (croqui, valor do Claude, valor corrigido). Consentimento por projeto, padrão NÃO, revogável, sem nome de cliente. Fica em `local/`, fora do git.

## Cortado da v1 (volta com dados)

- Camada 2 (ML): volta quando houver pelo menos 30 croquis corrigidos de verdade; a linha de base continua sendo o Claude sem treino. Classificação e previsão do próximo passo saem.
- Orçamento, organizar pastas, DWG nativo e a ambição de produto para outras fábricas.

## Agenda (Maria)

- Nada antes de 19/11 (provas até 13/11, entregas 17-18/11).
- Lynceus (m9) continua sendo o projeto principal de ML até 13/12; o Hephaestus é o assistente da m8, com 1 h de suporte por semana.
- Risco nomeado: 8 projetos e ideias abertos em 48 h. Escolher 2 frentes ativas depois de 19/11.

## Próximos passos

1. **Até 15/11:** o Enzo descreve para a Maria, em 5 linhas, o dia normal do Nonno e os tipos de arquivo que ele recebe. Não precisa instalar nada nem falar com ele.
2. **Depois de 19/11:** consentimento do Nonno e da fábrica; escolher 1 tipo de carreta e 10 croquis antigos com as medidas conhecidas, guardados em `local/`.
3. Depois: as skills `ler-croqui` e `conferir-tabela`, testadas nos 10 croquis.

## Não verificado

- Conector oficial de WhatsApp e de Gmail no Claude desktop.
- Custo da assinatura.
- Se a fábrica autoriza a nuvem.
- Quem é dono dos desenhos antigos.

## Referências

- Prior-art: ~/OpenBot/Shared/Transfers/boss/2026-11-08-hephaestus-prior-art.md. Construir o núcleo de carreta; adotar CadQuery/build123d e ezdxf; adaptar o FreeCAD TechDraw; ODA só com receita; Backflip AI é o concorrente mais próximo.

## 3D com Blender (Enzo, 08/11/2026)

Duas peças, cada uma no que faz melhor (o mesmo caminho da skill desenho-cm do AutoCADKI, testado em 19/10):
1. **Geometria de engenharia:** build123d (Apache-2.0), 1:1 em mm, a partir da tabela aprovada, exportando STEP (CAD) e GLB.
2. **Apresentação:** Blender 5.2 (GPL, instalado em /Applications/Blender.app) importa o GLB e gera materiais, luz, imagens das vistas, turntable e vídeo de apresentação. Controle pelo MCP oficial do Blender Lab v1.0.3 (fixado; o pacote PyPI `blender-mcp` é outro projeto, não usar).

Regras: o Blender não é fonte de medida (só mostra); antes do render, a caixa delimitadora e as posições de eixo do modelo batem com a tabela; o MCP do Blender roda Python sem trava, então só trabalha em arquivos novos em `local/`. Alternativa sem Blender: prévia GLB direto no navegador.

## Criação de peças no Mac (prior-art, 08/11/2026)

O Enzo queria SolidWorks, mas precisa rodar no Mac. O SolidWorks desktop só roda em Windows x86_64; o Parallels é suportado, mas Apple Silicon não está confirmado na página oficial.

Decisão: **adaptar**.
- **A IA gera as peças:** build123d (gumyr/build123d, Apache-2.0, ★3,6k) pelo plugin text-to-cad 0.8.3 (earthtojake/text-to-cad, MIT, ★25,8k), já instalado e usado no AutoCADKI. Saída STEP/GLB/DXF.
- **O engenheiro edita as peças:** FreeCAD 1.1.4 (grátis, nativo no Apple Silicon, Python, TechDraw para a prancha 2D cotada) com o FreeCAD MCP (neka-nat/freecad-mcp, MIT, ★3,2k, push em 07/11/2026) para a IA abrir e ajustar o modelo junto com ele.
- **Alternativa paga:** Onshape Standard (US$ 1.500 por usuário/ano, no navegador, REST API + FeatureScript; o plano grátis é não comercial e público).
- **Descartados:** SolidWorks desktop (Windows), Alibre (Windows), Plasticity (sem histórico paramétrico), Shapr3D (sem API).

Não verificado: DXF/DWG de desenhos no Onshape e no Fusion; planos do Onshape com acesso à API; o preço comercial do SolidWorks e do xDesign; o FreeCAD MCP rodando nesta máquina. Instalar exige o sim do Enzo.

### Instalado (08/11/2026, com o sim do Enzo)
- FreeCAD 1.1.4 (Homebrew cask) em /Applications/FreeCAD.app.
- Add-on FreeCADMCP de neka-nat/freecad-mcp@ec8abf21 em ~/Library/Application Support/FreeCAD/v1-1/Mod/ (servidor RPC só em 127.0.0.1 por padrão; acesso remoto desligado).
- `.mcp.json` local (fora do git): `uvx freecad-mcp==0.1.30`.
- Teste: chapa 300x200x6 com 4 furos de 18 mm gerada no freecadcmd; volume 353.892,7 mm3 = conta esperada; STEP em local/teste/ (fora do git).
- Falta: ligar o add-on no FreeCAD (workbench MCP Addon > Start RPC Server) e testar o MCP numa sessão do Claude aberta no repo.
