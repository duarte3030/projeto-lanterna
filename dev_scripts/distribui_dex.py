#!/usr/bin/env python3
"""Distribui a dex inteira pelas 5 regioes: mato, estatico, presente, evolucao.

    python3 dev_scripts/distribui_dex.py --tabela          # (re)escreve o JSON de decisao
    python3 dev_scripts/distribui_dex.py --selvagem        # aplica as linhas de mato
    python3 dev_scripts/distribui_dex.py --motor           # conserto de regiao + EVO_ITEM
    python3 dev_scripts/distribui_dex.py --presentes       # NPCs de presente
    python3 dev_scripts/distribui_dex.py --estaticos --regiao Sinnoh
    python3 dev_scripts/distribui_dex.py --estaticos --dry-run          # todas as regioes
    python3 dev_scripts/distribui_dex.py --demo            # autoteste com mutacao plantada

Sem `--aplica` NADA e escrito: todo subcomando so relata o que faria.

O que este arquivo e, e o que ele NAO e
---------------------------------------
Ele e o EXECUTOR. A decisao mora em `dev_scripts/dex_distribuicao.json`, uma
linha por entrada inobtenivel, gerada por `--tabela` a partir de tres fontes
medidas: o censo (`dev_scripts/censo_dex.py`), a pesquisa de lendarios
(`lendarios_referencia.csv`, copiada para `dev_scripts/`) e o perfil de tipos
das proprias tabelas de encontro. Quem quiser mudar UMA decisao muda o JSON;
quem quiser mudar a REGUA muda `plano()` aqui e roda `--tabela` de novo.

Ele NAO e uma segunda ferramenta de estatico: a geometria (busca em largura com
colisao E elevacao, portao de nao-ilhar, rota de pernas retas, 3 tiles de
distancia de NPC que anda) vem importada de `dev_scripts/lendarios_sinnoh.py`,
que ja a tinha e ja foi provada pelo T123.

A regua, em dez linhas (PLANO-DEX.md secao 3, decidida pelo condutor)
--------------------------------------------------------------------
 1. Nivel nao se toca: a linha nova herda o nivel do slot que ela ocupa, e o
    estatico herda o nivel da fonte. Quem rebaixa para 5 e o modo de teste.
 2. Slot "vazio" = slot DUPLICADO. Nao ha slot vazio no JSON de encontros; ha
    5.622 slots em que a mesma especie ocupa duas linhas da MESMA tabela. A
    especie nova entra na SEGUNDA ocorrencia, entao nenhuma especie que a fonte
    pos sai da tabela.
 3. Gen 1 a 5 vai para a regiao da geracao. Sem excecao.
 4. Bioma sai do PERFIL DE TIPOS da propria tabela, nao de julgamento de mapa.
 5. Empate de bioma resolve por cota da regiao (a que recebeu menos leva).
 6. TYPE_WATER so em `water_mons`/`fishing_mons`; quem nao e agua so em
    `land_mons`/`rock_smash_mons`.
 7. Lenda nunca vai para o mato: e sempre estatico, um lugar por Pokemon.
 8. Lar canonico primeiro (coluna de recomendacao da pesquisa), bioma depois.
 9. Nada de trava de pos-jogo.
10. Padrao cosmetico espalha por rodizio de regiao (Vivillon acaba com os 20
    padroes espalhados pelas 5; familia de 5 ou menos fica com uma por regiao).

Armadilhas medidas nesta rodada, que valem para quem mexer aqui
---------------------------------------------------------------
1. **Johto e Sinnoh compartilham o MESMO mapsec.** Os 65 apelidos de MAPSEC de
   Johto (`MAPSEC_NEW_BARK_TOWN`, `MAPSEC_ILEX_FOREST`, ...) sao todos
   `#define ... MAPSEC_SINNOH_WEST` em `include/constants/region_map_sections.h`.
   Nenhuma faixa de sectionId separa as duas regioes; por isso o conserto de
   motor resolve Johto pelo GRUPO DE MAPA, e nao pelo mapsec. Ver `--motor`.
2. **`ITEM_LINKING_CORD` JA existe neste repo** (`include/constants/items.h`,
   id 796) e o upstream ja deu segunda linha `EVO_ITEM` a 12 evolucoes de
   troca. O `PLANO-DEX.md` diz que nao existe porque procurou por `LINK_CABLE`.
   Faltam exatamente DUAS: Karrablast e Shelmet, que sao `EVO_TRADE` com
   `IF_TRADE_PARTNER_SPECIES` e nao tem alternativa nenhuma.
3. **As 243 entradas de MACRO nao tem `OVERWORLD(` visivel ao censo**, porque
   `catalogo_especies._blocos` nao as enxerga. Isso NAO impede nada aqui: todas
   elas vao para o mato, e so estatico precisa de gfx de overworld.
"""
import argparse
import collections
import csv
import glob
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
import catalogo_especies                    # noqa: E402
import censo_dex                            # noqa: E402
import lendarios_sinnoh as LS               # noqa: E402  (geometria ja provada)

TABELA = f"{RAIZ}/dev_scripts/dex_distribuicao.json"
PESQUISA = f"{RAIZ}/dev_scripts/lendarios_referencia.csv"
ENCONTROS = f"{RAIZ}/src/data/wild_encounters.json"
FLAGS_H = f"{RAIZ}/include/constants/flags.h"
REGIOES_H = f"{RAIZ}/include/regions.h"
CASOS = f"{RAIZ}/dev_scripts/testes_criticos/129_dex_completa.json"
# Arquivos de caso que SAEM desta tabela (129 da onda A, 131 a 135 da onda B, e
# 136, o arquivo adversarial do fechador, que reanda as MESMAS rotas do 132).
# Ler o proprio rastro fecha um ciclo: ver `corredor_de_casos`.
CASOS_DERIVADOS = re.compile(r"^(129|13[1-6])_")

MARCA = "distribui_dex"
MARCA_INI = "// >>> Dex completa: HIDE dos estaticos (dev_scripts/distribui_dex.py) >>>"
MARCA_FIM = "// <<< Dex completa <<<"
INC_INI = "@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>"
INC_FIM = "@ <<< Dex completa <<<"

# Cauda da maior faixa livre (0x20D2-0x321F, medida por flags_livres.py). A
# CABECA fica para quem pedir reserva; o lendarios_sinnoh.py ja mora em
# 0x3220-0x322A, logo acima. 96 estaticos cabem em 0x31C0-0x321F.
FLAG_BASE = 0x31A0
FLAG_TETO = 0x321F
# O commit em que o `wild_encounters.json` ainda era o da fonte, ANTES da onda A.
# E o unico lado independente que existe para conferir o mato (ver
# `diff_do_mato`): tudo o mais nesta rodada saiu desta mesma tabela.
BASE_MATO = "0cb8724099"
# Duas flags de "ja peguei" para os dois NPCs de presente, logo ABAIXO do bloco
# dos estaticos. Sem elas o NPC entrega o mesmo Pokemon a cada fala.
FLAG_PRESENTE_INICIAL = 0x319E
FLAG_PRESENTE_EVENTO = 0x319F

CINCO = ("Kanto", "Johto", "Hoenn", "Sinnoh", "Unova")
REGIAO_DA_GEN = {1: "Kanto", 2: "Johto", 3: "Hoenn", 4: "Sinnoh", 5: "Unova"}
AGUA = ("water_mons", "fishing_mons")
TERRA = ("land_mons", "rock_smash_mons")

# Teto do motor. `BellchimeTrail` tem 64 e nao aceita mais nenhum objeto.
TETO_OBJETOS = 64

# Segundo teto, e o que NAO aparece em erro nenhum: o motor so tem
# OBJECT_EVENTS_COUNT = 16 slots de sprite ativo (include/constants/global.h) e
# um deles e sempre o jogador, entao sobram 15. `TrySpawnObjectEvents`
# (src/event_object_movement.c) acorda TODO template dentro de uma janela em
# volta do jogador: com MAP_OFFSET 7, MAP_OFFSET_W 15 e MAP_OFFSET_H 14, a
# condicao `left <= npcX <= right` vira `pos.x - 9 <= tile.x <= pos.x + 10` e a
# de y vira `pos.y - 7 <= tile.y <= pos.y + 9`. Sao 20 por 17 tiles. Do 16o
# objeto em diante `TrySpawnObjectEventTemplate` desiste CALADO: o lendario
# existe no mapa, tem script, tem flag, e simplesmente nao aparece na tela.
# Por isso a distancia de 5 tiles entre estaticos nao basta sozinha: 4 colunas
# por 4 linhas de 5 em 5 ja sao 16 dentro de uma janela so.
JANELA_SPRITE = (20, 17)
TETO_SPRITE = 15

# Sufixo de forma regional. Estas NAO seguem a regra 3 (regiao da geracao):
# um Rattata de Alola e gen 1 de dex e nao tem nada que fazer em Kanto.
SUFIXO_REGIONAL = ("_ALOLA", "_GALAR", "_HISUI", "_PALDEA")

# Familias cosmeticas: a mesma especie em N pinturas. Espalham por rodizio.
COSMETICAS = ("VIVILLON", "SCATTERBUG", "SPEWPA", "FURFROU", "FLABEBE",
              "FLOETTE", "FLORGES", "MINIOR", "DEERLING", "SAWSBUCK",
              "PUMPKABOO", "GOURGEIST", "SQUAWKABILLY", "TATSUGIRI",
              "ALCREMIE", "UNOWN", "BASCULIN", "SHELLOS", "GASTRODON",
              "SILVALLY", "ARCEUS", "GENESECT", "OGERPON")

# Nivel da FONTE do estatico. Nao e chute de dificuldade: e o nivel em que o
# jogo de origem entrega o bicho. O modo LV.5 de fabrica rebaixa tudo sozinho.
NIVEL_ESTATICO = {
    "mitico": 30, "ub": 60, "paradox": 60, "capa": 70, "padrao": 50,
}
CAPA = ("RESHIRAM", "ZEKROM", "KYUREM", "XERNEAS", "YVELTAL", "ZYGARDE",
        "SOLGALEO", "LUNALA", "NECROZMA", "ZACIAN", "ZAMAZENTA", "ETERNATUS",
        "KORAIDON", "MIRAIDON", "TERAPAGOS", "CALYREX")
MITICO = ("CELEBI", "JIRACHI", "PHIONE", "MANAPHY", "SHAYMIN", "VICTINI",
          "KELDEO", "MELOETTA", "DIANCIE", "HOOPA", "VOLCANION", "MAGEARNA",
          "MARSHADOW", "ZERAORA", "MELTAN", "MELMETAL", "ZARUDE", "PECHARUNT")
UB = ("NIHILEGO", "BUZZWOLE", "PHEROMOSA", "XURKITREE", "CELESTEELA",
      "KARTANA", "GUZZLORD", "POIPOLE", "NAGANADEL", "STAKATAKA", "BLACEPHALON")
PARADOX = ("GREAT_TUSK", "SCREAM_TAIL", "BRUTE_BONNET", "FLUTTER_MANE",
           "SLITHER_WING", "SANDY_SHOCKS", "IRON_TREADS", "IRON_BUNDLE",
           "IRON_HANDS", "IRON_JUGULIS", "IRON_MOTH", "IRON_THORNS",
           "ROARING_MOON", "IRON_VALIANT", "WALKING_WAKE", "IRON_LEAVES",
           "GOUGING_FIRE", "RAGING_BOLT", "IRON_BOULDER", "IRON_CROWN")

# Zona unica das Ultra Beasts e as duas salas de Paradox, copiando Radical Red
# (11 UBs numa caverna so) e Elite Redux (Paradox em duas salas de Victory
# Road). Decisao do condutor de 21/08/2026, registrada em lendarios_referencia.
ZONA_UB = ("MtCoronet_B1F",)
SALA_PARADOX_ANTIGO = ("Unova_VictoryRoadCave2F",)
# O `Unova_VictoryRoadCave3F` era a escolha obvia e foi MEDIDO com capacidade
# ZERO (nenhum tile passa nos portoes de alcancabilidade e de nao-ilhar). As
# duas salas do andar de baixo, que sao Victory Road do mesmo jeito, tem 9 cada.
SALA_PARADOX_FUTURO = ("Unova_VictoryRoadCave1F", "Unova_VictoryRoadGrove")

# Reserva de mapas espacosos por regiao, para quando o mapa preferido nao tiver
# tile que passe nos portoes. A capacidade de CADA um foi medida em 21/08/2026
# pela mesma busca em largura do estatico (o numero entre parenteses e quantos
# objetos cabem antes de a busca ficar sem tile), e nao chutada pelo tamanho do
# mapa: `MtEmber_Summit_Frlg` e grande e cabe ZERO, porque o cume e um corredor.
POOL = ("RockTunnel_1F_Frlg", "SeafoamIslands_B1F_Frlg", "MtMoon_1F_Frlg",
        "CeruleanCave_1F_Frlg", "ViridianForest_Frlg", "PowerPlant_Frlg",
        "SafariZone_Center_Frlg", "PokemonTower_3F_Frlg",
        "MtSilver_Outside", "UnionCave_1F", "WhirlIslands_B1F", "IlexForest",
        "IcePath_1F", "RuinsOfAlph_Outside", "BurnedTower_B1F",
        "AncientTomb", "DesertRuins", "IslandCave", "MtPyre_Summit",
        "ShoalCave_LowTideEntranceRoom", "GraniteCave_1F", "MarineCave_End",
        "EternaForest", "SinnohVictoryRoad1F", "SnowpointTempleB5F",
        "SnowpointCity", "MtCoronet_B1F",
        "Unova_ChargestoneCave1F", "Unova_TwistMountain1F",
        "Unova_RelicCastleB1F", "Unova_VictoryRoadCave1F",
        "Unova_VictoryRoadCave2F", "Unova_VictoryRoadGrove")

# Bioma -> mapa de destino, por regiao. Tabela da secao 3 do PLANO-DEX.md, com
# um mapa que EXISTE neste repo por celula (conferido em `demo`).
BIOMA = {
    "floresta":  {"Johto": "IlexForest", "Kanto": "ViridianForest_Frlg"},
    "caverna":   {"Sinnoh": "MtCoronet_B1F", "Kanto": "CeruleanCave_B1F_Frlg"},
    "ruina":     {"Johto": "RuinsOfAlph_Outside", "Hoenn": "AncientTomb"},
    "agua":      {"Hoenn": "MarineCave_End", "Johto": "WhirlIslands_B1F"},
    "neve":      {"Sinnoh": "SnowpointTempleB5F", "Johto": "IcePath_1F"},
    "vulcao":    {"Kanto": "MtEmber_Summit_Frlg", "Hoenn": "TerraCave_End"},
    "ceu":       {"Unova": "Unova_DragonspiralTower1F", "Kanto": "PowerPlant_Frlg"},
    "cidade":    {"Hoenn": "MtPyre_Summit", "Unova": "Unova_RelicCastleB1F"},
}
TIPO_BIOMA = {
    "TYPE_GRASS": "floresta", "TYPE_BUG": "floresta", "TYPE_FAIRY": "floresta",
    "TYPE_ROCK": "caverna", "TYPE_GROUND": "caverna", "TYPE_STEEL": "caverna",
    "TYPE_DRAGON": "caverna",
    "TYPE_PSYCHIC": "ruina", "TYPE_GHOST": "ruina", "TYPE_DARK": "ruina",
    "TYPE_WATER": "agua", "TYPE_ICE": "neve", "TYPE_FIRE": "vulcao",
    "TYPE_FLYING": "ceu", "TYPE_ELECTRIC": "ceu",
    "TYPE_NORMAL": "cidade", "TYPE_POISON": "cidade", "TYPE_FIGHTING": "cidade",
}

# Presentes por `givemon`: quem NAO tem gfx de overworld e portanto nao pode
# ser estatico, mais os tres iniciais de Hoenn, que sumiram deste jogo (o
# laboratorio do Birch entrega Chikorita/Cyndaquil/Totodile).
INICIAIS_HOENN = ("SPECIES_TREECKO", "SPECIES_TORCHIC", "SPECIES_MUDKIP")
PRESENTE_SEM_OVERWORLD = re.compile(
    r"^SPECIES_(PIKACHU_(?!MEGA)|PICHU_SPIKY|EEVEE_STARTER)")

