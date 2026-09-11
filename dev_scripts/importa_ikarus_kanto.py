#!/usr/bin/env python3
"""Traz a arte do Ikarus' Tileset Patch v3.2 para a Kanto deste repositório.

Uso:
    python3 dev_scripts/importa_ikarus_kanto.py --medir    # só relatório, não escreve
    python3 dev_scripts/importa_ikarus_kanto.py --aplicar  # escreve os arquivos

O QUE ISSO É
------------
O Ikarus é um patch IPS de TILESET sobre a FireRed 1.0 (BPRE, sha1
41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc), com gráficos de gen 4. Ele não é um
hack de história: o que ele troca é arte de tileset e o desenho (blockdata) dos
mapas externos de Kanto e das Sevii. A planta continua a oficial: nenhum mapa
muda de tamanho.

Como a fonte é uma ROM e não um decomp, tudo aqui é RIPADO da ROM patchada e
comparado com a ROM limpa, byte a byte. O de-para de "qual tileset é qual" não
foi adivinhado pelo nome: veio dos símbolos do `pokefirered.map` do pret, que dá
o endereço de cada `gTileset_*`, e da leitura do cabeçalho de 24 bytes
(isCompressed, isSecondary, tiles, palettes, metatiles, callback,
metatileAttributes) nas duas ROMs.

O QUE ENTRA E O QUE FICA NOSSO
------------------------------
- tiles.png, paletas, metatiles.bin: do Ikarus, inteiros.
- metatile_attributes.bin: do Ikarus, com o COMPORTAMENTO traduzido da
  numeração da FireRed para a nossa. Os outros campos (terreno, tipo de
  encontro, layerType, bit 31) passam intactos.
- map.bin e border.bin: do Ikarus, nos mapas em que ele redesenhou.
- Warps, NPCs, gatilhos, scripts, conexões, encontros: nossos, intocados.

PALETAS
-------
Só se escreve a faixa que o tileset realmente carrega: primário FRLG usa 0..6
(NUM_PALS_IN_PRIMARY_FRLG = 7), secundário usa 7..12. As outras ficam como
estão, porque o motor nem as lê nesse slot.
"""
import json
import os
import re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTES = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas"
ROM_LIMPA = f"{FONTES}/pokefirered/pokefirered.gba"
MAPFILE = f"{FONTES}/pokefirered/pokefirered.map"
ROM_IKARUS = f"{FONTES}/romhacks/ikarus-tileset-v3.2/firered-ikarus-v3.2.gba"

SHA1_BASE = "41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc"
MD5_IKARUS = "958ecefa1bb999e3f95d0890f380fffe"

# de-para medido: simbolo do pokefirered  ->  pasta deste repositorio
TILESETS = {
    "gTileset_General":         "primary/general_frlg",
    "gTileset_PalletTown":      "secondary/pallet_town_frlg",
    "gTileset_ViridianCity":    "secondary/viridian_city_frlg",
    "gTileset_PewterCity":      "secondary/pewter_city_frlg",
    "gTileset_CeruleanCity":    "secondary/cerulean_city_frlg",
    "gTileset_LavenderTown":    "secondary/lavender_town_frlg",
    "gTileset_VermilionCity":   "secondary/vermilion_city_frlg",
    "gTileset_CeladonCity":     "secondary/celadon_city_frlg",
    "gTileset_FuchsiaCity":     "secondary/fuchsia_city_frlg",
    "gTileset_CinnabarIsland":  "secondary/cinnabar_island_frlg",
    "gTileset_IndigoPlateau":   "secondary/indigo_plateau_frlg",
    "gTileset_SaffronCity":     "secondary/saffron_city_frlg",
    "gTileset_Cave":            "secondary/cave_frlg",
    "gTileset_ViridianForest":  "secondary/viridian_forest_frlg",
    "gTileset_SeafoamIslands":  "secondary/seafoam_islands_frlg",
    "gTileset_CeruleanCave":    "secondary/cerulean_cave_frlg",
    "gTileset_MtEmber":         "secondary/mt_ember_frlg",
    "gTileset_BerryForest":     "secondary/berry_forest_frlg",
    "gTileset_NavelRock":       "secondary/navel_rock_frlg",
    "gTileset_SeviiIslands123": "secondary/sevii_islands_123_frlg",
    "gTileset_SeviiIslands45":  "secondary/sevii_islands_45_frlg",
    "gTileset_SeviiIslands67":  "secondary/sevii_islands_67_frlg",
    "gTileset_SSAnne":          "secondary/ss_anne_frlg",
    "gTileset_IslandHarbor":    "secondary/island_harbor_frlg",
    "gTileset_RockTunnel":      "secondary/rock_tunnel_frlg",
}

