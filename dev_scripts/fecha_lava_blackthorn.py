#!/usr/bin/env python3
"""Fecha a lava do ginásio de Blackthorn: colisão 0 em elevação 2 vira colisão 1.

Por que existe
--------------
A frente da ponte de Blackthorn (rodada 13, 06/09/2026) mediu e deixou escrito
o que sobrava: **429 células de lava com colisão 0 e elevação 2** no
`data/layouts/BlackthornCity_Gym/map.bin`. Hoje ninguém pisa nelas, e não por
mérito do dado: quem barra é `IsElevationMismatchAt`
(`src/event_object_movement.c:10014`), que recusa o passo entre elevações
diferentes, e o jogador anda em elevação 3. É mina, e não defeito visível:
qualquer ponte nova encostando na lava por uma célula de elevação 0
(`ELEVATION_TRANSITION`, que casa com qualquer vizinho) deixaria o jogador
entrar na elevação 2 e nunca mais sair, porque de 2 não se volta para 3.

`dev_scripts/porta_ginasios_johto.py` LÊ o `map.bin` e nunca o escreve: ele
gera `scripts.inc`. Por isso este conserto é dado, e mora aqui, num arquivo
próprio, idempotente e com `--demo`.

O que ele faz, e o que ele NÃO faz
----------------------------------
Muda só os dois bits de colisão (bits 10 e 11 do u16 do bloco) das células que
têm **colisão 0 E elevação 2**. Metatile e elevação ficam byte a byte iguais,
então nenhum pixel muda e nenhuma regra de camada de desenho é tocada.

As 64 células de ponte que o roteiro abre com `setmetatile` estão em
**colisão 1 e elevação 0**, ou seja fora do recorte: a interseção com o alvo é
vazia, conferida aqui pelo `--demo`. Os três Pokémon de enfeite que ficam em
cima da lava (CHARIZARD 28,20 e DRAGONITE 11,15 em
`MOVEMENT_TYPE_WALK_IN_PLACE_DOWN`, MAGCARGO 28,53 em
`MOVEMENT_TYPE_WANDER_AROUND` com alcance 0) não andam, então fechar a célula
não prende ninguém que se mexia.

Uso
---
    python3 dev_scripts/fecha_lava_blackthorn.py            # mede, não escreve
    python3 dev_scripts/fecha_lava_blackthorn.py --aplica   # escreve o map.bin
    python3 dev_scripts/fecha_lava_blackthorn.py --demo     # autoteste
"""
import argparse
import json
import os
import re
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAYOUT = "LAYOUT_BLACKTHORN_CITY_GYM"
MAPA = "BlackthornCity_Gym"
WARP_CHEGADA = (20, 58)  # o único warp do mapa, e é onde o jogador nasce


def carrega_layout():
    lays = json.load(open(os.path.join(REPO, "data/layouts/layouts.json"),
                          encoding="utf-8"))["layouts"]
    for l in lays:
        if l and l.get("id") == LAYOUT:
            caminho = os.path.join(REPO, l["blockdata_filepath"])
            return l["width"], l["height"], caminho, open(caminho, "rb").read()
    raise SystemExit(f"layout {LAYOUT} não achado")


def bloco(dados, w, x, y):
    """(metatile, colisão, elevação) do bloco em (x, y)."""
    v = struct.unpack_from("<H", dados, 2 * (y * w + x))[0]
    return v & 0x3FF, (v >> 10) & 3, (v >> 12) & 0xF


def alvo(dados, w, h):
    """As células de lava: colisão 0 e elevação 2."""
    return {(x, y) for y in range(h) for x in range(w)
            if bloco(dados, w, x, y)[1] == 0 and bloco(dados, w, x, y)[2] == 2}


def celulas_de_ponte():
    """As células que o roteiro do ginásio abre com `setmetatile`."""
    texto = open(os.path.join(REPO, "data/maps", MAPA, "scripts.inc"),
                 encoding="utf-8").read()
    return {(int(x), int(y)) for x, y, _, _ in re.findall(
        r"setmetatile\s+(\d+),\s*(\d+),\s*(\d+),\s*(TRUE|FALSE)", texto)}


def alcance(dados, w, h, colisao):
    """BFS com a regra do motor: colisão 0 e elevação compatível.

    `IsElevationMismatchAt` deixa passar quando uma das duas pontas é 0
    (transição) ou 15 (multinível); fora disso as elevações têm que ser iguais.
    """
    inicio = WARP_CHEGADA
    vistas, fila = {inicio}, [inicio]
    while fila:
        x, y = fila.pop()
        e0 = bloco(dados, w, x, y)[2]
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < w and 0 <= ny < h) or (nx, ny) in vistas:
                continue
            if colisao(nx, ny) != 0:
                continue
            e1 = bloco(dados, w, nx, ny)[2]
            if e0 != e1 and 0 not in (e0, e1) and 15 not in (e0, e1):
                continue
            vistas.add((nx, ny))
            fila.append((nx, ny))
    return vistas


