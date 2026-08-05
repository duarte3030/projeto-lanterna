#!/usr/bin/env python3
"""Troca o interior emprestado de Hoenn pela planta real do ginasio de Sinnoh.

Uso:
    python3 dev_scripts/porta_ginasios_sinnoh.py            # so relata
    python3 dev_scripts/porta_ginasios_sinnoh.py --gravar   # grava os arquivos

De onde vem cada numero (medido em 05/08/2026, nao lembrado):

  Qual map_data pertence a qual ginasio: include/data/map_headers.h da decomp
  pokeplatinum da o .mapMatrixID de cada MAP_HEADER_*_GYM, e
  res/field/matrices/map_matrix_NNN.json diz qual MAP_NNN fica em cada celula.
  Interior de ginasio e matriz propria de 1 celula (32x32), menos Pastoria, que
  e 1x2 (32x64, MAP_223 em cima e MAP_224 embaixo).

  A grade de permissao em si: res/field/maps/data/map_data_NNN.bin, offset 0x10,
  0x800 bytes, u16 por tile. Formato documentado em DEMAKE-DS.md; leitura em
  dev_scripts/demake_ds.py (grade_gen4).

  Posicao de lider, treinador, placa e porta: res/field/events/events_*.json da
  mesma decomp, no MESMO sistema de coordenadas da grade (campos x e z).

  Metatile de chao e parede: contados no map.bin do ginasio de Hoenn que cada
  ginasio de Sinnoh ja usava emprestado, entao sao numeros que aquele tileset
  desenha de verdade. Mesmo metodo do esconderijo de Mahogany. A porta e 6/7 do
  gTileset_Building (primario de todos eles), conferida na ultima linha dos seis
  map.bin de ginasio de Hoenn.
"""
import json
import os
import re
import struct
import sys
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from demake_ds import grade_gen4  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAVAR = "--gravar" in sys.argv
LADO = 32

# Comportamentos (enum TileBehavior, include/constants/field/map_tile_behaviors.h).
BEH_ICE = 0x20
BEH_ALTURA_DINAMICA = 0x59          # piso que sobe/desce (Pastoria, Sunyshore)
BEH_PASTORIA = (0x56, 0x57, 0x58)   # niveis de agua do ginasio de Pastoria
BEH_WARP = (0x65, 0x67, 0x69, 0x6E)
BEH_BLOQUEIO_DIRECIONAL = (0x30, 0x31, 0x49, 0x4A)

PORTA_ESQ, PORTA_DIR = 0x3006, 0x3007   # gTileset_Building, elevacao 3, sem colisao


def andavel(bruto):
    """A ordem importa: na gen 4 quem impede de andar e o comportamento, nao o
    bit 15 (ver DEMAKE-DS.md). Piso de altura dinamica entra no estado inicial:
    com o bit ligado ele esta fechado quando o jogador entra."""
    comportamento, colisao = bruto & 0xFF, (bruto >> 15) & 1
    if comportamento in BEH_BLOQUEIO_DIRECIONAL:
        return False
    if comportamento == BEH_ALTURA_DINAMICA:
        return not colisao
    if comportamento == BEH_ICE or comportamento in BEH_PASTORIA or comportamento in BEH_WARP:
        return True
    return not colisao


def bloco(metatile, colisao, elevacao):
    return metatile | (colisao << 10) | (elevacao << 12)


def _pasta_tileset(simbolo):
    nome = simbolo.replace("gTileset_", "")
    nome = re.sub(r"(?<!^)(?=[A-Z])", "_", nome).lower()
    for camada in ("secondary", "primary"):
        caminho = os.path.join(REPO, "data/tilesets", camada, nome)
        if os.path.isdir(caminho):
            return caminho
    raise ValueError(f"tileset {simbolo} nao achado em data/tilesets")


