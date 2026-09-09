#!/usr/bin/env python3
"""Refino de `LilycoveCity` (tema PORTO E PRAIA), no `gTileset_Lilycove`, com os
móveis de cais importados do `Pokémon Light Platinum`.

O QUE ESTA CIDADE TEM DE ERRADO, medido pela `dev_scripts/regua_cidades.py` nesta
árvore em 09/09/2026. Das **1.453 células andáveis a pé**, a maior contagem das
quatro regiões desta onda, o carimbo dominante é o metatile **1**, a grama lisa
do `gTileset_General`, com **559 células (38,5%)**. Mas a régua conta ID e o
tapete de verdade é MAIOR do que ela diz, e isto é o primeiro achado desta
passada:

    OS NOVE GÊMEOS DO CALÇAMENTO. Os metatiles 554, 555, 556, 562, 563, 564,
    570, 571 e 572 do `gTileset_Lilycove` têm as OITO entradas byte a byte
    iguais (`9234 9235 9235 9234 0000 0000 0000 0000`) e o mesmo atributo
    `0x0000`. São NOVE cópias pixel a pixel do mesmo calçamento, e o Emerald
    pinta a praça com as nove misturadas. Somadas dão **275 células**, ou seja
    18,9% do chão, e a régua as lê como nove carimbos pequenos: o 555 com 6,4%,
    o 563 com 5,8%, o 571 com 4,7% e por aí. Quem olha só a coluna `liso` acha
    que Lilycove é menos lisa do que Mossdeep; quem olha a tela vê grama chapada
    e praça chapada, 834 células de dois desenhos.

As QUATRO famílias de chão desta cidade, medidas célula a célula:

    família     metatile(s)                  atributo  células  elevações
    grama       1                            0x0000        559  3 (386), 5 (169), 0 (4)
    calçamento  554..572, os nove gêmeos     0x0000        275  3 (202), 5 (73)
    areia       292                          0x1021        117  3 (117)
    maresia     398..430 (o 414 é o miolo)   0x0017        193  3 (193)

TRÊS DELAS SÃO TRATADAS E A QUARTA É REPROVADA POR NÚMERO, e a quarta é a que
mais dói deixar. Depois desta passada o dominante passa a ser o **414, a maresia
da orla, com 193 células**, e a régua fecha na casa dos 13%, abaixo do teto de
20% da onda. A maresia não foi quebrada, e o motivo não é medo da água, é
medida:

  1. O 414 é `448 449 449 448` na paleta 4, e o par 448/449 é ÁGUA RASA quase
     chapada. Os arranjos possíveis desses dois tiles medem, em distância RGB
     média por pixel contra o carimbo, **4,3 (só o 448), 4,3 (só o 449), 4,3
     (448/449 em colunas), 8,6 (troca) e 12,2 (espelho horizontal)**. Só dois
     passam o piso de 8,0 do `varia_carimbo.py`, e os dois são o MESMO par de
     tiles deslocado de oito pixels.
  2. Os arranjos que medem longe (**47,5 a 95,1**) só medem longe porque
     misturam o par 454/455, que é ÁGUA FUNDA. Pintar água funda numa célula
     que o jogador ATRAVESSA A PÉ é mentir sobre a profundidade, e é o mesmo
     erro que o coqueiro do Scorched Silver pagou em Dewford: passa no número e
     reprova no desenho.
  3. E o argumento que fecha: **448, 449, 454 e 455 são VAGAS PINADAS**. O
     `dev_scripts/pinos_anim.py gTileset_General` mede que
     `TilesetAnim_General` reescreve as vagas 432 a 461 a cada dezesseis quadros
     (`QueueAnimTiles_General_Water`, `src/tileset_anims.c`). Toda distância
     medida acima é do QUADRO ZERO; em jogo a orla inteira já se mexe. Espelhar
     tile animado é enfeitar uma coisa que o motor redesenha sozinha.

  Resultado: **ZERO célula de maresia é escrita**, e o auto-teste tem um portão
  que reprova se alguma for.

ACHADO DE LADO, PARA O CONDUTOR, e ele é sobre OUTRA cidade desta onda. O
`praia_dewford.py` monta quatro das dezesseis variantes de areia com os tiles
**496 e 498** do `gTileset_General`, chamados ali de "faixa de transição clara
para escura". As vagas 496 a 501 são o destino do
`QueueAnimTiles_General_Waterfall`, que `TilesetAnim_General` dispara em
`timer % 16 == 3`: em jogo, aquelas células de areia de DewfordTown recebem os
seis tiles da CACHOEIRA, e não a arte estática que o render mostra. Medido nesta
árvore comparando `data/tilesets/primary/general/anim/waterfall/0.png` com as
vagas 496 a 501 do `tiles.png`: o conteúdo é diferente. Esta passada NÃO conserta
Dewford (não é a cidade dela e mexer no `map.bin` de outra frente seria pior),
mas deixa o achado escrito, e por causa dele NENHUMA vaga pinada entra no
vocabulário de chão daqui.

A ÁGUA DE SURF NÃO É TOCADA, e agora com a fonte na mão. `MB_SHALLOW_WATER` não
tem `TILE_FLAG_SURFABLE` na `sTileBitAttributes` de `src/metatile_behavior.c`:
maresia é chão que se atravessa a pé, e o alcance de Surf não passa por ela. As
679 células do mar a leste têm comportamento `MB_OCEAN_WATER` e companhia, estão
todas no `enfeita_cidades.agua()`, e o auto-teste compara o CONJUNTO de células
de água antes e depois exigindo igualdade, além de comparar o carimbo de
comportamento célula a célula.

OS DEZ IRMÃOS, e aqui a lista é limpa. O `data/layouts/layouts.json` dá dez
layouts com `secondary_tileset` exatamente `gTileset_Lilycove`: `LilycoveCity`,
`Route121`, `Route122`, `Route123` e as SEIS folhas da `SafariZone`. Os dez têm
`blockdata_filepath` PRÓPRIO, os dez existem em disco e NENHUM caminho se
repete, ou seja não há aqui o caso dos quatro esboços de Kalos que emprestam o
`map.bin` de `PetalburgCity`. O `gTileset_LilycoveSinnoh`, que aparece em
`PastoriaCity` e nas duas metades da `Route212`, é OUTRO tileset e não é irmão.

O ORÇAMENTO NÃO PRECISOU DE COMPACTAÇÃO, e isso muda o risco da passada. O
`gTileset_Lilycove` está em 432 de 512 tiles, com 80 vagas livres no fim, e em
351 de 512 metatiles, com 161 vagas livres no fim. Como o kit inteiro cabe nessas
vagas, o `compacta_tileset.py` não roda, nenhum tile existente é renumerado e a
prova de zero pixel nos irmãos é por CONSTRUÇÃO reforçada por render. Duas
medidas que valem estar escritas:

  - `pinos_anim.py gTileset_Lilycove` diz `anim=nao`: o `.callback` põe
    `sSecondaryTilesetAnimCallback = NULL` e o secundário NÃO escreve vaga
    nenhuma em tempo de execução. ZERO PINO. Toda vaga de 432 a 511 é livre de
    verdade.
  - `gTilesetTiles_Lilycove` em `src/data/tilesets/graphics.h` NÃO declara
    `-num_tiles`. Crescer o `tiles.png` não esbarra no `-Wnum_tiles` que parou o
    build de Dewford, e o `graphics.h` fica INTOCADO.

AS PALETAS LIVRES SÃO QUATRO, medidas por metatile VIVO (os que aparecem em
`map.bin` de algum dos dez irmãos): as vagas **6, 10, 11 e 12** não têm UM índice
aceso. As 8 e a 9 têm catorze dos quinze em uso e a 7 tem sete. Este kit gasta
três (6, 10 e 11) e deixa a 12 inteira.

A FONTE, e a triagem que decidiu o desenho.

O CANDIDATO DO ÍNDICE FOI REPROVADO, com o número. O
`/tmp/claude-501/FONTES-POR-TILESET.md` aponta um só candidato para
`secondary/lilycove`: o `light-platinum` `0x286DCC`, `frac_nova` 0,982, a maior
fração de arte nova da lista de Hoenn. Ele foi EXTRAÍDO e o mapa de amostra dele
(g00m06, 40x64) foi RENDERIZADO: é uma cidade de NEVE, com asfalto escuro,
pinheiro nevado e pátio de contêineres com touca de neve em cima de cada caixa.
As médias RGB dos quatro metatiles mais usados dele, contra as nossas:

    fonte 0x286DCC       média RGB      contra a nossa calçada (179,199,164)
    mt 519 (neve)        (202,221,229)  72,4
    mt 654 (asfalto)     ( 88, 96,120)  144,3
    mt 521 (borda)       (133,159,181)  63,3
    mt 524 (borda)       (130,163,180)  62,9

    e contra a nossa grama (116,197,165): 109,9 / 88,9 / 44,6 / 45,3

Três dos quatro passam de 60 contra o critério de ~50 que Pastoria, Sandgem e
Hearthome fixaram, e o único que fica perto (o 521, a 44,6 da grama) é a BORDA
entre neve e asfalto, que sozinha não é chão. O tema fecha a conta: engradado
com neve em cima num porto de verão não é peça que não casa, é peça de outra
estação. REPROVADO.

O QUE ENTROU É O SECUNDÁRIO COSTEIRO DO MESMO HACK, o `0x286D54`, o mesmo par que
`costa_sandgem.py`, `orla_sunyshore.py` e `praia_dewford.py` já usaram, de
WesleyFG, base Ruby (AXVE), md5 `7fd2c08735459d99fa23fdaa9b755486`. O mapa de
amostra dele (g00m01, 78x60) é uma cidade de PORTO de verdade: praia de areia,
cais de concreto, guindaste, contêiner empilhado e boia. E as CINCO peças
escolhidas são DIFERENTES das seis que Dewford levou, de propósito, para as duas
cidades de mar de Hoenn não saírem com a mesma mobília:

    engradado laranja   local   9    boia salva-vidas   local 358
    engradado azul      local  13    cabeço de amarração local 362
    boia no mourão      local 322

  Os dois engradados são o MESMO desenho em duas paletas do hack (a 1 e a 0), o
  que dá duas cores de contêiner por oito tiles. As três peças de cais moram na
  paleta 6 da fonte. Três paletas do hack, três vagas nossas: 1 -> 6, 0 -> 10,
  6 -> 11.

O QUE FOI REPROVADO POR NÚMERO OU POR DESENHO, além do `0x286DCC`:

  - O TAMBOR do `0x286D54` (locais 11 e 12), que é a peça de porto que mais falta
    aqui. Ele mora na paleta 2 do hack, ou seja custaria a QUARTA vaga de paleta
    livre, e a arte dele ocupa só a coluna esquerda da célula (os quadrantes 1 e
    3 são o piso da fonte): meia peça por uma paleta inteira. Ficou de fora, e a
    vaga 12 ficou livre para quem vier depois.
  - O CONVÉS DE TÁBUA do nosso primário (metatiles 426, 427, 428, 434 e 436), que
    seria o chão de cais perfeito. Os nove pedaços do remendo NÃO TÊM O MESMO
    ATRIBUTO: o 426, 427, 428, 434 e 436 são `0x0000` e o 435, 441, 442 e 443 são
    `0x1000`. Pintar um remendo com eles trocaria o `layerType` de célula
    ANDÁVEL, que é o item 4 do `portao_planta.py`. Sem os nove pedaços não há
    borda, e textura de chão sem borda vira retalho, que é a lição que Pastoria
    pagou. O 441, 442 e 443 também não servem como móvel: a camada de cima deles
    acende 256 pixels de 256, ou seja tapa a célula inteira.
  - O CANTEIRO DE FLOR, o metatile 4 do primário. É COVERED, ANIMADO (a camada de
    cima aponta para as vagas pinadas 508 a 511) e a cidade JÁ o usa como célula
    ANDÁVEL em 34 lugares. Plantá-lo sólido faria a mesma flor ser pisável num
    canto e parede no outro, que é a mesma poda que Littleroot fez.
  - A AREIA NA CALÇADA E A LAJOTA NA PRAIA. Cada família de chão só recebe
    variante da própria família, e cada móvel declara em qual família pousa: o
    engradado laranja e a boia salva-vidas só na areia, o cabeço e o contêiner
    azul só no calçamento, o arbusto e a touceira só na grama. O remendo de
    AREAL sobre a grama é a única travessia, e ela é condicionada: só vale se o
    retângulo encostar (Chebyshev 3) numa célula de areia ou de maresia, que é a
    regra `perto` que `mato_littleroot.py` escreveu para a praia de Petalburg.

AS REGRAS DE MONTAGEM, e a armadilha que cada uma resolve:

  - CHÃO é metatile novo cujo atributo é IGUAL, bit a bit, ao do carimbo da
    família. A grama e o calçamento são `0x0000` (`layerType` NORMAL) e a areia é
    `0x1021` (`MB_SAND`, COVERED). Em NORMAL o motor manda LIXO para o BG3 e a
    camada de baixo para o BG2, então toda variante NORMAL tem que ter a camada
    de baixo CHEIA (256 pixels opacos) e a de cima VAZIA. Em COVERED o carimbo
    292 duplica a camada de baixo na de cima, e as variantes copiam a estrutura
    dele em vez de deixar a de cima vazia.
  - REMENDO é autotile de NOVE peças com borda desenhada, e a região é ABERTA em
    3x3 antes de pintar, senão apareceria célula sem norte e sem sul, que
    precisaria de uma décima peça que o `gTileset_General` não desenhou. O miolo
    da TERRA é remontado: o metatile 268 do primário tem atributo `0x00A0`,
    `MB_BERRY_TREE_SOIL`, e pintá-lo numa célula de grama mudaria o
    comportamento de célula andável e ainda poria solo de amoreira sem amoreira.
  - MÓVEL é célula que vira SÓLIDA: a arte vai na camada de CIMA, a de baixo
    recebe o NOSSO chão da família entrada por entrada, e o atributo é
    comportamento ZERADO com `layerType` COVERED (0x1000).
  - MÓVEL É DE BEIRA: encosta num sólido, na água ou na borda do mapa. Peça solta
    no meio da praça lê como erro de mapa.
  - QUADRANTE DE BAIXO SOBE quando o de cima está vazio, e quadrante promovido
    que é PISO da fonte é descartado e recebe o nosso chão.
  - Nenhum id de flag, var, script, música, treinador ou espécie é importado. Só
    ARTE.

Uso:
    python3 dev_scripts/porto_lilycove.py                # mede e mostra o plano
    python3 dev_scripts/porto_lilycove.py --aplicar      # escreve tileset e mapa
    python3 dev_scripts/porto_lilycove.py --desfazer     # devolve o map.bin
    python3 dev_scripts/porto_lilycove.py --demo         # auto-teste
    python3 dev_scripts/porto_lilycove.py --extrai       # regera o kit da ROM
    python3 dev_scripts/porto_lilycove.py --so-tileset   # só o tileset
    python3 dev_scripts/porto_lilycove.py --prova-tiles  # o kit contra a ROM
"""
import collections
import glob
import json
import os
import re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")
os.environ.setdefault("REPO_MAPAS", RAIZ)
import arte_ginasios_sinnoh as G     # noqa: E402
import enfeita_cidades as E          # noqa: E402

