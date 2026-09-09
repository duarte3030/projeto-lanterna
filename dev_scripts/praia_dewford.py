#!/usr/bin/env python3
"""Refino de `DewfordTown` (tema PRAIA E PESCADOR), no `gTileset_Dewford`, com os
móveis de cais importados do `Pokémon Light Platinum`.

O QUE ESTA CIDADE TEM DE ERRADO, medido pela `dev_scripts/regua_cidades.py` nesta
árvore em 09/09/2026: das 212 células andáveis a pé, **145 (68,4%) são o metatile
292**, a areia lisa do `gTileset_General`, e **32 (15,1%) são o metatile 569**, o
arbusto do `gTileset_Dewford` plantado sobre a MESMA areia. Os dois juntos comem
83,5% do chão. É o segundo pior carimbo das quatro regiões e o defeito é literal:
a ilha do Brawly é um tapete de areia chapada com quatro prédios em cima.

DOIS CARIMBOS, e o segundo não pode ser ignorado. A régua mede o DOMINANTE, e
solidificar célula TIRA do denominador: derrubar só o 292 chega a SUBIR a fração
do 569. As duas famílias são tratadas juntas, cada uma com o próprio catálogo, o
próprio atributo e as próprias bolhas.

    carimbo    metatile  atributo  células  elevações
    areia           292    0x1021      145  3 (145)
    moita           569    0x0021       32  3 (32)

OS DOIS ATRIBUTOS NÃO SÃO ESCOLHA DESTA PASSADA. `0x1021` é `MB_SAND` com
`layerType` COVERED e `0x0021` é `MB_SAND` com `layerType` NORMAL, que é o que o
Emerald carimbou nas 177 células, e o portão 4 do `portao_planta.py` cobra
`(behavior, layerType)` idêntico em toda célula que continua andável. Portanto
TODA variante de areia sai com `0x1021` bit a bit e TODA variante de moita sai
com `0x0021` bit a bit. A diferença entre os dois não é decoração: NORMAL manda a
camada de cima para o BG1, ACIMA do boneco, que é justamente o que faz o jogador
passar ATRÁS da folhagem do arbusto; COVERED põe as duas camadas abaixo dele.
Trocar um pelo outro não quebraria build nenhum e apareceria só dentro do jogo.

AS VAGAS DE TILE 170 A 175 SÃO INTOCÁVEIS, e esta passada não escreve uma delas.
`src/tileset_anims.c` (`QueueAnimTiles_Dewford_Flag`) copia 6 tiles da bandeira
para `NUM_TILES_IN_PRIMARY + 170` em tempo de execução e não sabe de
renumeração. O `compacta_tileset.py` é ciente dos pinos pelo `pinos_anim.py`, e a
compactação desta passada foi conferida DEPOIS: as seis vagas continuam byte a
byte iguais às de antes. ACHADO DE LADO, e ele é anterior a esta passada: NENHUM
metatile do `gTileset_Dewford` referencia os tiles 170 a 175 (conferido varrendo
os 379 metatiles), ou seja a animação da bandeira já escreve hoje em VRAM que
nenhum metatile pede. O que esta passada garante é que ela não PIOROU: as vagas
estão onde estavam, com o mesmo conteúdo.

A COMPACTAÇÃO VEIO ANTES DE TUDO, e ela é o que paga o orçamento. O
`gTileset_Dewford` estava em 512 de 512 tiles, e 331 deles eram MORTOS (nenhum
metatile os referencia). `compacta_tileset.py gTileset_Dewford --aplicar` desceu
o arquivo para 192 tiles e devolveu 320 vagas, e a prova é de PIXEL: os seis
mapas irmãos foram renderizados antes e depois e a diferença é ZERO em
102.400 + 819.200 + 409.600 + 307.200 + 230.400 + 129.024 pixels.

A FONTE, e a triagem que decidiu o desenho. Foram medidos, por folha de contato
(`fontes-mapas/romhacks/ferramentas/folha_tema.py`), os secundários de seis hacks
de base Emerald com arte de praia e porto: `scorched-silver`, `mega-emerald-x-y`,
`x-y-emerald`, `run-and-bun`, `light-platinum` e `golden-glazed`. O resultado
partiu a decisão em duas:

  - PARA O CHÃO NÃO ENTRA NADA DE FORA, e o motivo é o mesmo de Hearthome: o que
    a areia precisa é de VARIAÇÃO, não de outra areia. O nosso `gTileset_General`
    tem 35 tiles 8x8 pintados só com os quatro índices de areia da paleta 5
    (11 a 14), e seis deles são textura de verdade que casa com praia: o `0x02` e
    o `0x03` (areia grossa manchada), o `0x81` (cascalho claro), o `0xD5` (sulco
    horizontal, que lê como marca de maré) e o `0x1F0` e o `0x1F2` (faixa de
    transição clara para escura). As DEZESSEIS variantes desta passada saem
    desses seis mais os dois do próprio carimbo (`0x108` e `0x118`), por espelho
    e por mistura de quadrante, e custam ZERO tile, ZERO cor e só uma vaga de
    metatile cada. Medido: elas ficam de 15,0 a 35,8 de distância pixel a pixel
    do carimbo, de 13,0 a 35,1 de cor, e o par MAIS PRÓXIMO entre duas delas está
    a 8,5, acima do piso de 8,0 que o `varia_carimbo.py` documenta como
    "invisível em jogo".
  - PARA OS MÓVEIS DE PESCADOR NÃO EXISTE FONTE NOSSA. Conferido no atlas dos
    379 metatiles do `gTileset_Dewford` e nos 512 do `gTileset_General`: não há
    uma boia, um tambor, um balde nem um quadro de avisos de cais em lugar nenhum
    dos dois. O que há é pedra, pedregulho, moita, árvore, poste, mourão e cerca
    de cais, e esses OITO são NOSSOS e custam zero. Os SEIS de pescador vêm do
    `Pokémon Light Platinum`.

O QUE FOI REPROVADO POR NÚMERO, e o número está aqui porque reprovar medindo vale
mais do que importar peça que não casa:

  - O RESORT DE PRAIA DO `scorched-silver` (secundário `0x492AD4`, o mapa g00m15,
    60x50), que é a peça mais bonita da triagem inteira: coqueiro, guarda-sol
    aberto em três cores e espreguiçadeira, tudo em base Emerald. O coqueiro dele
    é um bloco 2x2 e o topo dele tem atributo `0x0021`; o nosso carimbo é
    `0x1021`. Para a linha de cima continuar ANDÁVEL ela teria que herdar o
    `0x1021` do carimbo, e aí a copa desenharia ABAIXO do boneco, ou seja o
    jogador andaria NA FRENTE da folhagem em vez de atrás. A saída seria
    solidificar as QUATRO células, e numa cidade de 212 células andáveis cada
    coqueiro custaria 4 do denominador da régua por cópia. Ficou de fora, e o
    guarda-sol junto: Dewford é a ilha do ginásio de luta e da Granite Cave, não
    uma estação balneária, e espreguiçadeira ao lado do dojo do Brawly lê como
    outro mapa.
  - O CALÇADÃO BEGE do próprio Light Platinum, sempre. A camada de baixo dos sete
    móveis é o piso do hack, e ele é achado por EVIDÊNCIA e não por constante:
    todo padrão de camada de baixo que aparece em 4 ou mais metatiles diferentes
    da fonte é piso dela, e camada de baixo que repete o mesmo tile nos quatro
    quadrantes também é. Cada móvel recebe o NOSSO chão entrada por entrada.
  - O METATILE 20 DO NOSSO PRIMÁRIO, que a primeira lista trazia como "caixa de
    madeira". Ele é feito dos tiles 213 e 229, e o 213 é EXATAMENTE o tile de
    sulcos horizontais que esta passada usa como "areia ondulada". A mesma arte
    não pode ser marca de maré no chão e engradado sólido ao lado: ou é uma coisa
    ou é a outra. Ficou a marca de maré, que é o que a praia pede.
  - OS METATILES 508 E 509 do primário ("mato de duna"), que passam na cor (39,3
    e 39,5 de distância) e reprovam no OLHO: a arte da camada de cima deles é a
    METADE DE BAIXO de um arbusto que mora na célula acima, então solta na areia
    ela vira um borrão verde grudado na borda de cima da célula. No lugar deles
    entra a moita 514, que é redonda e fecha sozinha.

OS MÓVEIS IMPORTADOS, do `Pokémon Light Platinum`, de WesleyFG, base Ruby (AXVE),
md5 `7fd2c08735459d99fa23fdaa9b755486`. O par é o primário de exterior
`0x286CF4` com o secundário costeiro `0x286D54`, o mesmo que o
`costa_sandgem.py` e o `orla_sunyshore.py` já usaram, e as peças são as SEIS de
cais e pesca:

    boia no suporte  local  17     boia deitada      local 127
    balde            local 374     poste do cais     local 391
    tambor           local 382     quadro de avisos  local 395

O ORÇAMENTO DE PALETA fechou em DUAS vagas, e não por sorte: a arte dos sete mora
nas paletas 0 e 1 do hack, e a camada de baixo deles (o calçadão) mora na 9, que
esta passada joga fora. Medindo por metatile VIVO (os que aparecem em `map.bin`
de algum dos SEIS layouts do tileset), as vagas 6, 7, 10, 11 e 12 do
`gTileset_Dewford` estão 100% livres: nenhum pixel que chega à tela pinta com
elas. A armadilha 4 do `compacta_paletas.py` (metatile do PRIMÁRIO alcançável
pintando com vaga de secundário) foi conferida e dá ZERO aqui. Vão DUAS: a
paleta 0 do hack para a vaga 6 e a paleta 1 para a vaga 7. Sobram a 10, a 11 e
a 12 inteiras.

AS REGRAS DE MONTAGEM, e a armadilha que cada uma resolve:

  - CHÃO DE AREIA é metatile com arte só na camada de BAIXO e atributo IGUAL, bit
    a bit, ao do 292 (0x1021).
  - CHÃO DE MOITA troca o DESENHO do arbusto e não a areia de baixo dele, com o
    atributo do 569 (0x0021), e essa escolha é medida: o arbusto acende 202 dos
    256 pixels da célula, então trocar só a areia move a imagem de 3,3 a 7,8
    pixel a pixel, abaixo do piso de 8,0. A única variante que passa é a moita
    redonda do metatile 514, a 94,9 de distância. É a única família desta passada
    que desenha acima do boneco, e ela já fazia isso antes: é o "jogador atrás do
    mato" do jogo base. Mesmo assim ela paga o portão E3 (a arte de cima não pode
    tapar a célula inteira) e o portão da camada de baixo CHEIA, porque
    `METATILE_LAYER_TYPE_NORMAL` desenha LIXO no BG3.
  - MÓVEL é célula que vira SÓLIDA: a arte vai na camada de CIMA, a de baixo
    recebe o NOSSO chão de areia entrada por entrada, e o atributo é
    comportamento ZERADO com layerType COVERED (0x1000).
  - MÓVEL DE PRAIA ENCOSTA EM ALGUMA COISA: ou num sólido, ou na água, ou na
    moita. Boia solta no meio do areal lê como erro de mapa, e é a mesma razão
    pela qual o guarda-sol saiu de Sandgem.
  - QUADRANTE DE BAIXO SOBE quando o de cima está vazio, que é a regra do
    `porto_canalave.py`.
  - A MANCHA É BOLHA, não sal e pimenta, e o auto-teste prova isso comparando o
    tamanho médio do pedaço conexo com o de uma sabotagem que espalha as MESMAS
    células ao acaso.
  - Nenhum id de flag, var, script, música, treinador ou espécie é importado. Só
    ARTE.

A BEIRA DO MAR NÃO É TOCADA, e isso é medido e não prometido: a família de areia
é filtrada por comportamento (`enfeita_cidades.agua()`), então nenhuma célula de
água entra no catálogo, e o `portao_planta.py` cobra o alcance a pé pelos dois
portões. O alcance de Surf depende da célula de água e da elevação, e as duas
ficam intactas por construção: esta passada só escreve nos 10 bits baixos
(metatile) e no bit de colisão, nunca nos 4 bits de elevação.

Uso:
    python3 dev_scripts/praia_dewford.py                  # mede e mostra o plano
    python3 dev_scripts/praia_dewford.py --aplicar        # escreve tileset e mapa
    python3 dev_scripts/praia_dewford.py --desfazer       # devolve o map.bin
    python3 dev_scripts/praia_dewford.py --demo           # auto-teste
    python3 dev_scripts/praia_dewford.py --extrai         # regera o kit da ROM
    python3 dev_scripts/praia_dewford.py --so-tileset     # so o tileset, sem mapa
    python3 dev_scripts/praia_dewford.py --prova-tiles    # o kit contra a ROM

O PLACAR desta passada, medido nesta árvore em 09/09/2026: 148 células escritas,
12 delas solidificadas, 136 de mancha; a régua cai de 68,4% para 10,5% (o carimbo
292 vai de 145 para 8 células de 200 andáveis e o dominante passa a ser o 569,
com 21) e o `liso3` de 86,8% para 23,5%; metatiles distintos de 81 para 110; 16
tiles novos (vagas 192 a 207 de 512, sobram 304), 31 metatiles novos (locais 379
a 409, ids 891 a 921) e duas vagas de paleta, a 6 e a 7, com 10 cores cada. A ROM
ENCOLHE 1.248 bytes (31.563.764 para 31.562.516), porque a compactação devolveu
mais espaço do que este kit gastou.
"""
import collections
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")
os.environ.setdefault("REPO_MAPAS", RAIZ)
import arte_ginasios_sinnoh as G     # noqa: E402
import enfeita_cidades as E          # noqa: E402

