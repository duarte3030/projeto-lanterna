#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Refino de `MossdeepCity` (tema ESPAÇO E COSTA), no `gTileset_Mossdeep`.

O QUE ESTA CIDADE TEM DE ERRADO, medido pela `dev_scripts/regua_cidades.py`
nesta árvore em 09/09/2026: das 1.291 células andáveis a pé, **440 (34,1%) são o
metatile 1**, a grama lisa do `gTileset_General`. Mossdeep é a ilha do Space
Center, do ginásio dos gêmeos Tate e Liza e da casa do Steven, é a SEGUNDA MAIOR
cidade desta onda e mesmo assim o chão dela é um bloco de dezesseis pixels
repetido quatrocentas e quarenta vezes, do pátio do centro espacial até a beira
do mar.

As 440 células estão TODAS com o atributo `0x0000` (comportamento zero,
`layerType` NORMAL); isso foi medido, não suposto. Elas NÃO estão todas na mesma
elevação: são 257 na 5, 123 na 7, 55 na 9 e 5 na 4, porque a ilha é de vários
patamares ligados por escada. Isso não atrapalha a mancha (mancha não muda
elevação nem colisão) e é justamente por isso que o portão de alcance roda com
`corredores_multinivel`, e não com o `corredores_de_teste`, que não conhece
elevação 15.

O QUE NÃO É MEXIDO, e cada coisa por um motivo medido:

  - A ÁGUA. O mar em volta é caminho de Surf e nenhuma célula dele muda. São 751
    células do metatile 368 (`MB_OCEAN_WATER`) e mais 235 do metatile 414
    (`MB_SHALLOW_WATER`), o lençol raso do oeste e a orla da ilha. O 414 É
    contado como chão andável a pé pela régua (o comportamento dele não está na
    lista de `enfeita_cidades.agua()`), e por isso ele é quem herda o posto de
    carimbo dominante depois desta passada. **Ele podia ter sido quebrado sem
    custo nenhum**: medido aqui, CINCO dos nove arranjos de espelho do par
    448/449 passam no piso de 8,0 do `varia_carimbo.py` (os quatro mistos caem
    em 6,7 e seriam cortados), e espelhar não muda o tile que a animação
    escreve, então a água continuaria animando. Não foi feito de propósito: a
    regra desta frente é que nenhuma célula de água muda, e os tiles 448 e 449
    são vagas ANIMADAS do `gTileset_General` (a faixa 432 a 461, medida com o
    `dev_scripts/pinos_anim.py`), ou seja arte do primário compartilhado por
    toda a Hoenn. Fica escrito com o número para o condutor decidir, e não
    escondido atrás de "não deu".

  - A AREIA QUE JÁ ESTÁ NO MAPA (os metatiles 280, 281, 282, 288, 289, 290, 296,
    297 e 298, 214 células somadas) é a rede de caminho que o Emerald desenhou
    ligando as portas da cidade. Ela não é reescrita: o que esta passada faz é
    USAR o autotile dela para abrir manchas NOVAS de duna dentro da grama.

  - A GRAMA DEBAIXO DE ÁRVORE E DE ESCADA (os metatiles 4, 794 e 795, 74 células
    somadas) tem arte na camada de cima e fica onde está.

O QUE ESTA PASSADA FAZ, na ordem em que paga:

  1. COMPACTA O TILESET, e é o que paga o orçamento. O `gTileset_Mossdeep`
     estava em 512 de 512 tiles e 279 deles eram MORTOS: nenhum metatile os
     referenciava. O `compacta_tileset.py` desceu para 233 tiles vivos (240 no
     png, que é o próximo múltiplo de 16) e devolveu 272 vagas até o teto de
     512. A prova é de PIXEL: os SETE mapas irmãos foram renderizados antes e
     depois e a diferença é ZERO em 8.601.600 pixels. Não há pino de animação
     nenhum para proteger: o `pinos_anim.py` diz que o
     `InitTilesetAnim_Mossdeep` põe `sSecondaryTilesetAnimCallback = NULL` e não
     escreve vaga nenhuma em tempo de execução. E o `src/data/tilesets/
     graphics.h` NÃO foi tocado, porque a linha do Mossdeep não declara
     `-num_tiles`, ao contrário da do Dewford e da do Rustboro.

  2. AS TRÊS FAMÍLIAS DE AUTOTILE QUE JÁ ESTAVAM PAGAS. O achado que barateia
     esta cidade inteira: o `gTileset_General` já tem TRÊS autotiles de nove
     peças desenhados sobre a nossa grama, e os vinte e sete metatiles deles
     têm atributo `0x0000`, igual ao do carimbo. São a AREIA (280 a 298), a
     GRAMA CLARA (464 a 482) e a TERRA (259 a 277). Esta passada usa as duas
     primeiras: custo ZERO de tile, de cor e de metatile pela borda inteira, e o
     que se gasta é só o MIOLO. A terra ficou de fora porque o miolo dela (o
     268) é `MB_BERRY_TREE_SOIL`, comportamento próprio, e entraria remontada
     por uma vaga de metatile que rende pouco numa cidade que já tem duas
     famílias de mancha.

  3. O RUÍDO DE ARRANJO na grama que sobra, por espelho e rearranjo dos DOIS
     tiles do próprio carimbo (o 2 e o 3 do `gTileset_General`, na paleta 2).
     Custo ZERO de tile e de cor. Os NOVE arranjos passam no piso de 8,0 (a
     grama tem pinta; a areia, quase chapada, teria os nove cortados, e o
     gerador corta sozinho). É a camada SUTIL, e é ela que derruba a coluna
     `liso`.

  4. OS DETALHES DE COSTA, na segunda passada de ruído, cada um desenhado SOBRE
     o tile do próprio carimbo (a máscara só troca os pixels do detalhe), de
     modo que o detalhe casa com a grama por construção em vez de casar por
     sorte: touceira de capim de praia, concha, seixo, respingo de areia,
     florzinha e cabo de serviço. Eles são ESPARSOS por desenho: o ruído de
     arranjo roda ANTES e come nove décimos das células, e só o que sobra chega
     aqui.

  5. A MOBÍLIA DE BEIRA, em células solidificadas, sempre com comportamento
     ZERADO e `layerType` COVERED, sempre encostada em prédio, penhasco ou na
     borda do mapa. Cinco peças DESENHADAS aqui, do vocabulário do centro
     espacial e do cais (tambor, caixa de equipamento, antena pequena, carretel
     de cabo e boia), quatro peças de custo ZERO que o `gTileset_General` já
     desenhou sobre a nossa grama e que a cidade NÃO USA em lugar nenhum (as
     pedras 110 e 111, o matacão 224 e o mourão 307, conferidos um a um no
     `map.bin`) e a cerca branca 328/329/330, também de custo zero e também
     ausente do mapa.

A PALETA, e o truque que faz o custo de cor ser ZERO: a arte nova mora no
`tiles.png` do SECUNDÁRIO mas é pintada com paleta do PRIMÁRIO. O índice de
paleta de uma entrada de metatile não tem nada a ver com o lado de onde o tile
vem, e é isso que o `70aea067d5` (Goldenrod) usou. Os detalhes de grama usam a
paleta 2, a mesma do carimbo; a areia e a mobília técnica usam a paleta 5, a
mesma da areia do mapa. Nenhum byte de `data/tilesets/secondary/mossdeep/
palettes/` muda, e as paletas livres 6 e 12 do secundário continuam livres.

