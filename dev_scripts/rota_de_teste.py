#!/usr/bin/env python3
"""Calcula e SIMULA o roteiro de um caso de suíte antes de gastar emulador.

Nasceu na onda 4 da frente C, em 11/09/2026, de duas rodadas vermelhas que não
eram bug do jogo:

1. **A rota atravessava o quadrado de um NPC que anda.** O `object_event` 3 de
   FloaromaTown é `MOVEMENT_TYPE_WANDER_AROUND` com raio 1x1 a partir de (15,28),
   ou seja pode estar em qualquer das nove células do quadrado. O caso passava ou
   falhava conforme o boneco tivesse andado, que é o pior tipo de teste: vermelho
   que não quer dizer nada. Aqui, TODA célula que um NPC que anda pode ocupar é
   tratada como bloqueio na busca.
2. **A conversão de caminho em roteiro perdia passo.** O motor gasta UM aperto só
   para VIRAR quando a direção muda (o primeiro aperto numa direção nova não
   anda), e uma perna que topa em parede para no meio sem avisar. Contar isso de
   cabeça erra; aqui a perna é simulada de volta e a ferramenta RECUSA imprimir
   um roteiro que não chega onde se pediu.

Uso:

    python3 dev_scripts/rota_de_teste.py --mapa TwinleafTown \\
        --de 16,24 --para 5,8 --olhando DOWN --satura DOWN*4

`--de` é onde o jogador COMEÇA (para warp de porta, é um tile ao sul do
`warp_event`, que é o empurrão de chegada de porta). `--satura` acrescenta uma
perna final saturante e diz onde ela para, que é como se prova "isto aqui é
sólido" sem depender de contar toque.

As regras de andar saem do motor, não de palpite: colisão nos bits 10-11 do
`map.bin` (`MAPGRID_COLLISION_MASK`, include/global.fieldmap.h) e elevação nos
bits 12-15, com transição permitida quando as duas são iguais ou uma delas é 0
(a elevação "qualquer").

LIMITE CONHECIDO, e ele é de propósito: a simulação NÃO atravessa conexão de
mapa nem dispara warp. Rota que sai da cidade para a rota vizinha é calculada até
a última célula DE DENTRO, e a perna saturante para na borda; a travessia em si
continua sendo provada no emulador, que é onde ela acontece. Rota que PISA num
`warp_event` também não é simulada além dali, porque o motor teria trocado de
mapa. Quem escreve o caso soma essa perna à mão e confere na foto.
"""
import argparse
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from copia_cidade_fonte import RAIZ, le_layouts, le_blocos

D = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}


class Mapa:
    def __init__(self, nome, com_npc_parado=True):
        with open(os.path.join(RAIZ, "data", "maps", nome, "map.json"),
                  encoding="utf-8") as f:
            self.mj = json.load(f)
        lays = le_layouts(os.path.join(RAIZ, "data/layouts/layouts.json"))["layouts"]
        self.lay = next(l for l in lays if l["id"] == self.mj["layout"])
        self.w, self.h = self.lay["width"], self.lay["height"]
        self.b = le_blocos(os.path.join(RAIZ, self.lay["blockdata_filepath"].lstrip("./")))
        self.occ = set()
        for e in (self.mj.get("object_events") or []):
            t = e["movement_type"]
            rx = e.get("movement_range_x") or 0
            ry = e.get("movement_range_y") or 0
            anda = any(k in t for k in ("WANDER", "WALK", "ROAM"))
            if anda:
                self.occ |= self.alcance_do_npc(e["x"], e["y"], rx, ry)
            elif com_npc_parado:
                self.occ.add((e["x"], e["y"]))

    def alcance_do_npc(self, x0, y0, rx, ry):
        """Onde um NPC que anda PODE estar, pela régua do motor.

        **RAIO ZERO NUM EIXO NÃO QUER DIZER "não anda nesse eixo": quer dizer
        SEM LIMITE nesse eixo.** Está em `IsCoordOutsideObjectEventMovementRange`
        (`src/event_object_movement.c`), lido em 11/09/2026 e não presumido:

            if (objectEvent->range.rangeX != 0) { ...compara left e right... }
            if (objectEvent->range.rangeY != 0) { ...compara top e bottom... }
            return FALSE;

        Com `rangeX` 0 o bloco inteiro é pulado e a coordenada X NUNCA reprova; o
        único freio que sobra é a colisão. A primeira versão desta ferramenta
        lia raio 0 como "uma célula só", e isso custou um vermelho intermitente
        de verdade: o T175.4 desce a coluna 44 de Oreburgh e o `object_event` 13,
        em (43,21) com raio (0,2), pode estar em QUALQUER coluna da faixa
        y=19..23, inclusive na 44. O caso passava quando a mulher estava parada
        e falhava quando ela tinha andado, e a busca dizia que a coluna estava
        livre.

        Então o alcance é: busca em largura a partir da célula inicial, andando
        só por célula andável e respeitando a régua de elevação, com o eixo
        LIMITADO só onde o raio é diferente de zero.
        """
        vistos, fila = {(x0, y0)}, collections.deque([(x0, y0)])
        while fila:
            x, y = fila.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if not (0 <= nx < self.w and 0 <= ny < self.h):
                    continue
                if (nx, ny) in vistos:
                    continue
                if rx and not (x0 - rx <= nx <= x0 + rx):
                    continue
                if ry and not (y0 - ry <= ny <= y0 + ry):
                    continue
                if self.col(nx, ny) != 0:
                    continue
                e1, e2 = self.ele(x, y), self.ele(nx, ny)
                if not (e1 == e2 or e1 == 0 or e2 == 0):
                    continue
                vistos.add((nx, ny))
                fila.append((nx, ny))
        return vistos

    def col(self, x, y):
        return (self.b[y * self.w + x] & 0x0C00) >> 10

    def ele(self, x, y):
        return (self.b[y * self.w + x] >> 12) & 0xF

    def pode(self, a, b):
        x, y = b
        if not (0 <= x < self.w and 0 <= y < self.h):
            return False
        if self.col(x, y) != 0 or (x, y) in self.occ:
            return False
        e1, e2 = self.ele(*a), self.ele(x, y)
        return e1 == e2 or e1 == 0 or e2 == 0


