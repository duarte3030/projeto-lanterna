#!/usr/bin/env python3
"""Escreve o JOGO dos sete mapas do subsolo de Goldenrod copiados do GS Chronicles.

A ARTE veio da `copia_cidade.py` (sete mapas, quatro provas em ZERO pixel cada).
Este arquivo escreve o que a ferramenta de cópia NÃO escreve, e diz por quê em
cada linha: warp, objeto, placa e gatilho. Regra do contrato
(`Pokemon Claude/METODO-COPIA-CIDADES.md`, seções 1 e 2): a arte é do autor do
hack, o JOGO é nosso.

O QUE NÃO PODE MUDAR, E POR QUE
-------------------------------
- a ORDEM e os ÍNDICES de `object_events` dos quatro mapas que já existiam: o
  save guarda "objeto N deste mapa já sumiu" por índice. Só se ACRESCENTA no
  fim. Aqui: Storage ganha o objeto 7 e o 8, e mais nada.
- o ID de cada warp que já existia: outros mapas apontam para ele por NÚMERO.
  Os warps só mudam de POSIÇÃO, para a porta equivalente do desenho do autor.
  Warp novo entra no FIM da lista.
- `mapLayoutId`: o layout foi substituído no lugar pela `copia_cidade.py`.

O CASAMENTO, LIDO ABRINDO O DESTINO DE CADA WARP NA ROM DELES
--------------------------------------------------------------
    g9m3  47x10 -> UndergroundEntrance   galeria das três portas da cidade
    g10m5 24x36 -> UndergroundTunnel     corredor de LOJAS com a porta trancada
    g1m52 46x19 -> UndergroundSwitches   1ª sala atrás da porta, com o par interno
    g1m53 31x23 -> UndergroundStorage    2ª sala do depósito
    g1m54 27x23 -> UndergroundWarehouse  3ª sala (mapa NOVO)
    g10m1 55x27 -> Sewers                esgoto (mapa NOVO)
    g10m2 50x50 -> SewersPipes           labirinto de canos (mapa NOVO)

Uso:
    python3 dev_scripts/subsolo_goldenrod.py            # escreve
    python3 dev_scripts/subsolo_goldenrod.py --conferir # só confere, exit 1
"""
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def obj(gfx, x, y, script="0", flag="0", mov="MOVEMENT_TYPE_FACE_DOWN",
        tt="TRAINER_TYPE_NONE", sight="0", rx=0, ry=0, local_id=None):
    d = {}
    if local_id:
        d["local_id"] = local_id
    d.update({
        "graphics_id": gfx, "x": x, "y": y, "elevation": 0,
        "movement_type": mov, "movement_range_x": rx, "movement_range_y": ry,
        "trainer_type": tt, "trainer_sight_or_berry_tree_id": sight,
        "script": script, "flag": flag,
    })
    return d


def treinador(gfx, x, y, script, mov, sight=3, rx=0, ry=0):
    return obj(gfx, x, y, script=script, mov=mov, tt="TRAINER_TYPE_NORMAL",
               sight=str(sight), rx=rx, ry=ry)


def bola(x, y, item, flag):
    return obj("OBJ_EVENT_GFX_ITEM_BALL", x, y, script="Common_EventScript_FindItem",
               flag=flag, mov="MOVEMENT_TYPE_LOOK_AROUND", sight=item)


def warp(x, y, mapa, wid):
    return {"x": x, "y": y, "elevation": 0, "dest_map": mapa, "dest_warp_id": str(wid)}


def placa(x, y, script):
    return {"type": "sign", "x": x, "y": y, "elevation": 0,
            "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY", "script": script}


def escondido(x, y, item, flag):
    return {"type": "hidden_item", "x": x, "y": y, "elevation": 0,
            "item": item, "flag": flag, "quantity": 1, "underfoot": False}


