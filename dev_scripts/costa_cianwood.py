#!/usr/bin/env python3
"""Refino de `CianwoodCity` (tema PRAIA e PENHASCO), no `gTileset_CianwoodCity`,
com arte importada do `Pokémon Scorched Silver`.

O QUE ESTA CIDADE TEM DE ERRADO, medido pela `dev_scripts/regua_cidades.py` nesta
árvore em 09/09/2026: `CianwoodCity` é a mais pobre de Johto inteira, com 54,5%
do chão andável a pé (491 células de 901) num metatile só, o 113. E o segundo
carimbo é quase tão grande quanto: o metatile 277, a areia da vila, ocupa outras
236 células, 26,2%. Os dois somados dão 80,7% do chão andável.

DOIS CARIMBOS E DUAS FAMÍLIAS, e é isso que decide o desenho desta passada. A
régua mede o DOMINANTE, então derrubar só o 113 não fecha nada: o 277 assume o
posto no mesmo instante, e 26,2% continua acima do teto de 20% da onda. Pior,
solidificar célula tira do denominador e chega a SUBIR a fração do que sobra. As
duas famílias são tratadas juntas, cada uma com o próprio catálogo, e as duas
medidas antes e depois.

AS DUAS FAMÍLIAS NÃO SÃO A MESMA COISA NEM NA GEOMETRIA NEM NA MONTAGEM, e a
diferença foi medida célula a célula antes de uma linha ser escrita:

  - O CARIMBO 113 É O PENHASCO, e ele não é o chão da vila: é o paredão de rocha
    que fecha a cidade a oeste. Ele tem atributo 0x1000, ou seja comportamento
    `MB_NORMAL` e layerType COVERED, e a arte dele mora na camada de CIMA (os
    tiles 0x082, 0x083, 0x092 e 0x093 da paleta 1 do primário, os quatro 100%
    opacos); a camada de baixo é o tile 0x013 repetido quatro vezes, um verde
    chapado que NENHUM pixel mostra. Rotulando os componentes de chão andável
    ligados a pé, as 491 células dele se repartem assim: 459 no pedaço de x=0 a
    x=9 e y=3 a y=60, que é um bloco de 460 células SEPARADO da vila, e as 32
    restantes espalhadas. O jogador NÃO ANDA nesse bloco: os componentes da
    cidade são nove e a vila é outro, o de 405 células. Ele conta na régua e
    aparece na tela (a câmera mostra quinze colunas, e de dentro da vila as
    colunas 3 a 9 estão no quadro), mas ninguém pisa nele. `enfeita_cidades.
    alcance` o dá por alcançado, e isso é uma armadilha e não um fato: aquela
    conta parte de warp OU DE OBJETO, e há cinco objetos plantados lá dentro
    (dois SHUCKLE, dois GEODUDE e o engenheiro de (0,34)). Quem separa é a
    rotulação de componentes, que é o segundo portão desta onda.
  - O CARIMBO 277 É A AREIA DA VILA, com atributo 0x0021, ou seja `MB_SAND` e
    layerType NORMAL, e a arte dele mora na camada de BAIXO (os tiles 0x020 e
    0x021 da paleta 5), com a de cima VAZIA. Com layerType NORMAL a camada de
    cima vai para o BG1, que desenha ACIMA de todo sprite: areia por cima do
    boneco seria defeito, não enfeite, e por isso toda peça de CHÃO desta
    família entra na camada de BAIXO e deixa a de cima vazia, exatamente como o
    277 faz.

Então cada família tem a própria montagem, e as duas são as do metatile que elas
substituem, bit a bit:

    penhasco   chão   = [camada de baixo do 113] + [arte de rocha]     attr 0x1000
    penhasco   móvel  = [camada de CIMA do 113]  + [arte da peça]      attr 0x1000
    praia      chão   = [arte de areia]          + [vazio]             attr 0x0021
    praia      móvel  = [camada de baixo do 277] + [arte da peça]      attr 0x1000
    praia      topo   = [camada de baixo do 277] + [arte da peça]      attr 0x0021

A linha do MÓVEL do penhasco é a que precisa de explicação, porque ela parece
errada e não é: o chão VISÍVEL do penhasco é a camada de CIMA do 113, e não a de
baixo. Pôr a camada de baixo dele embaixo de um pedregulho encheria a célula de
verde chapado em volta da pedra. Com COVERED as duas camadas ficam ABAIXO do
sprite (`DrawMetatile` em `src/fieldmap.c`), então descer a rocha para a camada
de baixo não muda nada do que se vê e libera a de cima para a peça.

O CHÃO NOVO É NOSSO, E ISSO NÃO É ECONOMIA, É COR. As duas ROM hacks foram
abertas e medidas antes de a decisão ser tomada, e as duas REPROVAM como tapete:

  - a rocha do `Scorched Silver` (o secundário 0x492AD4 sobre o primário
    0x49240C, o par da vila de praia dele) é ROSADA: (216,176,160) de claro e
    (128,88,88) de sombra. A nossa é (192,168,120) e (176,136,88), um marrom
    quente. São 47 de distância RGB no tom claro e uma diferença de MATIZ, não
    de luminância: em mancha ao lado do carimbo isso vira retalho rosa no meio
    do penhasco marrom, que é o defeito nº 1 da lista do `enfeita_cidades.py`.
  - a areia dele é (216,200,128) contra a nossa (238,230,139), 38,8 de
    distância. Essa passaria (o `costa_sandgem.py` aceitou 42 em Sandgem), e ela
    ENTRA, mas como areia MOLHADA e em pouca célula, não como base.

E o nosso tileset tem o que faz falta, de graça. Varrendo os 640 metatiles do
`gTileset_JohtoNorthEast` e os 240 do `gTileset_CianwoodCity` atrás de camada
inteira com quatro tiles 100% opacos e SÓ cores da família (sem verde de grama,
sem cinza de calçada, sem azul de água), sobram TRÊS desenhos de rocha (os
metatiles 108, 113 e 121, sendo que 124, 351, 469 e 539 são o MESMO desenho do
121, com distância RGB ZERO entre eles, e o 485 foi cortado porque tem 14 pixels
de verde no canto) e cento e vinte e sete de areia, em DOIS tons: o claro do
próprio 277, (238,230,139), e um tostado, (213,197,131), que é areia batida. Cada
desenho rende QUATRO silhuetas sem custar tile nem cor, pelos bits de espelho
horizontal e vertical que a entrada de metatile já carrega (0x400 e 0x800), e é
assim que o próprio primário faz nos pares dele.

O QUE VEM DA ROM HACK, então, é o que o nosso tileset NÃO tem: as peças. Fonte
única, `Pokémon Scorched Silver` v1.3 Complete, de Sloo sobre o
pokeemerald-expansion da RHH, base Emerald (BPEE), md5
`f7af51cecd3e170cc373fba01753053c`, cópia privada em
`fontes-mapas/romhacks/scorched-silver/`. O par é o primário `0x49240C` com o
secundário `0x492AD4`, que é a vila de praia do hack (o mapa g00m15, 60x50, com
coqueiro, penhasco e areia). O `--extrai` confere o md5 ANTES de ler um byte e
para se a cópia for outra. A ROM nunca entra no repositório: o que está
versionado é o kit CONVERTIDO, em `dev_scripts/costa_cianwood_kit.json`, com a
paleta em RGB e o tile em nibble já reindexado para a vaga nova.

O ORÇAMENTO DE PALETA, medido nesta árvore. `NUM_PALS_TOTAL` é 13
(`include/fieldmap.h`) e Johto é `bigPrimary`: sete vagas do primário (0 a 6) e
SEIS do secundário (7 a 12). Contando por metatile VIVO (os que aparecem em
`map.bin` de algum dos cinco layouts do tileset), as vagas do secundário em uso
são 8, 9, 11 e 12, e as vagas 7 e 10 não são pintadas por pixel nenhum que
chegue à tela. Duas vagas livres é orçamento largo para esta onda: a rodada de
Snowpoint teve UMA.

    vaga  7   PRAIA   13 cores: a areia molhada (paleta 5 do hack) e o coqueiro
                      (paleta 2 do hack), que dividem a vaga porque a união das
                      duas dá 13 EXATAS, medido
    vaga 10   PEDRA    7 cores: o pedregulho de granito e o poste de luz, os
                      dois na paleta 1 do hack

O QUE FICOU DE FORA, e por CARÁTER, não por orçamento. O secundário `0x492AD4` é
um balneário: ele tem guarda-sol em três cores, espreguiçadeira, cabine de
banho e toldo listrado, tudo desenhado e tudo cabendo (o par de guarda-sóis custa
11 cores e a espreguiçadeira 7). Não entram. Cianwood é a cidade do Chuck, uma
vila rude de ilha com ginásio de luta, farmácia e Shuckle na pedra, e não um
resort: guarda-sol ali descaracteriza do mesmo jeito que a calçada de pedra
descaracterizou Snowpoint, que é a decisão 56 do Gui. O que entra da praia é o
COQUEIRO, e ainda assim só na metade SUL, que é o lado do mar aberto, pela mesma
regra que o `costa_sandgem.py` usou em Sandgem.

O QUE FICOU DE FORA POR MEDIDA: o metatile 485 do nosso primário (14 pixels de
verde de grama no canto, que apareceriam como um respingo no meio da rocha) e os
metatiles 124, 351, 469 e 539, que desenham os MESMOS 256 pixels do 121 e por
isso são a mesma variante, não quatro. O caso 6 do auto-teste reprova variante
que é cópia pixel a pixel de outra, que é a regra 8 desta onda.

Uso:
    python3 dev_scripts/costa_cianwood.py                  # mede e mostra o plano
    python3 dev_scripts/costa_cianwood.py --aplicar        # grava tileset e mapa
    python3 dev_scripts/costa_cianwood.py --desfazer       # devolve o map.bin
    python3 dev_scripts/costa_cianwood.py --demo           # auto-teste
    python3 dev_scripts/costa_cianwood.py --extrai         # regera o kit da ROM
    python3 dev_scripts/costa_cianwood.py --so-tileset     # so o tileset, sem mapa
    python3 dev_scripts/costa_cianwood.py --prova-extracao # o par do hack, pixel a pixel
    python3 dev_scripts/costa_cianwood.py --prova-tiles    # o kit contra a ROM
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

# O bloco de teste DESTA rodada e derivado do desenho, e nao o contrario: se o
# `corredores_de_teste` o lesse, o corredor sairia do proprio enfeite.
E.BLOCO_PROPRIO = "200_costa_cianwood.json"

DESTINO = f"{RAIZ}/data/tilesets/secondary/cianwood_city"
KIT_JSON = f"{RAIZ}/dev_scripts/costa_cianwood_kit.json"
PLANO = f"{RAIZ}/dev_scripts/costa_cianwood.json"

PRIMARIO = "gTileset_JohtoNorthEast"
SECUNDARIO = "gTileset_CianwoodCity"
ALVO = "CianwoodCity"
# Os CINCO layouts que dividem o `gTileset_CianwoodCity`, lidos de
# `data/layouts/layouts.json` nesta arvore. As quatro rotas sao a PROVA de nao
# regressao desta passada: se so vaga livre for ocupada, elas renderizam com
# zero pixel de diferenca, e isso e medido, nao presumido.
IRMAOS = [ALVO, "Route41", "Route44", "Route47", "Route48"]

# JOHTO E `bigPrimary`, e a conta nao e a de Sinnoh (medido em
# `tools/mapjson/mapjson.cpp` e `include/fieldmap.h`): o primario leva 640
# tiles, 640 metatiles e 7 paletas, e o secundario 384 / 384 / 6. O atributo de
# metatile continua de 2 bytes.
N_META_PRI = 640
N_TILES_PRI = 640
N_PAL_PRI = 7
TETO_TILES = 384
TETO_META = 384
TILE_LOCAL_0 = 96           # o tiles.png tem 96 tiles; sobram 288 vagas
META_LOCAL_0 = 240          # ha 240 metatiles definidos; sobram 144 vagas no fim
MARGEM = 1
TETO_REGUA = 20.0           # o alvo desta onda: carimbo dominante <= 20%
PISO_DIST = 8.0             # distancia RGB minima entre duas variantes de chao

# ------------------------------------------------------------------- a FONTE
SS = dict(slug="scorched-silver", hack="Pokemon Scorched Silver", autor="Sloo",
          md5="f7af51cecd3e170cc373fba01753053c", base="Emerald (BPEE)",
          pri=0x49240C, sec=0x492AD4, split=(512, 512, 6))

# PALETA DE ORIGEM -> VAGA NOSSA. As paletas 5 (areia) e 2 (folhagem do
# coqueiro) do hack dividem a vaga 7 porque a uniao delas da 13 cores, medido; a
# paleta 1 (granito e metal) fica sozinha na vaga 10 com 7.
VAGAS_PAL = {5: 7, 2: 7, 1: 10}

# Quantos metatiles DIFERENTES da fonte precisam repetir o mesmo PADRAO de
# camada de baixo para ele ser piso da fonte. Medido no par desta rodada: no
# primario do hack os padroes de piso aparecem 96, 58, 41, 27, 19, 15, 12, 11, 9
# e 7 vezes e o primeiro padrao de ARTE aparece 3; o corte de 4 fica com folga.
PISO_MIN = 4

# ------------------------------------------------------------------ as FAMILIAS
# `camada` diz em qual camada do metatile a arte da FAMILIA mora, e e ela que
# separa a montagem das duas. `attr` e o atributo INTEIRO do carimbo.
# `solidos` diz se a MANCHA daquela familia tambem pinta celula SOLIDA. So o
# penhasco liga isso, e o motivo esta no render de 09/09/2026: o metatile 113
# aparece 948 vezes no mapa, 491 com colisao 0 e 457 com colisao 1, e as duas
# metades sao o MESMO paredao de rocha na tela. Pintando so as andaveis, a
# textura nova parava numa linha reta invisivel no meio do penhasco e o oeste do
# mapa ficava com um retangulo de rocha manchada dentro de um paredao liso, que
# le como bug de mapa. Pintar celula solida nao mexe em nada mecanico: a colisao
# continua 1, a elevacao continua a mesma, celula solida nao entra na regua nem
# na regra de (comportamento, layerType) das andaveis, e o metatile novo tem o
# atributo INTEIRO do 113.
FAMILIAS = {
    "penhasco": dict(carimbo=113, attr=0x1000, camada=1, solidos=True),
    "praia":    dict(carimbo=277, attr=0x0021, camada=0, solidos=False),
}

# ------------------------------------------------------------------- os TEMAS
# CHAO NOSSO: `mt` e o metatile do nosso par de onde a ARTE sai, e `giro` diz
# qual das quatro orientacoes entra (0 = como esta, 1 = espelho horizontal,
# 2 = vertical, 3 = os dois). A arte e copiada da camada da FAMILIA e reassentada
# sobre a base dela, com o atributo do carimbo. Custa ZERO tile e ZERO cor.
CHAO_NOSSO = {
    # tres desenhos de rocha x quatro orientacoes. O 113 na orientacao 0 e o
    # proprio carimbo e por isso nao entra.
    "penhasco": [
        dict(nome="rocha clara",        mt=108, giro=0),
        dict(nome="rocha clara H",      mt=108, giro=1),
        dict(nome="rocha clara V",      mt=108, giro=2),
        dict(nome="rocha clara HV",     mt=108, giro=3),
        dict(nome="rocha media H",      mt=113, giro=1),
        dict(nome="rocha media V",      mt=113, giro=2),
        dict(nome="rocha media HV",     mt=113, giro=3),
        dict(nome="rocha escura",       mt=121, giro=0),
        dict(nome="rocha escura H",     mt=121, giro=1),
        dict(nome="rocha escura V",     mt=121, giro=2),
        dict(nome="rocha escura HV",    mt=121, giro=3),
    ],
    # A AREIA TEM DOIS TONS E SO DOIS, e isso foi MEDIDO, nao escolhido. Varrendo
    # os 880 metatiles do par atras de camada de baixo com quatro tiles opacos e
    # so cores de areia, sobram 127 candidatos; comparados pixel a pixel, TODOS
    # eles caem em dois grupos: o claro do proprio 277, (238,230,139), e o
    # tostado do 351, (213,197,131). A distancia media entre os dois grupos e
    # 43,7 e DENTRO de cada grupo ela e 3,4 ou ZERO, ou seja o que parecia
    # "quinze variantes de areia" no atlas era o mesmo desenho com um seixo em
    # outro lugar. O caso 6 do auto-teste reprovou a primeira lista inteira, e
    # foi ele que obrigou esta secao a ser reescrita.
    #
    # Entao a variacao da praia sai da MISTURA dos dois tons no nivel do
    # QUADRANTE: `claro` diz de onde vem o tom claro e `mascara` diz quais dos
    # quatro quadrantes recebem o tom escuro (bit 0 = quadrante NO, 1 = NE,
    # 2 = SO, 3 = SE). Um quadrante trocado ja da 43,7/4 = 10,9 de distancia,
    # acima do piso de 8,0, e o desenho que sai e o de areia umida avancando
    # sobre a seca, que e o que a mare deixa numa praia de verdade. Custa ZERO
    # tile e ZERO cor: os dois tiles ja estao no `tiles.png`.
    "praia": [
        dict(nome="areia umida",        mt=351, giro=0),
        dict(nome="areia umida H",      mt=351, giro=1),
        dict(nome="areia umida V",      mt=351, giro=2),
        dict(nome="mare canto NO",      mt=351, giro=0, claro=277, mascara=0x1),
        dict(nome="mare canto NE",      mt=351, giro=1, claro=277, mascara=0x2),
        dict(nome="mare canto SO",      mt=351, giro=2, claro=277, mascara=0x4),
        dict(nome="mare canto SE",      mt=351, giro=0, claro=277, mascara=0x8),
        dict(nome="mare norte",         mt=351, giro=1, claro=277, mascara=0x3),
        dict(nome="mare sul",           mt=351, giro=2, claro=277, mascara=0xC),
        dict(nome="mare oeste",         mt=351, giro=0, claro=277, mascara=0x5),
        dict(nome="mare leste",         mt=351, giro=1, claro=277, mascara=0xA),
        dict(nome="mare diagonal",      mt=351, giro=2, claro=277, mascara=0x6),
        dict(nome="mare diagonal 2",    mt=351, giro=0, claro=277, mascara=0x9),
        dict(nome="mare quase cheia",   mt=351, giro=1, claro=277, mascara=0x7),
        dict(nome="mare quase cheia 2", mt=351, giro=2, claro=277, mascara=0xB),
        dict(nome="mare quase cheia 3", mt=351, giro=0, claro=277, mascara=0xD),
        dict(nome="mare quase cheia 4", mt=351, giro=1, claro=277, mascara=0xE),
    ],
}

# CHAO IMPORTADO: a areia MOLHADA do hack, o unico tapete que vem de fora nesta
# passada. Ela entra na camada de baixo inteira, como o 277 faz, e a camada de
# cima tem que estar vazia na fonte.
CHAO_SS = [
    dict(nome="areia molhada",   ss=289, familia="praia"),
    dict(nome="areia lavada",    ss=297, familia="praia"),
]

# MOVEIS IMPORTADOS de uma celula: arte na camada de CIMA, com furo. `familia`
# diz sobre qual carimbo a peca pousa; `ambas` significa que ela serve as duas.
MOVEIS_SS = [
    dict(nome="pedra grande",  ss=197, familia="ambas"),
    dict(nome="pedra meia",    ss=315, familia="ambas"),
    dict(nome="pedra lasca",   ss=354, familia="ambas"),
    dict(nome="pedra lasca 2", ss=355, familia="ambas"),
]

# BLOCOS IMPORTADOS: `linhas` e a grade de metatiles da fonte, de cima para
# baixo. A ULTIMA linha vira SOLIDA em COVERED e as de cima continuam ANDAVEIS
# com o atributo do carimbo, o que poe a arte delas no BG1 e faz o jogador passar
# ATRAS. So a familia `praia` aceita bloco: o `penhasco` e COVERED, e em COVERED
# nao existe "passar atras".
BLOCOS_SS = [
    dict(nome="coqueiro alto", familia="praia", faixa="sul",
         linhas=[[626, 627], [634, 635], [642, 643]]),
    dict(nome="coqueiro",      familia="praia", faixa="sul",
         linhas=[[634, 635], [642, 643]]),
    dict(nome="poste de luz",  familia="praia",
         linhas=[[46], [47]]),
]

# MOVEIS NOSSOS: a ARTE sai da camada de cima de um metatile do nosso par e a
# celula vira solida em COVERED com comportamento zerado. Custa ZERO.
# A `flor` (metatile 4) foi CORTADA por medida: a camada de cima dela e 100%
# opaca nos quatro quadrantes (256 pixels de 256), ou seja ela e um tapete de
# canteiro sobre grama, e plantada na areia viraria um retangulo verde. Ficaram
# as tres que tem furo de verdade.
MOVEIS_NOSSOS = [
    dict(nome="placa de madeira", mt=3,   familia="praia"),
    dict(nome="poste duplo",      mt=222, familia="praia"),
    dict(nome="poste de madeira", mt=240, familia="penhasco"),
]

# QUANTAS DE CADA, por familia. Os grupos de mancha sao GRANDES de proposito:
# grupo de uma peca so faz cada bolha sair de uma cor unica, e ai saber onde a
# celula esta passa a adivinhar o que ela e, que e o caso 11a do auto-teste.
TEMA = dict(
    alvo=ALVO,
    bolhas={
        "penhasco": [
            dict(grupo=["rocha clara", "rocha clara H", "rocha clara V",
                        "rocha clara HV"],                    quantas=70, tam=(18, 38)),
            dict(grupo=["rocha escura", "rocha escura H", "rocha escura V",
                        "rocha escura HV"],                   quantas=70, tam=(18, 38)),
            dict(grupo=["rocha media H", "rocha media V", "rocha media HV",
                        "rocha clara HV", "rocha escura H"],  quantas=70, tam=(16, 34)),
        ],
        # A AREIA IMPORTADA VEM PRIMEIRO na lista, e isso nao e estilo. As bolhas
        # sao servidas UMA por especificacao a cada rodada e a vila tem so 236
        # celulas de areia, das quais 127 sobram depois da orla dos 39 eventos e
        # dos corredores da suite: na primeira versao a areia molhada estava no
        # fim e ficou com ZERO celulas, ou seja a unica arte de chao que vem da
        # ROM hack nao aparecia no mapa.
        "praia": [
            dict(grupo=["areia molhada", "areia lavada"],      quantas=16, tam=(8, 16)),
            dict(grupo=["mare canto NO", "mare canto NE", "mare canto SO",
                        "mare canto SE"],                      quantas=16, tam=(9, 18)),
            dict(grupo=["mare norte", "mare sul", "mare oeste",
                        "mare leste"],                         quantas=16, tam=(9, 18)),
            dict(grupo=["mare diagonal", "mare diagonal 2",
                        "areia umida", "areia umida H"],       quantas=16, tam=(8, 16)),
            dict(grupo=["mare quase cheia", "mare quase cheia 2",
                        "mare quase cheia 3", "mare quase cheia 4",
                        "areia umida V"],                      quantas=16, tam=(8, 16)),
        ],
    },
    moveis=[
        dict(nome="pedra grande",    familia="penhasco", quantos=7, espaco=6),
        dict(nome="pedra meia",      familia="penhasco", quantos=6, espaco=6),
        dict(nome="pedra lasca",     familia="penhasco", quantos=5, espaco=6),
        dict(nome="pedra lasca 2",   familia="penhasco", quantos=5, espaco=6),
        dict(nome="pedra grande",    familia="praia",    quantos=4, espaco=7),
        dict(nome="pedra meia",      familia="praia",    quantos=3, espaco=7),
        dict(nome="pedra lasca",     familia="praia",    quantos=3, espaco=7),
        dict(nome="placa de madeira", familia="praia",   quantos=1, espaco=12),
        dict(nome="poste duplo",     familia="praia",    quantos=2, espaco=8),
        dict(nome="poste de madeira", familia="penhasco", quantos=3, espaco=8),
    ],
    blocos=[
        dict(nome="coqueiro alto", quantos=2, espaco=6),
        dict(nome="coqueiro",      quantos=3, espaco=5),
        dict(nome="poste de luz",  quantos=3, espaco=7),
    ],
)

ESPACO_ENTRE_MOVEIS = 2     # Chebyshev minimo entre dois moveis QUAISQUER
PISO_BOLHA = 4              # tamanho minimo de uma bolha que a regiao cortou

N4 = E.N4


def _mistura(*n):
    """Hash determinista de inteiros, 32 bits. Nada de `random`: o plano tem
    que sair identico em qualquer maquina e em qualquer versao de Python."""
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


def _attr_nosso(gid):
    """Atributo de um metatile do DISCO, com o corte de 640 de Johto.

    `arte_ginasios_sinnoh.comportamento` corta em 512, que e a conta de
    Hoenn/Sinnoh, e em Johto isso le o secundario no lugar errado. A diferenca
    foi medida nesta arvore e e pequena em Cianwood (901 celulas andaveis contra
    902), mas ela existe e nenhuma conta DESTE script depende dela.
    """
    ap, asec = G._attrs(PRIMARIO), G._attrs(SECUNDARIO)
    t, i = (ap, gid) if gid < N_META_PRI else (asec, gid - N_META_PRI)
    return t[i] if 0 <= i < len(t) else 0


def _ents_nosso(gid):
    tp, ts = _tileset(PRIMARIO), _tileset(SECUNDARIO)
    tset, loc = (tp, gid) if gid < N_META_PRI else (ts, gid - N_META_PRI)
    return list(struct.unpack_from("<8H", tset["metatiles"], loc * 16))


def _arte_de_chao(c, camada):
    """As quatro entradas de arte de uma peca de CHAO nossa.

    Sem `claro` e o metatile inteiro, girado. Com `claro`, cada quadrante vem do
    tom claro ou do escuro conforme o bit da `mascara`, que e a mistura de dois
    tons descrita em CHAO_NOSSO.
    """
    escuro = _gira(_ents_nosso(c["mt"])[camada * 4:camada * 4 + 4], c["giro"])
    if any(not (v & 0x3FF) for v in escuro):
        raise SystemExit("o metatile %d tem quadrante vazio na camada %d e nao "
                         "serve de chao" % (c["mt"], camada))
    if "claro" not in c:
        return escuro
    claro = _gira(_ents_nosso(c["claro"])[camada * 4:camada * 4 + 4],
                  c.get("giro_claro", 0))
    if any(not (v & 0x3FF) for v in claro):
        raise SystemExit("o metatile %d (tom claro) tem quadrante vazio"
                         % c["claro"])
    if not 1 <= c["mascara"] <= 14:
        raise SystemExit("a mascara 0x%X de %s e tom puro, nao mistura"
                         % (c["mascara"], c["nome"]))
    return [escuro[i] if (c["mascara"] >> i) & 1 else claro[i] for i in range(4)]


def _opacos_de(entradas):
    """Quantos pixels acesos as quatro entradas desenham, no total."""
    import render_maps as RM
    tp, ts = _tileset(PRIMARIO), _tileset(SECUNDARIO)
    tot = 0
    for v in entradas:
        idx = v & 0x3FF
        if not idx:
            continue
        tile = RM.resolver_tile(tp, ts, idx)
        if tile:
            tot += sum(1 for linha in tile for c in linha if c)
    return tot


def _gira(quad, giro):
    """Uma das quatro orientacoes de uma camada de metatile.

    Espelhar nao custa tile nem cor: os bits 0x400 (horizontal) e 0x800
    (vertical) da entrada ja existem e o proprio primario os usa nos pares dele.
    Girar tambem TROCA a ordem dos quadrantes, senao o desenho sai com as
    metades no lugar errado.
    """
    ordem, bits = {0: ([0, 1, 2, 3], 0x000),
                   1: ([1, 0, 3, 2], 0x400),
                   2: ([2, 3, 0, 1], 0x800),
                   3: ([3, 2, 1, 0], 0xC00)}[giro]
    return [0 if not (quad[i] & 0x3FF) else (quad[i] ^ bits) for i in ordem]


def carimbo_de(qual):
    """(camada de BASE, camada de ARTE, atributo) do carimbo da familia.

    A camada de BASE e a que fica embaixo da arte no metatile do carimbo; a de
    ARTE e a que desenha. No `penhasco` isso e (baixo, cima) e na `praia` e
    (cima, baixo), e e essa inversao que as duas familias tem de diferente.
    """
    f = FAMILIAS[qual]
    ents = _ents_nosso(f["carimbo"])
    if _attr_nosso(f["carimbo"]) != f["attr"]:
        raise SystemExit("o carimbo %d de %s tem atributo 0x%04X e o script "
                         "espera 0x%04X" % (f["carimbo"], qual,
                                            _attr_nosso(f["carimbo"]), f["attr"]))
    if f["camada"] == 1:
        return ents[:4], ents[4:], f["attr"]
    if any(v & 0x3FF for v in ents[4:]):
        raise SystemExit("o carimbo %d de %s ja usa a camada de cima"
                         % (f["carimbo"], qual))
    return ents[4:], ents[:4], f["attr"]


def monta_chao(qual, arte):
    """As oito entradas de um metatile de CHAO da familia."""
    base, _a, _at = carimbo_de(qual)
    return (list(base) + list(arte)) if FAMILIAS[qual]["camada"] == 1 \
        else (list(arte) + list(base))


def piso_visivel(qual):
    """As quatro entradas que MOSTRAM o chao da familia.

    E a camada de ARTE do carimbo, e nao a de baixo: no penhasco a camada de
    baixo do 113 e verde chapado que nenhum pixel mostra.
    """
    _b, arte, _at = carimbo_de(qual)
    return list(arte)


def monta_movel(qual, arte):
    """Camada de baixo = o chao VISIVEL da familia; camada de cima = a peca."""
    return piso_visivel(qual) + list(arte)


def vagas_livres():
    """{vaga: [indices de cor que NENHUM pixel VIVO nosso usa]}.

    "Vivo" e a palavra que importa: o `gTileset_CianwoodCity` define 240
    metatiles e so 124 deles aparecem em `map.bin` de algum dos cinco layouts. O
    portao que prova que a conta esta certa nao esta aqui, esta no render das
    quatro rotas irmas com ZERO pixel diferente.

    Os metatiles que ESTA passada grava sao ignorados de proposito, para que
    rodar `--extrai` depois de `--aplicar` de o mesmo kit.
    """
    import render_maps as RM
    ts, tp = _tileset(SECUNDARIO), _tileset(PRIMARIO)
    usados = collections.defaultdict(set)
    vivos = set()
    for nome in IRMAOS:
        vivos |= {c & 0x3FF for c in G.grade(nome)[4]}

    def anota(tset, loc):
        for (it, fh, fv, ip) in RM.entradas_metatile(tset["metatiles"], loc):
            if it == 0 or ip < N_PAL_PRI:
                continue
            tile = RM.resolver_tile(tp, ts, it)
            if tile is None:
                continue
            for linha in tile:
                for c in linha:
                    if c:
                        usados[ip].add(c)

    for gid in sorted(x for x in vivos if x >= N_META_PRI):
        local = gid - N_META_PRI
        if local < META_LOCAL_0:
            anota(ts, local)
    # A ARMADILHA 4 do `compacta_paletas.py`: metatile do PRIMARIO alcancavel
    # tambem pode pintar com vaga de secundario. A conta roda de qualquer jeito,
    # porque "medi uma vez" nao e portao.
    for gid in sorted(x for x in vivos if x < N_META_PRI):
        anota(tp, gid)
    return {v: [i for i in range(1, 16) if i not in usados[v]]
            for v in range(N_PAL_PRI, 13)}


# ---------------------------------------------------------------- a EXTRACAO
def _nibbles(dados, local):
    """8 linhas de 8 nibbles, o pixel PAR no nibble BAIXO (ver extrai_tileset)."""
    b = dados[local * 32:local * 32 + 32]
    return [[(b[y * 4 + (x >> 1)] >> (0 if x % 2 == 0 else 4)) & 0xF
             for x in range(8)] for y in range(8)]


def _rgb(ts, i):
    """BGR555 do GBA para o RGB888 que o repo usa: cinco bits DESLOCADOS TRES
    casas, nao esticados para 0..255.

    Todo `.pal` deste repositorio esta na conta de deslocar, e o
    `ferramentas/prova_extracao.py`, que e o portao da extracao, tambem.
    """
    c = struct.unpack_from("<16H", ts["pal"], i * 32)
    return [[((v >> s) & 0x1F) << 3 for s in (0, 5, 10)] for v in c]


def _piso_da_fonte(tset):
    """Os tiles que a FONTE usa como piso, por evidencia e nao por decoreba.

    Duas assinaturas: (a) padrao de camada de baixo que aparece em PISO_MIN
    metatiles diferentes ou mais; (b) camada de baixo que repete o MESMO tile
    nos quatro quadrantes. Piso e o que se repete debaixo de tudo; arte de peca
    aparece em um ou dois metatiles.
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


