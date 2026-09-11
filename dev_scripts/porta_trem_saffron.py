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
nessa mesma parede, a da Copycat's House (`warp_events[1]`), e a cola ao lado.

A ARMADILHA QUE CUSTOU UMA PASSADA: a porta do Ikarus tem TRÊS metatiles de
largura, não um. São 1005 | 1006 | 1023 em cima e 1013 | 1014 | 1022 embaixo, e
só o do MEIO (1014) carrega o comportamento 0x069 (`MB_WARP_DOOR`); as duas
pernas são pilar de pedra. A primeira versão copiou só a coluna do meio, e o
arco ficou sem as pernas: ombro claro e vão preto encostando direto no tijolo.
Quem viu foi a prancha de antes e depois, de novo.

Por isso o bloco copiado é 3x2, de (21,13) a (23,14), e ele é colado em (17,13)
a (19,14). Com isso o metatile do meio, o que é porta, cai exatamente em
(18,14), que é onde o `warp_events[15]` já estava: o warp NÃO muda de posição.

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
# O bloco 3x2 da porta da Copycat's House, que é o molde, e onde ele vai.
ORIGEM = (21, 13)
DESTINO = (17, 13)
# Antes de colar, as duas células que o importador preservou voltam ao desenho
# do Ikarus, senão o script não é idempotente: rodar duas vezes leria a si mesmo.
IKARUS = {(18, 13): 0x07EB, (18, 14): 0x07F3}


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

    for cel, v in IKARUS.items():
        if le(*cel) != v:
            print(f"{str(cel):10s} {le(*cel):#08x} -> {v:#08x}  volta ao desenho do Ikarus")
            if aplica:
                grava(*cel, v)

    print(f"\n{'celula':10s} {'antes':>8s} {'depois':>8s}  fonte")
    for dx in range(3):
        for dy in range(2):
            src = (ORIGEM[0] + dx, ORIGEM[1] + dy)
            dst = (DESTINO[0] + dx, DESTINO[1] + dy)
            v = le(*src)
            print(f"{str(dst):10s} {le(*dst):#08x} {v:#08x}  copiado de {src}"
                  f"{'   <- esta e a PORTA' if (dx, dy) == (1, 1) else ''}")
            if aplica:
                grava(*dst, v)

    j = json.load(open(f"{RAIZ}/data/maps/SaffronCity_Frlg/map.json"))
    wp = j["warp_events"][15]
    assert (wp["x"], wp["y"]) == (18, 14) and "TRAIN_STATION" in wp["dest_map"], wp
    print(f"\nwarp 15 continua em (18,14) -> {wp['dest_map']}")
    meio = le(18, 14) & 0x3FF
    assert meio == 1014, f"a celula do warp ficou com o metatile {meio}, e nao a porta 1014"
    print("(18,14) e o metatile 1014, o unico do arco com comportamento de porta")
    if aplica:
        open(caminho, "wb").write(bytes(b))
        print("GRAVADO em", caminho)
    else:
        print("só medição")


if __name__ == "__main__":
    main()
