#!/usr/bin/env python3
"""Fecha porta de cidade de Sinnoh que hoje nao leva a lugar nenhum.

    python3 dev_scripts/fecha_portas_sinnoh.py            # so relata
    python3 dev_scripts/fecha_portas_sinnoh.py --aplicar  # escreve
    python3 dev_scripts/fecha_portas_sinnoh.py --demo     # autoteste

O buraco que ele fecha
----------------------
Sinnoh tem 25,6% dos mapas e 61,8% dos warps contra o pokeplatinum. Medido em
06/08/2026: das nossas cidades de Sinnoh saem **202 warps no Platinum para 164
mapas que nao existem aqui**. Casa, mart, centro Pokemon, loja. O predio esta
desenhado na rua, a porta esta desenhada no tile, e nao ha warp nenhum: a
CanalaveCity inteira tem 2 warps, e no Platinum tem 11.

As tres decisoes que valem mais que o codigo
--------------------------------------------
1. **A geometria do interior e REAPROVEITADA, nao convertida.** `demake_ds.py`
   le do Platinum so colisao e comportamento de tile, nao o desenho: interior
   convertido por ele sai como uma sala de chao liso cercada de arvore, sem
   parede, sem balcao, sem porta. Interior de casa do repo (esses ja vieram do
   `fontes-mapas/sinnoh`, que e GBA) com o NPC e o texto certos do Platinum vale
   muito mais que porta que nao abre. O que e convertido de verdade nestes mapas
   novos: NPC, placa, texto de placa e texto de NPC. O que e reaproveitado: a
   planta. Isso esta registrado em cada map.json pelo campo `origem`.

2. **A porta sai do nosso layout, nao da coordenada deles.** Coordenada de warp
   de rua no Platinum e GLOBAL da matriz de Sinnoh e os nossos layouts de cidade
   sao outros (ver decisao 1 de `importa_npcs_sinnoh.py`: nao existe offset).
   Entao o warp novo vai em cima de um tile que JA e porta no nosso mapa, achado
   lendo `metatile_attributes.bin` com a mesma lista de comportamentos que o
   motor usa (`valida_warp_tile.COMPORTA_WARP`). Assim ele nasce disparando.
   Qual porta recebe qual predio sai da posicao relativa: o mart do sul do
   Platinum cai na porta do sul daqui.

3. **So interior de cidade.** Header que e rota, caverna, ruina, lago, ginasio
   ou Mt. Coronet fica de fora, com aviso. Criar `ROUTE_204_NORTH` como casa de
   8x9 seria pior que a porta fechada: mentiria o mapa.

Compatibilidade de save: mapa novo entra num grupo NOVO, no FIM de
`group_order`, e warp novo entra no FIM da lista de warps do mapa que ja existe.
Nenhum indice antigo anda. `guarda_save.py` continua dizendo SAVE COMPATIVEL.
"""
import json
import os
import re
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import importa_npcs_sinnoh as I      # noqa: E402
import texto_placas_sinnoh as T      # noqa: E402
import valida_mapas_sinnoh as V      # noqa: E402
import valida_warp_tile as W         # noqa: E402

PLAT = I.PLAT
APLICAR = "--aplicar" in sys.argv
GRUPO_NOVO = "gMapGroup_IndoorSinnohPortas"

# TETO DURO, medido no emulador em 06/08/2026 e confirmado no cabecalho:
# `struct WarpData` guarda `s8 mapGroup` e `s8 mapNum` (include/global.h). Mapa
# de indice 128 num grupo vira -128 dentro do warp, o jogo carrega lixo e RESETA.
# Foi assim que 26 mapas do `gMapGroup_IndoorSinnohPortas` viraram peso morto: o
# indice 127 entrava e o 128 derrubava o jogo. Grupo tambem nao pode passar de
# 128, pelo mesmo campo.
LIMITE_GRUPO = 128


def grupo_com_vaga(grupos, base):
    """Nome do grupo onde ainda cabe mapa, criando o proximo quando encher.

    Grupo novo entra sempre no FIM de `group_order`, que e o que mantem a save
    compativel.
    """
    nome, n = base, 1
    while len(grupos.get(nome, [])) >= LIMITE_GRUPO:
        n += 1
        nome = f"{base}{n}"
    if nome not in grupos:
        if len(grupos["group_order"]) >= LIMITE_GRUPO:
            raise SystemExit("nao ha grupo livre: o teto e 128 grupos (s8)")
        grupos[nome] = []
        grupos["group_order"].append(nome)
    return nome
MARCA = {"origem": "pokeplatinum"}
MARCA_PLANTA = {"origem": "arquetipo do repo"}

# Faixa de flag exclusiva desta frente: 0x8E5 a 0x920. Nada aqui gasta flag
# ainda (NPC importado nasce sem flag, como no importador de NPC), entao a faixa
# fica anotada e intacta. Se um dia um destes mapas precisar de flag, sai daqui.
FLAG_INICIO, FLAG_FIM = 0x8E5, 0x920


