#!/usr/bin/env python3
"""A esteira de carvão de Oreburgh volta a andar, com os quadros do próprio autor.

Uso:
    python3 dev_scripts/anima_esteira_oreburgh.py --verifica   # mede e confere, não escreve
    python3 dev_scripts/anima_esteira_oreburgh.py --aplicar    # grava quadros, C e callback

POR QUE ISSO EXISTE
-------------------
O Retro Platinum (blloop) anima as esteiras do pátio da mina: o
`gTileset_OreburghSouth` dele tem `.callback = InitTilesetAnim_Oreburgh`, que
reescreve os slots de VRAM 512 a 543 com três famílias de quadros
(`coal_orthogonal`, 8 tiles; `coal_slope_shallow`, 14; `coal_slope_steep`, 10),
oito quadros cada, trocando a cada 16 quadros de tela. Na cópia (commit
6e38e23876, `--sem-animacao`) a esteira ficou PARADA, e o PLANO-COPIA-SINNOH.md,
seção 11.3, deu o motivo: a ferramenta de cópia só sabe animar reservando a
faixa INTEIRA 432-511 do primário novo (80 slots), e Oreburgh ocupa 1.023 dos
1.024 slots. Isso é verdade da ferramenta, não do problema.

O QUE FOI MEDIDO (24/09/2026), e é o que torna o conserto de custo zero:

1. Nas 82 células da fonte que pedem os slots animados, o tile animado está
   SEMPRE na camada de cima e a do meio está vazia. Então o achatamento de
   três para duas camadas NÃO compôs nenhum tile animado com outro: cada um dos
   32 tiles animados do autor virou exatamente UM slot nosso, sem espelhamento,
   na paleta 10, com 0 pixel de diferença de cor no quadro 0.
2. Esses 32 slots não são usados por NENHUM outro metatile, e os metatiles que
   os usam não aparecem em nenhuma outra célula. Animar o slot anima só a
   esteira.
3. A paleta 10 nossa tem as MESMAS cores da paleta 10 dele, só que em outra
   ordem (o empacotador de paletas reordena). Todas as oito cores que os
   quadros 1 a 7 usam existem nela. Então cada quadro é convertido cor a cor,
   pelo RGB, sem aproximação nenhuma.

Resultado: nenhum slot novo, nenhum metatile novo, `map.bin` intocado. O que
entra é um callback que reescreve os 32 slots onde eles estão (seis trechos
contíguos, dois na fase 0 e quatro na fase 1, como o callback do autor) e oito
quadros de 32 tiles, 8.192 B de ROM.

A GUARDA: o quadro 0 convertido tem de ser BYTE A BYTE o que o `tiles.png` do
par já tem naqueles slots. Se alguém regerar o par com `copia_cidade_fonte.py
--aplicar`, os slots mudam de lugar e o `.callback` volta a NULL (a esteira para
de novo, sem pintar lixo); rode este script de novo com `--aplicar` e ele
recalcula tudo. `--verifica` reprova se o que está no disco não bate.
"""
import argparse
import os
import re
import struct
import sys

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTE_PADRAO = ("/Users/duarte/Projetos/pokemon-claude/fontes-mapas/romhacks/"
                "retro-platinum/fonte")

# A receita da fusão (copia_cidade_fonte.FUSOES["OreburghCity"]): o mapa sul do
# hack entra no nosso de 72x76 com a origem em (14,32).
SUL_X, SUL_Y = 14, 32
SUL_W, SUL_H = 58, 44
NOSSO_W = 72

# As três famílias do callback do autor (src/tileset_anims.c dele,
# QueueAnimTiles_Coal_*): primeiro slot de VRAM, quantos tiles e a FASE dentro
# do período de 16 (o ortogonal na fase 0, as duas rampas na fase 1).
FAMILIAS = [
    ("coal_orthogonal", 512, 8, 0),
    ("coal_slope_shallow", 520, 14, 1),
    ("coal_slope_steep", 534, 10, 1),
]
N_QUADROS = 8
PERIODO = 16
PAL_ANIM = 10

