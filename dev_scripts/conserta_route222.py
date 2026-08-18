#!/usr/bin/env python3
"""Religa a estrada NORTE de Valor para a Route 222, que morria em 4 tiles.

Uso:
    python3 dev_scripts/conserta_route222.py --demo    # so se prova, nao grava
    python3 dev_scripts/conserta_route222.py           # grava (idempotente)

O QUE ESTAVA ERRADO, medido em 18/08/2026 no `data/layouts/Route222/map.bin`
---------------------------------------------------------------------------
O `PLANO-OBRAS-SINNOH.md` (onda 5) registrou a pendencia assim: "nenhuma das
entradas do lado de Valor (coluna x=0) alcanca a coluna x=91, que e a borda de
Sunyshore". A medicao esta certa e a CONCLUSAO estava errada, e as duas coisas
importam:

- **A coluna 91 nao e a estrada.** A Route 222 chega em Sunyshore por WARP, pelo
  portao: `Route222` warp 0 em (89,23) -> `Route222_Access` -> warp 1 em (11,5)
  -> `SunyshoreCity` (4,48). Os tres disparam (`valida_warp_tile.py`: os warps
  da Route222 estao entre os 97,7% que funcionam). A borda direita do layout so
  tem terra em (91,13) e (91,14), um bolso de DOIS tiles que a fonte desenha
  como anel decorativo, e do outro lado da costura a coluna x=0 de
  `SunyshoreCity` e agua ou parede em TODAS as linhas (medido: sy=0..13 e
  sy=55..63 elevacao 1, o resto colisao 1). Abrir a coluna 91 nao levaria a
  lugar nenhum.
- **A estrada QUE EXISTE estava partida, e por elevacao, nao por colisao.** Das
  11 entradas da coluna x=0, seis (y=4,7,10,21,22,23,24,25) caem na regiao
  grande de 1139 tiles, que contem o portao (89,23). Mas so DUAS delas tem
  vizinho andavel do lado de Valor: (55,39) -> y=3 e (55,57..61) -> y=21..25
  (as outras, (55,43) e (55,46) e (55,63), nem sao alcancaveis dentro do proprio
  ValorLakefront). E dessas duas:
    * a do SUL (y=21..25) e a que o Collector tranca. O bloqueio nao desarma
      neste porte: quem escreve `VAR_SINNOH_VALOR_BLOQUEIO_SUNYSHORE = 1` na
      fonte e a cena pos-8a insignia do laboratorio de Sandgem, que nao foi
      portada (esta dito em data/maps/ValorLakefront/scripts.inc e no plano);
    * a do NORTE (y=3), que o proprio scripts.inc do ValorLakefront diz que
      "fica aberta" de proposito, caia num BOLSO DE 4 TILES: (0,3),(1,3),(2,3),
      (3,3), elevacao 3, com a regiao grande logo abaixo em elevacao 4.
      `IsElevationMismatchAt` (src/event_object_movement.c:10010) barra 3 contra
      4 sem nada aparecer na colisao (licao 6 do ESTADO 0.e), entao o jogador
      entrava pela estrada norte, andava tres tiles e batia numa parede que nao
      existe no desenho.

  Somando: **Sunyshore ficava inalcancavel a pe vindo de Valor.**

O CONSERTO, e por que e este
----------------------------
A grade de permissao da fonte (pokeplatinum, `map_data_149/150/151.bin`, as tres
celulas de `MAP_HEADER_ROUTE_222` na matriz, alinhadas com o nosso layout em
dx=0 / dy=+2, 81,7% de acordo na mascara de bloqueio) nao tem elevacao por tile:
as tres celulas tem `altitudes` = 0, ou seja a Route 222 da fonte e UM nivel so,
e a coluna x=2 desce da entrada norte ate a praia sem degrau nenhum. A elevacao
4 da metade oeste e invencao do redesenho a mao que importou este mapa (commit
f97a18dc82), e ela CASA com o ValorLakefront do outro lado da costura em
y=21..25, entao apagar a elevacao 4 quebraria a estrada sul. Reconverter o
blockdata inteiro pela fonte tambem esta fora: perderia a arte, os dois warps de
casa (predio da gen 4 e modelo 3D, a grade so entrega buraco bloqueado) e os 23
object_events, e a licao do ESTADO 0.e e exatamente essa ("gerador que nao sabe
o que a mao decidiu desfaz a decisao calado").

Entao o conserto e o degrau, e usa o IDIOMA QUE O PROPRIO MAPA JA TEM: os tiles
de `ELEVATION_TRANSITION` (elevacao 0) que ele ja usa em (21,10), (21,11),
(21,19), (21,20), (39,10), (39,11), (81,18) e (81,19) para costurar a elevacao 4
com a 3. Os tres tiles da linha 3 que tem vizinho andavel logo abaixo passam a
ser elevacao 0:

    (0,3) (1,3) (2,3)   elevacao 3 -> 0

Metatile e colisao ficam intactos: so a elevacao muda, entao o desenho na tela e
o mesmo. Elevacao 0 vale NOS DOIS SENTIDOS por construcao do motor: quem chega
de Valor (55,39), elevacao 3, entra; quem sobe da regiao de elevacao 4 pisa no
tile de transicao, fica com `currentElevation` 0, e ai
`IsElevationMismatchAt(0, ...)` devolve FALSE para qualquer destino, inclusive a
volta para a elevacao 3 do ValorLakefront.

O QUE ESTE CONSERTO NAO FAZ, e esta aberto de proposito
--------------------------------------------------------
- **Nao mexe na coluna 91.** Continua sendo um bolso de 2 tiles, e continua sem
  destino do lado de Sunyshore. Se um dia a costura de mapa tiver que valer, o
  trabalho e do lado de SunyshoreCity (abrir terra na coluna x=0), nao daqui.
- **Nao abre a estrada sul.** Ela e trancada de proposito pelo Collector, e o
  desarme mora numa cena que este porte nao tem.
- **Nao religa (0,27)**, um corredor de praia de 22 tiles que a fonte tem
  colado na praia grande (linha 24 da fonte, x=0..20) e o redesenho separou com
  uma parede na nossa linha 26. Ninguem o alcanca por dentro do ValorLakefront
  ((55,63) nao e alcancavel la), entao abrir 21 tiles de parede seria arte nova
  sem estrada atras.
- **Nao mexe nas placas de (81,16), (54,16) e (65,16)**, que estao sem tile de
  leitura embaixo. Sao bg_events, defeito anterior e de outra familia.
"""
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TRANSICAO = 0  # ELEVATION_TRANSITION, o mesmo valor de (21,10) e irmaos