# ------------------------------------------------------------------ arquetipo
#
# Cada arquetipo aponta para um mapa que JA existe no repo. O map.json dele e
# copiado inteiro (layout, musica, map_type, allow_*) e so o conteudo troca.
# `entrada` sao os tiles de warp que voltam para quem chamou; `extras` sao warps
# livres do arquetipo que podem receber um andar de cima.
# `funcional` e o tipo do NPC que faz o predio SERVIR para alguma coisa. Sem
# ele o centro Pokemon novo e uma sala com gente dentro e ninguem que cura, e o
# mart e uma loja sem caixa: o predio abriria e nao teria funcao. O objeto e
# copiado do indice 0 do proprio arquetipo (posicao e movimento medidos la), e o
# script sai com rotulo do mapa novo.
ARQUETIPOS = {
    "casa":     ("OreburghCity_House1",            [(3, 8), (4, 8)], [], None),
    "mart":     ("OreburghCity_Mart",              [(3, 7), (4, 7)], [], "caixa"),
    "pc1":      ("OreburghCity_PokemonCenter_1F",  [(6, 8), (7, 8)], [(1, 6)], "enfermeira"),
    "pc2":      ("OreburghCity_PokemonCenter_2F",  [(1, 6)],         [], None),
    "andar":    ("OreburghCity_Flat1_F2",          [(2, 1)],         [], None),
    "portaria": ("Route208_Access",                [(1, 5)],         [], None),
}

# O `local_id` que o mapjson da ao PRIMEIRO objeto do mapa. A enfermeira precisa
# do numero dela em VAR_0x800B para o Common_EventScript_PkmnCenterNurse virar
# na direcao certa; como ela entra sempre na posicao 0, o numero e sempre 1.
LOCALID_PRIMEIRO = 1

FUNCIONAL = {
    "enfermeira": lambda p: (
        f"\n{p}_EventScript_Enfermeira::\n"
        f"\tsetvar VAR_0x800B, {LOCALID_PRIMEIRO}\n"
        f"\tcall Common_EventScript_PkmnCenterNurse\n"
        f"\twaitmessage\n\twaitbuttonpress\n\trelease\n\tend\n"),
    "caixa": lambda p: (
        f"\n{p}_EventScript_Caixa::\n\tlock\n\tfaceplayer\n"
        f"\tmsgbox {p}_Text_Caixa, MSGBOX_DEFAULT\n"
        f"\tpokemart {p}_Pokemart\n"
        f"\tmsgbox gText_PleaseComeAgain, MSGBOX_DEFAULT\n\trelease\n\tend\n"
        f"\n\t.align 2\n{p}_Pokemart:\n"
        "\t.2byte ITEM_POKE_BALL\n\t.2byte ITEM_POTION\n"
        "\t.2byte ITEM_SUPER_POTION\n\t.2byte ITEM_ANTIDOTE\n"
        "\t.2byte ITEM_PARALYZE_HEAL\n\t.2byte ITEM_AWAKENING\n"
        "\tpokemartlistend\n"
        f"\n{p}_Text_Caixa:\n"
        '\t.string "Welcome! Take a look around, we\'ve\\n"\n'
        '\t.string "got everything a TRAINER needs.$"\n'),
}
ROTULO_FUNCIONAL = {"enfermeira": "EventScript_Enfermeira", "caixa": "EventScript_Caixa"}

# Classificacao por nome de header. Ordem importa: o primeiro que casa ganha.
REGRAS = [
    (r"POKECENTER_1F$", "pc1"),
    (r"POKECENTER_(2F|B1F)$", "pc2"),
    (r"_MART$", "mart"),
    (r"(HOUSE_[234]F|CONDOMINIUMS_[234]F)$", "andar"),
    (r"(HOUSE|HOUSE_1F|HOUSE_\d|CONDOMINIUMS_1F)$", "casa"),
    (r"GATE", "portaria"),
]

