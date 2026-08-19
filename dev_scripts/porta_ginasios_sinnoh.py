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

# preenchido por verifica(), lido por demo(). Existe para o demo poder exigir que
# uma mutacao MUDE o numero, em vez de so conferir que o script nao explodiu.
ULTIMA_MEDIDA = {}


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


def andavel_plataforma(bruto):
    """Ginasio de plataformas suspensas (Canalave). Aqui a regra normal se inverte.

    Medido em map_data_225 (32x32 = 1024 tiles): 592 tiles com comportamento 0 e
    SEM colisao, 293 com 0x59 (piso de altura dinamica), 128 com colisao, 10 com
    0x6E e 1 com 0x65 (as portas/elevadores). Aplicar `andavel` da 896 de 896
    andaveis, uma sala vazia: e a leitura que fez a tentativa anterior falhar.

    A explicacao esta na altura. O ginasio do Byron e um vao com passarelas
    suspensas; o proprio Byron esta em `events_canalave_city_gym.json` com
    x=16, z=3, **y=30**, num andar que a grade 2D nao representa. Os 592 tiles
    "sem colisao" nao sao chao: sao o VAZIO entre as passarelas, que na gen 4 nao
    leva bit de colisao porque quem impede de cair e a altura, nao a grade.
    Quem e chao de verdade e o 0x59, e so ele.

    Entao aqui piso = 0x59 mais os tiles de porta/elevador, e todo o resto vira
    parede. Sobram 304 tiles de piso, 227 deles ligados a porta de entrada.
    """
    comportamento = bruto & 0xFF
    return comportamento == BEH_ALTURA_DINAMICA or comportamento in BEH_WARP


def bloco(metatile, colisao, elevacao):
    return metatile | (colisao << 10) | (elevacao << 12)


# --------------------------------------------------- append de metatile (B13)
#
# AUTORIZADO em 18/08/2026, 90 bytes. O que ele resolve: a grade do Platinum diz
# GELO em 497 tiles de Snowpoint e passagem direcional em 10 de Oreburgh e 13 de
# Snowpoint, e nos achatavamos tudo em chao e parede porque NENHUM metatile do
# par de tilesets do ginasio carrega o MB_* correspondente.
#
# A saida NAO e tileset novo: `MB_ICE` e ATRIBUTO, nao arte. O chao de Snowpoint
# pode continuar com o desenho que ja tem e ainda assim escorregar. Entao cada
# entrada aqui e um metatile NOVO no FIM do secundario que COPIA os 16 bytes de
# arte de um metatile existente e so troca o atributo.
#
# Por que append e seguro, medido e nao presumido (18/08/2026): o maior metatile
# que qualquer layout da arvore referencia com `gTileset_SootopolisGym` e 633,
# que e exatamente o ultimo existente (512+121); o proximo livre e 634. Indice
# novo no fim nao renumera nada e nenhum mapa de Hoenn enxerga o que foi
# acrescentado. Tiles graficos: ZERO, porque a arte e copiada; isso importa
# porque o sootopolis_gym esta em 496 de 512 tiles e nao teria folga para arte
# nova. Metatiles: 122 de 512, folga de 390.
#
# Custo: 16 B em metatiles.bin + 2 B em metatile_attributes.bin por entrada.
APPEND = {
    # 520 e o chao que Pastoria e Snowpoint ja usam neste tileset.
    "gTileset_SootopolisGym": [("MB_ICE", 520),
                               ("MB_IMPASSABLE_WEST_AND_EAST", 520),
                               ("MB_IMPASSABLE_SOUTH_AND_NORTH", 520)],
    # 513 e o chao de Oreburgh, Eterna e Canalave.
    "gTileset_RustboroGym": [("MB_IMPASSABLE_EAST", 513),
                             ("MB_IMPASSABLE_WEST", 513)],
}

# gen 4 -> MB_* do GBA, so o que o append passou a saber desenhar.
GELO_G4 = 0x20
DIRECIONAL_G4 = {0x30: "MB_IMPASSABLE_EAST", 0x31: "MB_IMPASSABLE_WEST",
                 0x49: "MB_IMPASSABLE_SOUTH_AND_NORTH",
                 0x4A: "MB_IMPASSABLE_WEST_AND_EAST"}


def aplica_append(gravar=False):
    """{(tileset, MB_*): metatile}. Idempotente: reusa o que ja esta gravado."""
    mb = _mb_por_nome()
    saida = {}
    for ts, pedidos in APPEND.items():
        pasta = _pasta_tileset(ts)
        arte = bytearray(open(os.path.join(pasta, "metatiles.bin"), "rb").read())
        attr = bytearray(open(os.path.join(pasta, "metatile_attributes.bin"), "rb").read())
        assert len(arte) // 16 == len(attr) // 2, f"{ts}: arte e atributo descasados"
        mudou = False
        for nome, modelo in pedidos:
            alvo, molde = mb[nome], arte[(modelo - 512) * 16:(modelo - 512 + 1) * 16]
            # ja existe? (mesmo atributo E mesma arte). E isto que faz rodar duas
            # vezes nao acrescentar duas vezes.
            achado = next(
                (512 + i for i in range(len(attr) // 2)
                 if struct.unpack_from("<H", attr, i * 2)[0] & 0xFF == alvo
                 and arte[i * 16:(i + 1) * 16] == molde), None)
            if achado is None:
                achado = 512 + len(attr) // 2
                assert achado - 512 < 512, f"{ts}: estourou o teto de 512 metatiles"
                arte += molde
                attr += struct.pack("<H", alvo)
                mudou = True
            saida[(ts, nome)] = achado
        if mudou and gravar:
            open(os.path.join(pasta, "metatiles.bin"), "wb").write(arte)
            open(os.path.join(pasta, "metatile_attributes.bin"), "wb").write(attr)
    return saida


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
                 bg=(), layout=None, nome_layout=None, piso=andavel, porta_dupla=False):
        self.piso = piso                # predicado de "isto e chao"
        self.porta_dupla = porta_dupla  # forca a metade direita da porta
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
            # So o lider. O guia (6,23) e o visitante (4,18) SAIRAM em 18/08/2026,
            # e a razao vale para qualquer ginasio: os dois eventos da fonte que
            # eles copiavam ja tinham sido trazidos pelo importador de NPC, entao
            # cada um existia DUAS vezes no mapa. O visitante era pior: ele e o
            # mesmo evento (4,18) que virou `YoungsterJonathon`, e o Jonathon
            # carrega batalha (`trainerbattle_single TRAINER_SINNOH_YOUNGSTER_
            # JONATHON`) enquanto o visitante so tinha um msgbox. Ficou quem
            # carrega mais. O conserto de coordenada do corte empilhava os dois
            # exatamente no mesmo tile, que foi como a duplicata apareceu.
            # Conferido antes de apagar: nenhum script aponta para
            # LOCALID_OREBURGH_GYM_VISITOR (o `#define` daquele header e GERADO
            # pelo mapjson a partir do indice, entao ele se refaz sozinho), e o
            # ginasio nao tem applymovement nem setobjectxy, logo id implicito
            # de objeto nao e referencia de ninguem.
            {"LOCALID_OREBURGH_GYM_ROARK": (5, 3)},
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

    # Canalave: matriz 112 -> MAP_225. Achatado de proposito, com o piso invertido
    # (ver `andavel_plataforma`): as passarelas de 0x59 sao o chao, o vao entre
    # elas vira parede. Byron NAO cabe onde o Platinum o poe (x=16, z=3, y=30, um
    # andar que a grade 2D nao tem), entao a posicao dele aqui e ESCOLHA, como a
    # da Fantina: o ponto mais distante da porta medido por flood fill, (26,12),
    # a 41 passos, que e a ponta da passarela da direita.
    Ginasio("CanalaveCity_Gym", [225], (16, 27), "RustboroCity_Gym",
            ("gTileset_Building", "gTileset_RustboroGym"), (513, 518, 526),
            ("MAP_CANALAVE_CITY", 1),
            {"LOCALID_BYRON_GYM_LEADER": (26, 12)},
            layout="LAYOUT_CANALAVE_CITY_GYM", nome_layout="CanalaveCity_Gym_Layout",
            piso=andavel_plataforma, porta_dupla=True),
]


