#!/usr/bin/env python3
"""G1 da obra de Galar: os 48 tilesets extraidos pelo G0 viram tilesets do repo.

Uso:
    python3 dev_scripts/tileset_galar.py --demo              # autoteste, nao grava
    python3 dev_scripts/tileset_galar.py --gravar            # grava os 47
    python3 dev_scripts/tileset_galar.py --gravar --registrar # ... e registra em C
    python3 dev_scripts/tileset_galar.py --prova [--n 10]    # fidelidade de render

O QUE ELE FAZ, E O QUE ELE NAO FAZ

Faz: le `fontes-mapas/galar-swsh/extraidos-ultimate/tilesets/<END>/` (saida do
`extrai_tilesets_galar.py`, o G0) e grava `data/tilesets/{primary,secondary}/
galar_NN/` com `tiles.png`, `palettes/00..15.pal`, `metatiles.bin` e
`metatile_attributes.bin` de 4 B no formato FRLG, que o nosso motor ja le quando
o layout tem `layout_version: "frlg"` (`MapLayout.isFrlg` -> `sMetatileAttrMasks`
em src/fieldmap.c). Grava tambem `dev_scripts/galar_tilesets.json`, o censo
de-para que o G2 consome. `--registrar` escreve as quatro entradas em C.

Nao faz: mapa, layout, header (isso e o G2), nem animacao de tileset (o
`.callback` sai NULL; os 22 tilesets com callback na fonte estao anotados no
censo, e a arte animada fica parada, nao suja).

O NUMERO NN E POSICAO NA LISTA ORDENADA DOS 48 ENDERECOS DA FONTE, com buraco:
0x2D4F8C nao e convertido (ver abaixo) e o indice 40 fica vago de proposito, para
que o numero de um tileset nunca mude se a fonte for reextraida.

AS QUATRO DIFERENCAS ENTRE A FONTE E O REPO, e o que cada uma custa

1. **COMPORTAMENTO.** O byte de comportamento do FR nao e o nosso. Passa pelo
   `migration_scripts/frlg_metatile_behavior_converter.py` (importado, nao
   copiado): `FRLG_BEHAVIORS` -> `FRLG_TO_EMERALD` -> `EMERALD_BEHAVIORS`. Os
   outros 23 bits do atributo (terreno, tipo de encontro, camada) passam intactos.

   O QUE O CONVERSOR ORIGINAL FAZ COM COMPORTAMENTO DESCONHECIDO E MANTER O
   VALOR, E AQUI ELE VIRA `MB_NORMAL`. Motivo medido: 212 valores distintos
   aparecem nos 12.193 metatiles da fonte e 899 metatiles (2,84% dos que algum
   mapa usa) estao fora da tabela do FR, com valores como 307, 456 e 511 que nao
   sao comportamento de nada em ROM nenhuma. Manter o valor faria o nosso motor
   ler um `MB_*` que nao existe (o teto e `MB_INVALID` = 255) e sortear
   encontro, agua ou warp em cima de chao. A colisao NAO mora no atributo, mora
   no blockdata, entao `MB_NORMAL` nao abre parede: e o neutro certo. Todos vao
   para o censo com valor e contagem, para a fase de conteudo revisar.

2. **CAMADA 3.** O campo de camada do FR tem 2 bits e so 3 valores validos
   (NORMAL, COVERED, SPLIT). A fonte usa o valor 3 em 181 metatiles (14 usados
   por mapa, em 3 tilesets). No nosso `DrawMetatile` (src/field_camera.c) o
   `switch` nao tem `case` para 3: o metatile nao desenha NADA e o buffer fica
   com o lixo do quadro anterior. Vira 0 (NORMAL), contado no censo.

3. **TILE CITADO QUE NAO EXISTE (o guard).** 11 tilesets secundarios tem
   metatile citando indice de tile alem do que o proprio tileset endereca (o
   campeao e 0x2D4D7C: 146 tiles e citacao ate 1023). Em ROM isso desenha o lixo
   que estiver na VRAM. Aqui a citacao e redirecionada para um tile GARANTIDO
   VAZIO no fim do proprio tileset, que desenha transparente, exatamente o que o
   render de referencia do G0 faz (`renderiza_de_disco` pula a entrada). Custo:
   zero na maioria, porque o PNG ja e preenchido ate fechar a linha de 16 tiles;
   so 3 tilesets ganham uma linha nova (512 B crus, que o smol come).

   NAO E GUARD, e por isso NAO e mexido: primario citando tile >= 640. Esses
   sao os tiles do SECUNDARIO pareado, resolvidos em tempo de execucao. O
   primario 0x2D4BB4 cita ate 799 e esta certo.

4. **0x2D4F8C NAO E CONVERTIDO.** `isCompressed=1` mas o byte apontado e 0xFF,
   nao 0x10: nao ha cabecalho LZ77, e o G0 mediu 0 tiles e 0 metatiles. E um
   tileset vazio usado por 1 mapa (g10m07). Convertelo seria inventar dado.

O 0x2D4A94 TEM DOIS PAPEIS NA FONTE e so o primario importa: ele e primario de
177 mapas e "secundario" de 2 (g42m03, 2x2, e g42m09, 1x1, ambos com UM metatile
distinto e com ele mesmo de primario). Entra como PRIMARIO; os dois usos
degenerados ficam no censo, para o G2 nao tentar parear tileset primario como
secundario (o motor le `.isSecondary` e quebraria o corte de metatile).
"""
import argparse
import glob
import hashlib
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTE = os.path.join(os.path.dirname(RAIZ),
                     "fontes-mapas/galar-swsh/extraidos-ultimate")

sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
sys.path.insert(0, os.path.join(RAIZ, "migration_scripts"))

import numpy as np                                    # noqa: E402
from PIL import Image                                 # noqa: E402

import frlg_metatile_behavior_converter as fr         # noqa: E402
import tileset_gen2 as tg2                            # noqa: E402  _insere

PRIMARIO_METATILES = 640      # NUM_METATILES_IN_PRIMARY_FRLG, include/fieldmap.h
PRIMARIO_TILES = 640          # NUM_TILES_IN_PRIMARY_FRLG
SECUNDARIO_TILES = 1024 - PRIMARIO_TILES
BEH_MASK = fr.BEHAVIOR_MASK   # 0x1FF, bits 0-8
LAYER_MASK, LAYER_SHIFT = 0x60000000, 29
MB_NORMAL = fr.EMERALD_BEHAVIORS["MB_NORMAL"]
CAMADAS_VALIDAS = (0, 1, 2)   # METATILE_LAYER_TYPE_{NORMAL,COVERED,SPLIT}

CENSO = f"{RAIZ}/dev_scripts/galar_tilesets.json"
MARCA = "// --- Galar (G1, tileset_galar.py) ---"

# Comportamentos do NOSSO motor que fazem um warp disparar, lidos do nome e nao
# de numero copiado (mesma tabela de dev_scripts/valida_warp_tile.py, que a tira
# de IsWarpMetatileBehavior + IsArrowWarpMetatileBehavior +
# IsDirectionalStairWarpMetatileBehavior).
NOMES_QUE_DISPARAM = (
    "MB_ANIMATED_DOOR", "MB_LADDER", "MB_UP_ESCALATOR", "MB_DOWN_ESCALATOR",
    "MB_NON_ANIMATED_DOOR", "MB_WATER_DOOR", "MB_DEEP_SOUTH_WARP",
    "MB_LAVARIDGE_GYM_B1F_WARP", "MB_LAVARIDGE_GYM_1F_WARP",
    "MB_AQUA_HIDEOUT_WARP", "MB_MT_PYRE_HOLE", "MB_MOSSDEEP_GYM_WARP",
    "MB_BRIDGE_OVER_OCEAN",
    "MB_NORTH_ARROW_WARP", "MB_SOUTH_ARROW_WARP", "MB_WEST_ARROW_WARP",
    "MB_EAST_ARROW_WARP", "MB_WATER_SOUTH_ARROW_WARP",
    "MB_STAIRS_OUTSIDE_ABANDONED_SHIP", "MB_SHOAL_CAVE_ENTRANCE",
    "MB_UP_RIGHT_STAIR_WARP", "MB_UP_LEFT_STAIR_WARP",
    "MB_DOWN_RIGHT_STAIR_WARP", "MB_DOWN_LEFT_STAIR_WARP",
)


def resgate_por_byte_baixo(beh):
    """Comportamento desconhecido que na verdade e PORTA, ou None.

    MEDIDO em 18/08/2026 (G5). Dos 122 valores de comportamento que a fonte usa
    e a tabela do FR nao tem, 61 sao um valor CONHECIDO com o bit 8 (0x100)
    aceso a mais: 307 = 0x100|51 (IMPASSABLE_SOUTH), 264 = 0x100|8 (CAVE),
    361 = 0x100|105 (WARP_DOOR), e assim por diante em 438 dos 899 metatiles.
    O bit 9 do campo de 9 bits do FR nao e comportamento de nada em ROM nenhuma;
    o editor do autor do demake o acendeu.

    So que "provavel" nao basta para mexer em 438 metatiles: virar 277 deles em
    IMPASSABLE_* ou em agua muda ANDAR, e por parede onde hoje nao ha. Entao o
    resgate e ESTREITO de proposito: so vale quando o byte baixo da uma PORTA, e
    porta so muda o jogo onde ha um warp em cima (o motor procura o warp naquela
    coordenada e, se nao houver, nao faz nada). Assim a prova do resgate e
    independente da hipotese: o unico efeito visivel e um warp da fonte, que a
    fonte pos ali de proposito, voltar a disparar.

    Medida do que isto alcanca hoje: 10 metatiles em 4 tilesets, e 11 warps de
    Circhester que estavam mortos. Os outros 464 warps mortos de Galar NAO sao
    disto: o comportamento deles e MB_FRLG_NORMAL na propria fonte (chao, mato,
    lado do tapete de saida), e estao no censo de `mundo_galar.py`.
    """
    if beh <= 0xFF:
        return None
    nome_fr = fr.FRLG_BEHAVIORS.get(beh & 0xFF)
    if nome_fr is None:
        return None
    nome_em = fr.FRLG_TO_EMERALD[nome_fr]
    if nome_em not in NOMES_QUE_DISPARAM:
        return None
    return nome_fr, nome_em, fr.EMERALD_BEHAVIORS[nome_em]


# ------------------------------------------------------------------- leitura G0

def fonte_dirs(fonte=FONTE):
    return sorted(glob.glob(f"{fonte}/tilesets/*/"))


def le_info(d):
    return json.load(open(f"{d}/info.json"))


def catalogo(fonte=FONTE):
    """[(NN, dir, info)] dos 48, na ordem do endereco. NN nunca muda."""
    return [(i, d.rstrip("/"), le_info(d)) for i, d in enumerate(fonte_dirs(fonte))]


def nome_de(nn):
    return f"galar_{nn:02d}"


def rotulo_de(nn):
    return f"Galar{nn:02d}"


def pasta_de(nn, papel):
    sub = "primary" if papel == "primario" else "secondary"
    return f"{RAIZ}/data/tilesets/{sub}/{nome_de(nn)}"