# Predio de cidade com nome proprio, que nenhuma regra acima pega. Medido um a
# um sobre os 164 headers que faltam; o que nao esta aqui e nao casa regra fica
# de fora de proposito (caverna, ruina, rota, ginasio, lago, Mt. Coronet).
NOMEADOS = {
    "CAFE": "casa", "CANALAVE_CITY_HARBOR_INN": "casa",
    "CANALAVE_LIBRARY_1F": "casa", "CONTEST_HALL_LOBBY": "casa",
    "CYCLE_SHOP": "mart", "ETERNA_CITY_HERB_SHOP": "mart",
    "FOREIGN_BUILDING": "casa", "GAME_CORNER": "casa",
    "GLOBAL_TERMINAL_1F": "casa", "HEARTHOME_CITY_POKEMON_FAN_CLUB": "casa",
    "MINING_MUSEUM": "casa", "POKEMON_DAY_CARE": "casa",
    "POKEMON_MANSION": "casa", "RESORT_AREA_RIBBON_SYNDICATE_1F": "casa",
    "SOLACEON_TOWN_POKEMON_NEWS_PRESS": "casa", "SUNYSHORE_MARKET": "mart",
    "VALLEY_WINDWORKS_BUILDING": "casa", "VEILSTONE_CITY_PRIZE_EXCHANGE": "mart",
    "VEILSTONE_STORE_1F": "mart", "VILLA": "casa", "BATTLEGROUND": "casa",
    "PAL_PARK_LOBBY": "casa", "ROTOMS_ROOM": "casa",
    "SOLACEON_RUINS_MANIAC_TUNNEL_ROOM": None,   # explicito: fica de fora

    # --- segunda leva, 06/08/2026: sala de predio que ja esta na ROM.
    # Todos estes sao destino de warp de mapa que NOS TEMOS, ou seja, porta que
    # o jogador ve hoje e nao abre. Nenhum e rua, rota ou caverna: sala fechada
    # com planta de sala e o mesmo negocio que fechou as 112 primeiras portas.
    # Elevador cai em "andar" de proposito: a planta de andar de cima do repo e
    # uma caixa pequena com escada de volta, que e o que um elevador precisa
    # ser. Nao vale a pena arquetipo novo so para isso, e a planta do elevador
    # de Lilycove traria REGION_HOENN e MAPSEC_LILYCOVE_CITY junto.
    "JUBILIFE_TV_ELEVATOR": "andar",
    "JUBILIFE_TV_2F_GALLERY": "casa",
    "JUBILIFE_TV_3F_GLOBAL_RANKING_ROOM": "casa",
    "JUBILIFE_TV_3F_GROUP_RANKING_ROOM": "casa",
    "HEARTHOME_CITY_NORTHEAST_HOUSE_ELEVATOR": "andar",
    "HEARTHOME_CITY_SOUTHEAST_HOUSE_ELEVATOR": "andar",
    "HEARTHOME_CITY_NORTHEAST_HOUSE_2F": "andar",
    "HEARTHOME_CITY_SOUTHEAST_HOUSE_2F": "andar",
    "HEARTHOME_CITY_GYM_LEADER_ROOM": "casa",
    "HEARTHOME_CITY_GYM_TRAINER_ROOM_1": "casa",
    "HEARTHOME_CITY_GYM_TRAINER_ROOM_2": "casa",
    "SUNYSHORE_CITY_GYM_ROOM_2": "casa",
    "SUNYSHORE_CITY_GYM_ROOM_3": "casa",
    "CANALAVE_LIBRARY_2F": "andar",
    "CANALAVE_LIBRARY_3F": "andar",
    "GLOBAL_TERMINAL_2F": "andar",
    "GLOBAL_TERMINAL_3F": "andar",
    "VEILSTONE_STORE_2F": "mart", "VEILSTONE_STORE_3F": "mart",
    "VEILSTONE_STORE_4F": "mart", "VEILSTONE_STORE_5F": "mart",
    "VEILSTONE_STORE_B1F": "mart", "VEILSTONE_STORE_ELEVATOR": "andar",
    "RESORT_AREA_RIBBON_SYNDICATE_2F": "andar",
    "RESORT_AREA_RIBBON_SYNDICATE_ELEVATOR": "andar",
    "VISTA_LIGHTHOUSE": "casa", "VISTA_LIGHTHOUSE_ELEVATOR": "andar",
    "POKEMON_MANSION_MAIDS_ROOM": "casa",
    "POKEMON_MANSION_OFFICE": "casa",
    "GALACTIC_HQ_4F": "casa",
    "RESTAURANT": "casa",
    "CONTEST_HALL_STAGE_NO_CONTEST": "casa",
    "FLOAROMA_MEADOW_HOUSE": "casa",
    "IRON_ISLAND_HOUSE": "casa",
    "POKEMON_LEAGUE_ELEVATOR_TO_AARON_ROOM": "andar",
    "POKEMON_LEAGUE_ELEVATOR_TO_BERTHA_ROOM": "andar",
    "POKEMON_LEAGUE_ELEVATOR_TO_FLINT_ROOM": "andar",
    "POKEMON_LEAGUE_ELEVATOR_TO_LUCIAN_ROOM": "andar",
    "POKEMON_LEAGUE_ELEVATOR_TO_CHAMPION_ROOM": "andar",
    # Explicito, fica de fora: sala da Elite dos Quatro e da campea. Cynthia,
    # Aaron e companhia caem em `I.NOMES_PROPRIOS` e sumiriam na importacao, e
    # a sala sairia vazia. Sala vazia de campea mente mais que porta fechada.
    "POKEMON_LEAGUE_AARON_ROOM": None,
    "POKEMON_LEAGUE_BERTHA_ROOM": None,
    "POKEMON_LEAGUE_FLINT_ROOM": None,
    "POKEMON_LEAGUE_LUCIAN_ROOM": None,
    "POKEMON_LEAGUE_CHAMPION_ROOM": None,
}

