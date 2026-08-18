# Plano da obra de Galar (Fase E do PRD)

Desenhado pela condutora em 18/08/2026 sobre o reconhecimento medido da
fonte (`fontes-mapas/galar-swsh/`, demake fan-made Ultimate Plus
v1.2.1.2, base FireRed; relatório de medição na sessão desta data).
Documento de referência único da obra: executor não inventa número, tabela
ou id; o que não está aqui ou nos censos gerados volta para cá.

LEMBRETE PERMANENTE: o material é trabalho fan-made de terceiros. Uso
privado; NUNCA publicar sem crédito e permissão. A ROM do demake e a
extração ficam em `fontes-mapas/` (repo local, sem remote), como sempre.

## O que a medição estabeleceu (fatos, não estimativas)

- 438 mapas novos válidos em 44 grupos da fonte; blockdata completo em
  disco (1.264 KB, conferido byte a byte contra as dimensões), formato u16
  FRLG cru (metatile 0-9, colisão 10-11, elevação 12-15; primário até 639,
  secundário 640-1023), NENHUM mapa estoura os tetos do nosso motor.
- Eventos estruturados em disco: 4.640 objetos (4.264 plausíveis), 2.147
  warps (1.510 plausíveis; 637 sujos concentrados), 1.023 coord, 694 bg
  (404 sujos concentrados em 8 mapas), itens escondidos decodificados.
- TILESETS NÃO EXTRAÍDOS: 48 tilesets (~450 KB com tiles LZ77) vivem só na
  ROM do demake; o `renderiza.py` já resolve struct, LZ77 e paletas, falta
  gravar. ATENÇÃO: a ordem dos campos da struct Tileset do FR difere da
  nossa (callback 0x10/atributos 0x14 lá; invertidos aqui).
- Scripts/cenas: só ponteiros (3.209 de objeto + 256 de header). Encontros
  e treinadores DO DEMAKE: não extraídos. Enciclopédia validada em
  `preparados/` (11 líderes, 13 áreas).
- O NOSSO motor já fala FRLG nativamente (`layout_version: "frlg"`, 344
  layouts usam; `frlg_metatile_behavior_converter.py` existe): blockdata
  entra SEM remapear ids de metatile.
- ORÇAMENTO CORRIGIDO PELA CONDUTORA: o reconhecimento usou o espaço do
  ESTADO 0.e (pré-Fase D). Depois do D1+D2+D3 a ROM está em 92,90% com
  ~2,38 MB livres; a Ultimate Plus INTEIRA pede ~1,89 MB. CABE COM DLC,
  folga ~490 KB. A decisão do Gui de 17/08 ("campanha base primeiro")
  fica satisfeita importando tudo de uma vez, com o DLC entrando junto
  porque o custo marginal é geometria já paga.
