#!/usr/bin/env python3
"""Escreve o JOGO NOSSO dentro dos nove mapas da Undersea Cavern copiados do
Liquid Crystal (frente D, onda 2, 11/09/2026).

POR QUE ISTO EXISTE
-------------------
`copia_mapa_rom.py` traz a ARTE com fidelidade de pixel e grava as quatro listas
de evento VAZIAS de propósito (regra 1.2 do METODO-COPIA-CIDADES.md). Quem põe
warp, treinador, item e placa é gente, e são 58 warps e 33 objetos espalhados
por nove mapas: escrever isso à mão no JSON é onde se troca um número e ninguém
vê. Aqui a tabela fica em UM lugar, legível, e o JSON sai dela.

O QUE ELE NÃO FAZ
-----------------
- Não toca em `map.bin`, `border.bin` nem em tileset: a planta é cópia byte a
  byte do hack e mexer nela seria inventar desenho.
- Não escreve `scripts.inc`, texto, encontro selvagem, treinador nem flag. Isso
  é texto de jogo e mora nos arquivos de sempre, escrito à mão.
- Não cria warp em tile que não dispara. Todas as coordenadas abaixo foram
  MEDIDAS: comportamento em `MetatileBehavior_IsWarpDoor`/`IsLadder`/
  `IsArrowWarp` (96 MB_NON_ANIMATED_DOOR, 97 MB_LADDER, 101 MB_SOUTH_ARROW_WARP)
  e colisão 0, que é o par que `dev_scripts/valida_warp_tile.py` exige.

A TOPOLOGIA, e por que ela não é a do hack
------------------------------------------
O hack liga estes nove mapas por 71 warps, mas 13 deles saem para mapas do
enredo do Liquid Crystal (Cianwood, Cinnabar Volcano, Route 100) e 7 estão em
cima de água ou de `MB_FRLG_CAVE`, que no nosso motor NÃO dispara warp nenhum.
Sobram 51 warps de verdade, e eles não fecham: medindo as regiões andáveis mapa
a mapa (busca em largura sobre a colisão), três regiões grandes do Chasm (a
galeria do rio, 466 células; a câmara nordeste, 50; a poça sudeste, 26) só eram
alcançadas por warps que iam para fora. Por isso as três descidas da cachoeira
do Chasm em (61,44), (62,44) e (63,44), que o hack deixou SEM warp, viraram as
portas dessas três regiões, e a escada da Glacier em (5,6) passou a nascer na
Gallery (2,40), outra porta que o hack não usou. Nenhum tile foi desenhado para
isso: as cinco portas já estavam na arte.
"""
import collections
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------------- tabela
# warp: (x, y, mapa de destino, id de warp no destino)
WARPS = {
    "LcUnderseaEntrance": [
        (8, 30, "MAP_LC_UNDERSEA_CAVERN", 0),
    ],
    "LcUnderseaCavern": [
        (10, 4, "MAP_LC_UNDERSEA_ENTRANCE", 0),
        (46, 9, "MAP_LC_UNDERSEA_SPRINGS", 0),
        (49, 30, "MAP_LC_UNDERSEA_DEPTHS", 0),
    ],
    "LcUnderseaSprings": [
        (43, 39, "MAP_LC_UNDERSEA_CAVERN", 1),
        (39, 6, "MAP_LC_UNDERSEA_DEPTHS", 3),
        (31, 4, "MAP_LC_UNDERSEA_DEPTHS", 1),
        (12, 4, "MAP_LC_UNDERSEA_DEPTHS", 2),
        (7, 5, "MAP_LC_UNDERSEA_CHASM", 0),
        (14, 43, "MAP_LC_UNDERSEA_GALLERY", 2),
    ],
    "LcUnderseaDepths": [
        (8, 36, "MAP_LC_UNDERSEA_CAVERN", 2),
        (29, 28, "MAP_LC_UNDERSEA_SPRINGS", 2),
        (6, 28, "MAP_LC_UNDERSEA_SPRINGS", 3),
        (41, 26, "MAP_LC_UNDERSEA_SPRINGS", 1),
        (44, 7, "MAP_LC_UNDERSEA_GALLERY", 0),
        (22, 3, "MAP_LC_UNDERSEA_GALLERY", 1),
        (44, 3, "MAP_LC_UNDERSEA_SHRINE", 0),
        (36, 43, "MAP_LC_UNDERSEA_DEPTHS", 8),
        (10, 77, "MAP_LC_UNDERSEA_DEPTHS", 7),
        (39, 75, "MAP_LC_UNDERSEA_DEPTHS", 10),
        (5, 86, "MAP_LC_UNDERSEA_DEPTHS", 9),
        (45, 88, "MAP_LC_UNDERSEA_DEPTHS", 12),
        (7, 108, "MAP_LC_UNDERSEA_DEPTHS", 11),
        (6, 117, "MAP_LC_UNDERSEA_DEPTHS", 14),
        (31, 93, "MAP_LC_UNDERSEA_DEPTHS", 13),
        (44, 107, "MAP_LC_UNDERSEA_DEPTHS", 16),
        (12, 125, "MAP_LC_UNDERSEA_DEPTHS", 15),
        (34, 100, "MAP_LC_UNDERSEA_SHRINE", 3),
    ],
    "LcUnderseaGallery": [
        (43, 31, "MAP_LC_UNDERSEA_DEPTHS", 4),
        (24, 53, "MAP_LC_UNDERSEA_DEPTHS", 5),
        (42, 2, "MAP_LC_UNDERSEA_SPRINGS", 5),
        (2, 40, "MAP_LC_UNDERSEA_GLACIER", 0),
    ],
    "LcUnderseaShrine": [
        (7, 24, "MAP_LC_UNDERSEA_DEPTHS", 6),
        (9, 3, "MAP_LC_UNDERSEA_SHRINE", 2),
        (35, 20, "MAP_LC_UNDERSEA_SHRINE", 1),
        (35, 9, "MAP_LC_UNDERSEA_DEPTHS", 17),
    ],
    "LcUnderseaChasm": [
        (16, 40, "MAP_LC_UNDERSEA_SPRINGS", 4),
        (39, 1, "MAP_LC_UNDERSEA_CHASM", 2),
        (39, 40, "MAP_LC_UNDERSEA_CHASM", 1),
        (61, 44, "MAP_LC_UNDERSEA_CHASM", 6),
        (62, 44, "MAP_LC_UNDERSEA_CHASM", 7),
        (63, 44, "MAP_LC_UNDERSEA_CHASM", 8),
        (84, 7, "MAP_LC_UNDERSEA_CHASM", 3),
        (99, 12, "MAP_LC_UNDERSEA_CHASM", 4),
        (100, 42, "MAP_LC_UNDERSEA_CHASM", 5),
    ],
    "LcUnderseaGlacier": [
        (5, 6, "MAP_LC_UNDERSEA_GALLERY", 3),
        (8, 7, "MAP_LC_UNDERSEA_GLACIER", 2),
        (4, 21, "MAP_LC_UNDERSEA_GLACIER", 1),
        (4, 19, "MAP_LC_UNDERSEA_GLACIER", 4),
        (25, 7, "MAP_LC_UNDERSEA_GLACIER", 3),
        (22, 5, "MAP_LC_UNDERSEA_GLACIER", 6),
        (41, 20, "MAP_LC_UNDERSEA_GLACIER", 5),
        (38, 21, "MAP_LC_UNDERSEA_GLACIER", 8),
        (22, 19, "MAP_LC_UNDERSEA_GLACIER", 7),
        (24, 20, "MAP_LC_UNDERSEA_GLACIER", 10),
        (38, 5, "MAP_LC_UNDERSEA_GLACIER", 9),
        (38, 7, "MAP_LC_UNDERSEA_ALCOVE", 0),
    ],
    "LcUnderseaAlcove": [
        (9, 7, "MAP_LC_UNDERSEA_GLACIER", 11),
    ],
}

