#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remapeamento de Mahogany para o desenho do Scorched Silver (seção 2 do contrato).

A arte é o mapa `g0m13` do Pokémon Scorched Silver v1.3 (40x30), trazida byte a
byte por `copia_cidade_secundario.py` para o secundário
`gTileset_MahoganyTownCopiaSec`. O JOGO é nosso, e é este arquivo: cada warp,
NPC e placa vai para o lugar equivalente do desenho novo, e a saída leste passa
a ser uma GUARITA.

A NEVE VEM DO PRÓPRIO AUTOR
---------------------------
A Mahogany do Scorched Silver JÁ É NEVADA: chão branco, pinheiros com neve,
telhados brancos e `clima=4` (WEATHER_SNOW) no cabeçalho do mapa dele. A neve
que o Gui pediu em 06/09/2026 continua, e agora é arte COPIADA do hack, byte a
byte, e não a troca de paleta do `mahogany_neve.py`. O secundário antigo de
neve (`gTileset_MahoganyTownNeve`) ficou sem dono e saiu da ROM; o `map.json`
continua com `WEATHER_SNOW`.

QUAL MAPA É A MAHOGANY DELES
----------------------------
A seção 4 do hack, `g0m13`, é o único mapa de cidade com neve e o único cujas
portas levam a um ginásio de gelo. As seis portas casadas pela FUNÇÃO, lida no
destino de cada warp dele:

    porta     destino no hack   o que é                         nosso mapa
    (15,5)    g26m84            guarita com guarda               Gate_MahoganyTown_Route43
    (8,21)    g13m4             loja grande, com balcão          MahoganyTown_Shop (a loja
                                                                 da Rocket, que desce ao
                                                                 esconderijo)
    (16,21)   g14m0             ginásio de gelo, piso escorrega  MahoganyTown_Gym
    (26,21)   g5m4              Centro Pokémon                   MahoganyTown_PokemonCenter
    (28,13)   g5m7              casa                             MahoganyTown_House1
    (18,13)   g3m4              casa                             nenhum: porta FECHADA

A COSTURA
---------
A cidade coube INTEIRA no secundário (tentativa 1 da seção 3.2): 204 metatiles
do autor, 353 tiles e 6 paletas, com o nosso `gTileset_JohtoNorthEast`. A
Route42 e a Route43 passaram a usar o MESMO secundário, com os metatiles delas
pinados no mesmo índice (render delas com 0 pixel de mudança), e a faixa do
Lago da Fúria que a Route43 desenha pela conexão também ficou pinada. Oeste e
norte continuam CONEXÃO aberta, com offset recalculado:

- oeste: a estrada do autor sai nas linhas 10 a 13, e a Route42 chega nas
  linhas 6 a 9, então o offset vai de 1 para 4;
- norte: a guarita do autor ocupa as colunas 13 a 17, e a metade de cima da
  guarita na Route43 fica nas colunas 10 a 14, então o offset vai de 2 para 3.

LESTE: GUARITA, e não conexão. A Route44 divide o secundário com Blackthorn
(ESTADO 0.am, Blackthorn), então a conexão direta faria a travessia recarregar
o secundário errado (contrato 3.1). A estrada do autor sai nas linhas 14 e 15;
as duas células da borda viram seta para o leste (clones dos metatiles dele,
só com o comportamento trocado) e levam à `Gate_MahoganyTown_Route44`, molde
horizontal da `Gate_EcruteakCity_Route42` (cidade a oeste, rota a leste). Do
lado da Route44 a seta para o oeste é a vaga 97 do primário (a única vazia, e
nenhum layout a usa), clone do metatile 220 com `MB_WEST_ARROW_WARP`, em (0,15):
nem o secundário da Route44 nem o de Blackthorn mudam, e o render dela muda 0
pixel.

Uso:
    python3 dev_scripts/remapeia_mahogany.py            # só confere e mostra
    python3 dev_scripts/remapeia_mahogany.py --aplicar