def _lista_de_pecas():
    """[(papel, dict)] de tudo que precisa sair da ROM, em ordem FIXA."""
    lista = [("chao", c) for c in CHAO_SS]
    lista += [("movel", m) for m in MOVEIS_SS]
    for b in BLOCOS_SS:
        for li, linha in enumerate(b["linhas"]):
            for k, loc in enumerate(linha):
                lista.append(("movel", dict(
                    nome="%s L%d C%d" % (b["nome"], li, k), ss=loc)))
    return lista


def extrai():
    """Regera `costa_cianwood_kit.json` a partir da ROM privada do Scorched Silver."""
    ferr = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/romhacks"
    if not os.path.isdir(ferr):
        raise SystemExit("nao achei fontes-mapas/romhacks: --extrai so roda na "
                         "maquina que tem as ROMs. O kit ja extraido esta em "
                         + os.path.relpath(KIT_JSON, RAIZ))
    sys.path.insert(0, f"{ferr}/ferramentas")
    import hashlib
    from gbamap import Rom  # noqa: E402

    pasta = os.path.join(ferr, SS["slug"])
    gba = [f for f in sorted(os.listdir(pasta)) if f.lower().endswith(".gba")][0]
    caminho = os.path.join(pasta, gba)
    md5 = hashlib.md5(open(caminho, "rb").read()).hexdigest()
    if md5 != SS["md5"]:
        raise SystemExit("a ROM em %s tem md5 %s e o kit foi feito com %s"
                         % (gba, md5, SS["md5"]))
    r = Rom(caminho)
    r.n_meta_pri, r.n_tiles_pri, r.n_pal_pri = SS["split"]
    t1 = r.parse_tileset(SS["pri"])
    t2 = r.parse_tileset(SS["sec"])
    if t1 is None or t2 is None:
        raise SystemExit("o par 0x%X / 0x%X do hack nao abriu"
                         % (SS["pri"], SS["sec"]))
    NP = r.n_tiles_pri
    livres = vagas_livres()
    pal = {i: _rgb(t1 if i < r.n_pal_pri else t2, i) for i in range(16)}
    piso = dict(p=_piso_da_fonte(t1), s=_piso_da_fonte(t2))

    def ents_de(ss):
        """As oito entradas do metatile GLOBAL `ss` da fonte.

        O id e global no espaco do hack: abaixo de `n_meta_pri` ele mora no
        primario e acima dele no secundario, com o local descontado. Errar isso
        nao da erro silencioso, da `unpack_from` fora do buffer, e foi assim que
        a primeira rodada de `--extrai` parou.
        """
        tset, local = ((t1, ss) if ss < r.n_meta_pri
                       else (t2, ss - r.n_meta_pri))
        return list(struct.unpack_from("<8H", tset["meta"], local * 16))

    def px_de(idx):
        return (_nibbles(t1["tiles"], idx) if idx < NP
                else _nibbles(t2["tiles"], idx - NP))

    def branco(v):
        """A entrada aponta para um tile 8x8 SEM UM PIXEL aceso?"""
        idx = v & 0x3FF
        if not idx:
            return True
        return not any(c for linha in px_de(idx) for c in linha)

    def eh_piso(v):
        idx = v & 0x3FF
        lado = "p" if idx < NP else "s"
        return idx in piso[lado]

    tiles_px, tiles_vaga, tiles_cor = {}, {}, {}

    def guarda(v):
        """Registra o tile 8x8 daquela entrada e devolve a chave dele.

        A CHAVE LEVA A PALETA DE ORIGEM: o mesmo desenho 8x8 pintado com duas
        paletas do hack tem que virar DUAS vagas nossas, senao a segunda apaga a
        primeira.
        """
        idx, ip = v & 0x3FF, (v >> 12) & 0xF
        if ip not in VAGAS_PAL:
            return None
        lado, li = ("p", idx) if idx < NP else ("s", idx - NP)
        ch = "%s:%d:%d" % (lado, li, ip)
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
    for papel, p in _lista_de_pecas():
        ents = ents_de(p["ss"])
        baixo, cima = ents[:4], ents[4:]
        if papel == "chao":
            # o chao entra INTEIRO na camada de baixo, e a de cima da fonte tem
            # que estar vazia: camada de cima em celula andavel com layerType
            # NORMAL desenha ACIMA do jogador.
            if any(not branco(v) for v in cima):
                raise SystemExit("%s: a peca de chao %d tem camada de cima"
                                 % (p["nome"], p["ss"]))
            if len({v & 0x3FF for v in baixo}) < 2:
                raise SystemExit("%s: o metatile %d repete o mesmo tile nos "
                                 "quatro quadrantes, e por isso e chao liso da "
                                 "fonte, nao arte" % (p["nome"], p["ss"]))
            usadas, saida = [], []
            for q in range(4):
                ch = guarda(baixo[q])
                if ch is None:
                    raise SystemExit("%s: o quadrante %d usa a paleta %d, fora "
                                     "do kit" % (p["nome"], q,
                                                 (baixo[q] >> 12) & 0xF))
                usadas.append(ch)
                saida.append(baixo[q])
        else:
            # QUADRANTE DE BAIXO SOBE quando o de cima esta vazio; quadrante
            # promovido que e PISO da fonte, ou que a fonte pinta com paleta que
            # este kit nao importa, e DESCARTADO e recebe o NOSSO chao.
            usadas, saida = [], []
            for q in range(4):
                de_baixo = branco(cima[q])
                v = baixo[q] if de_baixo else cima[q]
                if not (v & 0x3FF) or (de_baixo and eh_piso(v)):
                    usadas.append(None)
                    saida.append(0)
                    continue
                ch = guarda(v)
                usadas.append(ch)
                saida.append(v if ch is not None else 0)
            if not any(usadas):
                raise SystemExit("%s: o metatile %d nao sobrou com nenhum "
                                 "quadrante de arte" % (p["nome"], p["ss"]))
        pecas.append(dict(papel=papel, nome=p["nome"], ss=p["ss"],
                          ents=saida, usadas=usadas))

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

    # REINDEXA cada nibble para a tabela nova. A cor 0 continua 0 e nenhuma cor
    # e aproximada: a tabela de destino tem as MESMAS cores RGB da fonte, so em
    # outro indice, entao o pixel sai identico ao da ROM.
    saida_tiles = {}
    for ch, vaga in tiles_vaga.items():
        ip = int(ch.split(":")[2])
        origem = pal[ip]
        saida_tiles[ch] = [[0 if c == 0 else indice[(vaga, tuple(origem[c]))]
                            for c in linha] for linha in tiles_px[ch]]

    dados = dict(
        fonte=dict(hack=SS["hack"], autor=SS["autor"], base=SS["base"],
                   arquivo=gba, md5=md5, pri="0x%X" % SS["pri"],
                   sec="0x%X" % SS["sec"], split=list(SS["split"]),
                   n_tiles_pri=NP),
        vagas_pal={str(k): v for k, v in VAGAS_PAL.items()},
        vagas_livres={str(k): v for k, v in livres.items()},
        paletas=paletas, tiles=saida_tiles, tiles_vaga=tiles_vaga,
        piso_da_fonte={k: sorted(v) for k, v in piso.items()},
        pecas=pecas)
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


