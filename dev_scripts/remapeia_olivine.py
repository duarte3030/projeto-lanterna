#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remapeamento de Olivine para o desenho do Scorched Silver (seção 2 do contrato).

A ferramenta `copia_cidade.py` trouxe a ARTE do mapa `g0m4` do Pokémon Scorched
Silver, byte a byte. O JOGO é nosso, e é este arquivo: cada warp, NPC e placa vai
para o lugar equivalente do desenho novo.

QUAL MAPA É A OLIVINE DELES, E COMO ISSO FOI PROVADO
----------------------------------------------------
A tabela de nomes de seção da ROM (gRegionMapEntries, em 0x6B2AD4) diz que a
seção 11 é "OLIVINE CITY", e o único mapa de cidade com `secao=11` é o `g0m4`,
de 60x54. A conferência não parou aí: os nove warps dele foram lidos da ROM e o
DESTINO de cada um foi aberto, porque telhado não diz função.

    porta       mapa do hack   como se sabe o que é              nosso mapa
    (18,31)     g12m2 14x9     layout de Centro POKéMON, o       PokemonCenter
                               mesmo blockdata 0x4E2680 de 15
                               mapas, um por cidade
    (31,31)     g12m4 11x8     layout de Mart, blockdata         Mart
                               0x4E28D4, 13 mapas
    (14,15)     g8m1  19x18    música 568, a mesma dos oito      Gym
                               ginásios do hack (Azalea g3m3,
                               Ecruteak g4m1, Violet g11m3...)
    (47,28)     g24m79 13x14   seção 85 = "LIGHTHOUSE", seis     Lighthouse
                               andares (g24m79 a g24m85)
    (25,40)     g12m9 19x14    o texto do NPC diz "Welcome to    PortOutside
                               the Olivine City harbor!", e a
                               célula é MB_SOUTH_ARROW_WARP
    (18,22)     g12m0 10x10    casa                              House3
    (33,20)     g12m5 11x8     casa                              House1
    (38,20)     g12m7 11x8     casa                              House2
    (11,31)     g12m6 10x10    casa                              Cafe

A nossa Olivine tem CAFE e o desenho do autor não tem: pela seção 2 do contrato,
o prédio nosso é encaixado no desenho deles. Ele fica na casa de sudoeste, em
(11,31), que é a mais perto da água, porque a fala do NPC do povoamento já dizia
"The CAFE by the water is the best thing in this city". Nenhuma porta do autor
sobrou sem uso, então nenhuma placa `closed` foi preciso.

AS TRÊS CONEXÕES VIRARAM WARP, E O NÚMERO QUE DECIDIU ISSO
-----------------------------------------------------------
A ordem de tentativa da seção 3.2 do contrato manda tentar PRIMEIRO a cidade
inteira no secundário, compartilhando o primário com as rotas. Medido:

    arte da Olivine do Scorched Silver:  350 metatiles, 551 tiles, 86 cores
    orçamento de um secundário:          384 metatiles, 384 tiles,  6 paletas

O gargalo é o TILE, e ele não tem conserto de empacotamento: 551 é o número de
tiles 8x8 DISTINTOS POR CONTEÚDO, antes de qualquer paleta, contra 384 vagas.
Sobram 167 tiles de fora, 143% do orçamento. Os três vizinhos também reprovam a
segunda metade da regra (nenhum usa ZERO metatile do secundário dele: Route39
usa 61, Route40 usa 23 e OlivineCity_PortOutside usa 26), então nem a saída da
Route33 com a Azalea existia aqui.

Logo, regra 3.1: par de tilesets próprio, e toda saída vira WARP, porque
`LoadMapFromCameraTransition` (src/overworld.c:911) recarrega só o tileset
SECUNDÁRIO numa travessia por conexão e a rota vizinha sairia desenhada com o
primário da cidade.

Uso:
    python3 dev_scripts/remapeia_olivine.py            # só mostra o que faria
    python3 dev_scripts/remapeia_olivine.py --aplicar