# O `enfeita_cidades.py` PULA o proprio bloco de teste quando varre os corredores
# que a suite anda, e a razao e circularidade: o bloco desta passada e derivado DO
# desenho, e nao o contrario. Aqui o bloco proprio e o 213.
BLOCO_PROPRIO = "213_praia_dewford.json"
E.BLOCO_PROPRIO = BLOCO_PROPRIO

ALVO = "DewfordTown"
DESTINO = f"{RAIZ}/data/tilesets/secondary/dewford"
KIT_JSON = f"{RAIZ}/dev_scripts/praia_dewford_kit.json"
PLANO = f"{RAIZ}/dev_scripts/praia_dewford.json"

PRIMARIO = "gTileset_General"
SECUNDARIO = "gTileset_Dewford"
# Os SEIS layouts vivos que dividem o `gTileset_Dewford`. Conferido lendo
# `data/layouts/layouts.json` e testando a existencia do `map.bin` em disco.
IRMAOS = ["DewfordTown", "Route105", "Route106", "Route107",
          "BirthIsland_Exterior", "NavelRock_Exterior"]

TETO_TILES = 512
TETO_META = 512
TILE_LOCAL_0 = 192          # o tiles.png tem 192 tiles depois da compactacao
META_LOCAL_0 = 379          # o maior local usado nos seis mapas e o 378
PINOS_ANIM = set(range(170, 176))   # a bandeira; NUNCA escrever aqui
MARGEM = 1                  # celulas de folga em relacao a borda do mapa
TETO_REGUA = 20.0           # o alvo desta onda: carimbo dominante <= 20%
TETO_COR = 42.0             # distancia de cor media aceita entre chao novo e carimbo
PISO_VARIANTE = 8.0         # distancia pixel a pixel minima entre duas variantes
# Quanto uma projecao simples da posicao pode acertar a peca ALEM do chute cego
# antes de a mancha virar "padrao". Aqui o corte e 12,0% e nao os 8,0% de
# Sunyshore, e o motivo e o TAMANHO: Dewford tem 20x20 e a mancha inteira cabe em
# menos de 110 celulas, entao "x mod 7" tem 15 celulas por classe e o ruido
# amostral sozinho ja passa de 8%. Medido nesta cidade com as bolhas desta
# passada, no plano de verdade e nas tres sabotagens de padrao.
PISO_PADRAO = 0.12
PISO_MANCHA = 60            # abaixo disso a passada nao fez o servico
ESPACO_ENTRE_MOVEIS = 2     # Chebyshev minimo entre dois moveis QUAISQUER
PISO_BOLHA = 3              # tamanho minimo de uma bolha que a regiao cortou

N4 = E.N4

CARIMBOS = dict(areia=292, moita=569)
ELEVACOES = dict(areia={3}, moita={3})
PAL_AREIA = 5               # a vaga de paleta que o carimbo 292 usa

# ------------------------------------------------------------------- a FONTE
LP = dict(slug="light-platinum", hack="Pokemon Light Platinum", autor="WesleyFG",
          md5="7fd2c08735459d99fa23fdaa9b755486", base="Ruby (AXVE)",
          pri=0x286CF4, sec=0x286D54, split=(512, 512, 6))

# PALETA DE ORIGEM -> VAGA NOSSA. Só as duas do hack em que a arte dos sete
# móveis mora. Quadrante pintado com qualquer outra paleta da fonte é
# DESCARTADO e recebe o nosso chão.
VAGAS_PAL = {0: 6, 1: 7}

# Quantos metatiles DIFERENTES da fonte precisam repetir o mesmo PADRAO de camada
# de baixo para ele ser piso dela. O mesmo corte de 4 que o `costa_sandgem.py`
# mediu neste mesmo secundario.
PISO_MIN = 4

# ------------------------------------------------------------------ o CHÃO
# Cada variante e um metatile NOVO no `gTileset_Dewford` cujos quatro quadrantes
# apontam para tile do NOSSO primario, na paleta 5, com os bits de espelho ditos
# aqui. Custo: ZERO tile, ZERO cor, uma vaga de metatile cada.
#
# O CARIMBO 292 e `[264, 280, 280, 264]` sem espelho nenhum: o 264 e areia chapada
# (os 64 pixels no indice 12) e o 280 e a mesma areia com nove pixels de salpico.
# A "base" das variantes de um quadrante so espelha o 280, e isso ja e variacao de
# graca: o 264 e uniforme e espelho nele nao muda um pixel.
BASE_Q = [(264, 0, 0), (280, 1, 0), (280, 0, 1), (264, 1, 1)]


def _u(t):
    return [(t, 0, 0), (t, 1, 0), (t, 0, 1), (t, 1, 1)]


def _h(t):
    return [(t, 0, 0), (t, 1, 0), (t, 0, 0), (t, 1, 0)]


def _d(t):
    return [(t, 0, 0), (280, 1, 0), (280, 0, 1), (t, 1, 1)]


def _a(t):
    return [(264, 0, 0), (t, 1, 0), (t, 0, 1), (264, 1, 1)]


def _n(t):
    return [(t, 0, 0), (t, 0, 0), (t, 0, 0), (t, 0, 0)]


def _y(a, b):
    """A metade de CIMA com uma textura e a de BAIXO com outra."""
    return [(a, 0, 0), (a, 1, 0), (b, 0, 1), (b, 1, 1)]


def _x(a, b):
    """As duas texturas na DIAGONAL."""
    return [(a, 0, 0), (b, 1, 0), (b, 0, 1), (a, 1, 1)]


# As dezesseis variantes, e o que cada tile do primario e de verdade (conferido
# pixel a pixel na paleta 5): o 2 e o 3 sao areia grossa manchada, o 129 e areia
# com cascalho claro, o 213 e a marca de sulco horizontal da mare e o 496 e o 498
# sao faixa de transicao clara para escura.
#
# TRES FAMILIAS DE VARIANTE FORAM CORTADAS DEPOIS DO RENDER, e as tres pelo mesmo
# defeito: QUADRADO. A primeira lista punha um tile ESCURO (o 454 ou o 455, o
# indice 14 da paleta) num quadrante so, para fazer mancha de areia molhada, e a
# malha pontilhada do 356 em outro, para fazer concha espalhada. No render as
# celulas vizinhas alinhavam os quadrantes escuros e o chao virava um TABULEIRO de
# quadrados de 8x8, que le como piso de ladrilho e nao como areia. O 356 sozinho
# passou a ler como tela de mosquiteiro. Ficaram so as texturas que variam DENTRO
# do proprio tile de 8x8, e as misturas passaram a ser de duas texturas (metade de
# cima com uma, metade de baixo com outra, ou as duas na diagonal), nunca textura
# contra chapado.
CHAO = [
    dict(nome="areia grossa",              quads=_u(2)),
    dict(nome="areia batida",              quads=_n(3)),
    dict(nome="areia de cascalho",         quads=_u(129)),
    dict(nome="areia ondulada",            quads=_u(213)),
    dict(nome="areia ondulada larga",      quads=_h(213)),
    dict(nome="faixa de maresia",          quads=_u(496)),
    dict(nome="faixa de maresia larga",    quads=_h(496)),
    dict(nome="maresia funda",             quads=_u(498)),
    dict(nome="areia grossa com maresia",  quads=_y(2, 496)),
    dict(nome="areia grossa com ondas",    quads=_y(2, 213)),
    dict(nome="onda sobre maresia funda",  quads=_y(213, 498)),
    dict(nome="areia batida com maresia",  quads=_x(3, 498)),
    dict(nome="cascalho com maresia",      quads=_y(129, 498)),
    dict(nome="onda entre maresia",        quads=_x(213, 498)),
    dict(nome="onda entre areia grossa",   quads=_x(2, 213)),
    dict(nome="cascalho entre areia batida", quads=_x(3, 129)),
]

# A MOITA e o segundo carimbo. A arte de cima (o arbusto do 569) fica IGUAL e so
# a areia de baixo muda: tres variantes, tres vagas de metatile, zero tile.
# A MOITA SO ACEITA VARIANTE QUE TROCA O ARBUSTO, e isso e medida e nao gosto. A
# primeira versao desta passada quebrava o 569 trocando a AREIA de baixo dele, do
# mesmo jeito que faz com o carimbo de areia, e o caso 6 do auto-teste reprovou
# na hora: o arbusto acende 202 dos 256 pixels da celula, entao trocar a areia
# que sobra move a imagem de 3,3 a 7,8 pixel a pixel, tudo abaixo do piso de 8,0
# que o `varia_carimbo.py` documenta como invisivel em jogo. Seria derrubar a
# regua sem mudar a tela, que e exatamente o que a trava existe para proibir.
#
# O que sobra e trocar o DESENHO. Entra a moita redonda do proprio
# `gTileset_Dewford` (a camada de cima do metatile 514, que os seis mapas usam
# como arbusto SOLIDO e que aqui vira arbusto ANDAVEL, com o atributo do 569):
# 94,0 de distancia do arbusto do carimbo, e custa ZERO tile e ZERO cor.
# Ficaram de fora o arbusto de cabeca para baixo (o 569 com espelho vertical,
# 119,4 de distancia) e a moita redonda virada (103,1): as duas passam no numero
# e reprovam no olho, porque poem a sombra da folhagem EM CIMA, e a luz desta
# arte vem de cima em todo o resto do mapa.
MATA = [
    dict(nome="moita redonda", topo_mt=514, quads=list(BASE_Q)),
]

# ------------------------------------------------------ os MÓVEIS que sao NOSSOS
# Metatile do nosso par de tilesets cuja camada de CIMA e levantada sobre a nossa
# areia. Custa ZERO tile, ZERO cor e uma vaga de metatile.
# QUASE TODA PECA ENTRA UMA VEZ SO, e isso e conta e nao gosto. Depois do anel de
# eventos e da margem sobram 39 celulas candidatas, e cada peca posta mata o anel
# de oito em volta dela (`ESPACO_ENTRE_MOVEIS`): cabem doze pecas no mapa
# inteiro. Com `quantos=2` ou `3` as primeiras da lista comiam o espaco e seis dos
# catorze desenhos nao chegavam a aparecer, entre eles tres dos SEIS importados,
# que sao justamente os que dao o tema de pescador. Com um por
# desenho a cidade ganha variedade em vez de repeticao, que e a mesma poda que o
# Gui mandou fazer em 07/09/2026 (`TETO_POR_CARIMBO` = 2 no
# `enfeita_cidades.py`).
MOVEIS_NOSSOS = [
    dict(nome="pedra da praia",     mt=226, quantos=1, espaco=5),
    dict(nome="pedregulho",         mt=504, quantos=1, espaco=5),
    dict(nome="moita de praia",     mt=514, quantos=2, espaco=5),
    dict(nome="arvore da praia",    mt=570, quantos=2, espaco=6),
    dict(nome="poste de amarracao", mt=320, quantos=1, espaco=5),
    dict(nome="mourao",             mt=313, quantos=1, espaco=5),
    dict(nome="cerca do cais",      mt=329, quantos=1, espaco=5),
    dict(nome="cabeco da cerca",    mt=328, quantos=1, espaco=5),
]

# ------------------------------------------------------ os MÓVEIS do hack
MOVEIS_LP = [
    dict(nome="boia no suporte",      lp=17,  quantos=1, espaco=5),
    dict(nome="boia deitada",         lp=127, quantos=1, espaco=5),
    dict(nome="tambor do cais",       lp=382, quantos=1, espaco=5),
    dict(nome="balde do pescador",    lp=374, quantos=1, espaco=5),
    dict(nome="poste do cais",        lp=391, quantos=1, espaco=5),
    dict(nome="quadro de avisos",     lp=395, quantos=1, espaco=8),
]

