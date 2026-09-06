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
CASOS_FORMA = f"{RAIZ}/dev_scripts/testes_criticos/137_dex_formas.json"
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

# EXCECAO NOMEADA a regra 3, e a unica que existe. Especie que ficou
# inobtenivel porque a REMOCAO FISICA dos mapas cortados
# (`remove_mapas_cortados.py`, 22/08/2026) apagou a tabela de mato onde ela
# morava volta para a regiao de onde o corte a tirou, e nao para a regiao da
# geracao dela. Razao: isto e REPOSICAO de um lar destruido por obra nossa, e
# nao colocacao nova, e mandar o Surskit para Hoenn (gen 3) tiraria de Sinnoh
# uma especie que a FONTE tinha posto la. A regra 3 continua valendo para todo
# o resto; a excecao fica escrita aqui para nao ser silenciosa.
#
# Medido em 22/08/2026: a `Route229` era a UNICA casa de Surskit e Masquerain
# no jogo inteiro, `water_mons`, e saiu com a Battle Zone. O Masquerain NAO
# ganha linha de mato: e Bug/Flying, a regra 6 proibe agua para quem nao e
# TYPE_WATER, e ele sai de graca do Surskit por `EVO_LEVEL` 22.
REPOE_NA_REGIAO = {"SPECIES_SURSKIT": "Sinnoh"}

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
        # `galar_selvagens` entra na MESMA desmontagem desde 07/09/2026: sem
        # ela, a segunda rodada de `--tabela` veria o slot ja escrito como se
        # nao fosse mais duplicado, escolheria outro, e a linha antiga ficaria
        # orfa com a especie nova gravada para sempre.
        for chave in ("selvagens", "galar_selvagens"):
            for l in antigo.get(chave, []):
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


def tabelas_de_encontro(mapa_regiao, regioes=CINCO):
    """[(mapa, tipo, regiao, perfil_de_tipos, [indices de slot duplicado])].

    Slot duplicado = a especie daquele indice ja apareceu ANTES na mesma tabela
    e no mesmo tipo. Trocar o segundo nao tira nada do jogo: a especie da fonte
    continua na primeira ocorrencia. Foi assim que o censo mediu 5.622 deles.

    `regioes` existe desde 07/09/2026 (cartucho 2): a obra de Galar chama esta
    mesma funcao com `("Galar",)`, e o padrao continua sendo as CINCO, para que
    nenhuma linha das cinco regioes mude de slot por causa dela.
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
            if regiao not in regioes:
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
    nossas = {l["especie"] for k in BUCKETS + BUCKETS_GALAR
              for l in gravada.get(k, [])}

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


ITEM_DE_USO = ("FORM_CHANGE_ITEM_USE", "FORM_CHANGE_ITEM_USE_MULTICHOICE")


def _itens_citados_em_data():
    """Todo ITEM_* que aparece em `data/`: giveitem, additem, bola de item,
    pokemart. E a unica prova barata de que o jogo ENTREGA o item."""
    fora = set()
    for cam in glob.glob(f"{RAIZ}/data/**/*", recursive=True):
        if not cam.endswith((".inc", ".json")):
            continue
        txt = open(cam, encoding="utf-8", errors="ignore").read()
        # O PROPRIO bloco desta ferramenta sai da varredura. Sem isto a
        # segunda rodada de `--tabela` acha os nove itens ja citados em
        # `data/`, conclui que o jogo os entrega e APAGA as linhas de
        # `chaves` da tabela; a de `--presentes` seguinte tiraria o
        # `additem` do NPC. Mesma armadilha que `censo_base` desarma para o
        # mato, e sem uma linha de erro na tela.
        txt = re.sub(re.escape(INC_INI) + r".*?" + re.escape(INC_FIM), "",
                     txt, flags=re.S)
        # COMENTARIO NAO ENTREGA ITEM. `data/maps/RotomsRoom/scripts.inc:44`
        # cita ITEM_ROTOM_CATALOG dentro de um `@` explicativo, e so por causa
        # dessa linha o Rotom Catalog saia da lista de chaves: a ferramenta
        # concluia que o jogo entrega o item, o NPC do laboratorio parava de
        # dar, e as cinco formas do Rotom voltavam a ser inobteniveis sem uma
        # linha de erro. Medido em 23/08/2026, no `--demo` do fechador da
        # rodada 12. Comentario de `.inc` comeca em `@` e vai ate o fim da
        # linha; `.json` nao tem comentario, entao a poda so cabe aqui.
        if cam.endswith(".inc"):
            txt = re.sub(r"@[^\n]*", "", txt)
        fora.update(re.findall(r"\bITEM_[A-Z0-9_]+", txt))
    return fora


def chaves_de_forma(fmc):
    """Os itens-chave que uma troca de forma exige e que o jogo NAO entrega.

    Medido em 22/08/2026: nove itens de `FORM_CHANGE_ITEM_USE*` nao apareciam
    em UMA linha de `data/` (Gracidea, os quatro nectares, Prison Bottle,
    Reveal Glass, Rotom Catalog e Zygarde Cube). O censo nunca olhou para o
    item, entao contava as formas deles como obteniveis com o item fora do
    jogo: a conta da Dex estava certa no papel e mentia no cartucho. Aqui o
    item vira linha de decisao e sai pelo MESMO NPC de presente do
    laboratorio, que ja e o guarda-chuva de tudo que nao tem lugar proprio.
    """
    citados = _itens_citados_em_data()
    destrava = collections.defaultdict(set)
    for alvo, origens in fmc.items():
        for _de, t_, par in origens:
            if t_ not in ITEM_DE_USO:
                continue
            m = re.match(r"(ITEM_[A-Z0-9_]+)", (par or "").strip())
            if m and m.group(1) not in citados:
                destrava[m.group(1)].add(alvo)
    return [dict(item=k, como="chave", mapa=MAPA_PRESENTE, metodo="additem",
                 origem="censo",
                 destrava=sorted(x.replace("SPECIES_", "") for x in v),
                 nota=f"{len(v)} entrada(s) de Dex dependiam deste item e "
                      "nenhuma linha de data/ o entregava")
            for k, v in sorted(destrava.items())]


def chaves_de_acesso():
    """Item-chave de ACESSO: o que abre MAPA, e nao o que troca de forma.

    `chaves_de_forma` so olha `FORM_CHANGE_ITEM_USE`, entao nao enxerga este
    caso, e o filtro `_itens_citados_em_data` tambem nao ajudaria: o Aurora
    Ticket APARECE em `data/`, com um `giveitem` que mora dentro do Mystery
    Gift (`data/scripts/gift_aurora_ticket.inc`), que este cartucho nao tem.
    O item passava por entregue e nao era.

    Medido em 23/08/2026: sem ele, `FLAG_ENABLE_SHIP_BIRTH_ISLAND` nunca
    acende, o menu da balsa de Lilycove (src/script_menu.c, que cobra bolsa E
    flag) nunca lista a Birth Island, o Seagallop de Vermilion tampouco, e as
    DUAS Birth Island ficam sem uma porta: o Deoxys da Dex tinha estatico,
    mapa e script, e nenhum caminho ate ele. A regra da pesquisa de lendarios
    (`dev_scripts/lendarios_referencia.csv`, linha 22) ja mandava "nao copiar
    o gate por Mystery Gift"; aqui ela vira codigo. O portao de ENREDO fica de
    pe: a balsa so atende com `FLAG_SYS_GAME_CLEAR`, entao Deoxys continua
    pos-Liga.
    """
    return [dict(item="ITEM_AURORA_TICKET", como="chave", mapa=MAPA_PRESENTE,
                 metodo="additem", flag="FLAG_ENABLE_SHIP_BIRTH_ISLAND",
                 origem="pesquisa",
                 destrava=["DEOXYS_ATTACK", "DEOXYS_DEFENSE",
                           "DEOXYS_NORMAL", "DEOXYS_SPEED"],
                 nota="as duas Birth Island nao tinham porta: o unico "
                      "`giveitem` deste item mora no Mystery Gift, que este "
                      "cartucho nao tem. A flag da balsa sai junto com o item")]


def formas_em_cadeia(alc_direto, fmc):
    """As entradas que so aparecem depois de DUAS ou mais trocas de forma.

    Eram os 5 "inobteniveis" de 22/08/2026 (Deoxys-Defesa, Deoxys-Velocidade,
    Zygarde-10%-Power-Construct, Zygarde-Completo e Zygarde-Mega). Nenhum era
    questao de lugar: `censo_dex.censo()` fechava a alcancabilidade so por
    EVOLUCAO e testava a troca de forma contra esse fecho, entao enxergava UM
    passo de forma e a corrente de dois quebrava calada. O fecho de forma
    entrou no censo; esta lista existe para a tabela registrar quais entradas
    dependiam dele, e serve de sentinela: se ela crescer, apareceu corrente
    nova que ninguem conferiu.
    """
    profund, fila = {n: 0 for n in alc_direto}, list(alc_direto)
    while fila:
        atual = fila.pop()
        for alvo, origens in fmc.items():
            if alvo in profund:
                continue
            for de, t_, _p in origens:
                if de == atual and t_ not in censo_dex.FORMA_REVERTE:
                    profund[alvo] = profund[atual] + 1
                    fila.append(alvo)
                    break
    cat = catalogo_completo()
    return [dict(especie=n, como="forma", regiao="", mapa="", metodo="",
                 slot=None, nivel=0, flag="", origem="censo",
                 passos=profund[n],
                 nota=f"{profund[n]} trocas de forma a partir de "
                      + "; ".join(sorted(
                          de.replace("SPECIES_", "") for de, t_, _p in fmc[n]
                          if t_ not in censo_dex.FORMA_REVERTE
                          and profund.get(de, 99) == profund[n] - 1)))
            for n in sorted((x for x, d in profund.items()
                             if d >= 2 and x in cat),
                            key=lambda n: (cat[n].dex, n))]


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
    _PLANO["chaves"] = sorted(chaves_de_forma(fmc) + chaves_de_acesso(),
                               key=lambda l: l["item"])
    direta = {l.nome for l in linhas
              if l.categoria in ("selvagem", "estatico", "presente", "troca",
                                 "evolucao")}
    _PLANO["formas"] = formas_em_cadeia(_fecha(direta | diretos, evo, {}), fmc)
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
    # MAPA SEM WARP NENHUM: `LS.planeja` indexa `warp_events[warp_id]` sem
    # perguntar, e o `max(1, ...)` de antes mandava ele ler o warp 0 de uma
    # lista vazia. Nas cinco regioes isso nunca aconteceu porque todo mapa tem
    # porta; metade da Wild Area de Galar so tem CONEXAO, e ali o `--estaticos`
    # morria com IndexError em vez de dizer "este mapa nao serve". Sem warp nao
    # ha rota de caso critico, entao o mapa realmente nao serve.
    warps = len(d.get("warp_events", []))
    if not warps:
        return None
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
# FORA de BUCKETS de proposito: `censo_base` varre BUCKETS por `especie` para
# desmontar o que ja foi aplicado, e linha de `chaves` nao tem especie.
EXTRAS = ("chaves", "formas")


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
    agua separada de terra (6) e rodizio de regiao para cosmetico (10).

    ESTAVEL contra arvore ja mexida (22/08/2026): quem ja tem escolha GRAVADA e
    ainda valida (a tabela existe, o slot continua duplicado e ainda guarda a
    especie que a linha diz ter substituido) FICA ONDE ESTA, e so o resto e
    replanejado. Sem isto, uma especie nova no meio da lista empurra a escolha
    de todas as seguintes um slot adiante, e `aplica_selvagem` deixa ORFA a
    linha antiga que a tabela nova nao menciona mais: o slot velho continua com
    a especie nova escrita e ninguem mais o restaura. Medido: a remocao fisica
    dos mapas cortados matou a tabela da `Route229` e o replanejamento sem esta
    trava mexia em NOVE linhas que ninguem pediu, uma delas deixando a
    `SeafloorCavernRoom1` com um Salazzle-Totem no lugar do Zubat para sempre.
    """
    tabelas = tabelas_de_encontro(censo_dex.mapas())
    livres = {(t["mapa"], t["tipo"]): list(t["dup"]) for t in tabelas}
    por_chave = {(t["mapa"], t["tipo"]): t for t in tabelas}
    usos = collections.Counter()
    cota = collections.Counter()
    ordem_cosmetica = collections.Counter()

    reserva = {}
    for l in tabela_gravada().get("selvagens", []):
        chave = (l["mapa"], l["metodo"])
        if l["especie"] not in nomes or chave not in livres:
            continue
        if l["slot"] not in livres[chave]:
            continue
        if _nivel_do_slot(l["mapa"], l["metodo"], l["slot"])[1] != l["substituido"]:
            continue
        livres[chave].remove(l["slot"])
        usos[chave] += 1
        cota[por_chave[chave]["regiao"]] += 1
        reserva[l["especie"]] = (por_chave[chave], l["slot"], l["origem"])

    fora = []
    for n in nomes:
        e = cat[n]
        tipos = set(e.tipos)
        grupo = AGUA if "TYPE_WATER" in tipos else TERRA
        if n in reserva:
            # O rodizio de cosmetico continua correndo, senao a familia inteira
            # muda de pino so porque um irmao ficou reservado.
            if eh_cosmetica(n):
                ordem_cosmetica[_familia(n)] += 1
            t, slot, origem = reserva[n]
            nivel, antes = _nivel_do_slot(t["mapa"], t["tipo"], slot)
            fora.append(dict(especie=n, como="selvagem", regiao=t["regiao"],
                             mapa=t["mapa"], metodo=t["tipo"], slot=slot,
                             nivel=nivel, flag="", origem=origem,
                             substituido=antes,
                             nota=f"gen {e.gen}; tipos "
                                  f"{'/'.join(x.replace('TYPE_', '') for x in e.tipos)}; "
                                  f"slot duplicado {slot} de {t['n']}"))
            continue
        if n in REPOE_NA_REGIAO:
            permitidas, origem = [REPOE_NA_REGIAO[n]], "corte"
        elif eh_cosmetica(n):
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
        "totais": {k: len(p[k]) for k in BUCKETS + EXTRAS + BUCKETS_GALAR},
        **p,
    }
    novo = json.dumps(d, indent=2, ensure_ascii=False) + "\n"
    velho = open(TABELA, encoding="utf-8").read() if os.path.exists(TABELA) else ""
    if novo == velho:
        return []
    if gravar:
        open(TABELA, "w", encoding="utf-8").write(novo)
    todos = BUCKETS + EXTRAS + BUCKETS_GALAR
    return [f"dex_distribuicao.json: {sum(len(p[k]) for k in todos)} "
            f"linhas ({', '.join(f'{k} {len(p[k])}' for k in todos)})"]


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
          "\tfaceplayer"]
    # As chaves de troca de forma vem ANTES do `goto_if_set`, e de proposito:
    # a guarda e o `checkitem` de cada item, nao a flag do NPC. Assim quem
    # falou com ele de bolso cheio ganha o item na proxima fala, em vez de
    # perde-lo para sempre; e quem ja tem tudo nao ve nada acontecer.
    # `additem` no lugar de `giveitem` porque `giveitem` abre janela e fanfarra
    # nove vezes seguidas.
    for l in tabela().get("chaves", []):
        p += [f"\tcheckitem {l['item']}",
              f"\tcall_if_eq VAR_RESULT, FALSE, {m}_EventScript_DexChave"
              + l["item"].replace("ITEM_", "").title().replace("_", "")]
    p += [f"\tgoto_if_set FLAG_DEX_PRESENTE_EVENTO, {m}_EventScript_DexDistribuicaoJaDeu",
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
          '\t.string "Whatever does not fit in your\\n"',
          '\t.string "party goes to your PC.\\p"',
          '\t.string "The odd trinkets are in your KEY\\n"',
          '\t.string "ITEMS. Some POKéMON change shape\\l"',
          '\t.string "when you use them.$"', ""]
    for l in tabela().get("chaves", []):
        p += [f"{m}_EventScript_DexChave"
              + l["item"].replace("ITEM_", "").title().replace("_", "") + "::",
              f"\tadditem {l['item']}"]
        # Chave de ACESSO carrega a flag do transporte junto: o item sozinho
        # nao abre a balsa, o menu cobra os dois (src/script_menu.c).
        if l.get("flag"):
            p += [f"\tsetflag {l['flag']}"]
        p += ["\treturn",
              ""]
    p += [INC_FIM]
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