# ---------------------------------------------------------------------------
# GoldenrodCity_UndergroundEntrance  <- g9m3 (47x10)
#
# A galeria do autor são TRÊS alcovas SEPARADAS (medido: três componentes de 59
# células cada, sem passagem a pé entre elas). Cada alcova tem uma escada para a
# cidade embaixo e uma escada para baixo em cima:
#     alcova 1, x 0..10 : (5,8) cidade  e (8,3)  esgoto
#     alcova 2, x 18..28: (23,8) cidade e (26,3) corredor de lojas
#     alcova 3, x 36..46: (41,8) cidade e (44,3) corredor de lojas
# É EXATAMENTE o desenho do autor: os três quiosques da Goldenrod dele, em
# (19,14), (18,40) e (54,43), caem nesta galeria, e as escadas de baixo levam
# duas ao corredor de lojas (nas duas pontas dele) e uma ao esgoto.
# ---------------------------------------------------------------------------
ENTRANCE = {
    "warps": [
        # ids 0 a 3 já existiam e mantêm o DESTINO; só mudaram de posição.
        warp(26, 3, "MAP_GOLDENROD_CITY_UNDERGROUND_TUNNEL", 1),
        warp(44, 3, "MAP_GOLDENROD_CITY_UNDERGROUND_TUNNEL", 0),
        warp(23, 8, "MAP_GOLDENROD_CITY", 2),
        warp(41, 8, "MAP_GOLDENROD_CITY", 15),
        # NOVOS, no fim: o terceiro quiosque e a boca do esgoto.
        warp(5, 8, "MAP_GOLDENROD_CITY", 18),
        warp(8, 3, "MAP_GOLDENROD_CITY_SEWERS", 0),
    ],
    "objetos": [
        # Os dois NPCs que já existiam, nos lugares de NPC do autor.
        obj("OBJ_EVENT_GFX_PICNICKER", 3, 4, script="GoldenrodUnderground_EventScript_Teacher",
            flag="FLAG_HIDE_GOLDENROD_NPCS", mov="MOVEMENT_TYPE_LOOK_AROUND"),
        obj("OBJ_EVENT_GFX_CAMPER", 20, 3, script="GoldenrodUnderground_EventScript_SuperNerd",
            flag="FLAG_HIDE_GOLDENROD_NPCS", mov="MOVEMENT_TYPE_LOOK_AROUND"),
    ],
    "placas": [],
}

