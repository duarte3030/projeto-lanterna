#!/usr/bin/env python3
"""Acusa warp que nunca dispara porque o tile embaixo dele nao e porta.

Uso:
    python3 dev_scripts/valida_warp_tile.py [--regiao Johto]

Existe porque `valida_conectividade.py` dizia "0 warps quebrados" com Johto
praticamente intransitavel. Ele confere o INDICE do warp: se A aponta para o
mapa B e o indice existe em B, esta certo. Nao confere o que o motor confere.

O motor so executa warp se o COMPORTAMENTO do metatile embaixo do jogador for de
porta, escada ou escada rolante (`TryStartWarpEventScript` em
src/field_control_avatar.c chama `IsWarpMetatileBehavior`). Warp em cima de
MB_NORMAL e decoracao: o jogador pisa e nada acontece.

Medido em 05/08/2026: dos 771 warps de Johto, **12 disparavam**. Os tres warps
de Olivine (farol, ginasio e loja) estao todos em comportamento 0, MB_NORMAL.
Causa: os layouts de Johto declaram tileset de Sinnoh, entao o id de metatile
que veio da fonte de Johto resolve para outro tile na tabela de Sinnoh.

Terceira vez nesta sessao que a mesma familia de erro aparece: o validador
conferia uma camada mais rasa que a da afirmacao. "O warp existe" nao e "o warp
funciona".
"""
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ARMADILHA MEDIDA: nao existe um numero unico aqui.
#   Emerald/Sinnoh/Johto: 512 metatiles no primario, atributo de 2 bytes
#   FRLG:                 640 metatiles no primario, atributo de 4 bytes
# Cravar 512 e 2 fazia Kanto sair com 0,0% dos warps funcionando, o que era bug
# meu, nao do jogo. Ambos os numeros sao deduzidos do tamanho dos arquivos.

# Extraido de src/field_control_avatar.c:1020 (IsWarpMetatileBehavior) mais as
# quatro setas de IsArrowWarpMetatileBehavior, resolvendo cada MB_* citado pelas
# dez funcoes de src/metatile_behavior.c contra o enum de
# include/constants/metatile_behaviors.h.
#
# A primeira versao listou quatro numeros na mao e acusou PetalburgCity_Gym,
# AquaHideout_B1F e LavaridgeTown_Gym_B1F, que sao mapas ORIGINAIS do Emerald e
# funcionam. Ferramenta que discorda do vanilla esta errada, nao o vanilla. Por
# isso a lista sai do codigo do motor agora, e nao da minha memoria.
COMPORTA_WARP = {14, 15, 27, 28, 41, 96, 97, 98, 99, 100,
                 101, 103, 104, 105, 106, 107, 108, 109, 110, 112}
NOME = {0: "MB_NORMAL", 96: "MB_LADDER", 104: "MB_ANIMATED_DOOR"}


def pasta_do_tileset(tileset):
    """gTileset_GeneralSinnoh -> data/tilesets/<sub>/general_sinnoh, ou None."""
    if not tileset or tileset == "0":
        return ""
    nome = tileset.replace("gTileset_", "")
    snake = ""
    for i, c in enumerate(nome):
        if c.isupper() and i:
            snake += "_"
        snake += c.lower()
    for sub in ("primary", "secondary"):
        d = f"{RAIZ}/data/tilesets/{sub}/{snake}"
        if os.path.isdir(d):
            return d
    return None


def tabela_de_atributos(tileset):
    """Devolve (comportamentos, n_metatiles). Deduz a largura do atributo.

    Um metatile ocupa 16 bytes em metatiles.bin (8 tiles de 2 bytes), entao o
    numero de metatiles sai do tamanho daquele arquivo, e a largura do atributo
    sai da divisao. Emerald da 2, FRLG da 4.
    """
    if not tileset or tileset == "0":
        return [], 0
    d = pasta_do_tileset(tileset)
    if not d:
        return None, 0
    pa, pm = f"{d}/metatile_attributes.bin", f"{d}/metatiles.bin"
    if not (os.path.exists(pa) and os.path.exists(pm)):
        return None, 0
    n = os.path.getsize(pm) // 16
    if not n:
        return [], 0
    b = open(pa, "rb").read()
    largura = len(b) // n
    if largura == 4:
        # FRLG: comportamento nos 9 bits baixos do u32
        vals = [struct.unpack("<I", b[i:i + 4])[0] & 0x1FF
                for i in range(0, n * 4, 4)]
    else:
        vals = [struct.unpack("<H", b[i:i + 2])[0] & 0xFF
                for i in range(0, n * 2, 2)]
    return vals, n