A FONTE DE ARTE, e as TRÊS REPROVAÇÕES, cada uma com o número na mão. O índice
`/tmp/claude-501/FONTES-POR-TILESET.md` dá TRÊS candidatos para
`secondary/mossdeep`. Os três foram extraídos com o `extrai_tileset.py`,
renderizados e medidos metatile a metatile contra os nossos quatro chãos. As
cores médias dos nossos: grama (116,5; 197,4; 165,0), areia (222,0; 204,4;
130,6), raso (155,7; 165,5; 193,0).

  - `light-platinum 0x286DE4` (arte nova 0,985, 7 usos, amostra g00m03 36x46).
    Varrendo os 512 metatiles dele e ficando só com os que poderiam ser chão (a
    camada de cima VAZIA e as quatro entradas de baixo vindas do próprio
    secundário, para não medir tile de um primário que não foi extraído),
    sobram 21 metatiles e 84 comparações. O MELHOR fica a **57,5** do nosso
    raso, contra o critério de cerca de 50 que Pastoria, Sandgem e Hearthome
    fixaram, e ampliado ele é PARALELEPÍPEDO CINZA COM TERRA, calçamento de
    vila de montanha. Contra a nossa grama e a nossa areia ele passa de 68.
    REPROVADO por cor.

  - `x-y-emerald 0x3DF794` (0,837, 13 usos, g00m12 20x20). O melhor fica a
    **52,6** do nosso raso e a 77,0 da nossa areia, e ampliado é MÁRMORE CLARO
    COM MOTIVO DE FLOR DE QUATRO PONTAS, piso de interior. REPROVADO por cor e
    por desenho.

  - `x-y-emerald 0x3DF71C` (0,837, 6 usos, g00m00 30x45). Este é o único que
    PASSA no critério de cor: o metatile local 279 fica a **14,9** da nossa
    grama. E é exatamente por isso que ele mostra o que a régua de cor sozinha
    não vê: medido pixel a pixel, ele tem **UMA COR SÓ**, (112,192,160), um
    quadrado verde CHAPADO. Importar o chão mais parecido do índice seria
    importar o contrário do que esta onda existe para fazer, que é tirar chão
    chapado do mapa. Os outros três dele (locais 174, 182 e 198) ficam entre
    57,4 e 60,6 e são campo de flor amarelada. REPROVADO por desenho, com a
    distância a favor dele.

  Consequência direta: **NADA FOI IMPORTADO, e por isso o `CREDITS.md` NÃO FOI
  TOCADO**. Abrir seção vazia seria mentira de arquivo.

O QUE FICOU DE FORA, com o motivo medido:

  - O PÁTIO DE LAJOTA TÉCNICA do Space Center, que seria a peça mais temática
    desta cidade. Ele morreu na GEOMETRIA, não no gosto: a grama de Mossdeep é
    fita estreita entre prédio, penhasco e caminho de areia, e o mapa inteiro
    só tem ONZE cantos de retângulo 3x3 de grama, contra os 534 de calçamento
    contínuo que Rustboro tinha. Dos onze, só CINCO ficam a leste de x=56 e os
    cinco estão em y>=23, ou seja a mais de seis células do bloco do centro
    espacial, que ocupa de y=2 a y=17. Um autotile próprio de nove peças mais
    meio fio custa onze vagas de metatile e seis de tile para render dois
    remendos de dezoito células que não encostam no prédio a que pertencem. A
    lajota que sobreviveu está na MOBÍLIA, que é onde o vocabulário técnico
    cabe sem pedir vão largo.

  - A TERRA (o autotile 259 a 277) como terceira família, pelo motivo do item 2
    acima.

  - Os metatiles 806, 807, 815, 819, 821, 852 e 860 do `gTileset_Mossdeep`, que
    são os SETE metatiles de camada de baixo igual à do carimbo que nenhum dos
    sete irmãos usa, ou seja móvel de custo zero por definição. Olhados
    ampliados, os sete são PEDAÇO DE FACHADA: parede de casa, degrau de escada,
    painel de janela e bloco de telhado. Fachada deitada no chão é o defeito que
    Rustboro mediu nos metatiles 574 e 660. Os que ENTRAM são os quatro do
    primário, que são pedra e mourão, arte feita para ficar em pé no chão.

  - O metatile 27 (a placa) como móvel: placa sem texto atrás é promessa que o
    jogo não cumpre, e Littleroot, Lavaridge e Rustboro já reprovaram a mesma
    peça pelo mesmo motivo. Texto atrás exigiria `bg_event` novo no `map.json`,
    e o `map.json` fica INTOCADO.

  - As florzinhas do metatile 4 como móvel: a cidade já tem QUARENTA E OITO
    delas, medido no `map.bin`. Flor número quarenta e nove não é enfeite, é
    repetição. A florzinha que ENTRA é DETALHE de chão, andável, e não móvel.

Uso:
    python3 dev_scripts/costa_mossdeep.py
    python3 dev_scripts/costa_mossdeep.py --aplicar
    python3 dev_scripts/costa_mossdeep.py --desfazer
    python3 dev_scripts/costa_mossdeep.py --demo
    python3 dev_scripts/costa_mossdeep.py --so-tileset
