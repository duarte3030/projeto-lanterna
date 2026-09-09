#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Refino de `RustboroCity` (tema PEDRA E ESCOLA), no `gTileset_Rustboro`.

O QUE ESTA CIDADE TEM DE ERRADO, medido pela `dev_scripts/regua_cidades.py`
nesta árvore em 09/09/2026: das 1.162 células andáveis a pé, **534 (46,0%) são o
metatile 699**, o calçamento de treliça diagonal cor de creme do
`gTileset_Rustboro`. Rustboro é a maior cidade desta onda e a mais construída:
tem a Devon Corporation, a escola de treinadores, o ginásio de pedra da Roxanne,
um chafariz, dezessete postes de luz e uma rede de grades brancas. E mesmo assim
o chão dela é um bloco de dezesseis pixels repetido quinhentas e trinta e quatro
vezes, do pátio da Devon até a porta do ginásio.

As 534 células estão TODAS com o atributo `0x0000` (comportamento zero,
`layerType` NORMAL) e TODAS na elevação 3; isso foi medido, não suposto, e é o
que permite tratá-las como um carimbo só.

Os outros chãos da cidade NÃO SÃO MEXIDOS, e cada um por um motivo medido:

  - a RUA clara (os metatiles 761, 768, 770 e 777, 182 células somadas, mais as
    bordas 760, 762, 776 e 778) é um autotile inteiro que o Emerald desenhou
    ligando as portas. Trocar peça dela abriria costura na rua.
  - o CALÇAMENTO NA SOMBRA (o metatile 707, 69 células, o mesmo desenho do 699
    na paleta 11) é a sombra que os prédios projetam na calçada. Ele corre em
    faixas verticais coladas nas paredes, e mexer nele apagaria a sombra.
  - a GRAMA (o metatile 1, 155 células) fica na orla do mapa, debaixo das
    árvores e na beira do rio. Rustboro é cidade cinza e institucional; encher a
    orla dela de moita seria o contrário do que ela é. A grama recebe RUÍDO DE
    ARRANJO e nada mais.
  - a ÁGUA do rio (o metatile 368, 142 células) não é chão andável e a régua já
    a tira da conta; ela nunca entra no catálogo.

O QUE ESTA PASSADA FAZ, na ordem em que paga:

  1. COMPACTA O TILESET, e é o que paga o orçamento. O `gTileset_Rustboro`
     estava em 512 de 512 tiles e 235 deles eram MORTOS: nenhum metatile os
     referenciava. O `compacta_tileset.py` desceu para 452 tiles vivos (464 no
     png, que é o próximo múltiplo de 16) e devolveu 48 vagas até o teto de 512,
     mais as 12 vagas em branco que sobram na última linha do png, ou seja 60
     vagas de tile no total. A prova é de PIXEL: os OITO mapas irmãos foram
     renderizados antes e depois e a diferença é ZERO em 3.306.240 pixels.
     Os PINOS DE ANIMAÇÃO (as vagas 128 a 159 e 448 a 451, 36 vagas que o
     `TilesetAnim_Rustboro` sobrescreve em tempo de execução com a água do canal
     e o chafariz) foram conferidos com o `dev_scripts/pinos_anim.py` ANTES e
     conferidos tile a tile DEPOIS: as 36 continuam byte a byte iguais. O
     `compacta_tileset.py` desta árvore já ajusta o `-num_tiles` do
     `src/data/tilesets/graphics.h` sozinho (commit `52fde0f339`), e ajustou:
     498 para 464.

  2. O CALÇAMENTO GRANDE, que é a arte nova desta passada e o que a torna
     bonita. Rustboro é a cidade da PEDRA: ela tem a pedreira ao norte
     (`Route116`), o ginásio de pedra e a mineradora. O chão dela ganha
     REMENDOS DE LAJE, retângulos de laje grande com junta forte, cercados por
     um MEIO FIO de duas linhas. A laje é desenhada aqui, em máscara de texto,
     e pintada SÓ com índices que a paleta 8 (a do próprio carimbo) já tem:
     ZERO cor nova, e o `git diff` dos dezesseis `.pal` prova.

     Por que remendo de laje e não textura importada: ver a seção da FONTE.
     Por que retângulo com meio fio e não bolha com franja: calçamento
     encostando em calçamento não pede franja de transição, pede FIO. Praça de
     verdade se constrói assim, com uma fiada de meio fio delimitando o
     recorte, e o desenho sai lendo como coisa PROJETADA em vez de mancha. As
     nove peças do autotile saem de TRÊS tiles (fio na horizontal, fio na
     vertical, canto do fio) pelos bits de espelho, que são de graça.

  3. O PARALELEPÍPEDO e a ROSÁCEA, a segunda família de remendo: pedra miúda
     de quatro por quatro pixels, com uma roseta de mosaico no meio de alguns
     recortes. É o desenho de praça cívica, que casa com a escola e com a
     prefeitura de vidro da Devon.

  4. O RUÍDO DE ARRANJO no calçamento que sobra, por espelho e rearranjo dos
     TRÊS tiles do próprio carimbo (o 680, o 679 e o 681 da paleta 8, depois da
     compactação). Custo ZERO de tile e de cor. É a camada SUTIL: ela não é o
     enfeite, é o fundo, e sem ela a treliça diagonal repetiria o mesmo bloco de
     dezesseis pixels quinhentas vezes. O gerador CORTA sozinho o arranjo que
     não passa no piso de 8,0 do `varia_carimbo.py`, e diz na tela quais caíram.

  5. OS DETALHES SOLTOS, na segunda passada de ruído: bueiro, trinca, musgo na
     junta e cascalho da pedreira, cada um desenhado SOBRE o tile do próprio
     carimbo (a máscara só troca os pixels do detalhe), de modo que o detalhe
     casa com a treliça por construção em vez de casar por sorte.

  6. A MOBÍLIA DE BEIRA, em células solidificadas, sempre com comportamento
     ZERADO e `layerType` COVERED, sempre encostada em prédio, grade ou na borda
     do mapa.

O ACHADO QUE PAGOU A MOBÍLIA, e ele é grande: **47 metatiles do
`gTileset_Rustboro` têm EXATAMENTE a mesma camada de baixo do carimbo**, ou
seja, já estão desenhados em cima do nosso calçamento. Vinte e quatro deles são
`layerType` COVERED com comportamento zero, que é a definição de móvel pronto, e
DOIS deles (o 718 e o 719, duas seções da grade de ferro da cidade) não são
usados por NENHUM dos oito mapas irmãos. Custo de pôr essas peças no mapa: ZERO
tile, ZERO cor, ZERO metatile. É o mesmo achado que pagou Snowpoint em
`ace0ac7877`, e aqui ele é maior porque Rustboro é uma cidade rica de tileset.