# ---------------------------------------------------------------------------
# GoldenrodCity_UndergroundTunnel  <- g10m5 (24x36)
#
# O corredor de lojas. As quatro BANCAS do autor são alcovas de 2 a 4 células
# FECHADAS, com um metatile MB_COUNTER na parede (medido em (9,16), (3,18),
# (9,19), (3,22) e (9,25)): o vendedor fica dentro e o jogador fala por cima do
# balcão. É onde os nossos três NPCs de loja entram.
#
# As duas PERSIANAS de metal, em (22,9) e (16,27), são as portas de serviço do
# autor. A de (22,9) fica FECHADA e é a nossa porta da BASEMENT KEY; a de
# (16,27) fica aberta, porque é a única entrada do terceiro salão do depósito
# (ver scripts.inc).
# ---------------------------------------------------------------------------
TUNNEL = {
    "warps": [
        warp(2, 34, "MAP_GOLDENROD_CITY_UNDERGROUND_ENTRANCE", 1),
        warp(2, 3, "MAP_GOLDENROD_CITY_UNDERGROUND_ENTRANCE", 0),
        warp(22, 9, "MAP_GOLDENROD_CITY_UNDERGROUND_SWITCHES", 1),
        # NOVO: a segunda persiana, que o autor liga ao terceiro salão do depósito.
        warp(16, 27, "MAP_GOLDENROD_CITY_UNDERGROUND_WAREHOUSE", 0),
    ],
    "objetos": [
        treinador("OBJ_EVENT_GFX_SCIENTIST_1", 10, 13,
                  "GoldenrodCity_UndergroundTunnel_EventScript_Issac",
                  "MOVEMENT_TYPE_FACE_LEFT", rx=3),
        obj("OBJ_EVENT_GFX_OLD_WOMAN", 10, 16, script="LavaridgeTown_HerbShop_EventScript_Clerk",
            flag="FLAG_HIDE_GOLDENROD_NPCS", mov="MOVEMENT_TYPE_FACE_LEFT"),
        obj("OBJ_EVENT_GFX_WORKER_M", 2, 18, flag="FLAG_DAY_POKEMON",
            mov="MOVEMENT_TYPE_FACE_RIGHT"),
        obj("OBJ_EVENT_GFX_CLERK", 10, 19, flag="FLAG_NIGHT_POKEMON",
            mov="MOVEMENT_TYPE_FACE_LEFT"),
        treinador("OBJ_EVENT_GFX_SCIENTIST_1", 2, 9,
                  "GoldenrodCity_UndergroundTunnel_EventScript_Teru",
                  "MOVEMENT_TYPE_FACE_RIGHT", rx=3),
        treinador("OBJ_EVENT_GFX_SCIENTIST_1", 7, 33,
                  "GoldenrodCity_UndergroundTunnel_EventScript_Eric",
                  "MOVEMENT_TYPE_FACE_UP", ry=3),
        treinador("OBJ_EVENT_GFX_SCIENTIST_1", 14, 29,
                  "GoldenrodCity_UndergroundTunnel_EventScript_Donald",
                  "MOVEMENT_TYPE_FACE_LEFT", rx=3),
        bola(5, 30, "ITEM_COIN_CASE",
             "FLAG_ITEM_JOHTO_GOLDENRODCITYUNDERGROUNDTUNNEL_COIN_CASE"),
        bola(8, 3, "ITEM_PARALYZE_HEAL",
             "FLAG_ITEM_JOHTO_GOLDENRODCITYUNDERGROUNDTUNNEL_PARALYZE_HEAL"),
        bola(22, 12, "ITEM_ANTIDOTE",
             "FLAG_ITEM_JOHTO_GOLDENRODCITYUNDERGROUNDTUNNEL_ANTIDOTE"),
        bola(8, 35, "ITEM_SUPER_POTION",
             "FLAG_ITEM_JOHTO_GOLDENRODCITYUNDERGROUNDTUNNEL_SUPER_POTION"),
        obj("OBJ_EVENT_GFX_BEAUTY", 5, 11, flag="FLAG_HIDE_GOLDENROD_UNDERGROUND_KIMONO",
            mov="MOVEMENT_TYPE_FACE_LEFT"),
    ],
    # Só a persiana de (22,9) leva placa: ela é a que fica FECHADA e que o
    # roteiro abre com a BASEMENT KEY. A de (16,27) fica aberta, como no mapa do
    # autor, porque é a única entrada do terceiro salão do depósito.
    "placas": [
        placa(22, 9, "GoldenrodCity_UndergroundTunnel_EventScript_Door"),
    ],
}