# ----------------------------------------------- Galar (cartucho 2, onda 2)
#
# Por que existe um bloco separado para UMA regiao
# ------------------------------------------------
# O resto deste arquivo distribui quem estava INOBTENIVEL no censo. A obra de
# Galar e outra pergunta, e ela nasce do cartucho 2: as quatro regioes do
# cartucho 1 (Kanto, Johto, Hoenn e Sinnoh) SAEM, e toda especie cuja unica
# fonte esteja la deixa de existir para quem jogar o cartucho 2. Medido em
# 07/09/2026: 46 entradas de geracao 8 tem fonte direta e NENHUMA em Galar, e
# 31 delas so tem fonte nas quatro regioes que saem. A geracao de Galar
# precisando de Kanto para existir e o defeito que este bloco fecha.
#
# A regua e a MESMA das cinco regioes, e por isso o bloco reusa `_melhor_tabela`
# (slot duplicado, bioma por perfil de tipos, agua separada de terra), `cabe` /
# `_encaixa` (a geometria do `lendarios_sinnoh`, ja provada pelo T123) e
# `nivel_de`. O que muda e so o conjunto de mapas e a lista de entrada.
#
# QUEM ENTRA, e por que nao sao as 140
# ------------------------------------
# O apendice do `onda1_lote_e_pedidos_scripts.txt` lista 140 entradas de gen 8
# sem fonte em Galar. 94 delas sao `evolucao`, `forma_batalha` ou
# `forma_permanente`: elas nao tem fonte em regiao NENHUMA, nem aqui nem nas
# cinco, porque saem de outra coisa. Dar objeto a um Alcremie-Morango-Creme de
# Rubi seria inventar fonte que a regra 10 nao pede. Sobram as 46 com fonte
# direta, e dessas entram so as RAIZES: quem ja sai de graca de uma especie que
# Galar tem (Thwackey sai do Grookey) nao ganha linha, exatamente como o
# `plano()` faz com o efeito cascata. O fecho e o `_fecha`, com a semente
# restrita a quem tem fonte em Galar.
#
# ONDE ESTE BLOCO PODE ESCREVER
# -----------------------------
# So no `wild_encounters.json` e na propria tabela de decisao. Estatico e
# presente viram PEDIDO em `dev_scripts/onda2_lote_h_pedidos_scripts.json`,
# porque `data/maps/Galar_*/map.json` e `data/scripts/galar_*.inc` sao de
# outros executores nesta onda. A flag de cada estatico ja vem escolhida, na
# faixa 0x2280-0x22FF, que e exclusiva deste lote.
PEDIDOS_GALAR = f"{RAIZ}/dev_scripts/onda2_lote_h_pedidos_scripts.json"
FLAG_GALAR_BASE = 0x2280
FLAG_GALAR_TETO = 0x22FF

# Area canonica -> mapas dela no repo, na ordem em que o encaixe tenta. A ordem
# saiu da CAPACIDADE medida (`cabe`) em 07/09/2026, e nao do tamanho do mapa:
# `Galar_RoseTower04` e o topo da torre e cabe ZERO, `Galar_CrownTundra13` ja
# tem 38 objetos e estoura a janela de sprite.
AREA_GALAR = {
    "weald": ("Galar_SlumberingWeald03", "Galar_SlumberingWeald04",
              "Galar_SlumberingWeald01", "Galar_SlumberingWeald02"),
    "torre": ("Galar_RoseTower01", "Galar_RoseTower02", "Galar_RoseTower03"),
    "armadura": ("Galar_IsleOfArmor05", "Galar_IsleOfArmor07",
                 "Galar_IsleOfArmor08", "Galar_IsleOfArmor12",
                 "Galar_IsleOfArmor06", "Galar_IsleOfArmor10",
                 "Galar_IsleOfArmor03", "Galar_IsleOfArmor04"),
    "tundra": ("Galar_CrownTundra10", "Galar_CrownTundra11",
               "Galar_CrownTundra12", "Galar_CrownTundra14",
               "Galar_CrownTundra15", "Galar_CrownTundra16",
               "Galar_CrownTundra18", "Galar_CrownTundra01",
               "Galar_CrownTundra02", "Galar_CrownTundra03"),
}

# LAR CANONICO (regra 8), aqui lido do jogo de origem e escrito uma linha por
# lenda, no lugar do `lendarios_referencia.csv`, que nao tem coluna de Galar.
LAR_GALAR = {
    "SPECIES_ZACIAN_HERO": "weald",       # onde o jogo os apresenta
    "SPECIES_ZAMAZENTA_HERO": "weald",
    "SPECIES_ETERNATUS": "torre",         # Torre Rose / usina de energia
    "SPECIES_KUBFU": "armadura",          # dojo da Ilha da Armadura
    "SPECIES_ZARUDE": "armadura",         # floresta da mesma ilha
    "SPECIES_REGIELEKI": "tundra",        # os quatro da Tundra da Coroa
    "SPECIES_REGIDRAGO": "tundra",
    "SPECIES_CALYREX_ICE": "tundra",
    "SPECIES_CALYREX_SHADOW": "tundra",
    "SPECIES_ENAMORUS_INCARNATE": "tundra",
}

# Cauda da preferencia, para quem nao tem lar canonico. Mesma ideia do `BIOMA`
# das cinco regioes, em tabela PROPRIA: por Galar dentro daquele dicionario
# mudaria a escolha dos 106 estaticos ja gravados, porque a cota de Galar
# comeca em zero e ganharia todo desempate.
BIOMA_GALAR = {
    "floresta": "Galar_GlimwoodTangle01",
    "caverna": "Galar_GalarMine01",
    "ruina": "Galar_CrownTundra18",
    "agua": "Galar_IsleOfArmor07",
    "neve": "Galar_CrownTundra11",
    "vulcao": "Galar_GalarMine05",
    "ceu": "Galar_RoseTower01",
    "cidade": "Galar_IsleOfArmor05",
}
POOL_GALAR = tuple(m for a in ("tundra", "armadura", "weald", "torre")
                   for m in AREA_GALAR[a])

# Mapa do NPC de presente. Wedgehurst e onde mora o laboratorio no jogo de
# origem, e o `Galar_Wedgehurst01` e o primeiro da familia que tem DUAS colunas
# de warp livres para a regra do NPC (medido, ver `decide_npcs_presente`).
MAPAS_PRESENTE_GALAR = ("Galar_Wedgehurst01", "Galar_Wedgehurst02",
                        "Galar_Wedgehurst03", "Galar_Wedgehurst05")

BUCKETS_GALAR = ("galar_selvagens", "galar_estaticos", "galar_presentes",
                 "galar_evolucoes")