def fecha(dados, w, celulas):
    """Devolve o map.bin com colisão 1 nas células dadas."""
    novo = bytearray(dados)
    for x, y in celulas:
        pos = 2 * (y * w + x)
        v = struct.unpack_from("<H", novo, pos)[0]
        struct.pack_into("<H", novo, pos, (v & ~(3 << 10)) | (1 << 10))
    return bytes(novo)


def relatorio(aplica=False):
    w, h, caminho, dados = carrega_layout()
    lava = alvo(dados, w, h)
    pontes = celulas_de_ponte()
    print(f"{MAPA} ({w}x{h}): {len(lava)} células de lava "
          f"(colisão 0, elevação 2); {len(pontes)} células de ponte no roteiro")
    if lava & pontes:
        raise SystemExit(f"RECUSADO: {len(lava & pontes)} célula(s) de ponte "
                         f"dentro do alvo; fechar a lava fecharia a passagem")

    def col_base(x, y):
        return bloco(dados, w, x, y)[1]

    def col_pontes(x, y):
        return 0 if (x, y) in pontes else col_base(x, y)

    novo = fecha(dados, w, lava)

    def col_novo(x, y):
        return bloco(novo, w, x, y)[1]

    def col_novo_pontes(x, y):
        return 0 if (x, y) in pontes else col_novo(x, y)

    fechado_a = alcance(dados, w, h, col_base)
    fechado_d = alcance(novo, w, h, col_novo)
    aberto_a = alcance(dados, w, h, col_pontes)
    aberto_d = alcance(novo, w, h, col_novo_pontes)
    print(f"alcance com as pontes FECHADAS: {len(fechado_a)} antes, "
          f"{len(fechado_d)} depois")
    print(f"alcance com as pontes ABERTAS:  {len(aberto_a)} antes, "
          f"{len(aberto_d)} depois")
    if fechado_a != fechado_d or aberto_a != aberto_d:
        raise SystemExit("RECUSADO: o alcance mudou; o conserto não é neutro")
    # A célula ao lado da Clair, no alto do mapa, é o fim da travessia.
    for alvo_clair in ((19, 5), (20, 5)):
        if alvo_clair not in aberto_d:
            raise SystemExit(f"RECUSADO: {alvo_clair} deixou de ser alcançável")
    trocados = sum(1 for y in range(h) for x in range(w)
                   if bloco(dados, w, x, y) != bloco(novo, w, x, y))
    print(f"blocos a mudar: {trocados} (só os bits de colisão; "
          f"metatile e elevação intactos)")
    if not aplica:
        print("nada escrito (use --aplica)")
        return 0
    if novo == dados:
        print("nada a fazer: já está aplicado")
        return 0
    open(caminho, "wb").write(novo)
    print(f"escrito: {caminho}")
    return 0


def demo():
    w, h, _, dados = carrega_layout()
    lava = alvo(dados, w, h)
    pontes = celulas_de_ponte()
    assert not (lava & pontes), "ponte dentro do alvo"
    assert pontes, "nenhuma célula de ponte lida do scripts.inc"
    # idempotência: fechar duas vezes dá o mesmo arquivo, e a segunda passada
    # não acha alvo nenhum.
    um = fecha(dados, w, lava)
    assert alvo(um, w, h) == set(), "sobrou lava aberta depois de fechar"
    assert fecha(um, w, alvo(um, w, h)) == um, "não é idempotente"
    # metatile e elevação intactos
    for y in range(h):
        for x in range(w):
            a, b = bloco(dados, w, x, y), bloco(um, w, x, y)
            assert a[0] == b[0] and a[2] == b[2], f"({x},{y}) mudou de desenho"
    # a mudança é só de colisão, e só nas células do alvo
    mudou = {(x, y) for y in range(h) for x in range(w)
             if bloco(dados, w, x, y) != bloco(um, w, x, y)}
    assert mudou == lava, "mudou célula fora do alvo"
    print(f"demo OK: {len(lava)} células de lava, {len(pontes)} de ponte, "
          f"interseção vazia, desenho intacto, idempotente")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplica", action="store_true")
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()
    return demo() if args.demo else relatorio(args.aplica)


if __name__ == "__main__":
    sys.exit(main())
