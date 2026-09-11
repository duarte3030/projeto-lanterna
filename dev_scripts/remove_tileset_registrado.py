#!/usr/bin/env python3
"""Apaga um tileset REGISTRADO que ficou sem dono.

Nasceu em 11/09/2026, quando Twinleaf saiu do par próprio e voltou para a regra
3.2 do contrato (cidade no SECUNDÁRIO, primário da região compartilhado). O
`gTileset_TwinleafRetroPrim` continuou em `graphics.h`, `metatiles.h`,
`headers.h` e `tilesets.h` sem layout nenhum apontando para ele, ou seja 512
tiles e 512 metatiles de peso morto na ROM.

Uso:
    python3 dev_scripts/remove_tileset_registrado.py TwinleafRetroPrim [--aplicar]

Sem `--aplicar` ele só diz o que tiraria. Ele RECUSA apagar tileset que algum
layout ainda usa, que é a única forma de isto virar um tiro no pé.
"""
import json
import os
import re
import shutil
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def layouts_que_usam(simbolo):
    with open(os.path.join(RAIZ, "data/layouts/layouts.json"), encoding="utf-8") as f:
        dados = json.load(f)
    alvo = f"gTileset_{simbolo}"
    return [l["name"] for l in dados["layouts"]
            if alvo in (l.get("primary_tileset"), l.get("secondary_tileset"))]


def tira_blocos(caminho, padroes, aplicar):
    texto = open(caminho, encoding="utf-8").read()
    novo, tirados = texto, 0
    for pad in padroes:
        while True:
            achado = re.search(pad, novo, re.S)
            if not achado:
                break
            novo = novo[:achado.start()] + novo[achado.end():]
            tirados += 1
    novo = re.sub(r"\n{3,}", "\n\n", novo)
    if tirados and aplicar:
        open(caminho, "w", encoding="utf-8").write(novo)
    return tirados


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    simbolo = sys.argv[1]
    aplicar = "--aplicar" in sys.argv
    usam = layouts_que_usam(simbolo)
    if usam:
        raise SystemExit(f"RECUSO: {len(usam)} layouts ainda usam "
                         f"gTileset_{simbolo}: {usam[:5]}")
    total = 0
    total += tira_blocos(
        os.path.join(RAIZ, "src/data/tilesets/graphics.h"),
        [rf"\nconst u32 gTilesetTiles_{simbolo}\[\][^;]*;",
         rf"\nconst u16 gTilesetPalettes_{simbolo}\[\]\[16\] =\s*\{{.*?\}};"], aplicar)
    total += tira_blocos(
        os.path.join(RAIZ, "src/data/tilesets/metatiles.h"),
        [rf"\nconst u16 gMetatiles_{simbolo}\[\][^;]*;",
         rf"\nconst u16 gMetatileAttributes_{simbolo}\[\][^;]*;"], aplicar)
    total += tira_blocos(
        os.path.join(RAIZ, "src/data/tilesets/headers.h"),
        [rf"\nconst struct Tileset gTileset_{simbolo} =\s*\{{.*?\}};"], aplicar)
    total += tira_blocos(
        os.path.join(RAIZ, "include/tilesets.h"),
        [rf"\nextern const u32 gTilesetTiles_{simbolo}\[\];",
         rf"\nextern const u16 gTilesetPalettes_{simbolo}\[\]\[16\];",
         rf"\nextern const struct Tileset gTileset_{simbolo};"], aplicar)
    pasta_nome = re.sub(r"(?<!^)(?=[A-Z])", "_", simbolo).lower()
    for tipo in ("primary", "secondary"):
        pasta = os.path.join(RAIZ, "data/tilesets", tipo, pasta_nome)
        if os.path.isdir(pasta):
            print(f"  pasta {os.path.relpath(pasta, RAIZ)}"
                  + (" APAGADA" if aplicar else " (apagaria)"))
            if aplicar:
                shutil.rmtree(pasta)
    print(f"  {total} blocos de registro "
          + ("removidos" if aplicar else "seriam removidos"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