# OS TRÊS INICIAIS DE GALAR SAEM DO MATO E VIRAM PRESENTE (decisão da condutora
# da onda 2, 07/09/2026). Sem esta lista, `plano_galar` os classifica como
# `selvagem` (não são lenda) e o rodízio de bioma os espalha por slot duplicado:
# na tabela de 07/09 o Grookey caiu em `MAP_GALAR_UNDERWATER_02`, o Scorbunny em
# `MAP_GALAR_MOTOSTOKE_18` e o Sobble num slot de pesca. Inicial não nasce no
# mato em jogo nenhum da série, e o molde de presente já existe nesta árvore
# (`data/maps/Unova_NuvemaLab`, três bolas com a MESMA flag de esconder).
INICIAIS_GALAR = ("SPECIES_GROOKEY", "SPECIES_SCORBUNNY", "SPECIES_SOBBLE")

# WEDGEHURST NÃO TEM LABORATÓRIO, e isso foi MEDIDO em 07/09/2026, não presumido:
# nenhum dos 17 mapas `Galar_Wedgehurst*` tem NPC de cientista (`OBJ_EVENT_GFX_
# SCIENTIST_*`), e as únicas citações da Sonia em Galar estão em NPC de rua
# (`Galar_Route0202`) e da praça (`Galar_Wedgehurst05`). O prédio escolhido é o
# CENTRO POKÉMON, `Galar_Wedgehurst03`, reconhecido por três marcas do próprio
# mapa: `MUS_RG_POKE_CENTER`, `OBJ_EVENT_GFX_NURSE_FRLG` no balcão e
# `MAP_TYPE_INDOOR`. Os três tiles são de (2,5) a (4,5), linha livre encostada na
# parede de baixo, e nenhum deles ilha tile nenhum do mapa (conferido por busca
# em largura contra o blockdata).
MAPA_INICIAL_GALAR = "Galar_Wedgehurst03"
TILE_INICIAL_GALAR = (3, 5)
FLAG_INICIAL_GALAR = "FLAG_INICIAL_GALAR"
FLAG_EVENTO_GALAR = "FLAG_DEX_PRESENTE_EVENTO_GALAR"

# SOBRA DE FIRERED DENTRO DOS GRUPOS DE GALAR. Sao mapas importados junto, e a
# decisao de escopo sobre eles esta ABERTA desde 06/09/2026 (secao 5 do
# `ESTADO-CARTUCHO-2.md`). Mapa que pode ser cortado nao pode receber a UNICA
# fonte de uma especie: se o corte vier, a especie volta a nao existir no
# cartucho 2 e ninguem percebe. Eles continuam com as tabelas que a importacao
# trouxe; o que nao entra ali e colocacao NOVA.
SOBRAS_DE_ESCOPO_GALAR = ("AlteringCave", "LostCave", "LiptooChamber",
                          "RixyChamber", "ScufibChamber", "TanobyKey",
                          "NewmoonIsland")


def flag_galar_de(nome):
    """Nome de flag do estatico de Galar.

    NAO e o `flag_de`: `FLAG_HIDE_DEX_ZACIAN_HERO` ja existe no `flags.h`, do
    Zacian que a onda A pos em Viridian Forest. Duas flags com o mesmo nome
    seriam duas macros com o mesmo nome, e o Zacian de Galar apagaria o de
    Kanto (ou o contrario) sem ninguem ver.
    """
    return "FLAG_HIDE_DEX_GALAR_" + nome.replace("SPECIES_", "")


def raizes_de_galar(linhas, evo, fmc, cat):
    """(raizes, faltavam, alcancaveis_hoje) da geracao 8 dentro de Galar.

    `raizes` sao as entradas que precisam de fonte PROPRIA em Galar: as que
    ficam faltando depois de fechar evolucao e troca de forma a partir de quem
    Galar ja tem. `faltavam` e a lista inteira antes do fecho, para o relatorio
    poder dizer quantas sairam de graca.

    LE O CENSO DE VERDADE, e nao o `censo_base` que o resto do arquivo usa, por
    uma razao medida: o `censo_base` apaga TODO script de especie que esta na
    tabela desta ferramenta, e com ele apaga tambem o estatico de Galar que o
    `estaticos_galar.py` gravou da ROM do demake. Lendo o censo desmontado, 16
    das 45 entradas somem da conta com cara de ja resolvidas.

    A idempotencia vem de outro lugar: as especies que ESTA ferramenta ja
    colocou em Galar saem da semente e voltam para a lista de faltantes, entao
    rodar de novo depois de aplicar da exatamente o mesmo plano.
    """
    minhas = {l["especie"] for k in BUCKETS_GALAR
              for l in tabela_gravada().get(k, [])}
    semente = {l.nome for l in linhas
               if "Galar" in l.regioes.split(",")} - minhas
    direta = ("selvagem", "estatico", "presente", "troca")
    g8 = [l for l in linhas if l.gen == 8]
    faltavam = sorted((l.nome for l in g8
                       if l.categoria in direta
                       and ("Galar" not in l.regioes.split(",")
                            or l.nome in minhas)),
                      key=lambda n: (cat[n].dex, n))
    raizes, diretos = [], set()
    restante = set(faltavam)
    while restante:
        alc = _fecha(semente | diretos, evo, fmc)
        restante = {n for n in faltavam if n not in alc}
        if not restante:
            break
        novas = {n for n in restante if not (_origens(n, evo, fmc) & restante)}
        if not novas:
            novas = restante        # ciclo puro: todos viram raiz
        raizes += sorted(novas, key=lambda n: (cat[n].dex, n))
        diretos |= novas

    # SEGUNDA VOLTA: a entrada de gen 8 que nao tem fonte direta em regiao
    # NENHUMA (ela e `evolucao` ou forma) e cuja UNICA origem e uma especie de
    # outra geracao que Galar tambem nao tem. Aqui nao se coloca a forma, e sim
    # a ORIGEM dela, que e o que o `plano()` das cinco regioes tambem faz com as
    # raizes. Medido em 07/09/2026: existe UMA, e ela fecha a geracao 8 inteira
    # dentro de Galar. `SPECIES_BASCULEGION_F` so sai de
    # `SPECIES_BASCULIN_WHITE_STRIPED`, que hoje so mora em Hoenn e portanto
    # tambem sairia do cartucho 2.
    alc = _fecha(semente | set(raizes), evo, fmc)
    g8 = {l.nome for l in linhas if l.gen == 8}
    for n in sorted(g8 - alc, key=lambda z: (cat[z].dex, z)):
        for o in sorted(_origens(n, evo, fmc)):
            if o in alc or o in raizes or o not in cat:
                continue
            raizes.append(o)
            faltavam.append(o)
            alc = _fecha(semente | set(raizes), evo, fmc)
    return raizes, faltavam, _fecha(semente, evo, fmc)


def decide_selvagem_galar(nomes, cat):
    """Mato de Galar: slot duplicado, bioma por perfil de tipos, agua separada.

    E `decide_selvagem` com a lista de tabelas trocada. A trava de estabilidade
    e a mesma: quem ja tem escolha gravada e ainda valida fica onde esta.
    """
    mapa_regiao = censo_dex.mapas()
    tabelas = [t for t in tabelas_de_encontro(mapa_regiao, regioes=("Galar",))
               if not any(x in mapa_regiao[t["mapa"]][0]
                          for x in SOBRAS_DE_ESCOPO_GALAR)]
    livres = {(t["mapa"], t["tipo"]): list(t["dup"]) for t in tabelas}
    por_chave = {(t["mapa"], t["tipo"]): t for t in tabelas}
    usos = collections.Counter()
    cota = collections.Counter()

    reserva = {}
    for l in tabela_gravada().get("galar_selvagens", []):
        chave = (l["mapa"], l["metodo"])
        if l["especie"] not in nomes or chave not in livres:
            continue
        if l["slot"] not in livres[chave]:
            continue
        if _nivel_do_slot(l["mapa"], l["metodo"], l["slot"])[1] != l["substituido"]:
            continue
        livres[chave].remove(l["slot"])
        usos[chave] += 1
        reserva[l["especie"]] = (por_chave[chave], l["slot"], l["origem"])

    fora = []
    for n in nomes:
        e = cat[n]
        tipos = set(e.tipos)
        grupo = AGUA if "TYPE_WATER" in tipos else TERRA
        if n in reserva:
            t, slot, origem = reserva[n]
        else:
            alvo = _melhor_tabela(tabelas, livres, usos, cota, ["Galar"],
                                  grupo, tipos)
            if alvo is None:
                raise SystemExit(f"{n}: acabaram os slots duplicados de "
                                 f"{'/'.join(grupo)} em Galar. Pare e meca.")
            t, slot, _n = alvo
            origem = "bioma"
            usos[(t["mapa"], t["tipo"])] += 1
        cota["Galar"] += 1
        nivel, antes = _nivel_do_slot(t["mapa"], t["tipo"], slot)
        fora.append(dict(especie=n, como="selvagem", regiao="Galar",
                         mapa=t["mapa"], metodo=t["tipo"], slot=slot,
                         nivel=nivel, flag="", origem=origem,
                         substituido=antes,
                         nota=f"gen {e.gen}; tipos "
                              f"{'/'.join(x.replace('TYPE_', '') for x in e.tipos)}; "
                              f"slot duplicado {slot} de {t['n']}"))
    return fora


def decide_estaticos_galar(nomes, cat):
    """Lenda de Galar: lar canonico primeiro, bioma depois, reserva por ultimo.

    A geometria e a mesma do `decide_estaticos` (busca em largura com colisao e
    elevacao, portao de nao-ilhar, teto de 64 objetos e janela de 15 sprites), e
    a segunda passada (rota com os irmaos como parede) tambem roda. A TERCEIRA
    passada do outro, a do `escorrega`, nao roda aqui: ela existe para o par
    negativo dos casos do T129, e este lote nao gera caso de emulador.
    """
    existem = mapas_existentes()
    usados = collections.defaultdict(set)
    fora = []
    for i, n in enumerate(nomes):
        area = LAR_GALAR.get(n)
        pref = list(AREA_GALAR[area]) if area else []
        origem = "lar canonico" if area else "bioma"
        pref.append(BIOMA_GALAR[bioma_de(cat[n].tipos)])
        pref += [m for m in POOL_GALAR if m not in pref]
        mapa, e = _encaixa(pref, usados, existem)
        if mapa is None:
            raise SystemExit(f"{n}: nenhum mapa de Galar da preferencia nem da "
                             "reserva tem tile livre. Pare e meca.")
        if area and mapa not in AREA_GALAR[area]:
            origem = "bioma"
        usados[mapa].add(e["T"])
        # ELEVACAO DO PROPRIO TILE, e nao o 0 que o aplicador das cinco regioes
        # crava. Em Galar ha mapa com ponte e com nivel de altura de verdade
        # (as pontes da Wild Area), e objeto com elevacao errada some ou fica
        # atravessavel. O fechador aplica o que estiver aqui.
        _d, _W, _H, _g, _o, _m, _w = LS.contexto(mapa)
        elev = LS.elev(_g[e["T"][1]][e["T"][0]])
        curto = n.replace("SPECIES_", "")
        fora.append(dict(especie=n, como="estatico", regiao="Galar", mapa=mapa,
                         elevacao=elev,
                         local_id="LOCALID_DEX_GALAR_%s" % curto,
                         script="%s_EventScript_DexGalar%s"
                                % (mapa, curto.title().replace("_", "")),
                         metodo="objeto+script", slot=None, nivel=nivel_de(n),
                         flag=flag_galar_de(n), origem=origem,
                         tile=list(e["T"]),
                         nota=f"gen {cat[n].gen}; tipos "
                              f"{'/'.join(t.replace('TYPE_', '') for t in cat[n].tipos)}",
                         **_geometria(e)))
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
                l["rota_irmas"] = False
                continue
            l.update(_geometria(e))
            l["rota_irmas"] = True
    fim = FLAG_GALAR_BASE + len(fora) - 1
    if fim > FLAG_GALAR_TETO:
        raise SystemExit(f"{len(fora)} estaticos de Galar nao cabem em "
                         f"0x{FLAG_GALAR_BASE:04X}-0x{FLAG_GALAR_TETO:04X}")
    for i, l in enumerate(fora):
        l["endereco_da_flag"] = "0x%04X" % (FLAG_GALAR_BASE + i)
    return fora


