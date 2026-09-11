#!/usr/bin/env python3
"""Copia uma cidade inteira de um decomp de terceiro (hoje: Retro Platinum) para cá.

Uso:
    python3 dev_scripts/copia_cidade_fonte.py --cidade JubilifeCity --demo
    python3 dev_scripts/copia_cidade_fonte.py --cidade JubilifeCity --aplicar

POR QUE ISSO EXISTE
-------------------
A seção 0.ae do ESTADO fechou o assunto "gerador de arte": peça espalhada por
algoritmo para bater um número de carimbo está proibida. O refino volta como
CÓPIA de cidade desenhada por gente. O contrato é
`Pokemon Claude/METODO-COPIA-CIDADES.md`, e esta ferramenta é o braço mecânico
dele para a frente de Sinnoh: ela traz a ARTE inteira do hack e não traz NADA do
jogo dele (warp, NPC, script, gatilho e conexão continuam sendo nossos).

O QUE FOI MEDIDO ANTES DE ESCREVER ISTO (10/09/2026, não presumir de novo)
-------------------------------------------------------------------------
1. **Metatile de três camadas.** O `metatiles.bin` do Retro Platinum tem 24
   bytes por metatile (12 u16): [baixo 0..3][meio 4..7][topo 8..11]. O nosso tem
   16 bytes (8 u16), duas camadas. LIGAR três camadas aqui custaria
   `NUM_TILES_PER_METATILE` 8 -> 12, o que reescreve o formato dos **221
   metatiles.bin** do repositório (905.776 B viram 1.358.664 B, +452.888 B de
   ROM) e colide de frente com as outras três frentes de cópia, que mexem em
   tileset ao mesmo tempo. O briefing autoriza ligar a opção só se ela NÃO mudar
   o formato dos tilesets existentes; ela muda. Então o caminho é **achatar para
   duas camadas**, célula a célula, com prova de pixel.

2. **Quanto custa achatar, medido nos seis mapas de cidade da fonte:** a maioria
   dos metatiles usa só uma ou duas camadas e passa direto. As células em que as
   TRÊS camadas têm tile são poucas: 30 em Twinleaf, 73 em Sandgem, 140 em
   Jubilife, 60 em Oreburgh norte, 72 em Oreburgh sul, 180 em Floaroma. Só essas
   viram tile novo (a composição do fundo com o meio), e o topo continua sendo o
   topo.

3. **Fronteira primário/secundário é o slot de VRAM 512, não `len(tiles)`.** O
   `tiles.png` de `outdoor_jubilife` traz 240 tiles dentro dos 512 slots do
   primário. Usar `len(tiles)` como fronteira pinta o prédio inteiro de magenta.

4. **O atributo de metatile é IGUAL nos dois lados** (2 bytes,
   `behavior = attr & 0x00FF`, `layerType = (attr & 0xF000) >> 12`), e o enum
   `MB_*` é numericamente idêntico em tudo que a fonte usa: o que difere são os
   slots 0x23, 0x2C-0x2D, 0x54-0x5F, 0xA1-0xAF e 0xC8-0xCC, onde nós pusemos
   comportamento de FireRed e eles deixaram `MB_UNUSED_*`. A ferramenta COPIA o
   comportamento e ACUSA qualquer valor que caia nesses slots.

5. **Paletas.** São 13 no total, 6 do primário e 7 do secundário. A cidade
   copiada passa a usar o NOSSO primário (`gTileset_GeneralSinnoh`), por causa
   da costura: o motor desenha o mapa vizinho com os tilesets do mapa atual, e
   se a rota vizinha não compartilhar o primário ela vira lixo na tela. Logo as
   paletas 0-5 da fonte MORREM aqui (o terreno natural passa a ser o nosso, pelo
   de-para) e as 6-12 da fonte entram inteiras nas 6-12 daqui, 1 para 1. Medido
   por cidade, os tiles que a fonte pinta com paleta 6-12 são 216 (Twinleaf),
   417 (Sandgem), 337 (Jubilife), 347 (Oreburgh norte), 277 (Oreburgh sul) e 270
   (Floaroma): todos abaixo dos 512 slots de um secundário, com folga para os
   tiles compostos do achatamento.

6. **Secundário novo por cidade, sempre.** Os secundários que as cinco cidades
   usam hoje são compartilhados: `gTileset_PetalburgSinnoh` por 62 layouts,
   `gTileset_Jubilife` por 7, `gTileset_MauvilleSinnoh` por 4 e
   `gTileset_RustboroSinnoh` por 3. Reaproveitar qualquer um deles mudaria a
   arte das rotas irmãs, que é exatamente o que a seção 5 do contrato proíbe.

BOA NOTÍCIA É SUSPEITA
----------------------
`--demo` não aplica nada: ele mede, imprime os números e roda as provas
NEGATIVAS (o teste que tem de FALHAR se a ferramenta estiver mentindo). Render
limpo demais aqui é quase sempre fronteira de VRAM errada, não arte boa.
"""
import argparse
import json
import os
import re
import struct
import sys

try:
    from PIL import Image, ImageDraw
except ImportError:  # pragma: no cover
    print("ERRO: este script precisa do Pillow (PIL).", file=sys.stderr)
    raise

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABELA_ANEL_PADRAO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "anel_sinnoh_retro.json")
FONTE_PADRAO = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/romhacks/retro-platinum/fonte"

NUM_TILES_IN_PRIMARY = 512
NUM_METATILES_IN_PRIMARY = 512
NUM_PALS_IN_PRIMARY = 6
NUM_PALS_TOTAL = 13
TILES_POR_METATILE_FONTE = 12   # três camadas
TILES_POR_METATILE_NOSSO = 8    # duas camadas
# Janela que o motor desenha do mapa conectado. É por isso que o anel de 8 tiles
# da borda tem de continuar sendo a NOSSA arte (contrato, seção 3) e é por isso
# que a fidelidade da cópia se mede só no interior.
ANEL_COSTURA = 8

# Acima desta distância de desenho (soma do quadrado da diferença de cor nos 256
# pixels do metatile), o melhor candidato do vocabulário da rota é considerado
# LONGE e a busca pode olhar os 512 do primário, sempre dentro da mesma família
# de chão. O valor é o que separa, nas seis medidas de 11/09/2026, o "areia com
# areia" do "areia com gelo": 1.500.000 deixa a areia de praia de Floaroma e de
# Oreburgh achar a nossa areia e continua barrando a troca de assunto.
LIMITE_ANEL_LONGE = 1_500_000

# Camadas do nosso motor (include/global.fieldmap.h).
LAYER_NORMAL = 0   # meio + topo   (o fundo é lixo, o metatile cobre tudo)
LAYER_COVERED = 1  # fundo + meio  (nada cobre o jogador)
LAYER_SPLIT = 2    # fundo + topo  (o topo cobre o jogador)

# Slots do enum MB_* em que o nosso repositório e o do Retro Platinum divergem.
# Comportamento da fonte que caia aqui não pode ser copiado sem alguém olhar.
MB_DIVERGENTES = (
    set([0x23, 0x2C, 0x2D])
    | set(range(0x54, 0x60))
    | set(range(0xA1, 0xB0))
    | set(range(0xC8, 0xCD))
)

MAGENTA = (255, 0, 255)


# ---------------------------------------------------------------- leitura -----

def le_jasc_pal(caminho):
    """Devolve 16 tuplas RGB. O formato é o mesmo nos dois repositórios."""
    with open(caminho, encoding="utf-8") as f:
        linhas = [l.strip() for l in f if l.strip()]
    if linhas[0] != "JASC-PAL":
        raise ValueError(f"{caminho}: não é JASC-PAL")
    n = int(linhas[2])
    cores = []
    for linha in linhas[3:3 + n]:
        r, g, b = (int(v) for v in linha.split()[:3])
        cores.append((r, g, b))
    while len(cores) < 16:
        cores.append((0, 0, 0))
    return cores[:16]