# ---------------------------------------------------------------------------
# GoldenrodCity_UndergroundSwitches  <- g1m52 (46x19)
#
# O primeiro salão do depósito. Ele tem DUAS metades que não se ligam a pé
# (medido: 261 células a oeste e 38 a leste): quem chega do corredor de lojas
# cai na metade LESTE, em (41,9), e só sai dela pela escada (41,3), que teleporta
# para a escada (27,3) da metade OESTE. Esse par de warps INTERNO é do autor e
# é o quebra-cabeça da sala. Ele entra como warp NOVO, ids 2 e 3.
# Os três painéis do nosso enigma de interruptores vão nos três pilares de
# máquina da fileira do meio, em (6,8), (12,8) e (18,8), que são parede e ficam
# ao lado de chão andável dos dois lados.
# ---------------------------------------------------------------------------
SWITCHES = {
    "warps": [
        warp(26, 13, "MAP_GOLDENROD_CITY_UNDERGROUND_STORAGE", 1),
        warp(41, 9, "MAP_GOLDENROD_CITY_UNDERGROUND_TUNNEL", 2),
        warp(41, 3, "MAP_GOLDENROD_CITY_UNDERGROUND_SWITCHES", 3),
        warp(27, 3, "MAP_GOLDENROD_CITY_UNDERGROUND_SWITCHES", 2),
    ],
    "objetos": [
        treinador("OBJ_EVENT_GFX_ROCKET_M", 19, 8,
                  "GoldenrodCity_UndergroundSwitches_EventScript_Grunt11",
                  "MOVEMENT_TYPE_LOOK_AROUND", rx=4, ry=4),
        treinador("OBJ_EVENT_GFX_ROCKET_M", 16, 3,
                  "GoldenrodCity_UndergroundSwitches_EventScript_Grunt20",
                  "MOVEMENT_TYPE_LOOK_AROUND", rx=4, ry=4),
        treinador("OBJ_EVENT_GFX_ROCKET_M", 3, 3,
                  "GoldenrodCity_UndergroundSwitches_EventScript_Grunt10",
                  "MOVEMENT_TYPE_LOOK_AROUND", rx=4, ry=4),
        treinador("OBJ_EVENT_GFX_BIKER", 5, 10,
                  "GoldenrodCity_UndergroundSwitches_EventScript_Duncan",
                  "MOVEMENT_TYPE_LOOK_AROUND", rx=4, ry=4),
        treinador("OBJ_EVENT_GFX_BIKER", 7, 14,
                  "GoldenrodCity_UndergroundSwitches_EventScript_Eddie",
                  "MOVEMENT_TYPE_LOOK_AROUND", sight=4, rx=4, ry=1),
        treinador("OBJ_EVENT_GFX_ROCKET_M", 24, 14,
                  "GoldenrodCity_UndergroundSwitches_EventScript_Grunt27",
                  "MOVEMENT_TYPE_FACE_DOWN", rx=1, ry=1),
        treinador("OBJ_EVENT_GFX_RED", 20, 4,
                  "GoldenrodCity_UndergroundSwitches_EventScript_Silver",
                  "MOVEMENT_TYPE_FACE_UP"),
        bola(7, 3, "ITEM_MAX_REVIVE",
             "FLAG_ITEM_JOHTO_GOLDENRODCITYUNDERGROUNDSWITCHES_MAX_REVIVE"),
        bola(1, 14, "ITEM_MAX_POTION",
             "FLAG_ITEM_JOHTO_GOLDENRODCITYUNDERGROUNDSWITCHES_MAX_POTION"),
        bola(21, 4, "ITEM_SMOKE_BALL",
             "FLAG_ITEM_JOHTO_GOLDENRODCITYUNDERGROUNDSWITCHES_SMOKE_BALL"),
    ],
    "placas": [
        placa(6, 8, "GoldenrodCity_UndergroundSwitches_EventScript_Panel1"),
        placa(12, 8, "GoldenrodCity_UndergroundSwitches_EventScript_Panel2"),
        placa(18, 8, "GoldenrodCity_UndergroundSwitches_EventScript_Panel3"),
    ],
}
# O objeto 6 (Silver) tem local_id nomeado; o `escreve` repõe.
SWITCHES["objetos"][6]["local_id"] = "LOCALID_GOLDENROD_CITY_UNDERGROUND_SWITCHES_SILVER"

# ---------------------------------------------------------------------------
# GoldenrodCity_UndergroundStorage  <- g1m53 (31x23)
#
# O segundo salão, um labirinto de prateleiras. A escada (28,4) é a que o autor
# usa para o terceiro salão; aqui ela é a nossa subida para o porão da loja de
# departamentos, e a razão está MEDIDA: no mapa do autor, o outro lado dessa
# escada (a célula (24,2) do g1m54) cai num bolso de OITO células sem saída, e a
# metade útil do terceiro salão é outra. Ou seja, o par de portas que perdemos
# não levava a lugar nenhum nem no jogo dele.
# O objeto 7 (quarto treinador) e o 8 (sétima bola) são ACRÉSCIMOS no FIM.
# ---------------------------------------------------------------------------
STORAGE = {
    "warps": [
        warp(28, 4, "MAP_GOLDENROD_CITY_DEPARTMENT_STORE_BASEMENT", 0),
        warp(3, 17, "MAP_GOLDENROD_CITY_UNDERGROUND_SWITCHES", 0),
    ],
    "objetos": [
        bola(8, 6, "ITEM_ULTRA_BALL",
             "FLAG_ITEM_JOHTO_GOLDENRODCITYUNDERGROUNDSTORAGE_ULTRA_BALL"),
        bola(12, 11, "ITEM_MAX_ETHER",
             "FLAG_ITEM_JOHTO_GOLDENRODCITYUNDERGROUNDSTORAGE_MAX_ETHER"),
        bola(20, 4, "ITEM_TM_CALM_MIND",
             "FLAG_ITEM_JOHTO_GOLDENRODCITYUNDERGROUNDSTORAGE_TM_CALM_MIND"),
        treinador("OBJ_EVENT_GFX_ROCKET_M", 11, 4,
                  "GoldenrodCity_UndergroundStorage_EventScript_Grunt12",
                  "MOVEMENT_TYPE_FACE_UP_AND_LEFT", rx=4, ry=4),
        treinador("OBJ_EVENT_GFX_ROCKET_M", 24, 5,
                  "GoldenrodCity_UndergroundStorage_EventScript_Grunt19",
                  "MOVEMENT_TYPE_FACE_DOWN_AND_RIGHT", rx=4, ry=4),
        treinador("OBJ_EVENT_GFX_ROCKET_M", 26, 14,
                  "GoldenrodCity_UndergroundStorage_EventScript_Eto",
                  "MOVEMENT_TYPE_FACE_UP", sight=2, rx=2, ry=2),
        obj("OBJ_EVENT_GFX_GENTLEMAN", 25, 6, flag="FLAG_HIDE_GOLDENROD_ROCKETS",
            mov="MOVEMENT_TYPE_FACE_DOWN_AND_RIGHT"),
        # ACRÉSCIMOS no fim (índices 7 e 8):
        treinador("OBJ_EVENT_GFX_ROCKET_F", 20, 12,
                  "GoldenrodCity_UndergroundStorage_EventScript_Grunt28",
                  "MOVEMENT_TYPE_FACE_LEFT", rx=3),
        bola(28, 22, "ITEM_MAX_ELIXIR",
             "FLAG_ITEM_JOHTO_GOLDENRODCITYUNDERGROUNDSTORAGE_MAX_ELIXIR"),
    ],
    "placas": [],
}

