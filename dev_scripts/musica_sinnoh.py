#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pendura a trilha de DPPt nos ~430 mapas vivos de Sinnoh, pela FONTE.

POR QUE ESTE SCRIPT EXISTE
--------------------------
Sinnoh tinha 430 mapas vivos tocando música de Hoenn e de Kanto (medido:
130 `MUS_PETALBURG`, 101 `MUS_RG_MT_MOON`, 59 `MUS_POKE_CENTER`, ...). A onda
anterior importou as faixas de DPPt, mas pendurar faixa em mapa é o passo em
que o erro nasce, por três motivos que se somam:

1. É trabalho de 430 arquivos JSON. À mão, um deles sai errado e ninguém vê.
2. A atribuição CERTA não é a que a memória diz, é a que o jogo original diz.
   Duas armadilhas medidas na fonte: `CELESTIC_TOWN` NÃO tem tema próprio, ela
   usa o mesmo `SEQ_CITY04` de `ETERNA_CITY`; e `SOLACEON_TOWN` divide o
   `SEQ_CITY06` com `PASTORIA_CITY`.
3. O nome da faixa importada NÃO é o nome da sequência da fonte. O pacote de
   trilhas (CyanSMP64, via `fontes-mapas/hns`) batiza por lugar; a fonte
   numera (`SEQ_CITY06_D`). Ligar os dois é o miolo deste arquivo e está
   documentado em COMO O DE-PARA SEQ -> MUS FOI MEDIDO, abaixo.

A saída é auditável: `dev_scripts/musica_sinnoh_de_para.json` guarda UMA linha
por mapa, dizendo com qual header da fonte ele casou, qual `SEQ_*` aquele
header pede, qual faixa nossa saiu disso e, quando a faixa da fonte não existe
aqui, qual substituta entrou e por quê.

COMO O DE-PARA SEQ -> MUS FOI MEDIDO (e não lembrado)
-----------------------------------------------------
O pacote de MIDIs não carrega o nome `SEQ_*` de origem em lugar nenhum. O que
ele carrega é a ORDEM: as regras do `songs.mk` de `fontes-mapas/hns` estão na
ordem do SDAT, e o SDAT do Platinum está listado em
`fontes-mapas/pokeplatinum/generated/sdat.txt`. Alinhando as duas listas:

    sdat.txt 1059..1087   pacote (blocos `_day` do songs.mk)
    TOWN01_D              mus_dp_twinleaf_day
    TOWN02_D              mus_dp_sandgem_day
    TOWN03_D              mus_dp_floaroma_day
    TOWN04_D              mus_dp_solaceon_day
    TOWN06_D              mus_dp_route225_day
    TOWN07_D              mus_dp_valor_lakefront_day
    CITY01_D              mus_dp_jubilife_day
    ...                   ...
    CITY05_D              mus_dp_hearthome_day
    CITY06_D              (NÃO IMPORTADA: o pacote pula)
    CITY07_D              mus_dp_veilstone_day
    ...                   ...
    CITY11_D              mus_dp_fight_area_day
    ROAD_A_D              mus_dp_route201_day
    ...                   ...
    ROAD_BZA_D            mus_dp_route228_day
    OPENING               mus_dp_rowan
    TV_HOUSOU             mus_dp_tv_broadcast

O alinhamento não é palpite: ele se confere sozinho contra os `map_headers.h`
da fonte. `ROAD_A` é usado por `ROUTE_201`, `ROAD_B` por `ROUTE_203`, `ROAD_C`
por `ROUTE_205`, `ROAD_SNOW` por `ROUTE_216`, `CITY07` por `VEILSTONE_CITY`,
`CITY11` por `FIGHT_AREA`, `KENKYUJO` (laboratório) pelo laboratório do Rowan,
`D_KOUEN` (parque) pela Amity Square, `AUS` pelo Hall of Origin. As 23 faixas
de mapa do bloco batem UMA A UMA com o lugar que o nome do pacote diz. A única
que não bate é `TOWN04_D`, que nenhum header do Platinum usa e que o pacote
chama de `solaceon`; e a única que o pacote pula é `CITY06_D`, que o Platinum
usa em 14 mapas (Solaceon e Pastoria). A leitura honesta disso é que o pacote
foi extraído de Diamond/Pearl, onde `TOWN04` é o tema de Solaceon e `CITY06`
ainda não estava em uso.

Consequência prática, e ela decide os três apelidos de `songs.h`:

- Solaceon fica com `MUS_DP_SOLACEON_*` (o tema que o pacote batizou de
  Solaceon). Correto pelo nome e pelo lugar.
