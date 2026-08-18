#!/usr/bin/env python3
"""Comprime (ou descomprime) os ícones de Pokémon em src/data/graphics/pokemon.h.

Os ícones são 32x64 4bpp, 1024 B crus cada. Passando para .smol eles caem para
cerca de 300 B, e o motor descomprime no carregamento (src/pokemon_icon.c).

Uso:
    python3 dev_scripts/comprime_icones.py --lista
    python3 dev_scripts/comprime_icones.py --aplica
    python3 dev_scripts/comprime_icones.py --reverte
"""

import argparse
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ALVO = RAIZ / "src/data/graphics/pokemon.h"

# const u8 gMonIcon_X[] = INCGFX_U8("caminho.png", ".4bpp");
CRU_GFX = re.compile(
    r'^(\s*)const u8 (gMon(?:Icon|EggIcon)\w*)\[\] = INCGFX_U8\("([^"]+)", "\.4bpp"\);'
)
# const u8 gMonIcon_X[] = INCBIN_U8("caminho.4bpp");
CRU_BIN = re.compile(
    r'^(\s*)const u8 (gMon(?:Icon|EggIcon)\w*)\[\] = INCBIN_U8\("([^"]+)\.4bpp"\);'
)
# extern const u8 gMonIcon_X[ARRAY_COUNT(gMonIcon_Y)] ASSET_ALIAS(gMonIcon_Y);
CRU_ALIAS = re.compile(
    r'^(\s*)extern const u8 (gMon(?:Icon|EggIcon)\w*)\[ARRAY_COUNT\((\w+)\)\] '
    r'ASSET_ALIAS\((\w+)\);(.*)$'
)

COMP_GFX = re.compile(
    r'^(\s*)const u32 (gMon(?:Icon|EggIcon)\w*)\[\] = INCGFX_U32\("([^"]+)", "\.4bpp\.smol"\);'
)
COMP_BIN = re.compile(
    r'^(\s*)const u32 (gMon(?:Icon|EggIcon)\w*)\[\] = INCBIN_U32\("([^"]+)\.4bpp\.smol"\);'
)
COMP_ALIAS = re.compile(
    r'^(\s*)extern const u32 (gMon(?:Icon|EggIcon)\w*)\[ARRAY_COUNT\((\w+)\)\] '
    r'ASSET_ALIAS\((\w+)\);(.*)$'
)


def comprime(linha):
    m = CRU_GFX.match(linha)
    if m:
        ind, nome, png = m.groups()
        return f'{ind}const u32 {nome}[] = INCGFX_U32("{png}", ".4bpp.smol");\n'
    m = CRU_BIN.match(linha)
    if m:
        ind, nome, cam = m.groups()
        return f'{ind}const u32 {nome}[] = INCBIN_U32("{cam}.4bpp.smol");\n'
    m = CRU_ALIAS.match(linha)
    if m:
        ind, nome, cnt, alvo, resto = m.groups()
        return (f'{ind}extern const u32 {nome}[ARRAY_COUNT({cnt})] '
                f'ASSET_ALIAS({alvo});{resto}\n')
    return None


def descomprime(linha):
    m = COMP_GFX.match(linha)
    if m:
        ind, nome, png = m.groups()
        return f'{ind}const u8 {nome}[] = INCGFX_U8("{png}", ".4bpp");\n'
    m = COMP_BIN.match(linha)
    if m:
        ind, nome, cam = m.groups()
        return f'{ind}const u8 {nome}[] = INCBIN_U8("{cam}.4bpp");\n'
    m = COMP_ALIAS.match(linha)
    if m:
        ind, nome, cnt, alvo, resto = m.groups()
        return (f'{ind}extern const u8 {nome}[ARRAY_COUNT({cnt})] '
                f'ASSET_ALIAS({alvo});{resto}\n')
    return None


def roda(transforma, grava):
    linhas = ALVO.read_text(encoding="utf-8").splitlines(keepends=True)
    n = 0
    for i, linha in enumerate(linhas):
        nova = transforma(linha)
        if nova is not None:
            linhas[i] = nova
            n += 1
    if grava and n:
        ALVO.write_text("".join(linhas), encoding="utf-8")
    return n


def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--lista", action="store_true", help="conta sem gravar")
    g.add_argument("--aplica", action="store_true", help="cru -> .smol")
    g.add_argument("--reverte", action="store_true", help=".smol -> cru")
    a = p.parse_args()

    if a.lista:
        print(f"crus: {roda(comprime, False)}  comprimidos: {roda(descomprime, False)}")
    elif a.aplica:
        print(f"comprimidos {roda(comprime, True)} ícones")
    else:
        print(f"revertidos {roda(descomprime, True)} ícones")
    return 0


if __name__ == "__main__":
    sys.exit(main())
