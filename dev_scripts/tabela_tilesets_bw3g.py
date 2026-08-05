#!/usr/bin/env python3
"""Tabela que falta ao `demake_gen2.py`: qual metatile de gen 3 usar por CLASSE.

O conversor classifica cada quadrante de bloco do BW3G em `chao`, `parede`,
`agua`, `grama`, `escada`, `porta` ou `balcao`, e diz explicitamente que não
resolve "qual metatile bonito usar". Este arquivo resolve, para os 58 tilesets
de origem do hack.

Como os ids foram obtidos (MEDIDOS, não escolhidos de cabeça):

  1. Só entram pares primary+secondary que EXISTEM em `data/tilesets/` e que
     algum layout de `data/layouts/layouts.json` já usa. Par que ninguém usa não
     está provado carregando.
  2. `chao` e `parede` saem da contagem de frequência dos `map.bin` dos layouts
     desse par (u16 little-endian; `id = v & 0x3FF`, `colisao = (v >> 10) & 3`).
  3. `chao` só aceita metatile com comportamento `MB_NORMAL`. Sem esse filtro a
     frequência mente: em `SootopolisCity_Gym_1F` o metatile mais pisado é o 525
     = `MB_THIN_ICE`, gelo que racha e derruba o jogador num andar que não
     existe. Já custou um bug real neste projeto.
  4. Dois filtros a mais, achados medindo, e cada um consertou uma mentira:
     - **presença em pelo menos 2 layouts.** Sem isso, `interior` elegeria
       parede = 513, cujos 225 usos vêm todos de UM mapa só
       (`Route110_TrickHouseCorridor`), e `loja` elegeria parede = 1, o vazio
       preto do primary Building, vindo só de `Route121_SafariZoneEntrance`.
     - **`parede` não pode ter comportamento de água.** Em `caverna` o campeão
       absoluto de colisão 1 é o 657 (14276 usos), água decorativa não surfável
       usada como preenchimento; vira parede feita de água em mapa inteiro.
  5. `chao` do exterior foi medido só nos mapas de topo (`Route201_Layout`,
     `SandgemTown_Layout`, ...). A importação de Johto pendurou dezenas de
     INTERIORES no par de exterior, e contando tudo junto o vencedor virava o
     metatile 0, o vazio preto de `GoldenrodCity_TrainStation`.
  6. As outras classes saem do COMPORTAMENTO, não da frequência: `grama` =
     `MB_TALL_GRASS`, `agua` = `MB_POND_WATER`, `escada` = `MB_LADDER`, `porta` =
     `MB_ANIMATED_DOOR`/`MB_NON_ANIMATED_DOOR`, `balcao` = `MB_COUNTER`. Quando o
     par não tem a classe, ela cai de propósito em `chao` ou `parede` (anotado na
     linha), nunca num id que não existe naquele par.

Colisão: `porta` e `escada` vão com 0 porque no gen 2 são casas em que o jogador
PISA (a porta é um warp). `agua` vai com 0 de propósito: no gen 3 a água é
colisão 0 e quem barra o jogador a pé é o comportamento, que é o mesmo que
libera o Surf. `balcao` vai com 1: balcão é para falar por cima, não atravessar.

Rodar `python3 dev_scripts/tabela_tilesets_bw3g.py` reabre os
`metatile_attributes.bin` e confere tudo. Imprime OK ou lista os problemas.
"""
import os
import re
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BW3G = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/bw3g"

# ---------------------------------------------------------------- as tabelas

