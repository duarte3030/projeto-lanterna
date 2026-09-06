#!/usr/bin/env python3
"""Preenche `map_name_popup` nos map.json e gera `src/data/map_popup_names.h`.

Uso:
    python3 dev_scripts/nomes_popup.py            # escreve os map.json, o .h e o CSV
    python3 dev_scripts/nomes_popup.py --seco     # nao escreve nada, so relata
    python3 dev_scripts/nomes_popup.py --tabela   # so o .h (e o passo do Makefile)
    python3 dev_scripts/nomes_popup.py --demo     # autoteste, sai 1 se algo cair

Por que existe
--------------
MAPSEC e `u8` e divide o espaco de valores com METLOC_SPECIAL_EGG (0xFD), entao
Johto, Sinnoh, Unova e Galar NAO tem uma secao por cidade: cada lugar e apelido
de um MAPSEC de GRUPO (ver src/data/region_map/region_map_sections.constants.json.txt).
Como `GetPopUpMapName` copiava `gRegionMapEntries[mapsec].name`, o letreiro de
centenas de mapas dizia "SINNOH WEST", "UNOVA EAST" ou "GALAR SOUTH" em vez do
nome do lugar. O Gui pegou isso no playtest da ROM 2026-08-23d.

O conserto DESACOPLA o nome do letreiro do MAPSEC, sem tocar em MAPSEC nem no
"met location" do sumario do Pokemon (que continua por grupo, e isso e aceito):
cada map.json ganha o campo opcional `map_name_popup` com a string ja no formato
exibido, e `--tabela` destila o CAMPO dos 2.400 map.json numa tabela indexada
por (grupo, numero de mapa). `tools/mapjson` le o map.json por CHAVE e ignora
campo que nao conhece, entao o campo novo nao mexe no header do mapa.

A fonte da verdade da tabela e o CAMPO, nunca a derivacao: `--tabela` nao olha o
dicionario de radicais, so o que esta escrito no map.json. E por isso que editar
`map_name_popup` a mao muda o letreiro no proximo `make`, sem tocar aqui.

De onde sai o nome, nesta ordem
-------------------------------
    (a) o NOME DA PASTA, por dicionario de radicais (RADICAIS_*), que e a unica
        fonte que sobreviveu em Sinnoh (398 mapas com o MAPSEC de grupo cru) e
        em Galar (172 mapas com MAPSEC_GALAR_POSTWICK por valor padrao errado);
    (b) o APELIDO do `region_map_section`, transformado, que e a fonte boa em
        Johto e Unova, onde o demake carregou o apelido certo em cada mapa;
    (c) o que nao resolver vai para dev_scripts/qa/nomes_popup_revisao.csv e NAO
        recebe campo, caindo no comportamento antigo.

Interior herda o lugar da cidade, como no jogo original. Mapa TUMULO
(`MAPSEC_NONE`) fica fora. Kanto e Hoenn ficam fora: tem MAPSEC proprio.

O script e idempotente: rodar de novo sobre a arvore ja escrita nao muda byte.
"""
import argparse
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CAMINHO_CONSTANTES = "src/data/region_map/region_map_sections.constants.json.txt"
CAMINHO_TABELA = "src/data/map_popup_names.h"
CAMINHO_CSV = "dev_scripts/qa/nomes_popup_revisao.csv"

# Largura da caixa do letreiro, em pixel, na fonte FONT_NARROWER. E a mesma
# regua do teste "Map names fit in popup" de test/text.c, e o nome ja vem com o
# sufixo de andar ("B1F", "2F") somado antes de medir.
LARGURA_MAXIMA_PX = 80

# Espaco do nome dentro do buffer do letreiro:
# MAP_POPUP_STRING_BUFFER_LENGTH - MAP_POPUP_PREFIX_BUFFER_LENGTH, menos o EOS.
# E o mesmo buffer que test/text.c usa para medir.
CARACTERES_MAXIMOS = 27 - 6 - 1


# ---------------------------------------------------------------- largura ----