# As duas evolucoes de troca que ficaram sem alternativa. `ITEM_LINKING_CORD`
# ja existe e ja e o que o upstream usa nas outras 12; nao se inventa item.
EVO_ITEM_NOVAS = (
    ("gen_5_families.h", "SPECIES_KARRABLAST", "SPECIES_ESCAVALIER"),
    ("gen_5_families.h", "SPECIES_SHELMET", "SPECIES_ACCELGOR"),
)


# --------------------------------------------------------------------- leitura

def _familia(nome):
    return nome.replace("SPECIES_", "").split("_")[0]


def eh_regional(nome):
    return any(s in nome for s in SUFIXO_REGIONAL)


def eh_cosmetica(nome):
    return _familia(nome) in COSMETICAS


def nivel_de(nome):
    n = nome.replace("SPECIES_", "")
    for grupo, chave in ((PARADOX, "paradox"), (UB, "ub"),
                         (MITICO, "mitico"), (CAPA, "capa")):
        if any(n == g or n.startswith(g + "_") for g in grupo):
            return NIVEL_ESTATICO[chave]
    return NIVEL_ESTATICO["padrao"]


def mapas_cortados():
    """Os mapas que o Gui tirou do escopo em 21/08/2026 (secao 0.j do ESTADO).

    Casamento EXATO, nunca por prefixo: a lista tem `PokemonMansion`, que e a
    mansao de SINNOH, e um prefixo pegaria junto o `PokemonMansion_1F_Frlg` de
    Cinnabar, que esta no escopo e e um lar de lendario perfeitamente vivo.
    """
    import completude
    return {a for g in completude.CORTES_DO_GUI for a in g.get("alvo", [])}


def mapas_existentes():
    """Pasta que existe E nao foi cortada do escopo. Regra 9: nada de mapa que
    o jogador nunca vai alcancar."""
    cortados = mapas_cortados()
    return {d for d in os.listdir(f"{RAIZ}/data/maps")
            if os.path.isdir(f"{RAIZ}/data/maps/{d}") and d not in cortados}


def pesquisa_lendarios(universo):
    """{SPECIES_X: (regiao, pasta_do_mapa, 'pesquisa')} lido do CSV da pesquisa.

    A coluna `mapa_recomendado_repo` e texto livre com alternativas ("A ou B
    (ver risco)"). A regra e literal e nao interpretativa: pega o PRIMEIRO
    token do texto que seja pasta existente em `data/maps/`. Se nenhum for,
    a especie cai no bioma, e a linha do JSON diz `origem: bioma`.
    """
    if not os.path.exists(PESQUISA):
        return {}
    existem = mapas_existentes()
    fora = {}
    for r in csv.DictReader(open(PESQUISA, encoding="utf-8")):
        regiao = r["regiao_recomendada"].strip()
        if regiao not in CINCO:
            continue
        mapa = next((t for t in re.findall(r"[A-Za-z0-9_]+",
                                           r["mapa_recomendado_repo"])
                     if t in existem), None)
        if not mapa:
            continue
        for pedaco in re.split(r"[/,]", r["especie"]):
            alvo = "SPECIES_" + re.sub(r"[^A-Z0-9]+", "_",
                                       pedaco.strip().upper()).strip("_")
            if alvo in universo:
                fora[alvo] = (regiao, mapa, "pesquisa")
                continue
            # Tapu Koko -> SPECIES_TAPU_KOKO ja casou acima; Tornadus ->
            # SPECIES_TORNADUS_INCARNATE, Xerneas -> SPECIES_XERNEAS_NEUTRAL.
            cand = sorted(n for n in universo if n.startswith(alvo + "_"))
            if cand:
                fora[cand[0]] = (regiao, mapa, "pesquisa")
    return fora


def bioma_de(tipos):
    for t in tipos:
        if t in TIPO_BIOMA:
            return TIPO_BIOMA[t]
    return "cidade"


_BASE = {}


def encontros_base():
    """O `wild_encounters.json` como ele era ANTES desta ferramenta.

    Toda linha do plano guarda `substituido`, a especie que ocupava o slot. Com
    ela, o baseline se reconstroi a qualquer hora, e e por isso que `--tabela` e
    `--selvagem` sao idempotentes: sem o baseline, rodar `--tabela` depois de
    `--selvagem` veria menos slots duplicados (porque as especies novas ja nao
    repetem ninguem) e cuspiria um plano diferente a cada rodada.
    """
    if _BASE:
        return _BASE["d"]
    d = json.load(open(ENCONTROS, encoding="utf-8"))
    _BASE["d"] = d
    antigo = tabela_gravada()
    if antigo:
        idx = _indice(d)
        for l in antigo.get("selvagens", []):
            mons = idx.get((l["mapa"], l["metodo"]))
            if mons and l.get("substituido"):
                mons[l["slot"]]["species"] = l["substituido"]
    return d


def _indice(d):
    fora = {}
    for g in d["wild_encounter_groups"]:
        if not g.get("for_maps"):
            continue
        for enc in g["encounters"]:
            mid = enc.get("map", enc.get("base_label", g["label"]))
            for tp in censo_dex.TIPOS_SELVAGEM:
                if tp in enc:
                    fora[(mid, tp)] = enc[tp]["mons"]
    return fora


def tabelas_de_encontro(mapa_regiao):
    """[(mapa, tipo, regiao, perfil_de_tipos, [indices de slot duplicado])].

    Slot duplicado = a especie daquele indice ja apareceu ANTES na mesma tabela
    e no mesmo tipo. Trocar o segundo nao tira nada do jogo: a especie da fonte
    continua na primeira ocorrencia. Foi assim que o censo mediu 5.622 deles.
    """
    d = encontros_base()
    cat = catalogo_completo()
    fora = []
    for grupo in d["wild_encounter_groups"]:
        if not grupo.get("for_maps"):
            continue                      # Battle Pyramid/Pike nao e mundo
        for enc in grupo["encounters"]:
            mid = enc.get("map", enc.get("base_label", grupo["label"]))
            regiao = mapa_regiao.get(mid, (None, "?"))[1]
            if regiao not in CINCO:
                continue
            for tipo in censo_dex.TIPOS_SELVAGEM:
                if tipo not in enc:
                    continue
                mons = enc[tipo]["mons"]
                vistos, dup = set(), []
                perfil = collections.Counter()
                for i, m in enumerate(mons):
                    e = cat.get(m["species"])
                    if e:
                        perfil.update(e.tipos)
                    if m["species"] in vistos:
                        dup.append(i)
                    vistos.add(m["species"])
                if dup:
                    fora.append(dict(mapa=mid, tipo=tipo, regiao=regiao,
                                     perfil=perfil, dup=dup, n=len(mons)))
    return fora


_CAT = {}


def catalogo_completo():
    if not _CAT:
        c = catalogo_especies.carrega()
        c.update(censo_dex.entradas_macro(c))
        _CAT.update(c)
    return _CAT


# ---------------------------------------------------------------------- plano

def _fecha(seeds, evo, fmc):
    """Fecho de alcancabilidade: evolucao que roda no jogo solo + troca de forma
    que NAO reverte. E a mesma regra que `censo_dex.censo()` usa para decidir
    entre `evolucao`/`forma_permanente`/`forma_batalha` e `inobtenivel`; se as
    duas discordarem, o censo manda e este fecho e que esta errado."""
    alc = set(seeds)
    mudou = True
    while mudou:
        mudou = False
        for alvo, origens in evo.items():
            if alvo in alc:
                continue
            for de, met, _p, cond in origens:
                if de in alc and not censo_dex._evo_travada(met, cond):
                    alc.add(alvo)
                    mudou = True
                    break
        for alvo, origens in fmc.items():
            if alvo in alc:
                continue
            for de, t_, _p in origens:
                if t_ not in censo_dex.FORMA_REVERTE and de in alc:
                    alc.add(alvo)
                    mudou = True
                    break
    return alc


def _origens(nome, evo, fmc):
    fora = {de for de, met, _p, cond in evo.get(nome, [])
            if not censo_dex._evo_travada(met, cond)}
    fora |= {de for de, t_, _p in fmc.get(nome, [])
             if t_ not in censo_dex.FORMA_REVERTE}
    return fora


def censo_base():
    """O censo como se ESTA ferramenta nunca tivesse rodado.

    Sem isto, `--tabela` nao e idempotente e a segunda rodada e destrutiva: o
    censo leria o `wild_encounters.json` JA escrito, veria as 233 especies novas
    como obteniveis e as apagaria da tabela de decisao, que e a fonte da verdade
    da onda B. Aconteceu de verdade em 21/08/2026, e a tabela caiu de 475 para
    154 linhas sem nenhum erro na tela.

    Duas desmontagens, e as duas leem a propria tabela gravada:
    1. o mato volta ao baseline pela coluna `substituido` (ver `encontros_base`);
    2. `givemon`/`seteventmon` de especie QUE ESTA NA TABELA sao ignorados. Toda
       especie da tabela estava `inobtenivel` por definicao, entao nenhuma delas
       tinha script antes; nao ha como esse filtro apagar fonte alheia.
    """
    sel, varre = censo_dex.selvagem, censo_dex._varre_scripts
    evo_orig = censo_dex.evolucoes

    def selvagem_base(mapa_regiao):
        d = encontros_base()
        fora = collections.defaultdict(list)
        for grupo in d["wild_encounter_groups"]:
            frontier = not grupo.get("for_maps")
            for enc in grupo["encounters"]:
                mid = enc.get("map", enc.get("base_label", grupo["label"]))
                regiao = ("Frontier" if frontier
                          else mapa_regiao.get(mid, (None, "?"))[1])
                for tipo in censo_dex.TIPOS_SELVAGEM:
                    if tipo not in enc:
                        continue
                    for mon in enc[tipo]["mons"]:
                        fora[mon["species"]].append(
                            (mid, regiao, tipo, mon["min_level"], mon["max_level"]))
        return fora

    gravada = tabela_gravada()
    nossas = {l["especie"] for k in BUCKETS for l in gravada.get(k, [])}

    def varre_base():
        return [x for x in varre() if x[3] not in nossas]

    def evolucoes_base():
        # 3. as duas segundas linhas `EVO_ITEM` que `--motor` escreve tambem
        #    saem: com elas no lugar, Escavalier e Accelgor deixam de ser
        #    inobteniveis e SUMIRIAM da tabela na segunda rodada.
        e = evo_orig()
        for _arq, de, alvo in EVO_ITEM_NOVAS:
            e[alvo] = [x for x in e.get(alvo, [])
                       if x[:3] != (de, "EVO_ITEM", "ITEM_LINKING_CORD")]
        return e

    censo_dex.selvagem = selvagem_base
    censo_dex._varre_scripts = varre_base
    censo_dex.evolucoes = evolucoes_base
    try:
        return censo_dex.censo()
    finally:
        censo_dex.selvagem, censo_dex._varre_scripts = sel, varre
        censo_dex.evolucoes = evo_orig


_PLANO = {}


def plano():
    """A tabela de decisao inteira. Deterministica: mesma arvore, mesma saida."""
    if _PLANO:
        return _PLANO
    linhas = censo_base()
    por_nome = {l.nome: l for l in linhas}
    cat = catalogo_completo()
    evo = censo_dex.evolucoes()
    fmc = censo_dex.formas()
    # As duas linhas EVO_ITEM que `--motor` escreve entram JA no fecho: sem
    # isso o plano daria linha de mato a Escavalier e Accelgor sem precisar.
    for _arq, de, alvo in EVO_ITEM_NOVAS:
        evo.setdefault(alvo, []).append((de, "EVO_ITEM", "ITEM_LINKING_CORD", ""))

    ino = [l for l in linhas if l.categoria == "inobtenivel"]
    nomes_ino = {l.nome for l in ino}
    ja = {l.nome for l in linhas if l.categoria != "inobtenivel"}

    presentes = sorted(
        n for n in nomes_ino
        if n in INICIAIS_HOENN or PRESENTE_SEM_OVERWORLD.match(n))
    estaticos = sorted(
        (n for n in nomes_ino if por_nome[n].lenda and por_nome[n].base),
        key=lambda n: cat[n].dex)

    # Quem sai de graca quando estatico e presente entrarem; o que sobra vira
    # fonte direta, rodada a rodada, sempre pelas RAIZES (quem nao depende de
    # ninguem que ainda esteja faltando). Assim Gourgeist-Grande so ganha linha
    # propria se o Pumpkaboo-Grande tambem nao tiver de onde vir.
    #
    # A regra 7 vale para FORMA tambem, e nao so para especie-base: as 10 formas
    # de lenda que o efeito cascata nao resolve (os tres passaros de Galar, as
    # duas fusoes do Kyurem, as duas do Necrozma, as duas do Calyrex e o Magearna
    # Original) viram ESTATICO, nunca mato. As duas sem gfx de overworld
    # (Eternamax e Zarude-Dada) nao podem ser objeto e caem no `givemon`.
    diretos = set(presentes) | set(estaticos)
    selvagens = []
    while True:
        alc = _fecha(ja | diretos, evo, fmc)
        falta = nomes_ino - alc - diretos
        if not falta:
            break
        raizes = {n for n in falta if not (_origens(n, evo, fmc) & falta)}
        if not raizes:
            raizes = falta          # ciclo puro: todos viram raiz
        for n in sorted(raizes, key=lambda n: (cat[n].dex, n)):
            if not por_nome[n].lenda:
                selvagens.append(n)
            elif por_nome[n].ow:
                estaticos.append(n)
            else:
                presentes.append(n)
        diretos |= raizes
    estaticos.sort(key=lambda n: cat[n].dex)
    presentes.sort(key=lambda n: cat[n].dex)

    _PLANO["npcs_presente"] = decide_npcs_presente()
    _PLANO["estaticos"] = decide_estaticos(estaticos, cat)
    _PLANO["selvagens"] = decide_selvagem(selvagens, cat)
    _PLANO["presentes"] = decide_presentes(presentes, cat)
    resolvidos = {l["especie"] for k in ("estaticos", "selvagens", "presentes")
                  for l in _PLANO[k]}
    _PLANO["evolucoes"] = [
        dict(especie=n, como="evolucao", regiao="", mapa="", metodo="",
             slot=None, nivel=0, flag="",
             origem="censo",
             nota="sai de graca no efeito cascata: " + "; ".join(
                 sorted(x.replace("SPECIES_", "")
                        for x in _origens(n, evo, fmc)) or ["troca de forma"]))
        for n in sorted(nomes_ino - resolvidos, key=lambda n: (cat[n].dex, n))]
    return _PLANO


def flag_de(nome):
    return "FLAG_HIDE_DEX_" + nome.replace("SPECIES_", "")


_REGIAO_MAPA = {}


def regiao_do_mapa(pasta):
    """A regiao de uma PASTA de mapa, pela mesma regua do completude.py."""
    if not _REGIAO_MAPA:
        g = json.load(open(f"{RAIZ}/data/maps/map_groups.json"))
        for grp in g["group_order"]:
            for m in g[grp]:
                _REGIAO_MAPA[m] = censo_dex._regiao_de(m, grp)
    return _REGIAO_MAPA.get(pasta, "?")


_CABE = {}


def lotacao(pontos):
    """Quantos objetos caem, no PIOR caso, dentro de UMA janela de sprite.

    Varre a janela por todas as ancoras que importam (as coordenadas dos
    proprios objetos: qualquer janela cheia pode ser empurrada ate encostar num
    objeto sem perder nenhum). E deliberadamente pessimista, porque nao exige
    que exista tile andavel para o jogador naquela ancora: errar para o lado de
    sobrar sprite custa um reposicionamento, errar para o outro custa um
    lendario invisivel que nenhum teste de compilacao acha.
    """
    if not pontos:
        return 0
    W, H = JANELA_SPRITE
    return max(sum(1 for x, y in pontos if xl <= x < xl + W and yt <= y < yt + H)
               for xl in {p[0] for p in pontos} for yt in {p[1] for p in pontos})