- Pastoria NÃO tem faixa própria aqui: `SEQ_CITY06` não foi importada. É um
  buraco declarado. A substituta é `MUS_DP_SOLACEON_*`, e isso não é chute:
  no Platinum as duas cidades tocam LITERALMENTE a mesma sequência.
- Celestic estava apontando para Solaceon e isso é ERRADO. Pela fonte,
  `CELESTIC_TOWN` usa `SEQ_CITY04`, o mesmo de `ETERNA_CITY`. Corrigido em
  `include/constants/songs.h` na mesma onda deste script.

O QUE ELE ESCREVE
-----------------
1. `dev_scripts/musica_sinnoh_de_para.json`  (auditoria, uma linha por mapa)
2. o campo `music` de cada `data/maps/*/map.json` de Sinnoh
3. `src/data/musica_noite.h`, a tabela `_DAY -> _NIGHT` que o gancho de
   `src/overworld.c` usa. Ela SAI DAQUI para não existirem duas verdades.

REGRA DO `map.json`: vai sempre a faixa `_DAY` (ou a faixa única quando não há
par). Quem troca para `_NIGHT` é o gancho, em tempo de execução. Não existe
`map.json` de Sinnoh pedindo `_NIGHT`.

USO
---
    python3 dev_scripts/musica_sinnoh.py             # escreve de verdade
    python3 dev_scripts/musica_sinnoh.py --demo      # só diz o que faria
    python3 dev_scripts/musica_sinnoh.py --autoteste # prova o de-para sozinho
