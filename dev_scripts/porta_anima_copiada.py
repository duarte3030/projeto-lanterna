#!/usr/bin/env python3
"""Gera a arte da animação de porta das cidades copiadas de Sinnoh (frente C).

Por que este script existe
--------------------------
As cidades copiadas do Retro Platinum ganharam PARES DE TILESETS PRÓPRIOS
(`gTileset_FloaromaRetroPrim/Sec`, `gTileset_TwinleafRetroPrim/Sec`). Os
metatiles de porta do autor foram promovidos a `MB_ANIMATED_DOOR` e os warps
funcionam, mas `sDoorAnimGraphicsTable` (`src/field_door.c`) não tinha entrada
para os pares novos, então `StartDoorOpenAnimation` devolvia -1 e a porta NÃO
animava. O Retro Platinum não tem arte de porta abrindo (as portas dele são
`MB_NON_ANIMATED_DOOR`), então a arte da animação tem de ser DERIVADA da porta
fechada, mecanicamente, sem inventar desenho novo.

O que o motor exige (lido em `src/field_door.c` e `src/field_camera.c`, não
presumido)
----------------------------------------------------------------------------
- `BuildDoorTiles` só escreve os tiles novos nos 4 PRIMEIROS tiles de cada
  metatile (a camada de BAIXO); os 4 de cima viram tile 0. `DrawDoorMetatileAt`
  desenha com `METATILE_LAYER_TYPE_COVERED`, ou seja BG3 recebe a camada de
  baixo, BG2 recebe a de cima (tile 0, transparente) e BG1 recebe 0. Logo, cada
  quadrante de 8x8 do quadro tem de ser a arte COMPOSTA das duas camadas,
  achatada, e desenhada com UMA paleta só.
- `CopyDoorTilesToVram` copia 8 tiles para `NUM_TILES_TOTAL - 8` = 1016 quando
  `size` não é 2. Nenhum metatile dos dois pares referencia tile >= 1016
  (medido: maior índice 596 em Floaroma, 303 em Twinleaf), então a faixa está
  livre.
- `sDoorOpenAnimFrames` usa os offsets -1, 0, 0x100 e 0x200: um quadro fechado
  (que o motor redesenha do próprio tileset) mais TRÊS quadros de 8 tiles. Por
  isso o PNG é 16x96, com os tiles em ordem (col0,lin0),(col1,lin0),(col0,lin1)...
  e os 8 tiles de um quadro nas 4 primeiras linhas de 8px: tiles 0-3 são o
  metatile DE CIMA e tiles 4-7 o metatile DE BAIXO.

A porta de UMA CÉLULA (`size` 0) e por que ela foi necessária
-------------------------------------------------------------
`sDoorAnimGraphicsTable` casa só metatile + tileset, e o mesmo metatile de porta
aparece no mapa debaixo de PAREDES DIFERENTES:

    FloaromaTown  143  (26,23) tem o metatile 163 em cima (parede azul da Loja)
                       (18,32) tem o metatile 135 em cima (parede laranja do
                       Centro Pokémon). Os dois diferem em 249 dos 256 pixels.
    TwinleafTown   78  (5,13) e (16,23) têm o 71 em cima (parede com janela)
                       (16,13) e (6,23)  têm o 113 em cima (parede com telhado
                       verde). Os dois diferem em 229 dos 256 pixels.

Com `size` 1 o motor REDESENHA a célula de cima, e uma entrada só não pode
servir às duas paredes: três das sete células de porta piscariam a parede errada
durante a animação. Medido também que a folha da porta cabe INTEIRA no metatile
de baixo nas três portas (a célula de cima é parede e telhado, não porta). Por
isso `src/field_door.c` ganhou `size` 0, "porta de uma célula": o motor anima só
o metatile de baixo e a célula de cima fica como está, pixel a pixel certa em
todas as células. Os tiles 0-3 de cada quadro (o metatile de cima) saem
TRANSPARENTES de propósito, porque nunca são lidos.

Uso
---
    python3 dev_scripts/porta_anima_copiada.py            # gera a arte e imprime a tabela
    python3 dev_scripts/porta_anima_copiada.py --prova    # + PNG de conferência
    python3 dev_scripts/porta_anima_copiada.py --rebaixa  # rebaixa as não-portas
    python3 dev_scripts/porta_anima_copiada.py --porta floaroma_retro_vidro

O script é RE-RODÁVEL: ele lê o par de tilesets do disco toda vez, então depois
de o par ser regerado por `copia_cidade_fonte.py --par-proprio` basta rodá-lo de
novo para a arte e os índices de paleta voltarem a bater.
"""