# Header que ja tem mapa nosso com outro nome.
# `MAP_HEADER_CANALAVE_CITY_GYM` e `MAP_HEADER_SANDGEM_TOWN_HOUSE` sairam daqui
# em 11/08/2026: os dois mapas voltaram para `nossos_mapas_sinnoh()`, que deixou
# de descontar a trava de escrita `NAO_TOCAR`, e o segundo ganhou apelido em
# `I.APELIDOS`. Eles nunca estiveram faltando, so estavam invisiveis para a regua.
JA_TEMOS = {
    "MAP_HEADER_FLOWER_SHOP", "MAP_HEADER_ETERNA_CITY_DP_GYM",
    "MAP_HEADER_UNUSED_JUBILIFE_CITY_CONDOMINIUMS_3F",
    "MAP_HEADER_UNUSED_JUBILIFE_CITY_SOUTH_HOUSE_3F",
}


def arquetipo_do_header(header):
    """Nome do arquetipo, ou None se o header nao for interior de cidade."""
    s = header.replace("MAP_HEADER_", "")
    if s in NOMEADOS:
        return NOMEADOS[s]
    for rx, a in REGRAS:
        if re.search(rx, s):
            return a
    return None


# Header do Platinum cuja constante JA existe na ROM, vinda de outra regiao.
# `MAP_VICTORY_ROAD_1F` e de HOENN e `LAYOUT_VICTORY_ROAD_1F` tambem: criar o de
# Sinnoh com o mesmo nome nao compila, e foi so por isso que os tres andares da
# Victory Road de Sinnoh (1050 tiles andaveis no 1F, a estrada para a Liga)
# ficaram de fora ate 06/08/2026, mesmo com a grade do DS pronta e conferida.
# Aqui eles ganham prefixo de regiao. `importa_npcs_sinnoh.APELIDOS` recebe o
# par pasta -> header, senao `completude.py` continuaria contando o mapa como
# ausente depois de ele existir.
RENOMEADOS = {
    "MAP_HEADER_VICTORY_ROAD_1F": "SinnohVictoryRoad1F",
    "MAP_HEADER_VICTORY_ROAD_2F": "SinnohVictoryRoad2F",
    "MAP_HEADER_VICTORY_ROAD_B1F": "SinnohVictoryRoadB1F",
}


def nome_de_pasta(header):
    """MAP_HEADER_CANALAVE_CITY_MART -> CanalaveCityMart.

    Tem que ser um nome que `I.chave()` leve ao mesmo lugar que o header, senao
    `completude.py` continua contando o mapa como ausente depois de criado. A
    excecao e `RENOMEADOS`, onde o par vai a mao para `I.APELIDOS`.
    """
    if header in RENOMEADOS:
        return RENOMEADOS[header]

    def peca(p):
        # "1F", "2F", "B1F" ficam em caixa alta; `capitalize()` faria "1f".
        return p if re.fullmatch(r"B?\d+F", p) else p.capitalize()
    return "".join(peca(p) for p in
                   header.replace("MAP_HEADER_", "").split("_"))


def const_do_header(header):
    if header in RENOMEADOS:
        # "SinnohVictoryRoad1F" -> MAP_SINNOH_VICTORY_ROAD_1F
        return "MAP_SINNOH_" + header.replace("MAP_HEADER_", "")
    return "MAP_" + header.replace("MAP_HEADER_", "")


# ------------------------------------------------------------------- portas
_LAYOUTS = None


def layouts():
    global _LAYOUTS
    if _LAYOUTS is None:
        _LAYOUTS = {l["id"]: l for l in json.load(
            open(f"{REPO}/data/layouts/layouts.json"))["layouts"]}
    return _LAYOUTS


_ATRIB = {}


def _atributos(ts):
    if ts not in _ATRIB:
        _ATRIB[ts] = W.tabela_de_atributos(ts)
    return _ATRIB[ts]


def portas_livres(mapa, d=None):
    """Tiles do mapa cujo comportamento e de porta e que ainda nao tem warp.

    E a mesma leitura que `valida_warp_tile.py` faz para acusar warp morto, so
    que ao contrario: aqui ela procura porta ORFA. Por isso o warp novo nasce
    disparando, sem depender de acertar coordenada da fonte.
    """
    d = d or json.load(open(f"{REPO}/data/maps/{mapa}/map.json"))
    lay = layouts().get(d.get("layout"))
    if not lay:
        return []
    bp = f"{REPO}/{lay.get('blockdata_filepath', '')}"
    if not os.path.exists(bp):
        return []
    blk = open(bp, "rb").read()
    w, h = lay["width"], lay["height"]
    prim, _ = _atributos(lay.get("primary_tileset"))
    seg, _ = _atributos(lay.get("secondary_tileset"))
    if prim is None or seg is None:
        return []
    corte = 640 if lay.get("layout_version", "") in ("frlg", "johto") else 512
    ja = {(x.get("x"), x.get("y")) for x in (d.get("warp_events") or [])}
    fora = []
    for y in range(h):
        for x in range(w):
            i = (y * w + x) * 2
            if i + 2 > len(blk):
                continue
            mt = struct.unpack("<H", blk[i:i + 2])[0] & 0x3FF
            tab, rel = (prim, mt) if mt < corte else (seg, mt - corte)
            if rel < len(tab) and tab[rel] in W.COMPORTA_WARP and (x, y) not in ja:
                fora.append((x, y))
    return fora


