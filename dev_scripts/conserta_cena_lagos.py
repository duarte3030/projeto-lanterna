#!/usr/bin/env python3
"""Tira da agua os NPCs da cena da Galactica no Lago Verity.

Medido em 12/08/2026, depois que os casos T94.3 e T94.5 reprovaram: quatro dos
cinco objetos da cena estao em cima de `MB_POND_WATER` com elevacao 1, ou seja
sobre a agua do lago. O jogador anda em elevacao 3 e nunca os alcanca, entao a
Mars, que e conversa (`TRAINER_TYPE_NONE`), fica impossivel de acionar e a cena
inteira do Lago Verity morre.

Por que mover e seguro aqui, e foi conferido antes de escrever: o
`scripts.inc` do mapa tem ZERO `applymovement` e ZERO `setobjectxy`, e o fim da
cena usa `removeobject LOCALID_*`, que e constante e nao coordenada. Nao ha
coreografia presa a posicao.

A escolha de destino nao e gosto: cada NPC vai para o tile de TERRA
ALCANCAVEL A PE mais proximo do lugar onde ele estava, medido por busca em
largura a partir do warp do mapa, sem entrar na agua e respeitando elevacao
(so anda entre elevacoes iguais, ou quando uma das duas e 0). O `--demo`
reprova se algum deles deixar de ser alcancavel.

Uso:
    python3 dev_scripts/conserta_cena_lagos.py            # relatorio
    python3 dev_scripts/conserta_cena_lagos.py --demo     # asserts
    python3 dev_scripts/conserta_cena_lagos.py --aplica   # grava o map.json
"""
import json
import struct
import sys
from collections import deque

RAIZ = __file__.rsplit("/dev_scripts/", 1)[0]
MAPA = "LakeVerity"
WARP_DE_ENTRADA = (38, 43)

# Destino escolhido a mao, um por NPC que esta na agua, e cada um e o tile de
# terra alcancavel mais proximo da posicao original. A Mars fica no ponto mais
# ao norte da praia porque e ela quem fecha a cena, e ela olha para o sul, que
# e por onde o jogador chega.
DESTINOS = {
    (36, 32): (39, 33),   # Mars
    (37, 32): (40, 34),
    (37, 33): (38, 34),
    (35, 36): (36, 36),
}


def carrega():
    layouts = {l["id"]: l for l in json.load(
        open(f"{RAIZ}/data/layouts/layouts.json"))["layouts"]}
    mapa = json.load(open(f"{RAIZ}/data/maps/{MAPA}/map.json"))
    lay = layouts[mapa["layout"]]
    largura, altura = lay["width"], lay["height"]
    bruto = open(f"{RAIZ}/{lay['blockdata_filepath']}", "rb").read()
    grade = [struct.unpack("<H", bruto[i * 2:i * 2 + 2])[0]
             for i in range(largura * altura)]
    return mapa, grade, largura, altura


def colisao(grade, largura, x, y):
    return (grade[y * largura + x] >> 10) & 3


def elevacao(grade, largura, x, y):
    return (grade[y * largura + x] >> 12) & 15


def alcancaveis(grade, largura, altura, inicio=WARP_DE_ENTRADA):
    """Tiles que o jogador alcanca A PE: sem entrar na agua (elevacao 1) e so
    entre elevacoes iguais, ou quando uma das duas e 0, que e a regra do motor."""
    vistos = {inicio}
    fila = deque([inicio])
    while fila:
        x, y = fila.popleft()
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < largura and 0 <= ny < altura):
                continue
            if (nx, ny) in vistos or colisao(grade, largura, nx, ny) != 0:
                continue
            e1 = elevacao(grade, largura, x, y)
            e2 = elevacao(grade, largura, nx, ny)
            if (e1 != e2 and e1 != 0 and e2 != 0) or e2 == 1:
                continue
            vistos.add((nx, ny))
            fila.append((nx, ny))
    return vistos


def encostado(pos, vistos, ocupados):
    """O jogador consegue falar com quem esta em pos? Basta um vizinho alcancavel
    e livre de outro NPC."""
    x, y = pos
    for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        p = (x + dx, y + dy)
        if p in vistos and p not in ocupados:
            return True
    return False


def relatorio(aplica=False):
    mapa, grade, largura, altura = carrega()
    vistos = alcancaveis(grade, largura, altura)
    objetos = mapa["object_events"]
    ocupados = {(o["x"], o["y"]) for o in objetos}

    mudados = 0
    for obj in objetos:
        atual = (obj["x"], obj["y"])
        if atual not in DESTINOS:
            continue
        destino = DESTINOS[atual]
        if destino in ocupados:
            raise SystemExit(f"destino {destino} ja tem NPC em cima")
        if destino not in vistos:
            raise SystemExit(f"destino {destino} nao e alcancavel a pe")
        print(f"  {obj['graphics_id']:32s} {atual} -> {destino}"
              f"  (elev {elevacao(grade, largura, *atual)}"
              f" -> {elevacao(grade, largura, *destino)})")
        if aplica:
            ocupados.discard(atual)
            obj["x"], obj["y"] = destino
            ocupados.add(destino)
        mudados += 1

    if aplica and mudados:
        with open(f"{RAIZ}/data/maps/{MAPA}/map.json", "w") as saida:
            json.dump(mapa, saida, indent=2)
            saida.write("\n")
        print(f"gravado: {mudados} objetos")
    elif not mudados:
        print("nada a mover (ja aplicado)")
    return mudados


def demo():
    mapa, grade, largura, altura = carrega()
    vistos = alcancaveis(grade, largura, altura)
    assert WARP_DE_ENTRADA in vistos, "o warp de entrada tem que estar na busca"
    assert len(vistos) > 100, f"busca pequena demais: {len(vistos)}"

    # A agua nunca entra na busca a pe: e o que separa este mapa em duas ilhas.
    agua = [p for p in vistos if elevacao(grade, largura, *p) == 1]
    assert not agua, f"a busca a pe entrou na agua: {agua[:3]}"

    # Todo destino escolhido tem que ser terra alcancavel, senao mover nao
    # conserta nada.
    for origem, destino in DESTINOS.items():
        assert destino in vistos, f"destino {destino} nao alcancavel"
        assert elevacao(grade, largura, *destino) != 1, \
            f"destino {destino} esta na agua"

    # Contraprova: um destino no meio do lago tem que ser recusado. Sem isto o
    # teste passaria mesmo com a tabela inteira errada.
    assert (36, 32) not in vistos, "o meio do lago nao pode ser alcancavel"

    objetos = mapa["object_events"]
    ocupados = {(o["x"], o["y"]) for o in objetos}
    cena = [o for o in objetos if "MAGMA" in o["graphics_id"]]
    assert len(cena) == 5, f"a cena tem 5 objetos, achei {len(cena)}"

    faltando = [(o["x"], o["y"]) for o in cena
                if not encostado((o["x"], o["y"]), vistos, ocupados)]
    if faltando:
        print(f"demo: cena AINDA inalcancavel em {faltando} "
              "(rode --aplica)")
    else:
        print("demo ok (5 de 5 da cena encostados em terra alcancavel)")
    return not faltando


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    elif "--aplica" in sys.argv:
        relatorio(aplica=True)
        demo()
    else:
        relatorio(aplica=False)
