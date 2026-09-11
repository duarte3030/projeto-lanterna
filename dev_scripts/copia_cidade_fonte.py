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
FONTE_PADRAO = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/romhacks/retro-platinum/fonte"

NUM_TILES_IN_PRIMARY = 512
NUM_METATILES_IN_PRIMARY = 512
NUM_PALS_IN_PRIMARY = 6
NUM_PALS_TOTAL = 13
TILES_POR_METATILE_FONTE = 12   # três camadas
TILES_POR_METATILE_NOSSO = 8    # duas camadas

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

    def __init__(self, fonte_prim, fonte_sec):
        self.prim = fonte_prim
        self.sec = fonte_sec
        self.sem_paleta = []
        self.compostos = {}   # chave -> (pixels, paleta_de_origem)

    def tiles_e_paletas(self, entrada):
        return resolve(entrada, self.prim, self.sec)

    def pixels(self, entrada):
        if (entrada & 0x3FF) == 0:
            return [None] * 64
        tiles, paletas, local = resolve(entrada, self.prim, self.sec)
        return pinta_tile(tiles, paletas, local, transparente=None)

    def camadas(self, metatile12):
        return [metatile12[0:4], metatile12[4:8], metatile12[8:12]]

    def achata(self, metatile12):
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
                chave = (f, m)
                if chave not in self.compostos:
                    px = compoe(self.pixels(f), self.pixels(m))
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