def _objetos_do_mapa(d):
    """Os objetos que JA estao no mapa e nao vieram desta ferramenta."""
    return [(o["x"], o["y"]) for o in d.get("object_events", [])
            if o.get("origem") != MARCA]


_ROTA_LS = {}


def rota_dos_lendarios_sinnoh(mapa):
    """Os tiles que o T123 PISA neste mapa. Sao parede para o estatico novo.

    Medido em 21/08/2026: com os 106 estaticos aplicados, T123.9, T123.10,
    T123.13 e T123.14 reprovaram, porque um estatico da dex caiu em cima da
    caminhada do Regigigas (SnowpointTempleB5F) e da do Shaymin (FloaromaTown).
    Nao ilhar tile nenhum nao basta: caso de emulador ja escrito e uma rota
    exata, e objeto novo no meio dela para o jogador antes da hora.

    Inclui `vazio`, o tile em que o PAR NEGATIVO para, porque ele anda um tile
    alem do lendario.
    """
    if mapa not in _ROTA_LS:
        fora = set()
        for L, e in LS.plano():
            if L["mapa"] != mapa:
                continue
            x, y = e["pouso"]
            fora.add((x, y))
            for D, n, _sat in e["rota"]:
                dx, dy = LS.DIRS[D]
                for _ in range(n):
                    x, y = x + dx, y + dy
                    fora.add((x, y))
            fora.add(tuple(e["para"]))
            fora.add(tuple(e["vazio"]))
        _ROTA_LS[mapa] = fora
    return _ROTA_LS[mapa]


_CORREDOR = {}


def corredor_de_casos(mapa):
    """Os tiles que QUALQUER caso critico ja escrito anda neste mapa.

    A rede que pega o que o `rota_dos_lendarios_sinnoh` nao pega: T124.11,
    T124.13 e T124.14 reprovaram em 21/08/2026 porque um estatico da dex caiu
    na coluna que o caso do Giratina desce no Distortion World, e esse caso nao
    sai de gerador nenhum, sai de um JSON escrito a mao.

    Le o roteiro do proprio caso e refaz a caminhada sobre a grade de colisao. E
    aproximacao POR CIMA de proposito (anda os K toques inteiros em vez de K-1,
    e nao entende porta nem seta): reservar tile demais custa um estatico em
    outro canto do mapa, reservar de menos custa um caso reprovado que ninguem
    liga a esta rodada.

    CIRCULARIDADE, consertada em 21/08/2026: os arquivos de caso 129 e 131 a 135
    sao ESCRITOS a partir desta tabela, depois que ela ja existe. Le-los aqui
    faz o `plano()` de uma segunda rodada reservar os corredores que ele mesmo
    criou e mudar de decisao (Kanto ia de 15 estaticos para 16, Johto de 22 para
    30), e o `--demo` reprovava comparando a tabela gravada com um plano que
    nunca poderia bater. Arquivo derivado desta tabela nao entra na conta.
    """
    if mapa in _CORREDOR:
        return _CORREDOR[mapa]
    d = json.load(open(f"{RAIZ}/data/maps/{mapa}/map.json", encoding="utf-8"))
    const, fora = d["id"], set()
    W, H, g = LS.grade(d["layout"])
    for arq in sorted(glob.glob(f"{RAIZ}/dev_scripts/testes_criticos/*.json")):
        if CASOS_DERIVADOS.match(os.path.basename(arq)):
            continue
        for c in json.load(open(arq, encoding="utf-8")):
            prova = c.get("prova") or {}
            if prova.get("mapa") == const and prova.get("pos"):
                fora.add(tuple(prova["pos"]))
            if c.get("warp") != const:
                continue
            w = d.get("warp_events", [])[c.get("warp_id", 0)]
            x, y = w["x"], w["y"]
            fora.add((x, y))
            fora.add((x, y + 1))
            for passo_txt in (c.get("roteiro") or "").split(","):
                alvo = passo_txt.split(":")[-1]
                D_, _, n_ = alvo.partition("*")
                if D_ not in LS.DIRS:
                    continue
                dx, dy = LS.DIRS[D_]
                for _ in range(int(n_ or 1)):
                    nx, ny = x + dx, y + dy
                    if LS.passo(W, H, g, nx, ny, LS.elev(g[y][x]), ()) is None:
                        break
                    x, y = nx, ny
                    fora.add((x, y))
    _CORREDOR[mapa] = fora
    return fora


def visao_de_treinador(d):
    """Os tiles em que um treinador VE o jogador, e por isso a rota nao pisa.

    Medido em 21/08/2026 no MtPyre_Summit: a rota subia a coluna 24 e o jogador
    parava em (24,18), quatorze tiles antes do lendario, porque o Aqua Member de
    (25,18) puxava batalha. A busca em largura julga colisao, elevacao e corpo
    de NPC; linha de visao ela nao via, e caso que atravessa linha de visao nao
    falha por acaso, falha sempre.

    O raio vai nas QUATRO direcoes, e nao so na que o `movement_type` diz: NPC
    que anda vira de lado, e o custo de proibir 4 raios curtos e uma rota um
    pouco mais longa, nao um mapa a menos.
    """
    fora = set()
    for o in d.get("object_events", []):
        if o.get("trainer_type", "TRAINER_TYPE_NONE") == "TRAINER_TYPE_NONE":
            continue
        try:
            alcance = int(str(o.get("trainer_sight_or_berry_tree_id", "0")), 0)
        except ValueError:
            alcance = 0
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            for k in range(1, alcance + 1):
                fora.add((o["x"] + dx * k, o["y"] + dy * k))
    return fora


def cabe(mapa, usados):
    """Existe tile para MAIS UM estatico neste mapa? Medido, nunca estimado.

    E a mesma busca em largura do `lendarios_sinnoh` (colisao E elevacao, o
    portao de nao-ilhar, distancia de NPC que anda). Existe porque o tamanho do
    mapa NAO diz nada: `MtEmber_Summit_Frlg` e um cume grande e nao cabe nenhum,
    e `Unova_VictoryRoadCave3F` cabe ZERO.

    Alem dos portoes da geometria, um SEGUNDO teto: o tile escolhido nao pode
    fazer nenhuma janela de 20x17 passar de 15 objetos (ver TETO_SPRITE). Tile
    reprovado vira parede e a busca roda de novo, entao quem estoura a janela e
    reposicionado pelo GERADOR, dentro do mesmo mapa, antes de tentar o proximo
    da lista de preferencia.

    Devolve o plano inteiro do `lendarios_sinnoh.planeja` (tile, warp, rota,
    tile de parada e tile vazio do par negativo), ou None.
    """
    chave = (mapa, tuple(sorted(usados)))
    if chave not in _CABE:
        _CABE[chave] = _planeja_com_teto(mapa, usados)
    return _CABE[chave]


def _planeja_com_teto(mapa, usados):
    try:
        d = json.load(open(f"{RAIZ}/data/maps/{mapa}/map.json", encoding="utf-8"))
    except OSError:
        return None
    fixos = _objetos_do_mapa(d)
    if len(fixos) + len(usados) + 1 > TETO_OBJETOS:
        return None
    warps = max(1, len(d.get("warp_events", [])))
    olhos = (visao_de_treinador(d) | rota_dos_lendarios_sinnoh(mapa)
             | corredor_de_casos(mapa))
    vetados = set()
    while True:
        achou = None
        for w in range(warps):
            achou = LS.planeja(mapa, w, extra=set(usados) | vetados | olhos,
                               longe=set(usados), ignora=(MARCA,))
            if achou is not None:
                break
        if achou is None:
            return None
        if lotacao(fixos + list(usados) + [achou["T"]]) <= TETO_SPRITE:
            return achou
        vetados.add(achou["T"])


def rota_entre_vizinhos(mapa, alvo, irmaos):
    """A rota ate `alvo` com TODOS os outros estaticos do mapa como parede.

    Segunda passada, e ela existe por um defeito medido em 21/08/2026: na
    primeira passada o estatico numero i so enxerga os i-1 anteriores, entao a
    rota dele podia atravessar o tile do numero i+1, que ainda nao existia. Em
    MtCoronet_B1F o jogador subia a coluna 2 e batia no Poipole 50 tiles antes
    do Volcanion; em Unova_VictoryRoadCave2F ele batia no Walking Wake.

    O TILE nao muda (ele ja passou por todos os portoes na primeira passada);
    muda so o caminho ate ele. Devolve None quando nao ha caminho limpo, e ai
    quem chama fica com a rota da primeira passada e diz isso em voz alta.
    """
    d = json.load(open(f"{RAIZ}/data/maps/{mapa}/map.json", encoding="utf-8"))
    parede = (set(irmaos) | visao_de_treinador(d)
              | rota_dos_lendarios_sinnoh(mapa) | corredor_de_casos(mapa))
    # 4 pernas e o padrao do T123 e resolve quase tudo; 6 e 8 existem so para os
    # mapas apertados, onde os proprios irmaos viraram labirinto (as 12 Ultra
    # Beasts do MtCoronet_B1F ficam na mesma coluna, e passar por elas exige
    # contornar cada uma). Custam tempo, entao so rodam quando 4 nao acha.
    for pernas in (4, 6, 8):
        for w in range(max(1, len(d.get("warp_events", [])))):
            e = LS.planeja(mapa, w, extra=parede, ignora=(MARCA,), alvo=alvo,
                           max_pernas=pernas)
            if e is not None:
                return e
    return None


def _encaixa(preferidos, usados, existem):
    """O primeiro mapa da lista que ainda tem tile. Devolve (mapa, plano)."""
    for m in preferidos:
        if m not in existem:
            continue
        e = cabe(m, usados.get(m, ()))
        if e is not None:
            return m, e
    return None, None


def _geometria(e):
    """A geometria do `lendarios_sinnoh.planeja` em JSON, na MESMA forma que os
    `npcs_presente` ja usam.

    Ela mora na tabela e nao e recalculada na hora de aplicar por um motivo
    medido: o `planeja` le os objetos do map.json e trata todos como parede,
    entao depois da PRIMEIRA aplicacao o tile escolhido ja e parede e a busca
    devolveria outro. Recalcular na aplicacao faz `--estaticos` mudar de
    resposta a cada rodada, que e o oposto de idempotente. A tabela e a decisao;
    quem quiser mover um estatico roda `--tabela` de novo.
    """
    return dict(warp=e["warp"], dir=e["dir"],
                para=list(e["para"]), vazio=list(e["vazio"]),
                porta=list(e["porta"]), pouso=list(e["pouso"]),
                rota=[[D, n, sat] for D, n, sat in e["rota"]])


def decide_estaticos(nomes, cat):
    """Lenda nunca vai para o mato (regra 7). Lar canonico primeiro (regra 8).

    Tres excecoes deliberadas, decididas pelo condutor a partir da pesquisa de
    rom hacks: as 11 Ultra Beasts vao para UMA zona so (Radical Red poe as 11
    em Cerulean Cave 2F) e os 20 Paradox vao para DUAS salas de Victory Road
    (Elite Redux faz igual). Sao 31 objetos que viram 3 mapas em vez de 31.

    O mapa escolhido e SEMPRE conferido por busca em largura antes de entrar na
    tabela. Sem essa conferencia a tabela prometia 16 estaticos em mapas onde
    nenhum tile passa nos portoes, e quem descobria era o executor da onda B.
    """
    pesq = pesquisa_lendarios(set(cat))
    existem = mapas_existentes()
    cota = collections.Counter()
    usados = collections.defaultdict(set)
    fora = []
    for n in nomes:
        curto = n.replace("SPECIES_", "")
        if any(curto == u or curto.startswith(u + "_") for u in UB):
            pref, origem = list(ZONA_UB), "pesquisa"
        elif any(curto == p or curto.startswith(p + "_") for p in PARADOX):
            futuro = curto.startswith("IRON_")
            pref = list(SALA_PARADOX_FUTURO if futuro else SALA_PARADOX_ANTIGO)
            origem = "pesquisa"
        elif n in pesq:
            pref, origem = [pesq[n][1]], "pesquisa"
        else:
            pref, origem = [], "bioma"
        b = bioma_de(cat[n].tipos)
        # A cauda da lista de preferencia e sempre a mesma: o bioma da especie
        # (a regiao com menos estatico primeiro) e depois a reserva inteira.
        pref += [m for _c, _r, m in sorted(
            (cota[r], r, m) for r, m in BIOMA[b].items() if m in existem)]
        pref += sorted(POOL, key=lambda m: (cota[regiao_do_mapa(m)], m))
        mapa, e = _encaixa(pref, usados, existem)
        if mapa is None:
            raise SystemExit(f"{n}: nenhum mapa da preferencia nem da reserva "
                             "tem tile livre. Pare e meca.")
        if mapa != pref[0]:
            origem = "bioma"
        regiao = regiao_do_mapa(mapa)
        usados[mapa].add(e["T"])
        cota[regiao] += 1
        fora.append(dict(especie=n, como="estatico", regiao=regiao, mapa=mapa,
                         metodo="objeto+script", slot=None, nivel=nivel_de(n),
                         flag=flag_de(n), origem=origem,
                         tile=list(e["T"]),
                         nota=f"gen {cat[n].gen}; tipos "
                              f"{'/'.join(t.replace('TYPE_', '') for t in cat[n].tipos)}",
                         **_geometria(e)))
    # SEGUNDA PASSADA: a rota de cada um, agora com TODOS os irmaos do mapa
    # como parede. Ver `rota_entre_vizinhos`.
    por_mapa = collections.defaultdict(list)
    for l in fora:
        por_mapa[l["mapa"]].append(l)
    for mapa, irmaos in por_mapa.items():
        if len(irmaos) < 2:
            irmaos[0]["rota_irmas"] = True
            continue
        tiles = [tuple(l["tile"]) for l in irmaos]
        for l in irmaos:
            meu = tuple(l["tile"])
            e = rota_entre_vizinhos(mapa, meu, [t for t in tiles if t != meu])
            if e is None:
                # A rota da 1a passada fica, e a linha diz que ela atravessa
                # irmao. Caso de emulador escrito em cima dela NASCE reprovado:
                # quem for escrever os 101 casos le este campo antes.
                l["rota_irmas"] = False
                continue
            l.update(_geometria(e))
            l["rota_irmas"] = True

    # `vazio` (onde o PAR NEGATIVO para) tem que sair so de parede DE VERDADE.
    # A busca usa paredes virtuais (linha de visao de treinador, rota do T123,
    # corredor de caso critico) para escolher por onde andar, e elas nao param
    # o jogador: com a flag de HIDE acesa ele escorrega ALEM delas. Medido em
    # 21/08/2026 no T129.14, que esperava (2,59) e viu (2,60), um tile alem da
    # rota do Heatran.
    for mapa, irmaos in por_mapa.items():
        d = json.load(open(f"{RAIZ}/data/maps/{mapa}/map.json", encoding="utf-8"))
        W, H, g = LS.grade(d["layout"])
        reais = set(_objetos_do_mapa(d)) | {tuple(l["tile"]) for l in irmaos}
        for l in irmaos:
            px, py = l["para"]
            # O proprio bicho esta ESCONDIDO no par negativo, entao o tile dele
            # nao e parede nessa passagem.
            bloq = reais - {tuple(l["tile"])}
            c = LS.escorrega(W, H, g, bloq, px, py, LS.elev(g[py][px]), l["dir"])
            if not c:
                continue
            velho, novo = tuple(l["vazio"]), (c[-1][0], c[-1][1])
            if velho == novo:
                continue
            l["vazio"] = list(novo)
            # A ULTIMA perna tem que crescer junto. Ela e saturante, entao no
            # caso POSITIVO o toque a mais nao anda nada (o bicho segura o
            # jogador em `para`); no NEGATIVO, sem os toques novos, o jogador
            # para no meio do escorregao e o caso reprova por um tile que ele
            # nunca teve como alcancar.
            dx, dy = LS.DIRS[l["dir"]]
            n_velho = l["rota"][-1][1]
            ini = (velho[0] - dx * n_velho, velho[1] - dy * n_velho)
            l["rota"][-1][1] = abs(novo[0] - ini[0]) + abs(novo[1] - ini[1])

    fim = FLAG_BASE + len(fora) - 1
    if fim > FLAG_TETO:
        raise SystemExit(f"{len(fora)} estaticos nao cabem em "
                         f"0x{FLAG_BASE:04X}-0x{FLAG_TETO:04X}: peca outra faixa.")
    return fora


