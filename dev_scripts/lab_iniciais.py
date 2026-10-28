#!/usr/bin/env python3
"""Laboratório do Oak com 52 iniciais: arte, mapa, conferência e roteiro.

Pedido do Gui em 28/10/2026: no laboratório do Oak em Pallet Town (o jogo começa
ali), trocar a escolha de três iniciais por mesinhas de três Poké Balls, 52 bolas
(os 27 iniciais das gerações 1 a 9 e mais 25 espécies), e o jogador leva UMA, no
nível 5. O lado do jogo está em `src/lab_iniciais.c` (tabela das 49 bolas novas,
que é o ÚNICO ponto de dado de posição e espécie) e no script do laboratório. Este
arquivo DERIVA o resto daquela tabela e confere.

Uso:
    python3 dev_scripts/lab_iniciais.py --arte      # tampo de mesa com bola no tileset
    python3 dev_scripts/lab_iniciais.py --mapa      # map.bin, tamanho do layout, bg_events
    python3 dev_scripts/lab_iniciais.py --confere   # tudo bate? (0 = verde; não escreve nada)
    python3 dev_scripts/lab_iniciais.py --render saida.png [--escala 2]
    python3 dev_scripts/lab_iniciais.py --roteiro   # passeio pelas 49 bolas novas (caso T364.5)

`--arte` e `--mapa` são idempotentes: rodar de novo sobre o resultado não muda um
byte, e é isso que `--confere` cobra.

A ARTE (decisão do pedido: nada de arte inventada)
--------------------------------------------------
Não há metatile de Poké Ball sobre mesa em tileset nenhum do par do laboratório
(`gTileset_BuildingFrlg` + `gTileset_Lab_Frlg`, atlas olhado em 28/10/2026). Então
o tampo com bola é MONTADO: os pixels do sprite `OBJ_EVENT_GFX_ITEM_BALL`
(`graphics/object_events/pics/misc/ball_poke.png`, quadro 0, metade de baixo,
cores de `graphics/object_events/palettes/npc_3.pal`) por cima dos tiles do tampo
da mesa de Kanto (metatiles 0x2A8, 0x2A9 e 0x2AA), na mesma posição em que o jogo
desenha a bola-objeto. Os três tampos com bola saem em 0x32F, 0x330 e 0x331.
As três bolas de Kanto continuam objetos e não usam esta arte.

Cores: os tiles do tampo usam a paleta 12 do secundário, que não tem as cores da
bola. A paleta 9 do `lab_frlg` estava inteira preta e nenhum tile a usava (nem do
secundário, nem do primário `building_frlg`, medido): ela vira a paleta do tampo
com bola, com as cores 0 a 6 iguais às da 12 (as que o tampo usa) e as cores da
bola em seguida. Nenhum outro mapa que usa `gTileset_Lab_Frlg` muda um pixel: os
oito tiles e os três metatiles são acrescentados no FIM, e a paleta 9 era morta.
O PNG de tiles é refluído para 8 tiles por linha (120 = 8 x 15), para não sobrar
tile vazio no fim (lição da 0.ao do ESTADO); a ORDEM dos tiles não muda.

O MAPA
------
O laboratório cresce para a DIREITA e para BAIXO, sem deslocar coordenada nenhuma
do que já existia: a sala original (x 0..12, y 0..13) fica byte a byte igual, com
a mesa de Kanto, o Oak, o rival, a porta e os gatilhos de batalha onde sempre
estiveram. A ala nova (x 13..30, y 0..18) liga à sala só pela metade de CIMA
(y 3..7 em x = 13): a coluna x = 13 é parede preta de y 8 para baixo, então a ala
não tem caminho até a porta que fuja dos gatilhos de (5..7, 8). É isso que segura
a cena de escolha ("Don't go away yet!") e a batalha de saída. `--confere` prova.

As 16 mesas cheias ficam em 4 fileiras (tampos em y 4, 7, 10 e 13, pés andáveis
na fileira de baixo) e 4 colunas (x 15, 19, 23 e 27), com corredor de uma célula
entre elas. A 17ª mesa fica sozinha no centro da fileira de baixo (x 21..23,
y 16) e tem só a bola do meio: 49 = 16 x 3 + 1, e com as três de Kanto são as
52 do pedido (17 mesas de 3 e 1 mesa com 1).
"""
import argparse
import collections
import json
import os
import re
import struct
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TILESET = os.path.join(RAIZ, "data/tilesets/secondary/lab_frlg")
PRIMARIO = os.path.join(RAIZ, "data/tilesets/primary/building_frlg")
MAPA_BIN = os.path.join(RAIZ, "data/layouts/PalletTown_ProfessorOaksLab_Frlg/map.bin")
LAYOUTS = os.path.join(RAIZ, "data/layouts/layouts.json")
MAPA_JSON = os.path.join(RAIZ, "data/maps/PalletTown_ProfessorOaksLab_Frlg/map.json")
FONTE_C = os.path.join(RAIZ, "src/lab_iniciais.c")
SPRITE_BOLA = os.path.join(RAIZ, "graphics/object_events/pics/misc/ball_poke.png")
PALETA_BOLA = os.path.join(RAIZ, "graphics/object_events/palettes/npc_3.pal")
LAYOUT_ID = "LAYOUT_PALLET_TOWN_PROFESSOR_OAKS_LAB"
SCRIPT_BOLA = "PalletTown_ProfessorOaksLab_EventScript_BolaDaMesaNova"
# O laboratório como estava no master de 28/10/2026 (7daca4e59f): a sala
# original tem de continuar byte a byte igual a este.
COMMIT_ORIGINAL = "7daca4e59f"

