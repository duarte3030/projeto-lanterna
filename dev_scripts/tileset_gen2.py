#!/usr/bin/env python3
"""B12.a: converte um tileset do BW3G (pokecrystal, gen 2) em tileset SECUNDARIO
do pokeemerald-expansion.

Uso:
    python3 dev_scripts/tileset_gen2.py --demo                  # autoteste, nao grava
    python3 dev_scripts/tileset_gen2.py --medir                 # placar dos 58, nao grava
    python3 dev_scripts/tileset_gen2.py castelia [--gravar]     # um tileset
    python3 dev_scripts/tileset_gen2.py --usados --gravar       # os 46 usados por mapa

O QUE ELE FAZ, E O QUE ELE NAO FAZ

Faz: le `gfx/tilesets/<n>.png` (2bpp), `data/tilesets/<n>_metatiles.bin`,
`<n>_attributes.bin` e `<n>_collision.asm` do BW3G e grava
`data/tilesets/secondary/unova_<n>/` com `tiles.png` (4bpp indexado),
`palettes/00..15.pal` (JASC), `metatiles.bin` e `metatile_attributes.bin`.
Nao faz: registrar o tileset em C (isso e `--registrar`, que edita os quatro
arquivos do repo), nem tocar em mapa (isso e `blockdata_unova.py --arte-propria`).

O CASAMENTO, CAMPO A CAMPO, MEDIDO NAS DUAS ARVORES

  tile          8x8 2bpp (4 cores)      -> 8x8 4bpp (16 cores)   expandir, cor +1
  bloco         4x4 tiles = 32x32 px    -> 4 metatiles de 16x16   1 para 4
  paleta        3 bits (8 paletas)      -> 4 bits (16)            direto
  flip          bits 5 e 6 do attribute -> bits 10 e 11 da entrada direto
  prioridade    bit 7 do attribute      -> camada de cima          ver abaixo
  colisao       4 valores por bloco     -> 1 comportamento/metatile um para um

TRES DECISOES QUE MUDAM O RESULTADO, E POR QUE CADA UMA

1. **A cor 0 do gen 2 vira a cor 1 do GBA.** No GBA a cor 0 de qualquer paleta e
   TRANSPARENTE, e no gen 2 ela e uma cor de verdade (branco, quase sempre). Se
   traduzissemos 0->0, todo pixel branco viraria buraco mostrando o backdrop.
   Entao o pixel `v` do gen 2 vira `v + 1`, e a cor 0 fica sobrando de proposito.
   O tile local 0 do tileset gerado e todo zero: e ele que preenche a camada de
   cima dos metatiles que nao tem prioridade.

2. **Camada: METATILE_LAYER_TYPE_NORMAL sempre, e o tile com prioridade entra nas
   DUAS camadas.** Em `NORMAL` as entradas 0..3 vao para o BG do meio (abaixo do
   jogador) e as 4..7 para o BG de cima (acima do jogador). No gen 2 existe UMA
   camada e o bit de prioridade so diz "este tile desenha por cima do sprite";
   o tile continua sendo o fundo. Por isso o tile com prioridade e escrito em
   baixo E em cima: em baixo ele e o cenario, em cima ele esconde o jogador.
   Se fosse so em cima, uma copa de arvore viraria buraco preto.

3. **Deduplicacao por (visual, classe de colisao).** E ela que faz caber: um bloco
   da 4 metatiles e 58 tilesets x 253 blocos dariam 1012 metatiles no pior caso,
   contra teto de 512. A chave inclui a CLASSE porque o comportamento mora no
   metatile: dois quadrantes visualmente iguais com colisao diferente (chao e
   parede pintados igual) precisam de dois metatiles. Medido nos 57 que tem PNG,
   ja com as variantes de porta e de chao de masmorra: pior caso 342 metatiles
   (`pkmn_league`) e 246 tiles (`driftveil`), contra teto de 512 nos dois.

A PALETA DA NOITE FOI DESCARTADA (decisao do Gui, 12/08/2026): o pokeemerald nao
tinge tileset por horario, entao `*_nite.pal` nao entra. A paleta de dia sai de
`gfx/tilesets/<n>.pal` quando o tileset tem uma propria (e o que
`LoadSpecialMapPalette` carrega inteira, 8 paletas), e senao de `bg_tiles.pal`
pelo indice que `data/maps/environment_colors.asm` da ao ambiente dos mapas que
usam o tileset, na linha "day".

QUATRO TINTAS FICAM APROXIMADAS, e isso e escolha, nao esquecimento: no gen 2 a
paleta de `icirrus`, `pkmn_league`, `airport` e `port` depende do GRUPO DO MAPA,
e aqui ela e do tileset. Cada um leva a paleta da maioria dos seus mapas
(`icirrus.pal`, `pkmn_league.pal`, `airport.pal` e a padrao), entao a
DragonspiralTowerOutside, a entrada da Victory Road, os dois avioes e o ginasio
de Humilau saem com o tom do irmao. E diferenca de cor, nao de desenho.

O TETO DE PALETA E 7, NAO 8. O tileset secundario do GBA so possui as paletas 6 a
12 (`NUM_PALS_IN_PRIMARY` 6, `NUM_PALS_TOTAL` 13). O gen 2 tem 8. Medido nos 58:
so `port` usa as 8, e a oitava e a TEXT. Quando passa de 7, a paleta MENOS usada e
fundida na mais parecida (distancia RGB), com aviso impresso.

O PRECO DESSA FUSAO FOI MEDIDO, e ele e uma cor: comparando os 291 mapas pixel a
pixel contra o desenho tirado direto do gen 2, 288 batem EXATO e os tres do
`port` (HumilauGym, CasteliaPort, VirbankPort) diferem so no preto puro
(RGB 0,0,0), que vira o quase-preto 57,57,57 da paleta BROWN. Nenhum outro pixel
de nenhum outro mapa muda. Nao vale gastar tile duplicado para recuperar isso.
"""
import json
import os
import re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))

from PIL import Image                # noqa: E402

import blockdata_unova as bd         # noqa: E402  CLASSE/classe_de/quadrantes/mapas_unova
import importa_unova as iu           # noqa: E402
import valida_warp_tile as vw        # noqa: E402  _MB, COMPORTA_WARP

BW3G = iu.BW3G
MB = vw._MB
DESTINO = f"{RAIZ}/data/tilesets/secondary"

NUM_PALS_IN_PRIMARY = 6      # include/fieldmap.h
NUM_PALS_TOTAL = 13
MAX_PALETAS = NUM_PALS_TOTAL - NUM_PALS_IN_PRIMARY      # 7
MAX_TILES = 512              # NUM_TILES_TOTAL - NUM_TILES_IN_PRIMARY
MAX_METATILES = 512          # NUM_METATILES_TOTAL - NUM_METATILES_IN_PRIMARY

# ------------------------------------------------------- classe -> comportamento
#
# Reuso, nao copia: a tabela COLL_* -> classe e `blockdata_unova.CLASSE` (mais a
# permissao do gen 2 em `classe_de`), e o comportamento canonico de cada classe e
# o PRIMEIRO de `blockdata_unova.ESPERADO`, que e a mesma lista que o `--demo`
# daquele script ja usa para reprovar entrada mentirosa.
COMPORTAMENTO = {c: bd.ESPERADO[c][0] for c in bd.CLASSES}

# LEDGE DO GEN 2 NAO E LEDGE DO GEN 3, e tratar como se fosse cortava o mapa.
# Medido e consertado em 12/08/2026 (bloco B6).
#
# O que o gen 2 faz, lido no codigo da fonte e nao de memoria:
#   - `data/collision_permissions.asm:167` marca COLL_HOP_LEFT como LANDTILE, ou
#     seja o jogador ANDA em cima do tile de pulo, vindo de qualquer lado;
#   - `engine/overworld/player_movement.asm:362` (`.TryJump`) le
#     **`wPlayerStandingTile`**: o pulo sai do tile em que o jogador ESTA e vai
#     2 casas na direcao do ledge, e so acontece se o destino for andavel.
# O que o gen 3 faz: o ledge e a casa DA FRENTE, impassavel, e o jogador pula por
# cima dela (`ShouldJumpLedge` -> `GetLedgeJumpDirection`, src/event_object_movement).
# As duas semanticas estao deslocadas em UM TILE.
#
# Consequencia medida do jeito antigo (as 4 classes caindo em BLOQ): 244
# quadrantes viraram parede em 40 mapas de Unova, e em dois deles o mapa deixou
# de funcionar. Flood fill a partir dos warps, fonte contra ROM:
#   Unova_OpelucidGym        231 -> 41 tiles alcancaveis (o ginasio inteiro)
#   Unova_DragonspiralTower3F 117 -> 61, com os TRES itens e a escada do 4F fora
#
# ponytail: ledge de gen 2 vira CHAO COMUM (colisao 0, MB_NORMAL), guardando so o
# desenho da rampa. TETO DESTA SIMPLIFICACAO: perde-se o sentido unico, o jogador
# passa a poder voltar por onde pulou. CAMINHO DE UPGRADE, para quem quiser pulo
# de verdade: manter MB_JUMP_* mas DESLOCAR o metatile do ledge um tile na
# direcao do pulo (o ledge do gen 3 mora na casa da frente), o que e mexer na
# geometria do mapa e nao so na tabela de classes. Precedente desta mesma escolha,
# duas dezenas de linhas acima em `blockdata_unova.CLASSE`: as "side walls"
# (RIGHT_WALL e irmas) tambem viraram `chao`, com a mesma razao escrita la, "abrir
# uma cerca e menos grave que cortar um caminho".
LEDGES = ("ledge_baixo", "ledge_esq", "ledge_dir", "ledge_cima")
COMPORTAMENTO.update({c: "MB_NORMAL" for c in LEDGES})
# ...e a metade que RESTAURA o pulo: a parede que fica ENTRE o ledge e o pouso
# ganha uma variante do MESMO desenho com o MB_JUMP_* correspondente, que e o
# "deslocar um tile na direcao do pulo". Quem decide quais paredes sao essas e
# `blockdata_unova.alvos_de_pulo`, com a regra conservadora escrita la.
# Colisao 1, como todo ledge do gen 3: o jogador nao pisa nela, pula por cima.
PULO_CLASSE = {c: "pulo_" + c.split("_", 1)[1] for c in LEDGES}
COMPORTAMENTO.update({PULO_CLASSE[c]: bd.ESPERADO[c][0] for c in LEDGES})