# tileset do BW3G (nome minúsculo, sem "_collision.asm") -> (primary, secondary, paleta)
DESTINO = {
    # --- exterior: rotas, cidades, praia, ponte, deserto, floresta, porto ---
    "battle_tower_outside": ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh", "exterior_sinnoh"),
    "bridge":               ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh", "exterior_sinnoh"),
    "castelia":             ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh", "exterior_sinnoh"),
    "desert":               ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh", "exterior_sinnoh"),
    "dreamyard":            ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh", "exterior_sinnoh"),
    "driftveil":            ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh", "exterior_sinnoh"),
    "forest":               ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh", "exterior_sinnoh"),
    "icirrus":              ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh", "exterior_sinnoh"),
    "johto":                ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh", "exterior_sinnoh"),
    "johto_modern":         ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh", "exterior_sinnoh"),
    "kanto":                ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh", "exterior_sinnoh"),
    "lentimas":             ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh", "exterior_sinnoh"),
    "mistralton":           ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh", "exterior_sinnoh"),
    "nacrene":              ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh", "exterior_sinnoh"),
    "nimbasa":              ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh", "exterior_sinnoh"),
    "opelucid":             ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh", "exterior_sinnoh"),
    "park":                 ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh", "exterior_sinnoh"),
    "port":                 ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh", "exterior_sinnoh"),
    "striaton":             ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh", "exterior_sinnoh"),
    "unova_beach":          ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh", "exterior_sinnoh"),
    "unova_east":           ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh", "exterior_sinnoh"),
    "unova_north":          ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh", "exterior_sinnoh"),
    "unova_west":           ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh", "exterior_sinnoh"),
    "village_bridge":       ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh", "exterior_sinnoh"),
    "virbank":              ("gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh", "exterior_sinnoh"),

    # --- caverna: gruta, ruína subterrânea, caminho de gelo, passagem ---
    "cave":                 ("gTileset_GeneralSinnoh", "gTileset_CaveSinnoh", "caverna"),
    "cave_ruins":           ("gTileset_GeneralSinnoh", "gTileset_CaveSinnoh", "caverna"),
    "ice_path":             ("gTileset_GeneralSinnoh", "gTileset_CaveSinnoh", "caverna"),
    "ruins_of_alph":        ("gTileset_GeneralSinnoh", "gTileset_CaveSinnoh", "caverna"),
    "underground":          ("gTileset_GeneralSinnoh", "gTileset_CaveSinnoh", "caverna"),
    "unused_dark_cave":     ("gTileset_GeneralSinnoh", "gTileset_CaveSinnoh", "caverna"),

    # --- interior genérico: casa, prédio, laboratório, torre, sala de puzzle ---
    "aerodactyl_word_room": ("gTileset_Building", "gTileset_GenericBuilding", "interior"),
    "airport":              ("gTileset_Building", "gTileset_GenericBuilding", "interior"),
    "battle_tower":         ("gTileset_Building", "gTileset_GenericBuilding", "interior"),
    "beta_word_room":       ("gTileset_Building", "gTileset_GenericBuilding", "interior"),
    "complex":              ("gTileset_Building", "gTileset_GenericBuilding", "interior"),
    "facility":             ("gTileset_Building", "gTileset_GenericBuilding", "interior"),
    "game_corner":          ("gTileset_Building", "gTileset_GenericBuilding", "interior"),
    "gate":                 ("gTileset_Building", "gTileset_GenericBuilding", "interior"),
    "ho_oh_word_room":      ("gTileset_Building", "gTileset_GenericBuilding", "interior"),
    "house":                ("gTileset_Building", "gTileset_GenericBuilding", "interior"),
    "kabuto_word_room":     ("gTileset_Building", "gTileset_GenericBuilding", "interior"),
    "lab":                  ("gTileset_Building", "gTileset_GenericBuilding", "interior"),
    "lighthouse":           ("gTileset_Building", "gTileset_GenericBuilding", "interior"),
    "mansion":              ("gTileset_Building", "gTileset_GenericBuilding", "interior"),
    "omanyte_word_room":    ("gTileset_Building", "gTileset_GenericBuilding", "interior"),
    "players_house":        ("gTileset_Building", "gTileset_GenericBuilding", "interior"),
    "players_room":         ("gTileset_Building", "gTileset_GenericBuilding", "interior"),
    "pokecom_center":       ("gTileset_Building", "gTileset_GenericBuilding", "interior"),
    "radio_tower":          ("gTileset_Building", "gTileset_GenericBuilding", "interior"),
    "tower":                ("gTileset_Building", "gTileset_GenericBuilding", "interior"),
    "traditional_house":    ("gTileset_Building", "gTileset_GenericBuilding", "interior"),
    "train_station":        ("gTileset_Building", "gTileset_GenericBuilding", "interior"),

    # --- centro pokémon e loja: precisam de balcão de verdade ---
    "pokecenter":           ("gTileset_Building", "gTileset_PokemonCenter", "pokecenter"),
    "mart":                 ("gTileset_Building", "gTileset_Shop", "loja"),

    # --- salas de liga/campeão: piso de ginásio, sem porta nem balcão ---
    "champions_room":       ("gTileset_Building", "gTileset_RustboroGym", "ginasio"),
    "elite_four_room":      ("gTileset_Building", "gTileset_RustboroGym", "ginasio"),
    "pkmn_league":          ("gTileset_Building", "gTileset_RustboroGym", "ginasio"),
}