# Saffron: este projeto ja tinha mexido em 4 celulas (2x2 em 18,13). Elas sao
# reaplicadas por cima do desenho do Ikarus, senao a copia apaga a nossa porta.
NOSSAS_CELULAS = {"SaffronCity_Frlg": [(18, 13), (19, 13), (18, 14), (19, 14)]}

BEHAVIOR_MASK = 0x000001FF

# De-para de comportamento, FireRed -> este motor. NÃO foi escrito à mão: saiu de
# comparar os 61 tilesets `*_frlg` desta árvore com a FireRed limpa, e é uma
# FUNÇÃO (nenhum valor da FireRed cai em dois nossos). A prova de que está
# completo e certo é dura: aplicando esta tabela aos atributos da ROM limpa,
# saem BYTE A BYTE os 10.255 atributos de metatile que esta árvore já tem hoje,
# com ZERO divergência. Os 50 comportamentos que o Ikarus usa estão todos aqui.
DEPARA_BEHAVIOR = {
    0x011: 0x02c, 0x01b: 0x02d, 0x020: 0x023, 0x023: 0x020, 0x02a: 0x04f,
    0x02b: 0x000, 0x066: 0x00f, 0x06c: 0x0eb, 0x06d: 0x0ec, 0x06e: 0x0ed,
    0x06f: 0x0ee, 0x071: 0x070, 0x081: 0x0e1, 0x082: 0x0e2, 0x084: 0x01d,
    0x087: 0x01e, 0x088: 0x01f, 0x089: 0x059, 0x08a: 0x05a, 0x08b: 0x05b,
    0x08d: 0x05d, 0x08e: 0x05e, 0x091: 0x0a1, 0x092: 0x0a2, 0x093: 0x0a3,
    0x094: 0x0a4, 0x095: 0x0a5, 0x096: 0x0a6, 0x097: 0x0a7, 0x098: 0x0a8,
    0x099: 0x0a9, 0x09a: 0x0e4, 0x09b: 0x0ac, 0x09c: 0x0aa, 0x09d: 0x0ab,
    0x09e: 0x0ad, 0x09f: 0x0ae, 0x0a2: 0x0cb, 0x0a3: 0x0cc, 0x0d0: 0x0c8,
    0x0d1: 0x0c9,
}

# comportamentos que a FireRed e este motor numeram igual (medido na mesma
# comparacao). Um valor fora destes dois conjuntos e erro, nao conveniencia.
COMPORTAMENTOS_IDENTICOS = {
    0x00, 0x02, 0x08, 0x0c, 0x10, 0x13, 0x15, 0x16, 0x17, 0x21, 0x26, 0x27,
    0x28, 0x30, 0x31, 0x32, 0x33, 0x38, 0x39, 0x3b, 0x50, 0x51, 0x52, 0x53,
    0x54, 0x55, 0x56, 0x57, 0x58, 0x60, 0x61, 0x62, 0x63, 0x64, 0x65, 0x67,
    0x69, 0x6a, 0x6b, 0x80, 0x85, 0x86, 0x8f, 0xc0, 0xe0, 0xe1, 0xe3,
}


def lz77(data, off):
    assert data[off] == 0x10, f"nao e LZ77 em {off:#x}"
    size = int.from_bytes(data[off + 1:off + 4], "little")
    out = bytearray()
    p = off + 4
    while len(out) < size:
        flags = data[p]
        p += 1
        for i in range(8):
            if len(out) >= size:
                break
            if flags & (0x80 >> i):
                b1, b2 = data[p], data[p + 1]
                p += 2
                n = (b1 >> 4) + 3
                disp = ((b1 & 0xF) << 8) | b2
                start = len(out) - disp - 1
                for k in range(n):
                    out.append(out[start + k])
            else:
                out.append(data[p])
                p += 1
    return bytes(out[:size])


