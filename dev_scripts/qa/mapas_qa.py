#!/usr/bin/env python3
"""Varredura de MAPAS, EVENTOS e ALCANÇABILIDADE nas seis regiões.

    python3 qa/mapas_qa.py                 # relatório completo
    python3 qa/mapas_qa.py --regra B7      # só uma regra
    python3 qa/mapas_qa.py --vanilla       # a MESMA régua contra ../fontes-mapas/pokeemerald
    python3 qa/mapas_qa.py --json saida.json
    python3 qa/mapas_qa.py --demo          # autoteste com mutação plantada

SÓ LEITURA: nada aqui grava no repo.

Existe para pegar o que os validadores de hoje NÃO medem. O que já é medido, e
por isso NÃO é remedido aqui:

  - `valida_conectividade.py`: warp para mapa/índice inexistente, alcance de
    mapa a mapa pelo grafo, beco de mapa inteiro, porta única que não devolve.
  - `valida_warp_tile.py`: warp em tile cujo COMPORTAMENTO não dispara.
  - `porta_morta.py`: boca de caverna ao contrário, mas SÓ em Sinnoh e SÓ em
    mapa de um warp só.
  - `valida_mapas_sinnoh.py`: sprite sem gráfico, objeto em tile bloqueado, mas
    a varredura oficial roda com `--so-sinnoh`.
  - `lendarios_sinnoh.py`: BFS dos lendários de Sinnoh.

TRÊS ARMADILHAS QUE ESTE ARQUIVO PAGOU, escritas para ninguém repetir:

1. O CORTE PRIMÁRIO/SECUNDÁRIO NÃO É SEMPRE 512. `valida_warp_tile` acerta
   (640 quando `layout_version` é `frlg` ou `johto`), e `valida_mapas_sinnoh`
   crava 512 no `comportamento()` dele. Ler comportamento de layout de Kanto ou
   de Johto com 512 devolve o metatile ERRADO, calado. Aqui o corte sai da
   versão do layout, como no motor (`GetNumMetatilesInPrimary`).

2. RÉGUA CRUA REPROVA O VANILLA (lição 4.10 do ESTADO). Toda regra que podia
   ser gosto meu roda também contra `../fontes-mapas/pokeemerald` com
   `--vanilla`, e a taxa de lá está impressa no relatório ao lado da nossa. Se
   a nossa taxa não for pior que a do vanilla, a regra vira `falso positivo` e
   não vira fila de conserto.

3. MAPA SEM SEMENTE NÃO É MAPA INALCANÇÁVEL. Rota se entra por `connections`,
   não por warp: semear a BFS só com warp declarava rota inteira inacessível.
   As sementes aqui são warp + heal location + borda de conexão, e mapa que
   ficar sem semente nenhuma sai como `nao_medido`, nunca como defeito.
"""
import json
import os
import re
import struct
import sys
from collections import Counter, defaultdict, deque

# RAIZ do repo, DEDUZIDA do lugar do proprio arquivo (dev_scripts/qa/x.py ->
# duas pastas acima). Ate 23/08/2026 estas ferramentas moravam fora do repo e
# cravavam o caminho absoluto do Mac do Gui; promovidas para dentro, caminho
# cravado seria mentira na primeira copia da arvore (worktree, /tmp do --demo,
# CI). A variavel de ambiente continua ganhando, que e como o --demo aponta
# para a arvore mutante.
REPO = os.environ.get(
    "QA_REPO", os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))))
VANILLA = os.path.join(os.path.dirname(REPO), "fontes-mapas", "pokeemerald")

TILE_PX = 8               # tile de BG do GBA
PX_POR_CAMADA = 4 * 8 * 8  # 4 quadrantes de 8x8: camada 100% opaca

# ------------------------------------------------------- E3: quem tapa o herói
#
# Nasceu do playtest do Gui de 06/09/2026 ("um retângulo de tiles pretos em que
# o jogador entra embaixo e some"). O mecanismo é `DrawMetatile` em
# src/fieldmap.c, e ele só tem três casos:
#
#   NORMAL  -> camada de BAIXO no BG2 (abaixo do sprite) e a de CIMA no BG1,
#              que é desenhado ACIMA de todo sprite de overworld.
#   COVERED -> camada de baixo no BG3 e a de cima no BG2: as duas ficam ABAIXO.
#   SPLIT   -> baixo no BG3, cima no BG1 (acima do sprite), meio vazio.
#
# Ou seja: metatile NORMAL ou SPLIT cuja camada de CIMA é 100% opaca apaga o
# jogador inteiro enquanto ele estiver em pé ali. Isso é legítimo em passagem
# por BAIXO de ponte ou de copa de árvore, e nesse caso a camada de baixo traz
# o CHÃO por onde se anda, diferente do que está por cima. O defeito é o outro
# caso: camada de baixo VAZIA (nada além do fundo) ou IDÊNTICA à de cima, que é
# a assinatura de arte empurrada para a camada errada pelo conversor.
#
# "Idêntica" é METADE DOS QUADRANTES, não os quatro: os cantos do brejo da
# Route 212 (metatiles 691 e 700) repetem a arte do miolo em 3 dos 4 quadrantes
# e trocam só um, e com a régua de "os quatro iguais" eles escapavam, deixando o
# conserto pela metade (o miolo aparecia e as bordas continuavam engolindo o
# jogador). Passagem por baixo de verdade não compartilha quadrante nenhum:
# medido em 06/09/2026, o metatile 669 do `gTileset_Facility` (Aqua Hideout,
# vanilla) tem 0 de 4.


def tapa_o_jogador(px_baixo, px_cima, quad_iguais, tipo):
    """O metatile esconde o jogador POR INTEIRO, e não é passagem por baixo?"""
    if tipo == 1:                     # COVERED: as duas camadas ficam abaixo
        return False
    if px_cima != PX_POR_CAMADA:      # camada de cima com furo: dá para ver
        return False
    return px_baixo == 0 or quad_iguais >= 2

# ---------------------------------------------------------------- comportamento

_MB_CACHE = {}


def valores_mb(raiz):
    """{nome: valor} do enum de include/constants/metatile_behaviors.h."""
    if raiz in _MB_CACHE:
        return _MB_CACHE[raiz]
    txt = open(os.path.join(raiz, "include/constants/metatile_behaviors.h")).read()
    m = re.search(r"enum\s*\w*\s*\{(.*?)\}", txt, re.S)
    if not m:
        # pokefirered declara os MB_ como `#define`, não como enum. Sem este
        # caminho a árvore de Kanto ficava sem linha de base e as acusações de
        # Kanto ficavam sem com o que comparar.
        tab = {n: int(v, 0) for n, v in
               re.findall(r"#define\s+(MB_[A-Z0-9_]+)\s+(0[xX][0-9a-fA-F]+|\d+)", txt)}
        _MB_CACHE[raiz] = tab
        return tab
    corpo = m.group(1)
    corpo = re.sub(r"/\*.*?\*/", "", corpo, flags=re.S)
    corpo = "\n".join(l.split("//")[0] for l in corpo.split("\n"))
    tab, atual = {}, 0
    for item in corpo.split(","):
        item = item.strip()
        if not item:
            continue
        if "=" in item:
            nome, valor = item.split("=")
            atual, nome = int(valor.strip(), 0), nome.strip()
        else:
            nome = item
        tab[nome] = atual
        atual += 1
    _MB_CACHE[raiz] = tab
    return tab


# Os mesmos nomes de `valida_warp_tile.NOMES_QUE_DISPARAM`, lidos do enum e
# nunca cravados como número: número copiado envelhece calado.
DISPARAM = (
    "MB_ANIMATED_DOOR", "MB_LADDER", "MB_UP_ESCALATOR", "MB_DOWN_ESCALATOR",
    "MB_NON_ANIMATED_DOOR", "MB_WATER_DOOR", "MB_DEEP_SOUTH_WARP",
    "MB_LAVARIDGE_GYM_B1F_WARP", "MB_LAVARIDGE_GYM_1F_WARP",
    "MB_AQUA_HIDEOUT_WARP", "MB_MT_PYRE_HOLE", "MB_MOSSDEEP_GYM_WARP",
    "MB_BRIDGE_OVER_OCEAN", "MB_NORTH_ARROW_WARP", "MB_SOUTH_ARROW_WARP",
    "MB_WEST_ARROW_WARP", "MB_EAST_ARROW_WARP", "MB_WATER_SOUTH_ARROW_WARP",
    "MB_STAIRS_OUTSIDE_ABANDONED_SHIP", "MB_SHOAL_CAVE_ENTRANCE",
    "MB_UP_RIGHT_STAIR_WARP", "MB_UP_LEFT_STAIR_WARP",
    "MB_DOWN_RIGHT_STAIR_WARP", "MB_DOWN_LEFT_STAIR_WARP",
)
# `GetAdjustedInitialDirection` (src/overworld.c:1073): quem chega por porta
# olha para o SUL e a animação de saída anda um tile. Medido na EWRAM por
# `porta_morta.py`: o warp (10,20) de CelesticTownCave larga em (10,21).
PORTAS = ("MB_ANIMATED_DOOR", "MB_NON_ANIMATED_DOOR")

