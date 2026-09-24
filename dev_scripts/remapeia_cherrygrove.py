#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remapeamento de Cherrygrove City para o desenho do Scorched Silver (seção 2 do contrato).

A arte é o mapa `g0m10` do Pokémon Scorched Silver v1.3 (64x30), trazida byte a
byte por `copia_cidade_secundario.py --reusa-primario` para o secundário
`gTileset_CherrygroveCityCopiaSec`, sobre o NOSSO `gTileset_JohtoGeneral`. O
JOGO é nosso, e é este arquivo: cada warp, NPC e placa vai para o lugar
equivalente do desenho novo, e as duas saídas viram warp.

QUAL MAPA É A CHERRYGROVE DELES
-------------------------------
O `g0m10` é o único mapa de cidade com `secao=1` (a New Bark é a seção 0, o
`g0m9`), e liga a leste no `g0m16` e ao norte no `g0m17`, como a nossa liga na
Route29 e na Route30. As cinco portas foram casadas pela FUNÇÃO lida no
destino de cada warp na ROM:

    porta     destino no hack   o que é                          nosso warp
    (43,7)    g2m4  11x8        balcão com três objetos, o Mart  0, CherrygroveCity_Mart
    (52,7)    g2m2  14x9        balcão com escada, o Centro      1, CherrygroveCity_PokemonCenter
    (33,15)   g2m5  11x9        a casa grande do oeste           2, House1 (dois moradores)
    (47,15)   g2m0  10x9        casa de UM morador               3, House2 (o GUIDE GENT)
    (54,19)   g2m1  11x8        casa de dois moradores           4, House3 (dois moradores)

A ordem espacial também bate com a do mapa antigo (casa grande à esquerda, a do
meio, a de baixo à direita).

POR QUE AS DUAS SAÍDAS VIRAM WARP, SE A CIDADE COUBE NO SECUNDÁRIO
------------------------------------------------------------------
A cidade coube INTEIRA no secundário (tentativa 1 da seção 3.2): 233 metatiles
do autor, 374 tiles (388 desenhos distintos, 12 deles reaproveitados do nosso
primário pela forma, sem mudar cor nenhuma) e 6 paletas. O que não coube foram
os VIZINHOS, e a costura por conexão precisa deles no mesmo secundário (3.1):

- **Route30 (norte)** usa 62 metatiles do `gTileset_CherrygroveCity` antigo, e
  a Route31 mais 3. Pinados no secundário novo, as cores sobem de 64 para 105
  contra as 90 de seis paletas: NÃO CABE. E sem a Route30 no mesmo secundário,
  a faixa da cidade vista de dentro da rota é desenhada com o secundário da
  rota, ou seja, lixo.
- **Route29 (leste)** usa zero metatile de secundário, então poderia dividir o
  da cidade; mas a frente da New Bark (branch `copia-johto-newbark`) já pôs a
  Route29 no `gTileset_NewBarkTownCopiaSec`, pelo mesmo motivo do lado dela. As
  duas cidades juntas pedem 541 tiles contra 384: um secundário para as duas
  NÃO CABE. Casar índice por índice a faixa leste com o secundário da New Bark
  também não fecha: 26 de 45 metatiles da faixa têm par lá.

Então as duas saídas viram WARP com fade (a saída da seção 3.1), e as duas
conexões saem dos `map.json` dos três mapas:

- **Norte**: as cinco células da estrada do autor na linha 0 (x=35..39) viram
  `MB_NORTH_ARROW_WARP` (cópias dos metatiles do autor em vagas livres do
  secundário novo, só com o atributo trocado, zero pixel mudado). Do lado da
  Route30, as três células da estrada na linha 57 (x=24..26) viram
  `MB_SOUTH_ARROW_WARP`: cópias dos metatiles 219, 220 e 221 do primário nas
  vagas 840 a 842 do `gTileset_CherrygroveCity` antigo, que continua sendo o
  secundário da Route30, da Route31 e da Route46 e que nenhuma delas usa acima
  de 839. O render das três muda ZERO pixel.
- **Leste**: as quatro células da estrada na coluna 63 (y=14..17) viram
  `MB_EAST_ARROW_WARP`. Do lado da Route29 não há seta: o primário
  `gTileset_JohtoGeneral` está cheio (640 de 640) e o secundário da Route29 é da
  frente da New Bark. A volta é um GATILHO (`coord_event`) nas quatro células da
  coluna 0 (y=14..17), que chama `warp` para a seta da cidade; a chegada da
  cidade na Route29 é uma célula para dentro, na coluna 1, para o jogador não
  nascer em cima do gatilho. Nenhum byte de tileset nem de `map.bin` da Route29
  muda.

