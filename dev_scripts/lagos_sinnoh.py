#!/usr/bin/env python3
"""Converte o LEITO DRENADO dos tres lagos de Sinnoh, do DS para map.bin.

    python3 dev_scripts/lagos_sinnoh.py            # so mede
    python3 dev_scripts/lagos_sinnoh.py --demo     # autoteste, nao grava
    python3 dev_scripts/lagos_sinnoh.py --aplicar  # escreve map.bin e map.json

POR QUE ESTE ARQUIVO EXISTE, medido em 22/08/2026
--------------------------------------------------
`LakeVerityLowWater`, `LakeAcuityLowWater` e `LakeValorDrained` sao os tres
mapas em que o jogador ENTRA E FICA PRESO, e a fila (`sinnoh:lagos_low_water:
boca_ilhada`) ja tinha medido o porque no fechamento da rodada 7: a boca esta no
metatile 0x207 do `gTileset_CaveSinnoh` (MB_SOUTH_ARROW_WARP), colisao 0 e
ELEVACAO 3, e os ~800 tiles em volta estao na ELEVACAO 1, agua.
`IsElevationMismatchAt` (`src/event_object_movement.c:10014`) barra 3 contra 1,
entao cada passo a pe e recusado.

A causa nao e o mapa da fonte, e a REGRA de conversao. `converte_cavernas_sinnoh.
traduz` foi escrita para caverna de pedra e tem duas linhas que mentem num lago
drenado, as duas conferidas na grade da fonte antes de mexer:

1. **`0x00 sem colisao vira ROCHA.**  Numa caverna aquilo e o vazio atras da
   pedra, que o modelo 3D nem desenha. No `LAKE_VALOR_DRAINED` sao **718 tiles**
   de `TILE_BEHAVIOR_NONE` sem colisao, e ali eles sao o LEITO do lago, o chao
   que o jogo original deixa o jogador atravessar.
2. **`PUDDLE` (0x16) e `SHALLOW_WATER` (0x17) viram AGUA de elevacao 1.**  No
   Platinum os dois sao ANDAVEIS: e a lama rasa da margem. Sao **213 tiles** no
   Verity e o caminho inteiro da boca para o leito.

Aqui a regra e a do lago, e sai da mesma grade
-----------------------------------------------
`res/field/maps/data/map_data_NNN.bin`, u16 por tile, bit 15 = colisao e bits
0..7 = `TileBehavior`. Traducao, com o numero de cada faixa medido no dia:

| fonte                                   | nosso              |
|-----------------------------------------|--------------------|
| colisao                                 | rocha (753/761)    |
| `WATER_RIVER`/`WATERFALL`/`WATER_SEA`   | agua, elevacao 1   |
| `NONE`, `TALL_GRASS`, `PUDDLE`,         | chao, elevacao 3   |
| `SHALLOW_WATER`, `SNOW_*`, `WARP_*`     |                    |
| `WARP_*`                                | boca (metatile 519)|

Agua continua agua de proposito: no Platinum o Lago Verity com a agua baixa
ainda tem **587 tiles** de `WATER_SEA` e o Acuity **800**, e quem quiser
atravessar usa Surf, exatamente como la. O que muda e que agora existe margem
seca ligando a boca ao leito.

O WARP ANDA PARA A COORDENADA DA FONTE
---------------------------------------
Os nossos tres warps nasceram fora do lugar (Verity em (39,47) contra (46,54) da
fonte; Acuity em (20,43) contra (15,50)), e a conversao velha os plantou no meio
da pedra. Como o mapa inteiro esta sendo redesenhado pela grade da fonte, o warp
vai junto para a coordenada dela. **Indice de warp nao se mexe** (a save guarda
indice, nao coordenada), so o x/y de cada um, e o `dest_warp_id` fica intocado.

O PORTAO
--------
Depois de escrever, uma busca em largura com a REGRA DO MOTOR (a mesma
`conserta_route222.alcance`, que carrega elevacao) sai de cada warp e conta
quantos tiles o jogador alcanca A PE. Mapa que nao ganhar leito andavel de
verdade REPROVA e nada e escrito: o criterio de aceite da fila e "converter o
leito e SO ENTAO medir a conectividade", nao "escrever e torcer".
"""
import json
import os
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import conserta_route222 as R222            # noqa: E402  BFS com regra de elevacao
import converte_cavernas_sinnoh as CC       # noqa: E402  grade_do_header e as palavras
import importa_npcs_sinnoh as I            # noqa: E402  headers_do_platinum e PLAT

