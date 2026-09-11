#!/usr/bin/env python3
"""Prova que o tileset COMPILADO é byte a byte o da ROM do Blazing Emerald v1.6.

Por que existe, e por que ele é mais forte que comparar render: um render igual
prova que a imagem coincide depois de duas cadeias de conversão diferentes, e
qualquer uma das duas pode estar errada do mesmo jeito nas duas pontas. Este
script compara o que o `make` de fato pôs na ROM (`build.nosync/assets/.../
tiles.png*.4bpp`, que é a saída do gbagfx) com o blob LZ77 descomprimido da ROM
do hack. Zero byte diferente é a única nota que passa.

Ele pega, de uma vez, os três modos de errar que a extração tem (documentados no
cabeçalho do `fontes-mapas/romhacks/ferramentas/extrai_tileset.py`): ordem de
nibble invertida, PNG salvo com profundidade errada, e `-num_tiles` de
`src/data/tilesets/graphics.h` cortando a arte nova sem erro de build.

Rode SEMPRE depois de um `make`, porque ele lê a saída do build, não o PNG.

Uso:
    python3 dev_scripts/prova_blazing_bytes.py
"""
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FERRAMENTAS = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/romhacks/ferramentas"
ROM = ("/Users/duarte/Projetos/pokemon-claude/fontes-mapas/romhacks/blazing-emerald/"
       "Pokémon Blazing Emerald v1.6.gba")
INV = os.path.join(FERRAMENTAS, "inv", "blazing-emerald.json")

# offset do cabeçalho do tileset na ROM deles -> (pasta no nosso repo, tiles na ROM).
# `tiles na ROM` é o mesmo número que vai no `-num_tiles` de graphics.h.
ALVO = {
    0x3DF704: ("primary", "general", 512),
    0x3DF71C: ("secondary", "petalburg", 271),
    0x3DF734: ("secondary", "rustboro", 512),
    0x3DF74C: ("secondary", "dewford", 503),
    0x3DF764: ("secondary", "slateport", 504),
    0x3DF77C: ("secondary", "mauville", 503),
    0x3DF794: ("secondary", "lavaridge", 512),
    0x3DF7AC: ("secondary", "fallarbor", 502),
    0x3DF7C4: ("secondary", "fortree", 493),
    0x3DF7DC: ("secondary", "lilycove", 512),
    0x3DF7F4: ("secondary", "mossdeep", 512),
    0x3DF80C: ("secondary", "ever_grande", 320),
    0x3DF824: ("secondary", "pacifidlog", 512),
    0x3DF83C: ("secondary", "sootopolis", 328),
}

# Fallarbor e a unica cidade cujo TILESET nao vem do Blazing (decisao do Gui,
# resposta 71, e variante A do executor): ela recebeu o `map.bin` do Run and Bun
# por cima do NOSSO secundario, entao divergir da ROM do Blazing e o resultado
# CERTO aqui. Dewford saiu desta lista em 11/09/2026: o tileset dela e o do
# Blazing byte a byte; o que voltou a ser nosso foram 50 METATILES das ilhas
# irmas (ver `dev_scripts/preserva_metatiles_irmas.py`), e metatile nao entra
# nesta prova, que compara so a arte dos tiles.
PENDENTES = {"fallarbor"}


def main():
    if not os.path.exists(ROM):
        print(f"ROM do hack não está aqui ({ROM}); nada a provar.")
        return 0
    sys.path.insert(0, FERRAMENTAS)
    from gbamap import Rom  # noqa: E402

    rom = Rom(ROM)
    inv = json.load(open(INV, encoding="utf-8"))["tilesets"]
    verdes = falhas = pulados = 0
    for off, (tipo, nome, nt) in sorted(ALVO.items()):
        t = inv[str(off)]
        # `p_tiles` do inventário já é offset de arquivo em alguns casos e
        # ponteiro 0x08xxxxxx em outros; normalizar antes de ler.
        p = t["p_tiles"]
        fonte = p - 0x08000000 if p >= 0x08000000 else p
        bruto = (rom.lz77(fonte) if t["comp"] else rom.rom[fonte:fonte + t["tam_tiles"]])
        if bruto is None:
            print(f"{nome:12s} LZ77 falhou em 0x{fonte:X}")
            falhas += 1
            continue
        bruto = bruto[:t["tam_tiles"]]
        base = os.path.join(RAIZ, "build.nosync/assets/data/tilesets", tipo, nome)
        cand = os.path.join(base, f"tiles.png_num_tiles_{nt}__Wnum_tiles.4bpp")
        if not os.path.exists(cand):
            cand = os.path.join(base, "tiles.png.4bpp")
        if not os.path.exists(cand):
            print(f"{nome:12s} PULADO: sem saída de build (o tileset ainda não trocou, ou falta `make`)")
            pulados += 1
            continue
        g = open(cand, "rb").read()
        k = min(len(g), len(bruto))
        dif = sum(1 for a, b in zip(g[:k], bruto[:k]) if a != b)
        igual = len(g) >= len(bruto) and dif == 0
        if nome in PENDENTES and not igual:
            print(f"{nome:12s} PENDENTE: o desenho dela nao vem do Blazing, "
                  f"e o tileset ainda e o nosso ({dif} bytes diferentes)")
            pulados += 1
            continue
        print(f'{nome:12s} rom {len(bruto):6d} B  compilado {len(g):6d} B  '
              f'bytes diferentes {dif}  -> {"IGUAL" if igual else "DIVERGE"}')
        verdes += igual
        falhas += not igual
    print(f"\n{verdes} tilesets batem byte a byte com a ROM do Blazing; "
          f"{falhas} divergem; {pulados} pendentes ou sem saída de build.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