# ---------------------------------------------------------------------------
# GoldenrodCity_UndergroundWarehouse  <- g1m54 (27x23), MAPA NOVO
#
# O terceiro salão. O mapa do autor está INACABADO: das 270 células andáveis, só
# 123 se ligam à porta (17,5), que é a única que o jogo dele usa de verdade; os
# seis objetos que ele pôs caem TODOS fora dessa parte (dois deles com x = 28 e
# 29 num mapa de 27 de largura, ou seja, fora do mapa). Então a arte vem inteira,
# byte a byte, e os nossos objetos vão na parte que o jogador alcança.
# ---------------------------------------------------------------------------
WAREHOUSE = {
    "warps": [
        warp(17, 5, "MAP_GOLDENROD_CITY_UNDERGROUND_TUNNEL", 3),
    ],
    "objetos": [
        treinador("OBJ_EVENT_GFX_ROCKET_M", 5, 11,
                  "GoldenrodCity_UndergroundWarehouse_EventScript_Grunt29",
                  "MOVEMENT_TYPE_FACE_RIGHT", rx=3),
        treinador("OBJ_EVENT_GFX_ROCKET_F", 14, 15,
                  "GoldenrodCity_UndergroundWarehouse_EventScript_Grunt30",
                  "MOVEMENT_TYPE_FACE_UP", ry=3),
        bola(25, 9, "ITEM_STAR_PIECE",
             "FLAG_ITEM_JOHTO_GOLDENRODCITYUNDERGROUNDWAREHOUSE_STAR_PIECE"),
    ],
    "placas": [],
}

# ---------------------------------------------------------------------------
# GoldenrodCity_Sewers  <- g10m1 (55x27), MAPA NOVO
#
# A boca do esgoto. Duas passarelas sobre a água, ligadas por uma ponte central.
# A escada (9,9) sobe para a alcova 1 da galeria; o bueiro (51,22) desce para o
# labirinto de canos.
# ---------------------------------------------------------------------------
SEWERS = {
    "warps": [
        warp(9, 9, "MAP_GOLDENROD_CITY_UNDERGROUND_ENTRANCE", 5),
        warp(51, 22, "MAP_GOLDENROD_CITY_SEWERS_PIPES", 0),
    ],
    "objetos": [
        obj("OBJ_EVENT_GFX_WORKER_F", 12, 9, script="GoldenrodCity_Sewers_EventScript_Janitor",
            mov="MOVEMENT_TYPE_FACE_DOWN"),
        treinador("OBJ_EVENT_GFX_FISHERMAN", 21, 13,
                  "GoldenrodCity_Sewers_EventScript_Gordon",
                  "MOVEMENT_TYPE_FACE_RIGHT", rx=4),
        treinador("OBJ_EVENT_GFX_WORKER_M", 47, 22,
                  "GoldenrodCity_Sewers_EventScript_Brent",
                  "MOVEMENT_TYPE_FACE_LEFT", rx=4),
        bola(8, 21, "ITEM_MAX_REPEL", "FLAG_ITEM_JOHTO_GOLDENRODCITYSEWERS_MAX_REPEL"),
        bola(36, 11, "ITEM_NUGGET", "FLAG_ITEM_JOHTO_GOLDENRODCITYSEWERS_NUGGET"),
        bola(39, 20, "ITEM_FULL_HEAL", "FLAG_ITEM_JOHTO_GOLDENRODCITYSEWERS_FULL_HEAL"),
    ],
    "placas": [],
}

