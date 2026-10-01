#!/usr/bin/env python3
"""Redistribuição dos lendários do cartucho 1 (respostas 111 e 112 do Gui, 01/10/2026).

    python3 dev_scripts/redistribui_lendarios.py            # só relata o plano
    python3 dev_scripts/redistribui_lendarios.py --aplica   # escreve
    python3 dev_scripts/redistribui_lendarios.py --tabela   # tabela final em Markdown

O que ele faz, em ordem:
 1. Tira do lugar aberto os lendários da proposta
    (`~/Downloads/lendarios-redistribuicao-proposta-bugs3.md`, 46 linhas) e
    espalha os três grupos (5 Genesect, 8 Ogerpon, 18 formas de Arceus) por
    lugares temáticos das quatro regiões, um por mapa.
 2. O tile de cada um sai da MESMA busca em largura do `lendarios_sinnoh`
    (colisão e elevação, "pôr o bicho ali não ilha ninguém", longe de warp e de
    NPC que anda, rota de pernas retas até ele), com uma diferença deliberada:
    entre os tiles que passam nos portões, vence o MAIS FUNDO (mais longe da
    entrada), porque o pedido é lugar escondido. O teto de sprite do
    `distribui_dex` (8 por janela) continua valendo.
 3. A FLAG de cada objeto NÃO muda: quem já capturou não reencontra, e a save
    continua a mesma (nenhum bit novo, nenhum apelido movido).
 4. O nível de TODO lendário, mítico, sublendário e ultra-fera vem de
    `dev_scripts/niveis_lendarios.py` (50 a 100, pelo acesso do lugar).

A tabela de decisão dos estáticos continua sendo `dev_scripts/dex_distribuicao.json`;
este arquivo só reescreve as linhas que mudam de casa e chama o executor de
sempre (`distribui_dex.aplica_estaticos`). Os três de Sinnoh que moram na tabela
do `lendarios_sinnoh.py` (Darkrai, Cresselia, Shaymin) são movidos aqui, à mão,
porque o `--aplica` daquele arquivo replaneja os dez de uma vez.
"""
import argparse
import collections
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
import distribui_dex as DD          # noqa: E402
import lendarios_sinnoh as LS       # noqa: E402
import niveis_lendarios as NL       # noqa: E402
import inventario_lendarios as INV  # noqa: E402

# ------------------------------------------------------------------ destinos
# Linhas 1 a 46 da proposta (a 13, o SUICUNE de cena de Cianwood, fica: é a
# cena do Eusine, sem batalha, e a própria proposta a lista em "ficam").
PROPOSTA = {
    "SPECIES_ZAPDOS_GALAR": "SevenIsland_SevaultCanyon_Frlg",
    "SPECIES_POIPOLE": "DistortionWorldTurnbackCaveRoom",
    "SPECIES_NAGANADEL": "SpearPillar_Distorted",
    "SPECIES_ZAMAZENTA_HERO": "IronIslandIronRuins",
    "SPECIES_ETERNATUS": "CaveOfOrigin_B1F",
    "SPECIES_KUBFU": "MuscleIsland",
    "SPECIES_URSHIFU_SINGLE_STRIKE": "MuscleIsland",
    "SPECIES_KORAIDON": "MtEmber_RubyPath_B5F_Frlg",
    "SPECIES_TERAPAGOS_NORMAL": "SixIsland_DottedHole_SapphireRoom_Frlg",
    "SPECIES_PECHARUNT": "FiveIsland_LostCave_Room14_Frlg",
    "SPECIES_SUICUNE": "TinTower_1F",
    "SPECIES_SHAYMIN_LAND": "FloaromaMeadow",
    "SPECIES_TAPU_BULU": "DontoIsland",
    "SPECIES_ZACIAN_HERO": "EternaForest",
    "SPECIES_ZARUDE": "LcSafariForest",
    "SPECIES_OKIDOGI": "LcSafariMountain",
    "SPECIES_MUNKIDORI": "LcSafariForest",
    "SPECIES_FEZANDIPITI": "LcSafariWater",
    "SPECIES_THUNDURUS_INCARNATE": "SkyPillar_4F",
    "SPECIES_COSMOG": "MtMoon_B2F_Frlg",
    "SPECIES_SOLGALEO": "LcSilverCaveDepths",
    "SPECIES_LUNALA": "LcHollowCaveChamber",
    "SPECIES_MIRAIDON": "MtCoronet6F",
    "SPECIES_MOLTRES_GALAR": "HauntedWoods_Inner",
    "SPECIES_COSMOEM": "SevenIsland_TanobyRuins_ViapoisChamber_Frlg",
    "SPECIES_NECROZMA": "SevenIsland_TanobyRuins_RixyChamber_Frlg",
    "SPECIES_NECROZMA_DUSK_MANE": "SevenIsland_TanobyRuins_WeepthChamber_Frlg",
    "SPECIES_CALYREX": "RuinsOfAlph_WordsRoom1",
    "SPECIES_CALYREX_ICE": "RuinsOfAlph_WordsRoom2",
    "SPECIES_CALYREX_SHADOW": "RuinsOfAlph_WordsRoom3",
    "SPECIES_WO_CHIEN": "SevenIsland_TanobyRuins_DilfordChamber_Frlg",
    "SPECIES_CHIEN_PAO": "SevenIsland_TanobyRuins_LiptooChamber_Frlg",
    "SPECIES_TING_LU": "SevenIsland_TanobyRuins_MoneanChamber_Frlg",
    "SPECIES_CHI_YU": "SevenIsland_TanobyRuins_ScufibChamber_Frlg",
    "SPECIES_GLASTRIER": "ShoalCave_LowTideIceRoom",
    "SPECIES_VIRIZION": "CeruleanCave_2F_Frlg",
    "SPECIES_XERNEAS_NEUTRAL": "SixIsland_PatternBush_Frlg",
    "SPECIES_KARTANA": "FiveIsland_LostCave_Room10_Frlg",
    "SPECIES_ENAMORUS_INCARNATE": "FrozenHeights",
    "SPECIES_GENESECT": "PokemonMansion_B1F_Frlg",
    "SPECIES_OGERPON_TEAL": "ThreeIsland_BerryForest_Frlg",
}

