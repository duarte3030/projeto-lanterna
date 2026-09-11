#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remapeamento do ginásio de Olivine para o desenho do GS Chronicles.

A ARTE é o mapa `g11m3` do Pokémon GS Chronicles 2.7.6, de 15x35, copiado byte a
byte pelo `copia_cidade.py` (76 metatiles, 118 tiles, 4 vagas de paleta, as
quatro provas em zero). É o quinto ginásio redesenhado do dossiê (resposta 69 do
Gui): um salão alto de aço, com o chão de grade em volta e três salas largas de
plataforma branca no caminho até a líder. O quebra-cabeça é de GEOMETRIA e não
tem gatilho nenhum: ele já vem no `map.bin` do autor.

A CONVERSÃO DE COMPORTAMENTO, MEDIDA METATILE A METATILE
--------------------------------------------------------
O GS Chronicles é base FireRed e o atributo de metatile dele tem 4 bytes, com o
comportamento em 9 bits; o nosso é Emerald, com 2 bytes e 8 bits. O número não
significa a mesma coisa nos dois enums, e o `copia_cidade.py` TRUNCA sem
traduzir, de propósito, para não inventar. Dos 76 metatiles que o mapa usa, só
TRÊS têm comportamento diferente de zero na origem, e os três foram conferidos na
ROM (tileset secundário 0x2D4CA4):

    metatile  origem  FireRed                    o que fica
    11        519     0x84 MB_SIGNPOST           30, MB_SIGNPOST do Emerald
    21        529     0x65 MB_SOUTH_ARROW_WARP    0, MB_NORMAL (ver abaixo)
    32        542     0x65 MB_SOUTH_ARROW_WARP  101, MB_SOUTH_ARROW_WARP, a saída

O metatile 21 é a JANELA do alto da parede, usada por duas células, (4,2) e
(9,2), as duas com colisão 1 e nenhuma alcançável a pé: a seta nunca dispararia.
É dado errado do mesmo tipo que a Azalea já tinha tido, e vira MB_NORMAL com o
layerType intacto e ZERO pixel mudado. O 32 é a célula (7,33), o tapete vermelho
da porta, e é por ele que o jogador sai andando para o sul.

O metatile 11 é a ESTÁTUA, em (5,31) e (9,31), e é nela que as nossas duas placas
`OlivineCity_Gym_EventScript_Statue` passam a ficar.

Uso:
    python3 dev_scripts/remapeia_olivine_gym.py            # só mostra
    python3 dev_scripts/remapeia_olivine_gym.py --aplicar
"""
import argparse
import collections
import json
import os
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPA = os.path.join(REPO, "data/maps/OlivineCity_Gym/map.json")
BLOCOS = os.path.join(REPO, "data/layouts/OlivineCity_Gym/map.bin")
ATTR_PRI = os.path.join(REPO, "data/tilesets/primary/olivine_city_gym_copia_pri/metatile_attributes.bin")
LARGURA, ALTURA = 15, 35

MB_NORMAL = 0
MB_SIGNPOST = 30

# célula onde o metatile mora -> comportamento novo. A célula é a chave para o
# número do metatile nunca ser cravado: ele é lido do `map.bin`.
COMPORTAMENTOS = [((5, 31), MB_SIGNPOST, "estátua"),
                  ((4, 2), MB_NORMAL, "janela da parede do alto")]

WARPS = {0: (7, 33)}          # a saída, no tapete vermelho

OBJETOS = {
    0: (7, 4),     # JASMINE, no alto do salão
    1: (4, 13),    # EXPERT_F, primeira sala de plataforma
    2: (10, 21),   # GENTLEMAN, segunda sala de plataforma
    3: (6, 32),    # guia do ginásio, ao lado da porta
}

PLACAS = [("OlivineCity_Gym_EventScript_Statue", 9, 31),
          ("OlivineCity_Gym_EventScript_Statue", 5, 31)]


def celula(b, x, y):
    v = struct.unpack_from("<H", b, (y * LARGURA + x) * 2)[0]
    return v & 0x3FF, (v >> 10) & 3


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--aplicar", action="store_true")
    a = ap.parse_args()

    b = open(BLOCOS, "rb").read()
    if len(b) != LARGURA * ALTURA * 2:
        raise SystemExit("ERRO: o map.bin do ginásio não é %dx%d" % (LARGURA, ALTURA))
    attr = bytearray(open(ATTR_PRI, "rb").read())

    for onde, novo, nome in COMPORTAMENTOS:
        idx = celula(b, *onde)[0]
        v = struct.unpack_from("<H", attr, idx * 2)[0]
        print("metatile %3d (%s, célula %s): comportamento %d -> %d"
              % (idx, nome, onde, v & 0xFF, novo))
        struct.pack_into("<H", attr, idx * 2, (v & 0xFF00) | novo)

    with open(MAPA, encoding="utf-8") as f:
        d = json.load(f, object_pairs_hook=collections.OrderedDict)

    for i, (x, y) in sorted(WARPS.items()):
        w = d["warp_events"][i]
        print("warp %d: (%2d,%2d) -> (%2d,%2d)  %s" % (i, w["x"], w["y"], x, y, w["dest_map"]))
        w["x"], w["y"] = x, y

    for i in sorted(OBJETOS):
        o = d["object_events"][i]
        x, y = OBJETOS[i]
        if celula(b, x, y)[1] != 0:
            raise SystemExit("ERRO: objeto %d cairia em (%d,%d), que é parede" % (i, x, y))
        print("objeto %d %-28s (%2d,%2d) -> (%2d,%2d)" % (i, o["graphics_id"], o["x"], o["y"], x, y))
        o["x"], o["y"] = x, y

    modelo = d["bg_events"][0]
    novos = []
    for script, x, y in PLACAS:
        e = collections.OrderedDict(modelo)
        e["type"] = "sign"
        e["x"], e["y"] = x, y
        e["elevation"] = 0
        e["player_facing_dir"] = "BG_EVENT_PLAYER_FACING_ANY"
        e["script"] = script
        novos.append(e)
        print("placa %-44s (%2d,%2d)" % (script, x, y))
    d["bg_events"] = novos

    if a.aplicar:
        open(ATTR_PRI, "wb").write(bytes(attr))
        with open(MAPA, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print("APLICADO")
    else:
        print("(seco: nada foi escrito; use --aplicar)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