Uso:
    python3 dev_scripts/remapeia_cherrygrove.py            # só confere e mostra
    python3 dev_scripts/remapeia_cherrygrove.py --aplicar
"""
import argparse
import collections
import json
import os
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
MAPA = os.path.join(REPO, "data/maps/CherrygroveCity/map.json")
R29 = os.path.join(REPO, "data/maps/Route29/map.json")
R29_SCRIPTS = os.path.join(REPO, "data/maps/Route29/scripts.inc")
R30 = os.path.join(REPO, "data/maps/Route30/map.json")
R30_BLOCOS = os.path.join(REPO, "data/layouts/Route30/map.bin")
R30_LARGURA = 58
POVOA = os.path.join(REPO, "dev_scripts/povoa_cidades.json")
BLOCOS = os.path.join(REPO, "data/layouts/CherrygroveCity/map.bin")
SEC_NOVO = os.path.join(REPO, "data/tilesets/secondary/cherrygrove_city_copia_sec")
SEC_VELHO = os.path.join(REPO, "data/tilesets/secondary/cherrygrove_city")
PRI = os.path.join(REPO, "data/tilesets/primary/johto_general")
LARGURA, ALTURA = 64, 30
N_META_PRI = 640

MB_NORTE, MB_LESTE, MB_SUL = 0x64, 0x62, 0x65
MB_PORTA = {0x60, 0x69}
MB_SETA = {0x62, 0x63, 0x64, 0x65}
MB_AGUA = {0x10, 0x15}

# warp id -> (x, y). Os ids 0 a 4 NÃO mudam: os interiores apontam para eles.
WARPS = {
    0: (43, 7),    # Mart
    1: (52, 7),    # Pokémon Center
    2: (33, 15),   # House1, a casa grande do oeste
    3: (47, 15),   # House2, a do GUIDE GENT
    4: (54, 19),   # House3
}
NORTE_X = [35, 36, 37, 38, 39]           # setas da cidade na linha 0
LESTE_Y = [14, 15, 16, 17]               # setas da cidade na coluna 63
R30_X = [24, 25, 26]                     # setas da Route30 na linha 57
R30_Y = 57
R29_VOLTA_X, R29_CHEGADA_X = 0, 1        # gatilho e chegada na Route29


# ENCAIXE DE COLISÃO, declarado: o telhado da casa grande do oeste é andável por
# trás nas linhas 9 a 11 (colisão do autor), e a célula (34,11) é o metatile do
# meio do telhado, que tapa o jogador INTEIRO (achado E3 do mapas_qa). Ela ganha
# colisão; nenhum pixel muda, e o resto do telhado continua como o autor fez.
COLISAO_NOVA = [(34, 11)]


def par_norte(x):
    """Casamento das cinco células da cidade com as três da rota."""
    return {35: 24, 36: 24, 37: 25, 38: 26, 39: 26}[x]


# índice do object_event -> (x, y). A ORDEM da lista não muda (seção 1 do
# contrato: índice de objeto é estado de save).
OBJETOS = {
    0: (62, 13),   # GUIDE GENT de cenário: no canto da entrada leste, onde o autor tem o gatilho dele
    1: (17, 16),   # FISHER: na ilhota de areia do mar, como no mapa antigo
    2: (46, 18),   # BOY: o lugar do menino do autor, ao sul da casa do meio
    3: (49, 10),   # LASS que passeia: praça entre o Mart e o Centro, fora do caminho da saída norte
    4: (25, 9),    # CORSOLA na praia
    5: (26, 16),   # STARYU na praia
    6: (28, 20),   # KRABBY na ponta sul da praia
    7: (26, 8),    # CORSOLA na praia
    8: (31, 19),   # KRABBY no cantinho da praia
    9: (7, 11),    # CORSOLA na pedra do mar
    10: (6, 12),   # CORSOLA na pedra do mar
    11: (10, 24),  # CORSOLA na pedra do mar, ao sul
    12: (18, 25),  # CORSOLA na pedra do mar, ao sul
    13: (37, 3),   # SILVER: no meio do corredor da saída norte, olhando para baixo
    14: (65, 10),  # YOUNGSTER: fora da grade, como já estava (x=65 no mapa de 65)
    15: (29, 13),  # Povoa1, "the first city"
    16: (26, 12),  # Povoa2, o pescador, na beira da praia
    17: (46, 9),   # Povoa3, "The MART here", na calçada do Mart
    18: (40, 11),  # Povoa4, "ROUTE 30 goes north", ao lado da placa da cidade
}

PLACAS = {
    0: (42, 11),   # CitySign: a placa do próprio autor, no meio da cidade
}


def le_tileset(pasta):
    meta = bytearray(open(os.path.join(pasta, "metatiles.bin"), "rb").read())
    attr = bytearray(open(os.path.join(pasta, "metatile_attributes.bin"), "rb").read())
    return meta, attr


def grava_tileset(pasta, meta, attr):
    open(os.path.join(pasta, "metatiles.bin"), "wb").write(meta)
    open(os.path.join(pasta, "metatile_attributes.bin"), "wb").write(attr)


def seta_de(meta, attr, origem_meta, origem_attr, mb, livres):
    """Devolve o índice local de uma cópia de `origem` com o comportamento `mb`.

    Reaproveita a cópia se ela já existe (o script roda de novo sem duplicar)."""
    at = (origem_attr & 0xFF00) | mb
    n = len(attr) // 2
    for i in range(n):
        if meta[i * 16:(i + 1) * 16] == origem_meta and struct.unpack_from("<H", attr, i * 2)[0] == at:
            return i
    i = livres.pop(0)
    if i >= n:
        meta.extend(b"\0" * 16 * (i + 1 - n))
        attr.extend(b"\0" * 2 * (i + 1 - n))
    meta[i * 16:(i + 1) * 16] = origem_meta
    struct.pack_into("<H", attr, i * 2, at)
    return i


def setas_da_cidade(dados):
    """Troca as células das saídas da cidade por cópias-seta do mesmo metatile."""
    meta, attr = le_tileset(SEC_NOVO)
    palavras = [struct.unpack_from("<H", dados, i * 2)[0] for i in range(len(dados) // 2)]
    borda = open(os.path.join(REPO, "data/layouts/CherrygroveCity/border.bin"), "rb").read()
    usados = {v & 0x3FF for v in palavras} | {struct.unpack_from("<H", borda, i * 2)[0] & 0x3FF
                                                for i in range(len(borda) // 2)}
    livres = [i for i in range(384) if i + N_META_PRI not in usados and not any(meta[i * 16:(i + 1) * 16])]
    celulas = [((x, 0), MB_NORTE) for x in NORTE_X] + [((LARGURA - 1, y), MB_LESTE) for y in LESTE_Y]
    for (x, y), mb in celulas:
        v = palavras[y * LARGURA + x]
        idx = v & 0x3FF
        if idx < N_META_PRI:
            raise SystemExit("ERRO: a célula (%d,%d) é do primário" % (x, y))
        loc = idx - N_META_PRI
        a = struct.unpack_from("<H", attr, loc * 2)[0]
        if (a & 0xFF) in MB_SETA:
            continue   # já é seta
        novo = seta_de(meta, attr, bytes(meta[loc * 16:(loc + 1) * 16]), a, mb, livres)
        palavras[y * LARGURA + x] = (v & 0xFC00) | (novo + N_META_PRI)
    grava_tileset(SEC_NOVO, meta, attr)
    for x, y in COLISAO_NOVA:
        palavras[y * LARGURA + x] = (palavras[y * LARGURA + x] & ~0x0C00) | 0x0400
    return b"".join(struct.pack("<H", v) for v in palavras)


def setas_da_route30():
    meta, attr = le_tileset(SEC_VELHO)
    pmeta, pattr = le_tileset(PRI)
    dados = bytearray(open(R30_BLOCOS, "rb").read())
    n = len(attr) // 2
    livres = list(range(n, 384))
    ids = []
    for x in R30_X:
        v = struct.unpack_from("<H", dados, (R30_Y * R30_LARGURA + x) * 2)[0]
        idx = v & 0x3FF
        if idx >= N_META_PRI:
            loc = idx - N_META_PRI
            a = struct.unpack_from("<H", attr, loc * 2)[0]
            if (a & 0xFF) == MB_SUL:
                ids.append(idx)
                continue
            raise SystemExit("ERRO: (%d,%d) da Route30 já é do secundário e não é seta" % (x, R30_Y))
        origem = bytes(pmeta[idx * 16:(idx + 1) * 16])
        a = struct.unpack_from("<H", pattr, idx * 2)[0]
        novo = seta_de(meta, attr, origem, a, MB_SUL, livres) + N_META_PRI
        struct.pack_into("<H", dados, (R30_Y * R30_LARGURA + x) * 2, (v & 0xFC00) | novo)
        ids.append(novo)
    return meta, attr, dados, ids


def grade(dados):
    import copia_cidade as cc
    lado = cc.Lado("gTileset_JohtoGeneral", "gTileset_CherrygroveCityCopiaSec", 640, 640, 7)
    g = {}
    for y in range(ALTURA):
        for x in range(LARGURA):
            v = struct.unpack_from("<H", dados, (y * LARGURA + x) * 2)[0]
            comp = lado.atributo(v & 0x3FF)[0]
            g[(x, y)] = {"col": (v >> 10) & 3, "mb": comp}
    return g


def andavel(c):
    return c["col"] == 0 and c["mb"] not in MB_AGUA


def confere(mapa, dados):
    g = grade(dados)
    erros = []
    for i, w in enumerate(mapa["warp_events"]):
        c = g[(w["x"], w["y"])]
        esperado = MB_PORTA if i < 5 else MB_SETA
        if c["mb"] not in esperado:
            erros.append("warp %d em (%d,%d) não dispara (mb 0x%X)" % (i, w["x"], w["y"], c["mb"]))
    bloqueio = set()
    for i, o in enumerate(mapa["object_events"]):
        if (o["x"], o["y"]) not in g:
            continue   # o YOUNGSTER fora da grade, de propósito
        especie = "SPECIES(" in o["graphics_id"]
        if not especie and not andavel(g[(o["x"], o["y"])]):
            erros.append("objeto %d em (%d,%d) não é chão" % (i, o["x"], o["y"]))
        if especie and (o["x"], o["y"]) not in g:
            erros.append("objeto %d fora do mapa" % i)
        bloqueio.add((o["x"], o["y"]))
    ini = (WARPS[0][0], WARPS[0][1] + 1)
    vis = {ini}
    fila = collections.deque([ini])
    while fila:
        x, y = fila.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n in g and n not in vis and andavel(g[n]) and n not in bloqueio:
                vis.add(n)
                fila.append(n)
    for i in range(5):
        x, y = WARPS[i]
        if (x, y + 1) not in vis:
            erros.append("a frente da porta %d não se alcança da porta 0" % i)
    for i, w in enumerate(mapa["warp_events"][5:], 5):
        if (w["x"], w["y"]) not in vis:
            erros.append("a seta %d em (%d,%d) não se alcança" % (i, w["x"], w["y"]))
    for i, (x, y) in PLACAS.items():
        if (x, y + 1) not in vis:
            erros.append("a placa %d não se lê de baixo" % i)
    for i, o in enumerate(mapa["object_events"]):
        if o["script"] in ("0", 0):
            continue
        x, y = o["x"], o["y"]
        if not any(v in vis for v in ((x, y + 1), (x - 1, y), (x + 1, y), (x, y - 1))):
            erros.append("objeto %d com fala não tem vizinho alcançável" % i)
    # o SILVER tem de VER quem passa: o raio dele (4 para baixo) cai em chão
    s = mapa["object_events"][13]
    for d in range(1, int(s["trainer_sight_or_berry_tree_id"]) + 1):
        if (s["x"], s["y"] + d) not in vis:
            erros.append("o raio do SILVER cai fora do chão em (%d,%d)" % (s["x"], s["y"] + d))
    vis2 = {ini}
    fila = collections.deque([ini])
    while fila:
        x, y = fila.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n in g and n not in vis2 and andavel(g[n]):
                vis2.add(n)
                fila.append(n)
    ilhadas = sorted(c for c in vis2 - vis if c not in bloqueio)
    if ilhadas:
        erros.append("células ilhadas pelos objetos: %s" % ilhadas[:10])
    return erros, len(vis)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    args = ap.parse_args()
    with open(MAPA, encoding="utf-8") as f:
        mapa = json.load(f)
    with open(R29, encoding="utf-8") as f:
        r29 = json.load(f)
    with open(R30, encoding="utf-8") as f:
        r30 = json.load(f)

    dados = setas_da_cidade(open(BLOCOS, "rb").read()) if args.aplicar else open(BLOCOS, "rb").read()

    # ---- warps da cidade: 0 a 4 portas, 5 a 9 setas do norte, 10 a 13 setas do leste
    n29 = 2   # a Route29 tem os warps 0 e 1 (guarita da Route46); os novos vêm depois
    n30 = 2   # a Route30 tem os warps 0 e 1 (casa e MR. POKéMON)
    ws = mapa["warp_events"][:5]
    for i, (x, y) in WARPS.items():
        ws[i]["x"], ws[i]["y"] = x, y
    for x in NORTE_X:
        ws.append({"x": x, "y": 0, "elevation": 0, "dest_map": "MAP_ROUTE30",
                   "dest_warp_id": str(n30 + R30_X.index(par_norte(x)))})
    for k, y in enumerate(LESTE_Y):
        ws.append({"x": LARGURA - 1, "y": y, "elevation": 0, "dest_map": "MAP_ROUTE29",
                   "dest_warp_id": str(n29 + k)})
    mapa["warp_events"] = ws
    if len(mapa["object_events"]) != len(OBJETOS):
        raise SystemExit("ERRO: %d objetos no map.json e %d no remapeamento"
                         % (len(mapa["object_events"]), len(OBJETOS)))
    for i, (x, y) in OBJETOS.items():
        mapa["object_events"][i]["x"], mapa["object_events"][i]["y"] = x, y
    for i, (x, y) in PLACAS.items():
        mapa["bg_events"][i]["x"], mapa["bg_events"][i]["y"] = x, y
    mapa["connections"] = []

    # ---- Route30: setas na linha 57, sem a conexão
    volta_norte = {24: 6, 25: 7, 26: 8}   # célula da rota -> seta do meio da cidade
    r30["warp_events"] = r30["warp_events"][:n30] + [
        {"x": x, "y": R30_Y, "elevation": 0, "dest_map": "MAP_CHERRYGROVE_CITY",
         "dest_warp_id": str(volta_norte[x])} for x in R30_X]
    r30["connections"] = [c for c in r30["connections"] if c["map"] != "MAP_CHERRYGROVE_CITY"]

    # ---- Route29: chegada na coluna 1 e gatilho de volta na coluna 0, sem a conexão
    r29["warp_events"] = r29["warp_events"][:n29] + [
        {"x": R29_CHEGADA_X, "y": y, "elevation": 0, "dest_map": "MAP_CHERRYGROVE_CITY",
         "dest_warp_id": str(10 + k)} for k, y in enumerate(LESTE_Y)]
    r29["coord_events"] = [e for e in r29.get("coord_events", [])
                           if not e["script"].startswith("Route29_EventScript_VoltaCherrygrove")] + [
        {"type": "trigger", "x": R29_VOLTA_X, "y": y, "elevation": 0, "var": "VAR_TEMP_1",
         "var_value": "0", "script": "Route29_EventScript_VoltaCherrygrove%d" % k}
        for k, y in enumerate(LESTE_Y)]
    r29["connections"] = [c for c in r29["connections"] if c["map"] != "MAP_CHERRYGROVE_CITY"]

    erros, alcance = confere(mapa, dados)
    for e in erros:
        print("  ERRO:", e)
    print("células alcançáveis a pé da porta 0: %d; erros: %d" % (alcance, len(erros)))
    if erros:
        raise SystemExit(1)
    if not args.aplicar:
        return

    open(BLOCOS, "wb").write(dados)
    meta, attr, r30_dados, ids = setas_da_route30()
    grava_tileset(SEC_VELHO, meta, attr)
    open(R30_BLOCOS, "wb").write(r30_dados)
    print("setas da Route30 nos metatiles", ids)
    for caminho, doc in ((MAPA, mapa), (R29, r29), (R30, r30)):
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=2, ensure_ascii=False)
            f.write("\n")

    s = open(R29_SCRIPTS, encoding="utf-8").read()
    if "Route29_EventScript_VoltaCherrygrove0" not in s:
        bloco = ("\n@ Volta da Route29 para a CHERRYGROVE CITY (dev_scripts/remapeia_cherrygrove.py).\n"
                 "@ A cidade é cópia do Scorched Silver com secundário próprio, e a Route29 é\n"
                 "@ da New Bark: a conexão saiu e a travessia virou warp. Do lado da cidade é\n"
                 "@ seta; deste lado é gatilho, porque o primário está cheio e o secundário\n"
                 "@ não é desta frente. Um gatilho por célula, cada um para a seta da mesma linha.\n")
        for k in range(len(LESTE_Y)):
            bloco += ("\nRoute29_EventScript_VoltaCherrygrove%d::\n"
                      "\tlockall\n\twarp MAP_CHERRYGROVE_CITY, %d\n\twaitstate\n\treleaseall\n\tend\n"
                      % (k, 10 + k))
        open(R29_SCRIPTS, "w", encoding="utf-8").write(s.rstrip("\n") + "\n" + bloco)

    # o povoamento guarda posição; sem isto, `povoa_cidades.py --aplica`
    # devolveria os quatro NPCs para as coordenadas do mapa antigo.
    with open(POVOA, encoding="utf-8") as f:
        povoa = json.load(f)
    alvo = povoa["cidades"]["CherrygroveCity"]["npcs"]
    for n, i in zip(alvo, range(15, 19)):
        n["x"], n["y"] = OBJETOS[i]
    with open(POVOA, "w", encoding="utf-8") as f:
        json.dump(povoa, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("aplicado")


if __name__ == "__main__":
    main()
