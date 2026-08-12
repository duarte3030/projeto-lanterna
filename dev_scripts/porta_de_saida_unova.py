#!/usr/bin/env python3
"""Troca o comportamento das portas de SAÍDA que ficam no meio do mapa,
de `MB_NON_ANIMATED_DOOR` para `MB_SOUTH_ARROW_WARP`.

Uso:
    python3 dev_scripts/porta_de_saida_unova.py --demo    # prova, não grava
    python3 dev_scripts/porta_de_saida_unova.py           # grava (idempotente)
    python3 dev_scripts/porta_de_saida_unova.py --censo   # lista os candidatos

O QUE ESTÁ ERRADO NA CONVERSÃO, medido em 12/08/2026
----------------------------------------------------
`dev_scripts/blockdata_unova.py` manda a classe `porta` do gen 2 para
`MB_NON_ANIMATED_DOOR` (a primeira de `ESPERADO["porta"]`), e o gen 3 trata esse
comportamento de dois jeitos que o interior de Hoenn NÃO tem:

1. ao CHEGAR, `SetUpWarpExitTask` empurra o jogador um tile para o sul, com
   movimento segurado, que ignora colisão e limite de mapa;
2. ao ANDAR, `TryStartWarpEventScript` dispara o warp assim que o jogador PISA
   no tile, vindo de qualquer direção.

O interior de Hoenn usa `MB_SOUTH_ARROW_WARP` (medido: `RustboroCity_Gym`,
metatiles 6 e 7 do `gTileset_Building`), que não empurra e só dispara quando o
jogador aperta PARA BAIXO em cima dele.

O item 1 já está resolvido no motor, em `SetUpWarpExitTask`
(`src/field_screen_effect.c`): quando o tile do empurrão é impassável ou está
fora da grade, a saída passa a ser a sem empurrão. Isso cobre 265 warps em 137
mapas que caíam fora do mapa e outros 187 que caíam dentro de parede.

O item 2 só se resolve no DADO, e é o que esta ferramenta faz. Ele só vira
armadilha quando o tile de porta é a ÚNICA ligação entre a sala de chegada e o
resto do mapa: aí o jogador pisa nele para atravessar e volta para a rua.

POR QUE SÓ DUAS ENTRADAS AQUI, E NÃO A CLASSE INTEIRA
-----------------------------------------------------
A varredura completa está no `--censo`, e ela diz o tamanho do problema: de 470
metatiles de porta usados por warp no repo, **196 (558 warps)** têm o tile do
NORTE andável em TODOS os seus usos, que é a assinatura de "porta por onde se sai
andando para o sul". Os outros 274 (1000 warps) têm pelo menos um uso com o
norte bloqueado, ou seja são portas de ENTRADA, em que o jogador anda para o
norte contra a porta: para essas, seta sul quebraria a entrada. Um exemplo dos
dois no mesmo tileset: `gTileset_UnovaPkmnLeague` 683 são as quatro salas da
Elite (entra-se andando para o norte, fica como está) e 786/788 são a escada de
volta do salão (sai-se andando para o sul).

Virar os 196 de uma vez é conversão de leva, com rebuild e suíte inteira em cima,
e não fechamento: 558 warps mudam de regra e o único juiz é o emulador. Então
aqui entram só as portas cuja armadilha foi PROVADA no emulador nesta sessão, e
o censo fica escrito para a próxima leva não ter que remedir.

A ARMADILHA PROVADA (T92.6)
---------------------------
`Unova_PkmnLeagueMain` 28x24. O jogador que sobe da entrada nasce em (13,19) ou
(14,19) e a linha 19 só abre em x=6,7,8, x=13,14 e x=19,20,21: (13,19) e (14,19)
são a ÚNICA ligação entre a sala de chegada (linhas 20 a 23) e o salão da Elite.
Com comportamento de porta, andar para o norte ali manda o jogador de volta para
a `PkmnLeagueEntrance`. Isso não aparecia porque a cena `.PkmnLeagueEnter` carrega
o jogador seis passos para dentro; só que ela é PULADA quando
`FLAG_UNOVA_LIGA_VENCIDA` está acesa (`scripts.inc`, `EventScript_Terremoto`).
Ou seja: **depois de ganhar a Liga, o salão ficava inalcançável.** É exatamente o
que o T92.6 foi escrito para provar.

Com seta sul: o jogador nasce em (13,19), atravessa para (13,18) andando, e sai
pisando na porta e apertando PARA BAIXO. A cena passa a andar CINCO passos em vez
de seis, porque a partida subiu um tile (o empurrão sumiu); isso está no
`scripts.inc` do mapa, no mesmo commit.
"""
import json
import os
import struct
import sys
from collections import defaultdict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
import valida_warp_tile as W                                        # noqa: E402

PORTA = W._MB["MB_NON_ANIMATED_DOOR"]
SETA_SUL = W._MB["MB_SOUTH_ARROW_WARP"]

# (tileset, metatile). Só entra aqui porta cuja armadilha foi medida NO
# EMULADOR; o resto do universo está no --censo.
ALVOS = [
    ("gTileset_UnovaPkmnLeague", 786),   # Unova_PkmnLeagueMain (13,19)
    ("gTileset_UnovaPkmnLeague", 788),   # Unova_PkmnLeagueMain (14,19)
]
CORTE = 512   # os tilesets de Unova não são frlg nem johto


def caminho_attr(tileset):
    return f"{W.pasta_do_tileset(tileset)}/metatile_attributes.bin"


