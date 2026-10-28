#!/usr/bin/env python3
"""Põe as cores do mapa-múndi de Galar nos índices que o motor usa.

Uso:
    python3 dev_scripts/mapa_galar_indices.py          # converte (idempotente)
    python3 dev_scripts/mapa_galar_indices.py --demo   # só confere, não grava

Por que existe: `LoadRegionMapGfx` (src/region_map.c) carrega a paleta do mapa
em BG_PLTT_ID(7), ou seja, nas cores 112 a 159 do BG de 8 bits. O PNG de Hoenn
(`map.png`) já usa os índices 112 em diante. O de Galar, copiado do hack em
`graphics/pokenav/region_map/map_galar.png`, veio com os índices 1 a 15 (banco
0 do 4bpp do FireRed): sem esta conversão o mapa sairia com as cores da moldura
e do texto.

A conversão NÃO mexe na arte: índice i vira 112 + i e a cor da entrada 112 + i
da paleta do PNG é a cor i de antes. O `--demo` confere pixel a pixel, em RGB,
que a imagem convertida é igual à cópia aprovada (fontes-mapas/prd-assets/
fase1-arte/galar/mapa/map_galar.png), quando ela existe nesta máquina.
"""
import os
import sys

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PNG = os.path.join(RAIZ, "graphics/pokenav/region_map/map_galar.png")
FONTE = os.path.expanduser(
    "~/Projetos/pokemon-claude/fontes-mapas/prd-assets/fase1-arte/galar/mapa/map_galar.png")
BASE = 112


def pixels(im):
    f = getattr(im, "get_flattened_data", None) or im.getdata
    return list(f())


def rgb(im):
    return pixels(im.convert("RGB"))


def converte(im):
    idx = pixels(im)
    if min(idx) >= BASE:
        return im, False
    assert max(idx) < 16, f"índice {max(idx)} fora do banco 0"
    pal = im.getpalette()[:16 * 3]
    nova = [0] * (256 * 3)
    nova[BASE * 3:(BASE + 16) * 3] = pal
    out = Image.new("P", im.size)
    out.putpalette(nova)
    out.putdata([BASE + i for i in idx])
    return out, True


def main():
    demo = "--demo" in sys.argv
    im = Image.open(PNG)
    out, mudou = converte(im)
    idx = pixels(out)
    erros = []
    if min(idx) < BASE or max(idx) >= BASE + 48:
        erros.append(f"índices fora de {BASE}..{BASE + 47}: {min(idx)}..{max(idx)}")
    if rgb(out) != rgb(im):
        erros.append("a conversão mudou alguma cor")
    if os.path.exists(FONTE) and rgb(out) != rgb(Image.open(FONTE)):
        erros.append("a imagem difere da cópia aprovada em fontes-mapas")
    if demo and mudou:
        erros.append("o PNG do repo ainda está com os índices do hack (rode sem --demo)")
    if erros:
        print("REPROVADO:", "; ".join(erros))
        return 1
    if mudou and not demo:
        out.save(PNG)
    print(f"ok: {len(set(idx))} cores, índices {min(idx)}..{max(idx)}, "
          f"{'convertido agora' if mudou and not demo else 'já convertido'}; "
          f"{'igual à cópia aprovada' if os.path.exists(FONTE) else 'cópia aprovada ausente nesta máquina'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