# --- tileset -----------------------------------------------------------------
TILES_ORIGINAIS = 112          # tiles do secundário antes desta frente
METATILES_ORIGINAIS = 175      # metatiles do secundário antes desta frente
BASE_SECUNDARIO = 640          # FRLG: o primário tem 640 tiles e 640 metatiles
PALETA_TAMPO = 12              # paleta dos tiles do tampo da mesa
PALETA_NOVA = 9                # estava toda preta e sem uso
MESA_ESQ, MESA_MEIO, MESA_DIR = 0x2A8, 0x2A9, 0x2AA
BOLA_ESQ, BOLA_MEIO, BOLA_DIR = 0x32F, 0x330, 0x331
PES_ESQ, PES_MEIO, PES_DIR = 0x2B0, 0x2B1, 0x2B2

# --- mapa ----------------------------------------------------------------------
LARGURA_ORIG, ALTURA_ORIG = 13, 14
LARGURA, ALTURA = 31, 19
PISO = 0x289
PISO_SOMBRA_ESQ = 0x288        # piso com a sombra da parede à esquerda (x = 0 da sala)
VAZIO = 0x008                  # o preto do pé da sala (y = 13), com colisão
ESTANTE_TOPO = (0x06B, 0x06C)  # estante encostada na parede de fundo, como em x 9..12
ESTANTE_CORPO = (0x073, 0x074)
ESTANTE_PE = (0x283, 0x284)
FILEIRAS_MESA = (4, 7, 10, 13)  # y do tampo; os pés ficam em y + 1
COLUNAS_MESA = (15, 19, 23, 27)  # x da célula da esquerda
MESA_AVULSA = (21, 16)          # a mesa da 52ª bola, centrada sob as quatro colunas
NUM_BOLAS_NOVAS = 49
ABERTURA_X, ABERTURA_Y = 13, range(3, 8)
# Objetos parados da sala, que bloqueiam o passo (map.json): Oak depois da cena,
# rival, as duas Pokédex e as três bolas de Kanto. Os assistentes andam na metade
# de baixo e não entram na conta da ala.
OBJETOS_PARADOS = {(6, 3), (5, 4), (4, 1), (5, 1), (8, 4), (9, 4), (10, 4)}
BOLAS_KANTO = ((8, 4), (9, 4), (10, 4))
# Os três assistentes da metade de baixo: dois parados e uma que anda para cima e
# para baixo em x = 2 (MOVEMENT_TYPE_WANDER_UP_AND_DOWN, raio 4). Só o roteiro do
# emulador desvia deles; na cena de escolha eles nem estão no caminho.
AJUDANTES = {(3, 11), (11, 10)} | {(2, y) for y in range(6, 15)}
JOGADOR_DEPOIS_DA_CENA = (6, 4)   # PlayerEnter: 8 passos para cima a partir de (6,12)
PORTA = (6, 12)
GATILHOS = {(5, 8), (6, 8), (7, 8)}


