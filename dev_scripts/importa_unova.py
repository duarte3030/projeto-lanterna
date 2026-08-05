#!/usr/bin/env python3
"""Traz a regiao de Unova do BW3G (projeto pokecrystal) para dentro deste hack.

Uso:
    python3 dev_scripts/importa_unova.py --conferir   # so mede e relata, nao grava
    python3 dev_scripts/importa_unova.py --gravar     # gera mapas e registra

Fonte: github.com/AzureKeys/BW3G, "Black and White 3: Genesis", de Azure_Keys,
clonado em /tmp/bw3g-probe. E um projeto pokecrystal, entao o formato e o mesmo
que `dev_scripts/demake_gen2.py` ja converte; a unica diferenca e a extensao dos
blocos (`.ablk` em vez de `.blk`), byte por bloco igual.

Tres armadilhas medidas em 05/08/2026, e como este script escapa de cada uma:

1. **Nome CamelCase NAO vira a constante do mapa.** `GiantChasm1F` teria que
   virar `GIANT_CHASM_1F`, mas separar minuscula de maiuscula da
   `GIANT_CHASM1F`. A ligacao certa e POSICIONAL: o n-esimo `map` dentro de
   `MapGroup_X` em `data/maps/maps.asm` corresponde ao n-esimo `map_const`
   depois do n-esimo `newgroup` em `constants/map_constants.asm`. Conferido:
   198 dos 200 mapas com blocos proprios batem `len(.ablk) == w*h` por esse
   pareamento, contra 3 pelo pareamento por nome.

2. **91 mapas nao tem `.ablk` proprio, eles COMPARTILHAM.** Todo Pokecenter usa
   o mesmo bloco, toda casa idem. Quem resolve isso e `data/maps/blocks.asm`,
   onde varios rotulos `X_Blocks:` seguidos apontam para um unico `INCBIN`.

3. **`newgroup` aparece tambem na definicao do MACRO**, na primeira linha do
   arquivo. Casar `\\s*newgroup` inventa um grupo vazio e desloca TODOS os
   grupos em um, o que faz cada mapa herdar as dimensoes do vizinho. Por isso a
   regex exige fim de linha.

Compatibilidade de save (requisito do dono, 05/08/2026): a save guarda a posicao
como par de indices (mapGroup, mapNum). Este script SO ACRESCENTA, nunca
reordena: grupos novos vao para o FIM de `group_order`, mapas novos para o fim
do grupo novo, MAPSEC nova para o fim de `region_map_sections.json`. As unicas
flags que ele gasta saem da faixa que o dono reservou para itens de Unova em
05/08/2026 (`FLAG_ITEMS_UNOVA_START`, 467 delas), nunca do pool `FLAG_UNUSED_*`.
"""
import json
import os
import re
import shutil
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))

import demake_gen2 as dg  # noqa: E402

BW3G = "/tmp/bw3g-probe"
dg.FONTE = BW3G
dg.EXT = ".ablk"

PREFIXO = "Unova_"          # nome do mapa e da pasta
PREFIXO_ID = "MAP_UNOVA_"   # constante do mapa
PREFIXO_LAYOUT = "LAYOUT_UNOVA_"

# NPC, placa e warp nao gastam flag: o campo `flag` do object_event fica "0", o
# que quer dizer "sempre visivel". Quem gasta flag e so item (bola e escondido),
# e por obrigacao: sem flag propria o item renasce a cada entrada no mapa.
SEM_FLAG = "0"

# Faixa de flag reservada para os itens de Unova pelo dono do projeto em
# 05/08/2026: FLAG_ITEMS_UNOVA_START + 0x000 ate + 0x1D2, 467 flags, ja dentro de
# FLAGS_COUNT. Cada bola de item e cada item escondido PRECISA de uma flag
# propria, senao renasce a cada entrada no mapa e vira duplicador infinito.
# Nao usar FLAG_UNUSED_* para isto: o dono pediu explicitamente a faixa nova.
NUM_ITEMS_UNOVA = 0x1D3


def flag_de_item(contador):
    """Consome a proxima flag da faixa reservada. `contador` e uma lista de 1."""
    i = contador[0]
    contador[0] += 1
    return f"FLAG_ITEMS_UNOVA_START + 0x{i:03X}"

# Landmark do BW3G -> qual das tres MAPSEC de Unova. MAPSEC e u8 e esta com 212
# de 255 em uso, por isso a regiao inteira cabe em tres, com apelido por cidade
# (ver src/data/region_map/region_map_sections.constants.json.txt).
REGIAO = {
    "WEST": ["ASPERTIA_CITY", "FLOCCESY_TOWN", "FLOCCESY_RANCH", "VIRBANK_CITY",
             "VIRBANK_COMPLEX", "CASTELIA_CITY", "CASTELIA_SEWERS", "NACRENE_CITY",
             "STRIATON_CITY", "ACCUMULA_TOWN", "NUVEMA_TOWN", "DREAMYARD",
             "PINWHEEL_FOREST", "SKYARROW_BRIDGE", "R_1", "R_2", "R_3", "R_19",
             "R_20", "P2_LABORATORY", "LIBERTY_GARDEN", "WELLSPRING_CAVE",
             "R_17", "R_18", "WHITE_FOREST", "BLACK_CITY"],
    "NORTH": ["DRIFTVEIL_CITY", "MISTRALTON_CITY", "MISTRALTON_CAVE", "CHARGESTONE_CAVE",
              "TWIST_MOUNTAIN", "ICIRRUS_CITY", "MOOR_OF_ICIRRUS", "DRAGONSPIRAL_TOWER",
              "OPELUCID_CITY", "R_6", "R_7", "R_8", "R_9", "R_11", "R_23",
              "VICTORY_ROAD", "PKMN_LEAGUE", "COLD_STORAGE", "PWT"],
    "EAST": ["NIMBASA_CITY", "NIMBASA_PARK", "ANVILLE_TOWN", "LOSTLORN_FOREST",
             "DESERT_RESORT", "RELIC_CASTLE", "R_4", "R_5", "R_12", "R_13", "R_14",
             "R_15", "R_16", "R_21", "R_22", "UNDELLA_TOWN", "UNDELLA_BAY",
             "LACUNOSA_TOWN", "LENTIMAS_TOWN", "LENTIMAS_OUTSKIRTS", "HUMILAU_CITY",
             "GIANT_CHASM", "REVERSAL_MOUNTAIN", "STRANGE_HOUSE", "SEASIDE_CAVE",
             "MARINE_TUBE", "VILLAGE_BRIDGE", "ABUNDANT_SHRINE"],
}

AMBIENTE = {
    "TOWN": ("MAP_TYPE_TOWN", True), "ROUTE": ("MAP_TYPE_ROUTE", True),
    "INDOOR": ("MAP_TYPE_INDOOR", False), "CAVE": ("MAP_TYPE_UNDERGROUND", False),
    "GATE": ("MAP_TYPE_INDOOR", False), "DUNGEON": ("MAP_TYPE_UNDERGROUND", False),
    "ENVIRONMENT_5": ("MAP_TYPE_INDOOR", False),
}
LADO = {"north": "up", "south": "down", "west": "left", "east": "right"}

# Unico tileset do BW3G citado em maps.asm sem `_collision.asm` proprio (medido:
# 46 dos 47 tem). Cai no irmao, que e a mesma sala com outra paleta.
COLISAO_ALIAS = {"elite_four_room_2": "elite_four_room"}

# --------------------------------------------------------------------------
# Leitura do BW3G


def le_grupos():
    """[(nome_do_grupo, [(camel, const, w, h, tileset, ambiente, landmark, musica)])]

    O pareamento e POSICIONAL, ver o cabecalho deste arquivo.
    """
    mc = open(f"{BW3G}/constants/map_constants.asm").read()
    consts, atual = [], None
    for ln in mc.splitlines():
        if re.match(r"^\s*newgroup\s*(;.*)?$", ln):   # o `$` evita casar `newgroup: MACRO`
            atual = []
            consts.append(atual)
        m = re.match(r"\s*map_const\s+(\w+),\s*(\d+),\s*(\d+)", ln)
        if m and atual is not None:
            atual.append((m.group(1), int(m.group(2)), int(m.group(3))))

    ma = open(f"{BW3G}/data/maps/maps.asm").read()
    ordem = re.findall(r"^\tdw (MapGroup_\w+)", ma, re.M)
    porgrupo, cur = {}, None
    for ln in ma.splitlines():
        m = re.match(r"^(MapGroup_\w+):", ln)
        if m:
            cur = m.group(1)
            porgrupo[cur] = []
        m = re.match(r"\s*map\s+(\w+),\s*TILESET_(\w+),\s*(\w+),\s*(\w+),\s*(\w+)", ln)
        if m and cur:
            porgrupo[cur].append(m.groups())

    saida = []
    for i, g in enumerate(ordem):
        mapas = []
        for (const, w, h), mm in zip(consts[i], porgrupo[g]):
            mapas.append((mm[0], const, w, h, mm[1].lower(), mm[2], mm[3], mm[4]))
        saida.append((g, mapas))
    return saida


def le_blocos_compartilhados():
    """rotulo do mapa -> caminho do .ablk (varios mapas dividem o mesmo arquivo)."""
    saida, pendentes = {}, []
    for ln in open(f"{BW3G}/data/maps/blocks.asm"):
        m = re.match(r"^(\w+)_Blocks:", ln)
        if m:
            pendentes.append(m.group(1))
            continue
        m = re.match(r'\s*INCBIN\s+"([^"]+)"', ln)
        if m:
            for p in pendentes:
                saida[p] = os.path.join(BW3G, m.group(1))
            pendentes = []
    return saida


def le_conexoes():
    """mapa camel -> [(direcao, const_destino, offset_em_blocos)]."""
    saida, atual = {}, None
    for ln in open(f"{BW3G}/data/maps/attributes.asm"):
        m = re.match(r"\s*map_attributes\s+(\w+),\s*(\w+),\s*(\$?\w+),", ln)
        if m:
            atual = m.group(1)
            saida[atual] = {"borda": int(m.group(3).lstrip("$"), 16), "con": []}
            continue
        m = re.match(r"\s*connection\s+(\w+),\s*(\w+),\s*(\w+),\s*(-?\d+)", ln)
        if m and atual:
            saida[atual]["con"].append((m.group(1), m.group(3), int(m.group(4))))
    return saida


# --------------------------------------------------------------------------
# Texto: macros de gen 2 -> .string de gen 3

TROCA = [("<PLAY_G>", "{PLAYER}"), ("<PLAYER>", "{PLAYER}"), ("<PKMN>", "POKéMON"),
         ("<RIVAL>", "RIVAL"), ("#", "POKé"), ("<TARGET>", "o POKéMON"),
         ("<USER>", "o POKéMON"), ("<MOM>", "MAMÃE"), ("@", "")]
JUNTA = {"text": "", "line": r"\n", "next": r"\n", "cont": r"\l", "para": r"\p"}


def limpa(s):
    for a, b in TROCA:
        s = s.replace(a, b)
    return s.replace('"', "'").replace("\\", "/")


def le_textos(asm):
    """rotulo -> lista de linhas ja em formato .string, sem o terminador."""
    saida = {}
    rotulo, partes = None, None
    for ln in asm.splitlines():
        m = re.match(r"^(\w+):+\s*$", ln)
        if m:
            if rotulo and partes:
                saida[rotulo] = partes
            rotulo, partes = m.group(1), None
            continue
        m = re.match(r'^\t(text|line|next|cont|para)\s+"([^"]*)"', ln)
        if m:
            if partes is None:
                if m.group(1) != "text":      # bloco que nao comeca com `text` nao e texto
                    rotulo = None
                    continue
                partes = []
            partes.append(JUNTA[m.group(1)] + limpa(m.group(2)))
            continue
        if re.match(r"^\t(done|prompt|text_end)\s*$", ln):
            if rotulo and partes:
                saida[rotulo] = partes
            rotulo, partes = None, None
            continue
        if partes is not None and re.match(r"^\t\w", ln):
            # macro que nao sabemos traduzir (text_ram, text_decimal, sound_*):
            # o texto para aqui, o que ja veio continua valendo
            saida[rotulo] = partes
            rotulo, partes = None, None
    if rotulo and partes:
        saida[rotulo] = partes
    return saida


def emite_texto(rotulo, partes):
    linhas = [f"{rotulo}::"]
    for i, p in enumerate(partes):
        fim = "$" if i == len(partes) - 1 else ""
        linhas.append(f'\t.string "{p}{fim}"')
    return "\n".join(linhas) + "\n"


# --------------------------------------------------------------------------
# Eventos

RE_EVENTOS = re.compile(r"^(\w+)_MapEvents:", re.M)


def indice_asm():
    """rotulo do mapa -> caminho do .asm que tem o `<rotulo>_MapEvents`.

    O nome do ARQUIVO nao e o nome do mapa. `Rt5NimbasaGate` (em maps.asm) mora
    em `maps/R5NimbasaGate.asm`, e sao 36 casos assim. Achar pelo nome do arquivo
    deixava esses mapas com zero warp, e o validador acusava 86 warps quebrados
    apontando para eles. O indice e por ROTULO, que e o que o pokecrystal usa.
    """
    saida = {}
    for f in sorted(os.listdir(f"{BW3G}/maps")):
        if not f.endswith(".asm"):
            continue
        p = f"{BW3G}/maps/{f}"
        for m in RE_EVENTOS.finditer(open(p, encoding="utf-8", errors="replace").read()):
            saida[m.group(1)] = p
    return saida


def le_eventos(asm, rotulo=None):
    """Le o bloco `<Mapa>_MapEvents:` ate o fim do arquivo."""
    m = (re.search(rf"^{rotulo}_MapEvents:", asm, re.M) if rotulo else None) \
        or RE_EVENTOS.search(asm)
    if not m:
        return {"warp": [], "coord": [], "bg": [], "obj": []}
    corpo = asm[m.end():]
    ev = {"warp": [], "coord": [], "bg": [], "obj": []}
    for ln in corpo.splitlines():
        m = re.match(r"\s*warp_event\s+(-?\d+),\s*(-?\d+),\s*(\w+),\s*(\d+)", ln)
        if m:
            ev["warp"].append((int(m.group(1)), int(m.group(2)), m.group(3), int(m.group(4))))
            continue
        m = re.match(r"\s*coord_event\s+(-?\d+),\s*(-?\d+),\s*(\w+),\s*(\w+)", ln)
        if m:
            ev["coord"].append(m.groups())
            continue
        m = re.match(r"\s*bg_event\s+(-?\d+),\s*(-?\d+),\s*BGEVENT_(\w+),\s*(\w+)", ln)
        if m:
            ev["bg"].append((int(m.group(1)), int(m.group(2)), m.group(3), m.group(4)))
            continue
        m = re.match(r"\s*object_event\s+(-?\d+),\s*(-?\d+),\s*(\w+),\s*(\w+),\s*(-?\d+),"
                     r"\s*(-?\d+),\s*(-?\w+),\s*(-?\w+),\s*(\w+),\s*OBJECTTYPE_(\w*),"
                     r"\s*(-?\w+),\s*(\w+)", ln)
        if m:
            ev["obj"].append(dict(x=int(m.group(1)), y=int(m.group(2)), sprite=m.group(3),
                                  mov=m.group(4), rx=int(m.group(5)), ry=int(m.group(6)),
                                  tipo=m.group(10), script=m.group(12)))
    return ev


# Item do gen 2 -> item deste build. A regra e "ITEM_" + o nome; a tabela abaixo
# so lista as excecoes, conferidas contra include/constants/items.h e
# src/data/items.h (os TM moram no segundo, gerados por macro, e nao aparecem no
# primeiro: grep so no header de constantes da falso negativo).
#
# Este build tem apenas os 50 TM de Hoenn. Os 11 TM de gen 4 e 5 que o BW3G usa
# nao existem aqui e viram o TM mais proximo em tipo e papel; a troca esta na
# coluna de comentario para quem quiser refinar depois.
ITEM_TROCA = {
    "PARLYZ_HEAL": "ITEM_PARALYZE_HEAL", "ELIXER": "ITEM_ELIXIR",
    "MAX_ELIXER": "ITEM_MAX_ELIXIR", "NEVERMELTICE": "ITEM_NEVER_MELT_ICE",
    "BLACKGLASSES": "ITEM_BLACK_GLASSES", "TWISTEDSPOON": "ITEM_TWISTED_SPOON",
    "SILVERPOWDER": "ITEM_SILVER_POWDER", "TINYMUSHROOM": "ITEM_TINY_MUSHROOM",
    "BRIGHTPOWDER": "ITEM_BRIGHT_POWDER", "BLACKBELT": "ITEM_BLACK_BELT",
    "S_S_TICKET": "ITEM_SS_TICKET",
    "TM_SOLARBEAM": "ITEM_TM_SOLAR_BEAM", "TM_PSYCHIC_M": "ITEM_TM_PSYCHIC",
    "SHELL_STONE": "ITEM_WATER_STONE",          # pedra de evolucao propria do BW3G
    "TM_DAZZLINGLEAM": "ITEM_TM_PSYCHIC",       # nao ha TM de Fada neste build
    "TM_DREAM_EATER": "ITEM_TM_PSYCHIC",
    "TM_FLASH_CANNON": "ITEM_TM_STEEL_WING",
    "TM_FOCUS_BLAST": "ITEM_TM_BRICK_BREAK",
    "TM_ROCK_SLIDE": "ITEM_TM_ROCK_TOMB",
    "TM_STONE_EDGE": "ITEM_TM_ROCK_TOMB",
    "TM_SHADOW_CLAW": "ITEM_TM_SHADOW_BALL",
    "TM_SWORDS_DANCE": "ITEM_TM_BULK_UP",
    "TM_WILD_CHARGE": "ITEM_TM_THUNDERBOLT",
    "TM_WILL_O_WISP": "ITEM_TM_FLAMETHROWER",
    "TM_X_SCISSOR": "ITEM_TM_AERIAL_ACE",       # nao ha TM de Inseto neste build
}


