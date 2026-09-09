#!/usr/bin/env python3
"""Refino de arte de `CelesticTown` (RUINA) e `SolaceonTown` (CAMPO), com peca
importada do `Pokemon Light Platinum`, no `gTileset_Celestic`.

POR QUE EXISTE. A regua de `dev_scripts/regua_cidades.py` mede o "tapete" de chao
repetido, e as duas piores cidades que sobraram em Sinnoh sao estas: em
`CelesticTown` o metatile 1 (a grama lisa do PRIMARIO) ocupa 387 das 537 celulas
andaveis a pe, 72,1%; em `SolaceonTown` ocupa 777 de 1.209, 64,3%. Sao dois
mapas grandes de gramado liso com casa em cima. O alvo desta onda e carimbo
dominante de 20,0% ou menos, o que quer dizer trocar pelo menos 280 celulas em
Celestic e 536 em Solaceon.

O TEMA DE CADA UMA, e nenhuma das duas ganha o tema da outra. `CelesticTown` e a
vila do santuario antigo: entra PEDRA, laje solta, pedregulho, arvore morta e
muro caido. `SolaceonTown` e a vila rural do lado das ruinas: entra CAMPO,
canteiro de plantacao, medao de feno, fardo de palha e arvore dourada.

O ORCAMENTO DE PALETA, que e a conta que decidiu tudo. `NUM_PALS_TOTAL` e 13
(`include/fieldmap.h`): seis vagas sao do primario e SETE do secundario, da 6 a
12. No `gTileset_Celestic` as vagas 6, 7, 8, 9, 11 e 12 estavam em uso e sobrava
UMA, a 10. Uma vaga so nao paga dois temas: medido nesta frente, o kit de ruina
pede 10 cores nao-zero e o de campo pede 14, e a uniao dos dois da 24 para 15
lugares.

A SEGUNDA VAGA FOI PROVADA POR CONTAGEM DE COR, e e o achado que destrava a
rodada. A vaga 7 do `gTileset_Celestic` gasta uma vaga inteira com CINCO cores, e
so DOIS tiles do secundario pintam com ela (os tiles 44 e 51 de antes da
compactacao). A vaga 9 usa 13 cores, e o `.pal` dela declara 16: os indices 6 e 8
estao declarados e NENHUM pixel os usa. Das cinco cores da vaga 7, TRES ja
existem na vaga 9, com o mesmo RGB exato ((120,120,128), (88,88,112) e
(64,72,104)); as outras duas ((184,176,80) e (224,216,128)) cabem exatamente nos
dois indices ociosos. Entao a vaga 7 e fundida DENTRO da vaga 9 sem aproximar
nenhuma cor e sem mover nenhuma cor que ja estava la: os 13 indices vivos da vaga
9 ficam onde estao, byte a byte, e so os dois indices mortos sao preenchidos.
Quem pintava com a 7 passa a pintar com a 9. A vaga 7 fica LIVRE.

    vaga  7   CAMPO   14 cores, do secundario 0x286DE4 do Light Platinum
    vaga 10   RUINA   10 cores, do secundario 0x286F64 do Light Platinum

O `compacta_paletas.py` nao faz essa fusao e nao esta errado: ele trata a vaga 9
como PINO e pino nao entra em grupo. Aqui a vaga 9 tambem nao entra em grupo
nenhum, ela so RECEBE nos indices que estavam mortos, o que preserva o desenho de
quem ja pintava com ela por construcao e nao por cuidado. A prova e render: os
sete layouts do tileset saem com zero pixel diferente.

O ORCAMENTO DE TILE. O `gTileset_Celestic` tinha 448 tiles de 512 com 165
MORTOS. `compacta_tileset.py gTileset_Celestic --aplicar` levou para 283 vivos e
224 vagas livres, com os sete mapas renderizando com o mesmo md5 de PNG. A fusao
da vaga 7 gasta duas vagas (283 e 284), porque os dois tiles que pintavam com a
vaga 7 tambem sao usados com OUTRA paleta e nao podem ser reindexados no lugar:
cada um ganha uma copia com os nibbles remapeados. O kit desta rodada comeca na
vaga 285.

COMO CADA PECA E MONTADA, e onde mora a armadilha.

  - A CAMADA DE BAIXO E SEMPRE A NOSSA GRAMA em peca de papel `mancha`, `movel` e
    `topo`: a entrada do nosso metatile 1, quadrante por quadrante, byte a byte.
    Sem isso a peca importada chega com um retangulo do chao do Light Platinum em
    volta, e o chao dele NAO e o nosso: a grama do LP e (139,189,82), um verde
    amarelado, e a nossa e (115,197,164), um verde azulado. Sao cores diferentes
    e a emenda apareceria.
  - Em peca de papel `base` (a celula de baixo de uma peca de duas ou tres de
    altura) a camada de baixo pode ser ARTE de verdade, e ai ela entra. Quem
    separa arte de chao e EVIDENCIA, nao constante decorada: o censo dos padroes
    de camada de baixo do tileset inteiro da fonte diz que padrao se repete. No
    `0x286F64` o padrao (0x8369,0x836A,0x8379,0x837A) aparece em 38 metatiles, o
    (0x6203)x4 em 21 e o (0x6228,0x6229,0x6238,0x6239) em 8; nenhum padrao de
    arte de verdade passa de 2. Todo padrao com `LIMIAR_CHAO_FONTE` ocorrencias
    ou mais, e todo padrao de quatro tiles IGUAIS, e chao da fonte, e cada TILE
    que aparece nesses padroes vai para a lista de tile-de-chao. Entrada da
    camada de baixo que aponte para tile-de-chao, ou que seja zero, recebe a
    nossa grama.
  - QUADRANTE 100% OPACO DA CAMADA DE CIMA DESCE para a camada de baixo em toda
    celula que continua ANDAVEL. Isso tem duas consequencias e as duas sao
    boas: a laje de pedra passa a ler como CHAO em vez de adesivo, e a camada de
    cima de uma celula andavel nunca fica 100% opaca nos quatro quadrantes, que
    e exatamente o defeito E3 do `dev_scripts/qa/mapas_qa.py` (bloco preto
    andavel, o metatile que tapa o jogador inteiro). O portao nao e "confiei":
    o auto-teste conta pixel opaco quadrante a quadrante depois da descida.
  - Celula que vira SOLIDA (colisao 0 -> 1) leva comportamento ZERADO e
    layerType COVERED (0x1000). COVERED poe as duas camadas ABAIXO do sprite,
    que e o que faz o jogador parado ao sul aparecer NA FRENTE do medao de feno.
    Comportamento e id semantico e a regra 5 desta onda proibe importar id da
    fonte, so arte.
  - Celula ANDAVEL leva o atributo INTEIRO do nosso metatile 1 (0x0000), que e o
    que a regra 3 desta onda cobra de toda celula que continua andavel.

A LEI DE COLISAO desta onda: 0 -> 1 e PERMITIDA em celula que nao seja caminho,
warp, evento nem alcance de script, desde que o alcance a pe continue o mesmo.
1 -> 0 e PROIBIDA e fica em ZERO celulas. Elevacao intacta em 100% das palavras.

OS DOIS PORTOES DE ALCANCE, e o segundo nao e enfeite. O primeiro e busca em
largura a partir de todo warp e todo object_event, respeitando elevacao
(`enfeita_cidades.alcance`): `depois == antes - solidificadas`. O segundo e
rotulacao de COMPONENTES de chao andavel: nenhum pedaco pode se partir nem se
juntar. Em `SnowpointCity` o primeiro passou VERDE numa sabotagem que fechava um
corredor com warp dos DOIS lados, porque cada metade continuava alcancavel a
partir do proprio warp. Os dois rodam aqui, e rodam NA HORA, movel a movel.

DE ONDE VEM A ARTE. `Pokemon Light Platinum`, de WesleyFG, base Ruby (AXVE), md5
7fd2c08735459d99fa23fdaa9b755486, copia privada em
`fontes-mapas/romhacks/light-platinum/`. A ROM NUNCA entra no repositorio: o que
esta versionado e o kit CONVERTIDO em `dev_scripts/campo_celestic_kit.json`, com
a paleta em RGB e o tile em nibble ja reindexado para a vaga nova. `--extrai`
regenera esse arquivo e confere o md5 antes de ler um byte; `--aplicar` nunca
abre ROM nenhuma. Credito em `CREDITS.md`.

ORDEM DE RODAR, e ela nao e negociavel:

    python3 dev_scripts/compacta_tileset.py gTileset_Celestic --aplicar
    python3 dev_scripts/campo_celestic.py --aplicar

Uso:
    python3 dev_scripts/campo_celestic.py             # mede e mostra o plano
    python3 dev_scripts/campo_celestic.py --aplicar   # escreve tileset e mapas
    python3 dev_scripts/campo_celestic.py --desfazer  # devolve os map.bin
    python3 dev_scripts/campo_celestic.py --demo      # auto-teste
    python3 dev_scripts/campo_celestic.py --autoteste # idem
    python3 dev_scripts/campo_celestic.py --extrai    # regera o kit da ROM
"""
import collections
import heapq
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")
import arte_ginasios_sinnoh as G     # noqa: E402
import enfeita_cidades as E          # noqa: E402

DESTINO = f"{RAIZ}/data/tilesets/secondary/celestic"
KIT_JSON = f"{RAIZ}/dev_scripts/campo_celestic_kit.json"
PLANO = f"{RAIZ}/dev_scripts/campo_celestic.json"

PRIMARIO = "gTileset_GeneralSinnoh"
SECUNDARIO = "gTileset_Celestic"
# os SETE layouts que dividem o gTileset_Celestic. Os cinco que nao sao alvo tem
# que renderizar com zero pixel diferente.
IRMAOS = ["CelesticTown", "SolaceonTown", "Route209", "Route210_North",
          "Route210_South", "Route211_East", "Route215"]
ALVOS = ["CelesticTown", "SolaceonTown"]

CHAO = 1                    # metatile do PRIMARIO: a grama lisa das duas cidades
PAL_CAMPO = 7               # vaga liberada pela fusao da 7 dentro da 9
PAL_RUINA = 10              # a unica vaga que ja estava livre
PAL_FUNDE_EM = 9            # a vaga que RECEBE as cores da 7

TILE_LOCAL_0 = 285          # 283 vivos depois da compactacao + 2 copias da fusao
TILE_FUSAO_0 = 283          # onde as duas copias da fusao moram
META_LOCAL_0 = 262          # id global 774; o maior id em uso nos 7 mapas e 773
TETO_TILES = 512
TETO_META = 512
MARGEM = 2
LIMIAR_CHAO_FONTE = 4       # padrao de camada de baixo repetido tantas vezes e chao

FONTE_ROM = ("/Users/duarte/Projetos/pokemon-claude/fontes-mapas/romhacks"
             "/light-platinum")
MD5_FONTE = "7fd2c08735459d99fa23fdaa9b755486"

FONTES = {
    "ruina": dict(ts1=0x286CF4, ts2=0x286F64, pal=PAL_RUINA,
                  mapa="grupo 24 mapa 84, a montanha do templo, 50x70"),
    "campo": dict(ts1=0x286CF4, ts2=0x286DE4, pal=PAL_CAMPO,
                  mapa="grupo 0 mapa 3, a vila verde, 36x46"),
}