import argparse
import os
import struct
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from copia_cidade_fonte import (  # noqa: E402
    Tileset,
    desenha_metatile,
    le_blocos,
    le_layouts,
    pasta_do_simbolo,
)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NUM_PALS_IN_PRIMARY = 6
NUM_PALS_TOTAL = 13
NUM_METATILES_IN_PRIMARY = 512
MB_ANIMATED_DOOR = 0x69
MB_NON_ANIMATED_DOOR = 0x60
MASCARA_COMPORTAMENTO = 0x00FF


# ------------------------------------------------------------- o registro -----
# Uma entrada por metatile de porta DE VERDADE. `acima` é o metatile da célula
# de cima usado só para a prova de conferência (com `size` 0 o motor não o
# redesenha). `estilo` é a regra mecânica de abertura.

PORTAS = [
    dict(
        nome="floaroma_retro_vidro",
        cidade="FloaromaTown",
        simbolo="FloaromaRetro",
        rotulo="FloaromaRetroVidro",
        metatile=143,
        acima=163,
        estilo="lados",
        chao=1,
        som="DOOR_SOUND_SLIDING",
        comentario="porta de vidro do Centro Pokémon e da Loja (portas de correr)",
    ),
    dict(
        nome="floaroma_retro_madeira",
        cidade="FloaromaTown",
        simbolo="FloaromaRetro",
        rotulo="FloaromaRetroMadeira",
        metatile=196,
        acima=190,
        estilo="cortina",
        chao=1,
        som="DOOR_SOUND_NORMAL",
        comentario="porta de madeira das duas casas",
    ),
    dict(
        nome="twinleaf_retro_madeira",
        cidade="TwinleafTown",
        simbolo="TwinleafRetro",
        rotulo="TwinleafRetroMadeira",
        # O NÚMERO MUDOU em 11/09/2026, e o tileset também: Twinleaf voltou para a
        # regra 3.2 (cidade no SECUNDÁRIO, primário da região compartilhado), então
        # a porta saiu do metatile 78 do primário próprio, que deixou de existir,
        # para o 576 (local 64) do `gTileset_TwinleafRetroSec`. `GetDoorGraphics`
        # compara o tileset com o primário OU o secundário do layout, então a
        # entrada com o secundário casa do mesmo jeito.
        metatile=576,
        acima=569,
        estilo="cortina",
        chao=2,
        som="DOOR_SOUND_NORMAL",
        comentario="porta de madeira das quatro casas",
    ),
]

# Metatiles que receberam MB_ANIMATED_DOOR na conversão mas NÃO são porta: eles
# não têm folha nenhuma e nunca vão animar. `MB_NON_ANIMATED_DOOR` continua
# sendo comportamento de warp (`IsWarpMetatileBehavior`, src/field_control_avatar.c),
# então o warp continua disparando quando o jogador PISA na célula (todas têm
# colisão 0, medido).
NAO_SAO_PORTA = [
    dict(simbolo="FloaromaRetro", metatile=52,
         o_que="centro do toldo listrado da floricultura"),
    dict(simbolo="FloaromaRetro", metatile=123,
         o_que="vão entre as árvores para o Floaroma Meadow (metade esquerda)"),
    dict(simbolo="FloaromaRetro", metatile=124,
         o_que="vão entre as árvores para o Floaroma Meadow (metade direita)"),
]

# Fração da folha coberta pelo vão em cada quadro. O último quadro cobre a folha
# INTEIRA; `chao` (as linhas de baixo que são chão e não porta, medidas por porta
# e conferidas a cada rodada pelo relatório) nunca escurece.
FRACOES_CORTINA = (0.40, 0.72, 1.0)
# Deslocamento de cada folha de porta de correr, em frações da meia largura.
FRACOES_LADOS = (0.375, 0.75, 1.0)


# ---------------------------------------------------------------- leitura -----