"""
import collections
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")
os.environ.setdefault("REPO_MAPAS", RAIZ)
import enfeita_cidades as E          # noqa: E402
import mato_littleroot as M          # noqa: E402
import arte_ginasios_sinnoh as G     # noqa: E402

ALVO = "MossdeepCity"
KIT_JSON = f"{RAIZ}/dev_scripts/costa_mossdeep_kit.json"

# O bloco de teste DESTA rodada é o único que o varredor de corredores pula: os
# casos dele foram escritos DEPOIS do desenho e a partir dele, então tratá-los
# como corredor a preservar seria circular.
E.BLOCO_PROPRIO = "220_costa_mossdeep.json"

# ------------------------------------------- as constantes do motor, trocadas
M.DESTINO = f"{RAIZ}/data/tilesets/secondary/mossdeep"
M.SECUNDARIO = "gTileset_Mossdeep"
M.PRIMARIO = "gTileset_General"
M.PLANO = f"{RAIZ}/dev_scripts/costa_mossdeep.json"

# Os SETE irmãos, lidos do `layouts.json` (todo layout cujo `secondary_tileset`
# é o `gTileset_Mossdeep`). Nenhum `blockdata_filepath` se repete entre os sete,
# ou seja nenhum deles empresta o `map.bin` de outro, ao contrário do que
# acontece com `PetalburgCity` e os quatro layouts de Kalos; e os sete têm
# `map.bin` em disco e `map.json` próprio, conferido arquivo a arquivo.
M.IRMAOS = ["MossdeepCity", "Route124", "Route125", "Route126", "Route127",
            "Route128", "Route129"]

# o `metatiles.bin` do secundário tem 454 metatiles hoje: o kit vai DEPOIS
M.META_LOCAL_0 = 454
M.CARIMBO = 1                       # a grama lisa do PRIMÁRIO
M.CARIMBO2 = 1
M.BASES_MOVEL = [1]
M.SUFIXO_BASE = {1: ""}
M.FAMILIAS = {}                     # o kit desta cidade é escrito aqui embaixo
M.MOVEIS_DIRETOS = []
M.MOVEIS_REMONTADOS = []
M.ESPACO_ENTRE_MOVEIS = 2

PAL_GRAMA = 2                       # a paleta do carimbo
PAL_AREIA = 5                       # a paleta da areia e do metal
TILE_0 = 233                        # primeira vaga de tile livre depois da
                                    # compactação (o maior tile vivo é o 232)

# As NOVE peças dos autotiles que o `gTileset_General` JÁ desenhou sobre a nossa
# grama, na ordem [NO, N, NE, O, C, E, SO, S, SE]. Isto não foi lido de tabela
# antiga: foi APRENDIDO do mapa, varrendo as células destes metatiles nos sete
# irmãos e em mais três rotas e olhando o padrão de vizinhança de cada uma. Cada
# uma das nove aparece com o padrão que o papel dela manda, e com nenhum outro
# como maioria.
AUTO_AREIA = [280, 281, 282, 288, 289, 290, 296, 297, 298]
AUTO_GASTA = [464, 465, 466, 472, 473, 474, 480, 481, 482]


# ------------------------------------------- o tileset COM a arte desta passada
# O `confere` do motor mede a distância entre duas variantes de chão desenhando
# os dois metatiles e comparando pixel a pixel, e para desenhar ele lê o tile do
# `tiles.png` EM DISCO. Os tiles desta passada ainda não estão lá quando o
# auto-teste roda, e sem esta ponte todos eles saem em BRANCO: as variantes
# marcariam distância 0,0 uma da outra e o portão 4 acusaria uma cópia que não
# existe. Aqui o tileset do secundário é carregado uma vez e recebe os tiles
# NOVOS em memória, de modo que o portão mede a arte de verdade.
_TILES_EXTRA = {}
_CACHE_TS = {}


def _tileset(rotulo):
    chave = (rotulo, len(_TILES_EXTRA))
    if chave not in _CACHE_TS:
        import render_maps as RM
        ts = RM.carregar_tileset(rotulo)
        if rotulo == M.SECUNDARIO and _TILES_EXTRA:
            tiles = ts["tiles"]
            while len(tiles) <= max(_TILES_EXTRA):
                tiles.append([[0] * 8 for _ in range(8)])
            for vaga, pixels in _TILES_EXTRA.items():
                tiles[vaga] = [[pixels[y * 8 + x] for x in range(8)]
                               for y in range(8)]
        _CACHE_TS[chave] = ts
    return _CACHE_TS[chave]


M._tileset = _tileset


# ------------------------------------------------------------- a ARTE NOVA
# Máscara de 8x8, um caractere por pixel, em índice de paleta. `x` = NÃO MEXE, e
# só vale nas máscaras de DETALHE, que são desenhadas por cima do tile do
# próprio carimbo; `.` = transparente (índice 0), e só vale na camada de CIMA.
#
# Os índices da PALETA 2 (a da grama) que esta arte usa:
#   1 = verde-limão (180,255,131)   2 = verde (131,197,98)
#   3 = verde-escuro (57,139,49)    4 = verde quase preto (57,82,0)
#   5 = salmão (222,148,115)        6 = marrom acinzentado (106,90,90)
#   8 = marrom escuro (65,57,49)    9 = areia clara (255,197,148)
#   a = vermelho (222,106,98)       b = carmim (205,65,82)
#   c = menta clara (164,213,197)   d = menta (115,197,164), o corpo da grama
#   e = verde-mar (65,180,131)      f = verde-mar escuro (24,164,106)
#
# Os índices da PALETA 5 (a da areia e do metal):
#   1 = branco (255,255,255)        2 = quase branco (222,230,238)
#   3 = azul claro (189,205,230)    4 = azul acinzentado (156,180,222)
#   5 = cinza (131,131,139)         6 = cinza escuro (98,98,123)
#   7 = ardósia (65,74,106)         8 = azul-noite (41,49,90)
#   9 = azul (115,189,246)          a = azul médio (98,172,238)
#   b = creme (238,230,164)         c = areia (222,205,131), o corpo da areia
#   d = tan (213,180,106)           e = tan escuro (205,156,82)

# ------------------------------------------------- 1. os DETALHES sobre a GRAMA
# `quad` diz qual dos quatro tiles do carimbo serve de base (0 = noroeste,
# 1 = nordeste, 2 = sudoeste, 3 = sudeste); o carimbo é [tile 2, tile 3, tile 3,
# tile 2], então o quadrante 0 e o 1 já dão os dois tiles distintos.
DETALHES = {
    # TOUCEIRA DE CAPIM DA PRAIA: lâminas finas subindo, do escuro para o claro.
    # É a peça mais forte do jogo de detalhes porque é a única que muda a
    # SILHUETA da célula em vez de só a cor.
    "capim": [
        "xxxxxxxx",
        "xxx3xx3x",
        "xx3x3x3x",
        "xx3x2x2x",
        "x3x2x2x3",
        "x2x22x2x",
        "x2232322",
        "xx222x2x"],
    # CONCHA DE LEQUE, deitada na grama, com a dobradiça embaixo e as costelas
    # abrindo para cima. Contorno escuro para ela não sumir dentro do verde: a
    # primeira versão sem contorno media 6,4 contra a grama lisa e o portão 4
    # cortava, com razão.
    "concha": [
        "xxxxxxxx",
        "xx8888xx",
        "x895598x",
        "x859559x",
        "x895595x",
        "xx85598x",
        "xxx898xx",
        "xxxx8xxx"],
    # SEIXOS, três pedrinhas de tamanhos diferentes, cada uma com um pixel de
    # luz em cima. Três e não um campo denso: campo denso lê como tela de
    # mosquiteiro, que é o defeito que Dewford mediu no tile 356 e Sootopolis
    # no cascalho.
    "seixo": [
        "xxxxxxxx",
        "xx99xxxx",
        "x8669xxx",
        "x8669x99",
        "xx88x866",
        "xxxxx866",
        "xx99xx88",
        "xx66xxxx"],
    # RESPINGO DE AREIA que o vento trouxe da praia, grão esparso em dois tons.
    # Ele entra em DOIS quadrantes opostos e não nos quatro, e o motivo é
    # medido: nos quatro, com espelho, os grãos se alinham em coluna e o
    # metatile lê como TELA DE MOSQUITEIRO, que é exatamente o defeito que esta
    # onda já pagou duas vezes.
    "respingo": [
        "xx9xxxxx",
        "xxxxx5x9",
        "x9xxx9xx",
        "xxx5xxx9",
        "x9xxx9xx",
        "xxx9x5xx",
        "x5xxxxx9",
        "xxx9xx5x"],
    # FLORZINHA DO MAR, duas flores de quatro pétalas. Ela é DETALHE de chão, e
    # não móvel: a cidade já tem 48 células do metatile 4, que é a flor sólida
    # do primário, e a quadragésima nona seria repetição.
    "flor": [
        "xxxxxxxx",
        "xxbxxxxx",
        "xbabxx3x",
        "xxbxx3b3",
        "xx3xxxbx",
        "xx3xxx3x",
        "x33xxxxx",
        "xxxxxxxx"],
    # TAMPA DE INSPEÇÃO do centro espacial: um quarto de chapa redonda no canto
    # INTERNO do quadrante. Os quatro quadrantes com os QUATRO espelhos fecham a
    # chapa inteira no meio da célula, que é o mesmo mecanismo do bueiro de
    # Rustboro. É o único detalhe do vocabulário TÉCNICO que cabe num chão de
    # grama sem virar remendo, e ele existe porque o pátio de lajota morreu na
    # geometria (ver o cabeçalho).
    "tampa": [
        "xxxxxxxx",
        "xxxxxxxx",
        "xxxxxx88",
        "xxxxx866",
        "xxxx8669",
        "xxx86699",
        "xxx86996",
        "xx869969"],
}

# Como cada detalhe se espalha pelos QUATRO quadrantes do metatile: cada entrada
# é (usa, espelho), com `usa=None` querendo dizer "deixa o tile do carimbo nesse
# quadrante" e o espelho em 0..3 (bit 1 = horizontal, bit 2 = vertical). Só a
# TAMPA entra nos quatro, porque ela precisa fechar um círculo; os outros cinco
# entram em dois, e o motivo é medido dos dois lados: com UM quadrante a
# distância de pixel contra o carimbo fica abaixo do piso de 8,0 do
# `varia_carimbo.py` e o portão 4 do `confere` corta a peça, e com QUATRO o
# espelho alinha o desenho em coluna e ele vira padrão.
#
# O TILE DE BASE de cada quadrante é o tile do carimbo DAQUELE quadrante, e não
# um só para os quatro. O carimbo da grama é [tile 2, tile 3, tile 3, tile 2],
# ou seja os quadrantes 0 e 3 têm uma base e os 1 e 2 têm outra; desenhar os
# quatro por cima da mesma base deixaria os pixels `x` com a textura do
# quadrante errado. O gerador cria UM tile por (máscara, base) que aparecer de
# verdade, e por isso a `tampa` custa dois tiles e a `concha`, um.
ESPALHA_DETALHE = {
    "capim":    [(1, 0), (None, 0), (None, 0), (1, 1)],
    "concha":   [(None, 0), (1, 0), (1, 3), (None, 0)],
    "seixo":    [(1, 0), (None, 0), (None, 0), (1, 1)],
    "respingo": [(1, 0), (None, 0), (None, 0), (1, 3)],
    "flor":     [(1, 0), (None, 0), (None, 0), (1, 3)],
    "tampa":    [(1, 0), (1, 1), (1, 2), (1, 3)],
}

# ---------------------------------------------- 2. os MIOLOS NOVOS da AREIA
# Desenhados SOBRE o tile de areia do quadrante, pelo mesmo mecanismo do
# detalhe. O carimbo da areia é [264, 280, 280, 264]: o 264 é chapado e o 280
# tem grão, então aqui também a base é POR QUADRANTE.
AREIA_DETALHE = {
    # CONCHAS na areia, o desenho de maré baixa
    "areia_concha": [
        "xxxxxxxx",
        "xxxeexxx",
        "xxe11exx",
        "xe1221ex",
        "xe2112ex",
        "xe1212ex",
        "xe1111ex",
        "xxeeeeex"],
    # SEIXOS lavados pela maré
    "areia_seixo": [
        "xxxxxxxx",
        "xxeexxxx",
        "xe55exxx",
        "xe552xee",
        "xxeexe55",
        "xxxxxe52",
        "xxeexxee",
        "xxe5exxx"],
    # MARESIA: a faixa de areia MOLHADA que a maré deixa quando desce, mais
    # escura embaixo e com a borda de cima recortada. Ela repinta o quadrante
    # INTEIRO, sem um pixel `x`, e isso é de propósito: faixa de maré é uma
    # mudança de tom do chão, não um objeto pousado nele. A primeira versão era
    # uma ondulação em losango espelhada nos quatro quadrantes e no render ela
    # fechava uma CORRENTE de elos amarelos, tela de mosquiteiro de novo.
    "areia_maresia": [
        "cccccccc",
        "ccbcccdc",
        "cccccccc",
        "cddccddc",
        "ddcddccd",
        "dedddede",
        "eddeedde",
        "deedeeed"],
}

# Como cada miolo novo da areia se espalha pelos quatro quadrantes. A maresia
# entra nos DOIS de baixo, com espelho ZERO nos dois, para a faixa correr
# inteira de uma borda à outra da célula em vez de fechar um V.
ESPALHA_AREIA = {
    "areia_concha":  [(1, 0), (None, 0), (None, 0), (1, 3)],
    "areia_seixo":   [(None, 0), (1, 0), (1, 3), (None, 0)],
    "areia_maresia": [(None, 0), (None, 0), (1, 0), (1, 0)],
}

# ------------------------------------------------------ 3. a MOBÍLIA DESENHADA
# Máscaras da camada de CIMA, onde `.` é transparente e deixa a grama aparecer.
# Nenhuma peça é feita de quatro tiles: todas saem de um ou dois tiles pelos
# bits de espelho, que são de graça.
MOVEIS_ARTE = {
    # TAMBOR de combustível, deitado em pé. Dois tiles: a tampa e o corpo, cada
    # um espelhado na horizontal para fechar a peça inteira.
    "tambor_topo": ["........",
                    "........",
                    ".....666",
                    "....6555",
                    "...65222",
                    "...65211",
                    "...65222",
                    "...65666"],
    "tambor_base": ["....6555",
                    "....65ee",
                    "....65ee",
                    "....6555",
                    "....65ee",
                    "....65ee",
                    "....6555",
                    ".....666"],
    # CAIXA DE EQUIPAMENTO: caixote de tábua com cantoneira de metal e travessa
    # em losango. Um tile só, espelhado nos quatro quadrantes, e é o espelho que
    # fecha a cantoneira nos quatro lados e cruza a travessa no meio. As DUAS
    # primeiras versões foram reprovadas no render pelo mesmo motivo: com o
    # corpo pintado no quase branco da paleta 5 (o índice 2) e as barras no
    # laranja, a peça lia como JANELA DE VIDRO deitada no gramado, não como
    # caixote. O corpo passou para o tan (índice d), que é cor de tábua, e aí a
    # silhueta lê na primeira olhada.
    "caixa": ["........",
              ".6666666",
              ".65ddddd",
              ".65dddd6",
              ".65ddd66",
              ".65dd6dd",
              ".65d6ddd",
              ".6566666"],
    # ANTENA PEQUENA: a parabólica em cima e o tripé embaixo. Dois tiles, cada
    # um espelhado na horizontal.
    "antena_topo": ["........",
                    ".66.....",
                    ".6522...",
                    "..65222.",
                    "...65221",
                    "....6522",
                    ".....655",
                    "......66"],
    "antena_base": ["......65",
                    "......65",
                    "......65",
                    "......65",
                    ".....655",
                    "....6555",
                    "...65555",
                    "..655555"],
    # CARRETEL DE CABO, deitado. Um tile espelhado nos quatro quadrantes fecha o
    # disco inteiro com o furo no meio.
    "carretel": ["........",
                 "....6666",
                 "...65552",
                 "..655222",
                 ".6552266",
                 ".6522666",
                 ".6522665",
                 ".6522655"],
    # BOIA DE AMARRAÇÃO, na paleta da GRAMA porque a paleta 5 não tem vermelho
    # nenhum e boia cinzenta não é boia. Um tile espelhado nos quatro
    # quadrantes.
    "boia": ["........",
             "....888.",
             "...8bbb8",
             "..8bbaab",
             ".8bbaacc",
             ".8baaccc",
             ".8bacc99",
             ".8bac999"],
}

# Cada peça: (nome, paleta, [(tile, quadrante, espelho)]).
MOVEIS_DESENHADOS = [
    ("tambor", PAL_AREIA, [("tambor_topo", 0, 0), ("tambor_topo", 1, 1),
                           ("tambor_base", 2, 0), ("tambor_base", 3, 1)]),
    ("caixa de equipamento", PAL_AREIA,
     [("caixa", 0, 0), ("caixa", 1, 1), ("caixa", 2, 2), ("caixa", 3, 3)]),
    ("antena", PAL_AREIA, [("antena_topo", 0, 0), ("antena_topo", 1, 1),
                           ("antena_base", 2, 0), ("antena_base", 3, 1)]),
    ("carretel de cabo", PAL_AREIA,
     [("carretel", 0, 0), ("carretel", 1, 1),
      ("carretel", 2, 2), ("carretel", 3, 3)]),
    ("boia", PAL_GRAMA,
     [("boia", 0, 0), ("boia", 1, 1), ("boia", 2, 2), ("boia", 3, 3)]),
]

# DIRETO: metatile do `gTileset_General` que JÁ é COVERED, JÁ tem comportamento
# zero, JÁ tem a camada de baixo IGUAL à do carimbo e que NENHUMA célula de
# `MossdeepCity` usa hoje (medido no `map.bin`: 110, 111, 224 e 307 aparecem
# ZERO vezes). Custo: zero tile, zero cor, zero metatile.
MOVEIS_DIRETOS = [
    dict(nome="pedra", mt=110),
    dict(nome="pedra virada", mt=111),
    dict(nome="matacao", mt=224),
    dict(nome="mourao", mt=307),
]

# CERCA: corrida horizontal de células sólidas, ponta esquerda, meio e ponta
# direita. As três peças já existem no primário, já são COVERED, já têm a camada
# de baixo do carimbo e a cidade não usa NENHUMA delas.
CERCA = dict(esq=328, meio=329, dir=330)


# --------------------------------------------------------------- a arte crua
def _pinta(linhas, base=None):
    """[64 índices de paleta] a partir da máscara de texto."""
    if len(linhas) != 8:
        raise SystemExit("máscara com %d linhas" % len(linhas))
    fora = []
    for y, linha in enumerate(linhas):
        if len(linha) != 8:
            raise SystemExit("máscara com linha de %d pixels" % len(linha))
        for x, ch in enumerate(linha):
            if ch == "x":
                if base is None:
                    raise SystemExit("'x' só vale em máscara de detalhe")
                fora.append(base[y * 8 + x])
            elif ch == ".":
                fora.append(0)
            else:
                fora.append(int(ch, 16))
    return fora


def _tile_do_tileset(indice):
    """[64 índices] do tile que já está no tileset (primário ou secundário)."""
    import render_maps as RM
    tp, ts = M._tileset(M.PRIMARIO), M._tileset(M.SECUNDARIO)
    grade = RM.resolver_tile(tp, ts, indice)
    return [grade[y][x] for y in range(8) for x in range(8)]


def _bases_usadas(carimbo, espalha):
    """Os tiles de base que a máscara vai PRECISAR, um por quadrante ocupado."""
    return sorted({carimbo[k] for k, (usa, _f) in enumerate(espalha)
                   if usa is not None})


def desenha_tiles():
    """{nome: [64 índices]} de TODO tile novo desta passada, em ordem fixa.

    Detalhe desenhado por cima do chão vira UM TILE POR BASE que ele de fato
    encosta, com o nome `mascara#base`. É isso que faz os pixels `x`, os que a
    máscara deixa passar, saírem com a textura do quadrante CERTO.
    """
    carimbo = [t & 0x3FF for t in M.chao_nosso()[0]]
    car_areia = [e & 0x3FF for e in M._entradas_pri(AUTO_AREIA[4])[:4]]
    tiles = collections.OrderedDict()
    for nome, mascara in DETALHES.items():
        for base in _bases_usadas(carimbo, ESPALHA_DETALHE[nome]):
            tiles["%s#%d" % (nome, base)] = _pinta(mascara,
                                                   _tile_do_tileset(base))
    for nome, mascara in AREIA_DETALHE.items():
        for base in _bases_usadas(car_areia, ESPALHA_AREIA[nome]):
            tiles["%s#%d" % (nome, base)] = _pinta(mascara,
                                                   _tile_do_tileset(base))
    for nome, mascara in MOVEIS_ARTE.items():
        tiles[nome] = _pinta(mascara)
    return tiles


# ---------------------------------------------------- os RETÂNGULOS por ZONA
# O `retangulos` do motor só sabe filtrar por "encosta na água". Mossdeep pede
# outra coisa: a DUNA nova tem que nascer perto da costa ou da areia que já está
# no mapa, senão ela lê como buraco no meio do gramado; e o gramado GASTO é o
# contrário, ele é a grama pisada dos pátios. Este envelope acrescenta duas
# opções de `spec` e delega o resto ao motor, sem tocar no arquivo compartilhado.
_RETANGULOS = M.retangulos
_COSTA = {}


def _costa():
    """As células de água, de areia e de raso do mapa, para o filtro `perto`."""
    if not _COSTA:
        _d, L, W, H, v = G.grade(ALVO)
        beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
        AG = E.agua()
        faixa = set(AUTO_AREIA) | {286, 287, 292, 294, 295, 413, 414, 415, 430}
        _COSTA["cels"] = {(i % W, i // W) for i, c in enumerate(v)
                          if (c & 0x3FF) in faixa or beh(c & 0x3FF) in AG}
    return _COSTA["cels"]


def retangulos(livres, spec, perto=None):
    if spec.get("caixa"):
        x0, y0, x1, y1 = spec["caixa"]
        livres = {p for p in livres if x0 <= p[0] <= x1 and y0 <= p[1] <= y1}
    if spec.get("perto") == "costa":
        perto = _costa()
    return _RETANGULOS(livres, spec, perto)


M.retangulos = retangulos


# ---------------------------------------------------------------------- o KIT
def desenha_kit():
    """(metas, attrs, kit) sem escrever em disco, no formato do motor.

    `kit["tiles"]` é a extensão desta cidade: {nome: (vaga, [64 índices])}. O
    motor não conhece esse campo e não precisa conhecer, porque quem escreve o
    `tiles.png` é o `grava_tileset` daqui.
    """
    base_ent, attr_chao = M.chao_nosso()
    metas, attrs = {}, {}
    proximo = [M.META_LOCAL_0]
    kit = dict(familias={}, moveis=[], cerca=None, cercas=[], tiles={})

    def poe(ents, attr):
        local = proximo[0]
        metas[local] = list(ents)
        attrs[local] = attr
        proximo[0] += 1
        return 512 + local

    # ------------------------------------------------------ 1. os TILES novos
    crus = desenha_tiles()
    vaga = TILE_0
    T = {}
    for nome, pixels in crus.items():
        T[nome] = vaga
        kit["tiles"][nome] = (vaga, pixels)
        _TILES_EXTRA[vaga] = pixels
        vaga += 1
    if vaga > M.TETO_TILES:
        raise SystemExit("o kit estoura o teto de %d tiles do secundário"
                         % M.TETO_TILES)

    def q(nome, pal, flip=0):
        """A entrada de metatile do tile NOVO `nome`, com paleta e espelho."""
        return (pal << 12) | (flip << 10) | (512 + T[nome])

    def cam(quads):
        return list(quads) + [0, 0, 0, 0]

    # ---------------------------------- 2. a GRAMA: os nove arranjos do carimbo
    vivos, cortados = M.arranjos_da_familia(dict(a=2, b=3, pal=PAL_GRAMA))
    por_nome = dict(M.ARRANJOS)
    papel = {"a": 2, "b": 3}
    arranjos = []
    for nome in vivos:
        ents = [(PAL_GRAMA << 12) | (f << 10) | papel[k]
                for (k, f) in por_nome[nome]]
        arranjos.append(dict(nome="grama %s" % nome, mt=poe(cam(ents),
                                                            attr_chao)))
    kit["familias"]["grama"] = dict(fill=M.CARIMBO, auto=None,
                                    variantes=arranjos, cortados=cortados)

    # ------------------------------------------- 3. os DETALHES sobre a grama
    car = [t & 0x3FF for t in base_ent]
    detalhes = []
    for nome in DETALHES:
        quads = []
        for k, (usa, flip) in enumerate(ESPALHA_DETALHE[nome]):
            if usa is None:
                quads.append((PAL_GRAMA << 12) | car[k])
            else:
                quads.append(q("%s#%d" % (nome, car[k]), PAL_GRAMA, flip))
        detalhes.append(dict(nome="detalhe %s" % nome,
                             mt=poe(cam(quads), attr_chao)))
    kit["familias"]["detalhe"] = dict(fill=M.CARIMBO, auto=None,
                                      variantes=detalhes, cortados=[])

    # --------------------------------- 4. a AREIA: borda de graça, miolo novo
    ents_areia = M._entradas_pri(AUTO_AREIA[4])[:4]
    car_areia = [t & 0x3FF for t in ents_areia]
    var_areia = []
    for nome in AREIA_DETALHE:
        quads = []
        for k, (usa, flip) in enumerate(ESPALHA_AREIA[nome]):
            if usa is None:
                quads.append((PAL_AREIA << 12) | car_areia[k])
            else:
                quads.append(q("%s#%d" % (nome, car_areia[k]),
                               PAL_AREIA, flip))
        var_areia.append(dict(nome=nome.replace("_", " "),
                              mt=poe(cam(quads), attr_chao)))
    kit["familias"]["areia"] = dict(fill=AUTO_AREIA[4], auto=list(AUTO_AREIA),
                                    variantes=var_areia, cortados=[])

    # ------------------------ 5. a GRAMA GASTA: borda E miolo de graça, e os
    #                             nove arranjos dela, que também são de graça
    ents_gasta = M._entradas_pri(AUTO_GASTA[4])[:4]
    vivos_g, cort_g = M.arranjos_da_familia(dict(a=ents_gasta[0] & 0x3FF,
                                                 b=ents_gasta[1] & 0x3FF,
                                                 pal=(ents_gasta[0] >> 12) & 0xF))
    papel_g = {"a": ents_gasta[0] & 0x3FF, "b": ents_gasta[1] & 0x3FF}
    pal_g = (ents_gasta[0] >> 12) & 0xF
    var_gasta = []
    for nome in vivos_g:
        ents = [(pal_g << 12) | (f << 10) | papel_g[k]
                for (k, f) in por_nome[nome]]
        var_gasta.append(dict(nome="gasta %s" % nome,
                              mt=poe(cam(ents), attr_chao)))
    kit["familias"]["gasta"] = dict(fill=AUTO_GASTA[4], auto=list(AUTO_GASTA),
                                    variantes=var_gasta, cortados=cort_g)

    # ------------------------------------------------------------ 6. MÓVEIS
    for m in MOVEIS_DIRETOS:
        kit["moveis"].append(dict(nome=m["nome"], mt=m["mt"], remontado=False,
                                  base=M.CARIMBO))
    for nome, pal, pecas in MOVEIS_DESENHADOS:
        cima = [0, 0, 0, 0]
        for tile, quad, flip in pecas:
            cima[quad] = q(tile, pal, flip)
        kit["moveis"].append(dict(nome=nome, remontado=True, de=None,
                                  base=M.CARIMBO,
                                  mt=poe(list(base_ent) + cima, 0x1000)))

    kit["cercas"] = [dict(CERCA, sobre=M.CARIMBO)]
    kit["cerca"] = kit["cercas"][0]

    if proximo[0] > M.TETO_META:
        raise SystemExit("o kit estoura o teto de %d metatiles" % M.TETO_META)

    # A vaga de metatile só serve se ainda NÃO EXISTIR no arquivo (o kit CRESCE
    # o `metatiles.bin`, em vez de sobrescrever vaga usada).
    disco = M._ler("metatiles.bin")
    usados = set()
    for nome in M.IRMAOS:
        usados |= {c & 0x3FF for c in G.grade(nome)[4]}
    for local, ents in metas.items():
        gid = 512 + local
        if gid in usados and local >= len(disco) // 16:
            raise SystemExit("o mapa usa o metatile %d e ele nem existe" % gid)
        if local < len(disco) // 16:
            antigo = list(struct.unpack_from("<8H", disco, local * 16))
            if antigo != ents and not (len(set(antigo)) == 1 and antigo[0] <= 2):
                raise SystemExit("a vaga de metatile %d já está ocupada" % gid)
    return metas, attrs, kit


M.desenha_kit = desenha_kit


# ------------------------------------------------------------ escrita em disco
def grava_tiles(kit):
    """Escreve os tiles NOVOS no `tiles.png`, sem tocar em nenhum tile vivo.

    O png é indexado (modo P) com 16 tiles de 8x8 por linha. Ele CRESCE em
    linhas inteiras, porque o formato exige linha cheia, e as vagas que sobram
    na última linha ficam no índice 0.

    A conferência mais forte está aqui: nenhuma vaga ABAIXO de `TILE_0` é
    tocada. Não há pino de animação neste tileset para proteger (o
    `pinos_anim.py` diz que o `InitTilesetAnim_Mossdeep` não escreve vaga
    nenhuma em tempo de execução), e isso é conferido no `--demo`.
    """
    from PIL import Image
    caminho = f"{M.DESTINO}/tiles.png"
    im = Image.open(caminho)
    if im.mode != "P":
        raise SystemExit("o tiles.png não está indexado")
    larg, alt = im.size
    if larg != 128:
        raise SystemExit("o tiles.png não tem 128 px de largura")
    antes = list(im.get_flattened_data())
    paleta = im.getpalette()
    maior = max(v for v, _p in kit["tiles"].values())
    linhas = (maior // 16) + 1
    nova_alt = max(alt, linhas * 8)
    px = list(antes) + [0] * (larg * (nova_alt - alt))
    for _nome, (vaga, pixels) in kit["tiles"].items():
        if vaga < TILE_0:
            raise SystemExit("tile novo na vaga %d, abaixo de %d"
                             % (vaga, TILE_0))
        tx, ty = (vaga % 16) * 8, (vaga // 16) * 8
        for y in range(8):
            for x in range(8):
                px[(ty + y) * larg + tx + x] = pixels[y * 8 + x]
    guarda = TILE_0 // 16 * 8 * larg
    if px[:guarda] != antes[:guarda]:
        raise SystemExit("a escrita mexeu em tile vivo")
    fora = Image.new("P", (larg, nova_alt))
    fora.putpalette(paleta)
    fora.putdata(px)
    fora.save(caminho)


def grava_tileset(metas, attrs, kit):
    M.grava_tileset(metas, attrs)
    grava_tiles(kit)


def grava_kit(kit):
    """O kit em JSON, para a mensagem de commit e para o `--desfazer` humano."""
    saida = dict(
        alvo=ALVO, primario=M.PRIMARIO, secundario=M.SECUNDARIO,
        carimbo=M.CARIMBO, paleta_grama=PAL_GRAMA, paleta_areia=PAL_AREIA,
        tile_0=TILE_0,
        tiles={n: v for n, (v, _p) in kit["tiles"].items()},
        familias={nome: dict(fill=f["fill"], auto=f["auto"],
                             variantes=[dict(nome=c["nome"], mt=c["mt"])
                                        for c in f["variantes"]],
                             cortados=f["cortados"])
                  for nome, f in kit["familias"].items()},
        moveis=[dict(nome=m["nome"], mt=m["mt"], de=m.get("de"),
                     remontado=m.get("remontado", False))
                for m in kit["moveis"]],
        cerca=kit["cerca"])
    with open(KIT_JSON, "w") as f:
        json.dump(saida, f, indent=1, ensure_ascii=False)


# ------------------------------------------------------------------ MOSSDEEP
CIDADE = dict(
    # SEM TRILHA: a cidade já tem a rede de areia do Emerald ligando as portas
    # (214 células dos nove metatiles do autotile de areia). Uma segunda rede
    # seria duas ruas paralelas dizendo a mesma coisa, como em Petalburg e em
    # Lavaridge.
    trilha=None,
    remendos=[
        # as DUNAS. Elas só nascem a Chebyshev 3 de água, de raso ou da areia
        # que já está no mapa: sem esse filtro o gerador planta areia no meio do
        # gramado do centro espacial, que lê como buraco. O tamanho é 3x3 e 4x3
        # e não mais, e isso não é escolha: o mapa inteiro só tem ONZE cantos de
        # retângulo 3x3 de grama e TRÊS de 4x3.
        dict(familia="areia", quantos=4, larg=(3, 4), alt=(3, 3), espaco=2,
             semente=0x4D01, perto="costa", raio=3),
        # os PÁTIOS DE GRAMA PISADA, que é o que sobra de gramado em volta de
        # prédio muito usado. Vêm depois da duna de propósito: a duna tem filtro
        # e o pátio não, então deixar o pátio primeiro comeria os cantos que só
        # a duna sabe usar.
        dict(familia="gasta", quantos=4, larg=(3, 3), alt=(3, 3), espaco=2,
             semente=0x4D02),
    ],
    # As regiões vêm ANTES da mobília, e aqui isso não é preferência: a grama de
    # Mossdeep é fita estreita entre prédio, penhasco e caminho, com onze cantos
    # de 3x3 no mapa inteiro. Mobília posta antes comeria quase todos, que é o
    # mesmo motivo de Petalburg e de Oldale.
    regioes_antes=True,
    # DUAS passadas de ruído, as duas em cima do carimbo. A primeira espalha os
    # ARRANJOS e deixa cerca de um décimo das células como carimbo puro; a
    # segunda pega essas sobras e põe os DETALHES nelas. É assim que a concha e
    # o cabo ficam ESPARSOS em vez de virarem um sétimo da cidade cada um, que é
    # o que uma lista única de quinze variantes daria.
    ruido=[(1, "grama"), (1, "detalhe")],
    moveis={"tambor": (5, 6), "caixa de equipamento": (5, 6), "antena": (4, 8),
            "carretel de cabo": (4, 7), "boia": (3, 8), "pedra": (4, 6),
            "pedra virada": (4, 6), "matacao": (3, 7), "mourao": (4, 6)},
    cercas=3, cerca_comp=(3, 4), cerca_espaco=10,
    # o piso existe para pegar REGRESSÃO, e um piso muito abaixo do que a
    # passada entrega não pega nada. Ele é medido depois da rodada, não antes.
    min_regiao=45,
)

# Fração mínima dos 256 pixels da célula que um móvel tem que trocar. Ela vale
# porque móvel SOLIDIFICA a célula: peça que muda dez pixels vira parede
# invisível, e parede invisível é o pior defeito que uma passada de enfeite pode
# deixar, porque nenhum portão de colisão a acusa (a colisão está certa; o que
# está errado é o jogador não ver por que não passa).
PISO_COBERTURA = 0.20


# ------------------------------------------------------------- a RÉGUA DE COR
def _px_de_metatile(ents):
    """Os 256 pixels RGB de um metatile de OITO entradas, as duas camadas."""
    import render_maps as RM
    from PIL import Image
    tp, ts = _tileset(M.PRIMARIO), _tileset(M.SECUNDARIO)
    im = Image.new("RGB", (16, 16), (0, 0, 0))
    p = im.load()
    for cam in (0, 1):
        for q in range(4):
            val = ents[cam * 4 + q]
            idx, ip = val & 0x3FF, (val >> 12) & 0xF
            if not idx and cam == 1:
                continue
            tile = RM.resolver_tile(tp, ts, idx)
            if tile is None:
                continue
            cores = (tp if ip < 6 else ts)["paletas"].get(ip)
            if cores is None:
                continue
            RM.desenhar_tile(p, (q % 2) * 8, (q // 2) * 8, tile,
                             [tuple(c) for c in cores],
                             bool(val & 0x400), bool(val & 0x800))
    return list(im.get_flattened_data())


def roda(aplicar):
    metas, attrs, kit = desenha_kit()
    print("kit: %d metatiles novos (locais %d a %d, ids %d a %d de %d) e "
          "%d tiles novos (vagas %d a %d de %d), 0 cor"
          % (len(metas), min(metas), max(metas), 512 + min(metas),
             512 + max(metas), M.TETO_META, len(kit["tiles"]), TILE_0,
             max(v for v, _p in kit["tiles"].values()), M.TETO_TILES))
    for nome_fam, fam in kit["familias"].items():
        print("  %-9s %d variantes, %d cortadas pela régua de cor%s"
              % (nome_fam, len(fam["variantes"]), len(fam["cortados"]),
                 (" (pior " + ", ".join("%s %.1f" % c for c in fam["cortados"])
                  + ")") if fam["cortados"] else ""))
    if aplicar:
        grava_tileset(metas, attrs, kit)
        grava_kit(kit)
    guardado = M.carrega_plano()
    L, W, H, v, escritas, contas, _reg = M.plano_mapa(
        ALVO, CIDADE, kit, M.base_de(ALVO, guardado))
    a, na, ida = M.regua(v, W, H, L)
    b, nb, idb = M.regua(v, W, H, L, escritas)
    print("%s: %d elegíveis, %d regiões, %d solidificadas, %d células mudadas"
          % (ALVO, contas["elegiveis"], contas["regioes"], contas["solidos"],
             len(escritas)))
    print("  chão:  " + ", ".join("%s x%d" % kv
                                  for kv in sorted(contas["chao"].items())))
    print("  ruído: " + ", ".join("%s x%d" % kv
                                  for kv in sorted(contas["ruido"].items())))
    print("  móvel: " + ", ".join("%s x%d" % kv
                                  for kv in sorted(contas["moveis"].items()))
          + ", cerca x%d" % contas["cercas"])
    print("  régua: carimbo %d com %.1f%% de %d células ANTES; carimbo %d com "
          "%.1f%% de %d DEPOIS" % (ida, a, na, idb, b, nb))
    if aplicar:
        saida = list(v)
        for i, val in escritas.items():
            saida[i] = val
        with open(f"{RAIZ}/{L['blockdata_filepath']}", "wb") as f:
            f.write(struct.pack("<%dH" % len(saida), *saida))
        guardado[ALVO] = {"celulas": [[i, v[i], escritas[i]]
                                      for i in sorted(escritas)]}
        with open(M.PLANO, "w") as f:
            json.dump(guardado, f, indent=1)
        print("aplicado")
    return 0


# ------------------------------------------------------------------ auto-teste
def demo():
    """Prova positiva e as provas NEGATIVAS.

    O `mato_littleroot.demo` não serve aqui sem tradução: as sabotagens dele
    citam o primeiro móvel remontado do primário e a família "gasta" como se ela
    fosse a segunda base de móvel, e nenhuma das duas coisas vale neste kit. As
    sabotagens abaixo são as mesmas NOVE do motor, traduzidas para o vocabulário
    desta cidade, mais SEIS que só Mossdeep tem: a ausência de pino de animação,
    a vaga de tile, a paleta, a ÁGUA, a esparsidade do detalhe e a parede
    invisível.
    """
    metas, attrs, kit = desenha_kit()
    guardado = M.carrega_plano()
    plano = M.plano_mapa(ALVO, CIDADE, kit, M.base_de(ALVO, guardado))
    mau = M.confere(ALVO, CIDADE, metas, attrs, kit, plano)
    negativas = []

    def copia():
        return (dict(metas), dict(attrs), json.loads(json.dumps(kit)),
                (plano[0], plano[1], plano[2], list(plano[3]), dict(plano[4]),
                 plano[5], json.loads(json.dumps(plano[6]))))

    def sabota(nome, funcao, espera):
        args = funcao()
        queixas = M.confere(ALVO, CIDADE, *args)
        pega = [q for q in queixas if espera in q]
        if not pega:
            mau.append("SABOTAGEM NÃO ACUSADA (%s): %s" % (nome, queixas[:2]))
        else:
            negativas.append((nome, pega[0]))

    # N1. colisão 1 -> 0 numa célula de chão
    def n1():
        a = copia()
        _L, W, _H, v, esc, _ct, _rg = a[3]
        i = sorted(esc)[0]
        v[i] = v[i] | (1 << 10)
        return a
    sabota("colisão 1 -> 0", n1, "colisão 1 -> 0")

    # N2. elevação alterada
    def n2():
        a = copia()
        _L, W, _H, v, esc, _ct, _rg = a[3]
        i = sorted(esc)[0]
        esc[i] = (esc[i] & 0x0FFF) | (((v[i] >> 12) + 1) & 0xF) << 12
        return a
    sabota("elevação alterada", n2, "mudou ELEVAÇÃO")

    # N3. comportamento de um metatile de CHÃO sabotado
    def n3():
        a = copia()
        mt_id = kit["familias"]["areia"]["variantes"][0]["mt"]
        a[1][mt_id - 512] = (a[1][mt_id - 512] & 0xFF00) | 0x02
        return a
    sabota("behavior de chão sabotado", n3, "tem atributo")

    # N4. layerType NORMAL onde devia ser COVERED
    def n4():
        a = copia()
        mt_id = [m["mt"] for m in kit["moveis"] if m["remontado"]][0]
        a[1][mt_id - 512] = a[1][mt_id - 512] & 0x0FFF
        return a
    sabota("layerType NORMAL no móvel", n4, "não está em COVERED")

    # N5. camada de BAIXO de um móvel sabotada
    def n5():
        a = copia()
        mt_id = [m["mt"] for m in kit["moveis"] if m["remontado"]][0]
        ent = list(a[0][mt_id - 512])
        ent[0] = ent[4]
        a[0][mt_id - 512] = ent
        return a
    sabota("camada de baixo sabotada", n5,
           "não tem o nosso chão na camada de baixo")

    # N6. BORDA de autotile trocada pelo miolo: é a costura que nenhum outro
    #     portão pega, porque colisão, elevação, atributo e alcance ficam certos.
    def n6():
        a = copia()
        _L, W, _H, _v, esc, _ct, rg = a[3]
        for r in rg:
            fam = kit["familias"][r["familia"]]
            cels = {tuple(p) for p in r["celulas"]}
            for p in sorted(cels):
                _mt, lc = M.peca_autotile(fam["auto"], cels, p[0], p[1])
                if lc != (1, 1):
                    esc[p[1] * W + p[0]] = ((esc[p[1] * W + p[0]] & 0xFC00)
                                            | fam["fill"])
                    return a
        raise SystemExit("não achei borda de autotile para a sabotagem N6")
    sabota("borda virou miolo", n6, "o autotile manda")

    # N7. ruído escolhido por (x + y) % n, que é xadrez com período
    def n7():
        original = M._mistura
        M.__dict__["_mistura"] = (lambda *n: (n[0] + n[1]) if len(n) > 1
                                  else n[0])
        try:
            p2 = M.plano_mapa(ALVO, CIDADE, kit, M.base_de(ALVO, guardado))
        finally:
            M.__dict__["_mistura"] = original
        return (dict(metas), dict(attrs), json.loads(json.dumps(kit)), p2)
    sabota("ruído por (x+y)", n7, "virou padrão")

    # N8. variante de chão que é CÓPIA de outra: é enganar a régua sem mudar a
    #     tela, e o portão 4 é quem pega.
    def n8():
        a = copia()
        fam = a[2]["familias"]["detalhe"]
        mt_id = fam["variantes"][0]["mt"]
        a[0][mt_id - 512] = list(M.chao_nosso()[0]) + [0, 0, 0, 0]
        return a
    sabota("variante de chão é cópia", n8, "abaixo do piso")

    # N9. chão novo com arte na CAMADA DE CIMA, que em layerType NORMAL desenha
    #     ACIMA do jogador (o defeito E3)
    def n9():
        a = copia()
        mt_id = a[2]["familias"]["detalhe"]["variantes"][0]["mt"]
        ent = list(a[0][mt_id - 512])
        ent[4] = ent[0]
        a[0][mt_id - 512] = ent
        return a
    sabota("chão com camada de cima", n9, "usa a camada de cima")

    # --------------------------------------------- as SEIS que só Mossdeep tem
    import pinos_anim as PA
    from PIL import Image

    # N10. PINOS DE ANIMAÇÃO. Este tileset NÃO TEM NENHUM, e "não tem" precisa
    #      ser MEDIDO e não suposto: se um dia alguém ligar animação no
    #      `gTileset_Mossdeep`, esta conta acusa, porque ela cobra a ausência.
    vagas, ativa, _expl = PA.pinos_de_anim(M.SECUNDARIO)
    if ativa or vagas:
        mau.append("o gTileset_Mossdeep passou a ter animação em %d vagas (%s) "
                   "e o kit escreve a partir da vaga %d sem saber disso"
                   % (len(vagas), PA.faixas(vagas), TILE_0))
    negativas.append(("pino de animação",
                      "o pinos_anim.py mede ZERO vaga pinada neste tileset"))

    # N11. VAGA DE TILE: nenhum tile novo cai em vaga que algum metatile ANTIGO
    #      do tileset já pede. A conta olha só os metatiles ABAIXO de
    #      `META_LOCAL_0`, e a razão é que depois de um `--aplicar` os metatiles
    #      DESTE kit já estão no disco e pedem, com razão, os tiles deste kit:
    #      contá-los faria o portão acusar a própria passada.
    disco = M._ler("metatiles.bin")
    pedidos = set()
    for i in range(min(M.META_LOCAL_0, len(disco) // 16)):
        for j in range(8):
            w = struct.unpack_from("<H", disco, i * 16 + j * 2)[0]
            if (w & 0x3FF) >= 512:
                pedidos.add((w & 0x3FF) - 512)
    if pedidos and max(pedidos) >= TILE_0:
        mau.append("o tileset já pede o tile local %d, e o kit começa em %d"
                   % (max(pedidos), TILE_0))
    negativas.append(("vaga de tile",
                      "o maior tile pedido é o %d e o kit começa no %d"
                      % (max(pedidos), TILE_0)))

    # N12. PALETA: toda a arte nova usa SÓ índices que a paleta 2 ou a 5 do
    #      PRIMÁRIO já têm, e nenhum arquivo de `palettes/` do secundário muda.
    tp = _tileset(M.PRIMARIO)
    usados_por_pal = collections.defaultdict(set)
    for _n, (_v, px) in kit["tiles"].items():
        pass
    for nome_fam, fam in kit["familias"].items():
        for c in [dict(mt=fam["fill"])] + fam["variantes"]:
            if c["mt"] < 512 or (c["mt"] - 512) not in metas:
                continue
            for e in metas[c["mt"] - 512]:
                if (e & 0x3FF) >= 512:
                    usados_por_pal[(e >> 12) & 0xF].add((e & 0x3FF) - 512)
    for m in kit["moveis"]:
        if m["mt"] < 512 or (m["mt"] - 512) not in metas:
            continue
        for e in metas[m["mt"] - 512]:
            if (e & 0x3FF) >= 512:
                usados_por_pal[(e >> 12) & 0xF].add((e & 0x3FF) - 512)
    fora = []
    vaga_para_px = {v: p for _n, (v, p) in kit["tiles"].items()}
    for ip, vagas_t in sorted(usados_por_pal.items()):
        if ip >= 6:
            fora.append("a arte nova pediu a paleta %d do SECUNDÁRIO" % ip)
            continue
        n_cores = len(tp["paletas"][ip])
        for vt in vagas_t:
            if max(vaga_para_px[vt]) >= n_cores:
                fora.append("o tile %d usa índice acima de %d na paleta %d"
                            % (vt, n_cores - 1, ip))
    if fora:
        mau += fora
    negativas.append(("paleta", "a arte nova usa só as paletas %s do primário"
                      % sorted(usados_por_pal)))

    # N13. A ÁGUA. Nenhuma célula de água muda, e a prova é a de Sootopolis: o
    #      CARIMBO DE COMPORTAMENTO da grade inteira, byte a byte, tem que sair
    #      igual. Isso cobre o alcance de Surf por construção, porque quem
    #      decide se o Surf entra numa célula é o comportamento dela.
    _L, W, H, v, esc, _ct, _rg = plano
    saida = list(v)
    for i, val in esc.items():
        saida[i] = val
    beh = G.comportamento(_L["primary_tileset"], _L["secondary_tileset"])
    asec_novo = dict(attrs)

    def beh_de(mt_id):
        if mt_id >= 512 and (mt_id - 512) in asec_novo:
            return asec_novo[mt_id - 512] & 0xFF
        return beh(mt_id)

    car_antes = bytes(beh(c & 0x3FF) for c in v)
    car_depois = bytes(beh_de(c & 0x3FF) for c in saida)
    if car_antes != car_depois:
        n = sum(1 for a, b in zip(car_antes, car_depois) if a != b)
        mau.append("o carimbo de comportamento mudou em %d células: o alcance "
                   "de Surf não está mais provado" % n)
    AG = E.agua()
    molhadas = {i for i, c in enumerate(v)
                if beh(c & 0x3FF) in AG or beh(c & 0x3FF) == 0x17}
    tocadas = molhadas & set(esc)
    if tocadas:
        mau.append("a passada escreveu em %d células de água ou de raso: %s"
                   % (len(tocadas), sorted(tocadas)[:4]))
    negativas.append(("água", "o carimbo de comportamento das %d células sai "
                              "byte a byte igual e nenhuma das %d células de "
                              "água ou raso foi escrita"
                      % (len(v), len(molhadas))))

    # N14. O DETALHE é ESPARSO. Ele não pode passar de um vinte avos das células
    #      andáveis, senão vira chão e não detalhe.
    ids_det = {c["mt"] for c in kit["familias"]["detalhe"]["variantes"]}
    n_det = sum(1 for val in esc.values() if (val & 0x3FF) in ids_det)
    n_and = sum(1 for val in v if not ((val >> 10) & 3))
    if n_det > n_and / 20.0:
        mau.append("o detalhe pegou %d de %d células andáveis, mais de um "
                   "vinte avos: virou chão" % (n_det, n_and))
    negativas.append(("detalhe esparso", "%d células de detalhe em %d andáveis"
                      % (n_det, n_and)))

    # N15. PAREDE INVISÍVEL: todo móvel troca pelo menos `PISO_COBERTURA` dos
    #      256 pixels da célula. Móvel solidifica a célula, e peça que quase não
    #      se vê deixa o jogador batendo num quadrado vazio. Nenhum portão de
    #      colisão acusa isso, porque a colisão está certa.
    def ents_de(mt_id):
        if mt_id >= 512 and (mt_id - 512) in metas:
            return list(metas[mt_id - 512])
        return M._entradas_qq(mt_id)

    base_px = _px_de_metatile(list(M.chao_nosso()[0]) + [0, 0, 0, 0])
    piores = []
    pecas = [(m["nome"], m["mt"]) for m in kit["moveis"]]
    pecas += [("cerca %s" % k, kit["cerca"][k]) for k in ("esq", "meio", "dir")]
    for nome, mt_id in pecas:
        p = _px_de_metatile(ents_de(mt_id))
        n = sum(1 for i in range(256) if p[i] != base_px[i])
        piores.append((n, nome))
        if n < 256 * PISO_COBERTURA:
            mau.append("o móvel %s troca só %d dos 256 pixels da célula: vira "
                       "parede invisível" % (nome, n))
    piores.sort()
    negativas.append(("parede invisível", "a peça mais fraca é %s, com %d de "
                                          "256 pixels (%.1f%%), acima do piso "
                                          "de %.0f%%"
                      % (piores[0][1], piores[0][0], 100.0 * piores[0][0] / 256,
                         100 * PISO_COBERTURA)))

    # N16. TETO do secundário: 512 tiles e 512 metatiles no layout `emerald`.
    maior_tile = max(v2 for v2, _p in kit["tiles"].values())
    if maior_tile >= M.TETO_TILES or max(metas) >= M.TETO_META:
        mau.append("o kit passa do teto do secundário")
    im = Image.open(f"{M.DESTINO}/tiles.png")
    negativas.append(("teto", "maior tile novo %d de 512, maior metatile novo "
                              "%d de 512, png com %d vagas"
                      % (maior_tile, 512 + max(metas),
                         (im.size[0] // 8) * (im.size[1] // 8))))

    # N17. IDEMPOTÊNCIA: rodar o plano duas vezes dá o mesmo plano.
    p2 = M.plano_mapa(ALVO, CIDADE, kit, M.base_de(ALVO, guardado))
    if p2[4] != plano[4]:
        mau.append("segunda passada deu plano diferente")
    negativas.append(("idempotência", "duas passadas deram o mesmo plano de %d "
                                      "células" % len(plano[4])))

    for nome, texto in negativas:
        print("  prova: %-22s %s" % (nome, texto[:100]))
    if mau:
        print("DEMO VERMELHA, %d queixa(s):" % len(mau))
        for q in mau:
            print("  " + q)
        return 1
    print("DEMO VERDE, %d provas negativas" % len(negativas))
    return 0


def main():
    if "--desfazer" in sys.argv:
        return M.desfaz(ALVO)
    if "--demo" in sys.argv or "--autoteste" in sys.argv:
        return demo()
    if "--so-tileset" in sys.argv:
        metas, attrs, kit = desenha_kit()
        grava_tileset(metas, attrs, kit)
        grava_kit(kit)
        print("tileset escrito: %d metatiles novos, %d tiles novos, 0 cores"
              % (len(metas), len(kit["tiles"])))
        return 0
    return roda("--aplicar" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