def npcs_presente_galar():
    """Os dois NPCs de presente de Galar, pela MESMA regra do `decide_npcs_presente`
    (mesma coluna de um warp, dois tiles acima dele), agora varrendo uma lista
    de mapas ate um deles ter as duas colunas livres."""
    antigo = tabela_gravada().get("galar_npcs_presente")
    if antigo:
        return antigo
    for mapa in MAPAS_PRESENTE_GALAR:
        d, W, H, g, objs, _m, _w = LS.contexto(mapa)
        sementes = LS.sementes_dos_warps(d, W, H, g)
        base = LS.alcance(W, H, g, sementes, objs)
        fora, tomados = [], set()
        for wid, w in enumerate(d.get("warp_events", [])):
            wx, wy = w["x"], w["y"]
            parada, tile = (wx, wy - 1), (wx, wy - 2)
            if wy < 2 or tile in tomados or parada in tomados:
                continue
            if not (LS.anda(g[parada[1]][parada[0]])
                    and LS.anda(g[tile[1]][tile[0]])):
                continue
            if tile in objs or parada in objs or tile not in base:
                continue
            if LS.alcance(W, H, g, sementes, objs | tomados | {tile}) != \
                    base - tomados - {tile}:
                continue
            fora.append(dict(papel="presente%d" % (len(fora) + 1), mapa=mapa,
                             tile=list(tile), warp=wid, para=list(parada),
                             vazio=list(parada), dir="UP",
                             rota=[["UP", 1, True]]))
            tomados |= {tile, parada}
            if len(fora) == 2:
                return fora
    raise SystemExit("nenhum mapa de MAPAS_PRESENTE_GALAR tem duas colunas de "
                     "warp livres para os NPCs de presente. Pare e meca.")


def decide_presentes_galar(nomes, cat):
    """Quem NAO tem gfx de overworld nao pode ser objeto: vira `givemon` de NPC.

    Mesma decisao que `decide_presentes` toma nas cinco regioes; o que muda e o
    mapa, que aqui e de Galar.
    """
    npcs = npcs_presente_galar()
    fora, i = [], 0
    for n in nomes:
        if n in INICIAIS_GALAR:
            fora.append(dict(
                especie=n, como="presente", regiao="Galar",
                mapa=MAPA_INICIAL_GALAR, metodo="multichoice", slot=None,
                nivel=5, flag=FLAG_INICIAL_GALAR, origem="decisao",
                tile=list(TILE_INICIAL_GALAR), npc="iniciais",
                nota="inicial de Galar: um NPC do Centro Pokemon de "
                     "Wedgehurst entrega um dos tres a escolha, molde do "
                     "laboratorio do Birch"))
            continue
        npc = npcs[i % len(npcs)]
        i += 1
        fora.append(dict(
            especie=n, como="presente", regiao="Galar", mapa=npc["mapa"],
            metodo="givemon", slot=None, nivel=5, flag="", origem="censo",
            tile=list(npc["tile"]), npc=npc["papel"],
            nota="sem gfx de overworld (nao pode ser estatico): givemon por NPC"))
    return fora


_PLANO_GALAR = {}


def plano_galar():
    """As colocacoes de Galar, nos mesmos quatro baldes do plano das cinco."""
    if _PLANO_GALAR:
        return _PLANO_GALAR
    linhas = censo_dex.censo()
    cat = catalogo_completo()
    evo, fmc = censo_dex.evolucoes(), censo_dex.formas()
    por_nome = {l.nome: l for l in linhas}
    raizes, faltavam, _alc = raizes_de_galar(linhas, evo, fmc, cat)
    # MESMA classificacao do `plano()` das cinco regioes, e nao uma parecida:
    # quem NAO e lenda vai para o mato mesmo sem gfx de overworld (linha de
    # tabela nao precisa de sprite); lenda com gfx vira estatico; lenda sem gfx
    # vira presente. Foi assim que o Toxtricity-Gmax ganhou linha de mato em
    # Kanto, e e assim que ele ganha uma em Galar.
    estaticos = [n for n in raizes if por_nome[n].lenda and por_nome[n].ow]
    presentes = [n for n in raizes if por_nome[n].lenda and not por_nome[n].ow]
    selvagens = [n for n in raizes if not por_nome[n].lenda]
    # Os iniciais trocam de balde ANTES do rodízio de bioma, senão eles ocupam
    # slot duplicado de mato e o `substituido` daquele slot vira baseline.
    iniciais = [n for n in selvagens if n in INICIAIS_GALAR]
    selvagens = [n for n in selvagens if n not in INICIAIS_GALAR]
    presentes = iniciais + presentes
    fora = {
        "galar_selvagens": decide_selvagem_galar(selvagens, cat),
        "galar_estaticos": decide_estaticos_galar(estaticos, cat),
        "galar_presentes": decide_presentes_galar(presentes, cat),
    }
    resolvidos = {l["especie"] for k in fora for l in fora[k]}
    fora["galar_evolucoes"] = [
        dict(especie=n, como="evolucao", regiao="Galar", mapa="", metodo="",
             slot=None, nivel=0, flag="", origem="censo",
             nota="sai de graca em Galar depois das colocacoes acima: "
                  + "; ".join(sorted(x.replace("SPECIES_", "")
                                     for x in _origens(n, evo, fmc))
                              or ["troca de forma"]))
        for n in faltavam if n not in resolvidos]
    fora["galar_npcs_presente"] = npcs_presente_galar()
    minhas = {l["especie"] for k in BUCKETS_GALAR
              for l in tabela_gravada().get(k, [])}
    g8 = [l for l in linhas if l.gen == 8]
    fora["_resumo"] = {
        "gen8_com_fonte_em_galar_antes": len(
            {l.nome for l in g8 if "Galar" in l.regioes.split(",")} - minhas),
        "gen8_sem_fonte_em_galar": len(faltavam),
        "colocacoes": len(raizes),
        "gen8_colocadas": sum(1 for n in raizes if cat[n].gen == 8),
        "de_graca_por_evolucao_ou_forma": len(fora["galar_evolucoes"]),
    }
    _PLANO_GALAR.update(fora)
    return _PLANO_GALAR


def escreve_tabela_galar(gravar):
    """Grava SO os baldes de Galar dentro do `dex_distribuicao.json`.

    NAO chama `escreve_tabela`, e isso e deliberado: aquele reescreve o arquivo
    inteiro a partir do censo de HOJE, e o censo de hoje ja e outro (a onda 1
    importou 104 tabelas de encontro de Galar e com elas 592 especies ganharam
    fonte). Regravar o arquivo inteiro apagaria 44 linhas de mato das CINCO
    regioes que ja estao ESCRITAS no `wild_encounters.json`, e o `substituido`
    delas e a unica testemunha de qual especie estava no slot: some a linha,
    some o baseline, e o slot fica com a especie nova para sempre. Quem quiser
    reconciliar a tabela inteira com o censo novo que faca isso de propria
    conta, medindo; nao e obra deste lote e nao pode ser efeito colateral dele.
    """
    p = plano_galar()
    d = json.load(open(TABELA, encoding="utf-8"))
    novo_d = dict(d)
    for k in BUCKETS_GALAR + ("galar_npcs_presente",):
        novo_d[k] = p[k]
    novo_d["totais"] = dict(d.get("totais", {}))
    novo_d["totais"].update({k: len(p[k]) for k in BUCKETS_GALAR})
    novo = json.dumps(novo_d, indent=2, ensure_ascii=False) + "\n"
    if novo == open(TABELA, encoding="utf-8").read():
        return []
    if gravar:
        open(TABELA, "w", encoding="utf-8").write(novo)
    return ["dex_distribuicao.json: baldes de Galar ("
            + ", ".join(f"{k} {len(p[k])}" for k in BUCKETS_GALAR) + ")"]


def escreve_pedidos_galar(gravar):
    """O arquivo de pedidos do lote H: estatico e presente, prontos para aplicar.

    Nao escreve `.inc` nem `map.json` de proposito: nesta onda eles tem outros
    donos. O que sai daqui e a decisao inteira (mapa, tile, elevacao implicita
    do tile, nivel, flag com endereco) para o fechador aplicar sem refazer
    conta nenhuma.
    """
    t = plano_galar()
    d = {
        "gerado_por": "dev_scripts/distribui_dex.py --galar",
        "leia_antes": "Onda 2, lote H (Dex de geracao 8 em Galar). Cada linha e "
                      "um objeto de overworld a criar em data/maps/<mapa>/map.json "
                      "mais a cena em data/scripts/, no mesmo idioma que o "
                      "distribui_dex ja usa nas cinco regioes: estatico = "
                      "OBJ_EVENT_GFX_SPECIES + setwildbattle/seteventmon com a "
                      "flag de HIDE; presente = NPC com givemon. As flags da "
                      "faixa 0x2280-0x22FF sao exclusivas deste lote.",
        "faixa_de_flags": "0x%04X-0x%04X" % (FLAG_GALAR_BASE, FLAG_GALAR_TETO),
        "ordem_de_rodagem": [
            "1. python3 dev_scripts/importa_encontros_galar.py --aplicar   "
            "(reescreve TODAS as entradas de Galar do wild_encounters.json a "
            "partir da ROM do demake; roda SEMPRE antes do passo 2, senao "
            "apaga as linhas de mato da Dex em silencio)",
            "2. python3 dev_scripts/distribui_dex.py --galar --aplica       "
            "(regrava as linhas de mato da Dex e este arquivo de pedidos)",
            "3. python3 dev_scripts/estaticos_galar.py --aplicar            "
            "(o gerador de estatico mudou nesta rodada: a traducao de especie "
            "ganhou o `.` das formas regionais e o bloco de Alola. O diff "
            "medido em --seco e +204/-204 linhas no galar_estaticos.inc e "
            "51 linhas em 21 map.json, TODAS de antro de raide que trocou de "
            "especie pela rotacao; nenhum estatico entra nem sai)",
            "4. os objetos e cenas deste arquivo (estaticos e presentes), que "
            "sao de map.json e .inc e por isso ficaram como pedido",
        ],
        "totais": {k: len(t.get(k, [])) for k in BUCKETS_GALAR},
        "npcs_presente": t.get("galar_npcs_presente", []),
        "estaticos": t.get("galar_estaticos", []),
        "presentes": t.get("galar_presentes", []),
    }
    novo = json.dumps(d, indent=2, ensure_ascii=False) + "\n"
    velho = (open(PEDIDOS_GALAR, encoding="utf-8").read()
             if os.path.exists(PEDIDOS_GALAR) else "")
    if novo == velho:
        return []
    if gravar:
        open(PEDIDOS_GALAR, "w", encoding="utf-8").write(novo)
    return [f"onda2_lote_h_pedidos_scripts.json: "
            f"{len(d['estaticos'])} estatico(s) e {len(d['presentes'])} "
            f"presente(s) para o fechador aplicar"]


