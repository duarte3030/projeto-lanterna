#!/usr/bin/env python3
"""B12.b: reescreve o `blockdata` dos 291 mapas de Unova com comportamento honesto.

Uso:
    python3 dev_scripts/blockdata_unova.py --demo            # autoteste, nao grava
    python3 dev_scripts/blockdata_unova.py --medir           # mede o que esta na ROM hoje
    python3 dev_scripts/blockdata_unova.py --conferir        # simula os 291, nao grava
    python3 dev_scripts/blockdata_unova.py --mapa Unova_AspertiaCity [--gravar]
    python3 dev_scripts/blockdata_unova.py --arte-propria castelia [--gravar]
    python3 dev_scripts/blockdata_unova.py --arte-propria --gravar   # todos os convertidos
    python3 dev_scripts/blockdata_unova.py --gravar          # grava os 291

O QUE ESTE SCRIPT FAZ, E O QUE ELE NAO FAZ

Faz: reler cada `.ablk` do BW3G e emitir um `data/layouts/Unova_*/map.bin` novo
(mais o `border.bin`) usando os tilesets EMPRESTADOS que cada layout ja declara.
Nao faz: tileset proprio (isso e o B12.a), nem mexer em dimensao de layout, warp,
object_event, bg_event, indice de mapa, `map_groups.json` ou `layouts.json`.

POR QUE A CONVERSAO ORIGINAL FICOU POBRE, MEDIDO EM 12/08/2026

`demake_gen2.classe_de` reduz as 68 colisoes que o BW3G usa a sete classes, e as
que ele nao conhece caem em `parede`. Resultado na ROM: mediana de 3 metatiles
distintos por mapa, 155 dos 291 com 3 ou menos. Ledge, gelo, cachoeira, arvore de
Cut, balcao de loja e PISO DE CAVERNA viravam parede ou chao liso.

O piso de caverna e o caso caro: `MetatileBehavior_IsLandWildEncounter` exige
`TILE_FLAG_HAS_ENCOUNTERS` (src/metatile_behavior.c), que o `MB_NORMAL` nao tem e
o `MB_CAVE` tem. Com o chao das cavernas em `MB_NORMAL` (metatile 843), as 45
tabelas de encontro de caverna de Unova NUNCA disparavam, mesmo existindo grama
alta em outros 35 mapas. Aqui o chao de caverna passa a ser o 513, `MB_CAVE`
andavel, que e o mesmo que MtCoronet e IcePath usam em 85 mapas de Sinnoh.

O CASAMENTO, QUE E EXATO E NAO APROXIMADO

Um bloco do gen 2 tem 4x4 tiles de 8x8 = 32x32 px, e o `_collision.asm` da
`tilecoll A,B,C,D`: a colisao dos quatro quadrantes de 16x16, na ordem
cima-esquerda, cima-direita, baixo-esquerda, baixo-direita. Um quadrante de 16x16
E um metatile do GBA. Logo 1 bloco = 4 metatiles, sem perda e sem arredondamento,
e o `.ablk` de 14x22 de AspertiaCity vira o layout de 28x44 que ja esta na ROM.

DE ONDE SAI CADA NUMERO DA TABELA (nada foi escolhido de cabeca)

1. A classe de cada `COLL_*` sai do NOME quando o nome tem sentido de jogo
   (`TALL_GRASS`, `HOP_DOWN`, `LADDER`, ...) e, quando nao tem, da propria
   permissao do gen 2 em `data/collision_permissions.asm`: `LANDTILE` vira chao,
   `WATERTILE` vira agua, `WALLTILE` vira parede. Isso cobre inclusive os cinco
   valores de lixo (`01`, `FF`, `9C`, `64`, `65`) sem chute.
2. O metatile de destino sai de MEDIR os `map.bin` que ja existem no repo para
   aquele par de tilesets (excluindo Unova, que e justamente o degenerado), com o
   comportamento lido de `metatile_attributes.bin`. Entre dois candidatos com o
   comportamento certo, ganha o mais usado; o desempate visual foi feito
   renderizando o metatile com `dev_scripts/render_maps.py`.
3. Colisao e elevacao NAO sao copiadas do vanilla, sao regra: andavel = colisao 0
   e elevacao 3, agua = colisao 0 e elevacao 1 (`ELEVATION_SURF`), bloqueado =
   colisao 1 e elevacao 0. A elevacao importa: hoje Unova esta com elevacao 0 em
   TUDO, e `IsElevationMismatchAt` devolve FALSE para elevacao 0, entao o jogador
   atravessaria a agua a pe. Com agua em 1 e chao em 3, o motor barra sozinho,
   que e como o Hoenn vanilla faz (medido em Route103 e PetalburgCity).

Quando o par de tilesets emprestado nao tem o comportamento, a entrada cai numa
classe vizinha e o motivo comeca com "FALLBACK". `--demo` confere que toda
entrada NAO marcada como fallback tem mesmo o comportamento que promete.

DUAS DECISOES DO CONDUTOR, 12/08/2026, para o B12.a nao desfazer sem querer:

1. Os 18 mapas com `land_mons` que continuam sem tile de encontro
   (CelestialTower, DragonspiralTower1F a 6F, DreamyardB1F, LostlornForest,
   P2Lab, RelicCastle1F e B1F a B4F, StrangeHouse1F, StrangeHouseB1F,
   VirbankComplexOutside) FICAM ASSIM. Medido: `Building + GenericBuilding` nao
   tem UM metatile com `TILE_FLAG_HAS_ENCOUNTERS`, e o par de exterior so tem
   grama alta. Eles ganham piso proprio no B12.a, cujos tilesets de origem
   (`traditional_house`, `tower`, `desert`, `forest`, `facility`, `complex`)
   entram cedo na ordem de conversao. Proibido tapar isso com tapete de grama
   ou com parede de caverna na Dragonspiral.
2. O piso e a parede de caverna ficam em 513 + 753, o par canonico dos 85 mapas
   de Sinnoh, apesar do contraste baixo na visao geral do mapa. Trocar por
   estetica agora e retrabalho jogado fora quando o B12.a der arte propria as
   cavernas de Unova.
"""
import json
import os
import re
import statistics
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))

import importa_unova as iu      # noqa: E402  le_grupos, blocos compartilhados, conexoes
import valida_warp_tile as vw   # noqa: E402  atributos de metatile e comportamentos de warp

BW3G = iu.BW3G
MB = vw._MB
NOME_MB = vw.NOME