def _itens_do_build():
    """Todo ITEM_* que existe nesta build.

    Le os DOIS arquivos de proposito: os TM sao gerados por macro e so aparecem
    em src/data/items.h, e ITEM_X_DEFEND / ITEM_X_SPECIAL so existem como apelido
    de gen 5 em include/constants/items.h. Conferir num arquivo so da falso
    negativo, e o erro sai la no `ld` como "undefined reference", com o mapa
    inteiro ja gerado. Aconteceu com ITEM_X_SPECIAL_ATTACK, que eu inventei.
    """
    tem = set()
    for f in ("include/constants/items.h", "src/data/items.h"):
        tem |= set(re.findall(r"\b(ITEM_[A-Z0-9_]+)\b", open(f"{RAIZ}/{f}").read()))
    return tem


ITENS_DO_BUILD = _itens_do_build()


def item_gen3(nome):
    i = ITEM_TROCA.get(nome, "ITEM_" + nome)
    if i not in ITENS_DO_BUILD:
        raise SystemExit(f"item {nome} virou {i}, que nao existe nesta build; "
                         f"acrescente em ITEM_TROCA")
    return i


def item_do_script(asm, rotulo):
    """(item, quantidade, escondido) do rotulo apontado por um OBJECTTYPE_ITEMBALL
    ou por um bg_event BGEVENT_ITEM. None se o rotulo nao for de item."""
    m = re.search(rf"^{rotulo}:+\s*$", asm, re.M)
    if not m:
        return None
    for ln in asm[m.end():].splitlines()[:6]:
        if re.match(r"^\w+:", ln):
            break
        m2 = re.match(r"\s*itemball\s+(\w+)(?:,\s*(\d+))?", ln)
        if m2:
            return item_gen3(m2.group(1)), int(m2.group(2) or 1), False
        m2 = re.match(r"\s*hiddenitem\s+(\w+)", ln)
        if m2:
            return item_gen3(m2.group(1)), 1, True
    return None



# `jumpstd` do gen 2 que NAO e dialogo, e sim mobilia com comportamento proprio.
# Sao 66 objetos que sem isto ficariam mudos: 48 estantes, 18 pedras de Strength.
# A pedra e a que importa, porque e obstaculo de verdade: convertida como NPC
# mudo ela vira parede permanente e tranca a caverna.
STD_MOBILIA = {
    "magazinebookshelf": ("OBJ_EVENT_GFX_ITEM_BALL", "EventScript_BookShelf"),
    "difficultbookshelf": ("OBJ_EVENT_GFX_ITEM_BALL", "EventScript_BookShelf"),
    "picturebookshelf": ("OBJ_EVENT_GFX_ITEM_BALL", "EventScript_PictureBookShelf"),
    "strengthboulder": ("OBJ_EVENT_GFX_PUSHABLE_BOULDER", "EventScript_StrengthBoulder"),
}

# As estantes do BW3G sao bg_event, nao objeto, e por isso escapavam da tabela
# acima e eram DESCARTADAS por nao terem texto proprio. Sao 81 placas. O texto
# generico ja existe no repo (data/scripts/check_furniture.inc), entao nao ha
# nada para escrever.
# Ficam de fora de proposito: `gymstatue1/2` (o texto do gen 2 e montado em
# tempo de execucao com o nome do lider e a contagem de vitorias, e inventar um
# no lugar seria escrever conteudo, o que o dono vetou), e `apartmentstairs` e
# `elevatorbutton`, que sao comportamento e nao texto.
STD_PLACA = {
    "magazinebookshelf": "EventScript_BookShelf",
    "difficultbookshelf": "EventScript_BookShelf",
    "picturebookshelf": "EventScript_PictureBookShelf",
}

# Os treze chefes: 8 lideres de ginasio, o Elite dos Quatro e o campeao. No gen 2
# eles nao sao OBJECTTYPE_TRAINER; sao OBJECTTYPE_SCRIPT com um `loadtrainer` no
# meio, e por isso caiam aqui como NPC mudo de um texto so. A chave e o rotulo do
# script do BW3G, ou o SPRITE_ quando o objeto nao tem script (o campeao Genesis
# e cutscene: o objeto dele aponta para o script 0 e a batalha mora no MapScripts).
# Os textos sao os do proprio BW3G: `visto` e o que ele fala antes da batalha,
# `perde` e o `winlosstext`.
#
# O quinto campo, so nos 8 lideres de ginasio, e a insignia que o script acende
# depois da vitoria (ver FLAG_BADGE_UNOVA_* em include/constants/flags.h). A
# Elite dos Quatro nao entrega nada, entao la o campo nao existe. Nao ha texto
# de entrega: o BW3G nao escreve nenhum, e inventar um seria escrever conteudo.
LIDERES = {
    ("HumilauGym", "HumilauGymMarlonScript"):
        ("TRAINER_UNOVA_LEADER_MARLON", "MarlonGymIntroText", "MarlonWinLossText", 4,
         "FLAG_BADGE_UNOVA_HUMILAU"),
    ("LentimasGym", "LentimasGymShauntalScript"):
        ("TRAINER_UNOVA_LEADER_SHAUNTAL", "ShauntalGymIntroText2", "ShauntalWinLossText", 4,
         "FLAG_BADGE_UNOVA_LENTIMAS"),
    ("CasteliaGym", "CasteliaGymBurghScript"):
        ("TRAINER_UNOVA_LEADER_BURGH", "BurghGymIntroText", "BurghWinLossText", 4,
         "FLAG_BADGE_UNOVA_CASTELIA"),
    ("VirbankGym", "VirbankGymRoxieScript"):
        ("TRAINER_UNOVA_LEADER_ROXIE", "RoxieGymIntroText", "RoxieWinLossText", 4,
         "FLAG_BADGE_UNOVA_VIRBANK"),
    ("AspertiaGym", "AspertiaGymCherenScript"):
        ("TRAINER_UNOVA_LEADER_CHEREN", "CherenGymIntroText", "CherenWinLossText", 4,
         "FLAG_BADGE_UNOVA_ASPERTIA"),
    ("StriatonGym", "StriatonGymCilanScript"):
        ("TRAINER_UNOVA_LEADER_CILAN", "CilanGymIntroText", "CilanWinLossText", 4,
         "FLAG_BADGE_UNOVA_STRIATON"),
    ("MistraltonGym1F", "MistraltonGymSkylaScript"):
        ("TRAINER_UNOVA_LEADER_SKYLA", "SkylaGymIntroText", "SkylaWinLossText", 4,
         "FLAG_BADGE_UNOVA_MISTRALTON"),
    ("OpelucidGym", "OpelucidGymDraydenScript"):
        ("TRAINER_UNOVA_LEADER_DRAYDEN", "DraydenGymIntroText", "DraydenWinLossText", 4,
         "FLAG_BADGE_UNOVA_OPELUCID"),
    ("GrimsleysRoom", "EliteFourGrimsleyScript"):
        ("TRAINER_UNOVA_E4_GRIMSLEY", "EliteFourGrimsleyIntroText", "EliteFourGrimsleyWinText", 3),
    ("MarshalsRoom", "EliteFourMarshalScript"):
        ("TRAINER_UNOVA_E4_MARSHAL", "EliteFourMarshalIntroText", "EliteFourMarshalWinText", 3),
    ("ElesasRoom", "EliteFourElesaScript"):
        ("TRAINER_UNOVA_E4_ELESA", "EliteFourElesaIntroText", "EliteFourElesaWinText", 3),
    ("ColresssRoom", "EliteFourColressScript"):
        ("TRAINER_UNOVA_E4_COLRESS", "EliteFourColressIntroText", "EliteFourColressWinText", 3),
    # O campeao Genesis NAO entra aqui, apesar de TRAINER_UNOVA_CHAMPION_GENESIS
    # e o time dele existirem. A sala dele e cutscene: sete objetos empilhados em
    # tres casas, e o de Genesis divide a casa (7,10) com o da Juniper, que vem
    # ANTES na lista. Quem fala com a casa fala com a Juniper (muda), e o Genesis
    # ainda olha para cima, de costas para quem sobe da entrada, entao o raio de
    # visao tambem nunca dispara. Ligar isso exige mexer na geometria da sala, que
    # e conteudo novo e nao porte. A vaga 1379 fica pronta para quem fizer a
    # cutscene da Liga.
}