def aplica_selvagem_galar(gravar):
    """As linhas de mato de Galar, em slot DUPLICADO. Idempotente por baseline.

    ORDEM QUE IMPORTA: `importa_encontros_galar.py --aplicar` REESCREVE todas as
    entradas de Galar do `wild_encounters.json` a partir da ROM do demake, entao
    ele roda ANTES e este depois. Rodar na ordem trocada apaga estas linhas em
    silencio; o `--valida` do outro nao acusa, porque a tabela continua valida.
    """
    d = encontros_base()
    idx = _indice(d)
    conta = collections.Counter()
    # AS LINHAS DAS CINCO REGIOES ENTRAM JUNTO, e nao por gentileza: o
    # `encontros_base()` devolve o JSON DESMONTADO (com o `substituido` de volta
    # em cada slot), entao escrever so as de Galar por cima dele apagaria as 234
    # linhas de mato que a onda A ja aplicou. Medido aqui antes de gravar.
    for l in tabela().get("selvagens", []):
        mons = idx[(l["mapa"], l["metodo"])]
        alvo = mons[l["slot"]]
        if alvo["species"] != l["substituido"]:
            raise SystemExit(
                f"{l['especie']}: o slot {l['slot']} de {l['mapa']}/{l['metodo']} "
                f"nao tem mais {l['substituido']}. Refaca a tabela antes.")
        alvo["species"] = l["especie"]
    for l in plano_galar()["galar_selvagens"]:
        mons = idx[(l["mapa"], l["metodo"])]
        alvo = mons[l["slot"]]
        if alvo["species"] != l["substituido"]:
            raise SystemExit(
                f"{l['especie']}: o slot {l['slot']} de {l['mapa']}/{l['metodo']} "
                f"tem {alvo['species']} e a tabela diz que tinha "
                f"{l['substituido']}. Rode --tabela de novo antes de aplicar.")
        alvo["species"] = l["especie"]
        conta[l["metodo"]] += 1
    novo = json.dumps(d, indent=2, ensure_ascii=False) + "\n"
    if novo == open(ENCONTROS, encoding="utf-8").read():
        return []
    if gravar:
        open(ENCONTROS, "w", encoding="utf-8").write(novo)
    return [f"wild_encounters.json: {sum(conta.values())} linhas de Galar ("
            + ", ".join(f"{t.replace('_mons', '')} {n}"
                        for t, n in sorted(conta.items())) + ")"]


def demo_galar():
    """Autoteste do bloco de Galar, com mutacao plantada.

    Nao entra no `--demo` geral de proposito: aquele comeca pelo
    `plano_congelado`, que compara a tabela gravada com um plano refeito do
    zero, e ele JA estava vermelho antes desta rodada (a importacao de Galar da
    onda 1 deu fonte a especies que a tabela ainda lista como inobteniveis:
    medido em 07/09/2026, 213 selvagens no plano contra 234 na tabela, com esta
    rodada e sem ela). Reconciliar aquela tabela e obra propria, e nao efeito
    colateral desta.
    """
    global SOBRAS_DE_ESCOPO_GALAR
    falhas = []
    p = plano_galar()
    mapa_regiao = censo_dex.mapas()
    pasta_de = {m: v[0] for m, v in mapa_regiao.items()}

    # 1. todo mapa de destino existe, e e de Galar.
    existem = mapas_existentes()
    for l in p["galar_estaticos"] + p["galar_presentes"]:
        if l["mapa"] not in existem:
            falhas.append("mapa que nao existe: " + l["mapa"])
        if regiao_do_mapa(l["mapa"]) != "Galar":
            falhas.append("estatico fora de Galar: " + l["mapa"])
    for l in p["galar_selvagens"]:
        if mapa_regiao.get(l["mapa"], (None, "?"))[1] != "Galar":
            falhas.append("mato fora de Galar: " + l["mapa"])

    # 2. tile e flag: um por objeto, e dentro da faixa deste lote.
    tiles = collections.Counter((l["mapa"], tuple(l["tile"]))
                                for l in p["galar_estaticos"])
    for chave, n in tiles.items():
        if n > 1:
            falhas.append("dois estaticos no mesmo tile: %s" % (chave,))
    ends = [int(l["endereco_da_flag"], 16) for l in p["galar_estaticos"]]
    if len(set(ends)) != len(ends):
        falhas.append("flag repetida entre os estaticos de Galar")
    if ends and not (FLAG_GALAR_BASE <= min(ends) and max(ends) <= FLAG_GALAR_TETO):
        falhas.append("flag fora da faixa 0x%04X-0x%04X" % (FLAG_GALAR_BASE,
                                                           FLAG_GALAR_TETO))
    nomes = {l["flag"] for l in p["galar_estaticos"]}
    # O bloco que ESTE arquivo gera sai da busca. Sem isso a checagem inverte de
    # sentido assim que `--galar-objetos --aplica` roda pela primeira vez: ela
    # existe para pegar nome pedido por OUTRO dono, e passaria a acusar o
    # proprio escritor. Medido em 07/09/2026, com as 10 flags acusadas.
    texto = LS.substitui(open(FLAGS_H, encoding="utf-8").read(),
                         MARCA_FLAG_GALAR_INI, MARCA_FLAG_GALAR_FIM, "")
    for n in sorted(nomes):
        if re.search(r"#define\s+%s\b" % re.escape(n), texto):
            falhas.append("nome de flag ja existe no flags.h, e o dono nao e "
                          "este arquivo: " + n)

    # 2b. os tres iniciais sao PRESENTE, e nenhum deles ficou no mato.
    ini = [l for l in p["galar_presentes"] if l["especie"] in INICIAIS_GALAR]
    if len(ini) != len(INICIAIS_GALAR):
        falhas.append("inicial de Galar fora do balde de presente: %d de %d"
                      % (len(ini), len(INICIAIS_GALAR)))
    for l in ini:
        if l["metodo"] != "multichoice" or l["mapa"] != MAPA_INICIAL_GALAR:
            falhas.append("inicial de Galar com molde errado: " + l["especie"])
    if len({tuple(l["tile"]) for l in ini}) != 1:
        falhas.append("os tres iniciais de Galar tem que sair do MESMO NPC")
    for l in p["galar_selvagens"]:
        if l["especie"] in INICIAIS_GALAR:
            falhas.append("inicial de Galar no mato: " + l["especie"])

    # 3. o mato so ocupa slot DUPLICADO, e o `substituido` bate com o baseline.
    idx = _indice(encontros_base())
    for l in p["galar_selvagens"]:
        mons = idx[(l["mapa"], l["metodo"])]
        if mons[l["slot"]]["species"] != l["substituido"]:
            falhas.append("substituido nao bate: " + l["especie"])
        antes = [m["species"] for m in mons[:l["slot"]]]
        if l["substituido"] not in antes:
            falhas.append("slot nao era duplicado: " + l["especie"])

    # 4. nenhuma colocacao em mapa de escopo aberto.
    for l in p["galar_selvagens"]:
        if any(x in pasta_de[l["mapa"]] for x in SOBRAS_DE_ESCOPO_GALAR):
            falhas.append("colocacao em sobra de FireRed: " + l["mapa"])

    # 5. MUTACAO PLANTADA: sem o filtro de sobra de escopo, alguma colocacao cai
    # numa delas. Se este bloco NAO reprovar, o filtro nao esta pesando e o item
    # 4 acima passa por acaso.
    guarda = SOBRAS_DE_ESCOPO_GALAR
    # A RESERVA sai junto: `decide_selvagem_galar` respeita a escolha ja gravada
    # (e por isso o mato nao anda de slot a cada rodada), e com ela no lugar
    # nenhuma mutacao pode mover nada. Tirar o filtro sem tirar a reserva era um
    # teste que passava sozinho.
    guarda_res = _TABELA.pop("galar_selvagens", None)
    try:
        SOBRAS_DE_ESCOPO_GALAR = ()
        nomes_mato = [l["especie"] for l in p["galar_selvagens"]]
        mutante = decide_selvagem_galar(nomes_mato, catalogo_completo())
        caiu = [l["mapa"] for l in mutante
                if any(x in pasta_de[l["mapa"]] for x in guarda)]
        if not caiu:
            falhas.append("mutacao plantada NAO reprovou: tirar o filtro de "
                          "sobra de escopo nao muda colocacao nenhuma")
    finally:
        SOBRAS_DE_ESCOPO_GALAR = guarda
        if guarda_res is not None:
            _TABELA["galar_selvagens"] = guarda_res

    print("demo galar: %s (%d colocacoes: %d mato, %d estatico, %d presente)"
          % ("OK" if not falhas else "REPROVADO",
             len(p["galar_selvagens"]) + len(p["galar_estaticos"])
             + len(p["galar_presentes"]), len(p["galar_selvagens"]),
             len(p["galar_estaticos"]), len(p["galar_presentes"])))
    for f in falhas:
        print("  FALHA", f)
    return 1 if falhas else 0


def relata_galar():
    """O que a obra de Galar entregou, em numero, para o diario da onda.

    Le o RESUMO do proprio plano, e nao um censo novo: depois de `--aplica` o
    censo ja enxerga as linhas de mato recem-escritas, e recontar ali faria o
    relatorio encolher a cada rodada como se metade da obra nao existisse.
    """
    t = plano_galar()
    r = t["_resumo"]
    fora = [f"gen 8 com fonte DIRETA em Galar: "
            f"{r['gen8_com_fonte_em_galar_antes']} antes, "
            f"{r['gen8_com_fonte_em_galar_antes'] + r['gen8_colocadas']} depois "
            f"({r['gen8_colocadas']} colocacoes de gen 8, "
            f"{r['colocacoes'] - r['gen8_colocadas']} de outra geracao que "
            f"destrava forma de gen 8)",
            f"gen 8 sem fonte em Galar: {r['gen8_sem_fonte_em_galar']} tinham "
            f"fonte direta so em outra regiao; "
            f"{r['de_graca_por_evolucao_ou_forma']} delas saem de graca por "
            f"evolucao ou troca de forma depois das colocacoes"]
    for k in BUCKETS_GALAR:
        fora.append(f"  {k}: {len(t[k])}")
    return fora


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
    # A remocao fisica dos mapas cortados (`remove_mapas_cortados.py`,
    # 22/08/2026) tira a tabela de mato do cortado POR CHAVE. Sumir e legitimo
    # SO para mapa cortado, e nascer nunca e legitimo; as duas coisas separadas,
    # porque "o conjunto mudou" sozinho aceitaria perda silenciosa de mapa vivo.
    fora_do_escopo = {c for c, (pasta, _r) in censo_dex.mapas().items()
                      if pasta in mapas_cortados()}
    # TABELA VAZIA NAO E CONTEUDO. A rodada 12 tirou `water_mons` e
    # `fishing_mons` da Diglett's Cave de Johto, e as duas eram placeholder:
    # `encounter_rate` 0 e SPECIES_NONE em todos os slots. Sumir com elas nao
    # perde um encontro, e este guarda existe para perda de ENCONTRO. Sem a
    # poda, limpar placeholder ficava proibido para sempre.
    def vazia(mons):
        return all(m["species"] == "SPECIES_NONE" for m in mons)
    sumiram = {k for k in set(a) - set(b)
               if k[1] not in fora_do_escopo and not vazia(a[k])}
    assert not sumiram, ("T129.13: tabela de mapa VIVO sumiu: "
                         f"{sorted(sumiram)[:4]}")
    assert not set(b) - set(a), ("T129.13: tabela de encontro apareceu: "
                                 f"{sorted(set(b) - set(a))[:4]}")
    cortadas = len(set(a) - set(b))
    a = {k: v for k, v in a.items() if k in b}
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
            f"niveis alterados; {cortadas} tabelas de mapa CORTADO fora, e "
            "quem morava so nelas e cobrado pelo censo, nao aqui")