# Decisão 111 do Gui para os três grupos: ESPALHAR, cada um num lugar
# escondido e coerente com a forma, nas quatro regiões, um por mapa.
GENESECT = {  # drive -> lugar tecnológico ou abandonado
    "SPECIES_GENESECT_BURN": "MahoganyHideout_B3F",           # Johto, sala dos geradores Rocket
    "SPECIES_GENESECT_SHOCK": "NewMauville_Inside",           # Hoenn, usina abandonada
    "SPECIES_GENESECT_DOUSE": "AbandonedShip_CaptainsOffice",  # Hoenn, navio abandonado
    "SPECIES_GENESECT_CHILL": "GalacticHQ_Laboratory",        # Sinnoh, laboratório da Galáctica
}
OGERPON = {  # máscara -> lugar temático
    "SPECIES_OGERPON_TEAL_TERA": "PetalburgWoods_River",            # Hoenn, rio escondido do bosque
    "SPECIES_OGERPON_WELLSPRING": "LcUnderseaSprings",              # Johto, fonte
    "SPECIES_OGERPON_WELLSPRING_TERA": "SpringPath",                # Sinnoh, caminho da fonte
    "SPECIES_OGERPON_HEARTHFLAME": "FieryPath",                     # Hoenn, dentro do vulcão
    "SPECIES_OGERPON_HEARTHFLAME_TERA": "BurnedTower_1F",           # Johto, torre queimada
    "SPECIES_OGERPON_CORNERSTONE": "WaywardCaveB1F",                # Sinnoh, caverna de pedra
    "SPECIES_OGERPON_CORNERSTONE_TERA": "RockTunnel_B1F_Frlg",      # Kanto, túnel de pedra
}
ARCEUS = {  # tipo -> lugar do tipo (os que já estavam num lugar do tipo ficam)
    "SPECIES_ARCEUS_FIRE": "LcCinnabarVolcano",          # Kanto, vulcão
    "SPECIES_ARCEUS_FLYING": "TinTower_9F",              # Johto, alto da torre do Ho-Oh
    "SPECIES_ARCEUS_STEEL": "IronIslandB3F",             # Sinnoh, ilha de ferro
    "SPECIES_ARCEUS_DRAGON": "MeteorFalls_StevensCave",  # Hoenn, toca dos dragões
    "SPECIES_ARCEUS_POISON": "GreatMarsh6",              # Sinnoh, pântano
    "SPECIES_ARCEUS_ROCK": "OreburghMine_B2F",           # Sinnoh, mina
    "SPECIES_ARCEUS_BUG": "PetalburgWoods",              # Hoenn, bosque de insetos
    "SPECIES_ARCEUS_GRASS": "IlexForest",                # Johto, floresta do Celebi
    "SPECIES_ARCEUS_FAIRY": "MtMoon_B1F_Frlg",           # Kanto, casa dos Clefairy
    "SPECIES_ARCEUS_DARK": "RocketHideout_B4F_Frlg",     # Kanto, esconderijo Rocket
    "SPECIES_ARCEUS_FIGHTING": "MtMortar_B1F",           # Johto, caverna do Karate King
    "SPECIES_ARCEUS_GHOST": "OldChateauBackMiddleRoom",  # Sinnoh, mansão assombrada
    "SPECIES_ARCEUS_PSYCHIC": "SealedChamber_InnerRoom", # Hoenn, câmara selada
    # Ficam: WATER (Marine Cave, caverna submarina), ELECTRIC (Power Plant),
    # ICE (Ice Path), GROUND (Desert Ruins), NORMAL (Victory Road de Sinnoh).
}
DEX = {**PROPOSTA, **GENESECT, **OGERPON, **ARCEUS}

