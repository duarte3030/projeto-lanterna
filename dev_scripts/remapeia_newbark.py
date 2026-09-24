#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remapeamento de New Bark Town para o desenho do Scorched Silver (seção 2 do contrato).

A arte é o mapa `g0m9` do Pokémon Scorched Silver v1.3 (40x26), trazida byte a
byte por `copia_cidade_secundario.py` para o secundário
`gTileset_NewBarkTownCopiaSec`, sobre o NOSSO `gTileset_JohtoGeneral`. O JOGO é
nosso, e é este arquivo: cada warp, NPC e placa vai para o lugar equivalente do
desenho novo.

QUAL MAPA É A NEW BARK DELES
----------------------------
O `g0m9` é o único mapa de cidade com `secao=0` (a primeira seção de Johto) e
tem as quatro portas da New Bark de sempre. As portas foram casadas pela FUNÇÃO
e pela posição:

    porta     destino no hack   o que é                           nosso warp
    (17,6)    g1m1              o laboratório (a máquina do lado  0, NewBarkTown_Lab
                                é a placa dele, bg em (12,6))
    (26,8)    g1m0              a casa grande do nordeste, com a  1, PlayersHouse_1F
                                caixa de correio do jogador (23,8)
    (10,16)   g1m3              a casa do oeste                   2, NewBarkTown_House1
    (22,18)   g1m2              a casa do sul                     3, NewBarkTown_House2
                                                                  (a do PROF. ELM)

Os warps 4 a 7 eram warp MORTO no mapa antigo (MB_NORMAL com colisão 1, ESTADO
0.aa e a varredura de travessia): continuam mortos, em célula de árvore, com os
mesmos ids. O 6 era a porta lateral trancada do laboratório antigo, com a placa
`The door is locked.`; o laboratório do autor não tem porta lateral, então a
placa saiu (placa não é estado de save).

A COSTURA
---------
A cidade coube INTEIRA no secundário (tentativa 1 da seção 3.2): 146 metatiles
do autor, 265 tiles e 6 paletas. A Route29 e a Route27 usam ZERO metatile do
secundário antigo, então as três passam a apontar para o MESMO par, sem pino
nenhum (o arranjo da Azalea com a Route 33), e o render das duas rotas não muda
um pixel. O `gTileset_NewBarkTown` antigo ficou sem dono e saiu da ROM.

Offsets: a estrada do oeste do autor ocupa as linhas 10 a 13, e a da Route29
chega na borda leste nas linhas 16 a 19, então a Route29 fica 6 linhas acima
(era 5). O lago do autor encosta na borda leste nas linhas 10 a 13, e a água da
Route27 encosta na borda oeste nas linhas 22 a 25, então a Route27 fica 12
linhas acima (era 11). As demais linhas das duas bordas são árvore dos dois
lados.

Uso:
    python3 dev_scripts/remapeia_newbark.py            # só confere e mostra
    python3 dev_scripts/remapeia_newbark.py --aplicar