# Colisao e elevacao por classe. Nao sai de `blockdata_unova.PALETA` porque la
# varias entradas sao FALLBACK (o par emprestado nao tem a coisa) e o fallback
# carrega a colisao do substituto: `ledge_cima` vira chao ANDAVEL em todo par.
# Aqui o tileset e nosso, entao todas as classes existem de verdade.
ANDA, BLOQ, AGUA = bd.ANDA, bd.BLOQ, bd.AGUA
ANDAVEL = ("chao", "chao_caverna", "grama", "poca", "gelo", "escada", "porta") + LEDGES
AGUOSO = ("agua", "cachoeira")


def colisao_da_classe(c):
    return ANDA if c in ANDAVEL else AGUA if c in AGUOSO else BLOQ


# ---------------------------------------------------------------------- paletas

_RE_RGB = re.compile(r"RGB\s+([\d\s,]+)")


def le_pal_gen2(caminho):
    """[(r,g,b) x4] x N, na ordem do arquivo. Aceita 1 ou 4 cores por linha."""
    nums = []
    for ln in open(caminho):
        ln = ln.split(";")[0]
        m = _RE_RGB.search(ln)
        if m:
            nums += [int(v) for v in re.findall(r"\d+", m.group(1))]
    assert len(nums) % 12 == 0, f"{caminho}: {len(nums)} componentes, nao multiplo de 12"
    cores = [tuple(nums[i:i + 3]) for i in range(0, len(nums), 3)]
    return [cores[i:i + 4] for i in range(0, len(cores), 4)]


# data/maps/environment_colors.asm, linha "day" de cada grupo. Indice dentro de
# bg_tiles.pal, cujas 42 paletas sao morn(0-7) day(8-15) nite(16-23) dark(24-31)
# indoor(32-39) e agua de exterior(40-41).
DIA = {
    "exterior": [0x08, 0x09, 0x0a, 0x28, 0x0c, 0x0d, 0x0e, 0x0f],
    "interior": [0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x07],
    "masmorra": [0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f],
}
AMBIENTE_GRUPO = {"TOWN": "exterior", "ROUTE": "exterior", "INDOOR": "interior",
                  "GATE": "interior", "ENVIRONMENT_5": "interior",
                  "CAVE": "masmorra", "DUNGEON": "masmorra"}


MASMORRA = ("CAVE", "DUNGEON")     # os dois ambientes em que o gen 2 sorteia
                                   # encontro no CHAO, sem precisar de grama


def _uso_dos_mapas(_cache={}):
    """tileset -> (quantos mapas, grupo de ambiente predominante, {ambientes})."""
    if not _cache:
        conta = {}
        for _, mapas in iu.le_grupos():
            for camel, _c, _w, _h, tset, amb, _l, _m in mapas:
                n = iu.COLISAO_ALIAS.get(tset, tset)
                d, s = conta.setdefault(n, ({}, set()))
                g = AMBIENTE_GRUPO.get(amb, "interior")
                d[g] = d.get(g, 0) + 1
                s.add(amb)
        for n, (d, s) in conta.items():
            _cache[n] = (sum(d.values()), max(d, key=lambda k: d[k]), s)
    return _cache


def _pal_mansion():
    """`LoadMansionPalette` nao e um INCLUDE simples: copia as 8 primeiras de
    `mansion_1.pal` (que tem 9) e depois troca YELLOW por `mansion_2.pal`, WATER
    pela 7a de mansion_1 e ROOF pela 9a. Lido em
    `engine/tilesets/tileset_palettes.asm:550`."""
    m1 = le_pal_gen2(f"{BW3G}/gfx/tilesets/mansion_1.pal")
    m2 = le_pal_gen2(f"{BW3G}/gfx/tilesets/mansion_2.pal")
    p = list(m1[:8])
    p[3], p[4], p[6] = m1[6], m2[0], m1[8]      # WATER, YELLOW, ROOF
    return p


# Tileset cujo `LoadSpecialMapPalette` aponta para um .pal de nome DIFERENTE do
# tileset. Sem esta tabela os tres sairiam com a paleta padrao de interior, e sao
# 33 mapas de Unova (19 Pokecenters, 12 do mansion, 1 quarto do jogador).
PAL_ESPECIAL = {
    "pokecenter": "pokecom_center",     # LoadPokecenterPalette
    "players_room": "players_house",    # o dispatch manda TILESET_PLAYERS_ROOM
                                        # para .players_house
    "mansion": _pal_mansion,            # montada, ver acima
}


def paletas_gen2(nome):
    """As 8 paletas de 4 cores do tileset, e de onde elas vieram."""
    esp = PAL_ESPECIAL.get(nome)
    if callable(esp):
        return esp(), "mansion_1.pal + mansion_2.pal"
    if esp:
        return le_pal_gen2(f"{BW3G}/gfx/tilesets/{esp}.pal")[:8], f"{esp}.pal"
    proprio = f"{BW3G}/gfx/tilesets/{nome}.pal"
    if os.path.exists(proprio):
        p = le_pal_gen2(proprio)
        assert len(p) >= 8, f"{proprio}: so {len(p)} paletas"
        return p[:8], f"{nome}.pal"
    _n, grupo, _amb = _uso_dos_mapas().get(nome, (0, "interior", set()))
    fundo = le_pal_gen2(f"{BW3G}/gfx/tilesets/bg_tiles.pal")
    return [fundo[i] for i in DIA[grupo]], f"bg_tiles.pal/{grupo}"


def rgb5_para_888(c):
    """5 bits -> 8 bits com ida e volta exata (31 -> 255, e 255>>3 -> 31)."""
    return tuple((v << 3) | (v >> 2) for v in c)


# ------------------------------------------------------------------ leitura BW3G

def _png_dos_tilesets(_cache={}):
    """tileset -> arquivo PNG, lido de `gfx/tilesets.asm`.

    Nao da para deduzir pelo nome: `cave_ruins` desenha com `cave.png`, e
    `driftveil` e `mistralton` moram num arquivo de nome literal
    `driftveil.,driftveil_extra.png` (a concatenacao que o rgbgfx faz).
    """
    if _cache:
        return _cache
    pend = []
    for ln in open(f"{BW3G}/gfx/tilesets.asm"):
        ln = ln.strip()
        m = re.match(r"^Tileset(\w+)GFX:$", ln)
        if m:
            pend.append(re.sub(r"(?<!^)(?=[A-Z])", "_", m.group(1)).lower())
            continue
        m = re.match(r'^INCBIN "gfx/tilesets/(.+)\.2bpp\.lz"', ln)
        if m and pend:
            for n in pend:
                _cache[n] = m.group(1) + ".png"
        if not ln.startswith(";"):
            pend = pend if m is None and ln.endswith(":") else []
    return _cache


def png_de(nome):
    p = _png_dos_tilesets().get(nome, f"{nome}.png")
    return f"{BW3G}/gfx/tilesets/{p}"