def desenha_kit():
    """(tiles_novos, metas, attrs, catalogo), sem escrever em disco."""
    dados = kit()
    por_peca = {(p["papel"], p["nome"]): p for p in dados["pecas"]}
    tiles_novos, mapa_tile = {}, {}
    proximo = [TILE_LOCAL_0]
    metas, attrs = {}, {}
    proximo_meta = [META_LOCAL_0]
    catalogo = dict(chao={}, moveis={}, blocos={}, familia={})

    def vaga(chave):
        if chave not in mapa_tile:
            if chave not in dados["tiles"]:
                raise SystemExit("o kit em disco nao tem o tile %s" % chave)
            mapa_tile[chave] = proximo[0]
            tiles_novos[proximo[0]] = dados["tiles"][chave]
            proximo[0] += 1
        return mapa_tile[chave]

    def poe(ents, attr):
        if proximo_meta[0] >= TETO_META:
            raise SystemExit("acabaram as vagas de metatile livres")
        local = proximo_meta[0]
        metas[local] = list(ents)
        attrs[local] = attr
        proximo_meta[0] += 1
        return N_META_PRI + local

    def entrada(p, q):
        """A entrada NOSSA para o quadrante q da peca: mesmo tile, vaga nova,
        vaga de paleta nova, e os bits de espelho da fonte preservados."""
        ch = p["usadas"][q]
        if ch is None:
            return None
        v = p["ents"][q]
        alvo_pal = VAGAS_PAL[int(ch.split(":")[2])]
        return ((v & 0x0C00) | (N_TILES_PRI + vaga(ch)) | (alvo_pal << 12))

    # ------------------------------------------------------ 1. CHAO NOSSO
    for qual, lista in sorted(CHAO_NOSSO.items()):
        camada = FAMILIAS[qual]["camada"]
        _b, _a, attr = carimbo_de(qual)
        for c in lista:
            arte = _arte_de_chao(c, camada)
            gid = poe(monta_chao(qual, arte), attr)
            catalogo["chao"][c["nome"]] = gid
            catalogo["familia"][c["nome"]] = qual

    # ------------------------------------------------------ 2. CHAO IMPORTADO
    for c in CHAO_SS:
        p = por_peca[("chao", c["nome"])]
        arte = [entrada(p, q) for q in range(4)]
        if any(e is None for e in arte):
            raise SystemExit("%s: quadrante vazio em peca de chao" % c["nome"])
        _b, _a, attr = carimbo_de(c["familia"])
        gid = poe(monta_chao(c["familia"], arte), attr)
        catalogo["chao"][c["nome"]] = gid
        catalogo["familia"][c["nome"]] = c["familia"]

    # ---------------------------------------------------- 3. MOVEIS de 1 celula
    def registra_movel(nome, arte, familias):
        for qual in familias:
            gid = poe(monta_movel(qual, arte), 0x1000)
            catalogo["moveis"]["%s|%s" % (nome, qual)] = gid

    for m in MOVEIS_SS:
        p = por_peca[("movel", m["nome"])]
        arte = [entrada(p, q) or 0 for q in range(4)]
        if not any(arte):
            raise SystemExit("%s: peca sem arte" % m["nome"])
        familias = (["penhasco", "praia"] if m["familia"] == "ambas"
                    else [m["familia"]])
        registra_movel(m["nome"], arte, familias)
    for m in MOVEIS_NOSSOS:
        ents = _ents_nosso(m["mt"])
        arte = ents[4:]
        if not any(v & 0x3FF for v in arte):
            raise SystemExit("o metatile %d nao tem arte na camada de cima"
                             % m["mt"])
        if _opacos_de(arte) >= 4 * 64:
            raise SystemExit("o metatile %d tem a camada de cima 100%% opaca e "
                             "por isso e tapete, nao movel" % m["mt"])
        registra_movel(m["nome"], arte, [m["familia"]])

    # ------------------------------------------------- 4. BLOCOS de N linhas
    for b in BLOCOS_SS:
        qual = b["familia"]
        if FAMILIAS[qual]["camada"] != 0:
            raise SystemExit("%s: bloco so entra em familia de layerType NORMAL"
                             % b["nome"])
        _bb, _aa, attr = carimbo_de(qual)
        grade = []
        for li, linha in enumerate(b["linhas"]):
            ultima = li == len(b["linhas"]) - 1
            fora = []
            for k, _loc in enumerate(linha):
                p = por_peca[("movel", "%s L%d C%d" % (b["nome"], li, k))]
                arte = [entrada(p, q) or 0 for q in range(4)]
                if not any(arte):
                    raise SystemExit("%s: linha %d sem arte" % (b["nome"], li))
                fora.append(poe(monta_movel(qual, arte),
                                0x1000 if ultima else attr))
            grade.append(fora)
        catalogo["blocos"][b["nome"]] = dict(linhas=grade, familia=qual)
        catalogo["familia"][b["nome"]] = qual

    if proximo[0] > TETO_TILES:
        raise SystemExit("o kit estoura o teto de %d tiles (%d)"
                         % (TETO_TILES, proximo[0]))

    # A vaga de metatile so serve se NENHUM dos cinco mapas vivos usar o id. A
    # grade do ALVO entra pela base LIMPA desta passada, e nao pelo disco:
    # depois de um `--aplicar` o disco ja tem os ids que este kit acabou de
    # escrever, e o portao reprovaria a si mesmo na segunda rodada.
    guardado = carrega_plano()
    usados = set()
    for nome in IRMAOS:
        grade = base_de(nome, guardado) if nome == ALVO else G.grade(nome)[4]
        usados |= {c & 0x3FF for c in grade}
    for local in metas:
        if N_META_PRI + local in usados:
            raise SystemExit("algum dos cinco mapas usa o metatile %d"
                             % (N_META_PRI + local))
        if local < META_LOCAL_0:
            raise SystemExit("o local %d esta abaixo do primeiro livre" % local)
    return tiles_novos, metas, attrs, catalogo


