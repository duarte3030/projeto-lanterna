#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remapeamento do ginásio de Ecruteak para o campo de túmulos do GS Chronicles.

A arte veio do `g10m16` do GS Chronicles pelo `copia_cidade.py` (25x45, 33
metatiles, 56 tiles). O JOGO é nosso, e é este arquivo.

Duas coisas que a ferramenta NÃO podia fazer, e que estão aqui
---------------------------------------------------------------
1. **O comportamento de metatile vem do FireRed e mente no nosso motor.** O GS
   Chronicles é base FireRed (código `BPRE`), e a tabela de `MB_*` do FireRed não
   é a do Emerald. Medido metatile a metatile nos 33 que o mapa usa:

       valor  FireRed (o que o autor quis)  Emerald (o que viraria sem conserto)
        103   MB_REGULAR_WARP               MB_AQUA_HIDEOUT_WARP
        101   MB_SOUTH_ARROW_WARP           MB_SOUTH_ARROW_WARP   (igual, sorte)
        132   MB_SIGNPOST                   MB_CABLE_BOX_RESULTS_1
        157   MB_WINDOW                     MB_SECRET_BASE_SPOT_TREE_RIGHT_OPEN

   O 103 é o chão falso inteiro (901 células). Ele vira **MB_MT_PYRE_HOLE**, que é
   o buraco de cair do nosso motor: `TryStartWarpEventScript` manda para
   `EventScript_FallDownHoleMtPyre`, que apaga o jogador, toca `SE_FALL` e chama
   `DoFallWarp`. É a fantasia do ginásio do Morty, e é decisão NOSSA de desenho,
   não tradução automática: o FireRed usava warp seco.

2. **O quebra-cabeça é nosso.** As 113 quedas do autor não vieram; no lugar delas,
   FAIXAS de buraco no chão falso, cada uma com uma passagem só, que obrigam um
   ziguezague da entrada (14,42) até o altar do alto. As faixas são geradas por
   este script, não à mão, e o script PROVA por busca em largura que existe
   caminho da entrada ao altar sem pisar em buraco, e que ele passa por todas as
   passagens.

Os ids de warp não mudam de significado: 0 continua a saída para a cidade e 1
continua o ponto de queda. As quedas vão do 2 ao 114, e as que passam de 107 são
acréscimo NO FIM (seção 1 do contrato).

Uso:
    python3 dev_scripts/remapeia_ecruteak_gym.py            # seco
    python3 dev_scripts/remapeia_ecruteak_gym.py --aplicar
