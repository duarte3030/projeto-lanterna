#!/usr/bin/env python3
"""Refino de `SandgemTown` (tema PRAIA) e `TwinleafTown` (tema VILA DE BEIRA DE
LAGO), no `gTileset_PetalburgSinnoh`, com arte importada do `Pokémon Light
Platinum`.

O QUE ESTAS DUAS CIDADES TÊM DE ERRADO, medido pela `dev_scripts/regua_cidades.py`
nesta árvore em 08/09/2026: `TwinleafTown` gasta 47,3% do chão andável a pé (183
células de 387) com o metatile 1, a grama lisa do primário, e `SandgemTown` gasta
37,4% (182 de 486) com o mesmo metatile. Duas vilas com gramado chapado e um
caminho de areia igualmente chapado do começo ao fim.

DOIS CARIMBOS, e é aqui que esta passada difere de todas as anteriores da onda.
Em Snowpoint, Celestic, Solaceon, Oreburgh e Eterna havia UM tapete a quebrar. Em
Twinleaf e Sandgem há DOIS, e eles se revezam no topo da régua: a grama (metatile
1) com 47,3% e 37,4%, e a areia do caminho (metatile 289) com 17,6% e 26,7%.
Quebrar só o primeiro não fecha a régua, porque a régua mede o DOMINANTE e o
segundo assume o posto assim que o primeiro cai. Pior: solidificar célula tira do
denominador, então derrubar a grama chega a SUBIR a fração do que sobra. As duas
famílias são tratadas juntas, cada uma com o próprio catálogo, e as duas medidas
antes e depois.

A FONTE, e ela é uma só: `Pokémon Light Platinum`, de WesleyFG, base Ruby (AXVE),
md5 `7fd2c08735459d99fa23fdaa9b755486`, cópia privada em
`fontes-mapas/romhacks/light-platinum/`. O par é o primário de exterior `0x286CF4`
com o secundário `0x286D54`, que é a VILA COSTEIRA do hack (o mapa g00m01, 78x60,
com praia, coqueiro, guarda-sol e deque) e é TAMBÉM a vila verde do g00m37 (40x40,
gramado, caminho de areia, moita e banco). Esse duplo uso é a razão da escolha
entre os quatro secundários triados: os outros três pagam UM tema cada, e este
paga os DOIS, o que importa porque as duas cidades dividem o mesmo secundário
nosso e portanto o mesmo orçamento de paleta. O `--extrai` confere o md5 ANTES de
ler um byte e para se a cópia for outra. A ROM nunca entra no repositório: o que
está versionado é o kit CONVERTIDO, em `dev_scripts/costa_sandgem_kit.json`, com a
paleta em RGB e o tile em nibble já reindexado para a vaga nova.

O ORÇAMENTO DE PALETA, medido nesta árvore e não herdado de brief. `NUM_PALS_TOTAL`
é 13 (`include/fieldmap.h`): seis vagas do primário e SETE do secundário, da 6 à
12. Contando por metatile VIVO (os que aparecem em `map.bin` de algum dos 16
layouts vivos do tileset), as vagas em uso são 8, 9, 10 e 12, e as vagas 6, 7 e 11
não são usadas por pixel nenhum que chegue à tela. A armadilha 4 do
`compacta_paletas.py` foi conferida e NÃO existe aqui: nenhum metatile do PRIMÁRIO
alcançável nesses mapas pinta com vaga de secundário (zero entradas com paleta >= 6
nos 183 metatiles do primário que os 16 mapas usam). As três vagas estão livres de
verdade, e nenhuma compactação foi necessária.

    vaga  6   AREIA e TERRA   15 cores exatas, das paletas 5 e 3 do hack
    vaga  7   VERDE           12 cores, da paleta 2 do hack
    vaga 11   AZUL e BRANCO   11 cores, da paleta 0 do hack

A FUSÃO DAS PALETAS 5 E 3 NA VAGA 6 é o que faz o orçamento fechar, e ela foi
medida antes de ser escrita: a paleta 5 do hack (a areia) tem 7 cores nas peças
deste kit, a paleta 3 (a terra e a pedra) tem 9, e a união dá 15 EXATAS, que é
tudo que uma paleta de BG do GBA comporta. Nenhuma cor é aproximada: cada nibble é
reindexado para a tabela nova e o pixel sai idêntico ao da ROM.

O QUE FICOU DE FORA POR CAUSA DESSA CONTA, dito na cara: o guarda-sol LARANJA
(metatiles 133, 134, 141 e 135 do secundário) e a boia laranja (o 127). Os dois
usam a paleta 1 do hack, que pede 11 cores próprias, e não há quarta vaga: a união
da paleta 1 com qualquer uma das outras vai de 18 a 23 cores. Entre os dois
guarda-sóis ficou o AZUL, que é o que combina com o mar. Também ficou de fora o
toco de árvore do secundário (metatiles 104 e 105), que pede a paleta 10 do hack
com 11 cores: no lugar dele entram os pedregulhos que o NOSSO primário já tem
desenhados, o 224 sobre grama e o 226 sobre areia, que custam zero.

A GRAMA NÃO É IMPORTADA, e isso não é economia, é COR. A grama do Light Platinum
é (136,184,80), um verde amarelado, e a nossa é (115,197,164), um verde azulado:
90 de distância RGB, que numa mancha ao lado do carimbo vira remendo. A areia é
outra história: a do hack é (240,216,168) contra a nossa (222,206,132), 42 de
distância, que é a diferença entre areia seca e areia batida e é exatamente o que
uma praia tem. Por isso o catálogo de GRAMA desta passada é todo NOSSO (dez
metatiles do `gTileset_GeneralSinnoh` com o atributo IGUAL, bit a bit, ao do
metatile 1, mais oito espelhos horizontais deles) e o catálogo de AREIA é todo
IMPORTADO.

AS REGRAS DE MONTAGEM, e a armadilha que cada uma resolve:

  - CHÃO NOVO é metatile com arte só na camada de BAIXO e atributo IGUAL, bit a
    bit, ao do carimbo que ele substitui (0x0000 nos dois carimbos das duas
    cidades). Camada de cima em chão andável com layerType NORMAL desenharia
    ACIMA do jogador, e areia por cima do boneco é defeito, não enfeite. A única
    exceção são as peças NOSSAS de grama (tufo, moita), que desenham em cima de
    propósito desde o jogo base: é o "jogador atrás do mato". Mesmo elas pagam o
    portão do E3 do `mapas_qa.py`, que é não tapar o jogador INTEIRO.
  - MÓVEL é célula que vira SÓLIDA: a arte vai na camada de CIMA, a de baixo
    recebe o NOSSO chão entrada por entrada, e o atributo é comportamento ZERADO
    com layerType COVERED (0x1000), que põe as duas camadas ABAIXO do sprite.
  - CADA PEÇA SABE SOBRE QUAL CARIMBO ELA POUSA. O coqueiro e o guarda-sol pousam
    na AREIA e recebem a camada de baixo do metatile 289; a moita e o arbusto
    pousam na GRAMA e recebem a do metatile 1. Sem isso o coqueiro chegaria com um
    quadrado de grama em volta no meio da praia.
  - QUADRANTE DE BAIXO SOBE quando o de cima está vazio, que é a regra do
    `porto_canalave.py`: a fonte nem sempre desenha a peça na camada de cima.
  - O CHÃO DA FONTE NÃO ENTRA, e ele é achado por EVIDÊNCIA, não por constante
    decorada. São duas assinaturas, as duas medidas nesta rodada: (a) todo PADRÃO
    de camada de baixo que aparece em 4 ou mais metatiles DIFERENTES da fonte é
    piso dela, e cada tile daquele padrão vai para a lista; (b) camada de baixo
    que repete o MESMO tile nos quatro quadrantes também é piso. Juntas elas
    marcam 57 tiles no primário do hack e 62 no secundário, e pegam a grama
    (0x010, 0x011, 0x020, 0x021, 0x002, 0x003) e a areia (0x108, 0x118, 0x0A5,
    0x0A6, 0x0B5, 0x0B6) SEM pegar a sombra do coqueiro (0x20E), que é arte de
    verdade e precisa entrar na peça.
  - Nenhum id de flag, var, script, música, treinador ou espécie é importado.
    Comportamento é id semântico: todo móvel entra com o comportamento ZERADO.

NÃO HÁ TRILHA, e não há orla. As passadas anteriores desenhavam um esqueleto de
custo mínimo entre as portas e o engordavam para virar caminho batido, porque nas
cidades delas o caminho não existia no mapa. Aqui ele existe: o metatile 289 JÁ é
o caminho, desenhado à mão pelo demake, e fazer outra trilha por cima seria
desenhar duas vezes a mesma coisa.

A ORLA foi a segunda ideia, e ela chegou a ser escrita, aplicada e renderizada
antes de cair: pintar a BEIRA de cada família (a célula que faz fronteira com
qualquer coisa que não seja da família dela), com desgaste por hash da posição,
que é onde o pé gasta numa vila de verdade. Ela morreu no caso 11b do
auto-teste, o de FORMA, e o número é o motivo. Beira de caminho estreito é uma
linha de UMA célula de largura, e com desgaste ela vira tracejado: medido, a
mancha de areia de `SandgemTown` ficava com 5,2 células por pedaço conexo, contra
5,6 da SABOTAGEM que espalha as mesmas células ao acaso. Ou seja: a orla
desgastada era estatisticamente indistinguível de sal e pimenta, que é
exatamente o que a regra proíbe. Subir o desgaste para 85% levou a 8,4 e ainda
reprovava. Sem orla nenhuma, com as bolhas crescendo até a região acabar, a
mesma medida dá 32,3 em Sandgem e 59,0 em Twinleaf, contra 6,0 da sabotagem: uma
folga de mais de cinco vezes.

A BOLHA CRESCE ATÉ A REGIÃO ACABAR, e é essa a diferença para as passadas
anteriores. Nas cidades de antes a bolha tinha tamanho alvo e era DESCARTADA se
não o alcançasse; aqui o gramado e o caminho têm braços de três células de
largura, e descartar a bolha curta deixava o braço liso. A bolha curta é aceita
quando foi a região que acabou (a frente de onda esvaziou), e não a vontade de
crescer, com um piso absoluto de seis células para "mancha" continuar querendo
dizer mancha.

Uso:
    python3 dev_scripts/costa_sandgem.py                     # mede e mostra o plano
    python3 dev_scripts/costa_sandgem.py --aplicar           # os dois mapas
    python3 dev_scripts/costa_sandgem.py --aplicar --mapa SandgemTown
    python3 dev_scripts/costa_sandgem.py --desfazer          # devolve os map.bin
    python3 dev_scripts/costa_sandgem.py --demo              # auto-teste
    python3 dev_scripts/costa_sandgem.py --extrai            # regera o kit da ROM
    python3 dev_scripts/costa_sandgem.py --so-tileset        # so o tileset, sem mapa
    python3 dev_scripts/costa_sandgem.py --prova-extracao    # o par do hack, pixel a pixel
    python3 dev_scripts/costa_sandgem.py --prova-tiles       # o kit contra a ROM
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

# O `enfeita_cidades.py` PULA o proprio bloco de teste (`175_cidades_enfeitadas`)
# quando varre os corredores que a suite anda. Para esta passada o 175 e um bloco
# como qualquer outro, e ignora-lo ja custou um caso na rodada anterior desta onda
# (o T175.4 de Oreburgh). O nome e trocado ANTES da primeira chamada porque
# `corredores_de_teste` guarda o resultado em cache.
E.BLOCO_PROPRIO = "<nenhum bloco e proprio desta passada>"

DESTINO = f"{RAIZ}/data/tilesets/secondary/petalburg_sinnoh"
KIT_JSON = f"{RAIZ}/dev_scripts/costa_sandgem_kit.json"
PLANO = f"{RAIZ}/dev_scripts/costa_sandgem.json"

PRIMARIO = "gTileset_GeneralSinnoh"
SECUNDARIO = "gTileset_PetalburgSinnoh"
# Os 16 layouts VIVOS que dividem o `gTileset_PetalburgSinnoh`. O tileset e
# declarado como secundario de 62 layouts, mas 46 deles nao tem `map.bin` em
# disco: sao os tumulos das remocoes do cartucho 1. A lista foi conferida nesta
# arvore lendo `data/layouts/layouts.json` e testando a existencia do arquivo.
IRMAOS = ["TwinleafTown", "SandgemTown", "LakeVerity", "Route201", "Route202",
          "Route219", "Route220", "Route221", "VerityLakefront",
          "MtCoronetOutsideSouth", "MtCoronetOutsideNorth", "Route204North",
          "IronIsland", "FloaromaMeadow", "EternaForestOutside",
          "FuegoIronworksOutside"]

TETO_TILES = 512
TETO_META = 512
TILE_LOCAL_0 = 384          # o tiles.png tem 384 tiles; sobram 128 vagas
META_LOCAL_0 = 208          # o maior local usado em map.bin e o 207 (id 719)
MARGEM = 2
TETO_REGUA = 20.0           # o alvo desta onda: carimbo dominante <= 20%

# Os 65 metatiles QUEBRADOS do `gTileset_PetalburgSinnoh`: eles pedem tile local
# acima de 383, que nao existe no `tiles.png`, e NENHUM `map.bin` os desenha. O
# `compacta_tileset.py` os congela e segue; esta passada nao grava neles, para
# que o diff do `metatiles.bin` continue mostrando so o que este kit escreve.
QUEBRADOS = [216, 226, 227, 228, 229, 232, 292, 298, 300, 307, 308, 314, 321,
             322, 325, 337, 347, 359, 362, 365, 369, 370, 371, 372, 376, 379,
             381, 382, 383, 384, 385, 386, 387, 388, 390, 394, 395, 397, 398,
             399, 416, 426, 438, 444, 445, 447, 449, 453, 461, 462, 463, 464,
             465, 466, 467, 468, 474, 476, 477, 478, 479, 480, 481, 483, 484]

# ------------------------------------------------------------------- a FONTE
LP = dict(slug="light-platinum", hack="Pokemon Light Platinum", autor="WesleyFG",
          md5="7fd2c08735459d99fa23fdaa9b755486", base="Ruby (AXVE)",
          pri=0x286CF4, sec=0x286D54, split=(512, 512, 6))

# PALETA DE ORIGEM -> VAGA NOSSA. As paletas 5 e 3 do hack dividem a vaga 6
# porque a uniao delas da 15 cores EXATAS (medido: 7 + 9 com uma cor em comum).
VAGAS_PAL = {5: 6, 3: 6, 2: 7, 0: 11}

# Quantos metatiles DIFERENTES da fonte precisam repetir o mesmo PADRAO de
# camada de baixo para ele ser piso da fonte. O numero nao e chutado: no
# primario do hack os padroes de piso aparecem 35, 32, 21, 20, 19, 18, 16, 11 e
# 10 vezes e o primeiro padrao de ARTE aparece 3; no secundario, 93, 31, 19, 18,
# 17, 15, 14, 13, 10 e 7, e o primeiro de arte tambem 3. O corte de 4 fica com
# folga de mais de duas vezes para os dois lados.
PISO_MIN = 4

# ------------------------------------------------------------------ os TEMAS
# `lp` e o local do metatile na fonte; `lado` diz se ele mora no primario ("p")
# ou no secundario ("s") do hack.
#
# CHAO DE AREIA, importado. Sao oito variantes da areia do hack e duas da terra
# batida dele. As quatro dunas (411, 412, 419, 420) sao a MESMA marca do tile
# 0xF3 em quatro espelhos, um por quadrante: quatro silhuetas por cinco tiles.
CHAO_AREIA = [
    dict(nome="areia ondulada",   lado="p", lp=401),
    dict(nome="areia salpicada",  lado="p", lp=289),
    dict(nome="areia pontilhada", lado="p", lp=302),
    dict(nome="areia marcada",    lado="p", lp=311),
    dict(nome="duna canto NO",    lado="p", lp=411),
    dict(nome="duna canto NE",    lado="p", lp=412),
    dict(nome="duna canto SO",    lado="p", lp=419),
    dict(nome="duna canto SE",    lado="p", lp=420),
]
# A TERRA BATIDA FOI CORTADA DEPOIS DO RENDER, e o motivo esta escrito porque
# ele e o defeito nº 1 da lista do `enfeita_cidades.py` ("retalhos jogados no
# gramado"). Os metatiles 245 e 237 do primario do hack sao terra marrom
# (168,144,120) e a nossa areia e (222,206,132): 100 de distancia RGB, sem
# nenhuma borda de transicao desenhada. Espalhados no caminho, cada celula
# virava um QUADRADO marrom de lado reto no meio do bege, e no render de
# 08/09/2026 o caminho de Twinleaf ficou com cara de buraco, nao de trilha
# gasta. O mesmo aconteceu com o NOSSO metatile 231 (a terra de horta sobre a
# grama), que virou um retangulo marrom no gramado. Os dois sairam. O que ficou
# sao as oito variantes da AREIA do hack, que estao a 42 de distancia da nossa e
# leem como areia seca ao lado de areia batida, que e o que uma praia tem.

# CHAO DE GRAMA, NOSSO. Metatiles do `gTileset_GeneralSinnoh` desenhados sobre a
# camada de baixo do metatile 1, com o atributo IGUAL a ele, e nenhum deles
# aparece nas duas cidades. Custam ZERO tile, ZERO cor e uma vaga de metatile
# so quando entram espelhados.
# A LISTA FOI PODADA PELO CASO 6 DO AUTO-TESTE, e a poda vale ser contada porque
# ela e a regra 9 desta onda ("nunca duplicar arte para enganar a regua") pegando
# alguem em flagrante. A primeira versao trazia nove metatiles e oito espelhos, e
# a medida de distancia RGB media entre eles acusou catorze pares com distancia
# ZERO: o 46 e o 30 sao o MESMO desenho, o 47 e o 31 tambem, o espelho do 30 e o
# proprio 31, o espelho do 470 e o 471 e o 14 e simetrico, entao o espelho dele e
# ele mesmo. Dezessete "variantes" que eram NOVE desenhos. Sobraram os nove de
# verdade: cinco metatiles e quatro espelhos.
CHAO_GRAMA_NOSSO = [
    dict(nome="moita clara",   mt=14),
    dict(nome="tufo fundo",    mt=30),
    dict(nome="tufo claro",    mt=462),
    dict(nome="tufo torto",    mt=463),
    dict(nome="moita cerrada", mt=470),
]
# VARIANTE POR ESPELHO, que nao custa tile nem cor: o tufo com a metade espelhada
# e outra silhueta na tela, e e assim que o proprio primario faz nos pares dele.
# O 14 nao entra porque e simetrico e o espelho dele nao muda um pixel.
ESPELHO_GRAMA = [30, 462, 463, 470]

# MOVEIS IMPORTADOS, uma celula cada. `sobre` diz em qual carimbo a peca pousa.
MOVEIS_LP = [
    dict(nome="moita cheia",   lado="s", lp=86,  sobre="grama"),
    dict(nome="moita alta",    lado="s", lp=87,  sobre="grama"),
    dict(nome="moita redonda", lado="s", lp=152, sobre="grama"),
    dict(nome="arbusto",       lado="p", lp=22,  sobre="grama"),
    dict(nome="arbusto fundo", lado="p", lp=30,  sobre="grama"),
    dict(nome="arbusto raso",  lado="p", lp=31,  sobre="grama"),
    dict(nome="capim baixo",   lado="p", lp=5,   sobre="grama"),
    dict(nome="pedra dupla",   lado="p", lp=6,   sobre="grama"),
    dict(nome="pedra grande",  lado="p", lp=7,   sobre="grama"),
    dict(nome="flor azul",     lado="p", lp=150, sobre="grama"),
]
# O METATILE 13 DO PRIMARIO DO HACK, que a primeira lista trazia como "arbusto
# largo", foi cortado por MEDICAO e nao por gosto: o atributo dele e 0x0002, ou
# seja MB_TALL_GRASS, e a arte inteira dele mora na camada de BAIXO. Ele nao e
# uma moita solta, e o metatile de GRAMA ALTA da fonte, e por isso a assinatura
# de piso o marca inteiro e nao sobra quadrante nenhum de arte. O `--extrai`
# parou com "nao sobrou com nenhum quadrante de arte", que e exatamente o que
# ele tinha que dizer.
#
# O GUARDA-SOL E A BOIA FORAM CORTADOS DEPOIS DO RENDER, e por jogabilidade, nao
# por orcamento: eles cabiam na vaga 11 e estavam desenhados. `SandgemTown` tem
# ZERO celulas de agua (medido pelo comportamento, celula a celula) e nenhuma
# vista de mar: a praia dela mora na `Route219`, do outro lado da conexao sul. Um
# guarda-sol plantado no meio de um caminho de terra entre arvores nao le como
# praia, le como erro de mapa, que e a mesma razao pela qual a boca de galeria
# saiu de Oreburgh. No lugar deles a vaga 11 paga a FLOR AZUL do hack (o metatile
# 150 do primario), que serve as duas vilas.
#
# BLOCOS DE DUAS CELULAS DE ALTURA. A linha de CIMA continua ANDAVEL (a arte
# mora na camada de cima e o jogador passa ATRAS dela) e a de BAIXO vira solida
# em COVERED, que e o que faz o jogador parado ao sul aparecer NA FRENTE.
BLOCOS_LP = [
    dict(nome="coqueiro",   lado="s", topo=[145, 146], base=[153, 154],
         sobre="areia"),
]

# MOVEIS NOSSOS: metatiles do PRIMARIO desenhados sobre a camada de baixo de um
# dos dois carimbos e JA em COVERED com comportamento zerado. Custam zero.
MOVEIS_NOSSOS = [
    dict(nome="flor vermelha", mt=4,   sobre="grama"),
    dict(nome="pedregulho",    mt=224, sobre="grama"),
    dict(nome="pedra de areia", mt=226, sobre="areia"),
    dict(nome="placa",         mt=27,  sobre="grama"),
]

CARIMBOS = dict(grama=1, areia=289)

# O que cada cidade usa, e quantas de cada peca. Twinleaf e vila de INTERIOR, a
# beira de lago e mato, e nao leva peca de praia nenhuma. Sandgem e a vila do
# litoral e leva o coqueiro, na metade sul, que e o lado do mar.
TWINLEAF = dict(
    alvo="TwinleafTown",
    # OS GRUPOS SAO GRANDES DE PROPOSITO. Grupo de uma peca so faz cada bolha
    # sair de uma cor unica, e ai saber onde a celula esta passa a adivinhar o
    # que ela e: o caso 11a do auto-teste mediu isso em Twinleaf, com "x mod 7"
    # acertando 23% contra 10% do chute cego. Com o grupo misturando quatro ou
    # cinco silhuetas por hash da posicao, a bolha continua sendo mancha e o
    # interior dela deixa de ser adivinhavel.
    bolhas_grama=[
        dict(grupo=["tufo claro", "tufo claro espelhado",
                    "tufo torto", "tufo torto espelhado"],   quantas=9, tam=(14, 26)),
        dict(grupo=["tufo fundo", "tufo fundo espelhado",
                    "moita clara"],                          quantas=9, tam=(13, 24)),
        dict(grupo=["moita cerrada", "moita cerrada espelhada",
                    "tufo claro", "tufo torto espelhado"],   quantas=9, tam=(12, 22)),
    ],
    bolhas_areia=[
        dict(grupo=["areia ondulada", "areia marcada", "areia salpicada",
                    "duna canto NO", "duna canto SE"],       quantas=9, tam=(14, 26)),
        dict(grupo=["duna canto NE", "duna canto SO",
                    "areia pontilhada", "areia ondulada"],   quantas=9, tam=(14, 26)),
    ],
    moveis=[
        dict(nome="moita cheia",   quantos=4, espaco=6),
        dict(nome="moita alta",    quantos=4, espaco=6),
        dict(nome="moita redonda", quantos=4, espaco=6),
        dict(nome="arbusto",       quantos=3, espaco=7),
        dict(nome="arbusto fundo", quantos=3, espaco=7),
        dict(nome="arbusto raso",  quantos=3, espaco=7),
        dict(nome="capim baixo",   quantos=4, espaco=6),
        dict(nome="flor azul",     quantos=4, espaco=6),
        dict(nome="pedra dupla",   quantos=2, espaco=8),
        dict(nome="pedra grande",  quantos=2, espaco=8),
        dict(nome="flor vermelha", quantos=3, espaco=7),
        dict(nome="pedregulho",    quantos=2, espaco=9),
        dict(nome="placa",         quantos=1, espaco=12),
    ],
    blocos=[],
)
SANDGEM = dict(
    alvo="SandgemTown",
    bolhas_grama=[
        dict(grupo=["tufo claro", "tufo claro espelhado",
                    "tufo torto", "tufo torto espelhado"],   quantas=9, tam=(14, 26)),
        dict(grupo=["tufo fundo", "tufo fundo espelhado",
                    "moita clara"],                          quantas=9, tam=(13, 24)),
        dict(grupo=["moita cerrada", "moita cerrada espelhada",
                    "tufo claro", "tufo torto espelhado"],   quantas=9, tam=(12, 22)),
    ],
    bolhas_areia=[
        dict(grupo=["areia ondulada", "areia marcada", "areia salpicada",
                    "duna canto NO", "duna canto SE"],       quantas=9, tam=(16, 30)),
        dict(grupo=["duna canto NE", "duna canto SO",
                    "areia pontilhada", "areia ondulada"],   quantas=9, tam=(16, 30)),
    ],
    moveis=[
        dict(nome="moita cheia",   quantos=4, espaco=6),
        dict(nome="moita alta",    quantos=4, espaco=6),
        dict(nome="moita redonda", quantos=4, espaco=6),
        dict(nome="arbusto",       quantos=3, espaco=7),
        dict(nome="arbusto fundo", quantos=3, espaco=7),
        dict(nome="arbusto raso",  quantos=3, espaco=7),
        dict(nome="capim baixo",   quantos=4, espaco=6),
        dict(nome="flor azul",     quantos=3, espaco=6),
        dict(nome="pedra dupla",   quantos=2, espaco=8),
        dict(nome="pedra grande",  quantos=2, espaco=8),
        dict(nome="flor vermelha", quantos=2, espaco=7),
        dict(nome="pedregulho",    quantos=2, espaco=9),
        dict(nome="pedra de areia", quantos=3, espaco=8),
        dict(nome="placa",         quantos=1, espaco=12),
    ],
    # O COQUEIRO SO NASCE NA METADE SUL, que e o lado da conexao com a
    # `Route219`, a rota do mar. Palmeira e a unica peca de praia que sobreviveu
    # ao corte, e ela so le como litoral se estiver do lado do litoral: plantada
    # ao norte, entre o laboratorio e a loja, viraria enfeite de jardim.
    blocos=[
        dict(nome="coqueiro", quantos=4, espaco=5, faixa="sul"),
    ],
)
TEMAS = {"TwinleafTown": TWINLEAF, "SandgemTown": SANDGEM}
ORDEM = ["TwinleafTown", "SandgemTown"]   # ordem FIXA de alocacao de vaga

ESPACO_ENTRE_MOVEIS = 2     # Chebyshev minimo entre dois moveis QUAISQUER
PISO_BOLHA = 6              # tamanho minimo de uma bolha que a regiao cortou

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


def _espelha4(quad):
    """Espelho horizontal de UMA camada: troca as colunas e liga o bit 0x400."""
    fora = []
    for q in (1, 0, 3, 2):
        v = quad[q]
        fora.append(0 if (v & 0x3FF) == 0 else (v ^ 0x400))
    return fora


def _tileset(rotulo):
    import render_maps as RM
    return RM.carregar_tileset(rotulo)


def vagas_livres():
    """{vaga: [indices de cor que NENHUM pixel VIVO nosso usa]}.

    "Vivo" e a palavra que importa: o `gTileset_PetalburgSinnoh` tem 512
    metatiles e so 127 deles aparecem em `map.bin` de algum dos 16 layouts com
    arquivo em disco. Contar os 512 daria as sete vagas ocupadas e nao sobraria
    nenhuma; contar so os vivos da 6, 7 e 11 inteiras e mais tres indices na 8.
    O portao que prova que isso e verdade nao esta aqui, esta no render dos 14
    mapas irmaos com ZERO pixel diferente.

    Os metatiles que ESTA passada grava sao ignorados de proposito, para que
    rodar `--extrai` depois de `--aplicar` de o mesmo kit.
    """
    import render_maps as RM
    ts, tp = _tileset(SECUNDARIO), _tileset(PRIMARIO)
    usados = collections.defaultdict(set)
    vivos = set()
    for nome in IRMAOS:
        vivos |= {c & 0x3FF for c in G.grade(nome)[4]}
    for gid in sorted(x for x in vivos if x >= 512):
        local = gid - 512
        if local >= META_LOCAL_0:
            continue
        for (it, fh, fv, ip) in RM.entradas_metatile(ts["metatiles"], local):
            if it == 0 or ip < 6:
                continue
            if it >= len(tp["tiles"]) + TILE_LOCAL_0:
                continue
            tile = RM.resolver_tile(tp, ts, it)
            if tile is None:
                continue
            for linha in tile:
                for c in linha:
                    if c:
                        usados[ip].add(c)
    # A ARMADILHA 4 do `compacta_paletas.py`: metatile do PRIMARIO alcancavel
    # tambem pode pintar com vaga secundaria. Medido aqui e ZERO, mas a conta
    # roda de qualquer jeito, porque "medi uma vez" nao e portao.
    for gid in sorted(x for x in vivos if x < 512):
        for (it, fh, fv, ip) in RM.entradas_metatile(tp["metatiles"], gid):
            if it and ip >= 6:
                tile = RM.resolver_tile(tp, ts, it)
                if tile is None:
                    continue
                for linha in tile:
                    for c in linha:
                        if c:
                            usados[ip].add(c)
    return {v: [i for i in range(1, 16) if i not in usados[v]]
            for v in range(6, 13)}


# ---------------------------------------------------------------- a EXTRACAO
def _nibbles(dados, local):
    """8 linhas de 8 nibbles, o pixel PAR no nibble BAIXO (ver extrai_tileset)."""
    b = dados[local * 32:local * 32 + 32]
    return [[(b[y * 4 + (x >> 1)] >> (0 if x % 2 == 0 else 4)) & 0xF
             for x in range(8)] for y in range(8)]


def _rgb(ts, i):
    """BGR555 do GBA para o RGB888 que o repo usa: cinco bits DESLOCADOS TRES
    casas, nao esticados para 0..255.

    A conta importa e ja foi medida duas vezes nesta obra. As duas contas dao o
    MESMO cinco-bits depois que o `gbagfx` reconverte o `.pal` para `.gbapal`,
    entao a cor dentro da ROM e a mesma; o que muda e o numero escrito no `.pal`
    e, com ele, o pixel de todo render de conferencia. Todo `.pal` deste
    repositorio esta na conta de deslocar, e o `ferramentas/prova_extracao.py`,
    que e o portao da extracao, tambem. E a mesma conta de `render_hack.cor`.
    """
    c = struct.unpack_from("<16H", ts["pal"], i * 32)
    return [[((v >> s) & 0x1F) << 3 for s in (0, 5, 10)] for v in c]


def _piso_da_fonte(tset, n_tiles_pri):
    """Os tiles que a FONTE usa como piso, por evidencia e nao por decoreba.

    Duas assinaturas, as duas medidas: (a) padrao de camada de baixo que aparece
    em PISO_MIN metatiles diferentes ou mais; (b) camada de baixo que repete o
    MESMO tile nos quatro quadrantes. Piso e o que se repete debaixo de tudo;
    arte de peca aparece em um ou dois metatiles.
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
    """Regera `costa_sandgem_kit.json` a partir da ROM privada do Light Platinum.

    So roda na maquina que tem `fontes-mapas/romhacks/`. O que sai daqui e o
    asset CONVERTIDO (tiles em nibbles, ja reindexados para a vaga de destino, e
    paleta em RGB), nunca a ROM.
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
    piso = dict(p=_piso_da_fonte(t1, NP), s=_piso_da_fonte(t2, NP))

    def tset_de(lado):
        return t1 if lado == "p" else t2

    def ents_de(lado, local):
        return list(struct.unpack_from("<8H", tset_de(lado)["meta"], local * 16))

    def px_de(idx):
        return (_nibbles(t1["tiles"], idx) if idx < NP
                else _nibbles(t2["tiles"], idx - NP))

    def branco(v):
        """A entrada aponta para um tile 8x8 SEM UM PIXEL aceso?

        O `0x2401` que a moita do hack traz na camada de cima e o tile 1 do
        primario dele, e ele e todo transparente. Tratar isso como camada de
        cima cheia deixaria metade da peca VAZIA.
        """
        idx = v & 0x3FF
        if not idx:
            return True
        return not any(c for linha in px_de(idx) for c in linha)

    def eh_piso(v):
        idx = v & 0x3FF
        lado, li = ("p", idx) if idx < NP else ("s", idx - NP)
        # a lista de piso guarda o indice COMO A FONTE escreve, ou seja ja com o
        # deslocamento do split, entao a busca e pelo indice cru
        return idx in piso[lado]

    tiles_px, tiles_vaga, tiles_cor = {}, {}, {}

    def guarda(v):
        """Registra o tile 8x8 daquela entrada e devolve a chave dele.

        A CHAVE LEVA A PALETA DE ORIGEM, e isso nao e detalhe: o mesmo desenho
        8x8 pintado com duas paletas do hack tem que virar DUAS vagas nossas,
        senao a segunda apaga a primeira.
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
    lista = [("chao", c) for c in CHAO_AREIA]
    lista += [("movel", m) for m in MOVEIS_LP]
    for b in BLOCOS_LP:
        for papel2, lst in (("topo", b["topo"]), ("base", b["base"])):
            for k, loc in enumerate(lst):
                lista.append(("movel", dict(nome="%s %s %d" % (b["nome"], papel2, k),
                                            lado=b["lado"], lp=loc)))
    for papel, p in lista:
        ents = ents_de(p["lado"], p["lp"])
        baixo, cima = ents[:4], ents[4:]
        if papel == "chao":
            # o chao entra INTEIRO na camada de baixo, e a de cima fica vazia:
            # camada de cima em celula andavel com layerType NORMAL desenha
            # ACIMA do jogador.
            if any(not branco(v) for v in cima):
                raise SystemExit("%s: a peca de chao %d tem camada de cima"
                                 % (p["nome"], p["lp"]))
            if len({v & 0x3FF for v in baixo}) < 2:
                raise SystemExit("%s: o metatile %d repete o mesmo tile nos "
                                 "quatro quadrantes, e por isso e chao liso da "
                                 "fonte, nao arte" % (p["nome"], p["lp"]))
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
                                 "quadrante de arte" % (p["nome"], p["lp"]))
        pecas.append(dict(papel=papel, nome=p["nome"], lado=p["lado"],
                          lp=p["lp"], ents=saida, usadas=usadas))

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
        fonte=dict(hack=LP["hack"], autor=LP["autor"], base=LP["base"],
                   arquivo=gba, md5=md5, pri="0x%X" % LP["pri"],
                   sec="0x%X" % LP["sec"], split=list(LP["split"]),
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


def chao_nosso(qual):
    """(as quatro entradas da camada de BAIXO do carimbo, o atributo dele).

    E o chao que todo movel pousa em cima e que toda peca de topo herda.
    """
    tp = _tileset(PRIMARIO)
    mt = CARIMBOS[qual]
    ents = list(struct.unpack_from("<8H", tp["metatiles"], mt * 16))
    if any(v & 0x3FF for v in ents[4:]):
        raise SystemExit("o carimbo %d ja usa a camada de cima" % mt)
    return ents[:4], G._attrs(PRIMARIO)[mt]


def _locais_livres():
    """Os locais de metatile em que esta passada pode gravar, em ordem.

    Sao os locais do META_LOCAL_0 para cima que NAO estao na lista dos 65
    quebrados. O portao de verdade (nenhum dos 16 mapas usa o id) roda depois,
    no `desenha_kit`, sobre a grade de cada um deles.
    """
    proibidos = set(QUEBRADOS)
    return [l for l in range(META_LOCAL_0, TETO_META) if l not in proibidos]


def desenha_kit():
    """(tiles_novos, metas, attrs, carimbos), sem escrever em disco.

    A ALOCACAO E SEMPRE A DE `ORDEM` INTEIRA, e nao a do subconjunto pedido: a
    vaga de tile e a de metatile de cada peca precisam ser as MESMAS quer o
    commit seja o de Twinleaf, o de Sandgem ou os dois.
    """
    dados = kit()
    meta_pet = _ler("metatiles.bin")
    ap = G._attrs(PRIMARIO)
    tp = _tileset(PRIMARIO)

    por_peca = {(p["papel"], p["nome"]): p for p in dados["pecas"]}
    tiles_novos, mapa_tile = {}, {}
    proximo = [TILE_LOCAL_0]
    metas, attrs = {}, {}
    vagas_meta = _locais_livres()
    proximo_meta = [0]
    catalogo = dict(chao={}, moveis={}, blocos={}, sobre={})

    def vaga(chave):
        if chave not in mapa_tile:
            if chave not in dados["tiles"]:
                raise SystemExit("o kit em disco nao tem o tile %s" % chave)
            mapa_tile[chave] = proximo[0]
            tiles_novos[proximo[0]] = dados["tiles"][chave]
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
        alvo_pal = VAGAS_PAL[int(ch.split(":")[2])]
        return ((v & 0x0C00) | (512 + vaga(ch)) | (alvo_pal << 12))

    base_grama, attr_grama = chao_nosso("grama")
    base_areia, attr_areia = chao_nosso("areia")
    BASE = dict(grama=(base_grama, attr_grama), areia=(base_areia, attr_areia))

    # ------------------------------------------------------ 1. CHAO IMPORTADO
    for c in CHAO_AREIA:
        p = por_peca[("chao", c["nome"])]
        ents = [entrada(p, q) for q in range(4)]
        if any(e is None for e in ents):
            raise SystemExit("%s: quadrante vazio em peca de chao" % c["nome"])
        gid = poe(ents + [0, 0, 0, 0], attr_areia)
        catalogo["chao"][c["nome"]] = gid
        catalogo["sobre"][c["nome"]] = "areia"

    # ------------------------------------------------------ 2. CHAO NOSSO
    for c in CHAO_GRAMA_NOSSO:
        if ap[c["mt"]] != attr_grama:
            raise SystemExit("o metatile %d tem atributo 0x%04X e o carimbo de "
                             "grama tem 0x%04X" % (c["mt"], ap[c["mt"]], attr_grama))
        ents = list(struct.unpack_from("<8H", tp["metatiles"], c["mt"] * 16))
        if ents[:4] != base_grama:
            raise SystemExit("o metatile %d nao esta desenhado sobre a grama do "
                             "carimbo" % c["mt"])
        catalogo["chao"][c["nome"]] = c["mt"]
        catalogo["sobre"][c["nome"]] = "grama"
    por_mt = {c["mt"]: c["nome"] for c in CHAO_GRAMA_NOSSO}
    for mt in ESPELHO_GRAMA:
        ents = list(struct.unpack_from("<8H", tp["metatiles"], mt * 16))
        nome = por_mt[mt] + (" espelhada" if por_mt[mt].startswith("moita")
                             else " espelhado")
        gid = poe(list(base_grama) + _espelha4(ents[4:]), attr_grama)
        catalogo["chao"][nome] = gid
        catalogo["sobre"][nome] = "grama"

    # ---------------------------------------------------- 3. MOVEIS de 1 celula
    for m in MOVEIS_LP:
        p = por_peca[("movel", m["nome"])]
        cima = [entrada(p, q) or 0 for q in range(4)]
        if not any(cima):
            raise SystemExit("%s: peca sem arte" % m["nome"])
        base, _a = BASE[m["sobre"]]
        # comportamento ZERADO (nenhum id semantico e importado) e layerType
        # COVERED, que poe as duas camadas ABAIXO do sprite.
        gid = poe(list(base) + cima, 0x1000)
        catalogo["moveis"][m["nome"]] = gid
        catalogo["sobre"][m["nome"]] = m["sobre"]
    for m in MOVEIS_NOSSOS:
        base, _a = BASE[m["sobre"]]
        ents = list(struct.unpack_from("<8H", tp["metatiles"], m["mt"] * 16))
        if ents[:4] != base:
            raise SystemExit("o metatile %d nao esta desenhado sobre o carimbo "
                             "de %s" % (m["mt"], m["sobre"]))
        if ap[m["mt"]] != 0x1000:
            raise SystemExit("o metatile %d nao esta em COVERED com "
                             "comportamento zerado (0x%04X)" % (m["mt"], ap[m["mt"]]))
        catalogo["moveis"][m["nome"]] = m["mt"]
        catalogo["sobre"][m["nome"]] = m["sobre"]

    # ------------------------------------------------- 4. BLOCOS de 2 celulas
    for b in BLOCOS_LP:
        base, attr_base = BASE[b["sobre"]]
        ids = {}
        for papel2, lst, attr_peca in (("topo", b["topo"], attr_base),
                                       ("base", b["base"], 0x1000)):
            fora = []
            for k, _loc in enumerate(lst):
                p = por_peca[("movel", "%s %s %d" % (b["nome"], papel2, k))]
                cima = [entrada(p, q) or 0 for q in range(4)]
                if not any(cima):
                    raise SystemExit("%s: metade sem arte" % b["nome"])
                fora.append(poe(list(base) + cima, attr_peca))
            ids[papel2] = fora
        catalogo["blocos"][b["nome"]] = dict(topo=ids["topo"], base=ids["base"])
        catalogo["sobre"][b["nome"]] = b["sobre"]

    if proximo[0] > TETO_TILES:
        raise SystemExit("o kit estoura o teto de %d tiles (%d)"
                         % (TETO_TILES, proximo[0]))

    # A vaga de metatile so serve se NENHUM dos 16 mapas vivos usar o id, e se o
    # que esta la for enchimento do dumper ou ja for exatamente o que este kit
    # escreve. Diferente das passadas anteriores, aqui as vagas livres NAO sao
    # so enchimento: o tileset tem metatiles legitimos que nenhum mapa desenha.
    # A grade dos DOIS ALVOS entra pela base LIMPA desta passada, e nao pelo
    # disco: depois de um `--aplicar` o disco ja tem os ids que este kit acabou
    # de escrever, e o portao reprovaria a si mesmo na segunda rodada (medido:
    # "algum dos 16 mapas usa o metatile 720"). Os outros 14 entram como estao,
    # porque esta passada nao encosta neles.
    guardado = carrega_plano()
    usados = set()
    for nome in IRMAOS:
        grade = (base_de(nome, guardado) if nome in TEMAS else G.grade(nome)[4])
        usados |= {c & 0x3FF for c in grade}
    for local in metas:
        if 512 + local in usados:
            raise SystemExit("algum dos 16 mapas usa o metatile %d" % (512 + local))
        if local in set(QUEBRADOS):
            raise SystemExit("o local %d e um dos 65 quebrados congelados" % local)
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

    meta = bytearray(_ler("metatiles.bin"))
    attr = bytearray(_ler("metatile_attributes.bin"))
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

    A ORDEM E POR RODADA, e nao por especificacao inteira, e isso nao e estilo. A
    primeira versao servia uma especificacao ate o teto dela antes de olhar a
    proxima, e nas duas cidades desta passada isso deixou METADE do catalogo
    fora: o gramado de Twinleaf tem 183 celulas e as tres primeiras bolhas
    comiam 122, entao a moita, o tufo largo e o canteiro nunca chegavam a ser
    semeados. Servindo UMA bolha por especificacao a cada rodada, o que falta no
    fim e o excedente de todo mundo, e nao a lista inteira de quem estava no fim
    da fila.
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
                # vontade de crescer: em cidade estreita como estas duas, o
                # gramado tem bracos de tres celulas de largura e exigir o
                # tamanho cheio faria a bolha ser descartada e o braco ficar
                # liso. O piso absoluto de PISO_BOLHA existe para que "mancha"
                # continue querendo dizer mancha.
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

    POR QUE NAO BASTA O `enfeita_cidades.alcance`. Aquele mede "quem ainda e
    alcancavel a partir de algum ponto de partida", e ponto de partida ali e
    warp OU objeto: fechar um corredor com warp dos dois lados nao tira NENHUMA
    celula do alcance e mesmo assim parte a cidade em duas.
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
def plano_mapa(alvo, catalogo, base=None):
    """(L, W, H, v, escritas, contas) para UM mapa."""
    T = TEMAS[alvo]
    d, L, W, H, v0 = G.grade(alvo)
    v = list(base) if base is not None else list(v0)
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()

    # As duas FAMILIAS de chao. Uma celula so e elegivel se ela ainda for o
    # carimbo puro, se estiver na elevacao dominante daquele carimbo e se nao
    # for agua para o motor.
    fam, elev = {}, {}
    for qual, mt in CARIMBOS.items():
        alvos = [c for c in v if (c & 0x3FF) == mt and not ((c >> 10) & 3)]
        if not alvos:
            elev[qual] = None
            fam[qual] = set()
            continue
        elev[qual] = collections.Counter((c >> 12) & 0xF
                                         for c in alvos).most_common(1)[0][0]
        fam[qual] = {(i % W, i // W) for i in range(W * H)
                     if not ((v[i] >> 10) & 3) and (v[i] & 0x3FF) == mt
                     and ((v[i] >> 12) & 0xF) == elev[qual]
                     and beh(v[i] & 0x3FF) not in AG}
    elegivel = fam["grama"] | fam["areia"]

    escritas = {}
    ev, gelo = E.congelado(d)
    gelo |= E.corredores_de_teste(alvo, v, W, H, d)
    for idx, _a, _n in E.carrega_plano().get(alvo, {}).get("celulas", []):
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
        if (x, y) in gelo or i in escritas or (x, y) not in fam[qual]:
            return False
        return (aplicado[i] & 0x3FF) == CARIMBOS[qual]

    def espacado(nome, esp, x, y):
        if any(max(abs(x - px), abs(y - py)) < ESPACO_ENTRE_MOVEIS
               for px, py in postos):
            return False
        return not any(max(abs(x - px), abs(y - py)) < esp
                       for px, py in por_movel[nome])

    def tenta_solidificar(x, y, mt_id):
        """Solidifica (x,y) e devolve True se os DOIS portoes deixarem.

        O portao roda NA HORA e nao so no fim: se solidificar esta celula tirar
        do alcance a pe qualquer OUTRA celula, ou partir um pedaco de chao em
        dois, a escrita e desfeita e o gerador segue.
        """
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

    # ------ 1. BLOCO DE DUAS CELULAS, antes da mobilia de uma celula, porque
    # ele precisa de um retangulo 2x2 inteiro e a mobilia solta nao pode ter
    # comido metade dele. A linha de CIMA continua ANDAVEL e por isso nao entra
    # em `novos_solidos` nem no portao de alcance; a de BAIXO vira solida.
    conta_bloco = collections.Counter()
    por_bloco = []
    for b in T["blocos"]:
        info = catalogo["blocos"][b["nome"]]
        qual = catalogo["sobre"][b["nome"]]
        for x, y in ordem_cel:
            if conta_bloco[b["nome"]] >= b["quantos"]:
                break
            if b.get("faixa") == "sul" and y < H // 2:
                continue
            cels = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
            if any(not livre(cx, cy, qual) for cx, cy in cels):
                continue
            if any(max(abs(x - px), abs(y - py)) < b["espaco"]
                   for px, py in por_bloco):
                continue
            if any(max(abs(cx - px), abs(cy - py)) < ESPACO_ENTRE_MOVEIS
                   for cx, cy in cels for px, py in postos):
                continue
            topo = [(x, y), (x + 1, y)]
            for k, (cx, cy) in enumerate(topo):
                j = cy * W + cx
                escritas[j] = (aplicado[j] & 0xFC00) | info["topo"][k]
                aplicado[j] = escritas[j]
            ok = True
            for k, (cx, cy) in enumerate([(x, y + 1), (x + 1, y + 1)]):
                if not tenta_solidificar(cx, cy, info["base"][k]):
                    ok = False
                    break
            if not ok:
                for cx, cy in cels:
                    j = cy * W + cx
                    if j in escritas and (cx, cy) not in novos_solidos:
                        del escritas[j]
                        aplicado[j] = v[j]
                for cx, cy in [(x, y + 1), (x + 1, y + 1)]:
                    if (cx, cy) in novos_solidos:
                        novos_solidos.remove((cx, cy))
                        postos.remove((cx, cy))
                        del escritas[cy * W + cx]
                        aplicado[cy * W + cx] = v[cy * W + cx]
                continue
            por_bloco += cels
            postos += topo
            conta_bloco[b["nome"]] += 1

    # ------ 2. MOVEIS de uma celula. Eles vem ANTES da mancha de proposito, e a
    # razao esta medida em Snowpoint: movel posto no carimbo tira uma celula do
    # numerador E do denominador da regua; movel posto em cima de uma mancha
    # tira so do denominador, o que PIORA a conta.
    lista = T["moveis"]
    for x, y in ordem_cel:
        giro = ((x * 73856093) ^ (y * 19349663)) % len(lista)
        for k in range(len(lista)):
            m = lista[(giro + k) % len(lista)]
            if conta_mov[m["nome"]] >= m["quantos"]:
                continue
            qual = catalogo["sobre"][m["nome"]]
            if not livre(x, y, qual) or not espacado(m["nome"], m["espaco"], x, y):
                continue
            # movel de cidade encosta em alguma coisa: ou num solido, ou na
            # OUTRA familia de chao (a beira do caminho). Peca solta no meio do
            # vazio le como erro de mapa.
            outra = "areia" if qual == "grama" else "grama"
            perto = any(0 <= x + dx < W and 0 <= y + dy < H
                        and (((aplicado[(y + dy) * W + x + dx] >> 10) & 3)
                             or (x + dx, y + dy) in fam[outra])
                        for dx, dy in N4)
            if not perto:
                continue
            if not tenta_solidificar(x, y, catalogo["moveis"][m["nome"]]):
                continue
            por_movel[m["nome"]].append((x, y))
            conta_mov[m["nome"]] += 1
            break

    # ------------------------------------------------------------- 3. MANCHA
    conta_mancha = collections.Counter()

    def pintavel(p, qual):
        i = p[1] * W + p[0]
        return (p in fam[qual] and i not in escritas
                and (aplicado[i] & 0x3FF) == CARIMBOS[qual])

    def pinta(p, nomes):
        i = p[1] * W + p[0]
        nome = peca_da_mancha(nomes, p[0], p[1])
        escritas[i] = (aplicado[i] & 0xFC00) | catalogo["chao"][nome]
        aplicado[i] = escritas[i]
        conta_mancha[nome] += 1

    for qual, chave_bolhas in (("grama", "bolhas_grama"),
                               ("areia", "bolhas_areia")):
        livres = {p for p in fam[qual] if pintavel(p, qual)}
        for nomes, corpo in bolhas(livres, T[chave_bolhas],
                                   0x5EED if qual == "grama" else 0xB0A7):
            for p in sorted(corpo):
                pinta(p, nomes)

    # -------------------------------------------------------------- PORTOES
    depois = E.alcance(aplicado, W, H, ini)
    perdidas = antes_alc - depois - set(novos_solidos)
    if perdidas:
        raise SystemExit("%s: %d celulas ficariam inalcancaveis, ex.: %s"
                         % (alvo, len(perdidas), sorted(perdidas)[:6]))
    for x, y in E.eventos(d):
        if (x, y) in antes_alc and (x, y) not in depois:
            raise SystemExit("%s: evento em (%d,%d) ficaria inalcancavel"
                             % (alvo, x, y))
    queixas = ligacao_intacta(componentes(v, W, H), componentes(aplicado, W, H),
                              set(novos_solidos))
    if queixas:
        raise SystemExit("%s: %s" % (alvo, "; ".join(queixas)))
    contas = dict(moveis=dict(conta_mov), blocos=dict(conta_bloco),
                  manchas=dict(conta_mancha), solidos=len(novos_solidos),
                  grama=len(fam["grama"]), areia=len(fam["areia"]))
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

    Sem isso a idempotencia morre: as duas cidades JA tem desenho do
    `enfeita_cidades.py` em cima, com plano proprio, e planejar sobre um mapa ja
    enfeitado nao volta ao mesmo lugar. A saida e a do `porto_canalave.py`:
    planejar sobre a base LIMPA desta passada (o disco menos o que esta passada
    gravou) e escrever por cima do disco.
    """
    v = list(G.grade(alvo)[4])
    for idx, antigo, novo in guardado.get(alvo, {}).get("celulas", []):
        if v[idx] == novo:
            v[idx] = antigo
    return v


def roda(alvos, aplicar):
    tiles_novos, metas, attrs, catalogo = desenha_kit()
    print("kit: %d tiles novos (vagas %d a %d de %d, sobram %d), %d metatiles "
          "novos (locais %d a %d, ids %d a %d)"
          % (len(tiles_novos), min(tiles_novos), max(tiles_novos), TETO_TILES,
             TETO_TILES - max(tiles_novos) - 1, len(metas), min(metas),
             max(metas), 512 + min(metas), 512 + max(metas)))
    if aplicar:
        grava_tileset(tiles_novos, metas, attrs)
    guardado = carrega_plano()
    for alvo in alvos:
        base = base_de(alvo, guardado)
        L, W, H, v, escritas, contas = plano_mapa(alvo, catalogo, base)
        a, na, ida = regua(v, W, H, L)
        b, nb, idb = regua(v, W, H, L, escritas)
        print("%s: %d celulas de mancha, %d solidificadas, %d mudadas "
              "(familia grama %d, areia %d)"
              % (alvo, sum(contas["manchas"].values()), contas["solidos"],
                 len(escritas), contas["grama"], contas["areia"]))
        print("  mancha: " + ", ".join("%s x%d" % kv
                                       for kv in sorted(contas["manchas"].items())))
        print("  movel:  " + ", ".join("%s x%d" % kv
                                       for kv in sorted(contas["moveis"].items())))
        if contas["blocos"]:
            print("  bloco:  " + ", ".join("%s x%d" % kv
                                           for kv in sorted(contas["blocos"].items())))
        print("  regua: carimbo %d com %.1f%% de %d celulas ANTES; carimbo %d "
              "com %.1f%% de %d DEPOIS" % (ida, a, na, idb, b, nb))
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
        print("aplicado")
    return 0


def desfaz(alvos):
    guardado = carrega_plano()
    for alvo in alvos:
        if alvo not in guardado:
            print("%s: nada a desfazer" % alvo)
            continue
        d, L, W, H, v = G.grade(alvo)
        v, n = list(v), 0
        for idx, antigo, novo in guardado[alvo]["celulas"]:
            if v[idx] == novo:
                v[idx] = antigo
                n += 1
        with open(f"{RAIZ}/{L['blockdata_filepath']}", "wb") as f:
            f.write(struct.pack("<%dH" % len(v), *v))
        guardado.pop(alvo)
        print("%s: desfeitas %d celulas" % (alvo, n))
    with open(PLANO, "w") as f:
        json.dump(guardado, f, indent=1)
    return 0


# ------------------------------------------------------------------ conferencia
def _opacos(px):
    return sum(1 for linha in px for c in linha if c)


def confere(alvos, tiles_novos, metas, attrs, catalogo, planos):
    """Todas as regras desta onda, medidas sobre os dados que vierem.

    Ela e chamada DUAS vezes pelo auto-teste: uma com o plano de verdade, que
    tem que sair sem queixa, e uma por sabotagem, que tem que sair com a queixa
    certa. Regra conferida so no caminho feliz nao e regra, e prova positiva sem
    par negativo nao e prova.
    """
    mau = []
    dados = kit()
    ap = G._attrs(PRIMARIO)
    import render_maps as RM
    tp = _tileset(PRIMARIO)
    ts = _tileset(SECUNDARIO)

    def atributo(mt_id):
        """Atributo de um metatile, com o kit desta rodada valendo por cima."""
        if mt_id >= 512:
            local = mt_id - 512
            if local in attrs:
                return attrs[local]
            asec = G._attrs(SECUNDARIO)
            return asec[local] if local < len(asec) else 0
        return ap[mt_id] if mt_id < len(ap) else 0

    def entradas(mt_id):
        if mt_id >= 512 and (mt_id - 512) in metas:
            return list(metas[mt_id - 512])
        tset, loc = (tp, mt_id) if mt_id < 512 else (ts, mt_id - 512)
        return list(struct.unpack_from("<8H", tset["metatiles"], loc * 16))

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
                vaga = idx - len(tp["tiles"])
                if vaga in tiles_novos:
                    tile = tiles_novos[vaga]
                else:
                    tile = RM.resolver_tile(tp, ts, idx)
                if tile is None:
                    continue
                cores = (dados["paletas"].get(str(ip))
                         or (tp if ip < 6 else ts)["paletas"].get(ip))
                if cores is None:
                    continue
                RM.desenhar_tile(p, (q % 2) * 8, (q // 2) * 8, tile,
                                 [tuple(c) for c in cores],
                                 bool(val & 0x400), bool(val & 0x800))
        return list(im.get_flattened_data())

    # ------------------------------------------------------------ 1. orcamento
    if tiles_novos and max(tiles_novos) >= TETO_TILES:
        mau.append("estoura o teto de %d tiles" % TETO_TILES)
    if metas and max(metas) >= TETO_META:
        mau.append("estoura o teto de %d metatiles" % TETO_META)
    for local in metas:
        if local in set(QUEBRADOS):
            mau.append("o metatile %d e um dos 65 quebrados congelados"
                       % (512 + local))
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

    # ---------- 2. o kit nao pode importar paleta de origem fora de VAGAS_PAL
    for ch in dados["tiles"]:
        ip = int(ch.split(":")[2])
        if ip not in VAGAS_PAL:
            mau.append("o kit importou a paleta %d da fonte, fora do plano" % ip)

    # -------- 3. CHAO novo: atributo identico ao do carimbo em que ele pousa e,
    #             quando importado, camada de cima VAZIA
    importados = {c["nome"] for c in CHAO_AREIA}
    for nome, gid in catalogo["chao"].items():
        qual = catalogo["sobre"][nome]
        _b, attr_chao = chao_nosso(qual)
        if atributo(gid) != attr_chao:
            mau.append("o chao %s (%d) tem atributo 0x%04X e o carimbo de %s tem "
                       "0x%04X" % (nome, gid, atributo(gid), qual, attr_chao))
        cima = [e for e in entradas(gid)[4:] if e & 0x3FF]
        if cima and nome in importados:
            mau.append("o chao importado %s (%d) usa a camada de cima"
                       % (nome, gid))
        # CAMADA DE CIMA EM CHAO ANDAVEL. Com layerType NORMAL ela vai para o
        # BG1, que desenha ACIMA do sprite. O tufo de grama nosso desenha em
        # cima de proposito, que e o "jogador atras do mato" do jogo base; o que
        # ele nao pode e tapar o jogador INTEIRO, que e o defeito E3 do
        # `mapas_qa.py`.
        if cima and (atributo(gid) >> 12) & 0xF != 1:
            op = 0
            for e in cima:
                vaga = (e & 0x3FF) - len(tp["tiles"])
                op += (_opacos(tiles_novos[vaga]) if vaga in tiles_novos
                       else _opacos(RM.resolver_tile(tp, ts, e & 0x3FF)))
            if op >= 4 * 64:
                mau.append("o chao %s (%d) tapa o jogador inteiro (E3)"
                           % (nome, gid))

    # ------- 4. MOVEL e BASE: COVERED, comportamento zerado, e o NOSSO chao
    #            entrada por entrada na camada de baixo
    ids_base = {}
    for nome, info in catalogo["blocos"].items():
        for gid in info["base"]:
            ids_base[gid] = nome
    for gid, nome in list((g, n) for n, g in catalogo["moveis"].items()) \
            + list(ids_base.items()):
        qual = catalogo["sobre"][nome]
        base, _ac = chao_nosso(qual)
        a = atributo(gid)
        if (a >> 12) & 0xF != 1:
            mau.append("o movel %s (%d) nao esta em COVERED" % (nome, gid))
        if a & 0xFF:
            mau.append("o movel %s (%d) importou comportamento 0x%02X da fonte"
                       % (nome, gid, a & 0xFF))
        if entradas(gid)[:4] != base:
            mau.append("o movel %s (%d) nao tem o nosso chao de %s na camada de "
                       "baixo" % (nome, gid, qual))

    # ---- 5. TOPO de bloco: continua ANDAVEL com o atributo do chao, e a arte
    #        dele NAO pode ser 100% opaca, senao ela tapa o jogador (E3)
    for nome, info in catalogo["blocos"].items():
        qual = catalogo["sobre"][nome]
        base, attr_chao = chao_nosso(qual)
        for gid in info["topo"]:
            if atributo(gid) != attr_chao:
                mau.append("o topo de bloco %s (%d) nao herdou o atributo do "
                           "chao" % (nome, gid))
            if entradas(gid)[:4] != base:
                mau.append("o topo de bloco %s (%d) nao tem o nosso chao "
                           "embaixo" % (nome, gid))
            px = 0
            for e in entradas(gid)[4:]:
                if e & 0x3FF:
                    vaga = (e & 0x3FF) - len(tp["tiles"])
                    px += (_opacos(tiles_novos[vaga]) if vaga in tiles_novos
                           else 64)
            if px >= 4 * 64:
                mau.append("o topo de bloco %s (%d) tapa o jogador inteiro (E3)"
                           % (nome, gid))

    # ---------- 6. nenhuma variante de chao e copia pixel a pixel de outra
    for qual in ("grama", "areia"):
        lista = [g for n, g in catalogo["chao"].items()
                 if catalogo["sobre"][n] == qual] + [CARIMBOS[qual]]
        pix = {mt: px_de(mt) for mt in lista}
        for i, a in enumerate(lista):
            for b in lista[i + 1:]:
                dd = sum(sum((x - y) ** 2 for x, y in zip(p, q)) ** 0.5
                         for p, q in zip(pix[a], pix[b])) / 256.0
                if dd < 8.0:
                    mau.append("as variantes de chao %d e %d de %s tem distancia "
                               "%.1f, abaixo do piso de 8,0 do varia_carimbo.py: "
                               "isso e enganar a regua" % (a, b, qual, dd))

    # -------------------------------------------- 7 a 13. o plano, mapa a mapa
    for alvo in alvos:
        L, W, H, v, escritas, contas = planos[alvo]
        d = json.load(open(f"{RAIZ}/data/maps/{alvo}/map.json"))
        ev = E.eventos(d)
        saida = list(v)
        for i, val in escritas.items():
            saida[i] = val
        meus_chaos = {catalogo["chao"][n]: n for n in catalogo["chao"]}
        meus_moveis = {catalogo["moveis"][n]: n for n in catalogo["moveis"]}
        meus_topos = {t: n for n, b in catalogo["blocos"].items() for t in b["topo"]}
        meus_bases = {t: n for n, b in catalogo["blocos"].items() for t in b["base"]}
        carimbos_val = set(CARIMBOS.values())

        for i, val in escritas.items():
            x, y = i % W, i // W
            novo, velho = val & 0x3FF, v[i] & 0x3FF
            cn, cv = (val >> 10) & 3, (v[i] >> 10) & 3
            if (val >> 12) & 0xF != (v[i] >> 12) & 0xF:
                mau.append("%s: mudou ELEVACAO em (%d,%d)" % (alvo, x, y))
            if cv and not cn:
                mau.append("%s: colisao 1 -> 0 em (%d,%d), que segue proibida"
                           % (alvo, x, y))
            if novo in meus_chaos or novo in meus_topos:
                nome = meus_chaos.get(novo) or meus_topos.get(novo)
                if cn != cv or velho != CARIMBOS[catalogo["sobre"][nome]]:
                    mau.append("%s: chao/topo em celula errada em (%d,%d)"
                               % (alvo, x, y))
            elif novo in meus_moveis or novo in meus_bases:
                nome = meus_moveis.get(novo) or meus_bases.get(novo)
                if cv or not cn:
                    mau.append("%s: movel em (%d,%d) nao e solidificacao 0 -> 1"
                               % (alvo, x, y))
                if velho != CARIMBOS[catalogo["sobre"][nome]]:
                    mau.append("%s: movel fora do carimbo em (%d,%d)" % (alvo, x, y))
                if (x, y) in ev:
                    mau.append("%s: movel em cima do evento (%d,%d)" % (alvo, x, y))
            else:
                mau.append("%s: metatile %d escrito em (%d,%d) e de fora do kit"
                           % (alvo, novo, x, y))

        # 8. (comportamento, layerType) de toda celula ANDAVEL fica igual
        for i in range(W * H):
            if (saida[i] >> 10) & 3:
                continue
            a, b = atributo(v[i] & 0x3FF), atributo(saida[i] & 0x3FF)
            if (a & 0xFF, a & 0xF000) != (b & 0xFF, b & 0xF000):
                mau.append("%s: celula andavel (%d,%d) mudou (comportamento, "
                           "layerType)" % (alvo, i % W, i // W))
                break

        # 9 e 10. alcance a pe e LIGACAO a pe
        ini = E.partidas(d, W, H, v)
        antes, depois = E.alcance(v, W, H, ini), E.alcance(saida, W, H, ini)
        solid = {(i % W, i // W) for i in escritas
                 if not ((v[i] >> 10) & 3) and ((escritas[i] >> 10) & 3)}
        if (antes - depois) - solid:
            mau.append("%s: o alcance a pe perdeu %d celulas alem das "
                       "solidificadas: %s"
                       % (alvo, len((antes - depois) - solid),
                          sorted((antes - depois) - solid)[:6]))
        if depois - antes:
            mau.append("%s: o alcance a pe GANHOU celula" % alvo)
        mau += ["%s: %s" % (alvo, q) for q in
                ligacao_intacta(componentes(v, W, H), componentes(saida, W, H),
                                solid)]

        # 11. A MANCHA NAO PODE SER ADIVINHAVEL, e o teste tem dois lados.
        #  (a) PADRAO: nenhuma projecao simples da posicao pode ADIVINHAR a peca.
        #      A conta e por EIXO (x, y, x+y, x-y) e por MODULO de 2 a 8,
        #      chutando dentro de cada classe de resto a peca mais comum dela,
        #      contra o chute cego da peca mais comum do mapa.
        #  (b) FORMA: mancha e BOLHA, nao sal e pimenta, e a conta e o TAMANHO
        #      MEDIO do pedaco conexo, nao quantas vizinhas cada celula tem.
        mancha = {(i % W, i // W): (val & 0x3FF) for i, val in escritas.items()
                  if (val & 0x3FF) in meus_chaos}
        if len(mancha) < 120:
            mau.append("%s: so %d celulas de mancha" % (alvo, len(mancha)))
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
                    if ac - cego > 0.12:
                        mau.append("%s: saber %s mod %d adivinha a peca em %.0f%% "
                                   "das celulas contra %.0f%% do chute cego: "
                                   "virou padrao" % (alvo, rot, mod, 100 * ac,
                                                     100 * cego))
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
                mau.append("%s: a mancha media tem so %.1f celulas (%d em %d "
                           "pedacos): virou sal e pimenta, nao bolha"
                           % (alvo, len(mancha) / pedacos, len(mancha), pedacos))

        # 12. a regua tem que fechar em 20% ou menos
        b, nb, idb = regua(v, W, H, L, escritas)
        if b > TETO_REGUA:
            mau.append("%s: a regua ainda marca %.1f%% de carimbo dominante"
                       % (alvo, b))

        # 13. o bloco 2x2: toda BASE tem um TOPO logo acima, e as contas batem
        bases = {(i % W, i // W) for i, val in escritas.items()
                 if (val & 0x3FF) in meus_bases}
        topos = {(i % W, i // W) for i, val in escritas.items()
                 if (val & 0x3FF) in meus_topos}
        if len(bases) != len(topos):
            mau.append("%s: %d bases de bloco e %d topos" % (alvo, len(bases),
                                                             len(topos)))
        for x, y in bases:
            if (x, y - 1) not in topos:
                mau.append("%s: a base de bloco em (%d,%d) esta sem topo"
                           % (alvo, x, y))
                break
    return mau


# ------------------------------------------------------------------ auto-teste
def demo(alvos):
    """Prova positiva e as provas NEGATIVAS, cada sabotagem revertida em seguida.

    "Zero diferenca" so vale depois que a comparacao mostra que sabe reprovar.
    """
    tiles_novos, metas, attrs, catalogo = desenha_kit()
    guardado = carrega_plano()
    planos = {}
    for alvo in ORDEM:
        planos[alvo] = plano_mapa(alvo, catalogo, base_de(alvo, guardado))

    ts_do_disco = _tileset(SECUNDARIO)
    mau = confere(ORDEM, tiles_novos, metas, attrs, catalogo, planos)
    negativas = []

    def sabota(nome, funcao, espera):
        """Roda `funcao`, que devolve os dados sabotados, e exige acusacao."""
        args = funcao()
        queixas = confere(ORDEM, *args)
        pega = [q for q in queixas if espera in q]
        if not pega:
            mau.append("SABOTAGEM NAO ACUSADA (%s): %s" % (nome, queixas[:2]))
        else:
            negativas.append((nome, pega[0]))

    def copia():
        return (dict(tiles_novos), dict(metas), dict(attrs),
                json.loads(json.dumps(catalogo)),
                {k: (v[0], v[1], v[2], list(v[3]), dict(v[4]), v[5])
                 for k, v in planos.items()})

    alvo0 = "SandgemTown"

    # N1. colisao 1 -> 0 numa celula de mancha
    def n1():
        a = copia()
        L, W, H, v, esc, ct = a[4][alvo0]
        i = sorted(esc)[0]
        v[i] = v[i] | (1 << 10)          # a celula ERA solida
        return a
    sabota("colisao 1 -> 0", n1, "colisao 1 -> 0")

    # N2. elevacao alterada
    def n2():
        a = copia()
        L, W, H, v, esc, ct = a[4][alvo0]
        i = sorted(esc)[0]
        esc[i] = (esc[i] & 0x0FFF) | (((v[i] >> 12) + 1) & 0xF) << 12
        return a
    sabota("elevacao alterada", n2, "mudou ELEVACAO")

    # N3. comportamento de um metatile de CHAO importado sabotado
    def n3():
        a = copia()
        gid = a[3]["chao"][CHAO_AREIA[0]["nome"]]
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

    # N5. base de bloco gravada SEM o topo
    def n5():
        a = copia()
        L, W, H, v, esc, ct = a[4][alvo0]
        topos = {t for b in catalogo["blocos"].values() for t in b["topo"]}
        for i in sorted(esc):
            if (esc[i] & 0x3FF) in topos:
                del esc[i]
                break
        return a
    sabota("base de bloco sem o topo", n5, "bases de bloco e")

    # N6. camada de BAIXO de um movel sabotada (chao da fonte em vez do nosso)
    def n6():
        a = copia()
        gid = a[3]["moveis"][MOVEIS_LP[0]["nome"]]
        ent = list(a[1][gid - 512])
        ent[0] = ent[4]
        a[1][gid - 512] = ent
        return a
    sabota("camada de baixo sabotada", n6, "nao tem o nosso chao de")

    # N7. a peca de AREIA pousando na camada de baixo da GRAMA. E a sabotagem que
    #     so existe porque esta passada tem DOIS carimbos: com um so, trocar a
    #     base por outra base nao teria como acontecer. Ela ataca o pe do
    #     coqueiro, que e a unica peca importada que pousa na areia.
    def n7():
        a = copia()
        gid = a[3]["blocos"]["coqueiro"]["base"][0]
        base_g, _ = chao_nosso("grama")
        a[1][gid - 512] = list(base_g) + list(a[1][gid - 512])[4:]
        return a
    sabota("movel de areia com chao de grama", n7, "nao tem o nosso chao de areia")

    # N8. mancha escolhida por (x + y) % n, que e xadrez com periodo
    def n8():
        a = copia()
        original = globals()["peca_da_mancha"]
        globals()["peca_da_mancha"] = lambda nomes, x, y: nomes[(x + y) % len(nomes)]
        try:
            for alvo in ORDEM:
                a[4][alvo] = plano_mapa(alvo, catalogo, base_de(alvo, guardado))
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
            for alvo in ORDEM:
                a[4][alvo] = plano_mapa(alvo, catalogo, base_de(alvo, guardado))
        finally:
            globals()["peca_da_mancha"] = original
        return a
    sabota("mancha por x % n", n9, "virou padrao")

    # N10. corredor fechado que PARTE um pedaco de chao. O portao de alcance
    #      sozinho nao pega isso quando ha warp dos dois lados, e foi assim que
    #      Snowpoint passou verde com a cidade cortada.
    def n10():
        a = copia()
        L, W, H, v, esc, ct = a[4][alvo0]
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
        nomes = [c["nome"] for c in CHAO_AREIA]
        a[1][a[3]["chao"][nomes[1]] - 512] = list(a[1][a[3]["chao"][nomes[0]] - 512])
        return a
    sabota("variante de chao duplicada", n11, "abaixo do piso de 8,0")

    # N12. cor nova escrita num indice que os NOSSOS pixels ja usam. Aqui a
    #      sabotagem precisa INVENTAR a vaga: as tres que este kit usa (6, 7 e
    #      11) estao 100% livres, nenhum pixel vivo pinta com elas, e por isso
    #      nao ha indice ocupado nelas para estragar. A que tem indice ocupado e
    #      a vaga 8 (12 cores em uso e so os indices 8, 9 e 15 livres), entao o
    #      kit e reescrito no disco declarando a vaga 8 com o indice 1 trocado.
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

    # N13. gravar num dos 65 metatiles QUEBRADOS congelados
    def n13():
        a = copia()
        local = QUEBRADOS[0]
        a[1][local] = list(a[1][min(a[1])])
        a[2][local] = 0x1000
        return a
    sabota("grava em metatile quebrado", n13, "quebrados congelados")

    # ------------------------------------------------ o que esta NO DISCO
    # Sem este caso o auto-teste so confere o que ele mesmo acabou de calcular.
    from PIL import Image
    meta_disco = _ler("metatiles.bin")
    attr_disco = _ler("metatile_attributes.bin")
    png = Image.open(f"{DESTINO}/tiles.png")
    cols = png.size[0] // 8
    px = png.convert("P").load()

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
    for alvo in ORDEM:
        L, W, H, v, escritas, contas = planos[alvo]
        saida = list(v)
        for i, val in escritas.items():
            saida[i] = val
        volta = list(saida)
        for i in sorted(escritas):
            if volta[i] == escritas[i]:
                volta[i] = v[i]
        if volta != list(v):
            mau.append("%s: desfazer nao devolve a base" % alvo)
        _, _, _, _, esc2, _ = plano_mapa(alvo, catalogo, volta)
        if esc2 != escritas:
            mau.append("%s: segunda passada deu plano diferente" % alvo)

    if mau:
        print("DEMO VERMELHA")
        for x in dict.fromkeys(mau):
            print("  -", x)
        return 1
    print("DEMO VERDE")
    for alvo in ORDEM:
        L, W, H, v, escritas, contas = planos[alvo]
        a, na, ida = regua(v, W, H, L)
        b, nb, idb = regua(v, W, H, L, escritas)
        print("  %-13s %d celulas mudadas, %d solidificadas, regua %.1f%% -> %.1f%%"
              % (alvo, len(escritas), contas["solidos"], a, b))
    print("  %d tiles, %d metatiles, %d provas negativas:" % (len(tiles_novos),
                                                              len(metas),
                                                              len(negativas)))
    for nome, queixa in negativas:
        print("    %-32s -> %s" % (nome, queixa[:100]))
    return 0


# --------------------------------------------------------- prova de EXTRACAO
def prova_extracao(pasta=None):
    """Desenha o mapa g00m01 do hack DUAS vezes e exige ZERO pixel de diferenca.

    Esta e a prova na CAMADA DA AFIRMACAO, e nao no plano em memoria. De um lado,
    o mapa desenhado DIRETO DA ROM pelo `ferramentas/prova_extracao.py`; do
    outro, o MESMO mapa desenhado pelo `dev_scripts/render_maps.py` deste repo a
    partir do par de tilesets EXTRAIDO para pasta. Se os dois baterem pixel a
    pixel, a leitura de tile, de paleta, de metatile e de split de VRAM que este
    script usa esta certa; se um nibble estiver trocado, a arte importada ainda
    "pareceria arte", so que errada, que e o risco 1 do PRD.

    Ela nao instala nada dentro do repositorio de verdade: monta um REPO MINIMO
    numa pasta temporaria (o `layouts.json`, um `map.json`, o `graphics.h` e o
    `headers.h` que o `render_maps.py` precisa para achar as pastas) e aponta o
    `REPO_MAPAS` para la.

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
    raiz = pasta or tempfile.mkdtemp(prefix="prova-costa-")
    mini = os.path.join(raiz, "minirepo")
    for sub in ("data/layouts/HackAmostra", "data/maps/HackAmostra",
                "data/tilesets/primary", "data/tilesets/secondary",
                "src/data/tilesets"):
        os.makedirs(os.path.join(mini, sub), exist_ok=True)

    # 1. extrai o par para pasta, com o mesmo split que o kit usou
    for off, sub, flag in ((LP["pri"], "primary/lp_pri", []),
                           (LP["sec"], "secondary/lp_sec", ["--sec"])):
        alvo = os.path.join(mini, "data/tilesets", sub)
        cmd = ["python3", f"{F}/extrai_tileset.py", LP["slug"], "0x%X" % off,
               alvo, "--split", str(LP["split"][1])] + flag
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode:
            raise SystemExit("extrai_tileset falhou: %s" % (r.stderr or r.stdout))

    # 2. o mapa de amostra: o g00m01, a vila costeira 78x60 que usa o par
    sys.path.insert(0, F)
    from gbamap import Rom  # noqa: E402
    p = os.path.join(ferr, LP["slug"])
    gba = [f for f in sorted(os.listdir(p)) if f.lower().endswith(".gba")][0]
    r = Rom(os.path.join(p, gba))
    r.n_meta_pri, r.n_tiles_pri, r.n_pal_pri = LP["split"]
    inv = json.load(open(f"{F}/inv/{LP['slug']}.json"))
    hdr = inv["grupos"][0]["mapas"][1]
    L = hdr["layout"]
    if (L["ts1"], L["ts2"]) != (LP["pri"], LP["sec"]):
        raise SystemExit("o g00m01 usa 0x%X/0x%X, e o kit veio de 0x%X/0x%X"
                         % (L["ts1"], L["ts2"], LP["pri"], LP["sec"]))
    w, h = L["w"], L["h"]
    palavras = struct.unpack_from("<%dH" % (w * h), r.rom, L["blockdata"])
    with open(os.path.join(mini, "data/layouts/HackAmostra/map.bin"), "wb") as f:
        f.write(struct.pack("<%dH" % (w * h), *palavras))

    # 3. o repo minimo que o render_maps.py sabe ler
    with open(os.path.join(mini, "data/layouts/layouts.json"), "w") as f:
        json.dump(dict(layouts_table_label="gMapLayouts", layouts=[dict(
            id="LAYOUT_HACK_AMOSTRA", name="HackAmostra_Layout", width=w,
            height=h, primary_tileset="gTileset_LpPri",
            secondary_tileset="gTileset_LpSec",
            border_filepath="data/layouts/HackAmostra/border.bin",
            blockdata_filepath="data/layouts/HackAmostra/map.bin")]), f)
    with open(os.path.join(mini, "data/maps/HackAmostra/map.json"), "w") as f:
        json.dump(dict(id="MAP_HACK_AMOSTRA", name="HackAmostra",
                       layout="LAYOUT_HACK_AMOSTRA", object_events=[],
                       warp_events=[], coord_events=[], bg_events=[]), f)
    with open(os.path.join(mini, "src/data/tilesets/graphics.h"), "w") as f:
        for lab, sub in (("LpPri", "primary/lp_pri"), ("LpSec", "secondary/lp_sec")):
            f.write('const u32 gTilesetTiles_%s[] = INCGFX_U32("data/tilesets/%s'
                    '/tiles.png", ".4bpp.smol");\n' % (lab, sub))
    with open(os.path.join(mini, "src/data/tilesets/headers.h"), "w") as f:
        for lab in ("LpPri", "LpSec"):
            f.write("const struct Tileset gTileset_%s =\n{\n    .tiles = "
                    "gTilesetTiles_%s,\n};\n" % (lab, lab))

    # 4. desenha pelos DOIS caminhos e compara
    png_repo = os.path.join(raiz, "HackAmostra.png")
    png_rom = os.path.join(raiz, "g00m01-rom.png")
    amb = dict(os.environ, REPO_MAPAS=mini, SAIDA_MAPAS=raiz)
    rr = subprocess.run(["python3", f"{RAIZ}/dev_scripts/render_maps.py",
                         "HackAmostra"], capture_output=True, text=True, env=amb)
    if not os.path.exists(png_repo):
        raise SystemExit("render_maps nao desenhou: %s" % (rr.stdout + rr.stderr))

    def compara():
        return subprocess.run(["python3", f"{F}/prova_extracao.py", LP["slug"],
                               "0", "1", png_repo, png_rom, "--split",
                               str(LP["split"][1])], capture_output=True, text=True)

    saida = compara()
    print(saida.stdout.strip())
    if saida.returncode:
        return 1

    # 5. a comparacao tem que saber REPROVAR. Um unico nibble do tile mais
    #    desenhado do mapa e trocado no `tiles.png` extraido, e a prova roda de
    #    novo; depois o pixel volta e ela tem que aprovar outra vez.
    from PIL import Image
    conta = collections.Counter()
    for pal in palavras:
        mt = pal & 0x3FF
        conta[mt] += 1
    quente = conta.most_common(1)[0][0]
    lado = "primary/lp_pri" if quente < LP["split"][0] else "secondary/lp_sec"
    caminho = os.path.join(mini, "data/tilesets", lado, "tiles.png")
    im = Image.open(caminho)
    px = im.load()
    antigo = px[3, 3]
    px[3, 3] = (antigo + 5) % 16
    im.save(caminho)
    rr = subprocess.run(["python3", f"{RAIZ}/dev_scripts/render_maps.py",
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
    """Cada tile do kit, DEPOIS de reindexado, contra o tile da ROM: zero pixel.

    Reindexar nibble e a unica coisa que este kit faz com o desenho da fonte, e e
    exatamente onde um erro passaria despercebido: a arte continuaria parecendo
    arte, com as cores trocadas de lugar. A conta e direta: para cada tile do
    kit, o pixel (x,y) tem que ter a MESMA COR RGB que o pixel (x,y) do tile
    correspondente da ROM, lido com a paleta de origem dele.
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
    t1, t2 = r.parse_tileset(LP["pri"]), r.parse_tileset(LP["sec"])
    pal = {i: _rgb(t1 if i < 6 else t2, i) for i in range(16)}
    dados = kit()
    tiles_novos, _m, _a, _c = desenha_kit()
    inverso = {}
    for ch, vaga in dados["tiles_vaga"].items():
        inverso[ch] = vaga
    # a vaga fisica de cada chave, na mesma ordem em que `desenha_kit` aloca
    ordem = {}
    for local, tile in sorted(tiles_novos.items()):
        for ch, px in dados["tiles"].items():
            if px == tile and ch not in ordem:
                ordem[ch] = local
                break
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
    # a conta tem que saber REPROVAR
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


def alvos_do_argv():
    alvos = list(ORDEM)
    for i, a in enumerate(sys.argv):
        if a == "--mapa":
            alvos = [sys.argv[i + 1]]
    for a in alvos:
        if a not in TEMAS:
            raise SystemExit("mapa desconhecido: %s" % a)
    return alvos


def main():
    if "--extrai" in sys.argv:
        return extrai()
    if "--prova-extracao" in sys.argv:
        return prova_extracao()
    if "--prova-tiles" in sys.argv:
        return prova_tiles()
    if "--desfazer" in sys.argv:
        return desfaz(alvos_do_argv())
    if "--demo" in sys.argv or "--autoteste" in sys.argv:
        return demo(alvos_do_argv())
    if "--so-tileset" in sys.argv:
        t, m, at, c = desenha_kit()
        grava_tileset(t, m, at)
        print("tileset escrito: %d tiles, %d metatiles" % (len(t), len(m)))
        return 0
    return roda(alvos_do_argv(), "--aplicar" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