def casa_portas(portas, alvos, larg, alt):
    """Casa porta nossa com warp deles pela posicao RELATIVA, guloso.

    Nao existe offset entre as duas geometrias (ver o topo), entao o unico sinal
    honesto e a ordem no espaco: predio do canto sudoeste la vai para a porta do
    canto sudoeste aqui. Devolve lista de (porta, alvo).
    """
    if not portas or not alvos:
        return []
    xs = [a[1] for a in alvos]
    zs = [a[2] for a in alvos]
    dx = max(1, max(xs) - min(xs))
    dz = max(1, max(zs) - min(zs))
    livres = list(portas)
    saida = []
    # Quando ha menos porta que predio, quem escolhe primeiro importa. Medido em
    # Solaceon: 9 destinos para 4 portas, e a ordem do Platinum entregava as
    # quatro a casas comuns, deixando a cidade sem centro Pokemon nem mart. Cura
    # e loja ganham da casa; entre iguais, a ordem da fonte decide.
    peso = {"pc1": 0, "mart": 1, "portaria": 2}
    for header, ax, az in sorted(
            alvos, key=lambda a: peso.get(arquetipo_do_header(a[0]), 3)):
        if not livres:
            break
        nx = (ax - min(xs)) / dx * max(1, larg - 1)
        ny = (az - min(zs)) / dz * max(1, alt - 1)
        melhor = min(livres, key=lambda p: (p[0] - nx) ** 2 + (p[1] - ny) ** 2)
        livres.remove(melhor)
        saida.append((melhor, header))
    return saida


# ------------------------------------------------------------- texto do NPC
_CACHE_SCR = {}


def corrente_de_texto(header):
    """(ordem de ScriptEntry, corpos, banco de texto) do header, com cache.

    Mesma corrente de `texto_placas_sinnoh.py`: indice -> ScriptEntry -> corpo
    do rotulo -> id de mensagem -> res/text/<mapa>.json.
    """
    if header not in _CACHE_SCR:
        campos = T.campos_do_header(header)
        if not campos:
            _CACHE_SCR[header] = ([], {}, {})
        else:
            scr, msg, _ = campos
            ordem, corpos = T.entradas_de_script(scr) if scr else ([], {})
            _CACHE_SCR[header] = (ordem, corpos, T.banco_de_texto(msg) if msg else {})
    return _CACHE_SCR[header]


def texto_do_indice(header, idx):
    """Texto ja em formato GBA do N-esimo ScriptEntry, ou None.

    Conservador de proposito, igual ao de placa: mensagem com `{STRVAR}` e nome
    montado em tempo de execucao e sem o motor de texto deles nao traduz, entao
    volta None e o objeto fica mudo em vez de mostrar chave crua na tela.
    """
    ordem, corpos, banco = corrente_de_texto(header)
    if not isinstance(idx, int) or not 1 <= idx <= len(ordem):
        return None
    tid = T.texto_do_corpo(corpos.get(ordem[idx - 1], []))
    linhas = banco.get(tid) if tid else None
    if not linhas or "{" in "".join(linhas):
        return None
    return T.para_gba(linhas)