def le_tiles_png(caminho):
    """Devolve a lista de tiles 8x8, cada um com 64 índices de 0 a 15."""
    im = Image.open(caminho)
    if im.mode != "P":
        raise ValueError(f"{caminho}: esperado PNG indexado (modo P), veio {im.mode}")
    larg, alt = im.size
    if larg % 8 or alt % 8:
        raise ValueError(f"{caminho}: {larg}x{alt} não é múltiplo de 8")
    dados = im.load()
    por_linha = larg // 8
    tiles = []
    for i in range((larg // 8) * (alt // 8)):
        tx, ty = (i % por_linha) * 8, (i // por_linha) * 8
        tiles.append(bytes(dados[tx + x, ty + y] & 0x0F for y in range(8) for x in range(8)))
    return tiles


class Tileset:
    """Um tileset lido do disco, de qualquer um dos dois repositórios."""

    def __init__(self, pasta, tiles_por_metatile, rotulo):
        self.pasta = pasta
        self.rotulo = rotulo
        self.tpm = tiles_por_metatile
        self.tiles = le_tiles_png(os.path.join(pasta, "tiles.png"))
        self.paletas = []
        for i in range(16):
            p = os.path.join(pasta, "palettes", f"{i:02d}.pal")
            self.paletas.append(le_jasc_pal(p) if os.path.exists(p) else [(0, 0, 0)] * 16)
        bruto = open(os.path.join(pasta, "metatiles.bin"), "rb").read()
        passo = tiles_por_metatile * 2
        if len(bruto) % passo:
            raise ValueError(
                f"{pasta}/metatiles.bin: {len(bruto)} B não divide por {passo}. "
                "Camada errada? (fonte = 24 B, nosso = 16 B)")
        self.metatiles = [
            struct.unpack(f"<{tiles_por_metatile}H", bruto[i:i + passo])
            for i in range(0, len(bruto), passo)
        ]
        attr = open(os.path.join(pasta, "metatile_attributes.bin"), "rb").read()
        if len(attr) % 2:
            raise ValueError(f"{pasta}/metatile_attributes.bin: não é de 2 bytes")
        self.attrs = list(struct.unpack(f"<{len(attr)//2}H", attr))

    def __repr__(self):
        return (f"<{self.rotulo} {len(self.tiles)} tiles, {len(self.metatiles)} metatiles, "
                f"{len(self.attrs)} atributos>")


def le_layouts(caminho):
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def pasta_do_simbolo(raiz, simbolo, secundario):
    """gTileset_OutdoorJubilife -> data/tilesets/primary/outdoor_jubilife"""
    nome = re.sub(r"(?<!^)(?=[A-Z])", "_", simbolo.replace("gTileset_", "")).lower()
    tipo = "secondary" if secundario else "primary"
    return os.path.join(raiz, "data", "tilesets", tipo, nome)


def le_blocos(caminho):
    bruto = open(caminho, "rb").read()
    return [struct.unpack("<H", bruto[i:i + 2])[0] for i in range(0, len(bruto), 2)]


# --------------------------------------------------------------- pintura ------

def pinta_tile(tiles, paletas, entrada, transparente=None):
    """Devolve 64 pixels RGB ou `transparente` para o índice 0 da paleta.

    `entrada` é a palavra u16 do metatile: bits 0-9 índice, 10 flip X, 11 flip Y,
    12-15 paleta. `tiles` e `paletas` já vêm resolvidos pelo chamador, porque
    **o tileset do TILE e o tileset da PALETA não são a mesma escolha**: o tile
    vem do primário quando o índice é menor que 512, mas a paleta vem do
    primário quando o ÍNDICE DE PALETA é menor que 6. Um tile do primário
    pintado com a paleta 8 lê a paleta 8 do SECUNDÁRIO. Confundir as duas coisas
    foi o que encheu o primeiro render desta ferramenta de magenta e de preto
    (medido em 10/09/2026 contra o render de referência da fonte).
    """
    idx = entrada & 0x3FF
    flip_x = bool(entrada & 0x400)
    flip_y = bool(entrada & 0x800)
    pal = (entrada >> 12) & 0xF
    if idx >= len(tiles):
        return [MAGENTA] * 64
    tile = tiles[idx]
    cores = paletas[pal]
    saida = []
    for y in range(8):
        sy = 7 - y if flip_y else y
        for x in range(8):
            sx = 7 - x if flip_x else x
            c = tile[sy * 8 + sx]
            # O índice 0 é SEMPRE transparente no GBA. Pintá-lo com a cor 0 da
            # paleta (que nestes tilesets é o magenta de backdrop) cobre a
            # camada de baixo e apaga metade do mapa: foi assim que o primeiro
            # render desta ferramenta saiu com 1.944 células de 4.884 erradas.
            saida.append(transparente if c == 0 else cores[c])
    return saida


def resolve(entrada, prim, sec):
    """Devolve (tiles, paletas, entrada_local) para uma palavra de metatile.

    Separa as duas escolhas: o TILE pelo slot de VRAM (512), a PALETA pelo
    índice de paleta (6).
    """
    idx = entrada & 0x3FF
    pal = (entrada >> 12) & 0xF
    if idx < NUM_TILES_IN_PRIMARY:
        tiles, local = prim.tiles, idx
    else:
        tiles, local = sec.tiles, idx - NUM_TILES_IN_PRIMARY
    paletas = prim.paletas if pal < NUM_PALS_IN_PRIMARY else sec.paletas
    return tiles, paletas, (entrada & ~0x3FF) | local


def compoe(fundo, cima):
    """Empilha dois blocos de 64 pixels; `None` em `cima` deixa o fundo passar."""
    return [b if c is None else c for b, c in zip(fundo, cima)]


# ------------------------------------------------------------- achatamento ----

class Achatador:
    """Converte metatiles de três camadas em metatiles de duas.

    A regra, por metatile:

      * conta quantas das três camadas têm algum tile;
      * uma ou duas camadas -> passa direto, e o `layerType` diz quais das duas
        camadas do nosso motor recebem o desenho;
      * três camadas -> as células em que os TRÊS tiles existem viram um tile
        NOVO (fundo composto com meio), e o topo continua topo. As células em que
        uma das três está vazia não custam nada.

    O tile novo é pixel puro: nasce da composição de verdade dos dois tiles, e
    entra no pacote com a paleta que couber. Quando nenhuma paleta cobre as
    cores dos dois, o caso é registrado em `self.sem_paleta` em vez de sair
    quantizado calado.
    """

    def __init__(self, fonte_prim, fonte_sec, extras=(), rota=None):
        # PARTES: cada uma é um par (primário, secundário) da fonte. O caminho
        # normal tem uma só. A FUSÃO (Oreburgh, que o hack desenhou em dois
        # mapas) tem duas, e aí um `mid` do mapa fundido não diz sozinho de qual
        # par ele vem: quem diz é a `rota`, a tabela `mid novo -> (parte, mid
        # original)` que o `carrega_fusao` monta ao renumerar.
        #
        # Renumerar é o que faz a fusão caber. Juntar os dois pares num par só
        # NÃO cabe, e está medido: os dois secundários pedem 444 + 366 = 810
        # tiles para as 512 vagas de tile do secundário, e 7 + 7 paletas altas
        # para as 7 vagas. Os METATILES, sim, cabem: 128 + 81 do primário e
        # 172 + 139 do secundário são 520 distintos para os 1.024 números de 10
        # bits que uma célula de `map.bin` sabe escrever.
        self.partes = [(fonte_prim, fonte_sec)] + list(extras)
        self.rota = dict(rota or {})
        self.prim = fonte_prim
        self.sec = fonte_sec
        self.sem_paleta = []
        self.compostos = {}   # (parte, fundo, meio) -> pixels

    def resolve_mid(self, mid):
        """(primário, secundário, mid dentro daquele par, número da parte)."""
        parte, orig = self.rota.get(mid, (0, mid))
        prim, sec = self.partes[parte]
        return prim, sec, orig, parte

    def desenha(self, mid, fundo=(0, 0, 0)):
        prim, sec, m, _ = self.resolve_mid(mid)
        return desenha_metatile(prim, sec, m, TILES_POR_METATILE_FONTE, fundo)

    def atributo(self, mid):
        prim, sec, m, _ = self.resolve_mid(mid)
        return atributo_de(prim, sec, m)

    def metatile(self, mid):
        """(12 palavras, atributo, parte). Palavras None se o mid não existe."""
        prim, sec, m, parte = self.resolve_mid(mid)
        ts, local = (prim, m) if m < NUM_METATILES_IN_PRIMARY else \
                    (sec, m - NUM_METATILES_IN_PRIMARY)
        if local >= len(ts.metatiles):
            return None, 0, parte
        return ts.metatiles[local], (ts.attrs[local] if local < len(ts.attrs) else 0), parte

    def tiles_e_paletas(self, entrada, parte=0):
        return resolve(entrada, *self.partes[parte])

    def pixels(self, entrada, parte=0):
        if (entrada & 0x3FF) == 0:
            return [None] * 64
        tiles, paletas, local = resolve(entrada, *self.partes[parte])
        return pinta_tile(tiles, paletas, local, transparente=None)

    def camadas(self, metatile12):
        return [metatile12[0:4], metatile12[4:8], metatile12[8:12]]

    def achata(self, metatile12, parte=0):
        """Devolve (baixo[4], cima[4], layer_type, composicoes)."""
        camadas = self.camadas(metatile12)
        cheias = [i for i, c in enumerate(camadas) if any((t & 0x3FF) for t in c)]
        composicoes = []

        if len(cheias) <= 2:
            if not cheias:
                return [0, 0, 0, 0], [0, 0, 0, 0], LAYER_COVERED, composicoes
            if len(cheias) == 1:
                only = cheias[0]
                if only == 0:
                    return list(camadas[0]), [0] * 4, LAYER_COVERED, composicoes
                if only == 1:
                    return list(camadas[1]), [0] * 4, LAYER_COVERED, composicoes
                return [0] * 4, list(camadas[2]), LAYER_SPLIT, composicoes
            par = tuple(cheias)
            if par == (0, 1):
                return list(camadas[0]), list(camadas[1]), LAYER_COVERED, composicoes
            if par == (0, 2):
                return list(camadas[0]), list(camadas[2]), LAYER_SPLIT, composicoes
            # (1, 2): meio e topo, que é exatamente o nosso LAYER_NORMAL
            return list(camadas[1]), list(camadas[2]), LAYER_NORMAL, composicoes

        # Três camadas: funde fundo com meio, célula a célula.
        baixo = []
        for c in range(4):
            f, m = camadas[0][c], camadas[1][c]
            if (m & 0x3FF) == 0:
                baixo.append(f)
            elif (f & 0x3FF) == 0:
                baixo.append(m)
            else:
                chave = (parte, f, m)
                if chave not in self.compostos:
                    px = compoe(self.pixels(f, parte), self.pixels(m, parte))
                    self.compostos[chave] = px
                composicoes.append(chave)
                baixo.append(("COMPOSTO", chave))
        return baixo, list(camadas[2]), LAYER_SPLIT, composicoes


# ------------------------------------------------------------- empacotador ----

class PacoteSecundario:
    """Junta os tiles e as paletas que a cidade copiada precisa no secundário.

    O orçamento é duro e a ferramenta para quando estoura, em vez de cortar
    calada: 512 slots de tile (VRAM 512..1023) e 7 paletas (6..12).
    """

    def __init__(self):
        self.tiles = []            # lista de bytes de 64 índices
        self.indice_por_pixels = {}
        self.paletas = []          # lista de 16 tuplas RGB
        self.indice_por_paleta = {}
        self.estouros = []
        # As 6 paletas do NOSSO primário ficam carregadas na VRAM junto com a
        # cidade, e um tile do secundário pode apontar para elas. Ignorá-las
        # jogava todo tile de terreno da fonte para a quantização sem precisar.
        self.paletas_do_primario = []
        self.aproximados = 0

    def registra_paleta(self, cores):
        chave = tuple(cores)
        if chave in self.indice_por_paleta:
            return self.indice_por_paleta[chave]
        if len(self.paletas) >= NUM_PALS_TOTAL - NUM_PALS_IN_PRIMARY:
            self.estouros.append(f"paleta {len(self.paletas)+1} passa das 7 do secundário")
            return None
        self.indice_por_paleta[chave] = len(self.paletas)
        self.paletas.append(list(cores))
        return self.indice_por_paleta[chave]

    @staticmethod
    def espelha(indices64, flip_x, flip_y):
        saida = []
        for y in range(8):
            sy = 7 - y if flip_y else y
            for x in range(8):
                sx = 7 - x if flip_x else x
                saida.append(indices64[sy * 8 + sx])
        return bytes(saida)

    def registra_tile(self, indices64):
        """Devolve (indice, bits_de_flip) e reaproveita o tile espelhado.

        O GBA espelha de graça na hora de desenhar. Procurar as quatro
        orientações antes de gastar um slot é o que faz a arte de prédio, que é
        quase toda simétrica, caber nos 512.
        """
        base = bytes(indices64)
        for fx, fy, bits in ((False, False, 0), (True, False, 0x400),
                             (False, True, 0x800), (True, True, 0xC00)):
            chave = self.espelha(base, fx, fy)
            if chave in self.indice_por_pixels:
                return self.indice_por_pixels[chave], bits
        if len(self.tiles) >= NUM_TILES_IN_PRIMARY:
            # Os 512 slots são um teto de hardware, não uma meta. Quando acabam,
            # devolver 0 abria um BURACO no desenho (tile vazio no meio do
            # prédio). Reaproveitar o tile mais parecido que já está no pacote
            # erra alguns pixels num lugar só, e o contador `aproximados` diz
            # quantas vezes isso aconteceu para o render ser olhado com essa
            # informação na mão.
            melhor = min(self.tiles,
                         key=lambda t: sum(1 for a, b in zip(t, base) if a != b))
            self.aproximados += 1
            return self.indice_por_pixels[melhor], 0
        self.indice_por_pixels[base] = len(self.tiles)
        self.tiles.append(base)
        return self.indice_por_pixels[base], 0

    def encaixa_pixels(self, pixels_rgb):
        """Reindexa 64 pixels RGB numa das paletas já registradas.

        Devolve (indice_de_paleta, 64 índices) ou None quando nenhuma paleta
        cobre todas as cores. Não quantiza nada: quem não couber vira relatório.
        """
        cores = {p for p in pixels_rgb if p is not None}
        candidatas = ([(i, pal) for i, pal in enumerate(self.paletas_do_primario)]
                      + [(NUM_PALS_IN_PRIMARY + i, pal) for i, pal in enumerate(self.paletas)])
        for slot, pal in candidatas:
            if cores <= set(pal[1:]):
                mapa = {}
                for j, c in enumerate(pal):
                    mapa.setdefault(c, j)
                return slot, [0 if p is None else mapa[p] for p in pixels_rgb]
        return None

    def escreve(self, destino):
        os.makedirs(os.path.join(destino, "palettes"), exist_ok=True)
        largura, altura = 128, max(8, ((len(self.tiles) + 15) // 16) * 8)
        im = Image.new("P", (largura, altura), 0)
        achatada = []
        for cor in (self.paletas[0] if self.paletas else [(0, 0, 0)] * 16):
            achatada.extend(cor)
        achatada.extend([0] * (768 - len(achatada)))
        im.putpalette(achatada)
        px = im.load()
        for i, tile in enumerate(self.tiles):
            tx, ty = (i % 16) * 8, (i // 16) * 8
            for y in range(8):
                for x in range(8):
                    px[tx + x, ty + y] = tile[y * 8 + x]
        im.save(os.path.join(destino, "tiles.png"))
        for i in range(16):
            cores = self.paletas[i - NUM_PALS_IN_PRIMARY] if (
                NUM_PALS_IN_PRIMARY <= i < NUM_PALS_IN_PRIMARY + len(self.paletas)
            ) else [(0, 0, 0)] * 16
            with open(os.path.join(destino, "palettes", f"{i:02d}.pal"), "w", encoding="utf-8") as f:
                f.write("JASC-PAL\n0100\n16\n")
                for r, g, b in cores:
                    f.write(f"{r} {g} {b}\n")



# ------------------------------------------------------------- conversão ------

class TilesetEmMemoria:
    """Um tileset novo que ainda não foi para o disco, só para renderizar."""

    def __init__(self, pacote, metatiles, attrs):
        self.tiles = [list(t) for t in pacote.tiles]
        self.paletas = [[(0, 0, 0)] * 16 for _ in range(16)]
        for i, pal in enumerate(pacote.paletas):
            self.paletas[NUM_PALS_IN_PRIMARY + i] = list(pal)
        self.metatiles = [tuple(m) for m in metatiles]
        self.attrs = list(attrs)
        self.rotulo = "secundário novo (em memória)"


class Conversao:
    """Constrói o secundário novo da cidade e o `map.bin` convertido.

    A regra de ouro é a da seção 3 do contrato: a cidade copiada usa o NOSSO
    primário, porque o motor desenha o mapa vizinho com os tilesets do mapa
    atual. Então cada palavra de tile da fonte segue um de três caminhos:

      * **paleta 0-5** (terreno natural, pintado com a paleta do primário deles):
        vira tile do NOSSO primário pelo de-para. Custo: zero slot do secundário.
      * **paleta 6-12** (arte urbana autoral deles): entra no secundário novo,
        com a paleta 6-12 correspondente. Custo: um slot de tile.
      * **composição** (as células em que as três camadas tinham tile): vira um
        tile novo, pixel puro, com a paleta que couber.

    Quando um metatile inteiro da fonte casa com um metatile NOSSO pelo de-para,
    a palavra do mapa aponta direto para o nosso e o metatile nem chega a ocupar
    vaga no secundário. É por isso que o de-para vale tanto: cada metatile de
    grama que casa economiza um slot e mantém a costura com a rota vizinha.
    """

    def __init__(self, achatador, prim_nosso, depara, rotulo_primario, limite=0.30):
        self.a = achatador
        self.prim_nosso = prim_nosso
        self.depara = self.limpa_fracos(depara or {}, limite)
        self.rotulo_primario = rotulo_primario
        self.pacote = PacoteSecundario()
        self.pacote.paletas_do_primario = prim_nosso.paletas[:NUM_PALS_IN_PRIMARY]
        self.depara_tiles = dict(self.depara.get("tiles", {}))
        self.derivados = 0
        self.paletas_escolhidas = list(range(NUM_PALS_IN_PRIMARY, NUM_PALS_TOTAL))
        self.peso_paletas = {}
        self.mapa_metatile = {}        # id_fonte -> id_nosso (0-511 primário, 512+ secundário)
        self.metatiles_novos = []      # lista de 8 u16
        self.attrs_novos = []
        self.quantizados = []          # (chave, erro_maximo)
        self.sem_saida = []            # tiles que não couberam em lugar nenhum
        self.tiles_do_nosso_primario = 0
        self.tiles_do_secundario = 0
        self.tiles_compostos = 0

    @staticmethod
    def limpa_fracos(depara, limite):
        """Recusa o casamento do de-para acima de uma distância de desenho.

        Casamento funcional distante é troca de assunto na tela. Em Floaroma os
        quatro metatiles de canteiro de flor foram casados com a nossa grama a
        distância 0,37 (abaixo do "CASAMENTO FRACO" do executor, que corta em
        0,60), e os quatro desabavam sobre um metatile só: a cidade de campo
        florido saía de mato verde inteira, com os prédios certos por cima.

        Recusar manda a peça para o secundário novo, onde ela é copiada como
        está. Custa slot de tile e paga em desenho, e por isso o limite não é
        chutado: a ferramenta varre alguns valores e fica com o que renderiza
        mais parecido com a fonte.
        """
        limpo = dict(depara)
        metatiles = {}
        for k, v in depara.get("metatiles", {}).items():
            nota = (v.get("nota") or "")
            dist = None
            m = re.search(r"dist[âa]ncia de desenho\s+([0-9.]+)", nota)
            if m:
                try:
                    dist = float(m.group(1))
                except ValueError:
                    dist = None
            fraco = "CASAMENTO FRACO" in nota.upper()
            if fraco or (dist is not None and dist > limite):
                v = dict(v)
                v["nosso"] = None
                v["prova"] = "sem-equivalente"
            metatiles[k] = v
        limpo["metatiles"] = metatiles
        return limpo

    def deriva_depara_de_tiles(self):
        """Tira o de-para de TILE do de-para de METATILE, por posição de célula.

        O executor casou metatile com metatile por FUNÇÃO (grama com grama,
        cerca com cerca), porque igualdade de pixel entre a arte deles e a nossa
        é zero: a arte do Retro Platinum é redesenhada inteira. Só que um
        metatile URBANO deles pode ter uma célula de grama no canto, e essa
        célula precisa de um tile nosso equivalente mesmo que o metatile inteiro
        não case com nada.

        A derivação é direta: se o metatile M deles casa com o metatile N nosso,
        então o tile da célula c da camada de baixo de M corresponde ao tile da
        célula c da camada de baixo de N. Cada par vota, e o mais votado ganha.
        É evidência tirada do casamento que uma pessoa já julgou, e não um
        palpite novo.
        """
        # Tile que aparece em metatile que o executor marcou SEM EQUIVALENTE não
        # pode ser derivado para o nosso primário, nem por voto de outro
        # metatile. Sem essa trava, a calçada de concreto de Jubilife (tile 97,
        # paleta 4) era votada para o tijolo vermelho do nosso general_sinnoh e
        # a cidade inteira saía de tijolo rosa, com a arte dos prédios certa por
        # cima. O defeito não aparecia em número nenhum: só no render.
        proibidos = set()
        for id_fonte, de in self.depara.get("metatiles", {}).items():
            if de.get("nosso") is not None:
                continue
            mid = int(id_fonte)
            if mid >= NUM_METATILES_IN_PRIMARY or mid >= len(self.a.prim.metatiles):
                continue
            for entrada in self.a.prim.metatiles[mid]:
                if (entrada & 0x3FF) and ((entrada >> 12) & 0xF) < NUM_PALS_IN_PRIMARY:
                    proibidos.add(str(entrada & 0x3FF))
        self.tiles_proibidos = proibidos

        votos = {}
        for id_fonte, de in self.depara.get("metatiles", {}).items():
            alvo = de.get("nosso")
            if alvo is None:
                continue
            mid = int(id_fonte)
            if mid < NUM_METATILES_IN_PRIMARY and mid < len(self.a.prim.metatiles):
                m_f = self.a.prim.metatiles[mid]
            else:
                continue
            if alvo >= len(self.prim_nosso.metatiles):
                continue
            m_n = self.prim_nosso.metatiles[alvo]
            # camada de baixo com camada de baixo, célula por célula
            for c in range(4):
                ef, en = m_f[c], m_n[c]
                if (ef & 0x3FF) == 0 or (en & 0x3FF) == 0:
                    continue
                if ((ef >> 12) & 0xF) >= NUM_PALS_IN_PRIMARY:
                    continue
                chave = str(ef & 0x3FF)
                if chave in proibidos:
                    continue
                if chave in self.depara_tiles and self.depara_tiles[chave].get("nosso") is not None:
                    continue
                flip_f = ((ef >> 10) & 3)
                flip_n = ((en >> 10) & 3)
                votos.setdefault(chave, {})
                voto = (en & 0x3FF, (en >> 12) & 0xF, flip_f ^ flip_n)
                votos[chave][voto] = votos[chave].get(voto, 0) + 1
        for chave, contagem in votos.items():
            (idx, pal, flip), _ = max(contagem.items(), key=lambda t: t[1])
            self.depara_tiles[chave] = {
                "nosso": idx,
                "pal_nossa": pal,
                "flip": [bool(flip & 1), bool(flip & 2)],
                "prova": "derivado-do-metatile",
            }
            self.derivados += 1
        return self.derivados

    # --- paletas ---------------------------------------------------------
    def pesa_paletas(self, usados):
        """Quantas palavras de tile cada paleta da fonte ainda precisa atender."""
        peso = {}
        for mid in usados:
            de = self.depara.get("metatiles", {}).get(str(mid))
            if de and de.get("nosso") is not None:
                continue
            if mid < NUM_METATILES_IN_PRIMARY:
                ts, local = self.a.prim, mid
            else:
                ts, local = self.a.sec, mid - NUM_METATILES_IN_PRIMARY
            if local >= len(ts.metatiles):
                continue
            for entrada in ts.metatiles[local]:
                idx = entrada & 0x3FF
                if idx == 0:
                    continue
                pal = (entrada >> 12) & 0xF
                if (pal < NUM_PALS_IN_PRIMARY
                        and self.depara_tiles.get(str(idx), {}).get("nosso") is not None):
                    continue
                peso[pal] = peso.get(pal, 0) + 1
        return peso

    def usa_paletas(self, conjunto):
        """Fixa quais 7 paletas da fonte entram no secundário novo."""
        self.paletas_escolhidas = sorted(conjunto)
        for pal in self.paletas_escolhidas:
            cores = (self.a.prim.paletas[pal] if pal < NUM_PALS_IN_PRIMARY
                     else self.a.sec.paletas[pal])
            self.pacote.registra_paleta(cores)

    def prepara_paletas(self, usados=None):
        """Escolhe as 7 paletas do secundário novo pelo USO que sobra, não por posição.

        A ideia óbvia (copiar as paletas 6-12 da fonte para as 6-12 daqui, 1 para
        1) é a errada, e o número mostra: a arte urbana que mora no PRIMÁRIO
        deles (52% dele, medido pelo executor do de-para) é pintada com as
        paletas 0-5 deles, e essas paletas morrem quando a cidade passa a usar o
        nosso primário. Todo tile dessas ia para a quantização sem precisar.

        Então conta-se, tile a tile, quais paletas a arte que SOBRA para o
        secundário realmente usa, e ficam as 7 mais pedidas. As 6 do nosso
        primário continuam disponíveis de graça por cima disso, o que dá 13
        paletas de busca para 7 vagas de verdade.
        """
        if usados is None:
            for i in range(NUM_PALS_IN_PRIMARY, NUM_PALS_TOTAL):
                self.pacote.registra_paleta(self.a.sec.paletas[i])
            return

        peso = {}
        for mid in usados:
            de = self.depara.get("metatiles", {}).get(str(mid))
            if de and de.get("nosso") is not None:
                continue   # metatile inteiro vira nosso: não pesa nada
            if mid < NUM_METATILES_IN_PRIMARY:
                ts, local = self.a.prim, mid
            else:
                ts, local = self.a.sec, mid - NUM_METATILES_IN_PRIMARY
            if local >= len(ts.metatiles):
                continue
            for entrada in ts.metatiles[local]:
                idx = entrada & 0x3FF
                if idx == 0:
                    continue
                pal = (entrada >> 12) & 0xF
                if pal < NUM_PALS_IN_PRIMARY and self.depara_tiles.get(str(idx), {}).get("nosso") is not None:
                    continue   # esse tile vira do nosso primário: não pesa
                peso[pal] = peso.get(pal, 0) + 1

        ordem = sorted(peso, key=lambda p: -peso[p])[:NUM_PALS_TOTAL - NUM_PALS_IN_PRIMARY]
        self.paletas_escolhidas = sorted(ordem)
        for pal in self.paletas_escolhidas:
            cores = (self.a.prim.paletas[pal] if pal < NUM_PALS_IN_PRIMARY
                     else self.a.sec.paletas[pal])
            self.pacote.registra_paleta(cores)
        self.peso_paletas = peso

    def cores_da_paleta_secundaria(self, indice_local):
        return self.pacote.paletas[indice_local]

    # --- tiles -----------------------------------------------------------
    def entrada_convertida(self, entrada):
        """Converte uma palavra u16 da fonte para uma palavra nossa."""
        idx = entrada & 0x3FF
        if idx == 0:
            return 0
        pal = (entrada >> 12) & 0xF
        flips = entrada & 0xC00

        if pal < NUM_PALS_IN_PRIMARY:
            de = self.depara_tiles.get(str(idx))
            if de and de.get("nosso") is not None:
                self.tiles_do_nosso_primario += 1
                fx, fy = de.get("flip", [False, False])
                novo_flip = flips ^ ((0x400 if fx else 0) | (0x800 if fy else 0))
                return (de["nosso"] & 0x3FF) | novo_flip | ((de["pal_nossa"] & 0xF) << 12)
            # Sem equivalente no nosso primário: os pixels vão para o secundário.
            # O flip sai ANTES de pintar e volta na palavra. Registrar o tile já
            # espelhado gastava até quatro slots para o mesmo desenho, e foi o que
            # estourou o orçamento de Jubilife e das duas Oreburgh na primeira
            # medição (medido em 11/09/2026).
            sem_flip = entrada & ~0xC00
            return self.entrada_por_pixels(self.a.pixels(sem_flip),
                                           f"tile {idx} pal {pal}", flips=flips)

        # arte do secundário deles: pixels vão inteiros, com a paleta equivalente
        tiles, _, local = resolve(entrada, self.a.prim, self.a.sec)
        if pal not in self.paletas_escolhidas:
            # a paleta dela não ficou entre as 7: cai no caminho de pixel, que
            # procura entre as 13 e só quantiza se nenhuma cobrir
            sem_flip = entrada & ~0xC00
            return self.entrada_por_pixels(self.a.pixels(sem_flip),
                                           f"tile {idx} pal {pal}", flips=flips)
        # Um caminho só para todo mundo. Registrar o tile por ÍNDICE DE COR aqui
        # e por PIXEL no caminho de baixo dava duas entradas para o mesmo
        # desenho no pacote, e foram esses slots gêmeos que estouraram Jubilife
        # por 8 tiles na estratégia "uso" (medido em 11/09/2026).
        self.tiles_do_secundario += 1
        sem_flip = entrada & ~0xC00
        return self.entrada_por_pixels(self.a.pixels(sem_flip),
                                       f"tile {idx} pal {pal}", flips=flips)

    def entrada_por_pixels(self, pixels, rotulo, flips=0):
        """Põe 64 pixels RGB no secundário, achando paleta, e devolve a palavra.

        `flips` volta na palavra: o tile entra no pacote sem espelho e o motor
        espelha na hora de desenhar, que é de graça.
        """
        encaixe = self.pacote.encaixa_pixels(pixels)
        if encaixe is None:
            encaixe, erro = self.quantiza(pixels)
            self.quantizados.append((rotulo, erro))
            if encaixe is None:
                self.sem_saida.append(f"{rotulo}: nenhuma paleta cobre as cores")
                return 0
        slot, indices = encaixe
        novo, flip_extra = self.pacote.registra_tile(indices)
        if novo is None:
            self.sem_saida.append(f"{rotulo}: não coube nos 512 slots")
            return 0
        return (NUM_TILES_IN_PRIMARY + novo) | ((flips ^ flip_extra) & 0xC00) | ((slot & 0xF) << 12)

    def quantiza(self, pixels):
        """Último recurso: joga cada cor na mais próxima da melhor paleta.

        Nunca é silencioso. O chamador registra o par (o que era, quanto errou) e
        a ferramenta imprime o pior erro, porque quantizar calado é exatamente o
        tipo de "boa notícia" que o contrato manda desconfiar.
        """
        melhor = None
        candidatas = ([(i, pal) for i, pal in enumerate(self.pacote.paletas_do_primario)]
                      + [(NUM_PALS_IN_PRIMARY + i, pal) for i, pal in enumerate(self.pacote.paletas)])
        for i, pal in candidatas:
            erro = 0
            indices = []
            for p in pixels:
                if p is None:
                    indices.append(0)
                    continue
                d, j = min(((sum((a - b) ** 2 for a, b in zip(p, c)), k)
                            for k, c in enumerate(pal) if k > 0), key=lambda t: t[0])
                erro = max(erro, d)
                indices.append(j)
            if melhor is None or erro < melhor[0]:
                melhor = (erro, i, indices)
        if melhor is None:
            return None, 0
        erro, i, indices = melhor
        return (i, indices), erro

    # --- metatiles -------------------------------------------------------
    def converte_metatile(self, id_fonte):
        if id_fonte in self.mapa_metatile:
            return self.mapa_metatile[id_fonte]

        de = self.depara.get("metatiles", {}).get(str(id_fonte))
        if de and de.get("nosso") is not None:
            self.mapa_metatile[id_fonte] = de["nosso"]
            return de["nosso"]

        if id_fonte < NUM_METATILES_IN_PRIMARY:
            ts, local = self.a.prim, id_fonte
        else:
            ts, local = self.a.sec, id_fonte - NUM_METATILES_IN_PRIMARY
        if local >= len(ts.metatiles):
            self.mapa_metatile[id_fonte] = 0
            return 0

        baixo, cima, tipo, _ = self.a.achata(ts.metatiles[local])
        saida = []
        for entrada in list(baixo) + list(cima):
            if isinstance(entrada, tuple) and entrada and entrada[0] == "COMPOSTO":
                chave = entrada[1]
                pixels = self.a.compostos[chave]
                self.tiles_compostos += 1
                saida.append(self.entrada_por_pixels(pixels, f"composição {chave}"))
            else:
                saida.append(self.entrada_convertida(entrada))

        novo_id = NUM_METATILES_IN_PRIMARY + len(self.metatiles_novos)
        self.metatiles_novos.append(saida)
        attr = ts.attrs[local] if local < len(ts.attrs) else 0
        comportamento = attr & 0x00FF
        self.attrs_novos.append((comportamento & 0x00FF) | ((tipo & 0xF) << 12))
        self.mapa_metatile[id_fonte] = novo_id
        return novo_id

    def converte_blocos(self, blocos):
        saida = []
        for palavra in blocos:
            mid = palavra & 0x3FF
            resto = palavra & ~0x3FF     # colisão e elevação continuam iguais
            saida.append(self.converte_metatile(mid) | resto)
        return saida


def escreve_tileset(destino, pacote, metatiles, attrs):
    """Grava tiles.png, palettes/NN.pal, metatiles.bin e metatile_attributes.bin."""
    pacote.escreve(destino)
    with open(os.path.join(destino, "metatiles.bin"), "wb") as f:
        for m in metatiles:
            f.write(struct.pack("<8H", *m))
    with open(os.path.join(destino, "metatile_attributes.bin"), "wb") as f:
        for a in attrs:
            f.write(struct.pack("<H", a))




def escolhe_paletas_guloso(conv, usados, blocos):
    """Escolhe as 7 paletas uma a uma, pela cor que cada escolha SALVA.

    O critério é o erro de cor ponderado pelo número de células do mapa que
    pedem aquele tile: uma paleta que atende a calçada de uma avenida inteira
    vale mais do que uma que atende um vaso. O erro é medido só nas cores que o
    tile usa de verdade, e não na paleta inteira.

    Isso substitui o palpite "copie as 6-12" por uma conta, e é o que tira
    Floaroma e Sandgem do fundo do poço: elas usam 12 das 13 paletas da fonte
    com peso parecido, e qualquer regra fixa joga fora meia cidade.
    """
    from collections import Counter
    uso_celula = Counter(p & 0x3FF for p in blocos)

    # {(tile, paleta): peso}, só do que vai mesmo para o secundário
    pedidos = Counter()
    for mid in usados:
        de = conv.depara.get("metatiles", {}).get(str(mid))
        if de and de.get("nosso") is not None:
            continue
        if mid < NUM_METATILES_IN_PRIMARY:
            ts, local = conv.a.prim, mid
        else:
            ts, local = conv.a.sec, mid - NUM_METATILES_IN_PRIMARY
        if local >= len(ts.metatiles):
            continue
        peso = uso_celula.get(mid, 1)
        for entrada in ts.metatiles[local]:
            idx = entrada & 0x3FF
            if idx == 0:
                continue
            pal = (entrada >> 12) & 0xF
            if (pal < NUM_PALS_IN_PRIMARY
                    and conv.depara_tiles.get(str(idx), {}).get("nosso") is not None):
                continue
            pedidos[(entrada & ~0xC00)] += peso

    # cores que cada pedido usa
    cores_do_pedido = {}
    for entrada in pedidos:
        cores_do_pedido[entrada] = {c for c in conv.a.pixels(entrada) if c is not None}

    def paleta_de(p):
        return conv.a.prim.paletas[p] if p < NUM_PALS_IN_PRIMARY else conv.a.sec.paletas[p]

    # erro de cada pedido contra cada paleta candidata (13 da fonte)
    todas = list(range(NUM_PALS_TOTAL))
    erro = {}
    for p in todas:
        cores_pal = paleta_de(p)[1:]
        for entrada, cores in cores_do_pedido.items():
            pior = 0
            for c in cores:
                d = min(sum((a - b) ** 2 for a, b in zip(c, q)) for q in cores_pal)
                pior = max(pior, d)
            erro[(p, entrada)] = pior

    escolhidas = []
    melhor_atual = {e: min(erro[(p, e)] for p in todas) if False else None for e in pedidos}
    melhor_atual = {e: None for e in pedidos}
    for _ in range(NUM_PALS_TOTAL - NUM_PALS_IN_PRIMARY):
        ganho_por_pal = {}
        for p in todas:
            if p in escolhidas:
                continue
            ganho = 0
            for e, peso in pedidos.items():
                atual = melhor_atual[e]
                novo = erro[(p, e)]
                if atual is None or novo < atual:
                    ganho += peso * ((atual if atual is not None else 200000) - novo)
            ganho_por_pal[p] = ganho
        if not ganho_por_pal:
            break
        escolhida = max(ganho_por_pal, key=lambda x: ganho_por_pal[x])
        escolhidas.append(escolhida)
        for e in pedidos:
            v = erro[(escolhida, e)]
            if melhor_atual[e] is None or v < melhor_atual[e]:
                melhor_atual[e] = v
    return sorted(escolhidas)


# ------------------------------------------------------------- emissão --------

MARCA_FRENTE_C = "// ---- tilesets das cidades copiadas de Sinnoh (dev_scripts/copia_cidade_fonte.py) ----"


def registra_tileset(simbolo, pasta_rel, n_tiles):
    """Acrescenta o tileset novo em graphics.h, metatiles.h e headers.h.

    Tudo entra no FIM do arquivo, atrás de uma marca própria da frente, para que
    o `git merge origin/master` das outras frentes não brigue com este bloco
    (disciplina de repositório, seção 7 do contrato).
    """
    escritos = []

    g = os.path.join(RAIZ, "src/data/tilesets/graphics.h")
    texto = open(g, encoding="utf-8").read()
    if f"gTilesetTiles_{simbolo}[]" not in texto:
        bloco = [""]
        if MARCA_FRENTE_C not in texto:
            bloco.append(MARCA_FRENTE_C)
        # -num_tiles fecha o tamanho real e faz o build reclamar se a arte crescer
        bloco.append(
            f'const u32 gTilesetTiles_{simbolo}[] = INCGFX_U32("{pasta_rel}/tiles.png", '
            f'".4bpp.fastSmol", "-num_tiles {n_tiles} -Wnum_tiles");')
        bloco.append("")
        bloco.append(f"const u16 gTilesetPalettes_{simbolo}[][16] =")
        bloco.append("{")
        for i in range(16):
            bloco.append(f'    INCGFX_U16("{pasta_rel}/palettes/{i:02d}.pal", ".gbapal"),')
        bloco.append("};")
        open(g, "w", encoding="utf-8").write(texto.rstrip("\n") + "\n" + "\n".join(bloco) + "\n")
        escritos.append(g)

    m = os.path.join(RAIZ, "src/data/tilesets/metatiles.h")
    texto = open(m, encoding="utf-8").read()
    if f"gMetatiles_{simbolo}[]" not in texto:
        bloco = [""]
        if MARCA_FRENTE_C not in texto:
            bloco.append(MARCA_FRENTE_C)
        bloco.append(f'const u16 gMetatiles_{simbolo}[] = INCBIN_U16("{pasta_rel}/metatiles.bin");')
        bloco.append(f'const u16 gMetatileAttributes_{simbolo}[] = '
                     f'INCBIN_U16("{pasta_rel}/metatile_attributes.bin");')
        open(m, "w", encoding="utf-8").write(texto.rstrip("\n") + "\n" + "\n".join(bloco) + "\n")
        escritos.append(m)

    h = os.path.join(RAIZ, "src/data/tilesets/headers.h")
    texto = open(h, encoding="utf-8").read()
    if f"gTileset_{simbolo} =" not in texto:
        bloco = [""]
        if MARCA_FRENTE_C not in texto:
            bloco.append(MARCA_FRENTE_C)
        bloco += [
            f"const struct Tileset gTileset_{simbolo} =",
            "{",
            "    .isCompressed = TRUE,",
            "    .isSecondary = TRUE,",
            f"    .tiles = gTilesetTiles_{simbolo},",
            f"    .palettes = gTilesetPalettes_{simbolo},",
            f"    .metatiles = gMetatiles_{simbolo},",
            f"    .metatileAttributes = gMetatileAttributes_{simbolo},",
            "    .callback = NULL,",
            "};",
        ]
        open(h, "w", encoding="utf-8").write(texto.rstrip("\n") + "\n" + "\n".join(bloco) + "\n")
        escritos.append(h)
    return escritos


def religa_layout(nome_layout, simbolo_secundario, largura, altura):
    """Troca o secundário e o tamanho do layout, SEM mexer no `id`.

    O `mapLayoutId` não muda nunca: a save guarda o layout por id, e recriar o
    layout em vez de substituí-lo no lugar quebraria a save de quem já está
    dentro da cidade (item 3 da seção 1 do contrato).
    """
    caminho = os.path.join(RAIZ, "data/layouts/layouts.json")
    with open(caminho, encoding="utf-8") as f:
        dados = json.load(f)
    achou = False
    for l in dados["layouts"]:
        if l["name"] == nome_layout:
            l["secondary_tileset"] = f"gTileset_{simbolo_secundario}"
            l["width"] = largura
            l["height"] = altura
            achou = True
    if not achou:
        raise SystemExit(f"layout {nome_layout} não achado para religar")
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return caminho


def escreve_blocos(caminho, palavras):
    with open(caminho, "wb") as f:
        for p in palavras:
            f.write(struct.pack("<H", p))


# ------------------------------------------------------------------ render ----

def render_mapa(blocos, largura, altura, prim, sec, tpm_prim, tpm_sec, escala=1,
                objetos=None, achatador=None):
    """Desenha um mapa em PNG a partir de blocos e dois tilesets já carregados.

    Com `achatador`, quem resolve cada `mid` é ELE, e não o par (prim, sec)
    passado: é assim que o mapa FUNDIDO (Oreburgh, dois mapas do hack num só
    nosso) se desenha, porque ali cada metatile pode vir de um par diferente.
    """
    # A cor 0 da paleta 0 do primário é o backdrop compartilhado dos BG: é ela
    # que aparece onde nenhuma camada desenha, e não preto.
    fundo = prim.paletas[0][0]
    im = Image.new("RGB", (largura * 16, altura * 16), fundo)
    px = im.load()
    cache = {}
    for i, palavra in enumerate(blocos[:largura * altura]):
        mid = palavra & 0x3FF
        mx, my = (i % largura) * 16, (i // largura) * 16
        if mid not in cache and achatador is not None:
            cache[mid] = achatador.desenha(mid, fundo=fundo)
        if mid not in cache:
            if mid < NUM_METATILES_IN_PRIMARY:
                ts, tpm, local = prim, tpm_prim, mid
            else:
                ts, tpm, local = sec, tpm_sec, mid - NUM_METATILES_IN_PRIMARY
            if local >= len(ts.metatiles):
                cache[mid] = [MAGENTA] * 256
            else:
                m = ts.metatiles[local]
                bloco = [fundo] * 256
                for camada in range(tpm // 4):
                    for c in range(4):
                        entrada = m[camada * 4 + c]
                        if (entrada & 0x3FF) == 0:
                            continue
                        tiles, paletas, e = resolve(entrada, prim, sec)
                        if (e & 0x3FF) >= len(tiles):
                            continue
                        pix = pinta_tile(tiles, paletas, e, transparente=None)
                        ox, oy = (c % 2) * 8, (c // 2) * 8
                        for y in range(8):
                            for x in range(8):
                                p = pix[y * 8 + x]
                                if p is not None:
                                    bloco[(oy + y) * 16 + (ox + x)] = p
                cache[mid] = bloco
        bloco = cache[mid]
        for y in range(16):
            for x in range(16):
                px[mx + x, my + y] = bloco[y * 16 + x]
    if objetos:
        desenho = ImageDraw.Draw(im)
        for n, obj in enumerate(objetos, start=1):
            ox, oy = obj["x"] * 16, obj["y"] * 16
            desenho.rectangle([ox, oy, ox + 15, oy + 15], outline=(255, 0, 0), width=1)
            desenho.text((ox, oy - 8), str(n), fill=(255, 0, 0))
    if escala != 1:
        im = im.resize((im.width * escala, im.height * escala), Image.NEAREST)
    return im


def prova_contra_render_de_referencia(cidade, meu_png, pasta_ref):
    """Compara o meu render da FONTE com o render de referência da própria fonte.

    É a prova de que o leitor de metatile de TRÊS camadas está certo. Ela só
    vale com o overlay de `object_event` desenhado dos dois lados: sem ele, os
    retângulos vermelhos da referência aparecem como 0,15% de diferença e
    escondem qualquer defeito de verdade debaixo do mesmo número.
    """
    ref = os.path.join(pasta_ref, f"{cidade}.png")
    if not os.path.exists(ref):
        return None, f"render de referência não existe: {ref}"
    a = Image.open(meu_png).convert("RGB")
    b = Image.open(ref).convert("RGB")
    if a.size != b.size:
        return False, f"tamanhos diferentes: {a.size} contra {b.size}"
    pa, pb = a.load(), b.load()
    largura, altura = a.size
    n = sum(1 for y in range(altura) for x in range(largura) if pa[x, y] != pb[x, y])
    total = largura * altura
    return n == 0, f"{n} pixels diferentes de {total} ({100.0 * n / total:.4f}%)"


# ------------------------------------------------------------------ provas ----

def provas_negativas(achatador):
    """Testes que têm de FALHAR se a ferramenta estiver mentindo.

    Cada um devolve (nome, passou, explicação). "Passou" aqui significa que o
    erro FOI detectado, não que está tudo bem.
    """
    resultados = []

    # 1. Fronteira de VRAM: o tile 511 é o último do primário e o 512 é o
    #    primeiro do secundário. Esta prova já pegou um defeito de verdade, o
    #    dela mesma: comparar o objeto Tileset com a LISTA de tiles que o método
    #    devolve dá sempre falso, e a ferramenta acusava erro onde não havia.
    tiles512, _, local512 = achatador.tiles_e_paletas(512)
    tiles511, _, local511 = achatador.tiles_e_paletas(511)
    resultados.append((
        "fronteira de VRAM em 512",
        tiles512 is achatador.sec.tiles and local512 == 0
        and tiles511 is achatador.prim.tiles and local511 == 511,
        f"511 -> {'primário' if tiles511 is achatador.prim.tiles else 'secundário'} local {local511}; "
        f"512 -> {'secundário' if tiles512 is achatador.sec.tiles else 'primário'} local {local512}",
    ))

    # 2. Metatile de 24 B não pode ser lido como 16 B: as camadas mudam de lugar.
    m = achatador.prim.metatiles[0] if achatador.prim.metatiles else tuple([0] * 12)
    resultados.append((
        "metatile da fonte tem 12 entradas",
        len(m) == TILES_POR_METATILE_FONTE,
        f"{len(m)} entradas por metatile na fonte",
    ))

    # 3. Achatar um metatile com as três camadas cheias TEM de gerar composição.
    achou = False
    for m in achatador.prim.metatiles + achatador.sec.metatiles:
        camadas = [m[0:4], m[4:8], m[8:12]]
        if all(any(t & 0x3FF for t in c) for c in camadas):
            _, _, _, comps = achatador.achata(m)
            achou = bool(comps)
            break
    resultados.append((
        "achatamento de três camadas gera tile composto",
        achou,
        "metatile de três camadas achatado sem compor nada" if not achou else "compôs",
    ))

    # 4. Tile fora da faixa tem de sair MAGENTA, e não preto silencioso.
    fora = pinta_tile(achatador.prim.tiles, achatador.prim.paletas, 1023)
    resultados.append((
        "tile fora da faixa sai magenta",
        fora[0] == MAGENTA,
        f"cor devolvida {fora[0]}",
    ))
    return resultados


# ------------------------------------------------------------------- corpo ----

def carrega_lado_fonte(raiz_fonte, nome_layout):
    layouts = le_layouts(os.path.join(raiz_fonte, "data/layouts/layouts.json"))
    achados = [l for l in layouts["layouts"] if l["name"] == nome_layout]
    if not achados:
        raise SystemExit(f"layout {nome_layout} não existe na fonte")
    lay = achados[0]
    prim = Tileset(pasta_do_simbolo(raiz_fonte, lay["primary_tileset"], False),
                   TILES_POR_METATILE_FONTE, lay["primary_tileset"])
    sec = Tileset(pasta_do_simbolo(raiz_fonte, lay["secondary_tileset"], True),
                  TILES_POR_METATILE_FONTE, lay["secondary_tileset"])
    blocos = le_blocos(os.path.join(raiz_fonte, lay["blockdata_filepath"].lstrip("./")))
    borda = le_blocos(os.path.join(raiz_fonte, lay["border_filepath"].lstrip("./")))
    return lay, prim, sec, blocos, borda


# Cidade que o hack desenhou em DOIS mapas e que aqui é UM só. Hoje só
# Oreburgh. Os números vêm do dossiê (`dev_scripts/dossies_sinnoh/OreburghCity.json`)
# e da resposta 90 do condutor Fable, que escolheu a OPÇÃO 2: os dois mapas
# inteiros, menos a pilha de carvão do pátio, 955 tiles das 1.024 vagas.
FUSOES = {
    "OreburghCity": {
        "nosso": "OreburghCity_Layout",
        "largura": 72, "altura": 76,
        # `preenchimento` é o metatile 14 do primário `OutdoorOreburgh`, a rocha
        # de moldura que o próprio mapa sul usa no canto sudoeste e que os dois
        # `border.bin` deles já usam nos quatro cantos.
        "preenchimento": 14,
        "partes": [
            {"layout": "OreburghCityNorth_Layout", "mapa": "OreburghCityNorth",
             "x": 0, "y": 0},
            # A conexão do hack diz que o sul entra em x=14 do norte, e 14 + 58
            # fecha os 72 de largura do norte, sem sobra nem falta.
            {"layout": "OreburghCitySouth_Layout", "mapa": "OreburghCitySouth",
             "x": 14, "y": 32},
        ],
        # A pilha de carvão do pátio, em (27..36, 4..11) do mapa sul deles, que
        # é (41..50, 36..43) no fundido. Ela sozinha custa 156 tiles exclusivos
        # (desenho orgânico, sem repetição) e é o que separa a opção 1, que não
        # cabe, da opção 2, que cabe com 69 vagas de folga.
        "apagar": [[41, 36, 50, 43]],
    },
}


def carrega_fusao(raiz_fonte, spec):
    """Monta UM mapa de fonte a partir de dois mapas do hack, renumerando.

    Por que renumerar, e não simplesmente concatenar os dois pares de tilesets:
    medido em 11/09/2026, os dois secundários de Oreburgh pedem 444 + 366 = 810
    tiles para as 512 vagas de tile de um secundário, e 7 + 7 paletas altas para
    as 7 vagas. Um par só não comporta os dois. O que comporta é o espaço de
    NÚMERO de metatile: 128 + 81 do primário e 172 + 139 do secundário dão 520
    metatiles distintos, e uma célula de `map.bin` escreve 1.024 números. Então
    cada metatile usado ganha um número novo, e a tabela `rota` guarda de qual
    par ele veio. Quem lê a arte depois é o `Achatador`, que passa a ter uma
    lista de partes.

    A colisão e a elevação de cada célula vêm da célula ORIGINAL: só o número do
    metatile é trocado. O preenchimento (as 14 colunas que nenhum dos dois mapas
    cobre, mais o que `apagar` manda tirar) entra INTRANSPONÍVEL, porque a
    moldura deles tem colisão 0 e a busca em largura andaria por cima dela.
    """
    W, H = spec["largura"], spec["altura"]
    partes, dados = [], []
    for i, pedaco in enumerate(spec["partes"]):
        lay, prim, sec, blocos, borda = carrega_lado_fonte(raiz_fonte, pedaco["layout"])
        partes.append((prim, sec))
        dados.append((pedaco, lay, blocos, borda))

    rota, numeros = {}, {}

    def numero(parte, mid):
        chave = (parte, mid)
        if chave not in numeros:
            novo = len(numeros)
            if novo >= 1024:
                raise SystemExit("a fusão passou de 1.024 metatiles distintos")
            numeros[chave] = novo
            rota[novo] = chave
        return numeros[chave]

    # O preenchimento nasce primeiro, com o número 0 reservado para ele: assim
    # célula não escrita nunca fica apontando para arte por acidente.
    id_vazio = numero(0, spec["preenchimento"])
    blocos_f = [id_vazio | (1 << 10)] * (W * H)      # colisão 1 em tudo

    for i, (pedaco, lay, blocos, _borda) in enumerate(dados):
        ox, oy = pedaco["x"], pedaco["y"]
        for y in range(lay["height"]):
            for x in range(lay["width"]):
                gx, gy = ox + x, oy + y
                if not (0 <= gx < W and 0 <= gy < H):
                    raise SystemExit(f"a parte {pedaco['layout']} sai do "
                                     f"retângulo {W}x{H} em ({gx},{gy})")
                palavra = blocos[y * lay["width"] + x]
                novo = numero(i, palavra & 0x3FF)
                blocos_f[gy * W + gx] = novo | (palavra & ~0x3FF)

    for x0, y0, x1, y1 in spec.get("apagar", []):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                blocos_f[y * W + x] = id_vazio | (1 << 10)

    achatador = Achatador(partes[0][0], partes[0][1],
                          extras=partes[1:], rota=rota)
    lay_f = {"name": spec["nosso"], "width": W, "height": H,
             "primary_tileset": dados[0][1]["primary_tileset"],
             "secondary_tileset": dados[0][1]["secondary_tileset"],
             "fundida": [p["layout"] for p in spec["partes"]]}
    borda_f = [id_vazio] * 4
    print(f"  --fundir: {' + '.join(p['layout'] for p in spec['partes'])} "
          f"-> {W}x{H}, {len(numeros)} metatiles distintos renumerados "
          f"(de 1.024 possíveis)")
    return lay_f, partes[0][0], partes[0][1], blocos_f, borda_f, achatador


def objetos_da_fonte(raiz_fonte, nome_mapa):
    """Os `object_events` do mapa da fonte, só para desenhar o overlay da prova."""
    caminho = os.path.join(raiz_fonte, "data/maps", nome_mapa, "map.json")
    if not os.path.exists(caminho):
        return []
    with open(caminho, encoding="utf-8") as f:
        return json.load(f).get("object_events", [])


def carrega_lado_nosso(nome_layout):
    layouts = le_layouts(os.path.join(RAIZ, "data/layouts/layouts.json"))
    achados = [l for l in layouts["layouts"] if l["name"] == nome_layout]
    if not achados:
        raise SystemExit(f"layout {nome_layout} não existe aqui")
    lay = achados[0]
    prim = Tileset(pasta_do_simbolo(RAIZ, lay["primary_tileset"], False),
                   TILES_POR_METATILE_NOSSO, lay["primary_tileset"])
    sec = Tileset(pasta_do_simbolo(RAIZ, lay["secondary_tileset"], True),
                  TILES_POR_METATILE_NOSSO, lay["secondary_tileset"])
    blocos = le_blocos(os.path.join(RAIZ, lay["blockdata_filepath"].lstrip("./")))
    borda = le_blocos(os.path.join(RAIZ, lay["border_filepath"].lstrip("./")))
    return lay, prim, sec, blocos, borda


def mede(nome_fonte, nome_nosso, raiz_fonte, fusao=None):
    if fusao is not None:
        lay_f, prim_f, sec_f, blocos_f, borda_f, achatador = carrega_fusao(
            raiz_fonte, fusao)
    else:
        lay_f, prim_f, sec_f, blocos_f, borda_f = carrega_lado_fonte(raiz_fonte,
                                                                     nome_fonte)
        achatador = Achatador(prim_f, sec_f)
    lay_n, prim_n, sec_n, blocos_n, borda_n = carrega_lado_nosso(nome_nosso)

    usados = set()
    for palavra in blocos_f + borda_f:
        usados.add(palavra & 0x3FF)
    tres_camadas = 0
    celulas_compostas = 0
    tiles_pal_baixa = set()
    tiles_pal_alta = set()
    paletas_altas = set()
    comportamentos_suspeitos = {}

    for mid in sorted(usados):
        m, attr_f, parte = achatador.metatile(mid)
        if m is None:
            continue
        camadas = [m[0:4], m[4:8], m[8:12]]
        if sum(1 for c in camadas if any(t & 0x3FF for t in c)) == 3:
            tres_camadas += 1
        _, _, _, comps = achatador.achata(m, parte)
        celulas_compostas += len(comps)
        for entrada in m:
            idx = entrada & 0x3FF
            if idx == 0:
                continue
            pal = (entrada >> 12) & 0xF
            if pal < NUM_PALS_IN_PRIMARY:
                tiles_pal_baixa.add(idx)
            else:
                tiles_pal_alta.add(idx)
                paletas_altas.add(pal)
        comportamento = attr_f & 0x00FF
        if comportamento in MB_DIVERGENTES:
            comportamentos_suspeitos.setdefault(comportamento, []).append(mid)

    return {
        "lay_fonte": lay_f, "lay_nosso": lay_n,
        "prim_f": prim_f, "sec_f": sec_f, "prim_n": prim_n, "sec_n": sec_n,
        "blocos_f": blocos_f, "borda_f": borda_f,
        "blocos_n": blocos_n, "borda_n": borda_n,
        "achatador": achatador,
        "usados": usados,
        "tres_camadas": tres_camadas,
        "celulas_compostas": celulas_compostas,
        "compostos_distintos": len(achatador.compostos),
        "tiles_pal_baixa": tiles_pal_baixa,
        "tiles_pal_alta": tiles_pal_alta,
        "paletas_altas": sorted(paletas_altas),
        "comportamentos_suspeitos": comportamentos_suspeitos,
    }


def lados_com_conexao(nome_mapa):
    """Quais bordas da NOSSA cidade uma rota vizinha desenha.

    O motor desenha o mapa conectado com os tilesets do mapa atual, e a janela é
    de ANEL_COSTURA tiles. A recíproca também vale: parado na rota, o jogador vê
    a faixa da CIDADE desenhada com os tilesets da ROTA. Logo a faixa de 8 tiles
    de um lado CONECTADO tem de continuar sendo a nossa arte, e só ela. Lado sem
    conexão nenhuma (o oeste de Twinleaf, por exemplo) ninguém desenha de fora, e
    lá a arte é deles, inteira.
    """
    caminho = os.path.join(RAIZ, "data", "maps", nome_mapa, "map.json")
    if not os.path.exists(caminho):
        return set()
    with open(caminho, encoding="utf-8") as f:
        mj = json.load(f)
    return {c["direction"] for c in (mj.get("connections") or [])
            if c.get("direction") in ("up", "down", "left", "right")}


def zona_da_celula(cx, cy, largura, altura, lados):
    """'anel' se alguma rota vizinha desenha esta célula; 'interior' se não."""
    if "up" in lados and cy < ANEL_COSTURA:
        return "anel"
    if "down" in lados and cy >= altura - ANEL_COSTURA:
        return "anel"
    if "left" in lados and cx < ANEL_COSTURA:
        return "anel"
    if "right" in lados and cx >= largura - ANEL_COSTURA:
        return "anel"
    return "interior"


CIDADES = {
    "TwinleafTown": ("TwinleafTown_Layout", "TwinleafTown_Layout"),
    # A fundida: os dois mapas do hack num só nosso (ver FUSOES). Só existe
    # com --fundir; o nome do layout da fonte fica como rótulo.
    "OreburghCity": ("OreburghCityNorth_Layout", "OreburghCity_Layout"),
    "SandgemTown": ("SandgemTown_Layout", "SandgemTown_Layout"),
    "JubilifeCity": ("JubilifeCity_Layout", "JubilifeCity_Layout"),
    "OreburghCityNorth": ("OreburghCityNorth_Layout", "OreburghCity_Layout"),
    "OreburghCitySouth": ("OreburghCitySouth_Layout", "OreburghCity_Layout"),
    "FloaromaTown": ("FloaromaTown_Layout", "FloaromaTown_Layout"),
}


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--cidade", required=True, choices=sorted(CIDADES),
                   help="mapa da FONTE a medir ou copiar")
    p.add_argument("--fonte", default=FONTE_PADRAO, help="raiz do decomp de origem")
    p.add_argument("--demo", action="store_true", help="só mede e roda as provas negativas")
    p.add_argument("--render", metavar="PASTA", help="grava o render triplo nesta pasta")
    p.add_argument("--escala", type=int, default=1)
    p.add_argument("--depara", help="JSON de-para do primário (do executor C2)")
    p.add_argument("--converte", action="store_true",
                   help="roda a conversão em memória e imprime o orçamento real")
    p.add_argument("--aplicar", action="store_true",
                   help="grava o tileset novo, religa o layout e escreve o map.bin")
    p.add_argument("--simbolo", help="nome do tileset novo, ex.: JubilifeSinnohRP")
    p.add_argument("--par-proprio", action="store_true",
                   help="dá à cidade um PAR de tilesets só dela (primário novo + "
                        "secundário novo): 13 paletas, 944 slots de tile e 1024 "
                        "metatiles, com os índices da costura PINADOS")
    p.add_argument("--pinar-so-necessario", action="store_true",
                   help="pina só o que a costura EXIGE depois da troca (faixa da "
                        "rota vizinha + borda dela + os índices que o mapa NOVO usa "
                        "no anel). Sem isto, pina também o que a nossa cidade de "
                        "HOJE usa no anel, que deixa de existir quando o map.bin "
                        "é substituído")
    p.add_argument("--fundir", action="store_true",
                   help="monta o mapa da fonte a partir de DOIS mapas do hack "
                        "(hoje só OreburghCity: o norte 72x32 e o sul 58x44, "
                        "empilhados em 72x76, menos a pilha de carvão do pátio, "
                        "que é a opção 2 da resposta 90 do Fable)")
    p.add_argument("--recorte", metavar="X,Y,L,A",
                   help="recorta a planta da FONTE antes de copiar, em células. "
                        "Existe para a cidade cuja planta se estende ALÉM da "
                        "saída que o próprio autor desenhou: Floaroma é 42x44 "
                        "na fonte e 34x38 aqui (resposta 91 do Fable), porque "
                        "as setas de saída dele estão em x=33 e y=37 e o que "
                        "sobra fora disso é, no nosso mundo, Route 204 e 205")
    p.add_argument("--sem-animacao", action="store_true",
                   help="o primário novo NÃO anima: os 80 slots de VRAM de 432 a "
                        "511 viram arte e o .callback vira NULL. Só para cidade "
                        "que hoje não tem célula animada nenhuma (medir antes); "
                        "em troca o orçamento de tile sobe de 944 para 1024")
    p.add_argument("--sem-conexao", action="store_true",
                   help="a cidade NÃO tem conexão de mapa (as saídas viram warp, "
                        "ver dev_scripts/saidas_por_warp.py). O anel deixa de "
                        "existir: nada é pinado, o mapa inteiro é interior e a "
                        "arte da borda também é a do hack")
    p.add_argument("--anel-tabela", default=TABELA_ANEL_PADRAO,
                   help="JSON com o julgamento humano do anel, por cidade")
    p.add_argument("--prancha-anel", metavar="PASTA",
                   help="grava a prancha do anel (hack | cópia) de cada lado conectado")
    p.add_argument("--prova-fonte", action="store_true",
                   help="compara o render da FONTE com o render de referência dela (prova do leitor de 3 camadas)")
    args = p.parse_args()

    nome_fonte, nome_nosso = CIDADES[args.cidade]
    fusao = None
    if args.fundir:
        if args.cidade not in FUSOES:
            raise SystemExit(f"--fundir não tem receita para {args.cidade}")
        fusao = FUSOES[args.cidade]
    elif args.cidade in FUSOES:
        print(f"  AVISO: {args.cidade} é uma cidade FUNDIDA no hack "
              f"({' + '.join(p['layout'] for p in FUSOES[args.cidade]['partes'])}) "
              f"e sem --fundir você está copiando só a primeira metade.")
    d = mede(nome_fonte, nome_nosso, args.fonte, fusao=fusao)
    lf, ln = d["lay_fonte"], d["lay_nosso"]
    if args.recorte:
        rx, ry, rl, ra = (int(v) for v in args.recorte.split(","))
        W0, H0 = lf["width"], lf["height"]
        if rx < 0 or ry < 0 or rx + rl > W0 or ry + ra > H0:
            raise SystemExit(f"--recorte {args.recorte} sai da planta {W0}x{H0}")
        d["blocos_f"] = [d["blocos_f"][(ry + y) * W0 + rx + x]
                         for y in range(ra) for x in range(rl)]
        lf["width"], lf["height"] = rl, ra
        # `usados` e o resto da medida foram tirados da planta INTEIRA; refazer
        # com a planta recortada é o que faz o orçamento contar só o que entra.
        d["usados"] = {w & 0x3FF for w in d["blocos_f"]} | {w & 0x3FF
                                                            for w in d["borda_f"]}
        print(f"  --recorte: planta da fonte {W0}x{H0} -> {rl}x{ra} "
              f"a partir de ({rx},{ry})")
    lados = lados_com_conexao(ln["name"].replace("_Layout", ""))
    if args.sem_conexao:
        # Regra de motor medida em 11/09/2026 (contrato, seção 3.1): travessia
        # por conexão recarrega SÓ o secundário, então cidade com primário
        # próprio não pode ter conexão. Quem converte as saídas em warp é o
        # dev_scripts/saidas_por_warp.py; aqui a consequência é que o ANEL deixa
        # de existir, o mapa inteiro é interior e a arte da borda também é a do
        # hack.
        if lados:
            print(f"  --sem-conexao: os lados {sorted(lados)} deixam de ser anel "
                  f"(as conexões saem do map.json; ver saidas_por_warp.py)")
        lados = set()

    print(f"=== {args.cidade} ===")
    print(f"  nosso  {ln['name']:26s} {ln['width']:3d}x{ln['height']:<3d} "
          f"prim={ln['primary_tileset']} sec={ln['secondary_tileset']}")
    print(f"  fonte  {lf['name']:26s} {lf['width']:3d}x{lf['height']:<3d} "
          f"prim={lf['primary_tileset']} sec={lf['secondary_tileset']}")
    print(f"  metatiles usados pela fonte: {len(d['usados'])}")
    print(f"  metatiles de TRÊS camadas:   {d['tres_camadas']}")
    print(f"  células que viram composição: {d['celulas_compostas']} "
          f"({d['compostos_distintos']} tiles distintos depois de deduplicar)")
    print(f"  tiles com paleta 0-5 (viram o NOSSO primário pelo de-para): {len(d['tiles_pal_baixa'])}")
    print(f"  tiles com paleta 6-12 (vão para o secundário novo):        {len(d['tiles_pal_alta'])}")
    orcamento = len(d["tiles_pal_alta"]) + d["compostos_distintos"]
    folga = NUM_TILES_IN_PRIMARY - orcamento
    # Este orçamento é o do caminho ANTIGO (`--converte`), em que a cidade
    # ganhava só um secundário novo e continuava no primário compartilhado. No
    # `--par-proprio` ele não manda em nada: lá o orçamento é o do par inteiro
    # (944 tiles, ou 1.024 com `--sem-animacao`) e sai impresso mais abaixo. Um
    # ESTOURO aqui com `--par-proprio` ligado não é defeito, e dizer isso em voz
    # alta é mais barato do que o executor parar achando que é.
    sufixo = ("  <<< ESTOURO" if folga < 0 else "")
    if args.par_proprio:
        sufixo += "   (não vale com --par-proprio; ver o orçamento do par abaixo)"
    print(f"  ORÇAMENTO do secundário novo: {orcamento} de {NUM_TILES_IN_PRIMARY} slots, "
          f"folga {folga}" + sufixo)
    print(f"  paletas altas usadas pela fonte: {d['paletas_altas']} "
          f"({len(d['paletas_altas'])} de 7)")
    if d["comportamentos_suspeitos"]:
        print("  COMPORTAMENTOS em slot divergente (precisam de olho humano):")
        for c, ids in sorted(d["comportamentos_suspeitos"].items()):
            print(f"    0x{c:02X} em {len(ids)} metatiles: {ids[:8]}")
    else:
        print("  comportamentos: nenhum em slot divergente do enum MB_*")

    if args.demo:
        print("  --- provas negativas ---")
        falhou = False
        for nome, passou, expl in provas_negativas(d["achatador"]):
            marca = "ok " if passou else "RUIM"
            print(f"    [{marca}] {nome}: {expl}")
            falhou = falhou or not passou
        if falhou:
            print("  UMA PROVA NEGATIVA FALHOU: a leitura está errada, não siga.")
            return 1

    if args.par_proprio:
        roda_par_proprio(args, d, lf, ln, lados)

    if args.converte:
        depara = None
        if args.depara and os.path.exists(args.depara):
            with open(args.depara, encoding="utf-8") as f:
                bruto = json.load(f)
            chave = re.sub(r"(?<!^)(?=[A-Z])", "_",
                           lf["primary_tileset"].replace("gTileset_", "")).lower()
            depara = bruto.get("primarios", {}).get(chave)
            print(f"  de-para: {args.depara} seção {chave} "
                  f"({len((depara or {}).get('metatiles', {}))} metatiles, "
                  f"{len((depara or {}).get('tiles', {}))} tiles)")
        else:
            print("  de-para: NENHUM (tudo cai no secundário; é o pior caso)")
        # Duas estratégias de paleta, e a ferramenta fica com a que fecha:
        #   "fixas" copia as 6-12 da fonte, 1 para 1, e preserva os índices de
        #     cor originais dos tiles do secundário deles (zero quantização ali);
        #   "uso"  escolhe as 7 mais pedidas entre as 13, o que resgata a arte
        #     urbana que mora no PRIMÁRIO deles e morreria na quantização.
        # Nenhuma das duas ganha sempre: em Jubilife "fixas" cabe e "uso" estoura
        # por 4 tiles; em Twinleaf "uso" corta a quantização de 60 para 28.
        # Varredura de conjuntos de paleta. São 13 paletas na fonte para 7 vagas,
        # e nenhuma regra fixa ganha sempre: copiar as 6-12 preserva a arte do
        # secundário deles mas mata a calçada de concreto, que mora no primário
        # deles; escolher as 7 mais pedidas salva a calçada mas pode estourar os
        # 512 slots. Então prova-se um punhado de conjuntos e fica o melhor que
        # CABE, com a quantização como critério de desempate.
        alvo = render_mapa(d["blocos_f"], lf["width"], lf["height"], d["prim_f"], d["sec_f"],
                           TILES_POR_METATILE_FONTE, TILES_POR_METATILE_FONTE,
                           achatador=d["achatador"])
        alvo_px = alvo.load()

        # A MEDIDA QUE VALE É A DO INTERIOR, e a razão é o ponto cego que quase
        # passou batido em 11/09/2026. A conta antiga descontava toda célula cujo
        # metatile o de-para tivesse trocado pelo nosso. Só que é exatamente ali
        # que o de-para erra: em Sandgem os metatiles 24, 25 e 26 (o caminho de
        # terra) foram casados com 331, 289 e 333 do nosso general_sinnoh, que
        # são tábua de madeira e pedrisco, e a rua da cidade saiu de tábua. A
        # conta antiga não via nada: quanto MAIS o de-para trocasse, MENOS
        # células entravam no denominador, e a nota subia. Sandgem marcava 94,91%
        # com a rua errada.
        #
        # O interior é a região que nenhuma rota vizinha desenha (o motor desenha
        # o mapa conectado com os tilesets do mapa atual, e a janela é de 8
        # tiles). Lá dentro a arte tem de ser DELES, ponto. O anel de 8 tiles da
        # borda é NOSSO por necessidade de costura e sai da conta, mas sai por
        # POSIÇÃO, não por "o de-para mexeu", que é o que se podia fraudar.
        def fidelidade_interior(saida):
            spx = saida.load()
            iguais = difere = 0
            for cy in range(lf["height"]):
                for cx in range(lf["width"]):
                    if zona_da_celula(cx, cy, lf["width"], lf["height"], lados) != "interior":
                        continue
                    mx, my = cx * 16, cy * 16
                    for y in range(my, my + 16):
                        for x in range(mx, mx + 16):
                            if alvo_px[x, y] == spx[x, y]:
                                iguais += 1
                            else:
                                difere += 1
            return 100.0 * iguais / max(1, iguais + difere)

        def fidelidade_de(cand, blocos_novos, depara_usado):
            sec_mem = TilesetEmMemoria(cand.pacote, cand.metatiles_novos, cand.attrs_novos)
            saida = render_mapa(blocos_novos, lf["width"], lf["height"], d["prim_n"], sec_mem,
                                TILES_POR_METATILE_NOSSO, TILES_POR_METATILE_NOSSO)
            return fidelidade_interior(saida)

        # Primeiro o limite de aceitação do de-para, com a paleta gulosa fixa.
        melhor_limite, nota_limite = None, None
        for limite in (1.01, 0.60, 0.40, 0.30, 0.20, 0.10):
            t = Conversao(d["achatador"], d["prim_n"], depara, ln["primary_tileset"], limite)
            t.deriva_depara_de_tiles()
            t.usa_paletas(escolhe_paletas_guloso(t, d["usados"], d["blocos_f"]))
            bl = t.converte_blocos(d["blocos_f"])
            t.converte_blocos(d["borda_f"])
            fid = fidelidade_de(t, bl, t.depara)
            print(f"  limite de de-para {limite:4.2f}: tiles {len(t.pacote.tiles)}/512, "
                  f"aproximados {t.pacote.aproximados}, fidelidade {fid:.2f}%")
            if nota_limite is None or fid > nota_limite:
                melhor_limite, nota_limite = limite, fid
        print(f"  LIMITE escolhido: {melhor_limite:.2f}")

        base = Conversao(d["achatador"], d["prim_n"], depara, ln["primary_tileset"], melhor_limite)
        base.deriva_depara_de_tiles()
        peso = base.pesa_paletas(d["usados"])
        altas = sorted(range(NUM_PALS_IN_PRIMARY, NUM_PALS_TOTAL),
                       key=lambda x: -peso.get(x, 0))
        baixas = sorted([x for x in range(NUM_PALS_IN_PRIMARY) if peso.get(x, 0) > 0],
                        key=lambda x: -peso.get(x, 0))
        fixas = list(range(NUM_PALS_IN_PRIMARY, NUM_PALS_TOTAL))
        candidatos = {"fixas": fixas}
        candidatos["uso"] = sorted(peso, key=lambda x: -peso[x])[:7]
        for k in (1, 2, 3):
            if len(baixas) >= k:
                conj = altas[:-k] + baixas[:k]
                candidatos[f"troca{k}"] = sorted(conj)
        candidatos["guloso"] = escolhe_paletas_guloso(base, d["usados"], d["blocos_f"])
        print(f"  peso por paleta da fonte: "
              f"{ {k: peso[k] for k in sorted(peso, key=lambda x: -peso[x])} }")

        # A pontuação é a FIDELIDADE DO PIXEL RENDERIZADO, não a contagem de
        # tiles quantizados. Pontuar pela contagem escolhia, em Floaroma e em
        # Sandgem, o conjunto que salvava muitos tiles de terreno e sacrificava
        # a paleta dos prédios, e a cidade saía com 63% de fidelidade. A
        # afirmação que interessa é "a cópia parece a fonte", então a verificação
        # tem de ser feita nessa camada: renderiza, compara, escolhe.
        melhor = None
        for nome_estrategia, conjunto in candidatos.items():
            cand = Conversao(d["achatador"], d["prim_n"], depara, ln["primary_tileset"],
                             melhor_limite)
            cand.deriva_depara_de_tiles()
            cand.usa_paletas(conjunto)
            b = cand.converte_blocos(d["blocos_f"])
            bd = cand.converte_blocos(d["borda_f"])
            fid = fidelidade_de(cand, b, cand.depara)
            print(f"  paleta '{nome_estrategia}': {cand.paletas_escolhidas}, "
                  f"tiles {len(cand.pacote.tiles)}/512, "
                  f"aproximados {cand.pacote.aproximados}, "
                  f"quantizados {len(cand.quantizados)}, "
                  f"FIDELIDADE {fid:.2f}%")
            nota = (-fid, cand.pacote.aproximados)
            if melhor is None or nota < melhor[0]:
                melhor = (nota, nome_estrategia, cand, b, bd, fid)
        _, estrategia, conv, novos, nova_borda, fidelidade = melhor
        print(f"  ESCOLHIDA: '{estrategia}' {conv.paletas_escolhidas}, "
              f"fidelidade {fidelidade:.2f}%")
        print(f"  metatiles novos no secundário: {len(conv.metatiles_novos)} de {NUM_METATILES_IN_PRIMARY}")
        print(f"  tiles no secundário novo:      {len(conv.pacote.tiles)} de {NUM_TILES_IN_PRIMARY}")
        print(f"  paletas no secundário novo:    {len(conv.pacote.paletas)} de 7")
        print(f"  palavras de tile resolvidas: nosso primário {conv.tiles_do_nosso_primario}, "
              f"secundário {conv.tiles_do_secundario}, compostas {conv.tiles_compostos}")
        if conv.quantizados:
            pior = max(e for _, e in conv.quantizados)
            print(f"  QUANTIZADOS: {len(conv.quantizados)} tiles sem paleta exata, "
                  f"pior erro quadrático {pior}")
        else:
            print("  quantizados: nenhum (toda composição achou paleta exata)")
        if conv.sem_saida:
            print(f"  SEM SAÍDA: {len(conv.sem_saida)} casos, primeiros: {conv.sem_saida[:4]}")
        if conv.pacote.estouros:
            print(f"  ESTOUROS: {len(conv.pacote.estouros)} - {conv.pacote.estouros[:3]}")
        d["conversao"] = conv
        d["blocos_convertidos"] = novos
        d["borda_convertida"] = nova_borda

    if args.aplicar and d.get("par") is not None:
        par = d["par"]
        if par.recusas or par.sem_slot or par.sem_metatile:
            print("  NÃO APLICO: a costura ou o orçamento não fecharam.")
            return 1
        ok, falhas, _ = prova_da_costura(par)
        if falhas:
            print(f"  NÃO APLICO: {falhas} índices pinados não batem (furo de costura).")
            return 1
        base = args.simbolo or (args.cidade + "SinnohRP")
        sp, ss = base + "Prim", base + "Sec"
        pasta_p = f"data/tilesets/primary/{re.sub(r'(?<!^)(?=[A-Z])', '_', sp).lower()}"
        pasta_s = f"data/tilesets/secondary/{re.sub(r'(?<!^)(?=[A-Z])', '_', ss).lower()}"
        escreve_par(os.path.join(RAIZ, pasta_p), par.prim_tiles,
                    par.paletas[:NUM_PALS_IN_PRIMARY], 0,
                    par.prim_metatiles, par.prim_attrs)
        escreve_par(os.path.join(RAIZ, pasta_s), par.sec_tiles,
                    par.paletas[NUM_PALS_IN_PRIMARY:], NUM_PALS_IN_PRIMARY,
                    par.sec_metatiles, par.sec_attrs)
        tocados = registra_tileset_par(sp, pasta_p, len(par.prim_tiles), False,
                                       "NULL" if par.sem_anim
                                       else "InitTilesetAnim_General")
        tocados += registra_tileset_par(ss, pasta_s, len(par.sec_tiles), True, "NULL")
        pasta_blocos = os.path.dirname(
            os.path.join(RAIZ, ln["blockdata_filepath"].lstrip("./")))
        escreve_blocos(os.path.join(pasta_blocos, "map.bin"), par.blocos_novos)
        escreve_blocos(os.path.join(pasta_blocos, "border.bin"), par.borda_nova)
        religa_layout_par(ln["name"], sp, ss, lf["width"], lf["height"])
        print(f"  APLICADO o PAR: {pasta_p} ({len(par.prim_tiles)} tiles) e "
              f"{pasta_s} ({len(par.sec_tiles)} tiles); layout {ln['name']} agora "
              f"{lf['width']}x{lf['height']}, mapLayoutId intacto")
        print(f"  arquivos de registro tocados: "
              f"{', '.join(sorted({os.path.basename(t) for t in tocados}))}")
        print("  FALTA O JOGO: warps, NPCs, placas e conexões continuam nas "
              "coordenadas antigas. Rode o dossiê da cidade antes de olhar o emulador.")
    elif args.aplicar:
        conv = d.get("conversao")
        if conv is None:
            print("  --aplicar exige --converte (e um --depara que feche o orçamento)")
            return 1
        if conv.sem_saida:
            print("  NÃO APLICO: a conversão estourou o orçamento. "
                  "Conserte o de-para antes.")
            return 1
        simbolo = args.simbolo or (args.cidade + "SinnohRP")
        nome_pasta = re.sub(r"(?<!^)(?=[A-Z])", "_", simbolo).lower()
        pasta_rel = f"data/tilesets/secondary/{nome_pasta}"
        destino = os.path.join(RAIZ, pasta_rel)
        os.makedirs(destino, exist_ok=True)
        escreve_tileset(destino, conv.pacote, conv.metatiles_novos, conv.attrs_novos)
        tocados = registra_tileset(simbolo, pasta_rel, len(conv.pacote.tiles))
        pasta_blocos = os.path.dirname(
            os.path.join(RAIZ, ln["blockdata_filepath"].lstrip("./")))
        escreve_blocos(os.path.join(pasta_blocos, "map.bin"), d["blocos_convertidos"])
        escreve_blocos(os.path.join(pasta_blocos, "border.bin"), d["borda_convertida"])
        religa_layout(ln["name"], simbolo, lf["width"], lf["height"])
        print(f"  APLICADO: {pasta_rel} ({len(conv.pacote.tiles)} tiles, "
              f"{len(conv.metatiles_novos)} metatiles), layout {ln['name']} agora "
              f"{lf['width']}x{lf['height']} com gTileset_{simbolo}")
        print(f"  arquivos de registro tocados: {', '.join(os.path.basename(t) for t in tocados)}")
        print("  FALTA O JOGO: warps, NPCs, placas e conexões continuam nas "
              "coordenadas antigas. Rode o dossiê da cidade antes de olhar o emulador.")

    if args.render:
        os.makedirs(args.render, exist_ok=True)
        a = render_mapa(d["blocos_n"], ln["width"], ln["height"], d["prim_n"], d["sec_n"],
                        TILES_POR_METATILE_NOSSO, TILES_POR_METATILE_NOSSO, args.escala)
        a.save(os.path.join(args.render, f"{args.cidade}-nosso.png"))
        objs = objetos_da_fonte(args.fonte, args.cidade) if args.prova_fonte else None
        b = render_mapa(d["blocos_f"], lf["width"], lf["height"], d["prim_f"], d["sec_f"],
                        TILES_POR_METATILE_FONTE, TILES_POR_METATILE_FONTE, args.escala,
                        objetos=objs, achatador=d["achatador"])
        caminho_fonte = os.path.join(args.render, f"{args.cidade}-fonte.png")
        b.save(caminho_fonte)
        copia = None
        if d.get("par") is not None:
            par = d["par"]
            copia = (par.blocos_novos, par.tileset_primario(), par.tileset_secundario())
        elif d.get("conversao") is not None:
            conv = d["conversao"]
            copia = (d["blocos_convertidos"], d["prim_n"],
                     TilesetEmMemoria(conv.pacote, conv.metatiles_novos, conv.attrs_novos))
        if copia is not None:
            blocos_copia, prim_copia, sec_copia = copia
            c = render_mapa(blocos_copia, lf["width"], lf["height"],
                            prim_copia, sec_copia,
                            TILES_POR_METATILE_NOSSO, TILES_POR_METATILE_NOSSO, args.escala)
            c.save(os.path.join(args.render, f"{args.cidade}-copia.png"))
            print(f"  render da CÓPIA: {args.render}/{args.cidade}-copia.png")
            # Duas contas, e a que manda é a primeira. INTERIOR é a região que
            # nenhuma rota vizinha desenha (janela de ANEL_COSTURA tiles): lá a
            # arte tem de ser DELES. ANEL é o contorno, que é NOSSO de propósito
            # por causa da costura, e por isso é reportado à parte em vez de
            # entrar na nota. A conta antiga descontava "célula que o de-para
            # trocou", e isso era fraudável: trocar mais aumentava a nota.
            fonte_px = b.load()
            copia_px = c.load()
            cont = {"interior": [0, 0], "anel": [0, 0]}
            for cy in range(lf["height"]):
                for cx in range(lf["width"]):
                    zona = zona_da_celula(cx, cy, lf["width"], lf["height"], lados)
                    mx, my = cx * 16, cy * 16
                    for y in range(my, my + 16):
                        for x in range(mx, mx + 16):
                            cont[zona][0 if fonte_px[x, y] == copia_px[x, y] else 1] += 1
            for zona in ("interior", "anel"):
                ig, di = cont[zona]
                if ig + di:
                    print(f"  FIDELIDADE {zona:8s}: {100.0 * ig / (ig + di):6.2f}% "
                          f"({di} pixels diferentes de {ig + di})")
            print("  a nota que vale é a do INTERIOR; o anel de 8 tiles é a nossa "
                  "arte de costura e difere de propósito")
        print(f"  render: {args.render}/{args.cidade}-nosso.png e -fonte.png")
        if args.prova_fonte:
            pasta_ref = os.path.join(os.path.dirname(args.fonte.rstrip("/")), "render")
            igual, detalhe = prova_contra_render_de_referencia(args.cidade, caminho_fonte, pasta_ref)
            marca = "ok " if igual else "RUIM"
            print(f"  [{marca}] prova do leitor de 3 camadas contra o render da fonte: {detalhe}")
            if not igual:
                return 1
    return 0




# ============================================================== par próprio ===
#
# O modo `--par-proprio` dá a CADA cidade um par de tilesets só dela: primário
# NOVO e secundário NOVO. O orçamento passa de 7 paletas / 512 slots de tile
# (que é o que sobra quando a cidade usa o nosso `gTileset_GeneralSinnoh`) para
# 13 paletas, 944 slots de tile (1024 menos os 80 da animação) e 1024 metatiles.
# Com isso o INTERIOR da cidade deixa de precisar do de-para: a arte de lá passa
# a ser a deles, copiada.
#
# O preço é a COSTURA. O motor desenha o mapa conectado com os tilesets do mapa
# ATUAL, e a janela é de ANEL_COSTURA tiles nos dois sentidos. Então um conjunto
# de índices de metatile tem de ser PINADO no par novo: mesmo NÚMERO de índice,
# mesma IMAGEM de hoje, mesmo `behavior` e mesmo `layerType`. É o índice pinado
# que amarra os dois lados.
#
# E a FAIXA DE VRAM DA ANIMAÇÃO: `InitTilesetAnim_General` reescreve todo quadro
# os slots 432 a 511 do primário (água 432-461, borda de areia 464-473, borda de
# terra 480-489, cachoeira 496-501, flor 508-511). O primário novo reserva esses
# 80 slots com uma cópia byte a byte dos nossos e mantém o mesmo callback; arte
# deles NUNCA entra ali. Como os bytes do tile animado são ÍNDICES de cor fixos,
# a paleta que um metatile usa para desenhar um tile dessa faixa também tem de
# entrar no par novo VERBATIM, com as cores nas mesmas posições.

FAIXA_ANIM_INICIO = 432
FAIXA_ANIM_FIM = 512
MAX_CORES_POR_PALETA = 15   # o índice 0 é sempre transparente


def dist_cor(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2


# Famílias de CHÃO. A resposta 92 do condutor Fable manda que, no anel, o
# substituto seja "o chão coerente com o que o autor desenhou ao lado: grama com
# grama, terra com terra, água com água". A família é o guarda-corpo grosso dessa
# frase: ela impede a troca de assunto (areia de praia virando gelo, calçada
# virando água) quando a busca por imagem sai do vocabulário da rota. Dentro da
# mesma família quem decide é o PIXEL, não a função, porque foi o casamento por
# função que pôs rua de tábua na entrada sul de Sandgem.
def familia_do_bloco(pix):
    n = len(pix) or 1
    r = sum(p[0] for p in pix) / n
    g = sum(p[1] for p in pix) / n
    b = sum(p[2] for p in pix) / n
    # A ordem importa, e cada linha tem um caso real atrás dela. Não existe
    # família "outro": areia de praia caindo fora das famílias foi o que pôs
    # mourão de cerca branco espalhado na praia ao sul de Sandgem.
    #
    # O caso difícil é o bloco QUASE NEUTRO e claro: areia de praia e neve têm a
    # mesma cor média e saturação quase zero. O que separa as duas é a
    # TEMPERATURA (a areia puxa para o vermelho, a neve para o azul), e é essa a
    # primeira pergunta. Sem ela, a praia ao sul de Sandgem virava gelo.
    mx, mn = max(r, g, b), min(r, g, b)
    sat = mx - mn
    if sat <= 30:
        return "quente" if r > b + 6 else "cinza"
    if b == mx and b - max(r, g) > 12:
        return "agua"
    if g == mx and g - mn > 15:
        return "verde"
    if r >= g and r > b:
        return "quente"        # terra, areia, madeira, telhado, pedra quente
    return "cinza"             # concreto, pedra fria, neve, gelo, metal


def desenha_metatile(prim, sec, idx, tpm, fundo=(0, 0, 0)):
    """256 pixels RGB de um metatile, empilhando as camadas na ordem do motor."""
    if idx < NUM_METATILES_IN_PRIMARY:
        ts, local = prim, idx
    else:
        ts, local = sec, idx - NUM_METATILES_IN_PRIMARY
    if local >= len(ts.metatiles):
        return [MAGENTA] * 256
    m = ts.metatiles[local]
    bloco = [fundo] * 256
    for camada in range(tpm // 4):
        for c in range(4):
            entrada = m[camada * 4 + c]
            if (entrada & 0x3FF) == 0:
                continue
            tiles, paletas, e = resolve(entrada, prim, sec)
            if (e & 0x3FF) >= len(tiles):
                continue
            pix = pinta_tile(tiles, paletas, e, transparente=None)
            ox, oy = (c % 2) * 8, (c // 2) * 8
            for y in range(8):
                for x in range(8):
                    p = pix[y * 8 + x]
                    if p is not None:
                        bloco[(oy + y) * 16 + (ox + x)] = p
    return bloco


def atributo_de(prim, sec, idx):
    if idx < NUM_METATILES_IN_PRIMARY:
        ts, local = prim, idx
    else:
        ts, local = sec, idx - NUM_METATILES_IN_PRIMARY
    return ts.attrs[local] if local < len(ts.attrs) else 0


class TilesetMontado:
    """Um tileset construído em memória, com a mesma cara de `Tileset`."""

    def __init__(self, tiles, paletas, metatiles, attrs, rotulo):
        self.tiles = [bytes(t) for t in tiles]
        self.paletas = [list(p) for p in paletas]
        while len(self.paletas) < 16:
            self.paletas.append([(0, 0, 0)] * 16)
        self.metatiles = [tuple(m) for m in metatiles]
        self.attrs = list(attrs)
        self.rotulo = rotulo

    def __repr__(self):
        return (f"<{self.rotulo} {len(self.tiles)} tiles, {len(self.metatiles)} metatiles>")


# ------------------------------------------------------- conjunto pinado ------

def indice_de_mapas():
    """MAP_ROUTE201 -> (pasta, map.json) de todos os mapas NOSSOS."""
    idx = {}
    base = os.path.join(RAIZ, "data", "maps")
    for nome in sorted(os.listdir(base)):
        caminho = os.path.join(base, nome, "map.json")
        if not os.path.exists(caminho):
            continue
        with open(caminho, encoding="utf-8") as f:
            mj = json.load(f)
        if mj.get("id"):
            idx[mj["id"]] = (nome, mj)
    return idx


def conjunto_pinado(nome_mapa_nosso, lados):
    """Os índices de metatile que a costura obriga a manter iguais.

    União de duas coisas, e nenhuma das duas é opcional:

      * o que a ROTA vizinha desenha e a CIDADE pinta: a faixa de
        ANEL_COSTURA tiles do lado da rota que encosta na cidade, mais o
        `border.bin` dela (parado na cidade, esses metatiles da rota são
        desenhados com os tilesets da CIDADE);
      * o que a CIDADE mostra e a ROTA pinta: a faixa de ANEL_COSTURA tiles de
        cada borda CONECTADA da nossa cidade de hoje (parado na rota, essa faixa
        da cidade é desenhada com os tilesets da ROTA).

    Lado SEM conexão não entra: ninguém desenha aquilo de fora.
    """
    mapas = indice_de_mapas()
    layouts = {l["id"]: l for l in le_layouts(
        os.path.join(RAIZ, "data/layouts/layouts.json"))["layouts"]}
    if nome_mapa_nosso not in [n for n, _ in mapas.values()]:
        pass
    mj = None
    for nome, dados in mapas.values():
        if nome == nome_mapa_nosso:
            mj = dados
            break
    if mj is None:
        raise SystemExit(f"mapa {nome_mapa_nosso} não achado")

    def blocos_do_layout(lid):
        lay = layouts[lid]
        return (lay,
                le_blocos(os.path.join(RAIZ, lay["blockdata_filepath"].lstrip("./"))),
                le_blocos(os.path.join(RAIZ, lay["border_filepath"].lstrip("./"))))

    pinados = set()
    detalhe = {"rota": set(), "anel": set()}
    for c in (mj.get("connections") or []):
        d = c.get("direction")
        if d not in ("up", "down", "left", "right"):
            continue
        if c["map"] not in mapas:
            continue
        _, vmj = mapas[c["map"]]
        lay, bl, bd = blocos_do_layout(vmj["layout"])
        W, H = lay["width"], lay["height"]
        for y in range(H):
            for x in range(W):
                encosta = ((d == "up" and y >= H - ANEL_COSTURA)
                           or (d == "down" and y < ANEL_COSTURA)
                           or (d == "left" and x >= W - ANEL_COSTURA)
                           or (d == "right" and x < ANEL_COSTURA))
                if encosta:
                    detalhe["rota"].add(bl[y * W + x] & 0x3FF)
        for p in bd:
            detalhe["rota"].add(p & 0x3FF)

    lay, bl, bd = blocos_do_layout(mj["layout"])
    W, H = lay["width"], lay["height"]
    for y in range(H):
        for x in range(W):
            if zona_da_celula(x, y, W, H, lados) == "anel":
                detalhe["anel"].add(bl[y * W + x] & 0x3FF)

    pinados = detalhe["rota"] | detalhe["anel"]
    return pinados, detalhe


# -------------------------------------------------------------- o par ---------

class ParDeTilesets:
    """Primário novo + secundário novo de UMA cidade."""

    def __init__(self, achatador, prim_n, sec_n, depara, lados, lf,
                 blocos_f, borda_f, pinados, limite=0.60, vocabulario=None,
                 tabela_anel=None, sem_anim=False):
        self.a = achatador              # fonte, três camadas
        self.prim_n = prim_n            # gTileset_GeneralSinnoh
        self.sec_n = sec_n              # secundário de HOJE da nossa cidade
        self.depara = Conversao.limpa_fracos(depara or {}, limite)
        self.lados = lados
        self.lf = lf
        self.blocos_f = blocos_f
        self.borda_f = borda_f
        self.pinados = set(pinados)
        # VOCABULÁRIO do anel: os metatiles do nosso primário que a rota vizinha e
        # a borda da nossa cidade de hoje já usam. Quando o de-para não cobre um
        # metatile do anel, o substituto sai daqui, e não dos 512 do primário
        # inteiro. Escolher entre os 512 pelo pixel mais próximo punha ponte, água
        # e escada de tijolo na borda de Jubilife, porque a única coisa parecida
        # com concreto azulado no general_sinnoh é justamente isso. Restringir ao
        # que a rota já desenha ao lado dá mata, grama, cerca e caminho, que é o
        # que costura de verdade, e ainda não pina índice novo nenhum.
        self.vocabulario = set(vocabulario or [])
        self.tabela_anel = dict(tabela_anel or {})
        # Teto de slot de tile do primário novo. Com animação, os 80 slots de
        # 432 a 511 são reservados para `InitTilesetAnim_General` reescrever
        # todo quadro; sem ela (`--sem-animacao`, só para cidade que hoje NÃO
        # anima célula nenhuma), os 80 slots voltam a ser arte e o `.callback`
        # do primário vira NULL. Medido em 11/09/2026: Jubilife e Oreburgh têm
        # 0 células animadas hoje, Twinleaf 11, Sandgem 4, Floaroma 48.
        self.sem_anim = bool(sem_anim)
        self.teto_prim = NUM_TILES_IN_PRIMARY if self.sem_anim else FAIXA_ANIM_INICIO
        self.equiv_anel = {}
        self.avisos = []
        self.recusas = []               # índice pinado sem paleta exata
        self.quantizados = []           # (peso, erro quadrático)
        self.fusoes_exatas = 0
        self.fusoes_aprox = 0

    # --- anel -------------------------------------------------------------
    def pixels_da_fonte(self, mid):
        return self.a.desenha(mid)

    def comportamento_da_fonte(self, mid):
        return self.a.atributo(mid) & 0x00FF

    def mapeia_anel(self):
        """Diz qual metatile NOSSO cada metatile deles vira dentro do anel.

        O anel é a faixa que a ROTA vizinha desenha com os tilesets DELA. Logo o
        índice ali tem de existir no nosso primário compartilhado
        (`general_sinnoh`): arte do secundário da cidade não serve, porque a rota
        desenharia o secundário dela naquele número e sairia lixo.

        A ordem de escolha, depois da resposta 92 do condutor Fable (11/09/2026):

        1. **Tabela julgada por gente** (`anel_sinnoh_retro.json`), quando a
           cidade tem uma linha para aquele metatile. É o único lugar em que
           alguém decide na mão, e ela existe justamente para os casos em que
           nenhuma conta acerta.
        2. **Imagem, dentro do vocabulário da costura** (o que a rota vizinha e a
           borda da nossa cidade de hoje já desenham), com o MESMO comportamento e
           a MESMA família de chão.
        3. **Imagem, entre os 512 do primário**, ainda com o mesmo comportamento e
           a mesma família, e só quando o passo 2 ficou longe demais
           (`LIMITE_ANEL_LONGE`). É o que devolve areia de praia para Floaroma e
           para Oreburgh sem soltar a busca no primário inteiro.
        4. **Imagem, dentro do vocabulário**, sem o guarda de família, que é o
           último recurso.

        O de-para NÃO entra mais aqui. Ele casa por FUNÇÃO, e foi ele que pôs a
        rua de tábua na entrada sul de Sandgem e de Floaroma (os metatiles 24, 25
        e 26 da fonte, terra batida, casados com os nossos 331, 289 e 333, tábua e
        pedrisco). No interior o de-para já não era usado desde o par próprio; no
        anel ele sai agora. Continua valendo no arquivo como registro do
        casamento por função, que é o que a seção 4 do caderno descreve.
        """
        W, H = self.lf["width"], self.lf["height"]
        mids = set()
        for cy in range(H):
            for cx in range(W):
                if zona_da_celula(cx, cy, W, H, self.lados) == "anel":
                    mids.add(self.blocos_f[cy * W + cx] & 0x3FF)
        self.mids_anel = mids
        nossos = [desenha_metatile(self.prim_n, self.sec_n, i,
                                   TILES_POR_METATILE_NOSSO, fundo=(0, 0, 0))
                  for i in range(len(self.prim_n.metatiles))]
        comp_nosso = [atributo_de(self.prim_n, self.sec_n, i) & 0x00FF
                      for i in range(len(self.prim_n.metatiles))]
        fam_nosso = [familia_do_bloco(px) for px in nossos]
        vocab = sorted(i for i in self.vocabulario if i < len(nossos))
        if not vocab:
            vocab = list(range(len(nossos)))
        todos = list(range(len(nossos)))

        def perto(cands, alvo):
            return min(cands, key=lambda i: sum(dist_cor(a, b)
                                                for a, b in zip(nossos[i], alvo)))

        def erro(i, alvo):
            return sum(dist_cor(a, b) for a, b in zip(nossos[i], alvo))

        self.anel_origem = {}
        for mid in sorted(mids):
            forcado = self.tabela_anel.get(str(mid))
            if forcado is not None:
                self.equiv_anel[mid] = int(forcado)
                self.anel_origem[mid] = "tabela"
                continue
            alvo = self.pixels_da_fonte(mid)
            comp = self.comportamento_da_fonte(mid)
            fam = familia_do_bloco(alvo)
            mesmo_comp_v = [i for i in vocab if comp_nosso[i] == comp]
            mesma_fam_v = [i for i in mesmo_comp_v if fam_nosso[i] == fam]
            if mesma_fam_v:
                escolha = perto(mesma_fam_v, alvo)
                origem = "vocab"
                if erro(escolha, alvo) > LIMITE_ANEL_LONGE:
                    largo = [i for i in todos
                             if comp_nosso[i] == comp and fam_nosso[i] == fam]
                    if largo:
                        cand = perto(largo, alvo)
                        if erro(cand, alvo) < erro(escolha, alvo):
                            escolha, origem = cand, "primário"
            else:
                largo = [i for i in todos
                         if comp_nosso[i] == comp and fam_nosso[i] == fam]
                if largo:
                    escolha, origem = perto(largo, alvo), "primário"
                elif mesmo_comp_v:
                    escolha, origem = perto(mesmo_comp_v, alvo), "vocab-sem-família"
                else:
                    escolha, origem = perto(vocab, alvo), "vocab-sem-nada"
            self.equiv_anel[mid] = escolha
            self.anel_origem[mid] = origem
        self.pinados |= set(self.equiv_anel.values())
        from collections import Counter
        self.anel_contagem = Counter(self.anel_origem.values())
        return sum(1 for v in self.anel_origem.values() if v.startswith("vocab-sem"))

    # --- coleta -----------------------------------------------------------
    def coleta(self):
        """Junta todo bloco de 8x8 que o par novo vai precisar desenhar."""
        self.blocos = {}          # pixels -> info
        self.pin_palavras = {}    # índice pinado -> 8 palavras (dicionário ou None)

        def anota(pix, pinado, peso, anim=None, palvb=None, origem=None):
            # A CHAVE inclui a faixa de animação de propósito. Um tile de arte
            # deles com os mesmos pixels de um tile animado NÃO pode aliasar para
            # o slot animado: o callback reescreve aquele slot todo quadro e a
            # arte sumiria da tela sem aparecer em contador nenhum.
            chave = (pix, anim)
            info = self.blocos.get(chave)
            if info is None:
                info = {"pix": pix, "pinado": False, "peso": 0,
                        "anim": anim, "palvb": palvb, "origem": origem}
                self.blocos[chave] = info
            info["pinado"] = info["pinado"] or pinado
            info["peso"] += peso
            return chave

        for p in sorted(self.pinados):
            if p < NUM_METATILES_IN_PRIMARY:
                ts, local = self.prim_n, p
            else:
                ts, local = self.sec_n, p - NUM_METATILES_IN_PRIMARY
            if local >= len(ts.metatiles):
                self.avisos.append(f"índice pinado {p} não existe no par de hoje")
                self.pin_palavras[p] = None
                continue
            palavras = []
            for w in ts.metatiles[local]:
                idx = w & 0x3FF
                if idx == 0:
                    palavras.append(None)
                    continue
                tiles, paletas, e = resolve(w, self.prim_n, self.sec_n)
                if (e & 0x3FF) >= len(tiles):
                    palavras.append(None)
                    continue
                pix = tuple(pinta_tile(tiles, paletas, e & ~0xC00, transparente=None))
                anim = idx if FAIXA_ANIM_INICIO <= idx < FAIXA_ANIM_FIM else None
                palvb = list(paletas[(w >> 12) & 0xF]) if anim is not None else None
                chave = anota(pix, True, 1000, anim, palvb,
                              origem=("n", (w >> 12) & 0xF))
                palavras.append({"chave": chave, "flips": w & 0xC00})
            self.pin_palavras[p] = palavras

        W, H = self.lf["width"], self.lf["height"]
        uso = {}
        self.mid_interior = set()
        for cy in range(H):
            for cx in range(W):
                mid = self.blocos_f[cy * W + cx] & 0x3FF
                if zona_da_celula(cx, cy, W, H, self.lados) == "interior":
                    self.mid_interior.add(mid)
                    uso[mid] = uso.get(mid, 0) + 1
        for p in self.borda_f:
            mid = p & 0x3FF
            self.mid_interior.add(mid)
            uso[mid] = uso.get(mid, 0) + 1

        self.arte = {}
        for mid in sorted(self.mid_interior):
            m_fonte, attr_fonte, parte = self.a.metatile(mid)
            if m_fonte is None:
                self.arte[mid] = None
                continue
            baixo, cima, tipo, _ = self.a.achata(m_fonte, parte)
            palavras = []
            for entrada in list(baixo) + list(cima):
                if isinstance(entrada, tuple) and entrada and entrada[0] == "COMPOSTO":
                    pix = tuple(self.a.compostos[entrada[1]])
                    chave = anota(pix, False, uso.get(mid, 1), origem=None)
                    palavras.append({"chave": chave, "flips": 0})
                elif (entrada & 0x3FF) == 0:
                    palavras.append(None)
                else:
                    pix = tuple(self.a.pixels(entrada & ~0xC00, parte))
                    chave = anota(pix, False, uso.get(mid, 1),
                                  origem=("f", (entrada >> 12) & 0xF))
                    palavras.append({"chave": chave, "flips": entrada & 0xC00})
            self.arte[mid] = (palavras, tipo, attr_fonte & 0x00FF)
        self.uso = uso

    # --- paletas ----------------------------------------------------------
    def empacota_paletas(self, estrategia="cor"):
        """Põe as cores de todo mundo em 13 paletas de 15 cores.

        Três regras duras:
          1. cor de bloco PINADO é EXATA, nunca quantizada. Se não couber, a
             ferramenta RECUSA e diz quantas cores faltaram, porque a costura
             não fecha sem isso;
          2. a paleta de um tile da faixa de animação entra VERBATIM (as 16
             entradas na mesma ordem), porque os bytes que o callback escreve em
             VRAM todo quadro são índices de cor fixos;
          3. a arte deles pode quantizar, e cada bloco quantizado sai no
             relatório com o erro quadrático, nunca calado.

        O empacotamento é AGLOMERATIVO, e não guloso de primeira-que-couber: os
        conjuntos de cor começam um por balde e são fundidos aos pares pelo MENOR
        tamanho de união, com desempate pela maior interseção, até sobrarem 13. É
        a diferença entre aproveitar cor repetida entre dois tiles e desperdiçar
        vaga: o guloso deixava 61 blocos de Twinleaf na quantização. Só quando não
        existe mais nenhuma fusão EXATA possível é que entra a fusão APROXIMADA, e
        ela nunca desmancha um balde que tem cor de costura dentro.
        """
        import heapq

        self.paletas, self.fixas, self.cores_bin = [], [], []
        vistas = []
        for _, info in self.blocos.items():
            if info["anim"] is None:
                continue
            k = tuple(info["palvb"])
            if k not in vistas:
                vistas.append(k)
        for v in vistas:
            self.paletas.append(list(v))
            self.fixas.append(True)
            self.cores_bin.append({c for c in v[1:]})
        self.n_verbatim = len(vistas)

        def cores_de(pix):
            return frozenset(p for p in pix if p is not None)

        # Duas SEMENTES, e nenhuma das duas ganha sempre:
        #   "cor"    começa com um balde por conjunto de cor distinto. Empacota
        #            mais apertado, mas pode quebrar a paleta de um prédio ao
        #            meio quando o orçamento fecha;
        #   "paleta" começa com um balde por PALETA DE ORIGEM (as 13 deles para a
        #            arte, as nossas para a costura). Nasce com a arte inteira
        #            exata por construção, porque toda cor de um tile já cabia na
        #            paleta com que o autor o pintou, e só as composições de três
        #            camadas ficam soltas.
        # A ferramenta roda as duas e fica com a que quantiza menos, ponderado
        # pelo uso no mapa.
        baldes = {}
        if estrategia == "paleta":
            por_origem = {}
            for _, info in self.blocos.items():
                if info["anim"] is not None:
                    continue
                ch = info.get("origem")
                if ch is None:
                    ch = ("solto", cores_de(info["pix"]))
                b = por_origem.setdefault(ch, {"cores": set(), "pinado": False, "peso": 0})
                b["cores"] |= cores_de(info["pix"])
                b["pinado"] = b["pinado"] or info["pinado"]
                b["peso"] += info["peso"]
            for b in por_origem.values():
                c = frozenset(b["cores"])
                if len(c) > MAX_CORES_POR_PALETA:
                    continue
                d = baldes.setdefault(c, {"pinado": False, "peso": 0})
                d["pinado"] = d["pinado"] or b["pinado"]
                d["peso"] += b["peso"]
        else:
            for _, info in self.blocos.items():
                if info["anim"] is not None:
                    continue
                c = cores_de(info["pix"])
                b = baldes.setdefault(c, {"pinado": False, "peso": 0})
                b["pinado"] = b["pinado"] or info["pinado"]
                b["peso"] += info["peso"]

        restos = {c: b for c, b in baldes.items()
                  if not any(self.fixas[i] and c <= self.cores_bin[i]
                             for i in range(len(self.fixas)))}
        self.cores_totais = len(set().union(*restos)) if restos else 0
        self.baldes_iniciais = len(restos)

        grupos = [set(c) for c in restos]
        meta = [dict(b) for b in restos.values()]
        vivo = [True] * len(grupos)
        vivos = len(grupos)
        alvo = NUM_PALS_TOTAL - self.n_verbatim

        h = []
        for i in range(len(grupos)):
            for j in range(i + 1, len(grupos)):
                u = len(grupos[i] | grupos[j])
                if u <= MAX_CORES_POR_PALETA:
                    heapq.heappush(h, (u, -len(grupos[i] & grupos[j]), i, j))
        while vivos > alvo and h:
            u, _, i, j = heapq.heappop(h)
            if not vivo[i] or not vivo[j]:
                continue
            uni = grupos[i] | grupos[j]
            if len(uni) > MAX_CORES_POR_PALETA:
                continue
            if len(uni) != u:
                heapq.heappush(h, (len(uni), -len(grupos[i] & grupos[j]), i, j))
                continue
            grupos[i] = uni
            meta[i]["pinado"] = meta[i]["pinado"] or meta[j]["pinado"]
            meta[i]["peso"] += meta[j]["peso"]
            vivo[j] = False
            vivos -= 1
            self.fusoes_exatas += 1
            for k in range(len(grupos)):
                if k == i or not vivo[k]:
                    continue
                nu = len(grupos[i] | grupos[k])
                if nu <= MAX_CORES_POR_PALETA:
                    heapq.heappush(h, (nu, -len(grupos[i] & grupos[k]),
                                       min(i, k), max(i, k)))

        # Fusão APROXIMADA: só entra quando não existe mais nenhuma fusão exata, e
        # só desmancha balde SEM cor de costura dentro. Dissolver não joga a cor
        # fora: o que ainda couber no balde de destino ENTRA, e só o que sobrar é
        # que vai ser aproximado na hora de codificar. Jogar o balde inteiro fora
        # custava centenas de tiles quantizados por uma fusão só.
        self.pior_fusao = 0
        while vivos > alvo:
            cand = [i for i in range(len(grupos)) if vivo[i] and not meta[i]["pinado"]]
            if not cand:
                break
            melhor = None
            for i in cand:
                for j in range(len(grupos)):
                    if j == i or not vivo[j]:
                        continue
                    fora = grupos[i] - grupos[j]
                    erro = max((min(dist_cor(c, q) for q in grupos[j]) for c in fora),
                               default=0)
                    custo = erro * max(1, meta[i]["peso"])
                    if melhor is None or custo < melhor[0]:
                        melhor = (custo, i, j, erro)
            if melhor is None:
                break
            _, i, j, erro = melhor
            for c in sorted(grupos[i] - grupos[j]):
                if len(grupos[j]) < MAX_CORES_POR_PALETA:
                    grupos[j].add(c)
            meta[j]["peso"] += meta[i]["peso"]
            vivo[i] = False
            vivos -= 1
            self.fusoes_aprox += 1
            self.pior_fusao = max(self.pior_fusao, erro)

        self.mapa_bin = []
        for i in range(len(grupos)):
            if vivo[i]:
                self.paletas.append(None)
                self.fixas.append(False)
                self.cores_bin.append(set(grupos[i]))
        while len(self.paletas) < NUM_PALS_TOTAL:
            self.paletas.append(None)
            self.fixas.append(False)
            self.cores_bin.append(set())

        # Atribuição com EXPANSÃO. Um balde pode ter fechado com 10 cores, e um
        # bloco que precisa de 3 cores a mais cabe ali sem estourar as 15. A
        # versão que só procurava superconjunto exato mandava esse bloco para a
        # quantização com vaga de cor sobrando na paleta, e era assim que 200
        # blocos de Jubilife saíam aproximados.
        self.pal_do_bloco = {}
        ordem = sorted(self.blocos.items(),
                       key=lambda kv: (0 if kv[1]["pinado"] else 1, -kv[1]["peso"]))
        for chave, info in ordem:
            if info["anim"] is not None:
                self.pal_do_bloco[chave] = vistas.index(tuple(info["palvb"]))
                continue
            cores = cores_de(info["pix"])
            alvo_pal = None
            for i in range(len(self.paletas)):
                if cores <= self.cores_bin[i]:
                    alvo_pal = i
                    break
            if alvo_pal is None:
                cabe = None
                for i in range(len(self.paletas)):
                    if self.fixas[i]:
                        continue
                    u = self.cores_bin[i] | cores
                    if len(u) <= MAX_CORES_POR_PALETA:
                        custo = len(u) - len(self.cores_bin[i])
                        if cabe is None or custo < cabe[0]:
                            cabe = (custo, i)
                if cabe is not None:
                    alvo_pal = cabe[1]
                    self.cores_bin[alvo_pal] |= cores
            if alvo_pal is None:
                pior = None
                for i in range(len(self.paletas)):
                    if not self.cores_bin[i]:
                        continue
                    erro = max((min(dist_cor(c, q) for q in self.cores_bin[i])
                                for c in cores), default=0)
                    if pior is None or erro < pior[0]:
                        pior = (erro, i)
                alvo_pal = pior[1] if pior else 0
                if info["pinado"]:
                    faltam = min(len(cores - self.cores_bin[i])
                                 for i in range(len(self.paletas)))
                    self.recusas.append((chave, faltam))
                else:
                    self.quantizados.append((info["peso"], pior[0] if pior else 0))
            self.pal_do_bloco[chave] = alvo_pal

        fundo = self.a.prim.paletas[0][0]
        for i in range(len(self.paletas)):
            if self.fixas[i]:
                # a entrada 0 é sempre transparente e o motor ainda força preto
                # nela no primário: trocá-la não mexe em pixel nenhum
                self.paletas[i] = [fundo] + list(self.paletas[i][1:])
                continue
            cores = sorted(self.cores_bin[i])
            enchimento = cores[0] if cores else (0, 0, 0)
            self.paletas[i] = ([fundo] + cores
                               + [enchimento] * (MAX_CORES_POR_PALETA - len(cores)))

    def codifica(self, pix, pal_i):
        pal = self.paletas[pal_i]
        mapa = {}
        for j in range(15, 0, -1):
            mapa[pal[j]] = j
        saida = []
        for p in pix:
            if p is None:
                saida.append(0)
                continue
            j = mapa.get(p)
            if j is None:
                j = min(range(1, 16), key=lambda k: dist_cor(p, pal[k]))
            saida.append(j)
        return saida

    # --- tiles ------------------------------------------------------------
    def aloca_tiles(self):
        vazio = bytes(64)
        self.prim_tiles = [vazio] * NUM_TILES_IN_PRIMARY
        if not self.sem_anim:
            for i in range(FAIXA_ANIM_INICIO, FAIXA_ANIM_FIM):
                self.prim_tiles[i] = bytes(self.prim_n.tiles[i])
        self.sec_tiles = []
        # O slot 0 fica VAZIO de propósito: em todo o motor, `palavra & 0x3FF == 0`
        # quer dizer "célula sem desenho", e o render pula a camada. Arte alocada
        # no slot 0 some da tela sem aparecer em contador nenhum (foi o que fez a
        # PROVA C acusar 22 furos na primeira rodada de Twinleaf).
        self.livre_prim = 1
        self.pool = {}
        self.indice_do_bloco = {}
        self.sem_slot = []

        ordem = sorted(self.blocos.items(),
                       key=lambda kv: (0 if kv[1]["pinado"] else 1, -kv[1]["peso"]))
        for chave, info in ordem:
            if info["anim"] is not None:
                self.indice_do_bloco[chave] = (info["anim"], 0)
                continue
            indices = self.codifica(info["pix"], self.pal_do_bloco[chave])
            g, bits = self.registra_tile(indices)
            if g is None:
                self.sem_slot.append(info)
                self.indice_do_bloco[chave] = (None, 0)
            else:
                self.indice_do_bloco[chave] = (g, bits)

    def registra_tile(self, indices64):
        base = bytes(indices64)
        for fx, fy, bits in ((False, False, 0), (True, False, 0x400),
                             (False, True, 0x800), (True, True, 0xC00)):
            chave = PacoteSecundario.espelha(base, fx, fy)
            if chave in self.pool:
                return self.pool[chave], bits
        if self.livre_prim < self.teto_prim:
            g = self.livre_prim
            self.prim_tiles[g] = base
            self.livre_prim += 1
        elif len(self.sec_tiles) < NUM_TILES_IN_PRIMARY:
            g = NUM_TILES_IN_PRIMARY + len(self.sec_tiles)
            self.sec_tiles.append(base)
        else:
            return None, 0
        self.pool[base] = g
        return g, 0

    # --- metatiles --------------------------------------------------------
    def palavra(self, w):
        if w is None:
            return 0
        g, flip_extra = self.indice_do_bloco[w["chave"]]
        if g is None:
            return 0
        pal = self.pal_do_bloco[w["chave"]]
        return ((g & 0x3FF) | ((w["flips"] ^ flip_extra) & 0xC00)
                | ((pal & 0xF) << 12))

    def monta_metatiles(self):
        self.prim_metatiles = [[0] * 8 for _ in range(NUM_METATILES_IN_PRIMARY)]
        self.prim_attrs = [0] * NUM_METATILES_IN_PRIMARY
        self.sec_metatiles = [[0] * 8 for _ in range(NUM_METATILES_IN_PRIMARY)]
        self.sec_attrs = [0] * NUM_METATILES_IN_PRIMARY
        ocupado_prim, ocupado_sec = set(), set()

        for p, palavras in self.pin_palavras.items():
            if palavras is None:
                continue
            saida = [self.palavra(w) for w in palavras]
            attr = atributo_de(self.prim_n, self.sec_n, p)
            if p < NUM_METATILES_IN_PRIMARY:
                self.prim_metatiles[p] = saida
                self.prim_attrs[p] = attr
                ocupado_prim.add(p)
            else:
                local = p - NUM_METATILES_IN_PRIMARY
                if local >= NUM_METATILES_IN_PRIMARY:
                    self.avisos.append(f"índice pinado {p} fora dos 1024 metatiles")
                    continue
                self.sec_metatiles[local] = saida
                self.sec_attrs[local] = attr
                ocupado_sec.add(local)

        livres = ([i for i in range(1, NUM_METATILES_IN_PRIMARY) if i not in ocupado_prim]
                  + [NUM_METATILES_IN_PRIMARY + i
                     for i in range(NUM_METATILES_IN_PRIMARY) if i not in ocupado_sec])
        self.mapa_arte = {}
        self.sem_metatile = 0
        self.max_sec = max(ocupado_sec) if ocupado_sec else -1
        for mid in sorted(self.mid_interior):
            dados = self.arte.get(mid)
            if dados is None:
                continue
            palavras, tipo, comportamento = dados
            saida = [self.palavra(w) for w in palavras]
            attr = (comportamento & 0x00FF) | ((tipo & 0xF) << 12)
            if not livres:
                self.sem_metatile += 1
                continue
            i = livres.pop(0)
            if i < NUM_METATILES_IN_PRIMARY:
                self.prim_metatiles[i] = saida
                self.prim_attrs[i] = attr
            else:
                local = i - NUM_METATILES_IN_PRIMARY
                self.sec_metatiles[local] = saida
                self.sec_attrs[local] = attr
                self.max_sec = max(self.max_sec, local)
            self.mapa_arte[mid] = i
        n = self.max_sec + 1
        self.sec_metatiles = self.sec_metatiles[:max(n, 1)]
        self.sec_attrs = self.sec_attrs[:max(n, 1)]

    # --- mapa -------------------------------------------------------------
    def converte_mapa(self):
        W, H = self.lf["width"], self.lf["height"]
        saida = []
        for i, palavra in enumerate(self.blocos_f[:W * H]):
            mid = palavra & 0x3FF
            resto = palavra & ~0x3FF
            cx, cy = i % W, i // W
            if zona_da_celula(cx, cy, W, H, self.lados) == "anel":
                novo = self.equiv_anel.get(mid, 0)
            else:
                novo = self.mapa_arte.get(mid, 0)
            saida.append(novo | resto)
        borda = [self.mapa_arte.get(p & 0x3FF, 0) | (p & ~0x3FF) for p in self.borda_f]
        return saida, borda

    # --- saída ------------------------------------------------------------
    def tileset_primario(self):
        return TilesetMontado(self.prim_tiles, self.paletas[:NUM_PALS_IN_PRIMARY],
                              self.prim_metatiles, self.prim_attrs, "primário novo")

    def tileset_secundario(self):
        paletas = [[(0, 0, 0)] * 16] * NUM_PALS_IN_PRIMARY + self.paletas[NUM_PALS_IN_PRIMARY:]
        return TilesetMontado(self.sec_tiles, paletas,
                              self.sec_metatiles, self.sec_attrs, "secundário novo")

    def constroi(self, estrategia="cor"):
        faltantes = self.mapeia_anel()
        self.coleta()
        self.fecha(estrategia)
        return faltantes

    def fecha(self, estrategia):
        self.recusas, self.quantizados = [], []
        self.fusoes_exatas = self.fusoes_aprox = 0
        self.estrategia = estrategia
        self.empacota_paletas(estrategia)
        self.aloca_tiles()
        self.monta_metatiles()
        self.blocos_novos, self.borda_nova = self.converte_mapa()

    def custo_da_quantizacao(self):
        """Erro de cor ponderado pelo número de células do mapa que o pedem."""
        return sum(max(1, peso) * erro for peso, erro in self.quantizados)


# ------------------------------------------------------------- provas ---------

def prancha_do_anel(par, d, lf, cidade, pasta):
    """A prova do anel: o hack em cima, a cópia embaixo, lado a lado, e a
    contagem de pixel SÓ no anel.

    Igualdade de pixel no anel é sempre perto de zero e não mede nada: a arte ali
    é a NOSSA de propósito (a rota desenha aquela faixa com os tilesets dela). O
    que mede é a DISTÂNCIA de desenho: quanto a nossa moldura se afasta, cor a
    cor, do que o autor pôs naquele lugar. É esse número que cai quando a rua de
    terra deixa de virar tábua de madeira.
    """
    os.makedirs(pasta, exist_ok=True)
    W, H = lf["width"], lf["height"]
    A = ANEL_COSTURA
    prim_c, sec_c = par.tileset_primario(), par.tileset_secundario()
    fatias = {"up": (range(0, A), range(W)), "down": (range(H - A, H), range(W)),
              "left": (range(H), range(0, A)), "right": (range(H), range(W - A, W))}
    total_err = total_px = 0
    caminhos = []
    for lado in sorted(par.lados):
        ys, xs = (list(v) for v in fatias[lado])
        def banda(qual):
            im = Image.new("RGB", (len(xs) * 16, len(ys) * 16))
            for j, cy in enumerate(ys):
                for i, cx in enumerate(xs):
                    if qual == "hack":
                        mid = par.blocos_f[cy * W + cx] & 0x3FF
                        px = desenha_metatile(d["prim_f"], d["sec_f"], mid,
                                              TILES_POR_METATILE_FONTE, fundo=(0, 0, 0))
                    else:
                        mid = par.blocos_novos[cy * W + cx] & 0x3FF
                        px = desenha_metatile(prim_c, sec_c, mid,
                                              TILES_POR_METATILE_NOSSO, fundo=(0, 0, 0))
                    t = Image.new("RGB", (16, 16))
                    t.putdata(px)
                    im.paste(t, (i * 16, j * 16))
            return im
        a, b = banda("hack"), banda("copia")
        err = px = 0
        pa, pb = a.load(), b.load()
        for y in range(a.size[1]):
            for x in range(a.size[0]):
                err += dist_cor(pa[x, y], pb[x, y])
                px += 1
        total_err += err
        total_px += px
        if lado in ("up", "down"):
            out = Image.new("RGB", (a.size[0], a.size[1] * 2 + 6), MAGENTA)
            out.paste(a, (0, 0))
            out.paste(b, (0, a.size[1] + 6))
        else:
            out = Image.new("RGB", (a.size[0] * 2 + 6, a.size[1]), MAGENTA)
            out.paste(a, (0, 0))
            out.paste(b, (a.size[0] + 6, 0))
        if max(out.size) < 900:
            out = out.resize((out.size[0] * 2, out.size[1] * 2), Image.NEAREST)
        caminho = os.path.join(pasta, f"{cidade}-anel-{lado}.png")
        out.save(caminho)
        caminhos.append((lado, caminho, err / max(1, px)))
        print(f"  [anel] {lado:5s} distância média por pixel {err / max(1, px):9.1f}  -> "
              f"{os.path.relpath(caminho, RAIZ)}")
    print(f"  [anel] TOTAL distância média por pixel {total_err / max(1, total_px):9.1f} "
          f"em {total_px} pixels de anel")
    return total_err / max(1, total_px)


def prancha_da_costura(par, d, lf, ln, cidade, pasta):
    """A prova da COSTURA, desenhada como o motor desenha.

    Para cada conexão, duas vistas da mesma junta:

      * PARADO NA CIDADE: a faixa da cidade e a faixa da rota, as duas pintadas
        com os tilesets da CIDADE (é o que o motor faz: `FillConnection` copia 7
        linhas do mapa vizinho para dentro do `gBackupMapLayout` do mapa atual).
      * PARADO NA ROTA: as mesmas duas faixas, as duas pintadas com os tilesets
        da ROTA.

    Se a junta estiver suja, ela aparece aqui antes de aparecer no emulador: é
    nesta imagem que se vê árvore de um estilo encostando em árvore de outro.
    """
    os.makedirs(pasta, exist_ok=True)
    mapas = indice_de_mapas()
    layouts = {l["id"]: l for l in le_layouts(
        os.path.join(RAIZ, "data/layouts/layouts.json"))["layouts"]}
    mj = None
    for nome, dados in mapas.values():
        if nome == ln["name"].replace("_Layout", ""):
            mj = dados
            break
    if mj is None:
        return []
    prim_c, sec_c = par.tileset_primario(), par.tileset_secundario()
    W, H = lf["width"], lf["height"]
    A = ANEL_COSTURA
    saidas = []
    for c in (mj.get("connections") or []):
        d_ = c.get("direction")
        if d_ not in ("up", "down", "left", "right") or c["map"] not in mapas:
            continue
        _, vmj = mapas[c["map"]]
        lay_r = layouts[vmj["layout"]]
        prim_r = Tileset(pasta_do_simbolo(RAIZ, lay_r["primary_tileset"], False),
                         TILES_POR_METATILE_NOSSO, lay_r["primary_tileset"])
        sec_r = Tileset(pasta_do_simbolo(RAIZ, lay_r["secondary_tileset"], True),
                        TILES_POR_METATILE_NOSSO, lay_r["secondary_tileset"])
        bl_r = le_blocos(os.path.join(RAIZ, lay_r["blockdata_filepath"].lstrip("./")))
        RW, RH = lay_r["width"], lay_r["height"]
        off = c.get("offset", 0)

        def celula(qual, cx, cy, prim, sec):
            """Índice -> pixels, com o tileset pedido. `qual` diz de que mapa."""
            if qual == "cidade":
                if not (0 <= cx < W and 0 <= cy < H):
                    return [(0, 0, 0)] * 256
                mid = par.blocos_novos[cy * W + cx] & 0x3FF
            else:
                if not (0 <= cx < RW and 0 <= cy < RH):
                    return [(0, 0, 0)] * 256
                mid = bl_r[cy * RW + cx] & 0x3FF
            return desenha_metatile(prim, sec, mid, TILES_POR_METATILE_NOSSO,
                                    fundo=(0, 0, 0))

        # janela: A células da cidade e A células da rota, ao longo da junta
        if d_ in ("up", "down"):
            larg = max(W, RW)
            colunas = [(x, x - off) for x in range(larg)]   # (coluna cidade, coluna rota)
            if d_ == "down":
                linhas = [("cidade", y) for y in range(H - A, H)] + \
                         [("rota", y) for y in range(0, A)]
            else:
                linhas = [("rota", y) for y in range(RH - A, RH)] + \
                         [("cidade", y) for y in range(0, A)]
            tam = (larg * 16, len(linhas) * 16)
        else:
            alt = max(H, RH)
            colunas = [(y, y - off) for y in range(alt)]
            if d_ == "right":
                linhas = [("cidade", x) for x in range(W - A, W)] + \
                         [("rota", x) for x in range(0, A)]
            else:
                linhas = [("rota", x) for x in range(RW - A, RW)] + \
                         [("cidade", x) for x in range(0, A)]
            tam = (len(linhas) * 16, alt * 16)

        def vista(prim, sec):
            im = Image.new("RGB", tam, (0, 0, 0))
            for i, (qual, k) in enumerate(linhas):
                for j, (cc, cr) in enumerate(colunas):
                    outro = cc if qual == "cidade" else cr
                    if d_ in ("up", "down"):
                        px = celula(qual, outro, k, prim, sec)
                        im.paste(_t16(px), (j * 16, i * 16))
                    else:
                        px = celula(qual, k, outro, prim, sec)
                        im.paste(_t16(px), (i * 16, j * 16))
            return im

        a = vista(prim_c, sec_c)      # parado na cidade
        b = vista(prim_r, sec_r)      # parado na rota
        if d_ in ("up", "down"):
            out = Image.new("RGB", (a.size[0], a.size[1] * 2 + 6), MAGENTA)
            out.paste(a, (0, 0)); out.paste(b, (0, a.size[1] + 6))
        else:
            out = Image.new("RGB", (a.size[0] * 2 + 6, a.size[1]), MAGENTA)
            out.paste(a, (0, 0)); out.paste(b, (a.size[0] + 6, 0))
        caminho = os.path.join(pasta, f"{cidade}-costura-{d_}-{c['map']}.png")
        out.save(caminho)
        saidas.append(caminho)
        print(f"  [costura] {d_:5s} {c['map']:22s} offset {off:4d} -> "
              f"{os.path.relpath(caminho, RAIZ)}")
    return saidas


def _t16(px):
    t = Image.new("RGB", (16, 16))
    t.putdata(px)
    return t


def prova_da_costura(par):
    """Metatile a metatile: o par NOVO desenha o índice pinado igual ao de HOJE?"""
    novo_p, novo_s = par.tileset_primario(), par.tileset_secundario()
    ok, falhas, detalhes = 0, 0, []
    for p in sorted(par.pinados):
        if par.pin_palavras.get(p) is None:
            continue
        a = desenha_metatile(par.prim_n, par.sec_n, p, TILES_POR_METATILE_NOSSO, fundo=(0, 0, 0))
        b = desenha_metatile(novo_p, novo_s, p, TILES_POR_METATILE_NOSSO, fundo=(0, 0, 0))
        attr_a = atributo_de(par.prim_n, par.sec_n, p)
        attr_b = atributo_de(novo_p, novo_s, p)
        if a == b and (attr_a & 0x00FF) == (attr_b & 0x00FF) and \
           ((attr_a >> 12) & 0xF) == ((attr_b >> 12) & 0xF):
            ok += 1
        else:
            falhas += 1
            diff = sum(1 for x, y in zip(a, b) if x != y)
            detalhes.append((p, diff, attr_a, attr_b))
    return ok, falhas, detalhes


def prova_do_tile_zero(par):
    """O slot 0 do primário novo tem de ser 64 pixels transparentes.

    Regra de motor medida em 11/09/2026 (contrato, seção 3.1): `DrawMetatile`
    (`src/field_camera.c`) escreve o índice 0 no BG1 de todo metatile de
    `layerType` COVERED, contando com que o slot 0 não desenhe nada. Tileset
    copiado que empacote arte ali vira um bloco opaco POR CIMA do jogador
    sempre que ele passa debaixo de uma copa ou de um telhado, e isso não
    aparece em contador nenhum: some o sprite, não o pixel do mapa.

    Devolve (slot 0 vazio?, quantas palavras de metatile do par NOVO apontam
    para o slot 0). O segundo número não é defeito: é o normal, é assim que o
    formato diz "esta camada desta célula não desenha nada".
    """
    vazio = not any(par.prim_tiles[0])
    refs = 0
    for m in list(par.prim_metatiles) + list(par.sec_metatiles):
        refs += sum(1 for e in m if (e & 0x3FF) == 0)
    return vazio, refs


def prova_da_animacao(par):
    """Os 80 slots da faixa são byte a byte os nossos, e ninguém mais os usa."""
    iguais = all(bytes(par.prim_tiles[i]) == bytes(par.prim_n.tiles[i])
                 for i in range(FAIXA_ANIM_INICIO, FAIXA_ANIM_FIM))
    hoje = set()
    for i, m in enumerate(par.prim_n.metatiles):
        for c, e in enumerate(m):
            if FAIXA_ANIM_INICIO <= (e & 0x3FF) < FAIXA_ANIM_FIM:
                hoje.add((i, c, e & 0x3FF))
    for i, m in enumerate(par.sec_n.metatiles):
        for c, e in enumerate(m):
            if FAIXA_ANIM_INICIO <= (e & 0x3FF) < FAIXA_ANIM_FIM:
                hoje.add((NUM_METATILES_IN_PRIMARY + i, c, e & 0x3FF))
    novos = set()
    for i, m in enumerate(par.prim_metatiles):
        for c, e in enumerate(m):
            if FAIXA_ANIM_INICIO <= (e & 0x3FF) < FAIXA_ANIM_FIM:
                novos.add((i, c, e & 0x3FF))
    for i, m in enumerate(par.sec_metatiles):
        for c, e in enumerate(m):
            if FAIXA_ANIM_INICIO <= (e & 0x3FF) < FAIXA_ANIM_FIM:
                novos.add((NUM_METATILES_IN_PRIMARY + i, c, e & 0x3FF))
    intrusos = sorted(novos - hoje)
    return iguais, intrusos


# ------------------------------------------------------------- emissão --------

def escreve_par(destino, tiles, paletas, primeiro_pal, metatiles, attrs):
    """Grava tiles.png, palettes/NN.pal, metatiles.bin e metatile_attributes.bin."""
    os.makedirs(os.path.join(destino, "palettes"), exist_ok=True)
    largura = 128
    altura = max(8, ((len(tiles) + 15) // 16) * 8)
    im = Image.new("P", (largura, altura), 0)
    achatada = []
    for cor in paletas[0]:
        achatada.extend(cor)
    achatada.extend([0] * (768 - len(achatada)))
    im.putpalette(achatada)
    px = im.load()
    for i, tile in enumerate(tiles):
        tx, ty = (i % 16) * 8, (i // 16) * 8
        for y in range(8):
            for x in range(8):
                px[tx + x, ty + y] = tile[y * 8 + x]
    im.save(os.path.join(destino, "tiles.png"))
    for i in range(16):
        j = i - primeiro_pal
        cores = paletas[j] if 0 <= j < len(paletas) else [(0, 0, 0)] * 16
        with open(os.path.join(destino, "palettes", f"{i:02d}.pal"), "w", encoding="utf-8") as f:
            f.write("JASC-PAL\n0100\n16\n")
            for r, g, b in cores:
                f.write(f"{r} {g} {b}\n")
    with open(os.path.join(destino, "metatiles.bin"), "wb") as f:
        for m in metatiles:
            f.write(struct.pack("<8H", *m))
    with open(os.path.join(destino, "metatile_attributes.bin"), "wb") as f:
        for a in attrs:
            f.write(struct.pack("<H", a))


MARCA_PAR_C = ("// ---- pares de tilesets das cidades copiadas de Sinnoh "
               "(dev_scripts/copia_cidade_fonte.py --par-proprio) ----")


def registra_tileset_par(simbolo, pasta_rel, n_tiles, secundario, callback):
    """Acrescenta um tileset em graphics.h, metatiles.h, headers.h e tilesets.h.

    Tudo no FIM de cada arquivo, atrás de uma marca própria da frente, para que
    o `git merge origin/master` das outras frentes não brigue com este bloco.
    """
    # `gbagfx` recusa `-num_tiles 0` com "Number of tiles must be positive" e o
    # build inteiro para. Medido em 11/09/2026 em Twinleaf, a primeira cidade
    # cuja arte cabe TODA no primário do par próprio (304 tiles de 944, 137
    # metatiles): o secundário sai com 0 tile e 1 metatile, que o layout exige
    # existir mas ninguém desenha. O piso de 1 tile é o mínimo que o conversor
    # aceita; o tile é o transparente que a ferramenta já reserva no slot 0, e
    # nenhum metatile aponta para ele.
    n_tiles = max(1, n_tiles)
    escritos = []
    g = os.path.join(RAIZ, "src/data/tilesets/graphics.h")
    texto = open(g, encoding="utf-8").read()
    if f"gTilesetTiles_{simbolo}[]" not in texto:
        bloco = [""]
        if MARCA_PAR_C not in texto:
            bloco.append(MARCA_PAR_C)
        bloco.append(
            f'const u32 gTilesetTiles_{simbolo}[] = INCGFX_U32("{pasta_rel}/tiles.png", '
            f'".4bpp.fastSmol", "-num_tiles {n_tiles} -Wnum_tiles");')
        bloco.append("")
        bloco.append(f"const u16 gTilesetPalettes_{simbolo}[][16] =")
        bloco.append("{")
        for i in range(16):
            bloco.append(f'    INCGFX_U16("{pasta_rel}/palettes/{i:02d}.pal", ".gbapal"),')
        bloco.append("};")
        open(g, "w", encoding="utf-8").write(texto.rstrip("\n") + "\n" + "\n".join(bloco) + "\n")
        escritos.append(g)

    m = os.path.join(RAIZ, "src/data/tilesets/metatiles.h")
    texto = open(m, encoding="utf-8").read()
    if f"gMetatiles_{simbolo}[]" not in texto:
        bloco = [""]
        if MARCA_PAR_C not in texto:
            bloco.append(MARCA_PAR_C)
        bloco.append(f'const u16 gMetatiles_{simbolo}[] = INCBIN_U16("{pasta_rel}/metatiles.bin");')
        bloco.append(f'const u16 gMetatileAttributes_{simbolo}[] = '
                     f'INCBIN_U16("{pasta_rel}/metatile_attributes.bin");')
        open(m, "w", encoding="utf-8").write(texto.rstrip("\n") + "\n" + "\n".join(bloco) + "\n")
        escritos.append(m)

    h = os.path.join(RAIZ, "src/data/tilesets/headers.h")
    texto = open(h, encoding="utf-8").read()
    if f"gTileset_{simbolo} =" not in texto:
        bloco = [""]
        if MARCA_PAR_C not in texto:
            bloco.append(MARCA_PAR_C)
        bloco += [
            f"const struct Tileset gTileset_{simbolo} =",
            "{",
            "    .isCompressed = TRUE,",
            f"    .isSecondary = {'TRUE' if secundario else 'FALSE'},",
            f"    .tiles = gTilesetTiles_{simbolo},",
            f"    .palettes = gTilesetPalettes_{simbolo},",
            f"    .metatiles = gMetatiles_{simbolo},",
            f"    .metatileAttributes = gMetatileAttributes_{simbolo},",
            f"    .callback = {callback},",
            "};",
        ]
        open(h, "w", encoding="utf-8").write(texto.rstrip("\n") + "\n" + "\n".join(bloco) + "\n")
        escritos.append(h)

    t = os.path.join(RAIZ, "include/tilesets.h")
    texto = open(t, encoding="utf-8").read()
    if f"gTileset_{simbolo};" not in texto:
        linhas = [
            f"extern const u32 gTilesetTiles_{simbolo}[];",
            f"extern const u16 gTilesetPalettes_{simbolo}[][16];",
            f"extern const struct Tileset gTileset_{simbolo};",
        ]
        if MARCA_PAR_C not in texto:
            linhas.insert(0, MARCA_PAR_C)
        marca_fim = "#endif //GUARD_tilesets_H"
        novo = texto.replace(marca_fim, "\n".join(linhas) + "\n\n" + marca_fim)
        open(t, "w", encoding="utf-8").write(novo)
        escritos.append(t)
    return escritos


def religa_layout_par(nome_layout, simbolo_primario, simbolo_secundario, largura, altura):
    """Troca o PAR e o tamanho do layout, SEM mexer no `id`.

    O `mapLayoutId` não muda nunca: a save guarda o layout por id, e recriar o
    layout em vez de substituí-lo no lugar quebraria a save de quem está dentro
    da cidade (item 3 da seção 1 do contrato).
    """
    caminho = os.path.join(RAIZ, "data/layouts/layouts.json")
    with open(caminho, encoding="utf-8") as f:
        dados = json.load(f)
    achou = False
    for l in dados["layouts"]:
        if l["name"] == nome_layout:
            l["primary_tileset"] = f"gTileset_{simbolo_primario}"
            l["secondary_tileset"] = f"gTileset_{simbolo_secundario}"
            l["width"] = largura
            l["height"] = altura
            achou = True
    if not achou:
        raise SystemExit(f"layout {nome_layout} não achado para religar")
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return caminho


# --------------------------------------------------------------- corpo --------

def roda_par_proprio(args, d, lf, ln, lados):
    depara = None
    if args.depara and os.path.exists(args.depara):
        with open(args.depara, encoding="utf-8") as f:
            bruto = json.load(f)
        chave = re.sub(r"(?<!^)(?=[A-Z])", "_",
                       lf["primary_tileset"].replace("gTileset_", "")).lower()
        depara = bruto.get("primarios", {}).get(chave)

    nome_mapa = ln["name"].replace("_Layout", "")
    print(f"  --- par próprio ---")
    if getattr(args, "sem_conexao", False):
        # Sem conexão não há faixa desenhada de fora, logo não há índice a pinar
        # e não há vocabulário de rota a respeitar. A PROVA C (costura) fica sem
        # objeto: ela compara índices pinados, e não existe nenhum.
        pinados, detalhe = set(), {"rota": set(), "anel": set()}
        print("  SEM CONEXÃO: 0 índices pinados, mapa inteiro interior, "
              "PROVA C sem objeto")
        par = ParDeTilesets(d["achatador"], d["prim_n"], d["sec_n"], depara, lados, lf,
                            d["blocos_f"], d["borda_f"], pinados,
                            vocabulario=None, tabela_anel={},
                            sem_anim=getattr(args, "sem_animacao", False))
        return _fecha_par(args, d, lf, ln, lados, par, par.constroi("cor"))

    pinados, detalhe = conjunto_pinado(nome_mapa, lados)
    print(f"  pinados: rota {len(detalhe['rota'])}, anel da nossa cidade "
          f"{len(detalhe['anel'])}, união {len(pinados)} "
          f"({len([p for p in pinados if p >= NUM_METATILES_IN_PRIMARY])} no secundário de hoje)")
    if getattr(args, "pinar_so_necessario", False):
        # O anel da cidade de HOJE deixa de existir no instante em que o map.bin
        # é substituído: quem a rota vai desenhar é o anel do mapa NOVO, e esse
        # entra no conjunto pinado sozinho, pelo `mapeia_anel`. Pinar o antigo
        # custa cor e vaga de paleta sem comprar costura nenhuma.
        pinados = set(detalhe["rota"])
        print(f"  --pinar-so-necessario: o anel ANTIGO sai; ficam {len(pinados)} "
              f"da rota, mais o que o anel NOVO exigir")

    tabela = {}
    caminho_tabela = getattr(args, "anel_tabela", None) or TABELA_ANEL_PADRAO
    if os.path.exists(caminho_tabela):
        with open(caminho_tabela, encoding="utf-8") as f:
            tabela = (json.load(f).get("cidades", {}) or {}).get(args.cidade, {}) or {}
    print(f"  tabela do anel: {os.path.relpath(caminho_tabela, RAIZ)} "
          f"({len(tabela)} metatiles julgados na mão para {args.cidade})")

    par = ParDeTilesets(d["achatador"], d["prim_n"], d["sec_n"], depara, lados, lf,
                        d["blocos_f"], d["borda_f"], pinados,
                        vocabulario=detalhe["rota"] | detalhe["anel"],
                        tabela_anel=tabela,
                        sem_anim=getattr(args, "sem_animacao", False))
    faltantes = par.constroi("cor")
    return _fecha_par(args, d, lf, ln, lados, par, faltantes)


def _fecha_par(args, d, lf, ln, lados, par, faltantes):
    """Escolhe a semente de paleta, imprime o orçamento e roda as provas.

    Saiu de dentro do `roda_par_proprio` quando o modo `--sem-conexao` nasceu:
    os dois caminhos montam o par de um jeito (com ou sem índice pinado) e
    fecham do MESMO jeito, e duplicar este trecho era pedir para os dois
    divergirem calados.
    """
    # A pontuação é a FIDELIDADE DO PIXEL RENDERIZADO, não a contagem de blocos
    # quantizados nem o erro ponderado. A afirmação que interessa é "a cópia
    # parece a fonte", então a verificação tem de ser feita nessa camada:
    # renderiza, compara, escolhe. Em Twinleaf o erro ponderado apontava para a
    # semente 'paleta' e o pixel apontava para a 'cor' (100,00% contra 99,92%).
    alvo = render_mapa(d["blocos_f"], lf["width"], lf["height"], d["prim_f"], d["sec_f"],
                       TILES_POR_METATILE_FONTE, TILES_POR_METATILE_FONTE,
                       achatador=d["achatador"])
    alvo_px = alvo.load()

    def fidelidade(p):
        saida = render_mapa(p.blocos_novos, lf["width"], lf["height"],
                            p.tileset_primario(), p.tileset_secundario(),
                            TILES_POR_METATILE_NOSSO, TILES_POR_METATILE_NOSSO)
        spx = saida.load()
        ig = di = 0
        for cy in range(lf["height"]):
            for cx in range(lf["width"]):
                if zona_da_celula(cx, cy, lf["width"], lf["height"], lados) != "interior":
                    continue
                for y in range(cy * 16, cy * 16 + 16):
                    for x in range(cx * 16, cx * 16 + 16):
                        if alvo_px[x, y] == spx[x, y]:
                            ig += 1
                        else:
                            di += 1
        return 100.0 * ig / max(1, ig + di)

    notas = {}
    notas["cor"] = fidelidade(par)
    print(f"  semente 'cor'   : {len(par.quantizados)} blocos quantizados, "
          f"custo ponderado {par.custo_da_quantizacao()}, interior {notas['cor']:.2f}%")
    par.fecha("paleta")
    notas["paleta"] = fidelidade(par)
    print(f"  semente 'paleta': {len(par.quantizados)} blocos quantizados, "
          f"custo ponderado {par.custo_da_quantizacao()}, interior {notas['paleta']:.2f}%")
    if notas["cor"] >= notas["paleta"]:
        par.fecha("cor")
    print(f"  SEMENTE escolhida: '{par.estrategia}' (interior "
          f"{max(notas.values()):.2f}%)")
    print(f"  ANEL: {len(par.equiv_anel)} metatiles da fonte substituídos; "
          f"origem {dict(par.anel_contagem)}")
    if faltantes:
        print(f"    ATENÇÃO: {faltantes} sem candidato na mesma família de chão "
              f"(caíram no vizinho mais próximo sem guarda)")
    print(f"  PINADOS no fim (com os alvos do anel): {len(par.pinados)}")
    reservados = 0 if par.sem_anim else FAIXA_ANIM_FIM - FAIXA_ANIM_INICIO
    print(f"  tiles: primário {par.livre_prim}/{par.teto_prim} livres usados "
          f"+ {reservados} reservados de animação, "
          f"secundário {len(par.sec_tiles)}/{NUM_TILES_IN_PRIMARY} "
          f"(total {par.livre_prim + len(par.sec_tiles)} de "
          f"{par.teto_prim + NUM_TILES_IN_PRIMARY})")
    print(f"  metatiles: primário {sum(1 for m in par.prim_metatiles if any(m))}/512, "
          f"secundário {len(par.sec_metatiles)}/512")
    usadas = [len(c) for c in par.cores_bin]
    print(f"  paletas: {len(par.paletas)} de {NUM_PALS_TOTAL} "
          f"({par.n_verbatim} verbatim da animação), cores por paleta {usadas}")
    print(f"  empacotamento: {par.baldes_iniciais} conjuntos de cor distintos "
          f"({par.cores_totais} cores no total), {par.fusoes_exatas} fusões EXATAS, "
          f"{par.fusoes_aprox} APROXIMADAS (pior erro de fusão {par.pior_fusao})")
    print(f"  blocos de 8x8 distintos: {len(par.blocos)} "
          f"(pinados {sum(1 for i in par.blocos.values() if i['pinado'])})")
    if par.recusas:
        print(f"  RECUSA: {len(par.recusas)} blocos PINADOS sem paleta exata "
              f"(faltaram até {max(f for _, f in par.recusas)} cores). "
              f"A costura NÃO fecha assim.")
    if par.quantizados:
        pior = max(e for _, e in par.quantizados)
        print(f"  quantizados (só arte deles): {len(par.quantizados)} blocos, "
              f"pior erro quadrático {pior}")
    else:
        print("  quantizados: nenhum (toda cor achou paleta exata)")
    if par.sem_slot:
        print(f"  SEM SLOT DE TILE: {len(par.sem_slot)} blocos não couberam nos 944")
    if par.sem_metatile:
        print(f"  SEM SLOT DE METATILE: {par.sem_metatile} metatiles de arte não couberam")
    if par.avisos:
        print(f"  avisos: {par.avisos[:4]}")

    ok, falhas, detalhes = prova_da_costura(par)
    if ok + falhas == 0:
        print("  [ok ] PROVA C (costura): SEM OBJETO, a cidade não tem conexão "
              "(nenhum índice pinado)")
    else:
        print(f"  [{'ok ' if falhas == 0 else 'RUIM'}] PROVA C (costura): {ok} de {ok + falhas} "
              f"índices pinados batem pixel a pixel e no atributo")
    if falhas:
        print(f"    furos: {[(p, dif) for p, dif, _, _ in detalhes[:10]]}")

    vazio, refs = prova_do_tile_zero(par)
    print(f"  [{'ok ' if vazio else 'RUIM'}] PROVA DO TILE 0: o slot 0 do primário "
          f"novo está {'VAZIO' if vazio else 'COM ARTE'} "
          f"({refs} palavras de metatile apontam para ele, o que o motor lê como "
          f"'sem desenho')")
    if not vazio:
        print("    DrawMetatile escreve 0 no BG1 de todo metatile COVERED: com "
              "arte no slot 0, o jogador some debaixo de copa e telhado.")

    if par.sem_anim:
        print("  [ok ] PROVA DA ANIMAÇÃO: SEM OBJETO, o primário novo não tem "
              "animação (--sem-animacao; .callback = NULL e os 80 slots de "
              "432 a 511 viraram arte)")
    else:
        iguais, intrusos = prova_da_animacao(par)
        print(f"  [{'ok ' if iguais and not intrusos else 'RUIM'}] PROVA DA ANIMAÇÃO: "
              f"faixa 432-511 byte a byte {'igual' if iguais else 'DIFERENTE'}, "
              f"{len(intrusos)} referências novas à faixa")
    if getattr(args, "prancha_anel", None):
        prancha_do_anel(par, d, lf, args.cidade, args.prancha_anel)
        prancha_da_costura(par, d, lf, ln, args.cidade, args.prancha_anel)
    d["par"] = par
    return par


if __name__ == "__main__":
    sys.exit(main())