def comportamento(tilesets, metatile):
    """MB_* de um metatile. Primario e 0..511, secundario comeca em 512."""
    if metatile >= 512:
        caminho, i = _pasta_tileset(tilesets[1]), metatile - 512
    else:
        caminho, i = _pasta_tileset(tilesets[0]), metatile
    dados = open(os.path.join(caminho, "metatile_attributes.bin"), "rb").read()
    if (i + 1) * 2 > len(dados):
        raise ValueError(f"metatile {metatile} nao existe em {caminho}")
    return struct.unpack_from("<H", dados, i * 2)[0] & 0xFF


def confere_paleta(g):
    """O chao TEM que ser MB_NORMAL.

    Isto existe porque a primeira escolha de piso para Pastoria e Snowpoint foi o
    metatile 525 do gTileset_SootopolisGym, que e o mais usado como chao naquele
    mapa e e MB_THIN_ICE: gelo que racha e derruba o jogador num andar de baixo
    que estes ginasios nao tem. "Mais usado no mapa de origem" nao prova nada
    sozinho; o atributo do tileset prova.
    """
    chao = g.paleta[0]
    mb = comportamento(g.tilesets, chao)
    if mb != 0:
        raise ValueError(f"{g.pasta}: chao {chao} tem comportamento {mb:#x}, nao MB_NORMAL")
    for parede in g.paleta[1:]:
        comportamento(g.tilesets, parede)   # so confere que existe no tileset
    if comportamento(g.tilesets, PORTA_ESQ & 0x3FF) != 0x65:   # MB_SOUTH_ARROW_WARP
        raise ValueError(f"{g.pasta}: metatile de porta sem MB_SOUTH_ARROW_WARP")


class Ginasio:
    def __init__(self, pasta, mapas, warp, fonte, tilesets, paleta, saida, objetos,
                 bg=(), layout=None, nome_layout=None):
        self.pasta = pasta
        self.mapas = mapas              # indices de map_data_NNN.bin, de cima para baixo
        self.warp = warp                # (x, z) da porta na grade do DS
        self.fonte = fonte              # layout de Hoenn de onde saiu a paleta
        self.tilesets = tilesets
        self.paleta = paleta            # (chao, topo_de_parede, face_de_parede)
        self.saida = saida              # (MAP_* da cidade, indice do warp de la)
        self.objetos = objetos          # local_id -> (x, z) na grade do DS
        self.bg = bg                    # lista de (x, z) para bg_events, na ordem
        self.layout = layout or "LAYOUT_" + "".join(
            "_" + c if c.isupper() and i else c.upper() for i, c in enumerate(pasta)).upper()
        self.nome_layout = nome_layout or pasta + "_Layout"