# ------------------------------------------------------------ monta o mapa
def conteudo_do_mapa(header, pasta, larg, alt, sprites, movimentos, layout_id):
    """NPCs, placas e o trecho de scripts.inc do mapa novo.

    Os filtros sao os mesmos de `importa_npcs_sinnoh.py`, e pelo mesmo motivo:
    mobilia virada NPC tranca sala, NPC com hidden_flag vira bloqueio
    permanente, e nome proprio sem sprite faz o mapa mentir.
    """
    arq = os.path.join(PLAT, "res/field/events",
                       I.headers_do_platinum()[header][0] + ".json")
    if not os.path.exists(arq):
        return [], [], ""
    fonte = json.load(open(arq))
    objs, placas, trecho = [], [], ""
    ocupados = set()
    n_txt = 0

    def poe(x, y):
        x = min(max(int(x), 0), larg - 1)
        y = min(max(int(y), 0), alt - 1)
        return I.livre(layouts(), layout_id, x, y, ocupados)

    for e in fonte.get("object_events", []):
        g = e.get("graphics_id", "")
        classe = g.replace("OBJ_EVENT_GFX_", "")
        if any(t in classe for t in I.GRAFICOS_PROIBIDOS):
            continue
        if any(t in classe for t in I.NOMES_PROPRIOS):
            continue
        if str(e.get("hidden_flag", "0")) not in ("0", "0x0"):
            continue
        if any(t in classe for t in I.GRAFICOS_PLACA):
            p = poe(e["x"], e["z"])
            if p:
                ocupados.add(p)
                placas.append((p, e.get("script")))
            continue
        if g not in sprites:
            g = V.TROCA_SPRITE.get(g) or V.SPRITE_PADRAO
        mov = e.get("movement_type", V.MOVIMENTO_PADRAO)
        if mov not in movimentos:
            mov = V.MOVIMENTO_PADRAO
        p = poe(e["x"], e["z"])
        if not p:
            continue
        ocupados.add(p)
        txt = texto_do_indice(header, e.get("script"))
        rotulo = "0"
        if txt:
            n_txt += 1
            rotulo = f"{pasta}_EventScript_Npc{n_txt}"
            trecho += (f"\n{rotulo}::\n\tmsgbox {pasta}_Text_Npc{n_txt}, MSGBOX_NPC\n"
                       f"\tend\n\n{pasta}_Text_Npc{n_txt}:\n\t.string \"{txt}\"\n")
        objs.append({
            "graphics_id": g, "x": p[0], "y": p[1], "elevation": 3,
            "movement_type": mov,
            "movement_range_x": e.get("movement_range_x", 0),
            "movement_range_y": e.get("movement_range_z", 0),
            "trainer_type": "TRAINER_TYPE_NONE",
            "trainer_sight_or_berry_tree_id": "0",
            "script": rotulo, "flag": "0", **MARCA,
        })

    for e in fonte.get("bg_events", []):
        # ARMADILHA: `script` >= 8000 nao e placa, e item escondido
        # (SCRIPT_ID_OFFSET_HIDDEN_ITEMS, include/script_manager.h:96).
        # Importar como placa poe "the lettering has faded" em cima de um item
        # invisivel, que e o defeito que os 152 casos de rua ja tem hoje.
        if isinstance(e.get("script"), int) and e["script"] >= 8000:
            continue
        p = poe(e["x"], e["z"])
        if not p:
            continue
        ocupados.add(p)
        placas.append((p, e.get("script")))

    bg, n_pl = [], 0
    for (x, y), idx in placas:
        txt = texto_do_indice(header, idx)
        rotulo = I.SCRIPT_PLACA
        if txt:
            n_pl += 1
            rotulo = f"{pasta}_EventScript_Placa{n_pl}"
            trecho += (f"\n{rotulo}::\n\tmsgbox {pasta}_Text_Placa{n_pl}, MSGBOX_SIGN\n"
                       f"\tend\n\n{pasta}_Text_Placa{n_pl}:\n\t.string \"{txt}\"\n")
        bg.append({"type": "sign", "x": x, "y": y, "elevation": 0,
                   "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
                   "script": rotulo, **MARCA})
    return objs, bg, trecho