# O bloco de teste DESTA rodada é o único que o varredor de corredores pula: os
# casos dele foram escritos DEPOIS do desenho e a partir dele.
BLOCO_PROPRIO = "219_porto_lilycove.json"
E.BLOCO_PROPRIO = BLOCO_PROPRIO

ALVO = "LilycoveCity"
DESTINO = f"{RAIZ}/data/tilesets/secondary/lilycove"
KIT_JSON = f"{RAIZ}/dev_scripts/porto_lilycove_kit.json"
PLANO = f"{RAIZ}/dev_scripts/porto_lilycove.json"

PRIMARIO = "gTileset_General"
SECUNDARIO = "gTileset_Lilycove"

# Os DEZ layouts vivos que dividem o `gTileset_Lilycove`. Lido do
# `data/layouts/layouts.json` e conferido em disco: os dez têm `map.bin` próprio
# e nenhum caminho se repete.
IRMAOS = ["LilycoveCity", "Route121", "Route122", "Route123",
          "SafariZone_Northwest", "SafariZone_North", "SafariZone_Southwest",
          "SafariZone_South", "SafariZone_Northeast", "SafariZone_Southeast"]

TETO_TILES = 512            # NUM_TILES_IN_PRIMARY, include/fieldmap.h
TETO_META = 512             # NUM_METATILES_IN_PRIMARY, include/fieldmap.h
TILE_LOCAL_0 = 432          # o `tiles.png` tem 432 tiles: o kit vai DEPOIS
META_LOCAL_0 = 351          # o `metatiles.bin` tem 351: o kit vai DEPOIS
# ZERO pino: `pinos_anim.py gTileset_Lilycove` diz que o secundário não escreve
# vaga nenhuma em tempo de execução. O conjunto fica aqui, vazio e conferido,
# para o portão existir mesmo assim.
PINOS_ANIM = set()
# As vagas do PRIMÁRIO que `TilesetAnim_General` reescreve em tempo de execução.
# Nenhum tile de chão desta passada pode sair daqui: a arte estática que o render
# mostra não é a que o jogo desenha.
PINOS_PRIMARIO = (set(range(432, 462)) | set(range(464, 474))
                  | set(range(480, 490)) | set(range(496, 502))
                  | set(range(508, 512)))

MARGEM = 1
TETO_REGUA = 20.0
TETO_COR = 42.0             # distância de cor média aceita entre chão novo e carimbo
PISO_VARIANTE = 8.0         # distância pixel a pixel mínima entre duas variantes
PISO_PADRAO = 0.08          # quanto a posição pode adivinhar a peça além do chute cego
PISO_MANCHA = 400           # abaixo disso a passada não fez o serviço nesta cidade
ESPACO_ENTRE_MOVEIS = 2     # Chebyshev mínimo entre dois móveis QUAISQUER
MULTI_NIVEL = 15            # ELEVATION_MULTI_LEVEL: casa com QUALQUER elevação

N4 = E.N4

# ------------------------------------------------------------- as FAMÍLIAS
# `ids` são TODOS os metatiles que a cidade usa como aquele chão (o calçamento
# tem nove gêmeos byte a byte iguais); `canonico` é o que serve de base para
# móvel e de referência para a régua de cor. `a`/`b` é o par de tiles do chão e
# `pal` a vaga de paleta com que ele é pintado. `texturas` são os tiles NÃO
# PINADOS que passam na régua de cor da família e no olho.
#
# A PRIMEIRA LISTA DE TEXTURAS DESTA PASSADA FOI REPROVADA NO RENDER, e o defeito
# vale ficar escrito porque ele passou por DOIS filtros numéricos antes de
# aparecer na tela. As texturas eram escolhidas por (a) distância de cor MÉDIA do
# metatile inteiro contra o carimbo e (b) distância pixel a pixel entre
# variantes. As duas contas são médias, e média engole pixel: um tile com quatro
# pixels AZUIS e sessenta pixels de areia tem média de areia. No render a praia
# saiu salpicada de traço azul e a praça de mancha vermelha, porque tiles como o
# 102, o 150 e o 163 acendem índices que, na paleta da FAMÍLIA, guardam cor de
# água e de flor, e não de chão.
#
# O conserto é um portão POR ÍNDICE e não por média: `indices_da_familia()`
# calcula a banda de cor do carimbo (os índices que os tiles `a` e `b` acendem) e
# aceita como "da família" só o índice cuja cor está a menos de `BANDA_COR` do
# mais próximo deles. Uma textura só entra se TODO índice que ela acende estiver
# nessa banda. Medido nesta árvore: a banda da areia (paleta 5) é
# {11,12,13} e admite o 14; a da grama (paleta 2) é {12,13,14} e admite o 15; a
# do calçamento (paleta 9) é {2,3,13} e admite o 1, o 4 e o 12. Com o portão
# ligado, 43 tiles do primário passam para a areia, 44 para a grama e 59 para o
# calçamento, e a lista abaixo é o recorte desses por DESENHO: fica o grão que
# varia dentro do próprio tile de 8x8, e sai a forma grande (faixa vertical, que
# lê como tábua), o quadriculado grosso (que lê como tela de mosquiteiro) e todo
# tile com pixel transparente, que deixaria buraco na camada de baixo.
BANDA_COR = 60.0

FAMILIAS = {
    "grama": dict(
        ids=[1], canonico=1, a=2, b=3, pal=2,
        texturas=[94, 107, 123, 132, 139, 151, 153, 155]),
    "calcada": dict(
        ids=[554, 555, 556, 562, 563, 564, 570, 571, 572], canonico=563,
        a=564, b=565, pal=9,
        texturas=[213, 266, 278, 282, 284, 542]),
    "areia": dict(
        ids=[292], canonico=292, a=264, b=280, pal=5,
        texturas=[2, 3, 94, 107, 123, 129, 132, 139, 152, 155, 220, 284]),
}

# Os REMENDOS de autotile, todos sobre a GRAMA e todos já desenhados no
# `gTileset_General`, com canto arredondado e franja. `auto` é [NO,N,NE, O,C,E,
# SO,S,SE]; `fill` é o metatile que já desenha o miolo (None quando o miolo do
# primário tem comportamento próprio e precisa ser remontado).
REMENDOS = {
    "gasta": dict(a=266, b=282, pal=2, fill=473,
                  auto=[464, 465, 466, 472, 473, 474, 480, 481, 482]),
    # o miolo da terra (268) é MB_BERRY_TREE_SOIL: entra remontado
    "terra": dict(a=268, b=284, pal=3, fill=None,
                  auto=[259, 260, 261, 267, None, 269, 275, 276, 277]),
    "areal": dict(a=264, b=280, pal=5, fill=289,
                  auto=[280, 281, 282, 288, 289, 290, 296, 297, 298]),
}

# Os nove arranjos do par [a,b,b,a]. Cada entrada é (tile, espelho), com espelho
# em 0..3: bit 1 = horizontal (0x400), bit 2 = vertical (0x800). O primeiro é o
# ARRANJO DO CARIMBO e não vira metatile novo.
ARRANJOS = [
    ("carimbo",   [("a", 0), ("b", 0), ("b", 0), ("a", 0)]),
    ("espelhoH",  [("a", 1), ("b", 1), ("b", 1), ("a", 1)]),
    ("espelhoV",  [("a", 2), ("b", 2), ("b", 2), ("a", 2)]),
    ("espelhoHV", [("a", 3), ("b", 3), ("b", 3), ("a", 3)]),
    ("giro",      [("b", 1), ("a", 1), ("a", 1), ("b", 1)]),
    ("troca",     [("b", 0), ("a", 0), ("a", 0), ("b", 0)]),
    ("misto1",    [("a", 0), ("b", 1), ("b", 2), ("a", 3)]),
    ("misto2",    [("b", 3), ("a", 2), ("a", 1), ("b", 0)]),
    ("misto3",    [("a", 1), ("b", 0), ("b", 3), ("a", 2)]),
    ("misto4",    [("b", 2), ("a", 3), ("a", 0), ("b", 1)]),
]