# (layout, x, y, elevacao nova). Metatile e colisao ficam como estao.
TILES = [
    ("LAYOUT_ROUTE222", 0, 3, TRANSICAO),
    ("LAYOUT_ROUTE222", 1, 3, TRANSICAO),
    ("LAYOUT_ROUTE222", 2, 3, TRANSICAO),
]
# Por que exatamente estes tres, e nao a linha 3 inteira: (3,3) e o quarto tile
# do bolso e o vizinho de baixo dele, (3,4), e parede. Tile de transicao so
# serve onde ha degrau para costurar; em (3,3) seria enfeite.


def layouts():
    return {l["id"]: l for l in
            json.load(open(f"{RAIZ}/data/layouts/layouts.json"))["layouts"]}


def le_palavra(lay, x, y):
    b = open(f"{RAIZ}/{lay['blockdata_filepath']}", "rb").read()
    i = (y * lay["width"] + x) * 2
    return struct.unpack("<H", b[i:i + 2])[0]


def grava_palavra(lay, x, y, palavra):
    caminho = f"{RAIZ}/{lay['blockdata_filepath']}"
    b = bytearray(open(caminho, "rb").read())
    i = (y * lay["width"] + x) * 2
    b[i:i + 2] = struct.pack("<H", palavra)
    open(caminho, "wb").write(bytes(b))


def aplica(gravar=True):
    """Devolve a lista do que mudou. Idempotente: rodar de novo devolve []."""
    mudou = []
    tabela = layouts()
    for lid, x, y, nova in TILES:
        lay = tabela[lid]
        antes = le_palavra(lay, x, y)
        depois = (antes & 0x0FFF) | (nova << 12)   # so a elevacao muda
        if antes != depois:
            if gravar:
                grava_palavra(lay, x, y, depois)
            mudou.append(f"{lid} ({x},{y}) elevacao {(antes >> 12) & 0xF} -> {nova}")
    return mudou


# ------------------------------------------------------------------ autoteste

def _grade(lid):
    lay = layouts()[lid]
    W, H = lay["width"], lay["height"]
    b = open(f"{RAIZ}/{lay['blockdata_filepath']}", "rb").read()
    return W, H, [[struct.unpack("<H", b[(y * W + x) * 2:(y * W + x) * 2 + 2])[0]
                   for x in range(W)] for y in range(H)]