"""
import argparse
import collections
import json
import os
import re
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
MAPA = os.path.join(REPO, "data/maps/NewBarkTown/map.json")
R29 = os.path.join(REPO, "data/maps/Route29/map.json")
R27 = os.path.join(REPO, "data/maps/Route27/map.json")
POVOA = os.path.join(REPO, "dev_scripts/povoa_cidades.json")
SCRIPTS = os.path.join(REPO, "data/maps/NewBarkTown/scripts.inc")
BLOCOS = os.path.join(REPO, "data/layouts/NewBarkTown/map.bin")
LARGURA, ALTURA = 40, 26

# warp id -> (x, y). Os ids NÃO mudam: os interiores apontam para eles.
WARPS = {
    0: (17, 6),    # NewBarkTown_Lab
    1: (26, 8),    # PlayersHouse_1F
    2: (10, 16),   # House1, a do oeste
    3: (22, 18),   # House2, a do sul (PROF. ELM)
    4: (20, 7),    # mortos, em célula sólida, como já eram; o 4 e o 6 são
    5: (21, 7),    # DESTINO de outro mapa (WorldHub e a sala do laboratório),
    6: (19, 6),    # então ficam encostados em chão, como o 6 antigo ficava
    7: (3, 7),
}
MORTOS = {4, 5, 6, 7}

# índice do object_event -> (x, y). A ORDEM da lista não muda (índice de objeto
# é estado de save). Os PINECO de headbutt moravam em trilhas escondidas da
# mata antiga, que o desenho do autor não tem: vão para dentro da mata. O
# PINECO em (-2,23), fora da grade, fica onde estava.
OBJETOS = {
    0: (24, 12),   # FAT_MAN: a vaga do NPC do autor na estrada do meio
    1: (8, 19),    # LASS: ao lado do banco do oeste
    2: (12, 5),    # ITEM_BALL sem script: no pátio cercado do laboratório, como antes
    3: (30, 13),   # WOOPER: na beira do lago
    4: (27, 21),   # PINECO
    5: (21, 5),    # PINECO, na mata (o (16,4) antigo agora é telhado do laboratório)
    6: (11, 24),   # PINECO, na mata do sul (o mapa novo tem 26 linhas)
    7: (7, 2),     # PINECO, na mata
    8: (14, 7),    # SILVER, espiando a janela do laboratório
    9: (-2, 23),   # PINECO fora da grade, intacto
    10: (22, 9),   # Povoa1, "ELM's lab is the reason"
    11: (16, 12),  # Povoa2, na estrada do meio
    12: (32, 11),  # Povoa3, pescador na beira do lago, "ROUTE 27 is east"
    13: (13, 20),  # Povoa4
    14: (15, 15),  # Povoa5, virada para a placa da cidade
    15: (8, 11),   # Povoa6, "ROUTE 29 has soft grass", na estrada do oeste
    16: (20, 21),  # Povoa7
}
NA_MATA = {5, 6, 7, 9}

# placas: script -> (x, y). A "Door" (porta lateral trancada) sai.
PLACAS = {
    "NewBarkTown_EventScript_TownSign": (17, 14),             # placa do autor
    "NewBarkTown_EventScript_PlayersHouseMailbox": (23, 8),   # caixa de correio do autor
    "NewBarkTown_EventScript_ElmsHouseMailbox": (21, 18),     # parede ao lado da porta da casa do sul
    "NewBarkTown_EventScript_LabSign": (12, 6),               # a máquina que o autor usa de placa
}
PLACA_QUE_SAI = "NewBarkTown_EventScript_Door"

OFFSET_R29 = -6
OFFSET_R27 = -12


def grade():
    import copia_cidade as cc
    lado = cc.Lado("gTileset_JohtoGeneral", "gTileset_NewBarkTownCopiaSec", 640, 640, 7)
    dados = open(BLOCOS, "rb").read()
    g = {}
    for y in range(ALTURA):
        for x in range(LARGURA):
            v = struct.unpack_from("<H", dados, (y * LARGURA + x) * 2)[0]
            comp = lado.atributo(v & 0x3FF)[0]
            g[(x, y)] = {"col": (v >> 10) & 3, "elev": v >> 12, "mb": comp}
    return g


MB_AGUA = {0x15}
MB_PORTA = {0x60, 0x69}


def andavel(c):
    return c["col"] == 0 and c["mb"] not in MB_AGUA


def confere(mapa):
    """Provas de chão: porta em porta, morto em árvore, NPC em chão, e alcance."""
    g = grade()
    erros = []
    for i, w in enumerate(mapa["warp_events"]):
        c = g[(w["x"], w["y"])]
        if i in MORTOS:
            if c["col"] == 0 or c["mb"] != 0:
                erros.append("warp morto %d em (%d,%d) passou a disparar" % (i, w["x"], w["y"]))
        elif c["mb"] not in MB_PORTA:
            erros.append("warp %d em (%d,%d) não é porta (mb 0x%X)" % (i, w["x"], w["y"], c["mb"]))
    bloqueio = set()
    for i, o in enumerate(mapa["object_events"]):
        p = (o["x"], o["y"])
        if i in NA_MATA:
            if p in g and andavel(g[p]):
                erros.append("objeto %d da mata em (%d,%d) caiu em chão" % (i, p[0], p[1]))
            continue
        if not andavel(g[p]):
            erros.append("objeto %d em (%d,%d) não é chão" % (i, p[0], p[1]))
        bloqueio.add(p)
    frentes = [(i, (w["x"], w["y"] + 1)) for i, w in enumerate(mapa["warp_events"]) if i not in MORTOS]
    ini = frentes[0][1]

    def bfs(com_bloqueio):
        vis = {ini}
        fila = collections.deque([ini])
        while fila:
            x, y = fila.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, y + dy)
                if n in g and n not in vis and andavel(g[n]) and not (com_bloqueio and n in bloqueio):
                    vis.add(n)
                    fila.append(n)
        return vis

    vis = bfs(True)
    for i, f in frentes:
        if f not in vis:
            erros.append("a frente da porta %d, %s, não se alcança da porta 0" % (i, f))
    for nome, (x, y) in PLACAS.items():
        if not any(v in vis for v in ((x, y + 1), (x - 1, y), (x + 1, y), (x, y - 1))):
            erros.append("placa %s em (%d,%d) não tem vizinho alcançável" % (nome, x, y))
    # as duas saídas: a estrada do oeste (x=0) e a margem do lago (x=32, surf até x=39)
    for saida in ((0, 10), (0, 13), (32, 10), (32, 13)):
        if saida not in vis:
            erros.append("a saída %s não se alcança" % (saida,))
    ilhadas = sorted(c for c in bfs(False) - vis if c not in bloqueio)
    if ilhadas:
        erros.append("células ilhadas pelos objetos: %s" % ilhadas[:10])
    return erros, len(vis)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    args = ap.parse_args()
    with open(MAPA, encoding="utf-8") as f:
        mapa = json.load(f)
    for i, (x, y) in WARPS.items():
        mapa["warp_events"][i]["x"], mapa["warp_events"][i]["y"] = x, y
    if len(mapa["object_events"]) != len(OBJETOS):
        raise SystemExit("ERRO: %d objetos no map.json e %d no remapeamento"
                         % (len(mapa["object_events"]), len(OBJETOS)))
    for i, (x, y) in OBJETOS.items():
        mapa["object_events"][i]["x"], mapa["object_events"][i]["y"] = x, y
    mapa["bg_events"] = [b for b in mapa["bg_events"] if b["script"] != PLACA_QUE_SAI]
    for b in mapa["bg_events"]:
        b["x"], b["y"] = PLACAS[b["script"]]
    for c in mapa["connections"]:
        if c["map"] == "MAP_ROUTE29":
            c["offset"] = OFFSET_R29
        if c["map"] == "MAP_ROUTE27":
            c["offset"] = OFFSET_R27

    erros, alcance = confere(mapa)
    for e in erros:
        print("  ERRO:", e)
    print("células alcançáveis a pé da porta 0: %d; erros: %d" % (alcance, len(erros)))
    if erros:
        raise SystemExit(1)
    if not args.aplicar:
        return

    with open(MAPA, "w", encoding="utf-8") as f:
        json.dump(mapa, f, indent=2, ensure_ascii=False)
        f.write("\n")
    for caminho, off in ((R29, OFFSET_R29), (R27, OFFSET_R27)):
        with open(caminho, encoding="utf-8") as f:
            rota = json.load(f)
        for c in rota["connections"]:
            if c["map"] == "MAP_NEW_BARK_TOWN":
                c["offset"] = -off
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(rota, f, indent=2, ensure_ascii=False)
            f.write("\n")

    # o povoamento guarda posição; sem isto, `povoa_cidades.py --aplica`
    # devolveria os sete NPCs para as coordenadas do mapa antigo.
    with open(POVOA, encoding="utf-8") as f:
        povoa = json.load(f)
    alvo = povoa["cidades"]["NewBarkTown"]["npcs"]
    for n, i in zip(alvo, range(10, 17)):
        n["x"], n["y"] = OBJETOS[i]
    with open(POVOA, "w", encoding="utf-8") as f:
        json.dump(povoa, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # a placa que saiu leva junto o script e o texto dela, que ficariam órfãos
    s = open(SCRIPTS, encoding="utf-8").read()
    s = re.sub(r"NewBarkTown_EventScript_Door::\n\tmsgbox NewBarkTown_Text_Door, MSGBOX_SIGN\n\tend\n\n", "", s)
    s = re.sub(r"NewBarkTown_Text_Door::\n\t\.string \"The door is locked\.\$\"\n\n", "", s)
    open(SCRIPTS, "w", encoding="utf-8").write(s)
    print("aplicado")


if __name__ == "__main__":
    main()