# ---------------------------------------------------------------------------
# GoldenrodCity_SewersPipes  <- g10m2 (50x50), MAPA NOVO
#
# O quebra-cabeça de verdade. CINCO ilhas que não se ligam a pé, e NOVE bueiros:
# um sobe para o esgoto e os outros oito formam QUATRO pares que ligam ilha a
# ilha. Medido, a corrente é ilha 0 -> 4 -> 2 -> 1 -> 3, e a recompensa está na
# última. Os oito pares são do autor, byte a byte, incluindo os quatro itens
# escondidos, um por ilha das quatro primeiras.
# ---------------------------------------------------------------------------
PIPES = {
    "warps": [
        warp(8, 3, "MAP_GOLDENROD_CITY_SEWERS", 1),
        warp(1, 15, "MAP_GOLDENROD_CITY_SEWERS_PIPES", 5),
        warp(21, 21, "MAP_GOLDENROD_CITY_SEWERS_PIPES", 7),
        warp(26, 40, "MAP_GOLDENROD_CITY_SEWERS_PIPES", 4),
        warp(35, 32, "MAP_GOLDENROD_CITY_SEWERS_PIPES", 3),
        warp(28, 29, "MAP_GOLDENROD_CITY_SEWERS_PIPES", 1),
        warp(7, 45, "MAP_GOLDENROD_CITY_SEWERS_PIPES", 8),
        warp(29, 40, "MAP_GOLDENROD_CITY_SEWERS_PIPES", 2),
        warp(48, 29, "MAP_GOLDENROD_CITY_SEWERS_PIPES", 6),
    ],
    "objetos": [
        treinador("OBJ_EVENT_GFX_SCIENTIST_2", 44, 4,
                  "GoldenrodCity_SewersPipes_EventScript_Klaus",
                  "MOVEMENT_TYPE_FACE_LEFT", rx=3),
        treinador("OBJ_EVENT_GFX_LASS_FRLG", 2, 24,
                  "GoldenrodCity_SewersPipes_EventScript_Marnie",
                  "MOVEMENT_TYPE_FACE_RIGHT", rx=3),
        treinador("OBJ_EVENT_GFX_MANIAC", 29, 27,
                  "GoldenrodCity_SewersPipes_EventScript_Hugh",
                  "MOVEMENT_TYPE_FACE_DOWN", ry=3),
        treinador("OBJ_EVENT_GFX_BEAUTY_FRLG", 31, 39,
                  "GoldenrodCity_SewersPipes_EventScript_Dagmar",
                  "MOVEMENT_TYPE_FACE_RIGHT", rx=3),
        treinador("OBJ_EVENT_GFX_HIKER_FRLG", 18, 22,
                  "GoldenrodCity_SewersPipes_EventScript_Rufus",
                  "MOVEMENT_TYPE_FACE_LEFT", rx=3),
        treinador("OBJ_EVENT_GFX_SAILOR_FRLG", 38, 40,
                  "GoldenrodCity_SewersPipes_EventScript_Thomas",
                  "MOVEMENT_TYPE_FACE_UP", ry=3),
        treinador("OBJ_EVENT_GFX_PSYCHIC_M", 34, 30,
                  "GoldenrodCity_SewersPipes_EventScript_Yuki",
                  "MOVEMENT_TYPE_FACE_LEFT", rx=3),
        obj("OBJ_EVENT_GFX_MAN_3", 11, 38, script="GoldenrodCity_SewersPipes_EventScript_LostMan",
            mov="MOVEMENT_TYPE_FACE_DOWN"),
        bola(9, 41, "ITEM_RARE_CANDY", "FLAG_ITEM_JOHTO_GOLDENRODCITYSEWERSPIPES_RARE_CANDY"),
    ],
    "placas": [
        escondido(29, 8, "ITEM_REVIVE", "FLAG_ITEM_JOHTO_GOLDENRODCITYSEWERSPIPES_REVIVE"),
        escondido(7, 16, "ITEM_ELIXIR", "FLAG_ITEM_JOHTO_GOLDENRODCITYSEWERSPIPES_ELIXIR"),
        escondido(31, 31, "ITEM_MAX_ETHER", "FLAG_ITEM_JOHTO_GOLDENRODCITYSEWERSPIPES_MAX_ETHER"),
        escondido(48, 47, "ITEM_PP_UP", "FLAG_ITEM_JOHTO_GOLDENRODCITYSEWERSPIPES_PP_UP"),
    ],
}

