#!/usr/bin/env python3
"""Escreve o JOGO das áreas do pacote GS Chronicles (resposta 69 do Gui) por cima
da arte que a `copia_cidade.py` copiou do autor.

A arte é do autor do hack, byte a byte (quatro provas da ferramenta em ZERO). O
JOGO é nosso: warp, objeto, placa, gatilho, item, treinador e texto. Contrato:
`Pokemon Claude/METODO-COPIA-CIDADES.md`, seções 1 e 2.

O QUE NÃO PODE MUDAR, E POR QUE
-------------------------------
- a ORDEM e os ÍNDICES de `object_events` dos mapas que já existiam: a save
  guarda estado de objeto por índice. Só se ACRESCENTA no fim.
- o ID de cada warp que já existia: outros mapas apontam para ele por NÚMERO.
  O warp só muda de POSIÇÃO (e de destino quando o outro lado também mudou).
- `mapLayoutId`: o layout foi substituído no lugar.
- flag nova só por apelido de FLAG_UNUSED (0x218B em diante, dentro da faixa
  0x2181 a 0x21BF que a retomada de 23/09/2026 reservou a este pacote), e id de
  treinador novo só na faixa 2162 a 2181.

AS ÁREAS
--------
1. Ginásio de Violet (`g6m1` térreo + `g6m2` andar de cima). O nosso ginásio
   era um salão só; o do autor é um saguão e, subindo pelo elevador, a
   passarela sobre o vazio com o Falkner no fim. O saguão fica no lugar do
   nosso `VioletCity_Gym` (warp 0 continua sendo a porta da cidade) e o andar
   de cima é o mapa NOVO `VioletCity_Gym_2F`. O Falkner e os dois treinadores
   sobem: no térreo os três objetos antigos continuam na lista (índice é save)
   mas nascem escondidos por FLAG_HIDE_VIOLET_GYM_TERREO, que o ON_TRANSITION
   do saguão acende antes dos objetos aparecerem; no 2F entram três objetos
   NOVOS com os MESMOS roteiros. A flag de "já venci" é do id do treinador, não
   do objeto, então quem já venceu o Falkner continua com a insígnia e com ele
   derrotado. O guia do ginásio fica no saguão, no lugar do NPC do autor.
2. Praça da Torre do Rádio (`g3m66`, mapa NOVO `GoldenrodCity_RadioPlaza`). É
   o anexo oeste da Goldenrod do autor: as quatro setas da borda oeste da
   cidade, em (1,16) a (1,19), levam a ela, e a porta da Torre do Rádio mora
   nela, em (13,14). Até aqui a nossa torre estava ENCAIXADA num prédio da
   Goldenrod em (10,15), porque a praça não existia (ESTADO 0.ah). Agora ela
   volta ao prédio que o autor desenhou para ela: o warp 7 da Goldenrod, que
   era a porta da torre, vira a seta (1,16) da praça; a `RadioTower_1F` sai
   pela praça; a célula (10,15), que era parede lisa no desenho do autor e
   tinha ganhado uma porta encaixada, volta a ser a parede dele; e a placa da
   torre vai junto com ela.
3. Clareira da Rota 36 (`g1m36`, mapa NOVO `Route36_Clearing`). No hack ela
   fica entre a Rota 36 e as Ruínas de Alph. Aqui ela entra no mesmo lugar do
   caminho: a porta sul da guarita `Gate_RuinsOfAlph_Route36` sai na clareira
   e a clareira sai nas Ruínas, na porta que antes recebia a guarita. Nenhum
   pixel da Rota 36 nem das Ruínas muda.
4. Clareira de flores da Rota 42 (`g12m1`, mapa NOVO `Route42_Clearing`). No
   hack ela abre por uma fresta na mata do sul da Rota 42, logo depois da
   guarita de Ecruteak. A nossa Rota 42 é outra planta, e a fresta equivalente
   é a beira sul do bolsão de grama de (12,15) a (15,15). As duas células
   (13,15) e (14,15) ganham o comportamento MB_SOUTH_ARROW_WARP por um CLONE do
   metatile que já estava ali (os mesmos 16 bytes, só o atributo muda), no
   secundário `gTileset_MahoganyTown`: o render da Rota 42 fica com ZERO pixel
   de diferença. É o mesmo truque da guarita da Route 34 (ESTADO 0.ah). Os 13
   itens escondidos são os 13 do autor, nas mesmas células; o conteúdo é nosso.
5. National Park (`g1m38`, no lugar do nosso `NationalPark_Normal`, e o mesmo
   desenho no `NationalPark_BugContest`, como o autor faz: dois cabeçalhos
   sobre um layout). Remapeamento objeto a objeto, pela função: os três
   bancos, as duas lixeiras, as duas placas, a fonte e o canteiro do autor
   recebem os nossos NPCs sentados, lixeiras e placas; os quatro treinadores
   vão para os quatro lugares de treinador do autor; o item escondido da faixa
   oeste vai para a bola do autor em (1,42). O parque do autor não tem poste
   de luz, então os LIGHT_SPRITE (o brilho dos postes à noite) vão para fora
   do mapa, em (-9,-9), como os Pokémon de reserva do concurso já moram.

Uso:
    python3 dev_scripts/pacote_gsc_jogo.py            # escreve
    python3 dev_scripts/pacote_gsc_jogo.py --conferir # só confere, exit 1
"""
import json
import os
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIFS = []
CONFERIR = "--conferir" in sys.argv