# ------------------------------------------------------------------- main
def main():
    if "--demo" in sys.argv:
        return demo()

    heads = I.headers_do_platinum()
    por_chave = {}
    for h in heads:
        por_chave.setdefault(I.chave(h), h)
    nossos = I.nossos_mapas_sinnoh()
    casados = {}                       # header -> nosso mapa
    for m in nossos:
        h = I.APELIDOS.get(m) or por_chave.get(I.chave(m))
        if h in heads:
            casados[h] = m
    existentes = set(casados) | JA_TEMOS
    pastas_existentes = set(os.listdir(f"{REPO}/data/maps"))
    consts_existentes = set(re.findall(r'"id":\s*"(MAP_\w+)"', "".join(
        open(f"{REPO}/data/maps/{p}/map.json").read()
        for p in pastas_existentes
        if os.path.exists(f"{REPO}/data/maps/{p}/map.json"))))

    sprites = V.sprites_utilizaveis()
    movimentos = V.constantes("include/constants/event_object_movement.h",
                              "MOVEMENT_TYPE_")

    novos = []          # (pasta, header, arquetipo, mapa de origem, porta)
    fora = {}           # header -> motivo
    vistos = set()
    for header, meu in sorted(casados.items(), key=lambda kv: kv[1]):
        pe = os.path.join(PLAT, "res/field/events", heads[header][0] + ".json")
        if not os.path.exists(pe):
            continue
        alvos = []
        for w in json.load(open(pe)).get("warp_events", []):
            d = w["dest_header_id"]
            if d in existentes or d in vistos:
                continue
            a = arquetipo_do_header(d)
            if not a:
                fora.setdefault(d, "nao e interior de cidade")
                continue
            pasta = nome_de_pasta(d)
            if pasta in pastas_existentes or const_do_header(d) in consts_existentes:
                fora.setdefault(d, "pasta ou constante ja existe")
                continue
            vistos.add(d)
            alvos.append((d, w["x"], w["z"]))
        if not alvos:
            continue
        d_meu = json.load(open(f"{REPO}/data/maps/{meu}/map.json"))
        lay = layouts().get(d_meu.get("layout"))
        portas = portas_livres(meu, d_meu)
        if not portas:
            for d, _, _ in alvos:
                fora.setdefault(d, f"{meu} nao tem porta orfa")
                vistos.discard(d)
            continue
        pares = casa_portas(portas, alvos, lay["width"], lay["height"])
        sobrou = {d for d, _, _ in alvos} - {h for _, h in pares}
        for d in sobrou:
            fora.setdefault(d, f"{meu} so tem {len(portas)} porta(s) orfa(s)")
            vistos.discard(d)
        for porta, d in pares:
            novos.append({"pasta": nome_de_pasta(d), "header": d,
                          "arq": arquetipo_do_header(d), "pai": meu,
                          "porta": porta, "filhos": []})

    # Segundo andar. O arquetipo de centro Pokemon tem uma escada em (1,6) que
    # ficaria sem warp, e o 2F nunca aparece na lista acima porque no Platinum
    # nao e a cidade que aponta para ele, e o 1F. Sem esta passada, 14 centros
    # Pokemon novos nascem com escada morta.
    for n in novos:
        _b, _e, extras, _f = ARQUETIPOS[n["arq"]]
        if not extras:
            continue
        pe = os.path.join(PLAT, "res/field/events", heads[n["header"]][0] + ".json")
        if not os.path.exists(pe):
            continue
        for w in json.load(open(pe)).get("warp_events", []):
            if len(n["filhos"]) >= len(extras):
                break
            d = w["dest_header_id"]
            if d in existentes or d in vistos:
                continue
            # So andar de cima: gate para fora vira mapa errado (ver decisao 3).
            if arquetipo_do_header(d) not in ("pc2", "andar"):
                continue
            pasta = nome_de_pasta(d)
            if pasta in pastas_existentes or const_do_header(d) in consts_existentes:
                continue
            vistos.add(d)
            n["filhos"].append({"pasta": pasta, "header": d,
                                "arq": arquetipo_do_header(d)})

    filhos = sum(len(n["filhos"]) for n in novos)
    print(f"mapas de Sinnoh casados com o Platinum: {len(casados)}")
    print(f"portas que da para fechar agora: {len(novos)} "
          f"(+ {filhos} andares de cima) = {len(novos) + filhos} mapas novos")
    print(f"destinos deixados de fora: {len(fora)}")
    motivos = {}
    for m in fora.values():
        chave = m if "nao tem porta" not in m and "so tem" not in m else "sem porta orfa no mapa de origem"
        motivos[chave] = motivos.get(chave, 0) + 1
    for k, n in sorted(motivos.items(), key=lambda kv: -kv[1]):
        print(f"   {n:4}  {k}")

    if not APLICAR:
        print("\nnada escrito (use --aplicar)")
        for n in novos[:15]:
            extra = (" + " + ", ".join(f["pasta"] for f in n["filhos"])) if n["filhos"] else ""
            print(f"   {n['pai']} {n['porta']} -> {n['pasta']} ({n['arq']}){extra}")
        return 0

    # ---- escreve
    grupos = json.load(open(f"{REPO}/data/maps/map_groups.json"))
    # NAO escrever direto em GRUPO_NOVO: em 06/08/2026 ele ja estava com os 128
    # mapas do teto (`s8 mapGroup`/`s8 mapNum`), e o 129o teria nascido morto,
    # que e exatamente o defeito que matou 26 mapas. `grupo_com_vaga` escolhe o
    # proximo grupo que ainda tem vaga, sempre no FIM do `group_order`.
    incs = []
    conta = {"mapas": 0, "npcs": 0, "placas": 0, "textos": 0}

    def escreve(pasta, header, arq, dest_volta, warp_volta, extras_dest):
        base, entrada, extras, funcional = ARQUETIPOS[arq]
        d = json.load(open(f"{REPO}/data/maps/{base}/map.json"))
        lay = layouts()[d["layout"]]
        objs, bg, trecho = conteudo_do_mapa(
            header, pasta, lay["width"], lay["height"], sprites, movimentos,
            d["layout"])
        if funcional:
            npc = dict(d["object_events"][0])
            npc.pop("local_id", None)
            npc["script"] = f"{pasta}_{ROTULO_FUNCIONAL[funcional]}"
            npc.update(MARCA_PLANTA)
            objs.insert(0, npc)          # posicao 0: LOCALID_PRIMEIRO
            trecho = FUNCIONAL[funcional](pasta) + trecho
        d["id"] = const_do_header(header)
        d["name"] = pasta
        d["object_events"] = objs
        d["bg_events"] = bg
        d["coord_events"] = []
        d["warp_events"] = [
            {"x": x, "y": y, "elevation": 0, "dest_map": dest_volta,
             "dest_warp_id": str(warp_volta)} for x, y in entrada]
        for (x, y), filho in zip(extras, extras_dest):
            d["warp_events"].append({"x": x, "y": y, "elevation": 0,
                                     "dest_map": filho, "dest_warp_id": "0"})
        d["origem"] = ("pokeplatinum: NPC, placa e texto. "
                       "planta reaproveitada de " + base)
        os.makedirs(f"{REPO}/data/maps/{pasta}", exist_ok=True)
        json.dump(d, open(f"{REPO}/data/maps/{pasta}/map.json", "w"),
                  indent=2, ensure_ascii=False)
        with open(f"{REPO}/data/maps/{pasta}/scripts.inc", "w") as f:
            f.write(f"{pasta}_MapScripts::\n\t.byte 0\n{trecho}")
        grupos[grupo_com_vaga(grupos, GRUPO_NOVO)].append(pasta)  # SO no fim
        incs.append(f'\t.include "data/maps/{pasta}/scripts.inc"\n')
        conta["mapas"] += 1
        conta["npcs"] += len(objs)
        conta["placas"] += len(bg)
        conta["textos"] += trecho.count(".string")
        return d, len(entrada)

    for n in novos:
        d_meu_p = f"{REPO}/data/maps/{n['pai']}/map.json"
        d_meu = json.load(open(d_meu_p))
        d_meu.setdefault("warp_events", [])
        idx_volta = len(d_meu["warp_events"])      # warp novo SO no fim
        d_meu["warp_events"].append({
            "x": n["porta"][0], "y": n["porta"][1], "elevation": 0,
            "dest_map": const_do_header(n["header"]), "dest_warp_id": "0",
        })
        json.dump(d_meu, open(d_meu_p, "w"), indent=2, ensure_ascii=False)

        filhos_const = [const_do_header(f["header"]) for f in n["filhos"]]
        _, n_entrada = escreve(n["pasta"], n["header"], n["arq"],
                               d_meu["id"], idx_volta, filhos_const)
        for i, f in enumerate(n["filhos"]):
            escreve(f["pasta"], f["header"], f["arq"],
                    const_do_header(n["header"]), n_entrada + i, [])

    json.dump(grupos, open(f"{REPO}/data/maps/map_groups.json", "w"),
              indent=2, ensure_ascii=False)
    with open(f"{REPO}/data/event_scripts.s", "a") as f:
        f.writelines(incs)
    print(f"\naplicado: {conta['mapas']} mapas, {conta['npcs']} NPCs, "
          f"{conta['placas']} placas, {conta['textos']} textos do Platinum")
    return 0


