#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remapeamento de Cianwood para o desenho do Scorched Silver (seção 2 do contrato).

A arte é o mapa `g0m12` do Pokémon Scorched Silver v1.3 (40x60), trazida byte a
byte por `copia_cidade_secundario.py` para o secundário
`gTileset_CianwoodCityCopiaSec`. O JOGO é nosso, e é este arquivo: cada warp,
NPC, placa e gatilho vai para o lugar equivalente do desenho novo.

QUAL MAPA É A CIANWOOD DELES
----------------------------
A tabela de nomes de seção da ROM (gRegionMapEntries, 0x6B2AD4) diz que a seção
3 é "CIANWOOD CITY", e o único mapa de CIDADE com `secao=3` é o `g0m12`. As
oito portas dele foram casadas pela FUNÇÃO, lida no destino de cada warp:

    porta        destino no hack   como se sabe                    nosso mapa
    (10,39)      g29m1 15x12       música 568, a dos ginásios      CianwoodGym
    (28,48)      g4m5  14x9        balcão de Centro, com escada    CianwoodPokecenter
    (20,36)      g4m4  11x8        blockdata 0x4E28D4, a planta    CianwoodShop (a
                                   de Mart do hack                 FARMÁCIA)
    (9,9)        g3m0  10x8        casa                            CianwoodHouse1
    (23,42)      g4m0  10x8        casa                            CianwoodHouse2
    (10,47)      g4m3  10x8        casa                            CianwoodHouse3
    (19,48) e    g9m7  17x10       salão grande de porta dupla,    CliffEdgeGate
    (20,48)                        só liga a outro salão (g9m8)

A nossa Cianwood tem a CLIFF EDGE GATE e o desenho do autor não tem: pela seção
2 do contrato, o prédio nosso é encaixado no desenho deles. Ela fica no salão de
porta dupla, que é o único prédio público que sobrou e cujo interior no hack já
é um salão de recepção. As duas células da porta ganharam warp: a (19,48) é o
warp 1 de sempre e a (20,48) é o warp 7, novo, no FIM da lista.

A COSTURA, E POR QUE A CONEXÃO CONTINUA ABERTA
----------------------------------------------
A cidade coube INTEIRA no secundário (tentativa 1 da seção 3.2): 197 metatiles
do autor, 366 tiles e 6 paletas, com o nosso `gTileset_JohtoNorthEast` de
primário. A Route41 passou a usar o MESMO secundário, com os 38 metatiles dela
pinados no mesmo índice (render dela com 0 pixel de mudança), que é o arranjo
do jogo de fábrica: costura certa nos dois sentidos por construção.

O offset da conexão mudou de -10 para -4. A borda leste do desenho do autor é
MAR de cima a baixo, e a borda oeste da Route41 é mar até a linha 63 e penhasco
da linha 64 em diante. Com -10, as linhas 54 a 59 da cidade (mar) encostavam no
penhasco da rota; com -4, as 60 linhas da cidade encostam só em mar.

Uso:
    python3 dev_scripts/remapeia_cianwood.py            # só confere e mostra
    python3 dev_scripts/remapeia_cianwood.py --aplicar
