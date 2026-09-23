#!/usr/bin/env python3
"""Prova de ALCANCE das três áreas do Safari de Johto (Liquid Crystal).

O que ela prova, e por que a prova é esta
-----------------------------------------
O METODO-COPIA-CIDADES.md, seção 2, cobra de toda área copiada que "toda porta,
NPC e saída seja alcançável a pé a partir de todas as outras (busca em
largura)". O `portao_planta.py` não serve aqui (a planta é do hack, e muda de
propósito), e `valida_conectividade.py` só confere ÍNDICE de warp. Nenhum dos
dois anda no mapa.

Esta ferramenta anda. Para cada uma das três áreas ela:

1. monta a grade de passabilidade a partir do `map.bin` (colisão nos bits 10-11)
   e do comportamento de metatile do par de tilesets (resolvido pelo corte de
   640 da versão de layout `frlg`);
2. marca como OBSTÁCULO todo `object_event` do `map.json`. Isto não é
   preciosismo: NPC e Poké Bola PARADOS bloqueiam o tile em que estão, e num
   labirinto de Safari com corredor de um tile de largura um item mal posto
   tranca metade da área. O atendente da saída é obstáculo também, e é ele que
   tranca a porta de propósito;
3. roda busca em largura a partir do TILE DE CHEGADA (aquele em que o jogador
   fica depois de o script de entrada rodar) e cobra que seja alcançável:
   - um tile VIZINHO de cada `object_event` (é de onde se fala com o NPC e se
     pega o item: ninguém pisa em cima deles);
   - um tile vizinho de cada `bg_event` (placa), com o lado certo, já que placa
     fica em parede;
   - o tile da PORTA, ou seja o warp, para provar que dá para voltar. O
     atendente é o obstáculo que está EM CIMA da porta, então a conta da porta
     é feita com ele fora do caminho, que é o que o script dele faz quando o
     jogador aceita sair.

Ela também DIZ, sem reprovar, o que só se alcança nadando. A área da água é
água: a língua de terra da entrada tem 19 tiles e o resto do mapa é mar aberto,
então item em ilhota é alcançável de Surf e isso é desenho, não defeito. O que
seria defeito é isso acontecer sem ninguém ter medido, e por isso sai no
relatório.

Uso:
    python3 dev_scripts/prova_alcance_safari_johto.py
    python3 dev_scripts/prova_alcance_safari_johto.py --mapa LcSafariForest
Sai 1 se qualquer cobrança acima falhar.
"""
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))

import valida_warp_tile as VWT          # noqa: E402  (reusa NOME e tabela_de_atributos)

# Comportamentos em que só se anda NADANDO. Saem da mesma tabela
# `sTileBitAttributes` de src/metatile_behavior.c que o motor usa
# (TILE_FLAG_SURFABLE), mais a cachoeira, que é superfície de água.
SO_NADANDO = {
    "MB_POND_WATER", "MB_INTERIOR_DEEP_WATER", "MB_DEEP_WATER", "MB_OCEAN_WATER",
    "MB_SEMI_DEEP_WATER", "MB_SOOTOPOLIS_DEEP_WATER", "MB_NO_SURFACING",
    "MB_SEAWEED", "MB_SEAWEED_NO_SURFACING", "MB_FAST_WATER", "MB_WATERFALL",
    "MB_SHALLOW_WATER", "MB_CYCLING_ROAD_WATER",
}

# A área, o tile de CHEGADA (depois do script de entrada) e o tile da PORTA.
# Os três pares saem dos `map.json` e dos `scripts.inc` desta frente; se um
# deles mudar lá e não mudar aqui, a prova cai, que é o que se quer.
AREAS = {
    "LcSafariMountain": {"chegada": (9, 43), "porta": (9, 44)},
    "LcSafariForest":   {"chegada": (25, 48), "porta": (25, 49)},
    "LcSafariWater":    {"chegada": (43, 43), "porta": (43, 44)},
}