A FONTE DE ARTE, e as QUATRO REPROVAÇÕES, cada uma com o número na mão. O
índice `/tmp/claude-501/FONTES-POR-TILESET.md` dá QUATRO candidatos para
`secondary/rustboro`, o maior número da onda. Os quatro foram extraídos com o
`extrai_tileset.py`, renderizados com o `render_hack.py`, medidos metatile a
metatile contra os nossos quatro chãos e OLHADOS ampliados. A cor média do nosso
carimbo é (229,9; 230,4; 204,7).

  - `light-platinum 0x286D24` (arte nova 0,966, 8 usos, amostra g00m13 40x46) é
    uma CIDADE NO CÉU, construída sobre passarela de madeira, com nuvem no chão.
    O piso dela, medido no bloco mais uniforme do render, tem cor média
    (166,0; 146,5; 111,0), ou seja **141,1** de distância do nosso calçamento,
    contra o critério de cerca de 50 que Pastoria, Sandgem e Hearthome fixaram.
    Varrendo os 512 metatiles dele com a camada de cima VAZIA, ou seja os que
    poderiam ser chão, **UM ÚNICO** fica abaixo de 50 de algum chão nosso (o
    local 2, a 49,9 do nosso tijolo bege), e ampliado ele é NUVEM. REPROVADO.

  - `golden-glazed 0x3DF734` (0,956, 3 usos, g00m03 40x60) é uma cidade de
    ASFALTO ESCURO, com faixa de pedestre, bueiro e canteiro. É o candidato mais
    próximo do tema, e mesmo assim o asfalto dele tem cor média
    (118,3; 100,9; 105,9): **197,4** do nosso calçamento e **183,7** do nosso
    tijolo cinza. Dos 512 metatiles, DOIS ficam abaixo de 50 (os locais 139 e
    140, a 37,1 e 39,0 do nosso tijolo cinza) e ampliados os dois são CÉU sobre
    telhado. REPROVADO por cor.

  - `mega-emerald-x-y 0x3DF71C` (0,680, 7 usos, g00m00 30x30) é uma vila de
    GRAMA com caminho de areia: não tem uma célula de calçamento de pedra. Os
    metatiles dele mais próximos dos nossos chãos (os locais 145, 186, 210 e
    234, a 10,7 da nossa rua clara) são a PRÓPRIA rua clara do Rustboro
    original, arte que já está no repositório. Os 14 que passam no corte contra
    o tijolo bege são COPA DE ÁRVORE vista de cima e um xadrez pontilhado que
    lê como tela de mosquiteiro, o mesmo defeito que Dewford mediu no tile 356 e
    que Sootopolis mediu no cascalho. REPROVADO: não há o que importar.

  - `x-y-emerald 0x3DF764` (0,415, 3 usos, g00m01 40x60) É a Rustboro, redesenhada
    como cidade de GRAMA CHAPADA: o hack APAGOU o calçamento e pôs grama no
    lugar. O metatile dele mais próximo de um chão nosso é o local 195, a 47,8
    de distância de cor e 48,9 de pixel do nosso 699, e ampliado ele é a
    TRELIÇA DE CREME DO PRÓPRIO EMERALD, ou seja o que já temos. Os outros 16
    que passam no corte são parede de tijolo, cachoeira e chafariz. REPROVADO:
    importar seria importar o repositório de volta para dentro dele mesmo.

  Consequência direta: **NADA FOI IMPORTADO, e por isso o `CREDITS.md` NÃO FOI
  TOCADO**. Abrir seção vazia seria mentira de arquivo.

O QUE FICOU DE FORA, com o motivo medido:

  - O QUADRO DE AVISOS (metatile 856), que seria a peça mais temática desta
    cidade, porque Rustboro é a cidade da ESCOLA DE TREINADORES. Medido: a
    camada de cima dele são os tiles 414, 415, 430 e 431 na paleta 3, que é
    EXATAMENTE a camada de cima do metatile 27 do `gTileset_General`, a PLACA.
    Placa sem texto atrás é promessa que o jogo não cumpre, e Littleroot e
    Lavaridge já reprovaram a mesma peça pelo mesmo motivo. Pôr texto atrás dela
    exigiria `bg_event` novo no `map.json`, e o `map.json` fica INTOCADO.

  - Os metatiles 544, 546, 547, 548, 549, 550, 715, 731 e 533, que são chão
    ANDÁVEL do próprio tileset com a camada de baixo do carimbo: os nove têm
    `layerType` NORMAL **e arte na camada de cima**, ou seja o Emerald os desenha
    ACIMA do sprite do jogador. São a escada e o capacho das portas, e ali isso é
    de propósito. Abrir a regra para chão NOVO derrubaria o portão 2 do
    `confere`, que existe justamente para isso (é o defeito E3).

  - Os metatiles 574, 660, 553, 656, 657 e 658, que a régua de cor apontou como
    os mais parecidos com o carimbo (26,1 a 47,2 de distância) e que ampliados
    parecem calçamento de tijolo: medido no `map.bin`, os SEIS são usados
    exclusivamente como célula SÓLIDA, 13, 2, 16, 1, 4 e 1 vez. São PAREDE de
    prédio vista de frente. Deitá-los no chão poria fachada no piso.

  - O metatile 705 (a bacia de pedra) como móvel: a arte dele mora INTEIRA na
    camada de baixo e a de cima é vazia, então remontá-lo sobre o calçamento não
    desenharia nada.

  - Os metatiles 798, 799, 816, 817 e 818 (as balaustradas com grama), que
    seriam a "grade baixa" do tema: a metade de baixo deles mora na CAMADA DE
    BAIXO (os tiles de grama e o tile 399), então a remontagem só traz os postes
    e deixa um toco flutuando. As grades que ENTRAM são as do próprio
    calçamento, o 703, o 717, o 718, o 719, o 725 e o 745, que já vêm com a
    camada de baixo certa.

  - O POSTE DE LUZ (o par 538 embaixo, 530 em cima) como móvel novo: a cidade já
    tem DEZESSETE deles, medido. Poste número dezoito não é enfeite, é
    repetição; e a metade de cima (o 530) é `layerType` NORMAL com arte, ou seja
    a lâmpada desenha acima do jogador de propósito. Copiar essa combinação para
    células novas espalharia pela cidade o padrão que o portão 2 proíbe.

  - O CHAFARIZ (os metatiles 824, 825, 826, 832 e 833): a cidade já tem UM, e
    dois chafarizes a vinte células um do outro leem como erro de mapa.

Uso:
    python3 dev_scripts/pedra_rustboro.py
    python3 dev_scripts/pedra_rustboro.py --aplicar
    python3 dev_scripts/pedra_rustboro.py --desfazer
    python3 dev_scripts/pedra_rustboro.py --demo
    python3 dev_scripts/pedra_rustboro.py --so-tileset
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

ALVO = "RustboroCity"
KIT_JSON = f"{RAIZ}/dev_scripts/pedra_rustboro_kit.json"

# O bloco de teste DESTA rodada é o único que o varredor de corredores pula: os
# casos dele foram escritos DEPOIS do desenho e a partir dele, então tratá-los
# como corredor a preservar seria circular.
E.BLOCO_PROPRIO = "218_pedra_rustboro.json"