def le_charmap(raiz):
    """Mapa caractere -> byte, lido do charmap.txt do repo."""
    tabela = {}
    caminho = os.path.join(raiz, "charmap.txt")
    with open(caminho, encoding="utf-8") as arq:
        for linha in arq:
            achou = re.match(r"^'(.)'\s*=\s*([0-9A-Fa-f]{2})\s*$", linha)
            if achou:
                tabela[achou.group(1)] = int(achou.group(2), 16)
    return tabela


def le_larguras_narrower(raiz):
    """Larguras de glifo da FONT_NARROWER, lidas de src/fonts.c."""
    with open(os.path.join(raiz, "src/fonts.c"), encoding="utf-8") as arq:
        texto = arq.read()
    achou = re.search(r"gFontNarrowerLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};", texto, re.S)
    if not achou:
        raise SystemExit("nao achei gFontNarrowerLatinGlyphWidths em src/fonts.c")
    return [int(x) for x in re.findall(r"\d+", achou.group(1))]


class Regua:
    """Mede uma string na fonte do letreiro, do jeito que GetStringWidth mede."""

    def __init__(self, raiz):
        self.charmap = le_charmap(raiz)
        self.larguras = le_larguras_narrower(raiz)

    def px(self, texto):
        total = 0
        for ch in texto:
            byte = self.charmap.get(ch)
            if byte is None:
                return None
            total += self.larguras[byte]
        return total


def sufixo_de_andar(numero):
    """Reproduz MapNamePopupAppendFloorNum, para a medicao bater com o jogo."""
    if not numero:
        return ""
    if numero == 127:  # FLOOR_ROOFTOP
        return " ROOFTOP"
    if numero < 0:
        return " B%dF" % (-numero)
    return " %dF" % numero


# ------------------------------------------------------- apelidos e regiao ----

def le_apelidos(raiz):
    """Le os `#define MAPSEC_X MAPSEC_Y` e devolve (apelido -> grupo, regiao)."""
    caminho = os.path.join(raiz, CAMINHO_CONSTANTES)
    with open(caminho, encoding="utf-8") as arq:
        linhas = arq.read().splitlines()
    apelido = {}
    regiao_do_apelido = {}
    secao = "Johto"
    for linha in linhas:
        if "Sinnoh region map sections" in linha:
            secao = "Sinnoh"
        elif "Apelidos de MAPSEC de Unova" in linha:
            secao = "Unova"
        elif "Apelidos de MAPSEC de Galar" in linha:
            secao = "Galar"
        achou = re.match(r"#define\s+(MAPSEC_\w+)\s+(MAPSEC_\w+)\s*$", linha)
        if achou:
            apelido[achou.group(1)] = achou.group(2)
            regiao_do_apelido[achou.group(1)] = secao
    return apelido, regiao_do_apelido


GRUPOS_SINNOH = ("MAPSEC_SINNOH_WEST", "MAPSEC_SINNOH_EAST", "MAPSEC_SINNOH_NORTH")


def regiao_do_mapsec(mapsec, regiao_do_apelido):
    """Qual das quatro regioes sem MAPSEC proprio o mapa pertence, ou None."""
    if mapsec.startswith("MAPSEC_GALAR"):
        return "Galar"
    if mapsec.startswith("MAPSEC_UNOVA"):
        return "Unova"
    if mapsec in GRUPOS_SINNOH:
        return "Sinnoh"
    return regiao_do_apelido.get(mapsec)


# ------------------------------------------------ nome a partir do apelido ----

# Apelido cuja transformacao mecanica sairia errada ou larga demais.
APELIDO_ESPECIAL = {
    "MAPSEC_MT_SILVER": "MT. SILVER",
    "MAPSEC_MT_MORTAR": "MT. MORTAR",
    "MAPSEC_SS_AQUA": "S.S. AQUA",
    "MAPSEC_UNOVA_POKEMON_WORLD_TOURNAMENT": "WORLD TOURNAMENT",
    "MAPSEC_UNOVA_POKEMON_LEAGUE": "POKEMON LEAGUE",
    "MAPSEC_UNOVA_LENTIMAS_OUTSKIRTS": "LENTIMAS TOWN",
    "MAPSEC_UNOVA_DRIFTVEIL_DRAWBRIDGE": "DRIFTVEIL BRIDGE",
    "MAPSEC_UNOVA_CASTELIA_SEWERS": "CASTELIA SEWERS",
    "MAPSEC_UNOVA_SPECIAL_MAP": None,      # sala de link, sem lugar no mundo
    "MAPSEC_GALAR_DYNAMAX_ADVENTURE": "MAX LAIR",
    "MAPSEC_GALAR_STOW_ON_SIDE": "STOW-ON-SIDE",
}