PASTA_QUADROS = "data/tilesets/secondary/oreburgh_retro_sec/anim/esteira"
MARCA_INI = "// ---- esteira de carvão de Oreburgh (dev_scripts/anima_esteira_oreburgh.py) ----"
MARCA_FIM = "// ---- fim da esteira de carvão de Oreburgh ----"


def tiles_png(caminho):
    im = Image.open(caminho)
    px = im.load()
    w, h = im.size
    return [bytes(px[tx * 8 + x, ty * 8 + y] & 15 for y in range(8) for x in range(8))
            for ty in range(h // 8) for tx in range(w // 8)]


def paletas(pasta):
    out = []
    for i in range(16):
        linhas = open(os.path.join(pasta, "palettes", "%02d.pal" % i)).read().split("\n")
        out.append([tuple(int(v) for v in linhas[3 + j].split()) for j in range(16)])
    return out


def palavras(caminho):
    b = open(caminho, "rb").read()
    return struct.unpack("<%dH" % (len(b) // 2), b)


def metatiles(caminho, n):
    w = palavras(caminho)
    return [w[i:i + n] for i in range(0, len(w), n)]


def espelha(t, h, v):
    return bytes(t[(7 - y if v else y) * 8 + (7 - x if h else x)]
                 for y in range(8) for x in range(8))


def cores(t, e, pals):
    p = pals[(e >> 12) & 15]
    return [p[i] if i else None for i in espelha(t, e & 0x400, e & 0x800)]


def mede(fonte):
    """Devolve (slots, quadros, relatorio). Recusa com SystemExit se algo não bater."""
    sp = os.path.join(fonte, "data/tilesets/primary/outdoor_oreburgh")
    ss = os.path.join(fonte, "data/tilesets/secondary/oreburgh_south")
    st = tiles_png(os.path.join(sp, "tiles.png"))
    src_tiles = st + [bytes(64)] * (512 - len(st)) + tiles_png(os.path.join(ss, "tiles.png"))
    src_pals = paletas(sp)[:6] + paletas(ss)[6:13]
    mp = metatiles(os.path.join(sp, "metatiles.bin"), 12)
    src_met = mp + [(0,) * 12] * (512 - len(mp)) + metatiles(os.path.join(ss, "metatiles.bin"), 12)
    sul = palavras(os.path.join(fonte, "data/layouts/OreburghCitySouth/map.bin"))

    op = os.path.join(RAIZ, "data/tilesets/primary/oreburgh_retro_prim")
    os_ = os.path.join(RAIZ, "data/tilesets/secondary/oreburgh_retro_sec")
    ot = tiles_png(os.path.join(op, "tiles.png"))
    nossos_tiles = ot + [bytes(64)] * (512 - len(ot)) + tiles_png(os.path.join(os_, "tiles.png"))
    nossas_pals = paletas(op)[:6] + paletas(os_)[6:13]
    om = metatiles(os.path.join(op, "metatiles.bin"), 8)
    nossos_met = om + [(0,) * 8] * (512 - len(om)) + metatiles(os.path.join(os_, "metatiles.bin"), 8)
    nosso_mapa = palavras(os.path.join(RAIZ, "data/layouts/OreburghCity/map.bin"))

    # quadros do autor, por slot de VRAM dele
    quadros_fonte = {}
    fase_do = {}
    for nome, base, n, fase in FAMILIAS:
        por_quadro = [tiles_png(os.path.join(ss, "anim", nome, "%02d.png" % k))[:n]
                      for k in range(N_QUADROS)]
        for i in range(n):
            quadros_fonte[base + i] = [por_quadro[k][i] for k in range(N_QUADROS)]
            fase_do[base + i] = fase
    for t, q in quadros_fonte.items():
        if q[0] != src_tiles[t]:
            raise SystemExit(f"o quadro 0 do slot {t} da fonte não é o tiles.png dela")

    animados = set(quadros_fonte)
    par = {}          # slot nosso -> slot animado da fonte
    celulas = []
    mets_esteira = set()
    for y in range(SUL_H):
        for x in range(SUL_W):
            ms = src_met[sul[y * SUL_W + x] & 0x3FF]
            if not any((e & 0x3FF) in animados for e in ms):
                continue
            if any((e & 0x3FF) in animados for e in ms[:8]):
                raise SystemExit(f"({x},{y}) da fonte tem tile animado fora da camada de "
                                 f"cima: o achatamento compôs, e este script não sabe")
            X, Y = x + SUL_X, y + SUL_Y
            mid = nosso_mapa[Y * NOSSO_W + X] & 0x3FF
            mets_esteira.add(mid)
            celulas.append((X, Y))
            mn = nossos_met[mid]
            for q in range(4):
                es = ms[8 + q]
                if (es & 0x3FF) not in animados:
                    continue
                eo = mn[4 + q]
                a = cores(src_tiles[es & 0x3FF], es, src_pals)
                b = cores(nossos_tiles[eo & 0x3FF], eo, nossas_pals)
                if a != b:
                    raise SystemExit(f"célula ({X},{Y}) quadrante {q}: o nosso tile não é o "
                                     f"do autor no quadro 0")
                if (es ^ eo) & 0xC00 or (eo >> 12) & 15 != PAL_ANIM:
                    raise SystemExit(f"célula ({X},{Y}): espelhamento ou paleta diferente")
                s = eo & 0x3FF
                if par.setdefault(s, es & 0x3FF) != (es & 0x3FF):
                    raise SystemExit(f"slot {s} serve a dois tiles animados diferentes")
    if sorted(par.values()) != sorted(animados):
        faltam = sorted(animados - set(par.values()))
        raise SystemExit(f"tiles animados do autor sem slot nosso: {faltam}")

    # nenhum outro metatile pode usar esses slots, nem esses metatiles outra célula
    for mi, m in enumerate(nossos_met):
        if mi in mets_esteira:
            continue
        for e in m:
            if (e & 0x3FF) in par:
                raise SystemExit(f"o metatile {mi} (fora da esteira) usa o slot {e & 0x3FF}")
    cel = set(celulas)
    for i, v in enumerate(nosso_mapa):
        if (v & 0x3FF) in mets_esteira and (i % NOSSO_W, i // NOSSO_W) not in cel:
            raise SystemExit(f"metatile {v & 0x3FF} da esteira fora dela, em "
                             f"({i % NOSSO_W},{i // NOSSO_W})")

    # conversão cor a cor para a paleta 10 nossa
    pal_n = nossas_pals[PAL_ANIM]
    pal_f = src_pals[PAL_ANIM]
    idx_da_cor = {}
    for i in range(1, 16):
        idx_da_cor.setdefault(pal_n[i], i)
    if len(idx_da_cor) != 15:
        raise SystemExit("a paleta 10 nossa tem cor repetida: a conversão seria ambígua")

    def converte(t):
        out = []
        for i in t:
            if i == 0:
                out.append(0)
            elif pal_f[i] in idx_da_cor:
                out.append(idx_da_cor[pal_f[i]])
            else:
                raise SystemExit(f"cor {pal_f[i]} do quadro não existe na paleta 10 nossa")
        return bytes(out)

    slots = sorted(par)
    quadros = []
    for k in range(N_QUADROS):
        quadros.append([converte(quadros_fonte[par[s]][k]) for s in slots])
    for j, s in enumerate(slots):
        if quadros[0][j] != nossos_tiles[s]:
            raise SystemExit(f"o quadro 0 convertido do slot {s} não é o tiles.png do par")
    fases = [fase_do[par[s]] for s in slots]
    difs = [sum(1 for j in range(len(slots)) for p in range(64)
                if quadros[k][j][p] != quadros[0][j][p]) for k in range(N_QUADROS)]
    relatorio = {
        "celulas": len(celulas), "metatiles": len(mets_esteira), "slots": slots,
        "fases": fases, "pixels_diferentes_do_quadro_0": difs,
    }
    return slots, fases, quadros, relatorio


def trechos(slots, fases):
    """[(slot inicial, índice no quadro, quantos, fase)], contíguos e de mesma fase."""
    out = []
    for j, (s, f) in enumerate(zip(slots, fases)):
        if out and out[-1][0] + out[-1][2] == s and out[-1][3] == f:
            a = out[-1]
            out[-1] = (a[0], a[1], a[2] + 1, f)
        else:
            out.append((s, j, 1, f))
    return out


def imagem_quadro(tiles, paleta):
    ncol = 16
    nlin = (len(tiles) + ncol - 1) // ncol
    im = Image.new("P", (ncol * 8, nlin * 8), 0)
    flat = []
    for c in paleta:
        flat += list(c)
    im.putpalette(flat + [0] * (768 - len(flat)))
    px = im.load()
    for j, t in enumerate(tiles):
        tx, ty = (j % ncol) * 8, (j // ncol) * 8
        for p in range(64):
            px[tx + p % 8, ty + p // 8] = t[p]
    return im


def bloco_c(slots, fases, trs):
    linhas = [MARCA_INI,
              "// A esteira do pátio da mina, com os oito quadros do Retro Platinum (blloop),",
              "// gTileset_OreburghSouth dele. Os 32 tiles animados moram onde a cópia os pôs",
              "// (seis trechos de slot), e não numa faixa reservada: por isso o conserto não",
              "// custa slot nenhum. Gerado pelo script do cabeçalho; não editar à mão.",
              ]
    for k in range(N_QUADROS):
        linhas.append(f'const u16 gTilesetAnims_OreburghRetro_Esteira_Frame{k}[] = '
                      f'INCBIN_U16("{PASTA_QUADROS}/{k:02d}.4bpp");')
    linhas += ["", "const u16 *const gTilesetAnims_OreburghRetro_Esteira[] = {"]
    linhas += [f"    gTilesetAnims_OreburghRetro_Esteira_Frame{k}," for k in range(N_QUADROS)]
    linhas += ["};", "",
               "// {primeiro slot de VRAM, índice do primeiro tile no quadro, quantos, fase}",
               "static const u16 sOreburghRetro_EsteiraTrechos[][4] = {"]
    linhas += [f"    {{{a}, {b}, {c}, {d}}}," for a, b, c, d in trs]
    linhas += ["};", "",
               "static void TilesetAnim_OreburghRetro(u16 timer)",
               "{",
               "    u32 i;",
               f"    u16 fase = timer % {PERIODO};",
               f"    u16 q = (timer / {PERIODO}) % ARRAY_COUNT(gTilesetAnims_OreburghRetro_Esteira);",
               "",
               "    for (i = 0; i < ARRAY_COUNT(sOreburghRetro_EsteiraTrechos); i++)",
               "    {",
               "        if (sOreburghRetro_EsteiraTrechos[i][3] != fase)",
               "            continue;",
               "        AppendTilesetAnimToBuffer(gTilesetAnims_OreburghRetro_Esteira[q]",
               "                                      + sOreburghRetro_EsteiraTrechos[i][1] * (TILE_SIZE_4BPP / 2),",
               "                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(sOreburghRetro_EsteiraTrechos[i][0])),",
               "                                  sOreburghRetro_EsteiraTrechos[i][2] * TILE_SIZE_4BPP);",
               "    }",
               "}",
               "",
               "void InitTilesetAnim_OreburghRetro(void)",
               "{",
               "    sSecondaryTilesetAnimCounter = 0;",
               "    sSecondaryTilesetAnimCounterMax = 256;",
               "    sSecondaryTilesetAnimCallback = TilesetAnim_OreburghRetro;",
               "}",
               MARCA_FIM]
    return "\n".join(linhas) + "\n"


def aplica_c(texto_bloco, escreve):
    caminho = os.path.join(RAIZ, "src/tileset_anims.c")
    s = open(caminho).read()
    if MARCA_INI in s:
        ini = s.index(MARCA_INI)
        fim = s.index(MARCA_FIM) + len(MARCA_FIM) + 1
        novo = s[:ini] + texto_bloco + s[fim:]
    else:
        novo = s.rstrip("\n") + "\n\n" + texto_bloco
    if escreve:
        open(caminho, "w").write(novo)
    return novo == s


def aplica_h(escreve):
    ok = True
    caminho = os.path.join(RAIZ, "include/tileset_anims.h")
    s = open(caminho).read()
    decl = "void InitTilesetAnim_OreburghRetro(void);"
    if decl not in s:
        ok = False
        ancora = "void InitTilesetAnim_FloaromaRetro(void);"
        s = s.replace(ancora, ancora + "\n" + decl)
        if escreve:
            open(caminho, "w").write(s)
    caminho = os.path.join(RAIZ, "src/data/tilesets/headers.h")
    s = open(caminho).read()
    padrao = re.compile(r"(const struct Tileset gTileset_OreburghRetroSec =\s*\{.*?\.callback = )([^,]*)(,)",
                        re.S)
    m = padrao.search(s)
    if not m:
        raise SystemExit("gTileset_OreburghRetroSec não achado em headers.h")
    if m.group(2) != "InitTilesetAnim_OreburghRetro":
        ok = False
        s = padrao.sub(r"\1InitTilesetAnim_OreburghRetro\3", s, count=1)
        if escreve:
            open(caminho, "w").write(s)
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--fonte", default=FONTE_PADRAO)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--verifica", action="store_true")
    g.add_argument("--aplicar", action="store_true")
    a = ap.parse_args()

    slots, fases, quadros, rel = mede(a.fonte)
    trs = trechos(slots, fases)
    print(f"células da esteira: {rel['celulas']}, metatiles nossos: {rel['metatiles']}")
    print(f"slots animados: {len(slots)} em {len(trs)} trechos: "
          + ", ".join(f"{s}..{s + n - 1} (fase {f})" for s, _, n, f in trs))
    print("pixels que mudam contra o quadro 0, por quadro: "
          + " ".join(str(d) for d in rel["pixels_diferentes_do_quadro_0"]))

    pal = paletas(os.path.join(RAIZ, "data/tilesets/secondary/oreburgh_retro_sec"))[PAL_ANIM]
    pasta = os.path.join(RAIZ, PASTA_QUADROS)
    divergem = []
    for k in range(N_QUADROS):
        caminho = os.path.join(pasta, f"{k:02d}.png")
        if a.aplicar:
            os.makedirs(pasta, exist_ok=True)
            imagem_quadro(quadros[k], pal).save(caminho)
        if not os.path.exists(caminho) or tiles_png(caminho)[:len(slots)] != quadros[k]:
            divergem.append(caminho)
    igual_c = aplica_c(bloco_c(slots, fases, trs), a.aplicar)
    igual_h = aplica_h(a.aplicar)
    if a.aplicar:
        print("APLICADO: quadros em", PASTA_QUADROS, "e callback InitTilesetAnim_OreburghRetro")
        return 0
    falhas = divergem + ([] if igual_c else ["src/tileset_anims.c"]) + \
        ([] if igual_h else ["headers.h / tileset_anims.h"])
    if falhas:
        print("REPROVA: desatualizado:", ", ".join(falhas))
        return 1
    print("CONFERE: quadros, trechos e callback batem com o par de hoje")
    return 0


if __name__ == "__main__":
    sys.exit(main())