APLICAR = "--aplicar" in sys.argv
DEMO = "--demo" in sys.argv

# Palavras de 16 bits: as MESMAS que o conversor de caverna ja usa, e que os
# tres map.bin de hoje ja carregam (0x2F1 rocha, 0x201 chao, 0x0A1 agua).
CHAO = CC.CHAO            # metatile 513, colisao 0, elevacao 3
AGUA = CC.AGUA            # metatile 161, colisao 0, elevacao 1, MB_POND_WATER
SAIDA = CC.SAIDA          # metatile 519, MB_SOUTH_ARROW_WARP, elevacao 3

# Comportamento da fonte que vira AGUA (elevacao 1, so com Surf). PUDDLE (0x16)
# e SHALLOW_WATER (0x17) NAO estao aqui de proposito: no Platinum sao andaveis.
AGUAS_DE_LAGO = (0x10, 0x13, 0x15)
BOCAS = (0x6C, 0x6D, 0x6E, 0x6F)   # WARP_EAST/WEST/NORTH/SOUTH

LAGOS = {
    "LakeVerityLowWater": "MAP_HEADER_LAKE_VERITY_LOW_WATER",
    "LakeAcuityLowWater": "MAP_HEADER_LAKE_ACUITY_LOW_WATER",
    "LakeValorDrained": "MAP_HEADER_LAKE_VALOR_DRAINED",
}

# Piso de aceite por mapa: tiles alcancaveis A PE a partir de um warp. Sai da
# medida da propria fonte (126, 42 e 662 alcancaveis nela), com folga para baixo
# porque a nossa rocha de duas faces pode comer a beirada.
PISO = 30


def traduz_lago(larg, alt, grade, usadas=None):
    """Grade crua de lago drenado -> lista de palavras do pokeemerald.

    `usadas` sao as coordenadas que vao MESMO receber um warp_event nosso. So
    elas ganham o metatile de boca (519, MB_SOUTH_ARROW_WARP); todo outro
    WARP_* da fonte vira chao comum.

    ISSO NAO E DETALHE, e custou um caso vermelho: a fonte marca DUAS portas
    lado a lado onde o nosso mapa tem UMA (o LakeValorDrained tem WARP_EAST em
    (52,10) e (52,11) e so um warp_event). Pintando as duas de boca, o tile
    (52,11) ficava com comportamento de seta de warp SEM warp_event embaixo, e
    o motor mandava o jogador para o VALOR_LAKEFRONT assim que ele pisasse
    nela: o T157.4 saiu do mapa no segundo aperto. Seta de warp sem warp e
    armadilha, nao decoracao.
    """
    usadas = set() if usadas is None else set(usadas)
    def anda(i):
        v = grade[i]
        return not (v & 0x8000)      # sem colisao E andavel, inclusive 0x00

    saida = []
    for y in range(alt):
        for x in range(larg):
            i = y * larg + x
            if anda(i):
                beh = grade[i] & 0xFF
                saida.append(SAIDA if (x, y) in usadas else
                             AGUA if beh in AGUAS_DE_LAGO else CHAO)
                continue
            abaixo = y + 1 < alt and anda(i + larg)
            base = CC.ROCHA_FACE if abaixo else CC.ROCHA_TOPO
            esq = x > 0 and anda(i - 1)
            dir_ = x + 1 < larg and anda(i + 1)
            if esq and not dir_:
                base -= 1
            elif dir_ and not esq:
                base += 1
            saida.append(base)
    return saida


