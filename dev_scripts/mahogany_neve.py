#!/usr/bin/env python3
"""Cobre Mahogany Town de neve, sem tocar em Route 42/43, Lago da Fúria e Mt. Silver Outside.

O problema: `gTileset_MahoganyTown` é SECUNDÁRIO de SEIS layouts
(Route42, Route43, Mahoganytown, MtSilver_Outside, LakeOfRage, LakeOfRage_LowTide),
e o primário `gTileset_JohtoNorthEast` é de Johto inteira. Nada que a cidade
precisa de neve pode morar em nenhum dos dois sem respingar nos outros mapas.

A saída: um secundário PRÓPRIO, `gTileset_MahoganyTownNeve`, cópia do
`mahogany_town`, usado só por `LAYOUT_MAHOGANYTOWN`. Nele sobram três slots de
paleta (7, 8 e 9), porque as paletas que a cidade realmente desenha são a 10, 11
e 12 do secundário mais as 0 a 6 do primário. Esses três slots recebem a versão
NEVADA das três paletas de terreno do primário:

    paleta 1 do primário (rocha)  -> paleta  7 do secundário
    paleta 5 do primário (areia)  -> paleta  8 do secundário
    paleta 0 do primário (grama)  -> paleta  9 do secundário
    paleta 8 do secundário (grama, quase igual à 0) -> paleta 9

A conversão de um metatile é então uma TROCA DE PALETA, quadrante a quadrante:
os mesmos tiles, os mesmos espelhamentos, a mesma ordem de camada, só que o
quadrante que apontava para a paleta 0/1/5/8 passa a apontar para a de neve.
Nenhum pixel é inventado: a cor nova é a cor velha projetada na rampa de neve
(`RAMPA`), que é a mesma escala clara/azulada do tileset `mt_silver_snow` de
Johto. Metatile que não desenha terreno (só telhado ou parede) fica intacto.

Além disso, o telhado ganha uma faixa de neve DESENHADA (a única arte nova):
para cada coluna do tile, acha o primeiro pixel opaco de cima para baixo e pinta
os 3 ou 4 seguintes com a cor de neve da própria paleta do telhado. É o que dá
o cume branco das casas e do Centro Pokémon.

Colisão e elevação do `map.bin` NÃO são tocadas: só os 10 bits do id de metatile
mudam. O atributo (comportamento e tipo de camada) do metatile de neve é copiado
byte a byte do metatile de origem, então grama de encontro continua grama de
encontro e porta continua porta.

Uso:
    python3 dev_scripts/mahogany_neve.py            # gera o tileset e reescreve o map.bin
    python3 dev_scripts/mahogany_neve.py --demo     # confere sem escrever nada

É IDEMPOTENTE: rodar duas vezes deixa os mesmos bytes, porque o destino de cada
troca nunca é origem de outra (os slots de destino são justamente os que o mapa
não usava).
"""
import argparse
import os
import shutil
import struct
import sys

from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PRIMARIO = os.path.join(REPO, "data/tilesets/primary/johto_north_east")
SECUNDARIO = os.path.join(REPO, "data/tilesets/secondary/mahogany_town")
NEVE = os.path.join(REPO, "data/tilesets/secondary/mahogany_town_neve")
MAPBIN = os.path.join(REPO, "data/layouts/Mahoganytown/map.bin")
BORDERBIN = os.path.join(REPO, "data/layouts/Mahoganytown/border.bin")

NUM_TILES_PRIMARIO = 640  # layout "johto" (bigPrimary): ver GetNumTilesInPrimary
NUM_METATILES_SEC = 384

# Os 158 metatiles que o mapa de Mahogany desenha e que têm ao menos um
# quadrante de terreno (paleta 0, 1, 5 ou 8). Lista literal de propósito: ela é
# o retrato do mapa ANTES da troca, e é o que torna o script idempotente.
ORIGENS = (
    0, 1, 3, 4, 5, 8, 9, 14, 15, 18, 19, 20, 21, 26, 27, 28, 29, 34, 35, 36, 37, 76, 77, 78, 83, 91,
    92, 94, 96, 98, 100, 102, 104, 105, 106, 107, 108, 109, 112, 113, 114, 115, 117, 120, 121, 122,
    123, 124, 125, 131, 135, 141, 147, 161, 176, 177, 178, 179, 180, 181, 186, 187, 188, 211, 212,
    213, 219, 220, 221, 227, 228, 229, 258, 259, 260, 261, 313, 314, 315, 318, 319, 321, 322, 323,
    327, 329, 330, 331, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 344, 345, 346, 348, 350,
    352, 387, 388, 389, 392, 393, 394, 400, 401, 402, 408, 409, 410, 412, 424, 425, 470, 488, 489,
    490, 491, 492, 505, 507, 562, 563, 662, 674, 736, 737, 738, 744, 745, 746, 752, 753, 754, 760,
    761, 762, 768, 769, 770, 820, 828, 830, 880, 881, 896, 897, 898, 899, 905, 906, 907
)