def plano_congelado():
    """A tabela gravada, DEPOIS de conferida contra um plano feito do zero.

    O plano do zero manda no CONJUNTO de linhas: quem entra em cada balde. Se
    ele discordar disso, ou a regua mudou sem que a tabela fosse regerada, ou
    alguem editou a tabela a mao no lugar da regua. Foi assim que o fechador da
    rodada 12 achou os tres selvagens duplicados da Diglett's Cave.

    O que ele NAO manda, e isto e medido e nao suposto: o par especie -> CASA de
    um estatico. Ate 23/08/2026 havia um assert cobrando esse par, e ele estava
    VERMELHO com 8 casas trocadas em 106; a causa nao e edicao a mao, e a mesma
    que o proprio `demo` ja tinha escrito duas funcoes abaixo: `decide_estaticos`
    escolhe casa por COTA de regiao e por LOTACAO do mapa, e as duas leem a
    arvore. Depois de `--estaticos --aplica` a arvore ja tem os 106 objetos, e o
    plano refeito distribui as mesmas casas entre as mesmas especies numa ordem
    diferente. Cobrar o par era cobrar que uma funcao dependente de estado
    devolvesse o estado anterior, e isso nunca ia ficar verde de novo.
    """
    t = tabela()
    p = plano()
    for k in BUCKETS + EXTRAS:
        assert len(p[k]) == len(t.get(k, [])), (k, len(p[k]), len(t.get(k, [])))
        chave = "item" if k == "chaves" else "especie"
        a = {l[chave] for l in t.get(k, [])}
        b = {l[chave] for l in p[k]}
        assert a == b, (k, sorted(a - b)[:5], sorted(b - a)[:5])
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
    print(sonda_de_formas())

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

    # ---- T129.17: as chaves de troca de forma SAIREM do NPC, e a corrente de
    # dois passos ficar de pe. Sujeito da prova e o scripts.inc no disco.
    inc = open(f"{RAIZ}/data/maps/{MAPA_PRESENTE}/scripts.inc",
               encoding="utf-8").read()
    for l in t["chaves"]:
        if f"\tadditem {l['item']}\n" not in inc:
            falhas.append(f"T129.17: {l['item']} nao e entregue por "
                          f"{MAPA_PRESENTE}; {len(l['destrava'])} entradas de "
                          "Dex dependem dele")
        if f"\tcheckitem {l['item']}\n" not in inc:
            falhas.append(f"T129.17: {l['item']} e entregue sem guarda de "
                          "checkitem; a segunda fala com o NPC duplica o item")
    depois = {x.nome: x for x in censo_dex.censo()}
    ino = [n for n, x in depois.items() if x.categoria == "inobtenivel"]
    if ino:
        falhas.append(f"T129.17: ainda ha {len(ino)} entrada(s) inobtenivel: "
                      f"{sorted(ino)[:6]}")
    # Mutacao plantada: sem o fecho de forma do censo, as 5 correntes de dois
    # passos voltam a ser inobteniveis. Se a mutacao NAO reprovar, esta demo
    # nao esta provando que o 1.571 vem do motor.
    guarda = censo_dex.FORMA_REVERTE
    try:
        censo_dex.FORMA_REVERTE = guarda + censo_dex.FORMA_PERMANENTE
        mut = {x.nome for x in censo_dex.censo() if x.categoria == "inobtenivel"}
    finally:
        censo_dex.FORMA_REVERTE = guarda
    esperado = {l["especie"] for l in t["formas"]}
    if not esperado <= mut:
        falhas.append("T129.17: mutacao plantada NAO reprovou; as "
                      f"{len(esperado)} linhas de `formas` nao dependem do "
                      "fecho de troca de forma do censo")
    # ---- T129.18: quem perdeu o LAR na remocao fisica dos mapas cortados esta
    # de volta, e num mapa VIVO. A `Route229` era a unica casa de Surskit e
    # Masquerain no jogo inteiro e saiu com a Battle Zone em 22/08/2026; o censo
    # acusou os dois e a excecao `REPOE_NA_REGIAO` os devolveu a Sinnoh. A
    # armadilha que este bloco caca e a que o replanejamento de fato criou: o
    # `plano()` chegou a mandar uma linha para uma tabela que NAO EXISTE MAIS
    # (o Burmy-Planta ficou apontando para `MAP_ROUTE229/land_mons` e o
    # `--selvagem` parava com SystemExit). Cobrado para TODA a tabela, e nao so
    # para o Surskit.
    vivos = {(l["mapa"], l["metodo"]) for l in t["selvagens"]}
    idx = _indice(json.load(open(ENCONTROS, encoding="utf-8")))
    mortas = sorted(vivos - set(idx))
    if mortas:
        falhas.append(f"T129.18: {len(mortas)} linha(s) de mato apontam para "
                      f"tabela que nao existe mais: {mortas[:4]}")
    for n in REPOE_NA_REGIAO:
        linha = next((l for l in t["selvagens"] if l["especie"] == n), None)
        if linha is None:
            falhas.append(f"T129.18: {n} perdeu o lar no corte e nao tem linha")
        elif linha["regiao"] != REPOE_NA_REGIAO[n]:
            falhas.append(f"T129.18: {n} voltou para {linha['regiao']} e nao "
                          f"para {REPOE_NA_REGIAO[n]}, de onde o corte o tirou")
        elif linha["metodo"] not in AGUA:
            falhas.append(f"T129.18: {n} e de agua e foi para {linha['metodo']}")
        elif depois[n].categoria == "inobtenivel":
            falhas.append(f"T129.18: {n} tem linha e continua inobtenivel")
    # A lista aceita ESTATICO desde 23/08/2026, e a razao e medida: o Masquerain
    # ganhou um encontro estatico proprio na Galar_WildArea08 (bloco c5,
    # 22/08/2026, `data/scripts/galar_estaticos.inc`), que e um caminho de
    # obtencao tao bom quanto a evolucao. A pergunta deste bloco sempre foi "o
    # Masquerain ficou sem caminho depois que a Route229 caiu?", e "estatico" e
    # uma resposta SIM; recusa-lo era cobrar o caminho em vez do resultado.
    if "SPECIES_MASQUERAIN" in depois and \
            depois["SPECIES_MASQUERAIN"].categoria == "inobtenivel":
        falhas.append("T129.18: o Masquerain ficou sem caminho nenhum; ele e "
                      "Bug/Flying e a regra 6 proibe agua para quem nao e "
                      "TYPE_WATER, entao so evolucao ou estatico o devolvem")
    if not falhas:
        print(f"T129.18 OK: nenhuma das {len(t['selvagens'])} linhas de mato "
              f"aponta para tabela morta, e {'/'.join(sorted(REPOE_NA_REGIAO))} "
              "voltou para a agua da regiao de onde o corte o tirou")
    if not falhas:
        print(f"T129.17 OK: {len(t['chaves'])} itens-chave entregues com guarda "
              f"de checkitem, {len(depois)} entradas de Dex e ZERO inobtenivel; "
              f"as {len(esperado)} correntes de {'/'.join(sorted({str(l['passos']) for l in t['formas']}))} "
              "passos caem com a mutacao plantada")

    print("tabela: " + ", ".join(f"{k} {len(t[k])}" for k in BUCKETS + EXTRAS))
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


# ------------------------------ Galar: os objetos e as cenas (onda 2, lote H)
#
# ONDE ESTE PEDACO ESCREVE, e por que ele nao usa a MARCA das cinco regioes.
# `limpa_mapas_orfaos` varre `data/maps/*/map.json` inteiro e apaga todo objeto
# com `origem == MARCA` que nao esteja na tabela das CINCO. Marcar o estatico de
# Galar com a mesma string faria a proxima chamada de `--estaticos --aplica`
# apagar Galar inteiro em silencio, porque a tabela dos cinco nao cita mapa
# nenhum de Galar. Por isso a marca daqui e outra, e o filtro daquela varredura
# (`!= MARCA`) preserva estes objetos sozinho.
#
# ORDEM QUE IMPORTA: rodar DEPOIS de `estaticos_galar.py --aplicar`. Aquele
# gerador tira os objetos dele de todos os `map.json` de Galar e os repoe no
# FIM da lista; rodar este antes deixaria os objetos da Dex no meio, e a cada
# passada de `estaticos_galar` eles andariam de indice.
MARCA_GALAR = "distribui_dex galar"
MARCA_FLAG_GALAR_INI = ("// >>> Dex de Galar: HIDE dos estaticos e presentes "
                        "(dev_scripts/distribui_dex.py --galar-objetos) >>>")
MARCA_FLAG_GALAR_FIM = "// <<< Dex de Galar <<<"


def _trecho_estatico_galar(l):
    """O mesmo `_trecho_estatico` das cinco regioes, com o prefixo `Galar` nos
    nomes. O prefixo NAO e enfeite: `FLAG_HIDE_DEX_ZACIAN_HERO` e
    `LOCALID_DEX_ZACIAN_HERO` ja existem, do Zacian que a onda A pos em Kanto, e
    dois simbolos com o mesmo nome fariam um apagar o outro sem aviso."""
    m = l["mapa"]
    nome = "Galar" + l["especie"].replace("SPECIES_", "").title().replace("_", "")
    lid = "LOCALID_DEX_GALAR_" + l["especie"].replace("SPECIES_", "")
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


def _script_iniciais_galar():
    """O NPC que entrega UM dos tres iniciais de Galar, a escolha.

    Molde do `_script_presentes` do laboratorio do Birch, linha por linha, com
    a mesma armadilha ja paga la: NADA de `waitstate` depois do
    `dynmultistack`, porque `ScrCmd_dynmultichoice` ja para o contexto sozinho
    e o segundo o travaria para sempre.

    O texto sai em INGLES de proposito. A T07 do `checa_texto.py` reprova
    PORTUGUES em Galar desde a onda 1 (decisao 3 daquela onda), e frase nova em
    portugues aqui entregaria vermelho por acertar.
    """
    m = MAPA_INICIAL_GALAR
    ini = [l for l in tabela_gravada().get("galar_presentes", [])
           if l["metodo"] == "multichoice"]
    p = ["@ Gerado por dev_scripts/distribui_dex.py --galar-objetos. Nao editar a mao.",
         "",
         "@ Wedgehurst NAO tem laboratorio nesta arvore (medido em 07/09/2026:",
         "@ nenhum dos 17 mapas Galar_Wedgehurst* tem NPC de cientista). O predio",
         "@ e o CENTRO POKEMON, reconhecido por MUS_RG_POKE_CENTER e pela",
         "@ enfermeira do balcao. Os tres iniciais sairam do MATO por decisao da",
         "@ condutora da onda 2: eles caiam em slot duplicado de tabela selvagem,",
         "@ e um deles em mapa submerso.",
         f"{m}_EventScript_DexIniciaisGalar::",
         "\tlock",
         "\tfaceplayer",
         f"\tgoto_if_set {FLAG_INICIAL_GALAR}, {m}_EventScript_DexIniciaisGalarJaDeu",
         f"\tmsgbox {m}_Text_DexIniciaisGalarPergunta, MSGBOX_DEFAULT"]
    for i, l in enumerate(ini):
        nome = l["especie"].replace("SPECIES_", "").title()
        p.append(f"\tdynmultipush {m}_Text_DexInicialGalar{nome}, {i}")
    p += ["\tdynmultistack 0, 0, FALSE, 4, FALSE, 0, DYN_MULTICHOICE_CB_NONE",
          "\tcompare VAR_RESULT, MULTI_B_PRESSED",
          f"\tgoto_if_eq {m}_EventScript_DexIniciaisGalarSai"]
    for i, l in enumerate(ini):
        nome = l["especie"].replace("SPECIES_", "").title()
        p.append(f"\tgoto_if_eq VAR_RESULT, {i}, "
                 f"{m}_EventScript_DexInicialGalar{nome}")
    p += [f"\tgoto {m}_EventScript_DexIniciaisGalarSai", ""]
    for l in ini:
        nome = l["especie"].replace("SPECIES_", "").title()
        p += [f"{m}_EventScript_DexInicialGalar{nome}::",
              f"\tgivemon {l['especie']}, {l['nivel']}",
              f"\tsetflag {FLAG_INICIAL_GALAR}",
              f"\tmsgbox {m}_Text_DexIniciaisGalarEntregue, MSGBOX_DEFAULT",
              "\trelease",
              "\tend",
              ""]
    p += [f"{m}_EventScript_DexIniciaisGalarJaDeu::",
          f"\tmsgbox {m}_Text_DexIniciaisGalarJaDeu, MSGBOX_DEFAULT",
          "\trelease",
          "\tend",
          "",
          f"{m}_EventScript_DexIniciaisGalarSai::",
          "\trelease",
          "\tend",
          "",
          f"{m}_Text_DexIniciaisGalarPergunta:",
          '\t.string "The LEAGUE sends us three POKéMON\\n"',
          '\t.string "for new TRAINERS every year.\\p"',
          '\t.string "Nobody came for these. Pick one!$"',
          ""]
    for l in ini:
        nome = l["especie"].replace("SPECIES_", "").title()
        p += [f"{m}_Text_DexInicialGalar{nome}:",
              '\t.string "%s$"' % nome.upper(), ""]
    p += [f"{m}_Text_DexIniciaisGalarEntregue:",
          '\t.string "Take good care of it!$"', "",
          f"{m}_Text_DexIniciaisGalarJaDeu:",
          '\t.string "I hope the one you chose is\\ndoing well.$"', ""]
    return p