def nome_do_apelido(mapsec, apelidos=None):
    """MAPSEC_UNOVA_CASTELIA_CITY -> "CASTELIA CITY"; MAPSEC_GALAR_ROUTE01 -> "ROUTE 1".

    MAPSEC que NAO e apelido nao serve: e o MAPSEC de GRUPO, e o nome dele e
    justamente o "SINNOH WEST" que este conserto veio tirar do letreiro.
    """
    if apelidos is not None and mapsec not in apelidos:
        return None
    if mapsec in APELIDO_ESPECIAL:
        return APELIDO_ESPECIAL[mapsec]
    corpo = mapsec
    for prefixo in ("MAPSEC_UNOVA_", "MAPSEC_GALAR_", "MAPSEC_"):
        if corpo.startswith(prefixo):
            corpo = corpo[len(prefixo):]
            break
    achou = re.match(r"^ROUTE0*(\d+)$", corpo)
    if achou:
        return "ROUTE %d" % int(achou.group(1))
    achou = re.match(r"^R_0*(\d+)$", corpo)
    if achou:
        return "ROUTE %d" % int(achou.group(1))
    achou = re.match(r"^ROUTE_0*(\d+)(?:_(?:NORTH|SOUTH|EAST|WEST))?$", corpo)
    if achou:
        return "ROUTE %d" % int(achou.group(1))
    return corpo.replace("_", " ")


# -------------------------------------------------- nome a partir da pasta ----

