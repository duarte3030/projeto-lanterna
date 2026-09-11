#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O outro lado das três saídas de Olivine: Route39, Route40 e o porto.

A Olivine copiada tem par de tilesets PRÓPRIO, e por isso não pode ter conexão de
mapa nenhuma: `LoadMapFromCameraTransition` (src/overworld.c:911) recarrega só o
tileset SECUNDÁRIO numa travessia por conexão, porque o jogo original garante
primário comum entre mapas ligados. Quem atravessasse a pé levaria o primário da
cidade junto e veria a rota inteira desenhada com as paletas do Scorched Silver.

Então a conexão sai dos TRÊS vizinhos e cada borda ganha o par de setas:

    vizinho                  borda            células              warps novos
    Route39                  y=53 (sul)       x=24..27              3 a 6
    Route40                  x=33 (leste)     y=13..23             10 a 20
    OlivineCity_PortOutside  y=0 (norte)      x=14..16              1 a 3

A borda inteira ganha seta, não só o trecho que a cidade tem: a praia de Route40
é ANDÁVEL nas onze linhas de 13 a 23, e deixar oito delas batendo na borda do
mapa seria parede invisível. Do lado da cidade só há três células de praia, então
as onze caem em três warps (13, 14 e 15 da Olivine), quatro para o primeiro,
quatro para o segundo e três para o terceiro.

Nenhum pixel muda em rota nenhuma. As células trocam para um metatile CLONE, com
os mesmos tiles e as mesmas paletas do metatile que estava lá, e só o byte de
comportamento diferente. O clone entra em vaga LIVRE do SECUNDÁRIO de cada rota
(o secundário é só dela, ao contrário do `gTileset_JohtoGeneral`, que é da região
inteira e não pode ser mexido), o arquivo cresce no fim e nenhum índice que já
existia anda de lugar.

Uso:
    python3 dev_scripts/remapeia_olivine_vizinhos.py            # só mostra
    python3 dev_scripts/remapeia_olivine_vizinhos.py --aplicar