# AS BOLHAS. Grupo grande de proposito: bolha de uma peca so faz cada mancha sair
# de uma cor unica, e ai saber onde a celula esta passa a adivinhar a peca, que e
# o que o caso 11 do auto-teste proibe.
TEMA = dict(
    bolhas_areia=[
        dict(grupo=["areia grossa", "areia batida", "areia grossa com ondas"],
             tam=(6, 12), quantas=4),
        dict(grupo=["areia ondulada", "areia ondulada larga",
                    "onda entre areia grossa"], tam=(5, 11), quantas=4),
        dict(grupo=["faixa de maresia", "faixa de maresia larga",
                    "maresia funda"], tam=(5, 10), quantas=4),
        dict(grupo=["areia de cascalho", "cascalho com maresia",
                    "cascalho entre areia batida"], tam=(4, 9), quantas=4),
        dict(grupo=["onda sobre maresia funda", "onda entre maresia",
                    "areia batida com maresia", "areia grossa com maresia"],
             tam=(4, 9), quantas=4),
    ],
    bolhas_areia2=[
        dict(grupo=["areia grossa", "areia de cascalho", "areia batida",
                    "cascalho entre areia batida"], tam=(3, 7), quantas=5),
        dict(grupo=["areia ondulada", "faixa de maresia",
                    "areia grossa com maresia", "onda entre maresia"],
             tam=(3, 7), quantas=5),
        dict(grupo=["maresia funda", "onda sobre maresia funda",
                    "areia grossa com ondas", "areia batida com maresia"],
             tam=(2, 6), quantas=5),
    ],
    # A MOITA TEM UM GRUPO DE UM DESENHO SO, e isso e consequencia da medida
    # acima, nao descuido: so existe UMA variante que passa nos 8,0 pixel a
    # pixel. Metade das 32 celulas do carimbo vira moita redonda e a outra
    # metade fica como esta, que e o que derruba o 569 de 32 para dezesseis.
    bolhas_moita=[
        dict(grupo=["moita redonda"], tam=(2, 4), quantas=8, piso=1),
    ],
)


def _mistura(*n):
    """Hash determinista de inteiros, 32 bits. Nada de `random`: o plano tem que
    sair identico em qualquer maquina e em qualquer versao de Python."""
    h = 0x811C9DC5
    for x in n:
        h = ((h ^ (x & 0xFFFFFFFF)) * 0x01000193) & 0xFFFFFFFF
        h ^= h >> 15
    return h


# ------------------------------------------------------------ leitura do nosso
def _ler(nome):
    return open(f"{DESTINO}/{nome}", "rb").read()


def _entradas(bin_meta, local):
    return list(struct.unpack_from("<8H", bin_meta, local * 16))


def _tileset(rotulo):
    import render_maps as RM
    return RM.carregar_tileset(rotulo)


def ents_nossas(mt_id, tp=None, ts=None):
    """As oito entradas de um metatile NOSSO, pelo id global."""
    tp = tp or _tileset(PRIMARIO)
    ts = ts or _tileset(SECUNDARIO)
    tset, loc = (tp, mt_id) if mt_id < 512 else (ts, mt_id - 512)
    return list(struct.unpack_from("<8H", tset["metatiles"], loc * 16))


def attr_nosso(mt_id):
    if mt_id < 512:
        return G._attrs(PRIMARIO)[mt_id]
    return G._attrs(SECUNDARIO)[mt_id - 512]


def arte_em_cima(ents, tp=None, ts=None):
    """A camada de CIMA destas entradas acende ALGUM pixel?

    A pergunta nao e "o indice de tile e zero": o tile 1 do primario existe e nao
    tem um pixel aceso, e contar por indice diria que um chao chapado desenha por
    cima do jogador.
    """
    import render_maps as RM
    tp = tp or _tileset(PRIMARIO)
    ts = ts or _tileset(SECUNDARIO)
    for v in ents[4:]:
        idx = v & 0x3FF
        if not idx:
            continue
        tile = RM.resolver_tile(tp, ts, idx)
        if tile is None:
            continue
        if any(c for linha in tile for c in linha):
            return True
    return False


def vagas_livres():
    """{vaga: [indices de cor que NENHUM pixel VIVO nosso usa]}.

    "Vivo" e a palavra que importa: o `gTileset_Dewford` tem 379 metatiles e so
    241 deles aparecem em `map.bin` de algum dos seis layouts. A armadilha 4 do
    `compacta_paletas.py` (metatile do PRIMARIO alcancavel pintando com vaga de
    secundario) roda junto, porque "medi uma vez" nao e portao.
    """
    import render_maps as RM
    ts, tp = _tileset(SECUNDARIO), _tileset(PRIMARIO)
    usados = collections.defaultdict(set)
    vivos = set()
    for nome in IRMAOS:
        vivos |= {c & 0x3FF for c in G.grade(nome)[4]}
    for gid in sorted(vivos):
        tset, local = (ts, gid - 512) if gid >= 512 else (tp, gid)
        if gid >= 512 and local >= META_LOCAL_0:
            continue
        for (it, fh, fv, ip) in RM.entradas_metatile(tset["metatiles"], local):
            if it == 0 or ip < 6:
                continue
            tile = RM.resolver_tile(tp, ts, it)
            if tile is None:
                continue
            for linha in tile:
                for c in linha:
                    if c:
                        usados[ip].add(c)
    return {v: [i for i in range(1, 16) if i not in usados[v]]
            for v in range(6, 13)}


# ---------------------------------------------------------------- a EXTRAÇÃO
def _nibbles(dados, local):
    """8 linhas de 8 nibbles, o pixel PAR no nibble BAIXO (ver extrai_tileset)."""
    b = dados[local * 32:local * 32 + 32]
    if len(b) < 32:
        return [[0] * 8 for _ in range(8)]
    return [[(b[y * 4 + (x >> 1)] >> (0 if x % 2 == 0 else 4)) & 0xF
             for x in range(8)] for y in range(8)]


def _rgb(ts, i):
    """BGR555 do GBA para o RGB888 que o repo usa: cinco bits DESLOCADOS TRES
    casas, nao esticados para 0..255."""
    c = struct.unpack_from("<16H", ts["pal"], i * 32)
    return [[((v >> s) & 0x1F) << 3 for s in (0, 5, 10)] for v in c]