BUCKETS = ("estaticos", "selvagens", "presentes", "evolucoes")


def decide_npcs_presente():
    """Onde os dois NPCs de presente ficam, e a rota do caso de suite ate eles.

    Regra deliberadamente mais estreita que a do estatico: cada NPC fica na
    MESMA COLUNA de um warp, dois tiles acima dele. A rota do caso vira uma
    perna so, `UP` saturando contra o NPC, e nao depende de para onde o motor
    deixa o boneco olhando depois do warp.

    A razao e medida, nao estetica. A rota generica do `lendarios_sinnoh`
    (`DOWN` zerando, `LEFT` duas casas, `UP` dez) foi para o emulador e o
    jogador NAO andou para o lado: em (6,12), que e TILE DE PORTA, o passo
    lateral nao acontece, e ele acabou subindo pela propria coluna. A busca em
    largura julga colisao e elevacao, que e uma camada mais rasa do que a do
    motor de porta; em vez de remendar a busca (que o T123 ja usa e ja prova),
    esta ferramenta escolhe um tile onde as duas camadas concordam.

    Alcancabilidade e nao-ilhamento continuam MEDIDOS, com a mesma
    `lendarios_sinnoh.alcance`.
    """
    antigo = tabela_gravada().get("npcs_presente")
    if antigo:
        return antigo
    d, W, H, g, objs, _m, _w = LS.contexto(MAPA_PRESENTE)
    sementes = LS.sementes_dos_warps(d, W, H, g)
    base = LS.alcance(W, H, g, sementes, objs)
    warps = d.get("warp_events", [])
    fora, tomados = [], set()
    for papel in ("iniciais", "evento"):
        achou = None
        for wid, w in enumerate(warps):
            wx, wy = w["x"], w["y"]
            parada, tile = (wx, wy - 1), (wx, wy - 2)
            if wy < 2 or tile in tomados or parada in tomados:
                continue
            if not (LS.anda(g[parada[1]][parada[0]])
                    and LS.anda(g[tile[1]][tile[0]])):
                continue
            if tile in objs or parada in objs or tile not in base:
                continue
            # Por o NPC ali nao pode ilhar tile nenhum do mapa.
            if LS.alcance(W, H, g, sementes, objs | tomados | {tile}) != \
                    base - tomados - {tile}:
                continue
            achou = dict(papel=papel, mapa=MAPA_PRESENTE, tile=list(tile),
                         warp=wid, para=list(parada),
                         vazio=list(parada), dir="UP",
                         rota=[["UP", 1, True]])
            break
        if achou is None:
            raise SystemExit(f"{MAPA_PRESENTE}: nao ha coluna de warp livre "
                             f"para o NPC de {papel}. Pare e meca.")
        tomados |= {tuple(achou["tile"]), tuple(achou["para"])}
        fora.append(achou)
    return fora


def decide_presentes(nomes, cat):
    fora = []
    for n in nomes:
        inicial = n in INICIAIS_HOENN
        fora.append(dict(
            especie=n, como="presente", regiao="Hoenn",
            mapa="LittlerootTown_ProfessorBirchsLab",
            metodo="multichoice" if inicial else "givemon",
            slot=None, nivel=5, flag="", origem="censo",
            nota=("inicial de Hoenn: o Birch entrega um dos tres a escolha"
                  if inicial else
                  "sem gfx de overworld (nao pode ser estatico): givemon por NPC")))
    return fora


def decide_selvagem(nomes, cat):
    """Bioma pelo PERFIL DE TIPOS da propria tabela (regra 4), com cota (5),
    agua separada de terra (6) e rodizio de regiao para cosmetico (10)."""
    tabelas = tabelas_de_encontro(censo_dex.mapas())
    livres = {(t["mapa"], t["tipo"]): list(t["dup"]) for t in tabelas}
    usos = collections.Counter()
    cota = collections.Counter()
    ordem_cosmetica = collections.Counter()
    fora = []
    for n in nomes:
        e = cat[n]
        tipos = set(e.tipos)
        grupo = AGUA if "TYPE_WATER" in tipos else TERRA
        if eh_cosmetica(n):
            fam = _familia(n)
            pin = [CINCO[ordem_cosmetica[fam] % len(CINCO)]]
            ordem_cosmetica[fam] += 1
            permitidas, origem = pin, "bioma"
        elif eh_regional(n) or e.gen >= 6:
            permitidas, origem = list(CINCO), "bioma"
        else:
            permitidas, origem = [REGIAO_DA_GEN[e.gen]], "censo"
        alvo = _melhor_tabela(tabelas, livres, usos, cota, permitidas, grupo, tipos)
        if alvo is None and permitidas != list(CINCO):
            # A regiao pedida nao tem tabela do tipo certo com slot livre.
            # Dito no `origem`, nunca em silencio.
            alvo = _melhor_tabela(tabelas, livres, usos, cota, list(CINCO),
                                  grupo, tipos)
            origem = "bioma"
        if alvo is None:
            raise SystemExit(f"{n}: acabaram os slots duplicados de "
                             f"{'/'.join(grupo)}. Pare e meca.")
        t, slot, (nivel, antes) = alvo
        cota[t["regiao"]] += 1
        usos[(t["mapa"], t["tipo"])] += 1
        fora.append(dict(especie=n, como="selvagem", regiao=t["regiao"],
                         mapa=t["mapa"], metodo=t["tipo"], slot=slot,
                         nivel=nivel, flag="", origem=origem,
                         substituido=antes,
                         nota=f"gen {e.gen}; tipos "
                              f"{'/'.join(x.replace('TYPE_', '') for x in e.tipos)}; "
                              f"slot duplicado {slot} de {t['n']}"))
    return fora


def _melhor_tabela(tabelas, livres, usos, cota, permitidas, grupo, tipos):
    melhor = None
    for t in tabelas:
        if t["regiao"] not in permitidas or t["tipo"] not in grupo:
            continue
        chave = (t["mapa"], t["tipo"])
        if not livres[chave] or usos[chave] >= 3:
            continue
        pontos = sum(t["perfil"][x] for x in tipos)
        ordem = (-pontos, cota[t["regiao"]], usos[chave], t["mapa"], t["tipo"])
        if melhor is None or ordem < melhor[0]:
            melhor = (ordem, t, chave)
    if melhor is None:
        return None
    _o, t, chave = melhor
    slot = livres[chave].pop(0)
    return t, slot, _nivel_do_slot(t["mapa"], t["tipo"], slot)


_JSON_CACHE = {}


def _nivel_do_slot(mapa, tipo, slot):
    """Nivel da linha nova = o do slot que ela ocupa (regra 1). Nao ha "nivel
    da fonte" para uma especie que a fonte nunca pos ali; herdar o do slot e o
    que mantem a curva da regiao intacta."""
    if not _JSON_CACHE:
        _JSON_CACHE.update(_indice(encontros_base()))
    m = _JSON_CACHE[(mapa, tipo)][slot]
    return [m["min_level"], m["max_level"]], m["species"]


# -------------------------------------------------------------------- escrita

def escreve_tabela(gravar):
    # GUARDA que nasceu de um estrago de verdade (21/08/2026): apagar a tabela e
    # rodar `--tabela` de novo com o mato JA escrito cospe um plano truncado, sem
    # UMA mensagem de erro. O `censo_base` desmonta o que foi aplicado usando a
    # PROPRIA tabela; sem ela, nao ha como desmontar, e as 233 especies ja
    # escritas aparecem como obteniveis e somem da decisao.
    if not os.path.exists(TABELA) and MARCA_INI in open(FLAGS_H,
                                                        encoding="utf-8").read():
        raise SystemExit(
            "dex_distribuicao.json nao existe, mas o bloco de flags desta "
            "ferramenta JA esta no flags.h: alguma coisa ja foi aplicada e a "
            "tabela e a unica testemunha de qual era o baseline.\n"
            "Restaure a tabela (git) OU desfaca as aplicacoes "
            "(git checkout src/data/wild_encounters.json "
            "src/data/pokemon/species_info/gen_5_families.h "
            "data/maps/LittlerootTown_ProfessorBirchsLab include/constants/flags.h)"
            " antes de gerar de novo.")
    p = plano()
    d = {
        "gerado_por": "dev_scripts/distribui_dex.py --tabela",
        "leia_antes": "PLANO-DEX.md secao 3. Uma linha por entrada que estava "
                      "INOBTENIVEL no censo. `como` diz o caminho, `origem` diz "
                      "de onde a decisao saiu: censo (regra mecanica), pesquisa "
                      "(lendarios_referencia.csv) ou bioma (perfil de tipos).",
        "flag_base": f"0x{FLAG_BASE:04X}",
        "totais": {k: len(p[k]) for k in BUCKETS},
        **p,
    }
    novo = json.dumps(d, indent=2, ensure_ascii=False) + "\n"
    velho = open(TABELA, encoding="utf-8").read() if os.path.exists(TABELA) else ""
    if novo == velho:
        return []
    if gravar:
        open(TABELA, "w", encoding="utf-8").write(novo)
    return [f"dex_distribuicao.json: {sum(len(p[k]) for k in BUCKETS)} linhas "
            f"({', '.join(f'{k} {len(p[k])}' for k in BUCKETS)})"]


def aplica_selvagem(gravar):
    """Escreve as linhas de mato em slot DUPLICADO. Idempotente por baseline."""
    d = encontros_base()
    idx = _indice(d)
    conta = collections.Counter()
    for l in tabela()["selvagens"]:
        mons = idx[(l["mapa"], l["metodo"])]
        alvo = mons[l["slot"]]
        if alvo["species"] != l["substituido"]:
            raise SystemExit(
                f"{l['especie']}: o slot {l['slot']} de {l['mapa']}/{l['metodo']} "
                f"tem {alvo['species']} e a tabela diz que tinha "
                f"{l['substituido']}. Alguem mexeu no wild_encounters.json por "
                "fora; refaca a tabela com --tabela antes de aplicar.")
        alvo["species"] = l["especie"]
        conta[(l["regiao"], l["metodo"])] += 1
    # A comparacao e contra o ARQUIVO, e nao contra o baseline em memoria: o
    # baseline ja vem desmontado por `encontros_base`, entao ele SEMPRE difere
    # do resultado, e comparar com ele faria a ferramenta dizer que escreveu
    # mesmo quando nada mudou no disco.
    novo = json.dumps(d, indent=2, ensure_ascii=False) + "\n"
    if novo == open(ENCONTROS, encoding="utf-8").read():
        return []
    if gravar:
        open(ENCONTROS, "w", encoding="utf-8").write(novo)
    return [f"wild_encounters.json: {sum(conta.values())} linhas ("
            + ", ".join(f"{r}/{t.replace('_mons', '')} {n}"
                        for (r, t), n in sorted(conta.items())) + ")"]


_TABELA = {}


def tabela_gravada():
    """A decisao COMO ESTA NO DISCO, ou {} se ainda nao foi gerada.

    Nunca chama `plano()`: quem monta o plano precisa dela para desmontar o que
    ja foi aplicado, e uma coisa chamando a outra e recursao infinita (foi o que
    aconteceu em 21/08/2026 na primeira versao).
    """
    if not _TABELA and os.path.exists(TABELA):
        _TABELA.update(json.load(open(TABELA, encoding="utf-8")))
    return _TABELA


def tabela():
    """A decisao gravada, ou o plano em memoria quando ainda nao ha arquivo."""
    d = tabela_gravada()
    if not d:
        _TABELA.update(plano())
    return _TABELA


def bloco_de_flags():
    est = tabela()["estaticos"]
    out = [MARCA_INI,
           "// Uma flag de HIDE por estatico da Dex completa, na CAUDA da maior",
           "// faixa livre (0x20D2-0x321F, medida por dev_scripts/flags_livres.py);",
           "// logo acima moram as 11 do dev_scripts/lendarios_sinnoh.py.",
           "// Todas alocadas de uma vez, aqui, para que os executores de cada",
           "// regiao NAO disputem este arquivo na hora de escrever o estatico.",
           "// Apelidar FLAG_UNUSED nao mexe em FLAGS_COUNT: a save nao muda.",
           "// Gerado por dev_scripts/distribui_dex.py; nao editar a mao."]
    larg = max(len(l["flag"]) for l in est) + 2
    for i, l in enumerate(est):
        out.append("#define %-*s FLAG_UNUSED_0x%04X  // %s, %s"
                   % (larg, l["flag"], FLAG_BASE + i, l["regiao"], l["mapa"]))
    out.append("#define %-*s FLAG_UNUSED_0x%04X  // Birch ja entregou o inicial"
               % (larg, "FLAG_DEX_PRESENTE_INICIAL", FLAG_PRESENTE_INICIAL))
    out.append("#define %-*s FLAG_UNUSED_0x%04X  // os event-only ja foram dados"
               % (larg, "FLAG_DEX_PRESENTE_EVENTO", FLAG_PRESENTE_EVENTO))
    out.append(MARCA_FIM)
    return "\n".join(out) + "\n"


def aplica_flags(gravar):
    fl = open(FLAGS_H, encoding="utf-8").read()
    novo = LS.substitui(fl, MARCA_INI, MARCA_FIM, bloco_de_flags())
    if novo == fl:
        return []
    if gravar:
        open(FLAGS_H, "w", encoding="utf-8").write(novo)
    est = tabela()["estaticos"]
    return [f"flags.h: {len(est)} apelidos FLAG_HIDE_DEX_* em "
            f"0x{FLAG_BASE:04X}-0x{FLAG_BASE + len(est) - 1:04X}"]


# ------------------------------------------------------- conserto de motor

MOTOR_INI = "    // >>> Dex completa: as outras regioes (dev_scripts/distribui_dex.py) >>>"
MOTOR_FIM = "    // <<< Dex completa <<<"

MOTOR_SECAO = """    // >>> Dex completa: as outras regioes (dev_scripts/distribui_dex.py) >>>
    // MEDIDO em 21/08/2026, e nao lembrado: as tres faixas abaixo sao as unicas
    // do enum de MAPSEC que pertencem a UMA regiao so. `MAPSEC_SS_AQUA` (entre
    // Unova e Galar) fica de fora de proposito: e o barco, e ele liga Johto a
    // Kanto.
    if (sectionId >= MAPSEC_SINNOH_WEST && sectionId <= MAPSEC_SINNOH_NORTH)
        return REGION_SINNOH;
    if (sectionId >= MAPSEC_UNOVA_WEST && sectionId <= MAPSEC_UNOVA_NORTH)
        return REGION_UNOVA;
    if (sectionId >= MAPSEC_GALAR_SOUTH && sectionId <= MAPSEC_GALAR_OTHER)
        return REGION_GALAR;
    // <<< Dex completa <<<
"""

MOTOR_JOHTO = """
// Johto NAO tem faixa de mapsec propria, e essa e a armadilha desta funcao.
// Os 65 apelidos de MAPSEC de Johto (MAPSEC_NEW_BARK_TOWN, MAPSEC_ILEX_FOREST,
// MAPSEC_GOLDENROD_CITY, ...) sao todos `#define ... MAPSEC_SINNOH_WEST` em
// include/constants/region_map_sections.h, porque MAPSEC e u8 e nao cabe uma
// por cidade. Numericamente Johto E Sinnoh Oeste: nenhuma comparacao de
// sectionId pode separar as duas. Quem separa e o GRUPO do mapa, que e exato:
// os grupos 84 a 98 (`gMapGroup_TownsAndRoutes_Johto` ate
// `gMapGroup_SpecialArea_Johto`) sao Johto e nada mais, e sao contiguos.
//
// Custo de save ZERO: `location.mapGroup` ja e gravado pelo motor desde sempre
// e nenhum campo, tamanho ou ordem de SaveBlock muda aqui. E leitura.
static inline enum Region GetCurrentRegion(void)
{
    u32 grupo = gSaveBlock1Ptr->location.mapGroup;

    if (grupo >= MAP_GROUP(MAP_NEW_BARK_TOWN) && grupo <= MAP_GROUP(MAP_WORLD_HUB2))
        return REGION_JOHTO;
    return GetRegionForSectionId(gMapHeader.regionMapSectionId);
}
"""