def bocas_da_fonte(larg, alt, grade):
    """Coordenadas de WARP_* na grade da fonte, na ordem de leitura."""
    return [(x, y) for y in range(alt) for x in range(larg)
            if not (grade[y * larg + x] & 0x8000)
            and (grade[y * larg + x] & 0xFF) in BOCAS]


def alcance_a_pe(larg, alt, palavras, sementes):
    g = [[palavras[y * larg + x] for x in range(larg)] for y in range(alt)]
    return R222.alcance(larg, alt, g, sementes)


def plano():
    layouts = {l["id"]: l for l in json.load(
        open(os.path.join(REPO, "data/layouts/layouts.json")))["layouts"]}
    saida = []
    for mapa, header in LAGOS.items():
        pm = os.path.join(REPO, "data/maps", mapa, "map.json")
        d = json.load(open(pm))
        L = layouts[d["layout"]]
        larg, alt, grade = CC.grade_do_header(header)
        assert (larg, alt) == (L["width"], L["height"]), (
            f"{mapa}: a matriz da fonte e {larg}x{alt} e o nosso layout e "
            f"{L['width']}x{L['height']}; sem isso a conversao seria de outro mapa")
        bocas = bocas_da_fonte(larg, alt, grade)
        # O warp anda para a boca da fonte que leva AO MESMO DESTINO, nunca por
        # ordem de indice: no LakeValorDrained o nosso warp 1 vai para a
        # VALOR_CAVERN e a boca de indice 1 da fonte e a segunda porta do
        # lakefront, entao casar por ordem trocaria as duas portas de lugar.
        # Sem destino igual, cai para a ordem, e sem boca sobrando o warp fica
        # onde esta: nunca se inventa lugar.
        porta_de = {}
        fonte_ev = json.load(open(os.path.join(
            I.PLAT, "res/field/events",
            I.headers_do_platinum()[header][0] + ".json")))
        for w in fonte_ev.get("warp_events") or []:
            porta_de.setdefault(w["dest_header_id"], []).append((w["x"], w["z"]))
        warps = d.get("warp_events") or []
        novos, usadas = [], set()
        for i, w in enumerate(warps):
            chave = "MAP_HEADER_" + str(w.get("dest_map", "")).replace("MAP_", "", 1)
            alvo = next((c for c in porta_de.get(chave, []) if c not in usadas), None)
            if alvo is None:
                alvo = next((c for c in bocas if c not in usadas), None)
            if alvo is None:
                alvo = (w["x"], w["y"])
            usadas.add(alvo)
            novos.append(alvo)
        palavras = traduz_lago(larg, alt, grade, novos)
        sementes = [p for p in novos
                    if ((palavras[p[1] * larg + p[0]] >> 10) & 3) == 0]
        viz = alcance_a_pe(larg, alt, palavras, sementes)
        saida.append(dict(mapa=mapa, header=header, larg=larg, alt=alt,
                          caminho=os.path.join(REPO, L["blockdata_filepath"]),
                          palavras=palavras, warps=novos, mapjson=pm, d=d,
                          alcance=len(viz), antes=None))
    return saida