GINASIOS = [
    # Oreburgh: matriz 113 -> MAP_229. Roark (5,3), guia (6,23), Jonathon (4,18),
    # placas (3,23) e (7,23), porta (5,24).
    Ginasio("OreburghCity_Gym", [229], (5, 24), "RustboroCity_Gym",
            ("gTileset_Building", "gTileset_RustboroGym"), (513, 518, 526),
            ("MAP_OREBURGH_CITY", 6),
            {"LOCALID_OREBURGH_GYM_ROARK": (5, 3),
             "LOCALID_OREBURGH_GYM_GUIDE": (6, 23),
             "LOCALID_OREBURGH_GYM_VISITOR": (4, 18)},
            bg=[(3, 23)],
            layout="LAYOUT_OREBURGH_CITY_GYM", nome_layout="OreburghCity_Gym_Layout"),

    # Eterna: matriz 220 -> MAP_294. O labirinto de sebes/engrenagens da Gardenia.
    Ginasio("EternaCity_Gym", [294], (11, 27), "RustboroCity_Gym",
            ("gTileset_Building", "gTileset_RustboroGym"), (513, 518, 526),
            ("MAP_ETERNA_CITY", 1),
            {"LOCALID_ETERNA_GYM_GARDENIA": (11, 3)},
            layout="LAYOUT_ETERNA_CITY_GYM", nome_layout="EternaCity_Gym_Layout"),

    # Hearthome: o ginasio da Fantina e de quatro salas no Platinum (matrizes 222
    # a 225). Aqui cabe uma so, entao entra a sala do labirinto, MAP_232
    # (TRAINER_ROOM_2), que e a planta caracteristica. A Fantina nao mora nessa
    # sala no original (ela fica em MAP_233); a posicao dela aqui e escolha, no
    # fim do labirinto, e esta anotada como tal no relatorio.
    Ginasio("HearthomeCity_Gym", [232], (14, 22), "MossdeepCity_Gym",
            ("gTileset_Building", "gTileset_MossdeepGym"), (522, 520, 520),
            ("MAP_HEARTHOME_CITY", 4),
            {"LOCALID_FANTINA_GYM_LEADER": (14, 3)},
            layout="LAYOUT_HEARTHOME_CITY_GYM", nome_layout="HearthomeCity_Gym_Layout"),

    # Veilstone: matriz 115 -> MAP_235. O dojo em labirinto da Maylene.
    Ginasio("VeilstoneCity_Gym", [235], (12, 30), "DewfordTown_Gym",
            ("gTileset_Building", "gTileset_DewfordGym"), (521, 569, 540),
            ("MAP_VEILSTONE_CITY", 4),
            {"LOCALID_MAYLENE_GYM_LEADER": (12, 4)},
            layout="LAYOUT_VEILSTONE_CITY_GYM", nome_layout="VeilstoneCity_Gym_Layout"),

    # Pastoria: matriz 111 -> MAP_223 (z 0..31) sobre MAP_224 (z 32..63). O piso
    # de altura dinamica entra no estado em que o jogador acha o ginasio.
    Ginasio("PastoriaCity_Gym", [223, 224], (13, 42), "SootopolisCity_Gym_1F",
            ("gTileset_Building", "gTileset_SootopolisGym"), (520, 586, 594),
            ("MAP_PASTORIA_CITY", 1),
            {"LOCALID_WAKE_GYM_LEADER": (13, 4)},
            layout="LAYOUT_PASTORIA_CITY_GYM", nome_layout="PastoriaCity_Gym_Layout"),

    # Snowpoint: matriz 114 -> MAP_234. Sala de gelo. Sai do tileset de Lavaridge
    # (ginasio de lava) para o de Sootopolis, que e o ginasio de gelo que ja
    # existe no repo. Nenhuma arte nova, so troca de tileset existente.
    Ginasio("SnowpointCity_Gym", [234], (11, 28), "SootopolisCity_Gym_1F",
            ("gTileset_Building", "gTileset_SootopolisGym"), (520, 586, 594),
            ("MAP_SNOWPOINT_CITY", 0),
            {"LOCALID_CANDICE_GYM_LEADER": (11, 3)},
            layout="LAYOUT_SNOWPOINT_CITY_GYM", nome_layout="SnowpointCity_Gym_Layout"),

    # Sunyshore: tres salas no Platinum (matrizes 226 a 228). Entra a sala do
    # Volkner, MAP_298, que e a que tem a grade de esteiras e os quatro
    # treinadores. As duas salas de cima ficam de fora.
    Ginasio("SunyshoreCity_Gym", [298], (11, 25), "MauvilleCity_Gym",
            ("gTileset_Building", "gTileset_MauvilleGym"), (522, 531, 526),
            ("MAP_SUNYSHORE_CITY", 1),
            {"LOCALID_VOLKNER_GYM_LEADER": (11, 3)},
            layout="LAYOUT_SUNYSHORE_CITY_GYM", nome_layout="SunyshoreCity_Gym_Layout"),

    # Canalave NAO entra: MAP_225 e um ginasio de plataformas em varios niveis e
    # a grade 2D sai degenerada (896 de 896 tiles andaveis, Byron parado numa
    # regiao sem dado nenhum). Fica com o interior de Hoenn de proposito.
]


