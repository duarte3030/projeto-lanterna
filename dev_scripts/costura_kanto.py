#!/usr/bin/env python3
"""Desenha a COSTURA de cada conexão como o motor desenha, e não como o mapa é.

Uso:
    python3 dev_scripts/costura_kanto.py            # todas as costuras de Kanto
    python3 dev_scripts/costura_kanto.py Route5_Frlg

POR QUE EXISTE
--------------
`render_maps.py` desenha um mapa com os tilesets DELE, e por isso nunca vê o
defeito que mais aparece numa troca de região inteira. O motor desenha a faixa
do mapa VIZINHO (a conexão) com os TILESETS DO MAPA ATUAL: o índice de metatile
do vizinho é resolvido na tabela do mapa em que o jogador está. Quando os dois
lados usam secundários diferentes, a mesma célula vira desenho diferente de cada
lado da fronteira, e o jogador vê lixo.

Isso já era verdade na FireRed limpa. O que mudou com o Ikarus é a ALTURA do
risco: os secundários de Kanto foram de 64 a 285 metatiles para 384, então um
índice que antes caía fora da tabela (e o motor desenhava vazio) agora resolve
para um metatile de VERDADE, e diferente. Medido nesta árvore: 18 conexões de
Kanto têm célula de secundário na faixa visível do vizinho, e elas envolvem 14
pares de tileset, quase todos em volta de Saffron.

O QUE ELE DESENHA
-----------------
O mapa inteiro, e em volta dele as 7 células de cada vizinho que cabem na tela,
resolvidas com os tilesets DO MAPA DO MEIO, com uma linha amarela marcando a
fronteira. Costura limpa é a que continua o desenho; costura suja é a que corta.
"""
import json
import os
import sys
import struct

from PIL import Image, ImageDraw

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
os.environ.setdefault("REPO_MAPAS", RAIZ)
import render_maps as rm  # noqa: E402

SAIDA = os.environ.get("SAIDA_COSTURA", "/tmp/claude-501/costura-kanto")
FAIXA = 7  # células do vizinho que o motor traz para dentro da tela


def celulas(layout):
    b = open(os.path.join(RAIZ, layout["blockdata_filepath"]), "rb").read()
    return [struct.unpack_from("<H", b, i * 2)[0] & 0x3FF
            for i in range(len(b) // 2)]


def main():
    layouts = rm.carregar_layouts()
    cache = {}
    por_id = {}
    for grupo, lista in json.load(open(f"{RAIZ}/data/maps/map_groups.json")).items():
        if not isinstance(lista, list):
            continue
        for m in lista:
            p = f"{RAIZ}/data/maps/{m}/map.json"
            if os.path.exists(p):
                j = json.load(open(p))
                por_id[j["id"]] = (m, j, layouts.get(j["layout"]))

    alvos = sys.argv[1:]
    feitos = 0
    for nome, j, l in list(por_id.values()):
        if not l or l["primary_tileset"] != "gTileset_General_Frlg":
            continue
        if alvos and nome not in alvos:
            continue
        con = [c for c in (j.get("connections") or [])
               if c["direction"] in ("up", "down", "left", "right") and c["map"] in por_id]
        if not con:
            continue
        w, h = l["width"], l["height"]
        M = rm.META_PX
        img = Image.new("RGB", ((w + 2 * FAIXA) * M, (h + 2 * FAIXA) * M), (0, 0, 0))
        base = rm.renderizar_mapa(nome, layouts, cache)
        img.paste(Image.open(base), (FAIXA * M, FAIXA * M))

        ts_pri = cache[l["primary_tileset"]]
        ts_sec = cache[l["secondary_tileset"]]
        npri = 640 if (l.get("layout_version") or "emerald") in ("johto", "frlg") else 512
        npal = 7 if npri == 640 else 6
        px = img.load()
        for c in con:
            vn, vj, vl = por_id[c["map"]]
            cs = celulas(vl)
            vw, vh = vl["width"], vl["height"]
            off = c["offset"]
            d = c["direction"]
            for k in range(FAIXA):
                for t in range(max(w, h) + 2 * FAIXA):
                    if d == "up":
                        sx, sy = t - off, vh - FAIXA + k
                        dx, dy = t, k
                    elif d == "down":
                        sx, sy = t - off, k
                        dx, dy = t, FAIXA + h + k
                    elif d == "left":
                        sx, sy = vw - FAIXA + k, t - off
                        dx, dy = k, t
                    else:
                        sx, sy = k, t - off
                        dx, dy = FAIXA + w + k, t
                    if not (0 <= sx < vw and 0 <= sy < vh):
                        continue
                    if not (0 <= dx < w + 2 * FAIXA and 0 <= dy < h + 2 * FAIXA):
                        continue
                    idx = cs[sy * vw + sx]
                    ts, il = (ts_pri, idx) if idx < npri else (ts_sec, idx - npri)
                    if il >= len(ts["metatiles"]) // 16:
                        continue
                    ent = rm.entradas_metatile(ts["metatiles"], il)
                    for camada in (0, 1):
                        for q in range(4):
                            it, fh, fv, ip = ent[camada * 4 + q]
                            tile = rm.resolver_tile(ts_pri, ts_sec, it)
                            if tile is None:
                                continue
                            cores = (ts_pri if ip < npal else ts_sec)["paletas"].get(ip)
                            if cores is None:
                                continue
                            rm.desenhar_tile(px, dx * M + (q % 2) * 8,
                                             dy * M + (q // 2) * 8, tile, cores, fh, fv)
        dr = ImageDraw.Draw(img)
        dr.rectangle([FAIXA * M, FAIXA * M, (FAIXA + w) * M - 1, (FAIXA + h) * M - 1],
                     outline=(255, 230, 0), width=1)
        os.makedirs(SAIDA, exist_ok=True)
        img.save(f"{SAIDA}/{nome}.png")
        feitos += 1
        print("OK ", nome, "->", f"{SAIDA}/{nome}.png")
    print(f"\n{feitos} costuras desenhadas em {SAIDA}")


if __name__ == "__main__":
    main()