def render_mapa(blocos, largura, altura, prim, sec, tpm_prim, tpm_sec, escala=1, objetos=None):
    """Desenha um mapa em PNG a partir de blocos e dois tilesets já carregados."""
    # A cor 0 da paleta 0 do primário é o backdrop compartilhado dos BG: é ela
    # que aparece onde nenhuma camada desenha, e não preto.
    fundo = prim.paletas[0][0]
    im = Image.new("RGB", (largura * 16, altura * 16), fundo)
    px = im.load()
    cache = {}
    for i, palavra in enumerate(blocos[:largura * altura]):
        mid = palavra & 0x3FF
        mx, my = (i % largura) * 16, (i // largura) * 16
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


def mede(nome_fonte, nome_nosso, raiz_fonte):
    lay_f, prim_f, sec_f, blocos_f, borda_f = carrega_lado_fonte(raiz_fonte, nome_fonte)
    lay_n, prim_n, sec_n, blocos_n, borda_n = carrega_lado_nosso(nome_nosso)

    usados = set()
    for palavra in blocos_f + borda_f:
        usados.add(palavra & 0x3FF)

    achatador = Achatador(prim_f, sec_f)
    tres_camadas = 0
    celulas_compostas = 0
    tiles_pal_baixa = set()
    tiles_pal_alta = set()
    paletas_altas = set()
    comportamentos_suspeitos = {}

    for mid in sorted(usados):
        if mid < NUM_METATILES_IN_PRIMARY:
            ts, local = prim_f, mid
        else:
            ts, local = sec_f, mid - NUM_METATILES_IN_PRIMARY
        if local >= len(ts.metatiles):
            continue
        m = ts.metatiles[local]
        camadas = [m[0:4], m[4:8], m[8:12]]
        if sum(1 for c in camadas if any(t & 0x3FF for t in c)) == 3:
            tres_camadas += 1
        _, _, _, comps = achatador.achata(m)
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
        if local < len(ts.attrs):
            comportamento = ts.attrs[local] & 0x00FF
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


CIDADES = {
    "TwinleafTown": ("TwinleafTown_Layout", "TwinleafTown_Layout"),
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
    p.add_argument("--prova-fonte", action="store_true",
                   help="compara o render da FONTE com o render de referência dela (prova do leitor de 3 camadas)")
    args = p.parse_args()

    nome_fonte, nome_nosso = CIDADES[args.cidade]
    d = mede(nome_fonte, nome_nosso, args.fonte)
    lf, ln = d["lay_fonte"], d["lay_nosso"]

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
    print(f"  ORÇAMENTO do secundário novo: {orcamento} de {NUM_TILES_IN_PRIMARY} slots, "
          f"folga {folga}" + ("  <<< ESTOURO" if folga < 0 else ""))
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
                           TILES_POR_METATILE_FONTE, TILES_POR_METATILE_FONTE)
        alvo_px = alvo.load()

        def fidelidade_de(cand, blocos_novos, depara_usado):
            trocadas = {int(k) for k, v in (depara_usado or {}).get("metatiles", {}).items()
                        if v.get("nosso") is not None}
            sec_mem = TilesetEmMemoria(cand.pacote, cand.metatiles_novos, cand.attrs_novos)
            saida = render_mapa(blocos_novos, lf["width"], lf["height"], d["prim_n"], sec_mem,
                                TILES_POR_METATILE_NOSSO, TILES_POR_METATILE_NOSSO)
            spx = saida.load()
            iguais = difere = 0
            for i in range(lf["width"] * lf["height"]):
                if (d["blocos_f"][i] & 0x3FF) in trocadas:
                    continue
                mx, my = (i % lf["width"]) * 16, (i // lf["width"]) * 16
                for y in range(my, my + 16):
                    for x in range(mx, mx + 16):
                        if alvo_px[x, y] == spx[x, y]:
                            iguais += 1
                        else:
                            difere += 1
            return 100.0 * iguais / max(1, iguais + difere)

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

    if args.aplicar:
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
                        objetos=objs)
        caminho_fonte = os.path.join(args.render, f"{args.cidade}-fonte.png")
        b.save(caminho_fonte)
        if d.get("conversao") is not None:
            conv = d["conversao"]
            sec_novo = TilesetEmMemoria(conv.pacote, conv.metatiles_novos, conv.attrs_novos)
            c = render_mapa(d["blocos_convertidos"], lf["width"], lf["height"],
                            d["prim_n"], sec_novo,
                            TILES_POR_METATILE_NOSSO, TILES_POR_METATILE_NOSSO, args.escala)
            c.save(os.path.join(args.render, f"{args.cidade}-copia.png"))
            print(f"  render da CÓPIA: {args.render}/{args.cidade}-copia.png")
            # Fidelidade medida só onde a cópia DEVIA ser igual. As células cujo
            # metatile foi trocado pelo nosso (a mata e a grama da moldura) têm
            # de diferir mesmo: é a costura com as rotas vizinhas, e contá-las
            # como erro daria 41% de "infidelidade" numa cópia fiel.
            trocadas = {int(k) for k, v in (depara or {}).get("metatiles", {}).items()
                        if v.get("nosso") is not None}
            fonte_px = b.load()
            copia_px = c.load()
            iguais = difere = 0
            for i, palavra in enumerate(d["blocos_f"][:lf["width"] * lf["height"]]):
                if (palavra & 0x3FF) in trocadas:
                    continue
                mx, my = (i % lf["width"]) * 16, (i // lf["width"]) * 16
                for y in range(my, my + 16):
                    for x in range(mx, mx + 16):
                        if fonte_px[x, y] == copia_px[x, y]:
                            iguais += 1
                        else:
                            difere += 1
            total = iguais + difere
            if total:
                print(f"  FIDELIDADE no que foi copiado: {100.0 * iguais / total:.2f}% "
                      f"({difere} pixels diferentes de {total}); a moldura de mata "
                      f"e de grama é NOSSA de propósito e ficou fora da conta")
        print(f"  render: {args.render}/{args.cidade}-nosso.png e -fonte.png")
        if args.prova_fonte:
            pasta_ref = os.path.join(os.path.dirname(args.fonte.rstrip("/")), "render")
            igual, detalhe = prova_contra_render_de_referencia(args.cidade, caminho_fonte, pasta_ref)
            marca = "ok " if igual else "RUIM"
            print(f"  [{marca}] prova do leitor de 3 camadas contra o render da fonte: {detalhe}")
            if not igual:
                return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