def _script_evento_galar():
    """O NPC dos event-only de Galar: `givemon` sem escolha, mesma regra do
    `DexDistribuicao` do Birch. Sao as entradas SEM gfx de overworld, que por
    isso nao podem virar encontro estatico."""
    m = MAPAS_PRESENTE_GALAR[0]
    ev = [l for l in tabela_gravada().get("galar_presentes", [])
          if l["metodo"] == "givemon"]
    p = [f"{m}_EventScript_DexDistribuicaoGalar::",
         "\tlock",
         "\tfaceplayer",
         f"\tgoto_if_set {FLAG_EVENTO_GALAR}, "
         f"{m}_EventScript_DexDistribuicaoGalarJaDeu",
         f"\tmsgbox {m}_Text_DexDistribuicaoGalar, MSGBOX_DEFAULT"]
    for l in ev:
        p.append(f"\tgivemon {l['especie']}, {l['nivel']}")
    p += [f"\tsetflag {FLAG_EVENTO_GALAR}",
          f"\tmsgbox {m}_Text_DexDistribuicaoGalarFim, MSGBOX_DEFAULT",
          "\trelease",
          "\tend",
          "",
          f"{m}_EventScript_DexDistribuicaoGalarJaDeu::",
          f"\tmsgbox {m}_Text_DexDistribuicaoGalarFim, MSGBOX_DEFAULT",
          "\trelease",
          "\tend",
          "",
          f"{m}_Text_DexDistribuicaoGalar:",
          '\t.string "I keep the POKéMON from every\\n"',
          '\t.string "event that never came to GALAR.\\p"',
          '\t.string "You should have them.$"', "",
          f"{m}_Text_DexDistribuicaoGalarFim:",
          '\t.string "Whatever does not fit in your\\n"',
          '\t.string "party goes to your PC.$"', ""]
    return p


def bloco_flags_galar():
    """Os apelidos de flag desta obra, todos dentro da faixa 0x2280-0x22FF que o
    lote H reservou. Apelidar FLAG_UNUSED nao mexe em FLAGS_COUNT: a save nao
    muda."""
    est = tabela_gravada().get("galar_estaticos", [])
    larg = 38
    out = [MARCA_FLAG_GALAR_INI,
           "// Uma flag de HIDE por estatico da Dex de Galar, mais as duas dos",
           "// NPCs de presente. O nome leva GALAR porque os apelidos sem ele ja",
           "// existem, dos mesmos lendarios que a Dex das cinco regioes colocou",
           "// em Kanto, Johto e Hoenn. Gerado; nao editar a mao."]
    usados = 0
    for l in est:
        out.append("#define %-*s FLAG_UNUSED_%s  // Galar, %s"
                   % (larg, l["flag"], l["endereco_da_flag"].replace("0x", "0x"),
                      l["mapa"]))
        usados = max(usados, int(l["endereco_da_flag"], 16))
    for nome, comentario in ((FLAG_INICIAL_GALAR,
                              "o inicial de Galar ja foi escolhido"),
                             (FLAG_EVENTO_GALAR,
                              "os event-only de Galar ja foram dados")):
        usados += 1
        if usados > FLAG_GALAR_TETO:
            raise SystemExit("a faixa 0x%04X-0x%04X acabou" % (FLAG_GALAR_BASE,
                                                               FLAG_GALAR_TETO))
        out.append("#define %-*s FLAG_UNUSED_0x%04X  // %s"
                   % (larg, nome, usados, comentario))
    out.append(MARCA_FLAG_GALAR_FIM)
    return "\n".join(out) + "\n"


def _objeto_galar(local, gfx, script, flag, tile, elevacao=3):
    return {
        "local_id": local, "graphics_id": gfx,
        "x": tile[0], "y": tile[1], "elevation": elevacao,
        "movement_type": "MOVEMENT_TYPE_FACE_DOWN",
        "movement_range_x": 0, "movement_range_y": 0,
        "trainer_type": "TRAINER_TYPE_NONE",
        "trainer_sight_or_berry_tree_id": "0",
        "script": script, "flag": flag, "origem": MARCA_GALAR,
    }


def _escreve_inc(cam, corpo, gravar):
    inc = open(cam, encoding="utf-8").read()
    novo = LS.substitui(inc, INC_INI, INC_FIM,
                        "\n".join([INC_INI] + corpo + [INC_FIM]) + "\n")
    if novo == inc:
        return False
    if gravar:
        open(cam, "w", encoding="utf-8").write(novo)
    return True


def aplica_galar_objetos(gravar):
    """Os 10 estaticos e os dois NPCs de presente de Galar, em map.json e .inc."""
    t = tabela_gravada()
    est = t.get("galar_estaticos", [])
    pres = t.get("galar_presentes", [])
    npcs = t.get("galar_npcs_presente", [])
    mudou = []

    # --- objetos, um map.json por vez -------------------------------------
    por_mapa = collections.defaultdict(list)
    for l in est:
        nome = "Galar" + l["especie"].replace("SPECIES_", "").title().replace("_", "")
        por_mapa[l["mapa"]].append(_objeto_galar(
            "LOCALID_DEX_GALAR_" + l["especie"].replace("SPECIES_", ""),
            "OBJ_EVENT_GFX_SPECIES(%s)" % l["especie"].replace("SPECIES_", ""),
            f"{l['mapa']}_EventScript_Dex{nome}", l["flag"],
            (l["tile"][0], l["tile"][1]), elevacao=0))
    if any(l["metodo"] == "multichoice" for l in pres):
        por_mapa[MAPA_INICIAL_GALAR].append(_objeto_galar(
            "LOCALID_GALAR_DEX_INICIAIS", "OBJ_EVENT_GFX_SCIENTIST_2",
            f"{MAPA_INICIAL_GALAR}_EventScript_DexIniciaisGalar", "0",
            TILE_INICIAL_GALAR))
    if any(l["metodo"] == "givemon" for l in pres):
        m = MAPAS_PRESENTE_GALAR[0]
        tile = tuple(npcs[0]["tile"]) if npcs else None
        if tile is None:
            raise SystemExit("galar_npcs_presente vazio: rode --galar --aplica antes")
        por_mapa[m].append(_objeto_galar(
            "LOCALID_GALAR_DEX_EVENTO", "OBJ_EVENT_GFX_MANIAC",
            f"{m}_EventScript_DexDistribuicaoGalar", "0", tile))

    for mapa, itens in sorted(por_mapa.items()):
        cam = f"{RAIZ}/data/maps/{mapa}/map.json"
        d = json.load(open(cam, encoding="utf-8"))
        antes = d.get("object_events", [])
        # OS OBJETOS DESTE ESCRITOR ENTRAM ANTES DO BLOCO DE `estaticos_galar`, e
        # nao no fim da lista. Motivo medido em 07/09/2026: aquele gerador tira
        # os objetos DELE de todo map.json de Galar e os repoe no FIM, entao com
        # os da Dex depois deles a segunda passada de `estaticos_galar --aplicar`
        # mexeria em 3 mapas sem nada ter mudado, e o `--demo` dele reprova por
        # nao ser idempotente. Cada objeto novo continua entrando DEPOIS de todo
        # objeto que ja existia e nao e de gerador, que e o que a save cobra.
        limpo = [o for o in antes if o.get("origem") != MARCA_GALAR]
        corte = next((i for i, o in enumerate(limpo)
                      if o.get("origem") == "estaticos_galar"), len(limpo))
        novos = limpo[:corte] + itens + limpo[corte:]
        if len(novos) > TETO_OBJETOS:
            raise SystemExit(f"{mapa} chegaria a {len(novos)} objetos, acima "
                             f"do teto {TETO_OBJETOS}.")
        tiles = collections.Counter((o["x"], o["y"]) for o in novos)
        repetido = [k for k, n in tiles.items() if n > 1]
        if repetido:
            raise SystemExit(f"{mapa}: dois objetos no mesmo tile {repetido}")
        if novos != antes:
            d["object_events"] = novos
            if gravar:
                open(cam, "w", encoding="utf-8").write(
                    json.dumps(d, indent=2, ensure_ascii=False) + "\n")
            mudou.append(f"{mapa}/map.json: {len(itens)} objeto(s) da Dex de Galar")

    # --- cenas -------------------------------------------------------------
    cenas = collections.defaultdict(list)
    for l in est:
        cenas[l["mapa"]].append(_trecho_estatico_galar(l))
    if any(l["metodo"] == "multichoice" for l in pres):
        cenas[MAPA_INICIAL_GALAR] += _script_iniciais_galar()
    if any(l["metodo"] == "givemon" for l in pres):
        cenas[MAPAS_PRESENTE_GALAR[0]] += _script_evento_galar()
    for mapa, corpo in sorted(cenas.items()):
        if _escreve_inc(f"{RAIZ}/data/maps/{mapa}/scripts.inc", corpo, gravar):
            mudou.append(f"{mapa}/scripts.inc: cena da Dex de Galar")

    # --- flags -------------------------------------------------------------
    atual = open(FLAGS_H, encoding="utf-8").read()
    novo = LS.substitui(atual, MARCA_FLAG_GALAR_INI, MARCA_FLAG_GALAR_FIM,
                        bloco_flags_galar())
    if novo != atual:
        if gravar:
            open(FLAGS_H, "w", encoding="utf-8").write(novo)
        mudou.append(f"flags.h: {len(est) + 2} apelidos da Dex de Galar")
    return mudou


