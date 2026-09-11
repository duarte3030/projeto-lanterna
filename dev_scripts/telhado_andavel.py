#!/usr/bin/env python3
"""Célula ANDÁVEL em que o jogador é desenhado POR CIMA da arte, e o conserto.

Resposta 98 do condutor Fable, de 11/09/2026: "jogador em pé sobre telhado é
defeito do autor, não desenho; célula de telhado vira sólida".

## Por que a célula existe

O conserto de `layerType` da seção 7.2 do caderno da frente troca, nas células
ANDÁVEIS, o tipo de metatile de NORMAL/SPLIT para COVERED. `DrawMetatile`
(`src/field_camera.c`, lido em 11/09/2026) manda:

  * NORMAL e SPLIT: camada de cima no **BG1**, que fica ACIMA de todo sprite de
    overworld, ou seja o jogador SOME debaixo dela;
  * COVERED: camada de cima no **BG2**, que fica ABAIXO dos sprites, ou seja o
    jogador aparece EM CIMA dela.

Para passadiço, ponte e vão de porta isso é o certo: o jogador anda por cima e
se vê. Para TELHADO é errado nos dois sentidos, e o defeito é do autor do hack,
não da conversão: ele deixou colisão 0 numa célula de telhado, e no jogo dele o
jogador some lá em vez de aparecer. Nenhuma das duas é o que se quer. O conserto
é fechar a colisão.

## O que este script faz

1. `--lente`: lista toda célula andável cuja camada de CIMA desenha e cujo
   `layerType` é COVERED, e grava um render do mapa com essas células marcadas
   em vermelho. É a evidência que decide, célula a célula, o que é telhado e o
   que é passadiço: não existe regra de pixel que separe os dois, então quem
   separa é olho humano olhando a marca.
2. `--fecha`: lê a tabela `dev_scripts/telhados_sinnoh_retro.json` (por cidade,
   uma lista de metatiles e/ou de células) e põe colisão 1 nelas. Antes e depois
   ele roda uma busca em largura e RECUSA a mudança que deixe qualquer warp,
   `object_event` ou `bg_event` inalcançável, porque "a planta andável muda só
   ali" é parte da ordem, não um detalhe.

A tabela existe, em vez de uma regra automática, pelo mesmo motivo do
`anel_sinnoh_retro.json`: a conta erra feio nesse tipo de julgamento, e errar
calado aqui tranca o jogador ou abre buraco no mapa.
"""
import argparse
import collections
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from copia_cidade_fonte import (RAIZ, Tileset, pasta_do_simbolo, le_layouts,
                                le_blocos, render_mapa, TILES_POR_METATILE_NOSSO,
                                NUM_METATILES_IN_PRIMARY)
from PIL import Image, ImageDraw

COVERED = 1
TABELA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "telhados_sinnoh_retro.json")


def carrega(nome_mapa):
    with open(os.path.join(RAIZ, "data", "maps", nome_mapa, "map.json"),
              encoding="utf-8") as f:
        mj = json.load(f)
    lays = le_layouts(os.path.join(RAIZ, "data/layouts/layouts.json"))["layouts"]
    lay = next(l for l in lays if l["id"] == mj["layout"])
    prim = Tileset(pasta_do_simbolo(RAIZ, lay["primary_tileset"], False),
                   TILES_POR_METATILE_NOSSO, lay["primary_tileset"])
    sec = Tileset(pasta_do_simbolo(RAIZ, lay["secondary_tileset"], True),
                  TILES_POR_METATILE_NOSSO, lay["secondary_tileset"])
    blocos = le_blocos(os.path.join(RAIZ, lay["blockdata_filepath"].lstrip("./")))
    return mj, lay, prim, sec, blocos


def atributo(prim, sec, mid):
    if mid < NUM_METATILES_IN_PRIMARY:
        return prim.attrs[mid] if mid < len(prim.attrs) else 0
    local = mid - NUM_METATILES_IN_PRIMARY
    return sec.attrs[local] if local < len(sec.attrs) else 0


def topo_desenha(prim, sec, mid):
    """A camada de CIMA deste metatile põe algum pixel na tela?"""
    if mid < NUM_METATILES_IN_PRIMARY:
        ts, local = prim, mid
    else:
        ts, local = sec, mid - NUM_METATILES_IN_PRIMARY
    if local >= len(ts.metatiles):
        return False
    m = ts.metatiles[local]
    return any((p & 0x3FF) != 0 for p in m[4:8])


