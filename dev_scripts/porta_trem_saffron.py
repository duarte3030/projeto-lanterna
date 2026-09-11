#!/usr/bin/env python3
"""Redesenha a porta da estação do trem magnético de Saffron na arte do Ikarus.

Uso:
    python3 dev_scripts/porta_trem_saffron.py --medir
    python3 dev_scripts/porta_trem_saffron.py --aplicar

POR QUE EXISTE
--------------
Em 06/09/2026 o trem magnético ganhou a ponta de Saffron, e para isso quatro
células de `SaffronCity_Frlg` viraram porta: (18,13), (19,13), (18,14) e (19,14),
com o `warp_events[15]` em (18,14) apontando para
`MAP_SAFFRON_CITY_TRAIN_STATION`.

Quando Kanto trocou de arte para o Ikarus (10/09/2026), o importador PRESERVOU
essas quatro células, para não apagar a porta. O índice de metatile continuou o
mesmo, mas o DESENHO por trás dele não: o metatile 644 do secundário de Saffron
deixou de ser porta e virou outra coisa. O resultado, visto na prancha
`Kanto-SaffronCity_Frlg-antes-depois.png`, é um borrão roxo e marrom colado na
parede de pedra do Ikarus. Preservar o índice não preserva o desenho, e essa é a
lição desta correção.

O QUE ELE FAZ, e o que ele NÃO faz
----------------------------------
Não inventa tile nenhum. Ele copia a porta em arco que o PRÓPRIO Ikarus desenhou
nessa mesma parede, a da Copycat's House em (22,13) e (22,14) (`warp_events[1]`),
e a cola em (18,13) e (18,14). As outras duas células, (19,13) e (19,14), voltam
a ser a parede que o autor desenhou ali.

A palavra de 16 bits é copiada INTEIRA, com colisão e elevação: a porta do
Ikarus é `col=0, elev=3, comportamento 0x069 (MB_WARP_DOOR)`, que é a forma como
o motor espera uma porta que se pisa. A porta velha era `col=1, elev=0`, que
também dispara (o motor olha o tile que o jogador ENCARA), mas não há razão para
manter duas convenções na mesma parede quando a do autor está ali do lado.
"""
import json
import struct
import sys

import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAYOUT = "LAYOUT_SAFFRON_CITY"
# destino <- origem, tudo dentro do mesmo mapa e tudo desenho do Ikarus
COPIAS = [((18, 13), (22, 13)), ((18, 14), (22, 14))]
# (19,13) e (19,14) voltam a ser a parede do autor
PAREDE = {(19, 13): 0x07D3, (19, 14): 0x07E4}


def main():
    aplica = "--aplicar" in sys.argv
    lay = json.load(open(f"{RAIZ}/data/layouts/layouts.json"))
    l = next(x for x in lay["layouts"] if x and x["id"] == LAYOUT)
    w = l["width"]
    caminho = f"{RAIZ}/{l['blockdata_filepath']}"
    b = bytearray(open(caminho, "rb").read())

    def le(x, y):
        return struct.unpack_from("<H", b, (y * w + x) * 2)[0]

    def grava(x, y, v):
        struct.pack_into("<H", b, (y * w + x) * 2, v)

    print(f"{'celula':10s} {'antes':>8s} {'depois':>8s}  fonte")
    for dst, src in COPIAS:
        v = le(*src)
        print(f"{str(dst):10s} {le(*dst):#08x} {v:#08x}  copiado de {src}")
        if aplica:
            grava(*dst, v)
    for cel, v in PAREDE.items():
        print(f"{str(cel):10s} {le(*cel):#08x} {v:#08x}  parede do Ikarus")
        if aplica:
            grava(*cel, v)

    j = json.load(open(f"{RAIZ}/data/maps/SaffronCity_Frlg/map.json"))
    wp = j["warp_events"][15]
    assert (wp["x"], wp["y"]) == (18, 14) and "TRAIN_STATION" in wp["dest_map"], wp
    print(f"\nwarp 15 continua em (18,14) -> {wp['dest_map']}")
    if aplica:
        open(caminho, "wb").write(bytes(b))
        print("GRAVADO em", caminho)
    else:
        print("só medição")


if __name__ == "__main__":
    main()