# Radical de PASTA -> lugar. Vence o prefixo mais longo. So entra aqui radical
# que a pasta resolve melhor que o apelido: em Johto e Unova o apelido ja e o
# lugar, e o dicionario cobre so a excecao.
RADICAIS_SINNOH = {
    "AcuityCavern": "ACUITY CAVERN",
    "AcuityLakefront": "ACUITY LAKEFRONT",
    "CanalaveCity": "CANALAVE CITY",
    "CanalaveLibrary": "CANALAVE CITY",
    "CelesticTown": "CELESTIC TOWN",
    "ContestHallLobby": "HEARTHOME CITY",
    "CycleShop": "ETERNA CITY",
    "DistortionWorld": "DISTORTION WORLD",
    "EternaCity": "ETERNA CITY",
    "EternaForest": "ETERNA FOREST",
    "FloaromaMeadow": "FLOAROMA MEADOW",
    "FloaromaTown": "FLOAROMA TOWN",
    "FloaromaTwon": "FLOAROMA TOWN",           # a pasta tem o erro de digitacao
    "FootstepHouse": "SOLACEON TOWN",
    "FuegoIronworks": "FUEGO IRONWORKS",
    "GalacticHQ": "VEILSTONE CITY",
    "GalacticHq": "VEILSTONE CITY",
    "GrandLakeRoute213": "ROUTE 213",
    "GrandLakeValorLakefront": "VALOR LAKEFRONT",
    "HearthomeCity": "HEARTHOME CITY",
    "HotelGrandLake": "HOTEL GRAND LAKE",
    "IcebergRuins": "ICEBERG RUINS",
    "IronIsland": "IRON ISLAND",
    "IronRuins": "IRON RUINS",
    "JubilifeCity": "JUBILIFE CITY",
    "JubilifeTv": "JUBILIFE CITY",
    "LakeAcuity": "LAKE ACUITY",
    "LakeValor": "LAKE VALOR",
    "LakeVerity": "LAKE VERITY",
    "ManiacTunnel": "MANIAC TUNNEL",
    "MiningMuseum": "OREBURGH CITY",
    "MtCoronet": "MT. CORONET",
    "OldChateau": "OLD CHATEAU",
    "OreburghCity": "OREBURGH CITY",
    "OreburghGate": "OREBURGH GATE",
    "OreburghMine": "OREBURGH MINE",
    "PastoriaCity": "PASTORIA CITY",
    "PoffinHouse": "HEARTHOME CITY",
    "PokemonDayCare": "SOLACEON TOWN",
    "PokemonLeague": "POKEMON LEAGUE",
    "PokmonLeague": "POKEMON LEAGUE",          # a pasta tem o erro de digitacao
    "RavagedPath": "RAVAGED PATH",
    "RotomsRoom": "OLD CHATEAU",
    "Route205House": "ROUTE 205",
    "Route208House": "ROUTE 208",
    "Route209LostTower": "LOST TOWER",
    "Route210GrandmaWilmaHouse": "ROUTE 210",
    "Route212House": "ROUTE 212",
    "Route216House": "ROUTE 216",
    "Route217NortheastHouse": "ROUTE 217",
    "Route217WestHouse": "ROUTE 217",
    "Route221House": "ROUTE 221",
    "Route222EastHouse": "ROUTE 222",
    "Route222WestHouse": "ROUTE 222",
    "RuinManiacCave": "RUIN MANIAC CAVE",
    "SandgemTown": "SANDGEM TOWN",
    "Sandgem_Town": "SANDGEM TOWN",
    "SinnohLeague": "POKEMON LEAGUE",
    "SinnohVictoryRoad": "VICTORY ROAD",
    "SnowpointCity": "SNOWPOINT CITY",
    "SnowpointTemple": "SNOWPOINT TEMPLE",
    "SolaceonRuins": "SOLACEON RUINS",
    "SolaceonTown": "SOLACEON TOWN",
    "SpearPillar": "SPEAR PILLAR",
    "SunyshoreCity": "SUNYSHORE CITY",
    "SunyshoreMarket": "SUNYSHORE CITY",
    "TeamGalacticEternaBuilding": "ETERNA CITY",
    "TwinleafTown": "TWINLEAF TOWN",
    "Twinleaf_Town": "TWINLEAF TOWN",
    "ValleyWindworks": "VALLEY WINDWORKS",
    "ValorCavern": "VALOR CAVERN",
    "ValorLakefront": "VALOR LAKEFRONT",
    "VeilstoneCity": "VEILSTONE CITY",
    "VeilstoneStore": "VEILSTONE CITY",
    "VerityCavern": "VERITY CAVERN",
    "VerityLakefront": "VERITY LAKEFRONT",
    "VictoryRoad": "VICTORY ROAD",
    "VistaLighthouse": "SUNYSHORE CITY",
    "WaywardCave": "WAYWARD CAVE",
}

RADICAIS_JOHTO = {
    "BellchimeTrail": "BELLCHIME TRAIL",
}

RADICAIS_UNOVA = {}

# Galar e regular: `Galar_<Lugar><NN>`. O radical sai do CamelCase e o
# dicionario so corrige o que a quebra mecanica erraria.
RADICAIS_GALAR = {
    "CrownTundraIndoor": "CROWN TUNDRA",
    "DynamaxAdventure": "MAX LAIR",
    "GalarMine": "GALAR MINE",
    "StowOnSide": "STOW-ON-SIDE",
    "TurffieldIndoor": "TURFFIELD",
    "WildAreaCave": "WILD AREA",
    "WildAreaIndoor": "WILD AREA",
    "WyndonIndoor": "WYNDON",
}

RADICAIS = {
    "Sinnoh": RADICAIS_SINNOH,
    "Johto": RADICAIS_JOHTO,
    "Unova": RADICAIS_UNOVA,
    "Galar": RADICAIS_GALAR,
}

# Pasta que nao resolve nem por radical nem por apelido, e que tambem nao tem
# lugar obvio no jogo original: fica sem campo e sai no CSV de revisao.
PASTA_SEM_LUGAR = {
    "Cafe", "ForeignBuilding", "Restaurant",
}