# >>> TREINADORES DE UNOVA (gerado) >>>
# Treinadores de rota, caverna e predio: mesmo molde da LIDERES acima, so
# que gerado por dev_scripts/gera_treinadores_unova.py a partir do macro
# `trainer CLASSE, ID, EVENTO, VistoText, VenceText, ...` do BW3G. A chave e
# (mapa, rotulo do script do objeto OBJECTTYPE_TRAINER); dois objetos podem
# apontar para o mesmo treinador (as gemeas), e ai dividem o id de proposito.
# O ultimo campo e o raio de visao lido do proprio object_event.
TREINADORES = {
    ("CasteliaGym", "TrainerHarlequinCasteliaGym1"):
        ("TRAINER_UNOVA_HARLEQUIN_CASTELIA_GYM_1", "HarlequinCasteliaGym1SeenText", "HarlequinCasteliaGym1BeatenText", 2),
    ("CasteliaGym", "TrainerHarlequinCasteliaGym2"):
        ("TRAINER_UNOVA_HARLEQUIN_CASTELIA_GYM_2", "HarlequinCasteliaGym2SeenText", "HarlequinCasteliaGym2BeatenText", 2),
    ("CasteliaGym", "TrainerHarlequinCasteliaGym3"):
        ("TRAINER_UNOVA_HARLEQUIN_CASTELIA_GYM_3", "HarlequinCasteliaGym3SeenText", "HarlequinCasteliaGym3BeatenText", 1),
    ("CasteliaGym", "TrainerHarlequinCasteliaGym4"):
        ("TRAINER_UNOVA_HARLEQUIN_CASTELIA_GYM_4", "HarlequinCasteliaGym4SeenText", "HarlequinCasteliaGym4BeatenText", 2),
    ("CasteliaGym", "TrainerHarlequinCasteliaGym5"):
        ("TRAINER_UNOVA_HARLEQUIN_CASTELIA_GYM_5", "HarlequinCasteliaGym5SeenText", "HarlequinCasteliaGym5BeatenText", 2),
    ("CasteliaSewers", "TrainerJanitor1CasteliaSewers"):
        ("TRAINER_UNOVA_JANITOR_CASTELIA_SEWERS_1", "Janitor1CasteliaSewersSeenText", "Janitor1CasteliaSewersBeatenText", 2),
    ("CasteliaSewers", "TrainerJanitor2CasteliaSewers"):
        ("TRAINER_UNOVA_JANITOR_CASTELIA_SEWERS_2", "Janitor2CasteliaSewersSeenText", "Janitor2CasteliaSewersBeatenText", 3),
    ("CasteliaSewers", "TrainerJanitor3CasteliaSewers"):
        ("TRAINER_UNOVA_JANITOR_CASTELIA_SEWERS_4", "Janitor3CasteliaSewersSeenText", "Janitor3CasteliaSewersBeatenText", 2),
    ("CasteliaSewers", "TrainerScientistFCasteliaSewers"):
        ("TRAINER_UNOVA_SCIENTISTF_CASTELIA_SEWERS", "ScientistFCasteliaSewersSeenText", "ScientistFCasteliaSewersBeatenText", 1),
    ("CasteliaSewers", "TrainerScientistMCasteliaSewers"):
        ("TRAINER_UNOVA_SCIENTISTM_CASTELIA_SEWERS", "ScientistMCasteliaSewersSeenText", "ScientistMCasteliaSewersBeatenText", 2),
    ("CasteliaSewers", "TrainerWorker1CasteliaSewers"):
        ("TRAINER_UNOVA_WORKER_CASTELIA_SEWERS_1", "Worker1CasteliaSewersSeenText", "Worker1CasteliaSewersBeatenText", 3),
    ("CasteliaSewers", "TrainerWorker2CasteliaSewers"):
        ("TRAINER_UNOVA_WORKER_CASTELIA_SEWERS_2", "Worker2CasteliaSewersSeenText", "Worker2CasteliaSewersBeatenText", 3),
    ("CasteliaSewersRooms", "TrainerJanitorCasteliaSewersRooms"):
        ("TRAINER_UNOVA_JANITOR_CASTELIA_SEWERS_3", "JanitorCasteliaSewersRoomsSeenText", "JanitorCasteliaSewersRoomsBeatenText", 2),
    ("CasteliaSewersRooms", "TrainerWorkerCasteliaSewersRooms"):
        ("TRAINER_UNOVA_WORKER_CASTELIA_SEWERS_3", "WorkerCasteliaSewersRoomsSeenText", "WorkerCasteliaSewersRoomsBeatenText", 3),
    ("CelestialTower", "TrainerGentlemanCelestialTower"):
        ("TRAINER_UNOVA_GENTLEMAN_CELESTIAL_TOWER", "GentlemanCelestialTowerSeenText", "GentlemanCelestialTowerBeatenText", 2),
    ("CelestialTower", "TrainerHexManiac1CelestialTower"):
        ("TRAINER_UNOVA_HEX_MANIAC_CELESTIAL_TOWER_1", "HexManiac1CelestialTowerSeenText", "HexManiac1CelestialTowerBeatenText", 2),
    ("CelestialTower", "TrainerHexManiac2CelestialTower"):
        ("TRAINER_UNOVA_HEX_MANIAC_CELESTIAL_TOWER_2", "HexManiac2CelestialTowerSeenText", "HexManiac2CelestialTowerBeatenText", 3),
    ("CelestialTower", "TrainerLassCelestialTower"):
        ("TRAINER_UNOVA_LASS_CELESTIAL_TOWER", "LassCelestialTowerSeenText", "LassCelestialTowerBeatenText", 1),
    ("CelestialTower", "TrainerMaidCelestialTower"):
        ("TRAINER_UNOVA_MAID_CELESTIAL_TOWER", "MaidCelestialTowerSeenText", "MaidCelestialTowerBeatenText", 2),
    ("CelestialTower", "TrainerPokefanFCelestialTower"):
        ("TRAINER_UNOVA_POKEFANF_CELESTIAL_TOWER", "PokefanFCelestialTowerSeenText", "PokefanFCelestialTowerBeatenText", 2),
    ("CelestialTower", "TrainerPokefanMCelestialTower"):
        ("TRAINER_UNOVA_POKEFANM_CELESTIAL_TOWER", "PokefanMCelestialTowerSeenText", "PokefanMCelestialTowerBeatenText", 2),
    ("CelestialTower", "TrainerPsychicFCelestialTower"):
        ("TRAINER_UNOVA_PSYCHICF_CELESTIAL_TOWER", "PsychicFCelestialTowerSeenText", "PsychicFCelestialTowerBeatenText", 1),
    ("CelestialTower", "TrainerPsychicMCelestialTower"):
        ("TRAINER_UNOVA_PSYCHICM_CELESTIAL_TOWER", "PsychicMCelestialTowerSeenText", "PsychicMCelestialTowerBeatenText", 2),
    ("CelestialTower", "TrainerSocialiteCelestialTower"):
        ("TRAINER_UNOVA_SOCIALITE_CELESTIAL_TOWER", "SocialiteCelestialTowerSeenText", "SocialiteCelestialTowerBeatenText", 2),
    ("CelestialTower1F", "TrainerNurseCelestialTower"):
        ("TRAINER_UNOVA_NURSE_CELESTIAL_TOWER", "CelestialTowerNurseIntroText", "CelestialTowerNurseWinText", 0),
    ("ChargestoneCave1F", "TrainerAceTrainerF1Chargestone"):
        ("TRAINER_UNOVA_ACE_TRAINERF_CHARGESTONE_1", "AceTrainerF1ChargestoneSeenText", "AceTrainerF1ChargestoneBeatenText", 2),
    ("ChargestoneCave1F", "TrainerAceTrainerM1Chargestone"):
        ("TRAINER_UNOVA_ACE_TRAINERM_CHARGESTONE_1", "AceTrainerM1ChargestoneSeenText", "AceTrainerM1ChargestoneBeatenText", 2),
    ("ChargestoneCave1F", "TrainerGuitarist1Chargestone"):
        ("TRAINER_UNOVA_GUITARIST_CHARGESTONE_1", "Guitarist1ChargestoneSeenText", "Guitarist1ChargestoneBeatenText", 1),
    ("ChargestoneCave1F", "TrainerHiker1Chargestone"):
        ("TRAINER_UNOVA_HIKER_CHARGESTONE_1", "Hiker1ChargestoneSeenText", "Hiker1ChargestoneBeatenText", 1),
    ("ChargestoneCave1F", "TrainerPkmnRangerFChargestone"):
        ("TRAINER_UNOVA_PKMN_RANGERF_CHARGESTONE", "PkmnRangerFChargestoneSeenText", "PkmnRangerFChargestoneBeatenText", 1),
    ("ChargestoneCave1F", "TrainerScientistMChargestone"):
        ("TRAINER_UNOVA_SCIENTISTM_CHARGESTONE", "ScientistMChargestoneSeenText", "ScientistMChargestoneBeatenText", 2),
    ("ChargestoneCaveB1F", "TrainerAceTrainerF2Chargestone"):
        ("TRAINER_UNOVA_ACE_TRAINERF_CHARGESTONE_2", "AceTrainerF2ChargestoneSeenText", "AceTrainerF2ChargestoneBeatenText", 3),
    ("ChargestoneCaveB1F", "TrainerBattleGirlChargestone"):
        ("TRAINER_UNOVA_BATTLE_GIRL_CHARGESTONE", "BattleGirlChargestoneSeenText", "BattleGirlChargestoneBeatenText", 2),
    ("ChargestoneCaveB1F", "TrainerDoctorChargestone"):
        ("TRAINER_UNOVA_DOCTOR_CHARGESTONE", "ChargestoneDoctorIntroText", "ChargestoneDoctorWinText", 0),
    ("ChargestoneCaveB1F", "TrainerHiker2Chargestone"):
        ("TRAINER_UNOVA_HIKER_CHARGESTONE_2", "Hiker2ChargestoneSeenText", "Hiker2ChargestoneBeatenText", 2),
    ("ChargestoneCaveB1F", "TrainerPkmnRangerMChargestone"):
        ("TRAINER_UNOVA_PKMN_RANGERM_CHARGESTONE", "PkmnRangerMChargestoneSeenText", "PkmnRangerMChargestoneBeatenText", 2),
    ("ChargestoneCaveB1F", "TrainerScientistFChargestone"):
        ("TRAINER_UNOVA_SCIENTISTF_CHARGESTONE", "ScientistFChargestoneSeenText", "ScientistFChargestoneBeatenText", 2),
    ("ChargestoneCaveB2F", "TrainerAceTrainerM2Chargestone"):
        ("TRAINER_UNOVA_ACE_TRAINERM_CHARGESTONE_2", "AceTrainerM2ChargestoneSeenText", "AceTrainerM2ChargestoneBeatenText", 1),
    ("ChargestoneCaveB2F", "TrainerGuitarist2Chargestone"):
        ("TRAINER_UNOVA_GUITARIST_CHARGESTONE_2", "Guitarist2ChargestoneSeenText", "Guitarist2ChargestoneBeatenText", 2),
    ("ChargestoneCaveB2F", "TrainerHiker3Chargestone"):
        ("TRAINER_UNOVA_HIKER_CHARGESTONE_3", "Hiker3ChargestoneSeenText", "Hiker3ChargestoneBeatenText", 2),
    ("DesertResort", "DesertNurseScript"):
        ("TRAINER_UNOVA_NURSE_DESERT", "DesertNurseIntroText", "DesertNurseWinText", 0),
    ("DesertResort", "TrainerBackpackerFDesert"):
        ("TRAINER_UNOVA_BACKPACKERF_DESERT", "BackpackerFDesertSeenText", "BackpackerFDesertBeatenText", 3),
    ("DesertResort", "TrainerBackpackerMDesert"):
        ("TRAINER_UNOVA_BACKPACKERM_DESERT", "BackpackerMDesertSeenText", "BackpackerMDesertBeatenText", 2),
    ("DesertResort", "TrainerHexManiacDesert"):
        ("TRAINER_UNOVA_HEX_MANIAC_DESERT", "HexManiacDesertSeenText", "HexManiacDesertBeatenText", 3),
    ("DesertResort", "TrainerLassDesert"):
        ("TRAINER_UNOVA_LASS_DESERT", "LassDesertSeenText", "LassDesertBeatenText", 2),
    ("DesertResort", "TrainerPkmnRangerFDesert"):
        ("TRAINER_UNOVA_PKMN_RANGERF_DESERT", "PkmnRangerFDesertSeenText", "PkmnRangerFDesertBeatenText", 3),
    ("DesertResort", "TrainerPkmnRangerMDesert"):
        ("TRAINER_UNOVA_PKMN_RANGERM_DESERT", "PkmnRangerMDesertSeenText", "PkmnRangerMDesertBeatenText", 3),
    ("DesertResort", "TrainerRoughneckDesert"):
        ("TRAINER_UNOVA_ROUGHNECK_DESERT", "RoughneckDesertSeenText", "RoughneckDesertBeatenText", 3),
    ("DesertResort", "TrainerYoungsterDesert"):
        ("TRAINER_UNOVA_YOUNGSTER_DESERT", "YoungsterDesertSeenText", "YoungsterDesertBeatenText", 4),
    ("DragonspiralTower2F", "TrainerDragonspiralTowerGiallo"):
        ("TRAINER_UNOVA_GIALLO2", "DragonspiralTowerGialloSeenText", "DragonspiralTowerGialloBeatenText", 1),
    ("DragonspiralTower3F", "TrainerDragonspiralTowerRyoku"):
        ("TRAINER_UNOVA_RYOKU2", "DragonspiralTowerRyokuSeenText", "DragonspiralTowerRyokuBeatenText", 1),
    ("DragonspiralTower4F", "TrainerDragonspiralTowerBronius"):
        ("TRAINER_UNOVA_BRONIUS2", "DragonspiralTowerBroniusSeenText", "DragonspiralTowerBroniusBeatenText", 1),
    ("DragonspiralTower5F", "TrainerDragonspiralTowerGorm"):
        ("TRAINER_UNOVA_GORM2", "DragonspiralTowerGormSeenText", "DragonspiralTowerGormBeatenText", 1),
    ("Dreamyard", "TrainerSchoolKidFDreamyard"):
        ("TRAINER_UNOVA_SCHOOL_KIDF_DREAMYARD", "SchoolKidFDreamyardSeenText", "SchoolKidFDreamyardBeatenText", 2),
    ("Dreamyard", "TrainerSchoolKidMDreamyard"):
        ("TRAINER_UNOVA_SCHOOL_KIDM_DREAMYARD", "SchoolKidMDreamyardSeenText", "SchoolKidMDreamyardBeatenText", 3),
    ("Dreamyard", "TrainerYoungsterDreamyard"):
        ("TRAINER_UNOVA_YOUNGSTER_DREAMYARD", "YoungsterDreamyardSeenText", "YoungsterDreamyardBeatenText", 2),
    ("DreamyardB1F", "TrainerPsychicFDreamyard"):
        ("TRAINER_UNOVA_PSYCHICF_DREAMYARD", "PsychicFDreamyardSeenText", "PsychicFDreamyardBeatenText", 2),
    ("DreamyardB1F", "TrainerPsychicMDreamyard"):
        ("TRAINER_UNOVA_PSYCHICM_DREAMYARD", "PsychicMDreamyardSeenText", "PsychicMDreamyardBeatenText", 2),
    ("DreamyardB1F", "TrainerScientistFDreamyard"):
        ("TRAINER_UNOVA_SCIENTISTF_DREAMYARD", "ScientistFDreamyardSeenText", "ScientistFDreamyardBeatenText", 2),
    ("DreamyardB1F", "TrainerScientistMDreamyard"):
        ("TRAINER_UNOVA_SCIENTISTM_DREAMYARD", "ScientistMDreamyardSeenText", "ScientistMDreamyardBeatenText", 2),
    ("GiantChasmB1F", "TrainerAceTrainerFGiantChasm"):
        ("TRAINER_UNOVA_ACE_TRAINERF_GIANT_CHASM", "AceTrainerFGiantChasmSeenText", "AceTrainerFGiantChasmBeatenText", 1),
    ("GiantChasmB1F", "TrainerAceTrainerMGiantChasm"):
        ("TRAINER_UNOVA_ACE_TRAINERM_GIANT_CHASM", "AceTrainerMGiantChasmSeenText", "AceTrainerMGiantChasmBeatenText", 2),
    ("GiantChasmB1F", "TrainerBackpackerFGiantChasm"):
        ("TRAINER_UNOVA_BACKPACKERF_GIANT_CHASM", "BackpackerFGiantChasmSeenText", "BackpackerFGiantChasmBeatenText", 2),
    ("GiantChasmB1F", "TrainerBackpackerMGiantChasm"):
        ("TRAINER_UNOVA_BACKPACKERM_GIANT_CHASM", "BackpackerMGiantChasmSeenText", "BackpackerMGiantChasmBeatenText", 3),
    ("GiantChasmB1F", "TrainerHikerGiantChasm"):
        ("TRAINER_UNOVA_HIKER_GIANT_CHASM", "HikerGiantChasmSeenText", "HikerGiantChasmBeatenText", 3),
    ("HumilauGym", "TrainerSwimmerFHumilauGym"):
        ("TRAINER_UNOVA_SWIMMER_F_HUMILAU_GYM", "SwimmerFHumilauGymSeenText", "SwimmerFHumilauGymBeatenText", 2),
    ("HumilauGym", "TrainerSwimmerMHumilauGym"):
        ("TRAINER_UNOVA_SWIMMER_M_HUMILAU_GYM", "SwimmerMHumilauGymSeenText", "SwimmerMHumilauGymBeatenText", 2),
    ("LentimasOutskirts", "OutskirtsDoctorScript"):
        ("TRAINER_UNOVA_DOCTOR_OUTSKIRTS", "OutskirtsDoctorIntroText", "OutskirtsDoctorWinText", 0),
    ("LentimasOutskirts", "TrainerCyclistFOutskirts"):
        ("TRAINER_UNOVA_CYCLISTF_OUTSKIRTS", "CyclistFOutskirtsSeenText", "CyclistFOutskirtsBeatenText", 2),
    ("LentimasOutskirts", "TrainerCyclistMOutskirts"):
        ("TRAINER_UNOVA_CYCLISTM_OUTSKIRTS", "CyclistMOutskirtsSeenText", "CyclistMOutskirtsBeatenText", 3),
    ("LentimasOutskirts", "TrainerPkmnRangerFOutskirts"):
        ("TRAINER_UNOVA_PKMN_RANGERF_OUTSKIRTS", "PkmnRangerFOutskirtsSeenText", "PkmnRangerFOutskirtsBeatenText", 3),
    ("LentimasOutskirts", "TrainerPkmnRangerMOutskirts"):
        ("TRAINER_UNOVA_PKMN_RANGERM_OUTSKIRTS", "PkmnRangerMOutskirtsSeenText", "PkmnRangerMOutskirtsBeatenText", 3),
    ("LentimasOutskirts", "TrainerSchoolKidMOutskirts"):
        ("TRAINER_UNOVA_SCHOOL_KIDM_OUTSKIRTS", "SchoolKidMOutskirtsSeenText", "SchoolKidMOutskirtsBeatenText", 1),
    ("LentimasOutskirts", "TrainerYoungsterOutskirts"):
        ("TRAINER_UNOVA_YOUNGSTER_OUTSKIRTS", "YoungsterOutskirtsSeenText", "YoungsterOutskirtsBeatenText", 2),
    ("LostlornForest", "TrainerLassLostlorn"):
        ("TRAINER_UNOVA_LASS_LOSTLORN", "LassLostlornSeenText", "LassLostlornBeatenText", 1),
    ("LostlornForest", "TrainerPkmnBreederFLostlorn"):
        ("TRAINER_UNOVA_PKMN_BREEDERF_LOSTLORN", "PkmnBreederFLostlornSeenText", "PkmnBreederFLostlornBeatenText", 3),
    ("LostlornForest", "TrainerPkmnBreederMLostlorn"):
        ("TRAINER_UNOVA_PKMN_BREEDERM_LOSTLORN", "PkmnBreederMLostlornSeenText", "PkmnBreederMLostlornBeatenText", 2),
    ("LostlornForest", "TrainerSchoolKidFLostlorn"):
        ("TRAINER_UNOVA_SCHOOL_KIDF_LOSTLORN", "SchoolKidFLostlornSeenText", "SchoolKidFLostlornBeatenText", 2),
    ("LostlornForest", "TrainerSchoolKidMLostlorn"):
        ("TRAINER_UNOVA_SCHOOL_KIDM_LOSTLORN", "SchoolKidMLostlornSeenText", "SchoolKidMLostlornBeatenText", 3),
    ("LostlornForest", "TrainerYoungsterLostlorn"):
        ("TRAINER_UNOVA_YOUNGSTER_LOSTLORN", "YoungsterLostlornSeenText", "YoungsterLostlornBeatenText", 1),
    ("MarineTube", "TrainerNurseryAideMarineTube"):
        ("TRAINER_UNOVA_NURSERY_AIDE_MARINE_TUBE", "NurseryAideMarineTubeSeenText", "NurseryAideMarineTubeBeatenText", 0),
    ("MarineTube", "TrainerPreschoolerFMarineTube"):
        ("TRAINER_UNOVA_PRESCHOOLERF_MARINE_TUBE", "PreschoolerFMarineTubeSeenText", "PreschoolerFMarineTubeBeatenText", 1),
    ("MarineTube", "TrainerPreschoolerMMarineTube"):
        ("TRAINER_UNOVA_PRESCHOOLERM_MARINE_TUBE", "PreschoolerMMarineTubeSeenText", "PreschoolerMMarineTubeBeatenText", 1),
    ("MarineTube", "TrainerTwinsMarineTube"):
        ("TRAINER_UNOVA_TWINS_MARINE_TUBE", "TwinsMarineTubeSeenText", "TwinsMarineTubeBeatenText", 1),
    ("MistraltonCave1F", "TrainerHiker1MistraltonCave"):
        ("TRAINER_UNOVA_HIKER_MISTRALTON_CAVE_1", "Hiker1MistraltonCaveSeenText", "Hiker1MistraltonCaveBeatenText", 2),
    ("MistraltonCave1F", "TrainerHiker2MistraltonCave"):
        ("TRAINER_UNOVA_HIKER_MISTRALTON_CAVE_2", "Hiker2MistraltonCaveSeenText", "Hiker2MistraltonCaveBeatenText", 2),
    ("MistraltonCave2F", "TrainerAceTrainerFMistraltonCave"):
        ("TRAINER_UNOVA_ACE_TRAINERF_MISTRALTON_CAVE", "AceTrainerFMistraltonCaveSeenText", "AceTrainerFMistraltonCaveBeatenText", 1),
    ("MistraltonCave2F", "TrainerAceTrainerMMistraltonCave"):
        ("TRAINER_UNOVA_ACE_TRAINERM_MISTRALTON_CAVE", "AceTrainerMMistraltonCaveSeenText", "AceTrainerMMistraltonCaveBeatenText", 1),
    ("MistraltonGym1F", "TrainerPilot1MistraltonGym1F"):
        ("TRAINER_UNOVA_PILOT_MISTRALTON_GYM_1", "Pilot1MistraltonGym1FSeenText", "Pilot1MistraltonGym1FBeatenText", 2),
    ("MistraltonGym1F", "TrainerPilot2MistraltonGym1F"):
        ("TRAINER_UNOVA_PILOT_MISTRALTON_GYM_2", "Pilot2MistraltonGym1FSeenText", "Pilot2MistraltonGym1FBeatenText", 1),
    ("MistraltonGym1F", "TrainerPilot3MistraltonGym1F"):
        ("TRAINER_UNOVA_PILOT_MISTRALTON_GYM_3", "Pilot3MistraltonGym1FSeenText", "Pilot3MistraltonGym1FBeatenText", 2),
    ("MistraltonGym2F", "TrainerPilot1MistraltonGym2F"):
        ("TRAINER_UNOVA_PILOT_MISTRALTON_GYM_4", "Pilot1MistraltonGym2FSeenText", "Pilot1MistraltonGym2FBeatenText", 2),
    ("MistraltonGym2F", "TrainerPilot2MistraltonGym2F"):
        ("TRAINER_UNOVA_PILOT_MISTRALTON_GYM_5", "Pilot2MistraltonGym2FSeenText", "Pilot2MistraltonGym2FBeatenText", 1),
    ("MoorOfIcirrus", "TrainerFisher1MoorOfIcirrus"):
        ("TRAINER_UNOVA_FISHER_MOOR_OF_ICIRRUS_1", "Fisher1MoorOfIcirrusSeenText", "Fisher1MoorOfIcirrusBeatenText", 2),
    ("MoorOfIcirrus", "TrainerFisher2MoorOfIcirrus"):
        ("TRAINER_UNOVA_FISHER_MOOR_OF_ICIRRUS_2", "Fisher2MoorOfIcirrusSeenText", "Fisher2MoorOfIcirrusBeatenText", 1),
    ("MoorOfIcirrus", "TrainerPkmnRangerFMoorOfIcirrus"):
        ("TRAINER_UNOVA_PKMN_RANGERF_MOOR_OF_ICIRRUS", "PkmnRangerFMoorOfIcirrusSeenText", "PkmnRangerFMoorOfIcirrusBeatenText", 2),
    ("MoorOfIcirrus", "TrainerPkmnRangerMMoorOfIcirrus"):
        ("TRAINER_UNOVA_PKMN_RANGERM_MOOR_OF_ICIRRUS", "PkmnRangerMMoorOfIcirrusSeenText", "PkmnRangerMMoorOfIcirrusBeatenText", 3),
    ("NacreneOutskirt", "TrainerLassNacrene"):
        ("TRAINER_UNOVA_LASS_NACRENE_OUTSKIRT", "LassNacreneSeenText", "LassNacreneBeatenText", 3),
    ("NacreneOutskirt", "TrainerParasolLadyNacrene"):
        ("TRAINER_UNOVA_PARASOL_LADY_NACRENE_OUTSKIRT", "ParasolLadyNacreneSeenText", "ParasolLadyNacreneBeatenText", 2),
    ("NacreneOutskirt", "TrainerRichBoyNacrene"):
        ("TRAINER_UNOVA_RICH_BOY_NACRENE_OUTSKIRT", "RichBoyNacreneSeenText", "RichBoyNacreneBeatenText", 1),
    ("NacreneOutskirt", "TrainerYoungsterNacrene"):
        ("TRAINER_UNOVA_YOUNGSTER_NACRENE_OUTSKIRT", "YoungsterNacreneSeenText", "YoungsterNacreneBeatenText", 3),
    ("NacreneOutskirtEast", "TrainerBattleGirlNacrene"):
        ("TRAINER_UNOVA_BATTLE_GIRL_NACRENE_OUTSKIRT", "BattleGirlNacreneSeenText", "BattleGirlNacreneBeatenText", 2),
    ("NacreneOutskirtEast", "TrainerBlackbeltNacrene"):
        ("TRAINER_UNOVA_BLACKBELT_NACRENE_OUTSKIRT", "BlackbeltNacreneSeenText", "BlackbeltNacreneBeatenText", 2),
    ("NimbasaParkCoasterRoom", "TrainerGruntFNimbasaPark1"):
        ("TRAINER_UNOVA_GRUNTF_NIMBASA_1", "GruntFNimbasaPark1SeenText", "GruntFNimbasaPark1BeatenText", 2),
    ("NimbasaParkCoasterRoom", "TrainerGruntFNimbasaPark2"):
        ("TRAINER_UNOVA_GRUNTF_NIMBASA_2", "GruntFNimbasaPark2SeenText", "GruntFNimbasaPark2BeatenText", 2),
    ("NimbasaParkCoasterRoom", "TrainerGruntFNimbasaPark3"):
        ("TRAINER_UNOVA_GRUNTF_NIMBASA_3", "GruntFNimbasaPark3SeenText", "GruntFNimbasaPark3BeatenText", 1),
    ("NimbasaParkCoasterRoom", "TrainerGruntMNimbasaPark1"):
        ("TRAINER_UNOVA_GRUNTM_NIMBASA_1", "GruntMNimbasaPark1SeenText", "GruntMNimbasaPark1BeatenText", 2),
    ("NimbasaParkCoasterRoom", "TrainerGruntMNimbasaPark2"):
        ("TRAINER_UNOVA_GRUNTM_NIMBASA_2", "GruntMNimbasaPark2SeenText", "GruntMNimbasaPark2BeatenText", 2),
    ("NimbasaParkCoasterRoom", "TrainerGruntMNimbasaPark3"):
        ("TRAINER_UNOVA_GRUNTM_NIMBASA_3", "GruntMNimbasaPark3SeenText", "GruntMNimbasaPark3BeatenText", 4),
    ("NimbasaParkRunway", "TrainerGruntFNimbasaPark4"):
        ("TRAINER_UNOVA_GRUNTF_NIMBASA_4", "GruntFNimbasaPark4SeenText", "GruntFNimbasaPark4BeatenText", 2),
    ("NimbasaParkRunway", "TrainerGruntFNimbasaPark5"):
        ("TRAINER_UNOVA_GRUNTF_NIMBASA_5", "GruntFNimbasaPark5SeenText", "GruntFNimbasaPark5BeatenText", 2),
    ("NimbasaParkRunway", "TrainerGruntMNimbasaPark5"):
        ("TRAINER_UNOVA_GRUNTM_NIMBASA_5", "GruntMNimbasaPark5SeenText", "GruntMNimbasaPark5BeatenText", 2),
    ("OpelucidGym", "TrainerVeteranF1OpelucidGym"):
        ("TRAINER_UNOVA_VETERANF_OPELUCID_GYM_1", "VeteranF1OpelucidGymSeenText", "VeteranF1OpelucidGymBeatenText", 1),
    ("OpelucidGym", "TrainerVeteranF2OpelucidGym"):
        ("TRAINER_UNOVA_VETERANF_OPELUCID_GYM_2", "VeteranF2OpelucidGymSeenText", "VeteranF2OpelucidGymBeatenText", 1),
    ("OpelucidGym", "TrainerVeteranF3OpelucidGym"):
        ("TRAINER_UNOVA_VETERANF_OPELUCID_GYM_3", "VeteranF3OpelucidGymSeenText", "VeteranF3OpelucidGymBeatenText", 2),
    ("OpelucidGym", "TrainerVeteranM1OpelucidGym"):
        ("TRAINER_UNOVA_VETERANM_OPELUCID_GYM_1", "VeteranM1OpelucidGymSeenText", "VeteranM1OpelucidGymBeatenText", 1),
    ("OpelucidGym", "TrainerVeteranM2OpelucidGym"):
        ("TRAINER_UNOVA_VETERANM_OPELUCID_GYM_2", "VeteranM2OpelucidGymSeenText", "VeteranM2OpelucidGymBeatenText", 1),
    ("OpelucidGym", "TrainerVeteranM3OpelucidGym"):
        ("TRAINER_UNOVA_VETERANM_OPELUCID_GYM_3", "VeteranM3OpelucidGymSeenText", "VeteranM3OpelucidGymBeatenText", 1),
    ("P2Lab", "TrainerGruntF1P2Lab"):
        ("TRAINER_UNOVA_GRUNTF_P2_1", "GruntF1P2LabSeenText", "GruntF1P2LabBeatenText", 2),
    ("P2Lab", "TrainerGruntF2P2Lab"):
        ("TRAINER_UNOVA_GRUNTF_P2_2", "GruntF2P2LabSeenText", "GruntF2P2LabBeatenText", 3),
    ("P2Lab", "TrainerGruntM1P2Lab"):
        ("TRAINER_UNOVA_GRUNTM_P2_1", "GruntM1P2LabSeenText", "GruntM1P2LabBeatenText", 2),
    ("P2Lab", "TrainerGruntM2P2Lab"):
        ("TRAINER_UNOVA_GRUNTM_P2_2", "GruntM2P2LabSeenText", "GruntM2P2LabBeatenText", 2),
    ("P2Lab", "TrainerScientistP2Lab"):
        ("TRAINER_UNOVA_SCIENTISTM_P2", "ScientistP2LabSeenText", "ScientistP2LabBeatenText", 2),
    ("PinwheelForest", "TrainerHexManiacPinwheel"):
        ("TRAINER_UNOVA_HEX_MANIAC_PINWHEEL", "HexManiacPinwheelSeenText", "HexManiacPinwheelBeatenText", 1),
    ("PinwheelForest", "TrainerLassPinwheel"):
        ("TRAINER_UNOVA_LASS_PINWHEEL", "LassPinwheelSeenText", "LassPinwheelBeatenText", 2),
    ("PinwheelForest", "TrainerPkmnRangerFPinwheel1"):
        ("TRAINER_UNOVA_PKMN_RANGERF_PINWHEEL_1", "PkmnRangerFPinwheel1SeenText", "PkmnRangerFPinwheel1BeatenText", 2),
    ("PinwheelForest", "TrainerPkmnRangerFPinwheel2"):
        ("TRAINER_UNOVA_PKMN_RANGERF_PINWHEEL_2", "PkmnRangerFPinwheel2SeenText", "PkmnRangerFPinwheel2BeatenText", 3),
    ("PinwheelForest", "TrainerPkmnRangerMPinwheel1"):
        ("TRAINER_UNOVA_PKMN_RANGERM_PINWHEEL_1", "PkmnRangerMPinwheel1SeenText", "PkmnRangerMPinwheel1BeatenText", 2),
    ("PinwheelForest", "TrainerPkmnRangerMPinwheel2"):
        ("TRAINER_UNOVA_PKMN_RANGERM_PINWHEEL_2", "PkmnRangerMPinwheel2SeenText", "PkmnRangerMPinwheel2BeatenText", 1),
    ("PinwheelForest", "TrainerPsychicMPinwheel"):
        ("TRAINER_UNOVA_PSYCHICM_PINWHEEL", "PsychicMPinwheelSeenText", "PsychicMPinwheelBeatenText", 3),
    ("PinwheelForest", "TrainerYoungsterPinwheel"):
        ("TRAINER_UNOVA_YOUNGSTER_PINWHEEL", "YoungsterPinwheelSeenText", "YoungsterPinwheelBeatenText", 2),
    ("RelicCastle1F", "TrainerPsychicMRelicCastle1F"):
        ("TRAINER_UNOVA_PSYCHICM_RELIC_CASTLE", "PsychicMRelicCastle1FSeenText", "PsychicMRelicCastle1FBeatenText", 2),
    ("RelicCastleB1F", "TrainerPsychicFRelicCastleB1F"):
        ("TRAINER_UNOVA_PSYCHICF_RELIC_CASTLE_1", "PsychicFRelicCastleB1FSeenText", "PsychicFRelicCastleB1FBeatenText", 2),
    ("RelicCastleB2F", "TrainerPsychicFRelicCastleB2F"):
        ("TRAINER_UNOVA_PSYCHICF_RELIC_CASTLE_2", "PsychicFRelicCastleB2FSeenText", "PsychicFRelicCastleB2FBeatenText", 1),
    ("RelicPassageBack", "TrainerBackpackerMRelicPassage"):
        ("TRAINER_UNOVA_BACKPACKERM_RELIC_PASSAGE", "BackpackerMRelicPassageSeenText", "BackpackerMRelicPassageBeatenText", 2),
    ("RelicPassageBack", "TrainerHexManiacRelicPassage"):
        ("TRAINER_UNOVA_HEX_MANIAC_RELIC_PASSAGE", "HexManiacRelicPassageSeenText", "HexManiacRelicPassageBeatenText", 2),
    ("RelicPassageBack", "TrainerPsychicFRelicPassage"):
        ("TRAINER_UNOVA_PSYCHICF_RELIC_PASSAGE", "PsychicFRelicPassageSeenText", "PsychicFRelicPassageBeatenText", 2),
    ("RelicPassageBack", "TrainerWorkerRelicPassage"):
        ("TRAINER_UNOVA_WORKER_RELIC_PASSAGE", "WorkerRelicPassageSeenText", "WorkerRelicPassageBeatenText", 2),
    ("RelicPassageFront", "TrainerBackpackerFRelicPassage"):
        ("TRAINER_UNOVA_BACKPACKERF_RELIC_PASSAGE", "BackpackerFRelicPassageSeenText", "BackpackerFRelicPassageBeatenText", 3),
    ("RelicPassageFront", "TrainerHiker1RelicPassage"):
        ("TRAINER_UNOVA_HIKER_RELIC_PASSAGE_1", "Hiker1RelicPassageSeenText", "Hiker1RelicPassageBeatenText", 3),
    ("RelicPassageFront", "TrainerHiker2RelicPassage"):
        ("TRAINER_UNOVA_HIKER_RELIC_PASSAGE_2", "Hiker2RelicPassageSeenText", "Hiker2RelicPassageBeatenText", 2),
    ("RelicPassageFront", "TrainerNurseRelicPassage"):
        ("TRAINER_UNOVA_NURSE_RELIC_PASSAGE", "RelicPassageNurseIntroText", "RelicPassageNurseWinText", 0),
    ("RelicPassageFront", "TrainerPsychicMRelicPassage"):
        ("TRAINER_UNOVA_PSYCHICM_RELIC_PASSAGE", "PsychicMRelicPassageSeenText", "PsychicMRelicPassageBeatenText", 2),
    ("ReversalMountain1F", "TrainerBackpackerFReversal"):
        ("TRAINER_UNOVA_BACKPACKERF_REVERSAL", "BackpackerFReversalSeenText", "BackpackerFReversalBeatenText", 1),
    ("ReversalMountain1F", "TrainerBackpackerMReversal"):
        ("TRAINER_UNOVA_BACKPACKERM_REVERSAL", "BackpackerMReversalSeenText", "BackpackerMReversalBeatenText", 2),
    ("ReversalMountain1F", "TrainerBlackbeltReversal"):
        ("TRAINER_UNOVA_BLACKBELT_REVERSAL", "BlackbeltReversalSeenText", "BlackbeltReversalBeatenText", 1),
    ("ReversalMountain1F", "TrainerHiker2Reversal"):
        ("TRAINER_UNOVA_HIKER_REVERSAL_2", "Hiker2ReversalSeenText", "Hiker2ReversalBeatenText", 1),
    ("ReversalMountain1F", "TrainerLassReversal"):
        ("TRAINER_UNOVA_LASS_REVERSAL", "LassReversalSeenText", "LassReversalBeatenText", 3),
    ("ReversalMountain1F", "TrainerSchoolKidFReversal"):
        ("TRAINER_UNOVA_SCHOOL_KIDF_REVERSAL", "SchoolKidFReversalSeenText", "SchoolKidFReversalBeatenText", 2),
    ("ReversalMountainB1F", "TrainerBattleGirlReversal"):
        ("TRAINER_UNOVA_BATTLE_GIRL_REVERSAL", "BattleGirlReversalSeenText", "BattleGirlReversalBeatenText", 1),
    ("ReversalMountainB1F", "TrainerHiker1Reversal"):
        ("TRAINER_UNOVA_HIKER_REVERSAL_1", "Hiker1ReversalSeenText", "Hiker1ReversalBeatenText", 2),
    ("Rt1", "TrainerBattleGirlR1"):
        ("TRAINER_UNOVA_BATTLE_GIRL_R1", "BattleGirlR1SeenText", "BattleGirlR1BeatenText", 2),
    ("Rt1", "TrainerBlackbeltR1"):
        ("TRAINER_UNOVA_BLACKBELT_R1", "BlackbeltR1SeenText", "BlackbeltR1BeatenText", 3),
    ("Rt1", "TrainerMaidR1"):
        ("TRAINER_UNOVA_MAID_R1", "MaidR1SeenText", "MaidR1BeatenText", 3),
    ("Rt1", "TrainerPkmnRangerFR1"):
        ("TRAINER_UNOVA_PKMN_RANGERF_R1", "PkmnRangerFR1SeenText", "PkmnRangerFR1BeatenText", 2),
    ("Rt1", "TrainerPkmnRangerMR1"):
        ("TRAINER_UNOVA_PKMN_RANGERM_R1", "PkmnRangerMR1SeenText", "PkmnRangerMR1BeatenText", 2),
    ("Rt1", "TrainerTwinsR1"):
        ("TRAINER_UNOVA_TWINS_R1", "TwinsR1SeenText", "TwinsR1BeatenText", 3),
    ("Rt11", "TrainerBackersFR11"):
        ("TRAINER_UNOVA_BACKERSF_R11", "BackersFR11SeenText", "BackersFR11BeatenText", 1),
    ("Rt11", "TrainerBackersMR11"):
        ("TRAINER_UNOVA_BACKERSM_R11", "BackersMR11SeenText", "BackersMR11BeatenText", 1),
    ("Rt13", "TrainerLassR13"):
        ("TRAINER_UNOVA_LASS_R13", "LassR13SeenText", "LassR13BeatenText", 3),
    ("Rt13", "TrainerSchoolKidFR13"):
        ("TRAINER_UNOVA_SCHOOL_KIDF_R13", "SchoolKidFR13SeenText", "SchoolKidFR13BeatenText", 4),
    ("Rt13", "TrainerSchoolKidMR13"):
        ("TRAINER_UNOVA_SCHOOL_KIDM_R13", "SchoolKidMR13SeenText", "SchoolKidMR13BeatenText", 2),
    ("Rt13", "TrainerYoungsterR13"):
        ("TRAINER_UNOVA_YOUNGSTER_R13", "YoungsterR13SeenText", "YoungsterR13BeatenText", 3),
    ("Rt14", "TrainerPreschoolerF1R14"):
        ("TRAINER_UNOVA_PRESCHOOLERF_R14_1", "PreschoolerF1R14SeenText", "PreschoolerF1R14BeatenText", 3),
    ("Rt14", "TrainerPreschoolerF2R14"):
        ("TRAINER_UNOVA_PRESCHOOLERF_R14_2", "PreschoolerF2R14SeenText", "PreschoolerF2R14BeatenText", 3),
    ("Rt14", "TrainerPreschoolerM1R14"):
        ("TRAINER_UNOVA_PRESCHOOLERM_R14_1", "PreschoolerM1R14SeenText", "PreschoolerM1R14BeatenText", 3),
    ("Rt14", "TrainerPreschoolerM2R14"):
        ("TRAINER_UNOVA_PRESCHOOLERM_R14_2", "PreschoolerM2R14SeenText", "PreschoolerM2R14BeatenText", 2),
    ("Rt16", "TrainerBackersMR16"):
        ("TRAINER_UNOVA_BACKERSM_R16", "BackersMR16SeenText", "BackersMR16BeatenText", 1),
    ("Rt16", "TrainerBackpackerFR16"):
        ("TRAINER_UNOVA_BACKPACKERF_R16", "BackpackerFR16SeenText", "BackpackerFR16BeatenText", 4),
    ("Rt16", "TrainerBackpackerMR16"):
        ("TRAINER_UNOVA_BACKPACKERM_R16", "BackpackerMR16SeenText", "BackpackerMR16BeatenText", 3),
    ("Rt16", "TrainerCyclistFR16"):
        ("TRAINER_UNOVA_CYCLISTF_R16", "CyclistFR16SeenText", "CyclistFR16BeatenText", 2),
    ("Rt16", "TrainerCyclistMR16"):
        ("TRAINER_UNOVA_CYCLISTM_R16", "CyclistMR16SeenText", "CyclistMR16BeatenText", 3),
    ("Rt17", "R17DoctorScript"):
        ("TRAINER_UNOVA_DOCTOR_R17", "R17DoctorIntroText", "R17DoctorWinText", 0),
    ("Rt17", "TrainerFisher1R17"):
        ("TRAINER_UNOVA_FISHER_R17_1", "Fisher1R17SeenText", "Fisher1R17BeatenText", 3),
    ("Rt17", "TrainerFisher2R17"):
        ("TRAINER_UNOVA_FISHER_R17_2", "Fisher2R17SeenText", "Fisher2R17BeatenText", 1),
    ("Rt17", "TrainerSwimmerF1R17"):
        ("TRAINER_UNOVA_SWIMMER_F_R17_1", "SwimmerF1R17SeenText", "SwimmerF1R17BeatenText", 1),
    ("Rt17", "TrainerSwimmerF2R17"):
        ("TRAINER_UNOVA_SWIMMER_F_R17_2", "SwimmerF2R17SeenText", "SwimmerF2R17BeatenText", 2),
    ("Rt17", "TrainerSwimmerM1R17"):
        ("TRAINER_UNOVA_SWIMMER_M_R17_1", "SwimmerM1R17SeenText", "SwimmerM1R17BeatenText", 1),
    ("Rt17", "TrainerSwimmerM2R17"):
        ("TRAINER_UNOVA_SWIMMER_M_R17_2", "SwimmerM2R17SeenText", "SwimmerM2R17BeatenText", 1),
    ("Rt18", "TrainerBackpackerFR18"):
        ("TRAINER_UNOVA_BACKPACKERF_R18", "BackpackerFR18SeenText", "BackpackerFR18BeatenText", 3),
    ("Rt18", "TrainerBackpackerMR18"):
        ("TRAINER_UNOVA_BACKPACKERM_R18", "BackpackerMR18SeenText", "BackpackerMR18BeatenText", 3),
    ("Rt18", "TrainerBattleGirlR18"):
        ("TRAINER_UNOVA_BATTLE_GIRL_R18", "BattleGirlR18SeenText", "BattleGirlR18BeatenText", 2),
    ("Rt18", "TrainerBlackbeltR18"):
        ("TRAINER_UNOVA_BLACKBELT_R18", "BlackbeltR18SeenText", "BlackbeltR18BeatenText", 3),
    ("Rt18", "TrainerHikerR18"):
        ("TRAINER_UNOVA_HIKER_R18", "HikerR18SeenText", "HikerR18BeatenText", 2),
    ("Rt19", "TrainerBakerR19"):
        ("TRAINER_UNOVA_BAKER_R19", "BakerR19SeenText", "BakerR19BeatenText", 2),
    ("Rt19", "TrainerDepotAgent1R19"):
        ("TRAINER_UNOVA_DEPOT_AGENT_R19_1", "DepotAgent1R19SeenText", "DepotAgent1R19BeatenText", 2),
    ("Rt19", "TrainerDepotAgent2R19"):
        ("TRAINER_UNOVA_DEPOT_AGENT_R19_2", "DepotAgent2R19SeenText", "DepotAgent2R19BeatenText", 3),
    ("Rt19", "TrainerLadyR19"):
        ("TRAINER_UNOVA_LADY_R19", "LadyR19SeenText", "LadyR19BeatenText", 2),
    ("Rt19", "TrainerMaidR19"):
        ("TRAINER_UNOVA_MAID_R19", "MaidR19SeenText", "MaidR19BeatenText", 3),
    ("Rt19", "TrainerPkmnBreederFR19"):
        ("TRAINER_UNOVA_PKMN_BREEDERF_R19", "PkmnBreederFR19SeenText", "PkmnBreederFR19BeatenText", 3),
    ("Rt19", "TrainerPkmnBreederMR19"):
        ("TRAINER_UNOVA_PKMN_BREEDERM_R19", "PkmnBreederMR19SeenText", "PkmnBreederMR19BeatenText", 3),
    ("Rt2", "TrainerBackpackerFR2"):
        ("TRAINER_UNOVA_BACKPACKERF_R2", "BackpackerFR2SeenText", "BackpackerFR2BeatenText", 2),
    ("Rt2", "TrainerBackpackerMR2"):
        ("TRAINER_UNOVA_BACKPACKERM_R2", "BackpackerMR2SeenText", "BackpackerMR2BeatenText", 2),
    ("Rt2", "TrainerGentlemanR2"):
        ("TRAINER_UNOVA_GENTLEMAN_R2", "GentlemanR2SeenText", "GentlemanR2BeatenText", 2),
    ("Rt2", "TrainerLassR2"):
        ("TRAINER_UNOVA_LASS_R2", "LassR2SeenText", "LassR2BeatenText", 2),
    ("Rt2", "TrainerPolicemanR2"):
        ("TRAINER_UNOVA_POLICEMAN_R2", "PolicemanR2SeenText", "PolicemanR2BeatenText", 2),
    ("Rt2", "TrainerSocialiteR2"):
        ("TRAINER_UNOVA_SOCIALITE_R2", "SocialiteR2SeenText", "SocialiteR2BeatenText", 2),
    ("Rt2", "TrainerTwinsR2"):
        ("TRAINER_UNOVA_TWINS_R2", "TwinsR2SeenText", "TwinsR2BeatenText", 1),
    ("Rt2", "TrainerYoungsterR2"):
        ("TRAINER_UNOVA_YOUNGSTER_R2", "YoungsterR2SeenText", "YoungsterR2BeatenText", 3),
    ("Rt20", "TrainerNurseryAideR20"):
        ("TRAINER_UNOVA_NURSERY_AIDE_R20", "NurseryAideR20SeenText", "NurseryAideR20BeatenText", 3),
    ("Rt20", "TrainerSchoolKidF1R20"):
        ("TRAINER_UNOVA_SCHOOL_KIDF_R20_1", "SchoolKidF1R20SeenText", "SchoolKidF1R20BeatenText", 3),
    ("Rt20", "TrainerSchoolKidF2R20"):
        ("TRAINER_UNOVA_SCHOOL_KIDF_R20_2", "SchoolKidF2R20SeenText", "SchoolKidF2R20BeatenText", 3),
    ("Rt20", "TrainerSchoolKidF3R20"):
        ("TRAINER_UNOVA_SCHOOL_KIDF_R20_3", "SchoolKidF3R20SeenText", "SchoolKidF3R20BeatenText", 2),
    ("Rt20", "TrainerSchoolKidM1R20"):
        ("TRAINER_UNOVA_SCHOOL_KIDM_R20_1", "SchoolKidM1R20SeenText", "SchoolKidM1R20BeatenText", 3),
    ("Rt20", "TrainerSchoolKidM2R20"):
        ("TRAINER_UNOVA_SCHOOL_KIDM_R20_2", "SchoolKidM2R20SeenText", "SchoolKidM2R20BeatenText", 2),
    ("Rt20", "TrainerSchoolKidM3R20"):
        ("TRAINER_UNOVA_SCHOOL_KIDM_R20_3", "SchoolKidM3R20SeenText", "SchoolKidM3R20BeatenText", 3),
    ("Rt20", "TrainerTwinsR20"):
        ("TRAINER_UNOVA_TWINS_R20", "TwinsR20SeenText", "TwinsR20BeatenText", 1),
    ("Rt21", "TrainerBlackbeltR21"):
        ("TRAINER_UNOVA_BLACKBELT_R21", "BlackbeltR21SeenText", "BlackbeltR21BeatenText", 2),
    ("Rt21", "TrainerSwimmerF1R21"):
        ("TRAINER_UNOVA_SWIMMER_F_R21_1", "SwimmerF1R21SeenText", "SwimmerF1R21BeatenText", 3),
    ("Rt21", "TrainerSwimmerF2R21"):
        ("TRAINER_UNOVA_SWIMMER_F_R21_2", "SwimmerF2R21SeenText", "SwimmerF2R21BeatenText", 2),
    ("Rt21", "TrainerSwimmerF3R21"):
        ("TRAINER_UNOVA_SWIMMER_F_R21_3", "SwimmerF3R21SeenText", "SwimmerF3R21BeatenText", 2),
    ("Rt21", "TrainerSwimmerM1R21"):
        ("TRAINER_UNOVA_SWIMMER_M_R21_1", "SwimmerM1R21SeenText", "SwimmerM1R21BeatenText", 2),
    ("Rt21", "TrainerSwimmerM2R21"):
        ("TRAINER_UNOVA_SWIMMER_M_R21_2", "SwimmerM2R21SeenText", "SwimmerM2R21BeatenText", 2),
    ("Rt21", "TrainerSwimmerM3R21"):
        ("TRAINER_UNOVA_SWIMMER_M_R21_3", "SwimmerM3R21SeenText", "SwimmerM3R21BeatenText", 2),
    ("Rt23East", "TrainerAceTrainerF1R23"):
        ("TRAINER_UNOVA_ACE_TRAINERF_R23_1", "AceTrainerF1R23SeenText", "AceTrainerF1R23BeatenText", 1),
    ("Rt23East", "TrainerAceTrainerM1R23"):
        ("TRAINER_UNOVA_ACE_TRAINERM_R23_1", "AceTrainerM1R23SeenText", "AceTrainerM1R23BeatenText", 2),
    ("Rt23West", "TrainerAceTrainerF2R23"):
        ("TRAINER_UNOVA_ACE_TRAINERF_R23_2", "AceTrainerF2R23SeenText", "AceTrainerF2R23BeatenText", 1),
    ("Rt23West", "TrainerAceTrainerM2R23"):
        ("TRAINER_UNOVA_ACE_TRAINERM_R23_2", "AceTrainerM2R23SeenText", "AceTrainerM2R23BeatenText", 1),
    ("Rt23West", "TrainerBackpackerFR23"):
        ("TRAINER_UNOVA_BACKPACKERF_R23", "BackpackerFR23SeenText", "BackpackerFR23BeatenText", 2),
    ("Rt23West", "TrainerBackpackerMR23"):
        ("TRAINER_UNOVA_BACKPACKERM_R23", "BackpackerMR23SeenText", "BackpackerMR23BeatenText", 1),
    ("Rt23West", "TrainerBattleGirlR23"):
        ("TRAINER_UNOVA_BATTLE_GIRL_R23", "BattleGirlR23SeenText", "BattleGirlR23BeatenText", 1),
    ("Rt23West", "TrainerPkmnRangerFR23"):
        ("TRAINER_UNOVA_PKMN_RANGERF_R23", "PkmnRangerFR23SeenText", "PkmnRangerFR23BeatenText", 2),
    ("Rt23West", "TrainerPkmnRangerMR23"):
        ("TRAINER_UNOVA_PKMN_RANGERM_R23", "PkmnRangerMR23SeenText", "PkmnRangerMR23BeatenText", 2),
    ("Rt23West", "TrainerVeteranMR23"):
        ("TRAINER_UNOVA_VETERANM_R23", "VeteranMR23SeenText", "VeteranMR23BeatenText", 3),
    ("Rt3", "TrainerArtistR3"):
        ("TRAINER_UNOVA_ARTIST_R3", "ArtistR3SeenText", "ArtistR3BeatenText", 2),
    ("Rt3", "TrainerFisher1R3"):
        ("TRAINER_UNOVA_FISHER_R3_1", "Fisher1R3SeenText", "Fisher1R3BeatenText", 1),
    ("Rt3", "TrainerFisher2R3"):
        ("TRAINER_UNOVA_FISHER_R3_2", "Fisher2R3SeenText", "Fisher2R3BeatenText", 0),
    ("Rt3", "TrainerGentlemanR3"):
        ("TRAINER_UNOVA_GENTLEMAN_R3", "GentlemanR3SeenText", "GentlemanR3BeatenText", 3),
    ("Rt3", "TrainerPkmnRangerFR3"):
        ("TRAINER_UNOVA_PKMN_RANGERF_R3", "PkmnRangerFR3SeenText", "PkmnRangerFR3BeatenText", 3),
    ("Rt3", "TrainerPkmnRangerMR3"):
        ("TRAINER_UNOVA_PKMN_RANGERM_R3", "PkmnRangerMR3SeenText", "PkmnRangerMR3BeatenText", 1),
    ("Rt3", "TrainerSocialiteR3"):
        ("TRAINER_UNOVA_SOCIALITE_R3", "SocialiteR3SeenText", "SocialiteR3BeatenText", 3),
    ("Rt4", "TrainerBikerR4"):
        ("TRAINER_UNOVA_BIKER_R4", "BikerR4SeenText", "BikerR4BeatenText", 3),
    ("Rt4", "TrainerFisher1R4"):
        ("TRAINER_UNOVA_FISHER_R4_1", "Fisher1R4SeenText", "Fisher1R4BeatenText", 0),
    ("Rt4", "TrainerFisher2R4"):
        ("TRAINER_UNOVA_FISHER_R4_2", "Fisher2R4SeenText", "Fisher2R4BeatenText", 0),
    ("Rt4", "TrainerLadyR4"):
        ("TRAINER_UNOVA_LADY_R4", "LadyR4SeenText", "LadyR4BeatenText", 4),
    ("Rt4", "TrainerPokefanFR4"):
        ("TRAINER_UNOVA_POKEFANF_R4", "PokefanFR4SeenText", "PokefanFR4BeatenText", 2),
    ("Rt4", "TrainerPokefanMR4"):
        ("TRAINER_UNOVA_POKEFANM_R4", "PokefanMR4SeenText", "PokefanMR4BeatenText", 2),
    ("Rt4", "TrainerPoliceman1R4"):
        ("TRAINER_UNOVA_POLICEMAN_R4_1", "Policeman1R4SeenText", "Policeman1R4BeatenText", 3),
    ("Rt4", "TrainerPoliceman2R4"):
        ("TRAINER_UNOVA_POLICEMAN_R4_2", "Policeman2R4SeenText", "Policeman2R4BeatenText", 3),
    ("Rt4", "TrainerRichBoyR4"):
        ("TRAINER_UNOVA_RICH_BOY_R4", "RichBoyR4SeenText", "RichBoyR4BeatenText", 4),
    ("Rt4", "TrainerRoughneckR4"):
        ("TRAINER_UNOVA_ROUGHNECK_R4", "RoughneckR4SeenText", "RoughneckR4BeatenText", 3),
    ("Rt5", "TrainerArtistR5"):
        ("TRAINER_UNOVA_ARTIST_R5", "ArtistR5SeenText", "ArtistR5BeatenText", 2),
    ("Rt5", "TrainerBackersFR5"):
        ("TRAINER_UNOVA_BACKERSF_R5", "BackersFR5SeenText", "BackersFR5BeatenText", 1),
    ("Rt5", "TrainerBakerR5"):
        ("TRAINER_UNOVA_BAKER_R5", "BakerR5SeenText", "BakerR5BeatenText", 3),
    ("Rt5", "TrainerDancer1R5"):
        ("TRAINER_UNOVA_DANCER_R5_1", "Dancer1R5SeenText", "Dancer1R5BeatenText", 3),
    ("Rt5", "TrainerDancer2R5"):
        ("TRAINER_UNOVA_DANCER_R5_2", "Dancer2R5SeenText", "Dancer2R5BeatenText", 3),
    ("Rt5", "TrainerLinebackerR5"):
        ("TRAINER_UNOVA_LINEBACKER_R5", "LinebackerR5SeenText", "LinebackerR5BeatenText", 3),
    ("Rt6", "TrainerParasolLady1R6"):
        ("TRAINER_UNOVA_PARASOL_LADY_R6_1", "ParasolLady1R6SeenText", "ParasolLady1R6BeatenText", 3),
    ("Rt6", "TrainerParasolLady2R6"):
        ("TRAINER_UNOVA_PARASOL_LADY_R6_2", "ParasolLady2R6SeenText", "ParasolLady2R6BeatenText", 2),
    ("Rt6", "TrainerPkmnBreederFR6"):
        ("TRAINER_UNOVA_PKMN_BREEDERF_R6", "PkmnBreederFR6SeenText", "PkmnBreederFR6BeatenText", 2),
    ("Rt6", "TrainerPkmnBreederMR6"):
        ("TRAINER_UNOVA_PKMN_BREEDERM_R6", "PkmnBreederMR6SeenText", "PkmnBreederMR6BeatenText", 2),
    ("Rt6", "TrainerPkmnRangerFR6"):
        ("TRAINER_UNOVA_PKMN_RANGERF_R6", "PkmnRangerFR6SeenText", "PkmnRangerFR6BeatenText", 2),
    ("Rt6", "TrainerPkmnRangerMR6"):
        ("TRAINER_UNOVA_PKMN_RANGERM_R6", "PkmnRangerMR6SeenText", "PkmnRangerMR6BeatenText", 3),
    ("Rt6", "TrainerScientistFR6"):
        ("TRAINER_UNOVA_SCIENTISTF_R6", "ScientistFR6SeenText", "ScientistFR6BeatenText", 3),
    ("Rt6", "TrainerScientistMR6"):
        ("TRAINER_UNOVA_SCIENTISTM_R6", "ScientistMR6SeenText", "ScientistMR6BeatenText", 3),
    ("Rt7", "TrainerNurseryAideR7"):
        ("TRAINER_UNOVA_NURSERY_AIDE_R7", "NurseryAideR7SeenText", "NurseryAideR7BeatenText", 2),
    ("Rt7", "TrainerPkmnBreederFR7"):
        ("TRAINER_UNOVA_PKMN_BREEDERF_R7", "PkmnBreederFR7SeenText", "PkmnBreederFR7BeatenText", 2),
    ("Rt7", "TrainerPkmnBreederMR7"):
        ("TRAINER_UNOVA_PKMN_BREEDERM_R7", "PkmnBreederMR7SeenText", "PkmnBreederMR7BeatenText", 1),
    ("Rt7", "TrainerSchoolKidFR7"):
        ("TRAINER_UNOVA_SCHOOL_KIDF_R7", "SchoolKidFR7SeenText", "SchoolKidFR7BeatenText", 3),
    ("Rt7", "TrainerSchoolKidMR7"):
        ("TRAINER_UNOVA_SCHOOL_KIDM_R7", "SchoolKidMR7SeenText", "SchoolKidMR7BeatenText", 3),
    ("Rt7North", "TrainerBackpackerFR7North"):
        ("TRAINER_UNOVA_BACKPACKERF_R7", "BackpackerFR7NorthSeenText", "BackpackerFR7NorthBeatenText", 3),
    ("Rt7North", "TrainerBackpackerMR7North"):
        ("TRAINER_UNOVA_BACKPACKERM_R7", "BackpackerMR7NorthSeenText", "BackpackerMR7NorthBeatenText", 3),
    ("Rt7North", "TrainerHarlequinR7North"):
        ("TRAINER_UNOVA_HARLEQUIN_R7", "HarlequinR7NorthSeenText", "HarlequinR7NorthBeatenText", 4),
    ("Rt7North", "TrainerTwinsR7North"):
        ("TRAINER_UNOVA_TWINS_R7", "TwinsR7NorthSeenText", "TwinsR7NorthBeatenText", 1),
    ("Rt8", "TrainerFisherR8"):
        ("TRAINER_UNOVA_FISHER_R8", "FisherR8SeenText", "FisherR8BeatenText", 1),
    ("Rt8", "TrainerParasolLadyR8"):
        ("TRAINER_UNOVA_PARASOL_LADY_R8", "ParasolLadyR8SeenText", "ParasolLadyR8BeatenText", 3),
    ("Rt8", "TrainerPkmnRangerFR8"):
        ("TRAINER_UNOVA_PKMN_RANGERF_R8", "PkmnRangerFR8SeenText", "PkmnRangerFR8BeatenText", 3),
    ("Rt8", "TrainerPkmnRangerMR8"):
        ("TRAINER_UNOVA_PKMN_RANGERM_R8", "PkmnRangerMR8SeenText", "PkmnRangerMR8BeatenText", 2),
    ("Rt9", "TrainerBiker1R9"):
        ("TRAINER_UNOVA_BIKER_R9_1", "Biker1R9SeenText", "Biker1R9BeatenText", 3),
    ("Rt9", "TrainerBiker2R9"):
        ("TRAINER_UNOVA_BIKER_R9_2", "Biker2R9SeenText", "Biker2R9BeatenText", 2),
    ("Rt9", "TrainerRoughneck1R9"):
        ("TRAINER_UNOVA_ROUGHNECK_R9_1", "Roughneck1R9SeenText", "Roughneck1R9BeatenText", 3),
    ("Rt9", "TrainerRoughneck2R9"):
        ("TRAINER_UNOVA_ROUGHNECK_R9_2", "Roughneck2R9SeenText", "Roughneck2R9BeatenText", 2),
    ("SeasideCave1F", "TrainerBattleGirlSeasideCave1F"):
        ("TRAINER_UNOVA_BATTLE_GIRL_SEASIDE_CAVE_1", "BattleGirlSeasideCave1FSeenText", "BattleGirlSeasideCave1FBeatenText", 2),
    ("SeasideCave1F", "TrainerBlackbeltSeasideCave1F"):
        ("TRAINER_UNOVA_BLACKBELT_SEASIDE_CAVE_1", "BlackbeltSeasideCave1FSeenText", "BlackbeltSeasideCave1FBeatenText", 2),
    ("SeasideCave1F", "TrainerDoctorSeasideCave1F"):
        ("TRAINER_UNOVA_DOCTOR_SEASIDE_CAVE", "SeasideCaveDoctorIntroText", "SeasideCaveDoctorWinText", 0),
    ("SeasideCave1F", "TrainerVeteranFSeasideCave1F"):
        ("TRAINER_UNOVA_VETERANF_SEASIDE_CAVE", "VeteranFSeasideCave1FSeenText", "VeteranFSeasideCave1FBeatenText", 1),
    ("SeasideCaveB1F", "TrainerBattleGirlSeasideCaveB1F"):
        ("TRAINER_UNOVA_BATTLE_GIRL_SEASIDE_CAVE_2", "BattleGirlSeasideCaveB1FSeenText", "BattleGirlSeasideCaveB1FBeatenText", 3),
    ("SeasideCaveB1F", "TrainerBlackbeltSeasideCaveB1F"):
        ("TRAINER_UNOVA_BLACKBELT_SEASIDE_CAVE_2", "BlackbeltSeasideCaveB1FSeenText", "BlackbeltSeasideCaveB1FBeatenText", 1),
    ("SeasideCaveB2F", "TrainerGruntF1SeasideCave"):
        ("TRAINER_UNOVA_GRUNTF_SEASIDE_CAVE_1", "GruntF1SeasideCaveSeenText", "GruntF1SeasideCaveBeatenText", 1),
    ("SeasideCaveB2F", "TrainerGruntF2SeasideCave"):
        ("TRAINER_UNOVA_GRUNTF_SEASIDE_CAVE_2", "GruntF2SeasideCaveSeenText", "GruntF2SeasideCaveBeatenText", 1),
    ("SeasideCaveB2F", "TrainerGruntF3SeasideCave"):
        ("TRAINER_UNOVA_GRUNTF_SEASIDE_CAVE_3", "GruntF3SeasideCaveSeenText", "GruntF3SeasideCaveBeatenText", 1),
    ("SeasideCaveB2F", "TrainerGruntM1SeasideCave"):
        ("TRAINER_UNOVA_GRUNTM_SEASIDE_CAVE_1", "GruntM1SeasideCaveSeenText", "GruntM1SeasideCaveBeatenText", 1),
    ("SeasideCaveB2F", "TrainerGruntM2SeasideCave"):
        ("TRAINER_UNOVA_GRUNTM_SEASIDE_CAVE_2", "GruntM2SeasideCaveSeenText", "GruntM2SeasideCaveBeatenText", 1),
    ("SeasideCaveB2F", "TrainerGruntM3SeasideCave"):
        ("TRAINER_UNOVA_GRUNTM_SEASIDE_CAVE_3", "GruntM3SeasideCaveSeenText", "GruntM3SeasideCaveBeatenText", 1),
    ("TwistMountain1F", "TrainerVeteranMTwistMountain1F"):
        ("TRAINER_UNOVA_VETERANM_TWIST_MOUNTAIN_2", "VeteranMTwistMountain1FSeenText", "VeteranMTwistMountain1FBeatenText", 1),
    ("TwistMountain1F", "TrainerWorkerTwistMountain1F"):
        ("TRAINER_UNOVA_WORKER_TWIST_MOUNTAIN_5", "WorkerTwistMountain1FSeenText", "WorkerTwistMountain1FBeatenText", 2),
    ("TwistMountain2F", "TrainerHikerTwistMountain2F"):
        ("TRAINER_UNOVA_HIKER_TWIST_MOUNTAIN_1", "HikerTwistMountain2FSeenText", "HikerTwistMountain2FBeatenText", 1),
    ("TwistMountain2F", "TrainerVeteranFTwistMountain2F"):
        ("TRAINER_UNOVA_VETERANF_TWIST_MOUNTAIN_2", "VeteranFTwistMountain2FSeenText", "VeteranFTwistMountain2FBeatenText", 1),
    ("TwistMountain2F", "TrainerWorkerTwistMountain2F"):
        ("TRAINER_UNOVA_WORKER_TWIST_MOUNTAIN_4", "WorkerTwistMountain2FSeenText", "WorkerTwistMountain2FBeatenText", 3),
    ("TwistMountain3F", "TrainerVeteranFTwistMountain3F"):
        ("TRAINER_UNOVA_VETERANF_TWIST_MOUNTAIN_1", "VeteranFTwistMountain3FSeenText", "VeteranFTwistMountain3FBeatenText", 1),
    ("TwistMountain3F", "TrainerWorker1TwistMountain3F"):
        ("TRAINER_UNOVA_WORKER_TWIST_MOUNTAIN_2", "Worker1TwistMountain3FSeenText", "Worker1TwistMountain3FBeatenText", 2),
    ("TwistMountain3F", "TrainerWorker2TwistMountain3F"):
        ("TRAINER_UNOVA_WORKER_TWIST_MOUNTAIN_3", "Worker2TwistMountain3FSeenText", "Worker2TwistMountain3FBeatenText", 2),
    ("TwistMountainOutside", "TrainerHikerTwistMountainOutside"):
        ("TRAINER_UNOVA_HIKER_TWIST_MOUNTAIN_2", "HikerTwistMountainOutsideSeenText", "HikerTwistMountainOutsideBeatenText", 2),
    ("TwistMountainOutside", "TrainerNurseTwistMountainOutside"):
        ("TRAINER_UNOVA_NURSE_TWIST_MOUNTAIN", "NurseTwistMountainOutsideIntroText", "NurseTwistMountainOutsideWinText", 0),
    ("TwistMountainOutside", "TrainerVeteranMTwistMountainOutside"):
        ("TRAINER_UNOVA_VETERANM_TWIST_MOUNTAIN_1", "VeteranMTwistMountainOutsideSeenText", "VeteranMTwistMountainOutsideBeatenText", 1),
    ("TwistMountainOutside", "TrainerWorkerTwistMountainOutside"):
        ("TRAINER_UNOVA_WORKER_TWIST_MOUNTAIN_1", "WorkerTwistMountainOutsideSeenText", "WorkerTwistMountainOutsideBeatenText", 1),
    ("UndellaTown", "TrainerFisher1UndellaTown"):
        ("TRAINER_UNOVA_FISHER_UNDELLA_1", "Fisher1UndellaTownSeenText", "Fisher1UndellaTownBeatenText", 1),
    ("UndellaTown", "TrainerFisher2UndellaTown"):
        ("TRAINER_UNOVA_FISHER_UNDELLA_2", "Fisher2UndellaTownSeenText", "Fisher2UndellaTownBeatenText", 1),
    ("VictoryRoadCave1F", "TrainerAceTrainerFVictoryRoadCave1F"):
        ("TRAINER_UNOVA_ACE_TRAINERF_VICTORY_ROAD_INT_2", "AceTrainerFVictoryRoadCave1FSeenText", "AceTrainerFVictoryRoadCave1FBeatenText", 2),
    ("VictoryRoadCave1F", "TrainerAceTrainerMVictoryRoadCave1F"):
        ("TRAINER_UNOVA_ACE_TRAINERM_VICTORY_ROAD_INT_1", "AceTrainerMVictoryRoadCave1FSeenText", "AceTrainerMVictoryRoadCave1FBeatenText", 1),
    ("VictoryRoadCave1F", "TrainerHexManiacVictoryRoadCave1F"):
        ("TRAINER_UNOVA_HEX_MANIAC_VICTORY_ROAD_INT", "HexManiacVictoryRoadCave1FSeenText", "HexManiacVictoryRoadCave1FBeatenText", 1),
    ("VictoryRoadCave1F", "TrainerPsychicFVictoryRoadCave1F"):
        ("TRAINER_UNOVA_PSYCHICF_VICTORY_ROAD_INT", "PsychicFVictoryRoadCave1FSeenText", "PsychicFVictoryRoadCave1FBeatenText", 1),
    ("VictoryRoadCave1F", "TrainerPsychicMVictoryRoadCave1F"):
        ("TRAINER_UNOVA_PSYCHICM_VICTORY_ROAD_INT", "PsychicMVictoryRoadCave1FSeenText", "PsychicMVictoryRoadCave1FBeatenText", 2),
    ("VictoryRoadCave1F", "TrainerVeteranFVictoryRoadCave1F"):
        ("TRAINER_UNOVA_VETERANF_VICTORY_ROAD_INT_1", "VeteranFVictoryRoadCave1FSeenText", "VeteranFVictoryRoadCave1FBeatenText", 2),
    ("VictoryRoadCave1F", "TrainerVeteranMVictoryRoadCave1F"):
        ("TRAINER_UNOVA_VETERANM_VICTORY_ROAD_INT_1", "VeteranMVictoryRoadCave1FSeenText", "VeteranMVictoryRoadCave1FBeatenText", 2),
    ("VictoryRoadCave2F", "TrainerAceTrainerFVictoryRoadCave2F"):
        ("TRAINER_UNOVA_ACE_TRAINERF_VICTORY_ROAD_INT_1", "AceTrainerFVictoryRoadCave2FSeenText", "AceTrainerFVictoryRoadCave2FBeatenText", 2),
    ("VictoryRoadCave2F", "TrainerAceTrainerMVictoryRoadCave2F"):
        ("TRAINER_UNOVA_ACE_TRAINERM_VICTORY_ROAD_INT_2", "AceTrainerMVictoryRoadCave2FSeenText", "AceTrainerMVictoryRoadCave2FBeatenText", 2),
    ("VictoryRoadCave2F", "TrainerBackpackerMVictoryRoadCave2F"):
        ("TRAINER_UNOVA_BACKPACKERM_VICTORY_ROAD_INT", "BackpackerMVictoryRoadCave2FSeenText", "BackpackerMVictoryRoadCave2FBeatenText", 2),
    ("VictoryRoadCave2F", "TrainerPkmnRangerFVictoryRoadCave2F"):
        ("TRAINER_UNOVA_PKMN_RANGERF_VICTORY_ROAD_INT", "PkmnRangerFVictoryRoadCave2FSeenText", "PkmnRangerFVictoryRoadCave2FBeatenText", 1),
    ("VictoryRoadCave2F", "TrainerPkmnRangerMVictoryRoadCave2F"):
        ("TRAINER_UNOVA_PKMN_RANGERM_VICTORY_ROAD_INT", "PkmnRangerMVictoryRoadCave2FSeenText", "PkmnRangerMVictoryRoadCave2FBeatenText", 1),
    ("VictoryRoadCave2F", "TrainerVeteranMVictoryRoadCave2F"):
        ("TRAINER_UNOVA_VETERANM_VICTORY_ROAD_INT_2", "VeteranMVictoryRoadCave2FSeenText", "VeteranMVictoryRoadCave2FBeatenText", 2),
    ("VictoryRoadCave3F", "TrainerVeteranFVictoryRoadCave3F"):
        ("TRAINER_UNOVA_VETERANF_VICTORY_ROAD_INT_2", "VeteranFVictoryRoadCave3FSeenText", "VeteranFVictoryRoadCave3FBeatenText", 2),
    ("VictoryRoadGrove", "TrainerAceTrainerFVictoryRoadGrove"):
        ("TRAINER_UNOVA_ACE_TRAINERF_VICTORY_ROAD_EXT_1", "AceTrainerFVictoryRoadGroveSeenText", "AceTrainerFVictoryRoadGroveBeatenText", 2),
    ("VictoryRoadGrove", "TrainerAceTrainerMVictoryRoadGrove"):
        ("TRAINER_UNOVA_ACE_TRAINERM_VICTORY_ROAD_EXT_2", "AceTrainerMVictoryRoadGroveSeenText", "AceTrainerMVictoryRoadGroveBeatenText", 2),
    ("VictoryRoadOutdoor1F", "TrainerBackpackerFVictoryRoadOutdoor1F"):
        ("TRAINER_UNOVA_BACKPACKERF_VICTORY_ROAD_EXT", "BackpackerFVictoryRoadOutdoor1FSeenText", "BackpackerFVictoryRoadOutdoor1FBeatenText", 1),
    ("VictoryRoadOutdoor1F", "TrainerNurseVictoryRoadOutdoor1F"):
        ("TRAINER_UNOVA_NURSE_VICTORY_ROAD", "VictoryRoadNurseIntroText", "VictoryRoadNurseWinText", 0),
    ("VictoryRoadOutdoor1F", "TrainerVeteranFVictoryRoadOutdoor1F"):
        ("TRAINER_UNOVA_VETERANF_VICTORY_ROAD_EXT_1", "VeteranFVictoryRoadOutdoor1FSeenText", "VeteranFVictoryRoadOutdoor1FBeatenText", 2),
    ("VictoryRoadOutdoor1F", "TrainerVeteranMVictoryRoadOutdoor1F"):
        ("TRAINER_UNOVA_VETERANM_VICTORY_ROAD_EXT_1", "VeteranMVictoryRoadOutdoor1FSeenText", "VeteranMVictoryRoadOutdoor1FBeatenText", 1),
    ("VictoryRoadOutdoor2F", "TrainerAceTrainerFVictoryRoadOutdoor2F"):
        ("TRAINER_UNOVA_ACE_TRAINERF_VICTORY_ROAD_EXT_2", "AceTrainerFVictoryRoadOutdoor2FSeenText", "AceTrainerFVictoryRoadOutdoor2FBeatenText", 2),
    ("VictoryRoadOutdoor2F", "TrainerAceTrainerMVictoryRoadOutdoor2F"):
        ("TRAINER_UNOVA_ACE_TRAINERM_VICTORY_ROAD_EXT_1", "AceTrainerMVictoryRoadOutdoor2FSeenText", "AceTrainerMVictoryRoadOutdoor2FBeatenText", 2),
    ("VictoryRoadOutdoor2F", "TrainerBattleGirlVictoryRoadOutdoor2F"):
        ("TRAINER_UNOVA_BATTLE_GIRL_VICTORY_ROAD_EXT", "BattleGirlVictoryRoadOutdoor2FSeenText", "BattleGirlVictoryRoadOutdoor2FBeatenText", 1),
    ("VictoryRoadOutdoor2F", "TrainerBlackbeltVictoryRoadOutdoor2F"):
        ("TRAINER_UNOVA_BLACKBELT_VICTORY_ROAD_EXT", "BlackbeltVictoryRoadOutdoor2FSeenText", "BlackbeltVictoryRoadOutdoor2FBeatenText", 1),
    ("VictoryRoadOutdoor2F", "TrainerScientistFVictoryRoadOutdoor2F"):
        ("TRAINER_UNOVA_SCIENTISTF_VICTORY_ROAD_EXT", "ScientistFVictoryRoadOutdoor2FSeenText", "ScientistFVictoryRoadOutdoor2FBeatenText", 1),
    ("VictoryRoadOutdoor2F", "TrainerScientistMVictoryRoadOutdoor2F"):
        ("TRAINER_UNOVA_SCIENTISTM_VICTORY_ROAD_EXT", "ScientistMVictoryRoadOutdoor2FSeenText", "ScientistMVictoryRoadOutdoor2FBeatenText", 2),
    ("VictoryRoadOutdoor2F", "TrainerVeteranFVictoryRoadOutdoor2F"):
        ("TRAINER_UNOVA_VETERANF_VICTORY_ROAD_EXT_2", "VeteranFVictoryRoadOutdoor2FSeenText", "VeteranFVictoryRoadOutdoor2FBeatenText", 2),
    ("VictoryRoadOutdoor2F", "TrainerVeteranMVictoryRoadOutdoor2F"):
        ("TRAINER_UNOVA_VETERANM_VICTORY_ROAD_EXT_2", "VeteranMVictoryRoadOutdoor2FSeenText", "VeteranMVictoryRoadOutdoor2FBeatenText", 1),
    ("VillageBridge", "TrainerHoopster1VillageBridge"):
        ("TRAINER_UNOVA_HOOPSTER_VILLAGE_BRIDGE_1", "Hoopster1VillageBridgeSeenText", "Hoopster1VillageBridgeBeatenText", 3),
    ("VillageBridge", "TrainerHoopster2VillageBridge"):
        ("TRAINER_UNOVA_HOOPSTER_VILLAGE_BRIDGE_2", "Hoopster2VillageBridgeSeenText", "Hoopster2VillageBridgeBeatenText", 2),
    ("VillageBridge", "TrainerLinebackerVillageBridge"):
        ("TRAINER_UNOVA_LINEBACKER_VILLAGE_BRIDGE", "LinebackerVillageBridgeSeenText", "LinebackerVillageBridgeBeatenText", 3),
    ("VillageBridge", "TrainerMusicianVillageBridge"):
        ("TRAINER_UNOVA_MUSICIAN_VILLAGE_BRIDGE", "MusicianVillageBridgeSeenText", "MusicianVillageBridgeBeatenText", 3),
    ("VillageBridge", "TrainerSmasher1VillageBridge"):
        ("TRAINER_UNOVA_SMASHER_VILLAGE_BRIDGE_1", "Smasher1VillageBridgeSeenText", "Smasher1VillageBridgeBeatenText", 3),
    ("VillageBridge", "TrainerSmasher2VillageBridge"):
        ("TRAINER_UNOVA_SMASHER_VILLAGE_BRIDGE_2", "Smasher2VillageBridgeSeenText", "Smasher2VillageBridgeBeatenText", 2),
    ("VirbankComplexB1F", "TrainerScientistFVirbankComplexB1F"):
        ("TRAINER_UNOVA_SCIENTISTF_VIRBANK_COMPLEX_1", "ScientistFVirbankComplexB1FSeenText", "ScientistFVirbankComplexB1FBeatenText", 3),
    ("VirbankComplexB2F", "TrainerGruntFVirbankComplexB2F"):
        ("TRAINER_UNOVA_GRUNTF_VIRBANK_COMPLEX_2", "GruntFVirbankComplexB2FSeenText", "GruntFVirbankComplexB2FBeatenText", 2),
    ("VirbankComplexB2F", "TrainerGruntMVirbankComplexB2F"):
        ("TRAINER_UNOVA_GRUNTM_VIRBANK_COMPLEX_3", "GruntMVirbankComplexB2FSeenText", "GruntMVirbankComplexB2FBeatenText", 2),
    ("VirbankComplexB2F", "TrainerScientistFVirbankComplexB2F"):
        ("TRAINER_UNOVA_SCIENTISTF_VIRBANK_COMPLEX_2", "ScientistFVirbankComplexB2FSeenText", "ScientistFVirbankComplexB2FBeatenText", 3),
    ("VirbankComplexB2F", "TrainerScientistMVirbankComplexB2F"):
        ("TRAINER_UNOVA_SCIENTISTM_VIRBANK_COMPLEX", "ScientistMVirbankComplexB2FSeenText", "ScientistMVirbankComplexB2FBeatenText", 2),
    ("VirbankComplexOutside", "TrainerGruntFVirbankComplexOutside"):
        ("TRAINER_UNOVA_GRUNTF_VIRBANK_COMPLEX_1", "GruntFVirbankComplexOutsideSeenText", "GruntFVirbankComplexOutsideBeatenText", 4),
    ("VirbankComplexOutside", "TrainerGruntM1VirbankComplexOutside"):
        ("TRAINER_UNOVA_GRUNTM_VIRBANK_COMPLEX_1", "GruntM1VirbankComplexOutsideSeenText", "GruntM1VirbankComplexOutsideBeatenText", 2),
    ("VirbankComplexOutside", "TrainerGruntM2VirbankComplexOutside"):
        ("TRAINER_UNOVA_GRUNTM_VIRBANK_COMPLEX_2", "GruntM2VirbankComplexOutsideSeenText", "GruntM2VirbankComplexOutsideBeatenText", 3),
    ("VirbankGym", "TrainerGuitaristVirbankGym1"):
        ("TRAINER_UNOVA_GUITARIST_VIRBANK_GYM_1", "GuitaristVirbankGym1SeenText", "GuitaristVirbankGym1BeatenText", 1),
    ("VirbankGym", "TrainerGuitaristVirbankGym2"):
        ("TRAINER_UNOVA_GUITARIST_VIRBANK_GYM_2", "GuitaristVirbankGym2SeenText", "GuitaristVirbankGym2BeatenText", 2),
    ("VirbankGym", "TrainerMusicianVirbankGym1"):
        ("TRAINER_UNOVA_MUSICIAN_VIRBANK_GYM_1", "MusicianVirbankGym1SeenText", "MusicianVirbankGym1BeatenText", 3),
    ("VirbankGym", "TrainerMusicianVirbankGym2"):
        ("TRAINER_UNOVA_MUSICIAN_VIRBANK_GYM_2", "MusicianVirbankGym2SeenText", "MusicianVirbankGym2BeatenText", 2),
    ("WellspringCave1F", "TrainerBlackbeltWellspring1F"):
        ("TRAINER_UNOVA_BLACKBELT_WELLSPRING_1", "BlackbeltWellspring1FSeenText", "BlackbeltWellspring1FBeatenText", 2),
    ("WellspringCaveB1F", "TrainerBattleGirlWellspringB1F"):
        ("TRAINER_UNOVA_BATTLE_GIRL_WELLSPRING", "BattleGirlWellspringB1FSeenText", "BattleGirlWellspringB1FBeatenText", 4),
    ("WellspringCaveB1F", "TrainerBlackbeltWellspringB1F"):
        ("TRAINER_UNOVA_BLACKBELT_WELLSPRING_2", "BlackbeltWellspringB1FSeenText", "BlackbeltWellspringB1FBeatenText", 2),
    ("WellspringCaveB1F", "TrainerHikerWellspringB1F"):
        ("TRAINER_UNOVA_HIKER_WELLSPRING", "HikerWellspringB1FSeenText", "HikerWellspringB1FBeatenText", 1),
}
# <<< TREINADORES DE UNOVA (gerado) <<<