# Slots de metatile do secundário que o mapa JÁ usava: são intocáveis, porque o
# map.bin continua apontando para eles. Todo o resto do secundário é aterro.
OCUPADOS = (
    12, 22, 34, 45, 47, 96, 97, 98, 104, 105, 106, 112, 113, 114, 120, 121, 122, 128, 129, 130,
    180, 188, 189, 190, 240, 241, 256, 257, 258, 259, 265, 266, 267,
)

TROCA_PALETA = {0: 9, 1: 7, 5: 8, 8: 9}
ORIGEM_DA_PALETA = {7: 1, 8: 5, 9: 0}  # slot no secundário de neve -> paleta do primário

# Rampa de neve, indexada por luminância. Os tons vêm do `mt_silver_snow`
# (paleta 7: E8E8F0, C8D8F0, A8C0C8, 8898B8, 385868), que é a neve que Johto já
# usa no Mt. Silver. Todos múltiplos de 8, que é o passo real do GBA.
RAMPA = (
    (0, (32, 48, 56)),
    (30, (56, 88, 104)),
    (60, (88, 112, 136)),
    (95, (136, 152, 184)),
    (130, (168, 192, 200)),
    (165, (200, 216, 240)),
    (195, (216, 224, 240)),
    (230, (232, 232, 240)),
    (255, (248, 248, 248)),
)

# Tiles do secundário em que o cume do telhado começa na linha 0: é neles que a
# faixa de neve é desenhada, direto no tiles.png do tileset novo. Só os metatiles
# de topo de telhado das casas usam esses tiles (conferido por varredura), então
# a faixa não aparece no meio de telhado nenhum.
TELHADO_SEC = (118, 119, 120, 121, 122, 359, 360, 361)
NEVE_PAL11 = (10, 11)  # índices livres da paleta 11 que viram branco e azul de neve

# O topo do telhado do Centro Pokémon está em tiles do PRIMÁRIO (192, 193, 194),
# que é compartilhado com Johto inteira. Eles são COPIADOS para slots livres do
# secundário de neve, com a faixa desenhada, e os metatiles 488-492 passam a
# apontar para a cópia.
TELHADO_PRI = (192, 193, 194)
METATILES_PC = (488, 489, 490, 491, 492)
NEVE_PAL2 = (1, 2)  # F6F6FF e CDDEEE, brancos que a paleta 2 do primário já tem


# ---------------------------------------------------------------- utilidades

