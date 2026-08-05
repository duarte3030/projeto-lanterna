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
de Olivine (farol, ginasio e loja) estavam todos em comportamento 0, MB_NORMAL.
Causa: os layouts de Johto declaravam tileset de Sinnoh, entao o id de metatile
que veio da fonte de Johto resolvia para outro tile na tabela de Sinnoh.
Consertado por dev_scripts/importa_tilesets_johto.py; Johto foi a 701 (90,9%).

Placar depois de o corte primario/secundario passar a sair da constante do motor
e nao do tamanho do arquivo (ver a QUARTA ARMADILHA la embaixo):
    Hoenn 91,0%   Johto 90,9%   Sinnoh 86,0%   Unova 78,6%   Kanto 69,9%
Os numeros antigos de Hoenn (49,3%), Sinnoh (70,8%) e Unova (39,4%) eram desta
ferramenta mentindo, nao do jogo.

Terceira vez nesta sessao que a mesma familia de erro aparece: o validador
conferia uma camada mais rasa que a da afirmacao. "O warp existe" nao e "o warp
funciona".
"""
import json
import os
import re
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


# TERCEIRA ARMADILHA, achada em 05/08/2026: a pasta do tileset NAO sai do nome do
# simbolo. `gTileset_Route38Farmland` mora em `secondary/route_38_farmland` e
# `gTileset_TrainerHillCourtyard` mora em `secondary/battle_tower_outer`. A
# conversao CamelCase -> snake_case errava esses casos, `pasta_do_tileset`
# devolvia None e o `continue` la embaixo descartava o mapa INTEIRO sem avisar:
# 27 warps de Johto sumiam da conta em vez de aparecer como problema.
# Agora o caminho vem do proprio INCBIN de src/data/tilesets/metatiles.h, que e
# o mesmo dado que o build usa.
def _mapa_de_pastas():
    mt = open(f"{RAIZ}/src/data/tilesets/metatiles.h").read()
    sym2dir = dict(re.findall(
        r'gMetatiles_(\w+)\[\]\s*=\s*INCBIN_U16\("(data/tilesets/\w+/\w+)/metatiles\.bin"\)',
        mt))
    hdr = open(f"{RAIZ}/src/data/tilesets/headers.h").read()
    fora = {}
    for nome, corpo in re.findall(
            r'const struct Tileset gTileset_(\w+)\s*=\s*\{(.*?)\};', hdr, re.S):
        m = re.search(r'\.metatiles\s*=\s*gMetatiles_(\w+)', corpo)
        if m and m.group(1) in sym2dir:
            fora["gTileset_" + nome] = f"{RAIZ}/{sym2dir[m.group(1)]}"
    return fora


PASTAS = None


def pasta_do_tileset(tileset):
    """gTileset_GeneralSinnoh -> data/tilesets/<sub>/general_sinnoh, ou None."""
    global PASTAS
    if not tileset or tileset == "0":
        return ""
    if PASTAS is None:
        PASTAS = _mapa_de_pastas()
    return PASTAS.get(tileset)


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


PISO_PADRAO = 60  # por cento

# Regioes de verdade, para medir uma a uma. O total nunca chega a 100%: existe
# warp legitimo em tile que nao e porta (o motor tambem entra por script, e
# muita porta de Hoenn e trocada por setmetatile em tempo de execucao). Exigir
# 100% fazia o portao ficar vermelho para sempre, que e o mesmo que nao ter
# portao. O que interessa e catastrofe: Johto estava em 1,6% e ninguem viu.
REGIOES = {"Hoenn": "TownsAndRoutes", "Kanto": "Frlg", "Sinnoh": "Sinnoh",
           "Johto": "Johto", "Unova": "Unova"}


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
    mudos = []   # mapa descartado antes de conferir warp: isso e cegueira, nao zero
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
                mudos.append((m, f"layout {d.get('layout')} nao existe"))
                continue
            bp = f"{RAIZ}/{lay.get('blockdata_filepath', '')}"
            if not os.path.exists(bp):
                mudos.append((m, "sem blockdata"))
                continue
            blk = open(bp, "rb").read()
            w, h = lay["width"], lay["height"]
            prim, n_prim = atributos(lay.get("primary_tileset"))
            seg, _ = atributos(lay.get("secondary_tileset"))
            if prim is None or seg is None:
                falta = lay.get("primary_tileset") if prim is None else lay.get("secondary_tileset")
                mudos.append((m, f"tileset {falta} sem pasta"))
                continue
            # QUARTA ARMADILHA, medida em 05/08/2026. O corte primario/secundario
            # NAO e o tamanho do arquivo do primario: e a CONSTANTE que o motor
            # usa, `GetNumMetatilesInPrimary` (src/fieldmap.c), 512 no Emerald e
            # 640 no ramo grande (FRLG e Johto). Os dois so coincidem quando o
            # primario esta cheio.
            #
            # `gTileset_Building` tem 8 metatiles no arquivo, e e o primario de
            # quase todo interior de Hoenn. Com o corte tirado do arquivo, o
            # metatile 513 virava indice 505 do secundario em vez de indice 1, e
            # o validador acusava "alem da tabela". Eram 723 dos 769 warps que
            # Hoenn aparecia devendo: o jogo estava certo, a medicao e que estava
            # errada. Ler o tamanho do arquivo parecia mais seguro que cravar um
            # numero, e era justamente o contrario.
            versao = lay.get("layout_version", "")
            corte = 640 if versao in ("frlg", "johto") else 512
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

    if "--piso" in sys.argv:
        i = sys.argv.index("--piso")
        piso = int(sys.argv[i + 1]) if len(sys.argv) > i + 1 else PISO_PADRAO
        return abaixo_do_piso(piso)
    if mudos:
        print(f"\n{len(mudos)} mapas NAO conferidos (nao contam como zero, contam "
              f"como cegueira):")
        for m, motivo in mudos[:10]:
            print(f"      {m}: {motivo}")
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


def abaixo_do_piso(piso):
    """Reprova so a regiao que despencou. Devolve 1 se alguma ficou abaixo."""
    import subprocess
    ruins = []
    for nome, chave in REGIOES.items():
        r = subprocess.run([sys.executable, __file__, "--regiao", chave],
                           capture_output=True, text=True)
        m = re.search(r"\(([\d.]+)%\)", r.stdout)
        pct = float(m.group(1)) if m else 0.0
        marca = "ok " if pct >= piso else "ABAIXO"
        print(f"  {marca}  {nome:8s} {pct:5.1f}%")
        if pct < piso:
            ruins.append((nome, pct))
    if ruins:
        print(f"\n{len(ruins)} regiao(oes) abaixo do piso de {piso}%:")
        for n, p in ruins:
            print(f"  {n}: {p:.1f}%")
        return 1
    print(f"\nnenhuma regiao abaixo do piso de {piso}%.")
    return 0


def demo():
    """A resolucao da pasta do tileset e o ponto que quebra calado."""
    # sai do INCBIN, nao de conversao de nome
    assert pasta_do_tileset("gTileset_GeneralSinnoh").endswith(
        "data/tilesets/primary/general_sinnoh")
    assert pasta_do_tileset("gTileset_Petalburg").endswith(
        "data/tilesets/secondary/petalburg")
    # o caso que a conversao CamelCase -> snake_case errava: o digito colado
    assert pasta_do_tileset("gTileset_Route38Farmland").endswith(
        "data/tilesets/secondary/route38_farmland")
    # comportamento de porta entra, MB_NORMAL nao
    assert 104 in COMPORTA_WARP and 0 not in COMPORTA_WARP
    # o corte primario/secundario sai do tamanho do arquivo: 512 no Emerald,
    # 640 nos tilesets de Johto e de FRLG
    assert tabela_de_atributos("gTileset_JohtoGeneral")[1] == 640
    assert tabela_de_atributos("gTileset_GeneralSinnoh")[1] == 512
    # ...mas o corte NAO sai desse numero. gTileset_Building tem 8 metatiles no
    # arquivo e e primario de quase todo interior de Hoenn: o motor continua
    # cortando em 512. Confundir os dois custou 723 falsos positivos.
    assert tabela_de_atributos("gTileset_Building")[1] < 512
    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