def le_attr(tileset, metatile):
    b = open(caminho_attr(tileset), "rb").read()
    i = (metatile - CORTE) * 2
    return struct.unpack("<H", b[i:i + 2])[0]


def grava_attr(tileset, metatile, valor):
    p = caminho_attr(tileset)
    b = bytearray(open(p, "rb").read())
    i = (metatile - CORTE) * 2
    b[i:i + 2] = struct.pack("<H", valor)
    open(p, "wb").write(bytes(b))


def aplica(gravar=True):
    mudou = []
    for tileset, metatile in ALVOS:
        antes = le_attr(tileset, metatile)
        if antes & 0xFF == SETA_SUL:
            continue
        if antes & 0xFF != PORTA:
            raise SystemExit(f"{tileset} metatile {metatile} tem comportamento "
                             f"{antes & 0xFF}, e não {PORTA}: a premissa mudou, "
                             "não vou sobrescrever às cegas.")
        depois = (antes & ~0xFF) | SETA_SUL
        if gravar:
            grava_attr(tileset, metatile, depois)
        mudou.append(f"{tileset} metatile {metatile}: "
                     f"MB_NON_ANIMATED_DOOR -> MB_SOUTH_ARROW_WARP")
    return mudou


def censo():
    """Todo metatile de porta cujos usos como warp têm o NORTE andável."""
    layouts = {l["id"]: l for l in
               json.load(open(f"{RAIZ}/data/layouts/layouts.json"))["layouts"]}
    grupos = json.load(open(f"{RAIZ}/data/maps/map_groups.json"))
    cache = {}

    def attrs(ts):
        if ts not in cache:
            cache[ts] = W.tabela_de_atributos(ts)[0]
        return cache[ts]

    uso = defaultdict(list)
    for grupo, mapas in grupos.items():
        if not isinstance(mapas, list):
            continue
        for nome in mapas:
            p = f"{RAIZ}/data/maps/{nome}/map.json"
            if not os.path.exists(p):
                continue
            mapa = json.load(open(p))
            lay = layouts.get(mapa["layout"])
            if not lay:
                continue
            prim, sec = attrs(lay.get("primary_tileset")), attrs(lay.get("secondary_tileset"))
            corte = 640 if lay.get("layout_version", "") in ("frlg", "johto") else 512
            w, h = lay["width"], lay["height"]
            b = open(f"{RAIZ}/{lay['blockdata_filepath']}", "rb").read()

            def blk(x, y, _b=b, _w=w):
                return struct.unpack("<H", _b[(y * _w + x) * 2:(y * _w + x) * 2 + 2])[0]

            for wp in mapa.get("warp_events", []):
                x, y = wp["x"], wp["y"]
                if not (0 <= x < w and 0 <= y < h):
                    continue
                mid = blk(x, y) & 0x3FF
                if mid < corte:
                    comp, ts = (prim[mid] if prim and mid < len(prim) else None), lay.get("primary_tileset")
                else:
                    i = mid - corte
                    comp, ts = (sec[i] if sec and i < len(sec) else None), lay.get("secondary_tileset")
                if comp != PORTA:
                    continue
                norte = y > 0 and not ((blk(x, y - 1) >> 10) & 3)
                uso[(ts, mid)].append((nome, x, y, norte))
    bons = {k: l for k, l in uso.items() if all(u[3] for u in l)}
    print(f"metatiles de porta usados por warp: {len(uso)}")
    print(f"  candidatos a seta sul (norte andável em TODOS os usos): "
          f"{len(bons)} metatiles, {sum(len(l) for l in bons.values())} warps")
    print(f"  portas de entrada (algum uso com o norte bloqueado): "
          f"{len(uso) - len(bons)} metatiles, "
          f"{sum(len(l) for k, l in uso.items() if k not in bons)} warps")
    print(f"  já aplicados por esta ferramenta: {len(ALVOS)}")
    return 0


def demo():
    falhas = []
    guardados = {(t, m): le_attr(t, m) for t, m in ALVOS}
    try:
        # (a) mutação plantada: devolve tudo para porta e exige o conserto
        for (t, m), _ in guardados.items():
            grava_attr(t, m, (le_attr(t, m) & ~0xFF) | PORTA)
        primeira = aplica()
        if len(primeira) != len(ALVOS):
            falhas.append(f"a mutação plantada não foi consertada: {primeira}")
        for t, m in ALVOS:
            if le_attr(t, m) & 0xFF != SETA_SUL:
                falhas.append(f"{t} {m} ficou com {le_attr(t, m) & 0xFF}")
        # (b) idempotência
        if aplica():
            falhas.append("não é idempotente")
        # (c) contraprova: recusa mexer em metatile que não é porta
        t, m = ALVOS[0]
        grava_attr(t, m, (le_attr(t, m) & ~0xFF) | W._MB["MB_NORMAL"])
        try:
            aplica()
        except SystemExit:
            pass
        else:
            falhas.append("aceitou sobrescrever um metatile que não era porta")
    finally:
        for (t, m), v in guardados.items():
            grava_attr(t, m, v)
    for f in falhas:
        print(f"[FALHA] {f}")
    if not falhas:
        print("demo OK: mutação plantada consertada, idempotente, e recusa "
              "metatile que não é MB_NON_ANIMATED_DOOR.")
    return 1 if falhas else 0


if __name__ == "__main__":
    if "--demo" in sys.argv:
        sys.exit(demo())
    if "--censo" in sys.argv:
        sys.exit(censo())
    for linha in aplica() or ["nada a fazer (já estava aplicado)"]:
        print(linha)