# --------------------------------------------------------------------- classes
#
# COLL_* -> classe. So esta aqui o que tem sentido de jogo; o resto cai na
# permissao do gen 2 (ver `classe_de`). Nome sem o prefixo COLL_, que e como o
# `_collision.asm` escreve.
CLASSE = {
    "FLOOR": "chao", "CAVE": "chao_caverna", "PIT": "chao", "PIT_68": "chao",
    "STAIRCASE": "chao", "STAIRCASE_73": "chao",
    "STAIRS_RIGHT_DOWN": "chao", "STAIRS_LEFT_DOWN": "chao",
    "STAIRS_RIGHT_UP": "chao", "STAIRS_LEFT_UP": "chao",
    # as "side walls" do gen 2 sao LANDTILE: elas barram UMA direcao, nao a casa.
    # O par emprestado nao tem MB_IMPASSABLE_* (so o CaveSinnoh, e so ao norte),
    # entao viram chao. Abrir uma cerca e menos grave que cortar um caminho, e
    # sao 576 quadrantes nos 58 tilesets.
    "RIGHT_WALL": "chao", "LEFT_WALL": "chao", "UP_WALL": "chao",
    "DOWN_WALL": "chao", "UP_RIGHT_WALL": "chao", "UP_LEFT_WALL": "chao",
    "DOWN_RIGHT_WALL": "chao", "DOWN_LEFT_WALL": "chao",
    "BRAKE": "chao", "WALK_UP": "chao", "WALK_DOWN": "chao",
    "WALK_LEFT": "chao", "WALK_RIGHT": "chao",

    "TALL_GRASS": "grama", "TALL_GRASS_10": "grama", "LONG_GRASS": "grama",
    "GRASS_4A": "grama", "GRASS_4B": "grama",

    "WATER": "agua", "WATER_21": "agua", "WHIRLPOOL": "agua", "CUT_28": "agua",
    "CURRENT_RIGHT": "agua", "CURRENT_LEFT": "agua",
    "CURRENT_UP": "agua", "CURRENT_DOWN": "agua",
    "WATERFALL": "cachoeira", "WATERFALL_LEFT": "cachoeira",
    "WATERFALL_RIGHT": "cachoeira", "WATERFALL_UP": "cachoeira",
    "PUDDLE": "poca", "ICE": "gelo", "ICE_2B": "gelo",

    "WALL": "parede", "BUOY": "parede", "WINDOW": "parede",
    "INCENSE_BURNER": "parede", "VIRTUAL_BOY": "parede",
    "CUT_TREE": "arvore", "CUT_TREE_1A": "arvore", "HEADBUTT_TREE": "arvore",

    "HOP_DOWN": "ledge_baixo", "HOP_DOWN_LEFT": "ledge_baixo",
    "HOP_DOWN_RIGHT": "ledge_baixo",
    "HOP_LEFT": "ledge_esq", "HOP_UP_LEFT": "ledge_esq",
    "HOP_RIGHT": "ledge_dir", "HOP_UP_RIGHT": "ledge_dir",
    "HOP_UP": "ledge_cima",

    "LADDER": "escada",
    "DOOR": "porta", "DOOR_75": "porta", "DOOR_79": "porta", "DOOR_7D": "porta",
    "WARP_CARPET_DOWN": "porta", "WARP_CARPET_UP": "porta",
    "WARP_CARPET_LEFT": "porta", "WARP_CARPET_RIGHT": "porta",
    "WARP_PANEL": "porta", "WARP_77": "porta", "WARP_7F": "porta",

    "COUNTER": "balcao", "COUNTER_98": "balcao",
    "BOOKSHELF": "estante", "MART_SHELF": "estante",
    "PC": "pc", "TV": "tv", "RADIO": "tv", "TOWN_MAP": "tv",
}

CLASSES = ("chao", "chao_caverna", "grama", "agua", "cachoeira", "poca", "gelo",
           "parede", "arvore", "ledge_baixo", "ledge_esq", "ledge_dir",
           "ledge_cima", "escada", "porta", "balcao", "estante", "pc", "tv")

# classe -> comportamentos aceitos na conferencia (entrada marcada FALLBACK escapa)
ESPERADO = {
    # MB_CAVE entra em `chao` de proposito: dentro de caverna o piso comum E o
    # MB_CAVE, e e ele que carrega TILE_FLAG_HAS_ENCOUNTERS.
    "chao": ("MB_NORMAL", "MB_CAVE"),
    "chao_caverna": ("MB_CAVE",),
    "grama": ("MB_TALL_GRASS", "MB_LONG_GRASS"),
    "agua": ("MB_POND_WATER", "MB_DEEP_WATER", "MB_OCEAN_WATER",
             "MB_INTERIOR_DEEP_WATER", "MB_SHALLOW_WATER"),
    "cachoeira": ("MB_WATERFALL",),
    "poca": ("MB_PUDDLE", "MB_SHALLOW_WATER"),
    "gelo": ("MB_ICE", "MB_THIN_ICE"),
    "parede": ("MB_NORMAL", "MB_MOUNTAIN_TOP", "MB_CAVE"),
    "arvore": ("MB_NORMAL", "MB_MOUNTAIN_TOP", "MB_CAVE"),
    "ledge_baixo": ("MB_JUMP_SOUTH",),
    "ledge_esq": ("MB_JUMP_WEST",),
    "ledge_dir": ("MB_JUMP_EAST",),
    "ledge_cima": ("MB_JUMP_NORTH",),
    "escada": ("MB_LADDER",),
    "porta": ("MB_NON_ANIMATED_DOOR", "MB_ANIMATED_DOOR", "MB_SOUTH_ARROW_WARP",
              "MB_NORTH_ARROW_WARP", "MB_EAST_ARROW_WARP", "MB_WEST_ARROW_WARP"),
    "balcao": ("MB_COUNTER",),
    "estante": ("MB_BOOKSHELF", "MB_SHOP_SHELF", "MB_POKEMON_CENTER_BOOKSHELF",
                "MB_PICTURE_BOOK_SHELF"),
    "pc": ("MB_PC",),
    "tv": ("MB_TELEVISION",),
}

# ------------------------------------------------------------------- as paletas
#
# par (primary, secondary) declarado no layouts.json -> nome da paleta. O par sai
# do layouts.json e nao da tabela de importacao: o que manda e o que esta na ROM.
PALETA_DO_PAR = {
    ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh"): "exterior",
    ("gTileset_GeneralSinnoh", "gTileset_CaveSinnoh"): "caverna",
    ("gTileset_Building", "gTileset_GenericBuilding"): "interior",
    ("gTileset_Building", "gTileset_PokemonCenter"): "pokecenter",
    ("gTileset_Building", "gTileset_Shop"): "loja",
    ("gTileset_Building", "gTileset_RustboroGym"): "ginasio",
}

ANDA, BLOQ, AGUA = (0, 3), (1, 0), (0, 1)   # (colisao, elevacao)