# ------------------------------------------- as constantes do motor, trocadas
M.DESTINO = f"{RAIZ}/data/tilesets/secondary/rustboro"
M.SECUNDARIO = "gTileset_Rustboro"
M.PRIMARIO = "gTileset_General"
M.PLANO = f"{RAIZ}/dev_scripts/pedra_rustboro.json"

# Os OITO irmãos com `map.bin` em disco, lidos do `layouts.json`. O nono layout
# que aponta para este par de tilesets, `LAYOUT_PETALBURG_WOODS_OLD`, pede
# `data/layouts/PetalburgWoods_Old/map.bin`, arquivo que NÃO EXISTE em disco:
# ele é um esboço morto, e dizer que são nove irmãos seria contar um mapa que
# não existe. Nenhum `blockdata_filepath` se repete entre os oito, ou seja
# nenhum deles empresta o `map.bin` de outro, ao contrário do que acontece com
# `PetalburgCity` e os quatro layouts de Kalos.
M.IRMAOS = ["RustboroCity", "Route104", "Route116", "PetalburgWoods",
            "Route104_Prototype", "SouthernIsland_Exterior",
            "SouthernIsland_Interior", "FarawayIsland_Entrance"]

# o `metatiles.bin` do secundário tem 350 metatiles hoje: o kit vai DEPOIS
M.META_LOCAL_0 = 350
M.CARIMBO = 699                     # o calçamento de treliça, do SECUNDÁRIO
M.CARIMBO2 = 699
M.BASES_MOVEL = [699]
M.SUFIXO_BASE = {699: ""}
M.FAMILIAS = {}                     # o kit desta cidade é escrito aqui embaixo
M.MOVEIS_DIRETOS = []
M.MOVEIS_REMONTADOS = []
M.ESPACO_ENTRE_MOVEIS = 2

PAL = 8                             # a paleta do carimbo, e a ÚNICA que a arte
                                    # nova usa: zero cor nova, por construção
TILE_0 = 452                        # primeira vaga de tile livre depois da
                                    # compactação (o maior tile vivo é o 451, e
                                    # os pinos de animação param no 451)


# --------------------------------------------------------------- o carimbo
def chao_nosso(mt=None):
    """(as quatro entradas da camada de BAIXO do carimbo, o atributo dele).

    O motor tinha esta função cravada no PRIMÁRIO, porque o carimbo das seis
    cidades anteriores desta onda é a grama do `gTileset_General`. O de Rustboro
    é o metatile 699, do SECUNDÁRIO, e ler o 699 na tabela do primário devolve
    lixo plausível em silêncio. Esta versão lê do lado certo.
    """
    mt = M.CARIMBO if mt is None else mt
    ents = M._entradas_qq(mt)
    if any(v & 0x3FF for v in ents[4:]):
        raise SystemExit("o carimbo %d tem arte na camada de cima" % mt)
    if mt < 512:
        return ents[:4], G._attrs(M.PRIMARIO)[mt]
    return ents[:4], G._attrs(M.SECUNDARIO)[mt - 512]


M.chao_nosso = chao_nosso


# ------------------------------------------- o tileset COM a arte desta passada
# O `confere` do motor mede a distância entre duas variantes de chão desenhando
# os dois metatiles e comparando pixel a pixel, e para desenhar ele lê o tile do
# `tiles.png` EM DISCO. Os tiles desta passada ainda não estão lá quando o
# auto-teste roda, e sem esta ponte todos eles saem em BRANCO: as variantes
# marcariam distância 0,0 uma da outra e o portão 4 acusaria uma cópia que não
# existe. Pior: se o portão fosse afrouxado, ele passaria a não medir nada.
# Aqui o tileset do secundário é carregado uma vez e recebe os tiles NOVOS em
# memória, de modo que o portão mede a arte de verdade.
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
# Máscara de 8x8, um caractere por pixel, em índice da paleta 8. Os índices que
# a paleta 8 tem e que esta arte usa:
#   1 = branco (255,255,255)      2 = creme (238,238,213)
#   3 = oliva (205,205,164)       4 = oliva escuro (189,189,131)
#   5 = cinza (131,131,139)       6 = cinza escuro (98,98,123)
#   9 = azul pálido (205,213,230) d = 13, verde (139,189,139)
#   v = 14, verde oliva (123,164,74)
# `x` = NÃO MEXE, e só vale nas máscaras de DETALHE, que são desenhadas por
# cima do tile do próprio carimbo. É o que faz o detalhe casar com a treliça por
# construção, em vez de casar por sorte.
MASCARAS = {
    # ---------------------------------------------------------- a LAJE grande
    # Um quadrante de laje: junta no topo e na esquerda, realce branco por
    # dentro, corpo creme. Espelhado nos quatro quadrantes, o metatile vira UMA
    # laje de 16x16 com junta em volta, e nada no meio.
    "laje": ["44444444",
             "41111111",
             "41222222",
             "41222232",
             "41222222",
             "41232222",
             "41222222",
             "41222232"],
    # a mesma laje, gasta: pinta de oliva espalhada pelo corpo inteiro
    "laje_gasta": ["44444444",
                   "41111111",
                   "41323232",
                   "41232322",
                   "41323232",
                   "41232322",
                   "41323232",
                   "41232322"],
    # a RACHADURA corta a laje na diagonal. Ela entra em DOIS quadrantes opostos
    # do metatile, e não em um: com um só, a distância de pixel contra a laje
    # lisa fica em torno de 5 e o portão 4 do `confere` corta (com razão, porque
    # abaixo do piso de 8,0 do `varia_carimbo.py` a variante não se vê em jogo).
    "laje_racha": ["44444444",
                   "41111141",
                   "41222412",
                   "41224122",
                   "41241222",
                   "41412222",
                   "44122222",
                   "41222222"],
    # MUSGO na junta, do lado sombreado
    "laje_musgo": ["4444444d",
                   "4111ddd1",
                   "412dd222",
                   "41d22232",
                   "d1222222",
                   "d1232222",
                   "dd222222",
                   "4dd22232"],
    # -------------------------------------------------- o PARALELEPÍPEDO miúdo
    # Quatro pedras de 4x4 por tile, dezesseis por metatile.
    "paralelo": ["44444444",
                 "41112111",
                 "41222122",
                 "41222122",
                 "44444444",
                 "41112111",
                 "41222122",
                 "41222122"],
    "paralelo2": ["44444444",
                  "41113111",
                  "41232122",
                  "41223122",
                  "44444444",
                  "41132111",
                  "41223122",
                  "41233122"],
    # ---------------------------------------------------- a ROSÁCEA de mosaico
    # Um quarto de roseta, no canto INTERNO do quadrante. Espelhada nos quatro,
    # ela fecha uma roseta inteira no meio do metatile.
    # A PRIMEIRA versão desta máscara desenhava a curva na DIAGONAL, uma coluna
    # por linha, e no render ela fechava um LOSANGO achatado que lia como olho,
    # não como roseta. Esta é um quarto de círculo de raio 6 medido a partir do
    # centro do metatile, com anel branco, miolo azul pálido e um quadrado
    # oliva de quatro por quatro no meio, que é o que faz a peça ler como
    # mosaico de praça e não como bueiro.
    "rosacea": ["22222222",
                "22222222",
                "22222244",
                "22224411",
                "22244199",
                "22441999",
                "24119933",
                "24119933"],
    # ------------------------------------------------------------- o MEIO FIO
    # Duas linhas, cinza e branca, na borda de fora do recorte. `mfh` é a borda
    # de cima, `mfv` a da esquerda e `mfc` o canto; os outros seis lados saem
    # dos bits de espelho, que são de graça.
    "mfh": ["55555555",
            "11111111",
            "42222222",
            "41222222",
            "41222232",
            "41222222",
            "41232222",
            "41222222"],
    "mfv": ["54444444",
            "51111111",
            "51222222",
            "51222232",
            "51222222",
            "51232222",
            "51222222",
            "51222232"],
    "mfc": ["55555555",
            "51111111",
            "51222222",
            "51222232",
            "51222222",
            "51232222",
            "51222222",
            "51222232"],
    # ---------------------------------------------------------- o CANTEIRO
    # Caixa de pedra com terra e verde. Espelhada nos quatro quadrantes, fecha
    # uma caixa inteira. O índice 0 é TRANSPARENTE na camada de cima, e é por
    # isso que o calçamento aparece em volta da caixa.
    "canteiro": ["00000000",
                 "05555555",
                 "05111111",
                 "05144444",
                 "05144vv4",
                 "0514vvvd",
                 "0514vddd",
                 "0514vddd"],
    # ------------------------------------------------------ o MONTE DE PEDRA
    # Rustboro é a cidade da pedreira (`Route116`, ao norte), e o tileset dela
    # não tem uma pilha de blocos cortados em lugar nenhum: conferido no atlas
    # dos 350 metatiles do secundário e nos 512 do primário. A peça que existia
    # e quase serviu, o par 827 e 828, é uma rocha CORTADA AO MEIO (cada metade
    # tem borda reta de um lado), e o motor põe móvel um por célula, então cada
    # metade cairia sozinha e leria como pedra partida. Esta é desenhada: um
    # bloco em cima e dois embaixo, dois tiles espelhados na horizontal. O
    # índice 0 é TRANSPARENTE na camada de cima, e é por isso que o calçamento
    # aparece em volta da pilha.
    "monte_topo": ["00000000",
                   "00000000",
                   "00000555",
                   "00005111",
                   "00005122",
                   "00005122",
                   "00005555",
                   "00000000"],
    "monte_base": ["05555555",
                   "51111115",
                   "51222225",
                   "51222225",
                   "51222225",
                   "55555555",
                   "00000000",
                   "00000000"],
}