def simbolos_da_cidade(cidade):
    """(primário, secundário) do layout da cidade, lidos de layouts.json.

    Trocado em 11/09/2026: o script chutava `gTileset_<simbolo>Prim` e
    `<simbolo>Sec`, e isso quebrou no dia em que Twinleaf voltou para a regra 3.2
    e passou a usar o `gTileset_GeneralSinnoh` compartilhado como primário (o
    `twinleaf_retro_prim` deixou de existir). Ler o layout serve aos dois
    arranjos, o de par próprio e o de só secundário.
    """
    dados = le_layouts(os.path.join(RAIZ, "data/layouts/layouts.json"))
    for l in dados["layouts"]:
        if l["name"] == f"{cidade}_Layout":
            return (l["primary_tileset"].replace("gTileset_", ""),
                    l["secondary_tileset"].replace("gTileset_", ""))
    raise SystemExit(f"layout de {cidade} não achado em layouts.json")


def simbolo_do_metatile(cidade, metatile):
    """De qual tileset do par este número de metatile vem."""
    sp, ss = simbolos_da_cidade(cidade)
    return sp if metatile < NUM_METATILES_IN_PRIMARY else ss


def carrega_par(cidade):
    """Devolve (primário, secundário, paletas) do par de tilesets da cidade."""
    sp, ss = simbolos_da_cidade(cidade)
    prim = Tileset(pasta_do_simbolo(RAIZ, f"gTileset_{sp}", False), 8, sp)
    sec = Tileset(pasta_do_simbolo(RAIZ, f"gTileset_{ss}", True), 8, ss)
    # A paleta segue o ÍNDICE DE PALETA, não o slot de tile: 0..5 vêm do
    # primário e 6..12 do secundário (`resolve` em copia_cidade_fonte.py).
    paletas = [prim.paletas[i] if i < NUM_PALS_IN_PRIMARY else sec.paletas[i]
               for i in range(NUM_PALS_TOTAL)]
    return prim, sec, paletas


def quadrantes(pixels256):
    """Corta um metatile de 16x16 nos 4 quadrantes de 8x8, na ordem do motor."""
    saida = []
    for q in range(4):
        ox, oy = (q % 2) * 8, (q // 2) * 8
        saida.append([pixels256[(oy + y) * 16 + ox + x]
                      for y in range(8) for x in range(8)])
    return saida


# ---------------------------------------------------------------- paleta ------

def erro_cor(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b))


def melhor_indice(cor, paleta):
    """Índice de 1 a 15 mais próximo de `cor`. O 0 é sempre transparente."""
    return min(range(1, 16), key=lambda i: erro_cor(cor, paleta[i]))


def custo_da_paleta(contagem, paleta):
    """Erro quadrático total de pintar essas cores com essa paleta."""
    total = 0
    trocas = []
    for cor, n in contagem.items():
        i = melhor_indice(cor, paleta)
        e = erro_cor(cor, paleta[i])
        total += e * n
        if e:
            trocas.append((cor, paleta[i], e, n))
    return total, trocas


def escolhe_paleta(pix64, paletas, preferidas=()):
    """Escolhe a paleta do PAR que melhor pinta este quadrante.

    Primeiro procura paleta que contenha TODAS as cores (erro 0); entre elas
    prefere as que o metatile já usava, para não trocar a paleta sem motivo.
    Se nenhuma contiver todas, devolve a de menor erro quadrático e as trocas,
    para o relatório: quantização nunca acontece calada.
    """
    contagem = {}
    for c in pix64:
        if c is not None:
            contagem[c] = contagem.get(c, 0) + 1
    exatas = [i for i in range(NUM_PALS_TOTAL)
              if set(contagem) <= set(paletas[i][1:])]
    if exatas:
        for p in preferidas:
            if p in exatas:
                return p, 0, []
        return exatas[0], 0, []
    custos = [(custo_da_paleta(contagem, paletas[i])[0], i)
              for i in range(NUM_PALS_TOTAL)]
    custos.sort()
    melhor = custos[0][1]
    total, trocas = custo_da_paleta(contagem, paletas[melhor])
    return melhor, total, trocas


def codifica(pix64, paleta):
    """64 índices de 4 bits. `None` (transparente) vira 0."""
    return [0 if c is None else melhor_indice(c, paleta) for c in pix64]


def lum(cor):
    r, g, b = cor
    return 299 * r + 587 * g + 114 * b


def indice_mais_escuro(paleta):
    """Índice de 1 a 15 da cor mais escura da paleta (luminância)."""
    return min(range(1, 16), key=lambda i: lum(paleta[i]))