# paleta -> classe -> (metatile, colisao, elevacao, motivo)
PALETA = {
    # 75 mapas de Unova. GeneralSinnoh e primario (0-511), PetalburgSinnoh
    # secundario (512+). Medido em 52 layouts nao-Unova deste par.
    "exterior": {
        "chao":        (1, *ANDA, "MB_NORMAL, 1655 usos em 7 mapas, gramado liso"),
        "chao_caverna": (1, *ANDA, "FALLBACK -> chao: MB_CAVE so existe no CaveSinnoh"),
        "grama":       (13, *ANDA, "MB_TALL_GRASS, 823 usos em 4 mapas"),
        "agua":        (161, *AGUA, "MB_POND_WATER, 946 usos"),
        "cachoeira":   (76, *AGUA, "MB_WATERFALL, agua com espuma branca"),
        "poca":        (218, *ANDA, "MB_PUDDLE"),
        "gelo":        (1, *ANDA, "FALLBACK -> chao: nenhum MB_ICE neste par"),
        "parede":      (113, *BLOQ, "MB_MOUNTAIN_TOP, encosta de montanha, 49 usos"),
        "arvore":      (470, *BLOQ, "MB_NORMAL bloqueado, copa de arvore, 1141 usos"),
        "ledge_baixo": (135, *BLOQ, "MB_JUMP_SOUTH, 54 usos em 3 mapas"),
        "ledge_esq":   (133, *BLOQ, "MB_JUMP_WEST, 4 usos"),
        "ledge_dir":   (255, *BLOQ, "MB_JUMP_EAST, par de fundo verde do 254"),
        "ledge_cima":  (1, *ANDA, "FALLBACK -> chao: nenhum MB_JUMP_NORTH neste par"),
        "escada":      (167, *ANDA, "FALLBACK -> porta: nenhum MB_LADDER; porta tambem warpa"),
        "porta":       (167, *ANDA, "MB_NON_ANIMATED_DOOR, arco escuro"),
        "balcao":      (113, *BLOQ, "FALLBACK -> parede: nenhum MB_COUNTER neste par"),
        "estante":     (113, *BLOQ, "FALLBACK -> parede: nenhuma estante neste par"),
        "pc":          (113, *BLOQ, "FALLBACK -> parede: nenhum MB_PC neste par"),
        "tv":          (113, *BLOQ, "FALLBACK -> parede: nenhum MB_TELEVISION neste par"),
    },
    # 32 mapas de Unova. O 513 e a correcao central do bloco: MB_CAVE ANDAVEL,
    # 16811 usos em 85 mapas de Sinnoh, e o unico jeito de a caverna disparar
    # encontro (TILE_FLAG_HAS_ENCOUNTERS).
    "caverna": {
        "chao":        (513, *ANDA, "MB_CAVE andavel, 16811 usos em 85 mapas"),
        "chao_caverna": (513, *ANDA, "MB_CAVE andavel, mesmo piso"),
        "grama":       (13, *ANDA, "MB_TALL_GRASS do primario, compartilhado"),
        "agua":        (161, *AGUA, "MB_POND_WATER, 3733 usos em 7 mapas"),
        "cachoeira":   (76, *AGUA, "MB_WATERFALL do primario"),
        "poca":        (218, *ANDA, "MB_PUDDLE do primario"),
        "gelo":        (909, *ANDA, "MB_ICE do CaveSinnoh, piso do IcePath"),
        "parede":      (753, *BLOQ, "MB_CAVE bloqueado, 108438 usos, parede de rocha"),
        "arvore":      (753, *BLOQ, "FALLBACK -> parede: nao ha arvore em caverna"),
        "ledge_baixo": (593, *BLOQ, "MB_JUMP_SOUTH do CaveSinnoh, 7 usos"),
        "ledge_esq":   (850, *BLOQ, "MB_JUMP_WEST do CaveSinnoh"),
        "ledge_dir":   (851, *BLOQ, "MB_JUMP_EAST do CaveSinnoh"),
        "ledge_cima":  (513, *ANDA, "FALLBACK -> chao: nenhum MB_JUMP_NORTH neste par"),
        "escada":      (575, *ANDA, "MB_LADDER, 66 usos em 39 mapas"),
        "porta":       (167, *ANDA, "MB_NON_ANIMATED_DOOR do primario, arco de caverna"),
        "balcao":      (753, *BLOQ, "FALLBACK -> parede: nenhum MB_COUNTER neste par"),
        "estante":     (753, *BLOQ, "FALLBACK -> parede"),
        "pc":          (753, *BLOQ, "FALLBACK -> parede: nenhum MB_PC neste par"),
        "tv":          (753, *BLOQ, "FALLBACK -> parede: nenhum MB_TELEVISION neste par"),
    },
    # 138 mapas de Unova, o maior grupo. Building e primario e so tem 8 metatiles
    # (0-7), e e por isso que PC e TV vem de la: eles existem em TODO par que usa
    # Building, inclusive ginasio e loja.
    "interior": {
        "chao":        (812, *ANDA, "MB_NORMAL, 855 usos em 26 mapas"),
        "chao_caverna": (812, *ANDA, "FALLBACK -> chao: nao ha caverna em interior"),
        "grama":       (812, *ANDA, "FALLBACK -> chao: nenhum MB_TALL_GRASS neste par"),
        "agua":        (824, *BLOQ, "FALLBACK -> parede: nenhuma agua neste par"),
        "cachoeira":   (824, *BLOQ, "FALLBACK -> parede"),
        "poca":        (812, *ANDA, "FALLBACK -> chao"),
        "gelo":        (812, *ANDA, "FALLBACK -> chao"),
        "parede":      (824, *BLOQ, "MB_NORMAL bloqueado, 232 usos em 26 mapas"),
        "arvore":      (824, *BLOQ, "FALLBACK -> parede"),
        "ledge_baixo": (812, *ANDA, "FALLBACK -> chao: nenhum MB_JUMP_* neste par"),
        "ledge_esq":   (812, *ANDA, "FALLBACK -> chao"),
        "ledge_dir":   (812, *ANDA, "FALLBACK -> chao"),
        "ledge_cima":  (812, *ANDA, "FALLBACK -> chao"),
        "escada":      (523, *ANDA, "FALLBACK -> porta: sem MB_LADDER, e escada aqui e warp"),
        "porta":       (523, *ANDA, "MB_NON_ANIMATED_DOOR, 27 usos em 25 mapas"),
        "balcao":      (1014, *BLOQ, "MB_COUNTER"),
        "estante":     (898, *BLOQ, "MB_BOOKSHELF, 6 usos em 6 mapas"),
        "pc":          (4, *BLOQ, "MB_PC do primario Building"),
        "tv":          (542, *BLOQ, "MB_TELEVISION, 12 usos em 12 mapas"),
    },
    # 19 mapas de Unova (todo Pokecenter).
    "pokecenter": {
        "chao":        (514, *ANDA, "MB_NORMAL, 388 usos em 13 mapas"),
        "chao_caverna": (514, *ANDA, "FALLBACK -> chao"),
        "grama":       (514, *ANDA, "FALLBACK -> chao"),
        "agua":        (523, *BLOQ, "FALLBACK -> parede"),
        "cachoeira":   (523, *BLOQ, "FALLBACK -> parede"),
        "poca":        (514, *ANDA, "FALLBACK -> chao"),
        "gelo":        (514, *ANDA, "FALLBACK -> chao"),
        "parede":      (523, *BLOQ, "MB_NORMAL bloqueado, 71 usos em 13 mapas"),
        "arvore":      (523, *BLOQ, "FALLBACK -> parede"),
        "ledge_baixo": (514, *ANDA, "FALLBACK -> chao"),
        "ledge_esq":   (514, *ANDA, "FALLBACK -> chao"),
        "ledge_dir":   (514, *ANDA, "FALLBACK -> chao"),
        "ledge_cima":  (514, *ANDA, "FALLBACK -> chao"),
        "escada":      (575, *ANDA, "FALLBACK -> porta: escada de Pokecenter e warp"),
        "porta":       (575, *ANDA, "MB_NON_ANIMATED_DOOR, 16 usos em 6 mapas"),
        "balcao":      (727, *BLOQ, "MB_COUNTER, 15 usos, o balcao da enfermeira"),
        "estante":     (626, *BLOQ, "MB_POKEMON_CENTER_BOOKSHELF, 6 usos"),
        "pc":          (4, *BLOQ, "MB_PC do primario, 13 usos em 13 mapas"),
        "tv":          (3, *BLOQ, "MB_TELEVISION do primario Building"),
    },
    # 8 mapas de Unova (Mart e lojas de departamento).
    "loja": {
        "chao":        (616, *ANDA, "MB_NORMAL, 153 usos em 4 mapas"),
        "chao_caverna": (616, *ANDA, "FALLBACK -> chao"),
        "grama":       (616, *ANDA, "FALLBACK -> chao"),
        "agua":        (648, *BLOQ, "FALLBACK -> parede"),
        "cachoeira":   (648, *BLOQ, "FALLBACK -> parede"),
        "poca":        (616, *ANDA, "FALLBACK -> chao"),
        "gelo":        (616, *ANDA, "FALLBACK -> chao"),
        "parede":      (648, *BLOQ, "MB_NORMAL bloqueado, 61 usos em 7 mapas"),
        "arvore":      (648, *BLOQ, "FALLBACK -> parede"),
        "ledge_baixo": (616, *ANDA, "FALLBACK -> chao"),
        "ledge_esq":   (616, *ANDA, "FALLBACK -> chao"),
        "ledge_dir":   (616, *ANDA, "FALLBACK -> chao"),
        "ledge_cima":  (616, *ANDA, "FALLBACK -> chao"),
        "escada":      (592, *ANDA, "FALLBACK -> porta"),
        "porta":       (592, *ANDA, "MB_NON_ANIMATED_DOOR, 5 usos em 5 mapas"),
        "balcao":      (674, *BLOQ, "MB_COUNTER, 14 usos em 3 mapas"),
        "estante":     (691, *BLOQ, "MB_SHOP_SHELF, 8 usos em 3 mapas"),
        "pc":          (4, *BLOQ, "MB_PC do primario Building"),
        "tv":          (3, *BLOQ, "MB_TELEVISION do primario Building"),
    },
    # 19 mapas de Unova (salas da Liga, campeao, Elite dos Quatro).
    # Este par nao tem porta nenhuma: o unico comportamento de warp e a seta sul
    # do primario Building (metatile 7), que so dispara andando para BAIXO. Ainda
    # assim e melhor que o chao liso de antes, que nunca disparava.
    "ginasio": {
        "chao":        (513, *ANDA, "MB_NORMAL, 891 usos em 5 mapas"),
        "chao_caverna": (513, *ANDA, "FALLBACK -> chao"),
        "grama":       (513, *ANDA, "FALLBACK -> chao"),
        "agua":        (518, *BLOQ, "FALLBACK -> parede"),
        "cachoeira":   (518, *BLOQ, "FALLBACK -> parede"),
        "poca":        (513, *ANDA, "FALLBACK -> chao"),
        "gelo":        (513, *ANDA, "FALLBACK -> chao"),
        "parede":      (518, *BLOQ, "MB_NORMAL bloqueado, 491 usos em 5 mapas"),
        "arvore":      (518, *BLOQ, "FALLBACK -> parede"),
        "ledge_baixo": (513, *ANDA, "FALLBACK -> chao"),
        "ledge_esq":   (513, *ANDA, "FALLBACK -> chao"),
        "ledge_dir":   (513, *ANDA, "FALLBACK -> chao"),
        "ledge_cima":  (513, *ANDA, "FALLBACK -> chao"),
        "escada":      (7, *ANDA, "FALLBACK -> porta (seta sul)"),
        "porta":       (7, *ANDA, "MB_SOUTH_ARROW_WARP do primario; so dispara indo ao sul"),
        "balcao":      (518, *BLOQ, "FALLBACK -> parede"),
        "estante":     (518, *BLOQ, "FALLBACK -> parede"),
        "pc":          (4, *BLOQ, "MB_PC do primario Building"),
        "tv":          (3, *BLOQ, "MB_TELEVISION do primario Building"),
    },
}