# paleta -> { classe: (id_do_metatile, colisao) }   colisao: 0 = passa, 1 = bloqueia
PALETA = {
    # gTileset_GeneralSinnoh + gTileset_PetalburgSinnoh, 172 layouts (61 de topo)
    "exterior_sinnoh": {
        "chao":   (1, 0),      # MB_NORMAL, 3600 usos em 41 mapas de topo
        "parede": (113, 1),    # MB_MOUNTAIN_TOP, 10249 usos em 28 mapas (encosta de montanha)
        "agua":   (161, 0),    # MB_POND_WATER, 955 usos
        "grama":  (13, 0),     # MB_TALL_GRASS, 4735 usos
        "escada": (1, 0),      # FALLBACK -> chao: nenhum MB_LADDER neste par
        "porta":  (167, 0),    # MB_NON_ANIMATED_DOOR, 70 usos
        "balcao": (113, 1),    # FALLBACK -> parede: nenhum MB_COUNTER neste par
    },
    # gTileset_GeneralSinnoh + gTileset_CaveSinnoh, 35 layouts (MtCoronet, IcePath, DarkCave)
    "caverna": {
        "chao":   (843, 0),    # MB_NORMAL, 844 usos em 4 mapas (piso de rocha do Ice Path)
        "parede": (753, 1),    # MB_CAVE, 1334 usos em 5 mapas
        "agua":   (161, 0),    # MB_POND_WATER, 482 usos
        "grama":  (454, 0),    # MB_TALL_GRASS, 75 usos
        "escada": (833, 0),    # MB_LADDER, 6 usos
        "porta":  (461, 0),    # MB_ANIMATED_DOOR, 2 usos
        "balcao": (753, 1),    # FALLBACK -> parede: nenhum MB_COUNTER neste par
    },
    # gTileset_Building + gTileset_GenericBuilding, 61 layouts (casas de Hoenn e Sinnoh)
    "interior": {
        "chao":   (812, 0),    # MB_NORMAL, 762 usos em 23 mapas
        "parede": (824, 1),    # MB_NORMAL bloqueado, 208 usos em 23 mapas
        "agua":   (824, 1),    # FALLBACK -> parede: nenhuma água neste par
        "grama":  (812, 0),    # FALLBACK -> chao: nenhum MB_TALL_GRASS neste par
        "escada": (812, 0),    # FALLBACK -> chao: nenhum MB_LADDER neste par
        "porta":  (523, 0),    # MB_NON_ANIMATED_DOOR, 15 usos
        "balcao": (1014, 1),   # MB_COUNTER, 2 usos
    },
    # gTileset_Building + gTileset_PokemonCenter, 12 layouts
    "pokecenter": {
        "chao":   (514, 0),    # MB_NORMAL, 357 usos em 12 mapas
        "parede": (523, 1),    # MB_NORMAL bloqueado, 67 usos em 12 mapas
        "agua":   (523, 1),    # FALLBACK -> parede: nenhuma água neste par
        "grama":  (514, 0),    # FALLBACK -> chao: nenhum MB_TALL_GRASS neste par
        "escada": (514, 0),    # FALLBACK -> chao: nenhum MB_LADDER neste par
        "porta":  (575, 0),    # MB_NON_ANIMATED_DOOR, 15 usos
        "balcao": (727, 1),    # MB_COUNTER, 15 usos (o balcão da enfermeira)
    },
    # gTileset_Building + gTileset_Shop, 11 layouts (Mart, HerbShop, DepartmentStore)
    "loja": {
        "chao":   (616, 0),    # MB_NORMAL, 153 usos em 4 mapas
        "parede": (648, 1),    # MB_NORMAL bloqueado, 61 usos em 7 mapas
        "agua":   (648, 1),    # FALLBACK -> parede: nenhuma água neste par
        "grama":  (616, 0),    # FALLBACK -> chao: nenhum MB_TALL_GRASS neste par
        "escada": (616, 0),    # FALLBACK -> chao: nenhum MB_LADDER neste par
        "porta":  (592, 0),    # MB_NON_ANIMATED_DOOR, 5 usos
        "balcao": (674, 1),    # MB_COUNTER, 14 usos
    },
    # gTileset_Building + gTileset_RustboroGym, 4 layouts (Rustboro, Oreburgh, Eterna, Snowbelle)
    "ginasio": {
        "chao":   (513, 0),    # MB_NORMAL, 665 usos em 4 mapas
        "parede": (518, 1),    # MB_NORMAL bloqueado, 269 usos em 4 mapas
        "agua":   (518, 1),    # FALLBACK -> parede: nenhuma água neste par
        "grama":  (513, 0),    # FALLBACK -> chao: nenhum MB_TALL_GRASS neste par
        "escada": (513, 0),    # FALLBACK -> chao: nenhum MB_LADDER neste par
        "porta":  (513, 0),    # FALLBACK -> chao: nenhuma porta neste par
        "balcao": (518, 1),    # FALLBACK -> parede: nenhum MB_COUNTER neste par
    },
}