def celula(metatile, colisao, elevacao):
    return metatile | (colisao << 10) | (elevacao << 12)


# ---------------------------------------------------------------------------
# leitura da tabela em C (o único ponto de dado)
# ---------------------------------------------------------------------------
_PADRAO_BOLA = re.compile(r"\{\s*(\d+),\s*(\d+),\s*(SPECIES_\w+)\s*\}")


def bolas_da_fonte():
    texto = open(FONTE_C, encoding="utf-8").read()
    inicio = texto.index("sBolasDoLab[] =")
    fim = texto.index("};", inicio)
    return [(int(x), int(y), esp) for x, y, esp in _PADRAO_BOLA.findall(texto[inicio:fim])]


def mesas():
    """Lista de (x0, y): célula da esquerda do tampo de cada mesa nova."""
    return [(x0, y) for y in FILEIRAS_MESA for x0 in COLUNAS_MESA] + [MESA_AVULSA]


# ---------------------------------------------------------------------------
# PNG e paletas
# ---------------------------------------------------------------------------
def le_pal(caminho):
    linhas = open(caminho, encoding="utf-8").read().splitlines()
    assert linhas[0].strip() == "JASC-PAL", caminho
    n = int(linhas[2])
    return [tuple(int(v) for v in linhas[3 + i].split()) for i in range(n)]