"""
import argparse
import collections
import json
import os
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
MAPA = os.path.join(REPO, "data/maps/CianwoodCity/map.json")
ROTA = os.path.join(REPO, "data/maps/Route41/map.json")
POVOA = os.path.join(REPO, "dev_scripts/povoa_cidades.json")
SCRIPTS = os.path.join(REPO, "data/maps/CianwoodCity/scripts.inc")
BLOCOS = os.path.join(REPO, "data/layouts/CianwoodCity/map.bin")
LARGURA, ALTURA = 40, 60

# warp id -> (x, y). Os ids NÃO mudam: os interiores apontam para eles.
WARPS = {
    0: (9, 9),     # CianwoodHouse1, casa do norte
    1: (19, 48),   # CliffEdgeGate, salão de porta dupla (célula da esquerda)
    2: (23, 42),   # CianwoodHouse2
    3: (10, 47),   # CianwoodHouse3
    4: (10, 39),   # CianwoodGym
    5: (28, 48),   # CianwoodPokecenter
    6: (20, 36),   # CianwoodShop, a farmácia
}
# warp novo, no fim da lista: a outra célula da porta dupla do salão.
WARPS_NOVOS = [{"x": 20, "y": 48, "elevation": 0, "dest_map": "MAP_CLIFF_EDGE_GATE", "dest_warp_id": "0"}]

# índice do object_event -> (x, y). A ORDEM da lista não muda (seção 1 do
# contrato: índice de objeto é estado de save).
OBJETOS = {
    0: (17, 20),   # SUICUNE da cena: praia do norte, a mesma célula do hns
    1: (18, 29),   # EUSINE: sobe a coluna 18, que é areia de 23 a 29
    2: (14, 30),   # "Boulders to the north": na entrada da praia do norte
    3: (27, 40),   # "FLY to OLIVINE"
    4: (12, 42),   # "CHUCK spars": na porta do ginásio
    5: (24, 46),   # mulher, no corredor entre o salão e o Centro
    6: (30, 52),   # KRABBY, na praia sul
    7: (32, 51),   # KRABBY
    8: (31, 54),   # KRABBY
    9: (13, 51),   # SHUCKLE, ao pé das pedras do sudoeste
    10: (16, 53),  # SHUCKLE
    11: (7, 40),   # GEODUDE, ao pé do penhasco do ginásio
    12: (9, 19),   # GEODUDE, ao pé do penhasco da praia do norte
    13: (28, 34),  # PIDGEOTTO, na praia leste
    14: (11, 15),  # seis pedras quebráveis, "to the north of town"
    15: (12, 15),
    16: (11, 16),
    17: (20, 12),
    18: (21, 12),
    19: (20, 13),
    20: (17, 49),  # ENGINEER da obra da SAFARI ZONE, ao lado da CLIFF EDGE GATE
    21: (13, 44),  # Povoa1, "The GYM here fights bare handed"
    22: (31, 44),  # Povoa2, pescador na praia leste
    23: (24, 38),  # Povoa3, "The PHARMACY has medicine"
    24: (15, 47),  # Povoa4, virado para o salão da CLIFF EDGE GATE
    25: (30, 38),  # Povoa5, "ROUTE 41 east is open sea"
    26: (15, 50),  # SUICUNE da dex, ao lado da CLIFF EDGE GATE, como antes
}

# placas: índice do bg_event -> (x, y). As quatro caem em placa DO AUTOR.
PLACAS = {
    0: (17, 41),   # CitySign: o quadro da praça do meio
    1: (21, 36),   # Pharmacy: a fachada da farmácia, lida de baixo
    2: (13, 40),   # GymSign: o quadro ao lado do ginásio
    3: (23, 49),   # CaveSign (CLIFF EDGE CAVE): o quadro ao lado do salão
}

# O gatilho da cena do SUICUNE. No mapa antigo ele ficava num corredor de uma
# célula e todo mundo que subia pisava nele. A praia do autor tem OITO células de
# largura na linha 22 (x=11..18), e é a única linha que separa a cidade da casa
# do norte; um gatilho só em (18,22) deixaria a cena acontecer por sorte. As
# oito células disparam o MESMO script, com a MESMA var.
GATILHO_Y = 22
GATILHO_X = range(11, 19)

OFFSET_CONEXAO = -4

POVOA4_FALA = "CLIFF EDGE GATE is the big blue\\nhall. The rocks past it are worse."
POVOA4_ANTES = "CLIFF EDGE GATE is north.\\nThe rocks past it are worse."


def grade():
    import copia_cidade as cc
    lado = cc.Lado("gTileset_JohtoNorthEast", "gTileset_CianwoodCityCopiaSec", 640, 640, 7)
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
    """Provas de chão: porta em porta, NPC e gatilho em chão, e alcance."""
    g = grade()
    erros = []
    for i, w in enumerate(mapa["warp_events"]):
        c = g[(w["x"], w["y"])]
        if c["mb"] not in MB_PORTA:
            erros.append("warp %d em (%d,%d) não é porta (mb 0x%X)" % (i, w["x"], w["y"], c["mb"]))
    bloqueio = set()
    for i, o in enumerate(mapa["object_events"]):
        if not andavel(g[(o["x"], o["y"])]):
            erros.append("objeto %d em (%d,%d) não é chão" % (i, o["x"], o["y"]))
        bloqueio.add((o["x"], o["y"]))
    for e in mapa["coord_events"]:
        if not andavel(g[(e["x"], e["y"])]):
            erros.append("gatilho em (%d,%d) não é chão" % (e["x"], e["y"]))
    # alcance: da frente de cada porta, com os objetos parados como parede
    frentes = []
    for i, w in enumerate(mapa["warp_events"]):
        x, y = w["x"], w["y"]
        frentes.append((i, (x, y + 1) if g[(x, y)]["col"] else (x, y + 1)))
    ini = frentes[0][1]
    vis = {ini}
    fila = collections.deque([ini])
    while fila:
        x, y = fila.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n in g and n not in vis and andavel(g[n]) and n not in bloqueio:
                vis.add(n)
                fila.append(n)
    for i, f in frentes:
        if f not in vis:
            erros.append("a frente da porta %d, %s, não se alcança da porta 0" % (i, f))
    for i, (_x, _y) in PLACAS.items():
        vizinhos = [(_x, _y + 1), (_x - 1, _y), (_x + 1, _y), (_x, _y - 1)]
        if not any(v in vis for v in vizinhos):
            erros.append("placa %d em (%d,%d) não tem vizinho alcançável" % (i, _x, _y))
    # nenhuma célula andável que se alcançava sem os objetos fica ilhada com eles
    vis2 = {ini}
    fila = collections.deque([ini])
    while fila:
        x, y = fila.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n in g and n not in vis2 and andavel(g[n]):
                vis2.add(n)
                fila.append(n)
    ilhadas = sorted(c for c in vis2 - vis if c not in bloqueio)
    if ilhadas:
        erros.append("células ilhadas pelos objetos: %s" % ilhadas[:10])
    return erros, len(vis)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    args = ap.parse_args()
    with open(MAPA, encoding="utf-8") as f:
        mapa = json.load(f)
    n_warps_antes = len(mapa["warp_events"])
    if n_warps_antes == 7:
        for i, (x, y) in WARPS.items():
            mapa["warp_events"][i]["x"], mapa["warp_events"][i]["y"] = x, y
        mapa["warp_events"] += WARPS_NOVOS
    if len(mapa["object_events"]) != len(OBJETOS):
        raise SystemExit("ERRO: %d objetos no map.json e %d no remapeamento"
                         % (len(mapa["object_events"]), len(OBJETOS)))
    for i, (x, y) in OBJETOS.items():
        mapa["object_events"][i]["x"], mapa["object_events"][i]["y"] = x, y
    for i, (x, y) in PLACAS.items():
        mapa["bg_events"][i]["x"], mapa["bg_events"][i]["y"] = x, y
    modelo = dict(mapa["coord_events"][0])
    mapa["coord_events"] = []
    for x in sorted(GATILHO_X, reverse=True):
        e = dict(modelo)
        e["x"], e["y"] = x, GATILHO_Y
        mapa["coord_events"].append(e)
    for c in mapa["connections"]:
        if c["map"] == "MAP_ROUTE41":
            c["offset"] = OFFSET_CONEXAO

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
    with open(ROTA, encoding="utf-8") as f:
        rota = json.load(f)
    for c in rota["connections"]:
        if c["map"] == "MAP_CIANWOOD_CITY":
            c["offset"] = -OFFSET_CONEXAO
    with open(ROTA, "w", encoding="utf-8") as f:
        json.dump(rota, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # o povoamento guarda posição e fala; sem isto, `povoa_cidades.py --aplica`
    # devolveria os cinco NPCs para as coordenadas do mapa antigo.
    with open(POVOA, encoding="utf-8") as f:
        texto = f.read()
    povoa = json.loads(texto)
    alvo = povoa["cidades"]["CianwoodCity"]["npcs"]
    for n, i in zip(alvo, range(21, 26)):
        n["x"], n["y"] = OBJETOS[i]
    alvo[3]["falas"] = [POVOA4_FALA.replace("\\\\", "\\")]
    with open(POVOA, "w", encoding="utf-8") as f:
        json.dump(povoa, f, indent=2, ensure_ascii=False)
        f.write("\n")
    s = open(SCRIPTS, encoding="utf-8").read()
    if POVOA4_ANTES in s:
        s = s.replace(POVOA4_ANTES, POVOA4_FALA)
        open(SCRIPTS, "w", encoding="utf-8").write(s)
    print("aplicado")


if __name__ == "__main__":
    main()