# --------------------------------------------------------------- verificação


def _behaviors():
    """Nome -> valor do enum de include/constants/metatile_behaviors.h, na ordem."""
    corpo = open(os.path.join(REPO, "include/constants/metatile_behaviors.h")).read()
    corpo = corpo.split("enum {", 1)[1].split("};", 1)[0]
    tabela, i = {}, 0
    for linha in corpo.splitlines():
        linha = re.sub(r"//.*", "", linha).strip().rstrip(",").strip()
        if not linha:
            continue
        if "=" in linha:
            nome, valor = linha.split("=")
            nome, i = nome.strip(), int(valor.strip(), 0)
        else:
            nome = linha
        tabela[nome] = i
        i += 1
    return tabela


def _attr_paths():
    """gTileset_X -> caminho do metatile_attributes.bin, lido do próprio repo."""
    incbin = dict(re.findall(
        r'gMetatileAttributes_(\w+)\[\]\s*=\s*INCBIN_U16\("([^"]+)"\)',
        open(os.path.join(REPO, "src/data/tilesets/metatiles.h")).read()))
    caminhos, atual = {}, None
    for linha in open(os.path.join(REPO, "src/data/tilesets/headers.h")):
        m = re.match(r"const struct Tileset (gTileset_\w+)", linha)
        if m:
            atual = m.group(1)
        m = re.search(r"\.metatileAttributes\s*=\s*gMetatileAttributes_(\w+)", linha)
        if m and atual:
            caminhos[atual] = incbin.get(m.group(1))
    return caminhos


def _comportamentos(caminho, mascara):
    dados = open(os.path.join(REPO, caminho), "rb").read()
    return [struct.unpack_from("<H", dados, o)[0] & mascara for o in range(0, len(dados), 2)]