# Construtores de quadrante para as TEXTURAS. Cada um devolve quatro
# (tile, espelho), com o quadrante 0 no alto à esquerda, o 1 no alto à direita,
# o 2 embaixo à esquerda e o 3 embaixo à direita.
#
# DUAS REGRAS DE MONTAGEM, e as duas foram pagas no render desta passada.
#
# A primeira é a de Dewford: textura contra CHAPADO alinha quadrante com o
# vizinho e o chão vira TABULEIRO de 8x8. Por isso não existe construtor
# "textura num quadrante só": ou a textura toma a célula inteira, ou ela se
# divide com OUTRA textura.
#
# A segunda é desta passada e é mais sutil. A primeira versão tinha um
# construtor `_u(t)` que punha o MESMO tile nos quatro quadrantes com os quatro
# espelhos (nenhum, H, V, HV). Isso é um espelhamento de quatro dobras, e o
# resultado é SEMPRE simétrico nos dois eixos: no render a praia saiu com laços
# de gravata, anéis e barras verticais, porque um grão de areia espelhado quatro
# vezes vira ORNAMENTO. Chão não é simétrico; grão de chão é o mesmo azulejo
# repetido. Os construtores abaixo nunca espelham um quadrante contra o outro, e
# `_simetrico()` é o portão que reprova quem escapar.
def _p(t, f=0):
    """O MESMO azulejo nos quatro quadrantes, com o MESMO espelho. É o que o
    chão de verdade faz: repetir o desenho de 8x8."""
    return [(t, f)] * 4


def _d(a, b, f=0):
    """A estrutura do PRÓPRIO carimbo, [a,b,b,a], com duas texturas."""
    return [(a, f), (b, f), (b, f), (a, f)]


def _y(a, b, f=0):
    """A metade de CIMA com uma textura e a de BAIXO com outra."""
    return [(a, f), (a, f), (b, f), (b, f)]


def _c(a, b, f=0):
    """A coluna da ESQUERDA com uma textura e a da direita com outra."""
    return [(a, f), (b, f), (a, f), (b, f)]


def _simetrico(px):
    """O metatile de 16x16 é igual à própria imagem espelhada?

    'H' quando ele é igual espelhado na horizontal, 'V' na vertical, '' quando
    não é nenhum dos dois. Simetria de 16x16 lê como DESENHO e não como grão:
    o olho acha o eixo na hora e a célula deixa de ser chão para virar enfeite
    repetido. É o portão que corta o laço de gravata e o anel.
    """
    h = [px[y * 16 + (15 - x)] for y in range(16) for x in range(16)]
    v = [px[(15 - y) * 16 + x] for y in range(16) for x in range(16)]
    return ("H" if px == h else "") + ("V" if px == v else "")


# As texturas de cada família, montadas dos tiles vetados acima. O nome é o que
# aparece no plano e no stdout.
def _lista_texturas(nome_fam):
    t = FAMILIAS[nome_fam]["texturas"]
    saida = []
    for k, tt in enumerate(t):
        saida.append(("%s t%d" % (nome_fam, tt), _p(tt, 0)))
        if k % 3 == 0:
            saida.append(("%s t%d virado" % (nome_fam, tt), _p(tt, 1)))
    for k in range(len(t) - 1):
        a, b = t[k], t[k + 1]
        cons = (_d, _y, _c)[k % 3]
        saida.append(("%s t%d+%d" % (nome_fam, a, b), cons(a, b)))
    return saida


# ------------------------------------------------------ os MÓVEIS que são NOSSOS
# `de` é o metatile cuja camada de CIMA é levantada sobre o chão da família
# `sobre`. Custa ZERO tile, ZERO cor e uma vaga de metatile cada.
MOVEIS_NOSSOS = [
    # a GRAMA é o parque da cidade
    dict(nome="moita do parque",     de=699, sobre="grama"),
    dict(nome="arbusto",             de=29,  sobre="grama"),
    dict(nome="arbusto largo",       de=14,  sobre="grama"),
    dict(nome="touceira",            de=30,  sobre="grama"),
    dict(nome="touceira espelhada",  de=31,  sobre="grama"),
    dict(nome="placa do parque",     de=27,  sobre="grama"),
    dict(nome="matacao",             de=224, sobre="grama"),
    # o CALÇAMENTO é o cais e a praça do porto
    dict(nome="poste de amarracao",  de=306, sobre="calcada"),
    dict(nome="cabeco duplo",        de=307, sobre="calcada"),
    dict(nome="guarda-corpo",        de=460, sobre="calcada"),
    dict(nome="quadro de avisos",    de=577, sobre="calcada"),
    dict(nome="boia de sinalizacao", de=666, sobre="calcada"),
    # a AREIA é a praia a leste
    dict(nome="pedra da praia",      de=226, sobre="areia"),
    dict(nome="moita de praia",      de=631, sobre="areia"),
]

# ------------------------------------------------------ os MÓVEIS do hack
MOVEIS_LP = [
    dict(nome="engradado laranja",  lp=9,   sobre="areia"),
    dict(nome="engradado azul",     lp=13,  sobre="calcada"),
    dict(nome="rolo de cabo",       lp=127, sobre="calcada"),
    dict(nome="tina do pescador",   lp=15,  sobre="areia"),
    dict(nome="tina laranja",       lp=17,  sobre="areia"),
    # as DUAS pontas da amarracao. Elas NAO entram na mobilia solta: o cabo de
    # uma acaba no ar e so faz sentido com a outra do lado, entao elas viram uma
    # corrida de DUAS celulas em `CERCAS`.
    dict(nome="mourao do cabo",     lp=16,  sobre="calcada"),
    dict(nome="mourao do cabo 2",   lp=18,  sobre="calcada"),
]

# CERCAS: corrida horizontal de células sólidas, com ponta esquerda, meio e
# ponta direita. A da grama usa os metatiles 328, 329 e 330 do primário DIRETO
# (a camada de baixo deles já é o carimbo de grama e eles já são COVERED, custo
# ZERO); a do cais remonta a barreira prateada 704, 705 e 706 do secundário
# sobre o calçamento.
CERCAS = [
    dict(nome="cerca do parque", sobre="grama", direto=True,
         esq=328, meio=329, dir=330),
    # a AMARRACAO e a unica corrida montada de MOVEIS ja prontos, e ela tem
    # comprimento fixo DOIS: o cabo sai do mourao da esquerda e chega no da
    # direita. Com tres celulas o pedaco do meio seria cabo sem ponta. Ela vem
    # ANTES do guarda-corpo porque a praca tem 37 celulas de beira e quem corre
    # primeiro escolhe: com o guarda-corpo na frente, a amarracao nao cabia.
    dict(nome="amarracao do cais", sobre="calcada", direto=False,
         de_movel=("mourao do cabo", "mourao do cabo", "mourao do cabo 2")),
    dict(nome="guarda-corpo do cais", sobre="calcada", direto=False,
         esq=704, meio=705, dir=706),
]

# ------------------------------------------------------------------- a FONTE
LP = dict(slug="light-platinum", hack="Pokemon Light Platinum", autor="WesleyFG",
          md5="7fd2c08735459d99fa23fdaa9b755486", base="Ruby (AXVE)",
          pri=0x286CF4, sec=0x286D54, split=(512, 512, 6))

# PALETA DE ORIGEM -> VAGA NOSSA. Só as DUAS em que a arte das sete peças mora.
# Quadrante pintado com qualquer outra paleta da fonte é DESCARTADO e recebe o
# nosso chão.
VAGAS_PAL = {1: 6, 0: 10}

# Quantos metatiles DIFERENTES da fonte precisam repetir o mesmo PADRÃO de camada
# de baixo para ele ser piso dela.
PISO_MIN = 4


def _mistura(*n):
    """Hash determinista de inteiros, 32 bits. Nada de `random`: o plano tem que
    sair idêntico em qualquer máquina e em qualquer versão de Python."""
    h = 0x811C9DC5
    for x in n:
        h = ((h ^ (x & 0xFFFFFFFF)) * 0x01000193) & 0xFFFFFFFF
        h ^= h >> 15
    return h


# ------------------------------------------------------------ leitura do nosso
def _ler(nome):
    return open(f"{DESTINO}/{nome}", "rb").read()


def _tileset(rotulo):
    import render_maps as RM
    return RM.carregar_tileset(rotulo)


def _entradas(bin_meta, local):
    return list(struct.unpack_from("<8H", bin_meta, local * 16))


def ents_nossas(mt_id, tp=None, ts=None):
    """As oito entradas de um metatile NOSSO, pelo id global."""
    tp = tp or _tileset(PRIMARIO)
    ts = ts or _tileset(SECUNDARIO)
    tset, loc = (tp, mt_id) if mt_id < 512 else (ts, mt_id - 512)
    if (loc + 1) * 16 > len(tset["metatiles"]):
        return [0] * 8
    return list(struct.unpack_from("<8H", tset["metatiles"], loc * 16))


def attr_nosso(mt_id):
    if mt_id < 512:
        return G._attrs(PRIMARIO)[mt_id]
    a = G._attrs(SECUNDARIO)
    local = mt_id - 512
    return a[local] if local < len(a) else 0


def arte_em_cima(ents, tp=None, ts=None):
    """A camada de CIMA destas entradas acende ALGUM pixel?

    A pergunta não é "o índice de tile é zero": o tile 1 do primário existe e não
    tem um pixel aceso.
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
    """{vaga: [índices de cor que NENHUM pixel VIVO nosso usa]}.

    "Vivo" é a palavra que importa: o `gTileset_Lilycove` tem 351 metatiles e só
    265 aparecem em `map.bin` de algum dos DEZ layouts. A armadilha 4 do
    `compacta_paletas.py` (metatile do PRIMÁRIO alcançável pintando com vaga de
    secundário) roda junto, porque "medi uma vez" não é portão.
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
        if (local + 1) * 16 > len(tset["metatiles"]):
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
    """BGR555 do GBA para o RGB888 que o repo usa: cinco bits DESLOCADOS TRÊS
    casas, não esticados para 0..255."""
    c = struct.unpack_from("<16H", ts["pal"], i * 32)
    return [[((v >> s) & 0x1F) << 3 for s in (0, 5, 10)] for v in c]