"""
import argparse
import collections
import json
import os
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPA = os.path.join(REPO, "data/maps/OlivineCity/map.json")
BLOCOS = os.path.join(REPO, "data/layouts/OlivineCity/map.bin")
META_PRI = os.path.join(REPO, "data/tilesets/primary/olivine_city_copia_pri/metatiles.bin")
ATTR_PRI = os.path.join(REPO, "data/tilesets/primary/olivine_city_copia_pri/metatile_attributes.bin")
LARGURA, ALTURA = 60, 54

MB_NORMAL = 0
MB_WEST_ARROW_WARP = 99
MB_NORTH_ARROW_WARP = 100

# Os índices do tileset novo são os que o `copia_cidade.py` gerou nesta rodada.
# Nada aqui é número cravado: cada metatile é LIDO da célula onde o autor o usa.
ONDE_PLACA = (23, 28)    # o quadro de avisos da praça, o único desenho de placa
ONDE_ROOF = (36, 17)     # telhado com MB_NON_ANIMATED_DOOR errado, ver abaixo

# Vagas livres do primário novo: a arte usa 0..349, o tileset tem 640.
# (vaga, célula de onde clonar, comportamento novo). Nenhum pixel é desenhado:
# o metatile é o do autor, byte a byte; só o byte de comportamento muda.
METATILES_NOVOS = [
    (350, (23, 0), MB_NORTH_ARROW_WARP),   # estrada norte, borda esquerda
    (351, (24, 0), MB_NORTH_ARROW_WARP),   # estrada norte, miolo
    (352, (26, 0), MB_NORTH_ARROW_WARP),   # estrada norte, borda direita
    (353, (0, 32), MB_WEST_ARROW_WARP),    # praia oeste, faixa de cima
    (354, (0, 33), MB_WEST_ARROW_WARP),    # praia oeste, areia
]

# Célula -> (vaga do metatile novo, colisão nova ou None).
CELULAS_SAIDA = {
    (23, 0): (350, None), (24, 0): (351, None),
    (25, 0): (351, None), (26, 0): (352, None),
    (0, 32): (353, None), (0, 33): (354, None), (0, 34): (354, None),
}

# Placas do autor a encaixar: célula -> metatile lido de ONDE_PLACA, colisão 1.
# O desenho do autor tem CINCO quadros de avisos, em (12,16) ao lado do ginásio,
# (23,28) no meio da praça, (49,29) ao pé do farol e (35,21) e (40,21) entre as
# duas casas do leste. Os três primeiros recebem as nossas placas de ginásio,
# cidade e farol. Sobraram duas placas nossas, CAFE e PORT, e as duas ficam longe
# dos quadros que sobram, então cada uma ganha um quadro NOVO, com o MESMO
# metatile do autor, em célula de calçada que já era andável (a colisão passa a 1
# e nenhum caminho fecha: as duas ficam em praça larga, com linha livre em cima e
# embaixo).
PLACAS_NOVAS = [(10, 32), (24, 33)]

# Colisão a corrigir, sem tocar em pixel nenhum: (x, y, colisão nova).
# A linha de baixo do telhado da House3, em (17..21,19), veio ANDÁVEL do autor, e
# é esquecimento dele, não desenho: os metatiles 166, 167 e 168 são os MESMOS que
# ele usa no telhado da casa do CAFE, em (11..13,28), e lá estão com colisão 1;
# os cantos 165 e 169 têm os irmãos 170 e 171 na mesma casa, também com colisão 1.
# Com a linha andável, quem caminhasse por ali sumia da tela inteiro, que é o que
# a regra E3 do `mapas_qa.py` acusou em três células. A linha de CIMA do telhado
# (17..21,18) fica como está: o autor deixa ela andável nas duas casas, e ali o
# metatile não tapa o jogador por inteiro. O caminho da praça não fecha: a rua de
# y=17 passa inteira, de x=8 a x=27.
COLISAO = [(x, 19, 1) for x in range(17, 22)]

# warp id -> (x, y). O ID É A CHAVE E NÃO MUDA; os oito primeiros são os nossos
# de sempre, só que na porta equivalente do desenho novo.
WARPS = {
    0: (47, 28),   # Lighthouse
    1: (14, 15),   # Gym
    2: (11, 31),   # Cafe (casa do sudoeste, encaixe)
    3: (31, 31),   # Mart
    4: (33, 20),   # House1
    5: (38, 20),   # House2
    6: (18, 22),   # House3
    7: (18, 31),   # PokemonCenter
}

# Warps NOVOS, no FIM da lista (seção 1 do contrato: id nunca muda, só acrescenta).
WARPS_NOVOS = [
    (25, 40, "MAP_OLIVINE_CITY_PORT_OUTSIDE", "2"),  # 8, seta sul do píer
    (23,  0, "MAP_ROUTE39", "3"),                    # 9
    (24,  0, "MAP_ROUTE39", "4"),                    # 10
    (25,  0, "MAP_ROUTE39", "5"),                    # 11
    (26,  0, "MAP_ROUTE39", "6"),                    # 12
    (0,  32, "MAP_ROUTE40", "10"),                   # 13
    (0,  33, "MAP_ROUTE40", "14"),                   # 14
    (0,  34, "MAP_ROUTE40", "18"),                   # 15
]

# índice do object_event -> âncora nova. A ORDEM E OS ÍNDICES NÃO MUDAM.
# Quem está na água continua na água e quem está em terra continua em terra: o
# ajuste só procura célula do MESMO tipo.
OBJETOS = {
    0:  (24, 24),   # YOUNGSTER do POKéGEAR, praça do meio
    1:  (16, 17),   # SAILOR que fala da JASMINE, na rua do ginásio
    2:  (46, 30),   # SAILOR que fala do farol, ao pé do farol
    3:  (9, 22),    # ITEM_BALL, bosque do oeste
    4:  (19, 12),   # PIDGEOTTO, estrada do norte
    5:  (12, 40),   # KRABBY, mar do oeste
    6:  (33, 42),   # KRABBY, mar do sul
    7:  (44, 43),   # KRABBY, mar do sudeste
    8:  (52, 35),   # CORSOLA, enseada do leste
    9:  (55, 32),   # CORSOLA, enseada do leste
    10: (40, 44),   # TENTACOOL, mar do sul
    11: (23, 22),   # PIDGEY, praça
    12: (20, 34),   # MACHOKE, cais
    13: (26, 21),   # FURRET
    14: (38, 22),   # FURRET, quintal das casas do leste
    15: (10, 17),   # SKARMORY
    16: (24, 12),   # SENTRET, estrada do norte
    17: (9, 24),    # MACHOP
    18: (24, 6),    # MISDREAVUS, estrada do norte
    19: (12, 21),   # WOMAN_1
    20: (30, 32),   # CLERK, calçada do Mart
    21: (32, 32),   # TWIN do tutor de METRONOME, ao lado do Mart
    22: (10, 16),   # LIGHT_SPRITE, poste de (10,14)
    23: (18, 16),   # LIGHT_SPRITE, poste de (18,14)
    24: (15, 24),   # LIGHT_SPRITE, poste de (15,22)
    25: (22, 24),   # LIGHT_SPRITE, poste de (22,22)
    26: (9, 32),    # LIGHT_SPRITE, poste de (9,30)
    27: (15, 32),   # LIGHT_SPRITE, poste de (15,30)
    28: (21, 32),   # LIGHT_SPRITE, poste de (21,30)
    29: (29, 32),   # LIGHT_SPRITE, poste de (29,30)
    30: (46, 29),   # LIGHT_SPRITE, pé do farol
    31: (18, 34),   # LIGHT_SPRITE, cais oeste
    32: (30, 34),   # LIGHT_SPRITE, cais leste
    33: (40, 34),   # LIGHT_SPRITE, cais leste
    34: (26, 34),   # SAILOR do povoamento, boca do píer
    35: (36, 34),   # FISHERMAN do povoamento, cais
    36: (15, 17),   # OLD_MAN_2 do povoamento, rua do ginásio
    37: (12, 32),   # WOMAN_3 do povoamento, calçada do CAFE
    38: (24, 18),   # BOY_1 do povoamento, entrada da estrada do norte
}

# bg_event: (script, x, y). A lista é reescrita inteira; bg_event não entra na
# save, ao contrário de object_event.
PLACAS = [
    ("OlivineCity_EventScript_GymSign", 12, 16),
    ("OlivineCity_EventScript_Sign", 23, 28),
    ("OlivineCity_EventScript_LighthouseSign", 49, 29),
    ("OlivineCity_EventScript_CafeSign", 10, 32),
    ("OlivineCity_EventScript_PortSign", 24, 33),
]


def le_blocos():
    return bytearray(open(BLOCOS, "rb").read())


def celula(b, x, y):
    v = struct.unpack_from("<H", b, (y * LARGURA + x) * 2)[0]
    return v & 0x3FF, (v >> 10) & 3, (v >> 12) & 0xF


def andavel(b, x, y):
    if not (0 <= x < LARGURA and 0 <= y < ALTURA):
        return False
    return celula(b, x, y)[1] == 0


def agua(b, x, y):
    return celula(b, x, y)[2] == 1


def mais_perto(b, alvo, ocupadas):
    """Célula livre mais perto da âncora, do MESMO tipo (terra ou água)."""
    x0, y0 = alvo
    if not andavel(b, x0, y0):
        raise SystemExit("ERRO: a âncora %s não é chão nem água andável" % (alvo,))
    quero_agua = agua(b, x0, y0)
    if (x0, y0) not in ocupadas:
        return (x0, y0), 0
    for r in range(1, 12):
        melhor = None
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if max(abs(dx), abs(dy)) != r:
                    continue
                x, y = x0 + dx, y0 + dy
                if (andavel(b, x, y) and (x, y) not in ocupadas
                        and agua(b, x, y) == quero_agua):
                    d = dx * dx + dy * dy
                    if melhor is None or d < melhor[1]:
                        melhor = ((x, y), d)
        if melhor:
            return melhor[0], r
    raise SystemExit("ERRO: não achei célula livre perto de %s" % (alvo,))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--aplicar", action="store_true")
    a = ap.parse_args()

    b = le_blocos()
    if len(b) != LARGURA * ALTURA * 2:
        raise SystemExit("ERRO: o map.bin não é %dx%d" % (LARGURA, ALTURA))

    meta = bytearray(open(META_PRI, "rb").read())
    attr = bytearray(open(ATTR_PRI, "rb").read())

    # ------------------------------------------------- metatiles novos (setas)
    for vaga, onde, comportamento in METATILES_NOVOS:
        clone = celula(b, *onde)[0]
        if vaga * 16 + 16 > len(meta):
            raise SystemExit("ERRO: vaga %d fora do metatiles.bin" % vaga)
        meta[vaga * 16:(vaga + 1) * 16] = meta[clone * 16:(clone + 1) * 16]
        antigo = struct.unpack_from("<H", attr, clone * 2)[0]
        struct.pack_into("<H", attr, vaga * 2, (antigo & 0xFF00) | comportamento)
        print("metatile %3d: clone do %3d (célula %s), comportamento %d"
              % (vaga, clone, onde, comportamento))

    # -------------------------------------- porta de mentira no telhado da casa
    # O metatile do canto do telhado das duas casas do leste veio do autor com
    # MB_NON_ANIMATED_DOOR. Ele é usado por DUAS células do mapa inteiro, (36,17)
    # e (41,17), as duas em cima do telhado, onde o jogador nunca pisa (a busca
    # em largura não alcança nenhuma delas), então a porta nunca abriria. É dado
    # errado, do mesmo tipo que a Azalea já tinha tido, e vira MB_NORMAL com o
    # layerType intacto e ZERO pixel mudado.
    telhado = celula(b, *ONDE_ROOF)[0]
    v = struct.unpack_from("<H", attr, telhado * 2)[0]
    print("metatile %3d (telhado em %s): comportamento %d -> %d"
          % (telhado, ONDE_ROOF, v & 0xFF, MB_NORMAL))
    struct.pack_into("<H", attr, telhado * 2, (v & 0xFF00) | MB_NORMAL)

    # -------------------------------------------------- células do map.bin
    placa = celula(b, *ONDE_PLACA)[0]
    print("metatile de placa lido de %s: %d" % (ONDE_PLACA, placa))
    troca = dict(CELULAS_SAIDA)
    for x, y in PLACAS_NOVAS:
        troca[(x, y)] = (placa, 1)
    for (x, y), (idx, col) in sorted(troca.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        p = (y * LARGURA + x) * 2
        v = struct.unpack_from("<H", b, p)[0]
        resto = v & 0xFC00
        if col is not None:
            resto = (resto & ~0x0C00) | ((col & 3) << 10)
        struct.pack_into("<H", b, p, resto | (idx & 0x3FF))
        print("célula (%2d,%2d): metatile %3d -> %3d%s"
              % (x, y, v & 0x3FF, idx, "" if col is None else ", colisão %d" % col))

    for x, y, col in COLISAO:
        pos = (y * LARGURA + x) * 2
        v = struct.unpack_from("<H", b, pos)[0]
        struct.pack_into("<H", b, pos, (v & ~0x0C00) | ((col & 3) << 10))
        print("colisão (%2d,%2d): %d -> %d" % (x, y, (v >> 10) & 3, col))

    # ----------------------------------------------------------------- map.json
    with open(MAPA, encoding="utf-8") as f:
        d = json.load(f, object_pairs_hook=collections.OrderedDict)

    if d.get("connections"):
        raise SystemExit("ERRO: a Olivine ainda tem conexão de mapa; ver seção 3.1")

    for i, (x, y) in sorted(WARPS.items()):
        w = d["warp_events"][i]
        print("warp %2d: (%2d,%2d) -> (%2d,%2d)  %s" % (i, w["x"], w["y"], x, y, w["dest_map"]))
        w["x"], w["y"] = x, y
    if len(d["warp_events"]) == len(WARPS):
        modelo = d["warp_events"][0]
        for x, y, alvo, wid in WARPS_NOVOS:
            e = collections.OrderedDict(modelo)
            e["x"], e["y"], e["elevation"] = x, y, 0
            e["dest_map"], e["dest_warp_id"] = alvo, wid
            d["warp_events"].append(e)
            print("warp %2d NOVO: (%2d,%2d) -> %s %s" % (len(d["warp_events"]) - 1, x, y, alvo, wid))
    elif len(d["warp_events"]) != len(WARPS) + len(WARPS_NOVOS):
        raise SystemExit("ERRO: a lista de warps tem %d entradas" % len(d["warp_events"]))

    ocupadas = set()
    for i, o in enumerate(d["object_events"]):
        if i not in OBJETOS:
            ocupadas.add((o["x"], o["y"]))
    for i in sorted(OBJETOS):
        o = d["object_events"][i]
        (x, y), r = mais_perto(b, OBJETOS[i], ocupadas)
        ocupadas.add((x, y))
        print("objeto %2d %-34s (%2d,%2d) -> (%2d,%2d)%s"
              % (i, o["graphics_id"], o["x"], o["y"], x, y,
                 "" if r == 0 else "  (a âncora %s estava ocupada)" % (OBJETOS[i],)))
        o["x"], o["y"] = x, y
    for i, o in enumerate(d["object_events"]):
        if not andavel(b, o["x"], o["y"]):
            raise SystemExit("ERRO: objeto %d (%s) ficou em (%d,%d), que é parede"
                             % (i, o["graphics_id"], o["x"], o["y"]))
        if o["elevation"] == 3 and agua(b, o["x"], o["y"]):
            raise SystemExit("ERRO: objeto %d (%s) de elevação 3 caiu na água em (%d,%d)"
                             % (i, o["graphics_id"], o["x"], o["y"]))

    modelo = d["bg_events"][0]
    novos = []
    for script, x, y in PLACAS:
        e = collections.OrderedDict(modelo)
        e["type"] = "sign"
        e["x"], e["y"] = x, y
        e["elevation"] = 0
        e["player_facing_dir"] = "BG_EVENT_PLAYER_FACING_ANY"
        e["script"] = script
        e.pop("origem", None)
        novos.append(e)
        print("placa %-44s (%2d,%2d)" % (script, x, y))
    d["bg_events"] = novos

    if a.aplicar:
        open(META_PRI, "wb").write(bytes(meta))
        open(ATTR_PRI, "wb").write(bytes(attr))
        with open(BLOCOS, "wb") as f:
            f.write(bytes(b))
        with open(MAPA, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print("APLICADO")
    else:
        print("(seco: nada foi escrito; use --aplicar)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