def script_lider(nome, i, cfg):
    """`trainerbattle_single` e nada mais: o motor ja guarda sozinho a flag de
    'este treinador ja foi derrotado' (uma por vaga de treinador, dentro de
    flags[]), entao falar com o chefe de novo cai direto no `end` sem rebater e
    sem gastar flag nova.

    Serve tanto a LIDERES quanto a TREINADORES; a unica diferenca e o quinto
    campo, a insignia. Quando ele existe, a batalha passa a usar a forma de 4
    argumentos do macro (TRAINER_BATTLE_CONTINUE_SCRIPT), que continua no script
    dado APOS a vitoria; esse script acende a flag, toca a fanfarra do jogo e
    solta o jogador. Sem o quinto campo o script e o de sempre e nao muda nada.
    """
    treinador, visto, perde = cfg[0], cfg[1], cfg[2]
    insignia = cfg[4] if len(cfg) > 4 else None
    rot = f"{nome}_EventScript_Lider{i}"
    if not insignia:
        return rot, (f"{rot}::\n\ttrainerbattle_single {treinador}, "
                     f"{nome}_Text_{visto}, {nome}_Text_{perde}\n\tend\n")
    pos = f"{nome}_EventScript_Insignia{i}"
    return rot, (f"{rot}::\n\ttrainerbattle_single {treinador}, "
                 f"{nome}_Text_{visto}, {nome}_Text_{perde}, {pos}\n\tend\n\n"
                 f"{pos}::\n\tsetflag {insignia}\n"
                 f"\tcall Common_EventScript_PlayGymBadgeFanfare\n"
                 f"\trelease\n\tend\n")