def _piso_da_fonte(tset):
    """Os tiles que a FONTE usa como piso, por evidência e não por decoreba.

    Duas assinaturas: (a) padrão de camada de baixo que aparece em PISO_MIN
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
    """Regera `porto_lilycove_kit.json` a partir da ROM privada do Light Platinum.

    Só roda na máquina que tem `fontes-mapas/romhacks/`. O que sai daqui é o asset
    CONVERTIDO (tiles em nibbles, já reindexados para a vaga de destino, e paleta
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
        do hack tem que virar DUAS vagas nossas, senão a segunda apaga a
        primeira. É exatamente o caso dos dois engradados, que são o mesmo
        desenho nas paletas 1 e 0.
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

    # REINDEXA cada nibble para a tabela nova. A cor 0 continua 0 e nenhuma cor é
    # aproximada: a tabela de destino tem as MESMAS cores RGB da fonte, só em
    # outro índice, então o pixel sai idêntico ao da ROM.
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
def kit_lp():
    if not os.path.exists(KIT_JSON):
        raise SystemExit("falta %s; rode --extrai numa maquina com a ROM"
                         % os.path.relpath(KIT_JSON, RAIZ))
    return json.load(open(KIT_JSON))


def chao_da_familia(nome_fam, tp=None, ts=None):
    """(as quatro entradas da camada de BAIXO do carimbo, o atributo dele, se ele
    duplica a camada de baixo na de cima)."""
    mt = FAMILIAS[nome_fam]["canonico"]
    ents = ents_nossas(mt, tp, ts)
    return ents[:4], attr_nosso(mt), ents[4:] == ents[:4]


def _locais_livres():
    return list(range(META_LOCAL_0, TETO_META))


def _vagas_de_tile():
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


def _quad(tile, espelho, pal):
    return ((0x400 if espelho & 1 else 0) | (0x800 if espelho & 2 else 0)
            | tile | (pal << 12))


def _opacos(px):
    return sum(1 for linha in px for c in linha if c)


def _indices_do_tile(t, tp=None, ts=None):
    """Os índices de cor que o tile ACENDE. None quando o tile não existe."""
    import render_maps as RM
    tp = tp or _tileset(PRIMARIO)
    ts = ts or _tileset(SECUNDARIO)
    tile = RM.resolver_tile(tp, ts, t)
    if tile is None:
        return None
    return {c for linha in tile for c in linha if c}


def indices_da_familia(nome_fam, tp=None, ts=None):
    """(banda do carimbo, índices admitidos) de uma família.

    A banda é o conjunto de índices que os tiles `a` e `b` do carimbo acendem;
    admitido é todo índice cuja cor, NA PALETA DA FAMÍLIA, está a menos de
    `BANDA_COR` do mais próximo da banda. É este o portão que impede textura com
    pixel de água ou de flor de entrar como chão, e a média de cor do metatile
    inteiro não pega isso.
    """
    tp = tp or _tileset(PRIMARIO)
    ts = ts or _tileset(SECUNDARIO)
    f = FAMILIAS[nome_fam]
    banda = set()
    for t in (f["a"], f["b"]):
        banda |= (_indices_do_tile(t, tp, ts) or set())
    cores = (tp if f["pal"] < 6 else ts)["paletas"][f["pal"]]
    ok = {i for i in range(1, 16)
          if min(_dist_cor(cores[i], cores[j]) for j in banda) <= BANDA_COR}
    return banda, ok


# ---------------------------------------------------------------------- o KIT
def desenha_kit():
    """(tiles_novos, metas, attrs, catalogo), sem escrever em disco."""
    dados = kit_lp()
    tp, ts = _tileset(PRIMARIO), _tileset(SECUNDARIO)
    import render_maps as RM

    por_peca = {p["nome"]: p for p in dados["pecas"]}
    tiles_novos, mapa_tile = {}, {}
    vagas_tile = _vagas_de_tile()
    proximo = [0]
    metas, attrs = {}, {}
    vagas_meta = _locais_livres()
    proximo_meta = [0]
    catalogo = dict(chao={}, moveis={}, cercas={}, remendos={}, sobre={},
                    cortados={})

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

    def entrada_lp(p, q):
        ch = p["usadas"][q]
        if ch is None:
            return 0
        v = p["ents"][q]
        _idx, ip = ch.split(":")
        alvo_pal = VAGAS_PAL[int(ip)]
        return ((v & 0x0C00) | (512 + vaga(ch)) | (alvo_pal << 12))

    # ----------------------------------------------- 0. o carimbo de cada família
    BASE = {}
    for nome_fam in FAMILIAS:
        BASE[nome_fam] = chao_da_familia(nome_fam, tp, ts)
        fam = FAMILIAS[nome_fam]
        # os NOVE GÊMEOS têm que ser gêmeos mesmo: se um dia deixarem de ser, o
        # kit para aqui em vez de escrever variante de um chão que não existe.
        canon = ents_nossas(fam["canonico"], tp, ts)
        for mt in fam["ids"]:
            if ents_nossas(mt, tp, ts) != canon:
                raise SystemExit("o metatile %d da familia %s nao e igual ao "
                                 "canonico %d" % (mt, nome_fam, fam["canonico"]))
            if attr_nosso(mt) != BASE[nome_fam][1]:
                raise SystemExit("o metatile %d da familia %s tem atributo "
                                 "0x%04X e o canonico tem 0x%04X"
                                 % (mt, nome_fam, attr_nosso(mt),
                                    BASE[nome_fam][1]))

    px_carimbo = {f: px_metatile(ents_nossas(FAMILIAS[f]["canonico"], tp, ts),
                                 tp, ts) for f in FAMILIAS}

    def monta(nome_fam, quads):
        """As oito entradas de uma variante da família, com a estrutura do
        carimbo: em COVERED o carimbo duplica a camada de baixo na de cima."""
        _b, _a, dupe = BASE[nome_fam]
        pal = FAMILIAS[nome_fam]["pal"]
        baixo = [_quad(t, f, pal) for (t, f) in quads]
        return baixo + (list(baixo) if dupe else [0, 0, 0, 0])

    # -------------------------------------------- 1. CHÃO: arranjos e texturas
    for nome_fam, fam in FAMILIAS.items():
        _b, attr_fam, _d = BASE[nome_fam]
        tiles = {"a": fam["a"], "b": fam["b"]}
        vivos, cortados = [], []
        pix_fica = [px_metatile(monta(nome_fam,
                                      [(tiles[k], f) for (k, f) in ARRANJOS[0][1]]),
                                tp, ts)]
        for nome_arr, quads in ARRANJOS[1:]:
            q = [(tiles[k], f) for (k, f) in quads]
            p = px_metatile(monta(nome_fam, q), tp, ts)
            s = _simetrico(p)
            if s:
                cortados.append(("%s %s (simetria %s)" % (nome_fam, nome_arr, s),
                                 0.0))
                continue
            pior = min(_dist_pixels(p, o) for o in pix_fica)
            if pior < PISO_VARIANTE:
                cortados.append(("%s %s" % (nome_fam, nome_arr), pior))
                continue
            pix_fica.append(p)
            vivos.append(("%s %s" % (nome_fam, nome_arr), q))
        _banda, admitidos = indices_da_familia(nome_fam, tp, ts)
        for nome_tex, quads in _lista_texturas(nome_fam):
            for (t, _f) in quads:
                if t < 512 and t in PINOS_PRIMARIO:
                    raise SystemExit("a textura %s usa o tile %d, que a animacao "
                                     "do primario reescreve" % (nome_tex, t))
                fora = (_indices_do_tile(t, tp, ts) or set()) - admitidos
                if fora:
                    raise SystemExit("a textura %s usa o tile %d, que acende os "
                                     "indices %s fora da banda de cor de %s"
                                     % (nome_tex, t, sorted(fora), nome_fam))
            p = px_metatile(monta(nome_fam, quads), tp, ts)
            s = _simetrico(p)
            if s:
                cortados.append((nome_tex + " (simetria " + s + ")", 0.0))
                continue
            pior = min(_dist_pixels(p, o) for o in pix_fica)
            if pior < PISO_VARIANTE:
                cortados.append((nome_tex, pior))
                continue
            dc = _dist_cor(_cor_media(p), _cor_media(px_carimbo[nome_fam]))
            if dc > TETO_COR:
                cortados.append((nome_tex + " (cor)", dc))
                continue
            pix_fica.append(p)
            vivos.append((nome_tex, quads))
        for nome_v, quads in vivos:
            catalogo["chao"][nome_v] = poe(monta(nome_fam, quads), attr_fam)
            catalogo["sobre"][nome_v] = nome_fam
        catalogo["cortados"][nome_fam] = cortados

    # ---------------------------------------------------- 2. os REMENDOS de grama
    _b, attr_grama, dupe_grama = BASE["grama"]
    for nome_rem, rem in REMENDOS.items():
        auto = list(rem["auto"])
        fill = rem["fill"]
        if fill is None:
            # o miolo do primário tem comportamento próprio: remonta o NOSSO
            ents = [_quad(rem["a"] if k in (0, 3) else rem["b"], 0, rem["pal"])
                    for k in range(4)]
            fill = poe(ents + ([0, 0, 0, 0] if not dupe_grama else list(ents)),
                       attr_grama)
            auto[4] = fill
        # todas as nove peças têm que carregar o atributo da GRAMA, senão o
        # remendo troca (comportamento, layerType) de célula andável
        for mt in auto:
            a = attrs.get(mt - 512) if mt >= 512 and (mt - 512) in attrs \
                else attr_nosso(mt)
            if a != attr_grama:
                raise SystemExit("a peca %d do remendo %s tem atributo 0x%04X e "
                                 "a grama tem 0x%04X" % (mt, nome_rem, a,
                                                         attr_grama))
        # variantes do MIOLO, pelos mesmos nove arranjos
        tiles = {"a": rem["a"], "b": rem["b"]}
        pix_fica = [px_metatile(
            [_quad(tiles[k], f, rem["pal"]) for (k, f) in ARRANJOS[0][1]]
            + [0, 0, 0, 0], tp, ts)]
        var, cort = [], []
        for nome_arr, quads in ARRANJOS[1:]:
            e = [_quad(tiles[k], f, rem["pal"]) for (k, f) in quads] + [0, 0, 0, 0]
            p = px_metatile(e, tp, ts)
            s = _simetrico(p)
            if s:
                cort.append(("%s %s (simetria %s)" % (nome_rem, nome_arr, s), 0.0))
                continue
            pior = min(_dist_pixels(p, o) for o in pix_fica)
            if pior < PISO_VARIANTE:
                cort.append(("%s %s" % (nome_rem, nome_arr), pior))
                continue
            pix_fica.append(p)
            var.append(poe(e, attr_grama))
        catalogo["remendos"][nome_rem] = dict(auto=auto, fill=fill, var=var)
        catalogo["cortados"][nome_rem] = cort

    # -------------------------------------------- 3. MÓVEIS NOSSOS de 1 célula
    for m in MOVEIS_NOSSOS:
        base_ent, _a, _d = BASE[m["sobre"]]
        e = ents_nossas(m["de"], tp, ts)
        cima = list(e[4:])
        if not arte_em_cima(e, tp, ts):
            cima = list(e[:4])       # QUADRANTE DE BAIXO SOBE
        if not any(v & 0x3FF for v in cima):
            raise SystemExit("%s: o metatile %d nao tem arte" % (m["nome"],
                                                                 m["de"]))
        catalogo["moveis"][m["nome"]] = poe(list(base_ent) + cima, 0x1000)
        catalogo["sobre"][m["nome"]] = m["sobre"]

    # ------------------------------------------ 4. MÓVEIS IMPORTADOS de 1 célula
    for m in MOVEIS_LP:
        base_ent, _a, _d = BASE[m["sobre"]]
        p = por_peca[m["nome"]]
        cima = [entrada_lp(p, q) for q in range(4)]
        if not any(cima):
            raise SystemExit("%s: peca sem arte" % m["nome"])
        # comportamento ZERADO (nenhum id semântico é importado) e layerType
        # COVERED, que põe as duas camadas ABAIXO do sprite.
        catalogo["moveis"][m["nome"]] = poe(list(base_ent) + cima, 0x1000)
        catalogo["sobre"][m["nome"]] = m["sobre"]

    # ----------------------------------------------------------- 5. as CERCAS
    for c in CERCAS:
        base_ent, _a, _d = BASE[c["sobre"]]
        nova = dict(nome=c["nome"], sobre=c["sobre"])
        if c.get("de_movel"):
            # corrida feita de MÓVEIS já montados neste kit
            for papel, nome_m in zip(("esq", "meio", "dir"), c["de_movel"]):
                nova[papel] = catalogo["moveis"][nome_m]
            catalogo["cercas"][c["nome"]] = nova
            continue
        for papel in ("esq", "meio", "dir"):
            mt = c[papel]
            if c["direto"]:
                # a camada de baixo dele JÁ é o carimbo da família e ele JÁ é
                # COVERED: custo zero
                e = ents_nossas(mt, tp, ts)
                if e[:4] != list(base_ent) or (attr_nosso(mt) >> 12) & 0xF != 1:
                    raise SystemExit("a cerca %s: o metatile %d nao serve direto"
                                     % (c["nome"], mt))
                nova[papel] = mt
            else:
                e = ents_nossas(mt, tp, ts)
                cima = list(e[4:]) if arte_em_cima(e, tp, ts) else list(e[:4])
                nova[papel] = poe(list(base_ent) + cima, 0x1000)
        catalogo["cercas"][c["nome"]] = nova

    if tiles_novos and max(tiles_novos) >= TETO_TILES:
        raise SystemExit("o kit estoura o teto de %d tiles" % TETO_TILES)

    # A vaga de metatile só serve se NENHUM dos dez mapas vivos usar o id.
    guardado = carrega_plano()
    usados = set()
    for nome in IRMAOS:
        grade = base_de(nome, guardado) if nome == ALVO else G.grade(nome)[4]
        usados |= {c & 0x3FF for c in grade}
    for local in metas:
        if 512 + local in usados:
            raise SystemExit("algum dos dez mapas usa o metatile %d"
                             % (512 + local))
    return tiles_novos, metas, attrs, catalogo


def grava_tileset(tiles_novos, metas, attrs):
    """Escreve tiles.png, palettes/*.pal, metatiles.bin e metatile_attributes.bin.

    Idempotente: as vagas de tile, de paleta e de metatile são FIXAS.

    A ARMADILHA DO `Image.convert("P")`: numa imagem que JÁ é "P" ele devolve uma
    CÓPIA e não converte, e uma frente desta onda gravou metatiles e NENHUM tile
    por causa disso. Aqui a imagem nova nasce em "P" e recebe a paleta da antiga.
    """
    from PIL import Image
    dados = kit_lp()
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
    alvo_m = (max(metas) + 1) if metas else 0
    meta += bytes(max(0, alvo_m * 16 - len(meta)))
    attr += bytes(max(0, alvo_m * 2 - len(attr)))
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


# ------------------------------------------------------------- o AUTOTILE
def abre(regiao):
    """ABERTURA morfológica 3x3: só fica a célula que cabe dentro de um quadrado
    3x3 inteiramente na região.

    É ela que garante que o autotile de NOVE peças dá conta: toda célula que
    sobra tem vizinho ao norte OU ao sul e vizinho a leste OU a oeste, então
    nunca cai o caso "sem norte e sem sul", que precisaria de uma décima peça que
    o `gTileset_General` não desenhou.
    """
    regiao = set(regiao)
    quadrados = [(x, y) for (x, y) in regiao
                 if all((x + dx, y + dy) in regiao
                        for dx in (-1, 0, 1) for dy in (-1, 0, 1))]
    fora = set()
    for x, y in quadrados:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                fora.add((x + dx, y + dy))
    return fora & regiao


def peca_autotile(auto, regiao, x, y):
    """A peça do autotile para (x,y), pela vizinhança DENTRO da região.

    Canto reentrante (as quatro ortogonais na região e uma diagonal fora) cai no
    MIOLO, e isso é escolha consciente: o autotile do `gTileset_General` tem nove
    peças e não tem canto interno, exatamente como o Emerald original.
    """
    n = (x, y - 1) in regiao
    s = (x, y + 1) in regiao
    o = (x - 1, y) in regiao
    l = (x + 1, y) in regiao
    if not n and not s:
        raise SystemExit("celula (%d,%d) sem norte e sem sul: a abertura falhou"
                         % (x, y))
    if not o and not l:
        raise SystemExit("celula (%d,%d) sem leste e sem oeste: a abertura falhou"
                         % (x, y))
    lin = 0 if not n else (2 if not s else 1)
    col = 0 if not o else (2 if not l else 1)
    return auto[lin * 3 + col], (lin, col)


def retangulos(livres, spec, perto=None):
    """[(x0,y0,w,h)] de retângulos disjuntos e afastados dentro de `livres`.

    Retângulo, e não bolha, e a razão é a arte: pintado com o autotile de nove
    peças, um retângulo sai na tela com CANTO ARREDONDADO e franja em volta, que
    é como o Emerald desenha remendo de chão. Bolha de contorno livre produz
    canto reentrante, e canto reentrante não tem peça.
    """
    ordem = sorted(livres, key=lambda p: _mistura(p[0], p[1],
                                                  spec.get("semente", 0)))
    postos, saida = [], []
    lw, hw = spec["larg"]
    lh, hh = spec["alt"]
    for x0, y0 in ordem:
        if len(saida) >= spec["quantos"]:
            break
        w = lw + _mistura(x0, y0, 0xB10B) % (hw - lw + 1)
        h = lh + _mistura(x0, y0, 0xC0DE) % (hh - lh + 1)
        cels = [(x0 + i, y0 + j) for i in range(w) for j in range(h)]
        if any(c not in livres for c in cels):
            continue
        if any(max(abs(cx - px), abs(cy - py)) < spec["espaco"]
               for cx, cy in cels for px, py in postos):
            continue
        # `perto` é o que faz a praia ser praia: o remendo de AREAL só vale se
        # encostar numa célula de areia ou de maresia. Sem isso o gerador
        # espalharia areia no meio do gramado urbano, que lê como buraco.
        if perto is not None and not any(
                max(abs(cx - px), abs(cy - py)) <= spec.get("raio", 3)
                for cx, cy in cels for px, py in perto):
            continue
        postos += cels
        saida.append((x0, y0, w, h))
    return saida


# ------------------------------------------------------ os CORREDORES da suíte
def corredores_multinivel(v, W, H, d):
    """Os corredores da suíte, refeitos com a regra da ELEVAÇÃO 15.

    O `enfeita_cidades.corredores_de_teste` simula a caminhada com a regra
    "elevação 0 é curinga e o resto exige igualdade". Essa regra ignora a
    elevação 15 (`ELEVATION_MULTI_LEVEL`), que MANTÉM a elevação do jogador. As
    duas rodam, e a união é barata.
    """
    pasta = f"{RAIZ}/dev_scripts/testes_criticos"
    nome_mapa = "MAP_" + re.sub(r"(?<!^)(?=[A-Z])", "_",
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
            continue
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


# ----------------------------------------------------------- ligação a pé
def componentes(v, W, H):
    """{célula: rótulo} dos pedaços de chão andável ligados a pé."""
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
    """Nenhum pedaço de chão se PARTIU, e nenhum se juntou a outro."""
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


def _encosta(cels, grade, W, H, beh, AG):
    """MÓVEL DE BEIRA: encosta num sólido, na água ou na borda do mapa."""
    for x, y in cels:
        for dx, dy in N4:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < W and 0 <= ny < H):
                return True
            j = ny * W + nx
            if (grade[j] >> 10) & 3:
                return True
            if beh(grade[j] & 0x3FF) in AG:
                return True
    return False


# ---------------------------------------------------------------- o PLANO
def plano_mapa(catalogo, base=None):
    """(L, W, H, v, escritas, contas, regioes) para `LilycoveCity`."""
    d, L, W, H, v0 = G.grade(ALVO)
    v = list(base) if base is not None else list(v0)
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()

    def andavel(i):
        return not ((v[i] >> 10) & 3)

    # As TRÊS famílias tratadas. Uma célula só é elegível se ainda for um dos ids
    # do carimbo, se for andável e se não for ÁGUA para o motor. O filtro de água
    # é o que protege a beira do mar.
    fam = {}
    for nome_fam, f in FAMILIAS.items():
        ids = set(f["ids"])
        fam[nome_fam] = {(i % W, i // W) for i in range(W * H)
                         if andavel(i) and (v[i] & 0x3FF) in ids
                         and beh(v[i] & 0x3FF) not in AG}
    de_familia = {}
    for nome_fam, cels in fam.items():
        for p in cels:
            de_familia[p] = nome_fam

    # A MARESIA, que esta passada NÃO toca: guardada aqui para o portão.
    maresia = {(i % W, i // W) for i in range(W * H)
               if (beh(v[i] & 0x3FF) & 0xFF) == 0x17}
    agua = {(i % W, i // W) for i in range(W * H) if beh(v[i] & 0x3FF) in AG}
    # `perto` do remendo de AREAL: praia (areia) ou maresia.
    orla = fam["areia"] | maresia

    escritas = {}
    aplicado = list(v)
    # DOIS congelamentos. `gelo` (evento com folga de uma célula, corredor da
    # suíte com as duas regras de elevação) proíbe SOLIDIFICAR. `gelo_chao` é bem
    # menor de propósito: trocar o DESENHO do chão não muda colisão, elevação nem
    # comportamento, então não encurta perna de teste nem tapa evento.
    ev, halo = E.congelado(d)
    gelo = set(halo)
    gelo |= E.corredores_de_teste(ALVO, v, W, H, d)
    gelo |= corredores_multinivel(v, W, H, d)
    gelo_chao = set()
    for idx, _a, _n in E.carrega_plano().get(ALVO, {}).get("celulas", []):
        gelo_chao.add((idx % W, idx // W))
    gelo |= gelo_chao

    ini = E.partidas(d, W, H, v)
    antes_alc = E.alcance(v, W, H, ini)
    novos_solidos, postos = [], []
    conta_mov = collections.Counter()
    por_movel = collections.defaultdict(list)
    conta_chao = collections.Counter()
    conta_ruido = collections.Counter()
    regioes = []
    por_cerca = []
    conta_cerca = collections.Counter()

    def nao_liga(grade, x, y):
        """Os vizinhos andáveis de (x,y) ainda se falam sem passar por (x,y)?"""
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

    def livre(x, y, nome_fam):
        i = y * W + x
        if x < MARGEM or y < MARGEM or x >= W - MARGEM or y >= H - MARGEM:
            return False
        if (x, y) in gelo or i in escritas:
            return False
        if de_familia.get((x, y)) != nome_fam:
            return False
        return (aplicado[i] & 0x3FF) in set(FAMILIAS[nome_fam]["ids"])

    def tenta_solidificar(x, y, mt_id):
        i = y * W + x
        antigo = aplicado[i]
        aplicado[i] = (antigo & 0xF000) | (1 << 10) | mt_id   # elevação INTACTA
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

    # ------------------------------------------------------------ 1. as CERCAS
    # Vêm primeiro porque precisam de uma corrida inteira de células e a mobília
    # solta não pode ter comido o meio dela.
    for c in CERCAS:
        alvo_q = CIDADE["cercas"].get(c["nome"])
        if not alvo_q:
            continue
        quantas, comp_lo, comp_hi, espaco = alvo_q
        peca = catalogo["cercas"][c["nome"]]
        for x, y in ordem_cel:
            if conta_cerca[c["nome"]] >= quantas:
                break
            comp = comp_lo + _mistura(x, y, 0xFEE1) % (comp_hi - comp_lo + 1)
            cels = [(x + k, y) for k in range(comp)]
            if any(not livre(cx, cy, c["sobre"]) for cx, cy in cels):
                continue
            if any(max(abs(cx - px), abs(cy - py)) < espaco
                   for cx, cy in cels for px, py in por_cerca):
                continue
            if any(max(abs(cx - px), abs(cy - py)) < ESPACO_ENTRE_MOVEIS
                   for cx, cy in cels for px, py in postos):
                continue
            if not _encosta(cels, aplicado, W, H, beh, AG):
                continue
            ok = True
            for k, (cx, cy) in enumerate(cels):
                mt = peca["esq"] if k == 0 else (peca["dir"] if k == comp - 1
                                                 else peca["meio"])
                if not tenta_solidificar(cx, cy, mt):
                    ok = False
                    break
            if not ok:
                for cx, cy in cels:
                    if (cx, cy) in novos_solidos:
                        novos_solidos.remove((cx, cy))
                        postos.remove((cx, cy))
                        del escritas[cy * W + cx]
                        aplicado[cy * W + cx] = v[cy * W + cx]
                continue
            por_cerca += cels
            conta_cerca[c["nome"]] += 1

    # ---------------------------------------------------------- 2. a MOBÍLIA
    # Ela vem ANTES da mancha de propósito: móvel posto no carimbo tira uma
    # célula do numerador E do denominador da régua; móvel posto em cima de uma
    # mancha tira só do denominador, o que PIORA a conta.
    lista = MOVEIS_NOSSOS + MOVEIS_LP
    for x, y in ordem_cel:
        giro = ((x * 73856093) ^ (y * 19349663)) % len(lista)
        for k in range(len(lista)):
            m = lista[(giro + k) % len(lista)]
            # peça que não está na lista da cidade é peça de CORRIDA (a
            # amarração), e ela não entra solta.
            if m["nome"] not in CIDADE["moveis"]:
                continue
            q, espaco = CIDADE["moveis"][m["nome"]]
            if conta_mov[m["nome"]] >= q:
                continue
            if not livre(x, y, m["sobre"]):
                continue
            if any(max(abs(x - px), abs(y - py)) < ESPACO_ENTRE_MOVEIS
                   for px, py in postos):
                continue
            if any(max(abs(x - px), abs(y - py)) < espaco
                   for px, py in por_movel[m["nome"]]):
                continue
            if not _encosta([(x, y)], aplicado, W, H, beh, AG):
                continue
            if not tenta_solidificar(x, y, catalogo["moveis"][m["nome"]]):
                continue
            por_movel[m["nome"]].append((x, y))
            conta_mov[m["nome"]] += 1
            break

    # ------------------------------------------------------- 3. os REMENDOS
    def pintavel(p):
        i = p[1] * W + p[0]
        return (de_familia.get(p) == "grama" and i not in escritas
                and (aplicado[i] & 0x3FF) in set(FAMILIAS["grama"]["ids"]))

    def pinta_regiao(nome_rem, celulas):
        rem = catalogo["remendos"][nome_rem]
        celulas = abre({p for p in celulas if pintavel(p)})
        if not celulas:
            return None
        escolha_miolo = [rem["fill"]] + rem["var"]
        for p in sorted(celulas):
            mt_id, (lin, col) = peca_autotile(rem["auto"], celulas, p[0], p[1])
            if (lin, col) == (1, 1):
                # o MIOLO recebe os arranjos do remendo, e não o fill puro: sem
                # isso o miolo vira o carimbo novo e a régua não anda.
                mt_id = escolha_miolo[_mistura(p[0], p[1],
                                               0xA5A5 + len(escolha_miolo))
                                      % len(escolha_miolo)]
            i = p[1] * W + p[0]
            escritas[i] = (aplicado[i] & 0xFC00) | mt_id
            aplicado[i] = escritas[i]
            conta_chao[nome_rem] += 1
        return dict(remendo=nome_rem, celulas=sorted(celulas))

    for spec in CIDADE["remendos"]:
        livres = {p for p in fam["grama"] if pintavel(p) and p not in gelo_chao}
        perto = orla if spec.get("perto") == "orla" else None
        for (x0, y0, w, h) in retangulos(livres, spec, perto):
            r = pinta_regiao(spec["remendo"],
                             {(x0 + i, y0 + j) for i in range(w)
                              for j in range(h)})
            if r:
                regioes.append(r)

    # ------------------------------------------------ 4. o RUÍDO de arranjo
    # O que sobrou do carimbo de cada família troca de desenho por hash da
    # posição. É a camada SUTIL: ela quebra a repetição de dezesseis pixels e não
    # muda o desenho da cidade.
    for nome_fam, f in FAMILIAS.items():
        var = [g for n, g in catalogo["chao"].items()
               if catalogo["sobre"][n] == nome_fam]
        for mt_origem in f["ids"]:
            escolha = [mt_origem] + var
            for i in range(W * H):
                if not andavel(i) or i in escritas:
                    continue
                if (aplicado[i] & 0x3FF) != mt_origem:
                    continue
                if de_familia.get((i % W, i // W)) != nome_fam:
                    continue
                if (i % W, i // W) in gelo_chao:
                    continue
                x, y = i % W, i // W
                mt_id = escolha[_mistura(x, y, 0x5EED + mt_origem) % len(escolha)]
                if mt_id == mt_origem:
                    continue
                escritas[i] = (aplicado[i] & 0xFC00) | mt_id
                aplicado[i] = escritas[i]
                conta_ruido[nome_fam] += 1

    # -------------------------------------------------------------- PORTÕES
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

    contas = dict(moveis=dict(conta_mov), cercas=dict(conta_cerca),
                  chao=dict(conta_chao), ruido=dict(conta_ruido),
                  solidos=len(novos_solidos), regioes=len(regioes),
                  familias={k: len(s) for k, s in fam.items()},
                  maresia=len(maresia), agua=len(agua))
    return L, W, H, v, escritas, contas, regioes


def regua(v, W, H, L, escritas=None):
    """(carimbo dominante em %, células andáveis a pé, id do carimbo), como a
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
    """A grade como está no disco, só tirando o que ESTA passada escreveu."""
    v = list(G.grade(alvo)[4])
    for idx, antigo, novo in guardado.get(alvo, {}).get("celulas", []):
        if v[idx] == novo:
            v[idx] = antigo
    return v


def roda(aplicar):
    tiles_novos, metas, attrs, catalogo = desenha_kit()
    print("kit: %d tiles novos (vagas %d a %d de %d, sobram %d), %d metatiles "
          "novos (locais %d a %d, ids %d a %d)"
          % (len(tiles_novos), min(tiles_novos), max(tiles_novos), TETO_TILES,
             TETO_TILES - max(tiles_novos) - 1, len(metas), min(metas),
             max(metas), 512 + min(metas), 512 + max(metas)))
    for nome, cort in sorted(catalogo["cortados"].items()):
        if cort:
            print("  %-8s %d variantes cortadas pela regua (%s)"
                  % (nome, len(cort),
                     ", ".join("%s %.1f" % c for c in cort[:3])))
    if aplicar:
        grava_tileset(tiles_novos, metas, attrs)
    guardado = carrega_plano()
    base = base_de(ALVO, guardado)
    L, W, H, v, escritas, contas, _r = plano_mapa(catalogo, base)
    a, na, ida = regua(v, W, H, L)
    b, nb, idb = regua(v, W, H, L, escritas)
    print("%s: %d celulas mudadas, %d solidificadas, %d regioes de remendo"
          % (ALVO, len(escritas), contas["solidos"], contas["regioes"]))
    print("  familias: " + ", ".join("%s %d" % kv
                                     for kv in sorted(contas["familias"].items()))
          + " | maresia %d (INTOCADA), agua %d (INTOCADA)"
          % (contas["maresia"], contas["agua"]))
    print("  remendo: " + ", ".join("%s x%d" % kv
                                    for kv in sorted(contas["chao"].items())))
    print("  ruido:   " + ", ".join("%s x%d" % kv
                                    for kv in sorted(contas["ruido"].items())))
    print("  movel:   " + ", ".join("%s x%d" % kv
                                    for kv in sorted(contas["moveis"].items())))
    print("  cerca:   " + ", ".join("%s x%d" % kv
                                    for kv in sorted(contas["cercas"].items())))
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
def confere(tiles_novos, metas, attrs, catalogo, plano):
    """Todas as regras desta onda, medidas sobre os dados que vierem.

    Ela é chamada DUAS vezes pelo auto-teste: uma com o plano de verdade, que tem
    que sair sem queixa, e uma por sabotagem, que tem que sair com a queixa
    certa. Regra conferida só no caminho feliz não é regra.
    """
    mau = []
    dados = kit_lp()
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

    def opacos_de(gid, cam):
        op = 0
        for e in entradas(gid)[cam * 4:cam * 4 + 4]:
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

    # ---------- 3. CHÃO: atributo idêntico ao da família, estrutura do carimbo,
    # camada de baixo CHEIA quando o layerType é NORMAL, e cor perto do carimbo
    px_carimbo = {f: px_de(FAMILIAS[f]["canonico"]) for f in FAMILIAS}
    for nome, gid in catalogo["chao"].items():
        nome_fam = catalogo["sobre"][nome]
        _b, attr_fam, dupe = chao_da_familia(nome_fam, tp, ts)
        if atributo(gid) != attr_fam:
            mau.append("o chao %s (%d) tem atributo 0x%04X e o carimbo de %s tem "
                       "0x%04X" % (nome, gid, atributo(gid), nome_fam, attr_fam))
        e = entradas(gid)
        if dupe and e[4:] != e[:4]:
            mau.append("o chao %s (%d) nao duplica a camada de baixo na de cima, "
                       "como o carimbo de %s faz" % (nome, gid, nome_fam))
        if not dupe and any(vv & 0x3FF for vv in e[4:]):
            mau.append("o chao %s (%d) tem arte na camada de CIMA e o carimbo de "
                       "%s e NORMAL: ela desenharia acima do jogador"
                       % (nome, gid, nome_fam))
        # `METATILE_LAYER_TYPE_NORMAL` desenha LIXO no BG3 e põe a camada de
        # BAIXO no BG2: camada de baixo com buraco deixa o lixo aparecer.
        if opacos_de(gid, 0) != 4 * 64:
            mau.append("o chao %s (%d) tem camada de baixo com buraco" % (nome, gid))
        dc = _dist_cor(_cor_media(px_de(gid)), _cor_media(px_carimbo[nome_fam]))
        if dc > TETO_COR:
            mau.append("o chao %s (%d) esta a %.1f de cor do carimbo de %s, "
                       "acima do teto de %.1f" % (nome, gid, dc, nome_fam,
                                                  TETO_COR))
        # 3c. SIMETRIA: chão não é simétrico. Ver `_simetrico()`.
        s = _simetrico(px_de(gid))
        if s:
            mau.append("o chao %s (%d) e simetrico em %s: espelho de quatro "
                       "dobras vira ornamento, nao grao de chao"
                       % (nome, gid, s))
        # 3b. o portão POR ÍNDICE. A média acima engole pixel: quatro pixels
        # azuis em sessenta de areia não movem a média e aparecem na tela.
        _banda, admitidos = indices_da_familia(nome_fam, tp, ts)
        for e in entradas(gid):
            t = e & 0x3FF
            if not t:
                continue
            fora = (_indices_do_tile(t, tp, ts) or set()) - admitidos
            if fora:
                mau.append("o chao %s (%d) acende os indices %s, fora da banda "
                           "de cor de %s: sao pixels de outra coisa"
                           % (nome, gid, sorted(fora), nome_fam))
                break

    # ---------- 4. REMENDO: as nove peças com o atributo da GRAMA
    _b, attr_grama, _d = chao_da_familia("grama", tp, ts)
    for nome_rem, rem in catalogo["remendos"].items():
        for mt in list(rem["auto"]) + [rem["fill"]] + rem["var"]:
            if atributo(mt) != attr_grama:
                mau.append("a peca %d do remendo %s tem atributo 0x%04X e a "
                           "grama tem 0x%04X" % (mt, nome_rem, atributo(mt),
                                                 attr_grama))
            if opacos_de(mt, 0) != 4 * 64:
                mau.append("a peca %d do remendo %s tem camada de baixo com "
                           "buraco" % (mt, nome_rem))

    # ---------- 5. MÓVEL: COVERED, comportamento zerado, e o NOSSO chão embaixo
    for nome, gid in catalogo["moveis"].items():
        nome_fam = catalogo["sobre"][nome]
        base_ent, _a, _d = chao_da_familia(nome_fam, tp, ts)
        a = atributo(gid)
        if (a >> 12) & 0xF != 1:
            mau.append("o movel %s (%d) nao esta em COVERED" % (nome, gid))
        if a & 0xFF:
            mau.append("o movel %s (%d) importou comportamento 0x%02X da fonte"
                       % (nome, gid, a & 0xFF))
        if entradas(gid)[:4] != list(base_ent):
            mau.append("o movel %s (%d) nao tem o nosso chao de %s na camada de "
                       "baixo" % (nome, gid, nome_fam))
        if opacos_de(gid, 1) == 0:
            mau.append("o movel %s (%d) esta sem arte em cima" % (nome, gid))
    for nome, c in catalogo["cercas"].items():
        base_ent, _a, _d = chao_da_familia(c["sobre"], tp, ts)
        for papel in ("esq", "meio", "dir"):
            gid = c[papel]
            if (atributo(gid) >> 12) & 0xF != 1:
                mau.append("a cerca %s (%s, %d) nao esta em COVERED"
                           % (nome, papel, gid))
            if entradas(gid)[:4] != list(base_ent):
                mau.append("a cerca %s (%s, %d) nao tem o nosso chao de %s"
                           % (nome, papel, gid, c["sobre"]))

    # ---------- 6. nenhuma variante de chão é cópia pixel a pixel de outra
    for nome_fam in FAMILIAS:
        lista = [g for n, g in catalogo["chao"].items()
                 if catalogo["sobre"][n] == nome_fam]
        lista.append(FAMILIAS[nome_fam]["canonico"])
        pix = {mt: px_de(mt) for mt in lista}
        for i, a in enumerate(lista):
            for b in lista[i + 1:]:
                dd = _dist_pixels(pix[a], pix[b])
                if dd < PISO_VARIANTE:
                    mau.append("as variantes de chao %d e %d de %s tem distancia "
                               "%.1f, abaixo do piso de %.1f do varia_carimbo.py:"
                               " isso e enganar a regua"
                               % (a, b, nome_fam, dd, PISO_VARIANTE))

    # ---------------------------------------- 7 em diante: o plano, célula a célula
    L, W, H, v, escritas, contas, regioes = plano
    d = json.load(open(f"{RAIZ}/data/maps/{ALVO}/map.json"))
    ev = E.eventos(d)
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val
    meus_chaos = {g: n for n, g in catalogo["chao"].items()}
    meus_moveis = {g: n for n, g in catalogo["moveis"].items()}
    pecas_cerca = {}
    for nome, c in catalogo["cercas"].items():
        for papel in ("esq", "meio", "dir"):
            pecas_cerca[c[papel]] = (nome, c["sobre"])
    pecas_rem = {}
    for nome_rem, rem in catalogo["remendos"].items():
        for mt in list(rem["auto"]) + [rem["fill"]] + rem["var"]:
            pecas_rem[mt] = nome_rem
    ids_de = {}
    for nome_fam, f in FAMILIAS.items():
        for mt in f["ids"]:
            ids_de[mt] = nome_fam

    for i, val in escritas.items():
        x, y = i % W, i // W
        novo, velho = val & 0x3FF, v[i] & 0x3FF
        cn, cv = (val >> 10) & 3, (v[i] >> 10) & 3
        if (val >> 12) & 0xF != (v[i] >> 12) & 0xF:
            mau.append("%s: mudou ELEVACAO em (%d,%d)" % (ALVO, x, y))
        if cv and not cn:
            mau.append("%s: colisao 1 -> 0 em (%d,%d), que segue proibida"
                       % (ALVO, x, y))
        if velho not in ids_de:
            mau.append("%s: escreveu em (%d,%d), que nao era carimbo de familia "
                       "nenhuma (metatile %d)" % (ALVO, x, y, velho))
            continue
        if novo in meus_chaos:
            if cn != cv or ids_de[velho] != catalogo["sobre"][meus_chaos[novo]]:
                mau.append("%s: chao de %s em celula de %s em (%d,%d)"
                           % (ALVO, catalogo["sobre"][meus_chaos[novo]],
                              ids_de[velho], x, y))
        elif novo in pecas_rem:
            if cn != cv or ids_de[velho] != "grama":
                mau.append("%s: remendo fora da grama em (%d,%d)" % (ALVO, x, y))
        elif novo in meus_moveis:
            nome = meus_moveis[novo]
            if cv or not cn:
                mau.append("%s: movel em (%d,%d) nao e solidificacao 0 -> 1"
                           % (ALVO, x, y))
            if ids_de[velho] != catalogo["sobre"][nome]:
                mau.append("%s: movel de %s fora da familia dele em (%d,%d)"
                           % (ALVO, catalogo["sobre"][nome], x, y))
            if (x, y) in ev:
                mau.append("%s: movel em cima do evento (%d,%d)" % (ALVO, x, y))
        elif novo in pecas_cerca:
            nome, sobre = pecas_cerca[novo]
            if cv or not cn:
                mau.append("%s: cerca em (%d,%d) nao e solidificacao 0 -> 1"
                           % (ALVO, x, y))
            if ids_de[velho] != sobre:
                mau.append("%s: cerca de %s fora da familia dela em (%d,%d)"
                           % (ALVO, sobre, x, y))
        else:
            mau.append("%s: metatile %d escrito em (%d,%d) e de fora do kit"
                       % (ALVO, novo, x, y))

    # 8. (comportamento, layerType) de toda célula ANDÁVEL fica igual
    for i in range(W * H):
        if (saida[i] >> 10) & 3:
            continue
        a, b = atributo(v[i] & 0x3FF), atributo(saida[i] & 0x3FF)
        if (a & 0xFF, a & 0xF000) != (b & 0xFF, b & 0xF000):
            mau.append("%s: celula andavel (%d,%d) mudou (comportamento, "
                       "layerType)" % (ALVO, i % W, i // W))
            break

    # 9 e 10. alcance a pé e LIGAÇÃO a pé
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

    # 10b. A BEIRA DO MAR: o conjunto de células de ÁGUA é IDÊNTICO antes e
    # depois. É este o portão que garante que o alcance de Surf não mudou.
    def agua_de(grade):
        return {(i % W, i // W) for i in range(W * H)
                if beh(grade[i] & 0x3FF) in AG}
    if agua_de(v) != agua_de(saida):
        mau.append("%s: o conjunto de celulas de AGUA mudou, e com ele o alcance "
                   "de Surf" % ALVO)

    # 10c. A MARESIA não é tocada: nenhuma célula com comportamento 0x17 foi
    # escrita, nem antes nem depois. É o portão da decisão do cabeçalho.
    def maresia_de(grade):
        return {(i % W, i // W) for i in range(W * H)
                if (beh(grade[i] & 0x3FF) & 0xFF) == 0x17}
    if maresia_de(v) != maresia_de(saida):
        mau.append("%s: o conjunto de celulas de MARESIA mudou" % ALVO)
    for i in escritas:
        if (beh(v[i] & 0x3FF) & 0xFF) == 0x17:
            mau.append("%s: escreveu na maresia em (%d,%d), e esta passada nao "
                       "toca a orla" % (ALVO, i % W, i // W))
            break

    # 10d. NENHUM tile de chão pode sair de vaga PINADA do primário
    for nome, gid in catalogo["chao"].items():
        for e in entradas(gid):
            t = e & 0x3FF
            if t and t < 512 and t in PINOS_PRIMARIO:
                mau.append("o chao %s (%d) usa o tile %d, que a animacao do "
                           "primario reescreve em tempo de execucao"
                           % (nome, gid, t))
                break

    # 11. A MANCHA NÃO PODE SER ADIVINHÁVEL, e o teste tem dois lados.
    mancha = {(i % W, i // W): (val & 0x3FF) for i, val in escritas.items()
              if (val & 0x3FF) in meus_chaos or (val & 0x3FF) in pecas_rem}
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

    # 12. os REMENDOS têm que ser autotile de verdade: a peça de cada célula é a
    # que a vizinhança pede, e o miolo é o único que aceita variante.
    for r in regioes:
        rem = catalogo["remendos"][r["remendo"]]
        cels = set(map(tuple, r["celulas"]))
        miolo = set([rem["fill"]] + rem["var"])
        for p in cels:
            mt_id, (lin, col) = peca_autotile(rem["auto"], cels, p[0], p[1])
            posto = escritas[p[1] * W + p[0]] & 0x3FF
            if (lin, col) == (1, 1):
                if posto not in miolo:
                    mau.append("%s: o miolo do remendo em (%d,%d) nao e do "
                               "remendo %s" % (ALVO, p[0], p[1], r["remendo"]))
                    break
            elif posto != mt_id:
                mau.append("%s: a borda do remendo em (%d,%d) deveria ser o "
                           "metatile %d e e o %d"
                           % (ALVO, p[0], p[1], mt_id, posto))
                break

    # 13. a régua tem que fechar em 20% ou menos
    b, nb, idb = regua(v, W, H, L, escritas)
    if b > TETO_REGUA:
        mau.append("%s: a regua ainda marca %.1f%% de carimbo dominante"
                   % (ALVO, b))
    return mau


# ------------------------------------------------------------------ auto-teste
def demo():
    """Prova positiva e as provas NEGATIVAS, cada sabotagem revertida em seguida.

    "Zero diferenca" só vale depois que a comparação mostra que sabe reprovar.
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
        L, W, H, v, esc, ct, rg = plano
        return (dict(tiles_novos), dict(metas), dict(attrs),
                json.loads(json.dumps(catalogo)),
                (L, W, H, list(v), dict(esc), ct, json.loads(json.dumps(rg))))

    def chao_de(nome_fam, quantos=1):
        """Os primeiros chãos de uma família, em ordem estável. As sabotagens
        precisam escolher a família CERTA: uma família COVERED (a areia) não
        acusa "arte acima do jogador", porque nela o carimbo duplica a camada de
        baixo na de cima de propósito."""
        lista = [n for n in sorted(catalogo["chao"])
                 if catalogo["sobre"][n] == nome_fam]
        if len(lista) < quantos:
            raise SystemExit("a familia %s so tem %d chaos" % (nome_fam,
                                                               len(lista)))
        return lista[:quantos]

    um_chao, outro_chao = chao_de("grama", 2)
    chao_covered = chao_de("areia", 1)[0]

    # N1. colisão 1 -> 0 numa célula de mancha
    def n1():
        a = copia()
        L, W, H, v, esc, ct, rg = a[4]
        i = sorted(esc)[0]
        v[i] = v[i] | (1 << 10)
        return a
    sabota("colisao 1 -> 0", n1, "colisao 1 -> 0")

    # N2. elevação alterada
    def n2():
        a = copia()
        L, W, H, v, esc, ct, rg = a[4]
        i = sorted(esc)[0]
        esc[i] = (esc[i] & 0x0FFF) | (((v[i] >> 12) + 1) & 0xF) << 12
        return a
    sabota("elevacao alterada", n2, "mudou ELEVACAO")

    # N3. atributo de um metatile de CHÃO sabotado
    def n3():
        a = copia()
        gid = a[3]["chao"][um_chao]
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

    # N7. chão NORMAL com arte na camada de cima: desenharia acima do jogador
    def n7():
        a = copia()
        gid = a[3]["chao"][um_chao]
        e = list(a[1][gid - 512])
        e[4] = 0x2000 | 14
        a[1][gid - 512] = e
        return a
    sabota("arte de cima em chao NORMAL", n7, "acima do jogador")

    # N7b. chão COVERED que DEIXA de duplicar a camada de baixo na de cima
    def n7b():
        a = copia()
        gid = a[3]["chao"][chao_covered]
        e = list(a[1][gid - 512])
        e[4:] = [0, 0, 0, 0]
        a[1][gid - 512] = e
        return a
    sabota("chao COVERED sem a copia de cima", n7b, "nao duplica a camada")

    # N8. célula andável com (comportamento, layerType) trocado
    def n8():
        a = copia()
        gid = a[3]["chao"][um_chao]
        a[2][gid - 512] = 0x1000
        return a
    sabota("layerType de chao trocado", n8, "mudou (comportamento")

    # N9. um móvel plantado em cima de célula de EVENTO
    def n9():
        a = copia()
        L, W, H, v, esc, ct, rg = a[4]
        dd = json.load(open(f"{RAIZ}/data/maps/{ALVO}/map.json"))
        alvo_nome = MOVEIS_NOSSOS[0]["nome"]
        gid = a[3]["moveis"][alvo_nome]
        ids = set(FAMILIAS[a[3]["sobre"][alvo_nome]]["ids"])
        for x, y in sorted(E.eventos(dd)):
            i = y * W + x
            if (v[i] & 0x3FF) in ids and not ((v[i] >> 10) & 3):
                esc[i] = (v[i] & 0xF000) | (1 << 10) | gid
                return a
        raise SystemExit("nao ha evento em cima do carimbo para sabotar")
    sabota("movel em cima de evento", n9, "em cima do evento")

    # N10. duas variantes de chão IGUAIS pixel a pixel: é enganar a régua
    def n10():
        a = copia()
        gid_a = a[3]["chao"][um_chao]
        gid_b = a[3]["chao"][outro_chao]
        if a[3]["sobre"][um_chao] != a[3]["sobre"][outro_chao]:
            for n in sorted(a[3]["chao"]):
                if n != um_chao and a[3]["sobre"][n] == a[3]["sobre"][um_chao]:
                    gid_b = a[3]["chao"][n]
                    break
        a[1][gid_b - 512] = list(a[1][gid_a - 512])
        return a
    sabota("variante de chao duplicada", n10, "abaixo do piso de")

    # N11. cor nova escrita num índice que os NOSSOS pixels já usam
    def n11():
        a = copia()
        dados = kit_lp()
        alvo_vaga = None
        for vaga in range(6, 13):
            livres_v = set(dados["vagas_livres"].get(str(vaga)) or [])
            usados = [i for i in range(1, 16) if i not in livres_v]
            if usados and str(vaga) in dados["paletas"]:
                alvo_vaga, idx = str(vaga), usados[0]
                break
        if alvo_vaga is None:
            # nenhuma das vagas que este kit usa tem índice ocupado: sabota uma
            # que ele NÃO usa, declarando-a no kit
            for vaga in range(6, 13):
                livres_v = set(dados["vagas_livres"].get(str(vaga)) or [])
                usados = [i for i in range(1, 16) if i not in livres_v]
                if usados:
                    alvo_vaga, idx = str(vaga), usados[0]
                    dados["paletas"][alvo_vaga] = [
                        list(c) for c in ts_do_disco["paletas"][vaga]]
                    break
        if alvo_vaga is None:
            raise SystemExit("nao ha vaga com indice em uso para sabotar")
        pal = [list(c) for c in dados["paletas"][alvo_vaga]]
        pal[idx] = [255, 0, 255]
        dados["paletas"][alvo_vaga] = pal
        with open(KIT_JSON + ".sab", "w") as f:
            json.dump(dados, f)
        os.replace(KIT_JSON, KIT_JSON + ".bak")
        os.replace(KIT_JSON + ".sab", KIT_JSON)
        return a
    try:
        sabota("cor nova em indice ja usado", n11, "que algum pixel nosso usa")
    finally:
        if os.path.exists(KIT_JSON + ".bak"):
            os.replace(KIT_JSON + ".bak", KIT_JSON)

    # N12. gravar numa vaga de metatile que os mapas VIVOS usam
    def n12():
        a = copia()
        a[1][100] = list(a[1][min(a[1])])
        a[2][100] = 0x1000
        a[3]["chao"][um_chao] = 512 + 100
        return a
    sabota("grava em vaga de metatile viva", n12, "abaixo da primeira vaga livre")

    # N13. mexer numa célula de ÁGUA: o alcance de Surf mudaria
    def n13():
        a = copia()
        L, W, H, v, esc, ct, rg = a[4]
        beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
        AG = E.agua()
        gid = a[3]["chao"][um_chao]
        for i in range(W * H):
            if beh(v[i] & 0x3FF) in AG:
                esc[i] = (v[i] & 0xFC00) | gid
                return a
        raise SystemExit("o mapa nao tem celula de agua para sabotar")
    sabota("celula de agua trocada", n13, "alcance de Surf")

    # N14. mexer na MARESIA, que esta passada não toca
    def n14():
        a = copia()
        L, W, H, v, esc, ct, rg = a[4]
        beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
        gid = a[3]["chao"][um_chao]
        for i in range(W * H):
            if (beh(v[i] & 0x3FF) & 0xFF) == 0x17:
                esc[i] = (v[i] & 0xFC00) | gid
                return a
        raise SystemExit("o mapa nao tem maresia para sabotar")
    sabota("maresia trocada", n14, "escreveu na maresia")

    # N15. a BORDA do remendo trocada pelo MIOLO: nenhum outro portão pega isso
    def n15():
        a = copia()
        L, W, H, v, esc, ct, rg = a[4]
        for r in rg:
            rem = a[3]["remendos"][r["remendo"]]
            cels = set(map(tuple, r["celulas"]))
            for p in sorted(cels):
                _mt, (lin, col) = peca_autotile(rem["auto"], cels, p[0], p[1])
                if (lin, col) != (1, 1):
                    i = p[1] * W + p[0]
                    esc[i] = (esc[i] & 0xFC00) | rem["fill"]
                    return a
        raise SystemExit("nenhum remendo tem borda para sabotar")
    sabota("borda de remendo trocada pelo miolo", n15, "a borda do remendo")

    # N16. a mancha espalhada AO ACASO em vez de por região e por ruído: o
    # padrão por posição passaria a adivinhar a peça
    def n16():
        a = copia()
        L, W, H, v, esc, ct, rg = a[4]
        meus = set(a[3]["chao"].values())
        for i in list(esc):
            if (esc[i] & 0x3FF) in meus:
                lista = sorted(meus)
                esc[i] = (esc[i] & 0xFC00) | lista[(i % W) % len(lista)]
        return a
    sabota("mancha virou padrao de coluna", n16, "virou padrao")

    # N17. uma textura de chão trocada por um tile FORA da banda de cor da
    # família. É a sabotagem que reproduz o defeito que o render desta passada
    # pegou: média de cor não vê quatro pixels azuis em sessenta de areia.
    def n17():
        a = copia()
        tp, ts = _tileset(PRIMARIO), _tileset(SECUNDARIO)
        gid = a[3]["chao"][um_chao]
        _banda, admitidos = indices_da_familia("grama", tp, ts)
        alvo = None
        for t in range(1, 512):
            if t in PINOS_PRIMARIO:
                continue
            s = _indices_do_tile(t, tp, ts)
            if s and (s - admitidos):
                alvo = t
                break
        if alvo is None:
            raise SystemExit("nao ha tile fora da banda para sabotar")
        e = list(a[1][gid - 512])
        e[0] = (e[0] & 0xFC00) | alvo
        a[1][gid - 512] = e
        return a
    sabota("textura fora da banda de cor", n17, "fora da banda de cor")

    # N18. um chão montado com espelho de QUATRO DOBRAS, que é o defeito que a
    # praia desta passada mostrou no primeiro render: laço de gravata e anel.
    def n18():
        a = copia()
        gid = a[3]["chao"][um_chao]
        t = FAMILIAS["grama"]["texturas"][0]
        pal = FAMILIAS["grama"]["pal"]
        e = [_quad(t, f, pal) for f in range(4)]
        a[1][gid - 512] = e + [0, 0, 0, 0]
        return a
    sabota("chao com espelho de quatro dobras", n18, "e simetrico em")

    # ------------------------------------------------ o que está NO DISCO
    from PIL import Image
    meta_disco = _ler("metatiles.bin")
    attr_disco = _ler("metatile_attributes.bin")
    png = Image.open(f"{DESTINO}/tiles.png")
    cols = png.size[0] // 8
    px = png.load()

    postas = [l for l in metas if l * 16 + 16 <= len(meta_disco)
              and _entradas(meta_disco, l) == metas[l]]
    if not postas:
        print("aviso: o kit ainda nao foi aplicado no tileset; o caso de DISCO "
              "nao roda")
    else:
        if len(postas) != len(metas):
            mau.append("o kit esta pela metade no disco: %d de %d metatiles"
                       % (len(postas), len(metas)))
        for local, ents in metas.items():
            if local * 16 + 16 > len(meta_disco) or \
                    _entradas(meta_disco, local) != ents:
                mau.append("metatile %d no disco nao e o do kit" % (512 + local))
            elif struct.unpack_from("<H", attr_disco, local * 2)[0] != attrs[local]:
                mau.append("atributo do metatile %d no disco nao e o do kit"
                           % (512 + local))
        for vaga, tile in tiles_novos.items():
            if (vaga // cols) * 8 + 8 > png.size[1]:
                mau.append("a vaga de tile %d nao cabe no tiles.png" % vaga)
                continue
            x0, y0 = (vaga % cols) * 8, (vaga // cols) * 8
            if [[px[x0 + x, y0 + y] for x in range(8)] for y in range(8)] != tile:
                mau.append("o tile da vaga %d no disco nao e o do kit" % vaga)
        for vaga, cores in sorted(kit_lp()["paletas"].items()):
            arq = [l.split() for l in
                   open(f"{DESTINO}/palettes/%s.pal" % vaga.zfill(2)).read().split("\n")[3:]
                   if l.strip()]
            if [[int(z) for z in c] for c in arq[:16]] != cores:
                mau.append("a paleta %s no disco nao e a do kit" % vaga)

    # ------------------------------------------------------- idempotência
    L, W, H, v, escritas, contas, _rg = plano
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val
    volta = list(saida)
    for i in sorted(escritas):
        if volta[i] == escritas[i]:
            volta[i] = v[i]
    if volta != list(v):
        mau.append("%s: desfazer nao devolve a base" % ALVO)
    _, _, _, _, esc2, _, _ = plano_mapa(catalogo, volta)
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
    print("  %-14s %d celulas mudadas, %d solidificadas, regua %.1f%% (mt %d) -> "
          "%.1f%% (mt %d)" % (ALVO, len(escritas), contas["solidos"], a, ida,
                              b, idb))
    print("  %d tiles, %d metatiles, %d provas negativas:"
          % (len(tiles_novos), len(metas), len(negativas)))
    for nome, queixa in negativas:
        print("    %-38s -> %s" % (nome, queixa[:92]))
    return 0


# ------------------------------------------------- prova de TILE contra a ROM
def prova_tiles():
    """Cada tile do kit, DEPOIS de reindexado, contra o tile da ROM: zero pixel.

    Reindexar nibble é a única coisa que este kit faz com o desenho da fonte, e é
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
    dados = kit_lp()
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


# ------------------------------------------------------------------- LILYCOVE
CIDADE = dict(
    # os remendos: retângulos pintados com o autotile de nove peças, todos sobre
    # a GRAMA. O `areal` é o único condicionado: ele só vale encostado na orla.
    remendos=[
        dict(remendo="gasta", quantos=12, larg=(3, 6), alt=(3, 5), espaco=2,
             semente=0x202),
        dict(remendo="terra", quantos=6, larg=(3, 4), alt=(3, 3), espaco=2,
             semente=0x101),
        dict(remendo="areal", quantos=5, larg=(3, 5), alt=(3, 4), espaco=2,
             semente=0x303, perto="orla", raio=3),
        dict(remendo="gasta", quantos=10, larg=(3, 3), alt=(3, 3), espaco=2,
             semente=0x404),
    ],
    # (quantos, espaço mínimo entre duas cópias da MESMA peça)
    # (quantos, espaço mínimo entre duas cópias da MESMA peça)
    #
    # AS COTAS DO CALÇAMENTO SÃO DE UM, e isso é conta e não gosto. Medido nesta
    # árvore: a praça tem 275 células, 202 fora do gelo de evento e apenas **37
    # DE BEIRA** (encostadas num sólido, na água ou na borda). Cada peça posta
    # mata o anel de oito em volta dela, e as duas corridas de cerca do cais já
    # comem onze células. Com cota 2 ou 3 as primeiras da lista tomavam o espaço
    # e o quadro de avisos e a boia de sinalização não chegavam a aparecer: era
    # repetição no lugar de variedade, a mesma poda que Dewford fez. A praia tem
    # 32 células de beira e aceita duas de cada; o gramado tem 267 e aceita mais.
    moveis={
        "moita do parque": (7, 6), "arbusto": (7, 6), "arbusto largo": (6, 7),
        "touceira": (6, 7), "touceira espelhada": (6, 7),
        "placa do parque": (2, 14), "matacao": (5, 8),
        "poste de amarracao": (1, 6), "cabeco duplo": (1, 7),
        "guarda-corpo": (1, 8), "quadro de avisos": (1, 12),
        "boia de sinalizacao": (1, 8),
        "engradado azul": (1, 6), "rolo de cabo": (1, 7),
        "pedra da praia": (2, 6), "moita de praia": (2, 6),
        "engradado laranja": (2, 5), "tina do pescador": (2, 6),
        "tina laranja": (2, 6),
    },
    # nome da cerca -> (quantas, comprimento mínimo, máximo, espaço)
    cercas={"cerca do parque": (4, 3, 5, 8),
            "guarda-corpo do cais": (2, 3, 4, 10),
            "amarracao do cais": (1, 2, 2, 10)},
)


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