# treinador: (x, y, gfx, direcao, script, id de vista)
TREINADORES = {
    "LcUnderseaCavern": [
        (22, 10, "OBJ_EVENT_GFX_SWIMMER_M_LAND", "DOWN", "Marcus", 4),
        (34, 23, "OBJ_EVENT_GFX_SWIMMER_F_LAND", "LEFT", "Noelle", 4),
    ],
    "LcUnderseaSprings": [
        (29, 9, "OBJ_EVENT_GFX_SAILOR", "UP", "Holt", 4),
        (40, 22, "OBJ_EVENT_GFX_SWIMMER_F_LAND", "UP", "Peri", 3),
    ],
    "LcUnderseaDepths": [
        (20, 19, "OBJ_EVENT_GFX_FISHERMAN", "DOWN", "Odell", 4),
        (14, 39, "OBJ_EVENT_GFX_SWIMMER_M_LAND", "RIGHT", "Tobias", 4),
        (21, 73, "OBJ_EVENT_GFX_SWIMMER_F_LAND", "DOWN", "Ines", 4),
        (15, 90, "OBJ_EVENT_GFX_BLACK_BELT", "UP", "Koa", 4),
    ],
    "LcUnderseaGallery": [
        (20, 47, "OBJ_EVENT_GFX_SWIMMER_M_LAND", "UP", "Drake", 4),
        (8, 23, "OBJ_EVENT_GFX_HIKER", "DOWN", "Gale", 4),
    ],
    "LcUnderseaChasm": [
        (21, 17, "OBJ_EVENT_GFX_SWIMMER_F_LAND", "DOWN", "Orla", 4),
        (40, 28, "OBJ_EVENT_GFX_EXPERT_M", "LEFT", "Sorrel", 4),
    ],
    "LcUnderseaShrine": [
        (13, 16, "OBJ_EVENT_GFX_EXPERT_F", "DOWN", "Maris", 4),
    ],
}