def demo_galar_objetos():
    """Autoteste do escritor: nomes unicos, faixa de flag e tile livre."""
    falhas = []
    t = tabela_gravada()
    est = t.get("galar_estaticos", [])
    pres = t.get("galar_presentes", [])
    # 1. nenhum simbolo desta obra colide com os das cinco regioes.
    texto = open(FLAGS_H, encoding="utf-8").read()
    corpo = LS.substitui(texto, MARCA_FLAG_GALAR_INI, MARCA_FLAG_GALAR_FIM, "")
    for l in est:
        if re.search(r"#define\s+%s\b" % re.escape(l["flag"]), corpo):
            falhas.append("flag ja existe fora do bloco de Galar: " + l["flag"])
    # 2. faixa.
    ends = [int(l["endereco_da_flag"], 16) for l in est]
    if ends and not (FLAG_GALAR_BASE <= min(ends) and max(ends) + 2 <= FLAG_GALAR_TETO):
        falhas.append("faixa de flag estourada")
    # 3. o NPC de inicial nao pode nascer em cima de outro objeto.
    d = json.load(open(f"{RAIZ}/data/maps/{MAPA_INICIAL_GALAR}/map.json",
                       encoding="utf-8"))
    outros = {(o["x"], o["y"]) for o in d.get("object_events", [])
              if o.get("origem") != MARCA_GALAR}
    if TILE_INICIAL_GALAR in outros:
        falhas.append("o tile do NPC de inicial ja tem objeto")
    # 4. MUTACAO PLANTADA: sem o prefixo Galar, o nome de flag do Zacian bate com
    # o que a Dex das cinco ja escreveu. Se este bloco NAO acusar, o prefixo
    # deixou de proteger.
    sem_prefixo = [l["flag"].replace("FLAG_HIDE_DEX_GALAR_", "FLAG_HIDE_DEX_")
                   for l in est]
    if not any(re.search(r"#define\s+%s\b" % re.escape(n), corpo)
               for n in sem_prefixo):
        falhas.append("mutacao plantada NAO reprovou: tirar o prefixo GALAR do "
                      "nome de flag nao colide com nada")
    print("demo galar-objetos: %s (%d estatico, %d presente)"
          % ("OK" if not falhas else "REPROVADO", len(est), len(pres)))
    for f in falhas:
        print("  FALHA", f)
    return 1 if falhas else 0


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
    ap.add_argument("--galar", action="store_true",
                    help="Dex de geracao 8 em Galar: mato no wild_encounters e "
                         "pedidos de estatico/presente para o fechador")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--galar-objetos", action="store_true", dest="galar_objetos",
                    help="os 10 estaticos e os 2 NPCs de presente de Galar, em "
                         "map.json, scripts.inc e flags.h")
    ap.add_argument("--demo-galar", action="store_true", dest="demo_galar")
    ap.add_argument("--demo-galar-objetos", action="store_true",
                    dest="demo_galar_objetos")
    a = ap.parse_args()
    if a.demo_galar_objetos:
        raise SystemExit(demo_galar_objetos())
    if a.demo_galar:
        raise SystemExit(demo_galar())
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
    if a.galar:
        saida += escreve_tabela_galar(a.aplica and not a.dry)
        saida += aplica_selvagem_galar(a.aplica and not a.dry)
        saida += escreve_pedidos_galar(a.aplica and not a.dry)
        saida += relata_galar()
    if a.galar_objetos:
        saida += aplica_galar_objetos(a.aplica and not a.dry)
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


SONDA_FORMA = """
#include "global.h"
#include "constants/items.h"
#include "constants/species.h"
#include "constants/abilities.h"
#include "constants/form_change_types.h"

// T137.3: o que sustenta as CINCO ultimas entradas da Dex nao e um mapa, e a
// mecanica de troca de forma. Ela mora em `src/data/pokemon/form_change_tables.h`,
// que e `static const struct FormChange[]` e por isso nao cabe em
// `_Static_assert` (membro de struct nao e expressao constante). O que cabe, e
// e o que quebraria calado, sao os interruptores: se `P_FAMILY_DEOXYS` ou
// `P_FAMILY_ZYGARDE` cair, as tabelas somem do binario inteiras; se
// `P_GEN_9_MEGA_EVOLUTIONS` cair, o Zygarde-Mega perde a unica origem; e se
// algum dos tres itens virar ITEM_NONE, o `FORM_CHANGE_ITEM_USE` nunca dispara.
// O conteudo das tabelas fica com o T129.17, que le o header e derruba a
// afirmacao com mutacao plantada.
_Static_assert(P_FAMILY_DEOXYS, "sem_familia_deoxys");
_Static_assert(P_FAMILY_ZYGARDE, "sem_familia_zygarde");
_Static_assert(P_GEN_9_MEGA_EVOLUTIONS, "sem_mega_de_gen9_o_zygarde_mega_morre");
_Static_assert(ITEM_METEORITE != ITEM_NONE, "meteorito_sumiu");
_Static_assert(ITEM_ZYGARDE_CUBE != ITEM_NONE, "cubo_sumiu");
_Static_assert(ITEM_ZYGARDITE != ITEM_NONE, "zygardita_sumiu");
_Static_assert(ABILITY_POWER_CONSTRUCT != ABILITY_NONE, "power_construct_sumiu");
_Static_assert(SPECIES_DEOXYS_DEFENSE != SPECIES_NONE, "deoxys_defesa_sumiu");
_Static_assert(SPECIES_DEOXYS_SPEED != SPECIES_NONE, "deoxys_velocidade_sumiu");
_Static_assert(SPECIES_ZYGARDE_10_POWER_CONSTRUCT != SPECIES_NONE, "zygarde10pc_sumiu");
_Static_assert(SPECIES_ZYGARDE_COMPLETE != SPECIES_NONE, "zygarde_completo_sumiu");
_Static_assert(SPECIES_ZYGARDE_MEGA != SPECIES_NONE, "zygarde_mega_sumiu");
// A troca por USO de item e a por HP em batalha sao tipos DIFERENTES: e a
// diferenca entre "forma permanente" e "forma de batalha" no censo.
_Static_assert(FORM_CHANGE_ITEM_USE != FORM_CHANGE_BATTLE_HP_PERCENT_TURN_END,
               "uso_de_item_virou_a_mesma_coisa_que_hp_de_batalha");
%s
"""


def sonda_de_formas():
    """T137.3: os interruptores das cinco ultimas entradas, provados pelo gcc.

    Mutacao plantada junto, pelo mesmo motivo do `sonda_de_regiao`: uma sonda
    que nao compila por outro motivo passaria como verde.
    """
    ok = _compila_sonda(SONDA_FORMA % "")
    if ok is None:
        return ("T137.3 PULADO: arm-none-eabi-gcc nao encontrado (exporte "
                "DEVKITARM). NAO conte como passou.")
    if not ok:
        raise SystemExit("T137.3 REPROVADO: os interruptores de troca de forma "
                         "nao estao todos de pe; as cinco ultimas entradas da "
                         "Dex sairiam do binario sem uma linha de erro.")
    mutante = _compila_sonda(SONDA_FORMA % (
        '_Static_assert(ITEM_ZYGARDE_CUBE == ITEM_NONE, "mutacao");'))
    if mutante:
        raise SystemExit("T137.3 REPROVADO: a mutacao plantada COMPILOU, entao "
                         "a sonda nao esta provando nada.")
    return ("T137.3 OK: P_FAMILY_DEOXYS, P_FAMILY_ZYGARDE e "
            "P_GEN_9_MEGA_EVOLUTIONS de pe, Meteorito/Cubo/Zygardita e "
            "ABILITY_POWER_CONSTRUCT vivos, as cinco especies existem e "
            "FORM_CHANGE_ITEM_USE != FORM_CHANGE_BATTLE_HP_PERCENT_TURN_END; "
            "mutacao plantada reprovada")


def casos_t137():
    """Os dois casos de emulador da rodada das formas.

    O que este par prova e o BLOCO DE CHAVES novo no NPC de distribuicao: nove
    `checkitem` seguidos de `call_if_eq`, cada um chamando um rotulo que faz
    `additem` e `return`. `call` mal fechado nao da erro de compilacao, trava o
    contexto de script; foi a licao do `chapter_jump.inc` em 17/08/2026. Se
    qualquer um dos nove estiver torto, a fala nao chega aos `givemon` e o time
    nao enche.

    O que ele NAO prova, e fica dito: a BOLSA. O `gba_runner` le SaveBlock1 por
    offsets fixos (location, layout, party, flags, vars) e nao tem leitor de
    `bagPocket_KeyItems`; por-lo la significa mexer no runner e no
    `offsets_da_fonte`, que sao de TODO mundo e estao em uso por outros
    executores nesta mesma arvore. A posse do item fica provada em duas outras
    camadas: T129.17 le o `scripts.inc` gravado e exige `checkitem` + `additem`
    para os nove, e T137.3 prova no compilador que os itens e os interruptores
    de forma existem.
    """
    b = next(x for x in tabela()["npcs_presente"] if x["papel"] != "iniciais")
    mapa = "MAP_LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB"
    evento = [l for l in tabela()["presentes"] if l["metodo"] == "givemon"]
    chaves = tabela()["chaves"]
    num = numeros_de_especie()
    base = casos_t129()
    rota = next(c["roteiro"] for c in base if c["id"] == "T129.4")
    fala = next(c["roteiro"] for c in base if c["id"] == "T129.5")[len(rota):]
    return [
        dict(id="T137.1",
             nome=(
                 f"O NPC de distribuicao aguenta a SEGUNDA fala com os {len(chaves)} "
                 "`checkitem` novos no comeco do script. A rota e a do T129.5 e a "
                 "fala inteira roda DUAS vezes. Na primeira o NPC entrega os "
                 f"{len(evento)} event-only e faz `additem` dos {len(chaves)} "
                 "itens-chave que o jogo nao entrega (Gracidea, os quatro "
                 "nectares, Prison Bottle, Reveal Glass, Rotom Catalog, Zygarde "
                 "Cube e o Aurora Ticket, que abre a balsa da Birth Island); na "
                 f"segunda os {len(chaves)} `checkitem` devolvem TRUE, nenhum `call_if_eq` "
                 "dispara, e o `goto_if_set FLAG_DEX_PRESENTE_EVENTO` desvia "
                 "antes dos `givemon`. A prova e que o time continua em 6 e o "
                 f"primeiro continua sendo o "
                 f"{evento[0]['especie'].replace('SPECIES_', '')}: se algum dos "
                 f"{len(chaves)} `call` nao voltasse, o contexto de script travaria e o "
                 "time pararia em 0; se a guarda de flag tivesse quebrado, os "
                 f"{len(evento)} `givemon` rodariam de novo. Par negativo: T137.2."),
             flags=["FLAG_SEM_ENCONTRO_SELVAGEM"],
             warp=mapa, warp_id=b["warp"], time_jogador=True,
             roteiro=rota + fala + fala,
             prova=dict(mapa=mapa, time=6,
                        campos={"especie0": num[evento[0]["especie"]]})),
        dict(id="T137.2",
             nome=(
                 "PAR NEGATIVO DO T137.1: a MESMA rota, SEM apertar A nenhuma "
                 "vez. O time continua vazio e o jogador para "
                 f"em {tuple(b['para'])}, encostado no NPC. Sem ele o T137.1 passaria "
                 "num jogo em que o time ja viesse cheio de fabrica, e tambem "
                 "num jogo em que o NPC esta la e nao responde."),
             flags=["FLAG_SEM_ENCONTRO_SELVAGEM"],
             warp=mapa, warp_id=b["warp"], time_jogador=True,
             roteiro=rota,
             prova=dict(mapa=mapa, time=0, pos=list(b["para"]))),
    ]


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
    fora = []
    if antigo != casos:
        if gravar:
            open(CASOS, "w", encoding="utf-8").write(
                json.dumps(casos, indent=2, ensure_ascii=False) + "\n")
        fora.append(f"testes_criticos/129_dex_completa.json: {len(casos)} casos "
                    f"({len(gerados)} gerados, {len(casos) - len(gerados)} a mao)")
    t137 = casos_t137()
    novo = json.dumps(t137, indent=2, ensure_ascii=False) + "\n"
    velho = open(CASOS_FORMA, encoding="utf-8").read() if os.path.exists(
        CASOS_FORMA) else ""
    if novo != velho:
        if gravar:
            open(CASOS_FORMA, "w", encoding="utf-8").write(novo)
        fora.append(f"testes_criticos/137_dex_formas.json: {len(t137)} casos")
    return fora

if __name__ == "__main__":
    main()