# ------------------------------------------------------------------- as PECAS
# MANCHA: peca de UMA celula que continua ANDAVEL, com o mesmo atributo do nosso
# metatile 1. E ela quem move a regua, e por isso ela e a lista mais longa. O
# espelho custa ZERO tile: e o mesmo desenho com o bit 0x400 (horizontal) ou
# 0x800 (vertical) ligado, e e o proprio Light Platinum que faz isso nos pares
# dele. Espelho NAO e copia pixel a pixel: o desenho sai virado na tela.
MANCHAS = [
    dict(nome="laje solta",          fonte="ruina", lp=104, esp=""),
    dict(nome="laje solta virada",   fonte="ruina", lp=104, esp="h"),
    dict(nome="laje solta deitada",  fonte="ruina", lp=104, esp="v"),
    dict(nome="laje solta girada",   fonte="ruina", lp=104, esp="hv"),
    dict(nome="cascalho",            fonte="ruina", lp=38,  esp=""),
    dict(nome="cascalho virado",     fonte="ruina", lp=38,  esp="h"),
    dict(nome="pedra rachada",       fonte="ruina", lp=39,  esp=""),
    dict(nome="broto norte",         fonte="campo", lp=16,  esp=""),
    dict(nome="broto nordeste",      fonte="campo", lp=17,  esp=""),
    dict(nome="broto oeste",         fonte="campo", lp=24,  esp=""),
    dict(nome="broto leste",         fonte="campo", lp=25,  esp=""),
    dict(nome="broto sul",           fonte="campo", lp=32,  esp=""),
    # o metatile 33 do 0x286DE4 NAO entra: ele desenha os mesmos 256 pixels do
    # 17, e o caso 9 do auto-teste reprova variante que e copia pixel a pixel de
    # outra (regra 9 da onda). O canteiro usa o 17 nas duas pontas da direita.
    dict(nome="terra batida",        fonte="campo", lp=127, esp=""),
    dict(nome="terra batida 2",      fonte="campo", lp=135, esp=""),
    dict(nome="tufo de capim",       fonte="campo", lp=162, esp=""),
    dict(nome="tufo de capim virado", fonte="campo", lp=162, esp="h"),
]

# MOVEL: retangulo de celulas. `grade` sao os metatiles da fonte em ordem de
# leitura e `solidas` diz quais celulas viram SOLIDAS. A convencao segue o que o
# proprio Light Platinum desenha: a linha de BAIXO e solida e as de cima
# continuam andaveis, para o jogador passar ATRAS da copa e aparecer NA FRENTE
# do tronco. Peca de uma linha so e solida inteira.
#
# Cada composto foi lido do MAPA do hack, nao do atlas: o par (cima, baixo) e o
# par (esquerda, direita) sao os que aparecem juntos nos mapas de verdade, com a
# contagem medida (ex.: (40,48) 42 vezes, (69,77) 12, (26,34) 5, (320,328) 5).
MOVEIS = [
    dict(nome="pedregulho", fonte="ruina", tema="ruina",
         grade=[[40, 41], [48, 49]], solidas=[[0, 0], [1, 1]],
         onde="beira", quantos=7, espaco=6),
    dict(nome="arvore morta", fonte="ruina", tema="ruina",
         grade=[[69, 70], [77, 78]], solidas=[[0, 0], [1, 1]],
         onde="beira", quantos=8, espaco=5),
    dict(nome="arvore morta alta", fonte="ruina", tema="ruina",
         grade=[[71, 79], [69, 70], [77, 78]], solidas=[[0, 0], [0, 0], [1, 1]],
         onde="beira", quantos=4, espaco=7),
    dict(nome="monte de pedra", fonte="ruina", tema="ruina",
         grade=[[88], [96]], solidas=[[0], [1]],
         onde="beira", quantos=10, espaco=4),
    dict(nome="muro caido", fonte="ruina", tema="ruina",
         grade=[[44, 45, 46, 47]], solidas=[[1, 1, 1, 1]],
         onde="qualquer", quantos=4, espaco=9),
    dict(nome="laje do altar", fonte="ruina", tema="ruina",
         grade=[[154, 155, 156, 157, 158, 159]], solidas=[[1, 1, 1, 1, 1, 1]],
         onde="qualquer", quantos=1, espaco=12),
    dict(nome="medao de feno", fonte="campo", tema="campo",
         grade=[[26, 27], [34, 35]], solidas=[[0, 0], [1, 1]],
         onde="qualquer", quantos=5, espaco=8),
    dict(nome="fardo de palha", fonte="campo", tema="campo",
         grade=[[50, 51, 52]], solidas=[[1, 1, 1]],
         onde="qualquer", quantos=6, espaco=7),
    dict(nome="fardo redondo", fonte="campo", tema="campo",
         grade=[[96]], solidas=[[1]],
         onde="qualquer", quantos=9, espaco=5),
    # Os tres fardos redondos abaixo entraram DE GRACA: as cores deles ja estao
    # todas na vaga 7 que o kit paga, entao custam tile e metatile e ZERO cor.
    # Eles existem porque o primeiro render mostrou uma vila de domos dourados
    # todos iguais: medao de feno, arvore dourada e arvore dourada clara leem
    # igual de longe, e o que quebra isso e peca de UMA celula com silhueta
    # diferente.
    dict(nome="fardo redondo claro", fonte="campo", tema="campo",
         grade=[[40]], solidas=[[1]],
         onde="qualquer", quantos=8, espaco=5),
    dict(nome="fardo redondo escuro", fonte="campo", tema="campo",
         grade=[[41]], solidas=[[1]],
         onde="qualquer", quantos=8, espaco=5),
    dict(nome="monte de palha", fonte="campo", tema="campo",
         grade=[[66, 67]], solidas=[[1, 1]],
         onde="qualquer", quantos=7, espaco=6),
    dict(nome="palheiro largo", fonte="campo", tema="campo",
         grade=[[58, 59, 60]], solidas=[[1, 1, 1]],
         onde="qualquer", quantos=4, espaco=8),
    dict(nome="arvore dourada", fonte="campo", tema="campo",
         grade=[[320, 321], [328, 329]], solidas=[[0, 0], [1, 1]],
         onde="beira", quantos=6, espaco=6),
    dict(nome="arvore dourada clara", fonte="campo", tema="campo",
         grade=[[330, 331], [328, 329]], solidas=[[0, 0], [1, 1]],
         onde="beira", quantos=4, espaco=6),
]

TETO_MOVEIS = 60            # pecas de movel por cidade
ESPACO_ENTRE_MOVEIS = 2     # Chebyshev minimo entre duas pecas QUAISQUER

# ------------------------------------------------------------ o plano de cada
# `trilha` sao as manchas que pintam o caminho batido entre as portas; `bolhas`
# sao os grupos que crescem em mancha organica pelo resto do gramado. Nenhuma
# cidade recebe o tema da outra: Celestic e pedra, Solaceon e campo. O que
# ATRAVESSA os dois e so o que existe nos dois lugares de verdade: capim e terra
# batida em Celestic, pedra solta no pasto de Solaceon.
CIDADES = {
    "CelesticTown": dict(
        temas=["ruina"],
        trilha=["laje solta", "laje solta virada", "laje solta deitada",
                "laje solta girada"],
        borda_trilha=85,
        folga_semente=3,
        bolhas=[
            dict(pecas=["cascalho", "cascalho virado", "pedra rachada"],
                 quantas=10, tam=(5, 11)),
            dict(pecas=["terra batida", "terra batida 2"],
                 quantas=8, tam=(4, 8)),
            dict(pecas=["tufo de capim", "tufo de capim virado"],
                 quantas=10, tam=(4, 9)),
            # a segunda passada de cascalho e quem FECHA o gramado, e ela vem
            # por ultimo de proposito: os grupos escassos servem primeiro (a
            # licao medida no `neve_snowpoint2.py`), e o que sobrar vira pedra,
            # que e o tema da cidade.
            dict(pecas=["cascalho", "cascalho virado", "pedra rachada"],
                 quantas=22, tam=(4, 10)),
        ],
        canteiros=0,
    ),
    "SolaceonTown": dict(
        temas=["campo"],
        trilha=["terra batida", "terra batida 2", "laje solta",
                "laje solta virada"],
        borda_trilha=80,
        folga_semente=4,
        bolhas=[
            dict(pecas=["broto norte", "broto nordeste", "broto oeste",
                        "broto leste", "broto sul"],
                 quantas=24, tam=(6, 14)),
            dict(pecas=["cascalho", "cascalho virado", "pedra rachada",
                        "laje solta deitada", "laje solta girada"],
                 quantas=18, tam=(5, 11)),
            dict(pecas=["tufo de capim", "tufo de capim virado"],
                 quantas=20, tam=(5, 12)),
        ],
        canteiros=9,
    ),
}

# CANTEIRO: o bloco de plantacao de Solaceon, 2 de largura e de 3 a 5 de altura,
# montado como o Light Platinum monta (linha de cima 16/17, miolo 24/25 repetido,
# linha de baixo 32/33). Continua ANDAVEL do comeco ao fim: e chao plantado, nao
# obstaculo, e por isso ele nao encosta em nenhum portao de alcance.
CANTEIRO = dict(topo=["broto norte", "broto nordeste"],
                meio=["broto oeste", "broto leste"],
                base=["broto sul", "broto nordeste"],
                alturas=(3, 5))

N4 = E.N4


def _mistura(*n):
    """Hash determinista de inteiros, 32 bits. Nada de `random`: o plano tem que
    sair identico em qualquer maquina e em qualquer versao de Python."""
    h = 0x811C9DC5
    for x in n:
        h = ((h ^ (x & 0xFFFFFFFF)) * 0x01000193) & 0xFFFFFFFF
        h ^= h >> 15
    return h


def _espelha4(quad, eixo):
    """Espelho de uma camada de 4 quadrantes. 'h' troca as colunas e liga 0x400,
    'v' troca as linhas e liga 0x800."""
    fora = list(quad)
    if "h" in eixo:
        fora = [0 if (fora[q] & 0x3FF) == 0 else (fora[q] ^ 0x400)
                for q in (1, 0, 3, 2)]
    if "v" in eixo:
        fora = [0 if (fora[q] & 0x3FF) == 0 else (fora[q] ^ 0x800)
                for q in (2, 3, 0, 1)]
    return fora


def _entradas(bin_meta, local):
    return list(struct.unpack_from("<8H", bin_meta, local * 16))


def papel_de(mv, li, ci):
    """O papel de uma celula de movel, e ele decide de quem e a camada de baixo.

      `topo`   celula que continua ANDAVEL: a camada de baixo e a NOSSA grama.
      `movel`  celula SOLIDA de uma peca de UMA linha so. Objeto de uma celula de
               altura pousa NO chao, ele nao desenha chao debaixo de si, entao a
               camada de baixo tambem e a nossa grama. Foi assim que o fardo
               redondo (metatile 96 do 0x286DE4) deixou de trazer junto os cinco
               tons de grama sombreada da fonte, que a peca desenha embaixo dela
               e que custariam cinco cores da vaga 7 para nao aparecer nunca.
      `base`   celula SOLIDA que NAO e a primeira linha da peca. Ai a camada de
               baixo pode ser ARTE de verdade e ela entra: e o caso do tronco da
               arvore dourada (metatiles 328 e 329), cuja camada de CIMA e vazia
               e cujo desenho inteiro mora embaixo. Mesmo aqui o filtro de chao
               da fonte continua valendo tile a tile.
    """
    if not mv["solidas"][li][ci]:
        return "topo"
    return "movel" if li == 0 else "base"