# ------------------------------------------------------ os DETALHES SOLTOS
# Desenhados SOBRE o tile do carimbo indicado por `quad` (0 = noroeste,
# 1 = nordeste, 2 = sudoeste, 3 = sudeste). `x` deixa o pixel do carimbo.
DETALHES = {
    # BUEIRO: um quarto de tampa redonda, no canto INTERNO do quadrante. Os
    # quatro quadrantes espelhados fecham a tampa inteira no meio da célula.
    "bueiro": dict(quad=0, base=0, mascara=[
        "xxxxxxxx",
        "xxxxxxxx",
        "xxxxxxxx",
        "xxxxx655",
        "xxxx6511",
        "xxx65199",
        "xxx65991",
        "xx651991"]),
    # TRINCA: uma rachadura que atravessa a célula inteira, em dois quadrantes.
    # Ela é desenhada no CINZA (índice 5) e não no oliva (4): a treliça do
    # carimbo já é feita de oliva, e no render a primeira versão sumia dentro
    # do próprio padrão. O cinza é a única cor da paleta 8 que contrasta com o
    # creme E com o oliva ao mesmo tempo.
    "trinca": dict(quad=0, base=0, mascara=[
        "xxxxxxxx",
        "xxxxxxx5",
        "xxxxxx5x",
        "xxxxx5xx",
        "xxxx55xx",
        "xxx5xxxx",
        "xx5xxxxx",
        "x55xxxxx"]),
    # MUSGO que cresceu na junta, num canto da célula
    "musgo": dict(quad=0, base=0, mascara=[
        "xxxxxxxx",
        "xxxxxddx",
        "xxxxdddd",
        "xxxddddd",
        "xxxxdddd",
        "xxxxxddd",
        "xxxxxxdx",
        "xxxxxxxx"]),
    # CASCALHO da pedreira, lasca esparsa. Doze lascas de dois a quatro pixels,
    # e não um campo denso de pares: campo denso lê como tela de mosquiteiro,
    # que é o defeito que Dewford mediu no tile 356 e Sootopolis no cascalho.
    "cascalho": dict(quad=0, base=0, mascara=[
        "xxxxxxxx",
        "xx44xxxx",
        "xxxxxx5x",
        "x5xxxxxx",
        "xxxx44xx",
        "xx4xxxxx",
        "x55xxxxx",
        "xxxxx44x"]),
}

# Como cada detalhe se espalha pelos QUATRO quadrantes do metatile: cada
# entrada é (usa, espelho), com `usa=None` querendo dizer "deixa o tile do
# carimbo nesse quadrante" e o espelho em 0..3 (bit 1 = horizontal, bit 2 =
# vertical). O bueiro entra nos quatro com os QUATRO espelhos, e é isso que
# fecha a tampa redonda no meio da célula: a primeira versão desta tabela
# repetia os espelhos 0, 0, 1, 1 e no render saíam QUATRO ganchos soltos em vez
# de uma tampa. Os outros três entram em dois quadrantes, e o motivo é medido:
# com UM quadrante só, a distância de pixel contra o carimbo fica abaixo do
# piso de 8,0 do `varia_carimbo.py` e o portão 4 do `confere` corta a peça.
ESPALHA_DETALHE = {
    "bueiro":   [(1, 0), (1, 1), (1, 2), (1, 3)],
    "trinca":   [(1, 0), (None, 0), (1, 2), (None, 0)],
    "musgo":    [(1, 0), (None, 0), (None, 0), (1, 3)],
    "cascalho": [(1, 0), (1, 1), (None, 0), (1, 3)],
}