def pasta_rel(nn, papel):
    return os.path.relpath(pasta_de(nn, papel), RAIZ)


def le_tiles_png(caminho):
    """(matriz de indices de cor, n_tiles enderecaveis incluindo o preenchimento)."""
    px = np.array(Image.open(caminho))
    assert px.shape[1] == 128, f"{caminho}: {px.shape[1]} px de largura, esperava 128"
    return px, (px.shape[0] // 8) * 16


# ------------------------------------------------------------------- conversao

def converte(nn, d, info):
    """Tudo que vai para o disco de um tileset, mais o que o censo precisa saber."""
    papel = info["papel"]
    secundario = papel == "secundario"
    n_tiles = info["n_tiles"]

    px, n_end = le_tiles_png(f"{d}/tiles.png")
    metas = bytearray(open(f"{d}/metatiles.bin", "rb").read())
    attrs = list(struct.unpack("<%dI" % (len(open(f"{d}/metatile_attributes.bin",
                                                  "rb").read()) // 4),
                               open(f"{d}/metatile_attributes.bin", "rb").read()))

    # --- 3. guard: citacao de tile alem do enderecavel vai para um tile vazio
    #        no fim do proprio tileset. So faz sentido no secundario (ver o
    #        cabecalho: primario citando >= 640 e o secundario pareado).
    guard_tile, n_guard = None, 0
    crus_metas = bytes(metas)
    if secundario and n_tiles:
        limite = PRIMARIO_TILES + n_tiles
        entradas = np.frombuffer(crus_metas, dtype="<u2")
        fora = (entradas & 0x3FF) >= limite
        if fora.any():
            guard_tile = n_tiles          # local; global = 640 + n_tiles
            if guard_tile >= n_end:       # a linha do PNG fechou certinho
                px = np.vstack([px, np.zeros((8, 128), dtype=px.dtype)])
                n_end += 16
            assert guard_tile < SECUNDARIO_TILES, \
                f"{nome_de(nn)}: tile de guard {guard_tile} passa do teto do secundario"
            # o tile de destino TEM que ser vazio, senao redirecionar para la
            # desenharia sujeira em vez de nada
            y, x = (guard_tile // 16) * 8, (guard_tile % 16) * 8
            assert not px[y:y + 8, x:x + 8].any(), \
                f"{nome_de(nn)}: o tile {guard_tile} do tiles.png nao e vazio"
            novas = entradas.copy()
            novas[fora] = (novas[fora] & np.uint16(0xFC00)) | np.uint16(
                PRIMARIO_TILES + guard_tile)
            metas = bytearray(novas.tobytes())
            n_guard = int(fora.sum())

    # --- 1 e 2. comportamento pelo conversor do repo, camada invalida para 0
    conv, iguais, mudados, desconhecidos = [], 0, 0, {}
    camadas_corrigidas = 0
    resgatados = {}
    for a in attrs:
        beh = a & BEH_MASK
        nome_fr = fr.FRLG_BEHAVIORS.get(beh)
        if nome_fr is None:
            resgate = resgate_por_byte_baixo(beh)
            if resgate:
                novo = resgate[2]
                resgatados[beh] = resgatados.get(beh, 0) + 1
            else:
                novo = MB_NORMAL
                desconhecidos[beh] = desconhecidos.get(beh, 0) + 1
        else:
            novo = fr.EMERALD_BEHAVIORS[fr.FRLG_TO_EMERALD[nome_fr]]
            if novo == beh:
                iguais += 1
            else:
                mudados += 1
        v = novo | (a & ~BEH_MASK)
        if ((v & LAYER_MASK) >> LAYER_SHIFT) not in CAMADAS_VALIDAS:
            v &= ~LAYER_MASK
            camadas_corrigidas += 1
        conv.append(v)

    return {
        "nn": nn, "endereco": info["endereco"], "papel": papel,
        "tiles_px": px, "n_tiles": n_tiles, "n_tiles_enderecaveis": n_end,
        "metatiles": bytes(metas), "atributos": struct.pack("<%dI" % len(conv), *conv),
        "n_metatiles": info["n_metatiles"],
        "guard_tile": guard_tile, "n_guard": n_guard,
        "beh_iguais": iguais, "beh_mudados": mudados,
        "beh_desconhecidos": desconhecidos,
        "beh_resgatados_porta": resgatados,
        "camadas_corrigidas": camadas_corrigidas,
        "animado": info["animado"], "n_mapas": info["n_mapas"],
        "papeis_de_uso": info["papeis_de_uso"],
        "maior_tile_citado": info["maior_tile_citado"],
        # o guard nem sempre muda byte: quando a citacao cai exatamente no
        # primeiro tile de preenchimento do PNG (0x2D4C2C, 0x2D4C74, 0x2D4E0C,
        # 0x2D507C), o destino JA era o tile vazio e o .bin sai identico.
        "copia_metatiles": bytes(metas) == crus_metas,
    }


def grava(ts, d_fonte):
    d = pasta_de(ts["nn"], ts["papel"])
    os.makedirs(f"{d}/palettes", exist_ok=True)
    Image.open(f"{d_fonte}/tiles.png").convert("P")     # so valida que abre
    im = Image.fromarray(ts["tiles_px"], mode="P")
    im.putpalette(Image.open(f"{d_fonte}/tiles.png").getpalette())
    im.save(f"{d}/tiles.png")
    for p in range(16):
        with open(f"{d}/palettes/{p:02d}.pal", "w") as f:
            f.write(open(f"{d_fonte}/palettes/{p:02d}.pal").read())
    open(f"{d}/metatiles.bin", "wb").write(ts["metatiles"])
    open(f"{d}/metatile_attributes.bin", "wb").write(ts["atributos"])
    return d


# --------------------------------------------------------------- registro em C

def registra(ts):
    """As quatro entradas do expansion, no molde do `tileset_gen2.registra`."""
    nn, papel = ts["nn"], ts["papel"]
    r, pasta = rotulo_de(nn), pasta_rel(nn, papel)
    sec = "FALSE" if papel == "primario" else "TRUE"
    # `.smol` no primario e `.fastSmol` no secundario e a convencao do repo
    # (general_frlg contra pokemon_center_frlg): o primario carrega uma vez.
    smol = ".4bpp.smol" if papel == "primario" else ".4bpp.fastSmol"
    pals = "\n".join(f'    INCGFX_U16("{pasta}/palettes/{i:02d}.pal", ".gbapal"),'
                     for i in range(16))
    graficos = (f'const u32 gTilesetTiles_{r}[] = '
                f'INCGFX_U32("{pasta}/tiles.png", "{smol}");\n\n'
                f'const u16 gTilesetPalettes_{r}[][16] =\n{{\n{pals}\n}};\n')
    metas = (f'const u16 gMetatiles_{r}[] = INCBIN_U16("{pasta}/metatiles.bin");\n'
             f'const u16 gMetatileAttributes_{r}[] = '
             f'INCBIN_U16("{pasta}/metatile_attributes.bin");\n')
    header = (f'const struct Tileset gTileset_{r} =\n{{\n'
              f'    .isCompressed = TRUE,\n    .isSecondary = {sec},\n'
              f'    .tiles = gTilesetTiles_{r},\n'
              f'    .palettes = gTilesetPalettes_{r},\n'
              f'    .metatiles = gMetatiles_{r},\n'
              f'    .metatileAttributes = gMetatileAttributes_{r},\n'
              f'    .callback = NULL,\n}};\n')
    n = 0
    for caminho, bloco, chave, antes in (
            (f"{RAIZ}/src/data/tilesets/graphics.h", "\n" + graficos,
             f"const u32 gTilesetTiles_{r}[]", None),
            (f"{RAIZ}/src/data/tilesets/metatiles.h", "\n" + metas,
             f"const u16 gMetatiles_{r}[]", None),
            (f"{RAIZ}/src/data/tilesets/headers.h", "\n" + header,
             f"const struct Tileset gTileset_{r} =", None),
            (f"{RAIZ}/include/tilesets.h", f"extern const struct Tileset gTileset_{r};\n",
             f"extern const struct Tileset gTileset_{r};", "#endif //GUARD_tilesets_H")):
        tg2._insere(caminho, "\n" + MARCA + "\n", chave=MARCA, antes=antes)
        n += tg2._insere(caminho, bloco, chave=chave, antes=antes)
    return n


# --------------------------------------------------------------------- medicao

def kb_real(ts):
    """KB de ROM medidos com as ferramentas do proprio Makefile (gbagfx + smol).
    Cai para o cru se as ferramentas nao estiverem compiladas."""
    import subprocess
    import tempfile
    gfx = f"{RAIZ}/tools/gbagfx/gbagfx"
    smol = f"{RAIZ}/tools/compresSmol/compresSmol"
    fixo = len(ts["metatiles"]) + len(ts["atributos"]) + 16 * 32
    if not (os.path.exists(gfx) and os.path.exists(smol)):
        return (ts["n_tiles_enderecaveis"] * 32 + fixo) / 1024.0
    with tempfile.TemporaryDirectory() as d:
        png, bpp, out = f"{d}/t.png", f"{d}/t.4bpp", f"{d}/t.smol"
        Image.fromarray(ts["tiles_px"], mode="P").save(png)
        subprocess.run([gfx, png, bpp], check=True, capture_output=True)
        cmd = [smol, "-w", bpp, out] + ([] if ts["papel"] == "primario"
                                        else ["false", "false", "false"])
        subprocess.run(cmd, check=True, capture_output=True)
        return (os.path.getsize(out) + fixo) / 1024.0


# ------------------------------------------- decisao 3: reusar primario nosso?

def _pals_de(pasta):
    return [open(f"{pasta}/palettes/{p:02d}.pal").read().strip() for p in range(16)]


def compara_primarios(cat):
    """Decisao 3 do plano: primario do demake identico a um FRLG que ja temos =
    reusa o nosso. A identidade e ARTE + METATILES + PALETA (os atributos do
    repo ja passaram pelo conversor e os da fonte nao, entao comparalos so diria
    que a conversao existe). Comparacao no prefixo comum, porque o G0 corta o
    metatiles.bin no maior metatile que algum mapa usa."""
    nossos = sorted(d for d in glob.glob(f"{RAIZ}/data/tilesets/primary/*")
                    if os.path.isdir(d) and "galar_" not in os.path.basename(d))
    saida = {}
    for _nn, d, i in cat:
        if i["papel"] != "primario":
            continue
        px, _n = le_tiles_png(f"{d}/tiles.png")
        mt = open(f"{d}/metatiles.bin", "rb").read()
        pals = _pals_de(d)
        melhor, iguais_max = None, -1.0
        for outro in nossos:
            if not os.path.exists(f"{outro}/tiles.png"):
                continue
            qx, _q = le_tiles_png(f"{outro}/tiles.png")
            h = min(px.shape[0], qx.shape[0])
            frac = float((px[:h] == qx[:h]).mean())
            omt = open(f"{outro}/metatiles.bin", "rb").read()
            k = min(len(mt), len(omt))
            identico = (px.shape == qx.shape and (px == qx).all()
                        and mt[:k] == omt[:k] and pals == _pals_de(outro))
            if identico:
                melhor, iguais_max = os.path.basename(outro), 1.0
                break
            if frac > iguais_max:
                melhor, iguais_max = os.path.basename(outro), frac
        saida[i["endereco"]] = {
            "reusa_do_repo": melhor if iguais_max == 1.0 else None,
            "primario_do_repo_mais_parecido": melhor,
            "fracao_de_pixels_iguais": round(iguais_max, 4),
            "comparados": len(nossos),
        }
    return saida


# ------------------------------------------------------------------ censo

def monta_censo(convertidos, pulados, cat):
    de_para = {}
    for ts in convertidos:
        de_para[ts["endereco"]] = {
            "nome": nome_de(ts["nn"]), "rotulo": f"gTileset_{rotulo_de(ts['nn'])}",
            "pasta": pasta_rel(ts["nn"], ts["papel"]), "papel": ts["papel"],
            "papeis_de_uso": ts["papeis_de_uso"],
            "n_tiles": ts["n_tiles"], "n_metatiles": ts["n_metatiles"],
            "n_mapas": ts["n_mapas"], "animado": ts["animado"],
            "guard_entradas": ts["n_guard"], "guard_tile": ts["guard_tile"],
            "comportamentos_desconhecidos": ts["beh_desconhecidos"],
            "comportamentos_resgatados_porta": ts["beh_resgatados_porta"],
            "camadas_corrigidas": ts["camadas_corrigidas"],
        }
    return {
        "gerado_por": "dev_scripts/tileset_galar.py",
        "fonte": os.path.relpath(FONTE, os.path.dirname(RAIZ)),
        "primarios_do_demake": {
            ts["endereco"]: dict(nome=nome_de(ts["nn"]),
                                 **compara_primarios(cat)[ts["endereco"]])
            for ts in convertidos if ts["papel"] == "primario"},
        "papel_duplo": {
            "0x02D4A94": {"papel_adotado": "primario",
                          "usos_secundarios_degenerados": ["g42m03", "g42m09"],
                          "nota": "1 metatile distinto cada; o G2 NAO pode parear "
                                  "este tileset como secundario (.isSecondary=FALSE)"}},
        "nao_convertidos": pulados,
        "de_para": de_para,
    }


# ----------------------------------------------------- prova de fidelidade

class TilesetDoRepo:
    """O que o `renderiza_de_disco` do G0 espera, lido dos arquivos DO REPO."""

    def __init__(self, pasta):
        px, self.n_tiles = le_tiles_png(f"{pasta}/tiles.png")
        self.tiles = np.zeros((max(self.n_tiles, 1), 8, 8), dtype=np.uint8)
        for t in range(self.n_tiles):
            y, x = (t // 16) * 8, (t % 16) * 8
            self.tiles[t] = px[y:y + 8, x:x + 8]
        self.metatiles = np.frombuffer(open(f"{pasta}/metatiles.bin", "rb").read(),
                                       dtype="<u2").reshape(-1, 8).copy()
        self.paletas = []
        for p in range(16):
            linhas = open(f"{pasta}/palettes/{p:02d}.pal").read().split("\n")[3:19]
            self.paletas.append(np.array([[int(v) for v in l.split()] for l in linhas],
                                         dtype=np.uint8))
        self.info = {"animado": False}


def prova(n_amostra=10, fonte=FONTE):
    """Renderiza N mapas variados SO com os arquivos do repo e compara com o PNG
    de referencia do G0, pixel a pixel. O renderizador e o do G0, importado: se
    fosse outro, a prova estaria comparando dois erros."""
    cwd = os.getcwd()
    sys.path.insert(0, f"{os.path.dirname(RAIZ)}/fontes-mapas/galar-swsh")
    import extrai_tilesets_galar as g0     # noqa: E402  (faz chdir na importacao)
    os.chdir(cwd)

    censo = json.load(open(CENSO))["de_para"]
    grupos = json.load(open(f"{fonte}/mapas.json"))
    idx = {g0.chave_mapa(g, i): m for g, i, m in g0.mapas_novos(grupos)}

    # variedade = um mapa por tileset secundario, os mais ricos primeiro, e os
    # dois primarios obrigatoriamente representados.
    melhor = {}
    for chave, m in idx.items():
        t2 = m["layout"]["tileset2"]
        if t2 not in melhor or m["distintos"] > idx[melhor[t2]]["distintos"]:
            melhor[t2] = chave
    escolha = sorted(melhor.values(), key=lambda k: -idx[k]["distintos"])[:n_amostra]

    def garante(chaves):
        for c in chaves:
            if c and c not in escolha:
                escolha.append(c)

    # AMOSTRA POR RIQUEZA NAO PROVA O GUARD: os 11 tilesets com citacao de tile
    # inexistente sao pequenos e nao entram entre os mais ricos. Sao justamente
    # eles que podem desenhar sujeira, entao entram a forca.
    com_guard = {int(e, 16) for e, v in censo.items() if v["guard_entradas"]}
    garante(melhor.get(e) for e in sorted(com_guard))
    # e os dois primarios precisam aparecer
    for pri in sorted({m["layout"]["tileset1"] for m in idx.values()}):
        if pri not in {idx[k]["layout"]["tileset1"] for k in escolha}:
            cand = [k for k, m in idx.items() if m["layout"]["tileset1"] == pri]
            garante([max(cand, key=lambda k: idx[k]["distintos"])])

    cache, iguais, difs, pulados = {}, [], [], []
    for chave in escolha:
        m = idx[chave]
        ref = glob.glob(f"{fonte}/png/{chave}_*.png")
        ends = [f"0x{m['layout']['tileset1']:07X}", f"0x{m['layout']['tileset2']:07X}"]
        if not ref or any(e not in censo for e in ends):
            pulados.append((chave, "sem PNG" if not ref else "tileset nao convertido"))
            continue
        for e in ends:
            if e not in cache:
                cache[e] = TilesetDoRepo(f"{RAIZ}/{censo[e]['pasta']}")
        bd = open(f"{fonte}/blockdata/{chave}.bin", "rb").read()
        nosso = g0.renderiza_de_disco(m, cache[ends[0]], cache[ends[1]], bd)
        alvo = np.array(Image.open(ref[0]).convert("RGB"))
        if nosso.shape != alvo.shape:
            difs.append((chave, f"dimensao {nosso.shape} contra {alvo.shape}"))
        elif (nosso != alvo).any():
            difs.append((chave, f"{int((nosso != alvo).any(axis=2).sum())} px"))
        else:
            iguais.append(chave)

    print(f"\n== prova de fidelidade: {len(escolha)} mapas ({n_amostra} mais ricos "
          f"mais os {len(com_guard)} com guard), arquivos do REPO contra os PNGs "
          f"de referencia do G0 ==")
    for chave in sorted(escolha):
        m = idx[chave]
        marca = "OK  " if chave in iguais else "ERRO"
        motivo = dict(difs + pulados).get(chave, "pixel-identico")
        g = " guard" if m["layout"]["tileset2"] in com_guard else "      "
        print(f"  {marca} {chave:8} {m['layout']['w']:3d}x{m['layout']['h']:<3d} "
              f"{m['distintos']:3d} metatiles distintos  "
              f"pri 0x{m['layout']['tileset1']:07X} sec 0x{m['layout']['tileset2']:07X}"
              f"{g}  {motivo}")
    # MUTACAO: comparar duas imagens iguais e facil quando o comparador esta
    # quebrado. Mexer num metatile que o mapa USA tem que reprovar a comparacao.
    mutacao = "nao rodou (nenhum mapa bateu)"
    if iguais:
        chave = iguais[0]
        m = idx[chave]
        bd = np.frombuffer(open(f"{fonte}/blockdata/{chave}.bin", "rb").read(),
                           dtype="<u2") & 0x3FF
        alvo_mt = int(bd[bd >= PRIMARIO_METATILES].min()) - PRIMARIO_METATILES
        ts2 = cache[f"0x{m['layout']['tileset2']:07X}"]
        guarda = ts2.metatiles[alvo_mt].copy()
        try:
            ts2.metatiles[alvo_mt][0] ^= 0x07
            ref = np.array(Image.open(glob.glob(f"{fonte}/png/{chave}_*.png")[0])
                           .convert("RGB"))
            sujo = g0.renderiza_de_disco(m, cache[f"0x{m['layout']['tileset1']:07X}"],
                                         ts2, open(f"{fonte}/blockdata/{chave}.bin",
                                                   "rb").read())
            n = int((sujo != ref).any(axis=2).sum())
            mutacao = (f"OK, {n} px de diferenca em {chave} ao sujar o metatile "
                       f"{alvo_mt}" if n else "FALHOU: a mutacao passou")
            if not n:
                difs.append((chave, "mutacao nao pega"))
        finally:
            ts2.metatiles[alvo_mt] = guarda
    print(f"  mutacao do comparador: {mutacao}")

    animados = sorted(e for e, v in censo.items() if v["animado"])
    print(f"  {len(iguais)}/{len(escolha)} pixel-identicos, {len(difs)} divergentes, "
          f"{len(pulados)} pulados")
    print(f"  tilesets com callback de animacao na fonte ({len(animados)}), "
          f"desenhados parados aqui e no render de referencia: {', '.join(animados)}")
    return not difs and not pulados


# --------------------------------------------------------------------- demo

def demo(fonte=FONTE):
    falhas = []

    def checa(nome, obtido, esperado):
        ok = obtido == esperado
        print(f"  {'OK  ' if ok else 'ERRO'} {nome}: {obtido} (esperado {esperado})")
        if not ok:
            falhas.append(nome)

    cat = catalogo(fonte)
    convertidos = [(nn, d, i) for nn, d, i in cat if i["n_metatiles"] > 0]
    pulados = [(nn, d, i) for nn, d, i in cat if i["n_metatiles"] == 0]

    print("== contagens, contadas dos dois lados ==")
    checa("tilesets na fonte", len(cat), 48)
    checa("convertidos + pulados = fonte", len(convertidos) + len(pulados), len(cat))
    checa("pulados (0x2D4F8C, LZ77 anomalo)", [i["endereco"] for _n, _d, i in pulados],
          ["0x02D4F8C"])
    checa("primarios", sorted(i["endereco"] for _n, _d, i in convertidos
                              if i["papel"] == "primario"),
          ["0x02D4A94", "0x02D4BB4"])

    tss = [converte(nn, d, i) for nn, d, i in convertidos]
    por_end = {ts["endereco"]: ts for ts in tss}

    print("\n== primarios do demake contra os primarios FRLG que ja temos ==")
    cmp = compara_primarios(cat)
    for end, c in sorted(cmp.items()):
        print(f"  {end}: mais parecido e {c['primario_do_repo_mais_parecido']} com "
              f"{100 * c['fracao_de_pixels_iguais']:.1f}% dos pixels iguais "
              f"({c['comparados']} primarios comparados) -> "
              f"{'REUSA ' + c['reusa_do_repo'] if c['reusa_do_repo'] else 'ENTRA COMO NOVO'}")
    checa("primarios reusados do repo", [c["reusa_do_repo"] for c in cmp.values()],
          [None, None])
    # MUTACAO: comparar um primario do repo com ele mesmo TEM que dar reuso,
    # senao o comparador so sabe dizer "diferente".
    espelho = [(0, f"{RAIZ}/data/tilesets/primary/general_frlg",
                {"papel": "primario", "endereco": "0xESPELHO"})]
    checa("mutacao: general_frlg comparado consigo mesmo",
          compara_primarios(espelho)["0xESPELHO"]["reusa_do_repo"], "general_frlg")

    # --- os bytes gravados contra os extraidos, md5 a md5
    print("\n== md5 dos bins, la contra ca ==")
    def md5(b):
        return hashlib.md5(b).hexdigest()

    mt_iguais = mt_diferentes = pal_iguais = at_iguais = 0
    for nn, d, i in convertidos:
        ts = por_end[i["endereco"]]
        crus_mt = open(f"{d}/metatiles.bin", "rb").read()
        crus_at = open(f"{d}/metatile_attributes.bin", "rb").read()
        if md5(ts["metatiles"]) == md5(crus_mt):
            mt_iguais += 1
            assert ts["copia_metatiles"], f"{i['endereco']}: md5 igual mas bytes mudaram"
        else:
            mt_diferentes += 1
            assert ts["n_guard"], f"{i['endereco']}: md5 diferente sem guard aplicado"
        at_iguais += md5(ts["atributos"]) == md5(crus_at)
        pal_iguais += all(open(f"{d}/palettes/{p:02d}.pal").read()
                          == open(f"{d}/palettes/{p:02d}.pal").read() for p in range(16))
        assert len(ts["metatiles"]) == len(crus_mt) == ts["n_metatiles"] * 16
        assert len(ts["atributos"]) == len(crus_at) == ts["n_metatiles"] * 4
    com_guard = [ts for ts in tss if ts["n_guard"]]
    reescritos = [ts for ts in com_guard if not ts["copia_metatiles"]]
    checa("metatiles.bin com md5 identico ao extraido (conversao e copia)",
          mt_iguais, len(tss) - len(reescritos))
    checa("metatiles.bin alterados = tilesets em que o guard mudou byte",
          mt_diferentes, len(reescritos))
    checa("paletas identicas as extraidas", pal_iguais, len(tss))
    # atributo identico e legitimo: acontece no tileset cujos comportamentos, um
    # a um, tem o mesmo numero no FR e aqui. O que NAO pode e a conversao nao
    # mexer em nada, e por isso o teste e sobre o conjunto, nao sobre cada um.
    print(f"  ..   metatile_attributes.bin identicos ao extraido: {at_iguais} de "
          f"{len(tss)} (comportamento que coincide numero nos dois jogos)")
    checa("metatile_attributes.bin alterados pela conversao (tem que haver)",
          len(tss) - at_iguais > 0, True)
    checa("tamanhos: metatiles = n*16 e atributos = n*4 em todos", True, True)

    # --- guard
    print(f"\n== guard aplicado em {len(com_guard)} tilesets secundarios "
          f"({len(reescritos)} deles com byte reescrito) ==")
    for ts in sorted(com_guard, key=lambda t: t["endereco"]):
        assert ts["papel"] == "secundario", f"{ts['endereco']}: guard em primario"
        print(f"  {ts['endereco']} {nome_de(ts['nn']):9} {ts['n_tiles']:4d} tiles "
              f"(endereca ate {PRIMARIO_TILES + ts['n_tiles'] - 1:4d}), citacao ate "
              f"{ts['maior_tile_citado']:4d}, {ts['n_guard']:3d} entradas para o tile "
              f"vazio {ts['guard_tile']}, {ts['n_mapas']:3d} mapas"
              f"{'' if not ts['copia_metatiles'] else '  (ja caia no vazio, .bin intacto)'}")
    checa("tilesets com guard sao 11", len(com_guard), 11)
    # nenhum tile citado sobra fora do enderecavel depois do guard
    sobra = 0
    for ts in tss:
        if ts["papel"] != "secundario":
            continue
        e = np.frombuffer(ts["metatiles"], dtype="<u2") & 0x3FF
        sobra += int(((e >= PRIMARIO_TILES + ts["n_tiles_enderecaveis"])).sum())
    checa("citacoes fora do enderecavel apos o guard", sobra, 0)
    # MUTACAO: sem o guard as citacoes teriam sobrado
    antes = 0
    for _nn, d, i in convertidos:
        if i["papel"] != "secundario" or not i["n_tiles"]:
            continue
        e = np.frombuffer(open(f"{d}/metatiles.bin", "rb").read(), dtype="<u2") & 0x3FF
        antes += int((e >= PRIMARIO_TILES + por_end[i["endereco"]]["n_tiles_enderecaveis"]).sum())
    if antes == 0:
        falhas.append("mutacao do guard")
        print("  ERRO mutacao: sem o guard nada sobrava, entao o guard nao faz nada")
    else:
        print(f"  OK   mutacao: sem o guard sobrariam {antes} citacoes fora do tileset")

    # --- comportamentos
    print("\n== comportamentos convertidos ==")
    ig = sum(ts["beh_iguais"] for ts in tss)
    mu = sum(ts["beh_mudados"] for ts in tss)
    desc, resg = {}, {}
    for ts in tss:
        for v, n in ts["beh_desconhecidos"].items():
            desc[v] = desc.get(v, 0) + n
        for v, n in ts["beh_resgatados_porta"].items():
            resg[v] = resg.get(v, 0) + n
    n_desc = sum(desc.values())
    n_resg = sum(resg.values())
    total = sum(ts["n_metatiles"] for ts in tss)
    checa("iguais + remapeados + desconhecidos + resgatados = metatiles",
          ig + mu + n_desc + n_resg, total)
    print(f"  {total} metatiles: {ig} mantiveram o mesmo numero (o FR e o nosso "
          f"coincidem), {mu} remapeados para outro MB_*, {n_desc} fora da tabela "
          f"do FR -> MB_NORMAL")
    print(f"  {len(desc)} valores desconhecidos distintos, piores: "
          f"{sorted(desc.items(), key=lambda kv: -kv[1])[:6]}")
    # G5: o resgate estreito de porta (ver resgate_por_byte_baixo)
    print(f"  {n_resg} metatiles resgatados como PORTA pelo byte baixo, em "
          f"{len(resg)} valores: "
          f"{[(v, n, fr.FRLG_TO_EMERALD[fr.FRLG_BEHAVIORS[v & 0xFF]]) for v, n in sorted(resg.items())]}")
    # o resgate so pode devolver comportamento que dispara warp, nunca parede
    for v in resg:
        assert fr.FRLG_TO_EMERALD[fr.FRLG_BEHAVIORS[v & 0xFF]] in NOMES_QUE_DISPARAM, v
    # e ele e estreito: valor desconhecido que resolveria para algo que NAO e
    # porta continua desconhecido (senao 277 metatiles virariam IMPASSABLE_*)
    assert any(v > 0xFF and fr.FRLG_BEHAVIORS.get(v & 0xFF) for v in desc), \
        "o resgate deixou de ser estreito: nenhum desconhecido com byte baixo valido sobrou"
    # o conversor foi mesmo usado: um caso conhecido de cada lado
    assert fr.EMERALD_BEHAVIORS[fr.FRLG_TO_EMERALD["MB_FRLG_SIGNPOST"]] == 29
    assert fr.EMERALD_BEHAVIORS[fr.FRLG_TO_EMERALD["MB_FRLG_NORMAL"]] == 0
    # e ele mudou dado de verdade: cate um metatile cujo comportamento mudou
    achou = False
    for nn, d, i in convertidos:
        crus = struct.unpack("<%dI" % (i["n_metatiles"]),
                             open(f"{d}/metatile_attributes.bin", "rb").read())
        novo = struct.unpack("<%dI" % (i["n_metatiles"]), por_end[i["endereco"]]["atributos"])
        for a, b in zip(crus, novo):
            fa, fb = a & BEH_MASK, b & BEH_MASK
            if fa in fr.FRLG_BEHAVIORS and fa != fb:
                assert fb == fr.EMERALD_BEHAVIORS[fr.FRLG_TO_EMERALD[fr.FRLG_BEHAVIORS[fa]]]
                achou = True
                break
        if achou:
            break
    checa("um remapeamento conferido contra a tabela do conversor", achou, True)

    n_cam = sum(ts["camadas_corrigidas"] for ts in tss)
    print(f"  camada invalida (valor 3, que o `switch` do DrawMetatile nao "
          f"desenha) corrigida para NORMAL em {n_cam} metatiles")
    for ts in tss:
        for v in struct.unpack("<%dI" % ts["n_metatiles"], ts["atributos"]):
            assert ((v & LAYER_MASK) >> LAYER_SHIFT) in CAMADAS_VALIDAS
            assert (v & BEH_MASK) <= 255, f"{ts['endereco']}: comportamento > MB_INVALID"

    # --- custo
    print("\n== custo de ROM (gbagfx + compresSmol do repo) ==")
    kbs = [(kb_real(ts), ts) for ts in tss]
    tot = sum(k for k, _t in kbs)
    for k, ts in sorted(kbs, reverse=True, key=lambda kt: kt[0])[:5]:
        print(f"  {ts['endereco']} {nome_de(ts['nn']):9} {ts['papel']:10} "
              f"{ts['n_tiles']:4d} tiles {ts['n_metatiles']:4d} metatiles {k:7.1f} KB")
    print(f"  {len(tss)} tilesets, {tot:.1f} KB ({tot/1024:.2f} MB) com tiles ja comprimidos")

    print("\n== VERDE ==" if not falhas else f"\n== VERMELHO: {falhas} ==")
    return not falhas


# ------------------------------------------------------------------- execucao

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonte", default=FONTE)
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--gravar", action="store_true")
    ap.add_argument("--registrar", action="store_true")
    ap.add_argument("--prova", action="store_true")
    ap.add_argument("--n", type=int, default=10)
    a = ap.parse_args()

    if a.demo:
        return 0 if demo(a.fonte) else 1
    if a.prova and not (a.gravar or a.registrar):
        return 0 if prova(a.n, a.fonte) else 1

    cat = catalogo(a.fonte)
    convertidos, pulados = [], []
    for nn, d, i in cat:
        if i["n_metatiles"] == 0:
            pulados.append({"endereco": i["endereco"], "nn": nn,
                            "motivo": i.get("anomalia", "sem metatile"),
                            "mapas": i["mapas"]})
            continue
        ts = converte(nn, d, i)
        convertidos.append(ts)
        if a.gravar:
            grava(ts, d)
    if not a.gravar:
        print(f"{len(convertidos)} tilesets convertidos, {len(pulados)} pulados "
              f"(nada gravado; use --gravar)")
        return 0

    json.dump(monta_censo(convertidos, pulados, cat), open(CENSO, "w"),
              indent=1, ensure_ascii=False)
    print(f"{len(convertidos)} tilesets gravados, censo em {os.path.relpath(CENSO, RAIZ)}")
    if a.registrar:
        n = sum(registra(ts) for ts in convertidos)
        print(f"registro em C: {n} entradas novas nos 4 arquivos")
    if a.prova:
        return 0 if prova(a.n, a.fonte) else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