def alcance(W, H, g, sementes):
    """Busca em largura com a REGRA DO MOTOR, nao com colisao so.

    Estado e (x, y, elevacao corrente), porque elevacao 0 e transicao: quem pisa
    nela passa a aceitar qualquer destino (IsElevationMismatchAt devolve FALSE
    quando a elevacao do andarilho e 0). Sem o terceiro campo a busca mente nos
    dois sentidos: diz que o degrau nao existe, ou diz que ele e definitivo.
    """
    from collections import deque
    def andavel(v):
        return ((v >> 10) & 3) == 0
    def elev(v):
        return (v >> 12) & 0xF
    vistos, fila = set(), deque()
    for x, y in sementes:
        if andavel(g[y][x]):
            st = (x, y, elev(g[y][x]))
            vistos.add(st)
            fila.append(st)
    while fila:
        x, y, e = fila.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < W and 0 <= ny < H):
                continue
            v = g[ny][nx]
            if not andavel(v):
                continue
            eb = elev(v)
            if e != 0 and eb not in (0, 15) and e != eb:
                continue
            st = (nx, ny, e if eb == 15 else eb)
            if st not in vistos:
                vistos.add(st)
                fila.append(st)
    return {(x, y) for x, y, _ in vistos}


PORTAO = (89, 23)     # warp 0 da Route222, a porta do Route222_Access
NORTE = (0, 3)        # a entrada que vem de ValorLakefront (55,39)


def demo():
    """Prova com MUTACAO PLANTADA: sujo os tres tiles, exijo que a ferramenta
    conserte, exijo que a segunda passada nao mude nada, e exijo o FATO que
    interessa (a entrada norte alcanca o portao) antes e depois."""
    tabela = layouts()
    guardados = {(lid, x, y): le_palavra(tabela[lid], x, y)
                 for lid, x, y, _ in TILES}
    falhas = []
    try:
        # (a) estado plantado: a elevacao velha, 3, que partia a estrada
        for lid, x, y, _ in TILES:
            p = guardados[(lid, x, y)]
            grava_palavra(tabela[lid], x, y, (p & 0x0FFF) | (3 << 12))

        W, H, g = _grade("LAYOUT_ROUTE222")
        if PORTAO in alcance(W, H, g, [NORTE]):
            falhas.append("a premissa mudou: com elevacao 3 na linha 3 a entrada "
                          "norte JA alcancava o portao, entao este conserto "
                          "conserta outra coisa")

        primeira = aplica()
        if len(primeira) != len(TILES):
            falhas.append(f"a mutacao plantada nao foi consertada: {primeira}")

        W, H, g = _grade("LAYOUT_ROUTE222")
        for lid, x, y, nova in TILES:
            v = g[y][x]
            if (v >> 12) & 0xF != nova:
                falhas.append(f"({x},{y}) ficou com elevacao {(v >> 12) & 0xF}")
            if (v >> 10) & 3 != 0 or (v & 0x3FF) != (guardados[(lid, x, y)] & 0x3FF):
                falhas.append(f"({x},{y}): metatile ou colisao foram alterados, "
                              "e este conserto so pode mexer na elevacao")

        # (b) o fato: a entrada norte alcanca o portao, e ele alcanca a norte
        de_norte = alcance(W, H, g, [NORTE])
        if PORTAO not in de_norte:
            falhas.append(f"a entrada norte {NORTE} ainda nao alcanca o portao "
                          f"{PORTAO} ({len(de_norte)} tiles alcancados)")
        if NORTE not in alcance(W, H, g, [PORTAO]):
            falhas.append("a volta nao fecha: do portao nao se chega na entrada "
                          "norte. Degrau tem que valer nos DOIS sentidos.")

        # (c) o que NAO pode ter mudado junto: a estrada sul, que e a outra
        #     entrada boa, e o bolso da coluna 91, que continua bolso.
        if PORTAO not in alcance(W, H, g, [(0, 21)]):
            falhas.append("a estrada sul (0,21) deixou de alcancar o portao")
        if len(alcance(W, H, g, [(91, 13)])) != 2:
            falhas.append("o bolso da coluna 91 mudou de tamanho; ele nao era "
                          "para ser tocado")

        # (d) idempotencia
        segunda = aplica()
        if segunda:
            falhas.append(f"nao e idempotente, a segunda passada mudou: {segunda}")
    finally:
        atual = layouts()
        for (lid, x, y), palavra in guardados.items():
            grava_palavra(atual[lid], x, y, palavra)

    for f in falhas:
        print(f"[FALHA] {f}")
    if not falhas:
        print("demo OK: mutacao plantada consertada, metatile e colisao "
              "preservados, entrada norte alcanca o portao nos dois sentidos, "
              "estrada sul intacta, bolso da coluna 91 intacto, idempotente.")
    return 1 if falhas else 0


if __name__ == "__main__":
    if "--demo" in sys.argv:
        sys.exit(demo())
    for linha in aplica() or ["nada a fazer (ja estava consertado)"]:
        print(linha)