def verifica():
    erros = []
    MB = _behaviors()
    caminhos = _attr_paths()
    mascara = int(re.search(r"#define METATILE_ATTR_BEHAVIOR_MASK\s+(0x[0-9A-Fa-f]+)",
                            open(os.path.join(REPO, "include/global.fieldmap.h")).read()).group(1), 16)
    num_prim = int(re.search(r"#define NUM_METATILES_IN_PRIMARY\s+(\d+)",
                             open(os.path.join(REPO, "include/fieldmap.h")).read()).group(1))
    AGUA = {MB[n] for n in ("MB_POND_WATER", "MB_INTERIOR_DEEP_WATER", "MB_DEEP_WATER",
                            "MB_OCEAN_WATER", "MB_SHALLOW_WATER")}

    # (d) cobertura dos 58 tilesets de origem e das paletas citadas
    origem = sorted(f[:-len("_collision.asm")]
                    for f in os.listdir(os.path.join(BW3G, "data/tilesets"))
                    if f.endswith("_collision.asm")) if os.path.isdir(BW3G) else []
    if origem:
        for t in origem:
            if t not in DESTINO:
                erros.append(f"tileset de origem sem entrada em DESTINO: {t}")
        for t in DESTINO:
            if t not in origem:
                erros.append(f"DESTINO tem {t}, que não existe no BW3G")
    else:
        print(f"aviso: {BW3G} não está clonado; conferindo só a contagem de DESTINO")
        if len(DESTINO) != 58:
            erros.append(f"DESTINO tem {len(DESTINO)} entradas, o BW3G tem 58 tilesets")

    pares = {}
    for tileset, (prim, sec, paleta) in DESTINO.items():
        if paleta not in PALETA:
            erros.append(f"{tileset}: paleta {paleta} não existe em PALETA")
            continue
        if prim not in caminhos or sec not in caminhos:
            erros.append(f"{tileset}: {prim} ou {sec} não existe no repo")
            continue
        anterior = pares.setdefault(paleta, (prim, sec))
        if anterior != (prim, sec):
            erros.append(f"paleta {paleta} usada com dois pares: {anterior} e {(prim, sec)}")

    for paleta, (prim, sec) in sorted(pares.items()):
        ap = _comportamentos(caminhos[prim], mascara)
        as_ = _comportamentos(caminhos[sec], mascara)
        classes = PALETA[paleta]

        def beh(mid):
            if mid < len(ap):
                return ap[mid]
            if num_prim <= mid < num_prim + len(as_):
                return as_[mid - num_prim]
            return None

        for classe, (mid, col) in classes.items():
            # (a) o id existe no par
            if beh(mid) is None:
                erros.append(f"{paleta}.{classe}: metatile {mid} fora do par "
                             f"({prim} tem {len(ap)}, {sec} tem {len(as_)} a partir de {num_prim})")
                continue
            if col not in (0, 1):
                erros.append(f"{paleta}.{classe}: colisão {col} inválida")
        if beh(classes["chao"][0]) is None:
            continue
        # (b) chão precisa ser MB_NORMAL: frequência sozinha já elegeu gelo fino
        if beh(classes["chao"][0]) != MB["MB_NORMAL"]:
            erros.append(f"{paleta}.chao: metatile {classes['chao'][0]} tem comportamento "
                         f"{beh(classes['chao'][0])}, não MB_NORMAL")
        if classes["chao"][1] != 0:
            erros.append(f"{paleta}.chao: colisão {classes['chao'][1]}, o jogador não anda nele")
        if classes["parede"][1] != 1:
            erros.append(f"{paleta}.parede: colisão {classes['parede'][1]}, não bloqueia")
        # (c) grama e água só valem se NÃO foram declaradas fallback
        caiu = {classes["chao"], classes["parede"]}
        if classes["grama"] not in caiu and beh(classes["grama"][0]) != MB["MB_TALL_GRASS"]:
            erros.append(f"{paleta}.grama: metatile {classes['grama'][0]} não é MB_TALL_GRASS")
        if classes["agua"] not in caiu and beh(classes["agua"][0]) not in AGUA:
            erros.append(f"{paleta}.agua: metatile {classes['agua'][0]} não tem comportamento de água")
        if classes["escada"] not in caiu and beh(classes["escada"][0]) != MB["MB_LADDER"]:
            erros.append(f"{paleta}.escada: metatile {classes['escada'][0]} não é MB_LADDER")
        if classes["porta"] not in caiu and beh(classes["porta"][0]) not in (
                MB["MB_ANIMATED_DOOR"], MB["MB_NON_ANIMATED_DOOR"]):
            erros.append(f"{paleta}.porta: metatile {classes['porta'][0]} não é porta")
        if classes["balcao"] not in caiu and beh(classes["balcao"][0]) != MB["MB_COUNTER"]:
            erros.append(f"{paleta}.balcao: metatile {classes['balcao'][0]} não é MB_COUNTER")
    return erros, pares


if __name__ == "__main__":
    problemas, pares = verifica()
    for paleta, (prim, sec) in sorted(pares.items()):
        usam = sum(1 for v in DESTINO.values() if v[2] == paleta)
        print(f"{paleta:16} {prim} + {sec}   ({usam} tilesets do BW3G)")
    if problemas:
        print(f"\n{len(problemas)} problema(s):")
        for p in problemas:
            print("  -", p)
        sys.exit(1)
    print(f"\nOK: {len(DESTINO)} tilesets de origem, {len(PALETA)} paletas, "
          f"{sum(len(v) for v in PALETA.values())} metatiles conferidos")