def grava_tileset(tiles_novos, metas, attrs):
    """Escreve tiles.png, palettes/*.pal, metatiles.bin e metatile_attributes.bin.

    Idempotente: as vagas de tile, de paleta e de metatile sao FIXAS.
    """
    from PIL import Image
    dados = kit()
    antigo = Image.open(f"{DESTINO}/tiles.png")
    cols = antigo.size[0] // 8
    alvo = max(TILE_LOCAL_0 + len(tiles_novos), (antigo.size[1] // 8) * cols)
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

    fim = max(metas) + 1 if metas else META_LOCAL_0
    meta = bytearray(_ler("metatiles.bin"))
    attr = bytearray(_ler("metatile_attributes.bin"))
    meta.extend(b"\0" * max(0, fim * 16 - len(meta)))
    attr.extend(b"\0" * max(0, fim * 2 - len(attr)))
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
                # vontade de crescer: o penhasco de Cianwood tem braços de duas
                # celulas de largura e exigir o tamanho cheio deixaria o braco
                # liso. O piso de PISO_BOLHA existe para que "mancha" continue
                # querendo dizer mancha.
                if len(corpo) < lo and (frente or len(corpo) < PISO_BOLHA):
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


def peca_da_mancha(nomes, x, y):
    """Qual das pecas do grupo cai nesta celula. Hash da posicao, nao paridade:
    paridade vira xadrez e o auto-teste reprova."""
    return nomes[_mistura(x, y, 0xA5A5 + len(nomes)) % len(nomes)]


# ----------------------------------------------------------- ligacao a pe
def componentes(v, W, H):
    """{celula: rotulo} dos pedacos de chao andavel ligados a pe.

    POR QUE NAO BASTA O `enfeita_cidades.alcance`: aquele mede "quem ainda e
    alcancavel a partir de algum ponto de partida", e ponto de partida ali e warp
    OU OBJETO. Em Cianwood isso e decisivo, e nao teorico: o penhasco oeste tem
    cinco objetos dentro e por isso a conta de alcance o da por alcancado, mesmo
    ele sendo um pedaco SEPARADO em que o jogador nunca pisa.
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
    """(L, W, H, v, escritas, contas) do mapa alvo."""
    d, L, W, H, v0 = G.grade(ALVO)
    v = list(base) if base is not None else list(v0)
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()

    # As duas FAMILIAS de chao. Uma celula so e elegivel se ela ainda for o
    # carimbo puro, se for andavel e se nao for agua para o motor.
    #
    # A ELEVACAO NAO FILTRA, e essa e uma diferenca deliberada em relacao ao
    # `costa_sandgem.py`, com numero: o penhasco de Cianwood tem 354 celulas na
    # elevacao 4 e 137 na 0, e cortar pela elevacao dominante deixaria 137
    # celulas de tapete de fora, o que sozinho impedia a regua de fechar (28,2%
    # medidos na primeira rodada deste script). Repintar chao NAO mexe em
    # elevacao (a palavra so troca os dez bits de metatile) e solidificar
    # preserva os quatro bits altos, entao o filtro nao protegia nada aqui. O
    # portao que protege de verdade continua sendo o de LIGACAO a pe, que ja
    # recusa juntar dois pedacos de elevacao diferente.
    # `fam` e o que a MANCHA pode pintar e `fam_andavel` e o que o MOVEL pode
    # ocupar: no penhasco os dois nao sao a mesma coisa, porque a mancha tambem
    # pinta celula solida e movel so existe em celula andavel (ele e uma
    # solidificacao 0 -> 1).
    fam, fam_andavel, elev = {}, {}, {}
    for qual, f in FAMILIAS.items():
        mt = f["carimbo"]
        alvos = [c for c in v if (c & 0x3FF) == mt and not ((c >> 10) & 3)]
        elev[qual] = (collections.Counter((c >> 12) & 0xF
                                          for c in alvos).most_common(1)[0][0]
                      if alvos else None)
        fam_andavel[qual] = {(i % W, i // W) for i in range(W * H)
                             if not ((v[i] >> 10) & 3) and (v[i] & 0x3FF) == mt
                             and beh(v[i] & 0x3FF) not in AG}
        fam[qual] = set(fam_andavel[qual])
        if f["solidos"]:
            fam[qual] |= {(i % W, i // W) for i in range(W * H)
                          if ((v[i] >> 10) & 3) and (v[i] & 0x3FF) == mt}

    escritas = {}
    ev, gelo = E.congelado(d)
    gelo |= E.corredores_de_teste(ALVO, v, W, H, d)
    for idx, _a, _n in E.carrega_plano().get(ALVO, {}).get("celulas", []):
        gelo.add((idx % W, idx // W))

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

    def livre(x, y, qual):
        i = y * W + x
        if x < MARGEM or y < MARGEM or x >= W - MARGEM or y >= H - MARGEM:
            return False
        if (x, y) in gelo or i in escritas or (x, y) not in fam_andavel[qual]:
            return False
        return (aplicado[i] & 0x3FF) == FAMILIAS[qual]["carimbo"]

    def espacado(nome, esp, x, y):
        if any(max(abs(x - px), abs(y - py)) < ESPACO_ENTRE_MOVEIS
               for px, py in postos):
            return False
        return not any(max(abs(x - px), abs(y - py)) < esp
                       for px, py in por_movel[nome])

    def tenta_solidificar(x, y, mt_id):
        """Solidifica (x,y) e devolve True se os DOIS portoes deixarem."""
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

    # ------ 1. BLOCOS, antes da mobilia de uma celula, porque eles precisam de
    # um retangulo inteiro e a mobilia solta nao pode ter comido metade dele. As
    # linhas de CIMA continuam ANDAVEIS e por isso nao entram no portao de
    # alcance; a de BAIXO vira solida.
    conta_bloco = collections.Counter()
    por_bloco = []
    for b in TEMA["blocos"]:
        info = catalogo["blocos"][b["nome"]]
        qual = info["familia"]
        alt = len(info["linhas"])
        larg = len(info["linhas"][0])
        for x, y in ordem_cel:
            if conta_bloco[b["nome"]] >= b["quantos"]:
                break
            if b.get("faixa") == "sul" and y < H // 2:
                continue
            cels = [(x + cx, y + cy) for cy in range(alt) for cx in range(larg)]
            if any(not livre(cx, cy, qual) for cx, cy in cels):
                continue
            if any(max(abs(x - px), abs(y - py)) < b["espaco"]
                   for px, py in por_bloco):
                continue
            if any(max(abs(cx - px), abs(cy - py)) < ESPACO_ENTRE_MOVEIS
                   for cx, cy in cels for px, py in postos):
                continue
            topo = [(x + cx, y + cy) for cy in range(alt - 1) for cx in range(larg)]
            for cy in range(alt - 1):
                for cx in range(larg):
                    j = (y + cy) * W + x + cx
                    escritas[j] = (aplicado[j] & 0xFC00) | info["linhas"][cy][cx]
                    aplicado[j] = escritas[j]
            ok = True
            for cx in range(larg):
                if not tenta_solidificar(x + cx, y + alt - 1,
                                         info["linhas"][alt - 1][cx]):
                    ok = False
                    break
            if not ok:
                for cx, cy in cels:
                    j = cy * W + cx
                    if (cx, cy) in novos_solidos:
                        novos_solidos.remove((cx, cy))
                        postos.remove((cx, cy))
                    if j in escritas:
                        del escritas[j]
                    aplicado[j] = v[j]
                continue
            por_bloco += cels
            postos += topo
            conta_bloco[b["nome"]] += 1

    # ------ 2. MOVEIS de uma celula. Eles vem ANTES da mancha de proposito, e a
    # razao esta medida em Snowpoint: movel posto no carimbo tira uma celula do
    # numerador E do denominador da regua; movel posto em cima de uma mancha tira
    # so do denominador, o que PIORA a conta.
    lista = TEMA["moveis"]
    for x, y in ordem_cel:
        giro = ((x * 73856093) ^ (y * 19349663)) % len(lista)
        for k in range(len(lista)):
            m = lista[(giro + k) % len(lista)]
            chave = "%s|%s" % (m["nome"], m["familia"])
            if conta_mov[chave] >= m["quantos"]:
                continue
            qual = m["familia"]
            if not livre(x, y, qual) or not espacado(chave, m["espaco"], x, y):
                continue
            # movel de cidade encosta em alguma coisa: ou num solido, ou na OUTRA
            # familia de chao. Peca solta no meio do vazio le como erro de mapa.
            perto = any(0 <= x + dx < W and 0 <= y + dy < H
                        and (((aplicado[(y + dy) * W + x + dx] >> 10) & 3)
                             or (x + dx, y + dy) not in fam_andavel[qual])
                        for dx, dy in N4)
            if not perto:
                continue
            if not tenta_solidificar(x, y, catalogo["moveis"][chave]):
                continue
            por_movel[chave].append((x, y))
            conta_mov[chave] += 1
            break

    # ------------------------------------------------------------- 3. MANCHA
    conta_mancha = collections.Counter()

    def pintavel(p, qual):
        i = p[1] * W + p[0]
        return (p in fam[qual] and i not in escritas
                and (aplicado[i] & 0x3FF) == FAMILIAS[qual]["carimbo"]
                and MARGEM <= p[0] < W - MARGEM and MARGEM <= p[1] < H - MARGEM
                and p not in gelo)

    def pinta(p, nomes):
        i = p[1] * W + p[0]
        nome = peca_da_mancha(nomes, p[0], p[1])
        escritas[i] = (aplicado[i] & 0xFC00) | catalogo["chao"][nome]
        aplicado[i] = escritas[i]
        conta_mancha[nome] += 1

    pintaveis = {}
    for qual, semente in (("penhasco", 0x5EED), ("praia", 0xB0A7)):
        livres = {p for p in fam[qual] if pintavel(p, qual)}
        pintaveis[qual] = len(livres)
        for nomes, corpo in bolhas(livres, TEMA["bolhas"][qual], semente):
            for p in sorted(corpo):
                pinta(p, nomes)

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
    contas = dict(moveis=dict(conta_mov), blocos=dict(conta_bloco),
                  manchas=dict(conta_mancha), solidos=len(novos_solidos),
                  familias={q: len(fam[q]) for q in fam}, pintaveis=pintaveis,
                  andaveis={q: len(fam_andavel[q]) for q in fam_andavel})
    return L, W, H, v, escritas, contas


def regua(v, W, H, L, escritas=None):
    """(carimbo dominante em %, celulas andaveis a pe, id do carimbo), como a
    `regua_cidades.py` conta, com o MESMO corte de 512 que ela usa."""
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
    """A grade como esta no disco, so tirando o que ESTA passada escreveu."""
    v = list(G.grade(alvo)[4])
    for idx, antigo, novo in guardado.get(alvo, {}).get("celulas", []):
        if v[idx] == novo:
            v[idx] = antigo
    return v


def roda(aplicar):
    tiles_novos, metas, attrs, catalogo = desenha_kit()
    print("kit: %d tiles novos (vagas %d a %d de %d, sobram %d), %d metatiles "
          "novos (locais %d a %d, ids %d a %d de %d)"
          % (len(tiles_novos), min(tiles_novos), max(tiles_novos), TETO_TILES,
             TETO_TILES - max(tiles_novos) - 1, len(metas), min(metas),
             max(metas), N_META_PRI + min(metas), N_META_PRI + max(metas),
             TETO_META))
    if aplicar:
        grava_tileset(tiles_novos, metas, attrs)
    guardado = carrega_plano()
    base = base_de(ALVO, guardado)
    L, W, H, v, escritas, contas = plano_mapa(catalogo, base)
    a, na, ida = regua(v, W, H, L)
    b, nb, idb = regua(v, W, H, L, escritas)
    print("%s: %d celulas de mancha, %d solidificadas, %d mudadas (familia %s)"
          % (ALVO, sum(contas["manchas"].values()), contas["solidos"],
             len(escritas), contas["familias"]))
    print("  mancha: " + ", ".join("%s x%d" % kv
                                   for kv in sorted(contas["manchas"].items())))
    print("  movel:  " + ", ".join("%s x%d" % kv
                                   for kv in sorted(contas["moveis"].items())))
    print("  bloco:  " + ", ".join("%s x%d" % kv
                                   for kv in sorted(contas["blocos"].items())))
    print("  regua: carimbo %d com %.1f%% de %d celulas ANTES; carimbo %d com "
          "%.1f%% de %d DEPOIS" % (ida, a, na, idb, b, nb))
    if aplicar:
        saida = list(v)
        for i, val in escritas.items():
            saida[i] = val
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


# ------------------------------------------------------------------ conferencia
def _opacos(px):
    return sum(1 for linha in px for c in linha if c)


def confere(tiles_novos, metas, attrs, catalogo, plano):
    """Todas as regras desta onda, medidas sobre os dados que vierem.

    Ela e chamada DUAS vezes pelo auto-teste: uma com o plano de verdade, que tem
    que sair sem queixa, e uma por sabotagem, que tem que sair com a queixa
    certa. Regra conferida so no caminho feliz nao e regra.
    """
    mau = []
    dados = kit()
    import render_maps as RM
    tp = _tileset(PRIMARIO)
    ts = _tileset(SECUNDARIO)

    def atributo(mt_id):
        """Atributo de um metatile, com o kit desta rodada valendo por cima."""
        if mt_id >= N_META_PRI:
            local = mt_id - N_META_PRI
            if local in attrs:
                return attrs[local]
        return _attr_nosso(mt_id)

    def entradas(mt_id):
        if mt_id >= N_META_PRI and (mt_id - N_META_PRI) in metas:
            return list(metas[mt_id - N_META_PRI])
        return _ents_nosso(mt_id)

    def px_de(mt_id):
        """Os 256 pixels RGB do metatile, com o kit desta rodada valendo."""
        from PIL import Image
        im = Image.new("RGB", (16, 16), tp["paletas"][0][0])
        p = im.load()
        ent = entradas(mt_id)
        for cam in (0, 1):
            for q in range(4):
                val = ent[cam * 4 + q]
                idx, ip = val & 0x3FF, (val >> 12) & 0xF
                if not idx:
                    continue
                vaga = idx - N_TILES_PRI
                tile = (tiles_novos[vaga] if vaga in tiles_novos
                        else RM.resolver_tile(tp, ts, idx))
                if tile is None:
                    continue
                cores = (dados["paletas"].get(str(ip))
                         or (tp if ip < N_PAL_PRI else ts)["paletas"].get(ip))
                if cores is None:
                    continue
                RM.desenhar_tile(p, (q % 2) * 8, (q // 2) * 8, tile,
                                 [tuple(c) for c in cores],
                                 bool(val & 0x400), bool(val & 0x800))
        return list(im.get_flattened_data())

    def opacos_da_camada(mt_id, cam):
        tot = 0
        for e in entradas(mt_id)[cam * 4:cam * 4 + 4]:
            idx = e & 0x3FF
            if not idx:
                continue
            vaga = idx - N_TILES_PRI
            tile = (tiles_novos[vaga] if vaga in tiles_novos
                    else RM.resolver_tile(tp, ts, idx))
            tot += _opacos(tile) if tile else 0
        return tot

    # ------------------------------------------------------------ 1. orcamento
    if tiles_novos and max(tiles_novos) >= TETO_TILES:
        mau.append("estoura o teto de %d tiles" % TETO_TILES)
    if metas and max(metas) >= TETO_META:
        mau.append("estoura o teto de %d metatiles" % TETO_META)
    for local in metas:
        if local < META_LOCAL_0:
            mau.append("o metatile %d esta abaixo do primeiro local livre"
                       % (N_META_PRI + local))
    livres = dados["vagas_livres"]
    for vaga, cores in sorted(dados["paletas"].items()):
        if not N_PAL_PRI <= int(vaga) <= 12:
            mau.append("a vaga %s nao e de secundario" % vaga)
        antigo = ts["paletas"][int(vaga)]
        vagos = set(livres.get(vaga) or [])
        for i in range(1, 16):
            if tuple(cores[i]) != tuple(antigo[i]) and i not in vagos:
                mau.append("a vaga %s mudou a cor do indice %d, que algum pixel "
                           "nosso usa" % (vaga, i))

    # ---------- 2. o kit nao pode importar paleta de origem fora de VAGAS_PAL
    for ch in dados["tiles"]:
        ip = int(ch.split(":")[2])
        if ip not in VAGAS_PAL:
            mau.append("o kit importou a paleta %d da fonte, fora do plano" % ip)

    # -------- 3. CHAO novo: atributo IGUAL ao do carimbo da familia, montagem na
    #            camada certa e, na praia, camada de cima VAZIA
    for nome, gid in catalogo["chao"].items():
        qual = catalogo["familia"][nome]
        base, _arte, attr_chao = carimbo_de(qual)
        if atributo(gid) != attr_chao:
            mau.append("o chao %s (%d) tem atributo 0x%04X e o carimbo de %s tem "
                       "0x%04X" % (nome, gid, atributo(gid), qual, attr_chao))
        ent = entradas(gid)
        cam = FAMILIAS[qual]["camada"]
        if ent[(1 - cam) * 4:(1 - cam) * 4 + 4] != list(base):
            mau.append("o chao %s (%d) nao esta assentado sobre a base do "
                       "carimbo de %s" % (nome, gid, qual))
        if cam == 0 and any(e & 0x3FF for e in ent[4:]):
            mau.append("o chao %s (%d) da praia usa a camada de cima, que com "
                       "layerType NORMAL desenha ACIMA do jogador" % (nome, gid))
        if any(not (e & 0x3FF) for e in ent[cam * 4:cam * 4 + 4]):
            mau.append("o chao %s (%d) tem quadrante vazio" % (nome, gid))

    # ------- 4. MOVEL e ULTIMA LINHA de bloco: COVERED, comportamento zerado, e
    #            o chao VISIVEL da familia na camada de baixo
    ids_base = {}
    for nome, info in catalogo["blocos"].items():
        for gid in info["linhas"][-1]:
            ids_base[gid] = nome
    for gid, nome in list((g, n) for n, g in catalogo["moveis"].items()) \
            + list(ids_base.items()):
        qual = (catalogo["familia"][nome] if nome in catalogo["familia"]
                else nome.split("|")[-1])
        a = atributo(gid)
        if (a >> 12) & 0xF != 1:
            mau.append("o movel %s (%d) nao esta em COVERED" % (nome, gid))
        if a & 0xFF:
            mau.append("o movel %s (%d) importou comportamento 0x%02X da fonte"
                       % (nome, gid, a & 0xFF))
        if entradas(gid)[:4] != piso_visivel(qual):
            mau.append("o movel %s (%d) nao tem o nosso chao de %s na camada de "
                       "baixo" % (nome, gid, qual))
        if opacos_da_camada(gid, 1) >= 4 * 64:
            mau.append("o movel %s (%d) tem a camada de cima cheia: e tapete, "
                       "nao peca" % (nome, gid))

    # ---- 5. LINHAS DE CIMA de bloco: continuam ANDAVEIS com o atributo do
    #        carimbo, e a arte delas NAO pode ser 100% opaca (defeito E3)
    for nome, info in catalogo["blocos"].items():
        qual = info["familia"]
        base, _arte, attr_chao = carimbo_de(qual)
        for linha in info["linhas"][:-1]:
            for gid in linha:
                if atributo(gid) != attr_chao:
                    mau.append("a linha de cima do bloco %s (%d) nao herdou o "
                               "atributo do chao" % (nome, gid))
                if entradas(gid)[:4] != piso_visivel(qual):
                    mau.append("a linha de cima do bloco %s (%d) nao tem o nosso "
                               "chao embaixo" % (nome, gid))
                if opacos_da_camada(gid, 1) >= 4 * 64:
                    mau.append("a linha de cima do bloco %s (%d) tapa o jogador "
                               "inteiro (E3)" % (nome, gid))

    # ---------- 6. nenhuma variante de chao e copia pixel a pixel de outra
    for qual in FAMILIAS:
        lista = [g for n, g in catalogo["chao"].items()
                 if catalogo["familia"][n] == qual] + [FAMILIAS[qual]["carimbo"]]
        pix = {mt: px_de(mt) for mt in lista}
        for i, a in enumerate(lista):
            for b in lista[i + 1:]:
                dd = sum(sum((x - y) ** 2 for x, y in zip(p, q)) ** 0.5
                         for p, q in zip(pix[a], pix[b])) / 256.0
                if dd < PISO_DIST:
                    mau.append("as variantes de chao %d e %d de %s tem distancia "
                               "%.1f, abaixo do piso de %.1f: isso e enganar a "
                               "regua" % (a, b, qual, dd, PISO_DIST))

    # -------------------------------------------- 7 a 13. o plano, celula a celula
    L, W, H, v, escritas, contas = plano
    d = json.load(open(f"{RAIZ}/data/maps/{ALVO}/map.json"))
    ev = E.eventos(d)
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val
    meus_chaos = {catalogo["chao"][n]: n for n in catalogo["chao"]}
    meus_moveis = {catalogo["moveis"][n]: n for n in catalogo["moveis"]}
    meus_topos = {t: n for n, b in catalogo["blocos"].items()
                  for linha in b["linhas"][:-1] for t in linha}
    meus_bases = {t: n for n, b in catalogo["blocos"].items()
                  for t in b["linhas"][-1]}
    carimbo_do = {}
    for gid, nome in meus_chaos.items():
        carimbo_do[gid] = FAMILIAS[catalogo["familia"][nome]]["carimbo"]
    for gid, nome in meus_moveis.items():
        carimbo_do[gid] = FAMILIAS[nome.split("|")[-1]]["carimbo"]
    for gid, nome in list(meus_topos.items()) + list(meus_bases.items()):
        carimbo_do[gid] = FAMILIAS[catalogo["blocos"][nome]["familia"]]["carimbo"]

    for i, val in escritas.items():
        x, y = i % W, i // W
        novo, velho = val & 0x3FF, v[i] & 0x3FF
        cn, cv = (val >> 10) & 3, (v[i] >> 10) & 3
        if (val >> 12) & 0xF != (v[i] >> 12) & 0xF:
            mau.append("%s: mudou ELEVACAO em (%d,%d)" % (ALVO, x, y))
        if cv and not cn:
            mau.append("%s: colisao 1 -> 0 em (%d,%d), que segue proibida"
                       % (ALVO, x, y))
        if novo not in carimbo_do:
            mau.append("%s: metatile %d escrito em (%d,%d) e de fora do kit"
                       % (ALVO, novo, x, y))
            continue
        if velho != carimbo_do[novo]:
            mau.append("%s: peca fora do carimbo dela em (%d,%d)" % (ALVO, x, y))
        if novo in meus_chaos or novo in meus_topos:
            if cn != cv:
                mau.append("%s: chao/topo mudou colisao em (%d,%d)" % (ALVO, x, y))
        else:
            if cv or not cn:
                mau.append("%s: movel em (%d,%d) nao e solidificacao 0 -> 1"
                           % (ALVO, x, y))
            if (x, y) in ev:
                mau.append("%s: movel em cima do evento (%d,%d)" % (ALVO, x, y))

    # 8. (comportamento, layerType) de toda celula ANDAVEL fica igual
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

    # 11. A MANCHA NAO PODE SER ADIVINHAVEL, e o teste tem dois lados.
    #  (a) PADRAO: nenhuma projecao simples da posicao pode ADIVINHAR a peca.
    #  (b) FORMA: mancha e BOLHA, nao sal e pimenta, e a conta e o TAMANHO MEDIO
    #      do pedaco conexo.
    for qual in FAMILIAS:
        meus = {g for g, n in meus_chaos.items()
                if catalogo["familia"][n] == qual}
        mancha = {(i % W, i // W): (val & 0x3FF) for i, val in escritas.items()
                  if (val & 0x3FF) in meus}
        # O PISO DE MANCHA E RELATIVO, e o motivo esta medido. `CianwoodCity` tem
        # 39 eventos (27 objetos, 7 warps, 4 placas e 1 coord_event), e a orla de
        # uma celula em volta deles congela 306 celulas do mapa; somando os
        # corredores da suite e a margem da borda, das 236 celulas de areia so
        # 127 podem ser pintadas. Um piso absoluto de 100 celulas seria
        # impossivel de cumprir sem quebrar a orla dos eventos, e piso que so se
        # cumpre quebrando outra regra nao e portao, e armadilha.
        podem = contas.get("pintaveis", {}).get(qual, 0)
        if podem and len(mancha) < 0.40 * podem:
            mau.append("%s: a mancha de %s cobre so %d de %d celulas pintaveis "
                       "(%.0f%%), abaixo do piso de 40%%"
                       % (ALVO, qual, len(mancha), podem, 100.0 * len(mancha) / podem))
        if not mancha:
            continue
        tot = len(mancha)
        cego = collections.Counter(mancha.values()).most_common(1)[0][1] / tot

        def melhor_ganho(rotulos):
            """O maior ganho sobre o chute cego em toda a grade de eixo x modulo."""
            fora = (0.0, "", 0, 0.0)
            for rot, eixo in (("x", lambda p: p[0]), ("y", lambda p: p[1]),
                              ("x+y", lambda p: p[0] + p[1]),
                              ("x-y", lambda p: p[0] - p[1])):
                for mod in range(2, 9):
                    tab = collections.defaultdict(collections.Counter)
                    for p, mt_id in rotulos.items():
                        tab[eixo(p) % mod][mt_id] += 1
                    ac = sum(c.most_common(1)[0][1] for c in tab.values()) / tot
                    if ac - cego > fora[0]:
                        fora = (ac - cego, rot, mod, ac)
            return fora

        # O CORTE E CALIBRADO CONTRA O NULO, e nao cravado em 0,12. Com 57
        # celulas e modulo 8 cada classe fica com sete celulas, e a "peca mais
        # comum da classe" acerta bem acima do chute cego SO POR RUIDO: medido,
        # o proprio embaralhamento das mesmas pecas nas mesmas celulas passa dos
        # 12 pontos. Entao o teto e o maior ganho que VINTE embaralhamentos
        # deterministicos conseguem, mais uma folga de 3 pontos, e nunca menos
        # que os 12 pontos das passadas anteriores.
        chaves = sorted(mancha)
        valores = [mancha[p] for p in chaves]
        teto_nulo = 0.0
        for semente in range(20):
            baralho = sorted(range(len(chaves)),
                             key=lambda i: _mistura(i, semente, 0xDECAF))
            embaralhado = {chaves[i]: valores[baralho[i]]
                           for i in range(len(chaves))}
            teto_nulo = max(teto_nulo, melhor_ganho(embaralhado)[0])
        corte = max(0.12, teto_nulo + 0.03)
        ganho, rot, mod, ac = melhor_ganho(mancha)
        if ganho > corte:
            mau.append("%s: em %s, saber %s mod %d adivinha a peca em %.0f%% das "
                       "celulas contra %.0f%% do chute cego, ganho de %.0f pontos "
                       "acima do corte de %.0f: virou padrao"
                       % (ALVO, qual, rot, mod, 100 * ac, 100 * cego,
                          100 * ganho, 100 * corte))
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
        if len(mancha) / pedacos < 12.0:
            mau.append("%s: a mancha de %s tem so %.1f celulas por pedaco (%d em "
                       "%d): virou sal e pimenta, nao bolha"
                       % (ALVO, qual, len(mancha) / pedacos, len(mancha), pedacos))

    # 12. a regua tem que fechar em 20% ou menos
    b, nb, idb = regua(v, W, H, L, escritas)
    if b > TETO_REGUA:
        mau.append("%s: a regua ainda marca %.1f%% de carimbo dominante"
                   % (ALVO, b))

    # 13. o bloco: toda ULTIMA LINHA tem as de cima logo acima, e as contas batem
    bases = [(i % W, i // W) for i, val in escritas.items()
             if (val & 0x3FF) in meus_bases]
    topos = {(i % W, i // W) for i, val in escritas.items()
             if (val & 0x3FF) in meus_topos}
    esperados = 0
    for nome, info in catalogo["blocos"].items():
        n = contas["blocos"].get(nome, 0)
        esperados += n * (len(info["linhas"]) - 1) * len(info["linhas"][0])
    if len(topos) != esperados:
        mau.append("%s: %d celulas de topo de bloco e %d esperadas"
                   % (ALVO, len(topos), esperados))
    for x, y in bases:
        if (x, y - 1) not in topos:
            mau.append("%s: a base de bloco em (%d,%d) esta sem topo"
                       % (ALVO, x, y))
            break
    return mau


# ------------------------------------------------------------------ auto-teste
def demo():
    """Prova positiva e as provas NEGATIVAS, cada sabotagem revertida em seguida."""
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
                (L, W, H, list(v), dict(esc), json.loads(json.dumps(ct))))

    # N1. colisao 1 -> 0 numa celula de mancha
    def n1():
        """A celula tem que ser de MANCHA, e nao de movel.

        Numa celula de movel a colisao DEPOIS ja e 1, entao dizer que a de ANTES
        tambem era nao produz a transicao 1 -> 0 e a sabotagem passava despercebida
        (o que acusava era a regra do movel, que e outra). Medido na primeira
        rodada do auto-teste.
        """
        a = copia()
        L, W, H, v, esc, ct = a[4]
        i = next(j for j in sorted(esc) if not ((esc[j] >> 10) & 3))
        v[i] = v[i] | (1 << 10)          # a celula ERA solida
        return a
    sabota("colisao 1 -> 0", n1, "colisao 1 -> 0")

    # N2. elevacao alterada
    def n2():
        a = copia()
        L, W, H, v, esc, ct = a[4]
        i = sorted(esc)[0]
        esc[i] = (esc[i] & 0x0FFF) | (((v[i] >> 12) + 1) & 0xF) << 12
        return a
    sabota("elevacao alterada", n2, "mudou ELEVACAO")

    # N3. comportamento de um metatile de CHAO sabotado
    def n3():
        a = copia()
        gid = a[3]["chao"][CHAO_NOSSO["praia"][0]["nome"]]
        a[2][gid - N_META_PRI] = (a[2][gid - N_META_PRI] & 0xFF00) | 0x02
        return a
    sabota("behavior de chao sabotado", n3, "tem atributo")

    # N4. layerType NORMAL onde devia ser COVERED
    def n4():
        a = copia()
        gid = sorted(a[3]["moveis"].values())[0]
        a[2][gid - N_META_PRI] = a[2][gid - N_META_PRI] & 0x0FFF
        return a
    sabota("layerType NORMAL no movel", n4, "nao esta em COVERED")

    # N5. linha de cima de bloco apagada, deixando a base sozinha
    def n5():
        a = copia()
        L, W, H, v, esc, ct = a[4]
        topos = {t for b in catalogo["blocos"].values()
                 for linha in b["linhas"][:-1] for t in linha}
        for i in sorted(esc):
            if (esc[i] & 0x3FF) in topos:
                del esc[i]
                break
        return a
    sabota("linha de cima de bloco apagada", n5, "celulas de topo de bloco")

    # N6. camada de BAIXO de um movel sabotada (chao da OUTRA familia)
    def n6():
        a = copia()
        gid = a[3]["moveis"]["pedra grande|praia"]
        ent = list(a[1][gid - N_META_PRI])
        a[1][gid - N_META_PRI] = piso_visivel("penhasco") + ent[4:]
        return a
    sabota("movel de praia com chao de penhasco", n6,
           "nao tem o nosso chao de praia")

    # N7. peca de PENHASCO com a montagem da praia (arte na camada errada)
    def n7():
        a = copia()
        gid = a[3]["chao"][CHAO_NOSSO["penhasco"][0]["nome"]]
        ent = list(a[1][gid - N_META_PRI])
        a[1][gid - N_META_PRI] = ent[4:] + ent[:4]
        return a
    sabota("chao de penhasco com a camada trocada", n7,
           "nao esta assentado sobre a base")

    # N8. mancha escolhida por (x + y) % n, que e xadrez com periodo
    def n8():
        a = copia()
        original = globals()["peca_da_mancha"]
        globals()["peca_da_mancha"] = lambda nomes, x, y: nomes[(x + y) % len(nomes)]
        try:
            a = (a[0], a[1], a[2], a[3],
                 plano_mapa(catalogo, base_de(ALVO, guardado)))
        finally:
            globals()["peca_da_mancha"] = original
        return a
    sabota("mancha por (x+y) % n", n8, "virou padrao")

    # N9. mancha escolhida por x % n
    def n9():
        a = copia()
        original = globals()["peca_da_mancha"]
        globals()["peca_da_mancha"] = lambda nomes, x, y: nomes[x % len(nomes)]
        try:
            a = (a[0], a[1], a[2], a[3],
                 plano_mapa(catalogo, base_de(ALVO, guardado)))
        finally:
            globals()["peca_da_mancha"] = original
        return a
    sabota("mancha por x % n", n9, "virou padrao")

    # N10. corredor fechado que PARTE um pedaco de chao. O portao de alcance
    #      sozinho nao pega isso quando ha objeto dos dois lados, e em Cianwood
    #      isso nao e teoria: o penhasco oeste tem cinco objetos dentro.
    def n10():
        a = copia()
        L, W, H, v, esc, ct = a[4]
        final = list(v)
        for j, val in esc.items():
            final[j] = val
        antes = componentes(final, W, H)
        for y in range(H):
            for x in range(W):
                i = y * W + x
                if (final[i] >> 10) & 3:
                    continue
                teste = list(final)
                teste[i] = (final[i] & 0xF000) | (1 << 10) | (final[i] & 0x3FF)
                if ligacao_intacta(antes, componentes(teste, W, H), {(x, y)}):
                    esc[i] = teste[i]
                    return a
        raise SystemExit("nao achei ponto de articulacao para a sabotagem N10")
    sabota("corredor fechado", n10, "se partiu")

    # N11. duas variantes de chao IGUAIS pixel a pixel: e enganar a regua
    def n11():
        a = copia()
        nomes = [c["nome"] for c in CHAO_NOSSO["penhasco"]]
        alvo = a[3]["chao"][nomes[1]] - N_META_PRI
        a[1][alvo] = list(a[1][a[3]["chao"][nomes[0]] - N_META_PRI])
        return a
    sabota("variante de chao duplicada", n11, "abaixo do piso de")

    # N12. cor nova escrita num indice que os NOSSOS pixels ja usam. As duas
    #      vagas deste kit (7 e 10) estao 100% livres, entao a sabotagem precisa
    #      escolher uma vaga com indice ocupado e reescrever o kit NO DISCO.
    def n12():
        a = copia()
        dados = kit()
        alvo_vaga = None
        for vaga in range(N_PAL_PRI, 13):
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

    # N13. gravar num metatile ABAIXO do primeiro local livre, ou seja num que
    #      algum dos cinco mapas pode estar desenhando
    def n13():
        a = copia()
        local = META_LOCAL_0 - 1
        a[1][local] = list(a[1][min(a[1])])
        a[2][local] = 0x1000
        return a
    sabota("grava em metatile ja definido", n13,
           "abaixo do primeiro local livre")

    # N14. chao da PRAIA com arte na camada de cima. Com layerType NORMAL isso
    #      desenha ACIMA do jogador, e e o defeito que a familia praia existe
    #      para nao ter.
    def n14():
        a = copia()
        gid = a[3]["chao"][CHAO_NOSSO["praia"][0]["nome"]]
        ent = list(a[1][gid - N_META_PRI])
        a[1][gid - N_META_PRI] = ent[:4] + ent[:4]
        return a
    sabota("chao de praia com camada de cima", n14, "usa a camada de cima")

    # N15. copa de coqueiro 100% opaca: o jogador some embaixo dela (E3)
    def n15():
        a = copia()
        gid = a[3]["blocos"]["coqueiro"]["linhas"][0][0]
        cheio = [[15] * 8 for _ in range(8)]
        for e in a[1][gid - N_META_PRI][4:]:
            if e & 0x3FF:
                a[0][(e & 0x3FF) - N_TILES_PRI] = cheio
        ent = list(a[1][gid - N_META_PRI])
        primeiro = next(e for e in ent[4:] if e & 0x3FF)
        a[1][gid - N_META_PRI] = ent[:4] + [primeiro] * 4
        return a
    sabota("copa de coqueiro opaca", n15, "tapa o jogador inteiro (E3)")

    # ------------------------------------------------ o que esta NO DISCO
    from PIL import Image
    meta_disco = _ler("metatiles.bin")
    attr_disco = _ler("metatile_attributes.bin")
    png = Image.open(f"{DESTINO}/tiles.png")
    cols = png.size[0] // 8
    px = png.convert("P").load()

    postas = [l for l in metas
              if l * 16 + 16 <= len(meta_disco)
              and _entradas(meta_disco, l) == metas[l]]
    if not postas:
        print("aviso: o kit ainda nao foi aplicado no tileset; o caso de DISCO "
              "nao roda")
    else:
        if len(postas) != len(metas):
            mau.append("o kit esta pela metade no disco: %d de %d metatiles"
                       % (len(postas), len(metas)))
        for local, ents in metas.items():
            if local * 16 + 16 > len(meta_disco) \
                    or _entradas(meta_disco, local) != ents:
                mau.append("metatile %d no disco nao e o do kit"
                           % (N_META_PRI + local))
            if local * 2 + 2 > len(attr_disco) \
                    or struct.unpack_from("<H", attr_disco, local * 2)[0] != attrs[local]:
                mau.append("atributo do metatile %d no disco nao e o do kit"
                           % (N_META_PRI + local))
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
    print("  %s: %d celulas mudadas, %d solidificadas, regua %.1f%% (mt %d) -> "
          "%.1f%% (mt %d)" % (ALVO, len(escritas), contas["solidos"], a, ida,
                              b, idb))
    print("  %d tiles, %d metatiles, %d provas negativas:"
          % (len(tiles_novos), len(metas), len(negativas)))
    for nome, queixa in negativas:
        print("    %-38s -> %s" % (nome, queixa[:96]))
    return 0


# --------------------------------------------------------- prova de EXTRACAO
def prova_extracao(pasta=None):
    """Desenha o mapa g00m15 do hack DUAS vezes e exige ZERO pixel de diferenca.

    De um lado, o mapa desenhado DIRETO DA ROM pelo
    `ferramentas/prova_extracao.py`; do outro, o MESMO mapa desenhado pelo
    `dev_scripts/render_maps.py` deste repo a partir do par de tilesets
    EXTRAIDO. Se os dois baterem pixel a pixel, a leitura de tile, de paleta, de
    metatile e de split de VRAM que este script usa esta certa.

    Boa noticia e suspeita, entao ela termina SABOTANDO um nibble do tile mais
    desenhado daquele mapa e exigindo que a comparacao REPROVE.
    """
    import shutil
    import subprocess
    import tempfile
    ferr = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/romhacks"
    if not os.path.isdir(ferr):
        raise SystemExit("--prova-extracao so roda na maquina que tem as ROMs")
    F = f"{ferr}/ferramentas"
    raiz = pasta or tempfile.mkdtemp(prefix="prova-cianwood-")
    mini = os.path.join(raiz, "minirepo")
    for sub in ("data/layouts/HackAmostra", "data/maps/HackAmostra",
                "data/tilesets/primary", "data/tilesets/secondary",
                "src/data/tilesets"):
        os.makedirs(os.path.join(mini, sub), exist_ok=True)

    for off, sub, flag in ((SS["pri"], "primary/ss_pri", []),
                           (SS["sec"], "secondary/ss_sec", ["--sec"])):
        alvo = os.path.join(mini, "data/tilesets", sub)
        cmd = ["python3", f"{F}/extrai_tileset.py", SS["slug"], "0x%X" % off,
               alvo, "--split", str(SS["split"][1])] + flag
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode:
            raise SystemExit("extrai_tileset falhou: %s" % (r.stderr or r.stdout))

    sys.path.insert(0, F)
    from gbamap import Rom  # noqa: E402
    p = os.path.join(ferr, SS["slug"])
    gba = [f for f in sorted(os.listdir(p)) if f.lower().endswith(".gba")][0]
    r = Rom(os.path.join(p, gba))
    r.n_meta_pri, r.n_tiles_pri, r.n_pal_pri = SS["split"]
    inv = json.load(open(f"{F}/inv/{SS['slug']}.json"))
    hdr = inv["grupos"][0]["mapas"][15]
    L = hdr["layout"]
    if (L["ts1"], L["ts2"]) != (SS["pri"], SS["sec"]):
        raise SystemExit("o g00m15 usa 0x%X/0x%X, e o kit veio de 0x%X/0x%X"
                         % (L["ts1"], L["ts2"], SS["pri"], SS["sec"]))
    w, h = L["w"], L["h"]
    palavras = struct.unpack_from("<%dH" % (w * h), r.rom, L["blockdata"])
    with open(os.path.join(mini, "data/layouts/HackAmostra/map.bin"), "wb") as f:
        f.write(struct.pack("<%dH" % (w * h), *palavras))

    with open(os.path.join(mini, "data/layouts/layouts.json"), "w") as f:
        json.dump(dict(layouts_table_label="gMapLayouts", layouts=[dict(
            id="LAYOUT_HACK_AMOSTRA", name="HackAmostra_Layout", width=w,
            height=h, primary_tileset="gTileset_SsPri",
            secondary_tileset="gTileset_SsSec",
            border_filepath="data/layouts/HackAmostra/border.bin",
            blockdata_filepath="data/layouts/HackAmostra/map.bin")]), f)
    with open(os.path.join(mini, "data/maps/HackAmostra/map.json"), "w") as f:
        json.dump(dict(id="MAP_HACK_AMOSTRA", name="HackAmostra",
                       layout="LAYOUT_HACK_AMOSTRA", object_events=[],
                       warp_events=[], coord_events=[], bg_events=[]), f)
    with open(os.path.join(mini, "src/data/tilesets/graphics.h"), "w") as f:
        for lab, sub in (("SsPri", "primary/ss_pri"), ("SsSec", "secondary/ss_sec")):
            f.write('const u32 gTilesetTiles_%s[] = INCGFX_U32("data/tilesets/%s'
                    '/tiles.png", ".4bpp.smol");\n' % (lab, sub))
    with open(os.path.join(mini, "src/data/tilesets/headers.h"), "w") as f:
        for lab in ("SsPri", "SsSec"):
            f.write("const struct Tileset gTileset_%s =\n{\n    .tiles = "
                    "gTilesetTiles_%s,\n};\n" % (lab, lab))

    png_repo = os.path.join(raiz, "HackAmostra.png")
    png_rom = os.path.join(raiz, "g00m15-rom.png")
    amb = dict(os.environ, REPO_MAPAS=mini, SAIDA_MAPAS=raiz)
    rr = subprocess.run(["python3", f"{RAIZ}/dev_scripts/render_maps.py",
                         "HackAmostra"], capture_output=True, text=True, env=amb)
    if not os.path.exists(png_repo):
        raise SystemExit("render_maps nao desenhou: %s" % (rr.stdout + rr.stderr))

    def compara():
        return subprocess.run(["python3", f"{F}/prova_extracao.py", SS["slug"],
                               "0", "15", png_repo, png_rom, "--split",
                               str(SS["split"][1])], capture_output=True, text=True)

    saida = compara()
    print(saida.stdout.strip())
    if saida.returncode:
        return 1

    from PIL import Image
    conta = collections.Counter(pal & 0x3FF for pal in palavras)
    quente = conta.most_common(1)[0][0]
    lado = "primary/ss_pri" if quente < SS["split"][0] else "secondary/ss_sec"
    caminho = os.path.join(mini, "data/tilesets", lado, "tiles.png")
    im = Image.open(caminho)
    px = im.load()
    antigo = px[3, 3]
    px[3, 3] = (antigo + 5) % 16
    im.save(caminho)
    subprocess.run(["python3", f"{RAIZ}/dev_scripts/render_maps.py",
                    "HackAmostra"], capture_output=True, text=True, env=amb)
    sab = compara()
    print("com UM nibble trocado: " + sab.stdout.strip().split("\n")[-2])
    if not sab.returncode:
        print("A COMPARACAO NAO SABE REPROVAR: prova vazia")
        return 1
    im = Image.open(caminho)
    im.load()[3, 3] = antigo
    im.save(caminho)
    subprocess.run(["python3", f"{RAIZ}/dev_scripts/render_maps.py",
                    "HackAmostra"], capture_output=True, text=True, env=amb)
    volta = compara()
    print("revertido: " + volta.stdout.strip().split("\n")[-1])
    if volta.returncode:
        return 1
    if pasta is None:
        shutil.rmtree(raiz, ignore_errors=True)
    return 0


# ------------------------------------------------- prova de TILE contra a ROM
def prova_tiles():
    """Cada tile do kit, DEPOIS de reindexado, contra o tile da ROM: zero pixel."""
    ferr = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/romhacks"
    if not os.path.isdir(ferr):
        raise SystemExit("--prova-tiles so roda na maquina que tem as ROMs")
    sys.path.insert(0, f"{ferr}/ferramentas")
    from gbamap import Rom  # noqa: E402
    p = os.path.join(ferr, SS["slug"])
    gba = [f for f in sorted(os.listdir(p)) if f.lower().endswith(".gba")][0]
    r = Rom(os.path.join(p, gba))
    r.n_meta_pri, r.n_tiles_pri, r.n_pal_pri = SS["split"]
    t1, t2 = r.parse_tileset(SS["pri"]), r.parse_tileset(SS["sec"])
    pal = {i: _rgb(t1 if i < r.n_pal_pri else t2, i) for i in range(16)}
    dados = kit()
    n, dif = 0, 0
    for ch, px_kit in dados["tiles"].items():
        lado, li, ip = ch.split(":")
        li, ip = int(li), int(ip)
        crus = _nibbles((t1 if lado == "p" else t2)["tiles"], li)
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
    ch0 = sorted(dados["tiles"])[0]
    salvo = [linha[:] for linha in dados["tiles"][ch0]]
    dados["tiles"][ch0][0][0] = (salvo[0][0] + 1) % 16
    ruim = 0
    crus = _nibbles((t1 if ch0.split(":")[0] == "p" else t2)["tiles"],
                    int(ch0.split(":")[1]))
    ip = int(ch0.split(":")[2])
    cores_nossas = dados["paletas"][str(dados["tiles_vaga"][ch0])]
    for y in range(8):
        for x in range(8):
            a = tuple(pal[ip][crus[y][x]]) if crus[y][x] else None
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
    if "--prova-extracao" in sys.argv:
        return prova_extracao()
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
