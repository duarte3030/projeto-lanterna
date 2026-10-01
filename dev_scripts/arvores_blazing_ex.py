#!/usr/bin/env python3
"""Conserta as árvores de Hoenn em que a arte do Blazing e a colisão do EX discordam.

Bug do playtest de 30/09/2026 (fila de bugs 3): em Lavaridge o jogador anda em
cima do topo florido de uma árvore. A causa e as duas classes estão no
cabeçalho de `dev_scripts/qa/lente_arvores.py`; este script aplica o conserto
que aquela lente cobra, célula a célula, só no `map.bin`:

    A1 (árvore andável)      a célula ganha colisão 1. Metatile, elevação e
                             desenho ficam como estão.
    A2 (mudinha bloqueada)   478 vira 476 e 479 vira 477: o tronco com a ponta
                             da copa de baixo, que é o que o vanilla e o EX
                             desenham nesse índice e o que o Blazing chama de
                             476/477. Colisão e elevação ficam como estão.

Nenhum tileset, evento, warp ou script muda, então a save continua compatível.

Uso:
    python3 dev_scripts/arvores_blazing_ex.py            # só lista
    python3 dev_scripts/arvores_blazing_ex.py --aplicar  # escreve os map.bin
"""
import collections
import os
import struct
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "qa"))

import lente_arvores  # noqa: E402

TRONCO = {478: 476, 479: 477}


def main():
    aplicar = "--aplicar" in sys.argv
    raiz = lente_arvores.comum.RAIZ
    achados, _ = lente_arvores.varre(raiz)
    por_layout = collections.defaultdict(list)
    for a in achados:
        por_layout[a["layout"]].append(a)
    lays = {L["name"]: L for L, _m in lente_arvores.alvos(raiz)[0]}
    for nome, lista in sorted(por_layout.items()):
        L = lays[nome]
        w, v = lente_arvores.celulas(raiz, L)
        for a in lista:
            i = a["y"] * w + a["x"]
            x = v[i]
            if a["regra"] == "A1":
                v[i] = (x & ~(3 << 10)) | (1 << 10)
            else:
                v[i] = (x & ~0x3FF) | TRONCO[x & 0x3FF]
        cont = collections.Counter(a["regra"] for a in lista)
        print("%-34s A1 %3d  A2 %3d" % (nome, cont["A1"], cont["A2"]))
        if aplicar:
            caminho = os.path.join(raiz, L["blockdata_filepath"])
            open(caminho, "wb").write(struct.pack("<%dH" % len(v), *v))
    print("%d célula(s)%s" % (len(achados), ", gravadas" if aplicar else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