def quebra_camel(palavra):
    """"IsleOfArmor" -> "ISLE OF ARMOR"; "SlumberingWeald" -> "SLUMBERING WEALD"."""
    pedacos = re.findall(r"[A-Z][a-z]*|\d+", palavra)
    return " ".join(p.upper() for p in pedacos)


def nome_da_pasta(pasta, regiao):
    """Aplica o dicionario de radicais e, em Galar, a quebra mecanica."""
    if pasta in PASTA_SEM_LUGAR:
        return None
    nu = pasta
    if nu.startswith("Unused"):
        nu = nu[len("Unused"):]
    for prefixo in ("Galar_", "Unova_"):
        if nu.startswith(prefixo):
            nu = nu[len(prefixo):]
    tabela = RADICAIS[regiao]
    for radical in sorted(tabela, key=len, reverse=True):
        if nu.startswith(radical):
            return tabela[radical]
    if regiao == "Galar":
        # Galar numera a pasta com quatro digitos: Route0803 e o terceiro mapa
        # da rota 8, e nao a rota 803.
        achou = re.match(r"^Route(\d\d)\d\d$", nu)
        if achou:
            return "ROUTE %d" % int(achou.group(1))
    elif regiao == "Sinnoh":
        achou = re.match(r"^Route0*(\d+)", nu)
        if achou:
            return "ROUTE %d" % int(achou.group(1))
    if regiao == "Galar":
        raiz = re.sub(r"\d+$", "", nu)
        if raiz:
            return quebra_camel(raiz)
    return None


# ------------------------------------------------------------- a travessia ----

class Mapa:
    def __init__(self, grupo, numero, pasta, mapsec, andar, mostra, campo):
        self.grupo = grupo
        self.numero = numero
        self.pasta = pasta
        self.mapsec = mapsec
        self.andar = andar
        self.mostra = mostra
        self.campo = campo          # o `map_name_popup` que JA esta no map.json
        self.regiao = None
        self.nome = None
        self.origem = None
        self.divergencia = None


def le_mapas(raiz):
    """Le map_groups.json e cada map.json, na ORDEM que vira indice na ROM."""
    with open(os.path.join(raiz, "data/maps/map_groups.json"), encoding="utf-8") as arq:
        grupos = json.load(arq)
    mapas = []
    for indice_grupo, grupo in enumerate(grupos["group_order"]):
        for indice_mapa, pasta in enumerate(grupos[grupo]):
            caminho = os.path.join(raiz, "data/maps", pasta, "map.json")
            with open(caminho, encoding="utf-8") as arq:
                dados = json.load(arq)
            mapas.append(Mapa(indice_grupo, indice_mapa, pasta,
                              dados.get("region_map_section", "MAPSEC_NONE"),
                              int(dados.get("floor_number", 0) or 0),
                              bool(dados.get("show_map_name")),
                              dados.get("map_name_popup")))
    return mapas, len(grupos["group_order"])


def decide_nomes(raiz, mapas, apelidos, regiao_do_apelido, regua):
    """Preenche mapa.nome/origem e devolve as linhas do CSV de revisao."""
    revisao = []
    for mapa in mapas:
        if mapa.mapsec == "MAPSEC_NONE":
            continue
        mapa.regiao = regiao_do_mapsec(mapa.mapsec, regiao_do_apelido)
        if mapa.regiao is None:
            continue
        por_pasta = nome_da_pasta(mapa.pasta, mapa.regiao)
        por_apelido = nome_do_apelido(mapa.mapsec, apelidos)
        if por_pasta:
            mapa.nome, mapa.origem = por_pasta, "pasta"
            if por_apelido and por_apelido != por_pasta:
                mapa.divergencia = por_apelido
        elif por_apelido:
            mapa.nome, mapa.origem = por_apelido, "apelido"
        else:
            revisao.append((mapa, "", "sem radical e sem apelido util"))
            continue
        completo = mapa.nome + sufixo_de_andar(mapa.andar)
        largura = regua.px(completo)
        if len(completo) > CARACTERES_MAXIMOS:
            revisao.append((mapa, mapa.nome, "%d caracteres passam de %d"
                            % (len(completo), CARACTERES_MAXIMOS)))
            mapa.nome = None
        elif largura is None:
            revisao.append((mapa, mapa.nome, "caractere fora do charmap"))
            mapa.nome = None
        elif largura > LARGURA_MAXIMA_PX:
            revisao.append((mapa, mapa.nome, "largura %d px passa de %d"
                            % (largura, LARGURA_MAXIMA_PX)))
            mapa.nome = None
        elif mapa.divergencia:
            revisao.append((mapa, mapa.nome,
                            "aviso: a pasta manda, o apelido dizia %s" % mapa.divergencia))
    return revisao