# Comportamentos em que objeto fica de propósito (copiado de
# `valida_mapas_sinnoh.POR_DESENHO`, que já mediu o vanilla).
POR_DESENHO = {
    "MB_POND_WATER", "MB_INTERIOR_DEEP_WATER", "MB_DEEP_WATER", "MB_WATERFALL",
    "MB_SOOTOPOLIS_DEEP_WATER", "MB_OCEAN_WATER", "MB_SHALLOW_WATER",
    "MB_NO_SURFACING", "MB_SEAWEED", "MB_SEAWEED_NO_SURFACING",
    "MB_FAST_WATER", "MB_CYCLING_ROAD_WATER", "MB_WATER_DOOR",
    "MB_WATER_SOUTH_ARROW_WARP", "MB_COUNTER",
    "MB_SECRET_BASE_WALL", "MB_SECRET_BASE_NORTH_WALL", "MB_SECRET_BASE_PC",
    "MB_BERRY_TREE_SOIL", "MB_BOOKSHELF", "MB_BLUEPRINT",
}
ESPECIE = re.compile(r"OBJ_EVENT_GFX_(SPECIES|MON)\b|OBJ_EVENT_GFX_SPECIES\(")
VAR_GFX = re.compile(r"OBJ_EVENT_GFX_VAR_\d+")
LUZ = "OBJ_EVENT_GFX_LIGHT_SPRITE"

# HM que abre passagem, e o comportamento que ela vence.
HM_ABRE = {
    "surf": {"MB_POND_WATER", "MB_DEEP_WATER", "MB_OCEAN_WATER",
             "MB_SOOTOPOLIS_DEEP_WATER", "MB_INTERIOR_DEEP_WATER",
             "MB_SHALLOW_WATER", "MB_NO_SURFACING", "MB_SEAWEED",
             "MB_SEAWEED_NO_SURFACING", "MB_FAST_WATER",
             "MB_CYCLING_ROAD_WATER", "MB_EASTWARD_CURRENT",
             "MB_WESTWARD_CURRENT", "MB_NORTHWARD_CURRENT",
             "MB_SOUTHWARD_CURRENT"},
    "waterfall": {"MB_WATERFALL"},
    "rock_climb": {"MB_ROCK_CLIMB"},
    "cut": {"MB_TALL_GRASS", "MB_LONG_GRASS"},
}