# bola de item: (x, y, ITEM_*, sufixo da flag)
ITENS = {
    "LcUnderseaEntrance": [(11, 10, "ITEM_PEARL", "ENTRANCE_PEARL")],
    "LcUnderseaCavern": [
        (13, 7, "ITEM_BIG_PEARL", "CAVERN_BIG_PEARL"),
        (49, 26, "ITEM_MAX_REPEL", "CAVERN_MAX_REPEL"),
        (31, 14, "ITEM_PEARL", "CAVERN_PEARL"),
    ],
    "LcUnderseaSprings": [
        (9, 27, "ITEM_FULL_RESTORE", "SPRINGS_FULL_RESTORE"),
        (40, 24, "ITEM_WATER_STONE", "SPRINGS_WATER_STONE"),
    ],
    "LcUnderseaDepths": [
        (13, 24, "ITEM_MYSTIC_WATER", "DEPTHS_MYSTIC_WATER"),
        (8, 41, "ITEM_MAX_REVIVE", "DEPTHS_MAX_REVIVE"),
        (29, 74, "ITEM_RARE_CANDY", "DEPTHS_RARE_CANDY"),
        (22, 91, "ITEM_NUGGET", "DEPTHS_NUGGET"),
        (14, 105, "ITEM_HEART_SCALE", "DEPTHS_HEART_SCALE"),
        (46, 120, "ITEM_DEEP_SEA_TOOTH", "DEPTHS_DEEP_SEA_TOOTH"),
        (13, 122, "ITEM_DEEP_SEA_SCALE", "DEPTHS_DEEP_SEA_SCALE"),
        (34, 101, "ITEM_DRAGON_SCALE", "DEPTHS_DRAGON_SCALE"),
    ],
    "LcUnderseaGallery": [
        (16, 48, "ITEM_CALCIUM", "GALLERY_CALCIUM"),
        (35, 39, "ITEM_STARDUST", "GALLERY_STARDUST"),
    ],
    "LcUnderseaChasm": [
        (84, 12, "ITEM_PRISM_SCALE", "CHASM_PRISM_SCALE"),
        (99, 6, "ITEM_STAR_PIECE", "CHASM_STAR_PIECE"),
        (99, 41, "ITEM_MAX_ELIXIR", "CHASM_MAX_ELIXIR"),
    ],
    "LcUnderseaGlacier": [(23, 20, "ITEM_NEVER_MELT_ICE", "GLACIER_NEVER_MELT_ICE")],
    "LcUnderseaAlcove": [(13, 17, "ITEM_STARDUST", "ALCOVE_STARDUST")],
    "LcUnderseaShrine": [(34, 17, "ITEM_SEA_INCENSE", "SHRINE_SEA_INCENSE")],
}

