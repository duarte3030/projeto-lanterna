#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Porta DESENHADA que não leva a lugar nenhum, e warp que caiu fora da porta.

Uso:
    python3 dev_scripts/qa/lente_portas.py            # tabela por região e classe
    python3 dev_scripts/qa/lente_portas.py --lista    # cada achado, uma linha
    python3 dev_scripts/qa/lente_portas.py --região Johto
    python3 dev_scripts/qa/lente_portas.py --demo     # autoteste, exit 1 se cair

Por que existe
--------------
Pergunta do Gui em 06/09/2026: "reveja se da para entrar em TODAS as casas da
ROM". O `valida_warp_tile.py` responde METADE dela: ele parte do warp é pergunta
se o tile embaixo dispara. A outra metade nunca teve regua: partir do TILE e
perguntar se existe warp em cima. Porta desenhada sem warp é a casa que o
jogador anda até a porta é nada acontece, e nenhuma ferramenta da árvore a via.

As três regras, e a medida que separa bug de idioma do motor
------------------------------------------------------------
    P1  porta AO AR LIVRE sem warp    o caso do Gui: casa de rua que não abre
    P2  porta FECHADA sem warp        idioma do motor, ver a calibração abaixo
    P3  warp fora da célula da porta  o warp existe, a porta existe, e eles
                                      estão em células diferentes

A unidade não é a célula, e o BLOCO: células vizinhas com o MESMO comportamento
são uma porta só. Porta de prédio no FRLG tem três tiles de largura e portão de
Johto tem quatro, e só um deles carrega o warp; contar célula fazia a lente
acusar a porta inteira menos o tile do meio. (Mesma armadilha que o
`lente_warps.py` documenta pelo outro lado.)

A CALIBRACAO, medida em 06/09/2026 nas duas fontes intocadas
------------------------------------------------------------
A mesma lente rodada em `fontes-mapas/pokeemerald` e `fontes-mapas/pokefirered`,
que são o vanilla, contando BLOCO de porta sem warp:

    árvore                   ao ar livre        fechado
    pokeemerald (Hoenn)          1 / 202      103 / 310
    pokefirered (Kanto)         11 / 168        4 / 125
    ESTE repo, Hoenn             1 / 202      103 / 310
    ESTE repo, Kanto            11 / 168        4 / 123

Hoenn e Kanto batem com a fonte célula a célula, então NÃO ha o que consertar
nelas: a lente que acusasse ali estaria discordando do vanilla, que é a lição
4.2 do ESTADO. Os 12 casos entram na LISTA BRANCA abaixo, um a um, com o mapa e
a coordenada, e não por regra larga.

**P2 e FALSO POSITIVO CALIBRADO.** 103 blocos em 310 no Hoenn deste repo são os
MESMOS 103 em 310 do pokeemerald intocado: porta de fundo do 2F de Pokecenter,
porta de sala do Battle Frontier que abre por script, corredor da Battle Tent.
Cobrar isso seria mandar consertar o jogo original (lição 4.10). P2 e contado e
mostrado, nunca reprovado.

Porta que o SCRIPT mexe não conta, e isso sai do script
--------------------------------------------------------
Duas famílias de porta legitima não tem warp no `map.json` porque quem as abre e
o roteiro, e as duas são lidas dos `.inc`, nunca chutadas:

  * `setmetatile X, Y, ...` troca o tile em tempo de execução. E como a loja de
    Mahogany esconde a escada do esconderijo da Rocket (`MahoganyTown_Shop`
    warp 1 em (7,4), que o `valida_warp_tile` da por morto e não e).
  * `opendoor X, Y` / `closedoor X, Y` anima uma porta que o roteiro atravessa
    com `applymovement`. E o elevador de loja de departamento inteiro.

Célula citada por um desses comandos NO MESMO MAPA sai das três regras.

O que a lente NÃO cobra, e por que
-----------------------------------
`MB_BRIDGE_OVER_OCEAN` fica de fora da lista de porta. Ele dispara warp no motor
(`MetatileBehavior_IsUnionRoomWarp`, e a saída da Sala de Uniao reusa o
comportamento), mas no mapa ele é PONTE: 608 das 609 células do pokeemerald
intocado tem esse comportamento e nenhum warp, 592 delas só na Route110. Cobra-lo
seria 608 falsos positivos vindos do vanilla.

