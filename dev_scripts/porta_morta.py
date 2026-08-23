#!/usr/bin/env python3
"""Acha (e conserta) a boca de caverna montada ao contrário em Sinnoh.

    python3 dev_scripts/porta_morta.py            # só relata
    python3 dev_scripts/porta_morta.py --corrigir
    python3 dev_scripts/porta_morta.py --demo

## O defeito, medido antes de escrito

`MAP_CELESTIC_TOWN_CAVE` tem UM warp, em (10,20), e o metatile dele é
`MB_NON_ANIMATED_DOOR`. Entrando por ele o motor larga o jogador em (10,21),
uma casa ao SUL, porque porta empurra para fora. O corpo da caverna (fileiras 3
a 19, ~120 tiles andáveis, com a sala das pinturas) fica ao NORTE. E porta
dispara quando o jogador PISA nela, venha de onde vier: o primeiro passo para o
norte devolve o jogador a Celestic Town. Medido com
`dev_scripts/testa_critico.py`, roteiro `150:NADA,16:UP*3,120:NADA` a partir de
`MAP_CELESTIC_TOWN_CAVE:0` termina em `MAP_CELESTIC_TOWN (8,5)`.

A causa NÃO é a fonte: `res/field/events/events_celestic_town_cave.json` põe o
warp em (10,20) também. É a diferença de motor. No DS a saída de caverna dispara
pelo sentido do passo; aqui `MB_NON_ANIMATED_DOOR` dispara pelo pisão. Quem já
tinha resolvido isso nesta ROM foi `dev_scripts/lagos_sinnoh.py`, com o idioma
certo para boca de caverna: `MB_SOUTH_ARROW_WARP` no tile MAIS AO SUL do par, e
o jogador nasce EM CIMA dele olhando para dentro. Seta dispara só quando o passo
vai no sentido dela, então subir entra e descer sai.

## O portão, e por que ele não é "olhar o metatile"

Metatile de porta não é defeito por si: quase toda casa de Sinnoh tem um e
funciona, porque o corpo do mapa fica ao SUL da porta, do lado onde o jogador é
largado. O defeito é TOPOLÓGICO: com o tile do warp tratado como PAREDE, o tile
onde o jogador é largado alcança quase nada do mapa. É isso que este script
mede, mapa a mapa, e é por isso que ele acha o caso de Celestic sem uma lista
escrita à mão.
"""
import json
import os
import re
import sys
from collections import deque

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import importa_npcs_sinnoh as I  # noqa: E402
import valida_mapas_sinnoh as V  # noqa: E402

CORRIGIR = "--corrigir" in sys.argv
PORTA = "MB_NON_ANIMATED_DOOR"
SETA_SUL = "MB_SOUTH_ARROW_WARP"
# BECO: com o tile do warp tratado como parede, o pouso enxerga ISTO ou menos.
# O número é pequeno de propósito. A primeira régua deste script era "menos de
# metade do mapa" e ela acusou SETE mapas, dos quais seis eram falsos: os dois
# lagos e a Route 224 são partidos por água, e a Wayward Cave e o Old Chateau
# por corredor que pede outro warp. O que separa o defeito de verdade não é o
# tamanho da parte alcançada, é o BECO: em `CelesticTownCave` o pouso enxerga UM
# tile, ele mesmo, e a caverna inteira está do outro lado da porta.
TETO_BECO = 8


def pouso(lays, lid, x, y):
    """Onde o motor larga quem entra por este warp.

    Porta empurra uma casa para o SUL (`src/field_door.c` mais o
    `MetatileBehavior_IsNonAnimDoor` de `src/overworld.c`); o resto larga em
    cima do próprio tile. Conferido na EWRAM: warp (10,20) de
    `CelesticTownCave` larga em (10,21).
    """
    return (x, y + 1) if V.comportamento(lays, lid, x, y) == PORTA else (x, y)


def alcance(lays, lid, W, H, inicio, paredes):
    vistos, fila = {inicio}, deque([inicio])
    while fila:
        x, y = fila.popleft()
        for p in ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)):
            if p in vistos or p in paredes:
                continue
            if not (0 <= p[0] < W and 0 <= p[1] < H):
                continue
            if V.colisao(lays, lid, *p) != 0:
                continue
            vistos.add(p)
            fila.append(p)
    return vistos