COMPORTA_WARP = vw.COMPORTA_WARP

# ------------------------------------------------------------------ leitura BW3G

_RE_TILECOLL = re.compile(
    r"\s*tilecoll\s+(\w+),\s*(\w+),\s*(\w+),\s*(\w+)\s*;\s*([0-9a-fA-F]+)")


def valores_coll():
    """COLL_<NOME> -> valor, lido de constants/collision_constants.asm."""
    saida = {}
    for ln in open(f"{BW3G}/constants/collision_constants.asm"):
        m = re.match(r"COLL_(\w+)\s+EQU\s+\$([0-9a-fA-F]+)", ln)
        if m:
            saida[m.group(1)] = int(m.group(2), 16)
    return saida


def permissoes():
    """valor de COLL -> 'LANDTILE' | 'WATERTILE' | 'WALLTILE'.

    A ordem das linhas de `TileCollisionTable` E o indice: a n-esima linha e o
    COLL de valor n. Sao 256 entradas.
    """
    saida, i = {}, 0
    for ln in open(f"{BW3G}/data/collision_permissions.asm"):
        m = re.match(r"\s*(NONTALKABLE|TALKABLE)\s+(LANDTILE|WATERTILE|WALLTILE)", ln)
        if m:
            saida[i] = m.group(2)
            i += 1
    assert i == 256, f"collision_permissions.asm com {i} entradas, esperava 256"
    return saida


VALOR = valores_coll()
PERM = permissoes()
PADRAO_PERM = {"LANDTILE": "chao", "WATERTILE": "agua", "WALLTILE": "parede"}
_DESCONHECIDOS = set()


def classe_de(token):
    """Token do `_collision.asm` (nome ou hex cru) -> classe."""
    if token in CLASSE:
        return CLASSE[token]
    valor = VALOR.get(token)
    if valor is None and re.fullmatch(r"[0-9a-fA-F]{1,2}", token):
        valor = int(token, 16)
    if valor is None:
        _DESCONHECIDOS.add(token)
        return "parede"    # prender e menos grave que jogar o jogador para fora
    return PADRAO_PERM[PERM[valor]]


def quadrantes(arquivo_collision):
    """bloco -> (classe do quadrante) x4, na ordem CE, CD, BE, BD."""
    tabela = {}
    caminho = os.path.join(BW3G, "data/tilesets", arquivo_collision)
    for ln in open(caminho):
        m = _RE_TILECOLL.match(ln)
        if m:
            tabela[int(m.group(5), 16)] = tuple(classe_de(m.group(i)) for i in (1, 2, 3, 4))
    return tabela


# ------------------------------------------------------------------- conversao


def celula(classe, pal):
    mt, col, elev, _ = PALETA[pal][classe]
    return (mt & 0x3FF) | ((col & 3) << 10) | ((elev & 0xF) << 12)


def converte(blocos, lb, hb, tabqd, pal):
    """(bytes do .ablk, largura e altura em BLOCOS) -> bytes do map.bin."""
    lm, hm = lb * 2, hb * 2
    saida = bytearray(lm * hm * 2)
    faltando = ("parede",) * 4
    for by in range(hb):
        for bx in range(lb):
            quad = tabqd.get(blocos[by * lb + bx], faltando)
            for i, (dx, dy) in enumerate(((0, 0), (1, 0), (0, 1), (1, 1))):
                x, y = bx * 2 + dx, by * 2 + dy
                struct.pack_into("<H", saida, (y * lm + x) * 2, celula(quad[i], pal))
    return bytes(saida)


# ------------------------------------------------------------- B12.a: arte propria
#
# Quando o tileset do BW3G ja foi convertido em tileset secundario do GBA por
# `tileset_gen2.py`, o `.ablk` deixa de virar CLASSE DE COMPORTAMENTO e passa a
# virar o metatile REAL do bloco: mapeamento identidade pos-deduplicacao. O que
# NAO muda: dimensao do layout, indice de mapa, warp, object_event, bg_event e o
# tamanho de cada arquivo (o guarda-corpo do `grava` continua valendo).


def _tg2():
    """Import tardio: `tileset_gen2` importa ESTE arquivo, entao no topo daria
    ciclo. Aqui a dependencia so existe quando o modo de arte e pedido."""
    import tileset_gen2
    return tileset_gen2


def arte_disponivel(_cache={}):
    """Tileset do BW3G -> rotulo gTileset_*, so para os que estao NA BUILD.

    Existir a pasta nao basta: o B10 permite deixar tileset convertido no repo e
    fora da build (entrada comentada). Quem manda e a declaracao viva em
    `include/tilesets.h`, que e o que a build enxerga.
    """
    if _cache:
        return _cache
    tg = _tg2()
    vivos = set(re.findall(r"^extern const struct Tileset (gTileset_\w+);",
                           open(f"{RAIZ}/include/tilesets.h").read(), re.M))
    for n in tg.todos():
        rot = "gTileset_" + tg.rotulo_de(n)
        if rot in vivos and os.path.exists(f"{tg.pasta_de(n)}/metatiles.bin"):
            _cache[n] = rot
    return _cache


def _tileset_convertido(nome, _cache={}):
    if nome not in _cache:
        tg = _tg2()
        _cache[nome] = tg.converte(nome, tg.portas_necessarias(nome), tg.pulos_necessarios(nome))
    return _cache[nome]


