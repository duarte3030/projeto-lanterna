#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remapeamento de Ecruteak para o desenho do Scorched Silver (seção 2 do contrato).

A ferramenta `copia_cidade.py` trouxe a ARTE. O JOGO é nosso, e é este arquivo:
cada warp, NPC, placa e gatilho vai para o lugar equivalente do desenho novo.

De onde saiu cada casamento de porta
------------------------------------
Não foi chute: os 11 warps do PRÓPRIO mapa do hack (`g0m2`) foram lidos da ROM e
o destino de cada um foi aberto para ver o que é. O que isso mostrou:

    porta       mapa do hack   o que é                      nosso mapa
    (18,38)     g4m1  22x30    ginásio de passarela         EcruteakCity_Gym
    (39,38)     g10m5 14x9     duas ENFERMEIRAS             EcruteakCity_PokemonCenter
    (48,30)     g10m7 11x8     MART_EMPLOYEE                EcruteakCity_Mart
    (39,30)     g29m0 17x16    seis dançarinas              EcruteakCity_Theater
    (17,8)      g24m52 21x20   masmorra de 10 warps         BurnedTower_1F
    (34,13)     g24m77 10x21   salão de madeira com sábios  EcruteakCity_SageOffice1
    (16,30)     g10m2 11x8     casa                         EcruteakCity_House1
    (28,38)     g10m4 10x9     casa                         EcruteakCity_House2
    (49,38)     g24m78 11x8    casa                         EcruteakCity_House3
    (8,26)      g26m83 8x8     guarita                      Gate_EcruteakCity_Route38
    (57,34)     g26m85 8x8     guarita                      Gate_EcruteakCity_Route42

Sobraram DOIS mapas nossos sem porta no desenho deles: `EcruteakCity_SageOffice2`
e `TinTower_1F`, que no nosso jogo são a passagem norte para a Bellchime Trail.
A regra da seção 2 do contrato manda ENCAIXAR o prédio nosso no desenho deles, com
os tiles deles: a casa decorativa do alto (x=28..32, y=10..13), que o autor
desenhou sem porta nenhuma, ganha duas portas com o MESMO metatile de porta que o
autor usa na casa vizinha (índice 120), em (29,13) e (30,13). Nenhum tile novo é
inventado.

Os ids de warp NÃO mudam e a ordem dos `object_events` NÃO muda: outros mapas
apontam para os warps por número e a save guarda o índice do objeto (seção 1).

Uso:
    python3 dev_scripts/remapeia_ecruteak.py            # só mostra o que faria
    python3 dev_scripts/remapeia_ecruteak.py --aplicar