# A volta de barco. O BW3G nao tem porto para fora de Unova, entao o marinheiro
# do retorno e o unico conteudo que este import ACRESCENTA em vez de portar.
# Fica aqui, e nao editado a mao no map.json gerado, senao a proxima rodada do
# import apaga. Ele mora em Virbank Port, que ja e porto no original e e onde os
# quatro portos das outras regioes desembarcam (4, 6, uma casa acima da porta
# para a cidade, conferido andavel lendo o map.bin gerado).
MARINHEIRO = {
    "VirbankPort": dict(
        x=7, y=5, sprite="OBJ_EVENT_GFX_SAILOR",
        destinos=[(0, "Olivine", "MAP_OLIVINE_CITY_PORT_INSIDE", 8, 17, "Olivine City em Johto"),
                  (1, "Slateport", "MAP_SLATEPORT_CITY_HARBOR", 8, 14, "Slateport City em Hoenn"),
                  (2, "Vermilion", "MAP_VERMILION_CITY", 15, 10, "Vermilion City em Kanto"),
                  (4, "Canalave", "MAP_CANALAVE_CITY", 10, 10, "Canalave City em Sinnoh")]),
}


def script_marinheiro(nome, cfg):
    rot = f"{nome}_EventScript_Marinheiro"
    linhas = [f"{rot}::", "\tlock", "\tfaceplayer",
              f"\tmsgbox {nome}_Text_ParaOnde, MSGBOX_DEFAULT",
              "\tmultichoice 0, 0, MULTI_BOAT_DESTINATIONS, FALSE",
              "\tswitch VAR_RESULT"]
    for i, d, _, _, _, _ in cfg["destinos"]:
        linhas.append(f"\tcase {i}, {nome}_EventScript_Zarpar{d}")
    linhas += [f"\tmsgbox {nome}_Text_Volte, MSGBOX_DEFAULT", "\trelease", "\tend", ""]
    for _, d, mapa, x, y, humano in cfg["destinos"]:
        linhas += [f"{nome}_EventScript_Zarpar{d}::",
                   f"\tmsgbox {nome}_Text_Zarpar{d}, MSGBOX_DEFAULT", "\tclosemessage",
                   f"\twarpsilent {mapa}, {x}, {y}", "\trelease", "\tend", "",
                   f"{nome}_Text_Zarpar{d}:",
                   f'\t.string "Zarpando para {humano}!$"', ""]
    linhas += [f"{nome}_Text_ParaOnde:",
               '\t.string "Bem-vindo ao Porto de Virbank City em Unova!\\n'
               'Para onde gostaria de navegar?$"', "",
               f"{nome}_Text_Volte:",
               '\t.string "Volte quando quiser zarpar!$"', ""]
    return rot, "\n".join(linhas) + "\n"