def converte(g):
    """Devolve (largura, altura, blocos, alcancaveis, mapeia) ou levanta erro."""
    altura_ds = LADO * len(g.mapas)
    grade = []
    for i in g.mapas:
        grade += grade_gen4(i)

    livre = [andavel(b) for b in grade]
    wx, wz = g.warp
    if not livre[wz * LADO + wx]:
        raise ValueError(f"{g.pasta}: porta ({wx},{wz}) caiu em tile bloqueado")

    alcance = {(wx, wz)}
    fila = deque([(wx, wz)])
    while fila:
        x, z = fila.popleft()
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, nz = x + dx, z + dz
            if 0 <= nx < LADO and 0 <= nz < altura_ds and (nx, nz) not in alcance \
                    and livre[nz * LADO + nx]:
                alcance.add((nx, nz))
                fila.append((nx, nz))

    xs = [p[0] for p in alcance]
    zs = [p[1] for p in alcance]
    # margem: 1 tile de parede dos lados e embaixo, 2 em cima para caber o par
    # topo+face que os interiores do pokeemerald usam.
    x0, x1 = max(0, min(xs) - 1), min(LADO - 1, max(xs) + 1)
    z0, z1 = max(0, min(zs) - 2), min(altura_ds - 1, max(zs) + 1)
    largura, alt = x1 - x0 + 1, z1 - z0 + 1

    chao, topo, face = g.paleta
    blocos = []
    for z in range(z0, z1 + 1):
        for x in range(x0, x1 + 1):
            if (x, z) in alcance:
                blocos.append(bloco(chao, 0, 3))
            else:
                # tile fora do alcance vira parede: assim a colisao do map.bin
                # bate exatamente com o que o flood fill viu, sem bolsao solto.
                abaixo = (x, z + 1) in alcance
                blocos.append(bloco(face if abaixo else topo, 1, 0))

    def mapeia(x, z):
        return x - x0, z - z0

    px, pz = mapeia(wx, wz)
    blocos[pz * largura + px] = PORTA_ESQ
    if px + 1 < largura and (wx + 1, wz) in alcance:
        blocos[pz * largura + px + 1] = PORTA_DIR

    return largura, alt, blocos, alcance, mapeia


def grava(g, largura, alt, blocos, alcance, mapeia):
    pasta = os.path.join(REPO, "data/layouts", g.pasta)
    os.makedirs(pasta, exist_ok=True)
    with open(os.path.join(pasta, "map.bin"), "wb") as f:
        f.write(struct.pack(f"<{len(blocos)}H", *blocos))
    borda = open(os.path.join(REPO, "data/layouts", g.fonte, "border.bin"), "rb").read()
    with open(os.path.join(pasta, "border.bin"), "wb") as f:
        f.write(borda)

    # layouts.json
    caminho = os.path.join(REPO, "data/layouts/layouts.json")
    doc = json.load(open(caminho))
    entrada = {
        "id": g.layout,
        "name": g.nome_layout,
        "width": largura,
        "height": alt,
        "primary_tileset": g.tilesets[0],
        "secondary_tileset": g.tilesets[1],
        "border_filepath": f"data/layouts/{g.pasta}/border.bin",
        "blockdata_filepath": f"data/layouts/{g.pasta}/map.bin",
        "layout_version": "emerald",
    }
    for i, l in enumerate(doc["layouts"]):
        if l["id"] == g.layout:
            doc["layouts"][i] = entrada
            break
    else:
        doc["layouts"].append(entrada)
    with open(caminho, "w") as f:
        json.dump(doc, f, indent=2)
        f.write("\n")

    # map.json
    caminho = os.path.join(REPO, "data/maps", g.pasta, "map.json")
    m = json.load(open(caminho))
    m["layout"] = g.layout
    wx, wz = mapeia(*g.warp)
    m["warp_events"] = [{
        "x": wx, "y": wz, "elevation": 0,
        "dest_map": g.saida[0], "dest_warp_id": str(g.saida[1]),
    }]
    for o in m["object_events"]:
        alvo = g.objetos.get(o["local_id"])
        if alvo is None:
            raise ValueError(f"{g.pasta}: objeto {o['local_id']} sem posicao nova")
        o["x"], o["y"] = mapeia(*alvo)
        o["elevation"] = 3
    novos_bg = []
    for i, (x, z) in enumerate(g.bg):
        modelo = m["bg_events"][i] if i < len(m["bg_events"]) else None
        if modelo is None:
            continue
        modelo["x"], modelo["y"] = mapeia(x, z)
        novos_bg.append(modelo)
    m["bg_events"] = novos_bg
    with open(caminho, "w") as f:
        json.dump(m, f, indent=2)
        f.write("\n")