# O pulo do gen 2, traduzido para o gen 3, e o DESLOCAMENTO DE UM TILE.
#
# Medido no codigo da fonte, nao lembrado:
#   `data/collision_permissions.asm:167` -> COLL_HOP_* e LANDTILE, o jogador ANDA
#   em cima do tile de pulo; `engine/overworld/player_movement.asm:362`
#   (`.TryJump`) le `wPlayerStandingTile` e pula 2 casas a partir de ONDE ELE
#   ESTA, e so se o destino for andavel.
# No gen 3 o ledge e a casa DA FRENTE: `ShouldJumpLedge` olha o metatile do tile
# para onde o jogador anda e pula por cima dele.
#
# Logo: um HOP_LEFT do gen 2 em L vira, aqui, "L andavel + L+(-1,0) com
# MB_JUMP_WEST". Sem esse deslocamento o pulo simplesmente deixa de existir, e
# isso NAO e detalhe: no BW3G varios pulos atravessam PAREDE (medido em
# Unova_DragonspiralTower3F e Unova_OpelucidGym, onde o mapa se parte em ilhas
# sem eles).
PULO = {"ledge_esq": (-1, 0), "ledge_dir": (1, 0),
        "ledge_cima": (0, -1), "ledge_baixo": (0, 1)}
ANDAVEL_FONTE = ("chao", "chao_caverna", "grama", "poca", "gelo", "escada",
                 "porta") + tuple(PULO)


def alvos_de_pulo(blocos, lb, hb, tabqd):
    """{(x, y) em metatiles: classe de ledge} dos tiles que precisam de MB_JUMP_*.

    Regra, e ela e conservadora de proposito: so vira alvo o tile que a fonte tem
    como PAREDE e que fica entre um ledge e um destino ANDAVEL. Se o tile do meio
    ja for andavel, andar chega no mesmo lugar e marcar o tile como ledge do gen 3
    (que e impassavel) FECHARIA um caminho que existia. Se o destino for parede, o
    gen 2 tambem nao deixa pular, e o gen 3 pularia para dentro dela, porque
    `ShouldJumpLedge` nao confere o pouso.
    """
    lm, hm = lb * 2, hb * 2
    classe = {}
    for by in range(hb):
        for bx in range(lb):
            quad = tabqd.get(blocos[by * lb + bx], ("parede",) * 4)
            for i, (dx, dy) in enumerate(((0, 0), (1, 0), (0, 1), (1, 1))):
                classe[(bx * 2 + dx, by * 2 + dy)] = quad[i]
    saida = {}
    for (x, y), c in classe.items():
        if c not in PULO:
            continue
        dx, dy = PULO[c]
        meio, pouso = (x + dx, y + dy), (x + 2 * dx, y + 2 * dy)
        if classe.get(meio) != "parede":
            continue
        if classe.get(pouso) not in ANDAVEL_FONTE:
            continue
        saida[meio] = c
    return saida


def converte_arte(blocos, lb, hb, tabqd, ts, portas=(), ambiente=None):
    """Como `converte`, mas emitindo o metatile REAL de cada quadrante do bloco.

    `portas` = {(x, y)} em metatiles onde ha warp; ali entra a variante do MESMO
    desenho com comportamento de porta, que `tileset_gen2.portas_necessarias`
    mandou criar. O warp nao se move e nenhum outro tile muda.

    `ambiente` e o do gen 2 (`maps.asm`). Em CAVE e DUNGEON o chao usa a variante
    de masmorra, que sai com `MB_CAVE` e por isso dispara encontro selvagem; e o
    que destrava os mapas mudos do B12.c sem tapete de grama.
    """
    tg = _tg2()
    q2m = ts["masmorra2mt"] if ambiente in tg.MASMORRA else ts["quad2mt"]
    lm, hm = lb * 2, hb * 2
    saida = bytearray(lm * hm * 2)
    faltando = ("parede",) * 4
    forcados = 0
    pulos = alvos_de_pulo(blocos, lb, hb, tabqd)
    for by in range(hb):
        for bx in range(lb):
            b = blocos[by * lb + bx]
            quad = tabqd.get(b, faltando)
            for i, (dx, dy) in enumerate(((0, 0), (1, 0), (0, 1), (1, 1))):
                x, y = bx * 2 + dx, by * 2 + dy
                classe = quad[i]
                if ambiente in tg.MASMORRA and classe == "chao":
                    classe = "chao_caverna"
                mt = q2m.get((b, i))
                if (x, y) in portas and (b, i) in ts["porta2mt"]:
                    mt, classe = ts["porta2mt"][(b, i)], "porta"
                    forcados += 1
                elif (x, y) in pulos and (b, i, pulos[(x, y)]) in ts["pulo2mt"]:
                    classe = "pulo_" + pulos[(x, y)].split("_", 1)[1]
                    mt = ts["pulo2mt"][(b, i, pulos[(x, y)])]
                if mt is None:                  # bloco que o tileset nao tem
                    mt, classe = 0, "parede"
                col, elev = tg.colisao_da_classe(classe)
                struct.pack_into("<H", saida, (y * lm + x) * 2,
                                 ((512 + mt) & 0x3FF) | (col << 10) | (elev << 12))
    return bytes(saida), forcados


def warps_do_mapa(nome, l):
    d = le_map_json(nome)
    return {(w.get("x", 0), w.get("y", 0)) for w in (d or {}).get("warp_events") or []
            if 0 <= w.get("x", 0) < l["width"] and 0 <= w.get("y", 0) < l["height"]}


def grava_layouts(novos):
    """Aponta o `secondary_tileset` dos layouts de Unova convertidos para o
    tileset novo. NADA MAIS muda no layouts.json: nem dimensao, nem caminho de
    blockdata, nem entrada de outra regiao."""
    p = f"{RAIZ}/data/layouts/layouts.json"
    d = json.load(open(p))
    n = 0
    for l in d["layouts"]:
        if not l["id"].startswith("LAYOUT_UNOVA_"):
            continue
        nome = l["name"][:-len("_Layout")]
        novo = novos.get(nome)
        if novo and l["secondary_tileset"] != novo:
            l["secondary_tileset"] = novo
            n += 1
    if n:
        with open(p, "w") as f:
            # sem `\n` no fim: e assim que o arquivo esta no HEAD, e acrescentar
            # um poe uma linha a mais no diff que nao e mudanca de conteudo.
            json.dump(d, f, indent=2)
    return n


# ----------------------------------------------------------------- inventario

def layouts():
    return {l["id"]: l for l in
            json.load(open(f"{RAIZ}/data/layouts/layouts.json"))["layouts"]}


def mapas_unova():
    """[(nome, layout, tileset_gen2, arquivo_ablk, lb, hb)] na ordem do BW3G.

    Reusa o pareamento posicional do `importa_unova.py` (a armadilha 1 do
    cabecalho dele): o nome CamelCase NAO gera a constante do mapa.
    """
    blocos = iu.le_blocos_compartilhados()
    lay = layouts()
    saida, pulados = [], []
    for _, mapas in iu.le_grupos():
        for camel, const, w, h, tset, _amb, _lm, _mus in mapas:
            nome = iu.PREFIXO + camel
            lid = iu.PREFIXO_LAYOUT + const
            l = lay.get(lid)
            if l is None:
                pulados.append((nome, f"layout {lid} nao esta em layouts.json"))
                continue
            arq = blocos.get(camel)
            if not arq or not os.path.exists(arq):
                pulados.append((nome, "sem .ablk na fonte"))
                continue
            if (l["width"], l["height"]) != (w * 2, h * 2):
                pulados.append((nome, f"layout {l['width']}x{l['height']} nao casa "
                                      f"com o .ablk {w}x{h} (esperava {w*2}x{h*2})"))
                continue
            alvo = iu.COLISAO_ALIAS.get(tset, tset)
            par = (l["primary_tileset"], l["secondary_tileset"])
            # o segundo caso e o B12.a: depois que o layout aponta para o tileset
            # proprio, o par deixa de estar em PALETA_DO_PAR e o mapa seria pulado
            # calado, desfazendo a conversao na rodada seguinte.
            if par not in PALETA_DO_PAR and \
                    l["secondary_tileset"] != arte_disponivel().get(alvo):
                pulados.append((nome, f"par de tileset desconhecido: {par}"))
                continue
            saida.append((nome, l, alvo, camel, arq, w, h, _amb))
    return saida, pulados