def main():
    total = 0
    for p in plano():
        antigo = open(p["caminho"], "rb").read()
        velho = [antigo[i] | (antigo[i + 1] << 8) for i in range(0, len(antigo), 2)]
        # Alcance de HOJE, com os warps de hoje, para a comparacao ser honesta.
        d = p["d"]
        sem = [(w["x"], w["y"]) for w in (d.get("warp_events") or [])
               if ((velho[w["y"] * p["larg"] + w["x"]] >> 10) & 3) == 0]
        antes = len(alcance_a_pe(p["larg"], p["alt"], velho, sem))
        anda = sum(1 for v in p["palavras"] if ((v >> 10) & 3) == 0)
        print(f"{p['mapa']:22} {p['larg']}x{p['alt']}  andavel {anda:5}  "
              f"alcancavel a pe: {antes} -> {p['alcance']}  warps "
              f"{[(w['x'], w['y']) for w in (d.get('warp_events') or [])]} -> "
              f"{p['warps']}")
        if p["alcance"] < PISO:
            print(f"   REPROVADO: menos de {PISO} tiles a pe, nada escrito")
            return 1
        total += p["alcance"] - antes
        if APLICAR:
            with open(p["caminho"], "wb") as f:
                f.write(b"".join(struct.pack("<H", v) for v in p["palavras"]))
            for w, (x, y) in zip(d.get("warp_events") or [], p["warps"]):
                w["x"], w["y"] = x, y
            json.dump(d, open(p["mapjson"], "w"), indent=2, ensure_ascii=False)
    print(f"\ntiles a pe ganhos: {total}")
    print("aplicado" if APLICAR else "nada escrito (use --aplicar)")
    return 0


def demo():
    """Autoteste: a regra do lago tem que DISCORDAR da regra da caverna.

    Prova vazia seria comparar o resultado com ele mesmo. Aqui o par que
    discrimina e `converte_cavernas_sinnoh.traduz` (a regra velha) contra
    `traduz_lago` (a nova) na MESMA grade: se as duas dessem o mesmo mapa, o
    conserto nao existiria.
    """
    larg, alt, grade = CC.grade_do_header("MAP_HEADER_LAKE_VALOR_DRAINED")
    velha = CC.traduz(larg, alt, grade)
    bocas = bocas_da_fonte(larg, alt, grade)
    nova = traduz_lago(larg, alt, grade, bocas)
    assert len(velha) == len(nova) == larg * alt
    dif = sum(1 for a, b in zip(velha, nova) if a != b)
    assert dif > 500, f"a regra do lago mal muda o mapa ({dif} tiles)"
    anda_v = sum(1 for v in velha if ((v >> 10) & 3) == 0)
    anda_n = sum(1 for v in nova if ((v >> 10) & 3) == 0)
    assert anda_n > anda_v + 600, (
        f"leito nao abriu: andaveis {anda_v} -> {anda_n}")
    # A boca da fonte tem que virar tile de saida, e nao rocha.
    for x, y in bocas_da_fonte(larg, alt, grade):
        assert nova[y * larg + x] == SAIDA, f"boca ({x},{y}) nao virou saida"
    # E o jogador tem que sair da boca: alcance a pe maior que UM tile, que e
    # exatamente o defeito medido na fila.
    sementes = bocas
    assert len(alcance_a_pe(larg, alt, nova, sementes)) > PISO
    # boca SEM warp_event nosso nao pode ficar com seta de warp: prova de que a
    # armadilha do T157.4 nao volta.
    so_uma = traduz_lago(larg, alt, grade, bocas[:1])
    for x, y in bocas[1:]:
        assert so_uma[y * larg + x] != SAIDA, (
            f"({x},{y}) virou seta de warp sem warp_event embaixo")
    # E o LakeVerityLowWater e a prova do defeito da fila: com a regra velha,
    # sair da boca alcanca UM tile, o proprio.
    lv, av, gv = CC.grade_do_header("MAP_HEADER_LAKE_VERITY_LOW_WATER")
    bv = bocas_da_fonte(lv, av, gv)
    assert len(alcance_a_pe(lv, av, CC.traduz(lv, av, gv), bv)) <= 2, (
        "a regra velha nao prendia ninguem no Verity: o defeito nao era este")
    assert len(alcance_a_pe(lv, av, traduz_lago(lv, av, gv, bv), bv)) > 100
    print("demo ok")
    return 0


if __name__ == "__main__":
    sys.exit(demo() if DEMO else main())
