#!/usr/bin/env python3
"""Devolve ao tileset copiado do hack a definição NOSSA dos metatiles que só os
mapas IRMÃOS usam.

Por que existe (medido em 11/09/2026, frente Dewford)
-----------------------------------------------------
`copia_secundario_blazing.py` troca o secundário inteiro de uma cidade. O
problema é que um secundário de Hoenn quase nunca pertence só à cidade: o
`gTileset_Dewford` é dividido por seis layouts (DewfordTown, Route105, Route106,
Route107, BirthIsland_Exterior e NavelRock_Exterior), e o autor do Blazing
REORDENOU a tabela de metatiles dele. O índice 300, por exemplo, é uma coisa no
nosso tileset e outra no dele.

Resultado medido na primeira cópia crua de Dewford: a cidade ficou certa (só 4
dos 55 metatiles dela mudam de definição), mas BirthIsland_Exterior ganhou 45
metatiles trocados e NavelRock_Exterior 16, e o render virou lixo (árvore
laranja em cima de quadrado de areia, pedra no meio do píer). O contrato
METODO-COPIA-CIDADES, seção 5, cobra que a rota irmã saia com zero pixel de
mudança ou com a mudança declarada; lixo não é mudança declarável.

A medida que salva a operação: **a interseção é vazia**. Dos 109 metatiles que
mudam em Dewford, os 50 que quebram as irmãs NÃO são usados pela cidade. Então
dá para ficar com a arte do hack onde ela aparece e com a nossa onde só as irmãs
veem, sem nenhuma escolha de gosto no meio.

O que este script faz, exatamente:

  - lê os layouts que usam o tileset e separa os metatiles em três grupos:
    usados pelo DONO, usados só pelas IRMÃS, e usados por ninguém;
  - restaura, da revisão `--base`, a definição dos metatiles do grupo do MEIO;
  - não toca em tiles.png, nem em paleta, nem em metatile_attributes.bin. Paleta
    é global ao tileset: a mudança de cor das irmãs continua acontecendo, e é
    ela que o relatório declara.

É idempotente: rodar de novo com a árvore já consertada não muda byte nenhum,
porque os índices restaurados já são os da base.

Uso:
    python3 dev_scripts/preserva_metatiles_irmas.py dewford --dono DewfordTown \
        --base 78926232f9            # só mede
    python3 dev_scripts/preserva_metatiles_irmas.py dewford --dono DewfordTown \
        --base 78926232f9 --aplicar
"""
import argparse
import json
import os
import struct
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAM_METATILE = 16


def rotulo(pasta):
    return "".join(p.capitalize() for p in pasta.split("_"))


def layouts_do_tileset(alvo):
    with open(os.path.join(RAIZ, "data/layouts/layouts.json"), encoding="utf-8") as f:
        todos = json.load(f)["layouts"]
    return [l for l in todos
            if alvo in (l.get("primary_tileset"), l.get("secondary_tileset"))]


def mapas_por_layout():
    de_para = {}
    base = os.path.join(RAIZ, "data/maps")
    for nome in os.listdir(base):
        caminho = os.path.join(base, nome, "map.json")
        if not os.path.isfile(caminho):
            continue
        with open(caminho, encoding="utf-8") as f:
            de_para.setdefault(json.load(f)["layout"], []).append(nome)
    return de_para


def metatiles_usados(layout, n_meta_pri):
    """Índices LOCAIS do secundário citados pelo map.bin e pelo border.bin."""
    usados = set()
    for chave in ("blockdata_filepath", "border_filepath"):
        with open(os.path.join(RAIZ, layout[chave]), "rb") as f:
            buf = f.read()
        for off in range(0, len(buf) - 1, 2):
            idx = struct.unpack_from("<H", buf, off)[0] & 0x3FF
            if idx >= n_meta_pri:
                usados.add(idx - n_meta_pri)
    return usados


def main():
    p = argparse.ArgumentParser()
    p.add_argument("pasta", help="pasta em data/tilesets/secondary (ex.: dewford)")
    p.add_argument("--dono", required=True, help="nome do mapa dono do tileset (ex.: DewfordTown)")
    p.add_argument("--base", required=True, help="revisão git de onde vem a definição NOSSA")
    p.add_argument("--aplicar", action="store_true")
    args = p.parse_args()

    rel = f"data/tilesets/secondary/{args.pasta}/metatiles.bin"
    atual = open(os.path.join(RAIZ, rel), "rb").read()
    base = subprocess.run(["git", "-C", RAIZ, "show", f"{args.base}:{rel}"],
                          capture_output=True, check=True).stdout
    if len(base) != len(atual):
        sys.exit(f"metatiles.bin mudou de tamanho ({len(base)} -> {len(atual)}); "
                 "este script só sabe consertar tabela do mesmo tamanho")
    n = len(atual) // TAM_METATILE

    alvo = "gTileset_" + rotulo(args.pasta)
    de_para = mapas_por_layout()
    dono, irmas = set(), set()
    linhas = []
    for layout in layouts_do_tileset(alvo):
        n_meta_pri = 640 if (layout.get("layout_version") in ("johto", "frlg")) else 512
        usados = metatiles_usados(layout, n_meta_pri)
        nomes = de_para.get(layout["id"], [])
        (dono if args.dono in nomes else irmas).update(usados)
        linhas.append((",".join(nomes) or layout["id"], len(usados)))

    mudou = {i for i in range(n)
             if base[i * TAM_METATILE:(i + 1) * TAM_METATILE]
             != atual[i * TAM_METATILE:(i + 1) * TAM_METATILE]}
    restaurar = sorted((irmas - dono) & mudou)

    print(f"tileset          : {args.pasta}  ({alvo})")
    for nome, quantos in linhas:
        print(f"  layout         : {nome} usa {quantos} metatiles do secundário")
    print(f"metatiles        : {n}; mudaram na cópia {len(mudou)}")
    print(f"dono usa         : {len(dono)}; irmãs usam {len(irmas)}")
    print(f"interseção dono/irmãs que mudou: "
          f"{sorted((dono & irmas) & mudou) or 'vazia'}")
    print(f"a restaurar      : {len(restaurar)} {restaurar}")

    if not args.aplicar:
        print("\n(só medição; rode com --aplicar para escrever)")
        return
    novo = bytearray(atual)
    for i in restaurar:
        novo[i * TAM_METATILE:(i + 1) * TAM_METATILE] = base[i * TAM_METATILE:(i + 1) * TAM_METATILE]
    if bytes(novo) == atual:
        print("\nnada a fazer: a árvore já está consertada.")
        return
    with open(os.path.join(RAIZ, rel), "wb") as f:
        f.write(bytes(novo))
    print("\nescrito.")


if __name__ == "__main__":
    main()