# ------------------------------------------------------------------- medicao

def atributos(ts, _cache={}):
    if ts not in _cache:
        _cache[ts] = vw.tabela_de_atributos(ts)
    return _cache[ts]


def comportamentos(l):
    """(funcao metatile -> comportamento) para um layout."""
    prim, _ = atributos(l["primary_tileset"])
    seg, _ = atributos(l["secondary_tileset"])
    corte = 640 if l.get("layout_version") in ("frlg", "johto") else 512

    def beh(mt):
        tab, rel = (prim, mt) if mt < corte else (seg, mt - corte)
        return tab[rel] if 0 <= rel < len(tab) else None
    return beh


def le_map_json(nome):
    p = f"{RAIZ}/data/maps/{nome}/map.json"
    return json.load(open(p)) if os.path.exists(p) else None


def mede_mapa(nome, l, dados):
    """Metricas de UM mapa a partir dos bytes do blockdata (nao do disco).

    Separado de proposito: e assim que o `--demo` consegue medir um blockdata
    mutado sem gravar nada.
    """
    beh = comportamentos(l)
    w, h = l["width"], l["height"]
    ids, celulas = set(), []
    for o in range(0, len(dados), 2):
        v = struct.unpack_from("<H", dados, o)[0]
        ids.add(v & 0x3FF)
        celulas.append(v)
    encontro_terra = sum(1 for v in celulas
                         if beh(v & 0x3FF) in ENCONTRO_TERRA and ((v >> 10) & 3) == 0)
    m = {"distintos": len(ids), "grama": sum(1 for v in celulas
                                             if beh(v & 0x3FF) == MB["MB_TALL_GRASS"]),
         "encontro_terra": encontro_terra, "warps_mortos": [], "npcs_presos": []}
    d = le_map_json(nome)
    if not d:
        return m
    for i, wp in enumerate(d.get("warp_events") or []):
        x, y = wp.get("x", 0), wp.get("y", 0)
        if not (0 <= x < w and 0 <= y < h):
            m["warps_mortos"].append((i, x, y, "fora do mapa"))
            continue
        v = celulas[y * w + x]
        c = beh(v & 0x3FF)
        if c not in COMPORTA_WARP:
            m["warps_mortos"].append((i, x, y, NOME_MB.get(c, f"comportamento {c}")))
    for i, ob in enumerate(d.get("object_events") or []):
        x, y = ob.get("x", 0), ob.get("y", 0)
        if not (0 <= x < w and 0 <= y < h):
            m["npcs_presos"].append((i, x, y, "fora do mapa"))
            continue
        v = celulas[y * w + x]
        col, elev = (v >> 10) & 3, (v >> 12) & 0xF
        if col:
            m["npcs_presos"].append((i, x, y, "colisao 1"))
        elif elev not in (0, 15) and elev != ob.get("elevation", 3):
            m["npcs_presos"].append((i, x, y, f"elevacao {elev} != NPC {ob.get('elevation')}"))
    return m


ENCONTRO_TERRA = {MB[n] for n in ("MB_TALL_GRASS", "MB_LONG_GRASS", "MB_CAVE",
                                  "MB_DEEP_SAND", "MB_ASHGRASS", "MB_FOOTPRINTS",
                                  "MB_UNUSED_05") if n in MB}


def medicao(gerados=None, tilesets_novos=None):
    """Roda as quatro medicoes do aceite. `gerados` sobrepoe o disco, em memoria.

    `tilesets_novos` ({mapa: rotulo}) sobrepoe o `secondary_tileset` do layout sem
    gravar nada: sem isso o "depois" do modo de arte seria lido com a tabela de
    comportamento do tileset EMPRESTADO, e o placar mentiria inteiro.
    """
    lay = layouts()
    dist, grama, mapas_grama, warps, warps_ok, ruins = [], 0, 0, 0, 0, []
    npcs, presos = 0, []
    com_encontro, sem_encontro = 0, []
    enc = {e["map"] for e in json.load(
        open(f"{RAIZ}/src/data/wild_encounters.json"))["wild_encounter_groups"][0]["encounters"]
        if e["map"].startswith("MAP_UNOVA_") and "land_mons" in e}
    for lid, l in sorted(lay.items()):
        if not lid.startswith("LAYOUT_UNOVA_"):
            continue
        nome = l["name"][:-len("_Layout")]
        if (tilesets_novos or {}).get(nome):
            l = dict(l, secondary_tileset=tilesets_novos[nome])
        dados = (gerados or {}).get(nome)
        if dados is None:
            p = f"{RAIZ}/{l['blockdata_filepath']}"
            if not os.path.exists(p):
                continue
            dados = open(p, "rb").read()
        m = mede_mapa(nome, l, dados)
        dist.append(m["distintos"])
        grama += m["grama"]
        mapas_grama += 1 if m["grama"] else 0
        d = le_map_json(nome)
        if d and d["id"] in enc:
            if m["encontro_terra"]:
                com_encontro += 1
            else:
                sem_encontro.append(nome)
        nw = len((d or {}).get("warp_events") or [])
        warps += nw
        warps_ok += nw - len(m["warps_mortos"])
        if m["warps_mortos"]:
            ruins.append((nome, m["warps_mortos"]))
        npcs += len((d or {}).get("object_events") or [])
        if m["npcs_presos"]:
            presos.append((nome, m["npcs_presos"]))
    return {"mapas": len(dist), "mediana": statistics.median(dist) if dist else 0,
            "max": max(dist) if dist else 0, "min": min(dist) if dist else 0,
            "ate3": sum(1 for d in dist if d <= 3),
            "grama": grama, "mapas_com_grama": mapas_grama,
            "encontro_ok": com_encontro, "encontro_sem": sem_encontro,
            "warps": warps, "warps_ok": warps_ok, "warps_ruins": ruins,
            "npcs": npcs, "npcs_presos": presos}


def imprime(m, titulo):
    print(f"\n--- {titulo} ---")
    print(f"(a) metatiles distintos por mapa: mediana {m['mediana']}, "
          f"min {m['min']}, max {m['max']}, com 3 ou menos: {m['ate3']} de {m['mapas']}")
    print(f"(b) MB_TALL_GRASS: {m['grama']} tiles em {m['mapas_com_grama']} mapas; "
          f"mapas com land_mons e algum tile de encontro andavel: {m['encontro_ok']} "
          f"(sem: {len(m['encontro_sem'])})")
    print(f"(c) warps sobre tile que dispara: {m['warps_ok']} de {m['warps']} "
          f"({100*m['warps_ok']/m['warps']:.1f}%), em {len(m['warps_ruins'])} mapas")
    print(f"(d) NPCs em tile bloqueado ou de elevacao errada: "
          f"{sum(len(v) for _, v in m['npcs_presos'])} de {m['npcs']}, "
          f"em {len(m['npcs_presos'])} mapas")


# --------------------------------------------------------------- conferencias