def portas_mortas():
    """[(mapa, warp, pouso, alcançados, andáveis)] das bocas montadas ao contrário."""
    lays = {l["id"]: l for l in json.load(
        open(os.path.join(REPO, "data/layouts/layouts.json"),
             encoding="utf-8"))["layouts"]}
    saida = []
    for meu in sorted(I.nossos_mapas_sinnoh()):
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        if not os.path.exists(pm):
            continue
        d = json.load(open(pm, encoding="utf-8"))
        lid = d.get("layout")
        if lid not in lays:
            continue
        W, H = lays[lid]["width"], lays[lid]["height"]
        warps = [(w["x"], w["y"]) for w in (d.get("warp_events") or [])
                 if isinstance(w.get("x"), int)]
        if len(warps) != 1:
            continue          # com dois warps a topologia não prova nada sozinha
        anda = sum(1 for y in range(H) for x in range(W)
                   if V.colisao(lays, lid, x, y) == 0)
        if anda < 20:
            continue          # sala minúscula: metade de nada não é medida
        wx, wy = warps[0]
        p = pouso(lays, lid, wx, wy)
        if not (0 <= p[0] < W and 0 <= p[1] < H) or V.colisao(lays, lid, *p) != 0:
            continue
        if p == (wx, wy):
            continue          # não é porta: o motor não empurra, não há beco
        viz = alcance(lays, lid, W, H, p, {(wx, wy)})
        if len(viz) <= TETO_BECO and len(
                alcance(lays, lid, W, H, p, set())) > 4 * len(viz):
            saida.append((meu, (wx, wy), p, len(viz), anda))
    return saida


def metatile_de_boca(lay, lays_json):
    """O metatile de boca que os mapas de Sinnoh DESTE par de tilesets já usam.

    Não é uma constante e não é "o primeiro do tileset", e as duas coisas foram
    medidas antes de escritas. O 519 de `lagos_sinnoh.py` é do
    `gTileset_CaveSinnoh`, e a caverna de Celestic está em
    `gTileset_Building`/`gTileset_GenericBuilding`. E o MENOR índice com
    `MB_SOUTH_ARROW_WARP` nesse par é o 6, do tileset primário, que mapa nenhum
    usa: as bocas de verdade são `0x208` (86 vezes) e `0x209` (81), do
    secundário. Escolher pelo índice teria plantado um desenho que ninguém viu.
    Aqui a escolha é por VOTO: o metatile mais usado embaixo de um `warp_event`
    de comportamento de seta, nos mapas de Sinnoh com o MESMO par de tilesets.
    """
    import collections
    import struct
    par = (lay.get("primary_tileset"), lay.get("secondary_tileset"))
    votos = collections.Counter()
    for meu in I.nossos_mapas_sinnoh():
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        if not os.path.exists(pm):
            continue
        d = json.load(open(pm, encoding="utf-8"))
        L = lays_json.get(d.get("layout"))
        if not L or (L.get("primary_tileset"), L.get("secondary_tileset")) != par:
            continue
        blob = open(os.path.join(REPO, L["blockdata_filepath"]), "rb").read()
        for w in d.get("warp_events") or []:
            x, y = w.get("x"), w.get("y")
            if not isinstance(x, int) or not isinstance(y, int):
                continue
            if V.comportamento(lays_json, d["layout"], x, y) != SETA_SUL:
                continue
            i = (y * L["width"] + x) * 2
            votos[struct.unpack("<H", blob[i:i + 2])[0]] += 1
    return votos.most_common(1)[0][0] if votos else None