MOTOR_ANTIGO = """static inline enum Region GetCurrentRegion(void)
{
    return GetRegionForSectionId(gMapHeader.regionMapSectionId);
}
"""


def aplica_motor(gravar):
    """Duas coisas, e as duas sao dado ou uma comparacao: (1) `GetCurrentRegion`
    passa a devolver as regioes que o `enum Region` sempre teve e a funcao nunca
    entregava; (2) as duas evolucoes de troca que ficaram orfas ganham a mesma
    segunda linha `EVO_ITEM` que o upstream ja deu as outras doze."""
    mudou = []

    t = open(REGIOES_H, encoding="utf-8").read()
    novo = t
    if MOTOR_INI not in novo:
        novo = novo.replace("        return REGION_KANTO;\n",
                            "        return REGION_KANTO;\n" + MOTOR_SECAO, 1)
    if "#include \"constants/maps.h\"" not in novo:
        novo = novo.replace('#include "constants/regions.h"\n',
                            '#include "constants/regions.h"\n'
                            '#include "constants/map_groups.h"\n'
                            '#include "constants/maps.h"\n', 1)
    if MOTOR_ANTIGO in novo:
        novo = novo.replace(MOTOR_ANTIGO, MOTOR_JOHTO.lstrip("\n"), 1)
    if novo != t:
        if gravar:
            open(REGIOES_H, "w", encoding="utf-8").write(novo)
        mudou.append("include/regions.h: SINNOH/UNOVA/GALAR por faixa de mapsec, "
                     "JOHTO por grupo de mapa (mapsec de Johto == Sinnoh Oeste)")

    for arq, de, alvo in EVO_ITEM_NOVAS:
        cam = f"{RAIZ}/src/data/pokemon/species_info/{arq}"
        txt = open(cam, encoding="utf-8").read()
        linha = f"{{EVO_ITEM, ITEM_LINKING_CORD, {alvo}}}"
        if linha in txt:
            continue
        m = re.search(
            r"(\[\s*%s\s*\]\s*=.*?\.evolutions = EVOLUTION\()(.*?)(\)\s*,\s*\n)"
            % de, txt, re.S)
        if not m:
            raise SystemExit(f"nao achei o bloco de evolucao de {de} em {arq}")
        corpo = m.group(2).rstrip()
        novo_corpo = f"{corpo},\n{' ' * 32}{linha}"
        txt = txt[:m.start(2)] + novo_corpo + txt[m.end(2):]
        if gravar:
            open(cam, "w", encoding="utf-8").write(txt)
        mudou.append(f"{arq}: {de} ganha EVO_ITEM ITEM_LINKING_CORD -> {alvo}")
    return mudou


# ----------------------------------------------------------------- presentes

MAPA_PRESENTE = "LittlerootTown_ProfessorBirchsLab"


def _tiles_presente():
    """Dois tiles medidos no map.bin do laboratorio, pela MESMA busca em largura
    do lendarios_sinnoh: alcancaveis a pe, sem ilhar ninguem, longe de NPC que
    anda (o `Aide` do laboratorio e `MOVEMENT_TYPE_WANDER_AROUND`).

    Se os NPCs JA estao no mapa, os tiles deles sao reaproveitados sem medir de
    novo. Sem isto a ferramenta nao e idempotente: a segunda rodada enxerga os
    NPCs da primeira como parede e os muda de lugar, de novo e de novo.
    """
    n = tabela()["npcs_presente"]
    return ({"T": tuple(n[0]["tile"])}, {"T": tuple(n[1]["tile"])})


def _objeto_presente(local, gfx, script, flag, tile):
    return {
        "local_id": local, "graphics_id": gfx,
        "x": tile[0], "y": tile[1], "elevation": 3,
        "movement_type": "MOVEMENT_TYPE_FACE_DOWN",
        "movement_range_x": 0, "movement_range_y": 0,
        "trainer_type": "TRAINER_TYPE_NONE",
        "trainer_sight_or_berry_tree_id": "0",
        "script": script, "flag": flag, "origem": MARCA,
    }


def _script_presentes():
    m = MAPA_PRESENTE
    pres = tabela()["presentes"]
    iniciais = [l for l in pres if l["metodo"] == "multichoice"]
    evento = [l for l in pres if l["metodo"] == "givemon"]
    p = [INC_INI,
         "@ Gerado por dev_scripts/distribui_dex.py --presentes. Nao editar a mao.",
         "",
         "@ O Birch entrega UM dos tres iniciais de Hoenn, a escolha. Medido em",
         "@ 21/08/2026: SPECIES_TREECKO so aparecia em data/scripts/debug.inc, e o",
         "@ laboratorio entregava Chikorita/Cyndaquil/Totodile. A abertura do jogo",
         "@ NAO foi tocada; isto e um NPC a mais na sala.",
         "@ Sem `waitstate` depois do dynmultistack: ScrCmd_dynmultichoice ja para",
         "@ o contexto sozinho, e o segundo o travaria para sempre (licao do",
         "@ chapter_jump.inc, 17/08/2026).",
         f"{m}_EventScript_DexIniciaisHoenn::",
         "\tlock",
         "\tfaceplayer",
         f"\tgoto_if_set FLAG_DEX_PRESENTE_INICIAL, {m}_EventScript_DexIniciaisJaDeu",
         f"\tmsgbox {m}_Text_DexIniciaisPergunta, MSGBOX_DEFAULT"]
    for i, l in enumerate(iniciais):
        nome = l["especie"].replace("SPECIES_", "").title()
        p.append(f"\tdynmultipush {m}_Text_DexInicial{nome}, {i}")
    p += ["\tdynmultistack 0, 0, FALSE, 4, FALSE, 0, DYN_MULTICHOICE_CB_NONE",
          "\tcompare VAR_RESULT, MULTI_B_PRESSED",
          f"\tgoto_if_eq {m}_EventScript_DexIniciaisSai"]
    for i, l in enumerate(iniciais):
        nome = l["especie"].replace("SPECIES_", "").title()
        p.append(f"\tgoto_if_eq VAR_RESULT, {i}, {m}_EventScript_DexInicial{nome}")
    p += [f"\tgoto {m}_EventScript_DexIniciaisSai", ""]
    for l in iniciais:
        nome = l["especie"].replace("SPECIES_", "").title()
        p += [f"{m}_EventScript_DexInicial{nome}::",
              f"\tgivemon {l['especie']}, {l['nivel']}",
              "\tsetflag FLAG_DEX_PRESENTE_INICIAL",
              f"\tmsgbox {m}_Text_DexIniciaisEntregue, MSGBOX_DEFAULT",
              "\trelease",
              "\tend",
              ""]
    p += [f"{m}_EventScript_DexIniciaisJaDeu::",
          f"\tmsgbox {m}_Text_DexIniciaisJaDeu, MSGBOX_DEFAULT",
          "\trelease",
          "\tend",
          "",
          f"{m}_EventScript_DexIniciaisSai::",
          "\trelease",
          "\tend",
          "",
          f"{m}_Text_DexIniciaisPergunta:",
          '\t.string "There are three POKéMON here that\\n"',
          '\t.string "no TRAINER ever claimed.\\p"',
          '\t.string "Go on, take the one you like!$"',
          ""]
    for l in iniciais:
        nome = l["especie"].replace("SPECIES_", "").title()
        p += [f"{m}_Text_DexInicial{nome}:",
              '\t.string "%s$"' % nome.upper(), ""]
    p += [f"{m}_Text_DexIniciaisEntregue:",
          '\t.string "Take good care of it!$"', "",
          f"{m}_Text_DexIniciaisJaDeu:",
          '\t.string "I hope the one you chose is\\ndoing well.$"', "",
          "@ Os event-only: as entradas SEM gfx de overworld, que por isso NAO",
          "@ podem virar encontro estatico (bone do Pikachu, Pichu de orelha",
          "@ espetada, Pikachu e Eevee iniciais). `givemon` manda para o PC",
          "@ quando o time esta cheio, entao a ordem da lista nao importa.",
          f"{m}_EventScript_DexDistribuicao::",
          "\tlock",
          "\tfaceplayer",
          f"\tgoto_if_set FLAG_DEX_PRESENTE_EVENTO, {m}_EventScript_DexDistribuicaoJaDeu",
          f"\tmsgbox {m}_Text_DexDistribuicao, MSGBOX_DEFAULT"]
    for l in evento:
        p.append(f"\tgivemon {l['especie']}, {l['nivel']}")
    p += ["\tsetflag FLAG_DEX_PRESENTE_EVENTO",
          f"\tmsgbox {m}_Text_DexDistribuicaoFim, MSGBOX_DEFAULT",
          "\trelease",
          "\tend",
          "",
          f"{m}_EventScript_DexDistribuicaoJaDeu::",
          f"\tmsgbox {m}_Text_DexDistribuicaoFim, MSGBOX_DEFAULT",
          "\trelease",
          "\tend",
          "",
          f"{m}_Text_DexDistribuicao:",
          '\t.string "I keep the POKéMON from every\\n"',
          '\t.string "event that never came to us.\\p"',
          '\t.string "You should have them.$"', "",
          f"{m}_Text_DexDistribuicaoFim:",
          '\t.string "Whatever does not fit in your\\nparty goes to your PC.$"', "",
          INC_FIM]
    return "\n".join(p) + "\n"


def aplica_presentes(gravar):
    a, b = _tiles_presente()
    cam = f"{RAIZ}/data/maps/{MAPA_PRESENTE}/map.json"
    d = json.load(open(cam, encoding="utf-8"))
    antes = d.get("object_events", [])
    novos = [o for o in antes if o.get("origem") != MARCA]
    if len(novos) + 2 > TETO_OBJETOS:
        raise SystemExit(f"{MAPA_PRESENTE} chegaria a {len(novos) + 2} objetos, "
                         f"acima do teto {TETO_OBJETOS}.")
    novos += [
        _objeto_presente("LOCALID_BIRCHS_LAB_DEX_INICIAIS",
                         "OBJ_EVENT_GFX_SCIENTIST_2",
                         f"{MAPA_PRESENTE}_EventScript_DexIniciaisHoenn", "0",
                         a["T"]),
        _objeto_presente("LOCALID_BIRCHS_LAB_DEX_EVENTO",
                         "OBJ_EVENT_GFX_MANIAC",
                         f"{MAPA_PRESENTE}_EventScript_DexDistribuicao", "0",
                         b["T"]),
    ]
    mudou = []
    if novos != antes:
        d["object_events"] = novos
        if gravar:
            open(cam, "w", encoding="utf-8").write(
                json.dumps(d, indent=2, ensure_ascii=False) + "\n")
        mudou.append(f"{MAPA_PRESENTE}/map.json: 2 NPCs de presente em "
                     f"{a['T']} e {b['T']}")
    cam = f"{RAIZ}/data/maps/{MAPA_PRESENTE}/scripts.inc"
    inc = open(cam, encoding="utf-8").read()
    novo = LS.substitui(inc, INC_INI, INC_FIM, _script_presentes())
    if novo != inc:
        if gravar:
            open(cam, "w", encoding="utf-8").write(novo)
        pres = tabela()["presentes"]
        mudou.append(f"{MAPA_PRESENTE}/scripts.inc: {len(pres)} presentes "
                     f"({sum(1 for l in pres if l['metodo'] == 'multichoice')} "
                     f"a escolha, o resto por givemon)")
    return mudou


# ------------------------------------------------------------------ estaticos

def escolhe_tiles(regiao):
    """[(linha, escolha)] para os estaticos de UMA regiao, LIDO da tabela.

    A geometria inteira vem de `lendarios_sinnoh.planeja` (busca em largura com
    colisao E elevacao, portao de "por o bicho aqui nao ilha ninguem", 3 tiles
    de distancia de NPC que anda, rota de pernas retas com a ultima saturando
    contra o Pokemon), so que ela roda em `--tabela`, uma vez, com a arvore
    limpa, e fica GRAVADA. Aqui so se le.

    Rodar a busca de novo aqui era o que quebrava a idempotencia: o `planeja`
    trata todo objeto do map.json como parede, entao na segunda rodada o tile ja
    escolhido esta ocupado e a busca devolve outro, e `--estaticos` mudava o
    mapa a cada chamada.
    """
    fora, falhas = [], []
    for l in tabela()["estaticos"]:
        if l["regiao"] != regiao:
            continue
        if "rota" not in l:
            falhas.append(f"{l['especie']}: a linha da tabela nao tem geometria; "
                          "rode `--tabela --aplica` antes.")
            continue
        fora.append((l, dict(T=tuple(l["tile"]), warp=l["warp"], dir=l["dir"],
                             para=tuple(l["para"]), vazio=tuple(l["vazio"]),
                             porta=tuple(l["porta"]), pouso=tuple(l["pouso"]),
                             rota=[tuple(x) for x in l["rota"]])))
    return fora, falhas


def _trecho_estatico(l, e):
    """Mesmo idioma do lendarios_sinnoh: msgbox antes do cry (e o que deixa o
    caso PROVAR a trava sem entrar em batalha), e a HIDE so acende em VITORIA ou
    CAPTURA, nunca em fuga ou derrota."""
    m = l["mapa"]
    nome = l["especie"].replace("SPECIES_", "").title().replace("_", "")
    lid = f"LOCALID_DEX_{l['especie'].replace('SPECIES_', '')}"
    return "\n".join([
        f"{m}_EventScript_Dex{nome}::",
        "\tlockall",
        f"\tmsgbox {m}_Text_Dex{nome}Intro, MSGBOX_DEFAULT",
        "\twaitse",
        f"\tplaymoncry {l['especie']}, CRY_MODE_ENCOUNTER",
        "\tdelay 30",
        "\twaitmoncry",
        f"\tseteventmon {l['especie']}, {l['nivel']}",
        "\tsetflag FLAG_SYS_CTRL_OBJ_DELETE",
        "\tspecial BattleSetup_StartLegendaryBattle",
        "\tclearflag FLAG_SYS_CTRL_OBJ_DELETE",
        f"\tsetvar VAR_LAST_TALKED, {lid}",
        "\tspecialvar VAR_RESULT, GetBattleOutcome",
        f"\tcall_if_eq VAR_RESULT, B_OUTCOME_WON, {m}_EventScript_Dex{nome}Some",
        f"\tcall_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, {m}_EventScript_Dex{nome}Some",
        "\treleaseall",
        "\tend",
        "",
        f"{m}_EventScript_Dex{nome}Some::",
        "\tfadescreenswapbuffers FADE_TO_BLACK",
        f"\tremoveobject {lid}",
        f"\tsetflag {l['flag']}",
        "\tfadescreenswapbuffers FADE_FROM_BLACK",
        "\treturn",
        "",
        f"{m}_Text_Dex{nome}Intro:",
        '\t.string "%s appeared!$"' % l["especie"].replace("SPECIES_", ""),
        ""])