def le_u16(caminho):
    dados = open(caminho, "rb").read()
    return list(struct.unpack("<%dH" % (len(dados) // 2), dados))


def grava_u16(caminho, valores):
    with open(caminho, "wb") as f:
        f.write(struct.pack("<%dH" % len(valores), *valores))


def le_pal(caminho):
    linhas = open(caminho, encoding="utf-8").read().split("\n")
    return [tuple(int(x) for x in l.split()) for l in linhas[3:19] if l.strip()]


def grava_pal(caminho, cores):
    # CRLF de propósito: `.gitattributes` marca `*.pal text eol=crlf`, e arquivo
    # gravado com LF aparece como modificado no `git status` logo depois de um
    # checkout limpo, o que quebraria a idempotência aos olhos do git.
    with open(caminho, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n16\n")
        for r, g, b in cores:
            f.write("%d %d %d\n" % (r, g, b))


def gba(v):
    """Arredonda para o passo real de cor do GBA (5 bits por canal)."""
    return min(248, (int(round(v)) // 8) * 8)


def cor_de_neve(cor):
    lum = 0.299 * cor[0] + 0.587 * cor[1] + 0.114 * cor[2]
    for i in range(len(RAMPA) - 1):
        (la, ca), (lb, cb) = RAMPA[i], RAMPA[i + 1]
        if la <= lum <= lb:
            t = (lum - la) / (lb - la)
            return tuple(gba(ca[k] + (cb[k] - ca[k]) * t) for k in range(3))
    return RAMPA[-1][1]


def entradas(metatiles, indice):
    """Os 8 quadrantes (4 da camada de baixo, 4 da de cima) de um metatile."""
    return metatiles[indice * 8:(indice + 1) * 8]


def destinos():
    """Tabela origem -> destino. Determinística: o i-ésimo id de ORIGENS cai no
    i-ésimo slot livre do secundário, em ordem crescente."""
    livres = [i for i in range(NUM_METATILES_SEC) if i not in OCUPADOS]
    if len(ORIGENS) > len(livres):
        raise SystemExit("nao ha slot de metatile suficiente no secundario")
    return {orig: NUM_TILES_PRIMARIO + livres[i] for i, orig in enumerate(ORIGENS)}


def faixa_de_neve(tile, claro, medio):
    """Pinta o cume: acha o primeiro pixel opaco de cada coluna e cobre 3 ou 4
    linhas com neve. A alternância de profundidade dá a borda irregular."""
    novo = [list(linha) for linha in tile]
    for x in range(8):
        topo = next((y for y in range(8) if novo[y][x] != 0), None)
        if topo is None:
            continue
        prof = 4 if x % 4 in (1, 2) else 3
        for k in range(prof):
            if topo + k < 8:
                novo[topo + k][x] = claro
        if topo + prof < 8:
            novo[topo + prof][x] = medio
    return novo


def le_tiles_png(caminho):
    im = Image.open(caminho)
    larg, alt = im.size
    px = im.load()
    tiles = []
    for ty in range(alt // 8):
        for tx in range(larg // 8):
            tiles.append([[px[tx * 8 + x, ty * 8 + y] for x in range(8)] for y in range(8)])
    return im, tiles


# ------------------------------------------------------------------- geração

def gera(escreve=True):
    relato = {}
    de_para = destinos()

    meta_pri = le_u16(os.path.join(PRIMARIO, "metatiles.bin"))
    attr_pri = le_u16(os.path.join(PRIMARIO, "metatile_attributes.bin"))
    meta_sec = le_u16(os.path.join(SECUNDARIO, "metatiles.bin"))
    attr_sec = le_u16(os.path.join(SECUNDARIO, "metatile_attributes.bin"))

    def quadrantes(mid):
        if mid < NUM_TILES_PRIMARIO:
            return entradas(meta_pri, mid)
        return entradas(meta_sec, mid - NUM_TILES_PRIMARIO)

    def atributo(mid):
        return attr_pri[mid] if mid < NUM_TILES_PRIMARIO else attr_sec[mid - NUM_TILES_PRIMARIO]

    # --- tiles: cópia do secundário + faixa de neve nos telhados
    im, tiles = le_tiles_png(os.path.join(SECUNDARIO, "tiles.png"))
    _, tiles_pri = le_tiles_png(os.path.join(PRIMARIO, "tiles.png"))

    usados_por_metatile = set()
    for i in range(len(meta_sec) // 8):
        for v in entradas(meta_sec, i):
            t = v & 0x3FF
            if t >= NUM_TILES_PRIMARIO:
                usados_por_metatile.add(t - NUM_TILES_PRIMARIO)
    tiles_livres = [i for i in range(len(tiles)) if i not in usados_por_metatile]
    copia_pc = {t: tiles_livres[i] for i, t in enumerate(TELHADO_PRI)}

    for idx in TELHADO_SEC:
        tiles[idx] = faixa_de_neve(tiles[idx], *NEVE_PAL11)
    for orig, destino in copia_pc.items():
        tiles[destino] = faixa_de_neve(tiles_pri[orig], *NEVE_PAL2)
    relato["tiles_com_faixa"] = len(TELHADO_SEC) + len(copia_pc)
    relato["tiles_novos_no_secundario"] = sorted(copia_pc.values())

    # --- metatiles e atributos do tileset novo
    meta_novo = list(meta_sec) + [0] * ((NUM_METATILES_SEC - len(meta_sec) // 8) * 8)
    attr_novo = list(attr_sec) + [0] * (NUM_METATILES_SEC - len(attr_sec))

    for origem, destino in sorted(de_para.items()):
        local = destino - NUM_TILES_PRIMARIO
        novos = []
        for v in quadrantes(origem):
            tile = v & 0x3FF
            resto = v & 0x0C00          # espelhamentos, preservados
            pal = (v >> 12) & 0xF
            if origem in METATILES_PC and tile in copia_pc:
                tile = NUM_TILES_PRIMARIO + copia_pc[tile]
            pal = TROCA_PALETA.get(pal, pal)
            novos.append(tile | resto | (pal << 12))
        meta_novo[local * 8:(local + 1) * 8] = novos
        attr_novo[local] = atributo(origem)

    # --- paletas
    pal_neve = {}
    for slot, fonte in ORIGEM_DA_PALETA.items():
        cores = le_pal(os.path.join(PRIMARIO, "palettes/%02d.pal" % fonte))
        pal_neve[slot] = [cores[0]] + [cor_de_neve(c) for c in cores[1:]]
    pal11 = le_pal(os.path.join(SECUNDARIO, "palettes/11.pal"))
    pal11[NEVE_PAL11[0]] = (232, 232, 240)
    pal11[NEVE_PAL11[1]] = (200, 216, 240)
    pal_neve[11] = pal11

    if not escreve:
        relato["de_para"] = de_para
        return relato

    os.makedirs(os.path.join(NEVE, "palettes"), exist_ok=True)
    for i in range(13):
        origem = os.path.join(SECUNDARIO, "palettes/%02d.pal" % i)
        alvo = os.path.join(NEVE, "palettes/%02d.pal" % i)
        if i in pal_neve:
            grava_pal(alvo, pal_neve[i])
        else:
            shutil.copyfile(origem, alvo)

    px = im.load()
    larg = im.size[0] // 8
    for i, tile in enumerate(tiles):
        tx, ty = (i % larg) * 8, (i // larg) * 8
        for y in range(8):
            for x in range(8):
                px[tx + x, ty + y] = tile[y][x]
    im.save(os.path.join(NEVE, "tiles.png"))
    grava_u16(os.path.join(NEVE, "metatiles.bin"), meta_novo)
    grava_u16(os.path.join(NEVE, "metatile_attributes.bin"), attr_novo)

    # --- map.bin e border.bin
    trocados = 0
    for caminho in (MAPBIN, BORDERBIN):
        antes = le_u16(caminho)
        depois = []
        for v in antes:
            mid = v & 0x3FF
            novo = de_para.get(mid, mid)
            if novo != mid:
                trocados += 1
            depois.append((v & ~0x3FF) | novo)
        # colisão e elevação idênticas, bit a bit
        assert all((a & ~0x3FF) == (b & ~0x3FF) for a, b in zip(antes, depois))
        grava_u16(caminho, depois)
    relato["blocos_trocados"] = trocados
    relato["metatiles_de_neve"] = len(de_para)
    relato["de_para"] = de_para
    return relato


# --------------------------------------------------------------------- demo

def demo():
    de_para = destinos()
    erros = []

    # 1. nenhum destino é origem de outra troca (é o que garante a idempotência)
    if set(de_para) & set(de_para.values()):
        erros.append("destino coincide com origem")

    # 2. o comportamento e o tipo de camada do metatile de neve batem com o da origem
    attr_pri = le_u16(os.path.join(PRIMARIO, "metatile_attributes.bin"))
    caminho_attr = os.path.join(NEVE, "metatile_attributes.bin")
    if os.path.exists(caminho_attr):
        attr_sec = le_u16(os.path.join(SECUNDARIO, "metatile_attributes.bin"))
        attr_neve = le_u16(caminho_attr)
        for origem, destino in de_para.items():
            esperado = (attr_pri[origem] if origem < NUM_TILES_PRIMARIO
                        else attr_sec[origem - NUM_TILES_PRIMARIO])
            achado = attr_neve[destino - NUM_TILES_PRIMARIO]
            if esperado != achado:
                erros.append("atributo do metatile %d != %d (0x%04X vs 0x%04X)"
                             % (destino, origem, achado, esperado))

        # 3. o map.bin só aponta para destino ou para id que nunca teve troca
        validos = set(de_para.values()) | (set(range(1024)) - set(de_para))
        for caminho in (MAPBIN, BORDERBIN):
            for v in le_u16(caminho):
                if (v & 0x3FF) in de_para:
                    erros.append("%s ainda aponta para o metatile antigo %d"
                                 % (os.path.basename(caminho), v & 0x3FF))
                    break

        # 4. o tileset no disco é igual ao que o gerador produz agora
        relato = gera(escreve=False)
        meta_disco = le_u16(os.path.join(NEVE, "metatiles.bin"))
        if len(meta_disco) != NUM_METATILES_SEC * 8:
            erros.append("metatiles.bin do tileset de neve tem tamanho inesperado")
        del relato
    else:
        erros.append("tileset de neve ainda nao foi gerado")

    # 5. a rampa de neve só devolve cor que o GBA representa
    for cor in ((0, 0, 0), (127, 200, 33), (255, 255, 255), (106, 185, 121)):
        if any(c % 8 for c in cor_de_neve(cor)):
            erros.append("cor fora do passo do GBA: %s -> %s" % (cor, cor_de_neve(cor)))

    print("%d origens, %d destinos, %d checagens" % (len(de_para), len(set(de_para.values())), 5))
    for e in erros:
        print("FALHA:", e)
    print("DEMO OK" if not erros else "DEMO COM FALHA")
    return 0 if not erros else 1


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--demo", action="store_true")
    args = p.parse_args()
    if args.demo:
        return demo()
    relato = gera()
    for k in ("metatiles_de_neve", "blocos_trocados", "tiles_com_faixa", "tiles_novos_no_secundario"):
        print("%s: %s" % (k, relato[k]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