def caminho_mapa(nome):
    return os.path.join(REPO, "data/maps", nome, "map.json")


def le(nome):
    return json.load(open(caminho_mapa(nome), encoding="utf-8"))


def grava(nome, mj):
    antigo = le(nome)
    if antigo == mj:
        return
    DIFS.append(nome)
    if CONFERIR:
        print("DIFERENTE: %s" % nome)
        return
    with open(caminho_mapa(nome), "w", encoding="utf-8") as f:
        json.dump(mj, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("escrito: %s" % nome)


def obj(gfx, x, y, script="0", flag="0", mov="MOVEMENT_TYPE_FACE_DOWN",
        tt="TRAINER_TYPE_NONE", sight="0", rx=0, ry=0, local_id=None):
    d = {"graphics_id": gfx, "x": x, "y": y, "elevation": 0,
         "movement_type": mov, "movement_range_x": rx, "movement_range_y": ry,
         "trainer_type": tt, "trainer_sight_or_berry_tree_id": sight,
         "script": script, "flag": flag}
    if local_id:
        d["local_id"] = local_id
    return d


def warp(x, y, mapa, wid):
    return {"x": x, "y": y, "elevation": 0, "dest_map": mapa, "dest_warp_id": str(wid)}


def placa(x, y, script):
    return {"type": "sign", "x": x, "y": y, "elevation": 0,
            "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY", "script": script}


def escondido(x, y, item, flag):
    return {"type": "hidden_item", "x": x, "y": y, "elevation": 0,
            "item": item, "flag": flag, "quantity": 1, "underfoot": False}


def move(o, x, y):
    o["x"], o["y"] = x, y


# ============================================================ 1. Violet Gym


def ginasio_violet():
    t = le("VioletCity_Gym")
    # Os três que sobem para o 2F: continuam na lista, escondidos no térreo.
    for i in (0, 1, 2):
        t["object_events"][i]["flag"] = "FLAG_HIDE_VIOLET_GYM_TERREO"
    move(t["object_events"][0], 6, 2)    # atrás do parapeito, fora do alcance
    move(t["object_events"][1], 3, 2)
    move(t["object_events"][2], 9, 2)
    move(t["object_events"][3], 7, 6)    # guia: no lugar do NPC do autor
    t["warp_events"] = [
        warp(6, 9, "MAP_VIOLET_CITY", 7),               # 0: porta, destino de sempre
        warp(6, 6, "MAP_VIOLET_CITY_GYM_2F", 0),        # 1: NOVO, elevador
    ]
    t["bg_events"] = [placa(3, 8, "VioletCity_Gym_EventScript_Statue"),
                      placa(9, 8, "VioletCity_Gym_EventScript_Statue")]
    grava("VioletCity_Gym", t)

    s = le("VioletCity_Gym_2F")
    s["warp_events"] = [warp(6, 18, "MAP_VIOLET_CITY_GYM", 1)]
    s["object_events"] = [
        obj("OBJ_EVENT_GFX_WINONA", 6, 5, script="VioletCity_Gym_EventScript_Falkner",
            local_id="LOCALID_VIOLET_CITY_GYM_2F_FALKNER"),
        # Mesmos lugares e mesma visão (2) dos dois treinadores do autor: o
        # primeiro olha para OESTE e o segundo para LESTE, e a passarela em
        # zigue-zague passa na frente dos dois.
        obj("OBJ_EVENT_GFX_CAMPER", 8, 10, script="VioletCity_Gym_EventScript_Abe",
            mov="MOVEMENT_TYPE_FACE_LEFT", tt="TRAINER_TYPE_NORMAL", sight="2"),
        obj("OBJ_EVENT_GFX_CAMPER", 4, 14, script="VioletCity_Gym_EventScript_Rod",
            mov="MOVEMENT_TYPE_FACE_RIGHT", tt="TRAINER_TYPE_NORMAL", sight="2"),
    ]
    s["bg_events"] = []
    grava("VioletCity_Gym_2F", s)


# ============================================================ 2. Praça da torre


def praca_da_torre():
    p = le("GoldenrodCity_RadioPlaza")
    p["warp_events"] = [
        warp(26, 16, "MAP_GOLDENROD_CITY", 7),
        warp(26, 17, "MAP_GOLDENROD_CITY", 19),
        warp(26, 18, "MAP_GOLDENROD_CITY", 20),
        warp(26, 19, "MAP_GOLDENROD_CITY", 21),
        warp(13, 14, "MAP_GOLDENROD_CITY_RADIO_TOWER_1F", 0),
    ]
    p["object_events"] = [
        obj("OBJ_EVENT_GFX_OLD_MAN", 6, 14, script="GoldenrodCity_RadioPlaza_EventScript_OldMan"),
        obj("OBJ_EVENT_GFX_ITEM_BALL", 17, 14, script="Common_EventScript_FindItem",
            flag="FLAG_ITEM_JOHTO_GOLDENRODCITYRADIOPLAZA_ETHER",
            mov="MOVEMENT_TYPE_LOOK_AROUND", sight="ITEM_ETHER"),
        obj("OBJ_EVENT_GFX_LASS", 9, 17, script="GoldenrodCity_RadioPlaza_EventScript_Lass",
            mov="MOVEMENT_TYPE_WANDER_AROUND", rx=2, ry=1),
    ]
    p["bg_events"] = [placa(16, 15, "GoldenrodCity_EventScript_SignRadio"),
                      placa(8, 19, "EventScript_EmptyTrashCan")]
    grava("GoldenrodCity_RadioPlaza", p)

    g = le("GoldenrodCity")
    ws = g["warp_events"]
    if len(ws) not in (19, 22):
        raise SystemExit("ERRO: a GoldenrodCity tem %d warps; esperava 19 (antes) ou 22" % len(ws))
    ws[7] = warp(1, 16, "MAP_GOLDENROD_CITY_RADIO_PLAZA", 0)
    novos = [warp(1, 17, "MAP_GOLDENROD_CITY_RADIO_PLAZA", 1),
             warp(1, 18, "MAP_GOLDENROD_CITY_RADIO_PLAZA", 2),
             warp(1, 19, "MAP_GOLDENROD_CITY_RADIO_PLAZA", 3)]
    g["warp_events"] = ws[:19] + novos
    bg = [b for b in g["bg_events"]
          if not (b["x"] == 1 and b["y"] == 17)            # a placa closed da estrada oeste
          and b.get("script") != "GoldenrodCity_EventScript_SignRadio"]
    g["bg_events"] = bg
    grava("GoldenrodCity", g)

    # A porta da torre em (10,15) tinha sido ENCAIXADA pela onda da cidade numa
    # célula que no desenho do autor é parede lisa (metatile 194, a porta das
    # casinhas dele, com colisão 0). Com a torre de volta ao prédio do autor, a
    # célula volta a ser o que o autor desenhou: o metatile 196 com colisão 1,
    # conferido contra uma cópia nova e crua do `g3m5`, que difere do repo só
    # nesta célula e nas duas outras portas encaixadas (Game Corner e casa 3).
    L = next(x for x in json.load(open(os.path.join(REPO, "data/layouts/layouts.json")))["layouts"]
             if x.get("id") == "LAYOUT_GOLDENROD_CITY")
    cam = os.path.join(REPO, L["blockdata_filepath"])
    mapa = bytearray(open(cam, "rb").read())
    i = 2 * (15 * L["width"] + 10)
    quer = 196 | (1 << 10)
    if struct.unpack_from("<H", mapa, i)[0] != quer:
        if struct.unpack_from("<H", mapa, i)[0] & 0x3FF not in (194, 196):
            raise SystemExit("ERRO: (10,15) da Goldenrod não é mais a porta encaixada")
        DIFS.append("GoldenrodCity (10,15)")
        if CONFERIR:
            print("DIFERENTE: (10,15) da Goldenrod")
        else:
            struct.pack_into("<H", mapa, i, quer)
            open(cam, "wb").write(mapa)
            print("escrito: (10,15) da Goldenrod volta à parede do autor")

    r = le("GoldenrodCity_RadioTower_1F")
    r["warp_events"][0] = warp(9, 10, "MAP_GOLDENROD_CITY_RADIO_PLAZA", 4)
    grava("GoldenrodCity_RadioTower_1F", r)


# ============================================================ 3. Clareira 36


def clareira_36():
    c = le("Route36_Clearing")
    c["warp_events"] = [
        warp(2, 2, "MAP_GATE_RUINS_OF_ALPH_ROUTE36", 1),
        warp(3, 2, "MAP_GATE_RUINS_OF_ALPH_ROUTE36", 1),
        warp(17, 21, "MAP_RUINS_OF_ALPH_OUTSIDE", 1),
        warp(18, 21, "MAP_RUINS_OF_ALPH_OUTSIDE", 1),
    ]
    c["object_events"] = [
        obj("OBJ_EVENT_GFX_BUG_CATCHER", 7, 7, script="Route36_Clearing_EventScript_Wade",
            mov="MOVEMENT_TYPE_FACE_DOWN", tt="TRAINER_TYPE_NORMAL", sight="4"),
        obj("OBJ_EVENT_GFX_ITEM_BALL", 16, 2, script="Common_EventScript_FindItem",
            flag="FLAG_ITEM_JOHTO_ROUTE36CLEARING_MIRACLE_SEED",
            mov="MOVEMENT_TYPE_LOOK_AROUND", sight="ITEM_MIRACLE_SEED"),
        obj("OBJ_EVENT_GFX_ITEM_BALL", 6, 17, script="Common_EventScript_FindItem",
            flag="FLAG_ITEM_JOHTO_ROUTE36CLEARING_SUPER_REPEL",
            mov="MOVEMENT_TYPE_LOOK_AROUND", sight="ITEM_SUPER_REPEL"),
    ]
    c["bg_events"] = []
    grava("Route36_Clearing", c)

    gt = le("Gate_RuinsOfAlph_Route36")
    gt["warp_events"][1] = warp(7, 9, "MAP_ROUTE36_CLEARING", 0)
    grava("Gate_RuinsOfAlph_Route36", gt)
    ru = le("RuinsOfAlph_Outside")
    ru["warp_events"][1] = warp(20, 6, "MAP_ROUTE36_CLEARING", 2)
    grava("RuinsOfAlph_Outside", ru)


# ============================================================ 4. Clareira 42

ESCONDIDOS_42 = [
    # (x, y) do autor, item nosso, apelido de flag
    (31, 18, "ITEM_TINY_MUSHROOM", "FLAG_HIDDEN_ITEM_ROUTE42_CLEARING_01"),
    (50, 21, "ITEM_ETHER", "FLAG_HIDDEN_ITEM_ROUTE42_CLEARING_02"),
    (30, 12, "ITEM_BIG_MUSHROOM", "FLAG_HIDDEN_ITEM_ROUTE42_CLEARING_03"),
    (15, 22, "ITEM_HONEY", "FLAG_HIDDEN_ITEM_ROUTE42_CLEARING_04"),
    (7, 19, "ITEM_REVIVE", "FLAG_HIDDEN_ITEM_ROUTE42_CLEARING_05"),
    (42, 12, "ITEM_STARDUST", "FLAG_HIDDEN_ITEM_ROUTE42_CLEARING_06"),
    (52, 24, "ITEM_PP_UP", "FLAG_HIDDEN_ITEM_ROUTE42_CLEARING_07"),
    (56, 11, "ITEM_HYPER_POTION", "FLAG_HIDDEN_ITEM_ROUTE42_CLEARING_08"),
    (56, 19, "ITEM_MIRACLE_SEED", "FLAG_HIDDEN_ITEM_ROUTE42_CLEARING_09"),
    (56, 15, "ITEM_LEAF_STONE", "FLAG_HIDDEN_ITEM_ROUTE42_CLEARING_10"),
    (14, 15, "ITEM_SUN_STONE", "FLAG_HIDDEN_ITEM_ROUTE42_CLEARING_11"),
    (18, 18, "ITEM_BALM_MUSHROOM", "FLAG_HIDDEN_ITEM_ROUTE42_CLEARING_12"),
    (36, 22, "ITEM_RARE_CANDY", "FLAG_HIDDEN_ITEM_ROUTE42_CLEARING_13"),
]

# Os dois metatiles da beira sul do bolsão da Rota 42, e as vagas NOVAS do
# secundário gTileset_MahoganyTown que recebem os clones com seta. O arquivo tem
# 318 metatiles; os clones entram no FIM (318 e 319), e não numa vaga zerada do
# meio, porque metatile todo zero pode estar em uso como vazio de propósito.
MB_SOUTH_ARROW_WARP = 0x65
CLONES_42 = [
    # (x, y, metatile de hoje, vaga local no secundário)
    (13, 15, 625, 318),
    (14, 15, 486, 319),
]


def clareira_42():
    c = le("Route42_Clearing")
    c["warp_events"] = [warp(12, 9, "MAP_ROUTE42", 4), warp(13, 9, "MAP_ROUTE42", 5)]
    c["object_events"] = [
        obj("OBJ_EVENT_GFX_PICNICKER", 33, 17, script="Route42_Clearing_EventScript_Florist",
            mov="MOVEMENT_TYPE_WANDER_AROUND", rx=2, ry=1),
    ]
    c["bg_events"] = [escondido(x, y, item, flag) for x, y, item, flag in ESCONDIDOS_42]
    grava("Route42_Clearing", c)

    r = le("Route42")
    ws = r["warp_events"][:4]
    ws += [warp(13, 15, "MAP_ROUTE42_CLEARING", 0), warp(14, 15, "MAP_ROUTE42_CLEARING", 1)]
    r["warp_events"] = ws
    grava("Route42", r)

    # Clone de metatile com seta: 16 bytes iguais, atributo com o behavior novo.
    lay = json.load(open(os.path.join(REPO, "data/layouts/layouts.json")))
    L = next(x for x in lay["layouts"] if x.get("id") == "LAYOUT_ROUTE42")
    pri = os.path.join(REPO, "data/tilesets/primary/johto_north_east")
    sec = os.path.join(REPO, "data/tilesets/secondary/mahogany_town")
    mpri = open(os.path.join(pri, "metatiles.bin"), "rb").read()
    apri = open(os.path.join(pri, "metatile_attributes.bin"), "rb").read()
    msec = bytearray(open(os.path.join(sec, "metatiles.bin"), "rb").read())
    asec = bytearray(open(os.path.join(sec, "metatile_attributes.bin"), "rb").read())
    mapa = bytearray(open(os.path.join(REPO, L["blockdata_filepath"]), "rb").read())
    w = L["width"]
    mudou = False
    for x, y, orig, vaga in CLONES_42:
        if orig >= 640:
            raise SystemExit("ERRO: o metatile %d não é do primário" % orig)
        corpo = mpri[orig * 16:orig * 16 + 16]
        attr = struct.unpack_from("<H", apri, orig * 2)[0]
        novo_attr = (attr & 0xFF00) | MB_SOUTH_ARROW_WARP
        if len(msec) // 16 == vaga:
            msec += corpo
            asec += struct.pack("<H", 0)
            mudou = True
        elif bytes(msec[vaga * 16:vaga * 16 + 16]) != corpo:
            raise SystemExit("ERRO: a vaga %d do secundário já tem outro metatile" % vaga)
        if struct.unpack_from("<H", asec, vaga * 2)[0] != novo_attr:
            struct.pack_into("<H", asec, vaga * 2, novo_attr)
            mudou = True
        i = 2 * (y * w + x)
        v = struct.unpack_from("<H", mapa, i)[0]
        quer = (v & 0xFC00) | (640 + vaga)
        if v != quer:
            if (v & 0x3FF) != orig:
                raise SystemExit("ERRO: (%d,%d) da Rota 42 não tem mais o metatile %d" % (x, y, orig))
            struct.pack_into("<H", mapa, i, quer)
            mudou = True
    if mudou:
        DIFS.append("Route42 (metatiles)")
        if CONFERIR:
            print("DIFERENTE: clones de metatile da Rota 42")
        else:
            open(os.path.join(sec, "metatiles.bin"), "wb").write(msec)
            open(os.path.join(sec, "metatile_attributes.bin"), "wb").write(asec)
            open(os.path.join(REPO, L["blockdata_filepath"]), "wb").write(mapa)
            print("escrito: clones de metatile da Rota 42")


# ============================================================ 5. National Park

FORA = (-9, -9)   # fora do mapa e fora do alcance da câmera

# índice do objeto -> (x, y) no desenho do autor. LIGHT_SPRITE vai para FORA.
PARQUE_NORMAL = {
    0: (18, 37),   # LASS que passeia: no corredor central, entre a fonte e a praça
    1: (9, 40),    # YOUNGSTER sentado: banco da esquerda do autor
    2: (10, 40),   # GBA_KID sentado: mesmo banco
    3: (27, 40),   # WOMAN_2 sentada: banco da direita, onde o autor senta um casal
    4: (28, 40),   # PERSIAN ao lado dela, no mesmo banco
    5: (7, 23),    # Beverly: lugar de treinador do autor, na moita oeste
    6: (18, 28),   # Jack: lugar de treinador do autor, na moita central
    7: (7, 15),    # Krise: lugar de treinador do autor, no capim noroeste
    8: (26, 13),   # William: lugar de treinador do autor, no capim nordeste
    9: (23, 4),    # professora: no lugar da senhora do autor, no alto do parque
    10: (0, 11),   # árvore de Cut: fecha a faixa oeste, que só tem 1 célula aqui
    11: (1, 42),   # TM Dig: a bola do autor, no fim da faixa oeste
    12: (32, 6),   # Soothe Bell: o item do autor no alto da trilha nordeste
    13: (8, 32),   # Nidoran macho: no gramado sudoeste
    14: (21, 41),  # Sunkern: junto do canteiro de flores do autor
    15: (25, 41),  # Sunkern: junto do canteiro
    16: (20, 18),  # Psyduck: na beira da fonte
    17: (9, 32),   # Nidoran fêmea: no gramado sudoeste
    18: (12, 48),  # Murkrow: no corredor sul
    19: (33, 15),  # Murkrow: perto da guarita leste
    20: (24, 7),   # Scyther: no alto, no gramado nordeste (fora do caminho da Soothe Bell)
    21: (26, 8),   # Scyther
    22: (24, 45),  # Venonat: na praça sul
    23: (29, 33),  # Weedle: no gramado sudeste
    24: (1, 30),   # Caterpie: na faixa oeste, que ali tem duas células de largura
    25: (32, 27),  # Weedle: na beira leste
    26: (9, 49),   # Pidgey: no corredor sul, fora das duas setas
}
PARQUE_CONCURSO = {
    0: (9, 12),    # BC2
    1: (22, 8),    # BC1
    2: (20, 18),   # Psyduck na fonte
    3: (30, 7),    # Metapod
    4: (14, 6),    # Kakuna
    5: (24, 45),   # Venonat
    6: (29, 32),   # Pinsir
    7: (6, 30),    # Weedle
    8: (20, 45),   # Scyther na praça sul
    9: (12, 4),    # Caterpie
    10: (9, 50),   # atendente do concurso, ao lado da saída sul
    11: (25, 26),  # menino
    12: (11, 26),  # Belinda
    13: (21, 2),   # Paras
    14: (31, 44),  # Beedrill
    15: (4, 23),   # Butterfree no capim oeste (a faixa ali tem UMA célula)
    16: (35, 17),  # atendente lateral: em cima da seta leste, que é o que ela faz hoje
}


def parque():
    for nome, tabela in (("NationalPark_Normal", PARQUE_NORMAL),
                         ("NationalPark_BugContest", PARQUE_CONCURSO)):
        m = le(nome)
        for i, o in enumerate(m["object_events"]):
            if o["graphics_id"] == "OBJ_EVENT_GFX_LIGHT_SPRITE":
                move(o, *FORA)
            elif i in tabela:
                move(o, *tabela[i])
            elif o["x"] >= 0 and o["y"] >= 0:
                raise SystemExit("ERRO: %s objeto %d sem lugar no desenho do autor" % (nome, i))
        ws = m["warp_events"]
        # As quatro setas sul nossas viram as DUAS do autor, (10,51) e (11,51).
        # 3 e 4 ficam em cima de 0 e 1: o motor usa o primeiro warp da célula,
        # e nenhum mapa aponta para 3 ou 4.
        ws[0] = warp(10, 51, ws[0]["dest_map"], ws[0]["dest_warp_id"])
        ws[1] = warp(11, 51, ws[1]["dest_map"], ws[1]["dest_warp_id"])
        ws[3] = warp(10, 51, ws[3]["dest_map"], ws[3]["dest_warp_id"])
        ws[4] = warp(11, 51, ws[4]["dest_map"], ws[4]["dest_warp_id"])
        ws[2] = warp(35, 17, ws[2]["dest_map"], ws[2]["dest_warp_id"])
        if nome == "NationalPark_Normal":
            # A seta leste do autor tem DUAS células; a segunda ganha warp NOVO.
            if len(ws) == 5:
                ws.append(warp(35, 18, "MAP_GATE_NATIONAL_PARK", 2))
        else:
            # O concurso tem um warp 5 que volta para o próprio mapa em cima do
            # capim; ele não dispara e ninguém aponta para ele. Fica no capim
            # equivalente do autor.
            ws[5] = warp(17, 27, ws[5]["dest_map"], ws[5]["dest_warp_id"])
        bg = []
        for b in m["bg_events"]:
            s = b.get("script", "")
            if s.endswith("_Trash"):
                ja = [x for x in bg if x.get("script", "").endswith("_Trash")]
                b = dict(b, x=12 if not ja else 30, y=40)
            elif s.endswith("_RelaxationSquare"):
                b = dict(b, x=14, y=44)
            elif s.endswith("_BattleSign"):
                b = dict(b, x=27, y=31)
            elif s.endswith("_TrainerTips"):
                # O autor não desenhou uma terceira placa: a de dicas sai.
                continue
            bg.append(b)
        m["bg_events"] = bg
        grava(nome, m)


def main():
    ginasio_violet()
    praca_da_torre()
    clareira_36()
    clareira_42()
    parque()
    if CONFERIR:
        print("FALTA ESCREVER: %d" % len(DIFS) if DIFS else "tudo escrito")
        return 1 if DIFS else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