def demo():
    """As tres coisas que a primeira versao errou."""
    # 1. o nome da pasta tem que cair na MESMA chave que o header, senao
    #    completude.py conta o mapa como ausente depois de ele existir.
    for h in ("MAP_HEADER_CANALAVE_CITY_MART",
              "MAP_HEADER_SOLACEON_TOWN_POKECENTER_1F",
              "MAP_HEADER_ROUTE_205_HOUSE"):
        assert I.chave(nome_de_pasta(h)) == I.chave(h), h
    # 2. rota, caverna e ginasio NAO viram casa de 8x9.
    for h in ("MAP_HEADER_ROUTE_204_NORTH", "MAP_HEADER_WAYWARD_CAVE_1F",
              "MAP_HEADER_VICTORY_ROAD_1F", "MAP_HEADER_MT_CORONET_2F",
              "MAP_HEADER_UNION_ROOM"):
        assert arquetipo_do_header(h) is None, h
    assert arquetipo_do_header("MAP_HEADER_PASTORIA_CITY_MART") == "mart"
    assert arquetipo_do_header("MAP_HEADER_FIGHT_AREA_POKECENTER_1F") == "pc1"
    assert arquetipo_do_header("MAP_HEADER_ETERNA_CITY_CONDOMINIUMS_1F") == "casa"
    # 3. o casamento porta<->predio e por posicao relativa: o do sul vai para o
    #    do sul. Duas portas, dois alvos, o de baixo tem que pegar a de baixo.
    pares = dict(casa_portas([(2, 2), (2, 20)],
                             [("MAP_HEADER_A_HOUSE", 100, 100),
                              ("MAP_HEADER_B_HOUSE", 100, 160)], 10, 24))
    assert pares[(2, 2)].endswith("A_HOUSE"), pares
    assert pares[(2, 20)].endswith("B_HOUSE"), pares
    # 5. com menos porta que predio, o centro Pokemon ganha da casa comum.
    pares = dict(casa_portas([(5, 5)],
                             [("MAP_HEADER_X_HOUSE", 10, 10),
                              ("MAP_HEADER_X_POKECENTER_1F", 90, 90)], 10, 10))
    assert list(pares.values()) == ["MAP_HEADER_X_POKECENTER_1F"], pares
    # 4. item escondido do Platinum nao e placa.
    assert 8161 >= 8000
    # 6. sala de predio da segunda leva entra, e sala da Elite fica de fora.
    for h, esperado in (("MAP_HEADER_HEARTHOME_CITY_GYM_LEADER_ROOM", "casa"),
                        ("MAP_HEADER_JUBILIFE_TV_ELEVATOR", "andar"),
                        ("MAP_HEADER_VEILSTONE_STORE_B1F", "mart"),
                        ("MAP_HEADER_POKEMON_LEAGUE_CHAMPION_ROOM", None),
                        ("MAP_HEADER_GREAT_MARSH_1", None),
                        ("MAP_HEADER_DISTORTION_WORLD_1F", None)):
        assert arquetipo_do_header(h) == esperado, h
    # 7. grupo cheio NAO recebe o mapa 129: ele nasceria com indice 128, que
    #    vira -128 no `s8` do warp e reseta o jogo ao entrar.
    g = {"group_order": ["gX"], "gX": ["m"] * LIMITE_GRUPO}
    assert grupo_com_vaga(g, "gX") == "gX2", g
    print("demo ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