def limpa_mapas_orfaos(gravar):
    """Tira o estatico dos mapas que SAIRAM da tabela.

    `aplica_estaticos` so mexe nos mapas que a tabela cita, entao quando uma
    rodada de `--tabela` muda um lendario de mapa, o objeto velho fica no mapa
    velho para sempre. Medido em 21/08/2026: o SnowpointTempleB5F guardou um
    estatico orfao em (5,3) que reprovou o T123.9 e o T123.10, o par do
    Regigigas, muito depois de a tabela ja ter tirado o bicho de la.
    """
    # O laboratorio do Birch NAO e mapa de estatico, mas os dois NPC de
    # presente que moram nele usam a MESMA marca. Sem esta linha a limpeza
    # apagava os dois (medido em 21/08/2026, na primeira versao da varredura).
    vivos = {l["mapa"] for l in tabela()["estaticos"]} | {MAPA_PRESENTE}
    mudou = []
    for cam in sorted(glob.glob(f"{RAIZ}/data/maps/*/map.json")):
        mapa = os.path.basename(os.path.dirname(cam))
        if mapa in vivos:
            continue
        d = json.load(open(cam, encoding="utf-8"))
        antes = d.get("object_events", [])
        novos = [o for o in antes if o.get("origem") != MARCA]
        if len(novos) == len(antes):
            continue
        d["object_events"] = novos
        if gravar:
            open(cam, "w", encoding="utf-8").write(
                json.dumps(d, indent=2, ensure_ascii=False) + "\n")
        inc_cam = f"{RAIZ}/data/maps/{mapa}/scripts.inc"
        inc = open(inc_cam, encoding="utf-8").read()
        novo = LS.substitui(inc, INC_INI, INC_FIM, "")
        if novo != inc and gravar:
            open(inc_cam, "w", encoding="utf-8").write(novo)
        mudou.append(f"{mapa}: {len(antes) - len(novos)} estatico(s) orfao(s) removido(s)")
    return mudou


def aplica_estaticos(regiao, gravar):
    escolhas, falhas = escolhe_tiles(regiao)
    if falhas:
        raise SystemExit("\n".join(falhas))
    mudou = []
    por_mapa = collections.defaultdict(list)
    for l, e in escolhas:
        por_mapa[l["mapa"]].append((l, e))
    for mapa, itens in por_mapa.items():
        cam = f"{RAIZ}/data/maps/{mapa}/map.json"
        d = json.load(open(cam, encoding="utf-8"))
        antes = d.get("object_events", [])
        novos = [o for o in antes if o.get("origem") != MARCA]
        if len(novos) + len(itens) > TETO_OBJETOS:
            raise SystemExit(f"{mapa} chegaria a {len(novos) + len(itens)} "
                             f"objetos, acima do teto {TETO_OBJETOS}.")
        for l, e in itens:
            nome = l["especie"].replace("SPECIES_", "").title().replace("_", "")
            novos.append({
                "local_id": f"LOCALID_DEX_{l['especie'].replace('SPECIES_', '')}",
                "graphics_id": "OBJ_EVENT_GFX_SPECIES(%s)"
                               % l["especie"].replace("SPECIES_", ""),
                "x": e["T"][0], "y": e["T"][1], "elevation": 0,
                "movement_type": "MOVEMENT_TYPE_FACE_DOWN",
                "movement_range_x": 0, "movement_range_y": 0,
                "trainer_type": "TRAINER_TYPE_NONE",
                "trainer_sight_or_berry_tree_id": "0",
                "script": f"{mapa}_EventScript_Dex{nome}",
                "flag": l["flag"], "origem": MARCA})
        if novos != antes:
            d["object_events"] = novos
            if gravar:
                open(cam, "w", encoding="utf-8").write(
                    json.dumps(d, indent=2, ensure_ascii=False) + "\n")
            mudou.append(f"{mapa}: {len(itens)} estatico(s)")
        cam = f"{RAIZ}/data/maps/{mapa}/scripts.inc"
        inc = open(cam, encoding="utf-8").read()
        corpo = "\n".join([INC_INI] + [_trecho_estatico(l, e) for l, e in itens]
                          + [INC_FIM]) + "\n"
        novo = LS.substitui(inc, INC_INI, INC_FIM, corpo)
        if novo != inc:
            if gravar:
                open(cam, "w", encoding="utf-8").write(novo)
            mudou.append(f"{mapa}/scripts.inc: {len(itens)} encontro(s)")
    return mudou


# ------------------------------------------------------------------ autoteste

def _agua(nome, cat):
    return "TYPE_WATER" in cat[nome].tipos


def confere(t, cat):
    """As regras que NAO podem ser violadas, checadas sobre uma tabela qualquer.

    Vive fora do `demo` de proposito: e a mesma funcao que o `demo` usa contra a
    tabela boa e contra a tabela MUTADA, e e por isso que a mutacao plantada
    prova alguma coisa.
    """
    erros = []
    todas = [l for k in BUCKETS for l in t[k]]
    nomes = [l["especie"] for l in todas]
    if len(nomes) != len(set(nomes)):
        erros.append("especie repetida na tabela")
    for l in t["selvagens"]:
        e = cat[l["especie"]]
        if _agua(l["especie"], cat) and l["metodo"] not in AGUA:
            erros.append(f"{l['especie']} e TYPE_WATER e caiu em {l['metodo']}")
        if not _agua(l["especie"], cat) and l["metodo"] in AGUA:
            erros.append(f"{l['especie']} nao e agua e caiu em {l['metodo']}")
        if (e.gen <= 5 and not eh_regional(l["especie"])
                and not eh_cosmetica(l["especie"])
                and l["origem"] == "censo"
                and l["regiao"] != REGIAO_DA_GEN[e.gen]):
            erros.append(f"{l['especie']} e gen {e.gen} e foi para {l['regiao']}")
    for l in t["estaticos"]:
        if not cat[l["especie"]].lenda:
            erros.append(f"{l['especie']} nao e lenda e virou estatico")
    for l in t["selvagens"]:
        if cat[l["especie"]].lenda:
            erros.append(f"{l['especie']} e lenda e foi para o mato (regra 7)")
    return erros


def teto_do_motor():
    """T129.15: o teto de 15 e a janela de 20x17 saem do MOTOR, nao da memoria.

    `TETO_SPRITE` e `JANELA_SPRITE` sao numeros escritos a mao no topo deste
    arquivo, e numero escrito a mao envelhece calado: se alguem mexer em
    `OBJECT_EVENTS_COUNT` ou em `MAP_OFFSET`, o gerador continua distribuindo
    lendario pela regua velha e o unico sintoma e um bicho que nao aparece.
    Aqui as duas constantes sao RECALCULADAS a partir dos cabecalhos, com a
    conta feita em cima do proprio `TrySpawnObjectEvents`:

        left = pos.x - 2 ; right = pos.x + MAP_OFFSET_W + 2 ; npcX = x + MAP_OFFSET
          => x de (pos.x - 2 - MAP_OFFSET) a (pos.x + MAP_OFFSET_W + 2 - MAP_OFFSET)
          => largura MAP_OFFSET_W + 5
        top  = pos.y     ; bottom = pos.y + MAP_OFFSET_H + 2
          => altura MAP_OFFSET_H + 3

    Junto vai um fato MEDIDO nesta rodada e que nao estava escrito em lugar
    nenhum: template de `OBJ_EVENT_GFX_LIGHT_SPRITE` NAO gasta slot de
    ObjectEvent, porque o motor o manda para `SpawnLightSprite` no ramo de cima
    do `if`. O `lotacao()` conta essas luzes, entao a regua do gerador e
    PESSIMISTA, e errar para esse lado custa um lendario reposicionado, nunca um
    lendario invisivel. Fica dito para ninguem "consertar" o gerador afrouxando
    a conta sem medir de novo.
    """
    g = open(f"{RAIZ}/include/constants/global.h", encoding="utf-8").read()
    f = open(f"{RAIZ}/include/fieldmap.h", encoding="utf-8").read()
    n = int(re.search(r"#define OBJECT_EVENTS_COUNT\s+(\d+)", g).group(1))
    off = int(re.search(r"#define MAP_OFFSET\s+(\d+)", f).group(1))
    largura, altura = (off * 2 + 1) + 5, (off * 2) + 3
    assert TETO_SPRITE == n - 1, \
        f"TETO_SPRITE={TETO_SPRITE}, mas OBJECT_EVENTS_COUNT={n} (menos o jogador)"
    assert JANELA_SPRITE == (largura, altura), \
        f"JANELA_SPRITE={JANELA_SPRITE}, mas o motor usa {(largura, altura)}"
    luzes = 0
    for mapa in sorted({l["mapa"] for l in tabela()["estaticos"]}):
        d = json.load(open(f"{RAIZ}/data/maps/{mapa}/map.json", encoding="utf-8"))
        luzes += sum(1 for o in d.get("object_events", [])
                     if o.get("graphics_id") == "OBJ_EVENT_GFX_LIGHT_SPRITE")
    return (f"T129.15 OK: teto {TETO_SPRITE} = OBJECT_EVENTS_COUNT {n} menos o "
            f"jogador, janela {largura}x{altura} refeita de MAP_OFFSET {off}; "
            f"e {luzes} luzes contadas nos 29 mapas de estatico que o motor NAO "
            f"poe em slot de ObjectEvent (a regua e pessimista de proposito)")


def diff_do_mato(ref=None):
    """T129.13: o mato conferido contra o GIT, e nao contra a propria tabela.

    O T129.2 ja compara o `wild_encounters.json` de hoje com `encontros_base()`,
    que e o arquivo de hoje DESFEITO pela coluna `substituido` da tabela: se a
    tabela mentisse sobre o que substituiu, os dois lados mentiriam junto e o
    caso passaria. Esta prova sai do repositorio, que nenhuma ferramenta desta
    rodada escreveu, e cobra quatro coisas, por tabela e por slot: nenhuma
    tabela sumiu ou nasceu, nenhuma mudou de tamanho, nenhuma ESPECIE que a
    fonte tinha deixou de aparecer na tabela dela, e nenhum slot trocado mudou
    de NIVEL (regra 1 do plano: a linha nova herda o nivel do slot).
    """
    import subprocess
    ref = ref or BASE_MATO
    r = subprocess.run(["git", "show", f"{ref}:src/data/wild_encounters.json"],
                       cwd=RAIZ, capture_output=True, text=True)
    if r.returncode != 0:
        return (f"T129.13 PULADO: `git show {ref}:src/data/wild_encounters.json` "
                "nao existe neste clone. NAO conte como passou.")
    def tudo(d):
        # Indice PROPRIO, e nao o `_indice`: aquele so olha grupo com
        # `for_maps`, e deixa 254 das 1.248 tabelas de fora. Aqui a pergunta e
        # "alguma coisa se perdeu em ALGUM lugar", entao nada fica de fora.
        fora = {}
        for g in d["wild_encounter_groups"]:
            for enc in g.get("encounters", []):
                mid = enc.get("map", enc.get("base_label", g["label"]))
                for tp in censo_dex.TIPOS_SELVAGEM:
                    if tp in enc and enc[tp]:
                        fora[(g["label"], mid, tp)] = enc[tp]["mons"]
        return fora
    a, b = tudo(json.loads(r.stdout)), tudo(
        json.load(open(ENCONTROS, encoding="utf-8")))
    assert set(a) == set(b), f"T129.13: tabela de encontro apareceu ou sumiu: " \
                             f"{sorted(set(a) ^ set(b))[:4]}"
    perdidas, trocas, niveis = set(), 0, []
    for k in a:
        assert len(a[k]) == len(b[k]), f"T129.13: {k} mudou de tamanho"
        perdidas |= ({m["species"] for m in a[k]} - {m["species"] for m in b[k]})
        for x, y in zip(a[k], b[k]):
            if x["species"] == y["species"]:
                continue
            trocas += 1
            if (x["min_level"], x["max_level"]) != (y["min_level"], y["max_level"]):
                niveis.append((k, x["species"], y["species"]))
    assert not perdidas, f"T129.13: a fonte tinha e sumiu: {sorted(perdidas)[:8]}"
    assert not niveis, f"T129.13: slot trocado mudou de nivel: {niveis[:4]}"
    return (f"T129.13 OK: contra {ref}, {len(a)} tabelas intactas em numero e "
            f"tamanho, {trocas} slots trocados, ZERO especies perdidas e ZERO "
            f"niveis alterados")


def plano_congelado():
    """A tabela gravada, DEPOIS de conferida contra um plano feito do zero.

    O plano do zero nao pode mandar no tile (ver `demo`), mas pode e deve mandar
    no par especie -> regiao/mapa: se ele discordar, ou a regua mudou sem que a
    tabela fosse regerada, ou alguem editou a tabela a mao no lugar da regua.
    """
    t = tabela()
    p = plano()
    for k in BUCKETS:
        assert len(p[k]) == len(t[k]), (k, len(p[k]), len(t[k]))
    de_para = {l["especie"]: (l["regiao"], l["mapa"]) for l in t["estaticos"]}
    fora = [(l["especie"], de_para.get(l["especie"]), (l["regiao"], l["mapa"]))
            for l in p["estaticos"] if de_para.get(l["especie"]) !=
            (l["regiao"], l["mapa"])]
    assert not fora, f"o plano do zero discorda da tabela gravada: {fora[:5]}"
    return t


