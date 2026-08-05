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
                 conexoes=0, sem_texto=0, enfermeira=0, loja=0, marinheiro=0, item_sem_flag=0, mobilia=0)
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
