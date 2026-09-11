#!/usr/bin/env python3
"""Abre as DUAS bocas da HOLLOW CAVE na encosta da Route 45 de Johto.

    python3 dev_scripts/abre_bocas_hollow_cave.py            # so mede e relata
    python3 dev_scripts/abre_bocas_hollow_cave.py --aplicar  # escreve

Por que existe
--------------
A Hollow Cave veio do Liquid Crystal com os tiles de warp que o autor desenhou
DENTRO dela ((34,19) e (5,47) sao MB_SOUTH_ARROW_WARP), mas o lado de CA, a
Route 45, nao tinha nenhuma boca livre: a varredura de 11/09/2026 achou em toda
Johto uma unica entrada de caverna orfa, a de Route45 (39,53), e ela esta numa
bolsa de 15 celulas que nenhum caminho alcanca. Sem abrir boca, a caverna so
entraria por NPC guia, que e molde de BARCO e nao de caverna.

O que ele faz, e por que e barato
---------------------------------
Ele troca a palavra de 16 bits de DOIS tiles de parede da Route 45 pela palavra
da boca de caverna que o proprio mapa ja usa nas duas entradas da DARK CAVE:
`0x30A9`, ou seja metatile 169, colisao 0 e elevacao 3. O metatile 169 mora no
PRIMARIO `gTileset_JohtoGeneral`, que a Route 45 ja carrega, entao a boca custa
ZERO byte de arte: nenhum tile, nenhum metatile e nenhuma paleta entram.

A palavra e COPIADA do warp 0 da propria Route 45, em (14,4), e nao escolhida de
cabeca: desenho, colisao, elevacao e comportamento ja sao os de uma entrada que
o motor aceita neste mapa.

Onde as bocas nascem, e a regra que os dois pontos cumprem
----------------------------------------------------------
O criterio e o mesmo de `abre_bocas_cavernas_sinnoh.py`: o tile esta BLOQUEADO
hoje, tem chao ANDAVEL logo abaixo (que e por onde se entra numa porta), os
vizinhos de cima, de esquerda e de direita tambem estao bloqueados (e meio de
parede, nao quina de pedra solta) e o chao de baixo esta no componente andavel
que a rota inteira alcanca. Os dois escolhidos:

  (30,30)  base do paredao do meio da encosta, chao de terra em (30,31)
  ( 5,84)  base do paredao do sope sudoeste, grama em (5,85)

Os dois sao de metatile 121, que e a fiada de baixo da parede de rocha ocre da
Route 45, e a boca de (39,53) que o mapa ja tem esta na mesma fiada: o desenho
casa por construcao.

RODAR DUAS VEZES NAO ESTRAGA: o script confere a palavra de ENTRADA antes de
escrever e reconhece a de SAIDA para dizer "ja foi feito".
"""
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPA = "data/layouts/Route45/map.bin"
LARGURA = 46

PAREDE = 0x0479          # metatile 121, colisao 1: a fiada de baixo do paredao
BOCA = 0x30A9            # metatile 169, colisao 0, elevacao 3: a boca de caverna
BOCAS = [(30, 30), (5, 84)]


def palavra(blob, x, y):
    return struct.unpack_from("<H", blob, (y * LARGURA + x) * 2)[0]


def main(aplicar):
    caminho = os.path.join(RAIZ, MAPA)
    blob = bytearray(open(caminho, "rb").read())
    feitos, pendentes = [], []
    for x, y in BOCAS:
        v = palavra(blob, x, y)
        if v == BOCA:
            feitos.append((x, y))
        elif v == PAREDE:
            pendentes.append((x, y))
        else:
            print("ERRO: (%d,%d) tem 0x%04X, que nao e nem a parede 0x%04X nem a "
                  "boca 0x%04X. Nao escrevo em cima do que nao reconheco."
                  % (x, y, v, PAREDE, BOCA), file=sys.stderr)
            return 1
    for x, y in feitos:
        print("  (%2d,%2d) ja e boca de caverna, nada a fazer" % (x, y))
    for x, y in pendentes:
        abaixo = palavra(blob, x, y + 1)
        print("  (%2d,%2d) parede 0x%04X -> boca 0x%04X (abaixo: 0x%04X, metatile %d)"
              % (x, y, PAREDE, BOCA, abaixo, abaixo & 0x3FF))
    if not pendentes:
        return 0
    if not aplicar:
        print("nada escrito; rode com --aplicar")
        return 0
    for x, y in pendentes:
        struct.pack_into("<H", blob, (y * LARGURA + x) * 2, BOCA)
    open(caminho, "wb").write(bytes(blob))
    print("escrito: %s (%d bytes)" % (MAPA, len(blob)))
    return 0


if __name__ == "__main__":
    sys.exit(main("--aplicar" in sys.argv))