MAPAS = [
    ("GoldenrodCity_UndergroundEntrance", ENTRANCE),
    ("GoldenrodCity_UndergroundTunnel", TUNNEL),
    ("GoldenrodCity_UndergroundSwitches", SWITCHES),
    ("GoldenrodCity_UndergroundStorage", STORAGE),
    ("GoldenrodCity_UndergroundWarehouse", WAREHOUSE),
    ("GoldenrodCity_Sewers", SEWERS),
    ("GoldenrodCity_SewersPipes", PIPES),
]


def escreve(so_conferir=False):
    difs = 0
    for nome, plano in MAPAS:
        caminho = os.path.join(REPO, "data/maps", nome, "map.json")
        mj = json.load(open(caminho, encoding="utf-8"))
        novo = dict(mj)
        novo["warp_events"] = plano["warps"]
        novo["object_events"] = plano["objetos"]
        novo["bg_events"] = plano["placas"]
        if novo == mj:
            continue
        difs += 1
        if so_conferir:
            print("DIFERENTE: %s" % nome)
            continue
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(novo, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print("escrito: %-40s %2d warps, %2d objetos, %2d placas"
              % (nome, len(plano["warps"]), len(plano["objetos"]), len(plano["placas"])))

    # A GoldenrodCity abre o TERCEIRO QUIOSQUE em (54,43): a placa
    # `Common_EventScript_PortaFechada` que a onda da cidade deixou ali sai, e
    # entra um warp NOVO, id 18, no FIM da lista.
    caminho = os.path.join(REPO, "data/maps/GoldenrodCity/map.json")
    cj = json.load(open(caminho, encoding="utf-8"))
    quer_warp = warp(54, 43, "MAP_GOLDENROD_CITY_UNDERGROUND_ENTRANCE", 4)
    mudou = False
    if quer_warp not in cj["warp_events"]:
        if len(cj["warp_events"]) != 18:
            raise SystemExit("ERRO: a GoldenrodCity tem %d warps, esperava 18; "
                             "alguém mexeu na lista." % len(cj["warp_events"]))
        cj["warp_events"].append(quer_warp)
        mudou = True
    antes = len(cj["bg_events"])
    cj["bg_events"] = [b for b in cj["bg_events"]
                       if not (b["x"] == 54 and b["y"] == 43
                               and b.get("script") == "Common_EventScript_PortaFechada")]
    if len(cj["bg_events"]) != antes:
        mudou = True
    if mudou:
        difs += 1
        if so_conferir:
            print("DIFERENTE: GoldenrodCity")
        else:
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(cj, f, indent=2, ensure_ascii=False)
                f.write("\n")
            print("escrito: GoldenrodCity  warp 18 em (54,43) para a galeria, placa fechada fora")
    return difs


if __name__ == "__main__":
    so_conferir = "--conferir" in sys.argv
    d = escreve(so_conferir)
    if so_conferir and d:
        print("FALTA ESCREVER: %d mapas" % d)
        sys.exit(1)
    if so_conferir:
        print("os sete mapas e a cidade já estão como este arquivo manda")
