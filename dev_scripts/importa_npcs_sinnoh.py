#!/usr/bin/env python3
"""Traz NPC, placa e mobiliário de Sinnoh do pokeplatinum para os nossos map.json.

    python3 dev_scripts/importa_npcs_sinnoh.py            # só relata
    python3 dev_scripts/importa_npcs_sinnoh.py --aplicar  # escreve os map.json

A fonte é `fontes-mapas/pokeplatinum/res/field/events/events_*.json`, ligada ao
nosso mapa pelo nome do MAP_HEADER que `include/data/map_headers.h` associa a
cada arquivo de eventos.

Quatro decisões que valem mais que o código, todas tomadas por segurança:

1. **Coordenada.** O `z` deles é o nosso `y` (o `y` deles é altura). Mas mapa de
   rua no Platinum não usa coordenada local: usa coordenada GLOBAL da matriz de
   Sinnoh, e Jubilife começa em x=140, z=743. Pior, os nossos layouts de Sinnoh
   NÃO são os layouts do Platinum (a nossa Jubilife é 70x64; a matriz dela lá tem
   outra forma), então nem descontar o canto da matriz alinha os dois. Medido:
   os deltas entre o mesmo NPC nos dois lados variam de (89,724) a (164,732)
   dentro do MESMO mapa. Não existe offset.
   Por isso: interior (coordenada já local e dentro do nosso layout) entra
   IGUAL; mapa de rua entra por **proporção** da caixa da matriz do Platinum
   sobre o nosso layout, e depois `valida_mapas_sinnoh.py --corrigir` empurra
   quem caiu em tile bloqueado. A posição relativa se mantém, a exata não.
   Quem não couber de jeito nenhum fica de fora, nunca fora do mapa.

2. **`hidden_flag`.** Os `FLAG_HIDE_*` do Platinum não existem aqui. A política é
   NÃO importar objeto com hidden_flag: quem nasce escondido é NPC de história
   (grunt da Galáctica trancando estrada, lendário de lago), e trazer isso sem a
   flag põe um bloqueio permanente no caminho do jogador. Objeto de rua comum tem
   `hidden_flag: "0"` e passa.

3. **`script`.** Lá é número de índice; aqui é rótulo. NPC importado entra MUDO
   (`script: "0"`) e `trainer_type` forçado para NONE, porque treinador sem time
   é batalha contra o vazio. Placa aponta para um rótulo genérico compartilhado.

4. **Mobiliário nunca vira NPC.** Pedra de Strength virada NPC tranca caverna
   para sempre. Toda a lista `GRAFICOS_PROIBIDOS` fica de fora.
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import valida_mapas_sinnoh as V  # noqa: E402  reaproveita sprites_utilizaveis e TROCA_SPRITE

PLAT = os.path.join(os.path.dirname(REPO), "fontes-mapas/pokeplatinum")
APLICAR = "--aplicar" in sys.argv

# Rótulo único para toda placa importada. Ver decisão 3 no topo.
SCRIPT_PLACA = "Sinnoh_EventScript_PlacaImportada"

# Marca de origem gravada em cada evento importado. O mapjson ignora campo que
# não conhece, então ela é inerte na ROM e serve para uma coisa só: rodar
# --aplicar duas vezes não pode DOBRAR a população da cidade. Mapa que já tem a
# marca é pulado inteiro, e o script diz quantos pulou.
MARCA = {"origem": "pokeplatinum"}

# Objeto que empurra, bloqueia, dá item ou é cenário: não vira NPC. Decisão 4.
# ponytail: sem esta lista, os 110 BERRY_SOIL, 62 VENT e 16 BOLLARD de Sinnoh
# viravam OBJ_EVENT_GFX_MAN_1 e a cidade ganhava 190 pessoas de pé em cima de
# canteiro. Pedra de Strength virada NPC tranca caverna para sempre.
GRAFICOS_PROIBIDOS = (
    "BOULDER", "ROCK_SMASH", "CUT_TREE", "BREAKABLE", "ITEM_BALL", "POKEBALL",
    "BERRY_TREE", "BERRY_SOIL", "MOVING_BOX", "TRUCK", "MACHINE", "SUBMARINE",
    "VENT", "BOLLARD", "MAILBOX", "BOOK", "MOSS_ROCK", "ICE_ROCK", "SNOWBALL",
    "CAVE_PAINTING", "BRIEFCASE", "_DOOR", "WALL_BLOCKING", "GRUNTS_GROUP",
    "FOSSIL", "OLD_AMBER", "METEORITE", "CLIPBOARD",
)

# Placa do Platinum é objeto, não bg_event. Vira placa nossa em vez de gente.
GRAFICOS_PLACA = ("SIGNBOARD", "ARROW_SIGNPOST", "MAP_SIGNPOST",
                  "TRAINER_TIPS_SIGNPOST", "GYM_SIGNPOST")

# Personagem com nome próprio e Pokémon: sem sprite aqui, e trocar por genérico
# faz o mapa mentir (líder de ginásio com cara de nadador). Fica de fora e é
# registrado em PENDENCIAS-NPC-SINNOH.md. Decisão do Gui, 05/08/2026.
NOMES_PROPRIOS = (
    "CYNTHIA", "CYRUS", "MARS", "JUPITER", "SATURN", "CHARON", "ROARK",
    "GARDENIA", "MAYLENE", "CRASHER_WAKE", "FANTINA", "BYRON", "CANDICE",
    "VOLKNER", "AARON", "BERTHA", "FLINT", "LUCIAN", "PALMER", "LOOKER",
    "BUCK", "MIRA", "CHERYL", "MARLEY", "RILEY", "JASMINE", "GAME_DIRECTOR",
    "UXIE", "AZELF", "MESPRIT", "ARCEUS", "DARKRAI", "SHAYMIN", "HEATRAN",
    "REGIGIGAS", "CRESSELIA", "GIRATINA", "ROTOM", "PACHIRISU", "BUNEARY",
    "CROAGUNK", "HAPPINY", "STARLY", "DRIFLOON", "MAGIKARP", "TORCHIC",
    "SHROOMISH",
)

# Mapa que outro agente está editando neste bloco, ou que não faz sentido povoar.
#
# TRAVA DE ESCRITA, NUNCA RÉGUA DE MEDIÇÃO. Até 11/08/2026 esta lista era
# descontada dentro de `nossos_mapas_sinnoh()`, que é a régua que o
# `completude.py` usa: `CanalaveCity_Gym` e `SandgemTown_House1` estão na ROM e
# no `map_groups.json` e mesmo assim contavam como ausentes, exatamente o mesmo
# defeito de medida que segurava as seis salas da Elite dos Quatro por causa do
# nome. Quem não pode escrever agora não é quem não existe: use
# `mapas_editaveis_sinnoh()` para escrever e `nossos_mapas_sinnoh()` para medir.
NAO_TOCAR = ("CanalaveCity_Gym", "SandgemTown_House1")

# Nome que a normalização não casa sozinha. Nosso mapa -> MAP_HEADER do Platinum.
APELIDOS = {
    # Os três andares da Victory Road de Sinnoh entram com prefixo de região
    # porque `MAP_VICTORY_ROAD_1F` e `LAYOUT_VICTORY_ROAD_1F` já são de HOENN
    # (ver `fecha_portas_sinnoh.RENOMEADOS`). Sem estes três pares o mapa
    # existiria na ROM e `completude.py` continuaria contando ele como ausente.
    "SinnohVictoryRoad1F": "MAP_HEADER_VICTORY_ROAD_1F",
    "SinnohVictoryRoad2F": "MAP_HEADER_VICTORY_ROAD_2F",
    "SinnohVictoryRoadB1F": "MAP_HEADER_VICTORY_ROAD_B1F",
    "TwinleafTown_MainHouse_1F": "MAP_HEADER_TWINLEAF_TOWN_PLAYER_HOUSE_1F",
    "TwinleafTown_MainHouse_2F": "MAP_HEADER_TWINLEAF_TOWN_PLAYER_HOUSE_2F",
    "Twinleaf_Town_RivalsHouse_F1": "MAP_HEADER_TWINLEAF_TOWN_RIVAL_HOUSE_1F",
    "Twinleaf_Town_RivalsHouse_F2": "MAP_HEADER_TWINLEAF_TOWN_RIVAL_HOUSE_2F",
    "TwinleafTown_Haouse1": "MAP_HEADER_TWINLEAF_TOWN_NORTHEAST_HOUSE",
    "TwinleafTown_House2": "MAP_HEADER_TWINLEAF_TOWN_SOUTHWEST_HOUSE",
    "SandgemTown_RowanLab": "MAP_HEADER_SANDGEM_TOWN_POKEMON_RESEARCH_LAB",
    "SandgemTown_House1": "MAP_HEADER_SANDGEM_TOWN_HOUSE",
    "SandgemTown_RivalHouse_F1": "MAP_HEADER_SANDGEM_TOWN_COUNTERPART_HOUSE_1F",
    "SandgemTown_RivalHouse_F2": "MAP_HEADER_SANDGEM_TOWN_COUNTERPART_HOUSE_2F",
    "JubilifeCity_Flat1_F1": "MAP_HEADER_JUBILIFE_CITY_CONDOMINIUMS_1F",
    "JubilifeCity_Flat1_F2": "MAP_HEADER_JUBILIFE_CITY_CONDOMINIUMS_2F",
    "JubilifeCity_Flat2_F1": "MAP_HEADER_JUBILIFE_CITY_SOUTH_HOUSE_1F",
    "JubilifeCity_Flat2_F2": "MAP_HEADER_JUBILIFE_CITY_SOUTH_HOUSE_2F",
    "JubilifeCity_Flat3_F1": "MAP_HEADER_JUBILIFE_CITY_SOUTHWEST_HOUSE_1F",
    "JubilifeCity_Flat3_F2": "MAP_HEADER_JUBILIFE_CITY_SOUTHWEST_HOUSE_2F",
    "JubilifeCity_JubilifeTV_F1": "MAP_HEADER_JUBILIFE_TV_1F",
    "JubilifeCity_JubilifeTV_F2": "MAP_HEADER_JUBILIFE_TV_2F",
    "JubilifeCity_JubilifeTV_F3": "MAP_HEADER_JUBILIFE_TV_3F",
    "JubilifeCity_JubilifeTV_F4": "MAP_HEADER_JUBILIFE_TV_4F",
    "JubilifeCity_PoketchCompany_F1": "MAP_HEADER_POKETCH_CO_1F",
    "JubilifeCity_PoketchCompany_F2": "MAP_HEADER_POKETCH_CO_2F",
    "JubilifeCity_PoketchCompany_F3": "MAP_HEADER_POKETCH_CO_3F",
    "JubilifeCity_PokemonSchool": "MAP_HEADER_TRAINERS_SCHOOL",
    "OreburghCity_Flat1_F1": "MAP_HEADER_OREBURGH_CITY_NORTHWEST_HOUSE_1F",
    "OreburghCity_Flat1_F2": "MAP_HEADER_OREBURGH_CITY_NORTHWEST_HOUSE_2F",
    "OreburghCity_Flat2_F1": "MAP_HEADER_OREBURGH_CITY_NORTH_HOUSE_1F",
    "OreburghCity_Flat2_F2": "MAP_HEADER_OREBURGH_CITY_NORTH_HOUSE_2F",
    "OreburghCity_Flat3_F1": "MAP_HEADER_OREBURGH_CITY_EAST_HOUSE_1F",
    "OreburghCity_Flat3_F2": "MAP_HEADER_OREBURGH_CITY_EAST_HOUSE_2F",
    "OreburghCity_House1": "MAP_HEADER_OREBURGH_CITY_MIDDLE_HOUSE",
    "OreburghCity_House2": "MAP_HEADER_OREBURGH_CITY_WEST_HOUSE",
    "OreburghCity_House3": "MAP_HEADER_OREBURGH_CITY_SOUTH_HOUSE",
    "FloaromaTown_House1": "MAP_HEADER_FLOAROMA_TOWN_SOUTHEAST_HOUSE",
    "FloaromaTown_House2": "MAP_HEADER_FLOAROMA_TOWN_MIDDLE_HOUSE",
    "FloaromaTwon_PokemonCenter_2F": "MAP_HEADER_FLOAROMA_TOWN_POKECENTER_2F",
    "ValleyWindworks": "MAP_HEADER_VALLEY_WINDWORKS_OUTSIDE",
    "SinnohLeague_Entrance": "MAP_HEADER_POKEMON_LEAGUE",
    # As seis salas da Elite dos Quatro de Sinnoh JA ESTAO na ROM desde
    # `20ac2eaac4`, e as batalhas foram provadas no emulador em `T82.1` a
    # `T82.5`. `completude.py` contava as seis como ausentes porque o nome daqui
    # e `SinnohLeague_*` e o do Platinum e `POKEMON_LEAGUE_*`: mapa que existe
    # sumindo da conta por causa do nome e o mesmo defeito de regua que segurava
    # Unova em `Rt5NimbasaGate`. Nada de mapa entra aqui, so a medida acerta.
    "SinnohLeague_AaronsRoom": "MAP_HEADER_POKEMON_LEAGUE_AARON_ROOM",
    "SinnohLeague_BerthasRoom": "MAP_HEADER_POKEMON_LEAGUE_BERTHA_ROOM",
    "SinnohLeague_FlintsRoom": "MAP_HEADER_POKEMON_LEAGUE_FLINT_ROOM",
    "SinnohLeague_LuciansRoom": "MAP_HEADER_POKEMON_LEAGUE_LUCIAN_ROOM",
    "SinnohLeague_ChampionsRoom": "MAP_HEADER_POKEMON_LEAGUE_CHAMPION_ROOM",
    "SinnohLeague_HallOfFame": "MAP_HEADER_POKEMON_LEAGUE_HALL_OF_FAME",
    # Mesmo caso, por nome de predio: a loja de flores de Floaroma e
    # `MAP_HEADER_FLOWER_SHOP` la, sem o nome da cidade na frente.
    "FloaromaTown_FlowerShop": "MAP_HEADER_FLOWER_SHOP",
    # Os 3F dos dois predios de Jubilife que ja estao na ROM. No Platinum eles
    # sao os andares marcados UNUSED do MESMO predio (Flat1 e o condominio,
    # Flat2 e a casa do sul); Flat3 nao entra porque a casa do sudoeste do
    # Platinum so tem 1F e 2F, entao o nosso 3F nao tem par la.
    "JubilifeCity_Flat1_F3": "MAP_HEADER_UNUSED_JUBILIFE_CITY_CONDOMINIUMS_3F",
    "JubilifeCity_Flat2_F3": "MAP_HEADER_UNUSED_JUBILIFE_CITY_SOUTH_HOUSE_3F",
    "SunyshoreCity_Gym": "MAP_HEADER_SUNYSHORE_CITY_GYM_ROOM_1",
    "HearthomeCity_Gym": "MAP_HEADER_HEARTHOME_CITY_GYM_ENTRANCE_ROOM",
    "Route204": "MAP_HEADER_ROUTE_204_SOUTH",
    "Route206_North": "MAP_HEADER_ROUTE_206_CYCLING_ROAD_NORTH_GATE",
    "Route206_South": "MAP_HEADER_ROUTE_206_CYCLING_ROAD_SOUTH_GATE",
    "Route208_Access": "MAP_HEADER_ROUTE_208_GATE_TO_HEARTHOME_CITY",
    "Route209_Access": "MAP_HEADER_ROUTE_209_GATE_TO_HEARTHOME_CITY",
    "Route212_Access": "MAP_HEADER_ROUTE_212_GATE_TO_HEARTHOME_CITY",
    "Route213_Access": "MAP_HEADER_ROUTE_213_GATE_TO_PASTORIA_CITY",
    "Route214_Access": "MAP_HEADER_ROUTE_214_GATE_TO_VEILSTONE_CITY",
    "Route215_Access": "MAP_HEADER_ROUTE_215_GATE_TO_VEILSTONE_CITY",
    "Route218_East": "MAP_HEADER_ROUTE_218_GATE_TO_JUBILIFE_CITY",
    "Route218_West": "MAP_HEADER_ROUTE_218_GATE_TO_CANALAVE_CITY",
    "Route222_Access": "MAP_HEADER_ROUTE_222_GATE_TO_SUNYSHORE_CITY",
    "Route225_Access": "MAP_HEADER_ROUTE_225_GATE_TO_FIGHT_AREA",
    "Route226_Access": "MAP_HEADER_ROUTE_226_HOUSE",
    "HotelGrandLake": "MAP_HEADER_GRAND_LAKE_ROUTE_213_LOBBY",
}

# Prefixos que identificam mapa de Sinnoh no nosso data/maps.
PREFIXOS = V.PREFIXOS_SINNOH


def nossos_mapas_sinnoh():
    """ponytail: o prefixo "Route2" de valida_mapas_sinnoh.py pega Route26 a
    Route29, que são de Johto, e "Lake" pega LakeOfRage. Rota de Sinnoh tem
    três dígitos (201 a 230), e é assim que elas se separam."""
    base = os.path.join(REPO, "data/maps")
    # ponytail: prefixo nao alcanca predio de nome proprio (Cafe, Villa,
    # GameCorner, CycleShop, PokemonDayCare). O grupo alcanca: mapa que mora num
    # grupo com "Sinnoh" no nome E de Sinnoh, sem lista de nome para envelhecer.
    grupos = json.load(open(os.path.join(base, "map_groups.json")))
    por_grupo = {m for g in grupos.get("group_order", []) if "sinnoh" in g.lower()
                 for m in grupos.get(g, [])}

    def da_regiao(n):
        if n in por_grupo:
            return True
        if n.startswith("Route"):
            # sem ancora no fim: "Route205House" e de Sinnoh tanto quanto
            # "Route205_South". Route26 a Route29 (Johto) tem dois digitos e
            # nao casam com Route2[0-3]\d, que exige tres.
            return bool(re.match(r"Route2[0-3]\d", n))
        if n.startswith("LakeOfRage"):
            return False
        return any(n.startswith(p) for p in PREFIXOS)
    return [n for n in sorted(os.listdir(base))
            if not n.endswith("_Frlg") and da_regiao(n)
            and os.path.exists(os.path.join(base, n, "map.json"))]


def mapas_editaveis_sinnoh():
    """A régua MENOS a trava de escrita. Só quem VAI ESCREVER usa esta lista.

    Separada de `nossos_mapas_sinnoh()` em 11/08/2026: quem mede quanto de
    Sinnoh existe não pode perder mapa que existe só porque outro agente está
    editando ele hoje.
    """
    return [n for n in nossos_mapas_sinnoh() if n not in NAO_TOCAR]


def headers_do_platinum():
    """MAP_HEADER_X -> (arquivo de eventos, id da matriz)."""
    txt = open(os.path.join(PLAT, "include/data/map_headers.h")).read()
    fora = {}
    for bloco in re.finditer(r"\[(MAP_HEADER_[A-Z0-9_]+)\]\s*=\s*\{(.*?)\n    \},",
                             txt, re.S):
        nome, corpo = bloco.group(1), bloco.group(2)
        ev = re.search(r"\.eventsArchiveID\s*=\s*(\w+)", corpo)
        mx = re.search(r"\.mapMatrixID\s*=\s*(\w+)", corpo)
        if ev and ev.group(1).startswith("events_"):
            fora[nome] = (ev.group(1), mx.group(1) if mx else None)
    return fora


SINONIMOS = [
    ("pokemoncenter", "pokecenter"), ("pokmoncenter", "pokecenter"),
    ("pokemonleague", "pokemonleague"), ("pokmonleague", "pokemonleague"),
    ("condominiums", "flat"), ("apartments", "flat"),
    ("trainersschool", "pokemonschool"), ("poketchco", "poketchcompany"),
    ("jubilifetv", "jubilifecityjubilifetv"),
]


def chave(nome):
    n = nome.lower().replace("_", "").replace("-", "")
    n = re.sub(r"^mapheader", "", n)
    for a, b in SINONIMOS:
        n = n.replace(a, b)
    n = re.sub(r"f(\d)$", r"\1f", n)      # _F1 e 1F são o mesmo andar
    n = re.sub(r"b(\d)f$", r"b\1f", n)
    n = n.replace("route2", "route2")
    return n


def caixa_da_matriz(matriz_id, header):
    """Canto e tamanho, em tiles, que o header ocupa na matriz do Platinum."""
    p = os.path.join(PLAT, "res/field/matrices", f"{matriz_id}.json")
    if not os.path.exists(p):
        return None
    grade = json.load(open(p))["headers"]
    cels = [(r, c) for r, linha in enumerate(grade)
            for c, h in enumerate(linha) if h == header]
    if not cels:
        return None
    r0 = min(r for r, _ in cels); r1 = max(r for r, _ in cels)
    c0 = min(c for _, c in cels); c1 = max(c for _, c in cels)
    return c0 * 32, r0 * 32, (c1 - c0 + 1) * 32, (r1 - r0 + 1) * 32


def conversor_de_coordenada(fonte, larg, alt, header, matriz):
    """(x do Platinum, z do Platinum) -> (x, y) nosso, para UM mapa.

    Extraida de `main()` em 11/08/2026 e nao reescrita: `itens_escondidos_sinnoh`
    precisa da MESMA conta para reencontrar, pela coordenada, qual evento da
    fonte virou qual `bg_event` nosso. Duas copias da formula divergiriam calado
    no dia em que uma fosse ajustada, e o preco seria item escondido posto no
    lugar errado, exatamente o que a ferramenta existe para evitar.
    """
    todos = fonte.get("object_events", []) + fonte.get("bg_events", [])
    if not todos:
        return None
    xs = [e["x"] for e in todos]
    zs = [e["z"] for e in todos]
    if min(xs) >= 0 and min(zs) >= 0 and max(xs) < larg and max(zs) < alt:
        return lambda e: (e["x"], e["z"])
    cx = caixa_da_matriz(matriz, header) if matriz else None
    if not cx:
        # sem matriz: usa a própria nuvem de eventos como caixa
        cx = (min(xs), min(zs), max(1, max(xs) - min(xs) + 1),
              max(1, max(zs) - min(zs) + 1))
    ox, oz, cw, ch = cx

    def conv(e):
        x = int((e["x"] - ox) * (larg - 1) / max(1, cw - 1))
        y = int((e["z"] - oz) * (alt - 1) / max(1, ch - 1))
        return min(max(x, 0), larg - 1), min(max(y, 0), alt - 1)
    return conv


def main():
    sprites = V.sprites_utilizaveis()
    V.confere_tabela_de_trocas(sprites)
    movimentos = V.constantes("include/constants/event_object_movement.h", "MOVEMENT_TYPE_")
    layouts = {l["id"]: l for l in json.load(
        open(os.path.join(REPO, "data/layouts/layouts.json")))["layouts"]}

    heads = headers_do_platinum()
    por_chave = {}
    for h, (ev, mx) in heads.items():
        por_chave.setdefault(chave(h), (h, ev, mx))

    nossos = mapas_editaveis_sinnoh()
    casados, sem_par = [], []
    for m in nossos:
        h = APELIDOS.get(m)
        alvo = (h,) + heads[h] if h in heads else por_chave.get(chave(m))
        (casados.append((m,) + alvo) if alvo else sem_par.append(m))

    print(f"mapas de Sinnoh nossos: {len(nossos)}  casados: {len(casados)}  "
          f"sem par no Platinum: {len(sem_par)}")
    if "--sem-par" in sys.argv:
        for m in sem_par:
            print("   ", m)

    stats = {"objetos": 0, "placas": 0, "fora_hidden": 0, "fora_mobilia": 0,
             "fora_coord": 0, "fora_sem_espaco": 0, "fora_nome_proprio": 0,
             "trocas": 0, "mapas": 0, "ja_importado": 0}
    trocados, deixados = {}, {}
    for meu, header, arq_ev, matriz in casados:
        pe = os.path.join(PLAT, "res/field/events", arq_ev + ".json")
        if not os.path.exists(pe):
            continue
        fonte = json.load(open(pe))
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        d = json.load(open(pm))
        L = layouts[d["layout"]]
        larg, alt = L["width"], L["height"]

        conv = conversor_de_coordenada(fonte, larg, alt, header, matriz)
        if conv is None:
            continue

        existentes = (d.get("object_events") or []) + (d.get("bg_events") or [])
        if any(e.get("origem") == "pokeplatinum" for e in existentes):
            stats["ja_importado"] += 1
            continue
        ja = {(o.get("x"), o.get("y")) for o in (d.get("object_events") or [])}
        ja |= {(o.get("x"), o.get("y")) for o in (d.get("bg_events") or [])}
        # ponytail: NÃO tratar tile de warp como ocupado. Parecia defeito ter
        # placa em cima de porta, e 4 chegaram a ser removidas em 05/08/2026.
        # Medido depois, contra o jogo original: nós temos 30 de 2376 placas
        # sobre warp (1,26%), o pokeemerald vanilla tem 19 de 720 (2,64%) e o
        # pokefirered 5 de 702 (0,71%). O vanilla tem o DOBRO da nossa taxa:
        # é padrão do jogo, não defeito, e filtrar tiraria placa boa.
        novos_obj, novas_placas = [], []

        for e in fonte.get("object_events", []):
            g = e.get("graphics_id", "")
            # ponytail: comparar contra o nome INTEIRO fazia "VENT" casar com
            # "OBJ_EVENT_GFX_ACE_TRAINER_F" (e-VENT-o) e jogar 806 NPC fora em
            # silêncio. Substring só vale depois de tirar o prefixo comum.
            classe = g.replace("OBJ_EVENT_GFX_", "")
            # Ordem importa para o relatório: mobiliário sai como mobiliário, e
            # só depois o que sobrou é medido pela hidden_flag.
            if any(t in classe for t in GRAFICOS_PROIBIDOS):
                stats["fora_mobilia"] += 1
                continue
            if any(t in classe for t in NOMES_PROPRIOS):
                stats["fora_nome_proprio"] += 1
                deixados[g] = deixados.get(g, 0) + 1
                continue
            if str(e.get("hidden_flag", "0")) not in ("0", "0x0"):
                stats["fora_hidden"] += 1
                continue
            if any(t in classe for t in GRAFICOS_PLACA):
                x, y = conv(e)
                if (x, y) not in ja:
                    ja.add((x, y))
                    novas_placas.append(placa(x, y))
                continue
            if g not in sprites:
                novo = V.TROCA_SPRITE.get(g)
                if not novo:
                    trocados[g] = trocados.get(g, 0) + 1
                    novo = V.SPRITE_PADRAO
                stats["trocas"] += 1
                g = novo
            mov = e.get("movement_type", V.MOVIMENTO_PADRAO)
            if mov not in movimentos:
                mov = V.MOVIMENTO_PADRAO
            x, y = conv(e)
            pos = livre(layouts, d["layout"], x, y, ja)
            if pos is None:
                stats["fora_sem_espaco"] += 1
                continue
            ja.add(pos)
            novos_obj.append({
                "graphics_id": g, "x": pos[0], "y": pos[1], "elevation": 3,
                "movement_type": mov,
                "movement_range_x": e.get("movement_range_x", 0),
                "movement_range_y": e.get("movement_range_z", 0),
                "trainer_type": "TRAINER_TYPE_NONE",
                "trainer_sight_or_berry_tree_id": "0",
                "script": "0", "flag": "0", **MARCA,
            })

        for e in fonte.get("bg_events", []):
            x, y = conv(e)
            if (x, y) in ja:
                continue
            ja.add((x, y))
            novas_placas.append(placa(x, y))

        stats["fora_coord"] += len(fonte.get("coord_events", []))
        if not (novos_obj or novas_placas):
            continue
        stats["objetos"] += len(novos_obj)
        stats["placas"] += len(novas_placas)
        stats["mapas"] += 1
        # Objeto novo SEMPRE no fim: a save guarda índice de objeto.
        d["object_events"] = (d.get("object_events") or []) + novos_obj
        d["bg_events"] = (d.get("bg_events") or []) + novas_placas
        if APLICAR:
            json.dump(d, open(pm, "w"), indent=2, ensure_ascii=False)

    print("\nresumo:", stats)
    if trocados:
        print("\nsprites sem troca conhecida (viraram", V.SPRITE_PADRAO + "):")
        for g, n in sorted(trocados.items(), key=lambda kv: -kv[1]):
            print(f"  {n:5}  {g}")
    if deixados:
        print("\nNPC deixado de fora por ser nome próprio sem sprite:")
        for g, n in sorted(deixados.items(), key=lambda kv: -kv[1]):
            print(f"  {n:5}  {g}")
    print("\naplicado" if APLICAR else "\nnada escrito (use --aplicar)")
    return 0


def placa(x, y):
    return {"type": "sign", "x": x, "y": y, "elevation": 0,
            "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
            "script": SCRIPT_PLACA, **MARCA}


def livre(layouts, layout_id, x, y, ocupados, raio=8):
    """Tile andável e desocupado mais perto de (x,y). None se não houver."""
    for r in range(0, raio + 1):
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                if r and max(abs(dx), abs(dy)) != r:
                    continue
                p = (x + dx, y + dy)
                if p in ocupados:
                    continue
                if V.colisao(layouts, layout_id, *p) == 0:
                    return p
    return None


def demo():
    """As duas regras que a primeira versão errou."""
    # 1. andar escrito de dois jeitos é o mesmo andar
    assert chave("JubilifeCity_PokemonCenter_1F") == chave("MAP_HEADER_JUBILIFE_CITY_POKECENTER_1F")
    # 2. mapas diferentes continuam diferentes
    assert chave("Route205_North") != chave("MAP_HEADER_ROUTE_205_SOUTH")
    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