def escreve_pal(caminho, cores):
    with open(caminho, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n%d\n" % len(cores))
        for c in cores:
            f.write("%d %d %d\n" % c)


def tiles_do_png(caminho):
    from PIL import Image
    im = Image.open(caminho)
    assert im.mode == "P", caminho
    w, h = im.size
    px = im.load()
    return [tuple(px[tx * 8 + x, ty * 8 + y] for y in range(8) for x in range(8))
            for ty in range(h // 8) for tx in range(w // 8)]


def grava_png_de_tiles(caminho, tiles, por_linha, paleta_png):
    from PIL import Image
    linhas = (len(tiles) + por_linha - 1) // por_linha
    assert linhas * por_linha == len(tiles), "sobraria tile vazio no fim"
    im = Image.new("P", (por_linha * 8, linhas * 8))
    im.putpalette(paleta_png)
    px = im.load()
    for i, t in enumerate(tiles):
        tx, ty = i % por_linha, i // por_linha
        for k, v in enumerate(t):
            px[tx * 8 + k % 8, ty * 8 + k // 8] = v
    im.save(caminho, optimize=False)


def le_metatiles(caminho):
    b = open(caminho, "rb").read()
    return [list(struct.unpack("<8H", b[i:i + 16])) for i in range(0, len(b), 16)]


def le_atributos(caminho):
    b = open(caminho, "rb").read()
    return list(struct.unpack("<%dI" % (len(b) // 4), b))


# ---------------------------------------------------------------------------
# --arte
# ---------------------------------------------------------------------------
def pixels_da_bola():
    """{(x, y): (r, g, b)} da bola, na célula 16x16 em que o jogo a desenha.

    O sprite é 16x32 com a base apoiada na célula do objeto, então a metade de
    baixo do quadro 0 (o "olhando para baixo" de MOVEMENT_TYPE_FACE_DOWN) cai
    exatamente sobre o tampo."""
    from PIL import Image
    im = Image.open(SPRITE_BOLA)
    pal = le_pal(PALETA_BOLA)
    px = im.load()
    out = {}
    for y in range(16):
        for x in range(16):
            v = px[x, 16 + y]
            if v:
                out[(x, y)] = pal[v]
    return out


def monta_arte():
    """Devolve (tiles_novos, paleta_nova, metatiles_novos, atributos_novos)."""
    tiles = tiles_do_png(os.path.join(TILESET, "tiles.png"))[:TILES_ORIGINAIS]
    mts = le_metatiles(os.path.join(TILESET, "metatiles.bin"))[:METATILES_ORIGINAIS]
    atrs = le_atributos(os.path.join(TILESET, "metatile_attributes.bin"))[:METATILES_ORIGINAIS]
    p12 = le_pal(os.path.join(TILESET, "palettes/%02d.pal" % PALETA_TAMPO))
    bola = pixels_da_bola()

    # Paleta nova: 0..6 iguais à 12 (o tampo só usa estas), depois as cores da bola.
    paleta = list(p12[:7])
    for cor in sorted(set(bola.values()), key=lambda c: (c[0], c[1], c[2])):
        if cor not in paleta:
            paleta.append(cor)
    assert len(paleta) <= 16, f"cores demais: {len(paleta)}"
    paleta += [(0, 0, 0)] * (16 - len(paleta))
    indice_cor = {}
    for i, c in enumerate(paleta):
        indice_cor.setdefault(c, i)

    novos_tiles = []
    novos_mts = []
    for mid in (MESA_ESQ, MESA_MEIO, MESA_DIR):
        e = mts[mid - BASE_SECUNDARIO]
        topo = e[4:]
        img = [[0] * 16 for _ in range(16)]
        for k, ent in enumerate(topo):
            idx, hf, vf, pal = ent & 0x3FF, (ent >> 10) & 1, (ent >> 11) & 1, ent >> 12
            assert pal == PALETA_TAMPO and not hf and not vf and idx >= BASE_SECUNDARIO, hex(ent)
            t = tiles[idx - BASE_SECUNDARIO]
            ox, oy = (k % 2) * 8, (k // 2) * 8
            for p, v in enumerate(t):
                assert v <= 6, "o tampo usa cor fora de 0..6 da paleta 12"
                img[oy + p // 8][ox + p % 8] = v
        for (x, y), cor in bola.items():
            img[y][x] = indice_cor[cor]
        entradas = []
        for k in range(4):
            ox, oy = (k % 2) * 8, (k // 2) * 8
            t = tuple(img[oy + y][ox + x] for y in range(8) for x in range(8))
            if t not in novos_tiles:
                novos_tiles.append(t)
            entradas.append((BASE_SECUNDARIO + TILES_ORIGINAIS + novos_tiles.index(t))
                            | (PALETA_NOVA << 12))
        novos_mts.append(e[:4] + entradas)
    novos_atrs = [atrs[m - BASE_SECUNDARIO] for m in (MESA_ESQ, MESA_MEIO, MESA_DIR)]
    return novos_tiles, paleta, novos_mts, novos_atrs


def aplica_arte(escrever=True):
    """Escreve (ou só confere) a arte. Devolve lista de divergências."""
    from PIL import Image
    novos_tiles, paleta, novos_mts, novos_atrs = monta_arte()
    caminho_png = os.path.join(TILESET, "tiles.png")
    tiles = tiles_do_png(caminho_png)
    mts = le_metatiles(os.path.join(TILESET, "metatiles.bin"))
    atrs = le_atributos(os.path.join(TILESET, "metatile_attributes.bin"))
    esperado_tiles = tiles[:TILES_ORIGINAIS] + novos_tiles
    esperado_mts = mts[:METATILES_ORIGINAIS] + novos_mts
    esperado_atrs = atrs[:METATILES_ORIGINAIS] + novos_atrs
    assert BOLA_ESQ - BASE_SECUNDARIO == METATILES_ORIGINAIS
    erros = []
    if tiles != esperado_tiles:
        erros.append(f"tiles.png: {len(tiles)} tiles, esperado {len(esperado_tiles)} "
                     "(os 112 originais e os do tampo com bola)")
    if mts != esperado_mts:
        erros.append(f"metatiles.bin: {len(mts)} metatiles, esperado {len(esperado_mts)}")
    if atrs != esperado_atrs:
        erros.append("metatile_attributes.bin diverge")
    pal9 = os.path.join(TILESET, "palettes/%02d.pal" % PALETA_NOVA)
    if le_pal(pal9) != paleta:
        erros.append("paletas/09.pal diverge")
    if escrever and erros:
        paleta_png = Image.open(caminho_png).getpalette()
        grava_png_de_tiles(caminho_png, esperado_tiles, 8, paleta_png)
        with open(os.path.join(TILESET, "metatiles.bin"), "wb") as f:
            for m in esperado_mts:
                f.write(struct.pack("<8H", *m))
        with open(os.path.join(TILESET, "metatile_attributes.bin"), "wb") as f:
            f.write(struct.pack("<%dI" % len(esperado_atrs), *esperado_atrs))
        escreve_pal(pal9, paleta)
        print(f"arte gravada: {len(novos_tiles)} tiles novos, 3 metatiles "
              f"({hex(BOLA_ESQ)}..{hex(BOLA_DIR)}), paleta {PALETA_NOVA}")
        return []
    return erros


# ---------------------------------------------------------------------------
# --mapa
# ---------------------------------------------------------------------------
def le_grade(caminho, largura, altura):
    b = open(caminho, "rb").read()
    assert len(b) == 2 * largura * altura, (caminho, len(b), largura, altura)
    v = struct.unpack("<%dH" % (largura * altura), b)
    return [list(v[y * largura:(y + 1) * largura]) for y in range(altura)]


def grade_original():
    """A sala de 13x14 como estava no master de origem desta frente."""
    b = subprocess.run(["git", "-C", RAIZ, "show",
                        f"{COMMIT_ORIGINAL}:data/layouts/PalletTown_ProfessorOaksLab_Frlg/map.bin"],
                       capture_output=True, check=True).stdout
    v = struct.unpack("<%dH" % (LARGURA_ORIG * ALTURA_ORIG), b)
    return [list(v[y * LARGURA_ORIG:(y + 1) * LARGURA_ORIG]) for y in range(ALTURA_ORIG)]


def monta_grade(bolas):
    orig = grade_original()
    preto = celula(VAZIO, 1, 0)
    g = [[preto] * LARGURA for _ in range(ALTURA)]
    for y in range(ALTURA_ORIG):
        g[y][:LARGURA_ORIG] = orig[y]
    for x in range(LARGURA_ORIG, LARGURA):
        par = (x - LARGURA_ORIG) % 2
        g[0][x] = celula(ESTANTE_TOPO[par], 1, 0)
        g[1][x] = celula(ESTANTE_CORPO[par], 1, 0)
        g[2][x] = celula(ESTANTE_PE[par], 0, 3)
        for y in range(3, ALTURA - 1):
            if x == ABERTURA_X and y not in ABERTURA_Y:
                continue  # a parede preta que separa a ala da metade de baixo
            sombra = x == ABERTURA_X + 1 and y > max(ABERTURA_Y)
            g[y][x] = celula(PISO_SOMBRA_ESQ if sombra else PISO, 0, 3)
    com_bola = {(x, y) for x, y, _ in bolas}
    for x0, y in mesas():
        for k, (vazia, cheia, pes) in enumerate(((MESA_ESQ, BOLA_ESQ, PES_ESQ),
                                                  (MESA_MEIO, BOLA_MEIO, PES_MEIO),
                                                  (MESA_DIR, BOLA_DIR, PES_DIR))):
            x = x0 + k
            g[y][x] = celula(cheia if (x, y) in com_bola else vazia, 1, 0)
            g[y + 1][x] = celula(pes, 0, 3)
    return g


def eventos_de_bola(bolas):
    return [{"type": "sign", "x": x, "y": y, "elevation": 0,
             "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
             "script": SCRIPT_BOLA} for x, y, _ in bolas]


def aplica_mapa(escrever=True):
    bolas = bolas_da_fonte()
    erros = confere_tabela(bolas)
    if erros:
        return erros
    g = monta_grade(bolas)
    bin_novo = b"".join(struct.pack("<%dH" % LARGURA, *linha) for linha in g)
    texto_layouts = open(LAYOUTS, encoding="utf-8").read()
    padrao = re.compile(r'("id": "%s",\n\s+"name": "[^"]+",\n\s+"width": )(\d+)(,\n\s+"height": )(\d+)'
                        % LAYOUT_ID)
    m = padrao.search(texto_layouts)
    assert m, "layout do laboratório não achado em layouts.json"
    layouts_novo = padrao.sub(lambda mm: f"{mm.group(1)}{LARGURA}{mm.group(3)}{ALTURA}",
                              texto_layouts, count=1)
    texto_mapa = open(MAPA_JSON, encoding="utf-8").read()
    d = json.loads(texto_mapa)
    d["bg_events"] = [e for e in d["bg_events"] if e.get("script") != SCRIPT_BOLA] + eventos_de_bola(bolas)
    mapa_novo = json.dumps(d, indent=2, ensure_ascii=False) + "\n"

    erros = []
    if open(MAPA_BIN, "rb").read() != bin_novo:
        erros.append("map.bin diverge do que a tabela de src/lab_iniciais.c manda")
    if texto_layouts != layouts_novo:
        erros.append(f"layouts.json: o laboratório tem de medir {LARGURA}x{ALTURA}")
    if texto_mapa != mapa_novo:
        erros.append("map.json: os bg_events das bolas não batem com a tabela em C")
    if escrever and erros:
        open(MAPA_BIN, "wb").write(bin_novo)
        open(LAYOUTS, "w", encoding="utf-8").write(layouts_novo)
        open(MAPA_JSON, "w", encoding="utf-8").write(mapa_novo)
        print(f"mapa gravado: {LARGURA}x{ALTURA}, {len(bolas)} bg_events de bola")
        return []
    return erros


def confere_tabela(bolas):
    erros = []
    if len(bolas) != NUM_BOLAS_NOVAS:
        erros.append(f"a tabela em C tem {len(bolas)} bolas, esperado {NUM_BOLAS_NOVAS}")
    tampos = {(x0 + k, y) for x0, y in mesas() for k in range(3)}
    vistos = collections.Counter((x, y) for x, y, _ in bolas)
    for (x, y), n in vistos.items():
        if n > 1:
            erros.append(f"duas bolas na mesma célula ({x},{y})")
        if (x, y) not in tampos:
            erros.append(f"bola em ({x},{y}) fora de um tampo de mesa nova")
    especies = collections.Counter(esp for _, _, esp in bolas)
    for esp, n in especies.items():
        if esp == "SPECIES_NONE":
            erros.append("bola sem espécie (SPECIES_NONE) na tabela em C")
        elif n > 1:
            erros.append(f"{esp} aparece {n} vezes na tabela em C")
    kanto = {"SPECIES_BULBASAUR", "SPECIES_CHARMANDER", "SPECIES_SQUIRTLE"}
    if kanto & set(especies):
        erros.append("um inicial de Kanto está nas bolas novas; ele já é objeto")
    return erros


# ---------------------------------------------------------------------------
# --confere: alcance e a separação da ala
# ---------------------------------------------------------------------------
def andavel(g, x, y, bloqueios=()):
    if not (0 <= x < len(g[0]) and 0 <= y < len(g)):
        return False
    if (x, y) in OBJETOS_PARADOS or (x, y) in bloqueios:
        return False
    return (g[y][x] >> 10) & 3 == 0


def alcance(g, inicio, bloqueios=()):
    vistos = {inicio}
    fila = collections.deque([inicio])
    while fila:
        x, y = fila.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n not in vistos and andavel(g, *n, bloqueios):
                vistos.add(n)
                fila.append(n)
    return vistos


def confere_alcance(g, bolas):
    erros = []
    # Durante a cena de escolha (VAR_MAP_SCENE 2), o gatilho de (5..7, 8) devolve
    # o jogador para cima: a conta é a do jogador que NÃO passa da fileira 8.
    cima = alcance(g, JOGADOR_DEPOIS_DA_CENA, bloqueios=GATILHOS)
    todas = [(x, y) for x, y, _ in bolas] + list(BOLAS_KANTO)
    sem_acesso = []
    for x, y in todas:
        if not any((x + dx, y + dy) in cima for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))):
            sem_acesso.append((x, y))
    if sem_acesso:
        erros.append(f"bolas que o jogador não alcança na cena de escolha: {sem_acesso}")
    # A ala não pode ter caminho até a porta que fuja dos gatilhos.
    baixo = alcance(g, PORTA, bloqueios=GATILHOS)
    ala = [c for c in baixo if c[0] >= LARGURA_ORIG]
    if ala:
        erros.append(f"a metade de baixo alcança a ala sem passar pelos gatilhos: {sorted(ala)[:5]}")
    # A sala original continua byte a byte.
    orig = grade_original()
    difs = [(x, y) for y in range(ALTURA_ORIG) for x in range(LARGURA_ORIG) if g[y][x] != orig[y][x]]
    if difs:
        erros.append(f"a sala original mudou em {len(difs)} células: {difs[:5]}")
    return erros, len(todas), len(cima)


# ---------------------------------------------------------------------------
# --render
# ---------------------------------------------------------------------------
def render(saida, escala=2, grade=None):
    from PIL import Image
    T = {"p": tiles_do_png(os.path.join(PRIMARIO, "tiles.png")),
         "s": tiles_do_png(os.path.join(TILESET, "tiles.png"))}
    P = {}
    for i in range(7):
        P[i] = le_pal(os.path.join(PRIMARIO, "palettes/%02d.pal" % i))
    for i in range(7, 13):
        P[i] = le_pal(os.path.join(TILESET, "palettes/%02d.pal" % i))
    M = {"p": le_metatiles(os.path.join(PRIMARIO, "metatiles.bin")),
         "s": le_metatiles(os.path.join(TILESET, "metatiles.bin"))}

    def desenha(img, ent, ox, oy, transparente):
        idx, hf, vf, pl = ent & 0x3FF, (ent >> 10) & 1, (ent >> 11) & 1, ent >> 12
        t = T["p"][idx] if idx < BASE_SECUNDARIO else T["s"][idx - BASE_SECUNDARIO]
        for y in range(8):
            for x in range(8):
                v = t[(7 - y if vf else y) * 8 + (7 - x if hf else x)]
                if v == 0 and transparente:
                    continue
                img.putpixel((ox + x, oy + y), P[pl][v])

    def metatile(mid):
        img = Image.new("RGB", (16, 16))
        e = M["p"][mid] if mid < BASE_SECUNDARIO else M["s"][mid - BASE_SECUNDARIO]
        for k in range(8):
            desenha(img, e[k], (k % 2) * 8, ((k % 4) // 2) * 8, k >= 4)
        return img

    if grade is None:
        lay = [l for l in json.load(open(LAYOUTS))["layouts"] if l["id"] == LAYOUT_ID][0]
        grade = le_grade(MAPA_BIN, lay["width"], lay["height"])
    h, w = len(grade), len(grade[0])
    img = Image.new("RGB", (w * 16, h * 16))
    cache = {}
    for y in range(h):
        for x in range(w):
            mid = grade[y][x] & 0x3FF
            if mid not in cache:
                cache[mid] = metatile(mid)
            img.paste(cache[mid], (x * 16, y * 16))
    # As três bolas de Kanto são OBJETO; o render as desenha como o jogo, com os
    # mesmos pixels do sprite, para a prévia mostrar as 52.
    bola = pixels_da_bola()
    for bx, by in BOLAS_KANTO:
        for (x, y), cor in bola.items():
            img.putpixel((bx * 16 + x, by * 16 + y), cor)
    if escala != 1:
        img = img.resize((w * 16 * escala, h * 16 * escala), Image.NEAREST)
    img.save(saida)
    return img


# ---------------------------------------------------------------------------
# --roteiro: passeio pelas 49 bolas novas
# ---------------------------------------------------------------------------
DIRECOES = {(0, -1): "UP", (0, 1): "DOWN", (-1, 0): "LEFT", (1, 0): "RIGHT"}


def caminho(g, de, para, bloqueios):
    anterior = {de: None}
    fila = collections.deque([de])
    while fila:
        c = fila.popleft()
        if c == para:
            break
        for d in DIRECOES:
            n = (c[0] + d[0], c[1] + d[1])
            if n not in anterior and andavel(g, *n, bloqueios):
                anterior[n] = c
                fila.append(n)
    assert para in anterior, f"sem caminho de {de} a {para}"
    passos = []
    c = para
    while anterior[c] is not None:
        p = anterior[c]
        passos.append((c[0] - p[0], c[1] - p[1]))
        c = p
    return passos[::-1]


def comprime(passos):
    out = []
    for d in passos:
        if out and out[-1][0] == d:
            out[-1][1] += 1
        else:
            out.append([d, 1])
    return [f"16:{DIRECOES[d]}*{n}" if n > 1 else f"16:{DIRECOES[d]}" for d, n in out]


def roteiro_passeio(g, bolas, inicio=PORTA):
    """Anda da porta até cada bola nova, de baixo para cima por fileira, olha para
    o tampo e aperta A; fecha o texto com B."""
    alvos = sorted(((x, y) for x, y, _ in bolas), key=lambda c: (c[1], c[0]))
    partes = ["240:NADA"]
    pos = inicio
    for x, y in alvos:
        pe = (x, y + 1)
        partes += comprime(caminho(g, pos, pe, AJUDANTES))
        partes += ["16:UP", "30:NADA", "12:A", "90:NADA", "12:B", "40:NADA", "12:B", "40:NADA"]
        pos = pe
    return ",".join(partes)


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--arte", action="store_true")
    ap.add_argument("--mapa", action="store_true")
    ap.add_argument("--confere", action="store_true")
    ap.add_argument("--render")
    ap.add_argument("--escala", type=int, default=2)
    ap.add_argument("--roteiro", action="store_true")
    a = ap.parse_args()
    if a.arte:
        erros = aplica_arte(True)
        print("\n".join(erros) if erros else "arte em dia")
    if a.mapa:
        erros = aplica_mapa(True)
        print("\n".join(erros) if erros else "mapa em dia")
    if a.confere:
        erros = aplica_arte(False) + aplica_mapa(False)
        bolas = bolas_da_fonte()
        lay = [l for l in json.load(open(LAYOUTS))["layouts"] if l["id"] == LAYOUT_ID][0]
        g = le_grade(MAPA_BIN, lay["width"], lay["height"])
        e2, n, alc = confere_alcance(g, bolas)
        erros += e2
        for e in erros:
            print("FALHA:", e)
        if not erros:
            print(f"VERDE: arte e mapa batem com src/lab_iniciais.c; {n} bolas alcançáveis "
                  f"na cena de escolha ({alc} células andáveis sem passar pelos gatilhos); "
                  "a ala não chega à porta por fora dos gatilhos; a sala original igual "
                  f"byte a byte à de {COMMIT_ORIGINAL}")
        return 1 if erros else 0
    if a.render:
        render(a.render, a.escala)
        print("render:", a.render)
    if a.roteiro:
        bolas = bolas_da_fonte()
        lay = [l for l in json.load(open(LAYOUTS))["layouts"] if l["id"] == LAYOUT_ID][0]
        g = le_grade(MAPA_BIN, lay["width"], lay["height"])
        print(roteiro_passeio(g, bolas))
    return 0


if __name__ == "__main__":
    sys.exit(main())