def simbolos():
    s = {}
    with open(MAPFILE, errors="ignore") as fh:
        for line in fh:
            m = re.match(r"\s+0x0([0-9a-f]{7})\s+([A-Za-z_][A-Za-z0-9_]*)\s*$", line)
            if m:
                s.setdefault(m.group(2), int(m.group(1), 16))
    return s


def cabecalho(rom, addr):
    o = addr - 0x8000000
    t, p, mt, cb, at = struct.unpack_from("<5I", rom, o + 4)
    return dict(comp=rom[o], sec=rom[o + 1], tiles=t, pals=p, meta=mt, cb=cb, attrs=at)


def gbapal_para_jasc(b):
    linhas = ["JASC-PAL", "0100", "16"]
    for i in range(16):
        v = int.from_bytes(b[i * 2:i * 2 + 2], "little")
        comp = lambda c: (c << 3) | (c >> 2)
        linhas.append(f"{comp(v & 31)} {comp((v >> 5) & 31)} {comp((v >> 10) & 31)}")
    return "\r\n".join(linhas) + "\r\n"


def escreve_tiles_png(caminho, tiles, pal_gba):
    from PIL import Image
    n = len(tiles) // 32
    linhas = (n + 15) // 16
    im = Image.new("P", (128, linhas * 8), 0)
    paleta = []
    for i in range(16):
        v = int.from_bytes(pal_gba[i * 2:i * 2 + 2], "little")
        comp = lambda c: (c << 3) | (c >> 2)
        paleta += [comp(v & 31), comp((v >> 5) & 31), comp((v >> 10) & 31)]
    im.putpalette(paleta + [0] * (768 - len(paleta)))
    px = im.load()
    for t in range(n):
        tx, ty = (t % 16) * 8, (t // 16) * 8
        base = t * 32
        for y in range(8):
            for x in range(0, 8, 2):
                b = tiles[base + y * 4 + x // 2]
                px[tx + x, ty + y] = b & 15
                px[tx + x + 1, ty + y] = b >> 4
    im.save(caminho)
    return n, linhas * 8


def main():
    modo = sys.argv[1] if len(sys.argv) > 1 else "--medir"
    aplica = modo == "--aplicar"
    limpa = open(ROM_LIMPA, "rb").read()
    ika = open(ROM_IKARUS, "rb").read()
    sym = simbolos()

    relatorio = []
    conflitos = []
    for s, pasta in TILESETS.items():
        dst = f"{RAIZ}/data/tilesets/{pasta}"
        hl, hi = cabecalho(limpa, sym[s]), cabecalho(ika, sym[s])
        nosso_attr = open(f"{dst}/metatile_attributes.bin", "rb").read()
        n_nosso = len(nosso_attr) // 4
        repontado = hl["meta"] != hi["meta"]
        n_novo = (hi["attrs"] - hi["meta"]) // 16 if repontado else n_nosso
        assert 0 < n_novo <= (640 if hi["sec"] == 0 else 384), (s, n_novo)

        om, oa = hi["meta"] - 0x8000000, hi["attrs"] - 0x8000000
        meta = ika[om:om + n_novo * 16]
        attr = bytearray(ika[oa:oa + n_novo * 4])
        # traduz o comportamento da numeracao da FireRed para a nossa
        traduzidos = 0
        desconhecidos = []
        for i in range(n_novo):
            w = int.from_bytes(attr[i * 4:i * 4 + 4], "little")
            b = w & BEHAVIOR_MASK
            if b in DEPARA_BEHAVIOR:
                attr[i * 4:i * 4 + 4] = ((w & ~BEHAVIOR_MASK) | DEPARA_BEHAVIOR[b]).to_bytes(4, "little")
                traduzidos += 1
            elif b not in COMPORTAMENTOS_IDENTICOS:
                desconhecidos.append((i, b))
        conflitos.extend((s, i, b) for i, b in desconhecidos)

        tiles = lz77(ika, hi["tiles"] - 0x8000000) if hi["comp"] else None
        pal_ini, pal_fim = (0, 7) if hi["sec"] == 0 else (7, 13)
        op = hi["pals"] - 0x8000000
        n_tiles = len(tiles) // 32

        relatorio.append(dict(sym=s, pasta=pasta, sec=hi["sec"], nmeta_antes=n_nosso,
                              nmeta=n_novo, ntiles=n_tiles, preservados=traduzidos,
                              repontado=repontado))
        if aplica:
            open(f"{dst}/metatiles.bin", "wb").write(meta)
            open(f"{dst}/metatile_attributes.bin", "wb").write(bytes(attr))
            for i in range(pal_ini, pal_fim):
                open(f"{dst}/palettes/{i:02d}.pal", "w", newline="").write(
                    gbapal_para_jasc(ika[op + i * 32:op + i * 32 + 32]))
            escreve_tiles_png(f"{dst}/tiles.png", tiles, ika[op + pal_ini * 32:op + pal_ini * 32 + 32])

    # ---- mapas ----
    lay = json.load(open(f"{RAIZ}/data/layouts/layouts.json"))
    byid = {l["id"]: l for l in lay["layouts"] if l}
    mg = json.load(open(f"{RAIZ}/data/maps/map_groups.json"))
    nomes = [m for g, v in mg.items() if isinstance(v, list) for m in v]
    mapas = []
    for m in nomes:
        p = f"{RAIZ}/data/maps/{m}/map.json"
        if not os.path.exists(p):
            continue
        j = json.load(open(p))
        l = byid.get(j["layout"])
        if not l or l["primary_tileset"] != "gTileset_General_Frlg":
            continue
        stem = os.path.basename(os.path.dirname(l["blockdata_filepath"]))
        v = stem[:-5] if stem.endswith("_Frlg") else stem
        for arq, suf in (("map.bin", "Blockdata"), ("border.bin", "Border")):
            s = f"{v}_Layout_{suf}"
            if s not in sym:
                continue
            alvo = f"{RAIZ}/data/layouts/{stem}/{arq}"
            nosso = open(alvo, "rb").read()
            o = sym[s] - 0x8000000
            van, novo = limpa[o:o + len(nosso)], bytearray(ika[o:o + len(nosso)])
            if van == novo:
                continue
            for (cx, cy) in NOSSAS_CELULAS.get(stem, []) if arq == "map.bin" else []:
                i = (cy * l["width"] + cx) * 2
                novo[i:i + 2] = nosso[i:i + 2]
            mapas.append((stem, arq, sum(1 for a, b in zip(van, novo) if a != b),
                          nosso != van))
            if aplica:
                open(alvo, "wb").write(bytes(novo))

    # ---- relatorio ----
    print(f"{'tileset':28s} {'pasta':34s} sec {'nmeta':>12s} {'ntiles':>7s} {'traduzidos':>11s}")
    for r in relatorio:
        mm = f"{r['nmeta_antes']}->{r['nmeta']}"
        print(f"{r['sym']:28s} {r['pasta']:34s} {r['sec']:3d} {mm:>12s} {r['ntiles']:7d} {r['preservados']:11d}")
    print(f"\ntilesets: {len(relatorio)}   mapas com desenho novo: {len(mapas)}")
    print(f"comportamentos traduzidos: {sum(r['preservados'] for r in relatorio)}")
    print(f"COMPORTAMENTOS DA FIRERED SEM DE-PARA (tem de ser 0): {len(conflitos)}")
    for c in conflitos[:30]:
        print(f"   {c[0]} idx {c[1]}: comportamento {c[2]:#x} desconhecido")
    print("\nmapas (arquivo, bytes trocados, ja divergia de vanilla):")
    for m in mapas:
        print(f"   {m[0]:36s} {m[1]:10s} {m[2]:6d} {'NOSSO JA DIVERGIA' if m[3] else ''}")
    print("\nMODO:", "APLICADO" if aplica else "so medicao")


if __name__ == "__main__":
    main()