# Os três da tabela do lendarios_sinnoh.py (linhas 1, 2 e 15 da proposta).
SINNOH = {"DARKRAI": "Route209LostTower5F", "CRESSELIA": "SendoffSpring",
          "SHAYMIN": "Route224"}

# Mapas sem warp (só conexão de borda): o warp de debug sem warp válido põe o
# jogador no CENTRO do mapa (SetPlayerCoordsFromWarp, src/overworld.c). O
# planejador ganha um warp de mentira ali, e o caso de emulador usa warp_id 0.
SEM_WARP = ("MuscleIsland", "HauntedWoods_Inner", "PetalburgWoods_River")

# O Safari do Liquid Crystal: o atendente mora EM CIMA da porta, e só sai dela
# quando o jogador entra pelo balcão (VAR_SAFARI_ZONE_STATE = 2): o
# ON_TRANSITION o põe ao lado, o ON_FRAME sobe o jogador um tile e o atendente
# volta para a porta. O planejador parte do tile de cima da porta, com a porta
# como parede, e o caso de emulador acende a var antes do warp.
SAFARI_LC = {"LcSafariForest": ((25, 48), (25, 49)),
             "LcSafariMountain": ((9, 43), (9, 44)),
             "LcSafariWater": ((43, 43), (43, 44))}
VAR_SAFARI_ZONE_STATE = "0x40A4"

# Mapas com CENA de entrada que trava o jogador (map_script_2 no ON_FRAME): o
# caso de emulador entra no estado de DEPOIS da cena, que é o do jogo de verdade
# quando o jogador volta para caçar o lendário.
CENA_JA_VISTA = {"FiveIsland_LostCave_Room10_Frlg": "VAR_MAP_SCENE_FIVE_ISLAND_LOST_CAVE_ROOM10"}

_contexto_original = LS.contexto