def cor_do_vao(paletas_dos_quadrantes):
    """A cor do vão escuro, a MESMA nos quatro quadrantes quando for possível.

    Quadrante que escurece com uma cor sua e o vizinho com outra deixa costura
    visível no quadro aberto. Se as paletas escolhidas tiverem cor em comum,
    usa-se a mais escura delas; se não tiverem, cada quadrante usa a sua e o
    relatório diz que ficou costurado.
    """
    comuns = set(paletas_dos_quadrantes[0][1:])
    for p in paletas_dos_quadrantes[1:]:
        comuns &= set(p[1:])
    if comuns:
        return min(comuns, key=lum), True
    return None, False


# -------------------------------------------------------------- os quadros ----

def quadro_cortina(base256, k, chao):
    """O vão escurece de cima para baixo, k de 1 a 3.

    Regra mecânica de propósito: nada de arte inventada. As linhas 0..h-1 da
    FOLHA viram a cor mais escura disponível; o resto fica igual à porta
    fechada, e as `chao` linhas de baixo (chão e soleira, que não são porta)
    nunca escurecem, como o quadro aberto da porta de fábrica também não
    escurece o chão do vão (graphics/door_anims/general.png).
    """
    folha = 16 - chao
    h = int(round(FRACOES_CORTINA[k - 1] * folha))
    saida = list(base256)
    for y in range(h):
        for x in range(16):
            saida[y * 16 + x] = "escuro"
    return saida


def quadro_lados(base256, k, chao):
    """As duas folhas deslizam para os lados e o meio escurece, k de 1 a 3.

    É a porta de correr do Centro Pokémon e da Loja: a folha esquerda sai pela
    esquerda, a direita pela direita, e o vão cresce do centro. As `chao` linhas
    de baixo não deslizam nem escurecem.
    """
    d = int(round(FRACOES_LADOS[k - 1] * 8))
    saida = list(base256)
    for y in range(16 - chao):
        for x in range(16):
            if x < 8:
                origem = x + d           # folha esquerda desliza para a esquerda
                dentro = origem <= 7
            else:
                origem = x - d           # folha direita desliza para a direita
                dentro = origem >= 8
            saida[y * 16 + x] = base256[y * 16 + origem] if dentro else "escuro"
    return saida


def monta_quadros(base256, estilo, chao):
    if estilo == "cortina":
        return [quadro_cortina(base256, k, chao) for k in (1, 2, 3)]
    if estilo == "lados":
        return [quadro_lados(base256, k, chao) for k in (1, 2, 3)]
    raise ValueError(f"estilo desconhecido: {estilo}")


# ---------------------------------------------------------------- emissão -----