def tiles_gen2(nome):
    """[[indice de cor 0..3] x 64] por tile, na ordem do PNG (16 por linha)."""
    im = Image.open(png_de(nome)).convert("L")
    w, h = im.size
    assert w == 128, f"{nome}.png tem {w} px de largura, esperava 128"
    px = im.load()
    saida = []
    for t in range((w // 8) * (h // 8)):
        x0, y0 = (t % 16) * 8, (t // 16) * 8
        saida.append([(255 - px[x0 + x, y0 + y]) // 85
                      for y in range(8) for x in range(8)])
    return saida


def blocos_gen2(nome):
    """[(tile, paleta, xflip, yflip, prioridade) x16] por bloco, ordem do gen 2.

    O `palmap2attr.py` do BW3G ja moveu o bit de banco do byte do metatile para o
    bit 3 do attribute, entao o indice real do tile e `metatile | (banco << 7)`.
    """
    mt = open(f"{BW3G}/data/tilesets/{nome}_metatiles.bin", "rb").read()
    pa = f"{BW3G}/data/tilesets/{nome}_attributes.bin"
    at = open(pa, "rb").read() if os.path.exists(pa) else bytes(len(mt))
    at = (at + bytes(len(mt)))[:len(mt)]
    saida = []
    for b in range(len(mt) // 16):
        bloco = []
        for k in range(16):
            t, a = mt[b * 16 + k], at[b * 16 + k]
            bloco.append((t | ((a >> 3 & 1) << 7), a & 7,
                          a >> 5 & 1, a >> 6 & 1, a >> 7 & 1))
        saida.append(bloco)
    return saida


QUADRANTE = ((0, 0), (1, 0), (0, 1), (1, 1))   # CE, CD, BE, BD, a ordem do tilecoll


def quadrante_do_bloco(bloco, q):
    """As 4 entradas de tile de um quadrante de 16x16, em ordem de leitura."""
    qx, qy = QUADRANTE[q]
    return tuple(bloco[(qy * 2 + dy) * 4 + (qx * 2 + dx)]
                 for dy in (0, 1) for dx in (0, 1))


# --------------------------------------------------------------------- conversao

def _funde_paletas(usadas, pals, contagem):
    """Reduz a MAX_PALETAS fundindo a menos usada na mais parecida. gen2 -> gen2."""
    trocas, vivas = {}, list(usadas)
    while len(vivas) > MAX_PALETAS:
        morta = min(vivas, key=lambda p: contagem[p])
        vivas.remove(morta)
        alvo = min(vivas, key=lambda p: sum(
            (a - b) ** 2 for ca, cb in zip(pals[morta], pals[p]) for a, b in zip(ca, cb)))
        trocas[morta] = alvo
        print(f"    aviso: paleta {morta} ({contagem[morta]} tiles) fundida na {alvo}")
    for m, a in list(trocas.items()):
        while a in trocas:
            a = trocas[a]
        trocas[m] = a
    return vivas, trocas


def converte(nome, portas_extras=(), pulos_extras=()):
    """Converte um tileset. `portas_extras` = {(bloco, quadrante)} que precisam de
    uma variante com comportamento de porta (warp que a fonte poe sobre chao).
    `pulos_extras` = {(bloco, quadrante, classe_de_ledge)} que precisam da
    variante de PAREDE COM MB_JUMP_*, o outro lado do deslocamento de um tile
    (ver o cabecalho da tabela COMPORTAMENTO e `blockdata_unova.alvos_de_pulo`)."""
    pals8, origem_pal = paletas_gen2(nome)
    tiles = tiles_gen2(nome)
    blocos = blocos_gen2(nome)
    coll = bd.quadrantes(f"{nome}_collision.asm")

    # 1. quais paletas do gen 2 o tileset usa de fato
    contagem = {}
    for bloco in blocos:
        for t, p, *_ in bloco:
            contagem[p] = contagem.get(p, 0) + 1
    usadas = sorted(contagem)
    vivas, trocas = _funde_paletas(usadas, pals8, contagem)
    pal_gba = {p: NUM_PALS_IN_PRIMARY + i for i, p in enumerate(vivas)}
    for m, a in trocas.items():
        pal_gba[m] = pal_gba[a]

    # 2. metatiles, deduplicando por (visual, classe). O local 0 e reservado:
    #    metatile vazio e bloqueado, destino de bloco que o .ablk cita e o
    #    tileset nao tem.
    # 1b. o chao de MASMORRA e um metatile a parte, e nao e enfeite.
    #     No gen 2 quem sorteia encontro dentro de caverna e o CHAO (o ambiente
    #     do mapa e CAVE/DUNGEON e `TryWildEncounter` nao pede grama); no gen 3
    #     so dispara metatile com `TILE_FLAG_HAS_ENCOUNTERS`, que o MB_NORMAL
    #     nao tem e o MB_CAVE tem. Como o comportamento mora no METATILE e o
    #     ambiente e do MAPA, um tileset que serve casa E masmorra (e o caso do
    #     `traditional_house`: 7 casas, mas tambem CelestialTower e StrangeHouse)
    #     precisa das duas versoes do mesmo desenho de chao.
    _n, _g, ambientes = _uso_dos_mapas().get(nome, (0, "interior", set()))
    tem_masmorra = bool(ambientes & set(MASMORRA))
    tem_normal = bool(ambientes - set(MASMORRA)) or not tem_masmorra

    VAZIO = ((0, 0, 0, 0, 0),) * 4
    metatiles = {(VAZIO, "parede"): 0}
    ordem = [(VAZIO, "parede")]
    quad2mt, masmorra2mt, porta2mt, pulo2mt = {}, {}, {}, {}

    def registra_mt(vis, classe):
        chave = (vis, classe)
        if chave not in metatiles:
            metatiles[chave] = len(ordem)
            ordem.append(chave)
        return metatiles[chave]

    for b, bloco in enumerate(blocos):
        classes = coll.get(b, ("parede",) * 4)
        for q in range(4):
            vis = quadrante_do_bloco(bloco, q)
            if tem_normal:
                quad2mt[(b, q)] = registra_mt(vis, classes[q])
            if tem_masmorra:
                masmorra2mt[(b, q)] = registra_mt(
                    vis, "chao_caverna" if classes[q] == "chao" else classes[q])
            if (b, q) in portas_extras:
                porta2mt[(b, q)] = registra_mt(vis, "porta")
            for ledge in LEDGES:
                if (b, q, ledge) in pulos_extras:
                    pulo2mt[(b, q, ledge)] = registra_mt(vis, PULO_CLASSE[ledge])
    if not tem_normal:
        quad2mt = masmorra2mt
    if not tem_masmorra:
        masmorra2mt = quad2mt

    # 3. so os tiles usados, remapeados; o local 0 fica em branco (camada de cima)
    usados = sorted({e[0] for vis, _ in ordem for e in vis})
    tile_gba = {t: i + 1 for i, t in enumerate(usados)}
    n_tiles = len(usados) + 1

    assert len(ordem) <= MAX_METATILES, \
        f"{nome}: {len(ordem)} metatiles, teto {MAX_METATILES}"
    assert n_tiles <= MAX_TILES, f"{nome}: {n_tiles} tiles, teto {MAX_TILES}"

    # 4. bytes
    mt_bin, at_bin = bytearray(), bytearray()
    for vis, classe in ordem:
        baixo, cima = [], []
        for t, p, xf, yf, prio in vis:
            v = (512 + tile_gba.get(t, 0)) | (xf << 10) | (yf << 11) | (pal_gba[p] << 12)
            baixo.append(v)
            cima.append(v if prio else (512 | (NUM_PALS_IN_PRIMARY << 12)))
        for v in baixo + cima:
            mt_bin += struct.pack("<H", v)
        # atributo = comportamento; camada 0 = METATILE_LAYER_TYPE_NORMAL
        at_bin += struct.pack("<H", MB[COMPORTAMENTO[classe]])

    px_tiles = [[0] * 64] + [[v + 1 for v in tiles[t]] if t < len(tiles) else [0] * 64
                             for t in usados]
    paletas = []
    for i in range(16):
        k = i - NUM_PALS_IN_PRIMARY
        fonte = pals8[vivas[k]] if 0 <= k < len(vivas) else pals8[0]
        # a cor 0 fica vazia de proposito: no GBA ela e transparente, e o pixel
        # `v` do gen 2 foi deslocado para `v + 1` (decisao 1 do cabecalho).
        paletas.append([(0, 0, 0)] + [rgb5_para_888(c) for c in fonte]
                       + [(0, 0, 0)] * 11)

    ts = {"nome": nome, "tiles": px_tiles, "paletas": paletas,
          "metatiles": bytes(mt_bin), "atributos": bytes(at_bin),
          "quad2mt": quad2mt, "masmorra2mt": masmorra2mt, "porta2mt": porta2mt,
          "pulo2mt": pulo2mt,
          "tile_gba": tile_gba,
          "ordem": ordem, "ambientes": ambientes,
          "tem_masmorra": tem_masmorra, "tem_normal": tem_normal,
          "pal_gba": pal_gba, "origem_pal": origem_pal, "blocos": len(blocos),
          "n_metatiles": len(ordem), "n_tiles": n_tiles, "n_paletas": len(vivas)}
    ts["animacoes"] = animacoes_de(nome, tile_gba, px_tiles)
    return ts


# ---------------------------------------------------------------------- animacao
#
# O gen 2 anima tileset com um SCRIPT DE QUADROS (`engine/tilesets/tileset_anims.asm`):
# cada linha `dw <parametro>, <rotina>` roda em um quadro do ciclo e escreve 16
# bytes (um tile 2bpp) num tile de VRAM. O pokeemerald faz a mesma coisa por
# outro caminho: `AppendTilesetAnimToBuffer(quadro, BG_VRAM + tile, 32)` numa fila
# que o V-blank despeja (`TransferTilesetAnimsBuffer`). Sao o mesmo mecanismo, e
# por isso a porta e uma tabela, nao um motor novo.
#
# O que o conversor faz: descobre, POR TILESET, quais tiles sao animados e com
# quais quadros, e grava os quadros ja em 4bpp. Tres origens de quadro:
#
#  1. quadros explicitos na fonte (`gfx/tilesets/whirlpool/1.png`, ...);
#  2. alvo fixo cravado na rotina (flor no tile $03, arvore da floresta em $0c e
#     $0f, estrelas em $75/$77/$78, luzes em $1d/$2d) - tabela `ANIM_FIXO`, com a
#     linha do .asm de onde cada numero saiu;
#  3. rolagem (`ScrollTileDown` e irmas), que no gen 2 e CPU mexendo no proprio
#     tile. Aqui os 8 quadros sao PRE-DESENHADOS deslocando o tile: mesmo
#     resultado na tela, zero codigo novo no motor.
#
# FILTRO QUE IMPORTA: animacao cujo tile de origem nao sobreviveu a deduplicacao
# (ou seja, nenhum bloco daquele tileset usa aquele tile) e DESCARTADA. Sem isso
# a ROM pagaria quadros de agua para tileset que nao tem agua.
#
# FICA DE FORA, de proposito: `FlickeringCaveEntrancePalette` e
# `AnimateWaterPalette` sao animacao de PALETA, nao de tile. Precisariam de um
# segundo mecanismo (o `BlendAnimPalette_BattleDome_*` do pokeemerald) e valem
# um piscar de entrada de caverna. Tambem fica de fora o `TilesetEliteFourRoom2`
# (fogo do Grimsley e luzes): no nosso repo ele e apelido de `elite_four_room`
# (`importa_unova.COLISAO_ALIAS`), entao nao existe tileset separado para animar.

ANIM_TICKS = 16          # quadros de jogo entre dois passos da animacao
ANIM_PASSOS_ROLAGEM = 8  # o ciclo de `wTileAnimationTimer` do gen 2 e de 8

# rotina de alvo fixo -> (tile do gen 2, [PNGs de quadro], fase)
# Numeros lidos um a um em engine/tilesets/tileset_anims.asm.
ANIM_FIXO = {
    "AnimateFlowerTile":         (0x03, ["flower/cgb_1.png", "flower/cgb_2.png"], 0),
    "ForestTreeLeftAnimation":   (0x0C, ["forest-tree/1.png", "forest-tree/2.png"], 0),
    "ForestTreeRightAnimation":  (0x0F, ["forest-tree/3.png", "forest-tree/4.png"], 0),
    "ForestTreeLeftAnimation2":  (0x0C, ["forest-tree/1.png", "forest-tree/2.png"], 0),
    "ForestTreeRightAnimation2": (0x0F, ["forest-tree/3.png", "forest-tree/4.png"], 0),
    "StarsAnim1":  (0x77, ["stars/1.png"], 0),
    "StarsAnim2":  (0x78, ["stars/1.png"], 1),
    "StarsAnim3":  (0x75, ["stars/1.png"], 2),
    "LightsAnim1": (0x1D, ["lights/1.png", "lights/2.png",
                           "lights/3.png", "lights/4.png"], 2),
    "LightsAnim2": (0x2D, ["lights/1.png", "lights/2.png",
                           "lights/3.png", "lights/4.png"], 0),
}
# rotina que le o alvo e os quadros de uma struct `<X>Frames<N>` do .asm
ANIM_STRUCT = {"AnimateWhirlpoolTile", "AnimateFountainTile", "AnimateFanTile",
               "AnimateComputerTile0", "AnimateComputerTile1", "AnimateComputerTile2",
               "AnimateSkyTile1R", "AnimateSkyTile2R", "AnimateSkyTile3R",
               "AnimateSkyTile4R"}
# rotina cujo alvo vem do proprio parametro `vTiles2 tile $XX`
ANIM_PARAM = {"AnimateWaterTile": ["water/water.png"]}
# rolagem: (passo por ciclo, eixo). 'rl' = 4 para um lado e 4 de volta.
ANIM_ROLAGEM = {"ScrollTileRight": (1, "x"), "ScrollTileLeft": (-1, "x"),
                "ScrollTileDown": (1, "y"), "ScrollTileUp": (-1, "y"),
                "ScrollTileRightLeft": ("rl", "x"), "ScrollTileUpDown": ("rl", "y")}
ANIM_SEM_TILE = {"WaitTileAnimation", "StandingTileFrame8", "IncWaterFrame",
                 "IncFountainFrame", "DoneTileAnimation",
                 "FlickeringCaveEntrancePalette", "AnimateWaterPalette",
                 "AnimateTowerPillarTile", "LavaBubbleAnim1", "LavaBubbleAnim2"}

_RE_VTILE = re.compile(r"vTiles2 tile \$([0-9a-fA-F]+)")


def _le_anims_asm(_cache={}):
    """(tabelas, structs) de `engine/tilesets/tileset_anims.asm`.

    tabelas: tileset snake -> [(parametro, rotina)] na ordem do ciclo.
    structs: `WhirlpoolFrames1` -> (tile do gen 2, PNG dos quadros).
    """
    if _cache:
        return _cache["tabelas"], _cache["structs"]
    txt = open(f"{BW3G}/engine/tilesets/tileset_anims.asm").read().splitlines()
    rotulo_gfx = {}
    for ln in txt:
        m = re.match(r"^(\w+): INCBIN \"gfx/tilesets/(\S+)\.2bpp\"", ln.strip())
        if m:
            rotulo_gfx[m.group(1)] = m.group(2) + ".png"
    structs = {}
    for ln in txt:
        m = re.match(r"^(\w+Frames\w*): dw vTiles2 tile \$([0-9a-fA-F]+), (\w+)",
                     ln.strip())
        if m:
            structs[m.group(1)] = (int(m.group(2), 16), rotulo_gfx.get(m.group(3)))
    tabelas, pend, atual = {}, [], None
    for ln in txt:
        s = ln.strip()
        if s.startswith(";"):
            continue
        m = re.match(r"^Tileset(\w+)Anim:$", s)
        if m:
            if atual is not None:
                pend, atual = [], None
            pend.append(re.sub(r"(?<!^)(?=[A-Z])", "_", m.group(1)).lower())
            continue
        m = re.match(r"^dw\s+(.+?),\s*(\w+)\s*$", s)
        if m and pend:
            atual = atual if atual is not None else []
            for n in pend:
                tabelas.setdefault(n, atual)
            atual.append((m.group(1).strip(), m.group(2)))
            continue
        if s.endswith(":") and atual is not None:
            pend, atual = [], None
    _cache["tabelas"], _cache["structs"] = tabelas, structs
    return tabelas, structs


def _rotulo(arquivos):
    """`['forest-tree/1.png','forest-tree/2.png']` -> `forest_tree_1`. Inclui o
    nome do PRIMEIRO arquivo: sem ele as duas arvores da floresta (1+2 e 3+4)
    cairiam no mesmo rotulo e uma sobrescreveria a outra."""
    p = arquivos[0].replace(".png", "").replace("-", "_").replace("/", "_")
    return re.sub(r"_+", "_", p)


def _quadros_de_png(arquivos):
    """[[indice de cor 0..3] x 64] por quadro, lendo tiras de 8 px de largura."""
    saida = []
    for a in arquivos:
        im = Image.open(f"{BW3G}/gfx/tilesets/{a}").convert("L")
        w, h = im.size
        assert w == 8, f"{a}: {w} px de largura, quadro de animacao tem 8"
        px = im.load()
        for t in range(h // 8):
            saida.append([(255 - px[x, t * 8 + y]) // 85
                          for y in range(8) for x in range(8)])
    return saida


def _desloca(tile, dx, dy):
    return [tile[((y - dy) % 8) * 8 + ((x - dx) % 8)]
            for y in range(8) for x in range(8)]


def _quadros_de_rolagem(tile, ops):
    """Os 8 quadros de uma rolagem, pre-desenhados a partir do proprio tile.

    ponytail: a FASE nao e reproduzida ao pe da letra. No gen 2 o
    `wTileAnimationTimer` e compartilhado e cada rolagem do ciclo o incrementa de
    novo, entao dois tiles rolando no mesmo tileset saem defasados. Aqui todos
    comecam do mesmo passo. E deslocamento de 1 px num vaivem de 4; se algum dia
    isso incomodar, o conserto e dar uma fase inicial por indice de rolagem.
    """
    passo = sum(p for p, _e in (ANIM_ROLAGEM[o] for o in ops) if p != "rl")
    eixo = ANIM_ROLAGEM[ops[0]][1]
    vaivem = any(ANIM_ROLAGEM[o][0] == "rl" for o in ops)
    offs = [1, 2, 3, 4, 3, 2, 1, 0] if vaivem else \
           [(k * passo) % 8 for k in range(ANIM_PASSOS_ROLAGEM)]
    return [_desloca(tile, o if eixo == "x" else 0, 0 if eixo == "x" else o)
            for o in offs]


def animacoes_de(nome, tile_gba, px_tiles):
    """[(tile local, rotulo do conjunto de quadros, [quadros em 4bpp])] do tileset.

    `rotulo` global (`whirlpool_1`) quando os quadros vem da fonte e servem a
    qualquer tileset, e local (`<tileset>_r<tile>`) quando sao rolagem do proprio
    desenho. E o que deixa 20 tilesets dividirem os mesmos quadros de redemoinho.
    """
    tabelas, structs = _le_anims_asm()
    linhas = tabelas.get(nome)
    if not linhas:
        return []
    saida, vistos, buf = [], set(), None

    def poe(t_gen2, rotulo, quadros, fase=0):
        local = tile_gba.get(t_gen2)
        if local is None or t_gen2 in vistos or not quadros:
            return                      # tile que nenhum bloco usa: nao paga ROM
        vistos.add(t_gen2)
        q = quadros[fase:] + quadros[:fase] if fase else quadros
        saida.append((local, rotulo, [[v + 1 for v in f] for f in q]))

    for param, rot in linhas:
        if rot == "WriteTileToBuffer":
            m = _RE_VTILE.search(param)
            buf = (int(m.group(1), 16), []) if m else None
        elif rot in ANIM_ROLAGEM and buf:
            buf[1].append(rot)
        elif rot == "WriteTileFromBuffer" and buf and buf[1]:
            t = buf[0]
            local = tile_gba.get(t)
            if local is not None:
                poe(t, f"{nome}_r{t:02x}",
                    _quadros_de_rolagem([v - 1 for v in px_tiles[local]], buf[1]))
            buf = None
        elif rot in ANIM_FIXO:
            t, arqs, fase = ANIM_FIXO[rot]
            poe(t, _rotulo(arqs) + (f"_f{fase}" if fase else ""),
                _quadros_de_png(arqs), fase)
        elif rot in ANIM_STRUCT:
            t, arq = structs.get(param, (None, None))
            if arq:
                poe(t, _rotulo([arq]), _quadros_de_png([arq]))
        elif rot in ANIM_PARAM:
            m = _RE_VTILE.search(param)
            if m:
                poe(int(m.group(1), 16), _rotulo(ANIM_PARAM[rot]),
                    _quadros_de_png(ANIM_PARAM[rot]))
        elif rot not in ANIM_SEM_TILE and rot not in ("WriteTileFromBuffer",):
            raise AssertionError(f"{nome}: rotina de animacao desconhecida: {rot}")
    return saida


# ------------------------------------------------------------------ portas extras

def portas_necessarias(nome, _cache={}):
    """{(bloco, quadrante)} sob warp cuja colisao da fonte nao dispara warp aqui.

    No gen 2 o warp dispara em qualquer casa, o evento e que manda; no gen 3
    `IsWarpMetatileBehavior` exige porta, escada ou seta. Traduzir ao pe da letra
    deixa porta muda, entao o tileset ganha uma VARIANTE do mesmo desenho com
    comportamento de porta, e o metatile debaixo do warp usa a variante. O warp
    nao se move, e nenhum outro tile do mapa muda.
    """
    if nome in _cache:
        return _cache[nome]
    ok = {c for c in bd.CLASSES if MB[COMPORTAMENTO[c]] in bd.COMPORTA_WARP}
    saida = set()
    itens, _ = bd.mapas_unova()
    for _n, l, tset, _camel, arq, w, h, _amb in itens:
        if tset != nome:
            continue
        d = bd.le_map_json(_n)
        if not d:
            continue
        crus = open(arq, "rb").read()
        crus = (crus + bytes(w * h))[:w * h]
        coll = bd.quadrantes(f"{nome}_collision.asm")
        for wp in d.get("warp_events") or []:
            x, y = wp.get("x", 0), wp.get("y", 0)
            if not (0 <= x < l["width"] and 0 <= y < l["height"]):
                continue
            bx, by, q = x // 2, y // 2, (y % 2) * 2 + (x % 2)
            b = crus[by * w + bx]
            if b >= 0 and coll.get(b, ("parede",) * 4)[q] not in ok:
                saida.add((b, q))
    _cache[nome] = saida
    return saida


# ------------------------------------------------------------------ pulos extras

def pulos_necessarios(nome, _cache={}):
    """{(bloco, quadrante, classe_de_ledge)} das PAREDES que precisam de MB_JUMP_*.

    Mesmo formato e mesma ideia de `portas_necessarias`, so que aqui quem decide e
    a geometria do mapa e nao o warp: `blockdata_unova.alvos_de_pulo` diz quais
    tiles ficam entre um ledge do gen 2 e um pouso andavel, e sao esses que
    ganham a variante do mesmo desenho com o comportamento de pulo. Um mesmo
    (bloco, quadrante) pode ser alvo de direcoes diferentes em mapas diferentes,
    por isso a direcao entra na chave.
    """
    if nome in _cache:
        return _cache[nome]
    saida = set()
    itens, _ = bd.mapas_unova()
    coll = bd.quadrantes(f"{nome}_collision.asm")
    for _n, l, tset, _camel, arq, w, h, _amb in itens:
        if tset != nome:
            continue
        crus = open(arq, "rb").read()
        crus = (crus + bytes(w * h))[:w * h]
        for (x, y), ledge in bd.alvos_de_pulo(crus, w, h, coll).items():
            b = crus[(y // 2) * w + (x // 2)]
            saida.add((b, (y % 2) * 2 + (x % 2), ledge))
    _cache[nome] = saida
    return saida


# --------------------------------------------------------------------- gravacao

def pasta_de(nome):
    return f"{DESTINO}/unova_{nome}"


def rotulo_de(nome):
    return "Unova" + "".join(p.capitalize() for p in nome.split("_"))


def _escreve_tiles_png(ts, caminho):
    n = len(ts["tiles"])
    linhas = (n + 15) // 16
    im = Image.new("P", (128, linhas * 8), 0)
    plana = []
    for lin in range(linhas):
        for y in range(8):
            for col in range(16):
                t = lin * 16 + col
                plana += ts["tiles"][t][y * 8:y * 8 + 8] if t < n else [0] * 8
    im.putdata(plana)
    im.putpalette([v for c in ts["paletas"][NUM_PALS_IN_PRIMARY] for v in c])
    im.save(caminho)


PASTA_ANIM = f"{DESTINO}/unova_anim"
_CINZA = [v for i in range(16) for v in ((i * 17,) * 3)]


def grava_animacoes(ts):
    """Grava os quadros em PNG 4bpp. Rotulo global (redemoinho, flor, fonte) e
    gravado UMA vez e usado por todos os tilesets que o citam: sao 20 tilesets
    dividindo os mesmos 4 x 11 quadros de redemoinho."""
    for _local, rotulo, quadros in ts["animacoes"]:
        d = f"{PASTA_ANIM}/{rotulo}"
        os.makedirs(d, exist_ok=True)
        for i, q in enumerate(quadros):
            p = f"{d}/{i:02d}.png"
            im = Image.new("P", (8, 8), 0)
            im.putdata(q)
            im.putpalette(_CINZA)
            if os.path.exists(p):
                anterior = list(Image.open(p).convert("P").getdata())
                assert anterior == q, \
                    f"{p}: dois tilesets querem quadros diferentes no mesmo rotulo"
                continue
            im.save(p)


def grava(ts):
    d = pasta_de(ts["nome"])
    os.makedirs(f"{d}/palettes", exist_ok=True)
    _escreve_tiles_png(ts, f"{d}/tiles.png")
    for i, p in enumerate(ts["paletas"]):
        with open(f"{d}/palettes/{i:02d}.pal", "w") as f:
            f.write("JASC-PAL\n0100\n16\n")
            for r, g, b in p:
                f.write(f"{r} {g} {b}\n")
    open(f"{d}/metatiles.bin", "wb").write(ts["metatiles"])
    open(f"{d}/metatile_attributes.bin", "wb").write(ts["atributos"])
    grava_animacoes(ts)
    return d


def kb(ts):
    """KB de ROM: tiles (4bpp cru, antes do fastSmol) + metatiles + attrs + paletas.

    Teto, nao medida: o build ainda comprime os tiles com `compresSmol`. A medida
    de verdade e `kb_real`, que roda as duas ferramentas do proprio repo.
    """
    return (ts["n_tiles"] * 32 + len(ts["metatiles"]) + len(ts["atributos"])
            + 16 * 32) / 1024.0


def kb_real(ts):
    """KB de ROM MEDIDOS: passa o tiles.png pelo `gbagfx` e pelo `compresSmol`,
    que sao os dois passos que o Makefile roda (`%.4bpp: %.png` e `%.fastSmol`).
    Cai para `kb` se as ferramentas nao estiverem compiladas."""
    import subprocess
    import tempfile
    gfx, smol = f"{RAIZ}/tools/gbagfx/gbagfx", f"{RAIZ}/tools/compresSmol/compresSmol"
    if not (os.path.exists(gfx) and os.path.exists(smol)):
        return kb(ts)
    with tempfile.TemporaryDirectory() as d:
        png, bpp, fs = f"{d}/t.png", f"{d}/t.4bpp", f"{d}/t.4bpp.fastSmol"
        _escreve_tiles_png(ts, png)
        subprocess.run([gfx, png, bpp], check=True, capture_output=True)
        subprocess.run([smol, "-w", bpp, fs, "false", "false", "false"],
                       check=True, capture_output=True)
        tiles = os.path.getsize(fs)
    return (tiles + len(ts["metatiles"]) + len(ts["atributos"]) + 16 * 32) / 1024.0


# ------------------------------------------------------------------- registro em C

MARCA = "// --- Unova (B12.a, tileset_gen2.py) ---"


def _insere(caminho, bloco, antes=None, chave=None):
    """Acrescenta `bloco` no fim do arquivo, ou logo antes da linha `antes`
    (que e o `#endif` da guarda de `include/tilesets.h`: escrever depois dele
    poe a declaracao fora da guarda de inclusao dupla).

    `chave` e o simbolo que prova que a entrada ja existe. Comparar o bloco
    INTEIRO nao serve depois que `liga_animacao` troca o `.callback`: o texto
    velho deixa de casar e a entrada entraria duplicada.
    """
    txt = open(caminho).read()
    if (chave or bloco.strip()) in txt:
        return False
    if MARCA not in txt:
        marca = f"\n{MARCA}\n"
    else:
        marca = ""
    if antes and antes in txt:
        i = txt.rindex(antes)
        txt = txt[:i] + marca + bloco + "\n" + txt[i:]
    else:
        txt = txt.rstrip("\n") + "\n" + marca + bloco
    open(caminho, "w").write(txt)
    return True


ARQ_ANIM_C = f"{RAIZ}/src/data/tilesets/anims_unova.h"

_CAB_ANIM = """// GERADO por `python3 dev_scripts/tileset_gen2.py --usados --gravar`.
// Nao editar a mao: a proxima rodada sobrescreve o arquivo inteiro.
//
// Porte da animacao de tileset do BW3G (gen 2). No gen 2 cada linha de
// `engine/tilesets/tileset_anims.asm` roda num quadro do ciclo e escreve 16
// bytes num tile de VRAM; aqui os quadros ja vem prontos em 4bpp e quem os
// despeja e a fila do V-blank do proprio pokeemerald
// (`AppendTilesetAnimToBuffer` / `TransferTilesetAnimsBuffer`), a mesma que
// General, Rustboro e Sootopolis usam. Nenhum mecanismo novo.
//
// Custo de CPU: `TilesetAnim_Unova` so enfileira a animacao de indice
// `timer % 16`, entao no maximo UMA transferencia de 32 bytes por quadro, como
// no gen 2, onde cada linha da tabela tambem rodava num quadro so.
"""


def _c_nome(s):
    return re.sub(r"[^0-9a-zA-Z]", "_", s)


def gera_anims_c(nomes):
    """Escreve `src/data/tilesets/anims_unova.h` inteiro e liga o `.callback` de
    cada tileset animado em `headers.h`. Devolve (bytes de quadro, tilesets)."""
    conjuntos, blocos, inits, bytes_quadro = {}, [], [], 0
    for n in nomes:
        ts = converte(n, portas_necessarias(n), pulos_necessarios(n))
        anims = ts["animacoes"]
        if not anims:
            continue
        for _local, rotulo, quadros in anims:
            if rotulo in conjuntos:
                continue
            conjuntos[rotulo] = len(quadros)
            bytes_quadro += len(quadros) * 32
        r = rotulo_de(n)
        linhas = "\n".join(
            f"    {{ sUnovaAnimFrames_{_c_nome(rot)}, "
            f"ARRAY_COUNT(sUnovaAnimFrames_{_c_nome(rot)}), {local} }},"
            for local, rot, _q in anims)
        blocos.append(f"static const struct UnovaTilesetAnim "
                      f"sUnovaAnim_{r}[] =\n{{\n{linhas}\n}};\n")
        inits.append(f"void InitTilesetAnim_{r}(void)\n{{\n"
                     f"    InitUnovaTilesetAnim(sUnovaAnim_{r}, "
                     f"ARRAY_COUNT(sUnovaAnim_{r}));\n}}\n")
    partes = [_CAB_ANIM]
    for rotulo, n_q in sorted(conjuntos.items()):
        c = _c_nome(rotulo)
        for i in range(n_q):
            partes.append(f'static const u16 sUnovaAnimGfx_{c}_{i:02d}[] = '
                          f'INCGFX_U16("data/tilesets/secondary/unova_anim/'
                          f'{rotulo}/{i:02d}.png", ".4bpp");')
        alvos = ",\n".join(f"    sUnovaAnimGfx_{c}_{i:02d}" for i in range(n_q))
        partes.append(f"\nstatic const u16 *const sUnovaAnimFrames_{c}[] =\n"
                      f"{{\n{alvos}\n}};\n")
    partes += blocos + inits
    open(ARQ_ANIM_C, "w").write("\n".join(partes))
    return bytes_quadro, len(inits)


def liga_animacao(nomes):
    """Troca `.callback = NULL` por `InitTilesetAnim_Unova<X>` nos tilesets que
    tem animacao, e declara o init em `include/tileset_anims.h`."""
    h = open(f"{RAIZ}/src/data/tilesets/headers.h").read()
    decls, n = [], 0
    for nome in nomes:
        r = rotulo_de(nome)
        if not converte(nome, portas_necessarias(nome))["animacoes"]:
            continue
        decls.append(f"void InitTilesetAnim_{r}(void);")
        alvo = f"const struct Tileset gTileset_{r} =\n{{\n"
        i = h.find(alvo)
        if i < 0:
            continue
        fim = h.index("};", i)
        corpo = h[i:fim]
        if ".callback = NULL," in corpo:
            h = h[:i] + corpo.replace(".callback = NULL,",
                                      f".callback = InitTilesetAnim_{r},") + h[fim:]
            n += 1
    open(f"{RAIZ}/src/data/tilesets/headers.h", "w").write(h)
    ta = f"{RAIZ}/include/tileset_anims.h"
    txt = open(ta).read()
    novas = [d for d in decls if d not in txt]
    if novas:
        i = txt.rindex("#endif")
        marca = "" if MARCA in txt else f"\n{MARCA}\n"
        txt = txt[:i] + marca + "\n".join(novas) + "\n\n" + txt[i:]
        open(ta, "w").write(txt)
    return n


def registra(nome, dentro_da_build=True, motivo=""):
    """Escreve as quatro entradas que o expansion espera, copiando o padrao dos
    tilesets secundarios de Sinnoh (cave_sinnoh, canalave, celestic)."""
    r, pasta = rotulo_de(nome), f"data/tilesets/secondary/unova_{nome}"
    pals = "\n".join(f'    INCGFX_U16("{pasta}/palettes/{i:02d}.pal", ".gbapal"),'
                     for i in range(16))
    graficos = (f'const u32 gTilesetTiles_{r}[] = '
                f'INCGFX_U32("{pasta}/tiles.png", ".4bpp.fastSmol");\n\n'
                f'const u16 gTilesetPalettes_{r}[][16] =\n{{\n{pals}\n}};\n')
    metas = (f'const u16 gMetatiles_{r}[] = INCBIN_U16("{pasta}/metatiles.bin");\n'
             f'const u16 gMetatileAttributes_{r}[] = '
             f'INCBIN_U16("{pasta}/metatile_attributes.bin");\n')
    header = (f'const struct Tileset gTileset_{r} =\n{{\n'
              f'    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n'
              f'    .tiles = gTilesetTiles_{r},\n'
              f'    .palettes = gTilesetPalettes_{r},\n'
              f'    .metatiles = gMetatiles_{r},\n'
              f'    .metatileAttributes = gMetatileAttributes_{r},\n'
              f'    .callback = NULL,\n}};\n')
    externo = f"extern const struct Tileset gTileset_{r};\n"
    if not dentro_da_build:
        cab = f"// FORA DA BUILD: {motivo}\n"
        graficos = cab + "\n".join("// " + l for l in graficos.splitlines()) + "\n"
        metas = cab + "\n".join("// " + l for l in metas.splitlines()) + "\n"
        header = cab + "\n".join("// " + l for l in header.splitlines()) + "\n"
        externo = cab + "// " + externo
    c = "" if dentro_da_build else "// "
    n = 0
    n += _insere(f"{RAIZ}/src/data/tilesets/graphics.h", "\n" + graficos,
                 chave=f"{c}const u32 gTilesetTiles_{r}[]")
    n += _insere(f"{RAIZ}/src/data/tilesets/metatiles.h", "\n" + metas,
                 chave=f"{c}const u16 gMetatiles_{r}[]")
    n += _insere(f"{RAIZ}/src/data/tilesets/headers.h", "\n" + header,
                 chave=f"{c}const struct Tileset gTileset_{r} =")
    n += _insere(f"{RAIZ}/include/tilesets.h", externo,
                 antes="#endif //GUARD_tilesets_H",
                 chave=f"{c}extern const struct Tileset gTileset_{r};")
    return n


# ----------------------------------------------------------------------- medicao

def todos():
    """Os tilesets do BW3G que dao para converter. `unused_dark_cave` tem bloco e
    colisao mas nenhum PNG na fonte (e o nome diz que ele nao e usado); fica fora
    aqui e nao no meio da conversao."""
    return sorted(n for n in {f[:-len("_metatiles.bin")]
                              for f in os.listdir(f"{BW3G}/data/tilesets")
                              if f.endswith("_metatiles.bin")}
                  if os.path.exists(png_de(n)))


def usados():
    """Tilesets que algum dos 291 mapas de Unova usa, mais usados primeiro."""
    u = _uso_dos_mapas()
    return sorted(u, key=lambda n: (-u[n][0], n))


def medir(nomes):
    u = _uso_dos_mapas()
    print(f"{'mapas':>5} {'tileset':26} {'blk':>4} {'mt':>4} {'til':>4} {'pal':>3} "
          f"{'KB':>6}  paleta de")
    tot = 0.0
    for n in nomes:
        ts = converte(n, portas_necessarias(n), pulos_necessarios(n))
        k = kb_real(ts)
        tot += k
        print(f"{u.get(n, (0,))[0]:5d} {n:26} {ts['blocos']:4d} {ts['n_metatiles']:4d} "
              f"{ts['n_tiles']:4d} {ts['n_paletas']:3d} {k:6.1f}  {ts['origem_pal']}")
    print(f"\n{len(nomes)} tilesets, {tot:.1f} KB no total ({tot/1024:.2f} MB), "
          f"tiles ja comprimidos com o `compresSmol` do repo")


# ------------------------------------------------------------------------- demo

def _pixels_do_gba(ts, mt):
    """Redesenha um metatile ja convertido: 16x16 de (r,g,b), camada de baixo."""
    ent = struct.unpack_from("<8H", ts["metatiles"], mt * 16)
    saida = [[None] * 16 for _ in range(16)]
    for i in range(4):
        v = ent[i]
        t, xf, yf, p = v & 0x3FF, v >> 10 & 1, v >> 11 & 1, v >> 12 & 0xF
        px = ts["tiles"][t - 512]
        ox, oy = (i % 2) * 8, (i // 2) * 8
        for y in range(8):
            for x in range(8):
                c = px[(7 - y if yf else y) * 8 + (7 - x if xf else x)]
                saida[oy + y][ox + x] = ts["paletas"][p][c]
    return saida


def _pixels_do_gen2(nome, b, q):
    """O mesmo quadrante desenhado direto da fonte, sem passar pelo conversor."""
    pals8, _ = paletas_gen2(nome)
    tiles, blocos = tiles_gen2(nome), blocos_gen2(nome)
    saida = [[None] * 16 for _ in range(16)]
    for i, (t, p, xf, yf, _pr) in enumerate(quadrante_do_bloco(blocos[b], q)):
        ox, oy = (i % 2) * 8, (i // 2) * 8
        for y in range(8):
            for x in range(8):
                c = tiles[t][(7 - y if yf else y) * 8 + (7 - x if xf else x)]
                saida[oy + y][ox + x] = rgb5_para_888(pals8[p][c])
    return saida


def demo():
    # (a) a tabela de comportamento cobre todas as classes e todo nome existe
    for c in bd.CLASSES:
        assert COMPORTAMENTO[c] in MB, f"{c}: {COMPORTAMENTO[c]} nao e um MB_*"
    # e ela nao contradiz as entradas NAO-fallback do B12.b, FORA os ledges, que
    # divergem de proposito e por isso sao conferidos logo abaixo em vez de
    # simplesmente pulados: no par EMPRESTADO o unico desenho de rampa disponivel
    # e um MB_JUMP_* de gen 3 de verdade, que tem que continuar com colisao 1
    # (senao o jogador anda em cima dele e o pulo o joga 2 casas adiante, que pode
    # ser parede); no tileset PROPRIO o desenho e nosso e vira chao comum.
    for pal, ent in bd.PALETA.items():
        for c, (_mt, col, elev, motivo) in ent.items():
            if motivo.startswith("FALLBACK") or c in LEDGES:
                continue
            assert (col, elev) == colisao_da_classe(c), \
                f"{pal}.{c}: B12.b usa ({col},{elev}), aqui {colisao_da_classe(c)}"
    for c in LEDGES:
        assert colisao_da_classe(c) == ANDA and COMPORTAMENTO[c] == "MB_NORMAL", \
            f"{c}: ledge do gen 2 tem que virar chao andavel aqui, ver o cabecalho"
        assert bd.ESPERADO[c][0].startswith("MB_JUMP_"), \
            f"{c}: o B12.b deixou de tratar ledge como ledge de gen 3; releia a divergencia"

    ts = converte("castelia", portas_necessarias("castelia"), pulos_necessarios("castelia"))

    # (b) tetos do GBA, nos 58 tilesets, nao so no de teste
    piores = {"mt": (0, ""), "til": (0, ""), "pal": (0, "")}
    for n in todos():
        # com as variantes de porta: e o numero que vai para a ROM, nao o menor
        t = converte(n, portas_necessarias(n), pulos_necessarios(n))
        assert t["n_metatiles"] <= MAX_METATILES, f"{n} estourou metatiles"
        assert t["n_tiles"] <= MAX_TILES, f"{n} estourou tiles"
        assert t["n_paletas"] <= MAX_PALETAS, f"{n} estourou paletas"
        for k, v in (("mt", t["n_metatiles"]), ("til", t["n_tiles"]),
                     ("pal", t["n_paletas"])):
            if v > piores[k][0]:
                piores[k] = (v, n)

    # (c) round-trip de um bloco conhecido: o quadrante redesenhado a partir do
    #     tileset do GBA tem que dar pixel a pixel o mesmo que a fonte do gen 2.
    #     Bloco 1 de castelia = WALL,FLOOR,FLOOR,FLOOR, e o 4 = FLOOR,FLOOR,WALL,FLOOR.
    for b, q in ((1, 0), (1, 3), (4, 2), (0, 0), (10, 1)):
        assert _pixels_do_gba(ts, ts["quad2mt"][(b, q)]) == _pixels_do_gen2("castelia", b, q), \
            f"round-trip falhou no bloco {b} quadrante {q}"

    # (d) MUTACAO: trocar um tile de proposito TEM que reprovar o round-trip.
    #     Sem isto o item (c) e so uma frase.
    guarda = ts["tiles"][1]
    try:
        ts["tiles"][1] = [(v + 1) % 4 for v in guarda]
        bateu = all(_pixels_do_gba(ts, ts["quad2mt"][(b, q)]) == _pixels_do_gen2("castelia", b, q)
                    for b, q in ((1, 0), (1, 3), (4, 2), (0, 0), (10, 1)))
        assert not bateu, "a mutacao passou pelo round-trip: ele nao serve"
    finally:
        ts["tiles"][1] = guarda

    # (e) comportamento preservado por quadrante, nos dois modos
    def confere_comportamento(t, nome_ts):
        coll = bd.quadrantes(f"{nome_ts}_collision.asm")
        vistos = set()
        modos = ([(t["quad2mt"], False)] if t["tem_normal"] else []) + \
                ([(t["masmorra2mt"], True)] if t["tem_masmorra"] else [])
        for dic, masmorra in modos:
            for (b, q), mt in dic.items():
                classe = coll.get(b, ("parede",) * 4)[q]
                if masmorra and classe == "chao":
                    classe = "chao_caverna"
                beh = struct.unpack_from("<H", t["atributos"], mt * 2)[0] & 0xFF
                assert beh == MB[COMPORTAMENTO[classe]], \
                    f"{nome_ts} bloco {b} quadrante {q}: classe {classe} " \
                    f"virou comportamento {beh}"
                vistos.add(classe)
        for (b, q, ledge), mt in t["pulo2mt"].items():
            beh = struct.unpack_from("<H", t["atributos"], mt * 2)[0] & 0xFF
            assert beh == MB[bd.ESPERADO[ledge][0]], \
                f"{nome_ts} bloco {b} quadrante {q}: variante de pulo {ledge} " \
                f"saiu com comportamento {beh}"
            vistos.add(PULO_CLASSE[ledge])
        return vistos

    assert {"chao", "parede", "porta"} <= confere_comportamento(ts, "castelia"), \
        "castelia sem porta/chao/parede"

    # (e1) o deslocamento de um tile: o ledge do gen 2 tem que sair ANDAVEL e a
    #      parede que ele pula tem que sair com MB_JUMP_*. Sem os dois lados o
    #      pulo some e o mapa se parte em ilhas (Unova_DragonspiralTower3F e
    #      Unova_OpelucidGym, medidos por flood fill em 12/08/2026).
    torre = converte("tower", portas_necessarias("tower"), pulos_necessarios("tower"))
    assert torre["pulo2mt"], "tower sem variante de pulo: alvos_de_pulo nao achou nada"
    for (b, q, ledge), mt in torre["pulo2mt"].items():
        beh = struct.unpack_from("<H", torre["atributos"], mt * 2)[0] & 0xFF
        assert beh == MB[bd.ESPERADO[ledge][0]] and colisao_da_classe(PULO_CLASSE[ledge]) == BLOQ
    for (b, q), mt in torre["quad2mt"].items():
        if bd.quadrantes("tower_collision.asm").get(b, ("parede",) * 4)[q] in LEDGES:
            beh = struct.unpack_from("<H", torre["atributos"], mt * 2)[0] & 0xFF
            assert beh == MB["MB_NORMAL"], \
                f"tower bloco {b} quadrante {q}: ledge do gen 2 nao virou chao"

    # (e1b) MUTACAO da regra conservadora de `alvos_de_pulo`: alvo cujo POUSO e
    #       parede tem que ser recusado, senao o jogador pula para dentro do muro
    #       (o gen 3 nao confere o pouso, o gen 2 confere).
    coll_t = bd.quadrantes("tower_collision.asm")
    guarda = bd.ANDAVEL_FONTE
    try:
        bd.ANDAVEL_FONTE = ()          # nenhum pouso vale
        for n, l, tset, camel, arq, w, h, amb in bd.mapas_unova()[0]:
            if tset == "tower":
                crus = (open(arq, "rb").read() + bytes(w * h))[:w * h]
                assert not bd.alvos_de_pulo(crus, w, h, coll_t), \
                    "alvos_de_pulo aceitou pouso em parede: a regra nao filtra nada"
                break
    finally:
        bd.ANDAVEL_FONTE = guarda
    # tileset com grama e com agua de verdade, para nao provar so o caso facil
    assert "grama" in confere_comportamento(converte("forest"), "forest"), \
        "forest sem grama"
    assert "agua" in confere_comportamento(converte("unova_beach"), "unova_beach"), \
        "unova_beach sem agua"

    # (e2) o chao de masmorra tem que sair com comportamento que dispara encontro
    #      (`TILE_FLAG_HAS_ENCOUNTERS`), senao os 18 mapas mudos do B12.c seguem
    #      mudos com arte nova, que e trocar o problema de lugar.
    for n in ("tower", "desert", "traditional_house", "forest", "facility"):
        t = converte(n)
        c = bd.quadrantes(f"{n}_collision.asm")
        chaos = [mt for (b, q), mt in t["masmorra2mt"].items()
                 if c.get(b, ("parede",) * 4)[q] == "chao"]
        assert chaos, f"{n} sem um quadrante de chao sequer"
        for mt in chaos:
            assert struct.unpack_from("<H", t["atributos"], mt * 2)[0] & 0xFF \
                == MB["MB_CAVE"], f"{n}: chao de masmorra sem MB_CAVE"

    # (f) camada: tile SEM prioridade nao pode aparecer na camada de cima, e tile
    #     COM prioridade tem que aparecer nas duas.
    tp = converte("village_bridge")     # 385 tiles com prioridade, o campeao
    n_prio = 0
    for i, (vis, _c) in enumerate(tp["ordem"]):
        ent = struct.unpack_from("<8H", tp["metatiles"], i * 16)
        for k, (_t, _p, _xf, _yf, prio) in enumerate(vis):
            if prio:
                assert ent[4 + k] == ent[k], f"prioridade {i}/{k} nao foi para cima"
                n_prio += 1
            else:
                assert ent[4 + k] & 0x3FF == 512, f"{i}/{k} sujou a camada de cima"
    assert n_prio > 0, "village_bridge sem tile de prioridade"

    # (g) a cor 0 do gen 2 nunca vira a cor 0 do GBA (que e transparente)
    assert all(v > 0 for t in ts["tiles"][1:] for v in t), "tile com cor 0 (buraco)"
    assert set(ts["tiles"][0]) == {0}, "o tile 0 tinha que ser o vazio"

    # (h) idempotente
    assert converte("castelia")["metatiles"] == converte("castelia")["metatiles"]

    # (i) ANIMACAO: round-trip dos quadros contra a fonte, e o filtro que importa
    n_anim, tiles_anim = 0, 0
    for n in usados():
        t = converte(n)
        alvos = [l for l, _r, _q in t["animacoes"]]
        assert len(alvos) == len(set(alvos)), f"{n}: dois animadores no mesmo tile"
        for local, rotulo, quadros in t["animacoes"]:
            assert 0 < local < t["n_tiles"], f"{n}: animacao no tile {local}, fora"
            assert all(len(q) == 64 for q in quadros), f"{n}/{rotulo}: quadro torto"
            assert all(0 < v < 5 for q in quadros for v in q), \
                f"{n}/{rotulo}: cor fora de 1..4 (o +1 do gen 2 nao foi aplicado)"
        n_anim += 1 if t["animacoes"] else 0
        tiles_anim += len(t["animacoes"])
    # round-trip de um conjunto conhecido: os 11 quadros do redemoinho 1 da
    # Castelia tem que ser, pixel a pixel, `gfx/tilesets/whirlpool/1.png` + 1.
    tc = converte("castelia")
    wp = next(q for _l, r, q in tc["animacoes"] if r == "whirlpool_1")
    fonte = _quadros_de_png(["whirlpool/1.png"])
    assert len(wp) == len(fonte) == 11, f"redemoinho com {len(wp)} quadros"
    assert wp == [[v + 1 for v in f] for f in fonte], "quadro do redemoinho nao bate"
    # a fonte de Castelia tem que estar la, e nos SEIS tiles que o .asm cita
    assert sum(1 for _l, r, _q in tc["animacoes"]
               if r.startswith("castelia_fountain")) == 6, "fonte de Castelia incompleta"
    # rolagem: o quadro 0 e o proprio tile, e o ultimo volta ao lugar
    to = converte("opelucid")
    rol = next(q for _l, r, q in to["animacoes"] if r.startswith("opelucid_r"))
    assert len(rol) == 8 and rol[-1] == rol[7], "rolagem sem os 8 quadros"
    assert len({tuple(q) for q in rol}) > 1, "rolagem que nao mexe em nada"
    # MUTACAO: apontar a animacao para um tile que nenhum bloco usa TEM que
    # descartar a entrada, senao a ROM paga quadro que ninguem ve.
    assert any(r.startswith("flower") for _l, r, _q in converte("nimbasa")["animacoes"])
    guarda = ANIM_FIXO["AnimateFlowerTile"]
    try:
        orfao = next(t for t in range(256)
                     if t not in converte("nimbasa")["tile_gba"])
        ANIM_FIXO["AnimateFlowerTile"] = (orfao, guarda[1], guarda[2])
        assert not any(r.startswith("flower")
                       for _l, r, _q in converte("nimbasa")["animacoes"]), \
            "tile que nenhum bloco usa passou pelo filtro e pagaria ROM"
    finally:
        ANIM_FIXO["AnimateFlowerTile"] = guarda

    print(f"demo ok: {len(todos())} tilesets convertem dentro dos tetos "
          f"(pior metatiles {piores['mt'][0]} em {piores['mt'][1]}, "
          f"pior tiles {piores['til'][0]} em {piores['til'][1]}, "
          f"pior paletas {piores['pal'][0]} em {piores['pal'][1]}); "
          f"round-trip de 5 quadrantes de castelia bate pixel a pixel e a mutacao "
          f"foi pega; comportamento conferido em castelia, forest e unova_beach; "
          f"{n_prio} tiles de prioridade em duas camadas em village_bridge; "
          f"{tiles_anim} tiles animados em {n_anim} tilesets, round-trip do "
          f"redemoinho e da fonte de Castelia, mutacao do filtro pega")


# ---------------------------------------------------------------------- execucao

def main():
    arg = sys.argv[1:]
    if "--demo" in arg:
        return demo()
    if "--medir" in arg:
        return medir(usados() if "--usados" in arg else todos())
    nomes = usados() if "--usados" in arg else [a for a in arg if not a.startswith("--")]
    if not nomes:
        print(__doc__.split("\n\n")[1])
        return 1
    for n in nomes:
        ts = converte(n, portas_necessarias(n), pulos_necessarios(n))
        extra = len(set(ts["porta2mt"].values()))
        print(f"{n:26} {ts['n_metatiles']:4d} metatiles, {ts['n_tiles']:4d} tiles, "
              f"{ts['n_paletas']} paletas, {kb_real(ts):6.1f} KB, paleta de "
              f"{ts['origem_pal']}, {extra} variantes de porta")
        if "--gravar" in arg:
            grava(ts)
            registra(n)
    if "--gravar" in arg:
        b, q = gera_anims_c([n for n in nomes if n in usados()])
        print(f"\nanimacao: {q} tilesets, {b/1024:.1f} KB de quadros; "
              f"callbacks ligados: {liga_animacao(nomes)}")
    if "--gravar" not in arg:
        print("\n(nada gravado; use --gravar)")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