# Os arranjos do carimbo. O carimbo é [A, B, C, B] (os tiles 680, 679 e 681 na
# paleta 8, depois da compactação), e NÃO um par [a,b,b,a] como o das seis
# cidades anteriores: por isso o motor não sabe montá-lo e a lista vem escrita
# aqui. Cada entrada é (papel, espelho), com espelho 0..3 (bit 1 = horizontal,
# bit 2 = vertical). O primeiro é o ARRANJO DO CARIMBO e não vira metatile: ele
# está aqui só para a régua de cor poder comparar contra ele.
ARRANJOS = [
    ("carimbo",   [("A", 0), ("B", 0), ("C", 0), ("B", 0)]),
    ("espelhoH",  [("A", 1), ("B", 1), ("C", 1), ("B", 1)]),
    ("espelhoV",  [("A", 2), ("B", 2), ("C", 2), ("B", 2)]),
    ("espelhoHV", [("A", 3), ("B", 3), ("C", 3), ("B", 3)]),
    ("trocaAC",   [("C", 0), ("B", 0), ("A", 0), ("B", 0)]),
    ("giro",      [("B", 0), ("A", 0), ("B", 0), ("C", 0)]),
    ("misto1",    [("A", 0), ("C", 1), ("B", 2), ("A", 3)]),
    ("misto2",    [("C", 3), ("B", 2), ("A", 1), ("C", 0)]),
    ("misto3",    [("B", 1), ("A", 0), ("C", 3), ("B", 2)]),
    ("misto4",    [("C", 2), ("A", 3), ("B", 0), ("C", 1)]),
    ("misto5",    [("A", 2), ("C", 0), ("B", 1), ("A", 0)]),
    ("misto6",    [("B", 3), ("C", 2), ("A", 0), ("B", 1)]),
]

# ------------------------------------------------------------------ MÓVEIS
# DIRETO: metatile que JÁ existe no `gTileset_Rustboro`, JÁ é COVERED com
# comportamento zero e JÁ tem a camada de baixo IGUAL à do carimbo.
#
# ESTA LISTA ESTÁ VAZIA, e a razão é uma medida feita NO RENDER, não na
# planilha. O achado que abriu a lista continua valendo e está escrito no
# cabeçalho: 47 metatiles do `gTileset_Rustboro` têm exatamente a camada de
# baixo do carimbo e 24 deles são COVERED com comportamento zero, ou seja
# móveis prontos de custo ZERO. Só que os seis que serviriam pelo tema (o 703,
# o 717, o 718, o 719, o 725 e o 745) são SEÇÕES DA GRADE DE FERRO, arte
# desenhada para correr em LINHA: o corrimão atravessa a célula de ponta a
# ponta. Uma seção sozinha no meio do pátio foi renderizada e lida como
# CERCA QUEBRADA, um pedaço de grade flutuando. O motor põe móvel solto um por
# célula, com Chebyshev 2 entre dois quaisquer, então não há como pedir a ele
# uma corrida de grade. O que corre em linha nesta passada é o BANCO, pela via
# do `cerca`, que existe justamente para isso.
MOVEIS_DIRETOS = []

# BANCO: corrida horizontal de células sólidas, ponta esquerda, meio e ponta
# direita. As três peças já existem no tileset, já são COVERED e já têm a
# camada de baixo do carimbo; o mapa usa cada uma UMA vez, no banco que já está
# lá em frente à escola.
BANCO = dict(esq=728, meio=729, dir=730)

# REMONTADO: a camada de CIMA da peça, posta sobre a camada de baixo do
# carimbo, com `layerType` COVERED e comportamento ZERADO. Sem a remontagem a
# peça viria com o chão do doador embaixo (grama, no caso das quatro do
# primário; a grama da `Route104`, no caso do arbusto) e deixaria um quadrado
# verde no meio do calçamento.
MOVEIS_REMONTADOS = [
    dict(nome="moita",        de=704, lado="sec"),
    dict(nome="arbusto",      de=775, lado="sec"),
    dict(nome="matacao",      de=224, lado="pri"),
    dict(nome="pedra",        de=110, lado="pri"),
    dict(nome="pedra virada", de=111, lado="pri"),
    dict(nome="mourao",       de=307, lado="pri"),
]


# --------------------------------------------------------------- a arte crua
def _pinta(linhas, base=None):
    """[64 índices de paleta] a partir da máscara de texto."""
    fora = []
    for y, linha in enumerate(linhas):
        if len(linha) != 8:
            raise SystemExit("máscara com linha de %d pixels" % len(linha))
        for x, ch in enumerate(linha):
            if ch == "x":
                if base is None:
                    raise SystemExit("'x' só vale em máscara de detalhe")
                fora.append(base[y * 8 + x])
            elif ch == "d":
                fora.append(13)
            elif ch == "v":
                fora.append(14)
            else:
                fora.append(int(ch, 16))
    if len(linhas) != 8:
        raise SystemExit("máscara com %d linhas" % len(linhas))
    return fora


def _tile_do_tileset(indice):
    """[64 índices] do tile que já está no tileset (primário ou secundário)."""
    import render_maps as RM
    tp, ts = M._tileset(M.PRIMARIO), M._tileset(M.SECUNDARIO)
    grade = RM.resolver_tile(tp, ts, indice)
    return [grade[y][x] for y in range(8) for x in range(8)]


def desenha_tiles():
    """{nome: [64 índices]} de TODO tile novo desta passada, em ordem fixa."""
    carimbo = [t & 0x3FF for t in chao_nosso()[0]]
    tiles = collections.OrderedDict()
    for nome in ("laje", "laje_gasta", "laje_racha", "laje_musgo",
                 "paralelo", "paralelo2", "rosacea",
                 "mfh", "mfv", "mfc", "canteiro",
                 "monte_topo", "monte_base"):
        tiles[nome] = _pinta(MASCARAS[nome])
    for nome, d in DETALHES.items():
        base = _tile_do_tileset(carimbo[d["quad"]])
        tiles[nome] = _pinta(d["mascara"], base)
    return tiles