def confere_tabela():
    """Toda entrada nao marcada FALLBACK tem mesmo o comportamento que promete."""
    erros = []
    for pal, entradas in PALETA.items():
        par = next(p for p, n in PALETA_DO_PAR.items() if n == pal)
        prim, _ = atributos(par[0])
        seg, _ = atributos(par[1])

        def beh(mt):
            tab, rel = (prim, mt) if mt < 512 else (seg, mt - 512)
            return tab[rel] if 0 <= rel < len(tab) else None

        faltando = set(CLASSES) - set(entradas)
        if faltando:
            erros.append(f"{pal}: classes sem entrada: {sorted(faltando)}")
        for classe, (mt, col, elev, motivo) in entradas.items():
            if classe not in CLASSES:
                erros.append(f"{pal}.{classe}: classe que nao existe")
                continue
            c = beh(mt)
            if c is None:
                erros.append(f"{pal}.{classe}: metatile {mt} fora do par {par}")
                continue
            if col not in (0, 1):
                erros.append(f"{pal}.{classe}: colisao {col} invalida")
            if (col, elev) not in (ANDA, BLOQ, AGUA):
                erros.append(f"{pal}.{classe}: (colisao,elevacao)=({col},{elev}) "
                             f"fora das tres combinacoes permitidas")
            if motivo.startswith("FALLBACK"):
                continue
            aceitos = {MB[n] for n in ESPERADO[classe] if n in MB}
            if c not in aceitos:
                erros.append(f"{pal}.{classe}: metatile {mt} tem "
                             f"{NOME_MB.get(c, c)}, esperava um de {ESPERADO[classe]}")
            if classe in ("chao", "chao_caverna", "grama", "porta", "escada") and col:
                erros.append(f"{pal}.{classe}: colisao 1, o jogador nao pisa nele")
            if classe in ("parede", "arvore") and not col:
                erros.append(f"{pal}.{classe}: colisao 0, nao bloqueia")
            if classe == "agua" and (col, elev) != AGUA:
                erros.append(f"{pal}.{classe}: agua precisa de elevacao "
                             f"{AGUA[1]} (ELEVATION_SURF), tem {elev}")
    # toda colisao que os 58 tilesets usam de fato tem que ter classe conhecida
    for f in sorted(os.listdir(f"{BW3G}/data/tilesets")):
        if f.endswith("_collision.asm"):
            quadrantes(f)
    if _DESCONHECIDOS:
        erros.append(f"colisoes sem classe nem permissao: {sorted(_DESCONHECIDOS)}")
    return erros


# ------------------------------------------------------------------- execucao

def forca_warps(nome, l, dados, pal):
    """Poe o metatile de porta EMBAIXO de cada warp que cairia em tile mudo.

    Por que isto e legitimo e nao gambiarra: no gen 2 o warp dispara em qualquer
    casa, o evento e que manda; no gen 3 o motor exige comportamento de porta,
    escada ou seta (`IsWarpMetatileBehavior`). Entao a fonte tem warp honesto em
    cima de FLOOR e de CAVE, e traduzir isso ao pe da letra deixa 170 portas
    mudas, entre elas as 16 do MistraltonGym2F. O warp NAO se move: so o
    metatile debaixo dele muda.

    Nao ha risco de laco de warp na chegada: `TryStartStepBasedScript` so e
    chamado quando o jogador DA UM PASSO (src/field_control_avatar.c), nunca ao
    carregar o mapa.
    """
    d = le_map_json(nome)
    if not d:
        return dados, 0
    beh = comportamentos(l)
    w, h = l["width"], l["height"]
    saida, n = bytearray(dados), 0
    for wp in d.get("warp_events") or []:
        x, y = wp.get("x", 0), wp.get("y", 0)
        if not (0 <= x < w and 0 <= y < h):
            continue
        off = (y * w + x) * 2
        v = struct.unpack_from("<H", saida, off)[0]
        if beh(v & 0x3FF) in COMPORTA_WARP:
            continue
        struct.pack_into("<H", saida, off, celula("porta", pal))
        n += 1
    return bytes(saida), n


def gera(so=None, forcar=True, arte=False):
    """{nome: bytes do map.bin novo}, mais o border, os pulados, o uso por classe
    e {nome: rotulo do tileset novo} para os mapas que sairam com arte propria."""
    itens, pulados = mapas_unova()
    atrib = iu.le_conexoes()
    # `arte` liga a MIGRACAO de mapas novos. Mapa cujo layout JA aponta para o
    # tileset proprio sai com arte sempre: reconverte-lo pela tabela de classes
    # gravaria metatile do tileset emprestado num layout que nao o carrega mais.
    ja = arte_disponivel()
    saida, bordas, uso_classe, novos_ts = {}, {}, {}, {}
    forcados = 0
    for nome, l, tset, camel, arq, w, h, amb in itens:
        if so and nome != so:
            continue
        arq_col = tset + "_collision.asm"
        if not os.path.exists(os.path.join(BW3G, "data/tilesets", arq_col)):
            pulados.append((nome, f"{arq_col} nao existe na fonte"))
            continue
        tabqd = quadrantes(arq_col)
        crus = open(arq, "rb").read()
        if len(crus) != w * h:
            crus = (crus + bytes(w * h))[:w * h]   # mesma regra do importador
        if tset in ja and (arte or l["secondary_tileset"] == ja[tset]):
            ts = _tileset_convertido(tset)
            dados, n = converte_arte(crus, w, h, tabqd, ts,
                                     warps_do_mapa(nome, l) if forcar else (), amb)
            forcados += n
            bordas[nome] = converte_arte(bytes([atrib.get(camel, {}).get("borda", 0)]),
                                         1, 1, tabqd, ts, (), amb)[0]
            novos_ts[nome] = ja[tset]
        else:
            pal = PALETA_DO_PAR[(l["primary_tileset"], l["secondary_tileset"])]
            dados = converte(crus, w, h, tabqd, pal)
            if forcar:
                dados, n = forca_warps(nome, l, dados, pal)
                forcados += n
            bordas[nome] = converte(bytes([atrib.get(camel, {}).get("borda", 0)]),
                                    1, 1, tabqd, pal)
        saida[nome] = dados
        for quad in tabqd.values():
            for c in quad:
                uso_classe[c] = uso_classe.get(c, 0) + 1
    uso_classe["(warps com porta forcada)"] = forcados
    return saida, bordas, pulados, uso_classe, novos_ts


def grava(saida, bordas):
    mudados = 0
    for nome, dados in saida.items():
        for arquivo, novo in (("map.bin", dados), ("border.bin", bordas[nome])):
            p = f"{RAIZ}/data/layouts/{nome}/{arquivo}"
            atual = open(p, "rb").read() if os.path.exists(p) else None
            # guarda-corpo: se o tamanho mudasse, a dimensao do layout teria
            # mudado, e ai warp, NPC e placa sairiam todos do lugar. Nenhum
            # arquivo pode trocar de tamanho neste bloco.
            if atual is not None and len(atual) != len(novo):
                raise SystemExit(f"{p}: {len(atual)} -> {len(novo)} bytes. "
                                 f"Isso deslocaria o mapa inteiro; abortado.")
            if atual == novo:
                continue
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "wb").write(novo)
            mudados += 1
    return mudados