def _opacos(px):
    return sum(1 for linha in px for c in linha if c)


# ------------------------------------------------------------------- extracao
def extrai():
    """Regera `campo_celestic_kit.json` a partir da ROM privada do hack.

    So roda na maquina que tem `fontes-mapas/romhacks/`. O que sai daqui e o
    asset convertido (tile em nibble ja reindexado para a vaga nova e paleta em
    RGB), nunca a ROM.
    """
    if not os.path.isdir(FONTE_ROM):
        raise SystemExit("nao achei %s: --extrai so roda na maquina que tem a "
                         "ROM. O kit ja extraido esta em %s"
                         % (FONTE_ROM, os.path.relpath(KIT_JSON, RAIZ)))
    ferr = os.path.dirname(FONTE_ROM)
    sys.path.insert(0, f"{ferr}/ferramentas")
    import hashlib
    from gbamap import Rom  # noqa: E402

    gba = [f for f in sorted(os.listdir(FONTE_ROM)) if f.lower().endswith(".gba")]
    if not gba:
        raise SystemExit("nenhum .gba em %s" % FONTE_ROM)
    caminho = os.path.join(FONTE_ROM, gba[0])
    md5 = hashlib.md5(open(caminho, "rb").read()).hexdigest()
    if md5 != MD5_FONTE:
        raise SystemExit("a ROM em %s tem md5 %s e o kit foi feito com %s: nao "
                         "leio um byte de uma copia diferente"
                         % (caminho, md5, MD5_FONTE))
    r = Rom(caminho)
    # Light Platinum e base Ruby (AXVE) e o split de VRAM dele e o do Emerald.
    r.n_meta_pri, r.n_tiles_pri, r.n_pal_pri = 512, 512, 6
    npri = r.n_tiles_pri

    def nibbles(dados, local):
        """8 linhas de 8 nibbles, o pixel PAR no nibble BAIXO (ver extrai_tileset)."""
        b = dados[local * 32:local * 32 + 32]
        return [[(b[y * 4 + (x >> 1)] >> (0 if x % 2 == 0 else 4)) & 0xF
                 for x in range(8)] for y in range(8)]

    def rgb(ts, i):
        c = struct.unpack_from("<16H", ts["pal"], i * 32)
        return [[((v >> s) & 0x1F) * 255 // 31 for s in (0, 5, 10)] for v in c]

    # o que cada fonte precisa entregar
    quero = collections.defaultdict(list)
    for m in MANCHAS:
        quero[m["fonte"]].append(("mancha", m["lp"]))
    for mv in MOVEIS:
        for li, linha in enumerate(mv["grade"]):
            for ci, lp in enumerate(linha):
                quero[mv["fonte"]].append((papel_de(mv, li, ci), lp))

    abertas, pecas = {}, []
    tiles_px, tiles_pal = {}, {}
    chao_fonte, censo_fonte = {}, {}
    for chave, F in FONTES.items():
        t1 = r.parse_tileset(F["ts1"])
        t2 = r.parse_tileset(F["ts2"])
        n_meta = len(t2["meta"]) // 16
        abertas[chave] = dict(
            hack="Pokemon Light Platinum", autor="WesleyFG", arquivo=gba[0],
            md5=md5, base="Ruby (AXVE)", ts1="0x%X" % F["ts1"],
            ts2="0x%X" % F["ts2"], mapa=F["mapa"], n_tiles_pri=npri,
            split="512/512/6")

        # O CHAO DA FONTE, achado por EVIDENCIA. Censo dos padroes de camada de
        # baixo do tileset inteiro: padrao repetido e chao, padrao de arte
        # aparece uma ou duas vezes. Quatro tiles IGUAIS tambem e chao, que e a
        # assinatura que o `neve_snowpoint2.py` ja usava.
        censo = collections.Counter()
        for i in range(n_meta):
            censo[tuple(_entradas(t2["meta"], i)[:4])] += 1
        chao = set()
        for pat, k in censo.items():
            se_repete = len({x & 0x3FF for x in pat}) == 1
            if k >= LIMIAR_CHAO_FONTE or se_repete:
                chao |= {x & 0x3FF for x in pat if x & 0x3FF}
        chao_fonte[chave] = sorted(chao)
        censo_fonte[chave] = [[list(p), k] for p, k in censo.most_common(8)]

        vistos = set()
        for papel, local in quero[chave]:
            if (papel, local) in vistos:
                continue
            vistos.add((papel, local))
            if local >= n_meta:
                raise SystemExit("%s: o metatile %d nao existe no tileset"
                                 % (chave, local))
            ents = _entradas(t2["meta"], local)
            baixo_e_chao = papel in ("mancha", "topo", "movel")
            for k, val in enumerate(ents):
                idx, ip = val & 0x3FF, (val >> 12) & 0xF
                if idx == 0:
                    continue
                if k < 4:
                    # a camada de baixo so entra em peca de papel `base`, e
                    # mesmo ali so quando o tile nao e chao da fonte
                    if baixo_e_chao or idx in chao:
                        continue
                lado, li = ("p", idx) if idx < npri else ("s", idx - npri)
                ch = "%s:%s:%d:%d" % (chave, lado, li, ip)
                tiles_pal[ch] = (chave, ip)
                tiles_px[ch] = nibbles(t1["tiles"] if lado == "p" else t2["tiles"],
                                       li)
            pecas.append(dict(papel=papel, fonte=chave, lp=local,
                              ents=ents,
                              attr=struct.unpack_from("<H", t2["attr"],
                                                      local * 2)[0]))
        abertas[chave]["paletas"] = {
            str(i): rgb(t1 if i < 6 else t2, i) for i in range(16)}

    # ------------------------------------------------ as paletas novas, 7 e 10
    # Uniao das cores NAO-ZERO realmente pintadas pelos tiles de cada tema. Cor
    # igual conta UMA vez. Nada e aproximado: se estourar 15, para.
    paletas, indices = {}, {}
    for chave, F in FONTES.items():
        usadas = []
        for ch in sorted(tiles_px):
            if not ch.startswith(chave + ":"):
                continue
            _f, ip = tiles_pal[ch]
            origem = abertas[chave]["paletas"][str(ip)]
            for linha in tiles_px[ch]:
                for c in linha:
                    if c and origem[c] not in usadas:
                        usadas.append(origem[c])
        usadas.sort()
        if len(usadas) > 15:
            raise SystemExit("o tema %s precisaria de %d cores nao-zero na vaga "
                             "%d e so cabem 15: %s"
                             % (chave, len(usadas), F["pal"], usadas))
        paletas[str(F["pal"])] = ([[0, 0, 0]] + usadas
                                  + [[0, 0, 0]] * (15 - len(usadas)))
        indices[chave] = {tuple(c): i + 1 for i, c in enumerate(usadas)}

    # reindexa cada tile para a tabela da vaga do tema dele; a cor 0 fica 0.
    saida_tiles = {}
    for ch, px in sorted(tiles_px.items()):
        chave, ip = tiles_pal[ch]
        origem = abertas[chave]["paletas"][str(ip)]
        saida_tiles[ch] = [[0 if c == 0 else indices[chave][tuple(origem[c])]
                            for c in linha] for linha in px]

    dados = dict(fontes=abertas, paletas=paletas,
                 cores_usadas={k: sum(1 for c in v[1:] if c != [0, 0, 0])
                               for k, v in paletas.items()},
                 tiles=saida_tiles, tiles_paleta={k: list(v) for k, v
                                                  in tiles_pal.items()},
                 chao_da_fonte=chao_fonte, censo_chao=censo_fonte, pecas=pecas)
    with open(KIT_JSON, "w") as f:
        json.dump(dados, f, indent=1)
    print("kit gravado em %s: %d tiles, %d pecas"
          % (os.path.relpath(KIT_JSON, RAIZ), len(saida_tiles), len(pecas)))
    for k, v in sorted(dados["cores_usadas"].items()):
        print("   vaga %s: %d cores nao-zero" % (k, v))
    for k, v in sorted(chao_fonte.items()):
        print("   chao da fonte %s: %d tiles; os 4 padroes de camada de baixo "
              "mais repetidos sao %s"
              % (k, len(v), ", ".join("%s x%d" % ([hex(z) for z in pat], n)
                                      for pat, n in censo_fonte[k][:4])))
    return 0


# --------------------------------------------------------------------- leitura
def kit():
    if not os.path.exists(KIT_JSON):
        raise SystemExit("falta %s; rode --extrai numa maquina com a ROM"
                         % os.path.relpath(KIT_JSON, RAIZ))
    return json.load(open(KIT_JSON))


def _le_png():
    from PIL import Image
    img = Image.open(f"{DESTINO}/tiles.png").convert("P")
    cols = img.size[0] // 8
    px = img.load()
    n = cols * (img.size[1] // 8)
    tiles = []
    for i in range(n):
        x0, y0 = (i % cols) * 8, (i // cols) * 8
        tiles.append([[px[x0 + x, y0 + y] for x in range(8)] for y in range(8)])
    return img, cols, tiles


def _le_pal(vaga):
    linhas = [l.split() for l in
              open(f"{DESTINO}/palettes/%02d.pal" % vaga).read().split("\n")[3:]
              if l.strip()]
    return [[int(z) for z in c] for c in linhas[:16]]


def _grava_pal(vaga, cores):
    with open(f"{DESTINO}/palettes/%02d.pal" % vaga, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n16\n")
        for r, g, b in cores:
            f.write("%d %d %d\n" % (r, g, b))


def _grava_png(img, cols, tiles):
    from PIL import Image
    linhas = (len(tiles) + cols - 1) // cols
    novo = Image.new("P", (cols * 8, linhas * 8), 0)
    novo.putpalette(img.getpalette())
    px = novo.load()
    for i, t in enumerate(tiles):
        x0, y0 = (i % cols) * 8, (i // cols) * 8
        for y in range(8):
            for x in range(8):
                px[x0 + x, y0 + y] = t[y][x]
    novo.save(f"{DESTINO}/tiles.png")


# --------------------------------------------------------- a fusao da vaga 7
def plano_fusao():
    """(precisa, plano) da fusao da vaga 7 DENTRO da vaga 9.

    `plano` traz: `de_para` (indice da vaga 7 -> indice da vaga 9), `pal9` (a
    paleta 9 nova), `copias` (tile local do secundario -> vaga nova) e
    `entradas` (local do metatile, posicao) que passam a apontar para a vaga 9.
    Devolve `precisa=False` quando nenhum metatile pinta com a vaga 7, que e o
    caso depois da primeira aplicacao: e o que torna esta etapa idempotente.
    """
    import render_maps as RM
    os.environ.setdefault("REPO_MAPAS", RAIZ)
    tp = RM.carregar_tileset(PRIMARIO)
    split = len(tp["tiles"])
    meta = open(f"{DESTINO}/metatiles.bin", "rb").read()
    _img, _cols, tiles = _le_png()

    # ONDE A VAGA 7 E USADA, E POR QUEM. Os locais do KIT (de `META_LOCAL_0` para
    # cima) ficam de fora, e e isso que torna esta etapa idempotente: depois da
    # primeira aplicacao a vaga 7 volta a ser usada, mas so pelo proprio kit, e
    # ai nao ha nada para fundir. Sem esse recorte a segunda rodada tentaria
    # fundir a paleta nova do CAMPO dentro da vaga 9 e pararia com "nao cabe".
    usa7, por_tile_pal = [], collections.defaultdict(set)
    for local in range(META_LOCAL_0):
        for pos, v in enumerate(_entradas(meta, local)):
            idx, ip = v & 0x3FF, (v >> 12) & 0xF
            if idx == 0 or ip < 6:
                continue
            por_tile_pal[idx].add(ip)
            if ip == PAL_CAMPO:
                usa7.append((local, pos, idx))
    # o PRIMARIO tambem pode pintar com vaga de secundario; se pintar com a 7 ou
    # usar indice morto da 9, esta fusao esta proibida.
    prim7 = []
    idx9_prim = set()
    for local in range(len(tp["metatiles"]) // 16):
        for v in struct.unpack_from("<8H", tp["metatiles"], local * 16):
            idx, ip = v & 0x3FF, (v >> 12) & 0xF
            if idx == 0:
                continue
            if ip == PAL_CAMPO:
                prim7.append(local)
            if ip == PAL_FUNDE_EM:
                t = (tp["tiles"][idx] if idx < split
                     else (tiles[idx - split] if idx - split < len(tiles) else None))
                if t is not None:
                    idx9_prim |= {c for linha in t for c in linha if c}
    if prim7:
        raise SystemExit("o primario %s pinta com a vaga %d nos metatiles %s: a "
                         "fusao esta proibida" % (PRIMARIO, PAL_CAMPO, prim7[:5]))
    if not usa7:
        return False, None

    p7, p9 = _le_pal(PAL_CAMPO), _le_pal(PAL_FUNDE_EM)
    # indices que os PIXELS realmente usam em cada vaga
    idx7, idx9 = set(), set(idx9_prim)
    for local in range(META_LOCAL_0):
        for v in _entradas(meta, local):
            idx, ip = v & 0x3FF, (v >> 12) & 0xF
            if idx < split or ip not in (PAL_CAMPO, PAL_FUNDE_EM):
                continue
            li = idx - split
            if li >= len(tiles):
                continue
            alvo = idx7 if ip == PAL_CAMPO else idx9
            alvo |= {c for linha in tiles[li] for c in linha if c}

    cor9 = {i: tuple(p9[i]) for i in idx9}
    livres = [i for i in range(1, 16) if i not in idx9]
    de_para, novas = {}, []
    for i in sorted(idx7):
        c = tuple(p7[i])
        achou = [k for k, v in cor9.items() if v == c]
        if achou:
            de_para[i] = achou[0]
        else:
            novas.append((i, c))
    if len(novas) > len(livres):
        raise SystemExit("a vaga %d precisaria de %d indices livres na vaga %d e "
                         "so ha %d: a fusao nao cabe"
                         % (PAL_CAMPO, len(novas), PAL_FUNDE_EM, len(livres)))
    pal9 = [list(c) for c in p9]
    for k, (i, c) in enumerate(novas):
        de_para[i] = livres[k]
        pal9[livres[k]] = list(c)

    # tile usado TAMBEM com outra paleta nao pode ser reindexado no lugar: ele
    # ganha uma copia, e a entrada da vaga 7 passa a apontar para a copia.
    copias, proximo = {}, TILE_FUSAO_0
    for _local, _pos, idx in usa7:
        li = idx - split
        if li < 0:
            raise SystemExit("a vaga %d pinta o tile %d do PRIMARIO: nao da para "
                             "reindexar" % (PAL_CAMPO, idx))
        if len(por_tile_pal[idx]) > 1 and li not in copias:
            copias[li] = proximo
            proximo += 1
    return True, dict(de_para=de_para, pal9=pal9, copias=copias,
                      entradas=[(l, p, i) for l, p, i in usa7], split=split,
                      proximo=proximo)


def aplica_fusao(plano):
    """Escreve a fusao: paleta 9 nova, copias de tile e entradas repontadas."""
    img, cols, tiles = _le_png()
    split = plano["split"]
    while len(tiles) < max([TILE_FUSAO_0] + list(plano["copias"].values())) + 1:
        tiles.append([[0] * 8 for _ in range(8)])
    for li, vaga in sorted(plano["copias"].items()):
        tiles[vaga] = [[plano["de_para"].get(c, 0) if c else 0 for c in linha]
                       for linha in tiles[li]]
    meta = bytearray(open(f"{DESTINO}/metatiles.bin", "rb").read())
    for local, pos, idx in plano["entradas"]:
        li = idx - split
        novo_idx = split + plano["copias"][li] if li in plano["copias"] else idx
        v = struct.unpack_from("<H", meta, local * 16 + pos * 2)[0]
        v = (v & 0x0FFF & ~0x3FF) | (novo_idx & 0x3FF) | (PAL_FUNDE_EM << 12)
        struct.pack_into("<H", meta, local * 16 + pos * 2, v)
        if li not in plano["copias"]:
            tiles[li] = [[plano["de_para"].get(c, 0) if c else 0 for c in linha]
                         for linha in tiles[li]]
    open(f"{DESTINO}/metatiles.bin", "wb").write(bytes(meta))
    _grava_pal(PAL_FUNDE_EM, plano["pal9"])
    _grava_png(img, cols, tiles)


# ------------------------------------------------------------------ o desenho
def desenha_kit():
    """(tiles_novos, metas, attrs, carimbos) sem escrever nada em lugar nenhum.

    `carimbos` sai com `manchas` (id por nome) e `moveis` (a grade de ids).
    """
    dados = kit()
    import render_maps as RM
    os.environ.setdefault("REPO_MAPAS", RAIZ)
    tp = RM.carregar_tileset(PRIMARIO)
    meta_sec = open(f"{DESTINO}/metatiles.bin", "rb").read()

    chao_ents = list(struct.unpack_from("<8H", tp["metatiles"], CHAO * 16))
    attr_chao = G._attrs(PRIMARIO)[CHAO]
    if chao_ents[4:] != [0, 0, 0, 0]:
        raise SystemExit("o metatile %d do primario ja usa a camada de cima"
                         % CHAO)
    if attr_chao & 0xFF:
        raise SystemExit("o metatile %d do primario tem comportamento 0x%02X e "
                         "esta rodada supoe chao normal" % (CHAO, attr_chao & 0xFF))
    px_chao = {}
    for q, v in enumerate(chao_ents[:4]):
        idx = v & 0x3FF
        px_chao[q] = tp["tiles"][idx] if idx < len(tp["tiles"]) else None

    por_peca = {}
    for p in dados["pecas"]:
        por_peca[(p["fonte"], p["lp"], p["papel"])] = p
        por_peca.setdefault((p["fonte"], p["lp"]), p)

    tiles_novos, mapa_tile = {}, {}
    proximo = [TILE_LOCAL_0]

    def vaga(chave):
        if chave not in mapa_tile:
            if chave not in dados["tiles"]:
                raise SystemExit("o kit em disco nao tem o tile %s" % chave)
            mapa_tile[chave] = proximo[0]
            tiles_novos[proximo[0]] = dados["tiles"][chave]
            proximo[0] += 1
        return mapa_tile[chave]

    def traduz(fonte, v, quadrante=None):
        """Entrada da fonte -> entrada nossa: mesmo tile, vaga nova, paleta nova.

        `quadrante` so vem preenchido nas quatro entradas da camada de BAIXO, e
        ali valem duas trocas, as duas pela mesma razao: o chao do fundo tem que
        ser o NOSSO. Tile 0 e transparente e no fundo mostra o BACKDROP do BG,
        que aqui e azul; e o chao DA FONTE e um verde amarelado que nao e o
        nosso verde azulado.
        """
        npri = dados["fontes"][fonte]["n_tiles_pri"]
        chao = set(dados["chao_da_fonte"].get(fonte) or [])
        idx, ip = v & 0x3FF, (v >> 12) & 0xF
        if quadrante is not None and (idx == 0 or idx in chao):
            return chao_ents[quadrante]
        if idx == 0:
            return 0
        lado, li = ("p", idx) if idx < npri else ("s", idx - npri)
        ch = "%s:%s:%d:%d" % (fonte, lado, li, ip)
        return ((v & 0x0C00) | (512 + vaga(ch))
                | (FONTES[fonte]["pal"] << 12))

    metas, attrs = {}, {}
    proximo_meta = [META_LOCAL_0]

    def poe(ents, attr):
        local = proximo_meta[0]
        metas[local] = list(ents)
        attrs[local] = attr
        proximo_meta[0] += 1
        return 512 + local

    def opacidade(v):
        """Pixels opacos do tile de uma entrada JA TRADUZIDA (0 a 64)."""
        idx = v & 0x3FF
        if idx == 0:
            return 0
        if idx < 512:
            t = tp["tiles"][idx] if idx < len(tp["tiles"]) else None
        else:
            t = tiles_novos.get(idx - 512)
        return _opacos(t) if t else 64

    def monta(fonte, lp, papel, esp=""):
        """As oito entradas do metatile `lp` da fonte, ja traduzidas.

        O espelho e aplicado ANTES da traducao, nas entradas CRUAS: se fosse
        depois ele viraria tambem a NOSSA grama que entra no lugar do chao da
        fonte, e a nossa grama e um desenho de 2x2 tiles em que cada quadrante
        tem o seu.
        """
        p = por_peca.get((fonte, lp, papel)) or por_peca[(fonte, lp)]
        ents = p["ents"]
        if esp:
            ents = _espelha4(ents[:4], esp) + _espelha4(ents[4:], esp)
        andavel = papel in ("mancha", "topo")
        if papel in ("mancha", "topo", "movel"):
            baixo = list(chao_ents[:4])
        else:
            baixo = [traduz(fonte, v, q) for q, v in enumerate(ents[:4])]
        cima = [traduz(fonte, v) for v in ents[4:]]
        if andavel:
            # QUADRANTE 100% OPACO DA CAMADA DE CIMA DESCE. Ver o cabecalho: e o
            # que faz a laje ler como chao e o que impede o E3 por construcao.
            for q in range(4):
                if cima[q] and opacidade(cima[q]) == 64:
                    baixo[q] = cima[q]
                    cima[q] = 0
        return baixo + cima

    carimbos = {"manchas": {}, "moveis": []}

    # 1. MANCHA: uma celula, ANDAVEL, atributo do nosso metatile 1.
    for m in MANCHAS:
        gid = poe(monta(m["fonte"], m["lp"], "mancha", m["esp"]), attr_chao)
        carimbos["manchas"][m["nome"]] = dict(mt=gid, fonte=m["fonte"],
                                              lp=m["lp"], esp=m["esp"])

    # 2. MOVEL: retangulo. Linha de baixo SOLIDA e COVERED, as de cima andaveis
    #    com o atributo do chao.
    feito = {}
    for mv in MOVEIS:
        grade = []
        for li, linha in enumerate(mv["grade"]):
            saida = []
            for ci, lp in enumerate(linha):
                solida = bool(mv["solidas"][li][ci])
                papel = papel_de(mv, li, ci)
                ch = (mv["fonte"], lp, papel)
                if ch not in feito:
                    feito[ch] = poe(monta(mv["fonte"], lp, papel),
                                    0x1000 if solida else attr_chao)
                saida.append(feito[ch])
            grade.append(saida)
        carimbos["moveis"].append(dict(nome=mv["nome"], tema=mv["tema"],
                                       grade=grade, solidas=mv["solidas"],
                                       onde=mv["onde"], quantos=mv["quantos"],
                                       espaco=mv["espaco"]))

    if proximo[0] > TETO_TILES:
        raise SystemExit("o kit estoura o teto de %d tiles (%d)"
                         % (TETO_TILES, proximo[0]))
    if proximo_meta[0] > TETO_META:
        raise SystemExit("o kit estoura o teto de %d metatiles" % TETO_META)

    # A vaga de metatile so serve se for ENCHIMENTO do dumper (as oito entradas
    # iguais e baixas) ou se ja tiver o que este kit escreve (rodar duas vezes),
    # e NENHUM dos sete mapas do tileset pode usar o id.
    def enchimento(ent):
        return len(set(ent)) == 1 and ent[0] <= 2

    usados = set()
    for nome in IRMAOS:
        usados |= {c & 0x3FF for c in G.grade(nome)[4]}
    for local, ents in metas.items():
        gid = 512 + local
        antigo = _entradas(meta_sec, local)
        if not enchimento(antigo) and antigo != ents:
            raise SystemExit("vaga de metatile %d ja esta ocupada por outra coisa"
                             % gid)
        if gid in usados and enchimento(antigo):
            raise SystemExit("algum dos sete mapas usa o metatile %d e a vaga "
                             "esta vazia" % gid)

    # As duas vagas de paleta tem que estar livres em TODO metatile que nao seja
    # do kit. A vaga 7 so fica livre DEPOIS da fusao, entao aqui ela ainda pode
    # aparecer: quem confere isso e `plano_fusao`.
    for local in range(len(meta_sec) // 16):
        if local in metas:
            continue
        for v in _entradas(meta_sec, local):
            if (v & 0x3FF) and ((v >> 12) & 0xF) == PAL_RUINA:
                raise SystemExit("a paleta %d ja e usada pelo metatile %d"
                                 % (PAL_RUINA, 512 + local))
    return tiles_novos, metas, attrs, carimbos


def grava_tileset(tiles_novos, metas, attrs):
    dados = kit()
    img, cols, tiles = _le_png()
    alvo = max(tiles_novos) + 1 if tiles_novos else len(tiles)
    while len(tiles) < alvo:
        tiles.append([[0] * 8 for _ in range(8)])
    for v, t in tiles_novos.items():
        tiles[v] = t
    _grava_png(img, cols, tiles)
    for vaga, cores in dados["paletas"].items():
        _grava_pal(int(vaga), cores)
    meta = bytearray(open(f"{DESTINO}/metatiles.bin", "rb").read())
    attr = bytearray(open(f"{DESTINO}/metatile_attributes.bin", "rb").read())
    for local, ents in metas.items():
        for i, v in enumerate(ents):
            struct.pack_into("<H", meta, local * 16 + i * 2, v)
        struct.pack_into("<H", attr, local * 2, attrs[local])
    open(f"{DESTINO}/metatiles.bin", "wb").write(bytes(meta))
    open(f"{DESTINO}/metatile_attributes.bin", "wb").write(bytes(attr))


# ------------------------------------------------------------------- a trilha
def esqueleto(v, W, H, d, elegivel):
    """Caminho de custo minimo ligando as portas do mapa.

    O custo nao e so distancia: andar colado num solido custa mais, para a
    trilha sair pelo MEIO do corredor e nao raspando a parede; virar custa mais,
    para ela sair reta como caminho batido de verdade; e celula que nao pode
    receber mancha custa muito mais, mas nao e proibida, senao o caminho nao
    atravessa a soleira das portas nem os pedacos de chao que nao sao a nossa
    grama.
    """
    def andavel(i):
        return not ((v[i] >> 10) & 3)

    def perto_de_solido(x, y):
        return sum(1 for dx, dy in N4
                   if not (0 <= x + dx < W and 0 <= y + dy < H)
                   or ((v[(y + dy) * W + x + dx] >> 10) & 3))

    def custo(x, y):
        c = 1.0 + 2.0 * perto_de_solido(x, y)
        if (x, y) not in elegivel:
            c += 12.0
        return c

    def caminho(ini, fim):
        """Dijkstra com estado (celula, direcao), para poder cobrar a curva."""
        alvo = set(fim)
        dist, pai = {}, {}
        fila = [(0.0, ini[0], ini[1], 0, 0)]
        while fila:
            g, x, y, dx0, dy0 = heapq.heappop(fila)
            if (x, y, dx0, dy0) in dist:
                continue
            dist[(x, y, dx0, dy0)] = g
            if (x, y) in alvo and (dx0, dy0) != (0, 0):
                saida, no = [], (x, y, dx0, dy0)
                while no in pai:
                    saida.append((no[0], no[1]))
                    no = pai[no]
                saida.append((no[0], no[1]))
                return saida
            for dx, dy in N4:
                nx, ny = x + dx, y + dy
                if not (0 <= nx < W and 0 <= ny < H):
                    continue
                if not andavel(ny * W + nx):
                    continue
                # A CURVA E CARA de proposito: com pouca multa o caminho desce em
                # escada e a trilha dilatada sai com dente de serra.
                curva = 9.0 if (dx0, dy0) != (0, 0) and (dx, dy) != (dx0, dy0) else 0.0
                no = (nx, ny, dx, dy)
                if no in dist:
                    continue
                pai[no] = (x, y, dx0, dy0)
                heapq.heappush(fila, (g + custo(nx, ny) + curva, nx, ny, dx, dy))
        return []

    portas = []
    for w in (d.get("warp_events") or []):
        x, y = w["x"], w["y"]
        for dx, dy in ((0, 1), (0, 0), (0, -1), (1, 0), (-1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and andavel(ny * W + nx):
                portas.append((nx, ny))
                break
    chao = sorted(elegivel)
    if chao:
        ymin, ymax = min(y for _, y in chao), max(y for _, y in chao)
        xmin, xmax = min(x for x, _ in chao), max(x for x, _ in chao)
        for alvo_y in (ymin, ymax):
            faixa = [p for p in chao if abs(p[1] - alvo_y) <= 1]
            if faixa:
                portas.append(min(faixa, key=lambda p: abs(p[0] - W // 2)))
        for alvo_x in (xmin, xmax):
            faixa = [p for p in chao if abs(p[0] - alvo_x) <= 1]
            if faixa:
                portas.append(min(faixa, key=lambda p: abs(p[1] - H // 2)))
    if not portas:
        return set(), []
    # LIGACAO EM ARVORE, nao em fila: ligar porta 0 a 1, 1 a 2 e assim por diante
    # daria um zigue-zague que atravessa a cidade toda vez. Aqui cada porta nova
    # se liga a QUALQUER ponto ja ligado, e o resultado e uma rede com cruzamento.
    ossos = {portas[0]}
    for p in portas[1:]:
        trecho = caminho(p, ossos)
        if trecho:
            ossos |= set(trecho)
    return ossos, portas


def area_trilha(v, W, H, d, elegivel):
    """As celulas de TRILHA: o esqueleto engordado para tres de largura.

    A limpeza de faixa de uma celula existe por leitura de arte: risco de uma
    celula de largura no meio do gramado nao le como caminho, le como sujeira.
    """
    ossos, portas = esqueleto(v, W, H, d, elegivel)
    pav = set()
    for x, y in ossos:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                p = (x + dx, y + dy)
                if p in elegivel:
                    pav.add(p)
    while True:
        entra = {p for p in elegivel if p not in pav
                 and sum(1 for dx, dy in N4 if (p[0] + dx, p[1] + dy) in pav) >= 3}
        if not entra:
            break
        pav |= entra
    while True:
        fora = {(x, y) for x, y in pav
                if not ((x, y - 1) in pav or (x, y + 1) in pav)
                or not ((x - 1, y) in pav or (x + 1, y) in pav)}
        if not fora:
            break
        pav -= fora
    return pav, portas


def desgasta_trilha(trilha, corte):
    """A trilha que vai receber tinta: miolo inteiro e parte da borda.

    Miolo e a celula com as quatro vizinhas de N4 tambem na trilha. A borda
    passa por um hash da posicao e o corte e `corte` por cento. Nao ha estado nem
    ordem aqui: a mesma celula da a mesma resposta em qualquer maquina.
    """
    return {p for p in trilha
            if all((p[0] + dx, p[1] + dy) in trilha for dx, dy in N4)
            or _mistura(p[0], p[1], 0x7A17) % 100 < corte}


def bolhas(livres, spec_lista, folga=4):
    """[(indice_do_grupo, {celulas})], bolhas organicas crescidas por frente de onda.

    A SEMENTE nao e sorteio solto: as celulas livres sao ordenadas por um hash da
    posicao e a semente so e aceita se estiver a pelo menos 4 (Chebyshev) de toda
    semente ja aceita, o que espalha as bolhas em vez de deixa-las grudadas. O
    CRESCIMENTO e guloso com ruido: a cada passo entra a celula da frente de onda
    com o menor hash. Circulo daria bolha redonda e xadrez daria sal e pimenta;
    frente de onda com ruido da contorno irregular, que e o que mato de verdade
    faz.
    """
    ordem = sorted(livres, key=lambda p: _mistura(p[0], p[1], 0x5EED))
    tomadas, saida, sementes = set(), [], []
    for gi, spec in enumerate(spec_lista):
        feitas = 0
        for p in ordem:
            if feitas >= spec["quantas"]:
                break
            if p in tomadas:
                continue
            if any(max(abs(p[0] - q[0]), abs(p[1] - q[1])) < folga for q in sementes):
                continue
            lo, hi = spec["tam"]
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
                    r = (q[0] + dx, q[1] + dy)
                    if r in livres and r not in tomadas and r not in corpo:
                        frente.add(r)
            if len(corpo) < lo:
                continue
            tomadas |= corpo
            sementes.append(p)
            saida.append((gi, corpo))
            feitas += 1
    return saida


def peca_da_lista(lista, x, y):
    """Qual peca da lista cai nesta celula.

    Hash da posicao, nao paridade: paridade vira xadrez e o auto-teste reprova.
    O hash tambem nao tem periodo, porque nao e funcao de x nem de y sozinhos.
    """
    return lista[_mistura(x, y, 0xA5A5 + len(lista)) % len(lista)]


# ----------------------------------------------------------- ligacao a pe
def componentes(v, W, H):
    """{celula: rotulo} dos pedacos de chao andavel ligados a pe.

    POR QUE NAO BASTA O `enfeita_cidades.alcance`. Aquele mede "quem ainda e
    alcancavel a partir de algum ponto de partida", e ponto de partida ali e
    warp OU objeto. Num mapa com warp dos DOIS lados de um corredor, fechar o
    corredor nao tira NENHUMA celula do alcance, porque cada metade continua
    alcancavel a partir do proprio warp, e mesmo assim o jogador que entra de um
    lado nao chega mais no outro. Medido em `SnowpointCity` em 07/09/2026, com
    uma sabotagem que o portao antigo deixou passar VERDE.
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
    for p, r in antes.items():
        if p not in solidificadas:
            por_rotulo[r].add(p)
    for r, cels in por_rotulo.items():
        vistos = {depois.get(p) for p in cels}
        if len(vistos) > 1:
            mau.append("o pedaco %d de chao se partiu em %d" % (r, len(vistos)))
    juntou = collections.defaultdict(set)
    for p, r in depois.items():
        if p in antes:
            juntou[r].add(antes[p])
    for r, origens in juntou.items():
        if len(origens) > 1:
            mau.append("dois pedacos de chao que eram separados se juntaram")
    return mau


# ---------------------------------------------------------------- plano do mapa
def plano_mapa(alvo, carimbos, base=None):
    """(L, W, H, v, escritas, contas) de uma cidade."""
    CFG = CIDADES[alvo]
    d, L, W, H, v0 = G.grade(alvo)
    v = list(base) if base is not None else list(v0)
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()

    def andavel(i):
        return not ((v[i] >> 10) & 3)

    # ELEGIVEL: so a NOSSA grama lisa, andavel, e que nao seja agua. Elevacao NAO
    # entra no filtro (em `CelesticTown` a mesma grama aparece em duas
    # elevacoes), e nao precisa: a elevacao de cada celula e preservada bit a
    # bit na escrita.
    elegivel = {(i % W, i // W) for i in range(W * H)
                if andavel(i) and (v[i] & 0x3FF) == CHAO
                and beh(v[i] & 0x3FF) not in AG}

    escritas = {}
    trilha, portas = area_trilha(v, W, H, d, elegivel)

    # ------------------------------------------------------------- 1. os movei
    ev, gelo = E.congelado(d)
    gelo |= E.corredores_de_teste(alvo, v, W, H, d)
    # o que o `enfeita_cidades.py` ja desenhou nesta cidade fica de fora, mas SO
    # a celula: movel encostado em enfeite e cidade cheia, nao cidade errada.
    for idx, _a, _n in E.carrega_plano().get(alvo, {}).get("celulas", []):
        gelo.add((idx % W, idx // W))

    aplicado = list(v)
    ini = E.partidas(d, W, H, v)
    antes = E.alcance(v, W, H, ini)
    novos_solidos, postos = [], []
    conta_mov = collections.Counter()
    por_movel = collections.defaultdict(list)

    def livre(x, y):
        i = y * W + x
        if x < MARGEM or y < MARGEM or x >= W - MARGEM or y >= H - MARGEM:
            return False
        if (x, y) in gelo or i in escritas or (x, y) not in elegivel:
            return False
        if (x, y) in trilha:
            return False
        return (aplicado[i] & 0x3FF) == CHAO

    def solido(x, y):
        return 0 <= x < W and 0 <= y < H and ((aplicado[y * W + x] >> 10) & 3)

    def encosto_ok(onde, cels):
        if onde == "qualquer":
            return True
        if onde == "beira":
            return any(solido(x + dx, y + dy)
                       for x, y in cels for dx, dy in N4)
        return any((x + dx, y + dy) in trilha for x, y in cels for dx, dy in N4)

    def espacado(m, cels):
        for x, y in cels:
            if any(max(abs(x - px), abs(y - py)) < ESPACO_ENTRE_MOVEIS
                   for px, py in postos):
                return False
            if any(max(abs(x - px), abs(y - py)) < m["espaco"]
                   for px, py in por_movel[m["nome"]]):
                return False
        return True

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

    def tenta_peca(mv, x0, y0):
        """Escreve a peca inteira e devolve True se os dois portoes deixarem.

        O portao roda NA HORA e nao so no fim: se solidificar as celulas desta
        peca tirar do alcance a pe qualquer OUTRA celula, ou partir um pedaco de
        chao em dois, a escrita e desfeita e o gerador segue.
        """
        cels, novas = [], []
        for li, linha in enumerate(mv["grade"]):
            for ci, gid in enumerate(linha):
                x, y = x0 + ci, y0 + li
                if not livre(x, y):
                    return False
                cels.append((x, y, gid, bool(mv["solidas"][li][ci])))
        if not encosto_ok(mv["onde"], [(c[0], c[1]) for c in cels]):
            return False
        if not espacado(mv, [(c[0], c[1]) for c in cels]):
            return False
        guarda = {}
        for x, y, gid, sol in cels:
            i = y * W + x
            guarda[i] = aplicado[i]
            # ELEVACAO PRESERVADA (bits 12 a 15); a colisao so LIGA, nunca desliga
            aplicado[i] = ((aplicado[i] & 0xF000)
                           | ((1 << 10) if sol else (aplicado[i] & 0x0C00))
                           | gid)
            if sol:
                novas.append((x, y))
        perdidas = (antes - E.alcance(aplicado, W, H, ini)) \
            - set(novos_solidos) - set(novas)
        partiu = any(nao_liga(aplicado, x, y) for x, y in novas)
        if perdidas or partiu:
            for i, val in guarda.items():
                aplicado[i] = val
            return False
        for i in guarda:
            escritas[i] = aplicado[i]
        novos_solidos.extend(novas)
        postos.extend((c[0], c[1]) for c in cels)
        return True

    ordem_cel = sorted(((x, y) for y in range(H) for x in range(W)),
                       key=lambda p: ((p[0] * 2654435761 + p[1] * 40503) & 0xFFFF, p))
    meus = [m for m in carimbos["moveis"] if m["tema"] in CFG["temas"]]
    postas = []
    for x, y in ordem_cel:
        if sum(conta_mov.values()) >= TETO_MOVEIS:
            break
        giro = ((x * 73856093) ^ (y * 19349663)) % max(1, len(meus))
        for k in range(len(meus)):
            mv = meus[(giro + k) % len(meus)]
            if conta_mov[mv["nome"]] >= mv["quantos"]:
                continue
            if tenta_peca(mv, x, y):
                por_movel[mv["nome"]].append((x, y))
                conta_mov[mv["nome"]] += 1
                postas.append([mv["nome"], x, y])
                break

    # -------------------------------------------------------- 2. os canteiros
    # Bloco de plantacao de 2 de largura, ANDAVEL do comeco ao fim. Ele vem antes
    # da mancha solta para poder pegar um retangulo inteiro de grama limpa.
    conta_mancha = collections.Counter()
    ids = carimbos["manchas"]

    def pintavel(p):
        """A celula pode receber MANCHA?

        Repare que `gelo` (evento mais a orla de uma celula em volta, corredor de
        teste da suite, enfeite que o `enfeita_cidades.py` ja desenhou) NAO entra
        aqui, e nao entra de proposito: mancha nao mexe em colisao, nao mexe em
        elevacao e nao mexe em (comportamento, layerType), entao pintar a celula
        onde mora uma placa ou por onde a suite anda nao muda nada para o jogo,
        so troca o desenho do chao. Quem tem que respeitar `gelo` e o MOVEL, que
        solidifica, e ele respeita em `livre`. Com `gelo` valendo tambem para a
        mancha, a orla dos 21 eventos de `CelesticTown` comia o gramado inteiro e
        as bolhas nao tinham onde nascer: medido nesta frente, a regua parava em
        34,1%. O que continua fora e o que a passada anterior JA desenhou, que
        entra por `escritas` e pelo filtro de metatile.
        """
        i = p[1] * W + p[0]
        return (p in elegivel and i not in escritas
                and (aplicado[i] & 0x3FF) == CHAO)

    def pinta(p, nome):
        i = p[1] * W + p[0]
        escritas[i] = (aplicado[i] & 0xFC00) | ids[nome]["mt"]
        aplicado[i] = escritas[i]
        conta_mancha[nome] += 1

    n_cant = 0
    if CFG["canteiros"]:
        lo, hi = CANTEIRO["alturas"]
        for x, y in ordem_cel:
            if n_cant >= CFG["canteiros"]:
                break
            alt = lo + _mistura(x, y, 0xCA17) % (hi - lo + 1)
            cels = [(x + cx, y + cy) for cy in range(alt) for cx in range(2)]
            if any(not pintavel(p) or p in trilha
                   or p[0] < MARGEM or p[1] < MARGEM
                   or p[0] >= W - MARGEM or p[1] >= H - MARGEM for p in cels):
                continue
            # nao encosta em outro canteiro nem em movel
            if any(max(abs(p[0] - q[0]), abs(p[1] - q[1])) < 2
                   for p in cels for q in postos):
                continue
            for cy in range(alt):
                fila = (CANTEIRO["topo"] if cy == 0 else
                        CANTEIRO["base"] if cy == alt - 1 else CANTEIRO["meio"])
                for cx in range(2):
                    pinta((x + cx, y + cy), fila[cx])
            postos.extend(cels)
            n_cant += 1

    # ------------------------------------------------------------ 3. a mancha
    for p in sorted(x for x in desgasta_trilha(trilha, CFG["borda_trilha"])
                    if pintavel(x)):
        pinta(p, peca_da_lista(CFG["trilha"], p[0], p[1]))

    livres = {p for p in elegivel if pintavel(p)}
    for gi, corpo in bolhas(livres, CFG["bolhas"], CFG["folga_semente"]):
        lista = CFG["bolhas"][gi]["pecas"]
        for p in sorted(corpo):
            if pintavel(p):
                pinta(p, peca_da_lista(lista, p[0], p[1]))

    # ------------------------------------------------------------- os portoes
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val
    depois = E.alcance(saida, W, H, ini)
    perdidas = antes - depois - set(novos_solidos)
    if perdidas:
        raise SystemExit("%s: %d celulas ficariam inalcancaveis, ex.: %s"
                         % (alvo, len(perdidas), sorted(perdidas)[:6]))
    if depois - antes:
        raise SystemExit("%s: o alcance a pe GANHOU celula" % alvo)
    for x, y in E.eventos(d):
        if (x, y) in antes and (x, y) not in depois:
            raise SystemExit("%s: evento em (%d,%d) ficaria inalcancavel"
                             % (alvo, x, y))
    queixas = ligacao_intacta(componentes(v, W, H), componentes(saida, W, H),
                              set(novos_solidos))
    if queixas:
        raise SystemExit("%s: %s" % (alvo, "; ".join(queixas)))

    contas = dict(trilha=len(trilha), moveis=dict(conta_mov),
                  manchas=dict(conta_mancha), canteiros=n_cant,
                  solidos=len(novos_solidos), portas=len(portas),
                  postas=postas)
    return L, W, H, v, escritas, contas


# ------------------------------------------------------------------ regua
def regua(v, W, H, L, escritas=None):
    """(carimbo dominante, celulas andaveis a pe, id do carimbo) como a regua."""
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()
    cel = list(v)
    for i, val in (escritas or {}).items():
        cel[i] = val
    and_ = [c & 0x3FF for c in cel
            if not ((c >> 10) & 3) and beh(c & 0x3FF) not in AG]
    top = collections.Counter(and_).most_common(1)[0]
    return 100.0 * top[1] / len(and_), len(and_), top[0]


# ---------------------------------------------------------------------- rodagem
def carrega_plano():
    return json.load(open(PLANO)) if os.path.exists(PLANO) else {}


def base_de(alvo, guardado):
    """A grade como esta no disco, so tirando o que ESTA passada escreveu."""
    v = list(G.grade(alvo)[4])
    for idx, antigo, novo in guardado.get(alvo, {}).get("celulas", []):
        if v[idx] == novo:
            v[idx] = antigo
    return v


def roda(aplicar):
    precisa, pl = plano_fusao()
    if precisa:
        print("fusao da vaga %d dentro da %d: %d entradas, %d copias de tile "
              "(vagas %s), %d cores novas nos indices ociosos"
              % (PAL_CAMPO, PAL_FUNDE_EM, len(pl["entradas"]), len(pl["copias"]),
                 sorted(pl["copias"].values()),
                 sum(1 for i, j in pl["de_para"].items()
                     if _le_pal(PAL_FUNDE_EM)[j] != _le_pal(PAL_CAMPO)[i])))
        if aplicar:
            aplica_fusao(pl)
    else:
        print("fusao da vaga %d: nada a fazer, ninguem pinta com ela"
              % PAL_CAMPO)

    tiles_novos, metas, attrs, carimbos = desenha_kit()
    d = kit()
    print("kit: %d tiles novos (vagas %d a %d de %d, sobram %d), %d metatiles "
          "novos (locais %d a %d, ids %d a %d); vaga %d com %d cores, vaga %d "
          "com %d cores"
          % (len(tiles_novos), min(tiles_novos), max(tiles_novos), TETO_TILES,
             TETO_TILES - max(tiles_novos) - 1, len(metas), min(metas),
             max(metas), 512 + min(metas), 512 + max(metas),
             PAL_RUINA, d["cores_usadas"][str(PAL_RUINA)],
             PAL_CAMPO, d["cores_usadas"][str(PAL_CAMPO)]))
    if aplicar:
        grava_tileset(tiles_novos, metas, attrs)

    guardado = carrega_plano()
    for alvo in ALVOS:
        base = base_de(alvo, guardado)
        L, W, H, v, escritas, contas = plano_mapa(alvo, carimbos, base)
        a, na, ida = regua(v, W, H, L)
        b, nb, idb = regua(v, W, H, L, escritas)
        print("\n%s: trilha %d celulas, %d portas, %d canteiros, %d celulas "
              "solidificadas" % (alvo, contas["trilha"], contas["portas"],
                                 contas["canteiros"], contas["solidos"]))
        print("  manchas: %d em %s" % (sum(contas["manchas"].values()),
                                       ", ".join("%s x%d" % kv for kv
                                                 in sorted(contas["manchas"].items()))))
        print("  moveis: " + (", ".join("%s x%d" % kv for kv
                                        in sorted(contas["moveis"].items()))
                              or "nenhum"))
        print("  regua: carimbo %d com %.1f%% de %d celulas ANTES; carimbo %d "
              "com %.1f%% de %d DEPOIS" % (ida, a, na, idb, b, nb))
        print("  celulas do mapa mudadas: %d" % len(escritas))
        if aplicar:
            saida = list(v)
            for i, val in escritas.items():
                saida[i] = val
            with open(f"{RAIZ}/{L['blockdata_filepath']}", "wb") as f:
                f.write(struct.pack("<%dH" % len(saida), *saida))
            guardado[alvo] = {"celulas": [[i, v[i], escritas[i]]
                                          for i in sorted(escritas)]}
    if aplicar:
        with open(PLANO, "w") as f:
            json.dump(guardado, f, indent=1)
        print("\naplicado")
    return 0


def desfaz():
    guardado = carrega_plano()
    n = 0
    for alvo in list(guardado):
        d, L, W, H, v = G.grade(alvo)
        v = list(v)
        for idx, antigo, novo in guardado[alvo]["celulas"]:
            if v[idx] == novo:
                v[idx] = antigo
                n += 1
        with open(f"{RAIZ}/{L['blockdata_filepath']}", "wb") as f:
            f.write(struct.pack("<%dH" % len(v), *v))
        guardado.pop(alvo)
    with open(PLANO, "w") as f:
        json.dump(guardado, f, indent=1)
    print("desfeitas %d celulas" % n)
    return 0


# ------------------------------------------------------------------ auto-teste
def demo():
    from PIL import Image
    import render_maps as RM
    os.environ.setdefault("REPO_MAPAS", RAIZ)
    mau = []
    dados = kit()
    tiles_novos, metas, attrs, carimbos = desenha_kit()
    tp = RM.carregar_tileset(PRIMARIO)
    chao_ents = list(struct.unpack_from("<8H", tp["metatiles"], CHAO * 16))
    attr_chao = G._attrs(PRIMARIO)[CHAO]
    meta_sec = open(f"{DESTINO}/metatiles.bin", "rb").read()
    attr_sec = open(f"{DESTINO}/metatile_attributes.bin", "rb").read()

    ids_mancha = {c["mt"] for c in carimbos["manchas"].values()}
    ids_andavel, ids_solido = set(ids_mancha), set()
    for mv in carimbos["moveis"]:
        for li, linha in enumerate(mv["grade"]):
            for ci, gid in enumerate(linha):
                (ids_solido if mv["solidas"][li][ci] else ids_andavel).add(gid)

    # ---------------------------------------------------- 1. orcamento
    if TILE_LOCAL_0 + len(tiles_novos) > TETO_TILES:
        mau.append("estoura o teto de tiles")
    if max(metas) >= TETO_META:
        mau.append("estoura o teto de metatiles")
    for vaga in (PAL_CAMPO, PAL_RUINA):
        if not 6 <= vaga <= 12:
            mau.append("paleta %d nao e vaga de secundario" % vaga)
        cores = dados["paletas"][str(vaga)]
        nz = [c for c in cores[1:] if c != [0, 0, 0]]
        if len(nz) > 15:
            mau.append("a vaga %d tem %d cores nao-zero" % (vaga, len(nz)))
        if len({tuple(c) for c in nz}) != len(nz):
            mau.append("a vaga %d gasta duas vagas com a MESMA cor" % vaga)

    # ---------------------------------------------------- 2. a fusao da vaga 7
    # O teste e por CONSTRUCAO e nao por nome: nenhuma cor viva da vaga 9 pode
    # ter mudado de indice, e as cores que entraram tem que ser exatamente as da
    # vaga 7 que ainda nao existiam la.
    precisa, pl = plano_fusao()
    if precisa:
        p9_disco = _le_pal(PAL_FUNDE_EM)
        p7_disco = _le_pal(PAL_CAMPO)
        vivos = {j for j in pl["de_para"].values()}
        for i, j in sorted(pl["de_para"].items()):
            if p7_disco[i] != pl["pal9"][j]:
                mau.append("a fusao levaria a cor %s do indice %d da vaga %d "
                           "para o indice %d da vaga %d, que tem %s"
                           % (p7_disco[i], i, PAL_CAMPO, j, PAL_FUNDE_EM,
                              pl["pal9"][j]))
        # nenhum indice VIVO da vaga 9 pode mudar de cor
        for j in range(16):
            if pl["pal9"][j] != p9_disco[j] and j not in vivos:
                mau.append("a fusao mexeu no indice %d da vaga %d sem precisar"
                           % (j, PAL_FUNDE_EM))
    else:
        if any(((v >> 12) & 0xF) == PAL_CAMPO and (v & 0x3FF)
               for local in range(len(meta_sec) // 16)
               for v in _entradas(meta_sec, local)
               if local not in metas):
            mau.append("a vaga %d ainda e usada por metatile que nao e do kit"
                       % PAL_CAMPO)

    # ------------------------------- 3. a grama do fundo e a NOSSA em toda peca
    for gid in ids_mancha:
        ent = metas[gid - 512]
        for q in range(4):
            if ent[q] != chao_ents[q] and ent[q] != ent[4 + q]:
                # so vale se for quadrante que DESCEU da camada de cima
                if ent[4 + q] != 0:
                    mau.append("a mancha %d nao tem a nossa grama no quadrante "
                               "%d" % (gid, q))
    # ----------------------------- 4. comportamento importado: NENHUM
    for gid in ids_andavel | ids_solido:
        a = attrs[gid - 512]
        if a & 0xFF and a != attr_chao:
            mau.append("o metatile %d importou comportamento 0x%02X da fonte"
                       % (gid, a & 0xFF))
    # ----------------------------- 5. celula ANDAVEL herda o atributo do chao
    for gid in ids_andavel:
        if attrs[gid - 512] != attr_chao:
            mau.append("o metatile andavel %d tem atributo 0x%04X, e o do chao e "
                       "0x%04X" % (gid, attrs[gid - 512], attr_chao))
    # ----------------------------- 6. celula SOLIDA em COVERED
    for gid in ids_solido:
        if (attrs[gid - 512] >> 12) & 0xF != 1:
            mau.append("o metatile solido %d nao esta em COVERED" % gid)

    # ----------------------------- 7. E3: camada de cima nunca 100% opaca em
    #     metatile ANDAVEL. A conta e nos PIXELS, depois da descida, e nao no
    #     desenho de memoria. Sem a descida a laje do altar e o muro caido
    #     entrariam com os quatro quadrantes cheios.
    def opac(v):
        idx = v & 0x3FF
        if idx == 0:
            return 0
        if idx < 512:
            return _opacos(tp["tiles"][idx]) if idx < len(tp["tiles"]) else 64
        return _opacos(tiles_novos[idx - 512]) if (idx - 512) in tiles_novos else 64

    for gid in ids_andavel:
        ent = metas[gid - 512]
        if sum(opac(x) for x in ent[4:]) >= 4 * 64:
            mau.append("o metatile andavel %d tapa o jogador inteiro (E3)" % gid)

    # ----------------------------- 8. paleta: so as duas vagas do kit e as que o
    #     NOSSO metatile 1 ja usava, que entram junto com a grama substituida.
    pals_ok = {PAL_CAMPO, PAL_RUINA} | {(x >> 12) & 0xF for x in chao_ents
                                        if x & 0x3FF}
    for local, ent in metas.items():
        for x in ent:
            if (x & 0x3FF) and ((x >> 12) & 0xF) not in pals_ok:
                mau.append("o metatile %d aponta para a paleta %d, que nao e do "
                           "kit" % (512 + local, (x >> 12) & 0xF))

    # ----------------------------- 9. nenhuma mancha e copia PIXEL A PIXEL de
    #     outra: espelho vale, clone nao (regra 9 da onda).
    def pixels_de(gid):
        saida = []
        for x in metas[gid - 512]:
            idx = x & 0x3FF
            if idx == 0:
                saida.append(None)
                continue
            t = (tp["tiles"][idx] if idx < 512
                 else tiles_novos.get(idx - 512))
            if t is None:
                saida.append(None)
                continue
            hf, vf = x & 0x400, x & 0x800
            linhas = [list(reversed(l)) if hf else list(l) for l in t]
            if vf:
                linhas = list(reversed(linhas))
            saida.append([tuple(l) for l in linhas])
        return tuple(map(lambda z: tuple(z) if z else None, saida))

    vistos_px = {}
    for nome, c in sorted(carimbos["manchas"].items()):
        chave = pixels_de(c["mt"])
        if chave in vistos_px:
            mau.append("a mancha '%s' e copia pixel a pixel de '%s'"
                       % (nome, vistos_px[chave]))
        vistos_px[chave] = nome

    # ---------------------------------------------------- 10. o plano de cada mapa
    guardado = carrega_plano()
    resumo = {}
    for alvo in ALVOS:
        base = base_de(alvo, guardado)
        L, W, H, v, escritas, contas = plano_mapa(alvo, carimbos, base)
        d = json.load(open(f"{RAIZ}/data/maps/{alvo}/map.json"))
        ev = E.eventos(d)
        saida = list(v)
        for i, val in escritas.items():
            saida[i] = val
        resumo[alvo] = (L, W, H, v, escritas, contas, saida)

        for i, val in escritas.items():
            x, y = i % W, i // W
            mt_novo, mt_velho = val & 0x3FF, v[i] & 0x3FF
            col_novo, col_velho = (val >> 10) & 3, (v[i] >> 10) & 3
            if (val >> 12) & 0xF != (v[i] >> 12) & 0xF:
                mau.append("%s: mudou ELEVACAO em (%d,%d)" % (alvo, x, y))
            if col_velho and not col_novo:
                mau.append("%s: colisao 1 -> 0 em (%d,%d), que segue proibida"
                           % (alvo, x, y))
            if mt_velho != CHAO:
                mau.append("%s: peca fora da nossa grama lisa em (%d,%d)"
                           % (alvo, x, y))
            if mt_novo in ids_andavel:
                if col_novo != col_velho:
                    mau.append("%s: peca andavel mudou colisao em (%d,%d)"
                               % (alvo, x, y))
            elif mt_novo in ids_solido:
                if col_velho or not col_novo:
                    mau.append("%s: movel em (%d,%d) nao e solidificacao 0 -> 1"
                               % (alvo, x, y))
                if (x, y) in ev:
                    mau.append("%s: movel em cima do evento (%d,%d)"
                               % (alvo, x, y))
            else:
                mau.append("%s: metatile %d escrito em (%d,%d) nao e do kit"
                           % (alvo, mt_novo, x, y))

        # 10b. (comportamento, layerType) de toda celula ANDAVEL fica igual
        ap = G._attrs(L["primary_tileset"])
        asec = G._attrs(L["secondary_tileset"])

        def atributo(mt_id):
            """Atributo de um metatile, com o kit desta rodada valendo por cima:
            ele pode ainda nao estar no disco na primeira rodada."""
            if mt_id >= 512:
                local = mt_id - 512
                if local in attrs:
                    return attrs[local]
                return asec[local] if local < len(asec) else 0
            return ap[mt_id] if mt_id < len(ap) else 0

        for i in range(W * H):
            if (saida[i] >> 10) & 3:
                continue
            a, b = atributo(v[i] & 0x3FF), atributo(saida[i] & 0x3FF)
            if (a & 0xFF, a & 0xF000) != (b & 0xFF, b & 0xF000):
                mau.append("%s: celula andavel (%d,%d) mudou (comportamento, "
                           "layerType)" % (alvo, i % W, i // W))
                break

        # 10c. os dois portoes de alcance
        ini = E.partidas(d, W, H, v)
        antes, depois = E.alcance(v, W, H, ini), E.alcance(saida, W, H, ini)
        solidificadas = {(i % W, i // W) for i in escritas
                         if not ((v[i] >> 10) & 3) and ((escritas[i] >> 10) & 3)}
        if (antes - depois) - solidificadas:
            mau.append("%s: o alcance a pe perdeu %d celulas alem das "
                       "solidificadas: %s"
                       % (alvo, len((antes - depois) - solidificadas),
                          sorted((antes - depois) - solidificadas)[:6]))
        if depois - antes:
            mau.append("%s: o alcance a pe GANHOU celula" % alvo)
        mau += ["%s: %s" % (alvo, q) for q in
                ligacao_intacta(componentes(v, W, H), componentes(saida, W, H),
                                solidificadas)]

        # 10d. A MANCHA NAO PODE SER ADIVINHAVEL, e o teste tem dois lados.
        #   (a) PADRAO: nenhuma projecao simples da posicao pode ADIVINHAR a
        #       peca. Medir so a PARIDADE nao basta: com seis pecas num grupo, a
        #       paridade de x+y so estreita o palpite de seis para tres e o mapa
        #       fica listrado na diagonal com periodo 6 mesmo assim. A conta e
        #       por EIXO (x, y, x+y, x-y) e por MODULO de 2 a 8: dentro de cada
        #       classe de resto chuta-se a peca mais comum daquela classe, e o
        #       acerto e comparado com o de chutar a peca mais comum do mapa
        #       inteiro. Hash bom nao melhora o palpite; padrao periodico melhora
        #       muito. O corte de 12 pontos e o mesmo do `neve_snowpoint2.py`,
        #       calibrado la com folga de duas vezes para os dois lados.
        #   (b) FORMA: mancha tem que ser BOLHA, nao sal e pimenta, e a conta e o
        #       TAMANHO MEDIO do pedaco conexo, nao "quantas vizinhas cada celula
        #       tem", porque a segunda nao sabe reprovar.
        mancha_em = {(i % W, i // W): (val & 0x3FF) for i, val in escritas.items()
                     if (val & 0x3FF) in ids_mancha}
        if len(mancha_em) < 200:
            mau.append("%s: so %d celulas de mancha" % (alvo, len(mancha_em)))
        if mancha_em:
            tot = len(mancha_em)
            cego = collections.Counter(mancha_em.values()).most_common(1)[0][1] / tot
            for rotulo, eixo in (("x", lambda p: p[0]), ("y", lambda p: p[1]),
                                 ("x+y", lambda p: p[0] + p[1]),
                                 ("x-y", lambda p: p[0] - p[1])):
                for mod in range(2, 9):
                    tabela = collections.defaultdict(collections.Counter)
                    for p, mt_id in mancha_em.items():
                        tabela[eixo(p) % mod][mt_id] += 1
                    ac = sum(c.most_common(1)[0][1] for c in tabela.values()) / tot
                    if ac - cego > 0.12:
                        mau.append("%s: saber %s mod %d adivinha a peca de mancha "
                                   "em %.0f%% das celulas contra %.0f%% do chute "
                                   "cego: virou padrao"
                                   % (alvo, rotulo, mod, 100 * ac, 100 * cego))
            vistos_m, pedacos = set(), 0
            for p in sorted(mancha_em):
                if p in vistos_m:
                    continue
                pedacos += 1
                pilha = [p]
                vistos_m.add(p)
                while pilha:
                    q = pilha.pop()
                    for dx, dy in N4:
                        rr = (q[0] + dx, q[1] + dy)
                        if rr in mancha_em and rr not in vistos_m:
                            vistos_m.add(rr)
                            pilha.append(rr)
            if len(mancha_em) / pedacos < 12.0:
                mau.append("%s: a mancha media tem so %.1f celulas (%d celulas "
                           "em %d pedacos): virou sal e pimenta, nao bolha"
                           % (alvo, len(mancha_em) / pedacos, len(mancha_em),
                              pedacos))

        # 10e. PECA INTEIRA NO MAPA: cada peca anotada no plano tem que estar no
        #      mapa com TODAS as celulas dela, na posicao certa, e nenhuma celula
        #      de peca pode estar no mapa fora de uma peca anotada. A conta NAO
        #      pode ser "quantos topos e quantas bases por metatile", porque
        #      metatile de peca e COMPARTILHADO: a arvore dourada e a arvore
        #      dourada clara usam a MESMA linha de baixo (os metatiles 328 e 329
        #      do 0x286DE4) e a arvore morta alta usa o corpo inteiro da arvore
        #      morta. E este e o caso que pega a sabotagem de tirar o topo: se a
        #      celula de cima sumir do mapa, a peca anotada deixa de bater.
        por_nome = {m["nome"]: m for m in carimbos["moveis"]}
        cobertas = set()
        for nome, x0, y0 in contas["postas"]:
            mv = por_nome[nome]
            for li, linha in enumerate(mv["grade"]):
                for ci, gid in enumerate(linha):
                    x, y = x0 + ci, y0 + li
                    j = y * W + x
                    cobertas.add((x, y))
                    if (saida[j] & 0x3FF) != gid:
                        mau.append("%s: a peca %s em (%d,%d) devia ter o "
                                   "metatile %d em (%d,%d) e tem %d"
                                   % (alvo, nome, x0, y0, gid, x, y,
                                      saida[j] & 0x3FF))
                    if bool(mv["solidas"][li][ci]) != bool((saida[j] >> 10) & 3):
                        mau.append("%s: a celula (%d,%d) da peca %s tem a "
                                   "colisao errada" % (alvo, x, y, nome))
        de_peca = {g for m in carimbos["moveis"] for linha in m["grade"]
                   for g in linha}
        for i, val in escritas.items():
            if (val & 0x3FF) in de_peca and (i % W, i // W) not in cobertas:
                mau.append("%s: a celula (%d,%d) tem metatile de peca (%d) e nao "
                           "pertence a peca nenhuma do plano"
                           % (alvo, i % W, i // W, val & 0x3FF))
                break

        # 10f. a regua tem que fechar
        b, nb, idb = regua(v, W, H, L, escritas)
        if b > 20.0:
            mau.append("%s: a regua ainda marca %.1f%% de carimbo dominante"
                       % (alvo, b))

        # 10g. idempotente
        base2 = list(saida)
        for i in sorted(escritas):
            if base2[i] == escritas[i]:
                base2[i] = v[i]
        if base2 != list(v):
            mau.append("%s: desfazer nao devolve a base" % alvo)
        _, _, _, _, escritas2, _ = plano_mapa(alvo, carimbos, base2)
        if escritas2 != escritas:
            mau.append("%s: segunda passada deu plano diferente" % alvo)

    # ---------------------------------------------------- 11. O QUE ESTA NO DISCO
    # Sem este caso o auto-teste so confere o que ele mesmo acabou de calcular em
    # memoria: sabotar o atributo ou um tile DIRETO NO DISCO deixaria todos os
    # casos anteriores verdes.
    png = Image.open(f"{DESTINO}/tiles.png")
    cols = png.size[0] // 8
    pxd = png.convert("P").load()

    def enchimento(ent):
        return len(set(ent)) == 1 and ent[0] <= 2

    postas = [l for l in metas if not enchimento(_entradas(meta_sec, l))]
    if not postas:
        print("aviso: o kit ainda nao foi aplicado no tileset; caso 11 nao roda")
    else:
        if len(postas) != len(metas):
            mau.append("o kit esta pela metade no disco: %d de %d metatiles"
                       % (len(postas), len(metas)))
        for local, ent in metas.items():
            if _entradas(meta_sec, local) != ent:
                mau.append("o metatile %d no disco nao e o do kit" % (512 + local))
            if struct.unpack_from("<H", attr_sec, local * 2)[0] != attrs[local]:
                mau.append("o atributo do metatile %d no disco nao e o do kit"
                           % (512 + local))
        for v_, tile in tiles_novos.items():
            if (v_ // cols) * 8 + 8 > png.size[1]:
                mau.append("a vaga de tile %d nao cabe no tiles.png" % v_)
                continue
            x0, y0 = (v_ % cols) * 8, (v_ // cols) * 8
            if [[pxd[x0 + x, y0 + y] for x in range(8)] for y in range(8)] != tile:
                mau.append("o tile da vaga %d no disco nao e o do kit" % v_)
        for vaga in (PAL_CAMPO, PAL_RUINA):
            if _le_pal(vaga) != dados["paletas"][str(vaga)]:
                mau.append("a paleta %d no disco nao e a do kit" % vaga)

    if mau:
        print("DEMO VERMELHA")
        for x in dict.fromkeys(mau):
            print("  -", x)
        return 1
    linhas = []
    for alvo in ALVOS:
        L, W, H, v, escritas, contas, _s = resumo[alvo]
        a, _na, _i = regua(v, W, H, L)
        b, _nb, _j = regua(v, W, H, L, escritas)
        linhas.append("%s %.1f%% -> %.1f%% (%d celulas)"
                      % (alvo, a, b, len(escritas)))
    print("DEMO VERDE: %d tiles, %d metatiles, vagas %d e %d, %s, 11 casos"
          % (len(tiles_novos), len(metas), PAL_CAMPO, PAL_RUINA,
             "; ".join(linhas)))
    return 0


def main():
    if "--extrai" in sys.argv:
        return extrai()
    if "--demo" in sys.argv or "--autoteste" in sys.argv:
        return demo()
    if "--desfazer" in sys.argv:
        return desfaz()
    return roda("--aplicar" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