def escreve_png_indexado(caminho, tiles24, paleta_de_amostra):
    """Grava o PNG 16x96 INDEXADO. O gbagfx lê os ÍNDICES, não o RGB."""
    im = Image.new("P", (16, 96), 0)
    achatada = []
    for cor in paleta_de_amostra:
        achatada.extend(cor)
    achatada.extend([0] * (768 - len(achatada)))
    im.putpalette(achatada)
    px = im.load()
    for i, tile in enumerate(tiles24):
        tx, ty = (i % 2) * 8, (i // 2) * 8
        for y in range(8):
            for x in range(8):
                px[tx + x, ty + y] = tile[y * 8 + x]
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    im.save(caminho)


def processa(porta, escreve=True):
    """Compõe a arte, escolhe as paletas e devolve tudo o que o relatório usa."""
    prim, sec, paletas = carrega_par(porta["cidade"])
    baixo = desenha_metatile(prim, sec, porta["metatile"], 8, fundo=None)
    cima = desenha_metatile(prim, sec, porta["acima"], 8, fundo=None)

    # O metatile pode estar no primário OU no secundário do par: em Twinleaf,
    # depois da regra 3.2, a porta é o 576, que é o local 64 do secundário.
    if porta["metatile"] < NUM_METATILES_IN_PRIMARY:
        metatile = prim.metatiles[porta["metatile"]]
    else:
        metatile = sec.metatiles[porta["metatile"] - NUM_METATILES_IN_PRIMARY]
    usadas = [(w >> 12) & 0xF for w in metatile]

    # Só os 4 quadrantes do metatile DE BAIXO entram na animação (`size` 0).
    escolhas = []
    for q, pix in enumerate(quadrantes(baixo)):
        preferidas = [usadas[q], usadas[q + 4]]
        p, erro, trocas = escolhe_paleta(pix, paletas, preferidas)
        escolhas.append(dict(quadrante=q, paleta=p, erro=erro, trocas=trocas))

    quadros = monta_quadros(baixo, porta["estilo"], porta["chao"])

    escolhidas = [paletas[e["paleta"]] for e in escolhas]
    vao, unica = cor_do_vao(escolhidas)

    tiles24 = []
    for quadro in quadros:
        # tiles 0-3: metatile de CIMA, nunca lidos com `size` 0 (transparentes).
        tiles24.extend([bytes(64)] * 4)
        for q, pix in enumerate(quadrantes(quadro)):
            paleta = escolhidas[q]
            escuro = (paleta.index(vao) if unica else indice_mais_escuro(paleta))
            idx = [escuro if c == "escuro"
                   else (0 if c is None else melhor_indice(c, paleta))
                   for c in pix]
            tiles24.append(bytes(idx))

    caminho = os.path.join(RAIZ, "graphics", "door_anims", porta["nome"] + ".png")
    if escreve:
        escreve_png_indexado(caminho, tiles24, paletas[escolhas[0]["paleta"]])

    # As linhas de baixo que o script preservou, para a rodada seguinte conferir
    # que o par regerado continua com chão onde o registro diz que tem.
    linhas_de_chao = []
    for y in range(16 - porta["chao"], 16):
        linhas_de_chao.append((y, sorted({baixo[y * 16 + x] for x in range(16)})))

    return dict(porta=porta, prim=prim, sec=sec, paletas=paletas,
                baixo=baixo, cima=cima, escolhas=escolhas, quadros=quadros,
                tiles=tiles24, caminho=caminho, vao=vao, vao_unica=unica,
                linhas_de_chao=linhas_de_chao)


# ------------------------------------------------------------------ prova -----

def desenha_prova(resultados, caminho, escala=8):
    """Renderiza fechado + 3 quadros DECODIFICANDO o que acabou de ser gravado.

    É a prova de que a arte que vai para a ROM é a que o script acha que é: os
    quadros saem dos bytes do PNG, pintados com as paletas escolhidas, e não da
    composição em memória.
    """
    linhas = len(resultados)
    larg = (4 * 16 + 3 * 2) * escala
    alt = linhas * (32 + 2) * escala
    im = Image.new("RGB", (larg, alt), (24, 24, 24))
    px = im.load()

    def poe(col, lin, y0, pixels, altura):
        for y in range(altura):
            for x in range(16):
                c = pixels[y * 16 + x]
                if c is None:
                    c = (255, 0, 255)
                for dy in range(escala):
                    for dx in range(escala):
                        px[(col * 18 + x) * escala + dx,
                           (lin * 34 + y0 + y) * escala + dy] = c

    for lin, r in enumerate(resultados):
        poe(0, lin, 0, r["cima"], 16)
        poe(0, lin, 16, r["baixo"], 16)
        tiles = le_tiles_do_png(r["caminho"])
        for k in range(3):
            # A célula de cima não é redesenhada pelo motor com `size` 0: a
            # prova mostra o metatile de verdade, que é o que o jogador vê.
            poe(k + 1, lin, 0, r["cima"], 16)
            bloco = [None] * 256
            for q in range(4):
                paleta = r["paletas"][r["escolhas"][q]["paleta"]]
                tile = tiles[k * 8 + 4 + q]
                ox, oy = (q % 2) * 8, (q // 2) * 8
                for y in range(8):
                    for x in range(8):
                        v = tile[y * 8 + x]
                        bloco[(oy + y) * 16 + ox + x] = None if v == 0 else paleta[v]
            poe(k + 1, lin, 16, bloco, 16)

    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    im.save(caminho)
    return caminho


def le_tiles_do_png(caminho):
    im = Image.open(caminho)
    if im.mode != "P":
        raise ValueError(f"{caminho}: esperado PNG indexado")
    dados = im.load()
    larg, alt = im.size
    tiles = []
    for i in range((larg // 8) * (alt // 8)):
        tx, ty = (i % (larg // 8)) * 8, (i // (larg // 8)) * 8
        tiles.append(bytes(dados[tx + x, ty + y] & 0x0F
                           for y in range(8) for x in range(8)))
    return tiles


# --------------------------------------------------------------- rebaixar -----

def rebaixa(aplicar):
    """Troca MB_ANIMATED_DOOR por MB_NON_ANIMATED_DOOR nas não-portas."""
    por_simbolo = {}
    for item in NAO_SAO_PORTA:
        por_simbolo.setdefault(item["simbolo"], []).append(item)
    linhas = []
    for simbolo, itens in sorted(por_simbolo.items()):
        sp, ss = simbolos_da_cidade(itens[0]["cidade"])
        alto = itens[0]["metatile"] >= NUM_METATILES_IN_PRIMARY
        pasta = pasta_do_simbolo(RAIZ, f"gTileset_{ss if alto else sp}",
                                 bool(alto))
        caminho = os.path.join(pasta, "metatile_attributes.bin")
        bruto = bytearray(open(caminho, "rb").read())
        attrs = list(struct.unpack(f"<{len(bruto)//2}H", bruto))
        mudou = 0
        for item in itens:
            m = item["metatile"]
            antes = attrs[m]
            beh = antes & MASCARA_COMPORTAMENTO
            if beh == MB_NON_ANIMATED_DOOR:
                linhas.append(f"  {simbolo} metatile {m}: já estava em "
                              f"MB_NON_ANIMATED_DOOR ({item['o_que']})")
                continue
            if beh != MB_ANIMATED_DOOR:
                linhas.append(f"  {simbolo} metatile {m}: comportamento 0x{beh:02x} "
                              f"não é MB_ANIMATED_DOOR, NÃO mexido ({item['o_que']})")
                continue
            attrs[m] = (antes & ~MASCARA_COMPORTAMENTO) | MB_NON_ANIMATED_DOOR
            mudou += 1
            linhas.append(f"  {simbolo} metatile {m}: 0x{antes:04x} -> "
                          f"0x{attrs[m]:04x} ({item['o_que']})")
        if aplicar and mudou:
            with open(caminho, "wb") as f:
                for a in attrs:
                    f.write(struct.pack("<H", a))
    return linhas


# ----------------------------------------------------------------- censo ------

def censo_das_celulas(porta):
    """Quais células do mapa usam esse metatile de porta, e o que há em cima."""
    import json
    layouts = json.load(open(os.path.join(RAIZ, "data", "layouts", "layouts.json"),
                             encoding="utf-8"))
    alvo = None
    for l in layouts["layouts"]:
        if l["name"] == porta["cidade"] + "_Layout":
            alvo = l
            break
    if alvo is None:
        return []
    blocos = le_blocos(os.path.join(RAIZ, alvo["blockdata_filepath"]))
    w = alvo["width"]
    saida = []
    for i, v in enumerate(blocos):
        if (v & 0x3FF) == porta["metatile"]:
            x, y = i % w, i // w
            saida.append((x, y, blocos[(y - 1) * w + x] & 0x3FF))
    return saida


# ------------------------------------------------------------------ main ------

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--porta", action="append",
                    help="só esta porta (repetível); padrão é todas")
    ap.add_argument("--seco", action="store_true",
                    help="não grava PNG nenhum, só mede e imprime")
    ap.add_argument("--prova", action="store_true",
                    help="grava o PNG de conferência dos 4 estados")
    ap.add_argument("--saida-prova",
                    default=os.path.join(RAIZ, "amostras-tileset", "copia-cidades",
                                         "feito", "portas-retro-prova.png"),
                    help="caminho do PNG de conferência")
    ap.add_argument("--rebaixa", action="store_true",
                    help="aplica o rebaixamento das não-portas no "
                         "metatile_attributes.bin")
    ap.add_argument("--rebaixa-seco", action="store_true",
                    help="mostra o rebaixamento sem gravar")
    args = ap.parse_args()

    escolhidas = PORTAS
    if args.porta:
        escolhidas = [p for p in PORTAS if p["nome"] in args.porta]
        if not escolhidas:
            ap.error("nenhuma porta com esse nome: " + ", ".join(
                p["nome"] for p in PORTAS))

    resultados = []
    print("=" * 78)
    print("ARTE DA ANIMAÇÃO DE PORTA DAS CIDADES COPIADAS (frente C)")
    print("=" * 78)
    for porta in escolhidas:
        r = processa(porta, escreve=not args.seco)
        resultados.append(r)
        print()
        print(f"[{porta['nome']}] {porta['cidade']}, metatile {porta['metatile']}, "
              f"estilo {porta['estilo']}, som {porta['som']}")
        print(f"  {porta['comentario']}")
        celulas = censo_das_celulas(porta)
        acima = sorted({c[2] for c in celulas})
        print(f"  células no mapa: {[(x, y) for x, y, _ in celulas]}")
        print(f"  metatiles ACIMA delas: {acima}"
              + ("   <- diferem, e é por isso que a entrada usa size 0"
                 if len(acima) > 1 else ""))
        print(f"  arte: {os.path.relpath(r['caminho'], RAIZ)}"
              + ("  (NÃO gravada, modo --seco)" if args.seco else ""))
        pior = 0
        for e in r["escolhas"]:
            marca = "" if e["erro"] == 0 else f"  QUANTIZADO erro {e['erro']}"
            print(f"    quadrante {e['quadrante']} -> paleta {e['paleta']}{marca}")
            for cor, alvo, err, n in e["trocas"]:
                print(f"        {cor} -> {alvo}  erro {err} em {n} pixels")
            pior = max(pior, e["erro"])
        print(f"  pior erro de quadrante: {pior}")
        if r["vao_unica"]:
            print(f"  cor do vão (a mesma nos 4 quadrantes): {r['vao']}")
        else:
            print("  cor do vão: SEM cor comum às 4 paletas, cada quadrante usa "
                  "a sua mais escura (costura visível no quadro aberto)")
        print(f"  linhas de chão preservadas (chao={porta['chao']}): "
              + "; ".join(f"linha {y} {cores}" for y, cores in r["linhas_de_chao"]))

    print()
    print("-" * 78)
    print("PARA COLAR EM src/field_door.c")
    print("-" * 78)
    print("ATENÇÃO ao lugar da tabela: o bloco de `sDoorAnimGraphicsTable` é")
    print("`#if !IS_FRLG` ... `#else` ... `#endif // !IS_FRLG`. As entradas vão no")
    print("FIM DO PRIMEIRO ramo, logo ANTES do `#else`, e não antes do `#endif`:")
    print("antes do `#endif` é o ramo do FRLG, que não compila nesta build e some")
    print("calado (medido em 11/09/2026: a ROM não crescia um byte e os testes de")
    print("warp continuavam verdes porque o warp nunca dependeu da animação).")
    print()
    for r in resultados:
        p = r["porta"]
        print(f'static const u8 sDoorAnimTiles_{p["rotulo"]}[] = '
              f'INCGFX_U8("graphics/door_anims/{p["nome"]}.png", ".4bpp");')
    print()
    for r in resultados:
        p = r["porta"]
        # Com `size` 0 o motor chama BuildDoorTiles uma vez só, com
        # &paletteNums[0]: os 4 primeiros índices são os 4 quadrantes da CÉLULA
        # da porta e os 4 últimos são os bits de paleta do tile 0 (transparente,
        # então o valor não aparece na tela). São 8 como em toda a tabela, e
        # nenhuma leitura passa do fim do vetor.
        baixo = [e["paleta"] for e in r["escolhas"]]
        vals = ", ".join(str(v) for v in (baixo + baixo))
        print(f'static const u8 sDoorAnimPalettes_{p["rotulo"]}[] = {{{vals}}};')
    print()
    for r in resultados:
        p = r["porta"]
        print(f'    {{{p["metatile"]},{" " * max(1, 52 - len(str(p["metatile"])))}'
              f'&gTileset_{simbolo_do_metatile(p["cidade"], p["metatile"])}, '
              f'{p["som"]}, DOOR_SIZE_ONE_CELL, '
              f'sDoorAnimTiles_{p["rotulo"]}, sDoorAnimPalettes_{p["rotulo"]}}},')

    if args.prova and not args.seco:
        caminho = desenha_prova(resultados, args.saida_prova)
        print()
        print(f"prova gravada em {os.path.relpath(caminho, RAIZ)}")

    if args.rebaixa or args.rebaixa_seco:
        print()
        print("-" * 78)
        print("REBAIXAMENTO DAS NÃO-PORTAS"
              + ("" if args.rebaixa else "  (SECO, nada gravado)"))
        print("-" * 78)
        for linha in rebaixa(args.rebaixa):
            print(linha)

    return 0


if __name__ == "__main__":
    sys.exit(main())