def verifica():
    """Prova de sala destrancada, lida dos arquivos GRAVADOS, nao da conversao.

    "Converteu" nao e verificacao: o que trava o jogador e a colisao que sobrou no
    map.bin. Aqui o flood fill parte do warp do map.json, anda pelo map.bin com o
    tamanho declarado em layouts.json, e exige tile andavel colado no lider.
    """
    layouts = {l["id"]: l for l in json.load(
        open(os.path.join(REPO, "data/layouts/layouts.json")))["layouts"]}
    falhas = 0
    for g in GINASIOS:
        m = json.load(open(os.path.join(REPO, "data/maps", g.pasta, "map.json")))
        L = layouts[m["layout"]]
        largura, alt = L["width"], L["height"]
        dados = open(os.path.join(REPO, L["blockdata_filepath"]), "rb").read()
        blocos = struct.unpack(f"<{len(dados) // 2}H", dados)
        assert len(blocos) == largura * alt, f"{g.pasta}: map.bin nao bate com layouts.json"
        livre = lambda x, y: 0 <= x < largura and 0 <= y < alt and not (
            (blocos[y * largura + x] >> 10) & 3)

        w = m["warp_events"][0]
        inicio = (w["x"], w["y"])
        assert livre(*inicio), f"{g.pasta}: warp de entrada em tile bloqueado"
        vistos, fila = {inicio}, deque([inicio])
        while fila:
            x, y = fila.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if (x + dx, y + dy) not in vistos and livre(x + dx, y + dy):
                    vistos.add((x + dx, y + dy))
                    fila.append((x + dx, y + dy))
        for o in m["object_events"]:
            p = (o["x"], o["y"])
            perto = p in vistos or any(
                (p[0] + dx, p[1] + dy) in vistos for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if not perto:
                print(f"  FALHA {g.pasta}: {o['local_id']} em {p} inalcancavel do warp")
                falhas += 1
        print(f"{g.pasta:22s} {largura:3d}x{alt:<3d} tiles alcancaveis do warp: {len(vistos):4d}"
              f"   lider ok: {all((o['x'], o['y']) in vistos for o in m['object_events'])}")
    print("verificacao OK" if not falhas else f"{falhas} FALHAS")
    return falhas


def main():
    if "--verifica" in sys.argv:
        sys.exit(1 if verifica() else 0)
    for g in GINASIOS:
        confere_paleta(g)
        largura, alt, blocos, alcance, mapeia = converte(g)
        # o lider tem que ter chao livre nele ou colado nele, senao vira sala trancada
        for local_id, (x, z) in g.objetos.items():
            if (x, z) not in alcance:
                raise ValueError(f"{g.pasta}: {local_id} em ({x},{z}) nao e alcancavel da porta")
            nx, nz = mapeia(x, z)
            assert 0 <= nx < largura and 0 <= nz < alt, f"{g.pasta}: {local_id} fora do mapa"
        print(f"{g.pasta:22s} {largura:3d}x{alt:<3d} alcancaveis={len(alcance):4d} "
              f"tileset={g.tilesets[1]}")
        if GRAVAR:
            grava(g, largura, alt, blocos, alcance, mapeia)
    print("gravado" if GRAVAR else "nada gravado (use --gravar)")


if __name__ == "__main__":
    main()