Mapa TUMULO (`MAPSEC_NONE`, sem warp é sem conexão) fica fora do denominador,
como o ESTADO define: `remove_mapas_cortados.py` esvazia o mapa em vez de
apaga-lo, para não deslocar `mapGroup`/`mapNum` da save.
"""
import argparse
import collections
import json
import os
import re
import struct
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.dirname(AQUI))

import valida_warp_tile as vwt  # noqa: E402  (tabela de atributos e o enum MB_*)

# Tipos que `IsMapTypeOutdoors` (src/overworld.c) chama de ao ar livre.
AO_AR_LIVRE = {"MAP_TYPE_TOWN", "MAP_TYPE_CITY", "MAP_TYPE_ROUTE",
               "MAP_TYPE_OCEAN_ROUTE", "MAP_TYPE_UNDERWATER"}

# PORTA DESENHADA: o que o jogador le como entrada de prédio ou boca de caverna.
# Sai do enum do repo pelo NOME, nunca de número copiado, porque número
# envelhece calado quando alguém insere um MB_ no meio (a mesma armadilha que o
# `valida_warp_tile.py` já pagou).
NOMES_PORTA = ("MB_ANIMATED_DOOR", "MB_NON_ANIMATED_DOOR", "MB_WATER_DOOR",
               "MB_DEEP_SOUTH_WARP")
# ESCADA e ESCADA ROLANTE: entrada também, mas quase sempre interna.
NOMES_ESCADA = ("MB_LADDER", "MB_UP_ESCALATOR", "MB_DOWN_ESCALATOR",
                "MB_UP_RIGHT_STAIR_WARP", "MB_UP_LEFT_STAIR_WARP",
                "MB_DOWN_RIGHT_STAIR_WARP", "MB_DOWN_LEFT_STAIR_WARP")
# SETA de saída. No FRLG a saída de prédio tem três tiles e só o do meio carrega
# a seta, então ela é a família de maior ruido; fica medida a parte.
NOMES_SETA = ("MB_NORTH_ARROW_WARP", "MB_SOUTH_ARROW_WARP", "MB_WEST_ARROW_WARP",
              "MB_EAST_ARROW_WARP", "MB_WATER_SOUTH_ARROW_WARP",
              "MB_STAIRS_OUTSIDE_ABANDONED_SHIP", "MB_SHOAL_CAVE_ENTRANCE")

FAMILIA = {}
for _n in NOMES_PORTA:
    FAMILIA[_n] = "porta"
for _n in NOMES_ESCADA:
    FAMILIA[_n] = "escada"
for _n in NOMES_SETA:
    FAMILIA[_n] = "seta"
# comportamento (número) -> família
DE_FAMILIA = {vwt._MB[n]: f for n, f in FAMILIA.items() if n in vwt._MB}

GRUPO_DE_REGIAO = (("Frlg", "Kanto"), ("Johto", "Johto"),
                   ("Sinnoh", "Sinnoh"), ("Galactic", "Sinnoh"),
                   ("IndoorTwinleaf", "Sinnoh"), ("IndoorSandgem", "Sinnoh"),
                   ("IndoorJubilife", "Sinnoh"), ("IndoorOreburgh", "Sinnoh"),
                   ("IndoorFloaroma", "Sinnoh"))

# Unova e Galar sairam do escopo em 07/09/2026 (PRD-CARTUCHO-1.md): sobraram as
# quatro do cartucho 1, e as duas listas passaram a ser a mesma.
REGIOES = ("Kanto", "Johto", "Hoenn", "Sinnoh")
DO_CARTUCHO_1 = REGIOES

# Placas comuns de porta que não abre. Célula com `bg_event` apontando para uma
# delas sai das três regras: a porta continua fechada, mas o jogo passou a
# EXPLICAR isso ao jogador, que era o defeito de verdade (`data/scripts/
# portas_fechadas.inc`).
SCRIPTS_DE_PLACA = {"Common_EventScript_PortaFechada",
                    "Common_EventScript_BocaFechada",
                    "Common_EventScript_CaisFechado"}

# ---------------------------------------------------------------------------
# LISTA BRANCA: porta sem warp que é DESENHO, não defeito. Uma linha por caso,
# com o porque MEDIDO. Regra para entrar aqui: o caso foi aberto e conferido
# contra a fonte intocada, ou o mecanismo que o abre foi lido no motor. Nunca
# entra "para baixar o número".
# Chave: (pasta do mapa, x, y).
# ---------------------------------------------------------------------------
LISTA_BRANCA = {
    # --- Hoenn: idêntico ao pokeemerald intocado -------------------------
    ("SkyPillar_Outside", 15, 20):
        "Vanilla pokeemerald, célula a célula. A boca do Sky Pillar só abre "
        "depois do terremoto, e quem a abre e o roteiro.",

    # --- Kanto: idêntico ao pokefirered intocado -------------------------
    # Os 11 blocos de porta ao ar livre do FRLG intocado. Conferidos um a um em
    # 06/09/2026 rodando ESTA lente em fontes-mapas/pokefirered: mesmo mapa,
    # mesma coordenada, mesmo comportamento.
    ("SaffronCity_Frlg", 34, 52):
        "Vanilla pokefirered (SaffronCity 34,52). Fachada do Silph sem porta.",
    ("SaffronCity_Connection_Frlg", 30, 5):
        "Vanilla pokefirered. O mapa CONNECTION e o cenário de Saffron visto "
        "das rotas 5, 6, 7 e 8: ele não tem warp nenhum de propósito, porque "
        "quem tem porta é o MAP_SAFFRON_CITY de verdade, 66x55.",
    ("SaffronCity_Connection_Frlg", 36, 5): "Mesmo caso do (30,5).",
    ("SaffronCity_Connection_Frlg", 12, 7): "Mesmo caso do (30,5).",
    ("SaffronCity_Connection_Frlg", 17, 14): "Mesmo caso do (30,5).",
    ("SaffronCity_Connection_Frlg", 30, 14): "Mesmo caso do (30,5).",
    ("SaffronCity_Connection_Frlg", 37, 14): "Mesmo caso do (30,5).",
    ("SaffronCity_Connection_Frlg", 23, 23): "Mesmo caso do (30,5).",
    ("SaffronCity_Connection_Frlg", 14, 31): "Mesmo caso do (30,5).",
    ("SaffronCity_Connection_Frlg", 33, 31): "Mesmo caso do (30,5).",
    ("Route5_Frlg", 24, 38):
        "Vanilla pokefirered (Route5 24,38). Boca sul do Underground Path "
        "desenhada duas vezes; quem entra e o warp 0 em (31,31).",

    # --- Seta de saída ao ar livre, também idêntica a fonte ---------------
    # Medido em 06/09/2026: 5 blocos em Kanto e 1 em Hoenn, os MESMOS do
    # pokefirered e do pokeemerald intocados. São os três tiles de largura da
    # saída de prédio do FRLG, dos quais só o do meio carrega o warp, e a
    # armadilha já está escrita na seção "Warps que disparam de verdade" do
    # ESTADO: quem "consertar" isso está mexendo no vanilla.
    ("SaffronCity_Frlg", 1, 27): "Vanilla pokefirered (SaffronCity 1,27).",
    ("SaffronCity_Frlg", 65, 27): "Vanilla pokefirered (SaffronCity 65,27).",
    ("SaffronCity_Connection_Frlg", 24, 39):
        "Vanilla pokefirered (SaffronCity_Connection 24,39), no mapa que não "
        "tem warp nenhum de propósito.",
    ("Route7_Frlg", 22, 10): "Vanilla pokefirered (Route7 22,10).",
    ("Route8_Frlg", 0, 10): "Vanilla pokefirered (Route8 0,10).",
    ("BattleFrontier_OutsideWest", 26, 64):
        "Vanilla pokeemerald (BattleFrontier_OutsideWest 26,64).",

    # --- Monte Prata, encosta: a boca É a arte, e o warp mora ao lado -------
    # Medido em 07/09/2026 na pergunta 46. As três bocas de `MtSilver_
    # MountainSide` são `MB_NON_ANIMATED_DOOR` sólido, e a célula colada à
    # direita de cada uma é `MB_WEST_ARROW_WARP` com colisão 0 e COM warp:
    # (27,18) tem o warp 0 em (28,18), (34,31) tem o 1 em (35,31) e (41,40) tem
    # o 2 em (42,40), os três para `MT_SILVER_1F_WATERFALL_ROOM`. O jogador pisa
    # na seta, aperta para oeste e `TryArrowWarp` (src/field_control_avatar.c)
    # dispara. A lente só não juntava as duas células no mesmo bloco porque o
    # comportamento delas é diferente, que é o limite conhecido de `blocos()`.
    ("MtSilver_MountainSide", 27, 18):
        "O warp é o 0, em (28,18), MB_WEST_ARROW_WARP: a porta entra.",
    ("MtSilver_MountainSide", 34, 31):
        "O warp é o 1, em (35,31), MB_WEST_ARROW_WARP: a porta entra.",
    ("MtSilver_MountainSide", 41, 40):
        "O warp é o 2, em (42,40), MB_WEST_ARROW_WARP: a porta entra.",

    # --- Kanto, Ikarus' Tileset Patch v3.2 -------------------
    # As 17 portas que o autor desenhou sem destino NÃO moram
    # mais aqui: a onda 3 de Kanto (11/09/2026) pôs em cada uma
    # a placa `closed` do molde de Johto, e a lente as conta na
    # classe "placa", que é medida no `map.json` e não em lista.
    # Ver `dev_scripts/placas_ikarus_kanto.py`.
}

# ---------------------------------------------------------------------------
# SEM INTERIOR: porta que o jogador ve, não abre, e para a qual NÃO EXISTE mapa
# de interior na árvore. Consertar exigiria INVENTAR conteúdo, e isso é decisão
# do Gui, não do agente. Medido em 06/09/2026: Johto não tem UM SO mapa órfão
# (interior que ninguém aponta), então não existe interior cortado esperando ser
# religado. Estes casos são contados na classe "sem interior" e não em "trava".
# Chave: (pasta do mapa, x, y) -> nome do prédio, para o Gui decidir.
# ---------------------------------------------------------------------------
SEM_INTERIOR = {
    ("LakeOfRageLowTide", 15, 4):
        "Lago da Fúria MARÉ BAIXA, casa 1. O mapa inteiro é inalcançável, e "
        "isso é assim NA FONTE: no hns a maré baixa não é mapa vizinho, é "
        "TROCA DE LAYOUT no próprio LakeOfRage (`setmaplayoutindex "
        "LAYOUT_LAKE_OF_RAGE_LOW_TIDE` no ON_TRANSITION dele), e o mapa "
        "LakeOfRageLowTide só existe como casca do layout. O import não trouxe "
        "esse ON_TRANSITION, porque a var de enredo do hns foi cortada. Até "
        "07/09/2026 a Route43 declarava `up` DUAS vezes, para LAKE_OF_RAGE e "
        "para LAKE_OF_RAGE_LOW_TIDE: o motor anda pela PRIMEIRA "
        "(`GetMapConnection` para no primeiro casamento) e DESENHA a última "
        "(`InitBackupMapLayoutConnections` preenche as duas, e a segunda "
        "sobrescreve), então a segunda era conexão morta e enganosa. O "
        "fechador da rodada 13 tirou a duplicata.",
    ("LakeOfRageLowTide", 39, 41): "Lago da Fúria MARÉ BAIXA, casa 2, idem.",

    # --- Portão de rota desenhado dos DOIS lados da emenda ----------------
    # Todo portão de Johto e desenhado inteiro nos dois mapas que ele liga, e
    # cada mapa poe o warp só na porta virada para SI. A porta virada para a
    # emenda fica sem warp, e o prédio dela continua entravel: o warp está a
    # sete tiles, na outra porta do MESMO portão. Medido par a par em
    # 06/09/2026 (EcruteakCity 8,35 com warp contra 1,35 sem; Route38 43,16
    # com warp contra 50,16 sem, e assim por diante).
    ("EcruteakCity", 1, 35):
        "Portão Ecruteak/Route38, porta da emenda; o warp é o 0 em (8,35)",
    ("EcruteakCity", 62, 42):
        "Portão Ecruteak/Route42, porta da emenda; o warp é o 1 em (55,42)",
    ("Route38", 50, 16):
        "Portão Ecruteak/Route38 do lado da rota; o warp é o 0 em (43,16)",
    ("Route42", 1, 10):
        "Portão Ecruteak/Route42 do lado da rota; o warp é o 0 em (8,10)",
    ("Route32", 6, 3):
        "Portão Ruínas de Alph/Route32; o warp é o 0 em (13,3)",
    ("Route36", 9, 20):
        "Portão do Parque Nacional; o warp é o 2 em (16,20)",
    ("RuinsOfAlph_Outside", 45, 27):
        "Portão Ruínas de Alph/Route32 do outro lado; o warp é o 0 em (38,27)",
    ("OlivineCity_PortOutside", 18, 11):
        "Porto de Olivine, porta lateral do prédio; o warp é o 0 em (15,10)",
    ("OlivineCity_PortOutside", 14, 14):
        "Porto de Olivine, porta dos fundos do prédio; mesmo warp 0 em (15,10)",
}


# ---------------------------------------------------------------------------
def carrega_mapas(raiz):
    """pasta -> (json, nome do grupo). Le a ordem do map_groups.json."""
    grupos = json.load(open(os.path.join(raiz, "data/maps/map_groups.json")))
    fora = {}
    for nome_grupo in grupos["group_order"]:
        for nome in grupos.get(nome_grupo, []):
            p = os.path.join(raiz, "data/maps", nome, "map.json")
            if not os.path.exists(p):
                continue
            try:
                fora[nome] = (json.load(open(p, encoding="utf-8")), nome_grupo)
            except json.JSONDecodeError:
                continue
    return fora


def regiao_de(nome, grupo):
    for chave, r in GRUPO_DE_REGIAO:
        if chave in grupo:
            return r
    return "Hoenn"


RE_CELULA_DE_SCRIPT = re.compile(
    r"^\s*(setmetatile|opendoor|closedoor|setdoorclosed|setdooropened)\s+"
    r"(-?\d+)\s*,\s*(-?\d+)", re.M)


RE_MAP_SCRIPT = re.compile(r"^\s*map_script(?:_2)?\s+[^,]+,\s*([A-Za-z_]\w*)", re.M)
RE_ROTULO = re.compile(r"^([A-Za-z_]\w*)::?\s*$", re.M)


def _indice_de_rotulos(raiz):
    """rotulo -> caminho do .inc que o define. Um passe só, em cache."""
    if raiz in _indice_de_rotulos.cache:
        return _indice_de_rotulos.cache[raiz]
    idx, textos = {}, {}
    for base in ("data/maps", "data/scripts"):
        for dp, _dn, fn in os.walk(os.path.join(raiz, base)):
            for f in fn:
                if not f.endswith(".inc"):
                    continue
                cam = os.path.join(dp, f)
                texto = open(cam, encoding="utf-8", errors="replace").read()
                textos[cam] = texto
                for m in RE_ROTULO.finditer(texto):
                    idx.setdefault(m.group(1), cam)
    _indice_de_rotulos.cache[raiz] = (idx, textos)
    return idx, textos


_indice_de_rotulos.cache = {}


def celulas_de_script(raiz, nome, dados=None):
    """Células que o ROTEIRO do mapa mexe: {(x,y)}.

    `setmetatile` troca o tile (a escada escondida da loja de Mahogany) e
    `opendoor`/`closedoor` animam porta que o roteiro atravessa com
    `applymovement` (todo elevador de loja de departamento). Nos dois casos a
    porta é legitima e não tem warp: sem está leitura a lente acusaria mecanismo
    que o motor tem desde o Emerald.

    NÃO basta ler o `.inc` do próprio mapa. O elevador de Goldenrod e o caso
    que prova: os seis andares SO citam `GoldenrodDeptElevator_OnFrame`, e o
    `opendoor 9, 4` mora no `.inc` do mapa do elevador. Então aqui entra o
    arquivo do próprio mapa MAIS o arquivo de cada rotulo que ele cita, achado
    num índice de rotulo -> arquivo da árvore inteira. Sem isso a lente acusava
    seis vezes uma porta que abre.
    """
    idx, textos = _indice_de_rotulos(raiz)
    meu = os.path.join(raiz, "data/maps", nome, "scripts.inc")
    arquivos = {meu} if os.path.exists(meu) else set()
    citados = set()
    if os.path.exists(meu):
        citados |= set(RE_MAP_SCRIPT.findall(textos.get(meu, "")))
    for chave in ("coord_events", "bg_events", "object_events"):
        for e in (dados or {}).get(chave) or []:
            s = e.get("script")
            if s and s != "NULL" and s != "0":
                citados.add(s)
    for rotulo in citados:
        cam = idx.get(rotulo)
        if cam:
            arquivos.add(cam)
    fora = set()
    for cam in arquivos:
        for m in RE_CELULA_DE_SCRIPT.finditer(textos.get(cam, "")):
            fora.add((int(m.group(2)), int(m.group(3))))
    return fora


class Grade:
    """Comportamento e colisão de CADA célula de um mapa. None se não deu para ler."""

    def __init__(self, raiz):
        self.raiz = raiz
        self.layouts = {l["id"]: l for l in json.load(
            open(os.path.join(raiz, "data/layouts/layouts.json")))["layouts"]
            if "id" in l}
        self.cache_ts = {}

    def _atributos(self, ts):
        if ts not in self.cache_ts:
            self.cache_ts[ts] = vwt.tabela_de_atributos(ts)
        return self.cache_ts[ts]

    def de(self, dados):
        lay = self.layouts.get(dados.get("layout"))
        if not lay:
            return None
        bp = os.path.join(self.raiz, lay.get("blockdata_filepath", ""))
        if not os.path.exists(bp):
            return None
        prim, _ = self._atributos(lay.get("primary_tileset"))
        seg, _ = self._atributos(lay.get("secondary_tileset"))
        if prim is None or seg is None:
            return None
        blk = open(bp, "rb").read()
        w, h = lay["width"], lay["height"]
        # O corte primário/secundário e a CONSTANTE do motor
        # (`GetNumMetatilesInPrimary`), 512 no Emerald e 640 no ramo grande, e
        # NÃO o tamanho do arquivo do primário. Confundir os dois custou 723
        # falsos positivos ao `valida_warp_tile.py` em 05/08/2026.
        corte = 640 if lay.get("layout_version", "") in ("frlg", "johto") else 512
        celulas = {}
        for y in range(h):
            for x in range(w):
                i = (y * w + x) * 2
                if i + 2 > len(blk):
                    continue
                bruto = struct.unpack("<H", blk[i:i + 2])[0]
                mt, colisao = bruto & 0x3FF, (bruto >> 10) & 3
                tab, rel = (prim, mt) if mt < corte else (seg, mt - corte)
                if rel >= len(tab):
                    continue
                celulas[(x, y)] = (tab[rel], colisao)
        return celulas


VIZINHOS = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))


def blocos(celulas):
    """Componentes conexas de MESMO comportamento entre as células de entrada."""
    visto, fora = set(), []
    for c0 in celulas:
        if c0 in visto:
            continue
        alvo = celulas[c0]
        fila, bloco = [c0], []
        visto.add(c0)
        while fila:
            cx, cy = fila.pop()
            bloco.append((cx, cy))
            for dx, dy in VIZINHOS:
                v = (cx + dx, cy + dy)
                if v in celulas and v not in visto and celulas[v] == alvo:
                    visto.add(v)
                    fila.append(v)
        fora.append((alvo, sorted(bloco)))
    return fora


def varre(raiz=None):
    """Devolve (achados, censo). Achado e dict com regra, classe, região, texto."""
    raiz = raiz or REPO
    mapas = carrega_mapas(raiz)
    grade = Grade(raiz)
    achados = []
    censo = collections.Counter()

    for nome in sorted(mapas):
        dados, grupo = mapas[nome]
        # TUMULO: mapa cortado que ficou na tabela só para não deslocar índice
        # de save. Sem warp, sem conexão e MAPSEC_NONE, os três juntos, ou com o
        # carimbo `cortado_por` que a onda do cartucho 1 (07/09/2026) deixou nos
        # 729 mapas de Unova e Galar. Túmulo NÃO cai no balde padrão de Hoenn:
        # sai da conta antes de a região ser decidida.
        if (dados.get("cortado_por")
                or (str(dados.get("region_map_section")) == "MAPSEC_NONE"
                    and not dados.get("warp_events")
                    and not dados.get("connections"))):
            censo["tumulos"] += 1
            continue
        celulas = grade.de(dados)
        if celulas is None:
            # Cegueira contada como zero foi o defeito que o `valida_warp_tile`
            # já pagou: aqui ela é CONTADA, nunca silenciada.
            censo["mudos"] += 1
            continue
        reg = regiao_de(nome, grupo)
        fora = dados.get("map_type") in AO_AR_LIVRE
        censo["mapas"] += 1
        censo["mapas_" + ("fora" if fora else "dentro")] += 1
        warps = dados.get("warp_events") or []
        onde_ha_warp = {(w.get("x", 0), w.get("y", 0)) for w in warps}
        do_script = celulas_de_script(raiz, nome, dados)
        com_placa = {(b.get("x"), b.get("y")) for b in (dados.get("bg_events") or [])
                     if b.get("script") in SCRIPTS_DE_PLACA}

        def anota(regra, classe, x, y, texto):
            achados.append(dict(regra=regra, classe=classe, regiao=reg,
                                mapa=nome, x=x, y=y, texto=texto))

        # --- P1 e P2: porta desenhada sem warp em cima ----------------------
        de_entrada = {c: v[0] for c, v in celulas.items() if v[0] in DE_FAMILIA}
        for comportamento, bloco in blocos(de_entrada):
            fam = DE_FAMILIA[comportamento]
            censo[("blocos", fam, "fora" if fora else "dentro")] += 1
            if any(c in onde_ha_warp for c in bloco):
                continue
            if any(c in do_script for c in bloco):
                censo["porta_de_script"] += 1
                continue
            # PLACA: porta que o jogo EXPLICA. Medido no map.json, não em lista:
            # a célula tem `bg_event` apontando para uma das duas placas comuns
            # de porta fechada, então o jogador que anda até ela recebe uma
            # resposta em inglês em vez de silêncio. Isso é a decisão do Gui de
            # 07/09/2026 na pergunta 46, e é contado à parte, nunca reprovado.
            if any(c in com_placa for c in bloco):
                censo["placa"] += 1
                continue
            x, y = bloco[0]
            mb = vwt.NOME.get(comportamento, str(comportamento))
            largo = "" if len(bloco) == 1 else f", bloco de {len(bloco)} celulas"
            if (nome, x, y) in LISTA_BRANCA:
                censo["lista_branca"] += 1
                continue
            if not fora:
                # P2 e falso positivo CALIBRADO: a taxa aqui empata com a do
                # pokeemerald intocado (103 blocos em 310 mapas fechados, nos
                # dois). Fica contado e visível, nunca reprovado.
                anota("P2", "falso positivo", x, y,
                      f"{fam} {mb} sem warp em mapa fechado{largo}")
                continue
            if (nome, x, y) in SEM_INTERIOR:
                anota("P1", "sem interior", x, y,
                      f"{SEM_INTERIOR[(nome, x, y)]}: {mb} sem warp{largo}")
                continue
            anota("P1", "trava", x, y,
                  f"porta desenhada ao ar livre e sem warp: {mb}{largo}")

        # --- P3: o warp existe, a porta existe, e estão em células diferentes
        for i, w in enumerate(warps):
            x, y = w.get("x", 0), w.get("y", 0)
            aqui = celulas.get((x, y))
            if aqui is None:
                continue                    # fora da grade: e caso do P1 do lente_warps
            morto, motivo = vwt.warp_morto(aqui[0], aqui[1])
            if not morto or (x, y) in do_script:
                continue
            perto = []
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == dy == 0:
                        continue
                    v = celulas.get((x + dx, y + dy))
                    if v is None or v[0] not in DE_FAMILIA:
                        continue
                    if (x + dx, y + dy) in onde_ha_warp or (x + dx, y + dy) in do_script:
                        continue
                    if not vwt.warp_morto(v[0], v[1])[0]:
                        perto.append((x + dx, y + dy, vwt.NOME.get(v[0], v[0])))
            if perto:
                px, py, pmb = perto[0]
                anota("P3", "trava", x, y,
                      f"warp {i} em ({x},{y}) não dispara ({motivo}) e há "
                      f"{pmb} SEM warp em ({px},{py}): o warp está fora da "
                      f"célula da porta")
    return achados, censo


# ---------------------------------------------------------------------------
def tabela(achados, censo):
    por = collections.Counter((a["classe"], a["regiao"]) for a in achados)
    classes = [c for c in ("trava", "sem interior", "falso positivo")
               if any(k[0] == c for k in por)]
    regs = [r for r in REGIOES if any(k[1] == r for k in por)]
    larg = max([len(c) for c in classes] + [6])
    print(" " * (larg + 2) + "".join(f"{r:>9}" for r in regs) + f"{'total':>9}")
    for c in classes:
        linha = "".join(f"{por[(c, r)]:>9}" for r in regs)
        print(f"{c:<{larg}}  " + linha
              + f"{sum(por[(c, r)] for r in regs):>9}")
    print(f"\nmapas medidos: {censo['mapas']} "
          f"({censo['mapas_fora']} ao ar livre, {censo['mapas_dentro']} fechados), "
          f"túmulos fora do denominador: {censo['tumulos']}, "
          f"não medidos: {censo['mudos']}")
    print(f"portas com PLACA que explica (bg_event), fora da conta: "
          f"{censo['placa']}")
    print(f"portas que o ROTEIRO abre (setmetatile/opendoor), fora da conta: "
          f"{censo['porta_de_script']}; lista branca: {censo['lista_branca']}")
    travas = [a for a in achados if a["classe"] == "trava"]
    c1 = [a for a in travas if a["regiao"] in DO_CARTUCHO_1]
    print(f"\nTRAVAS no cartucho 1 (Kanto, Johto, Hoenn, Sinnoh): {len(c1)}")
    return travas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lista", action="store_true")
    ap.add_argument("--regiao")
    ap.add_argument("--classe")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        return demo()
    achados, censo = varre()
    if a.regiao:
        achados = [x for x in achados if x["regiao"].lower() == a.regiao.lower()]
    if a.classe:
        achados = [x for x in achados if x["classe"] == a.classe]
    if a.lista:
        for x in sorted(achados, key=lambda x: (x["regiao"], x["mapa"], x["y"], x["x"])):
            print(f"{x['regra']:3} {x['classe']:14} {x['regiao']:7} "
                  f"{x['mapa']:36} ({x['x']:3},{x['y']:3}) {x['texto']}")
        return 0
    tabela(achados, censo)
    return 0


def demo():
    """Autoteste com mutacao plantada: se a lente parar de morder, cai."""
    ruim = 0

    def falso(msg):
        nonlocal ruim
        ruim = 1
        print(f"  lente_portas DEMO: {msg}")

    # 1. A leitura do enum tem que ser por NOME, e as famílias tem que existir.
    if vwt._MB["MB_ANIMATED_DOOR"] not in DE_FAMILIA:
        falso("MB_ANIMATED_DOOR ficou de fora da familia de porta")
    if vwt._MB.get("MB_BRIDGE_OVER_OCEAN") in DE_FAMILIA:
        falso("MB_BRIDGE_OVER_OCEAN entrou na conta: sao 608 pontes do vanilla")

    # 2. O bloco: porta larga e UMA porta. Quatro células coladas com o mesmo
    #    comportamento e um warp em qualquer uma delas não pode acusar as
    #    outras três.
    cels = {(10, 4): 1, (11, 4): 1, (12, 4): 1, (13, 4): 1, (20, 4): 1}
    bs = blocos(cels)
    if len(bs) != 2 or sorted(len(b) for _, b in bs) != [1, 4]:
        falso(f"blocos() nao juntou a porta larga: {bs}")

    # 3. A leitura de `setmetatile`/`opendoor` sai do texto do script.
    cel = celulas_de_script(REPO, "MahoganyTown_Shop")
    if (7, 4) not in cel:
        falso("celulas_de_script nao viu o `setmetatile 7, 4` da loja de Mahogany")
    # O caso do elevador: o `opendoor 9, 4` está no .inc do MAPA DO ELEVADOR, e
    # o andar só cita o rotulo. Se a busca voltar a ser só o arquivo do próprio
    # mapa, este bloco cai.
    andar = json.load(open(os.path.join(
        REPO, "data/maps/GoldenrodCity_DepartmentStore_1F/map.json"), encoding="utf-8"))
    cel = celulas_de_script(REPO, "GoldenrodCity_DepartmentStore_1F", andar)
    if (9, 4) not in cel:
        falso("celulas_de_script nao seguiu o rotulo ate o `opendoor 9, 4` do elevador")

    achados, censo = varre()
    # Piso de cegueira. Medido em 07/09/2026, ja sem Unova e Galar: 1.573 mapas
    # vivos. O numero antigo era 2.300, de quando as seis regioes existiam.
    if censo["mapas"] < 1500:
        falso(f"so {censo['mapas']} mapas medidos, a arvore tem mais de 1.500")
    if censo["mudos"]:
        falso(f"{censo['mudos']} mapas nao medidos: a lente esta cega neles")

    # 4. Hoenn é o vanilla e Kanto é o Ikarus v3.2 já conferido porta a porta:
    #    trava ali é a lente discordando do desenho aprovado (lição 4.2). Este
    #    bloco cai se alguém afrouxar a lista branca, e é ele que obriga cada
    #    porta nova do hack a ser justificada uma a uma.
    for r in ("Hoenn", "Kanto"):
        n = len([a for a in achados if a["classe"] == "trava" and a["regiao"] == r])
        if n:
            falso(f"{n} trava(s) em {r}, que e vanilla intocado")

    if not ruim:
        print("demo ok")
    return ruim


if __name__ == "__main__":
    sys.exit(main() or 0)