def converte(g):
    """Devolve (largura, altura, blocos, alcancaveis, mapeia) ou levanta erro."""
    altura_ds = LADO * len(g.mapas)
    grade = []
    for i in g.mapas:
        grade += grade_gen4(i)

    livre = [g.piso(b) for b in grade]
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

    # Tile de passagem DIRECIONAL: na gen 4 e tile que so deixa passar num eixo
    # (a lateral das plataformas de Oreburgh, os obstaculos do gelo de
    # Snowpoint). O flood fill acima o trata como parede, e ate 18/08/2026 ele
    # SAIA como parede. Com o append ele volta a ser piso com restricao. Entra
    # so o que encosta na area alcancavel, para nao criar ilha dentro da parede.
    tem = aplica_append()
    direcional = {}
    for z in range(altura_ds):
        for x in range(LADO):
            mb = DIRECIONAL_G4.get(grade[z * LADO + x] & 0xFF)
            if not mb or (x, z) in alcance:
                continue
            if (g.tilesets[1], mb) in tem and any(
                    (x + dx, z + dz) in alcance
                    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                direcional[(x, z)] = tem[(g.tilesets[1], mb)]

    xs = [p[0] for p in alcance | set(direcional)]
    zs = [p[1] for p in alcance | set(direcional)]
    # margem: 1 tile de parede dos lados e embaixo, 2 em cima para caber o par
    # topo+face que os interiores do pokeemerald usam.
    x0, x1 = max(0, min(xs) - 1), min(LADO - 1, max(xs) + 1)
    z0, z1 = max(0, min(zs) - 2), min(altura_ds - 1, max(zs) + 1)
    largura, alt = x1 - x0 + 1, z1 - z0 + 1

    chao, topo, face = g.paleta
    gelo = tem.get((g.tilesets[1], "MB_ICE"))
    blocos = []
    for z in range(z0, z1 + 1):
        for x in range(x0, x1 + 1):
            if (x, z) in direcional:
                blocos.append(bloco(direcional[(x, z)], 0, 3))
            elif (x, z) in alcance:
                # GELO: mesmo desenho do chao, atributo MB_ICE. E o unico lugar
                # onde o metatile emitido nao e `chao`, e sai da FONTE, tile a
                # tile, nao de escolha.
                ehgelo = gelo is not None and grade[z * LADO + x] & 0xFF == GELO_G4
                blocos.append(bloco(gelo if ehgelo else chao, 0, 3))
            else:
                # tile fora do alcance vira parede: assim a colisao do map.bin
                # bate exatamente com o que o flood fill viu, sem bolsao solto.
                abaixo = (x, z + 1) in alcance or (x, z + 1) in direcional
                blocos.append(bloco(face if abaixo else topo, 1, 0))

    def mapeia(x, z):
        return x - x0, z - z0

    px, pz = mapeia(wx, wz)
    blocos[pz * largura + px] = PORTA_ESQ
    if px + 1 < largura and ((wx + 1, wz) in alcance or g.porta_dupla):
        blocos[pz * largura + px + 1] = PORTA_DIR

    return largura, alt, blocos, alcance | set(direcional), mapeia


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


def _modelo(g, m, blocos, largura, alt):
    """(passo, livre, comp_em) do MOTOR, lidos dos arquivos gravados.

    Um lugar so, porque `verifica()` e o conserto de NPC precisam da MESMA regra;
    duas copias divergiriam no dia em que uma fosse ajustada, e o preco seria NPC
    movido para tile que a verificacao considera bom e o jogo nao.

      - gelo: pisou em MB_ICE, `ForcedMovement_Slip` repete o passo na mesma
        direcao enquanto o tile SOB o jogador for gelo
        (`src/field_player_avatar.c`).
      - direcional: `IsMetatileDirectionallyImpassable` barra se a origem bloqueia
        o sentido ou o destino bloqueia o oposto (`src/event_object_movement.c`).
      - NPC e SOLIDO (`DoesObjectCollideWithObjectAt`), e no gelo isso nao e
        detalhe: escorregar contra um treinador PARA o jogador no tile de antes,
        ou seja cada NPC CRIA um ponto de parada colado nele mesmo.
    """
    mb = _mb_por_nome()
    cache = {}

    def comp_em(x, y):
        mt = blocos[y * largura + x] & 0x3FF
        if mt not in cache:
            cache[mt] = comportamento(g.tilesets, mt)
        return cache[mt]

    solidos = {(o["x"], o["y"]) for o in m["object_events"]}

    def livre(x, y):
        return (0 <= x < largura and 0 <= y < alt
                and not ((blocos[y * largura + x] >> 10) & 3)
                and (x, y) not in solidos)

    def barra(x, y, dx, dy, saindo):
        b = comp_em(x, y)
        n = {mb["MB_IMPASSABLE_NORTH"], mb["MB_IMPASSABLE_SOUTH_AND_NORTH"]}
        s = {mb["MB_IMPASSABLE_SOUTH"], mb["MB_IMPASSABLE_SOUTH_AND_NORTH"]}
        e = {mb["MB_IMPASSABLE_EAST"], mb["MB_IMPASSABLE_WEST_AND_EAST"]}
        w = {mb["MB_IMPASSABLE_WEST"], mb["MB_IMPASSABLE_WEST_AND_EAST"]}
        if not saindo:
            dx, dy = -dx, -dy              # o destino barra o sentido OPOSTO
        return b in (s if dy > 0 else n if dy < 0 else e if dx > 0 else w)

    def passo(p, d):
        """Onde o jogador PARA saindo de p no sentido d. p se nao sair."""
        dx, dy = d
        q = (p[0] + dx, p[1] + dy)
        if not livre(*q) or barra(*p, dx, dy, True) or barra(*q, dx, dy, False):
            return p
        while comp_em(*q) == mb["MB_ICE"]:
            r = (q[0] + dx, q[1] + dy)
            if not livre(*r) or barra(*q, dx, dy, True) or barra(*r, dx, dy, False):
                break
            q = r
        return q

    return passo, livre, comp_em


def _paradas(g, m, blocos, largura, alt):
    """Tiles em que o jogador consegue FICAR DE PE, partindo do warp de entrada.

    O destino de um NPC movido tem que estar aqui. `livre` nao basta: no gelo ha
    531 tiles andaveis para 88 paradas em Snowpoint, e um NPC posto num tile de
    passagem e um NPC com quem ninguem consegue falar. Repare que o proprio NPC
    conta como solido em `_modelo`, entao esta medida e o mundo COM ele parado
    onde esta hoje: e conservadora de proposito.
    """
    passo, livre, _ = _modelo(g, m, blocos, largura, alt)
    ini = (m["warp_events"][0]["x"], m["warp_events"][0]["y"])
    vistos, fila = {ini}, deque([ini])
    while fila:
        p = fila.popleft()
        for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = passo(p, d)
            if q not in vistos:
                vistos.add(q)
                fila.append(q)
    # um NPC nao fica EM cima de tile de parada: ele fica colado nele. Vale como
    # destino todo tile andavel com pelo menos uma parada ortogonal.
    return {(x, y) for x in range(largura) for y in range(alt)
            if any((x + dx, y + dy) in vistos for dx, dy in
                   ((1, 0), (-1, 0), (0, 1), (0, -1)))}


def verifica():
    """Prova de sala destrancada, lida dos arquivos GRAVADOS, nao da conversao.

    "Converteu" nao e verificacao: o que trava o jogador e a colisao que sobrou no
    map.bin. Aqui o flood fill parte do warp do map.json, anda pelo map.bin com o
    tamanho declarado em layouts.json, e exige tile andavel colado no lider.

    Desde 18/08/2026 o passo NAO e mais "um tile na direcao d". O append de
    `MB_ICE` poe deslize no jogo, e colisao livre deixou de significar que da
    para PARAR ali: em Snowpoint 531 tiles sao andaveis e so 72 sao lugares onde
    o jogador consegue ficar de pe. Verificar com o passo antigo daria verde num
    ginasio intransponivel. O modelo abaixo e o do motor, lido em
    `src/field_player_avatar.c` e `src/event_object_movement.c`:

      - pisou em MB_ICE: `GetForcedMovementByMetatileBehavior` devolve
        `ForcedMovement_Slip`, que repete o passo na MESMA direcao enquanto o
        tile SOB o jogador for gelo. Ele para no primeiro tile que nao e gelo,
        ou no ultimo gelo antes de uma colisao.
      - passagem direcional: `IsMetatileDirectionallyImpassable` barra o passo se
        o tile de ORIGEM bloqueia aquele sentido ou o de DESTINO bloqueia o
        sentido oposto. Sao as duas tabelas `g*DirectionBlockedMetatileFuncs`.

    E verifica tambem o que so aparece com deslize: TILE-ARMADILHA, o tile em que
    da para entrar e do qual nao da para voltar a porta. Sem esse portao um
    quebra-cabeca de gelo pode passar com o lider alcancavel e mesmo assim
    prender o jogador num canto para sempre.
    """
    layouts = {l["id"]: l for l in json.load(
        open(os.path.join(REPO, "data/layouts/layouts.json")))["layouts"]}
    mb = _mb_por_nome()
    falhas = 0
    for g in GINASIOS:
        m = json.load(open(os.path.join(REPO, "data/maps", g.pasta, "map.json")))
        L = layouts[m["layout"]]
        largura, alt = L["width"], L["height"]
        dados = open(os.path.join(REPO, L["blockdata_filepath"]), "rb").read()
        blocos = struct.unpack(f"<{len(dados) // 2}H", dados)
        assert len(blocos) == largura * alt, f"{g.pasta}: map.bin nao bate com layouts.json"

        passo, livre, comp_em = _modelo(g, m, blocos, largura, alt)

        def alcance_de(ini):
            """Onde o jogador consegue FICAR DE PE. No gelo isso e muito menos do
            que os tiles andaveis: em Snowpoint sao 88 de 531."""
            vistos, fila = {ini}, deque([ini])
            while fila:
                p = fila.popleft()
                for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    q = passo(p, d)
                    if q not in vistos:
                        vistos.add(q)
                        fila.append(q)
            return vistos

        w = m["warp_events"][0]
        inicio = (w["x"], w["y"])
        assert livre(*inicio), f"{g.pasta}: warp de entrada em tile bloqueado"
        vistos = alcance_de(inicio)
        # Duas reguas, porque ha dois jeitos de um NPC valer no jogo: CONVERSA
        # (lider, guia) exige tile de parada colado nele; VISTA (treinador) aceita
        # tambem que o tile vigiado seja uma PARADA, porque o jogador que para ali
        # e visto mesmo tendo chegado deslizando. Isso nao e deducao: o T115.4
        # entra em Snowpoint, desliza ate parar em (4,5) e a batalha da Alicia
        # abre, lida em gParties[OPPONENT][0].
        #
        # O que NAO entra na regua: aceitar que o tile vigiado seja apenas PISADO
        # de passagem no meio de um deslize. E plausivel e nao foi provado no
        # emulador, entao fica de fora; com a regra estrita os 6 treinadores de
        # Snowpoint passam, ou seja o afrouxamento nao compraria nada e so
        # esconderia treinador morto.
        frente = {"MOVEMENT_TYPE_FACE_DOWN": (0, 1), "MOVEMENT_TYPE_FACE_UP": (0, -1),
                  "MOVEMENT_TYPE_FACE_LEFT": (-1, 0), "MOVEMENT_TYPE_FACE_RIGHT": (1, 0)}
        for o in m["object_events"]:
            p = (o["x"], o["y"])
            colado = p in vistos or any(
                (p[0] + dx, p[1] + dy) in vistos for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            d = frente.get(o["movement_type"])
            if o["trainer_type"] == "TRAINER_TYPE_NORMAL" and d:
                vista = int(o["trainer_sight_or_berry_tree_id"] or 0) or 1
                ok = colado or any((p[0] + d[0] * i, p[1] + d[1] * i) in vistos
                                   for i in range(1, vista + 1))
                como = "parada colada nem parada na linha de vista"
            else:
                ok, como = colado, "tile de parada colado"
            if not ok:
                # FALHA DURA, inclusive para treinador. Isto foi AVISO por
                # algumas horas em 18/08/2026, enquanto o unico caso conhecido
                # (a Alicia de Snowpoint) morava em map.json de outro executor.
                # Assim que o arquivo liberou, o caso foi consertado e a regua
                # endureceu: treinador de ginasio que o jogador nunca consegue
                # enfrentar e defeito de JOGO, nao ruido de verificador, e quem
                # mexer em gelo ou em posicao de NPC tem que descobrir na hora.
                print(f"  FALHA {g.pasta}: {o.get('local_id', o['graphics_id'])} "
                      f"em {p} sem {como} a partir do warp")
                falhas += 1
        # DUPLICATA DA MESMA PESSOA DA FONTE. O criterio e o EVENTO DA FONTE e
        # nao o nome nosso, porque foi exatamente isso que deixou a duplicata de
        # Oreburgh passar despercebida por semanas: `LOCALID_OREBURGH_GYM_VISITOR`
        # e `YoungsterJonathon` sao nomes diferentes para o evento (4,18) do
        # Platinum. Enquanto os dois estavam desalinhados em 1 tile ninguem via;
        # o conserto do corte os empilhou e a duplicata apareceu.
        h = _header_da_fonte(g.pasta)
        fonte = _par_da_fonte(h) if h else []
        if fonte:
            mapeia = converte(g)[4]
            de_quem = {}
            for o in m["object_events"]:
                par = _casa(o, fonte, mapeia)
                if par is None:
                    continue
                if par in de_quem:
                    print(f"  FALHA {g.pasta}: {de_quem[par]} e "
                          f"{o.get('local_id', o['graphics_id'])} sao o MESMO evento "
                          f"{par} da fonte, duplicado")
                    falhas += 1
                de_quem[par] = o.get("local_id", o["graphics_id"])

        presos = [p for p in vistos if inicio not in alcance_de(p)]
        if presos:
            print(f"  FALHA {g.pasta}: {len(presos)} tile-armadilha (entra e nao "
                  f"volta a porta), ex.: {sorted(presos)[:5]}")
            falhas += 1
        gelo = sum(1 for i, b in enumerate(blocos)
                   if comp_em(i % largura, i // largura) == mb["MB_ICE"])
        andaveis = sum(1 for i in range(len(blocos)) if livre(i % largura, i // largura))
        ULTIMA_MEDIDA[g.pasta] = {"paradas": len(vistos),
                                  "gelo": gelo, "andaveis": andaveis,
                                  "armadilha": len(presos)}
        print(f"{g.pasta:22s} {largura:3d}x{alt:<3d} paradas alcancaveis do warp: "
              f"{len(vistos):4d}   gelo: {gelo:3d}   armadilha: {len(presos)}")
    print("verificacao OK" if not falhas else f"{falhas} FALHAS")
    return falhas


# ------------------------------------------------------------- censo de arte
#
# Por que este censo existe (18/08/2026). A regua de ARTE do completude.py acusa
# estes 8 ginasios como os piores mapas de Sinnoh (4 a 5 metatiles distintos).
# A acusacao esta certa no numero e ERRADA na conclusao: nao ha desenho para
# recuperar. A fonte de Sinnoh e a decomp pokeplatinum, e o que ela guarda em 2D
# e `res/field/maps/data/map_data_NNN.bin`, uma grade 32x32 de COLISAO e
# COMPORTAMENTO. A arte do ginasio e o NSBMD 3D do mesmo arquivo, que a grade nao
# carrega. Medido: dentro da area alcancavel os 8 ginasios tem de 2 a 6
# comportamentos distintos, e nos ja emitimos de 4 a 5 metatiles. Ou seja, ja
# emitimos MAIS do que a fonte sabe dizer.
#
# Isto NAO e o buraco de Unova. La o `.ablk` guardava 30 a 283 blocos de desenho
# e a conversao emitia 3: informacao existia e foi jogada fora. Aqui nao existe.
# Conferido tambem na segunda fonte: `fontes-mapas/sinnoh` (demake gen 3) tem
# LAYOUT_OREBURGH_CITY_GYM com 54 metatiles, e ele e byte a byte o
# RustboroCity_Gym de Hoenn (md5 d511ef095521d8a44c1f41072e83320e nos dois).
# Nao e arte de Sinnoh, e emprestimo de Hoenn.
#
# O que sobra de honesto e o comportamento que a grade tem e nos achatamos em
# chao. Este censo mede exatamente isso, e o resultado e que quase nada e
# mapeavel HOJE: o metatile com o MB_* certo nao existe no par de tilesets do
# ginasio. Rodar `--censo` diz, linha a linha, o que da e o que nao da e por que.

# gen 4 -> MB_* do GBA que diz a MESMA coisa. So entra contrapartida de verdade;
# comportamento fora desta tabela esta em SEM_EQUIVALENTE, com o motivo escrito.
EQUIVALE = {
    0x20: "MB_ICE",                        # ICE (escorrega)
    0x30: "MB_IMPASSABLE_EAST",            # BLOCK_EASTWARD
    0x31: "MB_IMPASSABLE_WEST",            # BLOCK_WESTWARD
    0x49: "MB_IMPASSABLE_SOUTH_AND_NORTH",  # BLOCK_NORTH_AND_SOUTH
    0x4A: "MB_IMPASSABLE_WEST_AND_EAST",   # BLOCK_EAST_AND_WEST
    0x65: "MB_SOUTH_ARROW_WARP",           # WARP_ENTRANCE_SOUTH (a porta)
    0x69: "MB_NON_ANIMATED_DOOR",          # DOOR
    0x6E: "MB_NORTH_ARROW_WARP",           # WARP_NORTH (elevador)
}

SEM_EQUIVALENTE = {
    0x59: ("piso que sobe e desce por interruptor; o GBA nao tem esse motor. O "
           "estado em que o jogador acha o ginasio E chao, e chao ja e o que "
           "emitimos: nada foi perdido"),
    0x56: "nivel ALTO de agua do ginasio de Pastoria; sem motor de nivel no GBA",
    0x57: "nivel MEDIO de agua do ginasio de Pastoria; idem",
    0x58: "nivel BAIXO de agua do ginasio de Pastoria; idem",
}

# Comportamento que so vira tile util se existir um warp_event apontando para
# ele. Criar warp e FRONTEIRA: blockdata novo nao mexe em warp (lei da casa), e
# tile de warp sem evento e porta que nao abre.
PRECISA_DE_WARP = (0x69, 0x6E)


def _mb_por_nome():
    v, tabela = -1, {}
    for linha in open(os.path.join(REPO, "include/constants/metatile_behaviors.h")):
        m = re.match(r"\s*(MB_\w+)\s*(?:=\s*(0x[0-9A-Fa-f]+|\d+))?\s*,?\s*$",
                     linha.split("//")[0])
        if not m:
            continue
        v = int(m.group(2), 0) if m.group(2) else v + 1
        tabela[m.group(1)] = v
    return tabela


def _mb_disponiveis(tilesets):
    """{MB_*: [metatiles do par que o carregam]}. Primario 0.., secundario 512.."""
    nome = {v: k for k, v in _mb_por_nome().items()}
    achado = {}
    for camada, base in ((0, 0), (1, 512)):
        caminho = os.path.join(_pasta_tileset(tilesets[camada]),
                               "metatile_attributes.bin")
        dados = open(caminho, "rb").read()
        for i in range(len(dados) // 2):
            b = struct.unpack_from("<H", dados, i * 2)[0] & 0xFF
            if b:
                achado.setdefault(nome.get(b, hex(b)), []).append(base + i)
    return achado


def censo():
    """Comportamento que a FONTE tem e nos achatamos, e se da para emitir hoje."""
    from collections import Counter
    print("Censo de arte dos ginasios de Sinnoh. A fonte e grade de colisao e\n"
          "comportamento (pokeplatinum, map_data_NNN.bin): ela NAO tem desenho 2D.\n")
    mapeavel = bloqueado = 0
    for g in GINASIOS:
        grade = []
        for i in g.mapas:
            grade += grade_gen4(i)
        tem = _mb_disponiveis(g.tilesets)
        caminho = os.path.join(_pasta_tileset(g.tilesets[1]), "metatile_attributes.bin")
        n_sec = os.path.getsize(caminho) // 2
        distintos = len({(b & 0x3FF) for b in struct.unpack(
            f"<{os.path.getsize(os.path.join(REPO, 'data/layouts', g.pasta, 'map.bin')) // 2}H",
            open(os.path.join(REPO, "data/layouts", g.pasta, "map.bin"), "rb").read())})
        print(f"== {g.pasta}  arte={distintos} metatiles  "
              f"{g.tilesets[1]} ({n_sec}/512 metatiles usados)")
        beh = Counter(v & 0xFF for v in grade)
        for b, n in sorted(beh.items(), key=lambda kv: -kv[1]):
            if b == 0:
                continue
            if b in SEM_EQUIVALENTE:
                print(f"   0x{b:02X} x{n:<4d} sem equivalente no GBA: {SEM_EQUIVALENTE[b]}")
                continue
            mb = EQUIVALE.get(b)
            if mb is None:
                print(f"   0x{b:02X} x{n:<4d} NAO CATALOGADO, ver o enum da fonte")
                continue
            onde = tem.get(mb)
            if not onde:
                print(f"   0x{b:02X} x{n:<4d} -> {mb}: NENHUM metatile do par tem "
                      f"esse atributo. So com append no tileset")
                bloqueado += 1
            elif b in PRECISA_DE_WARP:
                print(f"   0x{b:02X} x{n:<4d} -> {mb} em {onde}: existe, mas so "
                      f"funciona com warp_event novo, que e fronteira")
                bloqueado += 1
            else:
                print(f"   0x{b:02X} x{n:<4d} -> {mb} em {onde}: JA EMITIDO")
                mapeavel += 1
    print(f"\n{mapeavel} comportamentos ja emitidos, {bloqueado} bloqueados hoje.")
    # A invariante que este censo existe para segurar: a porta de todo ginasio
    # tem que ter MB_SOUTH_ARROW_WARP no par, senao a sala fica trancada.
    for g in GINASIOS:
        assert PORTA_ESQ & 0x3FF in _mb_disponiveis(g.tilesets)["MB_SOUTH_ARROW_WARP"], \
            f"{g.pasta}: metatile de porta sem MB_SOUTH_ARROW_WARP"
    # INVARIANTE QUE VIROU DE LADO EM 18/08/2026, e o comentario existe para o
    # proximo executor nao achar que quebrou. Ate a manha deste dia a linha era
    # `assert "MB_ICE" not in ...`, e ela documentava POR QUE o gelo de Snowpoint
    # nao tinha entrado: nenhum metatile do par carregava o atributo. O append de
    # 90 bytes (ver APPEND) resolveu isso, entao a asserção passou a ser a
    # INVERSA: o gelo tem que ESTAR la, senao os 497 tiles de Snowpoint voltam a
    # sair como chao comum, calados.
    snow = next(g for g in GINASIOS if g.pasta == "SnowpointCity_Gym")
    assert "MB_ICE" in _mb_disponiveis(snow.tilesets), \
        "MB_ICE sumiu do par de Snowpoint: o append foi revertido e o gelo morreu"
    oreb = next(g for g in GINASIOS if g.pasta == "OreburghCity_Gym")
    assert "MB_IMPASSABLE_EAST" in _mb_disponiveis(oreb.tilesets), \
        "as passagens direcionais de Oreburgh sumiram do RustboroGym"
    return 0


# ------------------------------------------------------- retratacao (18/08/2026)
#
# Este relatorio ja circulou com um numero errado meu, e ele fica escrito aqui
# para nao voltar a circular. Eu contei `TILE_BEHAVIOR_DYNAMIC_HEIGHT_COLLISION`
# (0x59) como PERDA: 445 tiles em Pastoria, 293 em Canalave e 146 em Sunyshore
# que "achatamos em chao". ERRADO, e medido depois: 0x59 e piso que sobe e desce
# por interruptor, e o estado em que o jogador ACHA o ginasio E chao. Chao e
# exatamente o que emitimos. Nao havia perda nenhuma, e nao ha nada a recuperar
# ali sem inventar um segundo metatile de piso, que seria decisao de desenho e
# nao conversao. O mesmo vale para os niveis de agua de Pastoria (0x56/57/58):
# sem motor de nivel no GBA, nao ha contrapartida honesta.
#
# TEXTO APROVADO para o ESTADO.md (guardado aqui para sobreviver caso ninguem
# costure hoje; quem costurar, copie daqui):
#
#   Os 104 mapas de Sinnoh abaixo do piso de arte NAO sao 104 defeitos. Medido em
#   18/08/2026: 62 de caverna e masmorra (8 a 9 metatiles), 25 de ruina Unown e
#   do Underground (6 a 7), 9 do Old Chateau (6 a 9) e OITO de ginasio (4 a 5).
#   A causa e a fonte: Sinnoh sai da decomp pokeplatinum, e o que ela guarda em
#   2D e uma grade 32x32 de COLISAO e COMPORTAMENTO. A arte do mapa e o NSBMD 3D
#   do mesmo arquivo, que a grade nao carrega. Nao existe desenho 2D na fonte de
#   Sinnoh para converter.
#
#   Isto NAO e o buraco de Unova. La o .ablk guardava de 30 a 283 blocos de
#   desenho e a conversao emitia 3: a informacao existia e foi jogada fora. Aqui
#   ela nao existe. Dentro da area alcancavel os 8 ginasios tem de 2 a 6
#   comportamentos distintos na fonte e nos emitimos de 4 a 5 metatiles, ou seja
#   ja emitimos MAIS do que a fonte sabe dizer. EternaCity_Gym e
#   VeilstoneCity_Gym tem exatamente 2 comportamentos na fonte, chao e porta,
#   contra 5 metatiles nossos: a regua os acusa como os piores mapas da regiao e
#   eles estao ACIMA da fonte deles.
#
#   A segunda fonte foi conferida antes de a frase ser escrita: fontes-mapas/
#   sinnoh (demake gen 3) tem LAYOUT_OREBURGH_CITY_GYM com 54 metatiles, e ele e
#   byte a byte o RustboroCity_Gym de Hoenn (md5 d511ef095521d8a44c1f41072e83320e
#   nos dois). Nao e arte de Sinnoh, e emprestimo de Hoenn. NENHUMA fonte tem
#   arte de ginasio de Sinnoh.
#
#   Consequencia de metodo: a prova de fidelidade pixel a pixel do molde
#   tileset_gen2.py, que vale para Unova, e INDEFINIDA para Sinnoh, porque nao ha
#   referencia 2D da fonte para re-renderizar. A camada certa da afirmacao aqui e
#   o comportamento: o MB_* do metatile emitido contra o TileBehavior da fonte,
#   tile a tile. Censo em `porta_ginasios_sinnoh.py --censo`.
#
#   CORRECAO DE CONTAGEM: sao OITO ginasios abaixo do piso, nao sete.
#   OreburghCity_Gym (5 metatiles) faltava na lista.
#
#   Referencia para calibrar o piso: ginasio de Hoenn de verdade tem de 55 a 67
#   metatiles distintos, e caverna de Hoenn de 27 a 38.


# ------------------------------------------- NPC deslocado pelo corte (B13.b)
#
# O DEFEITO, medido em 18/08/2026 depois que o gelo de Snowpoint tropecou nele.
# `importa_npcs_sinnoh.conversor_de_coordenada` escolhe entre tres reguas, nesta
# ordem: translacao PROVADA por warps, identidade, escala da caixa da matriz. A
# do meio, identidade, entra quando toda coordenada da fonte CABE dentro do nosso
# layout, e ela ignora que o mapa pode ter sido RECORTADO. Nos ginasios foi o meu
# proprio `converte()` que recortou (margem de 1 tile dos lados e 2 em cima), e
# entao a coordenada da fonte cabe e mesmo assim aponta para o lugar errado.
#
# ESCALA DO ESTRAGO, medida e nao estimada, nos 353 mapas de Sinnoh com NPC
# importado: a translacao provada por >=2 warps da (0,0) em 27 mapas, e diferente
# de (0,0) em 8 (dos quais 4 sao rota externa, onde a fonte usa coordenada de
# MUNDO e a regua certa ja e a escala, e um e a Route222 que ja foi consertada a
# parte). Nos outros 318 o warp nao prova nada. Ou seja: NAO ha epidemia em
# Sinnoh. O corte com deslocamento e dos 8 GINASIOS, e so deles, porque so eles
# passaram pelo `converte()` daqui.
#
# POR QUE O CONSERTO MORA AQUI E NAO NO CONVERSOR COMPARTILHADO. Seria mais bonito
# ensinar `conversor_de_coordenada` a descontar o corte, e cheguei a desenhar
# isso: aceitar a translacao quando os dois lados tem UM warp so (o par fica
# forcado, entao nao ha ambiguidade). Nao entrou, e o motivo esta escrito no
# proprio docstring de la: aquela funcao tambem e usada para REENCONTRAR, pela
# coordenada, evento que ja esta gravado (`itens_escondidos_sinnoh`,
# `texto_sinnoh`, `maquina_sinnoh`, `fila_b6`). Mudar a conta orfana o que ja foi
# gravado. Medido: existem dezenas de mapas com 1 warp de cada lado (elevador,
# B1F de centro Pokemon) cuja fonte usa outro sistema de coordenada, e a
# translacao "forcada" deles daria d=(13,4) ou d=(6,2), o que MOVERIA NPC certo
# para o lugar errado. Trocar risco em 353 mapas e 4 ferramentas para consertar
# 13 NPC em 5 mapas e um mau negocio. Aqui o corte e MEDIDO (sai do `converte()`,
# nao de constante) e o raio de acao e exatamente o conjunto afetado.
#
# O PORTAO: NPC so anda se o destino for tile andavel E alcancavel pela mesma BFS
# do `verifica()` (com deslize onde ha gelo). Quem o conserto jogaria para dentro
# de parede, ou para fora do mapa, NAO SE MOVE e vira linha de censo com motivo.


# ------------------------------------------------- FILA: bolas de neve (B13.c)
#
# NAO FEITO de proposito, registrado aqui em 18/08/2026 para quem pegar depois
# nao precisar remedir nada.
#
# O QUE FALTA. `res/field/events/events_snowpoint_city_gym.json` tem 19 objetos
# `LOCALID_SNOWBALL_1` a `LOCALID_SNOWBALL_19`, todos com script 2037 e posicao
# na grade da fonte (lembrar de descontar o corte z0=1 deste mapa):
#   (12,18) (10,21) (17,19) (11,16) (11,14) (11,11) (11,8) (13,8) (10,8) (12,8)
#   (9,4) (13,4) (10,15) (17,17) (17,18) (17,20) (12,21) (9,8) (20,23)
# Nenhum deles entrou na ROM. Sao os obstaculos EMPURRAVEIS que fazem o
# quebra-cabeca de gelo ser resolvivel: sem eles o jogador so consegue parar
# contra parede.
#
# A DIMENSAO DO PROBLEMA, medida: SnowpointCity_Gym tem 531 tiles andaveis e
# apenas 84 em que o jogador consegue FICAR DE PE (`--verifica`). Com as bolas o
# numero de paradas sobe, porque cada uma e um ponto de parada novo.
#
# A PERGUNTA DE MECANICA, que e por que isto nao e conversao e sim desenho, e
# portanto e decisao do Gui: empurravel no GBA e BLOCO DE STRENGTH
# (`MB_PUSHABLE_BOULDER` mais o HM e o estado de "ja empurrado" na save). O
# Platinum empurra bola de neve SEM HM nenhum, um tile por vez, e ela desliza
# ate bater. Portar isso e escolher entre (a) exigir Strength, que muda a
# progressao do jogo, (b) escrever um empurrao proprio para gelo, que e motor
# novo, ou (c) por as bolas como obstaculo FIXO, que resolve a travessia e mata
# o quebra-cabeca. As tres sao decisoes de desenho, nenhuma e traducao.
#
# TRES TREINADORES ANDAM JUNTO COM AS BOLAS, E ISTO NAO E OPCIONAL. O conserto de
# coordenada do corte (B13.b) RECUSOU mover estes tres de Snowpoint, porque a
# posicao correta deles nao e alcancavel no gelo de hoje:
#   acetrainerisaiah   esta em (18,15), a da fonte e (18,14)
#   acetrainerbrenna   esta em  (5,16), a da fonte e  (5,15)
#   acetrainersergio   esta em  (2,13), a da fonte e  (2,12)
# Eles ficam 1 tile fora do lugar DE PROPOSITO: mover agora trocaria erro
# cosmetico por treinador inalcancavel, que e pior, e foi exatamente o defeito da
# Alicia. Sao as bolas de neve que tornam aquelas casas alcancaveis. Quando as
# bolas entrarem, rodar `--gravar-npc` de novo move os tres sozinho, porque o
# portao de alcance passa a aceitar. **NAO "consertar" o alinhamento deles antes
# das bolas**: sem elas o jogo quebra e o `--verifica` acusa.
#
# CRITERIO DE ACEITE, se um dia entrar: (1) `--verifica` verde nos 8 ginasios,
# com a Candice ainda alcancavel e ZERO tile-armadilha, medido com as bolas no
# lugar; (2) numero de paradas de Snowpoint reportado antes e depois, porque e
# ele que diz se o quebra-cabeca virou jogavel; (3) caso de suite com fato de
# EWRAM provando que uma bola EMPURRADA muda a posicao final do jogador, mais
# par negativo sem a bola; (4) nenhum NPC empilhado (o portao de ocupacao de
# `npcs_deslocados` ja pega isso).


def _header_da_fonte(pasta, _cache={}):
    """MAP_HEADER_* do Platinum que corresponde a este ginasio."""
    if not _cache:
        import importa_npcs_sinnoh as I
        for h in I.headers_do_platinum():
            _cache.setdefault(I.chave(h), h)
    import importa_npcs_sinnoh as I
    return I.APELIDOS.get(pasta) or _cache.get(I.chave(pasta))


def _par_da_fonte(header):
    """[(nome normalizado, x, z)] dos object events da fonte."""
    import importa_npcs_sinnoh as I
    arq = os.path.join(I.PLAT, "res/field/events",
                       f"events_{header.replace('MAP_HEADER_', '').lower()}.json")
    if not os.path.exists(arq):
        return []
    saida = []
    for o in json.load(open(arq)).get("object_events", []):
        nome = str(o.get("id") or "")
        nome = nome[len("LOCALID_"):] if nome.startswith("LOCALID_") else nome
        saida.append((nome.replace("_", "").lower(), o["x"], o["z"]))
    return saida


def _casa(o, fonte, mapeia=None):
    """(x, z) na fonte do NPC `o`, ou None. Tres reguas, nesta ordem.

    1. NOME. `..._EventScript_AceTrainerAlicia` casa com `LOCALID_ACE_TRAINER_
       ALICIA`. Exato, nunca por sufixo: casar por sufixo fez `LOCALID_SNOWBALL_1`
       parear com qualquer script terminado em "1" e me deu um par falso.
    2. POSICAO CRUA, quando o nome nao serve. Metade dos NPC de ginasio entrou
       com script generico (`_EventScript_Npc1`), entao nao ha nome para casar.
       Mas eles foram postos pela regra da IDENTIDADE, ou seja a coordenada nossa
       E a da fonte: procurar a coordenada de volta identifica de qual evento cada
       um veio. So vale quando UM evento da fonte esta ali; empate nao e prova.
    3. POSICAO JA CORRIGIDA pelo corte. Sem esta, o NPC de script generico some do
       censo assim que e movido (a posicao dele deixa de bater com a crua), e o
       conserto deixa de ser idempotente na leitura: o mesmo NPC apareceria como
       "sem par na fonte" na segunda rodada. Tambem e o que mantem o portao de
       duplicata enxergando quem ja foi consertado.
    """
    alvo = (o.get("script") or "").split("EventScript_")[-1].lower()
    por_nome = [(x, z) for n, x, z in fonte if n == alvo]
    if len(por_nome) == 1:
        return por_nome[0]
    for regra in ((lambda x, z: (x, z)),
                  (mapeia if mapeia else None)):
        if regra is None:
            continue
        achado = [(x, z) for _, x, z in fonte if regra(x, z) == (o["x"], o["y"])]
        if len(achado) == 1:
            return achado[0]
    return None


def npcs_deslocados(gravar=False):
    """Censo linha a linha, e conserto se `gravar`. Idempotente."""
    sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
    import importa_npcs_sinnoh as I
    heads = I.headers_do_platinum()
    deles = {}
    for h in heads:
        deles.setdefault(I.chave(h), h)
    layouts = {l["id"]: l for l in json.load(
        open(os.path.join(REPO, "data/layouts/layouts.json")))["layouts"]}
    movidos = recusados = ja_ok = 0
    print(f"{'mapa':22s} {'NPC':30s} {'de':>9} {'para':>9}  situacao")
    for g in GINASIOS:
        largura, alt, _, _, mapeia = converte(g)
        x0, z0 = (-mapeia(0, 0)[0], -mapeia(0, 0)[1])
        h = I.APELIDOS.get(g.pasta) or deles.get(I.chave(g.pasta))
        fonte = _par_da_fonte(h) if h else {}
        caminho = os.path.join(REPO, "data/maps", g.pasta, "map.json")
        m = json.load(open(caminho))
        L = layouts[m["layout"]]
        dados = open(os.path.join(REPO, L["blockdata_filepath"]), "rb").read()
        blocos = struct.unpack(f"<{len(dados) // 2}H", dados)
        parada = _paradas(g, m, blocos, largura, alt)
        importados = [o for o in m["object_events"]
                      if str(o.get("origem", "")).startswith("pokeplatinum")]
        pares = {id(o): _casa(o, fonte, mapeia) for o in importados}

        # PORTAO DE MAPA, antes de mexer em qualquer NPC: se algum par cair FORA
        # do layout, o corte NAO e a translacao deste mapa e nao ha conserto a
        # fazer aqui. E o caso de Canalave, e ele nao e surpresa: o ginasio do
        # Byron e um vao de passarelas em ALTURA, o proprio Byron esta na fonte
        # com y=30 num andar que a grade 2D nao representa (ver
        # `andavel_plataforma`), e por isso os NPC de la entraram pela regra da
        # ESCALA e nao da identidade. Mover so os que por acaso caem dentro
        # espalharia o grupo por dois sistemas de coordenada, que e pior do que
        # o desalinhamento de hoje. Recusa o mapa inteiro.
        fora = [o for o in importados if pares[id(o)]
                and not (0 <= mapeia(*pares[id(o)])[0] < largura
                         and 0 <= mapeia(*pares[id(o)])[1] < alt)]
        if fora:
            print(f"{g.pasta:22s} {'(mapa inteiro)':30s} {'-':>9} {'-':>9}  "
                  f"RECUSADO: {len(fora)} de {len(importados)} pares caem FORA do "
                  f"layout {largura}x{alt} com o corte ({x0},{z0}); a translacao "
                  f"nao e deste mapa")
            recusados += len(importados)
            continue

        mudou = False
        for o in importados:
            par = pares[id(o)]
            if par is None:
                print(f"{g.pasta:22s} {o['graphics_id']:30s} "
                      f"{str((o['x'], o['y'])):>9} {'-':>9}  sem par na fonte, nao mexo")
                recusados += 1
                continue
            nx, ny = mapeia(*par)
            alvo = (o.get("script") or "").split("EventScript_")[-1].lower() or o["graphics_id"]
            if (o["x"], o["y"]) == (nx, ny):
                ja_ok += 1
                continue
            if (nx, ny) not in parada:
                print(f"{g.pasta:22s} {alvo:30s} {str((o['x'], o['y'])):>9} "
                      f"{str((nx, ny)):>9}  RECUSADO: destino nao e tile alcancavel")
                recusados += 1
                continue
            # DOIS NPC NO MESMO TILE e defeito, e este portao achou um de
            # verdade: em Oreburgh, `LOCALID_OREBURGH_GYM_VISITOR`, que o
            # `GINASIOS` daqui cria a partir do evento (4,18) da fonte, e o
            # `YoungsterJonathon` que o importador trouxe DO MESMO evento sao a
            # MESMA pessoa em duplicata, e o conserto de coordenada os empilhava
            # exatamente um em cima do outro. Duplicata e conteudo de map.json e
            # nao se resolve movendo nem apagando NPC por conta propria: fica
            # como linha de censo.
            ocupado = {(q["x"], q["y"]) for q in m["object_events"] if q is not o}
            if (nx, ny) in ocupado:
                print(f"{g.pasta:22s} {alvo:30s} {str((o['x'], o['y'])):>9} "
                      f"{str((nx, ny)):>9}  RECUSADO: destino ja ocupado por outro "
                      f"objeto (possivel duplicata da mesma pessoa da fonte)")
                recusados += 1
                continue
            print(f"{g.pasta:22s} {alvo:30s} {str((o['x'], o['y'])):>9} "
                  f"{str((nx, ny)):>9}  movido (corte z0={z0})")
            o["x"], o["y"] = nx, ny
            movidos += 1
            mudou = True
        if mudou and gravar:
            with open(caminho, "w") as f:
                json.dump(m, f, indent=2)
                f.write("\n")
    print(f"\n{movidos} movidos, {recusados} recusados, {ja_ok} ja no lugar"
          + ("" if gravar else "   (nada gravado, use --gravar-npc)"))
    return movidos, recusados


def demo():
    """Autoteste com MUTACAO PLANTADA. Verde aqui nao e "rodou": cada bloco
    estraga alguma coisa de proposito e exige que a medicao ACUSE."""
    import hashlib

    def md5(p):
        return hashlib.md5(open(p, "rb").read()).hexdigest()

    arquivos = [os.path.join(_pasta_tileset(ts), n)
                for ts in APPEND for n in ("metatiles.bin", "metatile_attributes.bin")]

    # 1. APPEND E IDEMPOTENTE. Rodar de novo nao pode acrescentar metatile
    #    repetido nem mover indice; foi por isso que aplica_append procura por
    #    (atributo, arte) antes de emendar.
    antes = {p: md5(p) for p in arquivos}
    primeiro = aplica_append(gravar=True)
    segundo = aplica_append(gravar=True)
    assert primeiro == segundo, f"append nao e idempotente: {primeiro} != {segundo}"
    assert all(md5(p) == antes[p] for p in arquivos), "append reescreveu arquivo ja pronto"
    print(f"  ok  append idempotente, indices {sorted(primeiro.values())}")

    # 2. ESTADO BOM, medido e nao suposto.
    verifica()
    s = ULTIMA_MEDIDA["SnowpointCity_Gym"]
    assert s["gelo"] >= 400, f"Snowpoint com {s['gelo']} tiles de gelo, esperado ~497"
    razao = s["paradas"] / s["andaveis"]
    assert razao < 0.3, (f"Snowpoint: {s['paradas']} paradas em {s['andaveis']} tiles "
                         f"andaveis (razao {razao:.2f}). Sem deslize isso vai a 1.0, "
                         f"ou seja o modelo de gelo parou de valer")
    print(f"  ok  gelo {s['gelo']}, paradas {s['paradas']} de {s['andaveis']} andaveis "
          f"(razao {razao:.2f}), armadilha {s['armadilha']}")

    # 3. MUTACAO PLANTADA: estraga o ATRIBUTO do gelo (MB_ICE vira MB_NORMAL) no
    #    arquivo de verdade e exige que a medicao caia. Se este bloco passar
    #    verde, a verificacao nao esta lendo o atributo e o gelo pode sumir sem
    #    ninguem ver.
    pasta = _pasta_tileset("gTileset_SootopolisGym")
    alvo = os.path.join(pasta, "metatile_attributes.bin")
    original = open(alvo, "rb").read()
    try:
        i = aplica_append()[("gTileset_SootopolisGym", "MB_ICE")] - 512
        estragado = bytearray(original)
        struct.pack_into("<H", estragado, i * 2, _mb_por_nome()["MB_NORMAL"])
        open(alvo, "wb").write(estragado)
        verifica()
        mutante = ULTIMA_MEDIDA["SnowpointCity_Gym"]
        assert mutante["gelo"] == 0, "atributo estragado e o gelo continuou contando"
        assert mutante["paradas"] > s["paradas"], (
            "sem gelo o jogador deveria parar em MAIS tiles, e nao parou: "
            "a verificacao nao esta modelando o deslize")
        print(f"  ok  mutacao no atributo ACUSADA: gelo {s['gelo']} -> 0, "
              f"paradas {s['paradas']} -> {mutante['paradas']}")
    finally:
        open(alvo, "wb").write(original)
    assert md5(alvo) == antes[alvo], "o demo nao restaurou o tileset"

    # 4. A geometria nao pode ter andado: e o que separa "troquei o desenho" de
    #    "movi warp e NPC", que a lei da casa proibe.
    L = {l["id"]: l for l in json.load(
        open(os.path.join(REPO, "data/layouts/layouts.json")))["layouts"]}
    for g in GINASIOS:
        largura, alt, _, _, mapeia = converte(g)
        e = L[g.layout]
        m = json.load(open(os.path.join(REPO, "data/maps", g.pasta, "map.json")))
        assert (largura, alt) == (e["width"], e["height"]), f"{g.pasta}: dimensao andou"
        assert mapeia(*g.warp) == (m["warp_events"][0]["x"], m["warp_events"][0]["y"]), \
            f"{g.pasta}: o warp andou"
    print("  ok  8 ginasios com dimensao e warp intactos")

    # 5. CONSERTO DE NPC: idempotente, e a MUTACAO PLANTADA empurra um NPC de
    #    volta para a coordenada errada e exige que o censo o ACHE. Sem este
    #    bloco, um censo que passasse a nao enxergar nada imprimiria "0 movidos"
    #    e pareceria saudavel, que e o jeito mais facil de este conserto morrer.
    mapa = os.path.join(REPO, "data/maps/VeilstoneCity_Gym/map.json")
    original = open(mapa).read()
    try:
        movidos, _ = npcs_deslocados()
        assert movidos == 0, f"conserto de NPC nao e idempotente: {movidos} pendentes"
        d = json.loads(original)
        alvo = next(o for o in d["object_events"]
                    if "BlackBeltColby" in (o.get("script") or ""))
        antes_y = alvo["y"]
        alvo["y"] += 1                       # devolve o erro de corte de +1
        with open(mapa, "w") as f:
            json.dump(d, f, indent=2)
            f.write("\n")
        movidos, _ = npcs_deslocados()
        assert movidos == 1, (f"a mutacao plantada (BlackBeltColby de {antes_y} para "
                              f"{antes_y + 1}) devia aparecer como 1 movido, veio {movidos}")
        print(f"  ok  mutacao no NPC ACUSADA: Colby em y={antes_y + 1} pedindo "
              f"volta para y={antes_y}")
    finally:
        open(mapa, "w").write(original)
    assert open(mapa).read() == original, "o demo nao restaurou o map.json"

    # 6. PORTAO DE DUPLICATA: replanta a duplicata de Oreburgh (um objeto novo
    #    apontando para o MESMO evento da fonte que o Jonathon) e exige que o
    #    `--verifica` reprove. Sem este bloco o portao poderia estar cego e o
    #    verde nao significaria nada, que e como a duplicata original sobreviveu.
    mapa = os.path.join(REPO, "data/maps/OreburghCity_Gym/map.json")
    original = open(mapa).read()
    try:
        assert verifica() == 0, "Oreburgh ja estava reprovando antes do plante"
        d = json.loads(original)
        clone = dict(next(o for o in d["object_events"]
                          if "YoungsterJonathon" in (o.get("script") or "")))
        clone["local_id"] = "LOCALID_OREBURGH_GYM_VISITOR"
        clone["y"] += 1                      # ao lado, como a duplicata original
        d["object_events"].insert(0, clone)
        with open(mapa, "w") as f:
            json.dump(d, f, indent=2)
            f.write("\n")
        assert verifica() > 0, ("a duplicata replantada NAO foi acusada: o portao "
                               "de evento da fonte esta cego")
        print("  ok  duplicata replantada ACUSADA pelo portao de evento da fonte")
    finally:
        open(mapa, "w").write(original)
    assert open(mapa).read() == original, "o demo nao restaurou o map.json de Oreburgh"
    print("demo OK")
    return 0


def main():
    if "--demo" in sys.argv:
        sys.exit(demo())
    if "--npc" in sys.argv or "--gravar-npc" in sys.argv:
        npcs_deslocados(gravar="--gravar-npc" in sys.argv)
        sys.exit(0)
    if "--censo" in sys.argv:
        sys.exit(censo())
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
            # SO o map.bin. `grava()` (que reescreve tambem layouts.json e
            # map.json) fica para quando a GEOMETRIA mudar de verdade; enquanto
            # largura, altura e a posicao do warp forem as mesmas, mexer no
            # map.json e (a) desnecessario e (b) fronteira, porque ele e do
            # executor que esta povoando Sinnoh com NPC AGORA. O assert abaixo e
            # o que separa os dois casos, e ele falha alto em vez de calado.
            L = json.load(open(os.path.join(REPO, "data/layouts/layouts.json")))
            e = next(l for l in L["layouts"] if l["id"] == g.layout)
            assert (e["width"], e["height"]) == (largura, alt), (
                f"{g.pasta}: geometria mudou ({e['width']}x{e['height']} -> "
                f"{largura}x{alt}); isso move warp e NPC, use grava() e avise")
            with open(os.path.join(REPO, e["blockdata_filepath"]), "wb") as f:
                f.write(struct.pack(f"<{len(blocos)}H", *blocos))
    print("gravado" if GRAVAR else "nada gravado (use --gravar)")


if __name__ == "__main__":
    main()
