#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Devolve a MECÂNICA que o redesenho de Kanto apagou, onde a arte é a mesma coisa.

    python3 dev_scripts/mecanica_ikarus_kanto.py            # só mede e relata
    python3 dev_scripts/mecanica_ikarus_kanto.py --aplicar  # escreve os atributos
    python3 dev_scripts/mecanica_ikarus_kanto.py --demo     # autoteste, exit 1 se cair

O QUE ESTA FERRAMENTA CONSERTA
------------------------------
A troca de arte de 11/09/2026 (Ikarus' Tileset Patch FR v3.2) trocou o `map.bin`
de 109 layouts de Kanto e os `metatile_attributes.bin` de 23 tilesets. A seção
0.ag do ESTADO mediu, célula a célula, o que isso apagou de COMPORTAMENTO, e
deixou a lista para a onda 3. Esta ferramenta fecha a parte da lista em que a
arte NOVA, na MESMA célula, continua sendo a mesma coisa: escada é escada,
piscina de fonte termal é piscina, fachada de Centro Pokémon é fachada de Centro
Pokémon, chão de cânion é chão de cânion.

A REGRA QUE DECIDE, e ela é dupla
---------------------------------
Um comportamento só volta quando as DUAS provas passam:

 1. **Censo de uso**, medido nos 166 layouts VIVOS de Kanto (os 178 que usam o
    `gTileset_General_Frlg` menos os 12 que não têm mapa nenhum: os quatro
    `LAYOUT_RS_*` e os oito `LAYOUT_PROTOTYPE_SEVII_ISLE_*`, sobras de Ruby e do
    protótipo que o jogo nunca carrega). O metatile NOVO tem de ser usado quase
    só onde o comportamento existia: 85% das células dele, no mínimo. Metatile
    compartilhado com chão comum fica de fora, porque mexer no atributo dele
    mudaria regra em centenas de células que NUNCA tiveram o comportamento.
 2. **Olho no desenho**, no render do metatile e no render do mapa em volta. A
    prova 1 sozinha ENGANA, e foi medido: o `gTileset_IndigoPlateau` mt656 é
    100% puro (13 de 13 células eram `MB_SHALLOW_WATER`) e o desenho novo da
    Route 23 no lugar é AREIA SECA do caminho do posto de insígnia. Devolver
    água ali seria repintar a regra por cima do desenho aprovado, que é o erro
    da seção 0.ae. Ficou de fora.

O QUE VOLTA (449 células, 30 metatiles em 8 tilesets)
-----------------------------------------------------
  `MB_ROCK_STAIRS`   265 células. O motor anda DEVAGAR na escada de pedra
      (`SLOW_MOVEMENT_ON_STAIRS`, src/field_player_avatar.c). O desenho novo é
      escada de pedra cinza com corrimão azul, conferida no render das ilhas
      Sevii, da Safari e da Cerulean Cave.
  `MB_MOUNTAIN_TOP`   91 células. Decide o CENÁRIO DA BATALHA
      (`BATTLE_ENVIRONMENT_MOUNTAIN`, src/battle_setup.c) e o terreno do DexNav.
      O desenho novo é o chão de cânion do Sevault e do Mt. Ember.
  `MB_HOT_SPRINGS`    37 células. Faz o vapor subir aos pés do jogador
      (`GROUND_EFFECT_FLAG_HOT_SPRINGS`) e PROÍBE correr
      (`MetatileBehavior_IsRunningDisallowed`). O desenho novo é a mesma piscina
      da Ember Spa, água clara com bolha de vapor.
  `MB_POKEMON_CENTER_SIGN`  30 células e `MB_POKEMART_SIGN` 26. O jogador que
      anda para o NORTE contra a fachada lê a placa do Centro ou da loja
      (`TrySetUpWalkIntoSignpostScript`, src/field_control_avatar.c). O desenho
      novo é a mesma fachada, e o Ikarus só trocou o número do metatile.

O QUE FICA COMO REDESENHO, e por quê (2.035 células)
-----------------------------------------------------
  `MB_CYCLING_ROAD_WATER`  750 células, todas da Route 17. Viraram
      `MB_OCEAN_WATER` nos metatiles 405, 406 e 407 do primário, que são o MAR
      de Kanto inteira (1.726 células no 406, das quais 1.053 já eram oceano).
      A única diferença de regra entre os dois é `TILE_FLAG_HAS_ENCOUNTERS`, e
      não existe jeito de devolvê-la sem transformar o mar da região.
  `MB_MOUNTAIN_TOP`  830 células, no `gTileset_General_Frlg` 217, 233, 225, 209,
      216 e companhia: o autor achatou a montanha para o chão comum que ele usa
      em toda Kanto (o 217 sozinho aparece 3.323 vezes, e só 608 delas eram
      montanha).
  `MB_SHALLOW_WATER`  443 células. Duas famílias: o autor secou a água (Route 23
      virou caminho de areia) ou trocou o raso pela PRAIA, com `MB_SAND` nos
      metatiles 389 e 390, que é decisão de desenho dele e tem pegada própria.
  `MB_ROCK_STAIRS`  12 células em metatile que virou chão comum de Cerulean.

A conta fecha: 373 + 1.119 + 37 + 36 + 26 + 751 + 751 perdidas nos layouts
vivos, 449 devolvidas aqui, 2.035 declaradas como redesenho.

O QUE ESTA FERRAMENTA NUNCA FAZ
-------------------------------
Não toca em `map.bin` (o desenho é do autor e foi aprovado na resposta 76), não
toca em colisão nem em elevação, não cria nem apaga metatile, e escreve SÓ os 9
bits baixos da palavra de atributo, deixando terreno, encontro e camada como
estão. Nenhuma flag e nenhuma var; `metatile_attributes.bin` não entra em save.
"""
import os
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import valida_warp_tile as vwt  # noqa: E402

APLICAR = "--aplicar" in sys.argv

# (comportamento, tileset, metatiles GLOBAIS, células que voltam)
# Os índices são globais (o primário vai até 639; o secundário começa em 640),
# como no `map.bin`, para bater com o censo sem conversão no meio.
TABELA = [
    ("MB_HOT_SPRINGS", "gTileset_MtEmber",
     (806, 807, 817, 819, 825), 37),
    ("MB_MOUNTAIN_TOP", "gTileset_SeviiIslands123",
     (707, 712, 713, 880, 881, 923, 1001), 32),
    ("MB_MOUNTAIN_TOP", "gTileset_SeviiIslands67",
     (909, 910, 921, 943, 945, 946, 951, 955, 956, 959, 988), 59),
    ("MB_POKEMART_SIGN", "gTileset_FuchsiaCity", (910,), 1),
    ("MB_POKEMART_SIGN", "gTileset_General_Frlg", (377, 378), 23),
    ("MB_POKEMART_SIGN", "gTileset_SaffronCity", (695,), 2),
    ("MB_POKEMON_CENTER_SIGN", "gTileset_General_Frlg", (441, 442), 30),
    ("MB_ROCK_STAIRS", "gTileset_CeruleanCave", (780, 795, 796), 12),
    ("MB_ROCK_STAIRS", "gTileset_FuchsiaCity", (950, 958), 22),
    ("MB_ROCK_STAIRS", "gTileset_SeviiIslands123", (953, 957, 958, 974), 114),
    ("MB_ROCK_STAIRS", "gTileset_SeviiIslands45", (816, 832, 833), 27),
    ("MB_ROCK_STAIRS", "gTileset_SeviiIslands67",
     (788, 796, 887, 911, 953, 954, 990), 90),
]

CORTE_PRIMARIO = 640   # `GetNumMetatilesInPrimary` no ramo FRLG


def caminho_attr(tileset):
    d = vwt.pasta_do_tileset(tileset)
    return (os.path.join(d, "metatile_attributes.bin"),
            os.path.join(d, "metatiles.bin"))


def aplica():
    """Escreve os 9 bits baixos. Devolve (metatiles mudados, já certos)."""
    mudados, ja = 0, 0
    por_tileset = {}
    for beh, ts, mts, _n in TABELA:
        por_tileset.setdefault(ts, []).extend((beh, mt) for mt in mts)
    for ts, itens in sorted(por_tileset.items()):
        pa, pm = caminho_attr(ts)
        b = bytearray(open(pa, "rb").read())
        n = os.path.getsize(pm) // 16
        if len(b) // n != 4:
            raise SystemExit(f"{ts}: atributo de {len(b)//n} bytes, esperado 4")
        for beh, mt in itens:
            i = mt if mt < CORTE_PRIMARIO else mt - CORTE_PRIMARIO
            if i >= n:
                raise SystemExit(f"{ts}: mt{mt} fora dos {n} metatiles")
            v = struct.unpack_from("<I", b, i * 4)[0]
            novo = (v & ~0x1FF) | vwt._MB[beh]
            if novo == v:
                ja += 1
                continue
            struct.pack_into("<I", b, i * 4, novo)
            mudados += 1
        if APLICAR:
            with open(pa, "wb") as f:
                f.write(bytes(b))
    return mudados, ja


def demo():
    """Autoteste do que a tabela promete, conferido na árvore."""
    falhas = []
    vistos = set()
    for beh, ts, mts, n in TABELA:
        if beh not in vwt._MB:
            falhas.append(f"{beh} não está no enum de metatile_behaviors.h")
            continue
        d = vwt.pasta_do_tileset(ts)
        if not d or not os.path.isdir(d):
            falhas.append(f"{ts}: pasta de tileset não encontrada")
            continue
        pa, pm = caminho_attr(ts)
        tot = os.path.getsize(pm) // 16
        larg = os.path.getsize(pa) // tot
        if larg != 4:
            falhas.append(f"{ts}: atributo de {larg} bytes, esperado 4 (FRLG)")
        for mt in mts:
            if (ts, mt) in vistos:
                falhas.append(f"{ts} mt{mt} aparece duas vezes na tabela")
            vistos.add((ts, mt))
            i = mt if mt < CORTE_PRIMARIO else mt - CORTE_PRIMARIO
            if i >= tot:
                falhas.append(f"{ts}: mt{mt} (local {i}) fora dos {tot}")
        if n <= 0:
            falhas.append(f"{beh}/{ts}: contagem de células {n}")

    # 1. a soma da tabela é a que o ESTADO vai registrar
    if sum(t[3] for t in TABELA) != 449:
        falhas.append(f"soma da tabela é {sum(t[3] for t in TABELA)}, e não 449")

    # 2. idempotência: rodar de novo não muda mais nada
    tab, _ = vwt.tabela_de_atributos("gTileset_General_Frlg")
    if tab is None:
        falhas.append("não deu para ler os atributos do primário de Kanto")

    # 3. nenhum metatile do primário compartilhado entra na tabela por engano:
    #    os únicos do `gTileset_General_Frlg` são os quatro da placa.
    do_primario = sorted(mt for _b, ts, mts, _n in TABELA
                         if ts == "gTileset_General_Frlg" for mt in mts)
    if do_primario != [377, 378, 441, 442]:
        falhas.append(f"metatiles do primário na tabela: {do_primario}")

    if falhas:
        for f_ in falhas:
            print("FALHA:", f_)
        return 1
    print(f"demo OK: {len(TABELA)} linhas, {len(vistos)} metatiles, "
          f"{sum(t[3] for t in TABELA)} células")
    return 0


def main():
    if "--demo" in sys.argv:
        sys.exit(demo())
    mudados, ja = aplica()
    print(f"metatiles a mudar: {mudados}; já com o comportamento certo: {ja}; "
          f"células alcançadas: {sum(t[3] for t in TABELA)}")
    if not APLICAR:
        print("(nada escrito; use --aplicar)")


if __name__ == "__main__":
    main()