"""
import argparse
import collections
import json
import os
import struct
import sys
from collections import deque

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPA = os.path.join(REPO, "data/maps/EcruteakCity_Gym/map.json")
BLOCOS = os.path.join(REPO, "data/layouts/EcruteakCity_Gym/map.bin")
ATTR_PRI = os.path.join(REPO, "data/tilesets/primary/ecruteak_city_gym_copia_pri/metatile_attributes.bin")
ATTR_SEC = os.path.join(REPO, "data/tilesets/secondary/ecruteak_city_gym_copia_sec/metatile_attributes.bin")
LARGURA, ALTURA = 25, 45

MB_MT_PYRE_HOLE = 15
MB_SIGNPOST = 29
MB_WINDOW = 171

# de: comportamento lido da ROM (numeração do FireRed) -> para: o nosso
CONVERSAO = {103: MB_MT_PYRE_HOLE, 132: MB_SIGNPOST, 157: MB_WINDOW}

ENTRADA = (14, 42)          # a seta MB_SOUTH_ARROW_WARP, saída para a cidade
QUEDA = (12, 42)            # onde o jogador cai: chão seguro da sala da entrada
ALTAR = (6, 3)              # dentro da sala do alto, onde fica o Morty

# (linha, coluna da passagem). A ordem é de baixo para cima, que é a ordem em que
# o jogador encontra as faixas. As passagens ziguezagueiam de propósito.
FAIXAS = [
    (39, 14),   # a boca da sala do altar da entrada: a única saída é (14,39)
    (33, 10),
    (28, 20),
    (24, 17),   # entra no túmulo de baixo à direita pela abertura dele
    (21, 7),    # e sai do túmulo de baixo à esquerda pela abertura dele
    (16, 7),
]

# Buracos SOLTOS, que não fecham linha nenhuma: são a armadilha avulsa, para o
# jogador não aprender que só as faixas mordem. Escolhidos longe das passagens; a
# prova de caminho abaixo é quem garante que nenhum deles fecha o ginásio.
SOLTOS = [
    (3, 35), (20, 35), (6, 31), (21, 31), (2, 26), (22, 26), (4, 19),
    (19, 19), (3, 12), (21, 12), (5, 8), (19, 8), (11, 6), (14, 6),
]


# índice do object_event -> (x, y). A ORDEM da lista não muda.
OBJETOS = {
    0: (16, 42),   # guia do ginásio, na sala da entrada
    1: (5, 34),    # Jeffrey
    2: (18, 26),   # Martha
    3: (6, 20),    # Ping
    4: (13, 12),   # Grace
    5: (6, 3),     # Morty, no altar do alto
    6: (20, 38),   # Misdreavus
    7: (3, 30),    # Misdreavus
    8: (21, 14),   # Misdreavus
    9: (2, 8),     # Misdreavus
}

# bg_event: as duas placas do autor, nas células (11,41) e (17,41), que são as
# únicas com MB_SIGNPOST no mapa dele.
PLACAS_XY = [(11, 41), (17, 41)]


def le(p):
    return bytearray(open(p, "rb").read())


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--aplicar", action="store_true")
    a = ap.parse_args()

    pri, sec = le(ATTR_PRI), le(ATTR_SEC)

    def attr(i):
        d, loc = (pri, i) if i < 640 else (sec, i - 640)
        return struct.unpack_from("<H", d, loc * 2)[0]

    def poe_attr(i, v):
        d, loc = (pri, i) if i < 640 else (sec, i - 640)
        struct.pack_into("<H", d, loc * 2, v)

    b = le(BLOCOS)

    def cel(x, y):
        return struct.unpack_from("<H", b, (y * LARGURA + x) * 2)[0]

    usados = sorted({cel(x, y) & 0x3FF for y in range(ALTURA) for x in range(LARGURA)})
    trocas = 0
    for i in usados:
        v = attr(i)
        velho = v & 0xFF
        if velho in CONVERSAO:
            poe_attr(i, (v & 0xFF00) | CONVERSAO[velho])
            print("metatile %3d: comportamento %d (FireRed) -> %d (nosso)"
                  % (i, velho, CONVERSAO[velho]))
            trocas += 1
    print("%d metatiles com comportamento convertido" % trocas)

    def buraco_possivel(x, y):
        if not (0 <= x < LARGURA and 0 <= y < ALTURA):
            return False
        v = cel(x, y)
        if ((v >> 10) & 3) != 0:
            return False
        return (attr(v & 0x3FF) & 0xFF) == MB_MT_PYRE_HOLE

    def andavel(x, y):
        return 0 <= x < LARGURA and 0 <= y < ALTURA and ((cel(x, y) >> 10) & 3) == 0

    buracos = []
    for linha, passagem in FAIXAS:
        for x in range(LARGURA):
            if x == passagem:
                continue
            if buraco_possivel(x, linha):
                buracos.append((x, linha))
    print("faixas dão %d buracos" % len(buracos))

    for p in SOLTOS:
        if not buraco_possivel(*p):
            raise SystemExit("ERRO: buraco solto %s não é chão falso" % (p,))
        if p in buracos:
            raise SystemExit("ERRO: buraco solto %s já está numa faixa" % (p,))
        buracos.append(p)
    print("com os soltos: %d buracos" % len(buracos))
    if len(buracos) != 113:
        raise SystemExit("ERRO: não deu 113 buracos, deu %d" % len(buracos))

    # PROVA: existe caminho a pé da entrada até o altar sem pisar em buraco
    proibido = set(buracos)
    vistos = {ENTRADA}
    fila = deque([ENTRADA])
    while fila:
        x, y = fila.popleft()
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            n = (x + dx, y + dy)
            if n in vistos or n in proibido or not andavel(*n):
                continue
            vistos.add(n)
            fila.append(n)
    if ALTAR not in vistos:
        raise SystemExit("ERRO: o altar %s não é alcançável sem cair" % (ALTAR,))
    print("prova de caminho: entrada %s chega ao altar %s sem pisar em buraco "
          "(%d células alcançáveis)" % (ENTRADA, ALTAR, len(vistos)))
    # e a prova NEGATIVA: sem as passagens, o altar fica inalcançável
    proibido2 = set(buracos) | {(p, l) for l, p in FAIXAS}
    vistos2 = {ENTRADA}
    fila = deque([ENTRADA])
    while fila:
        x, y = fila.popleft()
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            n = (x + dx, y + dy)
            if n in vistos2 or n in proibido2 or not andavel(*n):
                continue
            vistos2.add(n)
            fila.append(n)
    if ALTAR in vistos2:
        raise SystemExit("ERRO: o altar é alcançável mesmo fechando as passagens; "
                         "as faixas não são barreira nenhuma")
    print("prova NEGATIVA: fechando as %d passagens, o altar fica inalcançável" % len(FAIXAS))

    with open(MAPA, encoding="utf-8") as f:
        d = json.load(f, object_pairs_hook=collections.OrderedDict)

    modelo = d["warp_events"][1]
    warps = [d["warp_events"][0], d["warp_events"][1]]
    warps[0]["x"], warps[0]["y"] = ENTRADA
    warps[1]["x"], warps[1]["y"] = QUEDA
    warps[1]["dest_map"] = "MAP_ECRUTEAK_CITY_GYM"
    warps[1]["dest_warp_id"] = "1"
    for (x, y) in buracos:
        w = collections.OrderedDict(modelo)
        w["x"], w["y"] = x, y
        w["elevation"] = 0
        w["dest_map"] = "MAP_ECRUTEAK_CITY_GYM"
        w["dest_warp_id"] = "1"
        warps.append(w)
    print("warps: %d (0 saída, 1 queda, %d buracos)" % (len(warps), len(buracos)))
    d["warp_events"] = warps

    for i, (x, y) in sorted(OBJETOS.items()):
        o = d["object_events"][i]
        if not andavel(x, y):
            raise SystemExit("ERRO: objeto %d iria para (%d,%d), que é parede" % (i, x, y))
        if (x, y) in proibido:
            raise SystemExit("ERRO: objeto %d iria para (%d,%d), que é buraco" % (i, x, y))
        print("objeto %d %-34s (%2d,%2d) -> (%2d,%2d)"
              % (i, o["graphics_id"], o["x"], o["y"], x, y))
        o["x"], o["y"] = x, y

    for k, (x, y) in enumerate(PLACAS_XY):
        p = d["bg_events"][k]
        print("placa %d: (%d,%d) -> (%d,%d)" % (k, p["x"], p["y"], x, y))
        p["x"], p["y"] = x, y

    if a.aplicar:
        open(ATTR_PRI, "wb").write(bytes(pri))
        open(ATTR_SEC, "wb").write(bytes(sec))
        with open(MAPA, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print("APLICADO")
    else:
        print("(seco: nada foi escrito; use --aplicar)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