def jumpstd_de(asm, rotulo):
    """Se o script do gen 2 for um `jumpstd X`, devolve X.

    Vale a pena olhar isto porque dois `jumpstd` sao funcionalidade de verdade e
    nao texto: `pokecenternurse` (18 ocorrencias) e `scalingmart` (19). Sem eles a
    regiao inteira ficaria sem cura e sem loja, e o jogador teria que voltar de
    barco para outra regiao para curar.
    """
    m = re.search(rf"^{rotulo}:+\s*$", asm, re.M)
    if not m:
        return None
    for ln in asm[m.end():].splitlines()[:8]:
        if re.match(r"^\w+:", ln):
            break
        m2 = re.match(r"\s*jumpstd\s+(\w+)", ln)
        if m2:
            return m2.group(1)
    return None


# Loja provisoria de Unova. O BW3G usa `scalingmart`, que escala o estoque pelo
# numero de insignias e nao existe aqui; esta lista e o basico de sempre, e a
# escolha de estoque por cidade e acabamento, nao geometria.
LOJA = ["ITEM_POKE_BALL", "ITEM_POTION", "ITEM_SUPER_POTION", "ITEM_ANTIDOTE",
        "ITEM_PARALYZE_HEAL", "ITEM_AWAKENING", "ITEM_BURN_HEAL", "ITEM_ICE_HEAL",
        "ITEM_REPEL", "ITEM_ESCAPE_ROPE"]