def _piso_da_fonte(tset):
    """Os tiles que a FONTE usa como piso, por evidencia e nao por decoreba.

    Duas assinaturas: (a) padrao de camada de baixo que aparece em PISO_MIN
    metatiles diferentes ou mais; (b) camada de baixo que repete o MESMO tile nos
    quatro quadrantes.
    """
    pad = collections.Counter()
    for loc in range(len(tset["meta"]) // 16):
        e = struct.unpack_from("<8H", tset["meta"], loc * 16)[:4]
        pad[tuple(v & 0x3FF for v in e)] += 1
    fora = set()
    for p, c in pad.items():
        if c >= PISO_MIN or len(set(p)) == 1:
            fora |= set(p)
    return fora


def extrai():
    """Regera `praia_dewford_kit.json` a partir da ROM privada do Light Platinum.

    So roda na maquina que tem `fontes-mapas/romhacks/`. O que sai daqui e o asset
    CONVERTIDO (tiles em nibbles, ja reindexados para a vaga de destino, e paleta
    em RGB), nunca a ROM.
    """
    ferr = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/romhacks"
    if not os.path.isdir(ferr):
        raise SystemExit("nao achei fontes-mapas/romhacks: --extrai so roda na "
                         "maquina que tem as ROMs. O kit ja extraido esta em "
                         + os.path.relpath(KIT_JSON, RAIZ))
    sys.path.insert(0, f"{ferr}/ferramentas")
    import hashlib
    from gbamap import Rom  # noqa: E402

    pasta = os.path.join(ferr, LP["slug"])
    gba = [f for f in sorted(os.listdir(pasta)) if f.lower().endswith(".gba")][0]
    caminho = os.path.join(pasta, gba)
    md5 = hashlib.md5(open(caminho, "rb").read()).hexdigest()
    if md5 != LP["md5"]:
        raise SystemExit("a ROM em %s tem md5 %s e o kit foi feito com %s"
                         % (gba, md5, LP["md5"]))
    r = Rom(caminho)
    r.n_meta_pri, r.n_tiles_pri, r.n_pal_pri = LP["split"]
    t1 = r.parse_tileset(LP["pri"])
    t2 = r.parse_tileset(LP["sec"])
    if t1 is None or t2 is None:
        raise SystemExit("o par 0x%X / 0x%X do hack nao abriu"
                         % (LP["pri"], LP["sec"]))
    NP = r.n_tiles_pri
    livres = vagas_livres()
    pal = {i: _rgb(t1 if i < 6 else t2, i) for i in range(16)}
    piso = _piso_da_fonte(t2)

    def px_de(idx):
        return _nibbles(t1["tiles"], idx) if idx < NP else _nibbles(t2["tiles"],
                                                                    idx - NP)

    def branco(v):
        idx = v & 0x3FF
        if not idx:
            return True
        return not any(c for linha in px_de(idx) for c in linha)

    tiles_px, tiles_vaga, tiles_cor = {}, {}, {}

    def guarda(idx, ip):
        """Registra o tile 8x8 e devolve a chave dele.

        A CHAVE LEVA A PALETA DE ORIGEM: o mesmo desenho pintado com duas paletas
        do hack tem que virar DUAS vagas nossas, senao a segunda apaga a primeira.
        """
        if ip not in VAGAS_PAL:
            return None
        ch = "%d:%d" % (idx, ip)
        destino = VAGAS_PAL[ip]
        if tiles_vaga.setdefault(ch, destino) != destino:
            raise SystemExit("o tile %s foi pedido nas vagas %d e %d"
                             % (ch, tiles_vaga[ch], destino))
        tiles_px[ch] = px_de(idx)
        origem = pal[ip]
        tiles_cor.setdefault(ch, set())
        for linha in tiles_px[ch]:
            for c in linha:
                if c:
                    tiles_cor[ch].add(tuple(origem[c]))
        return ch

    pecas = []
    for p in MOVEIS_LP:
        ents = list(struct.unpack_from("<8H", t2["meta"], p["lp"] * 16))
        baixo, cima = ents[:4], ents[4:]
        # QUADRANTE DE BAIXO SOBE quando o de cima esta vazio; quadrante promovido
        # que e PISO da fonte, ou que a fonte pinta com paleta fora do kit, e
        # DESCARTADO e recebe o NOSSO chao.
        usadas, saida = [], []
        for q in range(4):
            de_baixo = branco(cima[q])
            v = baixo[q] if de_baixo else cima[q]
            if not (v & 0x3FF) or (de_baixo and (v & 0x3FF) in piso):
                usadas.append(None)
                saida.append(0)
                continue
            ch = guarda(v & 0x3FF, (v >> 12) & 0xF)
            usadas.append(ch)
            saida.append(v if ch is not None else 0)
        if not any(usadas):
            raise SystemExit("%s: o metatile %d nao sobrou com nenhum quadrante "
                             "de arte" % (p["nome"], p["lp"]))
        pecas.append(dict(nome=p["nome"], lp=p["lp"], ents=saida, usadas=usadas))

    # -------------------------------------------------- as paletas de destino
    ts_nosso = _tileset(SECUNDARIO)
    por_vaga = collections.defaultdict(set)
    for ch, vaga in tiles_vaga.items():
        por_vaga[vaga] |= tiles_cor[ch]
    paletas, indice = {}, {}
    for vaga, cores in sorted(por_vaga.items()):
        vagos = livres.get(vaga) or []
        cores = sorted(cores)
        if len(cores) > len(vagos):
            raise SystemExit("a vaga %d tem %d indices livres (%s) e o kit pede "
                             "%d cores" % (vaga, len(vagos), vagos, len(cores)))
        base = [list(c) for c in ts_nosso["paletas"][vaga]]
        for k, c in enumerate(cores):
            base[vagos[k]] = list(c)
            indice[(vaga, c)] = vagos[k]
        paletas[str(vaga)] = base

    # REINDEXA cada nibble para a tabela nova. A cor 0 continua 0 e nenhuma cor e
    # aproximada: a tabela de destino tem as MESMAS cores RGB da fonte, so em
    # outro indice, entao o pixel sai identico ao da ROM.
    saida_tiles = {}
    for ch, vaga in tiles_vaga.items():
        _idx, ip = ch.split(":")
        origem = pal[int(ip)]
        saida_tiles[ch] = [[0 if c == 0 else indice[(vaga, tuple(origem[c]))]
                            for c in linha] for linha in tiles_px[ch]]

    dados = dict(
        fonte=dict(hack=LP["hack"], autor=LP["autor"], base=LP["base"],
                   arquivo=gba, md5=md5, pri="0x%X" % LP["pri"],
                   sec="0x%X" % LP["sec"], split=list(LP["split"]),
                   n_tiles_pri=NP),
        vagas_pal={str(k): v for k, v in VAGAS_PAL.items()},
        vagas_livres={str(k): v for k, v in livres.items()},
        paletas=paletas, tiles=saida_tiles, tiles_vaga=tiles_vaga,
        piso_da_fonte=sorted(piso), pecas=pecas)
    with open(KIT_JSON, "w") as f:
        json.dump(dados, f, indent=1)
    print("kit gravado em %s: %d tiles, %d pecas"
          % (os.path.relpath(KIT_JSON, RAIZ), len(saida_tiles), len(pecas)))
    for vaga, cores in sorted(por_vaga.items()):
        print("  vaga %2d: %2d cores nos indices %s"
              % (vaga, len(cores), [indice[(vaga, c)] for c in sorted(cores)]))
    return 0


# --------------------------------------------------------------- o KIT em disco
def kit():
    if not os.path.exists(KIT_JSON):
        raise SystemExit("falta %s; rode --extrai numa maquina com a ROM"
                         % os.path.relpath(KIT_JSON, RAIZ))
    return json.load(open(KIT_JSON))


def chao_nosso(qual):
    """(as quatro entradas da camada de BAIXO do carimbo, o atributo dele).

    E o chao que todo movel pousa em cima e que toda variante herda. Os DOIS
    carimbos de Dewford tem a MESMA camada de baixo (a areia do 292), e o 569 so
    acrescenta o arbusto por cima: isso e conferido aqui, e nao suposto.
    """
    mt = CARIMBOS[qual]
    ents = ents_nossas(mt)
    return ents[:4], attr_nosso(mt)


def _locais_livres():
    """Os locais de metatile em que esta passada pode gravar, em ordem. O portao
    de verdade (nenhum dos seis mapas usa o id) roda depois, no `desenha_kit`."""
    return list(range(META_LOCAL_0, TETO_META))


def _vagas_de_tile():
    """As vagas de TILE livres, em ordem, PULANDO os pinos da animacao."""
    return [v for v in range(TILE_LOCAL_0, TETO_TILES) if v not in PINOS_ANIM]


def px_metatile(ents, tp, ts, tiles_novos=None, paletas=None):
    """Os 256 pixels RGB de um metatile descrito por oito entradas."""
    import render_maps as RM
    from PIL import Image
    im = Image.new("RGB", (16, 16), (0, 0, 0))
    p = im.load()
    for cam in (0, 1):
        for q in range(4):
            val = ents[cam * 4 + q]
            idx, ip = val & 0x3FF, (val >> 12) & 0xF
            if not idx:
                continue
            vaga = idx - len(tp["tiles"])
            if tiles_novos and vaga in tiles_novos:
                tile = tiles_novos[vaga]
            else:
                tile = RM.resolver_tile(tp, ts, idx)
            if tile is None:
                continue
            cores = None
            if paletas:
                cores = paletas.get(str(ip))
            if cores is None:
                cores = (tp if ip < 6 else ts)["paletas"].get(ip)
            if cores is None:
                continue
            RM.desenhar_tile(p, (q % 2) * 8, (q // 2) * 8, tile,
                             [tuple(c) for c in cores],
                             bool(val & 0x400), bool(val & 0x800))
    return list(im.getdata())


def _dist_pixels(a, b):
    return sum(sum((x - y) ** 2 for x, y in zip(p, q)) ** 0.5
               for p, q in zip(a, b)) / 256.0


def _cor_media(px):
    return tuple(sum(c[k] for c in px) / 256.0 for k in range(3))


def _dist_cor(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def quadrante(qd):
    """A entrada de 16 bits de um quadrante de chao NOSSO, na paleta do carimbo."""
    idx, fh, fv = qd
    return ((0x400 if fh else 0) | (0x800 if fv else 0) | idx
            | (PAL_AREIA << 12))


def desenha_kit():
    """(tiles_novos, metas, attrs, catalogo), sem escrever em disco."""
    dados = kit()
    tp, ts = _tileset(PRIMARIO), _tileset(SECUNDARIO)

    por_peca = {p["nome"]: p for p in dados["pecas"]}
    tiles_novos, mapa_tile = {}, {}
    vagas_tile = _vagas_de_tile()
    proximo = [0]
    metas, attrs = {}, {}
    vagas_meta = _locais_livres()
    proximo_meta = [0]
    catalogo = dict(chao={}, mata={}, moveis={}, sobre={})

    def vaga(chave):
        if chave not in mapa_tile:
            if chave not in dados["tiles"]:
                raise SystemExit("o kit em disco nao tem o tile %s" % chave)
            if proximo[0] >= len(vagas_tile):
                raise SystemExit("acabaram as vagas de tile livres")
            mapa_tile[chave] = vagas_tile[proximo[0]]
            tiles_novos[vagas_tile[proximo[0]]] = dados["tiles"][chave]
            proximo[0] += 1
        return mapa_tile[chave]

    def poe(ents, attr):
        if proximo_meta[0] >= len(vagas_meta):
            raise SystemExit("acabaram as vagas de metatile livres")
        local = vagas_meta[proximo_meta[0]]
        metas[local] = list(ents)
        attrs[local] = attr
        proximo_meta[0] += 1
        return 512 + local

    def entrada(p, q):
        """A entrada NOSSA para o quadrante q da peca: mesmo tile, vaga nova,
        vaga de paleta nova, e os bits de espelho da fonte preservados."""
        ch = p["usadas"][q]
        if ch is None:
            return None
        v = p["ents"][q]
        _idx, ip = ch.split(":")
        alvo_pal = VAGAS_PAL[int(ip)]
        return ((v & 0x0C00) | (512 + vaga(ch)) | (alvo_pal << 12))

    BASE = {q: chao_nosso(q) for q in CARIMBOS}
    if BASE["areia"][0] != BASE["moita"][0]:
        raise SystemExit("os dois carimbos nao tem a mesma camada de baixo: "
                         "%s x %s" % (BASE["areia"][0], BASE["moita"][0]))
    # O CARIMBO 292 DUPLICA a camada de baixo na de cima, e isso NAO e enfeite:
    # em `METATILE_LAYER_TYPE_COVERED` (`src/field_camera.c`) a camada de baixo
    # vai para o BG3 e a de cima para o BG2, as duas ABAIXO do sprite, e o BG1
    # fica transparente. Areia em cima de areia da o mesmo pixel. As variantes
    # copiam a estrutura do carimbo em vez de deixar a camada de cima vazia,
    # porque assim o metatile novo e do MESMO formato que o velho e nao depende
    # de o tile 0 do primario continuar em branco.
    ents_car = ents_nossas(CARIMBOS["areia"], tp, ts)
    if ents_car[4:] != ents_car[:4]:
        raise SystemExit("o carimbo de areia nao duplica a camada de baixo: %s"
                         % [hex(x) for x in ents_car])
    ARBUSTO = ents_nossas(CARIMBOS["moita"], tp, ts)[4:]

    # ------------------------------------------------------ 1. CHÃO de AREIA
    px_carimbo = {q: px_metatile(ents_nossas(CARIMBOS[q], tp, ts), tp, ts)
                  for q in CARIMBOS}
    for c in CHAO:
        _base, attr_carimbo = BASE["areia"]
        quads = [quadrante(qd) for qd in c["quads"]]
        ents = quads + list(quads)
        d = _dist_cor(_cor_media(px_metatile(ents, tp, ts, tiles_novos,
                                             dados["paletas"])),
                      _cor_media(px_carimbo["areia"]))
        if d > TETO_COR:
            raise SystemExit("o chao %s esta a %.1f de cor do carimbo de areia, "
                             "acima do teto de %.1f" % (c["nome"], d, TETO_COR))
        catalogo["chao"][c["nome"]] = poe(ents, attr_carimbo)
        catalogo["sobre"][c["nome"]] = "areia"

    # -------------------------------------------------------- 2. CHÃO de MOITA
    for c in MATA:
        _base, attr_carimbo = BASE["moita"]
        topo = ents_nossas(c["topo_mt"], tp, ts)[4:]
        if not any(vv & 0x3FF for vv in topo):
            raise SystemExit("a mata %s vem do metatile %d, que nao tem arte na "
                             "camada de cima" % (c["nome"], c["topo_mt"]))
        ents = [quadrante(qd) for qd in c["quads"]] + list(topo)
        catalogo["mata"][c["nome"]] = poe(ents, attr_carimbo)
        catalogo["sobre"][c["nome"]] = "moita"

    # -------------------------------------------- 3. MÓVEIS NOSSOS de 1 célula
    base_areia, _a = BASE["areia"]
    for m in MOVEIS_NOSSOS:
        e = ents_nossas(m["mt"], tp, ts)
        cima = list(e[4:])
        # QUADRANTE DE BAIXO SOBE quando o de cima esta vazio.
        if not arte_em_cima(e, tp, ts):
            cima = list(e[:4])
        if not any(v & 0x3FF for v in cima):
            raise SystemExit("%s: o metatile %d nao tem arte" % (m["nome"],
                                                                 m["mt"]))
        catalogo["moveis"][m["nome"]] = poe(list(base_areia) + cima, 0x1000)
        catalogo["sobre"][m["nome"]] = "areia"

    # ------------------------------------------ 4. MÓVEIS IMPORTADOS de 1 célula
    for m in MOVEIS_LP:
        p = por_peca[m["nome"]]
        cima = [entrada(p, q) or 0 for q in range(4)]
        if not any(cima):
            raise SystemExit("%s: peca sem arte" % m["nome"])
        # comportamento ZERADO (nenhum id semantico e importado) e layerType
        # COVERED, que poe as duas camadas ABAIXO do sprite.
        catalogo["moveis"][m["nome"]] = poe(list(base_areia) + cima, 0x1000)
        catalogo["sobre"][m["nome"]] = "areia"

    if tiles_novos and max(tiles_novos) >= TETO_TILES:
        raise SystemExit("o kit estoura o teto de %d tiles" % TETO_TILES)

    # A vaga de metatile so serve se NENHUM dos seis mapas vivos usar o id. A
    # grade do ALVO entra pela base LIMPA desta passada, e nao pelo disco: depois
    # de um `--aplicar` o disco ja tem os ids que este kit acabou de escrever, e o
    # portao reprovaria a si mesmo na segunda rodada.
    guardado = carrega_plano()
    usados = set()
    for nome in IRMAOS:
        grade = base_de(nome, guardado) if nome == ALVO else G.grade(nome)[4]
        usados |= {c & 0x3FF for c in grade}
    for local in metas:
        if 512 + local in usados:
            raise SystemExit("algum dos seis mapas usa o metatile %d"
                             % (512 + local))
    for vaga in tiles_novos:
        if vaga in PINOS_ANIM:
            raise SystemExit("o kit grava na vaga de tile %d, que e pino da "
                             "animacao da bandeira" % vaga)
    return tiles_novos, metas, attrs, catalogo


def grava_tileset(tiles_novos, metas, attrs):
    """Escreve tiles.png, palettes/*.pal, metatiles.bin e metatile_attributes.bin.

    Idempotente: as vagas de tile, de paleta e de metatile sao FIXAS.

    A ARMADILHA DO `Image.convert("P")`: numa imagem que JA e "P" ele devolve uma
    COPIA e nao converte, e uma frente desta onda gravou metatiles e NENHUM tile
    por causa disso. Aqui a imagem nova nasce em "P" e recebe a paleta da antiga.
    """
    from PIL import Image
    dados = kit()
    antigo = Image.open(f"{DESTINO}/tiles.png")
    cols = antigo.size[0] // 8
    alvo = max((max(tiles_novos) + 1) if tiles_novos else 0,
               (antigo.size[1] // 8) * cols)
    linhas = (alvo + cols - 1) // cols
    novo = Image.new("P", (antigo.size[0], linhas * 8), 0)
    novo.putpalette(antigo.getpalette())
    novo.paste(antigo, (0, 0))
    px = novo.load()
    for v, tile in tiles_novos.items():
        x0, y0 = (v % cols) * 8, (v // cols) * 8
        for y in range(8):
            for x in range(8):
                px[x0 + x, y0 + y] = tile[y][x]
    novo.save(f"{DESTINO}/tiles.png")

    for vaga, cores in sorted(dados["paletas"].items()):
        _grava_pal(int(vaga), cores)

    meta = bytearray(_ler("metatiles.bin"))
    attr = bytearray(_ler("metatile_attributes.bin"))
    falta = (max(metas) + 1) * 16 - len(meta) if metas else 0
    if falta > 0:
        meta += bytes(falta)
        attr += bytes((max(metas) + 1) * 2 - len(attr))
    for local, ents in metas.items():
        for i, v in enumerate(ents):
            struct.pack_into("<H", meta, local * 16 + i * 2, v)
        struct.pack_into("<H", attr, local * 2, attrs[local])
    open(f"{DESTINO}/metatiles.bin", "wb").write(bytes(meta))
    open(f"{DESTINO}/metatile_attributes.bin", "wb").write(bytes(attr))


def _grava_pal(vaga, cores):
    with open(f"{DESTINO}/palettes/%02d.pal" % vaga, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n16\n")
        for r, g, b in cores:
            f.write("%d %d %d\n" % (r, g, b))


# ------------------------------------------------------------ o ESPALHAMENTO
def bolhas(livres, spec, semente=0x5EED):
    """[(nomes, {celulas})], bolhas organicas crescidas por frente de onda.

    A SEMENTE nao e sorteio solto: as celulas livres sao ordenadas por um hash da
    posicao e a semente so e aceita a pelo menos 2 (Chebyshev) de toda semente ja
    aceita. O CRESCIMENTO e guloso com ruido: a cada passo entra a celula da
    frente de onda com o menor hash. Circulo daria bolha redonda e xadrez daria
    sal e pimenta; frente de onda com ruido da contorno irregular.

    A ORDEM E POR RODADA, e nao por especificacao inteira: servindo UMA bolha por
    especificacao a cada rodada, o que falta no fim e o excedente de todo mundo, e
    nao a lista inteira de quem estava no fim da fila.
    """
    ordem = sorted(livres, key=lambda p: _mistura(p[0], p[1], semente))
    tomadas, saida, sementes = set(), [], []
    feitas = [0] * len(spec)
    while True:
        andou = False
        for k, esp in enumerate(spec):
            if feitas[k] >= esp["quantas"]:
                continue
            achou = None
            for p in ordem:
                if p in tomadas:
                    continue
                if any(max(abs(p[0] - q[0]), abs(p[1] - q[1])) < 2
                       for q in sementes):
                    continue
                lo, hi = esp["tam"]
                alvo = lo + _mistura(p[0], p[1], 0xB10B) % (hi - lo + 1)
                corpo, frente = {p}, set()
                for dx, dy in N4:
                    q = (p[0] + dx, p[1] + dy)
                    if q in livres and q not in tomadas:
                        frente.add(q)
                while len(corpo) < alvo and frente:
                    q = min(frente, key=lambda r: _mistura(r[0], r[1], 0xC0FFEE))
                    frente.discard(q)
                    corpo.add(q)
                    for dx, dy in N4:
                        rr = (q[0] + dx, q[1] + dy)
                        if rr in livres and rr not in tomadas and rr not in corpo:
                            frente.add(rr)
                # ACEITA A BOLHA CURTA quando foi a REGIAO que acabou, e nao a
                # vontade de crescer: a moita de Dewford e uma fileira de celulas
                # soltas na borda do mapa e exigir tamanho cheio a deixaria lisa.
                if len(corpo) < lo and (frente or len(corpo) < esp.get("piso", PISO_BOLHA)):
                    continue
                achou = (p, corpo)
                break
            if achou is None:
                feitas[k] = esp["quantas"]     # nao ha mais lugar para esta
                continue
            p, corpo = achou
            tomadas |= corpo
            sementes.append(p)
            saida.append((esp["grupo"], corpo))
            feitas[k] += 1
            andou = True
        if not andou:
            break
    return saida


MULTI_NIVEL = 15        # ELEVATION_MULTI_LEVEL: casa com QUALQUER elevacao


def corredores_multinivel(v, W, H, d):
    """Os corredores da suite, refeitos com a regra da ELEVACAO 15.

    O `enfeita_cidades.corredores_de_teste` congela as celulas que a suite anda
    dentro do mapa e simula a caminhada com a regra "elevacao 0 e curinga e o
    resto exige igualdade". Essa regra ignora a elevacao 15
    (`ELEVATION_MULTI_LEVEL`), que MANTEM a elevacao do jogador. Dewford nao tem
    hoje nenhuma celula 15 (medido: as elevacoes do mapa sao 0, 1 e 3), entao aqui
    as duas contas coincidem, e e por isso mesmo que as DUAS rodam: a uniao e
    barata e nao depende de a medida continuar valendo depois que outra frente
    mexer no mapa.
    """
    import glob
    import re as _re
    pasta = f"{RAIZ}/dev_scripts/testes_criticos"
    nome_mapa = "MAP_" + _re.sub(r"(?<!^)(?=[A-Z])", "_",
                                 d.get("name", ALVO)).upper().replace("__", "_")
    obj = {(o["x"], o["y"]) for o in (d.get("object_events") or [])}
    warps = d.get("warp_events") or []
    pisadas = set()
    passo = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}

    def compativel(ea, eb):
        return ea in (0, MULTI_NIVEL) or eb in (0, MULTI_NIVEL) or ea == eb

    def caminha(x, y, pernas, olhando):
        pisadas.add((x, y))
        for direcao, n in pernas:
            dx, dy = direcao
            passos = n - 1 if olhando != direcao else n
            olhando = direcao
            for _ in range(max(0, passos)):
                nx, ny = x + dx, y + dy
                if not (0 <= nx < W and 0 <= ny < H):
                    break
                j = ny * W + nx
                if (v[j] >> 10) & 3 or (nx, ny) in obj:
                    break
                if not compativel((v[y * W + x] >> 12) & 0xF, (v[j] >> 12) & 0xF):
                    break
                x, y = nx, ny
                pisadas.add((x, y))

    for arq in sorted(glob.glob(f"{pasta}/*.json")):
        if os.path.basename(arq) == BLOCO_PROPRIO:
            continue   # o bloco desta rodada e derivado DO desenho, nao o contrario
        for caso in json.load(open(arq)):
            if caso.get("warp") != nome_mapa:
                continue
            wid = int(caso.get("warp_id", 0) or 0)
            if wid >= len(warps):
                continue
            pernas = []
            for tok in (caso.get("roteiro") or "").split(","):
                m = E._LEG.match(tok.strip())
                if m:
                    pernas.append((passo[m.group(1)], int(m.group(2) or 1)))
            for x0, y0 in ((warps[wid]["x"], warps[wid]["y"]),
                           (warps[wid]["x"], warps[wid]["y"] + 1)):
                if not (0 <= x0 < W and 0 <= y0 < H):
                    continue
                for olhando in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                    caminha(x0, y0, pernas, olhando)
    return pisadas


def peca_da_mancha(nomes, x, y):
    """Qual das pecas do grupo cai nesta celula. Hash da posicao, nao paridade:
    paridade vira xadrez e o auto-teste reprova."""
    return nomes[_mistura(x, y, 0xA5A5 + len(nomes)) % len(nomes)]


# ----------------------------------------------------------- ligacao a pe
def componentes(v, W, H):
    """{celula: rotulo} dos pedacos de chao andavel ligados a pe.

    POR QUE NAO BASTA O `enfeita_cidades.alcance`. Aquele mede "quem ainda e
    alcancavel a partir de algum ponto de partida", e fechar um corredor com warp
    dos dois lados nao tira NENHUMA celula do alcance e mesmo assim parte a cidade
    em duas.
    """
    rot, prox = {}, 0
    for y in range(H):
        for x in range(W):
            if (v[y * W + x] >> 10) & 3 or (x, y) in rot:
                continue
            fila, prox = [(x, y)], prox + 1
            rot[(x, y)] = prox
            while fila:
                cx, cy = fila.pop()
                ea = (v[cy * W + cx] >> 12) & 0xF
                for dx, dy in N4:
                    nx, ny = cx + dx, cy + dy
                    if not (0 <= nx < W and 0 <= ny < H) or (nx, ny) in rot:
                        continue
                    j = ny * W + nx
                    if (v[j] >> 10) & 3:
                        continue
                    eb = (v[j] >> 12) & 0xF
                    if ea and eb and ea != eb:
                        continue
                    rot[(nx, ny)] = prox
                    fila.append((nx, ny))
    return rot


def ligacao_intacta(antes, depois, solidificadas):
    """Nenhum pedaco de chao se PARTIU, e nenhum se juntou a outro."""
    mau = []
    por_rotulo = collections.defaultdict(set)
    for p, rr in antes.items():
        if p not in solidificadas:
            por_rotulo[rr].add(p)
    for rr, cels in por_rotulo.items():
        if len({depois.get(p) for p in cels}) > 1:
            mau.append("o pedaco %d de chao se partiu em %d"
                       % (rr, len({depois.get(p) for p in cels})))
    juntou = collections.defaultdict(set)
    for p, rr in depois.items():
        if p in antes:
            juntou[rr].add(antes[p])
    for rr, origens in juntou.items():
        if len(origens) > 1:
            mau.append("dois pedacos de chao que eram separados se juntaram")
    return mau


# ---------------------------------------------------------------- o PLANO
def plano_mapa(catalogo, base=None):
    """(L, W, H, v, escritas, contas) para `DewfordTown`."""
    d, L, W, H, v0 = G.grade(ALVO)
    v = list(base) if base is not None else list(v0)
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()

    # As duas FAMILIAS de chao. Uma celula so e elegivel se ainda for o carimbo
    # puro, se estiver numa das elevacoes que a familia aceita e se nao for AGUA
    # para o motor. O filtro de agua e o que protege a beira do mar: nenhuma
    # celula de superficie de Surf entra no catalogo.
    fam = {}
    for qual, mt in CARIMBOS.items():
        fam[qual] = {(i % W, i // W) for i in range(W * H)
                     if not ((v[i] >> 10) & 3) and (v[i] & 0x3FF) == mt
                     and ((v[i] >> 12) & 0xF) in ELEVACOES[qual]
                     and beh(v[i] & 0x3FF) not in AG}

    escritas = {}
    # DOIS GELOS, e a diferenca custou metade da regua na primeira rodada desta
    # passada. O `enfeita_cidades.congelado` devolve a celula de todo evento MAIS
    # um anel de uma celula em volta, e isso existe para o objeto SOLIDO: peca
    # nova encostada numa porta ou num NPC tranca gente. Repintar o CHAO nao
    # tranca nada: a colisao, a elevacao e o par (comportamento, layerType)
    # continuam identicos por construcao. Numa cidade de 20x20 com 11 NPCs, 5
    # warps e 5 placas, o anel come 81 das 145 celulas do carimbo, e usar o mesmo
    # gelo para os dois deixava a regua em 46,0%.
    #
    # `gelo_solido` (evento + anel + corredor da suite) manda no MOVEL.
    # `gelo` (so o corredor da suite e o que ESTA passada ja escreveu) manda na
    # MANCHA. Conferido a parte: NENHUM warp e NENHUMA placa de Dewford fica em
    # cima do carimbo (as cinco portas e as cinco placas sao metatile de predio,
    # com colisao 1), entao a mancha nunca toca um tile de warp.
    ev, halo = E.congelado(d)
    gelo = E.corredores_de_teste(ALVO, v, W, H, d)
    gelo |= corredores_multinivel(v, W, H, d)
    for idx, _a, _n in E.carrega_plano().get(ALVO, {}).get("celulas", []):
        gelo.add((idx % W, idx // W))
    gelo_solido = gelo | halo

    aplicado = list(v)
    ini = E.partidas(d, W, H, v)
    antes_alc = E.alcance(v, W, H, ini)
    novos_solidos, postos = [], []
    conta_mov = collections.Counter()
    por_movel = collections.defaultdict(list)

    def nao_liga(grade, x, y):
        """Os vizinhos andaveis de (x,y) ainda se falam sem passar por (x,y)?"""
        viz = [(x + dx, y + dy) for dx, dy in N4
               if 0 <= x + dx < W and 0 <= y + dy < H
               and not ((grade[(y + dy) * W + x + dx] >> 10) & 3)]
        if len(viz) < 2:
            return False
        vistos, fila, falta = {viz[0]}, [viz[0]], set(viz[1:])
        while fila and falta:
            cx, cy = fila.pop()
            ea = (grade[cy * W + cx] >> 12) & 0xF
            for dx, dy in N4:
                nx, ny = cx + dx, cy + dy
                if not (0 <= nx < W and 0 <= ny < H) or (nx, ny) in vistos:
                    continue
                j = ny * W + nx
                if (grade[j] >> 10) & 3:
                    continue
                eb = (grade[j] >> 12) & 0xF
                if ea and eb and ea != eb:
                    continue
                vistos.add((nx, ny))
                falta.discard((nx, ny))
                fila.append((nx, ny))
        return bool(falta)

    def livre(x, y):
        i = y * W + x
        if x < MARGEM or y < MARGEM or x >= W - MARGEM or y >= H - MARGEM:
            return False
        if (x, y) in gelo_solido or i in escritas or (x, y) not in fam["areia"]:
            return False
        return (aplicado[i] & 0x3FF) == CARIMBOS["areia"]

    def espacado(nome, esp, x, y):
        if any(max(abs(x - px), abs(y - py)) < ESPACO_ENTRE_MOVEIS
               for px, py in postos):
            return False
        return not any(max(abs(x - px), abs(y - py)) < esp
                       for px, py in por_movel[nome])

    def encostado(x, y):
        """MOVEL DE PRAIA ENCOSTA EM ALGUMA COISA: num solido, na agua ou na
        moita. Boia solta no meio do areal le como erro de mapa.

        O ANEL E O DE OITO, e nao o de quatro, e o numero mandou: com o anel de
        quatro sobram 25 celulas candidatas nesta cidade e cabem 12 pecas; com o
        de oito sobram 39 e cabem 18. A peca encostada na DIAGONAL de um predio
        continua encostada aos olhos de quem joga, que e o que a regra quer
        dizer."""
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if not dx and not dy:
                    continue
                nx, ny = x + dx, y + dy
                if not (0 <= nx < W and 0 <= ny < H):
                    return True      # a borda do mapa tambem e encosto
                j = ny * W + nx
                if (aplicado[j] >> 10) & 3:
                    return True
                if beh(aplicado[j] & 0x3FF) in AG:
                    return True
                if (nx, ny) in fam["moita"]:
                    return True
        return False

    def tenta_solidificar(x, y, mt_id):
        """Solidifica (x,y) e devolve True se os DOIS portoes deixarem. O portao
        roda NA HORA e nao so no fim."""
        i = y * W + x
        antigo = aplicado[i]
        aplicado[i] = (antigo & 0xF000) | (1 << 10) | mt_id   # elevacao INTACTA
        perdidas = (antes_alc - E.alcance(aplicado, W, H, ini)) \
            - set(novos_solidos) - {(x, y)}
        if perdidas or nao_liga(aplicado, x, y):
            aplicado[i] = antigo
            return False
        escritas[i] = aplicado[i]
        novos_solidos.append((x, y))
        postos.append((x, y))
        return True

    ordem_cel = sorted(((x, y) for y in range(H) for x in range(W)),
                       key=lambda p: ((p[0] * 2654435761 + p[1] * 40503) & 0xFFFF, p))

    # ------ 1. MOVEIS de uma celula. Eles vem ANTES da mancha de proposito:
    # movel posto no carimbo tira uma celula do numerador E do denominador da
    # regua; movel posto em cima de uma mancha tira so do denominador, o que
    # PIORA a conta.
    lista = MOVEIS_NOSSOS + MOVEIS_LP
    for x, y in ordem_cel:
        giro = ((x * 73856093) ^ (y * 19349663)) % len(lista)
        for k in range(len(lista)):
            m = lista[(giro + k) % len(lista)]
            if conta_mov[m["nome"]] >= m["quantos"]:
                continue
            if not livre(x, y) or not espacado(m["nome"], m["espaco"], x, y):
                continue
            if not encostado(x, y):
                continue
            if not tenta_solidificar(x, y, catalogo["moveis"][m["nome"]]):
                continue
            por_movel[m["nome"]].append((x, y))
            conta_mov[m["nome"]] += 1
            break

    # ------------------------------------------------------------- 2. MANCHA
    conta_mancha = collections.Counter()

    def pintavel(p, qual):
        i = p[1] * W + p[0]
        return (p in fam[qual] and i not in escritas and p not in gelo
                and (aplicado[i] & 0x3FF) == CARIMBOS[qual])

    def pinta(p, nomes, onde):
        i = p[1] * W + p[0]
        nome = peca_da_mancha(nomes, p[0], p[1])
        escritas[i] = (aplicado[i] & 0xFC00) | catalogo[onde][nome]
        aplicado[i] = escritas[i]
        conta_mancha[nome] += 1

    for qual, chave, onde, semente in (
            ("areia", "bolhas_areia", "chao", 0x5EED),
            ("moita", "bolhas_moita", "mata", 0xB0A7),
            ("areia", "bolhas_areia2", "chao", 0x5EED ^ 0x1234)):
        livres = {p for p in fam[qual] if pintavel(p, qual)}
        for nomes, corpo in bolhas(livres, TEMA[chave], semente):
            for p in sorted(corpo):
                pinta(p, nomes, onde)

    # -------------------------------------------------------------- PORTOES
    depois = E.alcance(aplicado, W, H, ini)
    perdidas = antes_alc - depois - set(novos_solidos)
    if perdidas:
        raise SystemExit("%s: %d celulas ficariam inalcancaveis, ex.: %s"
                         % (ALVO, len(perdidas), sorted(perdidas)[:6]))
    for x, y in E.eventos(d):
        if (x, y) in antes_alc and (x, y) not in depois:
            raise SystemExit("%s: evento em (%d,%d) ficaria inalcancavel"
                             % (ALVO, x, y))
    queixas = ligacao_intacta(componentes(v, W, H), componentes(aplicado, W, H),
                              set(novos_solidos))
    if queixas:
        raise SystemExit("%s: %s" % (ALVO, "; ".join(queixas)))
    contas = dict(moveis=dict(conta_mov), manchas=dict(conta_mancha),
                  solidos=len(novos_solidos),
                  areia=len(fam["areia"]), moita=len(fam["moita"]))
    return L, W, H, v, escritas, contas


def regua(v, W, H, L, escritas=None):
    """(carimbo dominante em %, celulas andaveis a pe, id do carimbo), como a
    `regua_cidades.py` conta."""
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()
    cel = list(v)
    for i, val in (escritas or {}).items():
        cel[i] = val
    and_ = [c & 0x3FF for c in cel
            if not ((c >> 10) & 3) and beh(c & 0x3FF) not in AG]
    top = collections.Counter(and_).most_common(1)[0]
    return 100.0 * top[1] / len(and_), len(and_), top[0]


# --------------------------------------------------------------------- rodagem
def carrega_plano():
    return json.load(open(PLANO)) if os.path.exists(PLANO) else {}


def base_de(alvo, guardado):
    """A grade como esta no disco, so tirando o que ESTA passada escreveu.

    Sem isso a idempotencia morre: planejar sobre um mapa ja desenhado nao volta
    ao mesmo lugar.
    """
    v = list(G.grade(alvo)[4])
    for idx, antigo, novo in guardado.get(alvo, {}).get("celulas", []):
        if v[idx] == novo:
            v[idx] = antigo
    return v


def roda(aplicar):
    tiles_novos, metas, attrs, catalogo = desenha_kit()
    if tiles_novos:
        print("kit: %d tiles novos (vagas %d a %d de %d, sobram %d), %d metatiles "
              "novos (locais %d a %d, ids %d a %d)"
              % (len(tiles_novos), min(tiles_novos), max(tiles_novos), TETO_TILES,
                 TETO_TILES - max(tiles_novos) - 1, len(metas), min(metas),
                 max(metas), 512 + min(metas), 512 + max(metas)))
    if aplicar:
        grava_tileset(tiles_novos, metas, attrs)
    guardado = carrega_plano()
    base = base_de(ALVO, guardado)
    L, W, H, v, escritas, contas = plano_mapa(catalogo, base)
    a, na, ida = regua(v, W, H, L)
    b, nb, idb = regua(v, W, H, L, escritas)
    print("%s: %d celulas de mancha, %d solidificadas, %d mudadas "
          "(familia areia %d, moita %d)"
          % (ALVO, sum(contas["manchas"].values()), contas["solidos"],
             len(escritas), contas["areia"], contas["moita"]))
    print("  mancha: " + ", ".join("%s x%d" % kv
                                   for kv in sorted(contas["manchas"].items())))
    print("  movel:  " + ", ".join("%s x%d" % kv
                                   for kv in sorted(contas["moveis"].items())))
    print("  regua: carimbo %d com %.1f%% de %d celulas ANTES; carimbo %d com "
          "%.1f%% de %d DEPOIS" % (ida, a, na, idb, b, nb))
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val
    conta = collections.Counter(c & 0x3FF for c in saida if not ((c >> 10) & 3))
    print("  os cinco mais comuns depois: " +
          ", ".join("%d x%d" % kv for kv in conta.most_common(5)))
    if aplicar:
        with open(f"{RAIZ}/{L['blockdata_filepath']}", "wb") as f:
            f.write(struct.pack("<%dH" % len(saida), *saida))
        guardado[ALVO] = {"celulas": [[i, v[i], escritas[i]]
                                      for i in sorted(escritas)]}
        with open(PLANO, "w") as f:
            json.dump(guardado, f, indent=1)
        print("aplicado")
    return 0


def desfaz():
    guardado = carrega_plano()
    if ALVO not in guardado:
        print("%s: nada a desfazer" % ALVO)
        return 0
    d, L, W, H, v = G.grade(ALVO)
    v, n = list(v), 0
    for idx, antigo, novo in guardado[ALVO]["celulas"]:
        if v[idx] == novo:
            v[idx] = antigo
            n += 1
    with open(f"{RAIZ}/{L['blockdata_filepath']}", "wb") as f:
        f.write(struct.pack("<%dH" % len(v), *v))
    guardado.pop(ALVO)
    with open(PLANO, "w") as f:
        json.dump(guardado, f, indent=1)
    print("%s: desfeitas %d celulas" % (ALVO, n))
    return 0


# ------------------------------------------------------------------ conferência
def _opacos(px):
    return sum(1 for linha in px for c in linha if c)


def confere(tiles_novos, metas, attrs, catalogo, plano):
    """Todas as regras desta onda, medidas sobre os dados que vierem.

    Ela e chamada DUAS vezes pelo auto-teste: uma com o plano de verdade, que tem
    que sair sem queixa, e uma por sabotagem, que tem que sair com a queixa certa.
    Regra conferida so no caminho feliz nao e regra.
    """
    mau = []
    dados = kit()
    import render_maps as RM
    tp = _tileset(PRIMARIO)
    ts = _tileset(SECUNDARIO)
    ap = G._attrs(PRIMARIO)
    asec = G._attrs(SECUNDARIO)

    def atributo(mt_id):
        if mt_id >= 512:
            local = mt_id - 512
            if local in attrs:
                return attrs[local]
            return asec[local] if local < len(asec) else 0
        return ap[mt_id] if mt_id < len(ap) else 0

    def entradas(mt_id):
        if mt_id >= 512 and (mt_id - 512) in metas:
            return list(metas[mt_id - 512])
        return ents_nossas(mt_id, tp, ts)

    def px_de(mt_id):
        return px_metatile(entradas(mt_id), tp, ts, tiles_novos, dados["paletas"])

    def opacos_de_cima(gid):
        op = 0
        for e in entradas(gid)[4:]:
            if e & 0x3FF:
                vaga = (e & 0x3FF) - len(tp["tiles"])
                if vaga in tiles_novos:
                    op += _opacos(tiles_novos[vaga])
                else:
                    t = RM.resolver_tile(tp, ts, e & 0x3FF)
                    op += _opacos(t) if t else 0
        return op

    # ------------------------------------------------------------ 1. orçamento
    if tiles_novos and max(tiles_novos) >= TETO_TILES:
        mau.append("estoura o teto de %d tiles" % TETO_TILES)
    if tiles_novos and min(tiles_novos) < TILE_LOCAL_0:
        mau.append("o kit grava tile abaixo da primeira vaga livre (%d)"
                   % TILE_LOCAL_0)
    if set(tiles_novos) & PINOS_ANIM:
        mau.append("o kit grava na vaga de tile pinada pela animacao da bandeira")
    if metas and max(metas) >= TETO_META:
        mau.append("estoura o teto de %d metatiles" % TETO_META)
    if metas and min(metas) < META_LOCAL_0:
        mau.append("o kit grava metatile abaixo da primeira vaga livre (%d)"
                   % META_LOCAL_0)
    livres = dados["vagas_livres"]
    for vaga, cores in sorted(dados["paletas"].items()):
        if not 6 <= int(vaga) <= 12:
            mau.append("a vaga %s nao e de secundario" % vaga)
        antigo = ts["paletas"][int(vaga)]
        vagos = set(livres.get(vaga) or [])
        for i in range(1, 16):
            if tuple(cores[i]) != tuple(antigo[i]) and i not in vagos:
                mau.append("a vaga %s mudou a cor do indice %d, que algum pixel "
                           "nosso usa" % (vaga, i))

    # ---------- 2. o kit não pode importar paleta de origem fora de VAGAS_PAL
    for ch in dados["tiles"]:
        _idx, ip = ch.split(":")
        if int(ip) not in VAGAS_PAL:
            mau.append("o kit importou a paleta %s da fonte, fora do plano" % ip)

    # ---------- 3. CHÃO de AREIA: atributo idêntico ao do carimbo, camada de
    # cima VAZIA e cor a menos de TETO_COR do carimbo
    px_carimbo = {q: px_de(CARIMBOS[q]) for q in CARIMBOS}
    _b, attr_areia = chao_nosso("areia")
    for nome, gid in catalogo["chao"].items():
        if atributo(gid) != attr_areia:
            mau.append("o chao %s (%d) tem atributo 0x%04X e o carimbo de areia "
                       "tem 0x%04X" % (nome, gid, atributo(gid), attr_areia))
        e = entradas(gid)
        if e[4:] != e[:4]:
            mau.append("o chao %s (%d) nao duplica a camada de baixo na de cima, "
                       "como o carimbo de areia faz" % (nome, gid))
        dc = _dist_cor(_cor_media(px_de(gid)), _cor_media(px_carimbo["areia"]))
        if dc > TETO_COR:
            mau.append("o chao %s (%d) esta a %.1f de cor do carimbo de areia, "
                       "acima do teto de %.1f" % (nome, gid, dc, TETO_COR))

    # ---------- 4. CHÃO de MOITA: atributo do 569, a MESMA arte de cima dele, e
    # a arte de cima nao pode tapar a celula inteira (portao E3)
    _bm, attr_moita = chao_nosso("moita")

    def opacos_de_baixo(gid):
        op = 0
        for e in entradas(gid)[:4]:
            if e & 0x3FF:
                vaga = (e & 0x3FF) - len(tp["tiles"])
                if vaga in tiles_novos:
                    op += _opacos(tiles_novos[vaga])
                else:
                    t = RM.resolver_tile(tp, ts, e & 0x3FF)
                    op += _opacos(t) if t else 0
        return op

    for nome, gid in catalogo["mata"].items():
        if atributo(gid) != attr_moita:
            mau.append("a mata %s (%d) tem atributo 0x%04X e o carimbo de moita "
                       "tem 0x%04X" % (nome, gid, atributo(gid), attr_moita))
        if opacos_de_cima(gid) == 0:
            mau.append("a mata %s (%d) esta sem arte em cima, e sem ela a celula "
                       "vira chao com layerType NORMAL" % (nome, gid))
        if opacos_de_cima(gid) >= 4 * 64:
            mau.append("a mata %s (%d) tapa o jogador inteiro (E3)" % (nome, gid))
        # `METATILE_LAYER_TYPE_NORMAL` desenha LIXO (o tile 0x3014) no BG3 e poe a
        # camada de BAIXO no BG2. Camada de baixo com buraco deixa o lixo
        # aparecer, e isso e defeito de tela que nenhum portao de planta pega.
        if opacos_de_baixo(gid) != 4 * 64:
            mau.append("a mata %s (%d) tem camada de baixo com buraco, e em "
                       "NORMAL o BG3 e lixo" % (nome, gid))

    # ---------- 5. MÓVEL: COVERED, comportamento zerado, e o NOSSO chão entrada
    # por entrada na camada de baixo
    base_areia, _a = chao_nosso("areia")
    for nome, gid in catalogo["moveis"].items():
        a = atributo(gid)
        if (a >> 12) & 0xF != 1:
            mau.append("o movel %s (%d) nao esta em COVERED" % (nome, gid))
        if a & 0xFF:
            mau.append("o movel %s (%d) importou comportamento 0x%02X da fonte"
                       % (nome, gid, a & 0xFF))
        if entradas(gid)[:4] != list(base_areia):
            mau.append("o movel %s (%d) nao tem o nosso chao de areia na camada "
                       "de baixo" % (nome, gid))

    # ---------- 6. nenhuma variante de chão e copia pixel a pixel de outra
    for qual, chave in (("areia", "chao"), ("moita", "mata")):
        lista = list(catalogo[chave].values()) + [CARIMBOS[qual]]
        pix = {mt: px_de(mt) for mt in lista}
        for i, a in enumerate(lista):
            for b in lista[i + 1:]:
                dd = _dist_pixels(pix[a], pix[b])
                if dd < PISO_VARIANTE:
                    mau.append("as variantes de chao %d e %d de %s tem distancia "
                               "%.1f, abaixo do piso de %.1f do varia_carimbo.py:"
                               " isso e enganar a regua"
                               % (a, b, qual, dd, PISO_VARIANTE))

    # ---------------------------------------- 7 a 13. o plano, célula a célula
    L, W, H, v, escritas, contas = plano
    d = json.load(open(f"{RAIZ}/data/maps/{ALVO}/map.json"))
    ev = E.eventos(d)
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val
    meus_chaos = {g: n for n, g in catalogo["chao"].items()}
    meus_matas = {g: n for n, g in catalogo["mata"].items()}
    meus_moveis = {g: n for n, g in catalogo["moveis"].items()}

    for i, val in escritas.items():
        x, y = i % W, i // W
        novo, velho = val & 0x3FF, v[i] & 0x3FF
        cn, cv = (val >> 10) & 3, (v[i] >> 10) & 3
        if (val >> 12) & 0xF != (v[i] >> 12) & 0xF:
            mau.append("%s: mudou ELEVACAO em (%d,%d)" % (ALVO, x, y))
        if cv and not cn:
            mau.append("%s: colisao 1 -> 0 em (%d,%d), que segue proibida"
                       % (ALVO, x, y))
        if novo in meus_chaos or novo in meus_matas:
            nome = meus_chaos.get(novo) or meus_matas.get(novo)
            if cn != cv or velho != CARIMBOS[catalogo["sobre"][nome]]:
                mau.append("%s: chao em celula errada em (%d,%d)" % (ALVO, x, y))
        elif novo in meus_moveis:
            nome = meus_moveis[novo]
            if cv or not cn:
                mau.append("%s: movel em (%d,%d) nao e solidificacao 0 -> 1"
                           % (ALVO, x, y))
            if velho != CARIMBOS[catalogo["sobre"][nome]]:
                mau.append("%s: movel fora do carimbo em (%d,%d)" % (ALVO, x, y))
            if (x, y) in ev:
                mau.append("%s: movel em cima do evento (%d,%d)" % (ALVO, x, y))
        else:
            mau.append("%s: metatile %d escrito em (%d,%d) e de fora do kit"
                       % (ALVO, novo, x, y))
        qual = "areia" if velho == CARIMBOS["areia"] else "moita"
        if (v[i] >> 12) & 0xF not in ELEVACOES[qual]:
            mau.append("%s: (%d,%d) tem elevacao fora da lista da familia"
                       % (ALVO, x, y))

    # 8. (comportamento, layerType) de toda célula ANDÁVEL fica igual
    for i in range(W * H):
        if (saida[i] >> 10) & 3:
            continue
        a, b = atributo(v[i] & 0x3FF), atributo(saida[i] & 0x3FF)
        if (a & 0xFF, a & 0xF000) != (b & 0xFF, b & 0xF000):
            mau.append("%s: celula andavel (%d,%d) mudou (comportamento, "
                       "layerType)" % (ALVO, i % W, i // W))
            break

    # 9 e 10. alcance a pe e LIGACAO a pe
    ini = E.partidas(d, W, H, v)
    antes, depois = E.alcance(v, W, H, ini), E.alcance(saida, W, H, ini)
    solid = {(i % W, i // W) for i in escritas
             if not ((v[i] >> 10) & 3) and ((escritas[i] >> 10) & 3)}
    if (antes - depois) - solid:
        mau.append("%s: o alcance a pe perdeu %d celulas alem das solidificadas: "
                   "%s" % (ALVO, len((antes - depois) - solid),
                           sorted((antes - depois) - solid)[:6]))
    if depois - antes:
        mau.append("%s: o alcance a pe GANHOU celula" % ALVO)
    mau += ["%s: %s" % (ALVO, q) for q in
            ligacao_intacta(componentes(v, W, H), componentes(saida, W, H), solid)]

    # 10b. A BEIRA DO MAR: nenhuma celula de AGUA foi escrita, e o conjunto de
    # celulas de agua e IDENTICO antes e depois. E este o portao que garante que
    # o alcance de Surf nao mudou.
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()

    def agua_de(grade):
        return {(i % W, i // W) for i in range(W * H)
                if beh(grade[i] & 0x3FF) in AG}
    if agua_de(v) != agua_de(saida):
        mau.append("%s: o conjunto de celulas de AGUA mudou, e com ele o alcance "
                   "de Surf" % ALVO)

    # 11. A MANCHA NÃO PODE SER ADIVINHAVEL, e o teste tem dois lados.
    # (a) PADRAO: nenhuma projecao simples da posicao pode ADIVINHAR a peca.
    # (b) FORMA: mancha e BOLHA, nao sal e pimenta, e a conta e o TAMANHO MEDIO
    # do pedaco conexo.
    mancha = {(i % W, i // W): (val & 0x3FF) for i, val in escritas.items()
              if (val & 0x3FF) in meus_chaos or (val & 0x3FF) in meus_matas}
    if len(mancha) < PISO_MANCHA:
        mau.append("%s: so %d celulas de mancha" % (ALVO, len(mancha)))
    if mancha:
        tot = len(mancha)
        cego = collections.Counter(mancha.values()).most_common(1)[0][1] / tot
        for rot, eixo in (("x", lambda p: p[0]), ("y", lambda p: p[1]),
                          ("x+y", lambda p: p[0] + p[1]),
                          ("x-y", lambda p: p[0] - p[1])):
            for mod in range(2, 9):
                tab = collections.defaultdict(collections.Counter)
                for p, mt_id in mancha.items():
                    tab[eixo(p) % mod][mt_id] += 1
                ac = sum(c.most_common(1)[0][1] for c in tab.values()) / tot
                if ac - cego > PISO_PADRAO:
                    mau.append("%s: saber %s mod %d adivinha a peca em %.0f%% das "
                               "celulas contra %.0f%% do chute cego: virou padrao"
                               % (ALVO, rot, mod, 100 * ac, 100 * cego))
        vistos, pedacos = set(), 0
        for p in sorted(mancha):
            if p in vistos:
                continue
            pedacos += 1
            pilha = [p]
            vistos.add(p)
            while pilha:
                q = pilha.pop()
                for dx, dy in N4:
                    rr = (q[0] + dx, q[1] + dy)
                    if rr in mancha and rr not in vistos:
                        vistos.add(rr)
                        pilha.append(rr)
        if len(mancha) / pedacos < 5.0:
            mau.append("%s: a mancha media tem so %.1f celulas (%d em %d "
                       "pedacos): virou sal e pimenta, nao bolha"
                       % (ALVO, len(mancha) / pedacos, len(mancha), pedacos))

    # 12. a regua tem que fechar em 20% ou menos
    b, nb, idb = regua(v, W, H, L, escritas)
    if b > TETO_REGUA:
        mau.append("%s: a regua ainda marca %.1f%% de carimbo dominante"
                   % (ALVO, b))
    return mau


# ------------------------------------------------------------------ auto-teste
def demo():
    """Prova positiva e as provas NEGATIVAS, cada sabotagem revertida em seguida.

    "Zero diferenca" so vale depois que a comparacao mostra que sabe reprovar.
    """
    tiles_novos, metas, attrs, catalogo = desenha_kit()
    guardado = carrega_plano()
    plano = plano_mapa(catalogo, base_de(ALVO, guardado))

    ts_do_disco = _tileset(SECUNDARIO)
    mau = confere(tiles_novos, metas, attrs, catalogo, plano)
    negativas = []

    def sabota(nome, funcao, espera):
        args = funcao()
        queixas = confere(*args)
        pega = [q for q in queixas if espera in q]
        if not pega:
            mau.append("SABOTAGEM NAO ACUSADA (%s): %s" % (nome, queixas[:2]))
        else:
            negativas.append((nome, pega[0]))

    def copia():
        L, W, H, v, esc, ct = plano
        return (dict(tiles_novos), dict(metas), dict(attrs),
                json.loads(json.dumps(catalogo)),
                (L, W, H, list(v), dict(esc), ct))

    # N1. colisão 1 -> 0 numa célula de mancha
    def n1():
        a = copia()
        L, W, H, v, esc, ct = a[4]
        i = sorted(esc)[0]
        v[i] = v[i] | (1 << 10)          # a celula ERA solida
        return a
    sabota("colisao 1 -> 0", n1, "colisao 1 -> 0")

    # N2. elevação alterada
    def n2():
        a = copia()
        L, W, H, v, esc, ct = a[4]
        i = sorted(esc)[0]
        esc[i] = (esc[i] & 0x0FFF) | (((v[i] >> 12) + 1) & 0xF) << 12
        return a
    sabota("elevacao alterada", n2, "mudou ELEVACAO")

    # N3. atributo de um metatile de CHÃO sabotado
    def n3():
        a = copia()
        gid = a[3]["chao"]["areia ondulada"]
        a[2][gid - 512] = (a[2][gid - 512] & 0xFF00) | 0x02   # MB_TALL_GRASS
        return a
    sabota("behavior de chao sabotado", n3, "tem atributo")

    # N4. layerType NORMAL onde devia ser COVERED
    def n4():
        a = copia()
        gid = a[3]["moveis"][MOVEIS_LP[0]["nome"]]
        a[2][gid - 512] = a[2][gid - 512] & 0x0FFF
        return a
    sabota("layerType NORMAL no movel", n4, "nao esta em COVERED")

    # N5. comportamento importado da fonte num móvel
    def n5():
        a = copia()
        gid = a[3]["moveis"][MOVEIS_LP[1]["nome"]]
        a[2][gid - 512] = a[2][gid - 512] | 0x02
        return a
    sabota("comportamento importado", n5, "importou comportamento")

    # N6. móvel SEM o nosso chão embaixo (o calçadão da fonte ficaria)
    def n6():
        a = copia()
        gid = a[3]["moveis"][MOVEIS_LP[0]["nome"]]
        e = list(a[1][gid - 512])
        e[0] = 0x5000 | 300
        a[1][gid - 512] = e
        return a
    sabota("chao da fonte no movel", n6, "nao tem o nosso chao")

    # N7. a MATA perdendo o arbusto: viraria chão liso com atributo NORMAL, ou
    # seja uma célula que desenha nada acima do boneco onde antes havia folhagem
    def n7():
        a = copia()
        gid = a[3]["mata"][MATA[0]["nome"]]
        e = list(a[1][gid - 512])
        e[4:] = [0, 0, 0, 0]
        a[1][gid - 512] = e
        return a
    sabota("mata sem o arbusto", n7, "sem arte em cima")

    # N8. célula andável com (comportamento, layerType) trocado
    def n8():
        a = copia()
        gid = a[3]["chao"]["areia grossa"]
        a[2][gid - 512] = 0x0021          # NORMAL onde o carimbo e COVERED
        return a
    sabota("layerType de chao trocado", n8, "mudou (comportamento")

    # N9. um móvel plantado em cima de célula de EVENTO
    def n9():
        a = copia()
        L, W, H, v, esc, ct = a[4]
        d = json.load(open(f"{RAIZ}/data/maps/{ALVO}/map.json"))
        ev = sorted(E.eventos(d))
        gid = a[3]["moveis"][MOVEIS_NOSSOS[0]["nome"]]
        for x, y in ev:
            i = y * W + x
            if (v[i] & 0x3FF) == CARIMBOS["areia"] and not ((v[i] >> 10) & 3):
                esc[i] = (v[i] & 0xF000) | (1 << 10) | gid
                return a
        raise SystemExit("nao ha evento em cima do carimbo para sabotar")
    sabota("movel em cima de evento", n9, "em cima do evento")

    # N10. a mancha espalhada AO ACASO, com as mesmas células
    def n10():
        a = copia()
        L, W, H, v, esc, ct = a[4]
        meus = set(catalogo["chao"].values()) | set(catalogo["mata"].values())
        cels = [i for i in esc if (esc[i] & 0x3FF) in meus]
        fam = collections.defaultdict(list)
        for i in cels:
            fam["areia" if (v[i] & 0x3FF) == CARIMBOS["areia"]
                else "moita"].append(i)
        for qual, idxs in fam.items():
            livres = [i for i in range(W * H)
                      if (v[i] & 0x3FF) == CARIMBOS[qual] and not ((v[i] >> 10) & 3)
                      and i not in esc]
            livres.sort(key=lambda i: _mistura(i, 0xDEAD))
            valores = [esc[i] & 0x3FF for i in idxs]
            for i in idxs:
                del esc[i]
            for k, val in enumerate(valores):
                if k < len(livres):
                    esc[livres[k]] = (v[livres[k]] & 0xFC00) | val
        return a
    sabota("mancha espalhada ao acaso", n10, "sal e pimenta")

    # N11. duas variantes de chão IGUAIS pixel a pixel: e enganar a regua
    def n11():
        a = copia()
        gid_a = a[3]["chao"]["areia ondulada"]
        gid_b = a[3]["chao"]["areia grossa"]
        a[1][gid_b - 512] = list(a[1][gid_a - 512])
        return a
    sabota("variante de chao duplicada", n11, "abaixo do piso de")

    # N12. cor nova escrita num índice que os NOSSOS pixels já usam. As vagas que
    # este kit usa (6 e 7) estao 100% livres, entao a sabotagem precisa declarar
    # uma vaga que TEM indice ocupado, que aqui e a 8 ou a 9.
    def n12():
        a = copia()
        dados = kit()
        alvo_vaga = None
        for vaga in range(6, 13):
            livres_v = set(dados["vagas_livres"].get(str(vaga)) or [])
            usados = [i for i in range(1, 16) if i not in livres_v]
            if usados:
                alvo_vaga, idx = str(vaga), usados[0]
                break
        if alvo_vaga is None:
            raise SystemExit("nao ha vaga com indice em uso para sabotar")
        pal = [list(c) for c in ts_do_disco["paletas"][int(alvo_vaga)]]
        pal[idx] = [255, 0, 255]
        dados["paletas"][alvo_vaga] = pal
        with open(KIT_JSON + ".sab", "w") as f:
            json.dump(dados, f)
        os.replace(KIT_JSON, KIT_JSON + ".bak")
        os.replace(KIT_JSON + ".sab", KIT_JSON)
        return a
    try:
        sabota("cor nova em indice ja usado", n12, "que algum pixel nosso usa")
    finally:
        if os.path.exists(KIT_JSON + ".bak"):
            os.replace(KIT_JSON + ".bak", KIT_JSON)

    # N13. gravar numa vaga de metatile que os mapas VIVOS usam
    def n13():
        a = copia()
        a[1][100] = list(a[1][min(a[1])])
        a[2][100] = 0x1000
        a[3]["chao"]["areia ondulada"] = 512 + 100
        return a
    sabota("grava em vaga de metatile viva", n13, "abaixo da primeira vaga livre")

    # N14. gravar tile numa das SEIS vagas pinadas pela animacao da bandeira
    def n14():
        a = copia()
        a[0][170] = [[0] * 8 for _ in range(8)]
        return a
    sabota("tile na vaga da bandeira", n14, "pinada pela animacao")

    # N15. mexer numa celula de AGUA: o alcance de Surf mudaria
    def n15():
        a = copia()
        L, W, H, v, esc, ct = a[4]
        beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
        AG = E.agua()
        gid = a[3]["chao"]["areia grossa"]
        for i in range(W * H):
            if beh(v[i] & 0x3FF) in AG:
                esc[i] = (v[i] & 0xFC00) | gid
                return a
        raise SystemExit("o mapa nao tem celula de agua para sabotar")
    sabota("celula de agua trocada", n15, "alcance de Surf")

    # ------------------------------------------------ o que está NO DISCO
    from PIL import Image
    meta_disco = _ler("metatiles.bin")
    attr_disco = _ler("metatile_attributes.bin")
    png = Image.open(f"{DESTINO}/tiles.png")
    cols = png.size[0] // 8
    px = png.load()

    postas = [l for l in metas if _entradas(meta_disco, l) == metas[l]]
    if not postas:
        print("aviso: o kit ainda nao foi aplicado no tileset; o caso de DISCO "
              "nao roda")
    else:
        if len(postas) != len(metas):
            mau.append("o kit esta pela metade no disco: %d de %d metatiles"
                       % (len(postas), len(metas)))
        for local, ents in metas.items():
            if _entradas(meta_disco, local) != ents:
                mau.append("metatile %d no disco nao e o do kit" % (512 + local))
            if struct.unpack_from("<H", attr_disco, local * 2)[0] != attrs[local]:
                mau.append("atributo do metatile %d no disco nao e o do kit"
                           % (512 + local))
        for vaga, tile in tiles_novos.items():
            if (vaga // cols) * 8 + 8 > png.size[1]:
                mau.append("a vaga de tile %d nao cabe no tiles.png" % vaga)
                continue
            x0, y0 = (vaga % cols) * 8, (vaga // cols) * 8
            if [[px[x0 + x, y0 + y] for x in range(8)] for y in range(8)] != tile:
                mau.append("o tile da vaga %d no disco nao e o do kit" % vaga)
        for vaga, cores in sorted(kit()["paletas"].items()):
            arq = [l.split() for l in
                   open(f"{DESTINO}/palettes/%s.pal" % vaga.zfill(2)).read().split("\n")[3:]
                   if l.strip()]
            if [[int(z) for z in c] for c in arq[:16]] != cores:
                mau.append("a paleta %s no disco nao e a do kit" % vaga)

    # ------------------------------------------------------- idempotencia
    L, W, H, v, escritas, contas = plano
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val
    volta = list(saida)
    for i in sorted(escritas):
        if volta[i] == escritas[i]:
            volta[i] = v[i]
    if volta != list(v):
        mau.append("%s: desfazer nao devolve a base" % ALVO)
    _, _, _, _, esc2, _ = plano_mapa(catalogo, volta)
    if esc2 != escritas:
        mau.append("%s: segunda passada deu plano diferente" % ALVO)

    if mau:
        print("DEMO VERMELHA")
        for x in dict.fromkeys(mau):
            print("  -", x)
        return 1
    print("DEMO VERDE")
    a, na, ida = regua(v, W, H, L)
    b, nb, idb = regua(v, W, H, L, escritas)
    print("  %-14s %d celulas mudadas, %d solidificadas, regua %.1f%% -> %.1f%%"
          % (ALVO, len(escritas), contas["solidos"], a, b))
    print("  %d tiles, %d metatiles, %d provas negativas:"
          % (len(tiles_novos), len(metas), len(negativas)))
    for nome, queixa in negativas:
        print("    %-34s -> %s" % (nome, queixa[:96]))
    return 0


# ------------------------------------------------- prova de TILE contra a ROM
def prova_tiles():
    """Cada tile do kit, DEPOIS de reindexado, contra o tile da ROM: zero pixel.

    Reindexar nibble e a unica coisa que este kit faz com o desenho da fonte, e e
    exatamente onde um erro passaria despercebido: a arte continuaria parecendo
    arte, com as cores trocadas de lugar.
    """
    ferr = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/romhacks"
    if not os.path.isdir(ferr):
        raise SystemExit("--prova-tiles so roda na maquina que tem as ROMs")
    sys.path.insert(0, f"{ferr}/ferramentas")
    from gbamap import Rom  # noqa: E402
    p = os.path.join(ferr, LP["slug"])
    gba = [f for f in sorted(os.listdir(p)) if f.lower().endswith(".gba")][0]
    r = Rom(os.path.join(p, gba))
    r.n_meta_pri, r.n_tiles_pri, r.n_pal_pri = LP["split"]
    t1 = r.parse_tileset(LP["pri"])
    t2 = r.parse_tileset(LP["sec"])
    NP = r.n_tiles_pri
    pal = {i: _rgb(t1 if i < 6 else t2, i) for i in range(16)}
    dados = kit()
    n, dif = 0, 0
    for ch, px_kit in dados["tiles"].items():
        idx, ip = (int(z) for z in ch.split(":"))
        crus = (_nibbles(t1["tiles"], idx) if idx < NP
                else _nibbles(t2["tiles"], idx - NP))
        vaga = dados["tiles_vaga"][ch]
        cores_nossas = dados["paletas"][str(vaga)]
        for y in range(8):
            for x in range(8):
                n += 1
                a = tuple(pal[ip][crus[y][x]]) if crus[y][x] else None
                b = (tuple(cores_nossas[px_kit[y][x]]) if px_kit[y][x] else None)
                if a != b:
                    dif += 1
                    if dif == 1:
                        print("  primeiro: tile %s (%d,%d) rom=%s kit=%s"
                              % (ch, x, y, a, b))
    print("tiles do kit contra a ROM: %d pixels, %d diferentes" % (n, dif))
    # a conta tem que saber REPROVAR
    ch0 = sorted(dados["tiles"])[0]
    idx0, ip0 = (int(z) for z in ch0.split(":"))
    salvo = [linha[:] for linha in dados["tiles"][ch0]]
    dados["tiles"][ch0][0][0] = (salvo[0][0] + 1) % 16
    crus = (_nibbles(t1["tiles"], idx0) if idx0 < NP
            else _nibbles(t2["tiles"], idx0 - NP))
    cores_nossas = dados["paletas"][str(dados["tiles_vaga"][ch0])]
    ruim = 0
    for y in range(8):
        for x in range(8):
            a = tuple(pal[ip0][crus[y][x]]) if crus[y][x] else None
            b = (tuple(cores_nossas[dados["tiles"][ch0][y][x]])
                 if dados["tiles"][ch0][y][x] else None)
            if a != b:
                ruim += 1
    print("com UM nibble trocado no kit: %d pixels diferentes (tem que ser > 0)"
          % ruim)
    return 0 if dif == 0 and ruim > 0 else 1


def main():
    if "--extrai" in sys.argv:
        return extrai()
    if "--prova-tiles" in sys.argv:
        return prova_tiles()
    if "--desfazer" in sys.argv:
        return desfaz()
    if "--demo" in sys.argv or "--autoteste" in sys.argv:
        return demo()
    if "--so-tileset" in sys.argv:
        t, m, at, c = desenha_kit()
        grava_tileset(t, m, at)
        print("tileset escrito: %d tiles, %d metatiles" % (len(t), len(m)))
        return 0
    return roda("--aplicar" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