"""
import argparse
import collections
import json
import os
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N_META_PRI = 640          # Johto é bigPrimary

MB_EAST_ARROW_WARP = 98
MB_WEST_ARROW_WARP = 99
MB_NORTH_ARROW_WARP = 100
MB_SOUTH_ARROW_WARP = 101

PRIMARIO = "data/tilesets/primary/johto_general"

# mapa -> (secundário, comportamento da seta, células, warps novos)
# warps novos: lista de (x, y, destino, id_do_warp_destino)
PLANO = [
    {
        "mapa": "Route39",
        "secundario": "data/tilesets/secondary/route38_farmland",
        "comportamento": MB_SOUTH_ARROW_WARP,
        "celulas": [(x, 53) for x in range(24, 28)],
        "warps": [(x, 53, "MAP_OLIVINE_CITY", str(9 + i)) for i, x in enumerate(range(24, 28))],
        "conexao_fora": "MAP_OLIVINE_CITY",
    },
    {
        "mapa": "Route40",
        "secundario": "data/tilesets/secondary/olivine_city",
        "comportamento": MB_EAST_ARROW_WARP,
        "celulas": [(33, y) for y in range(13, 24)],
        # quatro linhas para o warp 13 da cidade, quatro para o 14, três para o 15
        "warps": [(33, y, "MAP_OLIVINE_CITY", "13" if y < 17 else ("14" if y < 21 else "15"))
                  for y in range(13, 24)],
        "conexao_fora": "MAP_OLIVINE_CITY",
    },
    {
        "mapa": "OlivineCity_PortOutside",
        "secundario": "data/tilesets/secondary/port_indoor",
        "comportamento": MB_NORTH_ARROW_WARP,
        "celulas": [(x, 0) for x in range(14, 17)],
        "warps": [(x, 0, "MAP_OLIVINE_CITY", "8") for x in range(14, 17)],
        "conexao_fora": "MAP_OLIVINE_CITY",
    },
]


def layouts():
    with open(os.path.join(REPO, "data/layouts/layouts.json"), encoding="utf-8") as f:
        return {L["id"]: L for L in json.load(f)["layouts"]}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--aplicar", action="store_true")
    a = ap.parse_args()

    meta_pri = open(os.path.join(REPO, PRIMARIO, "metatiles.bin"), "rb").read()
    attr_pri = open(os.path.join(REPO, PRIMARIO, "metatile_attributes.bin"), "rb").read()
    lays = layouts()
    escritas = []

    for p in PLANO:
        nome = p["mapa"]
        caminho_json = os.path.join(REPO, "data/maps", nome, "map.json")
        with open(caminho_json, encoding="utf-8") as f:
            d = json.load(f, object_pairs_hook=collections.OrderedDict)
        L = lays[d["layout"]]
        W, H = L["width"], L["height"]
        if L["secondary_tileset"] != "gTileset_" + "".join(
                s.capitalize() for s in os.path.basename(p["secundario"]).split("_")):
            print("AVISO: %s usa %s (a pasta é %s)" % (nome, L["secondary_tileset"], p["secundario"]))
        blocos = bytearray(open(os.path.join(REPO, L["blockdata_filepath"]), "rb").read())

        meta_sec = bytearray(open(os.path.join(REPO, p["secundario"], "metatiles.bin"), "rb").read())
        attr_sec = bytearray(open(os.path.join(REPO, p["secundario"], "metatile_attributes.bin"), "rb").read())
        n_sec = len(meta_sec) // 16
        if len(attr_sec) != n_sec * 2:
            raise SystemExit("ERRO: %s tem %d metatiles e %d bytes de atributo"
                             % (p["secundario"], n_sec, len(attr_sec)))
        print("== %s  %dx%d  secundário %s com %d metatiles" % (nome, W, H, L["secondary_tileset"], n_sec))

        # -------- um clone por metatile DISTINTO que a borda usa
        de_para = {}
        for (x, y) in p["celulas"]:
            v = struct.unpack_from("<H", blocos, (y * W + x) * 2)[0]
            idx = v & 0x3FF
            if idx >= N_META_PRI:
                raise SystemExit("ERRO: %s (%d,%d) usa metatile %d, que já é do secundário"
                                 % (nome, x, y, idx))
            if idx in de_para:
                continue
            novo_local = n_sec + len(de_para)
            if novo_local >= 384:
                raise SystemExit("ERRO: %s estourou as 384 vagas do secundário" % nome)
            de_para[idx] = novo_local
        for idx, loc in sorted(de_para.items()):
            meta_sec += meta_pri[idx * 16:(idx + 1) * 16]
            velho = struct.unpack_from("<H", attr_pri, idx * 2)[0]
            attr_sec += struct.pack("<H", (velho & 0xFF00) | p["comportamento"])
            print("   metatile %4d (local %3d): clone do %3d do JohtoGeneral, comportamento %d"
                  % (N_META_PRI + loc, loc, idx, p["comportamento"]))

        for (x, y) in p["celulas"]:
            pos = (y * W + x) * 2
            v = struct.unpack_from("<H", blocos, pos)[0]
            novo = N_META_PRI + de_para[v & 0x3FF]
            struct.pack_into("<H", blocos, pos, (v & 0xFC00) | (novo & 0x3FF))
            print("   célula (%2d,%2d): metatile %3d -> %4d" % (x, y, v & 0x3FF, novo))

        # -------- conexão fora
        antes = len(d.get("connections") or [])
        d["connections"] = [c for c in (d.get("connections") or []) if c["map"] != p["conexao_fora"]]
        print("   conexões: %d -> %d (saiu %s)" % (antes, len(d["connections"]), p["conexao_fora"]))

        # -------- warps novos, sempre no FIM
        base = len(d["warp_events"])
        modelo = d["warp_events"][0]
        esperado = base + len(p["warps"])
        for i, (x, y, alvo, wid) in enumerate(p["warps"]):
            e = collections.OrderedDict(modelo)
            e["x"], e["y"], e["elevation"] = x, y, 0
            e["dest_map"], e["dest_warp_id"] = alvo, wid
            d["warp_events"].append(e)
            print("   warp %2d NOVO: (%2d,%2d) -> %s %s" % (base + i, x, y, alvo, wid))
        if len(d["warp_events"]) != esperado:
            raise SystemExit("ERRO: contagem de warps de %s" % nome)

        escritas.append((caminho_json, d,
                         os.path.join(REPO, L["blockdata_filepath"]), bytes(blocos),
                         os.path.join(REPO, p["secundario"], "metatiles.bin"), bytes(meta_sec),
                         os.path.join(REPO, p["secundario"], "metatile_attributes.bin"), bytes(attr_sec)))

    if a.aplicar:
        for cj, d, cb, blocos, cm, ms, ca, at in escritas:
            with open(cj, "w", encoding="utf-8") as f:
                json.dump(d, f, indent=2, ensure_ascii=False)
                f.write("\n")
            open(cb, "wb").write(blocos)
            open(cm, "wb").write(ms)
            open(ca, "wb").write(at)
        print("APLICADO")
    else:
        print("(seco: nada foi escrito; use --aplicar)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