"""
import argparse
import collections
import json
import os
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPA = os.path.join(REPO, "data/maps/EcruteakCity/map.json")
BLOCOS = os.path.join(REPO, "data/layouts/EcruteakCity/map.bin")
META_PRI = os.path.join(REPO, "data/tilesets/primary/ecruteak_city_copia_pri/metatiles.bin")
ATTR_PRI = os.path.join(REPO, "data/tilesets/primary/ecruteak_city_copia_pri/metatile_attributes.bin")
LARGURA, ALTURA = 66, 46

# Os índices de metatile do tileset novo MUDAM a cada rodada do `copia_cidade.py`
# (o `de_para` depende de quantos índices a costura pina), então nada aqui é
# número cravado: cada um é LIDO da célula onde o autor o usa.
ONDE_PORTA = (34, 13)   # a porta da casa de cima, à direita
ONDE_PLACA = (30, 30)   # o poste de placa do lote vazio
ONDE_TRILHA = (33, 45)  # a grama da trilha sul
METATILE_SAIDA_SUL = 303   # vaga livre: o mapa usa 0..302

# Metatile NOVO, clonado de outro do hack e só com o comportamento trocado.
# (vaga, clone de, comportamento novo). Nenhum pixel é desenhado: o tile é o do
# autor, byte a byte; só o byte de comportamento muda.
#
# Por que ele existe: Ecruteak NÃO TEM MAIS CONEXÃO DE MAPA NENHUMA, e a razão é
# do motor, não de gosto. `LoadMapFromCameraTransition` (src/overworld.c:911) só
# recarrega o tileset SECUNDÁRIO quando o jogador atravessa uma conexão; o
# PRIMÁRIO fica o da cidade, porque o jogo original garante que mapas ligados por
# conexão compartilham o primário. A cidade copiada tem um primário só dela, e
# medido em 11/09/2026 o resultado de atravessar a pé para a Route37 era a rota
# inteira desenhada com as paletas do Scorched Silver: árvore laranja, estrada
# preta, lixo na borda. Warp não tem esse defeito, porque ele faz carga completa
# de mapa. Então a saída sul virou warp, como as outras três já eram (portão a
# oeste, portão a leste, prédio dos sábios ao norte), e os dois tiles da trilha
# ganham MB_SOUTH_ARROW_WARP (101) para os warps 7 e 8 dispararem.
MB_SOUTH_ARROW_WARP = 101
METATILES_NOVOS = [(METATILE_SAIDA_SUL, "TRILHA", MB_SOUTH_ARROW_WARP)]

# Tiles a trocar no `map.bin`: (x, y, metatile novo, colisão nova ou None).
# Colisão None = mantém a do autor.
TILES = [
    (29, 13, "PORTA", None),          # porta encaixada: SageOffice2
    (30, 13, "PORTA", None),          # porta encaixada: TinTower
    (21, 38, "PLACA", 1),             # poste da placa do ginásio, no lote de areia
    (33, 45, "SAIDA_SUL", None),      # saída sul, warp 7 -> Route37
    (34, 45, "SAIDA_SUL", None),      # saída sul, warp 8 -> Route37
]

# Colisão a corrigir, sem tocar em pixel nenhum: (x, y, colisão nova).
# A cumeeira do telhado do teatro, em (38..40,26), veio ANDÁVEL do autor, e o
# metatile dela tapa o jogador POR INTEIRO (regra E3 do `mapas_qa.py`): quem
# subisse ali sumia da tela. Vira parede, e o caminho continua existindo pelas
# linhas 24 e 25, que são praça aberta.
COLISAO = [(38, 26, 1), (39, 26, 1), (40, 26, 1)]

# warp id -> (x, y). O ID É A CHAVE E NÃO MUDA.
WARPS = {
    0: (8, 26),    # Gate_EcruteakCity_Route38, seta oeste do portão
    1: (57, 34),   # Gate_EcruteakCity_Route42, seta leste do portão
    2: (17, 8),    # BurnedTower_1F, o templo roxo do alto
    3: (34, 13),   # EcruteakCity_SageOffice1, o salão de madeira
    4: (29, 13),   # EcruteakCity_SageOffice2, porta encaixada
    5: (30, 13),   # TinTower_1F, porta encaixada
    6: (39, 30),   # EcruteakCity_Theater, o pagode azul
    7: (33, 45),   # Route37, trilha sul (a mesma coluna de antes)
    8: (34, 45),   # Route37, trilha sul
    9: (16, 30),   # EcruteakCity_House1
    10: (28, 38),  # EcruteakCity_House2
    11: (39, 38),  # EcruteakCity_PokemonCenter
    12: (48, 30),  # EcruteakCity_Mart
    13: (18, 38),  # EcruteakCity_Gym
    14: (49, 38),  # EcruteakCity_House3
}

# índice do object_event -> âncora nova. Quem não está aqui fica onde está.
# A âncora é ONDE ELE DEVE FICAR; se a célula estiver ocupada ou não for chão,
# o script anda para a célula andável livre mais perto e DIZ que andou.
OBJETOS = {
    1: (20, 39),   # sábio do ginásio, na frente da porta do ginásio
    8: (24, 33),   # Vulpix, rua do meio
    10: (44, 32),  # Noctowl, leste
    12: (17, 10),  # Rattata, terraço do templo
    13: (19, 10),  # Rattata, terraço do templo
    14: (14, 16),  # Gastly, mato do noroeste
    15: (18, 16),  # Misdreavus
    16: (13, 24),  # Haunter
    17: (22, 16),  # Gastly
    18: (13, 32),  # Gastly
    19: (13, 40),  # Gengar, canto sudoeste
    20: (43, 21),  # Poliwag, margem do lago
    21: (45, 21),  # Poliwhirl, margem do lago
    23: (52, 40),  # Misdreavus, sudeste
    24: (54, 33),  # Misdreavus, leste
    25: (53, 24),  # Mismagius, nordeste
    26: (43, 33),  # Pidgeotto
    30: (13, 36),  # Misdreavus, oeste
    31: (52, 41),  # Youngster, rua sul
    32: (39, 31),  # Silver, na porta do teatro
    37: (28, 24),  # poste
    38: (16, 24),  # poste
    40: (13, 34),  # poste
    44: (36, 41),  # poste
    45: (31, 41),  # poste
    46: (50, 41),  # poste
    48: (43, 22),  # poste
}

# bg_event: (script, x, y). A ordem da lista é reescrita inteira; bg_event não
# entra na save, ao contrário de object_event.
PLACAS = [
    ("EcruteakCity_EventScript_BurnedSign", 19, 13),
    ("EcruteakCity_EventScript_OfficeSign", 32, 14),
    ("EcruteakCity_EventScript_CitySign", 30, 30),
    ("EcruteakCity_EventScript_TheaterSign", 37, 31),
    ("EcruteakCity_EventScript_GymSign", 21, 38),
    ("EcruteakCity_EventScript_MartSign", 50, 30),
]

GATILHOS = {0: (39, 32)}   # gatilho do Silver, um tile abaixo de onde ele para


def le_blocos():
    return bytearray(open(BLOCOS, "rb").read())


def andavel(b, x, y):
    if not (0 <= x < LARGURA and 0 <= y < ALTURA):
        return False
    return ((struct.unpack_from("<H", b, (y * LARGURA + x) * 2)[0] >> 10) & 3) == 0


def mais_perto(b, alvo, ocupadas):
    """Célula andável livre mais perto da âncora, em anéis de distância crescente."""
    x0, y0 = alvo
    if andavel(b, x0, y0) and (x0, y0) not in ocupadas:
        return (x0, y0), 0
    for r in range(1, 12):
        melhor = None
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if max(abs(dx), abs(dy)) != r:
                    continue
                x, y = x0 + dx, y0 + dy
                if andavel(b, x, y) and (x, y) not in ocupadas:
                    d = dx * dx + dy * dy
                    if melhor is None or d < melhor[1]:
                        melhor = ((x, y), d)
        if melhor:
            return melhor[0], r
    raise SystemExit("ERRO: não achei chão livre perto de %s" % (alvo,))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--aplicar", action="store_true")
    a = ap.parse_args()

    b = le_blocos()

    def indice(xy):
        x, y = xy
        return struct.unpack_from("<H", b, (y * LARGURA + x) * 2)[0] & 0x3FF

    achado = {"PORTA": indice(ONDE_PORTA), "PLACA": indice(ONDE_PLACA),
              "TRILHA": indice(ONDE_TRILHA), "SAIDA_SUL": METATILE_SAIDA_SUL}
    print("metatiles lidos do mapa: porta=%d, placa=%d, trilha=%d"
          % (achado["PORTA"], achado["PLACA"], achado["TRILHA"]))

    meta = bytearray(open(META_PRI, "rb").read())
    attr = bytearray(open(ATTR_PRI, "rb").read())
    for vaga, chave, comportamento in METATILES_NOVOS:
        clone = achado[chave]
        meta[vaga * 16:(vaga + 1) * 16] = meta[clone * 16:(clone + 1) * 16]
        antigo = struct.unpack_from("<H", attr, clone * 2)[0]
        struct.pack_into("<H", attr, vaga * 2, (antigo & 0xFF00) | (comportamento & 0xFF))
        print("metatile %3d: clone do %d com comportamento %d" % (vaga, clone, comportamento))

    for x, y, chave, col in TILES:
        idx = achado[chave]
        p = (y * LARGURA + x) * 2
        v = struct.unpack_from("<H", b, p)[0]
        resto = v & 0xFC00
        if col is not None:
            resto = (resto & ~0x0C00) | ((col & 3) << 10)
        struct.pack_into("<H", b, p, resto | (idx & 0x3FF))
        print("tile (%2d,%2d): metatile %3d -> %3d%s"
              % (x, y, v & 0x3FF, idx, "" if col is None else ", colisão %d" % col))

    for x, y, col in COLISAO:
        pos = (y * LARGURA + x) * 2
        v = struct.unpack_from("<H", b, pos)[0]
        struct.pack_into("<H", b, pos, (v & ~0x0C00) | ((col & 3) << 10))
        print("colisão (%2d,%2d): %d -> %d" % (x, y, (v >> 10) & 3, col))

    with open(MAPA, encoding="utf-8") as f:
        d = json.load(f, object_pairs_hook=collections.OrderedDict)

    for i, (x, y) in sorted(WARPS.items()):
        w = d["warp_events"][i]
        print("warp %2d: (%2d,%2d) -> (%2d,%2d)  %s" % (i, w["x"], w["y"], x, y, w["dest_map"]))
        w["x"], w["y"] = x, y

    ocupadas = set()
    for i, o in enumerate(d["object_events"]):
        if i not in OBJETOS:
            ocupadas.add((o["x"], o["y"]))
    for i in sorted(OBJETOS):
        o = d["object_events"][i]
        (x, y), r = mais_perto(b, OBJETOS[i], ocupadas)
        ocupadas.add((x, y))
        print("objeto %2d %-32s (%2d,%2d) -> (%2d,%2d)%s"
              % (i, o["graphics_id"], o["x"], o["y"], x, y,
                 "" if r == 0 else "  (a âncora %s estava ocupada ou em parede)" % (OBJETOS[i],)))
        o["x"], o["y"] = x, y
    # quem ficou parado mas caiu em parede é erro de projeto, não de execução
    for i, o in enumerate(d["object_events"]):
        if not andavel(b, o["x"], o["y"]):
            raise SystemExit("ERRO: objeto %d (%s) ficou em (%d,%d), que não é chão"
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

    for i, (x, y) in sorted(GATILHOS.items()):
        g = d["coord_events"][i]
        print("gatilho %d: (%2d,%2d) -> (%2d,%2d)" % (i, g["x"], g["y"], x, y))
        g["x"], g["y"] = x, y

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