def _contexto(nome, extra=(), ignora=(LS.MARCA,)):
    d, W, H, g, objs, moveis, warps = _contexto_original(nome, extra, ignora)
    if nome in SEM_WARP and not d.get("warp_events"):
        d = dict(d, warp_events=[{"x": W // 2, "y": H // 2, "elevation": 0,
                                  "dest_map": "MAP_NONE", "dest_warp_id": "0"}])
        warps = {(W // 2, H // 2)}
    # Borda com CONEXÃO: andar para fora dela leva ao mapa vizinho. O
    # `escorrega` acha que a borda para o jogador; ela não para. As células da
    # borda conectada entram no conjunto de warps, que a perna não pisa
    # (medido no T357: o par negativo do Petalburg Woods River saía do mapa).
    borda = set()
    for c in d.get("connections") or []:
        lado = c.get("direction")
        if lado == "up":
            borda |= {(x, 0) for x in range(W)}
        elif lado == "down":
            borda |= {(x, H - 1) for x in range(W)}
        elif lado == "left":
            borda |= {(0, y) for y in range(H)}
        elif lado == "right":
            borda |= {(W - 1, y) for y in range(H)}
    warps = set(warps) | borda
    if nome in SAFARI_LC:
        (px, py), porta = SAFARI_LC[nome]
        d = dict(d, warp_events=[{"x": px, "y": py, "elevation": 0,
                                  "dest_map": "MAP_NONE", "dest_warp_id": "0"}])
        warps = {porta}
        objs = set(objs) | {porta}
    return d, W, H, g, objs, moveis, warps


LS.contexto = _contexto
_sementes_original = LS.sementes_dos_warps


def _sementes(d, W, H, g):
    s = _sementes_original(d, W, H, g)
    return s or [(W // 2, H // 2)]


LS.sementes_dos_warps = _sementes


def _json(m):
    return json.load(open(f"{RAIZ}/data/maps/{m}/map.json", encoding="utf-8"))


# Warps que o planejador pode usar como partida, quando não são todos. O
# Spear Pillar distorcido tem três warps em chão comum (MB_NORMAL) em que o
# warp de debug pousa o jogador UM tile ao sul, e a primeira perna para cima
# pisa no warp e leva à sala do Palkia (medido no T357.119); a porta (warp 3)
# tem o pouso que o planejador conhece.
WARPS_OK = {"SpearPillar_Distorted": (3,)}


def _warps_de(m):
    if m in WARPS_OK:
        return list(WARPS_OK[m])
    return list(range(max(1, len(_json(m).get("warp_events", [])))))


def _n_warps(m):
    return max(1, len(_json(m).get("warp_events", [])))


def lendas_no_mapa(m):
    """Tiles de Pokémon de campo que já moram no mapa (qualquer origem)."""
    return {(o["x"], o["y"]) for o in _json(m).get("object_events", [])
            if "GFX_SPECIES" in o.get("graphics_id", "")}


ESPECIAL = re.compile(r"ICE|SPIN|SLIDE|ARROW|CURRENT|MB_JUMP|MUDDY|CRACKED|HOLE|"
                      r"WATERFALL|WARP|(?<!IN)DOOR|LADDER|STAIR|PORTHOLE")


def especiais(mapa):
    """Tiles em que andar NÃO é andar: gelo, giro, seta, correnteza, salto,
    buraco, escada, porta, e metatile sem comportamento lido NA BORDA do mapa
    (sai do mapa, medido no Spring Path; no miolo os tilesets de Sinnoh têm
    muito metatile sem atributo lido e ele é chão). Somam-se as células que algum script do mapa
    troca com `setmetatile` (portão de interruptor da Mansão, por exemplo): a
    busca em largura lê o map.bin parado e não sabe em que estado o portão
    está. Viram parede para a rota e para o tile do lendário; o pouso dos warps
    fica de fora, senão o próprio ponto de partida sumiria."""
    d = _json(mapa)
    W, H, g = LS.grade(d["layout"])
    lay = LS.layouts()[d["layout"]]
    tab = ((LS.V.tabela_de_atributos(lay.get("primary_tileset"))[0] or [])
           + (LS.V.tabela_de_atributos(lay.get("secondary_tileset"))[0] or []))
    inv = {v: k for k, v in LS.V.valores_dos_comportamentos().items()}
    fora = set()
    for y in range(H):
        for x in range(W):
            mt = g[y][x] & 0x3FF
            nome = inv.get(tab[mt]) if mt < len(tab) else None
            borda = x in (0, W - 1) or y in (0, H - 1)
            if (nome is None and borda) or (nome and ESPECIAL.search(nome)):
                fora.add((x, y))
    fora |= trocados(mapa)
    poupa = set()
    for w in d.get("warp_events", []):
        poupa |= {(w["x"], w["y"]), (w["x"], w["y"] + 1)}
    if mapa in SAFARI_LC:
        poupa.add(SAFARI_LC[mapa][0])
    if mapa in SEM_WARP:
        poupa.add((W // 2, H // 2))
    return fora - poupa


# Dois mapas-anel de 13x9 (Sendoff Spring e Spring Path) em que a busca não
# acha rota: o pouso é warp de SETA na borda (apertar contra a borda sai do
# mapa, medido no T123.17) e toda perna saturante pelo corredor do meio pisa no
# warp do outro lado. O lugar é o nicho em cima do pouso, a uma perna só: UP
# satura contra o bicho em (x,4); sem o bicho, o jogador para no próprio nicho,
# (x,3), que é beco (parede em volta). Medido no emulador pelo T123.17/18 e
# pelo T357.
MANUAL = {
    "SendoffSpring": dict(T=(1, 3), para=(1, 4), vazio=(1, 3), dir="UP", warp=0,
                          porta=(1, 5), pouso=(1, 5), rota=[("UP", 2, True)]),
    "SpringPath": dict(T=(11, 3), para=(11, 4), vazio=(11, 3), dir="UP", warp=0,
                       porta=(11, 5), pouso=(11, 5), rota=[("UP", 2, True)]),
}


_ROTULO_CHAMADO = re.compile(r"^\s*(?:call|goto|call_if_\w+|goto_if_\w+)\s+(?:[^,\n]+,\s*)*"
                             r"([A-Za-z0-9_]+)\s*$", re.M)


def trocados(mapa):
    """Células que algum script troca com `setmetatile`: as do próprio mapa e as
    dos rótulos que ele chama em `data/scripts/*.inc` (a Mansão de Cinnabar
    guarda os portões do B1F em data/scripts/pokemon_mansion.inc)."""
    inc = open(f"{RAIZ}/data/maps/{mapa}/scripts.inc", encoding="utf-8").read()
    corpos = [inc]
    chamados = set(_ROTULO_CHAMADO.findall(inc))
    if chamados:
        for cam in __import__("glob").glob(f"{RAIZ}/data/scripts/*.inc"):
            txt = open(cam, encoding="utf-8", errors="replace").read()
            for rot in chamados:
                m = re.search(rf"^{rot}::?\s*$(.*?)^\s*(?:return|end)\s*$", txt, re.M | re.S)
                if m:
                    corpos.append(m.group(1))
    fora = set()
    for corpo in corpos:
        for mx, my in re.findall(r"setmetatile\s+(\d+)\s*,\s*(\d+)", corpo):
            fora.add((int(mx), int(my)))
    return fora


def planeja_fundo(mapa, usados):
    """O tile MAIS FUNDO que passa em todos os portões, com rota até ele."""
    if mapa in MANUAL and not usados:
        return dict(MANUAL[mapa])
    d = _json(mapa)
    fixos = [(o["x"], o["y"]) for o in d.get("object_events", [])]
    if len(fixos) + len(usados) + 1 > DD.TETO_OBJETOS:
        return None
    try:
        corredor = DD.corredor_de_casos(mapa)
    except IndexError:
        # caso que warpa num mapa SEM warp cai no centro; o leitor de corredor
        # do distribui_dex não sabe disso. A suíte inteira pega o conflito.
        corredor = set()
    vizinhos = set(usados) | lendas_no_mapa(mapa)
    visao = DD.visao_de_treinador(d) | especiais(mapa)
    instaveis = trocados(mapa)
    for fundo, olhos, pernas, w in [(f, o, p, w) for f, o in ((True, visao | corredor),
                                                           (True, visao),
                                                           (False, visao))
                                    for p in (4, 6) for w in _warps_de(mapa)]:
        if True:
            vetados = set()
            while True:
                e = LS.planeja(mapa, w, extra=set(usados) | vetados,
                               longe=vizinhos, ignora=(), max_pernas=pernas, fundo=fundo,
                               proibidos=olhos, instaveis=instaveis)
                if e is None:
                    break
                # Dois tetos, medidos por quem veio antes: 15 objetos acordados
                # por janela (slots do motor) e 8 Pokémon de campo por janela
                # (sprite e VRAM; o NPC comum é folha de 8 tiles e não pesa
                # como um 64x64). A VRAM de cada mapa é conferida depois pelo
                # varre_vram_ow.py e pelo contador do plano B no emulador.
                todos = fixos + list(usados) + [e["T"]]
                mons = sorted(lendas_no_mapa(mapa)) + list(usados) + [e["T"]]
                if (DD.lotacao(todos) <= DD.TETO_SPRITE
                        and DD.lotacao(mons) <= DD.TETO_SPRITE_DEX):
                    return e
                vetados.add(e["T"])
    return None


def plano():
    """[(chave, mapa_destino, geometria)] para todos os que mudam de casa."""
    por_mapa = collections.defaultdict(list)
    for esp, m in DEX.items():
        por_mapa[m].append(("dex", esp))
    for lid, m in SINNOH.items():
        por_mapa[m].append(("ls", lid))
    fora, falhas = [], []
    for m in sorted(por_mapa):
        usados = []
        for tipo, chave in sorted(por_mapa[m]):
            e = planeja_fundo(m, usados)
            if e is None:
                falhas.append(f"{chave} -> {m}: nenhum tile passa nos portões")
                continue
            usados.append(e["T"])
            fora.append((tipo, chave, m, e))
    return fora, falhas


# ------------------------------------------------------------------ escrita

def _geo(e):
    return DD._geometria(e)


def aplica_dex(itens, gravar):
    """Reescreve as linhas da tabela e chama o executor de sempre."""
    t = json.load(open(DD.TABELA, encoding="utf-8"))
    por_esp = {l["especie"]: l for l in t["estaticos"]}
    for tipo, esp, m, e in itens:
        if tipo != "dex":
            continue
        l = por_esp[esp]
        l.update(mapa=m, regiao=DD.regiao_do_mapa(m), tile=list(e["T"]),
                 origem="redistribuicao_bugs3", rota_irmas=True, **_geo(e))
    # nível de toda lenda da tabela pelo lugar (Paradox não é lenda: fica)
    for l in t["estaticos"]:
        if l["mapa"] in NL.NIVEL:
            l["nivel"] = NL.nivel_no_mapa(l["mapa"])
    for l in t["presentes"]:
        if l["especie"] in ("SPECIES_ETERNATUS_ETERNAMAX", "SPECIES_ZARUDE_DADA"):
            l["nivel"] = NL.nivel_no_mapa(l["mapa"])
    if gravar:
        open(DD.TABELA, "w", encoding="utf-8").write(
            json.dumps(t, indent=2, ensure_ascii=False) + "\n")
    DD._TABELA.clear()
    saida = []
    if gravar:
        for r in DD.QUATRO:
            saida += DD.aplica_estaticos(r, True)
        saida += DD.limpa_mapas_orfaos(True)
        saida += DD.aplica_presentes(True)
        saida += DD.aplica_casos(True)
    return saida


def _tira_bloco_ls(m, ids, gravar):
    """Tira objetos e o trecho de script dos lendários de Sinnoh que saem de `m`."""
    d = _json(m)
    antes = d["object_events"]
    novos = [o for o in antes if not (o.get("origem") == LS.MARCA
             and any(o["local_id"].endswith("_" + i) for i in ids))]
    d["object_events"] = novos
    if gravar:
        open(f"{RAIZ}/data/maps/{m}/map.json", "w", encoding="utf-8").write(
            json.dumps(d, indent=2, ensure_ascii=False) + "\n")
    cam = f"{RAIZ}/data/maps/{m}/scripts.inc"
    inc = open(cam, encoding="utf-8").read()
    ficam = [L for L in LS.LENDARIOS if L["mapa"] == m and L["id"] not in ids
             and any(o.get("origem") == LS.MARCA and o["local_id"].endswith("_" + L["id"])
                     for o in novos)]
    corpo = ("\n".join([LS.INC_INI] + [LS.trecho(L) for L in ficam] + [LS.INC_FIM]) + "\n"
             if ficam else "")
    novo = LS.substitui(inc, LS.INC_INI, LS.INC_FIM, corpo)
    if gravar:
        open(cam, "w", encoding="utf-8").write(novo.rstrip("\n") + "\n")
    return len(antes) - len(novos)


def aplica_sinnoh(itens, gravar):
    saida = []
    sai = collections.defaultdict(list)
    novos_L = {}
    for tipo, lid, m, e in itens:
        if tipo != "ls":
            continue
        L = next(x for x in LS.LENDARIOS if x["id"] == lid)
        # A casa VELHA é onde o objeto está hoje no disco (a tabela do
        # lendarios_sinnoh.py já aponta para a nova).
        velho = next(os.path.basename(os.path.dirname(c)) for c in sorted(
            __import__("glob").glob(f"{RAIZ}/data/maps/*/map.json"))
            if any(o.get("origem") == LS.MARCA and o.get("local_id", "").endswith("_" + lid)
                   for o in json.load(open(c, encoding="utf-8")).get("object_events", [])))
        if velho == m:
            continue
        sai[velho].append(lid)
        L2 = dict(L, mapa=m, mapa_const=_json(m)["id"], warp=e["warp"],
                  nivel=NL.nivel_no_mapa(m), tile=e["T"])
        novos_L[lid] = (L2, e)
    for m, ids in sai.items():
        n = _tira_bloco_ls(m, ids, gravar)
        saida.append(f"{m}: {n} lendário(s) de Sinnoh saem ({', '.join(ids)})")
    for lid, (L2, e) in novos_L.items():
        m = L2["mapa"]
        d = _json(m)
        d["object_events"].append(LS.objeto(L2, e))
        cam = f"{RAIZ}/data/maps/{m}/scripts.inc"
        inc = open(cam, encoding="utf-8").read()
        corpo = "\n".join([LS.INC_INI, LS.trecho(L2), LS.INC_FIM]) + "\n"
        novo = LS.substitui(inc, LS.INC_INI, LS.INC_FIM, corpo)
        if gravar:
            open(f"{RAIZ}/data/maps/{m}/map.json", "w", encoding="utf-8").write(
                json.dumps(d, indent=2, ensure_ascii=False) + "\n")
            open(cam, "w", encoding="utf-8").write(novo.rstrip("\n") + "\n")
        saida.append(f"{m}: {lid} em {e['T']} (flag {LS.flag_de(L2)})")
    # casos do T123 dos três: mesmos ids, rota nova
    cam = LS.CASOS
    casos = json.load(open(cam, encoding="utf-8"))
    for i, L in enumerate(LS.LENDARIOS):
        if L["id"] not in novos_L:
            continue
        L2, e = novos_L[L["id"]]
        a, b = LS.casos_de(L2, e, i)
        for c in (a, b):
            for k, velho in enumerate(casos):
                if velho["id"] == c["id"]:
                    casos[k] = c
    if gravar:
        open(cam, "w", encoding="utf-8").write(
            json.dumps(casos, indent=2, ensure_ascii=False) + "\n")
    return saida, novos_L


_NIVEL_RE = re.compile(r"^(\s*(?:seteventmon|setwildbattle|givemon)\s+SPECIES_[A-Z0-9_]+\s*,\s*)(\d+)", re.M)


def aplica_niveis(gravar):
    """Todo ponto do inventário vai para o nível do lugar dele."""
    saida = []
    por_arq = collections.defaultdict(list)
    for p in INV.varre():
        alvo = NL.nivel_no_mapa(p["mapa"])
        if p["nivel"] != alvo:
            por_arq[p["arquivo"]].append((p["linha"], alvo, p))
    for arq, trocas in por_arq.items():
        cam = f"{RAIZ}/{arq}"
        linhas = open(cam, encoding="utf-8").read().split("\n")
        for n, alvo, p in trocas:
            l = linhas[n - 1]
            if p["como"] == "errante":
                novo = re.sub(r"(TryAddRoamer\(SPECIES_[A-Z0-9_]+,\s*)\d+", rf"\g<1>{alvo}", l)
            else:
                novo = _NIVEL_RE.sub(rf"\g<1>{alvo}", l)
            if novo == l:
                raise SystemExit(f"não consegui trocar o nível em {arq}:{n}: {l!r}")
            linhas[n - 1] = novo
            saida.append(f"{p['especie']} em {p['mapa']}: {p['nivel']} -> {alvo}")
        if gravar:
            open(cam, "w", encoding="utf-8").write("\n".join(linhas))
    return saida


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplica", action="store_true")
    ap.add_argument("--casos", action="store_true",
                    help="só reescreve o T357 a partir da tabela gravada")
    a = ap.parse_args()
    if a.casos:
        print(f"grava testes_criticos/357: {grava_casos()} casos")
        return
    # Idempotência: o plano é medido contra a árvore de ANTES (os bichos ainda
    # fora do destino). Depois de aplicado, replanejar enxergaria o próprio
    # trabalho como parede e devolveria outro tile; a tabela gravada é a decisão.
    t = json.load(open(DD.TABELA, encoding="utf-8"))
    ja = {l["especie"]: l["mapa"] for l in t["estaticos"]}
    if all(ja.get(e) == m for e, m in DEX.items()):
        print("redistribuição já aplicada (a tabela da Dex já aponta para os destinos); "
              "use --casos para reescrever o T357")
        return
    itens, falhas = plano()
    for f in falhas:
        print("FALHA " + f)
    for tipo, chave, m, e in itens:
        print(f"  {chave:36} -> {m:44} T={e['T']} warp {e['warp']} "
              f"rota {len(e['rota'])} pernas, nível {NL.nivel_no_mapa(m)}")
    if falhas:
        raise SystemExit(f"{len(falhas)} sem tile: pare e meça.")
    if not a.aplica:
        print(f"{len(itens)} movidos (só relato; --aplica escreve)")
        return
    for linha in aplica_sinnoh(itens, True)[0]:
        print("grava " + linha)
    for linha in aplica_dex(itens, True):
        print("grava " + linha)
    for linha in aplica_niveis(True):
        print("nível " + linha)
    json.dump([dict(tipo=t, chave=c, mapa=m, T=list(e["T"]), warp=e["warp"])
               for t, c, m, e in itens],
              open(f"{RAIZ}/dev_scripts/redistribuicao_bugs3.json", "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    print(f"grava testes_criticos/357: {grava_casos()} casos")



# ------------------------------------------------------------------ casos T357

CASOS_ROTAS = f"{RAIZ}/dev_scripts/testes_criticos/357_lendarios_redistribuidos_rotas.json"


def casos_rotas():
    """Um par por estático da Dex que mudou de casa: o jogador ANDA do warp até
    encostar no bicho (positivo) e, com a flag de HIDE acesa, escorrega pelo
    tile vazio (negativo). É a prova de emulador de que cada destino é
    alcançável a pé dentro do mapa e de que o objeto nasce onde a tabela diz.
    Os três de Sinnoh (Darkrai, Cresselia, Shaymin) ficam no T123, que já é
    deste formato."""
    t = json.load(open(DD.TABELA, encoding="utf-8"))
    por_esp = {l["especie"]: l for l in t["estaticos"]}
    fora, i = [], 1
    for esp in sorted(DEX, key=lambda e: (DEX[e], e)):
        l = por_esp[esp]
        m = l["mapa"]
        const = _json(m)["id"]
        e = dict(T=tuple(l["tile"]), warp=l["warp"], dir=l["dir"],
                 para=tuple(l["para"]), vazio=tuple(l["vazio"]),
                 porta=tuple(l["porta"]), pouso=tuple(l["pouso"]),
                 rota=[tuple(x) for x in l["rota"]])
        base = dict(flags=["FLAG_SEM_ENCONTRO_SELVAGEM"], warp=const, warp_id=e["warp"])
        extra = ""
        if m in SAFARI_LC:
            base["vars"] = {VAR_SAFARI_ZONE_STATE: 2}
            extra = (" Entrada pelo balcão do Safari (VAR_SAFARI_ZONE_STATE = 2): o "
                     "atendente sai da porta e o ON_FRAME sobe o jogador um tile antes "
                     "da rota começar.")
        if m in CENA_JA_VISTA:
            var = CENA_JA_VISTA[m]
            txt = "".join(open(c).read() for c in __import__("glob").glob(
                f"{RAIZ}/include/constants/vars*.h"))
            num = re.search(rf"#define {var}\s+(0x[0-9A-Fa-f]+)", txt).group(1)
            base.setdefault("vars", {})[num] = 1
            extra = (f" A cena de entrada do mapa já foi vista ({var} = 1), que é o "
                     "estado do jogo quando o jogador volta para caçar.")
        if m in SEM_WARP:
            extra = (" O mapa não tem warp: o warp de debug sem warp válido põe o "
                     "jogador no CENTRO do mapa, e a rota parte de lá.")
        curto = esp.replace("SPECIES_", "")
        rota = " ".join(f"{D}*{n}" if n else f"{D}(zera)" for D, n, _ in e["rota"])
        pos = LS.roteiro_de(e, True)
        neg = LS.roteiro_de(e, False)
        if m in SAFARI_LC:
            pos = pos.replace("60:NADA", "300:NADA", 1)
            neg = neg.replace("60:NADA", "300:NADA", 1)
        fora.append(dict(
            id=f"T357.{i}",
            nome=(f"{curto} MUDOU PARA {const} ({acesso_curto(m)}) E A INTERAÇÃO TRAVA O "
                  f"JOGADOR. Redistribuição dos lendários (respostas 111 e 112 do Gui, "
                  f"01/10/2026): o tile {e['T']} é o mais fundo do mapa que passa nos "
                  f"portões da busca em largura (colisão e elevação, não ilha ninguém, "
                  f"longe de warp e de NPC que anda). ROTA: {rota}, a partir do warp "
                  f"{e['warp']}; a última perna satura contra o Pokémon e para em "
                  f"{e['para']}. O A abre o msgbox de abertura e a perna de volta não "
                  f"anda.{extra} Par negativo: T357.{i + 1}."),
            roteiro=DD.sem_corrida(pos), prova=dict(mapa=const, pos=list(e["para"])),
            **json.loads(json.dumps(base))))
        nb = json.loads(json.dumps(base))
        nb["flags"].append(l["flag"])
        fora.append(dict(
            id=f"T357.{i + 1}",
            nome=(f"PAR NEGATIVO DO T357.{i}: com {l['flag']} ACESA (a flag de sempre "
                  f"do {curto}, que a redistribuição NÃO trocou) o tile {e['T']} está "
                  f"vazio e a mesma rota escorrega até {e['vazio']}."),
            roteiro=DD.sem_corrida(neg), prova=dict(mapa=const, pos=list(e["vazio"]), andou=True),
            **nb))
        i += 2
    return fora


def acesso_curto(m):
    return NL.acesso(m)


def grava_casos():
    casos = casos_rotas()
    open(CASOS_ROTAS, "w", encoding="utf-8").write(
        json.dumps(casos, indent=2, ensure_ascii=False) + "\n")
    return len(casos)


if __name__ == "__main__":
    main()