def busca(m, ini, fim):
    prev = {ini: None}
    fila = collections.deque([ini])
    while fila:
        c = fila.popleft()
        if c == fim:
            break
        for d in D:
            n = (c[0] + D[d][0], c[1] + D[d][1])
            if n not in prev and m.pode(c, n):
                prev[n] = c
                fila.append(n)
    if fim not in prev:
        return None
    cam, c = [], fim
    while c:
        cam.append(c)
        c = prev[c]
    return cam[::-1]


def pernas(cam):
    """Caminho em pernas, com o aperto a mais de cada virada."""
    out = []
    for a, b in zip(cam, cam[1:]):
        d = next(k for k, v in D.items() if (b[0] - a[0], b[1] - a[1]) == v)
        if out and out[-1][0] == d:
            out[-1][1] += 1
        else:
            out.append([d, 1])
    return [[d, n + 1] for d, n in out]


def anda(m, pos, olhando, pernas_):
    for d, n in pernas_:
        k = n
        if olhando != d:
            olhando = d
            k -= 1
        for _ in range(k):
            n2 = (pos[0] + D[d][0], pos[1] + D[d][1])
            if not m.pode(pos, n2):
                break
            pos = n2
    return pos, olhando


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--mapa", required=True)
    p.add_argument("--de", required=True, metavar="X,Y")
    p.add_argument("--para", required=True, metavar="X,Y")
    p.add_argument("--olhando", default="DOWN", choices=sorted(D))
    p.add_argument("--satura", metavar="DIR*N",
                   help="perna final saturante, ex.: DOWN*4")
    p.add_argument("--espera", type=int, default=180,
                   help="quadros de NADA no começo e no fim")
    args = p.parse_args()

    m = Mapa(args.mapa)
    ini = tuple(int(v) for v in args.de.split(","))
    fim = tuple(int(v) for v in args.para.split(","))
    cam = busca(m, ini, fim)
    if cam is None:
        print(f"SEM ROTA de {ini} a {fim} em {args.mapa} com os NPC que andam "
              f"tratados como bloqueio ({len(m.occ)} células)")
        return 1
    ps = pernas(cam)
    chegou, olhando = anda(m, ini, args.olhando, ps)
    if chegou != fim:
        print(f"RECUSO: o roteiro derivado para em {chegou}, e não em {fim}. "
              f"A conversão de caminho em perna perdeu passo; peça outro alvo.")
        return 1
    texto = ",".join(f"24:{d}*{n}" for d, n in ps)
    print(f"chega em {fim} em {len(cam) - 1} passos, {len(ps)} pernas")
    if args.satura:
        d, n = args.satura.split("*")
        parou, _ = anda(m, chegou, olhando, [[d, int(n)]])
        print(f"perna saturante {args.satura}: para em {parou}")
        texto += f",120:NADA,24:{d}*{n}"
    print(f'  "roteiro": "{args.espera}:NADA,{texto},{args.espera}:NADA",')
    return 0


if __name__ == "__main__":
    sys.exit(main())