# ------------------------------------------------------------- a RÉGUA DE COR
def _px_de_quads(quads):
    """Os 256 pixels RGB de um metatile montado só com a camada de baixo.

    `quads` é [(pixels_do_tile, espelho)] x4, com o tile já em lista de 64
    índices de paleta. A paleta é sempre a 8, a do carimbo.
    """
    cores = [tuple(c) for c in M._tileset(M.SECUNDARIO)["paletas"][PAL]]
    fora = [(0, 0, 0)] * 256
    for q, (tile, flip) in enumerate(quads):
        ox, oy = (q % 2) * 8, (q // 2) * 8
        for y in range(8):
            for x in range(8):
                sx = 7 - x if flip & 1 else x
                sy = 7 - y if flip & 2 else y
                fora[(oy + y) * 16 + ox + x] = cores[tile[sy * 8 + sx]]
    return fora


def _dist(a, b):
    return sum(sum((x - y) ** 2 for x, y in zip(p, q)) ** 0.5
               for p, q in zip(a, b)) / 256.0


def _px_de_metatile(ents):
    """Os 256 pixels RGB de um metatile de OITO entradas, as duas camadas.

    Diferente do `_px_de_quads`, que só monta a camada de baixo: aqui a camada
    de cima entra por cima, com o índice 0 valendo transparência, que é o que o
    `src/field_camera.c` faz.
    """
    import render_maps as RM
    tp, ts = _tileset(M.PRIMARIO), _tileset(M.SECUNDARIO)
    from PIL import Image
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


def arranjos_vivos():
    """(sobreviventes, cortados) dos arranjos do carimbo, pela régua de cor.

    O corte não é escolhido a dedo: é o piso de 8,0 do `varia_carimbo.py`, o
    mesmo das seis cidades anteriores. A treliça diagonal do calçamento TEM
    pinta, e por isso os espelhos dela ficam entre 8,0 e 13,8; num chão chapado
    eles cairiam para 2 ou 3 e o corte levaria todos, que é o que aconteceu com
    a terra e a areia em Littleroot.
    """
    tiles = {"A": None, "B": None, "C": None}
    car = [t & 0x3FF for t in chao_nosso()[0]]
    tiles["A"], tiles["B"], tiles["C"] = (_tile_do_tileset(car[0]),
                                          _tile_do_tileset(car[1]),
                                          _tile_do_tileset(car[2]))
    pix = {nome: _px_de_quads([(tiles[k], f) for (k, f) in quads])
           for nome, quads in ARRANJOS}
    fica, corta = [ARRANJOS[0][0]], []
    for nome, _q in ARRANJOS[1:]:
        pior = min(_dist(pix[nome], pix[o]) for o in fica)
        if pior < M.PISO_DISTANCIA:
            corta.append((nome, pior))
        else:
            fica.append(nome)
    return fica[1:], corta


# ---------------------------------------------------------------------- o KIT
def desenha_kit():
    """(metas, attrs, kit) sem escrever em disco, no formato do motor.

    `kit["tiles"]` é a extensão desta cidade: {nome: (vaga, [64 índices])}. O
    motor não conhece esse campo e não precisa conhecer, porque quem escreve o
    `tiles.png` é o `grava_tileset` daqui.
    """
    base_ent, attr_chao = chao_nosso()
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
    if vaga > 512:
        raise SystemExit("o kit estoura o teto de 512 tiles do secundário")

    def q(nome, flip=0):
        """A entrada de metatile do tile NOVO `nome`, com espelho."""
        return (PAL << 12) | (flip << 10) | (512 + T[nome])

    def cam(quads):
        return list(quads) + [0, 0, 0, 0]

    # -------------------------------------------------- 2. o MEIO FIO, as oito
    # peças de borda, feitas de TRÊS tiles pelos bits de espelho. Elas são
    # COMPARTILHADAS pelas duas famílias de remendo: o que muda de uma para a
    # outra é o MIOLO, não a borda, e é assim que uma praça de verdade é feita.
    L = lambda f=0: q("laje", f)          # noqa: E731
    H, V, C = (lambda f=0: q("mfh", f), lambda f=0: q("mfv", f),
               lambda f=0: q("mfc", f))
    borda = {
        "NO": cam([C(0), H(1), V(0), L(1)]),
        "N":  cam([H(0), H(1), L(0), L(1)]),
        "NE": cam([H(0), C(1), L(0), V(1)]),
        "O":  cam([V(0), L(1), V(2), L(3)]),
        "E":  cam([L(0), V(1), L(2), V(3)]),
        "SO": cam([V(0), L(1), C(2), H(3)]),
        "S":  cam([L(0), L(1), H(2), H(3)]),
        "SE": cam([L(0), V(1), H(2), C(3)]),
    }
    ids_borda = {papel: poe(ents, attr_chao) for papel, ents in borda.items()}

    # ------------------------------------------------ 3. as DUAS famílias de
    #                                                    remendo, com o miolo
    def familia(nome, miolo, variantes):
        fill = poe(cam(miolo), attr_chao)
        auto = [ids_borda["NO"], ids_borda["N"], ids_borda["NE"],
                ids_borda["O"], fill, ids_borda["E"],
                ids_borda["SO"], ids_borda["S"], ids_borda["SE"]]
        lista = []
        for nome_var, quads in variantes:
            lista.append(dict(nome="%s %s" % (nome, nome_var),
                              mt=poe(cam(quads), attr_chao)))
        kit["familias"][nome] = dict(fill=fill, auto=auto, variantes=lista,
                                     cortados=[])
        return fill

    familia("laje",
            [L(0), L(1), L(2), L(3)],
            [("gasta", [q("laje_gasta", 0), q("laje_gasta", 1),
                        q("laje_gasta", 2), q("laje_gasta", 3)]),
             ("rachada", [q("laje_racha", 0), L(1), L(2), q("laje_racha", 3)]),
             ("com musgo", [q("laje_musgo", 0), L(1),
                            q("laje_musgo", 2), L(3)])])
    familia("paralelo",
            [q("paralelo", 0), q("paralelo", 1),
             q("paralelo", 2), q("paralelo", 3)],
            [("gasto", [q("paralelo2", 0), q("paralelo2", 1),
                        q("paralelo2", 2), q("paralelo2", 3)]),
             ("rosacea", [q("rosacea", 0), q("rosacea", 1),
                          q("rosacea", 2), q("rosacea", 3)])])

    # ------------------------------- 4. o CALÇAMENTO: arranjos e detalhes
    car = [t & 0x3FF for t in base_ent]
    papel = {"A": car[0], "B": car[1], "C": car[2]}
    vivos, cortados = arranjos_vivos()
    por_nome = dict(ARRANJOS)
    arranjos = []
    for nome in vivos:
        ents = [(PAL << 12) | (f << 10) | papel[k] for (k, f) in por_nome[nome]]
        arranjos.append(dict(nome="calcamento %s" % nome,
                             mt=poe(cam(ents), attr_chao)))
    kit["familias"]["calcamento"] = dict(fill=M.CARIMBO, auto=None,
                                         variantes=arranjos, cortados=cortados)

    detalhes = []
    for nome in DETALHES:
        quads = []
        for k, (usa, flip) in enumerate(ESPALHA_DETALHE[nome]):
            if usa is None:
                quads.append((PAL << 12) | car[k])
            else:
                quads.append(q(nome, flip))
        detalhes.append(dict(nome="detalhe %s" % nome,
                             mt=poe(cam(quads), attr_chao)))
    kit["familias"]["detalhe"] = dict(fill=M.CARIMBO, auto=None,
                                      variantes=detalhes, cortados=[])

    # ------------------------------------------------------------ 5. MÓVEIS
    for m in MOVEIS_DIRETOS:
        kit["moveis"].append(dict(nome=m["nome"], mt=m["mt"], remontado=False,
                                  base=M.CARIMBO))
    vistos = {}
    for m in MOVEIS_REMONTADOS:
        cima = tuple(M._entradas_qq(m["de"])[4:])
        if not any(e & 0x3FF for e in cima):
            raise SystemExit("o metatile %d não tem arte na camada de cima"
                             % m["de"])
        if cima in vistos:
            raise SystemExit("a camada de cima de %d é IDÊNTICA à de %d"
                             % (m["de"], vistos[cima]))
        vistos[cima] = m["de"]
        kit["moveis"].append(dict(nome=m["nome"], remontado=True, de=m["de"],
                                  base=M.CARIMBO,
                                  mt=poe(list(base_ent) + list(cima), 0x1000)))
    # as DUAS peças de mobília DESENHADAS nesta passada
    kit["moveis"].append(dict(
        nome="canteiro", remontado=True, de=None, base=M.CARIMBO,
        mt=poe(list(base_ent) + [q("canteiro", 0), q("canteiro", 1),
                                 q("canteiro", 2), q("canteiro", 3)], 0x1000)))
    kit["moveis"].append(dict(
        nome="monte de pedra", remontado=True, de=None, base=M.CARIMBO,
        mt=poe(list(base_ent) + [q("monte_topo", 0), q("monte_topo", 1),
                                 q("monte_base", 0), q("monte_base", 1)],
               0x1000)))

    kit["cercas"] = [dict(BANCO, sobre=M.CARIMBO)]
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


KIT_DO_MOTOR = M.desenha_kit
M.desenha_kit = desenha_kit


# ------------------------------------------------------------ escrita em disco
def grava_tiles(kit):
    """Escreve os tiles NOVOS no `tiles.png`, sem tocar em nenhum tile vivo.

    O png é indexado (modo P) com 16 tiles de 8x8 por linha. Ele CRESCE em
    linhas inteiras, porque o formato exige linha cheia, e as vagas que sobram
    na última linha ficam no índice 0.

    A conferência mais forte está aqui: nenhuma vaga ABAIXO de `TILE_0` é
    tocada, e as vagas de 128 a 159 e de 448 a 451 (os pinos que o
    `TilesetAnim_Rustboro` sobrescreve em tempo de execução) estão todas abaixo
    de `TILE_0` por construção, porque `TILE_0` é 452.
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
            raise SystemExit("tile novo na vaga %d, abaixo de %d" % (vaga, TILE_0))
        tx, ty = (vaga % 16) * 8, (vaga // 16) * 8
        for y in range(8):
            for x in range(8):
                px[(ty + y) * larg + tx + x] = pixels[y * 8 + x]
    if px[:larg * alt][:TILE_0 // 16 * 8 * larg] != antes[:TILE_0 // 16 * 8 * larg]:
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
        carimbo=M.CARIMBO, paleta=PAL, tile_0=TILE_0,
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


# ------------------------------------------------------------------ RUSTBORO
CIDADE = dict(
    # SEM TRILHA: a cidade já tem a rede de rua clara do Emerald ligando as
    # portas (182 células andáveis dos metatiles 761, 768, 770 e 777). Uma
    # segunda rede seria duas ruas dizendo a mesma coisa, como em Petalburg e
    # em Lavaridge.
    trilha=None,
    remendos=[
        # os PÁTIOS DE LAJE. Rustboro tem os maiores vãos de calçamento da onda,
        # e por isso cabe retângulo grande aqui e não em Lavaridge.
        dict(familia="laje", quantos=9, larg=(5, 7), alt=(4, 5), espaco=2,
             semente=0x2B05),
        # as PRAÇAS DE PARALELEPÍPEDO, menores, com a rosácea no miolo
        dict(familia="paralelo", quantos=7, larg=(4, 5), alt=(3, 4), espaco=2,
             semente=0x2B06),
        # os RECORTES MIÚDOS, que entram nas sobras. Eles vêm por último de
        # propósito: o `retangulos` só aceita retângulo inteiro dentro do que
        # ainda é carimbo, e uma lista de tamanho único deixaria de fora todo
        # vão de três por três que sobra entre os pátios grandes.
        dict(familia="laje", quantos=6, larg=(3, 4), alt=(3, 3), espaco=2,
             semente=0x2B07),
        dict(familia="paralelo", quantos=5, larg=(3, 3), alt=(3, 3), espaco=2,
             semente=0x2B08),
    ],
    # As regiões vêm ANTES da mobília. A razão é a mesma de Petalburg: móvel
    # posto no carimbo tira uma célula do numerador E do denominador da régua,
    # e móvel posto em cima de mancha tira só do denominador, o que PIORA a
    # conta; mas móvel posto antes come os cantos de retângulo. Aqui o chão é
    # largo e as duas ordens dariam certo, e esta foi escolhida porque os
    # pátios são a peça principal do desenho e a mobília é o acabamento.
    regioes_antes=True,
    # DUAS passadas de ruído, as duas em cima do carimbo. A primeira espalha os
    # ARRANJOS e deixa cerca de um sétimo das células como carimbo puro; a
    # segunda pega essas sobras e põe os DETALHES nelas. É assim que o bueiro e
    # a trinca ficam ESPARSOS em vez de virarem um sétimo da cidade cada um,
    # que é o que uma lista única de dez variantes daria.
    ruido=[(699, "calcamento"), (699, "detalhe")],
    moveis={"moita": (4, 5), "arbusto": (4, 5), "canteiro": (6, 5),
            "monte de pedra": (4, 6), "matacao": (3, 6), "pedra": (3, 6),
            "pedra virada": (3, 6), "mourao": (4, 5)},
    cercas=3, cerca_comp=(3, 4), cerca_espaco=10,
    # o piso é 150 porque esta passada fecha em 168 células de recorte visível:
    # ele existe para pegar REGRESSÃO, e um piso muito abaixo do que a passada
    # entrega não pega nada.
    min_regiao=150,
)

# Fração mínima dos 256 pixels da célula que um móvel tem que trocar. Ela vale
# porque móvel SOLIDIFICA a célula: peça que muda dez pixels vira parede
# invisível, e parede invisível é o pior defeito que uma passada de enfeite
# pode deixar, porque nenhum portão de colisão a acusa (a colisão está certa; o
# que está errado é o jogador não ver por que não passa). Medido nesta árvore:
# a peça mais fraca das oito é a pedra, com 56 pixels de 256 (21,9%).
PISO_COBERTURA = 0.20


def roda(aplicar):
    metas, attrs, kit = desenha_kit()
    print("kit: %d metatiles novos (locais %d a %d, ids %d a %d de %d) e "
          "%d tiles novos (vagas %d a %d de 512), 0 cor"
          % (len(metas), min(metas), max(metas), 512 + min(metas),
             512 + max(metas), M.TETO_META, len(kit["tiles"]), TILE_0,
             max(v for v, _p in kit["tiles"].values())))
    for nome_fam, fam in kit["familias"].items():
        print("  %-11s %d variantes, %d cortadas pela régua de cor%s"
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
          + ", banco x%d" % contas["cercas"])
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
    citam a família "grama" pelo nome e o primeiro móvel remontado do primário,
    e nenhuma das duas existe neste kit. As sabotagens abaixo são as mesmas
    NOVE do motor, traduzidas para o vocabulário desta cidade, mais SEIS que só
    Rustboro tem: os pinos de animação, a vaga de tile, a paleta, o meio fio, a
    esparsidade do detalhe e o teto do tileset.
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
        mt_id = kit["familias"]["laje"]["fill"]
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
    sabota("meio fio virou miolo", n6, "o autotile manda")

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
        fam = a[2]["familias"]["laje"]
        mt_id = fam["variantes"][0]["mt"]
        a[0][mt_id - 512] = list(a[0][fam["fill"] - 512])
        return a
    sabota("variante de chão é cópia", n8, "abaixo do piso")

    # N9. chão novo com arte na CAMADA DE CIMA, que em layerType NORMAL desenha
    #     ACIMA do jogador (o defeito E3)
    def n9():
        a = copia()
        mt_id = a[2]["familias"]["laje"]["fill"]
        ent = list(a[0][mt_id - 512])
        ent[4] = ent[0]
        a[0][mt_id - 512] = ent
        return a
    sabota("chão com camada de cima", n9, "usa a camada de cima")

    # --------------------------------------------- as SEIS que só Rustboro tem
    import pinos_anim as PA
    from PIL import Image

    # N10. PINOS DE ANIMAÇÃO: nenhum tile novo cai numa vaga que o
    #      `src/tileset_anims.c` sobrescreve em tempo de execução. Isso não
    #      quebra build nenhum e não muda um pixel de render estático: só
    #      aparece dentro do jogo, e por isso precisa de portão próprio.
    vagas, ativa, _expl = PA.pinos_de_anim(M.SECUNDARIO)
    if not ativa:
        mau.append("o pinos_anim.py diz que o gTileset_Rustboro não tem "
                   "animação, e ele tem")
    if len(vagas) != 36:
        mau.append("os pinos de animação deram %d vagas, e a medida do "
                   "condutor é 36" % len(vagas))
    caiu = {v for v, _p in kit["tiles"].values()} & vagas
    if caiu:
        mau.append("tile novo em vaga de animação: %s" % sorted(caiu))
    negativas.append(("pino de animação", "as %d vagas %s ficam fora do kit"
                      % (len(vagas), PA.faixas(vagas))))

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

    # N12. PALETA: toda a arte nova usa SÓ índices que a paleta 8 já tem, e
    #      nenhum arquivo de `palettes/` muda. Prova negativa: um índice 15 na
    #      máscara seria cor viva, e a conta abaixo o acusaria.
    cores = M._tileset(M.SECUNDARIO)["paletas"][PAL]
    fora_da_paleta = set()
    for _n, (_v, pixels) in kit["tiles"].items():
        fora_da_paleta |= {p for p in pixels if p >= len(cores)}
    if fora_da_paleta:
        mau.append("a arte nova usa índice de cor %s, que a paleta %d não tem"
                   % (sorted(fora_da_paleta), PAL))
    usados_idx = sorted({p for _n, (_v, px) in kit["tiles"].items() for p in px})
    negativas.append(("paleta", "a arte nova usa os índices %s da paleta %d, e "
                                "nenhum outro" % (usados_idx, PAL)))

    # N13. O MEIO FIO é MESMO oito peças distintas: se duas fossem iguais, o
    #      recorte sairia com fio faltando de um lado e nada acusaria.
    ids = [kit["familias"]["laje"]["auto"][k] for k in (0, 1, 2, 3, 5, 6, 7, 8)]
    if len(set(ids)) != 8:
        mau.append("o meio fio tem %d peças distintas, e precisa de 8"
                   % len(set(ids)))
    ents = {i: tuple(metas[i - 512]) for i in ids}
    if len(set(ents.values())) != 8:
        mau.append("duas peças de meio fio têm as MESMAS entradas de tile")
    negativas.append(("meio fio", "as 8 peças de borda são distintas entre si"))

    # N14. O DETALHE é ESPARSO. Ele não pode passar de um vinte avos das
    #      células andáveis, senão vira chão e não detalhe.
    _L, W, _H, v, esc, contas, _rg = plano
    ids_det = {c["mt"] for c in kit["familias"]["detalhe"]["variantes"]}
    n_det = sum(1 for val in esc.values() if (val & 0x3FF) in ids_det)
    n_and = sum(1 for val in v if not ((val >> 10) & 3))
    if n_det > n_and / 20.0:
        mau.append("o detalhe pegou %d de %d células andáveis, mais de um "
                   "vinte avos: virou chão" % (n_det, n_and))
    negativas.append(("detalhe esparso", "%d células de detalhe em %d andáveis"
                      % (n_det, n_and)))

    # N15. O TETO do secundário: 512 tiles e 512 metatiles no layout `emerald`.
    maior_tile = max(v2 for v2, _p in kit["tiles"].values())
    if maior_tile >= 512 or max(metas) >= 512:
        mau.append("o kit passa do teto do secundário")
    im = Image.open(f"{M.DESTINO}/tiles.png")
    negativas.append(("teto", "maior tile novo %d de 512, maior metatile novo "
                              "%d de 512, png com %d vagas"
                      % (maior_tile, 512 + max(metas),
                         (im.size[0] // 8) * (im.size[1] // 8))))

    # N17. PAREDE INVISÍVEL: todo móvel troca pelo menos `PISO_COBERTURA` dos
    #      256 pixels da célula. Móvel solidifica a célula, e peça que quase
    #      não se vê deixa o jogador batendo num quadrado vazio. Nenhum portão
    #      de colisão acusa isso, porque a colisão está certa.
    px_kit = {}
    for m in kit["moveis"]:
        ent = metas.get(m["mt"] - 512)
        px_kit[m["nome"]] = _px_de_metatile(ent) if ent else None
    base_px = _px_de_metatile(list(chao_nosso()[0]) + [0, 0, 0, 0])
    piores = []
    for m in kit["moveis"]:
        p = px_kit[m["nome"]]
        if p is None:
            mau.append("o móvel %s não é do kit e não dá para medir" % m["nome"])
            continue
        n = sum(1 for i in range(256) if p[i] != base_px[i])
        piores.append((n, m["nome"]))
        if n < 256 * PISO_COBERTURA:
            mau.append("o móvel %s troca só %d dos 256 pixels da célula: "
                       "vira parede invisível" % (m["nome"], n))
    piores.sort()
    negativas.append(("parede invisível", "a peça mais fraca é %s, com %d de "
                                          "256 pixels (%.1f%%), acima do piso "
                                          "de %.0f%%"
                      % (piores[0][1], piores[0][0],
                         100.0 * piores[0][0] / 256, 100 * PISO_COBERTURA)))

    # N16. IDEMPOTÊNCIA: rodar o plano duas vezes dá o mesmo plano.
    p2 = M.plano_mapa(ALVO, CIDADE, kit, M.base_de(ALVO, guardado))
    if p2[4] != plano[4]:
        mau.append("segunda passada deu plano diferente")
    negativas.append(("idempotência", "duas passadas deram o mesmo plano de %d "
                                      "células" % len(plano[4])))

    for nome, texto in negativas:
        print("  prova: %-22s %s" % (nome, texto[:96]))
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