def corrige(meu, warp, lays_json):
    """Vira a boca: o warp desce um tile e o tile de baixo vira seta para o sul.

    Três escritas, e as três são obrigatórias juntas.

    1. O tile da PORTA vira chão comum (cópia do vizinho de dentro), porque
       porta dispara por pisão e é ela que estava selando o caminho.
    2. O tile de POUSO vira `MB_SOUTH_ARROW_WARP`, que só dispara quando o passo
       vai no sentido da seta. Subir entra, descer sai.
    3. O `warp_event` desce para o tile de pouso, senão o motor continuaria
       largando o jogador uma casa ao sul de um tile que não empurra mais.

    É o mesmo idioma que `dev_scripts/lagos_sinnoh.py` usa nas bocas dos três
    lagos, e o T157.6 já prova que ele funciona neste motor.
    """
    import struct
    pm = os.path.join(REPO, "data/maps", meu, "map.json")
    d = json.load(open(pm, encoding="utf-8"))
    wx, wy = warp
    lay = lays_json[d["layout"]]
    W = lay["width"]
    boca = metatile_de_boca(lay, lays_json)
    if boca is None:
        return f"{meu}: nenhum metatile de {SETA_SUL} neste par de tilesets"
    caminho = os.path.join(REPO, lay["blockdata_filepath"])
    blob = bytearray(open(caminho, "rb").read())

    def i(x, y):
        return (y * W + x) * 2

    dentro = struct.unpack("<H", blob[i(wx, wy - 1):i(wx, wy - 1) + 2])[0]
    blob[i(wx, wy):i(wx, wy) + 2] = struct.pack("<H", dentro)
    blob[i(wx, wy + 1):i(wx, wy + 1) + 2] = struct.pack("<H", boca)
    for w in d["warp_events"]:
        if (w["x"], w["y"]) == (wx, wy):
            w["y"] = wy + 1
    open(caminho, "wb").write(bytes(blob))
    with open(pm, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return (f"{meu}: warp ({wx},{wy}) -> ({wx},{wy + 1}), porta virou chao "
            f"0x{dentro:04X} e o pouso virou boca 0x{boca:04X}")


def demo():
    """As tres armadilhas deste script, com a mutacao plantada em memoria."""
    lays = {l["id"]: l for l in json.load(
        open(os.path.join(REPO, "data/layouts/layouts.json"),
             encoding="utf-8"))["layouts"]}
    d = json.load(open(os.path.join(REPO, "data/maps/CelesticTownCave/map.json"),
                       encoding="utf-8"))
    lid = d["layout"]
    W, H = lays[lid]["width"], lays[lid]["height"]
    anda = sum(1 for y in range(H) for x in range(W)
               if V.colisao(lays, lid, x, y) == 0)

    # 1. DEPOIS do conserto: o warp esta no tile de pouso, a boca e seta para o
    #    sul, e o pouso enxerga a caverna inteira.
    w = d["warp_events"][0]
    assert (w["x"], w["y"]) == (10, 21), f"o warp voltou para {w}"
    assert V.comportamento(lays, lid, 10, 21) == SETA_SUL
    assert pouso(lays, lid, 10, 21) == (10, 21), "seta nao empurra"
    viz = alcance(lays, lid, W, H, (10, 21), set())
    assert len(viz) == anda, f"pouso alcanca {len(viz)} de {anda}"

    # 2. MUTACAO PLANTADA: a geometria de ANTES, calculada no mapa de hoje. Se
    #    (10,20) voltasse a ser porta, o pouso ficaria a UM tile de 108, que e
    #    exatamente o que o detector procura. Sem este assert, `portas_mortas`
    #    poderia parar de achar qualquer coisa e ninguem notaria.
    beco = alcance(lays, lid, W, H, (10, 21), {(10, 20)})
    assert len(beco) <= TETO_BECO and len(viz) > 4 * len(beco), \
        f"a mutacao nao reprova: beco={len(beco)}, aberto={len(viz)}"

    # 3. O metatile de boca sai do VOTO dos mapas do mesmo par de tilesets, e
    #    nao do menor indice: o menor aqui e 6, do tileset primario, que mapa
    #    nenhum usa.
    assert metatile_de_boca(lays[lid], lays) == 0x208, \
        "o metatile de boca deste par de tilesets mudou de valor"
    assert not portas_mortas(), "sobrou porta morta em Sinnoh"
    print(f"porta_morta --demo: 3 armadilhas provadas; a caverna de Celestic tem "
          f"{anda} tiles andaveis e o pouso alcanca {len(viz)} (era {len(beco)})")


def main():
    if "--demo" in sys.argv:
        return demo()
    achados = portas_mortas()
    print(f"portas mortas em Sinnoh: {len(achados)}")
    for meu, w, p, viz, anda in achados:
        print(f"  {meu:34} warp {w} pouso {p}: alcança {viz} de {anda} andáveis")
    if CORRIGIR:
        lays = {l["id"]: l for l in json.load(
            open(os.path.join(REPO, "data/layouts/layouts.json"),
                 encoding="utf-8"))["layouts"]}
        for meu, w, _, _, _ in achados:
            print("  ", corrige(meu, w, lays))


if __name__ == "__main__":
    main()