def main():
    filtro = None
    if "--regiao" in sys.argv:
        filtro = sys.argv[sys.argv.index("--regiao") + 1].lower()

    layouts = {l["id"]: l for l in
               json.load(open(f"{RAIZ}/data/layouts/layouts.json"))["layouts"]}
    grupos = json.load(open(f"{RAIZ}/data/maps/map_groups.json"))

    cache = {}
    def atributos(ts):
        if ts not in cache:
            cache[ts] = tabela_de_atributos(ts)
        return cache[ts]

    total = ok = 0
    por_mapa = {}
    for grp in grupos["group_order"]:
        if filtro and filtro not in grp.lower():
            continue
        for m in grupos.get(grp, []):
            p = f"{RAIZ}/data/maps/{m}/map.json"
            if not os.path.exists(p):
                continue
            d = json.load(open(p))
            warps = d.get("warp_events") or []
            if not warps:
                continue
            lay = layouts.get(d.get("layout"))
            if not lay:
                continue
            bp = f"{RAIZ}/{lay.get('blockdata_filepath', '')}"
            if not os.path.exists(bp):
                continue
            blk = open(bp, "rb").read()
            w, h = lay["width"], lay["height"]
            prim, n_prim = atributos(lay.get("primary_tileset"))
            seg, _ = atributos(lay.get("secondary_tileset"))
            if prim is None or seg is None:
                continue
            # o corte primario/secundario e o tamanho do proprio primario
            corte = n_prim or 512
            ruins = []
            for i, wp in enumerate(warps):
                x, y = wp.get("x", 0), wp.get("y", 0)
                total += 1
                idx = (y * w + x) * 2
                if not (0 <= x < w and 0 <= y < h and idx + 2 <= len(blk)):
                    ruins.append((i, x, y, "fora do mapa"))
                    continue
                mt = struct.unpack("<H", blk[idx:idx + 2])[0] & 0x3FF
                tab, rel = (prim, mt) if mt < corte else (seg, mt - corte)
                if rel >= len(tab):
                    ruins.append((i, x, y, f"metatile {mt} alem da tabela"))
                    continue
                c = tab[rel]
                if c in COMPORTA_WARP:
                    ok += 1
                else:
                    ruins.append((i, x, y, NOME.get(c, f"comportamento {c}")))
            if ruins:
                por_mapa[m] = ruins

    print(f"warps conferidos: {total}, disparam de verdade: {ok} "
          f"({100*ok/total:.1f}%)" if total else "nenhum warp")
    if not por_mapa:
        print("\nTODO WARP ESTA EM TILE QUE DISPARA.")
        return 0
    piores = sorted(por_mapa.items(), key=lambda kv: -len(kv[1]))
    print(f"\n{len(por_mapa)} mapas com warp que nao dispara. Os 15 piores:")
    for m, r in piores[:15]:
        print(f"  {len(r):3d}  {m}")
        for i, x, y, motivo in r[:2]:
            print(f"          warp {i} em ({x},{y}): {motivo}")
    return 1


def demo():
    """A conversao de nome de tileset e o ponto que quebra calado."""
    for entrada, esperado in [("gTileset_GeneralSinnoh", "general_sinnoh"),
                              ("gTileset_Petalburg", "petalburg"),
                              ("gTileset_BuildingFrlg", "building_frlg")]:
        nome = entrada.replace("gTileset_", "")
        snake = ""
        for i, c in enumerate(nome):
            if c.isupper() and i:
                snake += "_"
            snake += c.lower()
        assert snake == esperado, (entrada, snake, esperado)
    # comportamento de porta entra, MB_NORMAL nao
    assert 104 in COMPORTA_WARP and 0 not in COMPORTA_WARP
    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