"""
import argparse
import collections
import json
import os
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
MAPA = os.path.join(REPO, "data/maps/Mahoganytown/map.json")
POVOA = os.path.join(REPO, "dev_scripts/povoa_cidades.json")
BLOCOS = os.path.join(REPO, "data/layouts/Mahoganytown/map.bin")
SEC = os.path.join(REPO, "data/tilesets/secondary/mahogany_town_copia_sec")
PRI = os.path.join(REPO, "data/tilesets/primary/johto_north_east")
LARGURA, ALTURA = 40, 30
N_META_PRI = 640

MB_EAST_ARROW_WARP = 0x62
MB_WEST_ARROW_WARP = 0x63
MB_PORTA = {0x60, 0x69}
MB_SETA_LESTE = {MB_EAST_ARROW_WARP}
MB_AGUA = {0x15}

GATE = "MAP_GATE_MAHOGANY_TOWN_ROUTE44"

# warp id -> (x, y). Os ids NÃO mudam: os interiores apontam para eles.
WARPS = {
    0: (15, 5),    # Gate_MahoganyTown_Route43, a guarita do autor no alto
    1: (8, 21),    # MahoganyTown_Shop, a loja grande (desce ao esconderijo)
    2: (28, 13),   # MahoganyTown_House1, a casa do leste
    3: (16, 21),   # MahoganyTown_Gym
    4: (26, 21),   # MahoganyTown_PokemonCenter
}
# warps NOVOS, no fim da lista: as duas setas da estrada leste, para a guarita.
SETAS_LESTE = [(39, 14), (39, 15)]

# índice do object_event -> (x, y). A ORDEM da lista não muda.
OBJETOS = {
    0: (4, 20),    # velho (anda), no canto do sudoeste, fora dos corredores
    1: (6, 22),    # "Visit Grandma's shop": na frente da loja
    2: (24, 16),   # careca, no largo entre o Centro e as casas
    3: (17, 9),    # "head north to LAKE OF RAGE": ao pé da guarita norte
    4: (24, 9),    # AIPOM
    5: (26, 11),   # AIPOM
    6: (22, 23),   # AIPOM
    7: (13, 9),    # AIPOM
    8: (9, 16),    # DELIBIRD, ao lado do boneco de neve do autor
    9: (19, 9),    # Povoa1, "The mountain air" (anda): no largo do norte
    10: (10, 22),  # Povoa2, "The shop here sells souvenirs": na loja
    11: (18, 22),  # Povoa3, "The GYM freezes": na porta do ginásio
    12: (14, 8),   # Povoa4, "ROUTE 43 north": ao lado da guarita norte
    13: (23, 12),  # Povoa5
    14: (29, 16),  # Povoa6
}

# placas: índice do bg_event -> (x, y).
PLACAS = {
    0: (4, 11),    # Sign (MAHOGANY TOWN): a placa do autor na entrada oeste
    1: (21, 13),   # CandybarSign: a placa do autor no largo das casas
    2: (14, 21),   # GymSign: na fachada do ginásio, lida de baixo
}
PLACAS_NOVAS = [{"type": "sign", "x": 18, "y": 13, "elevation": 0,
                 "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
                 "script": "Common_EventScript_PortaFechada"}]

OFFSET_ROUTE42 = 4
OFFSET_ROUTE43 = 3

ROUTE44 = os.path.join(REPO, "data/maps/Route44/map.json")
ROUTE44_BIN = os.path.join(REPO, "data/layouts/Route44/map.bin")
ROUTE44_W = 78
SETA_ROTA = (0, 15)
VAGA_PRIMARIO = 97       # vazia no primário e sem uso em layout nenhum
MODELO_ROTA = 220        # a areia do meio do caminho da Route44
NEUTRALIZA = 703         # seta sul morta no alto da guarita do autor, (15,0)
# a faixa do Lago da Fúria que a Route43 desenha pela conexão (pinada na cópia)
PINO_LAGO = [662, 674, 685, 687, 752, 753, 754, 760, 761, 762, 768, 769, 770,
             820, 821, 822, 828, 829, 830]


def le_meta(pasta):
    return (bytearray(open(os.path.join(pasta, "metatiles.bin"), "rb").read()),
            bytearray(open(os.path.join(pasta, "metatile_attributes.bin"), "rb").read()))


def grade(dados=None, clones=None):
    import copia_cidade as cc
    lado = cc.Lado("gTileset_JohtoNorthEast", "gTileset_MahoganyTownCopiaSec", 640, 640, 7)
    dados = dados or open(BLOCOS, "rb").read()
    g = {}
    for y in range(ALTURA):
        for x in range(LARGURA):
            v = struct.unpack_from("<H", dados, (y * LARGURA + x) * 2)[0]
            comp = lado.atributo(v & 0x3FF)[0]
            if clones and (v & 0x3FF) in clones.values():
                comp = MB_EAST_ARROW_WARP
            g[(x, y)] = {"col": (v >> 10) & 3, "elev": v >> 12, "mb": comp, "v": v}
    return g


def andavel(c):
    return c["col"] == 0 and c["mb"] not in MB_AGUA


def setas_no_secundario(dados):
    """Clona o metatile de cada célula da borda leste para uma vaga livre do
    secundário, trocando só o comportamento para MB_EAST_ARROW_WARP. Devolve o
    map.bin novo e os metatiles/atributos novos. Mesmos 16 bytes, então o
    desenho é o mesmo pixel a pixel."""
    meta, attr = le_meta(SEC)
    usados = set()
    for i in range(len(dados) // 2):
        usados.add(struct.unpack_from("<H", dados, i * 2)[0] & 0x3FF)
    # vagas livres: metatile todo zero e sem uso em NENHUM mapa que desenha com
    # este secundário (a cidade, a Route42 e a Route43) nem na faixa pinada do
    # Lago da Fúria.
    for nome in ("Route42", "Route43"):
        d = open(os.path.join(REPO, "data/layouts", nome, "map.bin"), "rb").read()
        usados |= {struct.unpack_from("<H", d, i * 2)[0] & 0x3FF for i in range(len(d) // 2)}
    usados |= set(PINO_LAGO)
    livres = [i for i in range(384)
              if meta[i * 16:(i + 1) * 16] == bytes(16) and (N_META_PRI + i) not in usados]
    novo = bytearray(dados)
    clones = {}
    for (x, y) in SETAS_LESTE:
        v = struct.unpack_from("<H", dados, (y * LARGURA + x) * 2)[0]
        idx = v & 0x3FF
        if idx not in clones:
            loc = livres.pop(0)
            meta[loc * 16:(loc + 1) * 16] = meta[(idx - N_META_PRI) * 16:(idx - N_META_PRI + 1) * 16]
            a = struct.unpack_from("<H", attr, (idx - N_META_PRI) * 2)[0]
            struct.pack_into("<H", attr, loc * 2, (a & 0xFF00) | MB_EAST_ARROW_WARP)
            clones[idx] = N_META_PRI + loc
        struct.pack_into("<H", novo, (y * LARGURA + x) * 2, (v & 0xFC00) | clones[idx])
    return novo, meta, attr, clones


def confere(mapa, dados, clones=None):
    """Provas de chão: porta em porta, seta em seta, NPC em chão, e alcance."""
    g = grade(bytes(dados), clones)
    erros = []
    for i, w in enumerate(mapa["warp_events"]):
        c = g[(w["x"], w["y"])]
        esperado = MB_SETA_LESTE if (w["x"], w["y"]) in SETAS_LESTE else MB_PORTA
        if c["mb"] not in esperado:
            erros.append("warp %d em (%d,%d) tem mb 0x%X" % (i, w["x"], w["y"], c["mb"]))
    bloqueio = set()
    for i, o in enumerate(mapa["object_events"]):
        if not andavel(g[(o["x"], o["y"])]):
            erros.append("objeto %d em (%d,%d) não é chão" % (i, o["x"], o["y"]))
        bloqueio.add((o["x"], o["y"]))
    frentes = []
    for i, w in enumerate(mapa["warp_events"]):
        x, y = w["x"], w["y"]
        if (x, y) in SETAS_LESTE:
            frentes.append((i, (x, y)))
        elif g[(x, y)]["col"] == 0:
            frentes.append((i, (x, y + 1)))    # porta sem colisão: a guarita norte
        else:
            frentes.append((i, (x, y + 1)))
    # e as saídas por conexão: a borda oeste andável (Route42)
    saidas = [("oeste", (0, y)) for y in range(ALTURA) if andavel(g[(0, y)])]

    def bfs(com_objetos):
        ini = frentes[0][1]
        vis = {ini}
        fila = collections.deque([ini])
        while fila:
            x, y = fila.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, y + dy)
                if n in g and n not in vis and andavel(g[n]) and not (com_objetos and n in bloqueio):
                    vis.add(n)
                    fila.append(n)
        return vis

    vis = bfs(True)
    for i, f in frentes:
        if f not in vis:
            erros.append("a frente do warp %d, %s, não se alcança do warp 0" % (i, f))
    if not any(p in vis for _n, p in saidas):
        erros.append("a saída oeste não se alcança")
    for i, (_x, _y) in list(PLACAS.items()) + [("fechada", (p["x"], p["y"])) for p in PLACAS_NOVAS]:
        viz = [(_x, _y + 1), (_x - 1, _y), (_x + 1, _y), (_x, _y - 1)]
        if not any(v in vis for v in viz):
            erros.append("placa %s em (%d,%d) não tem vizinho alcançável" % (i, _x, _y))
    ilhadas = sorted(c for c in bfs(False) - vis if c not in bloqueio)
    if ilhadas:
        erros.append("células ilhadas pelos objetos: %s" % ilhadas[:10])
    return erros, len(vis), [p for _n, p in saidas]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    args = ap.parse_args()
    with open(MAPA, encoding="utf-8") as f:
        mapa = json.load(f)
    dados = open(BLOCOS, "rb").read()
    ja = any((w["x"], w["y"]) in SETAS_LESTE for w in mapa["warp_events"][5:])
    if ja:
        # já aplicado: só confere o que está no repositório
        erros, alcance, saidas = confere(mapa, dados)
        for e in erros:
            print("  ERRO:", e)
        print("JÁ APLICADO. células alcançáveis a pé do warp 0: %d; saída oeste nas linhas %s; "
              "erros: %d" % (alcance, [y for _x, y in saidas], len(erros)))
        if args.aplicar or erros:
            raise SystemExit(1)
        return
    novo_bin, meta, attr, clones = setas_no_secundario(dados)
    print("setas leste: clones", {k: v for k, v in clones.items()})

    mapa["warp_events"] = mapa["warp_events"][:5]
    for i, (x, y) in WARPS.items():
        mapa["warp_events"][i]["x"], mapa["warp_events"][i]["y"] = x, y
    for (x, y) in SETAS_LESTE:
        mapa["warp_events"].append({"x": x, "y": y, "elevation": 0,
                                    "dest_map": GATE, "dest_warp_id": "0"})
    if len(mapa["object_events"]) != len(OBJETOS):
        raise SystemExit("ERRO: %d objetos no map.json e %d no remapeamento"
                         % (len(mapa["object_events"]), len(OBJETOS)))
    for i, (x, y) in OBJETOS.items():
        mapa["object_events"][i]["x"], mapa["object_events"][i]["y"] = x, y
    mapa["bg_events"] = mapa["bg_events"][:3]
    for i, (x, y) in PLACAS.items():
        mapa["bg_events"][i]["x"], mapa["bg_events"][i]["y"] = x, y
    mapa["bg_events"] += [dict(p) for p in PLACAS_NOVAS]
    conexoes = []
    for c in mapa["connections"]:
        if c["map"] == "MAP_ROUTE44":
            continue
        if c["map"] == "MAP_ROUTE42":
            c["offset"] = OFFSET_ROUTE42
        if c["map"] == "MAP_ROUTE43":
            c["offset"] = OFFSET_ROUTE43
        conexoes.append(c)
    mapa["connections"] = conexoes

    erros, alcance, saidas = confere(mapa, novo_bin, clones)
    for e in erros:
        print("  ERRO:", e)
    print("células alcançáveis a pé do warp 0: %d; saída oeste nas linhas %s; erros: %d"
          % (alcance, [y for _x, y in saidas], len(erros)))
    if erros:
        raise SystemExit(1)
    if not args.aplicar:
        return

    with open(MAPA, "w", encoding="utf-8") as f:
        json.dump(mapa, f, indent=2, ensure_ascii=False)
        f.write("\n")
    open(BLOCOS, "wb").write(novo_bin)
    # A célula (15,0), o alto do telhado da guarita do autor, vem com
    # MB_SOUTH_ARROW_WARP numa célula de colisão 1: nunca dispara, e a
    # lente_portas acusa porta ao ar livre sem warp. O metatile 703 só aparece
    # ali (nem Route42 nem Route43 o usam) e vira MB_NORMAL, camada intacta,
    # zero pixel. É o mesmo conserto do metatile 655 da Azalea (ESTADO 0.ah).
    loc = NEUTRALIZA - N_META_PRI
    a = struct.unpack_from("<H", attr, loc * 2)[0]
    if a & 0xFF == 0x65:
        struct.pack_into("<H", attr, loc * 2, a & 0xFF00)
    open(os.path.join(SEC, "metatiles.bin"), "wb").write(meta)
    open(os.path.join(SEC, "metatile_attributes.bin"), "wb").write(attr)

    for nome, alvo, off in (("Route42", "MAP_MAHOGANYTOWN", -OFFSET_ROUTE42),
                            ("Route43", "MAP_MAHOGANYTOWN", -OFFSET_ROUTE43)):
        p = os.path.join(REPO, "data/maps", nome, "map.json")
        with open(p, encoding="utf-8") as f:
            m = json.load(f)
        for c in m["connections"]:
            if c["map"] == alvo:
                c["offset"] = off
        with open(p, "w", encoding="utf-8") as f:
            json.dump(m, f, indent=2, ensure_ascii=False)
            f.write("\n")

    # Route44: sai a conexão com a Mahogany, entra a seta oeste para a guarita.
    with open(ROUTE44, encoding="utf-8") as f:
        r44 = json.load(f)
    r44["connections"] = [c for c in r44["connections"] if c["map"] != "MAP_MAHOGANYTOWN"]
    r44["warp_events"].append({"x": SETA_ROTA[0], "y": SETA_ROTA[1], "elevation": 0,
                               "dest_map": GATE, "dest_warp_id": "1"})
    with open(ROUTE44, "w", encoding="utf-8") as f:
        json.dump(r44, f, indent=2, ensure_ascii=False)
        f.write("\n")
    pm, pa = le_meta(PRI)
    if pm[VAGA_PRIMARIO * 16:(VAGA_PRIMARIO + 1) * 16] != bytes(16):
        raise SystemExit("ERRO: a vaga %d do primário não está vazia" % VAGA_PRIMARIO)
    pm[VAGA_PRIMARIO * 16:(VAGA_PRIMARIO + 1) * 16] = pm[MODELO_ROTA * 16:(MODELO_ROTA + 1) * 16]
    a = struct.unpack_from("<H", pa, MODELO_ROTA * 2)[0]
    struct.pack_into("<H", pa, VAGA_PRIMARIO * 2, (a & 0xFF00) | MB_WEST_ARROW_WARP)
    open(os.path.join(PRI, "metatiles.bin"), "wb").write(pm)
    open(os.path.join(PRI, "metatile_attributes.bin"), "wb").write(pa)
    rb = bytearray(open(ROUTE44_BIN, "rb").read())
    pos = (SETA_ROTA[1] * ROUTE44_W + SETA_ROTA[0]) * 2
    v = struct.unpack_from("<H", rb, pos)[0]
    if v & 0x3FF != MODELO_ROTA:
        raise SystemExit("ERRO: a Route44 não tem o 220 em %s" % (SETA_ROTA,))
    struct.pack_into("<H", rb, pos, (v & 0xFC00) | VAGA_PRIMARIO)
    open(ROUTE44_BIN, "wb").write(rb)

    # o povoamento guarda posição e fala; sem isto, `povoa_cidades.py --aplica`
    # devolveria os seis NPCs para as coordenadas do mapa antigo.
    with open(POVOA, encoding="utf-8") as f:
        povoa = json.load(f)
    alvo = povoa["cidades"]["Mahoganytown"]["npcs"]
    for n, i in zip(alvo, range(9, 15)):
        n["x"], n["y"] = OBJETOS[i]
    with open(POVOA, "w", encoding="utf-8") as f:
        json.dump(povoa, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("aplicado")


if __name__ == "__main__":
    main()