# --------------------------------------------------------------- a escrita ----

MARCA = '  "map_name_popup": '


def escreve_campo(caminho, nome):
    """Insere, atualiza ou tira `map_name_popup` logo abaixo de `region_map_section`.

    Edicao por TEXTO de proposito: reserializar o JSON inteiro mexeria em 2.400
    arquivos por causa de espaco em branco, e o diff deixaria de ser legivel.
    Toda linha antiga do campo sai antes de a nova entrar, senao rodar de novo
    empilharia uma copia por execucao.
    """
    with open(caminho, encoding="utf-8") as arq:
        linhas = arq.readlines()
    sem_campo = [linha for linha in linhas if not linha.startswith(MARCA)]
    saida = []
    posto = False
    for linha in sem_campo:
        saida.append(linha)
        if nome and not posto and linha.startswith('  "region_map_section": '):
            saida.append('  "map_name_popup": %s,\n' % json.dumps(nome))
            posto = True
    if saida == linhas:
        return False
    with open(caminho, "w", encoding="utf-8") as arq:
        arq.writelines(saida)
    return True


def identificador(nome):
    return "sPopupNome_" + re.sub(r"[^A-Za-z0-9]", "", nome.title())


AVISO = """//
// ARQUIVO GERADO. Nao edite a mao: rode `python3 dev_scripts/nomes_popup.py`,
// ou apenas `make`, que o passo de map_data_rules.mk regenera este arquivo a
// partir do campo `map_name_popup` de cada data/maps/*/map.json.
//
// Existe porque MAPSEC e u8 e nao cabe uma secao por cidade: Johto, Sinnoh,
// Unova e Galar tem um MAPSEC por GRUPO, e o letreiro de mapa dizia "SINNOH
// WEST" no lugar do nome. Aqui o nome do letreiro fica desacoplado do MAPSEC.
//
"""


def gera_tabela(mapas, quantos_grupos, regua):
    """Monta o texto do .h a partir do CAMPO `map_name_popup` de cada map.json.

    A fonte da verdade e o map.json, e nao a derivacao: quem editar o campo a
    mao tem que ver a mudanca no letreiro sem mexer no dicionario de radicais.
    """
    for mapa in mapas:
        if not mapa.campo:
            continue
        largura = regua.px(mapa.campo + sufixo_de_andar(mapa.andar))
        if len(mapa.campo) > CARACTERES_MAXIMOS or largura is None or largura > LARGURA_MAXIMA_PX:
            raise SystemExit("map_name_popup de %s nao cabe no letreiro: %r"
                             % (mapa.pasta, mapa.campo))
    nomes = sorted({m.campo for m in mapas if m.campo})
    vistos = {}
    for nome in nomes:                       # dois nomes com o mesmo identificador
        ident = identificador(nome)          # sobrescreveriam um ao outro em silencio
        if ident in vistos:
            raise SystemExit("identificador repetido: %r e %r viram %s"
                             % (vistos[ident], nome, ident))
        vistos[ident] = nome
    linhas = [AVISO, "#ifndef GUARD_DATA_MAP_POPUP_NAMES_H\n",
              "#define GUARD_DATA_MAP_POPUP_NAMES_H\n\n"]
    for nome in nomes:
        linhas.append('static const u8 %s[] = _("%s");\n' % (identificador(nome), nome))
    linhas.append("\n")

    por_grupo = {}
    for mapa in mapas:
        if mapa.campo:
            por_grupo.setdefault(mapa.grupo, {})[mapa.numero] = mapa.campo
    for grupo in sorted(por_grupo):
        entradas = por_grupo[grupo]
        ultimo = max(entradas)
        linhas.append("static const u8 *const sPopupNomesGrupo%d[] = {\n" % grupo)
        for numero in range(ultimo + 1):
            nome = entradas.get(numero)
            linhas.append("    [%d] = %s,\n" % (numero, identificador(nome) if nome else "NULL"))
        linhas.append("};\n\n")

    linhas.append("static const u8 *const *const sPopupNomesPorGrupo[] = {\n")
    for grupo in range(quantos_grupos):
        if grupo in por_grupo:
            linhas.append("    [%d] = sPopupNomesGrupo%d,\n" % (grupo, grupo))
        else:
            linhas.append("    [%d] = NULL,\n" % grupo)
    linhas.append("};\n\n")

    linhas.append("static const u8 sPopupNomesPorGrupoTamanho[] = {\n")
    for grupo in range(quantos_grupos):
        tamanho = max(por_grupo[grupo]) + 1 if grupo in por_grupo else 0
        linhas.append("    [%d] = %d,\n" % (grupo, tamanho))
    linhas.append("};\n\n")
    linhas.append("#endif // GUARD_DATA_MAP_POPUP_NAMES_H\n")
    return "".join(linhas)


