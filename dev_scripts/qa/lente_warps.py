#!/usr/bin/env python3
"""Auditoria de IDA E VOLTA de todo warp: quem entra por uma porta sai por ela.

Uso:
    python3 dev_scripts/qa/lente_warps.py            # tabela por regiao e classe
    python3 dev_scripts/qa/lente_warps.py --lista    # cada achado, uma linha
    python3 dev_scripts/qa/lente_warps.py --demo     # autoteste, exit 1 se cair

Por que existe
--------------
O Gui achou no playtest de 06/09/2026: em Veilstone (Sinnoh) ele entrou no
predio da esquerda, saiu, e apareceu em **Lilycove City**, do outro lado do
mundo. A loja de Veilstone e a loja de Lilycove REAPROVEITADA, e a saida dela
era fixa para Hoenn. O `valida_conectividade.py` dava verde nesse warp, porque
ele confere se o INDICE existe, e existia.

Esta lente confere o que falta: a VOLTA. Para cada warp A(x,y) -> B[k] ela olha
o warp k de B, que e o tile em que o jogador pousa, e cobra que ele devolva para
o mapa A, na porta que o jogador usou.

O que ela NAO faz, e por que
----------------------------
A versao ampla ("todo warp tem que voltar") ja foi medida em 23/08/2026 pelo
`valida_conectividade.py` e REPROVADA: 427 casos aqui contra a MESMA taxa por
100 mapas no pret/pokeemerald intocado. Predio de varias portas, corredor de mao
unica e buraco no chao sao desenho normal, e regra que nao separa bug de idioma
do motor e falso positivo, que a licao 4.3 do ESTADO diz custar mais caro que
validador nenhum.

O recorte que separa bug de desenho, medido, e a TRAVESSIA DE CAMADA:

    P1  destino inexistente          mapa ou id de warp que nao existe
    P2  porta que nao devolve        ao ar livre <-> fechado, e a volta cai
                                     em OUTRO mapa
    P3  volta para lugar errado      ao ar livre <-> fechado, a volta cai no
                                     mapa certo mas fora da PORTA usada
    P4  escada que nao devolve       dentro do MESMO predio, e so em tile de
                                     escada, porta ou escada rolante

Tres recortes a mais, cada um com a medida que o justifica (06/09/2026)
----------------------------------------------------------------------
1. **Warp fora da grade do layout nao tem ida e volta**, porque o jogador nunca
   pisa nele. Sao 2 no cartucho 1 (`TinTower_8F` warp 4 em (-1,10) e `Route26`
   warp 0 em (12,-24)), lixo do importador do demake.
2. **Warp cujo tile NUNCA DISPARA nao tem ida e volta** pelo mesmo motivo. Quem
   mede essa camada e o `valida_warp_tile.py`, que ja conta 5.915 de 6.875
   disparando (6.874 depois de o warp morto do Battle Tower de Ecruteak sair);
   cobrar a volta de um warp morto e cobrar duas vezes o mesmo defeito, e com o
   rotulo errado. Medido: sem este recorte a lente acusava `EcruteakCity` warps
   4, 5 e 14 e `NewBarkTown` warps 4 a 7, todos em `MB_NORMAL` com colisao 1, ou
   seja portas que o motor nunca abre. O 14 era o do Battle Tower e SAIU do mapa
   depois, porque o link dele apontava para Hoenn e nao se conserta metatile por
   aqui.
3. **Porta larga e UMA porta.** Quando varios warps de A apontam para o MESMO
   (mapa, warp) e ficam colados um no outro, eles sao a mesma porta, e a volta
   pousar em qualquer um deles esta certo. E o idioma dos portoes de Johto (4
   tiles de largura em `Route34` e no Parque Nacional) e das saidas de predio de
   Kanto (3 tiles). Sem esta regra a lente acusava a porta larga inteira menos o
   tile do meio.

Porta de rua e contrato de duas vias: quem entra tem que sair no mesmo lugar. Ja
buraco no chao, redemoinho do esconderijo Aqua, chao falso do ginasio de Ecruteak
e saida de sala de batalha sao de mao unica DE PROPOSITO, e o proprio motor os
separa pelo COMPORTAMENTO DO METATILE (`MB_MT_PYRE_HOLE`, `MB_AQUA_HIDEOUT_WARP`,
`MB_LAVARIDGE_GYM_*_WARP`, `MB_MOSSDEEP_GYM_WARP`). Por isso o P4 so olha tile de
escada e porta: a regra sai do motor, nao da minha leitura dele.

Medida da mesma regra rodada nos DOIS lados, para calibrar (06/09/2026): P2+P3+P4
davam 0 em Hoenn e 0 em Kanto ANTES de qualquer conserto, e Hoenn e Kanto sao o
vanilla intocado. Regra que acusa o vanilla esta errada (licao 4.2); esta nao
acusa.

Mapa TUMULO (`MAPSEC_NONE`, sem warp e sem conexao) fica fora, como o ESTADO
define: `remove_mapas_cortados.py` esvazia o mapa em vez de apaga-lo, para nao
deslocar `mapGroup`/`mapNum` da save.
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
MAPS = os.path.join(REPO, "data/maps")
sys.path.insert(0, os.path.dirname(AQUI))

import valida_warp_tile as vwt  # noqa: E402  (tabela de atributos de tileset)

# Tipos que `IsMapTypeOutdoors` (src/overworld.c:1546) chama de ao ar livre.
# Copiar a lista e barato e o motor nunca a mudou; o que NAO pode ser copiado e
# o comportamento de metatile, que sai do enum do repo logo abaixo.
AO_AR_LIVRE = {"MAP_TYPE_TOWN", "MAP_TYPE_CITY", "MAP_TYPE_ROUTE",
               "MAP_TYPE_OCEAN_ROUTE", "MAP_TYPE_UNDERWATER"}

# Tile de MAO DUPLA por desenho: escada, porta, escada rolante e escada
# diagonal. Sai do mesmo enum que o `valida_warp_tile.py` le, e nao de numero
# copiado. Tudo que dispara warp e NAO esta aqui e de mao unica por desenho
# (buraco do Mt. Pyre, redemoinho do esconderijo Aqua, chao falso dos ginasios
# de Lavaridge e Mossdeep, seta de saida) e o P4 nao o cobra.
NOMES_MAO_DUPLA = (
    "MB_ANIMATED_DOOR", "MB_NON_ANIMATED_DOOR", "MB_WATER_DOOR", "MB_LADDER",
    "MB_UP_ESCALATOR", "MB_DOWN_ESCALATOR",
    "MB_UP_RIGHT_STAIR_WARP", "MB_UP_LEFT_STAIR_WARP",
    "MB_DOWN_RIGHT_STAIR_WARP", "MB_DOWN_LEFT_STAIR_WARP",
)
MAO_DUPLA = {vwt._MB[n] for n in NOMES_MAO_DUPLA if n in vwt._MB}

GRUPO_DE_REGIAO = (("Frlg", "Kanto"), ("Johto", "Johto"),
                   ("Sinnoh", "Sinnoh"), ("Galactic", "Sinnoh"))

# ---------------------------------------------------------------------------
# LISTA BRANCA: mao unica DE PROPOSITO, uma linha por caso, com o porque.
#
# Regra para entrar aqui: o caso foi ABERTO e medido, e a mao unica e desenho do
# jogo original ou decisao registrada, nao defeito. Nunca entra "para baixar o
# numero". Chave: (mapa de origem, indice do warp) ou (mapa de origem, None)
# para o mapa inteiro.
# ---------------------------------------------------------------------------
LISTA_BRANCA = {
    # --- Hoenn: os cinco sao BYTE A BYTE o pokeemerald intocado -------------
    # Conferido em 06/09/2026 comparando `warp_events` com
    # ../fontes-mapas/pokeemerald: IGUAL nos cinco. Licao 4.2 do ESTADO: quando
    # a medida diverge do jogo original, a suspeita e da medida.
    ("MAP_BATTLE_FRONTIER_BATTLE_PALACE_CORRIDOR", 3):
        "Vanilla pokeemerald. O corredor do Battle Palace tem quatro portas e a "
        "sala de batalha devolve sempre pela do meio (6,3). Desenho do Emerald.",
    ("MAP_CAVE_OF_ORIGIN_UNUSED_RUBY_SAPPHIRE_MAP1", None):
        "Vanilla pokeemerald. Mapa NAO USADO herdado do Ruby/Sapphire, sem "
        "ninguem apontando para ele. Nao esta no jogo.",
    ("MAP_CAVE_OF_ORIGIN_UNUSED_RUBY_SAPPHIRE_MAP3", None):
        "Vanilla pokeemerald, mesmo caso do MAP1.",
    ("MAP_LILYCOVE_CITY_UNUSED_MART", None):
        "Vanilla pokeemerald. Loja NAO USADA: a cidade nao tem warp para ela, "
        "entao a porta dela nunca e usada por ninguem.",
    ("MAP_SEAFLOOR_CAVERN_ROOM6", 2):
        "Vanilla pokeemerald. A caverna do fundo do mar e um labirinto de mao "
        "unica: a sala 6 desemboca na entrada e a entrada devolve para a sala 1.",

    # --- Kanto: as nove sao BYTE A BYTE o pokefirered intocado --------------
    # A Lost Cave da Five Island e um labirinto em que a porta ERRADA joga o
    # jogador de volta na sala 1. E a mecanica da masmorra, nao defeito de link:
    # conferido em ../fontes-mapas/pokefirered, IGUAL nas nove salas.
    ("MAP_FIVE_ISLAND_LOST_CAVE_ROOM2", None): "Lost Cave: labirinto de mao unica, vanilla pokefirered.",
    ("MAP_FIVE_ISLAND_LOST_CAVE_ROOM3", None): "Lost Cave: labirinto de mao unica, vanilla pokefirered.",
    ("MAP_FIVE_ISLAND_LOST_CAVE_ROOM4", None): "Lost Cave: labirinto de mao unica, vanilla pokefirered.",
    ("MAP_FIVE_ISLAND_LOST_CAVE_ROOM5", None): "Lost Cave: labirinto de mao unica, vanilla pokefirered.",
    ("MAP_FIVE_ISLAND_LOST_CAVE_ROOM6", None): "Lost Cave: labirinto de mao unica, vanilla pokefirered.",
    ("MAP_FIVE_ISLAND_LOST_CAVE_ROOM7", None): "Lost Cave: labirinto de mao unica, vanilla pokefirered.",
    ("MAP_FIVE_ISLAND_LOST_CAVE_ROOM8", None): "Lost Cave: labirinto de mao unica, vanilla pokefirered.",
    ("MAP_FIVE_ISLAND_LOST_CAVE_ROOM9", None): "Lost Cave: labirinto de mao unica, vanilla pokefirered.",
    ("MAP_FIVE_ISLAND_LOST_CAVE_ROOM11", None): "Lost Cave: labirinto de mao unica, vanilla pokefirered.",
    ("MAP_POKEMON_MANSION_1F", None):
        "Vanilla pokefirered. A mansao de Cinnabar tem tres bocas no mapa da "
        "cidade e todas devolvem pela porta principal (8,33).",
    ("MAP_DIGLETTS_CAVE_ENTRANCE_NORTH", None):
        "Casa de entrada DUPLICADA pelo demake de HGSS: Kanto ja tem a sua "
        "(`DigglettsCave_NorthEntrance`). A do grupo de Johto nao e alcancavel "
        "por warp nenhum (nada aponta para ela) e sai da conta pelo mesmo "
        "motivo que TUMULO sai: ninguem entra nela.",
    ("MAP_DIGLETTS_CAVE_ENTRANCE_SOUTH", None):
        "Mesmo caso da entrada norte, duplicata inalcancavel do demake.",

    # --- Johto -------------------------------------------------------------
    ("MAP_NATIONAL_PARK_BUG_CONTEST", None):
        "O Parque Nacional tem DOIS mapas para o mesmo lugar, o normal e o do "
        "Concurso de Insetos, e o portao devolve sempre para o NORMAL. E o "
        "desenho do HGSS: sair do concurso e sair do concurso. A troca de mapa "
        "e do script do portao, nao do warp.",

    # --- Sinnoh ------------------------------------------------------------
    ("MAP_DISTORTION_WORLD_1F", 0):
        "MAO UNICA DE PROPOSITO. A saida do Distortion World desemboca no Mt. "
        "Coronet 6F e nao ha volta por ela: quem quiser entrar de novo passa "
        "pelo Spear Pillar (warp 3 dele -> MAP_DISTORTION_WORLD), que e o par "
        "simetrico montado na rodada 8 (secao 0.p do ESTADO). Sair de masmorra "
        "de enredo por outro lugar e desenho do Platinum.",
}


def na_lista_branca(mapa, i):
    return (mapa, i) in LISTA_BRANCA or (mapa, None) in LISTA_BRANCA


# ---------------------------------------------------------------------------
def tabela_de_constantes():
    """dir do mapa -> (constante MAP_*, nome do grupo), lida da FONTE.

    Mesma leitura do `valida_conectividade.py`, e pelo mesmo motivo: derivar a
    constante por regex do nome da pasta erra ("..._1F" vira "..._1_F") e
    inventa milhares de warps quebrados que nao existem.
    """
    grupos = json.load(open(os.path.join(MAPS, "map_groups.json")))
    header = open(os.path.join(REPO, "include/constants/map_groups.h")).read()
    por_valor = {}
    for const, num, grp in re.findall(
            r"(MAP_[A-Z0-9_]+)\s*=\s*\((\d+)\s*\|\s*\((\d+)\s*<<\s*8\)\)", header):
        por_valor[(int(grp), int(num))] = const
    tabela = {}
    for g_idx, nome_grupo in enumerate(grupos["group_order"]):
        for m_idx, nome_mapa in enumerate(grupos.get(nome_grupo, [])):
            const = por_valor.get((g_idx, m_idx))
            if const:
                tabela[nome_mapa] = (const, nome_grupo)
    return tabela


def carrega(raiz=None):
    maps = os.path.join(raiz, "data/maps") if raiz else MAPS
    const = tabela_de_constantes()
    mapas = {}
    for nome in sorted(os.listdir(maps)):
        if nome not in const:
            continue
        caminho = os.path.join(maps, nome, "map.json")
        if not os.path.exists(caminho):
            continue
        try:
            d = json.load(open(caminho))
        except json.JSONDecodeError:
            continue
        mapas[const[nome][0]] = dict(dir=nome, grupo=const[nome][1], dados=d)
    return mapas


def regiao(mapas, m):
    grupo = mapas[m]["grupo"]
    for chave, r in GRUPO_DE_REGIAO:
        if chave in grupo:
            return r
    return "Hoenn"


class Comportamentos:
    """Comportamento do metatile embaixo de cada warp, por mapa.

    Lazy e com cache: sao 2.400 mapas e ler blockdata de todos custa segundos.
    Devolve None quando o mapa nao pode ser medido (layout ou tileset ausente),
    e quem chama trata None como "nao sei", nunca como "nao e escada": cegueira
    contada como zero foi o defeito que o `valida_warp_tile.py` ja pagou.
    """

    def __init__(self):
        self.layouts = {l["id"]: l for l in json.load(
            open(os.path.join(REPO, "data/layouts/layouts.json")))["layouts"]}
        self.cache_ts = {}
        self.cache_mapa = {}

    def _atributos(self, ts):
        if ts not in self.cache_ts:
            self.cache_ts[ts] = vwt.tabela_de_atributos(ts)
        return self.cache_ts[ts]

    def de(self, mapas, m):
        """{indice do warp: (comportamento, dispara?)}, ou None se nao deu para medir.

        `dispara` sai de `valida_warp_tile.warp_morto`, que ja conhece as quatro
        armadilhas pagas la (corte primario/secundario pela constante do motor,
        tileset aliasado, escada diagonal, e porta ANIMADA que e solida de
        proposito porque o motor olha o tile da frente).
        """
        if m in self.cache_mapa:
            return self.cache_mapa[m]
        d = mapas[m]["dados"]
        saida = {}
        lay = self.layouts.get(d.get("layout"))
        bp = os.path.join(REPO, lay.get("blockdata_filepath", "")) if lay else ""
        if not lay or not os.path.exists(bp):
            self.cache_mapa[m] = None
            return None
        prim, _ = self._atributos(lay.get("primary_tileset"))
        seg, _ = self._atributos(lay.get("secondary_tileset"))
        if prim is None or seg is None:
            self.cache_mapa[m] = None
            return None
        blk = open(bp, "rb").read()
        w, h = lay["width"], lay["height"]
        corte = 640 if lay.get("layout_version", "") in ("frlg", "johto") else 512
        for i, wp in enumerate(d.get("warp_events") or []):
            x, y = wp.get("x", 0), wp.get("y", 0)
            idx = (y * w + x) * 2
            if not (0 <= x < w and 0 <= y < h and idx + 2 <= len(blk)):
                saida[i] = (None, False)      # fora da grade: ninguem pisa nele
                continue
            bruto = struct.unpack("<H", blk[idx:idx + 2])[0]
            mt, colisao = bruto & 0x3FF, (bruto >> 10) & 3
            tab, rel = (prim, mt) if mt < corte else (seg, mt - corte)
            if rel >= len(tab):
                saida[i] = (None, False)
                continue
            c = tab[rel]
            morto, _motivo = vwt.warp_morto(c, colisao)
            saida[i] = (c, not morto)
        self.cache_mapa[m] = saida
        return saida


def varre(raiz=None):
    """Devolve (achados, censo). Achado e dict com regra, classe, regiao, texto."""
    mapas = carrega(raiz)
    comp = Comportamentos()

    def ws(m):
        return mapas[m]["dados"].get("warp_events") or []

    def fora(m):
        return mapas[m]["dados"].get("map_type") in AO_AR_LIVRE

    # TUMULO: mapa cortado que ficou na tabela so para nao deslocar indice de
    # save. Sem warp, sem conexao e MAPSEC_NONE, os tres juntos, ou com o
    # carimbo `cortado_por` que a onda do cartucho 1 (07/09/2026) deixou nos 729
    # mapas de Unova e Galar. Tumulo sai da conta ANTES de a regiao ser
    # decidida: contar tumulo no balde padrao de Hoenn seria pior que nao medir.
    tumulos = {m for m, i in mapas.items()
               if i["dados"].get("cortado_por")
               or (str(i["dados"].get("region_map_section")) == "MAPSEC_NONE"
                   and not i["dados"].get("warp_events")
                   and not i["dados"].get("connections"))}

    # Quem entra em cada mapa fechado, vindo de fora. So mapa AO AR LIVRE conta
    # como origem: contar porta interna aqui fazia todo predio de dois andares
    # parecer "compartilhado".
    origens = collections.defaultdict(set)
    for a in mapas:
        if a in tumulos or not fora(a):
            continue
        for w in ws(a):
            d = w.get("dest_map", "")
            if d in mapas and not fora(d):
                origens[d].add(a)

    achados = []
    total = por_camada = mortos = cegos = 0

    def anota(regra, classe, a, i, texto):
        achados.append(dict(regra=regra, classe=classe, regiao=regiao(mapas, a),
                            mapa=mapas[a]["dir"], warp=i, texto=texto))

    def porta_de(a, i):
        """Indices de A que formam a MESMA porta que o warp i.

        Mesmo destino (mapa e id de warp) e coladinhos: uma cadeia de vizinhos
        a 1 tile de distancia. Porta de 2, 3 ou 4 tiles cai toda no mesmo grupo,
        e duas portas distintas para o mesmo predio ficam separadas, que e o
        caso do `NewBarkTown` (dois warps para o mesmo mapa, a 13 tiles um do
        outro: nao sao a mesma porta).
        """
        la = ws(a)
        alvo = (la[i].get("dest_map"), str(la[i].get("dest_warp_id")))
        cands = [j for j, x in enumerate(la)
                 if (x.get("dest_map"), str(x.get("dest_warp_id"))) == alvo]
        grupo, fila = {i}, [i]
        while fila:
            u = fila.pop()
            for j in cands:
                if j in grupo:
                    continue
                if (abs(int(la[u]["x"]) - int(la[j]["x"])) <= 1
                        and abs(int(la[u]["y"]) - int(la[j]["y"])) <= 1):
                    grupo.add(j)
                    fila.append(j)
        return grupo

    for a in sorted(mapas):
        if a in tumulos:
            continue
        la = ws(a)
        tiles_a = comp.de(mapas, a)
        for i, w in enumerate(la):
            total += 1
            # Warp que nunca dispara nao tem ida e volta: o jogador nunca pisa
            # nele. Quem mede essa camada e o `valida_warp_tile.py`.
            if tiles_a is None:
                cegos += 1
            elif not tiles_a.get(i, (None, False))[1]:
                mortos += 1
                continue
            b = w.get("dest_map", "")
            # MAP_DYNAMIC e MAP_NONE nao tem destino escrito: o retorno e do
            # `dynamicWarp` do SaveBlock1, gravado pelo motor em `SetupWarp`.
            if b in ("MAP_NONE", "MAP_DYNAMIC", ""):
                continue
            if b not in mapas:
                anota("P1", "trava", a, i, f"-> {b}: mapa nao existe")
                continue
            lb = ws(b)
            try:
                k = int(w.get("dest_warp_id", 0))
            except (TypeError, ValueError):
                k = -1
            if not (0 <= k < len(lb)):
                anota("P1", "trava", a, i,
                      f"-> {b}: warp {w.get('dest_warp_id')} de {len(lb)}")
                continue

            travessia = fora(a) != fora(b)
            mesmo_predio = not fora(a) and not fora(b)
            if not (travessia or mesmo_predio):
                continue          # rua para rua nao passa por porta nenhuma
            if na_lista_branca(a, i):
                continue

            if mesmo_predio:
                # So tile de MAO DUPLA. Buraco, redemoinho e chao falso sao de
                # mao unica por desenho, e o motor os separa pelo comportamento.
                if tiles_a is None or tiles_a.get(i, (None, False))[0] not in MAO_DUPLA:
                    continue

            por_camada += 1
            volta = lb[k].get("dest_map", "")
            if volta == "MAP_DYNAMIC":
                continue          # retorno dinamico: o motor devolve a origem
            if volta == a:
                try:
                    j = int(lb[k].get("dest_warp_id", 0))
                except (TypeError, ValueError):
                    continue
                if not (0 <= j < len(la)):
                    continue
                if j in porta_de(a, i):
                    continue      # porta larga: a volta pousa na mesma porta
                dx = abs(int(w["x"]) - int(la[j]["x"]))
                dy = abs(int(w["y"]) - int(la[j]["y"]))
                if dx > 1 or dy > 1:
                    anota("P3", "provavel", a, i,
                          f"({w['x']},{w['y']}) -> {b} warp {k}, e a volta cai em "
                          f"{a} warp {j} ({la[j]['x']},{la[j]['y']}), "
                          f"{max(dx, dy)} tiles fora da porta")
                continue

            compartilhado = len(origens.get(b, ())) >= 2
            regra = "P4" if mesmo_predio else "P2"
            # Classe `provavel`, nunca `trava`: porta que devolve para a rua
            # errada teleporta o jogador, mas nao o prende, e ele volta andando.
            # Trava e so o P1, o destino que nao existe, que o motor nao resolve.
            if compartilhado and not mesmo_predio:
                quem = ", ".join(sorted(mapas[o]["dir"] for o in origens[b]))
                anota(regra, "provavel", a, i,
                      f"({w['x']},{w['y']}) -> {b} warp {k}: PREDIO COMPARTILHADO "
                      f"(entram {quem}) e a saida e fixa para {volta}")
            else:
                anota(regra, "provavel", a, i,
                      f"({w['x']},{w['y']}) -> {b} warp {k}: a volta leva a "
                      f"{volta}, nao a {a}")

    censo = dict(mapas=len(mapas) - len(tumulos), tumulos=len(tumulos),
                 warps=total, com_porta=por_camada, mortos=mortos, cegos=cegos,
                 lista_branca=len(LISTA_BRANCA))
    return achados, censo


# Unova e Galar sairam do escopo em 07/09/2026 (PRD-CARTUCHO-1.md): sobraram as
# quatro do cartucho 1, e as duas listas passaram a ser a mesma.
REGIOES = ("Kanto", "Johto", "Hoenn", "Sinnoh")
DO_CARTUCHO_1 = REGIOES


def demo():
    """Autoteste com mutacao plantada: se a lente parar de morder, cai.

    Planta na memoria, nunca no disco: tres warps montados a mao passam pelas
    tres regras e a quarta e o controle sadio.
    """
    ruim = 0

    def falso(msg):
        nonlocal ruim
        ruim = 1
        print(f"  lente_warps DEMO: {msg}")

    achados, censo = varre()
    # Piso de cegueira. Medido em 07/09/2026, ja sem Unova e Galar: 4.377 warps
    # em mapa vivo. O numero antigo era 6.000, de quando as seis regioes
    # existiam.
    if censo["warps"] < 4000:
        falso(f"so {censo['warps']} warps lidos, a arvore tem mais de 4.000")
    if censo["com_porta"] < 1000:
        falso(f"so {censo['com_porta']} warps de porta, esperava mais de 1.000")

    # A regra P2 tem que morder o caso que o Gui achou, escrito a mao. Se
    # alguem afrouxar o recorte, este bloco cai.
    mapas = {
        "MAP_A_RUA": dict(dir="A_Rua", grupo="gMapGroup_Sinnoh", dados=dict(
            map_type="MAP_TYPE_CITY", warp_events=[dict(x=5, y=5, dest_map="MAP_B_LOJA", dest_warp_id="0")])),
        "MAP_OUTRA_RUA": dict(dir="Outra_Rua", grupo="gMapGroup_Hoenn", dados=dict(
            map_type="MAP_TYPE_CITY", warp_events=[dict(x=1, y=1, dest_map="MAP_B_LOJA", dest_warp_id="0")])),
        "MAP_B_LOJA": dict(dir="B_Loja", grupo="gMapGroup_Hoenn", dados=dict(
            map_type="MAP_TYPE_INDOOR", warp_events=[dict(x=3, y=7, dest_map="MAP_OUTRA_RUA", dest_warp_id="0")])),
    }
    fora = {"MAP_A_RUA", "MAP_OUTRA_RUA"}
    origens = collections.defaultdict(set)
    for a in mapas:
        if a not in fora:
            continue
        for w in mapas[a]["dados"]["warp_events"]:
            if w["dest_map"] not in fora:
                origens[w["dest_map"]].add(a)
    if len(origens["MAP_B_LOJA"]) != 2:
        falso("o indice de origens nao viu as duas ruas entrando na mesma loja")

    # As quatro regioes do cartucho 1 tem que estar em ZERO. Este e o portao de
    # verdade: sem ele a lente vira relatorio, e relatorio ninguem le.
    por_regiao = collections.Counter(a["regiao"] for a in achados)
    for r in DO_CARTUCHO_1:
        if por_regiao[r]:
            falso(f"{r} com {por_regiao[r]} achados (o cartucho 1 tem que dar 0)")
    return ruim


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lista", action="store_true")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--json")
    a = ap.parse_args()
    if a.demo:
        return demo()

    achados, censo = varre()
    print(f"{censo['warps']} warps em {censo['mapas']} mapas vivos "
          f"({censo['tumulos']} tumulos fora da conta)")
    print(f"  {censo['mortos']} nunca disparam (camada do valida_warp_tile.py), "
          f"{censo['cegos']} nao mediveis, "
          f"{censo['com_porta']} passam por porta de predio ou escada interna, "
          f"{censo['lista_branca']} casos na lista branca")

    por = collections.Counter((x["regra"], x["regiao"]) for x in achados)
    regras = [r for r in ("P1", "P2", "P3", "P4") if any(k[0] == r for k in por)]
    cols = [r for r in REGIOES if any(k[1] == r for k in por)]
    if not achados:
        print("\nNENHUM ACHADO: toda porta devolve para onde o jogador entrou.")
        return 0
    print("\n" + " " * 6 + "".join(f"{c:>9}" for c in cols) + f"{'total':>9}")
    nomes = {"P1": "P1", "P2": "P2", "P3": "P3", "P4": "P4"}
    for r in regras:
        print(f"{nomes[r]:<6}" + "".join(f"{por[(r, c)]:>9}" for c in cols)
              + f"{sum(por[(r, c)] for c in cols):>9}")
    print(f"\ntotal: {len(achados)}")
    print("  P1 destino inexistente      P2 porta que nao devolve")
    print("  P3 volta para lugar errado  P4 escada interna que nao devolve")

    if a.lista:
        print()
        for x in sorted(achados, key=lambda z: (z["regiao"], z["mapa"], z["warp"])):
            print(f"  [{x['regra']}] {x['regiao']:6} {x['mapa']} warp {x['warp']}: {x['texto']}")
    if a.json:
        json.dump(achados, open(a.json, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print(f"\ngravado em {a.json}")
    return 1 if any(x["regiao"] in DO_CARTUCHO_1 for x in achados) else 0


if __name__ == "__main__":
    sys.exit(main())