# placa: (x, y, sufixo do script)
PLACAS = {
    "LcUnderseaEntrance": [(12, 8, "TrenchSign")],
    "LcUnderseaCavern": [(20, 9, "EntranceSign")],
    "LcUnderseaSprings": [(18, 15, "SpringsSign")],
    "LcUnderseaDepths": [(28, 23, "DepthsSign"), (23, 88, "DeepSign")],
    "LcUnderseaGallery": [(26, 41, "GallerySign")],
    "LcUnderseaChasm": [(19, 22, "ChasmSign")],
    "LcUnderseaGlacier": [(23, 18, "GlacierSign")],
    "LcUnderseaShrine": [(12, 12, "ShrineSign")],
}

MAPAS = ["LcUnderseaEntrance", "LcUnderseaCavern", "LcUnderseaSprings",
         "LcUnderseaDepths", "LcUnderseaGallery", "LcUnderseaShrine",
         "LcUnderseaChasm", "LcUnderseaGlacier", "LcUnderseaAlcove"]

# id de treinador: a faixa desta frente é 2047 a 2076 (briefing de 11/09/2026).
PRIMEIRO_ID = 2047


def caminho(nome, arq):
    return os.path.join(RAIZ, "data/maps", nome, arq)


def constantes_de_treinador():
    """nome do treinador -> constante, na ordem em que aparecem na tabela."""
    saida = collections.OrderedDict()
    for nome in MAPAS:
        for (_x, _y, _g, _d, pessoa, _v) in TREINADORES.get(nome, []):
            saida[pessoa] = "TRAINER_JOHTO_LC_UNDERSEA_" + pessoa.upper()
    return saida


def monta(nome):
    d = json.load(open(caminho(nome, "map.json"), encoding="utf-8"))
    d["warp_events"] = [
        {"x": x, "y": y, "elevation": 0, "dest_map": dest, "dest_warp_id": str(wid)}
        for (x, y, dest, wid) in WARPS.get(nome, [])
    ]
    objetos = []
    for (x, y, gfx, direcao, pessoa, vista) in TREINADORES.get(nome, []):
        objetos.append({
            "graphics_id": gfx,
            "x": x, "y": y, "elevation": 3,
            "movement_type": "MOVEMENT_TYPE_FACE_" + direcao,
            "movement_range_x": 0, "movement_range_y": 0,
            "trainer_type": "TRAINER_TYPE_NORMAL",
            "trainer_sight_or_berry_tree_id": str(vista),
            "script": "%s_EventScript_%s" % (nome, pessoa),
            "flag": "0",
        })
    for (x, y, item, sufixo) in ITENS.get(nome, []):
        objetos.append({
            "graphics_id": "OBJ_EVENT_GFX_ITEM_BALL",
            "x": x, "y": y, "elevation": 3,
            "movement_type": "MOVEMENT_TYPE_LOOK_AROUND",
            "movement_range_x": 0, "movement_range_y": 0,
            "trainer_type": "TRAINER_TYPE_NONE",
            "trainer_sight_or_berry_tree_id": item,
            "script": "Common_EventScript_FindItem",
            "flag": "FLAG_ITEM_LC_UNDERSEA_" + sufixo,
        })
    d["object_events"] = objetos
    d["bg_events"] = [
        {"type": "sign", "x": x, "y": y, "elevation": 0,
         "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
         "script": "%s_EventScript_%s" % (nome, sufixo)}
        for (x, y, sufixo) in PLACAS.get(nome, [])
    ]
    d["coord_events"] = []
    return d


def main():
    aplicar = "--aplicar" in sys.argv
    total_w = total_o = total_p = 0
    for nome in MAPAS:
        d = monta(nome)
        total_w += len(d["warp_events"])
        total_o += len(d["object_events"])
        total_p += len(d["bg_events"])
        print("%-20s %2d warps  %2d objetos  %d placas"
              % (nome, len(d["warp_events"]), len(d["object_events"]),
                 len(d["bg_events"])))
        if aplicar:
            with open(caminho(nome, "map.json"), "w", encoding="utf-8") as f:
                json.dump(d, f, indent=2, ensure_ascii=False)
                f.write("\n")
    print("TOTAL %d warps, %d objetos, %d placas" % (total_w, total_o, total_p))
    print("\ntreinadores, na ordem dos ids %d em diante:" % PRIMEIRO_ID)
    for i, (pessoa, const) in enumerate(constantes_de_treinador().items()):
        print("   %d  %s  (%s)" % (PRIMEIRO_ID + i, const, pessoa))
    if not aplicar:
        print("\n(ensaio: nada foi escrito; passe --aplicar)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