"""

import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTE = ("/Users/duarte/Projetos/pokemon-claude/fontes-mapas/pokeplatinum"
         "/include/data/map_headers.h")
SDAT = ("/Users/duarte/Projetos/pokemon-claude/fontes-mapas/pokeplatinum"
        "/generated/sdat.txt")
MAPAS = os.path.join(RAIZ, "data", "maps")
JSON_SAIDA = os.path.join(RAIZ, "dev_scripts", "musica_sinnoh_de_para.json")
HEADER_SAIDA = os.path.join(RAIZ, "src", "data", "musica_noite.h")
MARCA = "dev_scripts/musica_sinnoh.py"

# Os 15 grupos de mapa que são Sinnoh. Não dá para usar `regionMapSectionId`
# aqui: `include/regions.h` avisa que os 65 apelidos de MAPSEC de Johto são
# todos `MAPSEC_SINNOH_WEST`, ou seja numericamente Johto É Sinnoh Oeste. Quem
# separa as duas é o GRUPO, e é por grupo que este script anda.
GRUPOS_SINNOH = [
    "gMapGroup_SinnohTownsRoutes", "gMapGroup_SpecialAreasSinnoh",
    "gMapGroup_DungeonsSinnoh", "gMapGroup_IndoorSinnoh",
    "gMapGroup_IndoorTwinleaf", "gMapGroup_IndoorSandgem",
    "gMapGroup_IndoorJubilife", "gMapGroup_IndoorOreburgh",
    "gMapGroup_IndoorFloaroma", "gMapGroup_SinnohLeague",
    "gMapGroup_TeamGalactic", "gMapGroup_IndoorSinnohPortas",
    "gMapGroup_SinnohCavernas", "gMapGroup_IndoorSinnohPortas2",
    "gMapGroup_SinnohInteriores",
]

# ---------------------------------------------------------------------------
# SEQ_* da fonte -> faixa desta ROM.
#
# Chave: o `SEQ_*` que o header da fonte pede no campo `.dayMusicID`.
# `noite`: só existe quando a fonte usa um `.nightMusicID` DIFERENTE.
# `falta`: a sequência da fonte não foi importada; `dia`/`noite` já são a
#          substituta e `porque` diz de onde ela veio.
# ---------------------------------------------------------------------------
SEQ = {
    # --- cidades e vilas (par dia/noite completo) ---------------------------
    "SEQ_TOWN01_D": dict(dia="MUS_DP_TWINLEAF_DAY", noite="MUS_DP_TWINLEAF_NIGHT"),
    "SEQ_TOWN02_D": dict(dia="MUS_DP_SANDGEM_DAY", noite="MUS_DP_SANDGEM_NIGHT"),
    "SEQ_TOWN03_D": dict(dia="MUS_DP_FLOAROMA_DAY", noite="MUS_DP_FLOAROMA_NIGHT"),
    "SEQ_TOWN04_D": dict(dia="MUS_DP_SOLACEON_DAY", noite="MUS_DP_SOLACEON_NIGHT"),
    "SEQ_TOWN06_D": dict(dia="MUS_DP_ROUTE225_DAY", noite="MUS_DP_ROUTE225_NIGHT"),
    "SEQ_TOWN07_D": dict(dia="MUS_DP_VALOR_LAKEFRONT_DAY",
                         noite="MUS_DP_VALOR_LAKEFRONT_NIGHT"),
    "SEQ_CITY01_D": dict(dia="MUS_DP_JUBILIFE_DAY", noite="MUS_DP_JUBILIFE_NIGHT"),
    "SEQ_CITY02_D": dict(dia="MUS_DP_CANALAVE_DAY", noite="MUS_DP_CANALAVE_NIGHT"),
    "SEQ_CITY03_D": dict(dia="MUS_DP_OREBURGH_DAY", noite="MUS_DP_OREBURGH_NIGHT"),
    "SEQ_CITY04_D": dict(dia="MUS_DP_ETERNA_DAY", noite="MUS_DP_ETERNA_NIGHT"),
    "SEQ_CITY05_D": dict(dia="MUS_DP_HEARTHOME_DAY", noite="MUS_DP_HEARTHOME_NIGHT"),
    "SEQ_CITY06_D": dict(dia="MUS_DP_SOLACEON_DAY", noite="MUS_DP_SOLACEON_NIGHT",
                         falta=True,
                         porque="SEQ_CITY06 não foi importada (o pacote de MIDIs "
                                "pula ela). Entra MUS_DP_SOLACEON_* (a SEQ_TOWN04 "
                                "do pacote) nos 14 mapas, Pastoria inclusive, e a "
                                "substituição é a que o próprio Platinum faz: lá "
                                "PASTORIA_CITY e SOLACEON_TOWN tocam a MESMA "
                                "sequência. O apelido MUS_DP_PASTORIA_* continua "
                                "em songs.h, inerte, para o dia em que alguém "
                                "importar a SEQ_CITY06 de verdade."),
    "SEQ_CITY07_D": dict(dia="MUS_DP_VEILSTONE_DAY", noite="MUS_DP_VEILSTONE_NIGHT"),
    "SEQ_CITY08_D": dict(dia="MUS_DP_SUNYSHORE_DAY", noite="MUS_DP_SUNYSHORE_NIGHT"),
    "SEQ_CITY09_D": dict(dia="MUS_DP_SNOWPOINT_DAY", noite="MUS_DP_SNOWPOINT_NIGHT"),
    "SEQ_CITY10_D": dict(dia="MUS_DP_POKEMON_LEAGUE_DAY",
                         noite="MUS_DP_POKEMON_LEAGUE_NIGHT"),
    "SEQ_CITY11_D": dict(dia="MUS_DP_FIGHT_AREA_DAY", noite="MUS_DP_FIGHT_AREA_NIGHT"),
    # --- rotas (par dia/noite completo) -------------------------------------
    "SEQ_ROAD_A_D": dict(dia="MUS_DP_ROUTE201_DAY", noite="MUS_DP_ROUTE201_NIGHT"),
    "SEQ_ROAD_B_D": dict(dia="MUS_DP_ROUTE203_DAY", noite="MUS_DP_ROUTE203_NIGHT"),
    "SEQ_ROAD_C_D": dict(dia="MUS_DP_ROUTE205_DAY", noite="MUS_DP_ROUTE205_NIGHT"),
    "SEQ_ROAD_D_D": dict(dia="MUS_DP_ROUTE206_DAY", noite="MUS_DP_ROUTE206_NIGHT"),
    "SEQ_ROAD_E_D": dict(dia="MUS_DP_ROUTE209_DAY", noite="MUS_DP_ROUTE209_NIGHT"),
    "SEQ_ROAD_F_D": dict(dia="MUS_DP_ROUTE210_DAY", noite="MUS_DP_ROUTE210_NIGHT"),
    "SEQ_ROAD_SNOW_D": dict(dia="MUS_DP_ROUTE216_DAY", noite="MUS_DP_ROUTE216_NIGHT"),
    "SEQ_ROAD_BZA_D": dict(dia="MUS_DP_ROUTE228_DAY", noite="MUS_DP_ROUTE228_NIGHT"),
    # --- Pokécenter: o único interior com par dia/noite na fonte ------------
    "SEQ_PC_01": dict(dia="MUS_DP_POKE_CENTER_DAY", noite="MUS_DP_POKE_CENTER_NIGHT"),
    # --- interiores e masmorras (faixa única) -------------------------------
    "SEQ_GYM": dict(dia="MUS_DP_GYM"),
    "SEQ_FS": dict(dia="MUS_DP_POKE_MART"),
    "SEQ_KENKYUJO": dict(dia="MUS_DP_ROWAN_LAB"),
    "SEQ_BLD_GAME": dict(dia="MUS_DP_GAME_CORNER"),
    "SEQ_BLD_DENDO": dict(dia="MUS_DP_HALL_OF_FAME_ROOM"),
    "SEQ_D_01": dict(dia="MUS_DP_VICTORY_ROAD"),
    "SEQ_D_02": dict(dia="MUS_DP_ETERNA_FOREST"),
    "SEQ_D_03": dict(dia="MUS_DP_OLD_CHATEAU"),
    "SEQ_D_04": dict(dia="MUS_DP_OREBURGH_MINE"),
    "SEQ_D_05": dict(dia="MUS_DP_OREBURGH_GATE"),
    "SEQ_D_06": dict(dia="MUS_DP_STARK_MOUNTAIN"),
    "SEQ_D_AGITO": dict(dia="MUS_DP_GALACTIC_HQ"),
    "SEQ_D_GINLOBBY": dict(dia="MUS_DP_GALACTIC_ETERNA_BUILDING"),
    "SEQ_D_LAKE": dict(dia="MUS_DP_LAKE"),
    "SEQ_D_RYAYHY": dict(dia="MUS_DP_LAKE_CAVERNS"),
    "SEQ_D_MOUNT1": dict(dia="MUS_DP_MT_CORONET"),
    "SEQ_D_MOUNT2": dict(dia="MUS_DP_SPEAR_PILLAR"),
    "SEQ_D_LEAGUE": dict(dia="MUS_DP_INSIDE_POKEMON_LEAGUE"),
    "SEQ_THE_EVENT04": dict(dia="MUS_DP_GALACTIC_HQ_BASEMENT"),
    "SEQ_PL_D_GIRATINA": dict(dia="MUS_PL_DISTORTION_WORLD"),
    # --- buracos declarados: a fonte usa, nós não importamos ----------------
    "SEQ_BLD_TV": dict(dia="MUS_DP_JUBILIFE_DAY", noite="MUS_DP_JUBILIFE_NIGHT",
                       falta=True,
                       porque="SEQ_BLD_TV (tema da Jubilife TV) não foi "
                              "importada. Os 7 mapas que a pedem são TODOS "
                              "andares da Jubilife TV, então a substituta da "
                              "mesma família é o tema da própria Jubilife."),
    "SEQ_BLD_CON": dict(dia="MUS_DP_HEARTHOME_DAY", noite="MUS_DP_HEARTHOME_NIGHT",
                        falta=True,
                        porque="SEQ_BLD_CON (Contest Hall) não foi importada. "
                               "Os 3 mapas que a pedem ficam em Hearthome, a "
                               "cidade dos concursos: entra o tema dela."),
    "SEQ_D_KOUEN": dict(dia="MUS_DP_HEARTHOME_DAY", noite="MUS_DP_HEARTHOME_NIGHT",
                        falta=True,
                        porque="SEQ_D_KOUEN (Amity Square) não foi importada. "
                               "A Amity Square é o parque DE Hearthome e se "
                               "entra por dois portões dela: entra o tema da "
                               "cidade, como já vale para os portões."),
    "SEQ_D_SAFARI": dict(dia="MUS_DP_ETERNA_FOREST", falta=True,
                         porque="SEQ_D_SAFARI (Great Marsh) não foi importada. "
                                "A substituta da mesma família é a floresta de "
                                "Eterna (SEQ_D_02), a outra área natural de "
                                "encontro selvagem a céu aberto que existe aqui."),
    # --- a fonte pede SILÊNCIO: não é buraco, é desenho ---------------------
    "SEQ_SILENCE_FIELD": dict(silencio=True),
    "SEQ_SILENCE_DUNGEON": dict(silencio=True),
    # --- a fonte não decidiu (header morto na fonte) ------------------------
    "SEQ_DUMMY": dict(herda_do_pai=True),
}

# ---------------------------------------------------------------------------
# Mapas nossos cujo nome NÃO casa com o header da fonte por normalização.
# São 72, e cada um foi conferido a mão contra a lista de `MAP_HEADER_*`.
# Onde nós inventamos o mapa ou onde a fonte parte em mais pedaços do que nós,
# o header escolhido é o do PAI mais próximo (ver campo `de_para` do JSON).
# ---------------------------------------------------------------------------
DE_PARA = {
    "PokmonLeague": "POKEMON_LEAGUE",                 # falta o 'e' no nosso nome
    "Route204": "ROUTE_204_SOUTH",                    # a fonte parte em norte/sul
    "ValleyWindworks": "VALLEY_WINDWORKS_BUILDING",
    "Route206_North": "ROUTE_206_CYCLING_ROAD_NORTH_GATE",
    "Route206_South": "ROUTE_206_CYCLING_ROAD_SOUTH_GATE",
    "Route208_Access": "ROUTE_208_GATE_TO_HEARTHOME_CITY",
    "Route209_Access": "ROUTE_209_GATE_TO_HEARTHOME_CITY",
    "Route212_Access": "ROUTE_212_GATE_TO_HEARTHOME_CITY",
    "Route213_Access": "ROUTE_213_GATE_TO_PASTORIA_CITY",
    "Route214_Access": "ROUTE_214_GATE_TO_VEILSTONE_CITY",
    "Route215_Access": "ROUTE_215_GATE_TO_VEILSTONE_CITY",
    "Route218_East": "ROUTE_218_GATE_TO_JUBILIFE_CITY",
    "Route218_West": "ROUTE_218_GATE_TO_CANALAVE_CITY",
    "Route222_Access": "ROUTE_222_GATE_TO_SUNYSHORE_CITY",
    "HotelGrandLake": "GRAND_LAKE_ROUTE_213_LOBBY",
    "HearthomeCity_Gym": "HEARTHOME_CITY_GYM_ENTRANCE_ROOM",
    "SunyshoreCity_Gym": "SUNYSHORE_CITY_GYM_ROOM_1",
    "TwinleafTown_MainHouse_1F": "TWINLEAF_TOWN_PLAYER_HOUSE_1F",
    "TwinleafTown_MainHouse_2F": "TWINLEAF_TOWN_PLAYER_HOUSE_2F",
    "Twinleaf_Town_RivalsHouse_F1": "TWINLEAF_TOWN_RIVAL_HOUSE_1F",
    "Twinleaf_Town_RivalsHouse_F2": "TWINLEAF_TOWN_RIVAL_HOUSE_2F",
    "TwinleafTown_Haouse1": "TWINLEAF_TOWN_NORTHEAST_HOUSE",
    "TwinleafTown_House2": "TWINLEAF_TOWN_SOUTHWEST_HOUSE",
    "SandgemTown_RivalHouse_F1": "SANDGEM_TOWN_COUNTERPART_HOUSE_1F",
    "SandgemTown_RivalHouse_F2": "SANDGEM_TOWN_COUNTERPART_HOUSE_2F",
    "SandgemTown_House1": "SANDGEM_TOWN_HOUSE",
    "SandgemTown_PokemonCenter_1F": "SANDGEM_TOWN_POKECENTER_1F",
    "SandgemTown_PokemonCenter_2F": "SANDGEM_TOWN_POKECENTER_2F",
    "SandgemTown_RowanLab": "SANDGEM_TOWN_POKEMON_RESEARCH_LAB",
    "JubilifeCity_PokemonSchool": "TRAINERS_SCHOOL",
    "JubilifeCity_JubilifeTV_F1": "JUBILIFE_TV_1F",
    "JubilifeCity_JubilifeTV_F2": "JUBILIFE_TV_2F",
    "JubilifeCity_JubilifeTV_F3": "JUBILIFE_TV_3F",
    "JubilifeCity_JubilifeTV_F4": "JUBILIFE_TV_4F",
    "JubilifeCity_Flat1_F1": "JUBILIFE_CITY_SOUTH_HOUSE_1F",
    "JubilifeCity_Flat1_F2": "JUBILIFE_CITY_SOUTH_HOUSE_2F",
    "JubilifeCity_Flat1_F3": "UNUSED_JUBILIFE_CITY_SOUTH_HOUSE_3F",
    "JubilifeCity_Flat2_F1": "JUBILIFE_CITY_CONDOMINIUMS_1F",
    "JubilifeCity_Flat2_F2": "JUBILIFE_CITY_CONDOMINIUMS_2F",
    "JubilifeCity_Flat2_F3": "UNUSED_JUBILIFE_CITY_CONDOMINIUMS_3F",
    "JubilifeCity_Flat3_F1": "JUBILIFE_CITY_SOUTHWEST_HOUSE_1F",
    "JubilifeCity_Flat3_F2": "JUBILIFE_CITY_SOUTHWEST_HOUSE_2F",
    # 3o andar que a fonte não tem: herda o pai, o próprio prédio.
    "JubilifeCity_Flat3_F3": "JUBILIFE_CITY_SOUTHWEST_HOUSE_2F",
    "JubilifeCity_PokemonCenter_1F": "JUBILIFE_CITY_POKECENTER_1F",
    "JubilifeCity_PokemonCenter_2F": "JUBILIFE_CITY_POKECENTER_2F",
    "OreburghCity_Flat1_F1": "OREBURGH_CITY_NORTHWEST_HOUSE_1F",
    "OreburghCity_Flat1_F2": "OREBURGH_CITY_NORTHWEST_HOUSE_2F",
    "OreburghCity_Flat2_F1": "OREBURGH_CITY_NORTH_HOUSE_1F",
    "OreburghCity_Flat2_F2": "OREBURGH_CITY_NORTH_HOUSE_2F",
    "OreburghCity_Flat3_F1": "OREBURGH_CITY_EAST_HOUSE_1F",
    "OreburghCity_Flat3_F2": "OREBURGH_CITY_EAST_HOUSE_2F",
    "OreburghCity_House1": "OREBURGH_CITY_WEST_HOUSE",
    "OreburghCity_House2": "OREBURGH_CITY_SOUTH_HOUSE",
    "OreburghCity_House3": "OREBURGH_CITY_MIDDLE_HOUSE",
    "OreburghCity_PokemonCenter_1F": "OREBURGH_CITY_POKECENTER_1F",
    "OreburghCity_PokemonCenter_2F": "OREBURGH_CITY_POKECENTER_2F",
    "FloaromaTown_House1": "FLOAROMA_TOWN_SOUTHEAST_HOUSE",
    "FloaromaTown_House2": "FLOAROMA_TOWN_MIDDLE_HOUSE",
    "FloaromaTown_FlowerShop": "FLOWER_SHOP",
    "FloaromaTown_PokemonCenter_1F": "FLOAROMA_TOWN_POKECENTER_1F",
    "FloaromaTwon_PokemonCenter_2F": "FLOAROMA_TOWN_POKECENTER_2F",  # typo nosso
    "SinnohLeague_Entrance": "POKEMON_LEAGUE_ELEVATOR_TO_AARON_ROOM",
    "SinnohLeague_AaronsRoom": "POKEMON_LEAGUE_AARON_ROOM",
    "SinnohLeague_BerthasRoom": "POKEMON_LEAGUE_BERTHA_ROOM",
    "SinnohLeague_FlintsRoom": "POKEMON_LEAGUE_FLINT_ROOM",
    "SinnohLeague_LuciansRoom": "POKEMON_LEAGUE_LUCIAN_ROOM",
    "SinnohLeague_ChampionsRoom": "POKEMON_LEAGUE_CHAMPION_ROOM",
    "SinnohLeague_HallOfFame": "POKEMON_LEAGUE_HALL_OF_FAME",
    "SinnohVictoryRoad1F": "VICTORY_ROAD_1F",
    "SinnohVictoryRoad2F": "VICTORY_ROAD_2F",
    "SinnohVictoryRoadB1F": "VICTORY_ROAD_B1F",
    "DistortionWorld": "DISTORTION_WORLD_1F",
}

# Mapas que a fonte marca `SEQ_DUMMY`: eles herdam do pai pelo prefixo do nome.
# A busca é pelo nome mais longo que ainda é prefixo, para "UnusedJubilifeCity"
# achar Jubilife e não parar em algo genérico.
PAIS = ["JubilifeCity", "OreburghCity", "EternaCity", "HearthomeCity",
        "PastoriaCity", "VeilstoneCity", "CanalaveCity", "SunyshoreCity",
        "SnowpointCity", "SolaceonTown", "CelesticTown", "TwinleafTown",
        "SandgemTown", "FloaromaTown"]


def normaliza(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def le_fonte():
    """{nome_normalizado: (MAP_HEADER, SEQ_dia, SEQ_noite)} dos 593 headers."""
    txt = open(FONTE, encoding="utf-8").read()
    saida = {}
    for nome, corpo in re.findall(
            r"\[MAP_HEADER_(\w+)\] = \{(.*?)\n    \},", txt, re.S):
        dia = re.search(r"\.dayMusicID = (\w+)", corpo)
        noite = re.search(r"\.nightMusicID = (\w+)", corpo)
        if not dia or not noite:
            continue
        saida[normaliza(nome)] = (nome, dia.group(1), noite.group(1))
    return saida


def mapas_de_sinnoh():
    """[(nome, caminho, json)] dos mapas VIVOS de Sinnoh (sem os `cortado_por`)."""
    grupos = json.load(open(os.path.join(MAPAS, "map_groups.json"),
                            encoding="utf-8"))
    saida, tumulos = [], 0
    for grupo in GRUPOS_SINNOH:
        for nome in grupos[grupo]:
            caminho = os.path.join(MAPAS, nome, "map.json")
            dados = json.load(open(caminho, encoding="utf-8"))
            if "cortado_por" in dados:
                tumulos += 1
                continue
            saida.append((nome, caminho, dados))
    return saida, tumulos


def pai_de(nome):
    candidatos = [p for p in PAIS if p.lower() in nome.lower()]
    return max(candidatos, key=len) if candidatos else None


def decide(nome, fonte):
    """Devolve o registro de auditoria de UM mapa."""
    reg = {"mapa": nome}
    alvo = DE_PARA.get(nome)
    reg["de_para"] = "manual" if alvo else "nome"
    chave = normaliza(alvo or nome)
    achado = fonte.get(chave)

    if not achado and not alvo:
        # mapa que inventamos: herda do pai mais próximo pelo nome
        pai = pai_de(nome)
        achado = fonte.get(normaliza(pai)) if pai else None
        reg["de_para"] = "pai:%s" % pai if achado else "sem par"
    if not achado:
        reg["erro"] = "sem header na fonte (nem por pai)"
        return reg

    header, seq_dia, seq_noite = achado
    reg["header_fonte"] = header
    reg["seq_dia"] = seq_dia
    reg["seq_noite"] = seq_noite

    regra = SEQ.get(seq_dia)
    if regra is None:
        reg["erro"] = "SEQ sem linha na tabela deste script: %s" % seq_dia
        return reg

    if regra.get("herda_do_pai"):
        pai = pai_de(nome)
        achado_pai = fonte.get(normaliza(pai)) if pai else None
        if not achado_pai:
            reg["erro"] = "SEQ_DUMMY e sem pai para herdar"
            return reg
        regra_pai = SEQ.get(achado_pai[1])
        if not regra_pai or "dia" not in regra_pai:
            reg["erro"] = "SEQ_DUMMY e o pai %s tambem nao decide" % pai
            return reg
        reg["musica"] = regra_pai["dia"]
        reg["musica_noite"] = regra_pai.get("noite")
        reg["faltando"] = bool(regra_pai.get("falta"))
        reg["motivo"] = ("a fonte marca SEQ_DUMMY neste header (mapa morto la); "
                         "herda do mapa pai %s" % pai)
        return reg

    if regra.get("silencio"):
        reg["musica"] = None
        reg["motivo"] = ("a fonte pede SILENCIO (%s). Esta base nao tem faixa de "
                         "silencio penduravel em map.json, entao o mapa fica com "
                         "a musica que ja tinha e NAO e tocado por este script."
                         % seq_dia)
        return reg

    reg["musica"] = regra["dia"]
    reg["musica_noite"] = regra.get("noite")
    reg["faltando"] = bool(regra.get("falta"))
    if regra.get("falta"):
        reg["motivo"] = regra["porque"]
    return reg


def escreve_map_json(caminho, musica):
    """Troca só o campo `music`, preservando o resto do arquivo byte a byte."""
    txt = open(caminho, encoding="utf-8").read()
    novo, n = re.subn(r'("music"\s*:\s*)"[A-Z0-9_]+"',
                      lambda m: m.group(1) + '"%s"' % musica, txt, count=1)
    if n != 1:
        raise SystemExit("map.json sem campo music unico: %s" % caminho)
    if novo == txt:
        return False
    open(caminho, "w", encoding="utf-8").write(novo)
    return True


def escreve_header(pares):
    linhas = [
        "// GERADO por %s. NAO EDITE A MAO." % MARCA,
        "//",
        "// A tabela dia -> noite de Sinnoh. Ela sai do MESMO de-para que",
        "// pendura a faixa nos map.json (dev_scripts/musica_sinnoh_de_para.json)",
        "// justamente para nao existirem duas verdades: se um mapa ganhar par",
        "// dia/noite novo, os dois lados mudam na mesma rodada do script.",
        "//",
        "// Custo de save: ZERO. Nada disto entra em SaveBlock; e uma tabela",
        "// const na ROM lida em tempo de warp.",
        "",
        "static const u16 sMusicaDiaNoiteSinnoh[][2] =",
        "{",
    ]
    for dia, noite in pares:
        linhas.append("    {%s, %s}," % (dia, noite))
    linhas += ["};", ""]
    open(HEADER_SAIDA, "w", encoding="utf-8").write("\n".join(linhas))


def autoteste(fonte):
    """Prova as afirmações que este script faz, sem tocar em arquivo."""
    # 1. os dois pares que a memoria erra, lidos da fonte
    assert fonte[normaliza("CELESTIC_TOWN")][1] == "SEQ_CITY04_D", \
        "CELESTIC_TOWN deixou de usar SEQ_CITY04 na fonte"
    assert fonte[normaliza("ETERNA_CITY")][1] == "SEQ_CITY04_D"
    assert fonte[normaliza("SOLACEON_TOWN")][1] == "SEQ_CITY06_D"
    assert fonte[normaliza("PASTORIA_CITY")][1] == "SEQ_CITY06_D"
    # 2. o apelido de songs.h tem de ter sido consertado
    sh = open(os.path.join(RAIZ, "include", "constants", "songs.h"),
              encoding="utf-8").read()
    assert re.search(r"#define\s+MUS_DP_CELESTIC_DAY\s+MUS_DP_ETERNA_DAY", sh), \
        "songs.h ainda manda Celestic para Solaceon (era o apelido errado)"
    assert re.search(r"#define\s+MUS_DP_PASTORIA_DAY\s+MUS_DP_SOLACEON_DAY", sh)
    # 3. o alinhamento SDAT x pacote: as ancoras que o provam
    ordem = [l.strip() for l in open(SDAT, encoding="utf-8") if l.strip()]
    for i, esperado in ((1059, "SEQ_TOWN01_D"), (1062, "SEQ_TOWN04_D"),
                        (1070, "SEQ_CITY06_D"), (1071, "SEQ_CITY07_D"),
                        (1084, "SEQ_OPENING")):
        achado = ordem[i - 1].split()[0]
        assert achado == esperado, \
            "sdat.txt linha %d virou %s (esperava %s)" % (i, achado, esperado)
    # 4. toda faixa citada na tabela SEQ existe em songs.h
    nomes = set(re.findall(r"^#define\s+([A-Z][A-Z0-9_]*)\s", sh, flags=re.M))
    for chave, regra in SEQ.items():
        for campo in ("dia", "noite"):
            if regra.get(campo) and regra[campo] not in nomes:
                raise AssertionError("%s pede %s, que songs.h nao define"
                                     % (chave, regra[campo]))
    # 5. todo alvo do DE_PARA existe mesmo na fonte
    perdidos = [k for k, v in DE_PARA.items() if normaliza(v) not in fonte]
    assert not perdidos, "DE_PARA aponta para header inexistente: %s" % perdidos
    print("autoteste OK: %d linhas na tabela SEQ, %d de-para manuais, "
          "ancoras do sdat.txt no lugar" % (len(SEQ), len(DE_PARA)))


def main():
    seco = "--demo" in sys.argv
    fonte = le_fonte()
    if "--autoteste" in sys.argv:
        return autoteste(fonte)

    mapas, tumulos = mapas_de_sinnoh()
    registros = [decide(nome, fonte) for nome, _, _ in mapas]
    erros = [r for r in registros if "erro" in r]
    if erros:
        for r in erros[:20]:
            print("ERRO %s: %s" % (r["mapa"], r["erro"]))
        raise SystemExit("%d mapas sem decisao. Nada foi escrito." % len(erros))

    mudados = 0
    for (nome, caminho, dados), reg in zip(mapas, registros):
        reg["musica_antes"] = dados.get("music")
        if not reg.get("musica"):
            continue
        if dados.get("music") == reg["musica"]:
            continue
        if not seco and escreve_map_json(caminho, reg["musica"]):
            mudados += 1
        elif seco:
            mudados += 1

    pares = sorted({(r["musica"], r["musica_noite"]) for r in registros
                    if r.get("musica") and r.get("musica_noite")})
    faltando = sorted({r["seq_dia"] for r in registros if r.get("faltando")})
    silencio = [r["mapa"] for r in registros if r.get("musica") is None]

    if not seco:
        escreve_header(pares)
        json.dump({
            "gerado_por": MARCA,
            "fonte": FONTE,
            "mapas_vivos": len(registros),
            "mapas_tumulo_ignorados": tumulos,
            "seq_sem_faixa_importada": faltando,
            "pares_dia_noite": [list(p) for p in pares],
            "mapas": registros,
        }, open(JSON_SAIDA, "w", encoding="utf-8"),
            ensure_ascii=False, indent=1, sort_keys=False)

    print("Sinnoh: %d mapas vivos, %d tumulos ignorados" % (len(registros), tumulos))
    print("%s%d map.json com o campo music trocado" % ("(--demo) " if seco else "",
                                                       mudados))
    print("%d pares dia/noite na tabela do gancho" % len(pares))
    print("SEQ sem faixa importada (buraco declarado, com substituta): %s"
          % ", ".join(faltando))
    print("mapas que a fonte manda ficar em silencio (nao tocados): %s"
          % ", ".join(silencio))


if __name__ == "__main__":
    sys.exit(main() or 0)