VIZINHOS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def grade(nome):
    """(largura, altura, {(x,y): nome do comportamento}, {(x,y): colisão})."""
    layouts = {l["id"]: l for l in json.load(
        open(os.path.join(RAIZ, "data/layouts/layouts.json")))["layouts"]}
    mapa = json.load(open(os.path.join(RAIZ, "data/maps", nome, "map.json")))
    lay = layouts[mapa["layout"]]
    w, h = lay["width"], lay["height"]
    bruto = open(os.path.join(RAIZ, lay["blockdata_filepath"]), "rb").read()
    pri, _ = VWT.tabela_de_atributos(lay["primary_tileset"])
    sec, _ = VWT.tabela_de_atributos(lay["secondary_tileset"])
    # 640 é o corte do primário na versão de layout "frlg" (include/fieldmap.h).
    # Deduzir esse número do TAMANHO do arquivo é a armadilha que o cabeçalho do
    # valida_warp_tile.py descreve: aqui ele é explícito e conferido.
    corte = 640 if lay.get("layout_version") == "frlg" else len(pri)
    if len(pri) != corte:
        raise SystemExit(f"{nome}: primário com {len(pri)} metatiles, corte {corte}")
    comportamento, colisao = {}, {}
    for i in range(w * h):
        v = struct.unpack("<H", bruto[i * 2:i * 2 + 2])[0]
        mid = v & 0x3FF
        bruto_comp = pri[mid] if mid < corte else sec[mid - corte]
        p = (i % w, i // w)
        comportamento[p] = VWT.NOME.get(bruto_comp, str(bruto_comp))
        colisao[p] = (v & 0x0C00) >> 10
    return w, h, comportamento, colisao, mapa


def busca(w, h, passavel, inicio):
    vistos = {inicio}
    fila = [inicio]
    while fila:
        x, y = fila.pop()
        for dx, dy in VIZINHOS:
            n = (x + dx, y + dy)
            if 0 <= n[0] < w and 0 <= n[1] < h and n not in vistos and passavel(n):
                vistos.add(n)
                fila.append(n)
    return vistos


def prova(nome):
    w, h, comp, col, mapa = grade(nome)
    chegada = AREAS[nome]["chegada"]
    porta = AREAS[nome]["porta"]

    objetos = {}
    for i, o in enumerate(mapa["object_events"]):
        objetos[(o["x"], o["y"])] = o.get("local_id") or o.get("script") or f"objeto {i}"

    def livre(p):
        return col[p] == 0

    def a_pe(p, ignorando=()):
        return livre(p) and comp[p] not in SO_NADANDO and (p in ignorando or p not in objetos)

    def nadando(p, ignorando=()):
        return livre(p) and (p in ignorando or p not in objetos)

    falhas = []
    if not a_pe(chegada, ignorando=(chegada,)):
        falhas.append(f"o tile de chegada {chegada} não é chão andável livre")

    andando = busca(w, h, lambda p: a_pe(p, ignorando=(chegada,)), chegada)
    molhado = busca(w, h, lambda p: nadando(p, ignorando=(chegada,)), chegada)

    print(f"== {nome}  {w}x{h}  chegada {chegada}  porta {porta}")
    print(f"   a pé alcança {len(andando)} tiles; a pé mais Surf alcança {len(molhado)}")

    # a porta: o atendente está EM CIMA dela de propósito, então a conta é com
    # ele fora do caminho, que é o estado em que o jogador aceita sair.
    sem_atendente = busca(
        w, h, lambda p: a_pe(p, ignorando=(chegada, porta)), chegada)
    if porta not in sem_atendente:
        falhas.append(f"a porta {porta} não é alcançável a pé a partir da chegada")
    else:
        print(f"   porta {porta}: alcançável a pé")

    for (x, y), rotulo in sorted(objetos.items()):
        if (x, y) == porta:
            continue                      # o atendente
        vizinhos_pe = [(x + dx, y + dy) for dx, dy in VIZINHOS
                       if (x + dx, y + dy) in andando]
        vizinhos_agua = [(x + dx, y + dy) for dx, dy in VIZINHOS
                         if (x + dx, y + dy) in molhado]
        if vizinhos_pe:
            print(f"   objeto {rotulo} em ({x},{y}): a pé, de {vizinhos_pe[0]}")
        elif vizinhos_agua:
            print(f"   objeto {rotulo} em ({x},{y}): SÓ NADANDO, de {vizinhos_agua[0]}")
        else:
            falhas.append(f"objeto {rotulo} em ({x},{y}) não é alcançável nem nadando")

    for b in mapa.get("bg_events", []):
        x, y = b["x"], b["y"]
        vizinhos_pe = [(x + dx, y + dy) for dx, dy in VIZINHOS
                       if (x + dx, y + dy) in andando]
        vizinhos_agua = [(x + dx, y + dy) for dx, dy in VIZINHOS
                         if (x + dx, y + dy) in molhado]
        rotulo = b.get("script", "placa")
        if vizinhos_pe:
            print(f"   placa {rotulo} em ({x},{y}): a pé, de {vizinhos_pe[0]}")
        elif vizinhos_agua:
            print(f"   placa {rotulo} em ({x},{y}): SÓ NADANDO, de {vizinhos_agua[0]}")
        else:
            falhas.append(f"placa {rotulo} em ({x},{y}) não é alcançável nem nadando")

    for f in falhas:
        print(f"   FALHA: {f}")
    return falhas


def main():
    alvos = list(AREAS)
    if "--mapa" in sys.argv:
        alvos = [sys.argv[sys.argv.index("--mapa") + 1]]
    falhas = []
    for nome in alvos:
        falhas += prova(nome)
    if falhas:
        print(f"\n{len(falhas)} FALHAS de alcance")
        return 1
    print("\nALCANCE OK nas três áreas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