def escreve_se_mudou(caminho, texto):
    if os.path.exists(caminho):
        with open(caminho, encoding="utf-8") as arq:
            if arq.read() == texto:
                return False
    with open(caminho, "w", encoding="utf-8") as arq:
        arq.write(texto)
    return True


def gera_csv(revisao):
    linhas = ["pasta,mapsec,regiao,nome_proposto,motivo\n"]
    for mapa, proposto, motivo in revisao:
        linhas.append("%s,%s,%s,%s,%s\n"
                      % (mapa.pasta, mapa.mapsec, mapa.regiao or "", proposto, motivo))
    return "".join(linhas)


# --------------------------------------------------------------- autoteste ----

def autoteste():
    falhas = []

    def confere(o_que, deu, esperado):
        if deu != esperado:
            falhas.append("%s: deu %r, esperava %r" % (o_que, deu, esperado))

    confere("apelido de rota de Unova", nome_do_apelido("MAPSEC_UNOVA_R_11"), "ROUTE 11")
    confere("apelido de rota de Galar", nome_do_apelido("MAPSEC_GALAR_ROUTE01"), "ROUTE 1")
    confere("apelido de rota partida", nome_do_apelido("MAPSEC_ROUTE_205_NORTH"), "ROUTE 205")
    confere("apelido de cidade", nome_do_apelido("MAPSEC_UNOVA_CASTELIA_CITY"), "CASTELIA CITY")
    confere("apelido com ponto", nome_do_apelido("MAPSEC_MT_SILVER"), "MT. SILVER")
    confere("pasta de Sinnoh", nome_da_pasta("SunyshoreCityPokecenter1F", "Sinnoh"), "SUNYSHORE CITY")
    confere("pasta de rota de Sinnoh", nome_da_pasta("Route221House", "Sinnoh"), "ROUTE 221")
    confere("pasta de ruina", nome_da_pasta("SolaceonRuinsRoom3", "Sinnoh"), "SOLACEON RUINS")
    confere("pasta de monte", nome_da_pasta("MtCoronet4FRoom3", "Sinnoh"), "MT. CORONET")
    confere("pasta Unused", nome_da_pasta("UnusedJubilifeCityHouse1", "Sinnoh"), "JUBILIFE CITY")
    confere("pasta de Galar", nome_da_pasta("Galar_TurffieldIndoor42", "Galar"), "TURFFIELD")
    confere("pasta de Galar por camel", nome_da_pasta("Galar_SlumberingWeald03", "Galar"), "SLUMBERING WEALD")
    confere("rota de Galar", nome_da_pasta("Galar_Route0803", "Galar"), "ROUTE 8")
    confere("pasta sem lugar", nome_da_pasta("Restaurant", "Sinnoh"), None)
    confere("sufixo de subsolo", sufixo_de_andar(-1), " B1F")
    confere("sufixo de andar", sufixo_de_andar(2), " 2F")
    confere("sem andar", sufixo_de_andar(0), "")

    regua = Regua(RAIZ)
    confere("largura conhecida", regua.px("SINNOH WEST"), 43)
    if regua.px("SUNYSHORE CITY") > LARGURA_MAXIMA_PX:
        falhas.append("SUNYSHORE CITY nao caberia na caixa, a regua esta errada")

    apelido, regiao_do_apelido = le_apelidos(RAIZ)
    confere("Johto e apelido de grupo de Sinnoh",
            apelido.get("MAPSEC_AZALEA_TOWN"), "MAPSEC_SINNOH_WEST")
    confere("regiao do apelido de Johto", regiao_do_apelido.get("MAPSEC_AZALEA_TOWN"), "Johto")
    confere("regiao do apelido de Galar", regiao_do_apelido.get("MAPSEC_GALAR_POSTWICK"), "Galar")
    confere("regiao do grupo cru de Sinnoh",
            regiao_do_mapsec("MAPSEC_SINNOH_NORTH", regiao_do_apelido), "Sinnoh")
    confere("Hoenn fica de fora", regiao_do_mapsec("MAPSEC_LITTLEROOT_TOWN", regiao_do_apelido), None)

    if falhas:
        for f in falhas:
            print("FALHOU:", f)
        return 1
    print("autoteste de nomes_popup: %d casos, todos verdes" % 25)
    return 0