def candidatas(nome_mapa):
    mj, lay, prim, sec, blocos = carrega(nome_mapa)
    w, h = lay["width"], lay["height"]
    achados = []
    for i, palavra in enumerate(blocos[:w * h]):
        mid, col = palavra & 0x3FF, (palavra & 0x0C00) >> 10
        if col != 0:
            continue
        if ((atributo(prim, sec, mid) >> 12) & 0xF) != COVERED:
            continue
        if not topo_desenha(prim, sec, mid):
            continue
        achados.append((i % w, i // w, mid))
    return mj, lay, prim, sec, blocos, achados


def alcance(blocos, w, h):
    """Busca em largura pelas células de colisão 0, a partir de cada componente."""
    # MAPGRID_COLLISION_MASK é 0x0C00, bits 10-11 (include/global.fieldmap.h).
    # A elevação é que mora em 12-15: ler `>> 12` como colisão dá a lente inteira
    # errada, e foi o que aconteceu na primeira rodada desta ferramenta.
    andavel = [ (blocos[y * w + x] & 0x0C00) == 0 for y in range(h) for x in range(w) ]
    visto = [-1] * (w * h)
    comp = 0
    for s in range(w * h):
        if not andavel[s] or visto[s] >= 0:
            continue
        fila = collections.deque([s])
        visto[s] = comp
        while fila:
            c = fila.popleft()
            cx, cy = c % w, c // w
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < w and 0 <= ny < h:
                    n = ny * w + nx
                    if andavel[n] and visto[n] < 0:
                        visto[n] = comp
                        fila.append(n)
        comp += 1
    return visto, comp


def pontos_do_jogo(mj):
    pts = []
    for k, rot in (("warp_events", "warp"), ("object_events", "obj"),
                   ("bg_events", "bg")):
        for i, e in enumerate(mj.get(k) or []):
            pts.append((rot, i, e["x"], e["y"]))
    return pts


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--mapa", required=True, help="pasta em data/maps, ex.: TwinleafTown")
    p.add_argument("--lente", metavar="PNG", help="grava o render com as candidatas marcadas")
    p.add_argument("--fecha", action="store_true",
                   help="aplica a tabela telhados_sinnoh_retro.json neste mapa")
    p.add_argument("--tabela", default=TABELA)
    args = p.parse_args()

    mj, lay, prim, sec, blocos, achados = candidatas(args.mapa)
    w, h = lay["width"], lay["height"]
    por_mid = collections.Counter(m for _, _, m in achados)
    print(f"=== {args.mapa} {w}x{h} ===")
    print(f"  células ANDÁVEIS com topo desenhando e layerType COVERED "
          f"(o jogador aparece EM CIMA da arte): {len(achados)}")
    for mid, n in sorted(por_mid.items()):
        cel = [(x, y) for x, y, m in achados if m == mid]
        print(f"    metatile {mid:4d}: {n:3d} célula(s)  {cel[:10]}"
              f"{' ...' if len(cel) > 10 else ''}")

    if args.lente:
        im = render_mapa(blocos, w, h, prim, sec,
                         TILES_POR_METATILE_NOSSO, TILES_POR_METATILE_NOSSO)
        d = ImageDraw.Draw(im)
        for x, y, mid in achados:
            d.rectangle([x * 16, y * 16, x * 16 + 15, y * 16 + 15],
                        outline=(255, 0, 0), width=2)
        os.makedirs(os.path.dirname(os.path.abspath(args.lente)), exist_ok=True)
        im.save(args.lente)
        print(f"  lente em {args.lente} ({im.width}x{im.height})")

    if args.fecha:
        tabela = {}
        if os.path.exists(args.tabela):
            with open(args.tabela, encoding="utf-8") as f:
                tabela = (json.load(f).get("cidades", {}) or {}).get(args.mapa, {}) or {}
        mids = set(tabela.get("metatiles", []))
        celulas = {tuple(c) for c in tabela.get("celulas", [])}
        if not mids and not celulas:
            print("  a tabela não manda fechar nada neste mapa; nada a fazer")
            return 0
        antes, n_antes = alcance(blocos, w, h)
        pts = pontos_do_jogo(mj)
        comp_antes = {(r, i): antes[y * w + x] for r, i, x, y in pts
                      if 0 <= x < w and 0 <= y < h}
        novos = list(blocos)
        mudadas = []
        for x, y, mid in achados:
            if mid in mids or (x, y) in celulas:
                i = y * w + x
                novos[i] = (novos[i] & ~0x0C00) | (1 << 10)
                mudadas.append((x, y, mid))
        depois, n_depois = alcance(novos, w, h)
        # A régua: nenhum ponto do JOGO pode mudar de componente, e nenhuma
        # célula que continua andável pode ficar separada das outras.
        quebrou = []
        for (r, i), c in comp_antes.items():
            e = next(e for rr, ii, xx, yy in pts if (rr, ii) == (r, i)
                     for e in [(xx, yy)])
            nx, ny = e
            if not (0 <= nx < w and 0 <= ny < h):
                continue
            if (novos[ny * w + nx] & 0x0C00) != 0:
                quebrou.append((r, i, nx, ny, "ficou SÓLIDO"))
        maior_antes = collections.Counter(
            antes[i] for i in range(w * h) if antes[i] >= 0).most_common(1)
        maior_depois = collections.Counter(
            depois[i] for i in range(w * h) if depois[i] >= 0).most_common(1)
        print(f"  fecha {len(mudadas)} célula(s): {mudadas}")
        print(f"  componentes andáveis: {n_antes} -> {n_depois}; "
              f"maior bolsa {maior_antes[0][1] if maior_antes else 0} -> "
              f"{maior_depois[0][1] if maior_depois else 0} células")
        if quebrou:
            print(f"  RECUSO: {len(quebrou)} ponto(s) do jogo ficariam em cima "
                  f"de célula sólida: {quebrou}")
            return 1
        if n_depois > n_antes:
            print(f"  RECUSO: o mapa andável se PARTIU ({n_antes} -> {n_depois} "
                  f"componentes). Isto é 'a planta andável muda só ali' falhando.")
            return 1
        dados = b"".join(struct.pack("<H", v) for v in novos)
        with open(os.path.join(RAIZ, lay["blockdata_filepath"].lstrip("./")), "wb") as f:
            f.write(dados)
        print(f"  APLICADO em {lay['blockdata_filepath']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