def resolve_texto(asm, rotulo, textos, visto=None):
    """Do rotulo de script do gen 2 ate o primeiro texto que ele mostra.

    Cobre os tres formatos que aparecem no BW3G: `jumptextfaceplayer X`,
    `writetext X` / `farwritetext X`, e o macro `trainer G, N, EVENTO, VistoText,
    ...` (que e o texto que o treinador diz ao ser visto). Se nada casar, devolve
    None e o objeto vira NPC mudo.
    """
    visto = visto or set()
    if rotulo in visto or rotulo in ("0", "-1", "NULL"):
        return None
    visto.add(rotulo)
    if rotulo in textos:
        return rotulo
    m = re.search(rf"^{rotulo}:+\s*$", asm, re.M)
    if not m:
        return None
    corpo = asm[m.end():]
    for ln in corpo.splitlines()[:40]:
        if re.match(r"^\w+:", ln):
            break
        m2 = re.match(r"\s*(?:jumptextfaceplayer|jumptext|farjumptext|writetext|"
                      r"farwritetext)\s+(\w+)", ln)
        if m2:
            return m2.group(1) if m2.group(1) in textos else None
        m2 = re.match(r"\s*trainer\s+\w+,\s*\w+,\s*\w+,\s*(\w+)", ln)
        if m2:
            return m2.group(1) if m2.group(1) in textos else None
        m2 = re.match(r"\s*(?:sjump|jump|callasm|jumpstd)\s+(\w+)", ln)
        if m2:
            return resolve_texto(asm, m2.group(1), textos, visto)
    return None


# --------------------------------------------------------------------------


def carrega_tabelas():
    """Tabelas produzidas pelos agentes paralelos, com queda para o basico."""
    try:
        import tabela_sprites_bw3g as ts
        sprite, movimento, musica = ts.SPRITE, ts.MOVIMENTO, ts.MUSICA
    except Exception as e:                      # noqa: BLE001
        print(f"  aviso: tabela de sprites ausente ({e}); usando o generico")
        sprite, movimento, musica = {}, {}, {}
    try:
        import tabela_tilesets_bw3g as tt
        destino, paleta = tt.DESTINO, tt.PALETA
    except Exception as e:                      # noqa: BLE001
        print(f"  aviso: tabela de tilesets ausente ({e}); usando a do demake")
        destino, paleta = {}, {}
    return sprite, movimento, musica, destino, paleta


