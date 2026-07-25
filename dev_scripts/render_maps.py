#!/usr/bin/env python3
"""Renderiza cada mapa de data/maps/*/map.json em um PNG.

Le o layout do mapa, decodifica o map.bin (metatiles), resolve cada
metatile nos tilesets primario/secundario (tiles 8x8 em 4bpp + paletas
JASC-PAL), desenha as duas camadas (baixo e cima) e marca os
object_events com um retangulo vermelho.

Uso: python3 dev_scripts/render_maps.py [NomeDoMapa ...]
Sem argumentos, renderiza todos os mapas em data/maps/.
"""
import json
import os
import re
import struct
import sys

from PIL import Image, ImageDraw

REPO = os.environ.get("REPO_MAPAS", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_DIR = os.environ.get("SAIDA_MAPAS", os.path.join(REPO, "..", "..", "mapas-png"))

TILE_PX = 8
META_PX = 16
NUM_PALETAS_PRIMARIO = 6  # convencao pokeemerald: paletas 0-5 vem do tileset primario, 6-15 do secundario


def carregar_layouts():
    with open(os.path.join(REPO, "data/layouts/layouts.json"), encoding="utf-8") as f:
        dados = json.load(f)
    return {layout["id"]: layout for layout in dados["layouts"]}


_PADRAO_INCBIN = re.compile(
    r'const u32 gTilesetTiles_([A-Za-z0-9]+)\[\] = INCBIN_U32\("(data/tilesets/(?:primary|secondary)/[a-z0-9_/]+?)/tiles'
)


def carregar_mapa_de_pastas_tileset():
    """Le graphics.h/graphics.c e monta {rotulo_gTileset: pasta_real}.

    O nome da pasta em disco nao segue uma convencao simples a partir do
    label (ex.: gTileset_PokemonCenter -> data/tilesets/secondary/pokemon_center),
    entao a fonte da verdade e o INCBIN_U32 dos arquivos fonte do jogo.
    """
    mapa = {}
    for rel in ("src/data/tilesets/graphics.h", "src/graphics.c"):
        caminho = os.path.join(REPO, rel)
        if not os.path.exists(caminho):
            continue
        with open(caminho, encoding="utf-8") as f:
            for label, pasta in _PADRAO_INCBIN.findall(f.read()):
                mapa[label] = os.path.join(REPO, pasta)

    # o nome da struct Tileset (gTileset_X, usado em layouts.json) as vezes
    # difere do nome do array de tiles (gTilesetTiles_Y); headers.h liga os dois.
    caminho_headers = os.path.join(REPO, "src/data/tilesets/headers.h")
    if os.path.exists(caminho_headers):
        with open(caminho_headers, encoding="utf-8") as f:
            texto = f.read()
        for struct_nome, tiles_nome in re.findall(
            r"const struct Tileset gTileset_([A-Za-z0-9]+) =\s*\{[^}]*?\.tiles = gTilesetTiles_([A-Za-z0-9]+),",
            texto,
            re.DOTALL,
        ):
            if tiles_nome in mapa:
                mapa[struct_nome] = mapa[tiles_nome]
    return mapa


_MAPA_TILESETS = carregar_mapa_de_pastas_tileset()


def caminho_tileset(label):
    nome = label.replace("gTileset_", "")
    pasta = _MAPA_TILESETS.get(nome)
    if pasta is None:
        raise ValueError(f"tileset {label} nao encontrado em graphics.h/graphics.c")
    return pasta


def carregar_paleta(caminho_pal):
    with open(caminho_pal, encoding="utf-8") as f:
        linhas = [l.strip() for l in f if l.strip()]
    # linhas[0]="JASC-PAL", [1]="0100", [2]=contagem, resto = "r g b"
    cores = []
    for linha in linhas[3:]:
        r, g, b = (int(v) for v in linha.split())
        cores.append((r, g, b))
    return cores


def carregar_paletas(pasta_tileset):
    paletas = {}
    pasta_pal = os.path.join(pasta_tileset, "palettes")
    for nome in os.listdir(pasta_pal):
        if nome.endswith(".pal"):
            idx = int(os.path.splitext(nome)[0])
            paletas[idx] = carregar_paleta(os.path.join(pasta_pal, nome))
    return paletas


def carregar_tileset(label):
    """Carrega tiles.png (4bpp indexado, tira de tiles 8x8) e paletas de um tileset."""
    pasta = caminho_tileset(label)
    img = Image.open(os.path.join(pasta, "tiles.png")).convert("P")
    largura, altura = img.size
    n_col = largura // TILE_PX
    n_lin = altura // TILE_PX
    n_tiles = n_col * n_lin
    px = img.load()
    tiles = []
    for i in range(n_tiles):
        col = (i % n_col) * TILE_PX
        lin = (i // n_col) * TILE_PX
        tile = [[px[col + x, lin + y] for x in range(TILE_PX)] for y in range(TILE_PX)]
        tiles.append(tile)
    paletas = carregar_paletas(pasta)
    # variantes de secret base (blue_cave, tree, ...) nao tem metatiles.bin
    # proprio; ele fica compartilhado na pasta pai (secret_base/metatiles.bin).
    caminho_meta = os.path.join(pasta, "metatiles.bin")
    if not os.path.exists(caminho_meta):
        caminho_meta = os.path.join(os.path.dirname(pasta), "metatiles.bin")
    metatiles = open(caminho_meta, "rb").read()
    return {"tiles": tiles, "paletas": paletas, "metatiles": metatiles}


def entradas_metatile(metatiles_bin, indice_local):
    """8 entradas de 2 bytes (4 camada baixo + 4 camada cima) de um metatile."""
    off = indice_local * 16
    dados = metatiles_bin[off:off + 16]
    entradas = []
    for i in range(8):
        valor = struct.unpack_from("<H", dados, i * 2)[0]
        idx_tile = valor & 0x3FF
        flip_h = bool(valor & 0x400)
        flip_v = bool(valor & 0x800)
        paleta = (valor >> 12) & 0xF
        entradas.append((idx_tile, flip_h, flip_v, paleta))
    return entradas


def desenhar_tile(canvas_px, x0, y0, tile, cores, flip_h, flip_v):
    for y in range(TILE_PX):
        fy = TILE_PX - 1 - y if flip_v else y
        for x in range(TILE_PX):
            fx = TILE_PX - 1 - x if flip_h else x
            idx_cor = tile[fy][fx]
            if idx_cor == 0:
                continue  # cor 0 = transparente
            canvas_px[x0 + x, y0 + y] = cores[idx_cor % len(cores)]


def resolver_tile(ts_pri, ts_sec, idx_tile):
    if idx_tile < len(ts_pri["tiles"]):
        return ts_pri["tiles"][idx_tile]
    idx_sec = idx_tile - len(ts_pri["tiles"])
    if 0 <= idx_sec < len(ts_sec["tiles"]):
        return ts_sec["tiles"][idx_sec]
    return None


def renderizar_mapa(nome_mapa, layouts, cache_tilesets):
    pasta_mapa = os.path.join(REPO, "data/maps", nome_mapa)
    with open(os.path.join(pasta_mapa, "map.json"), encoding="utf-8") as f:
        mapa = json.load(f)

    layout = layouts.get(mapa["layout"])
    if layout is None:
        raise ValueError(f"layout {mapa['layout']} nao encontrado em layouts.json")

    largura, altura = layout["width"], layout["height"]
    bin_path = os.path.join(REPO, layout["blockdata_filepath"])
    map_bin = open(bin_path, "rb").read()

    chave_pri = layout["primary_tileset"]
    chave_sec = layout["secondary_tileset"]
    if chave_pri not in cache_tilesets:
        cache_tilesets[chave_pri] = carregar_tileset(chave_pri)
    if chave_sec not in cache_tilesets:
        cache_tilesets[chave_sec] = carregar_tileset(chave_sec)
    ts_pri = cache_tilesets[chave_pri]
    ts_sec = cache_tilesets[chave_sec]

    cor_fundo = ts_pri["paletas"][0][0]  # cor 0 da paleta 0 = backdrop compartilhado do BG
    canvas = Image.new("RGB", (largura * META_PX, altura * META_PX), cor_fundo)
    canvas_px = canvas.load()

    for i in range(largura * altura):
        valor = struct.unpack_from("<H", map_bin, i * 2)[0]
        idx_metatile = valor & 0x3FF
        tx, ty = i % largura, i // largura
        x0, y0 = tx * META_PX, ty * META_PX

        if idx_metatile < 512:
            ts_meta, idx_local = ts_pri, idx_metatile
        else:
            ts_meta, idx_local = ts_sec, idx_metatile - 512

        n_meta = len(ts_meta["metatiles"]) // 16
        if idx_local >= n_meta:
            continue  # metatile fora do range: deixa o quadro em preto

        entradas = entradas_metatile(ts_meta["metatiles"], idx_local)
        for camada in (0, 1):  # 0 = baixo, 1 = cima
            for q in range(4):
                idx_tile, flip_h, flip_v, idx_pal = entradas[camada * 4 + q]
                tile = resolver_tile(ts_pri, ts_sec, idx_tile)
                if tile is None:
                    continue
                # paletas 0-5 sao do tileset primario, 6-15 do secundario; os dois
                # arquivos trazem os 16 slots, mas so um lado tem a cor real.
                fonte_pal = ts_pri if idx_pal < NUM_PALETAS_PRIMARIO else ts_sec
                cores = fonte_pal["paletas"].get(idx_pal)
                if cores is None:
                    continue
                qx, qy = x0 + (q % 2) * TILE_PX, y0 + (q // 2) * TILE_PX
                desenhar_tile(canvas_px, qx, qy, tile, cores, flip_h, flip_v)

    draw = ImageDraw.Draw(canvas)
    for i, obj in enumerate(mapa.get("object_events", []), start=1):
        ox, oy = obj["x"] * META_PX, obj["y"] * META_PX
        draw.rectangle([ox, oy, ox + META_PX - 1, oy + META_PX - 1], outline=(255, 0, 0), width=1)
        draw.text((ox, oy - 8), str(i), fill=(255, 0, 0))

    out_path = os.path.join(OUT_DIR, f"{mapa['name']}.png")
    os.makedirs(OUT_DIR, exist_ok=True)
    canvas.save(out_path)
    return out_path


def main():
    layouts = carregar_layouts()
    cache_tilesets = {}

    if len(sys.argv) > 1:
        nomes = sys.argv[1:]
    else:
        pasta_maps = os.path.join(REPO, "data/maps")
        nomes = sorted(
            n for n in os.listdir(pasta_maps)
            if os.path.isfile(os.path.join(pasta_maps, n, "map.json"))
        )

    ok, falhas = 0, []
    for nome in nomes:
        try:
            caminho = renderizar_mapa(nome, layouts, cache_tilesets)
            ok += 1
            print(f"OK  {nome} -> {caminho}")
        except Exception as e:
            falhas.append((nome, str(e)))
            print(f"FAIL {nome}: {e}")

    print(f"\n{ok} mapas renderizados, {len(falhas)} falharam.")
    for nome, erro in falhas:
        print(f"  - {nome}: {erro}")


if __name__ == "__main__":
    main()