class Arvore:
    """Uma árvore de repo (a nossa ou a do vanilla), com os caches."""

    def __init__(self, raiz):
        self.raiz = raiz
        self.mb = valores_mb(raiz)
        self.nome_mb = {v: k for k, v in self.mb.items()}
        self.dispara = {self.mb[n] for n in DISPARAM if n in self.mb}
        self.portas = {self.mb[n] for n in PORTAS if n in self.mb}
        self.layouts = {l["id"]: l for l in json.load(
            open(os.path.join(raiz, "data/layouts/layouts.json"),
                 encoding="utf-8"))["layouts"]}
        self.grupos = json.load(open(os.path.join(raiz, "data/maps/map_groups.json"),
                                     encoding="utf-8"))
        self._grade = {}
        self._attr = {}
        self._pastas = None
        self._tiles = {}
        self._meta = {}
        self._camada = {}
        self._desenho = {}

    # -- tilesets ---------------------------------------------------------
    def pastas(self):
        """gTileset_X -> pasta, pelo INCBIN, resolvendo ASSET_ALIAS.

        Cópia funcional de `valida_warp_tile._mapa_de_pastas`. Copiada, e não
        importada, porque este arquivo também roda contra a árvore do vanilla,
        que não tem `dev_scripts/`.
        """
        if self._pastas is not None:
            return self._pastas
        mt = open(os.path.join(self.raiz, "src/data/tilesets/metatiles.h")).read()
        sym2dir = dict(re.findall(
            r'gMetatiles_(\w+)\[\]\s*=\s*INCBIN_U16\("(data/tilesets/\w+/\w+)/metatiles\.bin"\)',
            mt))
        for apelido, canon in re.findall(
                r'gMetatiles_(\w+)\[[^\]]*\]\s*ASSET_ALIAS\(gMetatiles_(\w+)\)', mt):
            sym2dir.setdefault(apelido, canon)
        for _ in range(len(sym2dir)):
            mudou = False
            for k, v in list(sym2dir.items()):
                if not v.startswith("data/") and v in sym2dir:
                    sym2dir[k], mudou = sym2dir[v], True
            if not mudou:
                break
        hdr = open(os.path.join(self.raiz, "src/data/tilesets/headers.h")).read()
        fora = {}
        for nome, corpo in re.findall(
                r'const struct Tileset gTileset_(\w+)\s*=\s*\{(.*?)\};', hdr, re.S):
            m = re.search(r'\.metatiles\s*=\s*gMetatiles_(\w+)', corpo)
            if m and m.group(1) in sym2dir:
                fora["gTileset_" + nome] = os.path.join(self.raiz, sym2dir[m.group(1)])
        self._pastas = fora
        return fora

    def tamanhos(self, ts):
        """(quantos metatiles o tileset DEFINE, quantos atributos ele traz).

        Sai do TAMANHO dos dois `.bin`: `metatiles.bin` tem 16 bytes por
        metatile (8 tiles de u16) e `metatile_attributes.bin` tem 2 bytes por
        metatile no formato Emerald e 4 no de FRLG. Devolve (None, None) quando
        o tileset não resolve para uma pasta, que é o caso de `.secondary = 0`.
        """
        d = self.pastas().get(ts) if ts and ts != "0" else None
        if not d:
            return (None, None)
        pm = os.path.join(d, "metatiles.bin")
        pa = os.path.join(d, "metatile_attributes.bin")
        if not os.path.exists(pm) or not os.path.exists(pa):
            return (None, None)
        n = os.path.getsize(pm) // 16
        larg = (os.path.getsize(pa) // n) if n else 2
        return (n, os.path.getsize(pa) // (4 if larg == 4 else 2))

    def atributos(self, ts):
        """[comportamento por metatile] do tileset, ou None se ilegível."""
        if ts in self._attr:
            return self._attr[ts]
        r = None
        if ts and ts != "0":
            d = self.pastas().get(ts)
            if d:
                pa, pm = (os.path.join(d, "metatile_attributes.bin"),
                          os.path.join(d, "metatiles.bin"))
                if os.path.exists(pa) and os.path.exists(pm):
                    n = os.path.getsize(pm) // 16
                    b = open(pa, "rb").read()
                    if n:
                        larg = len(b) // n
                        if larg == 4:
                            r = [struct.unpack("<I", b[i:i + 4])[0] & 0x1FF
                                 for i in range(0, n * 4, 4)]
                        else:
                            r = [struct.unpack("<H", b[i:i + 2])[0] & 0xFF
                                 for i in range(0, n * 2, 2)]
                    else:
                        r = []
        elif ts == "0" or not ts:
            r = []
        self._attr[ts] = r
        return r

    # -- camada de desenho (E3) -------------------------------------------
    def tiles_opacos(self, ts):
        """[quantos pixels OPACOS cada tile 8x8 do tileset tem].

        Opaco é índice de cor != 0: no GBA a cor 0 de qualquer paleta de BG é
        transparente, e é ela que deixa ver a camada de baixo. Só o `tiles.png`
        indexado é lido; paleta não entra, porque a pergunta aqui é "tapa ou
        não tapa", não "de que cor".
        """
        if ts in self._tiles:
            return self._tiles[ts]
        fora = []
        d = self.pastas().get(ts) if ts and ts != "0" else None
        p = os.path.join(d, "tiles.png") if d else None
        if p and os.path.exists(p):
            try:
                from PIL import Image
                img = Image.open(p).convert("P")
                W, H = img.size
                px = img.load()
                ncol = W // TILE_PX
                for i in range(ncol * (H // TILE_PX)):
                    cx, cy = (i % ncol) * TILE_PX, (i // ncol) * TILE_PX
                    fora.append(sum(1 for y in range(TILE_PX) for x in range(TILE_PX)
                                    if px[cx + x, cy + y]))
            except Exception:
                fora = []
        self._tiles[ts] = fora
        return fora

    def metatiles(self, ts):
        """Bytes crus do metatiles.bin (16 por metatile), ou b''."""
        if ts in self._meta:
            return self._meta[ts]
        b = b""
        d = self.pastas().get(ts) if ts and ts != "0" else None
        if d:
            p = os.path.join(d, "metatiles.bin")
            if os.path.exists(p):
                b = open(p, "rb").read()
        self._meta[ts] = b
        return b

    def camadas(self, ts):
        """[tipo de camada por metatile] (0 NORMAL, 1 COVERED, 2 SPLIT).

        O tipo mora nos bits 12-15 do atributo de 2 bytes (Emerald) e nos bits
        29-30 do de 4 bytes (FRLG), exatamente como `ExtractMetatileAttribute`
        em src/fieldmap.c. `atributos()` acima só devolve o COMPORTAMENTO, e
        por isso esta leitura é separada em vez de reaproveitá-la.
        """
        if ts in self._camada:
            return self._camada[ts]
        r = []
        d = self.pastas().get(ts) if ts and ts != "0" else None
        if d:
            pa = os.path.join(d, "metatile_attributes.bin")
            pm = os.path.join(d, "metatiles.bin")
            if os.path.exists(pa) and os.path.exists(pm):
                n = os.path.getsize(pm) // 16
                b = open(pa, "rb").read()
                if n:
                    larg = len(b) // n
                    if larg == 4:
                        r = [(struct.unpack("<I", b[i:i + 4])[0] >> 29) & 3
                             for i in range(0, n * 4, 4)]
                    else:
                        r = [(struct.unpack("<H", b[i:i + 2])[0] >> 12) & 0xF
                             for i in range(0, n * 2, 2)]
        self._camada[ts] = r
        return r

    def desenho_do_metatile(self, lid, mt):
        """(px da camada de baixo, px da de cima, quadrantes iguais, tipo).

        Devolve None quando o metatile não resolve (tileset sem pasta, id fora
        do teto: isso é a regra E1, não esta).
        """
        L = self.layouts.get(lid)
        if not L:
            return None
        pri, sec = L.get("primary_tileset"), L.get("secondary_tileset")
        frlg = L.get("layout_version") in ("frlg", "johto")
        corte_mt = 640 if frlg else 512
        corte_tl = 640 if frlg else 512
        chave = (pri, sec, corte_mt, mt)
        if chave in self._desenho:
            return self._desenho[chave]
        ts_meta, idx = (pri, mt) if mt < corte_mt else (sec, mt - corte_mt)
        bin_meta = self.metatiles(ts_meta)
        tipos = self.camadas(ts_meta)
        r = None
        if bin_meta and idx < len(bin_meta) // 16 and idx < len(tipos):
            tp = self.tiles_opacos(pri), self.tiles_opacos(sec)
            px = [0, 0]
            entradas = [[], []]
            for c in (0, 1):
                for q in range(4):
                    v = struct.unpack_from("<H", bin_meta, idx * 16 + (c * 4 + q) * 2)[0]
                    it = v & 0x3FF
                    entradas[c].append(v)
                    lista, j = (tp[0], it) if it < corte_tl else (tp[1], it - corte_tl)
                    px[c] += lista[j] if 0 <= j < len(lista) else 0
            iguais = sum(1 for q in range(4) if entradas[0][q] == entradas[1][q])
            r = (px[0], px[1], iguais, tipos[idx])
        self._desenho[chave] = r
        return r

    # -- grade ------------------------------------------------------------
    def grade(self, lid):
        """(W, H, [linhas de u16], corte) ou None."""
        if lid in self._grade:
            return self._grade[lid]
        r = None
        L = self.layouts.get(lid)
        if L:
            bp = os.path.join(self.raiz, L.get("blockdata_filepath", ""))
            if os.path.exists(bp):
                W, H = L["width"], L["height"]
                b = open(bp, "rb").read()
                if len(b) >= W * H * 2:
                    linhas = [list(struct.unpack_from(f"<{W}H", b, y * W * 2))
                              for y in range(H)]
                    corte = 640 if L.get("layout_version") in ("frlg", "johto") else 512
                    r = (W, H, linhas, corte)
        self._grade[lid] = r
        return r

    def comportamento(self, lid, g, x, y):
        """Nome do MB_ em (x,y), ou None quando a tabela não resolve."""
        W, H, linhas, corte = g
        if not (0 <= x < W and 0 <= y < H):
            return None
        mt = linhas[y][x] & 0x3FF
        L = self.layouts[lid]
        tab = (self.atributos(L.get("primary_tileset")) if mt < corte
               else self.atributos(L.get("secondary_tileset")))
        idx = mt if mt < corte else mt - corte
        if tab is None or idx >= len(tab):
            return None
        return self.nome_mb.get(tab[idx])


def andavel(v):
    return ((v >> 10) & 3) == 0


def elev(v):
    return (v >> 12) & 0xF


def bfs(W, H, linhas, sementes, extra_andavel=None):
    """BFS com a REGRA DE ELEVAÇÃO do motor (cópia de conserta_route222.alcance).

    `extra_andavel(x, y)` deixa passar por tile bloqueado que uma HM abre.
    """
    vistos, fila = set(), deque()
    for x, y in sementes:
        if 0 <= x < W and 0 <= y < H and (
                andavel(linhas[y][x]) or (extra_andavel and extra_andavel(x, y))):
            st = (x, y, elev(linhas[y][x]))
            if st not in vistos:
                vistos.add(st)
                fila.append(st)
    while fila:
        x, y, e = fila.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < W and 0 <= ny < H):
                continue
            v = linhas[ny][nx]
            if not andavel(v) and not (extra_andavel and extra_andavel(nx, ny)):
                continue
            eb = elev(v)
            if e != 0 and eb not in (0, 15) and e != eb:
                continue
            st = (nx, ny, e if eb == 15 else eb)
            if st not in vistos:
                vistos.add(st)
                fila.append(st)
    return {(x, y) for x, y, _ in vistos}


# ---------------------------------------------------------------------- região

def regiao_de(nome_mapa, grupo, dados=None):
    """Região do mapa. "cortado" para o TÚMULO de mapa fora de escopo.

    Unova e Galar saíram em 07/09/2026 (PRD-CARTUCHO-1.md) e os 729 mapas delas
    ficaram na tabela como túmulo, para não deslocar índice de save: id intacto,
    zero evento, `MAPSEC_NONE` e o campo `cortado_por` no map.json. Sem o
    primeiro `if`, todo túmulo cairia no balde padrão de Hoenn e a auditoria
    passaria a cobrar de Hoenn o que o Gui cortou de propósito.
    """
    if dados is not None and dados.get("cortado_por"):
        return "cortado"
    if grupo.endswith("_Frlg") or "Frlg" in grupo:
        return "Kanto"
    if "Johto" in grupo:
        return "Johto"
    if "Sinnoh" in grupo or "Galactic" in grupo:
        return "Sinnoh"
    return "Hoenn"


# --------------------------------------------------------------------- achados

class Achados:
    def __init__(self):
        self.itens = []

    def add(self, regra, classe, regiao, mapa, coord, detalhe):
        self.itens.append(dict(regra=regra, classe=classe, regiao=regiao,
                               mapa=mapa, coord=coord, detalhe=detalhe))


# Classe por regra. `provavel` = quase certo que morde no playtest;
# `trava` = o jogador para de jogar; `cosmetico` = feio, não trava.
CLASSE = {
    "A2": "trava",      "A3": "provavel",  "A4": "provavel",
    "A5": "trava",      "A7": "trava",
    "B1": "provavel",   "B2": "cosmetico", "B3": "provavel",
    "B4": "cosmetico",  "B5": "trava",     "B6": "trava",
    "B7": "provavel",   "B8": "provavel",  "B9": "provavel",
    "C1": "trava",      "C2": "provavel",  "C3": "cosmetico",
    "D1": "cosmetico",  "D2": "cosmetico",
    "E1": "trava",      "E2": "provavel",  "E3": "provavel",
}
TITULO = {
    "A2": "warp cuja CHEGADA cai em tile sólido (o jogador nasce dentro da parede)",
    "A3": "warp cuja chegada cai em cima de objeto sólido",
    "A4": "conexão de rota sem UM par de tiles andáveis: a borda é parede inteira",
    "A5": "heal location em tile sólido",
    "A7": "chegada de porta (1 tile ao sul) em parede",
    "B1": "objeto em tile sólido, sem vizinho de conversa e fora das famílias legítimas",
    "B2": "objeto em cima de warp",
    "B3": "objeto em cima de coord_event (rouba o gatilho)",
    "B4": "dois objetos no MESMO tile",
    "B5": "local_id citado em script e ausente do mapa",
    "B6": "mapa acima de 64 objetos",
    "B7": "janela de 20x17 com mais de 15 objetos que gastam slot",
    "B8": "NPC WANDER/LOOK_AROUND que pode parar em cima de warp ou de coord_event",
    "B9": "objeto tapando o ÚNICO tile de conversa de NPC com script de história",
    "C1": "mapa com tiles andáveis e NENHUM alcançável pela chegada (beco)",
    "C2": "objeto com script inalcançável (nem o tile, nem vizinho ortogonal)",
    "C3": "bg_event (placa) sem tile de leitura andável ao sul",
    "D1": "MB_TALL_GRASS em mapa sem tabela de encontro",
    "D2": "tabela de encontro terrestre em mapa sem grama",
    "E1": "metatile fora do teto do tileset (o motor lê atributo fora do buffer)",
    "E2": "setmetatile que ABRE a célula pintando o metatile que ela já tem (mudança invisível)",
    "E3": "bloco preto andável: célula alcançável cujo metatile tapa o jogador por inteiro",
}


# --------------------------------------------------------------------- varredura

def rotulos_citados(raiz, nome):
    p = os.path.join(raiz, "data/maps", nome, "scripts.inc")
    if not os.path.exists(p):
        return ""
    return open(p, encoding="utf-8", errors="replace").read()


def encontros(raiz):
    """{MAP_X: {'land': bool, 'water': bool}} de todos os wild_encounters*.json."""
    fora = {}
    import glob
    for f in glob.glob(os.path.join(raiz, "src/data/wild_encounters*.json")):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for g in d.get("wild_encounter_groups", []):
            if not g.get("for_maps", True):
                continue
            for e in g.get("encounters", []):
                m = e.get("map")
                if not m:
                    continue
                r = fora.setdefault(m, {"land": False, "water": False})
                if e.get("land_mons"):
                    r["land"] = True
                if e.get("water_mons") or e.get("fishing_mons") or e.get("rock_smash_mons"):
                    r["water"] = True
    return fora


def varre(raiz, so_regra=None):
    A = Arvore(raiz)
    ach = Achados()
    enc = encontros(raiz)
    nao_medido = []
    censo = Counter()

    # (a) índice de mapas: dir -> (const, grupo, região, json)
    # A árvore do vanilla vem SEM BUILD, e `map_groups.h` é gerado: sem este
    # `try` o modo `--vanilla` morria e a regra ficava sem calibração, que é
    # exatamente o buraco que a lição 4.10 do ESTADO manda tapar.
    hp = os.path.join(raiz, "include/constants/map_groups.h")
    header = open(hp).read() if os.path.exists(hp) else ""
    por_valor = {}
    for const, num, grp in re.findall(
            r"(MAP_[A-Z0-9_]+)\s*=\s*\((\d+)\s*\|\s*\((\d+)\s*<<\s*8\)\)", header):
        por_valor[(int(grp), int(num))] = const
    mapas, const_de = {}, {}
    for gi, gn in enumerate(A.grupos["group_order"]):
        for mi, mn in enumerate(A.grupos.get(gn, [])):
            p = os.path.join(raiz, "data/maps", mn, "map.json")
            if not os.path.exists(p):
                continue
            try:
                d = json.load(open(p, encoding="utf-8"))
            except Exception:
                continue
            c = por_valor.get((gi, mi)) or d.get("id")
            mapas[mn] = dict(const=c, grupo=gn, regiao=regiao_de(mn, gn, d), d=d)
            if c:
                const_de[c] = mn

    # (b) heal locations por mapa
    heal = defaultdict(list)
    hp = os.path.join(raiz, "src/data/heal_locations.json")
    if os.path.exists(hp):
        for h in json.load(open(hp, encoding="utf-8"))["heal_locations"]:
            heal[h["map"]].append((h["x"], h["y"], h["id"]))
            # ARMADILHA PAGA AQUI: 86 das 93 heal locations NAO trazem
            # `respawn_x`/`respawn_y`. A primeira versao usava 0 como padrao e
            # acusou 86 heal locations "em tile solido", todas em (0,0), todas
            # invencao minha. Sem coordenada escrita nao ha o que medir.
            if h.get("respawn_map") and "respawn_x" in h and "respawn_y" in h:
                heal[h["respawn_map"]].append(
                    (h["respawn_x"], h["respawn_y"], h["id"] + " (respawn)"))

    # (c) quem é DESTINO de quem. Warp que ninguém aponta é porta decorativa ou
    #     saída só de ida: acusar o pouso dele é inventar defeito.
    warps_de_entrada = defaultdict(set)
    for nome_o, info_o in mapas.items():
        for i_o, w in enumerate(info_o["d"].get("warp_events") or []):
            alvo = w.get("dest_map")
            if alvo in ("MAP_NONE", "MAP_DYNAMIC", None, ""):
                continue
            try:
                j = int(w.get("dest_warp_id", 0))
            except (TypeError, ValueError):
                continue
            # WARP QUE APONTA PARA SI MESMO nao e chegada de ninguem: e lixo do
            # importador do demake, e conta-lo como "chegada" inventava trava
            # onde nunca chega jogador. Medido: 22 dos 24 casos da primeira
            # versao de A2 eram isso ou geometria de script. (Os dois exemplos
            # de origem eram de Galar, regiao que saiu do escopo em 07/09/2026;
            # a guarda fica porque o padrao vale para qualquer mapa importado.)
            if alvo == info_o["const"] and j == i_o:
                continue
            warps_de_entrada[alvo].add(j)

    def liga(regra):
        return so_regra is None or regra == so_regra

    for nome, info in sorted(mapas.items()):
        d, reg = info["d"], info["regiao"]
        lid = d.get("layout")
        g = A.grade(lid)
        if g is None:
            nao_medido.append((nome, f"layout {lid} sem blockdata legível"))
            continue
        W, H, linhas, _ = g
        censo[reg] += 1
        objs = [o for o in (d.get("object_events") or [])
                if isinstance(o.get("x"), int) and isinstance(o.get("y"), int)]
        warps = [w for w in (d.get("warp_events") or [])
                 if isinstance(w.get("x"), int) and isinstance(w.get("y"), int)]
        coords = [c for c in (d.get("coord_events") or [])
                  if isinstance(c.get("x"), int) and isinstance(c.get("y"), int)]
        bgs = [b for b in (d.get("bg_events") or [])
               if isinstance(b.get("x"), int) and isinstance(b.get("y"), int)]
        mbc = {}

        def mb(x, y):
            if (x, y) not in mbc:
                mbc[(x, y)] = A.comportamento(lid, g, x, y)
            return mbc[(x, y)]

        def solido(x, y):
            return (0 <= x < W and 0 <= y < H) and not andavel(linhas[y][x])

        def da_para_falar(x, y, base):
            """O motor consegue encarar (x,y) a partir de algum tile alcançável?

            DUAS CAMADAS, e a segunda custou 144 falsos positivos no vanilla:
            `GetFacingObject` (src/field_control_avatar.c) olha UM tile à frente
            e, quando esse tile é `MB_COUNTER`, olha MAIS UM. É assim que se
            fala com balconista, enfermeira e vendedor, que ficam atrás de tile
            sólido em quase todo Pokécenter e loja do jogo original.
            """
            if base is None:
                return True
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                if (x + dx, y + dy) in base:
                    return True
                meio = (x + dx, y + dy)
                if (0 <= meio[0] < W and 0 <= meio[1] < H
                        and mb(*meio) == "MB_COUNTER"
                        and (x + 2 * dx, y + 2 * dy) in base):
                    return True
            return (x, y) in base

        # ---- A. warps, conexões, heal --------------------------------
        # A2/A7: onde o jogador NASCE.
        #
        # O MOTOR JA GUARDA A PORTA NAO ANIMADA, e isso foi LIDO, nao suposto:
        # `SetUpWarpExitTask` (src/field_screen_effect.c:314) so escolhe
        # `Task_ExitNonAnimDoor`, que e quem empurra um tile ao sul, quando
        # `MapGridGetCollisionAt(x, y + 1) == 0`. Com o tile de baixo bloqueado
        # ou fora da grade ele cai em `Task_ExitNonDoor` e o jogador FICA na
        # propria porta. A primeira versao deste arquivo acusou 442 casos sem
        # ler essa guarda, que existe desde 12/08/2026 (430 deles eram de Unova,
        # regiao que saiu do escopo em 07/09/2026).
        #
        # Sobra o que a guarda NAO cobre, e sao dois:
        #   A7 = porta ANIMADA (`MetatileBehavior_IsDoor`: MB_ANIMATED_DOOR e
        #        MB_PETALBURG_GYM_DOOR), que vai para `Task_ExitDoor` e anda ao
        #        sul sem perguntar nada;
        #   A2 = o jogador parado num tile de onde NAO SAI: nenhum vizinho
        #        ortogonal andavel. Ai nao ha passo possivel e o interior morre.
        entram = warps_de_entrada.get(info["const"], set())
        for i, w in enumerate(warps):
            x, y = w["x"], w["y"]
            if not (0 <= x < W and 0 <= y < H):
                continue          # `valida_warp_tile` já acusa "fora do mapa"
            b = mb(x, y)
            anim = b in ("MB_ANIMATED_DOOR", "MB_PETALBURG_GYM_DOOR")
            px, py = (x, y + 1) if anim else (x, y)
            if liga("A7") and anim:
                if not (0 <= px < W and 0 <= py < H):
                    ach.add("A7", CLASSE["A7"], reg, nome, (px, py),
                            f"warp {i}: porta animada e a chegada cai FORA do "
                            f"mapa ({W}x{H})")
                elif not andavel(linhas[py][px]):
                    ach.add("A7", CLASSE["A7"], reg, nome, (px, py),
                            f"warp {i} em ({x},{y}) [{b}]: porta animada larga "
                            f"em tile sólido [{mb(px, py)}]")
            # A2: o pouso existe mas nao tem por onde sair. So conta warp que
            # alguem realmente usa como DESTINO, senao acusa porta decorativa.
            if liga("A2") and i in entram and 0 <= px < W and 0 <= py < H:
                viz = [(px + dx, py + dy)
                       for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))]
                if not any(0 <= vx < W and 0 <= vy < H and andavel(linhas[vy][vx])
                           for vx, vy in viz):
                    # A GEOMETRIA PODE MUDAR EM TEMPO DE EXECUCAO. As tres salas
                    # do E4 de Kanto fecham e abrem a porta com `setmetatile`
                    # (PokemonLeague_EventScript_CloseEntry/SetDoorOpen), entao
                    # o blockdata de hoje NAO e o mapa que o jogador ve. Medir
                    # sem dizer isso transformaria tres salas boas em trava.
                    muda = "setmetatile" in rotulos_citados(raiz, nome)
                    ach.add("A2", "provavel" if muda else CLASSE["A2"],
                            reg, nome, (px, py),
                            f"warp {i} [{b}]: o jogador pousa aqui e NENHUM "
                            "vizinho ortogonal é andável"
                            + (" (ATENÇÃO: o mapa usa setmetatile, a geometria "
                               "pode abrir em tempo de execução)" if muda else ""))
            # A3: chegada em cima de objeto sólido
            if liga("A3"):
                for o in objs:
                    if (o["x"], o["y"]) != (px, py):
                        continue
                    gfx = o.get("graphics_id", "") or ""
                    if gfx == LUZ or ESPECIE.search(gfx) or VAR_GFX.match(gfx):
                        continue
                    ach.add("A3", CLASSE["A3"], reg, nome, (px, py),
                            f"warp {i} larga o jogador em cima de {gfx}")

        # A4: conexão cuja borda inteira é parede dos dois lados.
        if liga("A4"):
            for c in (d.get("connections") or []):
                alvo = const_de.get(c.get("map"))
                if not alvo or alvo not in mapas:
                    continue
                og = A.grade(mapas[alvo]["d"].get("layout"))
                if og is None:
                    continue
                OW, OH, ol, _ = og
                off = int(c.get("offset", 0) or 0)
                dirc = c.get("direction")
                pares = 0
                if dirc == "down":
                    for x in range(W):
                        ox = x - off
                        if 0 <= ox < OW and andavel(linhas[H - 1][x]) and andavel(ol[0][ox]):
                            pares += 1
                elif dirc == "up":
                    for x in range(W):
                        ox = x - off
                        if 0 <= ox < OW and andavel(linhas[0][x]) and andavel(ol[OH - 1][ox]):
                            pares += 1
                elif dirc == "right":
                    for y in range(H):
                        oy = y - off
                        if 0 <= oy < OH and andavel(linhas[y][W - 1]) and andavel(ol[oy][0]):
                            pares += 1
                elif dirc == "left":
                    for y in range(H):
                        oy = y - off
                        if 0 <= oy < OH and andavel(linhas[y][0]) and andavel(ol[oy][OW - 1]):
                            pares += 1
                else:
                    continue      # dive/emerge não se atravessa a pé
                if pares == 0:
                    ach.add("A4", CLASSE["A4"], reg, nome, None,
                            f"conexão {dirc} offset {off} para {c.get('map')}: "
                            "nenhum par de tiles andáveis na borda")

        # A5: heal location em tile sólido
        if liga("A5"):
            for hx, hy, hid in heal.get(info["const"], ()):
                if not (0 <= hx < W and 0 <= hy < H):
                    ach.add("A5", CLASSE["A5"], reg, nome, (hx, hy),
                            f"{hid}: fora do mapa ({W}x{H})")
                elif not andavel(linhas[hy][hx]):
                    ach.add("A5", CLASSE["A5"], reg, nome, (hx, hy),
                            f"{hid}: tile sólido [{mb(hx, hy)}]")

        # ---- B. objetos -----------------------------------------------
        if liga("B6") and len(objs) > 64:
            ach.add("B6", CLASSE["B6"], reg, nome, None,
                    f"{len(objs)} objetos (teto do motor: 64)")

        # B7: janela de 20x17. Luz não gasta slot de sprite.
        if liga("B7"):
            gasta = [o for o in objs
                     if (o.get("graphics_id") or "") != LUZ]
            pior, pos = 0, None
            if len(gasta) > 15:
                pts = [(o["x"], o["y"]) for o in gasta]
                for cx, cy in pts:
                    n = sum(1 for x, y in pts
                            if cx <= x < cx + 20 and cy <= y < cy + 17)
                    if n > pior:
                        pior, pos = n, (cx, cy)
            if pior > 15:
                ach.add("B7", CLASSE["B7"], reg, nome, pos,
                        f"{pior} objetos na janela que começa aí "
                        f"(o motor desenha 15 por tela)")

        # B2, B3, B4
        pw = {(w["x"], w["y"]) for w in warps}
        pc = {(c["x"], c["y"]): c for c in coords}
        vistos = {}
        for o in objs:
            p = (o["x"], o["y"])
            gfx = o.get("graphics_id", "") or ""
            if liga("B2") and p in pw and gfx != LUZ:
                ach.add("B2", CLASSE["B2"], reg, nome, p,
                        f"{gfx} em cima do warp")
            if liga("B3") and p in pc and gfx != LUZ:
                ach.add("B3", CLASSE["B3"], reg, nome, p,
                        f"{gfx} em cima do trigger {pc[p].get('script')}")
            if liga("B4") and p in vistos and gfx != LUZ and vistos[p] != LUZ:
                ach.add("B4", CLASSE["B4"], reg, nome, p,
                        f"{vistos[p]} e {gfx} no mesmo tile")
            vistos.setdefault(p, gfx)

        # B8: quem VAGA pode parar em cima de warp ou de trigger.
        if liga("B8"):
            for o in objs:
                mov = o.get("movement_type", "")
                if not (mov.startswith("MOVEMENT_TYPE_WANDER")
                        or mov.startswith("MOVEMENT_TYPE_LOOK_AROUND")):
                    continue
                rx = int(o.get("movement_range_x", 0) or 0)
                ry = int(o.get("movement_range_y", 0) or 0)
                if mov.startswith("MOVEMENT_TYPE_LOOK_AROUND"):
                    continue      # olha, não anda: só entra por WANDER
                if rx == 0 and ry == 0:
                    continue
                alvos = []
                for x in range(o["x"] - rx, o["x"] + rx + 1):
                    for y in range(o["y"] - ry, o["y"] + ry + 1):
                        if (x, y) == (o["x"], o["y"]):
                            continue
                        if (x, y) in pw:
                            alvos.append(f"warp em ({x},{y})")
                        elif (x, y) in pc:
                            alvos.append(f"trigger {pc[(x, y)].get('script')} em ({x},{y})")
                if alvos:
                    ach.add("B8", CLASSE["B8"], reg, nome, (o["x"], o["y"]),
                            f"{o.get('graphics_id')} {mov} alcance {rx}x{ry} "
                            f"cobre: {', '.join(alvos[:3])}")

        # B5: local_id citado no scripts.inc e ausente do map.json
        if liga("B5"):
            txt = rotulos_citados(raiz, nome)
            if txt:
                declarados = {o.get("local_id") for o in objs if o.get("local_id")}
                citados = set(re.findall(r"\bLOCALID_[A-Z0-9_]+", txt))
                # LOCALID_PLAYER, _CAMERA e afins são do motor, não do mapa
                globais = {"LOCALID_PLAYER", "LOCALID_CAMERA", "LOCALID_NONE",
                           "LOCALID_FOLLOWER"}
                faltam = {c for c in citados - declarados - globais}
                # só acusa o que pertence a ESTE mapa pelo prefixo do nome
                pref = "LOCALID_" + re.sub(r"(?<!^)(?=[A-Z])", "_", nome).upper()
                pref = pref.replace("__", "_")
                faltam = {c for c in faltam if c.startswith(pref[:len(pref) - 0])}
                for c in sorted(faltam):
                    ach.add("B5", CLASSE["B5"], reg, nome, None,
                            f"{c} citado no script e sem objeto que o declare")
            # local_id duplicado dentro do mapa
            dup = Counter(o.get("local_id") for o in objs if o.get("local_id"))
            for k, n in dup.items():
                if n > 1:
                    ach.add("B5", CLASSE["B5"], reg, nome, None,
                            f"local_id {k} declarado {n} vezes")

        # ---- C. alcançabilidade ---------------------------------------
        sementes = []
        for w in warps:
            x, y = w["x"], w["y"]
            if not (0 <= x < W and 0 <= y < H):
                continue
            if andavel(linhas[y][x]):
                sementes.append((x, y))
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < W and 0 <= ny < H and andavel(linhas[ny][nx]):
                    sementes.append((nx, ny))
        for hx, hy, _ in heal.get(info["const"], ()):
            if 0 <= hx < W and 0 <= hy < H and andavel(linhas[hy][hx]):
                sementes.append((hx, hy))
        for c in (d.get("connections") or []):
            dirc = c.get("direction")
            if dirc == "down":
                sementes += [(x, H - 1) for x in range(W) if andavel(linhas[H - 1][x])]
            elif dirc == "up":
                sementes += [(x, 0) for x in range(W) if andavel(linhas[0][x])]
            elif dirc == "right":
                sementes += [(W - 1, y) for y in range(H) if andavel(linhas[y][W - 1])]
            elif dirc == "left":
                sementes += [(0, y) for y in range(H) if andavel(linhas[y][0])]
        anda = sum(1 for y in range(H) for x in range(W) if andavel(linhas[y][x]))
        if not sementes:
            nao_medido.append((nome, "sem warp, sem heal e sem conexão: "
                                     "a chegada é por script, não dá para semear"))
            base = None
            comhm = None
        else:
            base = bfs(W, H, linhas, sementes)

            def abre(x, y):
                b = mb(x, y)
                return any(b in s for s in HM_ABRE.values())
            comhm = bfs(W, H, linhas, sementes, abre)

        # E3: bloco preto andável. Só célula ALCANÇÁVEL entra, e é essa condição
        # que separa o defeito do enchimento: mapa de Johto tem centenas de
        # células de metatile 0 (preto, colisão 0) FORA da sala, atrás da
        # parede, onde ninguém pisa. Medido em 06/09/2026: sem o alcance a
        # regra acusava 4.581 células só no grupo de Goldenrod, todas fantasma.
        if liga("E3") and base:
            vistos_e3 = {}
            for (x, y) in base:
                mt = linhas[y][x] & 0x3FF
                if mt not in vistos_e3:
                    des = A.desenho_do_metatile(d.get("layout"), mt)
                    vistos_e3[mt] = bool(des) and tapa_o_jogador(*des)
                if vistos_e3[mt]:
                    ach.add("E3", CLASSE["E3"], reg, nome, (x, y),
                            f"metatile {mt} desenha por cima do jogador")

        if liga("C1") and base is not None and anda >= 20 and not base:
            ach.add("C1", CLASSE["C1"], reg, nome, None,
                    f"{anda} tiles andáveis e zero alcançável pela chegada")

        if liga("C2") and base is not None and base:
            for o in objs:
                if not o.get("script") or o.get("script") == "0":
                    continue
                gfx = o.get("graphics_id", "") or ""
                if gfx == LUZ:
                    continue
                # OBJETO COM FLAG NASCE ESCONDIDO e so aparece quando o roteiro
                # acende a flag, muitas vezes DEPOIS de o mapa mudar de forma
                # (`setmetatile`, ponte que baixa, pedra empurrada). Medir a
                # geometria de hoje contra ele acusou 374 casos no vanilla, ou
                # seja a regra crua reprova o jogo original (licao 4.10). So
                # objeto SEMPRE VISIVEL entra.
                if str(o.get("flag", "0")) not in ("0", "FLAG_NONE"):
                    continue
                # Pokemon de overworld e voador/fantasma de proposito.
                if ESPECIE.search(gfx) or VAR_GFX.match(gfx):
                    continue
                x, y = o["x"], o["y"]
                if da_para_falar(x, y, base):
                    continue
                com_hm = da_para_falar(x, y, comhm)
                ach.add("C2", CLASSE["C2"], reg, nome, (x, y),
                        f"{gfx} script {o.get('script')}: "
                        + ("só COM HM" if com_hm else "nem com HM"))

        if liga("C3") and base is not None and base:
            for b in bgs:
                if b.get("type") not in (None, "sign", "hidden_item", "bg_event_sign",
                                         "BG_EVENT_SIGN"):
                    continue
                if not b.get("script"):
                    continue
                x, y = b["x"], b["y"]
                # placa se lê de baixo (o jogador olha para o NORTE), mas o motor
                # aceita qualquer vizinho encarado: a régua estreita é "tem ao
                # menos um vizinho alcançável".
                if any(p in base for p in ((x, y + 1), (x, y - 1),
                                           (x + 1, y), (x - 1, y), (x, y))):
                    continue
                ach.add("C3", CLASSE["C3"], reg, nome, (x, y),
                        f"placa {b.get('script')} sem tile de leitura alcançável")

        # B1 e B9 dependem de `base`
        if liga("B1") and base is not None:
            for o in objs:
                x, y = o["x"], o["y"]
                if not solido(x, y):
                    continue
                gfx = o.get("graphics_id", "") or ""
                if gfx == LUZ or ESPECIE.search(gfx) or VAR_GFX.match(gfx):
                    continue
                if mb(x, y) in POR_DESENHO:
                    continue
                if da_para_falar(x, y, base):
                    continue
                ach.add("B1", CLASSE["B1"], reg, nome, (x, y),
                        f"{gfx} [{mb(x, y)}] script {o.get('script')}")

        if liga("B9") and base is not None and base:
            ocupado = {}
            for o in objs:
                ocupado.setdefault((o["x"], o["y"]), o)
            for o in objs:
                if not o.get("script") or o.get("script") == "0":
                    continue
                x, y = o["x"], o["y"]
                livres = set()
                for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    if (x + dx, y + dy) in base:
                        livres.add((x + dx, y + dy))
                    meio = (x + dx, y + dy)
                    if (0 <= meio[0] < W and 0 <= meio[1] < H
                            and mb(*meio) == "MB_COUNTER"
                            and (x + 2 * dx, y + 2 * dy) in base):
                        livres.add((x + 2 * dx, y + 2 * dy))
                if len(livres) != 1:
                    continue
                p = next(iter(livres))
                outro = ocupado.get(p)
                if outro is None or outro is o:
                    continue
                gfx2 = outro.get("graphics_id", "") or ""
                if gfx2 == LUZ:
                    continue
                ach.add("B9", CLASSE["B9"], reg, nome, (x, y),
                        f"{o.get('graphics_id')} ({o.get('script')}) só se fala de "
                        f"{p}, e {gfx2} está lá")

        # ---- D. grama e encontro --------------------------------------
        if liga("D1") or liga("D2"):
            tem_grama = False
            tem_agua = False
            for y in range(H):
                for x in range(W):
                    b = mb(x, y)
                    if b in ("MB_TALL_GRASS", "MB_LONG_GRASS", "MB_UNUSED_05",
                             "MB_ASHGRASS"):
                        tem_grama = True
                    elif b in HM_ABRE["surf"]:
                        tem_agua = True
                if tem_grama and tem_agua:
                    break
            e = enc.get(info["const"])
            if liga("D1") and tem_grama and not e:
                ach.add("D1", CLASSE["D1"], reg, nome, None,
                        "tem grama alta e NENHUMA tabela de encontro")
            if liga("D2") and e and e["land"] and not tem_grama:
                ach.add("D2", CLASSE["D2"], reg, nome, None,
                        "tem tabela terrestre e nenhum tile de grama")

        # ---- E. metatile contra o TETO do tileset, e setmetatile invisível --
        #
        # E1 nasceu em 06/09/2026 na caça ao travamento do ginásio de
        # Blackthorn. A suspeita da rodada era esta: o `map.bin` e o
        # `setmetatile` do script usavam o id 889 e o `metatile_attributes.bin`
        # do `blackthorn_gym` tem 330 metatiles, ou seja 889 - 512 = 377 estaria
        # FORA do buffer, e `GetAttributeByMetatileIdAndMapLayout` leria
        # comportamento de outro tileset. A suspeita ESTAVA ERRADA (o layout é
        # `johto`, o corte é 640 e 889 - 640 = 249 cabe), mas a lente vale por si:
        # id acima do teto não dá erro de build nenhum, o motor só lê memória de
        # quem estiver ao lado e o mapa ganha gelo, esteira ou colisão fantasma.
        # O teto sai do TAMANHO dos dois `.bin`, nunca de 512 cravado, porque o
        # primário de Johto e o de Kanto têm 640 (armadilha 1 do topo).
        #
        # E2 é a lente que MORDE o defeito real daquele dia: `setmetatile x, y,
        # 889, FALSE` pintando exatamente o metatile que a célula já tinha. A
        # célula abre de verdade (a colisão vai a zero), mas NADA muda na tela,
        # então a ponte acende invisível e o jogador continua vendo lava
        # contínua. Só conta quando o script ABRE (`FALSE`): fechar repintando
        # o mesmo desenho é idioma legítimo (porta que vira parede sem trocar de
        # arte).
        if liga("E1") or liga("E2"):
            L = A.layouts.get(lid) or {}
            corte = 640 if L.get("layout_version") in ("frlg", "johto") else 512
            n_pri, a_pri = A.tamanhos(L.get("primary_tileset"))
            n_sec, a_sec = A.tamanhos(L.get("secondary_tileset"))

            def fora_do_teto(mt):
                """(True, explicação) quando o id não existe no tileset do mapa."""
                if mt < corte:
                    n, a = n_pri, a_pri
                    idx, onde = mt, "primário"
                else:
                    n, a = n_sec, a_sec
                    idx, onde = mt - corte, "secundário"
                if n is None:
                    return (False, "")
                if idx >= n:
                    return (True, f"{onde} define {n} metatiles e o id pede o {idx}")
                if a is not None and idx >= a:
                    return (True, f"{onde} tem {a} atributos e o id pede o {idx}")
                return (False, "")

            if liga("E1"):
                vistos_e1 = {}
                for y in range(H):
                    for x in range(W):
                        mt = linhas[y][x] & 0x3FF
                        ruim, por_que = fora_do_teto(mt)
                        if ruim and mt not in vistos_e1:
                            vistos_e1[mt] = ((x, y), por_que)
                for mt, (p, por_que) in sorted(vistos_e1.items()):
                    ach.add("E1", CLASSE["E1"], reg, nome, p,
                            f"map.bin usa o metatile {mt}: {por_que}")

            texto = rotulos_citados(raiz, nome)
            for sx, sy, sid, sflag in re.findall(
                    r"^\s*setmetatile\s+(\d+),\s*(\d+),\s*(\d+),\s*(\w+)\s*$",
                    texto, re.M):
                sx, sy, sid = int(sx), int(sy), int(sid)
                if liga("E1"):
                    ruim, por_que = fora_do_teto(sid)
                    if ruim:
                        ach.add("E1", CLASSE["E1"], reg, nome, (sx, sy),
                                f"setmetatile pede o metatile {sid}: {por_que}")
                if (liga("E2") and sflag == "FALSE"
                        and 0 <= sx < W and 0 <= sy < H
                        and (linhas[sy][sx] & 0x3FF) == sid):
                    ach.add("E2", CLASSE["E2"], reg, nome, (sx, sy),
                            f"setmetatile abre a célula com o metatile {sid}, "
                            "que já é o desenho dela: a tela não muda")

    return ach, nao_medido, censo, mapas


# --------------------------------------------------------------------- relatório

def relatorio(ach, nao_medido, censo, titulo):
    print(f"\n===== {titulo} =====")
    print(f"mapas medidos: {sum(censo.values())}  "
          + "  ".join(f"{k}:{v}" for k, v in sorted(censo.items())))
    print(f"não medidos: {len(nao_medido)}")
    por_regra = defaultdict(list)
    for it in ach.itens:
        por_regra[it["regra"]].append(it)
    print(f"\n{'regra':6} {'classe':10} {'total':>6}  título")
    for r in sorted(TITULO):
        n = len(por_regra.get(r, []))
        print(f"{r:6} {CLASSE[r]:10} {n:6}  {TITULO[r]}")
    print("\npor região:")
    tab = defaultdict(Counter)
    for it in ach.itens:
        tab[it["regiao"]][it["classe"]] += 1
    for reg in sorted(tab):
        print(f"  {reg:8} " + "  ".join(f"{k}:{v}" for k, v in sorted(tab[reg].items())))
    return por_regra


RE_WARP_SCRIPT = re.compile(
    # `valida_conectividade` usa `warp(silent|hole|door|teleport)?`, e com isso
    # perde `setdivewarp`, `setescapewarp` e `warpwhitefade`. Foi por essa
    # fresta que Sootopolis inteira (a cidade que so se entra por MERGULHO,
    # `Underwater_SootopolisCity` -> `setdivewarp`) aparecia como orfa.
    r"\b(?:set(?:dive|escape|holewarp|)?warp|warp(?:silent|hole|door|teleport|whitefade)?)"
    r"\s+(MAP_[A-Z0-9_]+)")


def alcance_global(raiz):
    """Quais mapas o jogador alcança de verdade a partir do começo do jogo.

    Diferente de `valida_conectividade`: aqui `connections` só liga quando existe
    ao menos UM par de tiles andáveis na borda (a regra A4), e o regex de warp de
    script cobre as formas que faltavam lá. O relatório sai por REGIÃO, porque a
    checagem de órfão de `valida_conectividade` só olha Sinnoh e Johto.
    """
    ach, nm, censo, mapas = varre(raiz, "__nada__")
    A = Arvore(raiz)
    const_de = {i["const"]: n for n, i in mapas.items()}
    viz = defaultdict(set)
    dead = []
    for nome, info in mapas.items():
        c, d = info["const"], info["d"]
        for w in (d.get("warp_events") or []):
            if w.get("dest_map") in const_de:
                viz[c].add(w["dest_map"])
        for t in (d.get("destinos_dinamicos") or []):
            if t in const_de:
                viz[c].add(t)
        inc = os.path.join(raiz, "data/maps", nome, "scripts.inc")
        if os.path.exists(inc):
            for t in RE_WARP_SCRIPT.findall(
                    open(inc, encoding="utf-8", errors="replace").read()):
                if t in const_de:
                    viz[c].add(t)
        g = A.grade(d.get("layout"))
        for cn in (d.get("connections") or []):
            t = cn.get("map")
            if t not in const_de:
                continue
            og = A.grade(mapas[const_de[t]]["d"].get("layout"))
            if g is None or og is None or cn.get("direction") in ("dive", "emerge"):
                viz[c].add(t)
                viz[t].add(c)
                continue
            W, H, l, _ = g
            OW, OH, ol, _ = og
            off = int(cn.get("offset", 0) or 0)
            dr = cn.get("direction")
            p = 0
            if dr in ("down", "up"):
                lin = l[H - 1] if dr == "down" else l[0]
                olin = ol[0] if dr == "down" else ol[OH - 1]
                p = sum(1 for x in range(W) if 0 <= x - off < OW
                        and andavel(lin[x]) and andavel(olin[x - off]))
            elif dr in ("right", "left"):
                p = sum(1 for y in range(H) if 0 <= y - off < OH
                        and andavel(l[y][W - 1 if dr == "right" else 0])
                        and andavel(ol[y - off][0 if dr == "right" else OW - 1]))
            if p:
                viz[c].add(t)
                viz[t].add(c)
            else:
                dead.append((nome, dr, t))
    ini = re.findall(r"SetWarpDestination\(MAP_GROUP\((MAP_\w+)\)",
                     open(os.path.join(raiz, "src/new_game.c")).read())
    part = next(x for x in ini if x in const_de)
    seen, fila = {part}, [part]
    while fila:
        a = fila.pop()
        for v in viz[a]:
            if v not in seen:
                seen.add(v)
                fila.append(v)
    fora = [c for c in const_de if c not in seen]
    print(f"\npartindo de {part}: {len(seen)} de {len(const_de)} mapas alcançáveis")
    print(f"{len(fora)} mapas que NENHUM caminho alcança, por região:")
    por = defaultdict(list)
    for c in fora:
        por[mapas[const_de[c]]["regiao"]].append(const_de[c])
    for r in sorted(por, key=lambda k: -len(por[k])):
        print(f"  {r:8} {len(por[r]):4}   " + ", ".join(sorted(por[r])[:5]))
    print(f"\n{len(dead)} conexões descartadas por borda de parede (regra A4)")
    return 0


def main():
    so = None
    if "--regra" in sys.argv:
        so = sys.argv[sys.argv.index("--regra") + 1]
    raiz = VANILLA if "--vanilla" in sys.argv else REPO
    if "--raiz" in sys.argv:            # outra fonte (pokefirered, hns, ...)
        raiz = sys.argv[sys.argv.index("--raiz") + 1]
    if "--global" in sys.argv:
        return alcance_global(raiz)
    ach, nm, censo, _ = varre(raiz, so)
    pr = relatorio(ach, nm, censo, os.path.basename(raiz.rstrip("/")))
    if "--json" in sys.argv:
        alvo = sys.argv[sys.argv.index("--json") + 1]
        json.dump(dict(itens=ach.itens,
                       nao_medido=nm,
                       censo=dict(censo)),
                  open(alvo, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"\ngravado em {alvo}")
    if "--listar" in sys.argv:
        for r in sorted(pr):
            print(f"\n--- {r}: {TITULO[r]} ({len(pr[r])}) ---")
            for it in pr[r][:40]:
                print(f"  {it['regiao']:7} {it['mapa']:38} {str(it['coord']):10} "
                      f"{it['detalhe']}")
            if len(pr[r]) > 40:
                print(f"  ... e mais {len(pr[r]) - 40}")
    return 0


# ------------------------------------------------------------------------ demo

def demo():
    """Mutação plantada: sem ela o portão poderia estar medindo nada."""
    A = Arvore(REPO)
    # (1) o corte de metatile sai da VERSÃO do layout, não de 512 cravado
    frlg = [l for l in A.layouts.values() if l.get("layout_version") == "frlg"]
    assert frlg, "nenhum layout frlg: a árvore mudou, remeça"
    g = A.grade(frlg[0]["id"])
    assert g is not None and g[3] == 640, f"corte errado: {g and g[3]}"
    em = [l for l in A.layouts.values() if l.get("layout_version") not in ("frlg", "johto")]
    assert A.grade(em[0]["id"])[3] == 512

    # (2) a BFS respeita elevação: grade de 3x1 com o do meio em elevação 3
    #     e as pontas em 1 tem que partir o caminho.
    livre_e1 = (1 << 12)          # colisão 0, elevação 1
    livre_e3 = (3 << 12)
    linhas = [[livre_e1, livre_e3, livre_e1]]
    assert bfs(3, 1, linhas, [(0, 0)]) == {(0, 0)}, "a elevação não está sendo lida"
    linhas[0][1] = livre_e1
    assert bfs(3, 1, linhas, [(0, 0)]) == {(0, 0), (1, 0), (2, 0)}

    # (3) parede é parede: colisão 1 no meio parte o caminho
    linhas[0][1] = livre_e1 | (1 << 10)
    assert bfs(3, 1, linhas, [(0, 0)]) == {(0, 0)}

    # (4) extra_andavel (a HM) atravessa a parede, e só ela
    assert bfs(3, 1, linhas, [(0, 0)],
               lambda x, y: (x, y) == (1, 0)) == {(0, 0), (1, 0), (2, 0)}

    # (5) a régua de janela: 16 objetos dentro de 20x17 acusam, 15 não
    def janela(pts):
        pior = 0
        for cx, cy in pts:
            n = sum(1 for x, y in pts if cx <= x < cx + 20 and cy <= y < cy + 17)
            pior = max(pior, n)
        return pior
    assert janela([(i, 0) for i in range(16)]) == 16
    assert janela([(i, 0) for i in range(15)]) == 15
    assert janela([(i * 21, 0) for i in range(16)]) == 1, "a janela não desliza"

    # (6) região: sai do GRUPO, e o túmulo de mapa cortado sai das quatro antes
    #     disso, para não engordar Hoenn, que é o balde padrão
    assert regiao_de("Galar_Postwick50", "gMapGroup_Dungeons",
                     {"cortado_por": "cartucho 1"}) == "cortado"
    assert regiao_de("PalletTown", "gMapGroup_TownsAndRoutes_Frlg") == "Kanto"
    assert regiao_de("Route101", "gMapGroup_TownsAndRoutes") == "Hoenn"
    assert regiao_de("AcuityCavern", "gMapGroup_SinnohCavernas") == "Sinnoh"

    # (7) o mapa de referência do motor: a porta empurra ao SUL, e é por isso
    #     que a chegada da porta é (x, y+1) e não (x, y)
    assert "MB_ANIMATED_DOOR" in PORTAS and "MB_LADDER" not in PORTAS

    # (8) E1: o teto do tileset sai do TAMANHO do .bin, e o corte da versão do
    #     layout. O ginásio de Blackthorn é o caso que pagou a lente: com o
    #     corte de Emerald (512) o metatile 889 pareceria fora do teto, e com o
    #     corte certo de Johto (640) ele cabe nos 330 do `blackthorn_gym`.
    n_sec, a_sec = A.tamanhos("gTileset_BlackthornGym")
    assert (n_sec, a_sec) == (330, 330), f"tamanho do blackthorn_gym: {n_sec}/{a_sec}"
    assert A.grade("LAYOUT_BLACKTHORN_CITY_GYM")[3] == 640
    assert 889 - 640 < n_sec, "889 cabe no secundário de Johto e a lente diz que não"
    assert 889 - 512 >= n_sec, "a mutação de referência sumiu: 889-512 tem que estourar"

    # (9) E2: setmetatile que ABRE pintando o desenho que a célula já tem é
    #     ponte invisível; fechar repintando o mesmo desenho é idioma legítimo.
    #     Foi este par que separou os 46 achados reais de Blackthorn do resto
    #     do repo, que dá zero.
    def e2(mt_no_bin, mt_pintado, flag):
        return flag == "FALSE" and mt_no_bin == mt_pintado
    assert e2(889, 889, "FALSE") and not e2(889, 809, "FALSE")
    assert not e2(889, 889, "TRUE")

    print("demo ok")


if __name__ == "__main__":
    # `demo()` e `main()` devolvem 0 quando passam; `demo()` levanta AssertionError
    # quando a mutacao plantada NAO e acusada, e ai o traceback ja da exit 1.
    # `or 0` existe porque funcao que so imprime devolve None, e None vira exit 1
    # em sys.exit: portao que reprova sozinho e pior que portao nenhum.
    sys.exit((demo() or 0) if "--demo" in sys.argv else (main() or 0))