def main(gravar):
    grupos = le_grupos()
    blocos = le_blocos_compartilhados()
    atrib = le_conexoes()
    idx_asm = indice_asm()
    flag_item = [0]   # contador da faixa reservada, ver flag_de_item
    sprite, movimento, musica, destino, paleta = carrega_tabelas()

    # const do BW3G -> nome do mapa aqui. Precisa estar pronto ANTES de gerar,
    # porque warp aponta para mapa de outro grupo.
    nome_de = {}
    for _, mapas in grupos:
        for camel, const, *_ in mapas:
            nome_de[const] = PREFIXO + camel

    stats = dict(mapas=0, blocos_faltando=0, ajuste_tamanho=0, warps=0, placas=0,
                 objetos=0, textos=0, itemball=0, item_escondido=0, coord=0,
                 conexoes=0, sem_texto=0, enfermeira=0, loja=0, marinheiro=0, item_sem_flag=0,
                 mobilia=0, lider=0, treinador=0)
    saida_layouts, saida_grupos, saida_incs = [], [], []

    for gnome, mapas in grupos:
        chave = "gMapGroup_Unova" + gnome[len("MapGroup_"):]
        lista = []
        for camel, const, w, h, tset, amb, landmark, mus in mapas:
            arq = blocos.get(camel)
            if not arq or not os.path.exists(arq):
                stats["blocos_faltando"] += 1
                continue
            crus = open(arq, "rb").read()
            if len(crus) != w * h:
                stats["ajuste_tamanho"] += 1
                crus = (crus + bytes(w * h))[:w * h]   # falta vira bloco 0
            # o mesmo alias da colisao vale para o tileset de destino: sem ele
            # o `elite_four_room_2` cairia num par de tileset e numa paleta de
            # metatile que nao combinam, e a sala sairia com id de outro tileset
            alvo = COLISAO_ALIAS.get(tset, tset)
            prim, sec, pal = destino.get(alvo, ("gTileset_GeneralSinnoh",
                                                "gTileset_PetalburgSinnoh",
                                                "exterior_sinnoh"))
            tabela = dg.colisao_do_tileset(COLISAO_ALIAS.get(tset, tset) + "_collision.asm")
            lm, hm, dados = dg.converte_blocos(crus, w, h, tabela,
                                               paleta[pal])

            nome = PREFIXO + camel
            mid = PREFIXO_ID + const
            lay = PREFIXO_LAYOUT + const
            tipo, aberto = AMBIENTE.get(amb, ("MAP_TYPE_INDOOR", False))

            asm_p = idx_asm.get(camel) or f"{BW3G}/maps/{camel}.asm"
            asm = open(asm_p, encoding="utf-8", errors="replace").read() if os.path.exists(asm_p) else ""
            textos = le_textos(asm)
            ev = le_eventos(asm, camel)

            mapa = {
                "id": mid, "name": nome, "layout": lay,
                "music": musica.get(mus, "MUS_ROUTE118"),
                "region_map_section": "MAPSEC_UNOVA_" + landmark,
                "requires_flash": False, "weather": "WEATHER_NONE" if not aberto else "WEATHER_SUNNY",
                "map_type": tipo, "allow_cycling": aberto, "allow_escaping": False,
                "allow_running": True, "show_map_name": aberto,
                "battle_scene": "MAP_BATTLE_SCENE_NORMAL",
                "connections": [], "object_events": [], "warp_events": [],
                "coord_events": [], "bg_events": [],
            }

            for d, alvo, off in atrib.get(camel, {}).get("con", []):
                if alvo in nome_de:
                    # offset do gen 2 e em BLOCOS; o do gen 3 e em metatiles, e a
                    # convencao de sinal e a mesma (positivo desloca o mapa vizinho
                    # para a direita/baixo), conferido nos pares reciprocos de
                    # attributes.asm, que sempre vem com sinal trocado.
                    mapa["connections"].append({"map": PREFIXO_ID + alvo,
                                                "offset": off * 2,
                                                "direction": LADO[d]})
                    stats["conexoes"] += 1

            for x, y, alvo, wid in ev["warp"]:
                if alvo not in nome_de:
                    continue
                # gen 2 numera warp a partir de 1, gen 3 a partir de 0
                mapa["warp_events"].append({"x": x, "y": y, "elevation": 0,
                                            "dest_map": PREFIXO_ID + alvo,
                                            "dest_warp_id": str(max(0, wid - 1))})
                stats["warps"] += 1

            usados, corpo = {}, []
            for i, (x, y, kind, script) in enumerate(ev["bg"]):
                if kind == "ITEM":
                    it = item_do_script(asm, script)
                    if it and flag_item[0] < NUM_ITEMS_UNOVA:
                        mapa["bg_events"].append({
                            "type": "hidden_item", "x": x, "y": y, "elevation": 3,
                            "item": it[0], "flag": flag_de_item(flag_item),
                            "quantity": it[1], "underfoot": False})
                        stats["item_escondido"] += 1
                    else:
                        stats["item_sem_flag"] += 1
                    continue
                t = resolve_texto(asm, script, textos)
                if not t:
                    rot = STD_PLACA.get(jumpstd_de(asm, script))
                    if rot:
                        mapa["bg_events"].append({
                            "type": "sign", "x": x, "y": y, "elevation": 0,
                            "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
                            "script": rot})
                        stats["mobilia"] += 1
                    else:
                        stats["sem_texto"] += 1
                    continue
                usados[t] = textos[t]
                rot = f"{nome}_EventScript_Placa{i}"
                corpo.append(f"{rot}::\n\tmsgbox {nome}_Text_{t}, MSGBOX_SIGN\n\tend\n")
                mapa["bg_events"].append({"type": "sign", "x": x, "y": y, "elevation": 0,
                                          "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
                                          "script": rot})
                stats["placas"] += 1

            for i, o in enumerate(ev["obj"]):
                if o["tipo"] == "ITEMBALL":
                    it = item_do_script(asm, o["script"])
                    if it and flag_item[0] < NUM_ITEMS_UNOVA:
                        # o motor le o item de `trainer_sight_or_berry_tree_id` e a
                        # quantidade de `movement_range_x` (src/item_ball.c), e o
                        # `removeobject` do Std_FindItem acende a flag do objeto,
                        # que e o que impede a bola de renascer a cada entrada
                        mapa["object_events"].append({
                            "graphics_id": "OBJ_EVENT_GFX_ITEM_BALL",
                            "x": o["x"], "y": o["y"], "elevation": 3,
                            "movement_type": "MOVEMENT_TYPE_LOOK_AROUND",
                            "movement_range_x": it[1], "movement_range_y": 1,
                            "trainer_type": "TRAINER_TYPE_NONE",
                            "trainer_sight_or_berry_tree_id": it[0],
                            "script": "Common_EventScript_FindItem",
                            "flag": flag_de_item(flag_item)})
                        stats["itemball"] += 1
                    else:
                        stats["item_sem_flag"] += 1
                    continue
                cfg = LIDERES.get((camel, o["script"] if o["script"] not in ("0", "-1")
                                          else o["sprite"])) \
                    or TREINADORES.get((camel, o["script"]))
                if cfg:
                    for t in (cfg[1], cfg[2]):
                        usados[t] = textos[t]
                    rot, txt = script_lider(nome, i, cfg)
                    corpo.append(txt)
                    mapa["object_events"].append({
                        "graphics_id": sprite.get(o["sprite"], "OBJ_EVENT_GFX_BOY_1"),
                        "x": o["x"], "y": o["y"], "elevation": 3,
                        "movement_type": movimento.get(o["mov"], "MOVEMENT_TYPE_FACE_DOWN"),
                        "movement_range_x": 0, "movement_range_y": 0,
                        "trainer_type": "TRAINER_TYPE_NORMAL",
                        "trainer_sight_or_berry_tree_id": str(cfg[3]),
                        "script": rot, "flag": SEM_FLAG})
                    stats["lider" if cfg[0].startswith(
                        ("TRAINER_UNOVA_LEADER", "TRAINER_UNOVA_E4")) else "treinador"] += 1
                    continue
                std = jumpstd_de(asm, o["script"])
                if std in STD_MOBILIA:
                    gfx, rot = STD_MOBILIA[std]
                    mapa["object_events"].append({
                        "graphics_id": gfx, "x": o["x"], "y": o["y"], "elevation": 3,
                        "movement_type": "MOVEMENT_TYPE_FACE_DOWN",
                        "movement_range_x": 0, "movement_range_y": 0,
                        "trainer_type": "TRAINER_TYPE_NONE",
                        "trainer_sight_or_berry_tree_id": "0",
                        "script": rot, "flag": SEM_FLAG})
                    stats["mobilia"] += 1
                    continue
                t = resolve_texto(asm, o["script"], textos)
                rot = "0"
                if std == "pokecenternurse":
                    rot = f"{nome}_EventScript_Npc{i}"
                    # LOCALID e o indice do objeto + 1; este e o primeiro objeto
                    # a entrar na lista, entao vale len(...) + 1 no momento certo
                    corpo.append(f"{rot}::\n\tsetvar VAR_0x800B, "
                                 f"{len(mapa['object_events']) + 1}\n"
                                 f"\tcall Common_EventScript_PkmnCenterNurse\n"
                                 f"\twaitmessage\n\twaitbuttonpress\n\trelease\n\tend\n")
                    stats["enfermeira"] += 1
                elif std == "scalingmart":
                    rot = f"{nome}_EventScript_Npc{i}"
                    corpo.append(f"{rot}::\n\tlock\n\tfaceplayer\n"
                                 f"\tmessage gText_HowMayIServeYou\n\twaitmessage\n"
                                 f"\tpokemart {nome}_Loja{i}\n"
                                 f"\tmsgbox gText_PleaseComeAgain, MSGBOX_DEFAULT\n"
                                 f"\trelease\n\tend\n\n\t.align 2\n{nome}_Loja{i}:\n"
                                 + "".join(f"\t.2byte {x}\n" for x in LOJA)
                                 + "\tpokemartlistend\n")
                    stats["loja"] += 1
                elif t:
                    usados[t] = textos[t]
                    rot = f"{nome}_EventScript_Npc{i}"
                    corpo.append(f"{rot}::\n\tmsgbox {nome}_Text_{t}, MSGBOX_NPC\n\tend\n")
                else:
                    stats["sem_texto"] += 1
                mapa["object_events"].append({
                    "graphics_id": sprite.get(o["sprite"], "OBJ_EVENT_GFX_BOY_1"),
                    "x": o["x"], "y": o["y"], "elevation": 3,
                    "movement_type": movimento.get(o["mov"], "MOVEMENT_TYPE_FACE_DOWN"),
                    "movement_range_x": o["rx"], "movement_range_y": o["ry"],
                    "trainer_type": "TRAINER_TYPE_NONE",
                    "trainer_sight_or_berry_tree_id": "0",
                    "script": rot, "flag": SEM_FLAG})
                stats["objetos"] += 1

            if camel in MARINHEIRO:
                cfg = MARINHEIRO[camel]
                rot, txt = script_marinheiro(nome, cfg)
                corpo.append(txt)
                mapa["object_events"].append({
                    "graphics_id": cfg["sprite"], "x": cfg["x"], "y": cfg["y"],
                    "elevation": 3, "movement_type": "MOVEMENT_TYPE_FACE_DOWN",
                    "movement_range_x": 0, "movement_range_y": 0,
                    "trainer_type": "TRAINER_TYPE_NONE",
                    "trainer_sight_or_berry_tree_id": "0",
                    "script": rot, "flag": SEM_FLAG})
                stats["marinheiro"] += 1

            stats["coord"] += len(ev["coord"])
            stats["textos"] += len(usados)

            if gravar:
                dl = f"{RAIZ}/data/layouts/{nome}"
                os.makedirs(dl, exist_ok=True)
                open(f"{dl}/map.bin", "wb").write(dados)
                # borda: o bloco declarado em map_attributes, pelo mesmo caminho
                bb = atrib.get(camel, {}).get("borda", 0)
                _, _, bd = dg.converte_blocos(bytes([bb]), 1, 1, tabela,
                                              paleta[pal])
                open(f"{dl}/border.bin", "wb").write(bd)

                dm = f"{RAIZ}/data/maps/{nome}"
                os.makedirs(dm, exist_ok=True)
                json.dump(mapa, open(f"{dm}/map.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
                with open(f"{dm}/scripts.inc", "w", encoding="utf-8") as f:
                    f.write(f"@ {camel} do BW3G (Azure_Keys). Gerado por "
                            f"dev_scripts/importa_unova.py; nao editar a mao.\n\n")
                    f.write(f"{nome}_MapScripts::\n\t.byte 0\n\n")
                    f.write("\n".join(corpo))
                    f.write("\n")
                    for t, partes in usados.items():
                        f.write("\n" + emite_texto(f"{nome}_Text_{t}", partes))

            saida_layouts.append({
                "id": lay, "name": nome + "_Layout", "width": lm, "height": hm,
                "primary_tileset": prim, "secondary_tileset": sec,
                "border_filepath": f"data/layouts/{nome}/border.bin",
                "blockdata_filepath": f"data/layouts/{nome}/map.bin",
                "layout_version": "emerald"})
            lista.append(nome)
            saida_incs.append(f'\t.include "data/maps/{nome}/scripts.inc"')
            stats["mapas"] += 1
        if lista:
            saida_grupos.append((chave, lista))

    print(json.dumps(stats, indent=2, ensure_ascii=False))
    print(f"grupos novos: {len(saida_grupos)}")
    if not gravar:
        return

    registra(saida_layouts, saida_grupos, saida_incs, grupos)
    # ate o ponto fixo: apagar um warp renumera os que vem depois, e quem
    # apontava para o indice antigo passa a estourar. Uma passada so nao basta.
    ta = tb = 0
    for _ in range(10):
        a, b = saneia_warps()
        ta, tb = ta + a, tb + b
        if not a and not b:
            break
    print(f'warps de elevador apagados: {ta}; indices presos no ultimo: {tb}')


def saneia_warps():
    """Passe final sobre os map.json ja gravados: nenhum warp pode prender.

    Sobram dois defeitos que vem da propria fonte e nao da conversao:
    - **Elevador.** No gen 2 o elevador nao tem warp de volta; o destino e
      escolhido em tempo de execucao pelo script do painel. Convertido ao pe da
      letra, o jogador entra e nunca sai. Warp para mapa sem nenhum warp e
      APAGADO, entao o elevador fica inacessivel em vez de virar prisao.
    - **Indice fora do alcance.** O BW3G tem warp apontando para o 6o warp de um
      mapa que so tem 5 (sala do Cable Club). Fica preso no ultimo valido.
    Devolve (apagados, presos).
    """
    mapas = {}
    for d in sorted(os.listdir(f"{RAIZ}/data/maps")):
        if not d.startswith(PREFIXO):
            continue
        p = f"{RAIZ}/data/maps/{d}/map.json"
        mapas[json.load(open(p))["id"]] = p
    quantos = {i: len(json.load(open(p))["warp_events"]) for i, p in mapas.items()}
    apagados = presos = 0
    for i, p in mapas.items():
        m = json.load(open(p))
        novos = []
        for w in m["warp_events"]:
            n = quantos.get(w["dest_map"])
            if n is None:          # destino fora de Unova: nao mexe
                novos.append(w)
                continue
            if n == 0:
                apagados += 1
                continue
            if int(w["dest_warp_id"]) >= n:
                w["dest_warp_id"] = str(n - 1)
                presos += 1
            novos.append(w)
        if len(novos) != len(m["warp_events"]) or presos:
            m["warp_events"] = novos
            json.dump(m, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    return apagados, presos


def registra(layouts, grupos_novos, incs, grupos_bw):
    # layouts.json: so acrescenta
    p = f"{RAIZ}/data/layouts/layouts.json"
    d = json.load(open(p))
    # ATUALIZA no lugar quem ja existe, em vez de pular: rodar o import de novo
    # com a tabela de tileset corrigida tem que trocar o tileset do layout, e a
    # ordem de `layouts` nao importa para a save (o que importa e a de map_groups).
    pos = {l["id"]: i for i, l in enumerate(d["layouts"])}
    for l in layouts:
        if l["id"] in pos:
            d["layouts"][pos[l["id"]]] = l
        else:
            d["layouts"].append(l)
    json.dump(d, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    # map_groups.json: grupo novo SO no fim de group_order (a save guarda indice)
    p = f"{RAIZ}/data/maps/map_groups.json"
    d = json.load(open(p))
    for chave, lista in grupos_novos:
        if chave in d:
            continue
        d[chave] = lista
        d["group_order"].append(chave)
    json.dump(d, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    # event_scripts.s: acrescenta os includes no fim
    p = f"{RAIZ}/data/event_scripts.s"
    s = open(p, encoding="utf-8").read()
    novos = [i for i in incs if i not in s]
    if novos:
        s = s.rstrip("\n") + "\n\n\t@ Mapas de Unova (BW3G, de Azure_Keys)\n" + "\n".join(novos) + "\n"
        open(p, "w", encoding="utf-8").write(s)

    # MAPSEC: tres reais no fim da json, e um apelido por landmark no TEMPLATE
    # versionado (o .h e gerado e some no build)
    p = f"{RAIZ}/src/data/region_map/region_map_sections.json"
    d = json.load(open(p))
    tem = {m["id"] for m in d["map_sections"]}
    for r in ("WEST", "EAST", "NORTH"):
        i = f"MAPSEC_UNOVA_{r}"
        if i not in tem:
            d["map_sections"].append({"id": i, "name": f"UNOVA {r}", "x": 0, "y": 0,
                                      "width": 1, "height": 1})
    json.dump(d, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    landmarks = sorted({m[6] for _, ms in grupos_bw for m in ms})
    p = f"{RAIZ}/src/data/region_map/region_map_sections.constants.json.txt"
    s = open(p, encoding="utf-8").read()
    if "Apelidos de MAPSEC de Unova" not in s:
        bloco = ["", "// Apelidos de MAPSEC de Unova. Mesma razao dos de Johto e Sinnoh acima:",
                 "// MAPSEC e u8 e nao cabe uma por cidade, entao a regiao inteira mora em tres",
                 "// e cada landmark do BW3G e apelido de um grupo. Trocar de grupo aqui e uma",
                 "// linha, sem mexer em nenhum map.json."]
        for lm in landmarks:
            reg = next((r for r, v in REGIAO.items() if lm in v), "WEST")
            bloco.append(f"#define MAPSEC_UNOVA_{lm} MAPSEC_UNOVA_{reg}")
        alvo = "#endif // GUARD_CONSTANTS_REGION_MAP_SECTIONS_H"
        s = s.replace(alvo, "\n".join(bloco) + "\n\n" + alvo)
        open(p, "w", encoding="utf-8").write(s)
    print("registrado")


if __name__ == "__main__":
    if "--gravar" in sys.argv:
        main(True)
    else:
        main(False)