# ------------------------------------------------------------------- porta ----

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seco", action="store_true", help="nao escreve nada")
    ap.add_argument("--tabela", action="store_true", help="so gera o .h")
    ap.add_argument("--demo", action="store_true", help="autoteste")
    ap.add_argument("--autoteste", action="store_true", help="autoteste")
    args = ap.parse_args()

    if args.demo or args.autoteste:
        return autoteste()

    regua = Regua(RAIZ)
    mapas, quantos_grupos = le_mapas(RAIZ)

    if args.tabela:
        # Passo do make: le SO o campo dos map.json, sem derivar nada.
        escreveu = escreve_se_mudou(os.path.join(RAIZ, CAMINHO_TABELA),
                                    gera_tabela(mapas, quantos_grupos, regua))
        print("%s: %s" % (CAMINHO_TABELA, "reescrito" if escreveu else "sem mudanca"))
        return 0

    apelidos, regiao_do_apelido = le_apelidos(RAIZ)
    revisao = decide_nomes(RAIZ, mapas, apelidos, regiao_do_apelido, regua)

    if not args.seco:
        mexidos = 0
        for mapa in mapas:
            if mapa.regiao is None and mapa.nome is None and mapa.campo is None:
                continue
            caminho = os.path.join(RAIZ, "data/maps", mapa.pasta, "map.json")
            if escreve_campo(caminho, mapa.nome):
                mexidos += 1
            mapa.campo = mapa.nome
        print("map.json alterados: %d" % mexidos)
        escreve_se_mudou(os.path.join(RAIZ, CAMINHO_CSV), gera_csv(revisao))
        escreveu = escreve_se_mudou(os.path.join(RAIZ, CAMINHO_TABELA),
                                    gera_tabela(mapas, quantos_grupos, regua))
        print("%s: %s" % (CAMINHO_TABELA, "reescrito" if escreveu else "sem mudanca"))
    else:
        for mapa in mapas:
            mapa.campo = mapa.nome
        print("tabela teria %d bytes" % len(gera_tabela(mapas, quantos_grupos, regua)))

    por_regiao = {}
    for mapa in mapas:
        if mapa.regiao:
            chave = (mapa.regiao, bool(mapa.nome))
            por_regiao[chave] = por_regiao.get(chave, 0) + 1
    for regiao in ("Johto", "Sinnoh", "Unova", "Galar"):
        print("%-7s com nome: %4d   sem nome: %3d"
              % (regiao, por_regiao.get((regiao, True), 0), por_regiao.get((regiao, False), 0)))
    print("linhas no CSV de revisao: %d" % len(revisao))
    return 0


if __name__ == "__main__":
    sys.exit(main())