def demo():
    cat = catalogo_completo()
    # A TABELA GRAVADA e o sujeito da prova, e nao um plano recalculado. O plano
    # decide REGIAO por cota e por lotacao, e os dois dependem da arvore: depois
    # de `--estaticos --aplica` a arvore ja tem os 106 objetos, e recalcular do
    # zero e um exercicio sobre outro jogo. Fora isso, duas linhas da tabela
    # (Great Tusk e Scream Tail, no Unova_VictoryRoadCave2F) tiveram o tile
    # movido A MAO depois da geracao, por linha de visao de treinador; um
    # `--demo` que exigisse o plano nota por nota apagaria esse conserto.
    t = plano_congelado()
    falhas = []

    # 1. Cobertura: uma linha por entrada que o censo diz inobtenivel, e so.
    linhas = censo_base()
    ino = {l.nome for l in linhas if l.categoria == "inobtenivel"}
    da_tabela = {l["especie"] for k in BUCKETS for l in t[k]}
    assert da_tabela == ino, (len(da_tabela), len(ino),
                              sorted(da_tabela ^ ino)[:10])

    # 2. As regras duras.
    erros = confere(t, cat)
    assert not erros, erros[:8]

    # 3. Flags: uma por estatico, todas distintas, todas dentro da faixa, todas
    #    FLAG_UNUSED sem outro dono. Flag dobrada apaga a cena do vizinho.
    fl = open(FLAGS_H, encoding="utf-8").read()
    est = t["estaticos"]
    assert FLAG_BASE + len(est) - 1 <= FLAG_TETO, len(est)
    nomes_flag = [l["flag"] for l in est]
    assert len(set(nomes_flag)) == len(nomes_flag)
    for i, l in enumerate(est):
        alvo = f"FLAG_UNUSED_0x{FLAG_BASE + i:04X}"
        assert f"#define {alvo} " in fl, f"{alvo} nao existe no pool"
        donos = re.findall(rf"^#define (FLAG_\w+)\s+{alvo}\s*(?://.*)?$", fl, re.M)
        assert donos in ([], [l["flag"]]), f"{alvo} ja tem dono: {donos}"

    # 4. Mapa de estatico existe E nao esta cortado do escopo (regra 9).
    existem, cortados = mapas_existentes(), mapas_cortados()
    for l in est:
        assert l["mapa"] in existem, f"{l['especie']}: mapa {l['mapa']} nao existe"
        assert l["mapa"] not in cortados, f"{l['especie']}: {l['mapa']} cortado"

    # 4b. TETO DE SPRITE. E o defeito que nao da erro nenhum: o objeto fica no
    #     map.json, o script fica no scripts.inc, a flag fica limpa, e o bicho
    #     nao aparece porque o motor ja gastou os 16 slots naquela tela.
    por_mapa = collections.defaultdict(list)
    for l in est:
        assert "rota" in l, f"{l['especie']}: linha sem geometria; rode --tabela"
        por_mapa[l["mapa"]].append(tuple(l["tile"]))
    for mapa, tiles in por_mapa.items():
        assert len(set(tiles)) == len(tiles), f"{mapa}: dois estaticos no mesmo tile"
        d = json.load(open(f"{RAIZ}/data/maps/{mapa}/map.json", encoding="utf-8"))
        fixos = _objetos_do_mapa(d)
        # Nasceu de um estrago real (21/08/2026): a busca em largura ignorava
        # os objetos do `lendarios_sinnoh` e tres estaticos foram parar EM CIMA
        # do Shaymin, do Heatran e do Regigigas. Dois objetos no mesmo tile nao
        # dao erro de compilacao nenhum.
        em_cima = sorted(set(tiles) & set(fixos))
        assert not em_cima, f"{mapa}: estatico em cima de objeto que ja existia: {em_cima}"
        n = lotacao(fixos + tiles)
        assert n <= TETO_SPRITE, f"{mapa}: {n} objetos numa janela so (teto {TETO_SPRITE})"
        assert len(fixos) + len(tiles) <= TETO_OBJETOS, mapa
    #     MUTACAO PLANTADA: empilhar os estaticos de um mapa em volta de um
    #     ponto so tem que ESTOURAR. Sem ela o teto acima so mede o que o
    #     gerador ja acertou.
    empilhado = [(3 + 2 * (i % 4), 3 + 2 * (i // 4))
                 for i in range(TETO_SPRITE + 1)]
    assert lotacao(empilhado) > TETO_SPRITE, "o teto de sprite nao pega pilha"

    # 4c. IDEMPOTENCIA DO ESTATICO: `escolhe_tiles` le a tabela e nao remede
    #     nada, entao aplicar duas vezes escreve o MESMO objeto. Antes ele
    #     rodava a busca de novo, via o proprio objeto ja escrito como parede e
    #     devolvia outro tile a cada rodada.
    for r in CINCO:
        escolhas, sem_geometria = escolhe_tiles(r)
        falhas += sem_geometria[:3]
        assert not sem_geometria, sem_geometria[:3]
        assert [tuple(l["tile"]) for l, _e in escolhas] == \
               [tuple(e["T"]) for _l, e in escolhas], r
        assert len(escolhas) == sum(1 for l in est if l["regiao"] == r), r

    # 5. Nenhuma especie da FONTE some do mato: todo slot escrito e duplicado, e
    #    a especie que estava la continua na primeira ocorrencia da tabela.
    base = encontros_base()
    idx = _indice(base)
    for l in t["selvagens"]:
        mons = idx[(l["mapa"], l["metodo"])]
        antes = [m["species"] for m in mons]
        assert antes[l["slot"]] == l["substituido"], l["especie"]
        assert antes.index(l["substituido"]) < l["slot"], \
            f"{l['especie']}: slot {l['slot']} nao e duplicado em {l['mapa']}"

    # 6. MUTACAO PLANTADA: um Ferroseed no fundo do mar tem que ser PEGO.
    #    Sem este assert o `confere` so mede o que o gerador ja acertou.
    agua = next(l for l in t["selvagens"] if l["metodo"] in AGUA)
    mutada = {k: [dict(x) for x in t[k]] for k in BUCKETS}
    alvo = next(l for l in mutada["selvagens"] if l["especie"] == agua["especie"])
    alvo["metodo"] = "land_mons"
    assert confere(mutada, cat), "a regra da agua nao pega peixe em terra firme"

    # 7. MUTACAO PLANTADA 2: lenda no mato tem que ser PEGA.
    mutada = {k: [dict(x) for x in t[k]] for k in BUCKETS}
    lenda = dict(mutada["estaticos"][0])
    lenda["como"] = "selvagem"
    lenda["metodo"] = "land_mons"
    lenda["slot"] = 0
    lenda["substituido"] = "SPECIES_NONE"
    mutada["estaticos"] = mutada["estaticos"][1:]
    mutada["selvagens"] = mutada["selvagens"] + [lenda]
    assert any("regra 7" in x for x in confere(mutada, cat)), \
        "lenda no mato passou batido"

    # 8. Idempotencia do baseline: reconstruir a base a partir de `substituido`
    #    e reaplicar tem que dar o MESMO arquivo. E o que impede `--tabela` de
    #    cuspir um plano diferente depois de `--selvagem` ja ter rodado.
    d1 = json.loads(json.dumps(encontros_base()))
    i1 = _indice(d1)
    for l in t["selvagens"]:
        i1[(l["mapa"], l["metodo"])][l["slot"]]["species"] = l["especie"]
    i2 = _indice(json.loads(json.dumps(d1)))
    for l in t["selvagens"]:
        i2[(l["mapa"], l["metodo"])][l["slot"]]["species"] = l["substituido"]
    assert [m["species"] for k in sorted(i2) for m in i2[k]] == \
           [m["species"] for k in sorted(_indice(encontros_base())) for m in
            _indice(encontros_base())[k]], "o baseline nao volta"

    # 9. Presentes: quem entra por `givemon` e exatamente quem NAO pode ser
    #    estatico, mais os tres iniciais de Hoenn.
    sem_ow = {x.nome for x in linhas if not x.ow}
    for l in t["presentes"]:
        assert (l["especie"] in INICIAIS_HOENN
                or PRESENTE_SEM_OVERWORLD.match(l["especie"])
                or l["especie"] in sem_ow), l["especie"]

    # 10. O conserto de motor e reversivel e idempotente no TEXTO.
    txt = open(REGIOES_H, encoding="utf-8").read()
    assert "GetRegionForSectionId" in txt and "REGION_HOENN" in txt

    # ---- T129.1 e T129.2: o mato provado por LEITURA da tabela, nao por
    # sorteio no emulador. Encontro selvagem e sorteio, e sorteio nao e teste.
    vivo = json.load(open(ENCONTROS, encoding="utf-8"))
    iv = _indice(vivo)
    ib = _indice(encontros_base())
    faltam = [l["especie"] for l in t["selvagens"]
              if iv[(l["mapa"], l["metodo"])][l["slot"]]["species"] != l["especie"]]
    assert not faltam, f"T129.1: {len(faltam)} especies da tabela nao estao no "\
                       f"wild_encounters.json: {faltam[:6]}"
    sumiram = {s for k in ib for s in
               {m["species"] for m in ib[k]} - {m["species"] for m in iv[k]}}
    assert not sumiram, f"T129.2: especie que a FONTE tinha sumiu: {sorted(sumiram)[:8]}"
    for k in ib:
        assert len(ib[k]) == len(iv[k]), f"T129.2: {k} mudou de tamanho"
    print(diff_do_mato())
    print(teto_do_motor())
    print(f"T129.1 OK: {len(t['selvagens'])} especies novas presentes no "
          f"wild_encounters.json")
    print(f"T129.2 OK: nenhuma das {len({m['species'] for k in ib for m in ib[k]})} "
          f"especies da fonte sumiu, e nenhuma tabela mudou de tamanho")

    # ---- T129.6: o conserto de motor provado pelo COMPILADOR, e nao por regex.
    print(sonda_de_regiao())

    # AVISO, nao falha: estatico cujo mapa JA tem um objeto daquela especie.
    # Sao objetos de CENA (o Suicune que passa correndo por Cianwood, os dois
    # Celebi da Ilex Forest), todos escondidos por flag na maior parte do jogo,
    # entao o estatico novo nao briga por tile nem por flag. Fica dito porque
    # quem executa a onda B ve DOIS sprites da mesma especie no mesmo mapa e
    # precisa saber que isso e esperado, e nao um objeto dobrado.
    for l in est:
        cam = f"{RAIZ}/data/maps/{l['mapa']}/map.json"
        alvo = "OBJ_EVENT_GFX_SPECIES(%s)" % l["especie"].replace("SPECIES_", "")
        # Sem o filtro de `origem` o aviso passa a apontar para o objeto que
        # ESTA ferramenta acabou de escrever, e vira ruido em 106 linhas.
        d = json.load(open(cam, encoding="utf-8"))
        if any(o.get("graphics_id") == alvo and o.get("origem") != MARCA
               for o in d.get("object_events", [])):
            print(f"  AVISO: {l['mapa']} ja tem um objeto de "
                  f"{l['especie'].replace('SPECIES_', '')} (cena, escondido por "
                  f"flag); o estatico novo entra ao lado")

    print("tabela: " + ", ".join(f"{k} {len(t[k])}" for k in BUCKETS))
    print("estaticos por regiao: " + str(dict(collections.Counter(
        l["regiao"] for l in est))))
    print("selvagem por regiao: " + str(dict(collections.Counter(
        l["regiao"] for l in t["selvagens"]))))
    print("demo: %s" % ("OK" if not falhas else "REPROVADO"))
    return 1 if falhas else 0


SONDA = """
#include "global.h"
#include "constants/region_map_sections.h"
#include "constants/map_groups.h"
#include "constants/maps.h"
#include "constants/regions.h"
#include "constants/pokemon.h"

// A colisao que obriga Johto a sair por GRUPO e nao por mapsec.
_Static_assert(MAPSEC_NEW_BARK_TOWN == MAPSEC_SINNOH_WEST, "colisao_johto_sinnoh");
_Static_assert(MAPSEC_ILEX_FOREST == MAPSEC_SINNOH_WEST, "colisao_johto_sinnoh2");

// As tres faixas novas sao disjuntas entre si e disjuntas de Kanto.
_Static_assert(MAPSEC_SINNOH_WEST <= MAPSEC_SINNOH_NORTH, "faixa_sinnoh");
_Static_assert(MAPSEC_SINNOH_NORTH < MAPSEC_UNOVA_WEST, "sinnoh_antes_de_unova");
_Static_assert(MAPSEC_UNOVA_NORTH < MAPSEC_GALAR_SOUTH, "unova_antes_de_galar");
_Static_assert(MAPSEC_GALAR_SOUTH <= MAPSEC_GALAR_OTHER, "faixa_galar");
_Static_assert(MAPSEC_SPECIAL_AREA < MAPSEC_SINNOH_WEST, "kanto_nao_encosta");

// A faixa de GRUPO de Johto nao engole Hoenn nem Sinnoh nem Kanto.
_Static_assert(MAP_GROUP(MAP_NEW_BARK_TOWN) <= MAP_GROUP(MAP_WORLD_HUB2), "faixa_johto");
_Static_assert(MAP_GROUP(MAP_LITTLEROOT_TOWN) < MAP_GROUP(MAP_NEW_BARK_TOWN), "hoenn_fora");
_Static_assert(MAP_GROUP(MAP_PALLET_TOWN) < MAP_GROUP(MAP_NEW_BARK_TOWN), "kanto_fora");
_Static_assert(MAP_GROUP(MAP_MT_CORONET_B1F) < MAP_GROUP(MAP_NEW_BARK_TOWN)
            || MAP_GROUP(MAP_MT_CORONET_B1F) > MAP_GROUP(MAP_WORLD_HUB2), "sinnoh_fora");

// T129.14 (fechador, 21/08/2026): a Ilex Forest e o caso concreto que o
// IF_REGION vai ler, porque e la que mora o Okidogi da onda B. Pelo MAPSEC ela
// cai dentro da faixa de Sinnoh e `GetRegionForSectionId` devolveria
// REGION_SINNOH; e o ramo do GRUPO, e so ele, que a devolve como REGION_JOHTO.
// As tres afirmacoes abaixo sao as tres pernas dessa frase, e REGION_JOHTO !=
// REGION_SINNOH e a quarta: sem ela as outras tres seriam sobre nada.
_Static_assert(MAPSEC_ILEX_FOREST >= MAPSEC_SINNOH_WEST
            && MAPSEC_ILEX_FOREST <= MAPSEC_SINNOH_NORTH, "ilex_cairia_em_sinnoh");
_Static_assert(MAP_GROUP(MAP_ILEX_FOREST) >= MAP_GROUP(MAP_NEW_BARK_TOWN)
            && MAP_GROUP(MAP_ILEX_FOREST) <= MAP_GROUP(MAP_WORLD_HUB2), "ilex_no_grupo_johto");
_Static_assert(REGION_JOHTO != REGION_SINNOH, "johto_e_sinnoh_sao_a_mesma_coisa");
_Static_assert(IF_REGION != IF_NOT_REGION, "condicao_de_evolucao_por_regiao_sumiu");
%s
"""


def _compila_sonda(corpo):
    devkit = os.environ.get(
        "DEVKITARM",
        os.path.expanduser("~/toolchains/arm-gnu-toolchain-15.2.rel1-darwin-arm64"
                           "-arm-none-eabi"))
    gcc = os.path.join(devkit, "bin", "arm-none-eabi-gcc")
    if not os.path.exists(gcc):
        return None
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        c = os.path.join(tmp, "sonda.c")
        open(c, "w").write(corpo)
        r = subprocess.run(
            [gcc, "-c", "-iquote", "include", "-Wno-trigraphs", "-DMODERN=1",
             "-DTESTING=0", "-DEMERALD", "-std=gnu17", "-mthumb",
             "-mabi=apcs-gnu", "-march=armv4t", "-O0", "-o",
             os.path.join(tmp, "sonda.o"), c],
            cwd=RAIZ, capture_output=True, text=True)
        return r.returncode == 0


def sonda_de_regiao():
    """T129.6: o conserto de motor provado pelo COMPILADOR de verdade.

    `GetCurrentRegion` nao aparece na EWRAM, entao o harness do emulador nao a
    le. A camada certa da afirmacao e a que o motor usa: as CONSTANTES. Esta
    sonda compila com o mesmo `arm-none-eabi-gcc` do build e afirma, em
    `_Static_assert`, que (1) o mapsec de Johto e numericamente o mesmo de
    Sinnoh Oeste, que e a razao de Johto sair por grupo, e (2) as faixas novas
    sao disjuntas entre si e nao engolem Kanto, Hoenn nem Sinnoh.

    Mutacao plantada junto: uma afirmacao FALSA tem que reprovar a compilacao.
    Sem ela, uma sonda que nao compila por outro motivo passaria como "verde".
    """
    ok = _compila_sonda(SONDA % "")
    if ok is None:
        return ("T129.6 PULADO: arm-none-eabi-gcc nao encontrado (exporte "
                "DEVKITARM). NAO conte como passou.")
    if not ok:
        raise SystemExit("T129.6 REPROVADO: a sonda de regiao nao compila; as "
                         "faixas de mapsec ou de grupo estao erradas.")
    mutante = _compila_sonda(SONDA % (
        '_Static_assert(MAPSEC_SINNOH_WEST > MAPSEC_GALAR_OTHER, "mutacao");'))
    if mutante:
        raise SystemExit("T129.6 REPROVADO: a mutacao plantada COMPILOU, entao "
                         "a sonda nao esta provando nada.")
    return ("T129.6 OK: mapsec de Johto == Sinnoh Oeste (por isso Johto sai por "
            "grupo), faixas de Sinnoh/Unova/Galar disjuntas, e Hoenn, Kanto e "
            "Sinnoh fora da faixa de grupo de Johto; T129.14 OK: a Ilex Forest, "
            "onde mora o Okidogi, cairia em REGION_SINNOH pelo mapsec e so o "
            "ramo do GRUPO a devolve como REGION_JOHTO, com IF_REGION vivo e "
            "REGION_JOHTO != REGION_SINNOH; mutacao plantada reprovada")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tabela", action="store_true")
    ap.add_argument("--selvagem", action="store_true")
    ap.add_argument("--motor", action="store_true")
    ap.add_argument("--presentes", action="store_true")
    ap.add_argument("--estaticos", action="store_true")
    ap.add_argument("--regiao")
    ap.add_argument("--dry-run", action="store_true", dest="dry")
    ap.add_argument("--aplica", action="store_true")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        raise SystemExit(demo())
    saida = []
    if a.tabela:
        saida += escreve_tabela(a.aplica)
    if a.selvagem:
        saida += aplica_selvagem(a.aplica)
        saida += aplica_flags(a.aplica)
    if a.motor:
        saida += aplica_motor(a.aplica)
    if a.presentes:
        saida += aplica_presentes(a.aplica)
        saida += aplica_flags(a.aplica)
        saida += aplica_casos(a.aplica)
    if a.estaticos:
        regioes = [a.regiao] if a.regiao else list(CINCO)
        for r in regioes:
            if a.dry or not a.aplica:
                escolhas, falhas = escolhe_tiles(r)
                for f in falhas:
                    print("FALHA " + f)
                por_mapa = collections.Counter(l["mapa"] for l, _e in escolhas)
                saida.append(f"{r}: {len(escolhas)} estatico(s) com tile medido em "
                             f"{len(por_mapa)} mapa(s), {len(falhas)} sem tile")
                for l, e in escolhas:
                    saida.append(f"    {l['especie']:34} {l['mapa']:30} "
                                 f"T={e['T']} warp {e['warp']}")
            else:
                saida += aplica_estaticos(r, True)
        if not a.dry and a.aplica:
            saida += limpa_mapas_orfaos(True)
            saida += aplica_casos(True)
    if not saida:
        saida = ["nada a fazer (ja esta escrito, ou nenhum subcomando pedido)"]
    for linha in saida:
        print(("grava " if a.aplica and not a.dry else "faria ") + linha
              if not linha.startswith("    ") else linha)



# ------------------------------------------------------------- casos do T129

def numeros_de_especie():
    """{SPECIES_X: n} lido do enum, e nao decorado. Apelido herda o valor."""
    txt = open(f"{RAIZ}/include/constants/species.h", encoding="utf-8").read()
    fora = {}
    for nome, rhs in re.findall(
            r"^\s*(SPECIES_[A-Z0-9_]+)\s*=\s*([A-Za-z0-9_]+)\s*,", txt, re.M):
        if not rhs.startswith("SPECIES_"):
            fora[nome] = int(rhs, 0)
        elif rhs in fora:
            fora[nome] = fora[rhs]
        # Apelido para frente (`SPECIES_X = SPECIES_CUSTOM_END`) nao vira numero:
        # e sentinela de fim de tabela, nao especie.
    return fora


def casos_t129():
    """Os casos de emulador. Os de leitura de tabela (T129.1, T129.2) e o do
    compilador (T129.6) vivem no `--demo`, porque nao ha emulador que os prove.

    A rota sai da MESMA geometria que colocou o NPC: ultima perna saturando
    contra ele. Por isso o par negativo existe e para em outro tile.
    """
    n = tabela()["npcs_presente"]
    num = numeros_de_especie()
    pres = tabela()["presentes"]
    iniciais = [l for l in pres if l["metodo"] == "multichoice"]
    evento = [l for l in pres if l["metodo"] == "givemon"]
    mapa = "MAP_LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB"
    esc = {p["papel"]: dict(p, rota=[tuple(x) for x in p["rota"]],
                            para=tuple(p["para"]), vazio=tuple(p["vazio"]),
                            T=tuple(p["tile"])) for p in n}
    a, b = esc["iniciais"], esc["evento"]
    primeiro = iniciais[0]["especie"]

    # Os apertos DEPOIS de chegar: A abre a fala, A avanca a fala, A escolhe a
    # PRIMEIRA linha do menu (o cursor nasce nela), e os ultimos fecham o
    # "Take good care of it!".
    escolhe = ",16:A,150:NADA,16:A,150:NADA,16:A,240:NADA,16:A*3,180:NADA"
    # Medido, nao estimado: a fala do NPC de distribuicao tem \p e roda 19
    # `givemon` no meio, e com 150 quadros de folga o roteiro acabava antes de
    # o primeiro Pokemon entrar no time. Com estas esperas o time chega a 6.
    fala = ",16:A,240:NADA,16:A*2,300:NADA,16:A*2,300:NADA"

    def folgado(e):  # noqa: D401
        """A rota do `lendarios_sinnoh`, com FOLGA nas pernas que saturam.

        Medido em 21/08/2026: com a contagem exata o jogador parava em (6,12) em
        vez de (6,11), um tile curto. Perna que satura para na parede (ou no
        proprio NPC), entao toque a mais nao custa nada e toque a menos custa o
        caso inteiro; a folga e a forma robusta que o ESTADO ja recomenda para
        roteiro. As pernas EXATAS ficam exatas, porque nelas toque a mais anda.
        """
        r = LS.roteiro_de(
            dict(e, rota=[(D, n + 4 if sat else n, sat) for D, n, sat in e["rota"]]),
            False)
        # E a espera INICIAL de 60 quadros do `roteiro_de` nao chega para uma
        # PORTA de interior: medido em 21/08/2026, com 60 os primeiros apertos
        # sao engolidos pelo fade do warp e o jogador para um tile antes; com
        # 240 ele chega. Espera e de graca, aperto perdido nao e.
        assert r.startswith("60:NADA,"), r[:20]
        r = r[len("60:NADA,"):]
        # E a espera ENTRE pernas tambem: o primeiro passo do roteiro e uma
        # perna que ZERA, ou seja um aperto contra parede so para fixar a
        # direcao do boneco. Aqui esse aperto e DOWN em cima do TILE DE PORTA em
        # (6,12), e o motor gasta quadros nisso. Medido: com 40 quadros de folga
        # o jogador nao anda depois; com 240 ele anda. Isolado por par
        # diagnostico (mesma rota, so a espera muda).
        return "240:NADA," + r.replace("40:NADA", "240:NADA")

    return [
        dict(id="T129.3",
             nome=(
                 "O NPC do laboratorio do Birch ENTREGA o inicial de Hoenn "
                 "escolhido. Medido em 21/08/2026 e por isso este caso existe: "
                 "SPECIES_TREECKO, SPECIES_TORCHIC e SPECIES_MUDKIP nao existiam "
                 "neste jogo em lugar nenhum fora de data/scripts/debug.inc, e o "
                 "laboratorio entregava Chikorita, Cyndaquil e Totodile. A "
                 "abertura do jogo NAO foi tocada: isto e um NPC a mais na sala, "
                 f"em {a['T']}, com tile medido pela mesma busca em largura dos "
                 "lendarios (alcancavel, sem ilhar ninguem, longe do Aide, que e "
                 "MOVEMENT_TYPE_WANDER_AROUND). A rota tem a ultima perna "
                 f"saturando CONTRA o NPC e para em {a['para']}. Os A seguintes "
                 "abrem a fala, avancam e escolhem a PRIMEIRA linha do "
                 "dynmultichoice, que e o "
                 f"{primeiro.replace('SPECIES_', '')}. A prova nao e 'o time "
                 "cresceu': e a ESPECIE lida do gPlayerParty pela decifracao do "
                 "substruct 0, com `time_jogador` ligado. Par negativo: T129.4."),
             flags=["FLAG_SEM_ENCONTRO_SELVAGEM"],
             warp=mapa, warp_id=a["warp"], time_jogador=True,
             roteiro=folgado(a) + escolhe,
             prova=dict(mapa=mapa, time=1,
                        campos={"especie0": num[primeiro]})),
        dict(id="T129.4",
             nome=(
                 "PAR NEGATIVO DO T129.3: a MESMA rota, SEM apertar A. O time "
                 "continua vazio e o jogador para "
                 f"em {a['para']}, encostado no NPC. Sem este caso o positivo "
                 "passaria num jogo em que o inicial ja estivesse no time desde "
                 "o comeco, e tambem num jogo em que o NPC esta la mas nao "
                 "responde, que e exatamente o defeito dos dois Pokecenters "
                 "mudos de Sinnoh: 'o NPC esta la' nao e 'da para falar com ele'."),
             flags=["FLAG_SEM_ENCONTRO_SELVAGEM"],
             warp=mapa, warp_id=a["warp"], time_jogador=True,
             roteiro=folgado(a),
             prova=dict(mapa=mapa, time=0, pos=list(a["para"]))),
        dict(id="T129.5",
             nome=(
                 "O NPC de distribuicao entrega os event-only, e o primeiro que "
                 f"cai no time e o {evento[0]['especie'].replace('SPECIES_', '')}. "
                 f"Sao {len(evento)} entradas SEM gfx de overworld (os bones do "
                 "Pikachu, o Pichu de orelha espetada, o Pikachu e o Eevee "
                 "iniciais, e as lendas que nao tem desenho de overworld): elas "
                 "NAO podem virar encontro estatico, porque object_event exige "
                 "OBJ_EVENT_GFX_SPECIES, e por isso vao por `givemon`. O que "
                 "nao couber no time vai para o PC, entao a prova de time e 6 e "
                 "nao "
                 f"{len(evento)}. O NPC fica em {b['T']}, medido pela mesma "
                 f"busca em largura, e a rota para em {b['para']}."),
             flags=["FLAG_SEM_ENCONTRO_SELVAGEM"],
             warp=mapa, warp_id=b["warp"], time_jogador=True,
             roteiro=folgado(b) + fala,
             prova=dict(mapa=mapa, time=6,
                        campos={"especie0": num[evento[0]["especie"]]})),
    ]


def const_do_mapa(pasta):
    """MAP_MT_CORONET_B1F a partir de `MtCoronet_B1F`, LIDO do proprio map.json.

    O `lendarios_sinnoh` escreve esse nome a mao na tabela dele porque sao 11
    linhas. Aqui sao 106, e nome de constante nao se decora: `ViridianForest_Frlg`
    e `MAP_VIRIDIAN_FOREST`, sem o sufixo.
    """
    return json.load(open(f"{RAIZ}/data/maps/{pasta}/map.json",
                          encoding="utf-8"))["id"]


def _mais_longe(regiao):
    """O estatico da regiao mais distante do warp de chegada. Sem empate: a
    distancia desempata pelo nome da especie, entao a escolha e estavel."""
    linhas = [l for l in tabela()["estaticos"]
              if l["regiao"] == regiao and l.get("rota_irmas")]
    if not linhas:
        return None
    return max(linhas, key=lambda l: (
        max(abs(l["tile"][0] - l["porta"][0]), abs(l["tile"][1] - l["porta"][1])),
        l["especie"]))


def sem_corrida(roteiro):
    """16 quadros por toque EMPATA com o passo do jogador; 17 nao.

    Medido em 21/08/2026 no MtCoronet_B1F, com par diagnostico (mesma rota, so
    o numero de quadros muda): com `16:DOWN*n` o jogador anda n-2 tiles, com
    `17:`, `18:`, `20:` e `24:` ele anda n-1, que e o que a rota promete. Um
    passo custa exatamente 16 quadros, entao o toque seguinte cai no mesmo
    quadro em que o passo acaba e um deles se perde. Numa perna que SATURA isso
    nao aparece (toque a mais nao custa nada, e por isso o T123, que so tem
    perna de zerar e perna saturante, nunca viu o defeito); numa perna EXATA de
    41 tiles, como a do Mt. Coronet, o jogador para um tile antes e o caso
    inteiro reprova.

    Fica aqui e nao no `roteiro_de` porque o T123 ja esta gravado com 16 e
    passando: mexer la reescreveria 22 casos que ninguem pediu para mexer.
    """
    return roteiro.replace("16:", "17:")


def casos_estaticos():
    """Fumaca: UM estatico por regiao, com par negativo, no idioma do T123.

    Nao sao os 106. Sao 5 pares, um por regiao, no bicho MAIS LONGE do warp de
    chegada de cada uma, que e o caso mais caro de andar e portanto o que mais
    tem chance de pegar rota errada, tile errado ou objeto que nao nasceu. Os
    outros 101 saem depois, um por especie, escritos em cima desta mesma forma.

    A prova NAO e "o objeto esta no map.json": e o jogador ANDANDO ate encostar
    nele. A perna final satura contra o Pokemon e para em `para`; com a flag de
    HIDE acesa o tile fica vazio e a MESMA perna escorrega ate `vazio`. A
    diferenca entre os dois casos e exatamente UMA flag, e e isso que prova que
    a flag escrita no object_event e a mesma que o script acende ao vencer.
    """
    fora = []
    i = 7
    for regiao in CINCO:
        l = _mais_longe(regiao)
        if l is None:
            continue
        e = dict(T=tuple(l["tile"]), warp=l["warp"], dir=l["dir"],
                 para=tuple(l["para"]), vazio=tuple(l["vazio"]),
                 porta=tuple(l["porta"]), pouso=tuple(l["pouso"]),
                 rota=[tuple(x) for x in l["rota"]])
        const = const_do_mapa(l["mapa"])
        curto = l["especie"].replace("SPECIES_", "")
        rota = " ".join(f"{D}*{n}" if n else f"{D}(zera)" for D, n, _ in e["rota"])
        fora.append(dict(
            id=f"T129.{i}",
            nome=(
                f"{curto} EXISTE EM {const} ({regiao}) E A INTERACAO TRAVA O "
                f"JOGADOR. Fumaca da onda B1 da dex: sao 106 estaticos novos e "
                f"este e o de {regiao} MAIS LONGE do warp de chegada, que e o "
                f"caso mais caro de andar. O tile {tuple(e['T'])} saiu da mesma "
                f"busca em largura do T123 (colisao E elevacao, portao de que "
                f"por o bicho ali nao ilha nenhum tile do mapa, 3 tiles de "
                f"folga de NPC que anda) e passou tambem pelo teto de sprite: "
                f"nenhuma janela de 20x17 tiles do mapa fica com mais de "
                f"{TETO_SPRITE} objetos, senao o motor deixaria de acordar o "
                f"lendario sem dizer nada. ROTA: {rota}, a partir do warp "
                f"{e['warp']} ({e['porta'][0]},{e['porta'][1]}), pousando em "
                f"{tuple(e['pouso'])}. A ultima perna satura CONTRA o Pokemon e "
                f"para em {tuple(e['para'])}. O A abre o msgbox de abertura, que "
                f"comeca com lockall, e por isso a perna de volta NAO move o "
                f"jogador; o msgbox vem ANTES do playmoncry justamente para a "
                f"prova parar na caixa de texto, sem entrar na batalha, que o "
                f"harness nao le. Par negativo: T129.{i + 1}."),
            flags=["FLAG_SEM_ENCONTRO_SELVAGEM"],
            warp=const, warp_id=e["warp"],
            roteiro=sem_corrida(LS.roteiro_de(e, True)),
            prova=dict(mapa=const, pos=list(e["para"]))))
        fora.append(dict(
            id=f"T129.{i + 1}",
            nome=(
                f"PAR NEGATIVO DO T129.{i}: com {l['flag']} ACESA o tile "
                f"{tuple(e['T'])} esta VAZIO. MESMA rota (o positivo so "
                f"acrescenta o A e a perna de volta), e a perna final escorrega "
                f"ate {tuple(e['vazio'])} em vez de parar em {tuple(e['para'])}. "
                f"Sem ele o positivo nao prova nada: parada de jogador tem muitas "
                f"causas (parede, elevacao, mapa que nao carregou), e a diferenca "
                f"entre os dois casos e exatamente UMA flag. E tambem a prova de "
                f"que a flag de HIDE escrita no campo `flag` do object_event e a "
                f"mesma que o script acende ao vencer ou capturar. O `andou` "
                f"prova que o jogo continua respondendo."),
            flags=["FLAG_SEM_ENCONTRO_SELVAGEM", l["flag"]],
            warp=const, warp_id=e["warp"],
            roteiro=sem_corrida(LS.roteiro_de(e, False)),
            prova=dict(mapa=const, pos=list(e["vazio"]), andou=True)))
        i += 2
    return fora


def aplica_casos(gravar):
    """Escreve os casos GERADOS e preserva os escritos a mao.

    Os 101 casos de estatico que faltam serao escritos por outros executores
    neste mesmo arquivo, em append. Se este passo continuasse sobrescrevendo o
    arquivo inteiro, `--presentes` (que roda `aplica_casos` no fim) apagaria o
    trabalho deles calado. Regra: id que o gerador produz, o gerador manda; id
    que ele nao produz fica onde esta.
    """
    gerados = casos_t129() + casos_estaticos()
    meus = {c["id"] for c in gerados}
    antigo = json.load(open(CASOS, encoding="utf-8")) if os.path.exists(CASOS) else []
    def chave(c):
        a, b = c["id"].split(".")
        return (a, int(b))
    casos = sorted(gerados + [c for c in antigo if c["id"] not in meus], key=chave)
    if antigo == casos:
        return []
    if gravar:
        open(CASOS, "w", encoding="utf-8").write(
            json.dumps(casos, indent=2, ensure_ascii=False) + "\n")
    return [f"testes_criticos/129_dex_completa.json: {len(casos)} casos "
            f"({len(gerados)} gerados, {len(casos) - len(gerados)} a mao)"]

if __name__ == "__main__":
    main()