- Restrição mais dura: GRUPOS DE MAPA. Teto físico 128 (127 usados, 1
  livre, política "não criar grupo novo" do ESTADO relida como "não criar
  À TOA"). 438 mapas exigem alocador.

## Decisões da condutora (18/08/2026)

1. **Escopo geométrico total**: os 438 mapas entram (base + DLC), porque
   cabem. Cenas, treinadores e encontros ficam para a fase de conteúdo
   (fila própria, como o B6 fez com as outras regiões); os líderes usam a
   enciclopédia validada quando a fase de conteúdo abrir.
2. **Alocação de mapas por APPEND em grupos existentes com vaga**, mais o
   grupo livre: o conversor ganha um ALOCADOR que distribui os 438 em
   appends no fim de grupos com espaço (append não renumera nada que
   exista, mesma lei do save), gravando o censo `de-para`
   (grupo/índice da fonte → grupo/índice nosso) que TODA ferramenta
   posterior consome. Nenhum mapa existente muda de id. O grupo livre
   recebe os exteriores principais (legibilidade), o resto empacota.
3. **Tilesets**: extrator novo (`extrai_tilesets_galar.py`) reusando o
   código do renderiza.py, gravando no formato do repo (tiles.png 4bpp,
   metatiles.bin, metatile_attributes.bin FRLG de 4 B, palettes/*.pal),
   com PROVA DE FIDELIDADE: re-renderizar cada mapa a partir do que foi
   extraído tem que reproduzir o PNG de referência pixel a pixel (fora os
   tiles animados, listados). Primários do demake comparados por md5 com
   os FRLG que já temos: idêntico reusa, diferente entra como novo.
   Comportamentos passam pelo conversor FRLG existente. Registro via
   molde do `tileset_gen2.py` (`--registrar`).
4. **Eventos sujos não entram**: a triagem de plausibilidade do
   reconhecimento vira filtro do conversor (posição dentro do mapa,
   trainer_type sadio, warp com destino existente no de-para). O sujo sai
   para um censo `galar_sujeira.json` com motivo por linha, e NÃO vira
   dado de mapa. Warp cuja ponta é mapa inválido/inexistente fica sem
   destino funcional e entra na fila de conteúdo como pendência.
5. **NPCs entram MUDOS** (como Sinnoh fez): tabela de tradução dos 218
   gfx da fonte para `OBJ_EVENT_GFX_*` nossos (`tabela_gfx_galar.py`,
   molde da TROCA_SPRITE; sem gráfico equivalente = sprite padrão,
   documentado). Objeto com script vira NPC mudo com `script "0"`;
   trainer_type sadio fica anotado no censo para a fase de conteúdo.
6. **Itens escondidos** (277 decodificados): entram com flags novas da
   faixa de Galar. FAIXA AUTORIZADA: `0x1C00` em diante (contígua livre
   medida na Fase A, dono anotado em flags.h; ~1.062 endereços até
   0x2025, sobra folga para a fase de conteúdo).
7. **Música**: tabela de tradução dos 34 ids FR para `MUS_*` nossos,
   proposta pelo executor POR PAPEL (cidade, rota, interior, batalha) a
   partir do que o id toca no demake, aprovada pela condutora antes de
   gravar. `music 0` = sem música, fica.
8. **Seções**: as 44 viram `MAPSEC_GALAR_*` (cabem no u8 com folga),
   nomes normalizados (os erros do autor, "Hammmelock", corrigidos para o
   canônico de Galar com nota).
9. **Conexões e borders**: extrator complementa o `mapas.json` com os
   campos que o extrator original descartou (202 conexões, borders,
   borderWidth/Height, ponteiros de map script anotados para a fase de
   conteúdo).
10. **Heal locations**: em append, uma por cidade com Pokécenter
    identificável (warp para interior de Centro + PNG), no molde da Fase
    C. As demais ficam para a fase de conteúdo.
11. **Chapter Jump**: GALAR entra como sexta região do seletor quando os
    ginásios tiverem flag (fase de conteúdo); nesta obra entra só o
    capítulo "Start of region" apontando para o início jogável.
12. **Travessia**: a entrada de Galar liga na `travessia_regioes` (barco)
    na última leva desta obra, atrás de flag de teste até a fase de
    conteúdo abrir, para o Gui poder ANDAR em Galar sem história.

## Blocos executáveis

- **G0, extrator (ferramenta)**: `extrai_tilesets_galar.py` + os campos
  faltantes do mapas.json (conexões, borders, map scripts anotados) +
  filtros de plausibilidade gravando `galar_sujeira.json`. `--demo` =
  prova de fidelidade de render por amostra E a contagem exata dos censos.
- **G1, tilesets**: os 48 convertidos e registrados (`galar_00..`),
  comportamentos convertidos, primários deduplicados contra os FRLG
  existentes. Prova: render de 20 mapas variados pixel-idêntico à
  referência (fora animados).
- **G2, mundo**: alocador roda (de-para gravado), layouts
  `layout_version: "frlg"`, map.bin/border direto do blockdata, headers
  com música traduzida e MAPSEC novas. Build + T20-style caso de
  carregamento por região de amostra.
- **G3, portas e costura**: warps limpos pelo de-para, conexões, heal
  locations em append. Casos de travessia por amostra (warp de ida e
  volta em N mapas medidos).
- **G4, gente e itens**: NPCs mudos pela tabela de gfx, bg events com
  itens nas flags da faixa 0x1C00+, censo de trainer_type para o futuro.
- **G5, entrada e QA**: ligação na travessia atrás de flag, capítulo
  Start of region, suíte da obra (casos por amostra de cada bloco, pares
  negativos), fila de conteúdo de Galar GERADA (o análogo do fila_b6 para
  os 3.209 ponteiros de script anotados), ESTADO e ROMs.

Cada bloco fecha com o ciclo padrão (autor de casos adversarial quando há
conteúdo provável por EWRAM, consertador, fechador com suíte completa;
T11 obrigatório no G2, no G3 e no fechamento). As leis de sempre valem
todas (janela de save, append, faixas com dono, conserto no gerador,
suíte manda).

## Fora desta obra, dito

Cenas, treinadores, encontros, ginásios e Liga de Galar (fase de conteúdo
própria, com fila gerada no G5); decompilador de script do FR (avaliar na
fase de conteúdo se compensa contra porte manual por cena); os 47 headers
inválidos da fonte; o tileset isolado com LZ77 anômalo (investigar no G0 e
reportar).
