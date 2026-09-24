#!/usr/bin/env python3
"""Prova de alcance do subsolo de Goldenrod, a pé e por warp, NOS DOIS SENTIDOS.

O QUE ELA PROVA, E POR QUE PRECISA DE UM GRAFO E NÃO DE UM MAPA SÓ
------------------------------------------------------------------
Os mapas do subsolo do GS Chronicles são DE PROPÓSITO cheios de pedaços que não
se ligam a pé. Medido:

    UndergroundEntrance  3 componentes (as três alcovas de quiosque)
    UndergroundSwitches  2 componentes (as duas metades do primeiro salão)
    SewersPipes          5 componentes (as cinco ilhas do labirinto de canos)

Quem prova alcance mapa a mapa reprova os três e não aprende nada. O que importa
é o grafo INTEIRO: célula andável ligada à vizinha pela regra de elevação do
motor, mais uma aresta por warp, ligando a célula de origem à célula do warp de
destino.

E prova nos DOIS sentidos, porque "dá para chegar" não é "dá para voltar": a
busca roda uma vez no grafo e uma vez no grafo INVERTIDO, a partir da mesma
semente. Alvo que aparece nas duas listas é, por definição, mutuamente
alcançável com a semente, e portanto com qualquer outro alvo.

Semente: a porta do terceiro quiosque da GoldenrodCity, em (54,43), que é
justamente a que esta onda abriu.

Uso:
    python3 dev_scripts/alcance_subsolo_goldenrod.py          # imprime e exit 0/1
    python3 dev_scripts/alcance_subsolo_goldenrod.py -v       # lista cada alvo
"""
import json
import os
import struct
import sys
from collections import deque

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import render_maps as rm  # noqa: E402

# Os sete do subsolo, mais a cidade e o porão da loja, que são as duas pontas.
MAPAS = [
    "GoldenrodCity",
    "GoldenrodCity_UndergroundEntrance",
    "GoldenrodCity_UndergroundTunnel",
    "GoldenrodCity_UndergroundSwitches",
    "GoldenrodCity_UndergroundStorage",
    "GoldenrodCity_UndergroundWarehouse",
    "GoldenrodCity_Sewers",
    "GoldenrodCity_SewersPipes",
    "GoldenrodCity_DepartmentStoreBasement",
]
# Os que esta onda desenhou: é neles que todo alvo tem de fechar.
DO_SUBSOLO = set(MAPAS[1:8])

SEMENTE = ("GoldenrodCity", 54, 43)


def carrega():
    layouts = rm.carregar_layouts()
    mundo = {}
    for nome in MAPAS:
        mj = json.load(open(os.path.join(REPO, "data/maps", nome, "map.json"), encoding="utf-8"))
        L = layouts[mj["layout"]]
        w, h = L["width"], L["height"]
        dados = open(os.path.join(REPO, L["blockdata_filepath"]), "rb").read()
        grade = [[struct.unpack_from("<H", dados, (y * w + x) * 2)[0] for x in range(w)]
                 for y in range(h)]
        mundo[nome] = {"w": w, "h": h, "grade": grade, "json": mj,
                       "id": mj["id"]}
    por_id = {m["id"]: nome for nome, m in mundo.items()}
    return mundo, por_id


def andavel(v):
    return ((v >> 10) & 3) == 0


def elev(v):
    return (v >> 12) & 0xF


def arestas(mundo, por_id):
    """{(mapa,x,y): [(mapa,x,y), ...]} com passo a pé e passo por warp."""
    g = {}

    def liga(a, b):
        g.setdefault(a, [])
        if b not in g[a]:
            g[a].append(b)
        g.setdefault(b, [])

    for nome, m in mundo.items():
        w, h, grade = m["w"], m["h"], m["grade"]
        for y in range(h):
            for x in range(w):
                if not andavel(grade[y][x]):
                    continue
                g.setdefault((nome, x, y), [])
                e = elev(grade[y][x])
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if not (0 <= nx < w and 0 <= ny < h):
                        continue
                    v = grade[ny][nx]
                    if not andavel(v):
                        continue
                    eb = elev(v)
                    # a regra do motor: elevação 0 é transição e 15 é ponte
                    if e not in (0, 15) and eb not in (0, 15) and e != eb:
                        continue
                    liga((nome, x, y), (nome, nx, ny))

    for nome, m in mundo.items():
        for wa in m["json"]["warp_events"]:
            alvo = por_id.get(wa["dest_map"])
            if alvo is None:
                continue  # porta para fora do recorte: não é alvo desta prova
            destino = mundo[alvo]["json"]["warp_events"][int(wa["dest_warp_id"])]
            liga((nome, wa["x"], wa["y"]), (alvo, destino["x"], destino["y"]))
    return g


def busca(g, semente):
    vistos = {semente}
    fila = deque([semente])
    while fila:
        n = fila.popleft()
        for m in g.get(n, ()):
            if m not in vistos:
                vistos.add(m)
                fila.append(m)
    return vistos


def inverte(g):
    inv = {n: [] for n in g}
    for a, vs in g.items():
        for b in vs:
            inv.setdefault(b, []).append(a)
    return inv


def main():
    verboso = "-v" in sys.argv
    mundo, por_id = carrega()
    g = arestas(mundo, por_id)
    if SEMENTE not in g:
        raise SystemExit("ERRO: a semente %s não é célula andável" % (SEMENTE,))

    ida = busca(g, SEMENTE)
    volta = busca(inverte(g), SEMENTE)

    alvos = []
    for nome in sorted(DO_SUBSOLO):
        m = mundo[nome]
        for i, wa in enumerate(m["json"]["warp_events"]):
            alvos.append(("warp %d" % i, nome, wa["x"], wa["y"]))
        for i, o in enumerate(m["json"]["object_events"]):
            if o["trainer_type"] != "TRAINER_TYPE_NONE":
                alvos.append(("treinador %d" % i, nome, o["x"], o["y"]))
            elif o["graphics_id"] == "OBJ_EVENT_GFX_ITEM_BALL":
                alvos.append(("bola %d" % i, nome, o["x"], o["y"]))

    ruins = []
    for rotulo, nome, x, y in alvos:
        n = (nome, x, y)
        so_ida = n in ida
        so_volta = n in volta
        if not (so_ida and so_volta):
            ruins.append((rotulo, nome, x, y, so_ida, so_volta))
        elif verboso:
            print("  ok   %-40s %-14s (%2d,%2d)" % (nome, rotulo, x, y))

    print("alvos: %d (warp, treinador e bola dos sete mapas do subsolo)" % len(alvos))
    print("alcançados a pé e por warp a partir de GoldenrodCity (54,43): %d"
          % (len(alvos) - len(ruins)))
    if ruins:
        print("FALHOU em %d:" % len(ruins))
        for rotulo, nome, x, y, i, v in ruins:
            print("   %-40s %-14s (%2d,%2d)  ida=%s volta=%s" % (nome, rotulo, x, y, i, v))
        return 1
    print("PROVA DE ALCANCE: todos alcançáveis NOS DOIS SENTIDOS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