def demo():
    erros = confere_tabela()
    assert not erros, "tabela reprovada:\n  " + "\n  ".join(erros)

    # o casamento de dimensao que o PRD cita, conferido de novo aqui
    itens, pulados = mapas_unova()
    assert len(itens) >= 280, f"so {len(itens)} mapas casaram, esperava ~291"
    asp = next(i for i in itens if i[0] == "Unova_AspertiaCity")
    assert os.path.getsize(asp[4]) == asp[5] * asp[6] == 308, "AspertiaCity mudou de tamanho"
    assert (asp[1]["width"], asp[1]["height"]) == (28, 44)

    com_arte = arte_disponivel()
    saida, bordas, _, _, novos = gera(so="Unova_AspertiaCity")
    dados = saida["Unova_AspertiaCity"]
    assert len(dados) == 28 * 44 * 2, "map.bin com tamanho errado"
    assert len(bordas["Unova_AspertiaCity"]) == 2 * 2 * 2, "border.bin com tamanho errado"
    # idempotente: mesma entrada, mesma saida
    assert gera(so="Unova_AspertiaCity")[0]["Unova_AspertiaCity"] == dados

    m = mede_mapa("Unova_AspertiaCity", dict(asp[1], **(
        {"secondary_tileset": novos["Unova_AspertiaCity"]} if novos else {})), dados)
    if asp[2] in com_arte:
        # com tileset proprio (B12.a) o mesmo `.ablk` tem que render dezenas de
        # metatiles, nao um punhado de classes.
        assert m["distintos"] >= 20, f"Aspertia com arte e so {m['distintos']} distintos"
    else:
        # Aspertia e cidade: a fonte so usa WALL, FLOOR, WATER, DOOR, UP_WALL e
        # STAIRS, entao 4 metatiles distintos AQUI e o teto honesto, nao pobreza.
        assert m["distintos"] == 4, f"Aspertia com {m['distintos']} metatiles distintos"
    assert not m["warps_mortos"], f"warp morto em Aspertia: {m['warps_mortos']}"

    # um mapa rico, para provar que grama, agua, ledge e cachoeira chegam mesmo
    rico = next(i for i in itens if i[0] == "Unova_GiantChasmB1F")
    dr, _b, _p, _u, nr = gera(so=rico[0])
    lr = dict(rico[1], **({"secondary_tileset": nr[rico[0]]} if nr else {}))
    mr = mede_mapa(rico[0], lr, dr[rico[0]])
    assert mr["grama"] > 0, "GiantChasmB1F sem grama alta"
    assert mr["distintos"] >= 8, f"GiantChasmB1F com {mr['distintos']} distintos"

    # e uma caverna de verdade tem que ficar com piso que dispara encontro
    cav = next(i for i in itens if i[0] == "Unova_ChargestoneCave1F")
    dc, _b, _p, _u, nc = gera(so=cav[0])
    lc = dict(cav[1], **({"secondary_tileset": nc[cav[0]]} if nc else {}))
    mc = mede_mapa(cav[0], lc, dc[cav[0]])
    assert mc["encontro_terra"] > 0, "caverna sem tile de encontro andavel"

    # MUTACAO na tabela emprestada: se ela errar a porta, a conferencia (c) TEM
    # que acusar. Sem isto, "nenhum warp morto" e so uma frase. Roda no primeiro
    # mapa de exterior que AINDA nao tem arte propria (o B12.a vai esvaziando
    # esta lista; quando ela zerar, a tabela emprestada virou codigo morto).
    alvo = next((i for i in itens if i[2] not in com_arte
                 and PALETA_DO_PAR.get((i[1]["primary_tileset"],
                                        i[1]["secondary_tileset"])) == "exterior"
                 and (le_map_json(i[0]) or {}).get("warp_events")), None)
    if alvo:
        guarda = PALETA["exterior"]["porta"]
        try:
            PALETA["exterior"]["porta"] = (1, 0, 3, "MUTACAO: chao no lugar da porta")
            ruim = gera(so=alvo[0])[0][alvo[0]]
            assert mede_mapa(alvo[0], alvo[1], ruim)["warps_mortos"], \
                f"a mutacao passou pela conferencia (c) em {alvo[0]}: ela nao serve"
        finally:
            PALETA["exterior"]["porta"] = guarda
    # e a tabela mutada tambem tem que reprovar na conferencia estatica
    try:
        PALETA["caverna"]["grama"] = (753, 1, 0, "MUTACAO: parede no lugar da grama")
        assert confere_tabela(), "a mutacao passou pela conferencia da tabela"
    finally:
        PALETA["caverna"]["grama"] = (13, *ANDA, "MB_TALL_GRASS do primario, compartilhado")

    # MUTACAO na arte propria: apagar a variante de porta do tileset TEM que
    # matar warp em algum mapa. E a mesma prova, na camada nova.
    if com_arte:
        alvo = next((i for i in itens if i[2] in com_arte
                     and _tileset_convertido(i[2])["porta2mt"]
                     and (le_map_json(i[0]) or {}).get("warp_events")), None)
        if alvo:
            ts = _tileset_convertido(alvo[2])
            guarda = dict(ts["porta2mt"])
            try:
                ts["porta2mt"].clear()
                ruim = gera(so=alvo[0], arte=True)[0][alvo[0]]
                l2 = dict(alvo[1], secondary_tileset=com_arte[alvo[2]])
                assert mede_mapa(alvo[0], l2, ruim)["warps_mortos"], \
                    f"apagar a variante de porta nao matou warp em {alvo[0]}"
            finally:
                ts["porta2mt"].update(guarda)

    print(f"demo ok: tabela conferida, {len(itens)} mapas casam com o .ablk, "
          f"{len(pulados)} pulados, {len(com_arte)} tilesets com arte propria na "
          f"build, mutacao detectada em todas as conferencias")


def main():
    if "--demo" in sys.argv:
        return demo()
    if "--medir" in sys.argv:
        imprime(medicao(), "ROM de hoje")
        return 0
    so = None
    if "--mapa" in sys.argv:
        so = sys.argv[sys.argv.index("--mapa") + 1]
    erros = confere_tabela()
    if erros:
        print("tabela reprovada:")
        for e in erros:
            print("  -", e)
        return 1
    arte = "--arte-propria" in sys.argv
    if arte:
        i = sys.argv.index("--arte-propria")
        so_ts = [a for a in sys.argv[i + 1:] if not a.startswith("--")]
        if so_ts:
            faltam = [t for t in so_ts if t not in arte_disponivel()]
            if faltam:
                print(f"tileset sem arte propria na build: {faltam}")
                print(f"convertidos e na build hoje: {sorted(arte_disponivel())}")
                return 1
            for t in list(arte_disponivel()):
                if t not in so_ts:
                    del arte_disponivel()[t]
    saida, bordas, pulados, uso, novos = gera(
        so, forcar="--sem-forcar-warp" not in sys.argv, arte=arte)
    antes = medicao()
    depois = medicao(gerados=saida, tilesets_novos=novos)
    imprime(antes, "antes (o que esta na ROM)")
    imprime(depois, "depois (o blockdata novo)" + ("" if not so else f", so {so}"))
    print(f"\nquadrantes da fonte por classe: " + ", ".join(
        f"{k}={v}" for k, v in sorted(uso.items(), key=lambda kv: -kv[1])))
    print(f"mapas convertidos: {len(saida)}; pulados: {len(pulados)}")
    for nome, motivo in pulados:
        print(f"  pulado  {nome}: {motivo}")
    if depois["warps_ruins"]:
        print(f"\nwarps que ainda nao disparam, {len(depois['warps_ruins'])} mapas:")
        for nome, r in sorted(depois["warps_ruins"], key=lambda kv: -len(kv[1]))[:15]:
            print(f"  {len(r):3d}  {nome}: {r[0]}")
    if depois["npcs_presos"]:
        print(f"\nNPCs em tile bloqueado, {len(depois['npcs_presos'])} mapas:")
        for nome, r in sorted(depois["npcs_presos"], key=lambda kv: -len(kv[1]))[:15]:
            print(f"  {len(r):3d}  {nome}: {r[0]}")
    if depois["encontro_sem"]:
        print(f"\nmapas com land_mons e sem tile de encontro andavel: "
              f"{len(depois['encontro_sem'])}")
        for n in depois["encontro_sem"][:15]:
            print("   ", n)
    if novos:
        por_ts = {}
        for nome, rot in novos.items():
            por_ts.setdefault(rot, []).append(nome)
        print(f"\nmapas com tileset proprio: {len(novos)}, em {len(por_ts)} tilesets")
        for rot, ns in sorted(por_ts.items(), key=lambda kv: -len(kv[1])):
            print(f"  {len(ns):3d}  {rot}")
    if "--gravar" in sys.argv:
        print(f"\narquivos gravados: {grava(saida, bordas)}")
        if novos:
            print(f"layouts religados ao tileset novo: {grava_layouts(novos)}")
    else:
        print("\n(nada gravado; use --gravar)")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
