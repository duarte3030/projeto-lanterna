#!/usr/bin/env python3
"""Apaga mapa fantasma: aquele cujo map.json aponta para blockdata de OUTRA regiao.

Uso:
    python3 dev_scripts/limpa_fantasmas.py            # so lista
    python3 dev_scripts/limpa_fantasmas.py --apagar   # apaga

Existe porque esta e a terceira vez que aparece o mesmo padrao: alguem registra
uma regiao inteira com map.json de verdade e blockdata emprestado de Hoenn. A
Unova falsa tinha 47 retangulos apontando para o map.bin de Petalburg, e a Kalos
falsa tem 34, com 13 cidades dividindo PetalburgCity/map.bin e 8 ginasios
dividindo RustboroCity_Gym/map.bin.

O sintoma nao e o jogo quebrar, e o jogo MENTIR: a regiao aparece na lista, o
validador de warp passa, e nada disso e mapa de verdade.

Tambem limpa duas sujeiras estruturais que ja estouraram tres scripts nesta
sessao:
  - nome em group_order sem chave correspondente no map_groups.json
  - grupo com chave mas fora de group_order (nao compila, so espera alguem por)
"""
import json
import os
import shutil
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Um mapa e fantasma quando N mapas diferentes dividem o mesmo blockdata: mapa
# de verdade tem geometria propria. Dois compartilharem e reuso legitimo (as
# casas do vanilla fazem isso); treze cidades compartilharem e mentira.
LIMITE_COMPARTILHAMENTO = 3


def carrega():
    g = json.load(open(f"{RAIZ}/data/maps/map_groups.json"))
    lay = json.load(open(f"{RAIZ}/data/layouts/layouts.json"))
    return g, lay


def grupos_quebrados(g):
    """Devolve (pendurados, orfaos)."""
    listas = [k for k in g if isinstance(g[k], list) and k != "group_order"]
    pendurados = [x for x in g["group_order"] if x not in g]
    orfaos = [k for k in listas if k not in g["group_order"]]
    return pendurados, orfaos


def blockdata_por_mapa(g, lay):
    por_id = {l["id"]: l.get("blockdata_filepath", "") for l in lay["layouts"]}
    saida = {}
    for grp in g["group_order"] + [k for k in g if isinstance(g[k], list) and k != "group_order"]:
        for m in g.get(grp, []):
            p = f"{RAIZ}/data/maps/{m}/map.json"
            if not os.path.exists(p):
                continue
            d = json.load(open(p))
            saida[m] = (grp, d.get("layout", ""), por_id.get(d.get("layout", ""), ""))
    return saida


def fantasmas(mapas, grupos_validos=frozenset()):
    """Mapa cujo blockdata e compartilhado por muitos mapas de outro grupo.

    ATENCAO, erro que eu cometi na primeira versao: "divide blockdata" sozinho
    NAO e sinal de fantasma. No vanilla, todo Centro Pokemon 1F do jogo aponta
    para PokemonCenter_1F/map.bin, e toda Loja para Mart/map.bin. Isso e o
    projeto do jogo, nao bug. A primeira versao acusou 40 mapas de Hoenn e Kanto
    como fantasma, e o demo() passou porque eu so tinha testado o caso falso,
    nunca o legitimo.

    O que separa de verdade:
      - grupo ORFAO (fora de group_order, ou seja, nada compila) e
      - a MAIORIA do grupo com blockdata emprestado.
    Regiao de verdade tem reuso pontual de interior; regiao falsa e emprestada
    do comeco ao fim, inclusive as cidades.
    """
    from collections import defaultdict
    quem_usa = defaultdict(list)
    for m, (grp, lid, bp) in mapas.items():
        if bp:
            quem_usa[bp].append((m, grp))
    suspeitos = {}
    for bp, usuarios in quem_usa.items():
        if len(usuarios) < LIMITE_COMPARTILHAMENTO:
            continue
        # o dono do blockdata e quem da nome a pasta dele
        dono = os.path.basename(os.path.dirname(bp))
        for m, grp in usuarios:
            if m != dono and grp not in grupos_validos:
                suspeitos.setdefault(grp, []).append((m, bp))
    return suspeitos


def main():
    apagar = "--apagar" in sys.argv
    g, lay = carrega()
    pendurados, orfaos = grupos_quebrados(g)

    print("=== grupos pendurados (em group_order, sem chave) ===")
    for p in pendurados:
        print(f"  {p}")
    print("=== grupos orfaos (com chave, fora de group_order) ===")
    for o in orfaos:
        print(f"  {o}  ({len(g[o])} mapas)")

    mapas = blockdata_por_mapa(g, lay)
    # grupo que o jogo compila e legitimo por definicao: se algo la dentro
    # estiver errado, quem acusa e o validador de conectividade, nao este script
    susp = fantasmas(mapas, grupos_validos=set(g["group_order"]))
    print("\n=== mapas fantasma (grupo orfao, blockdata emprestado) ===")
    total = 0
    for grp, lst in sorted(susp.items()):
        # so acusa grupo que e MAJORITARIAMENTE fantasma: grupo de verdade tem
        # reuso pontual, grupo falso e reuso do comeco ao fim
        n_grupo = len(g.get(grp, []))
        if n_grupo and len(lst) / n_grupo < 0.5:
            continue
        total += len(lst)
        print(f"  {grp}: {len(lst)} de {n_grupo}")
        for m, bp in lst[:3]:
            print(f"      {m} -> {bp}")
        if len(lst) > 3:
            print(f"      ... e mais {len(lst)-3}")

    if not apagar:
        print(f"\n{total} mapas fantasma. Rode com --apagar para remover.")
        return 0

    # apaga: grupos orfaos majoritariamente fantasma, e nomes pendurados
    alvos = set()
    for grp, lst in susp.items():
        n_grupo = len(g.get(grp, []))
        if grp in orfaos and n_grupo and len(lst) / n_grupo >= 0.5:
            alvos.update(g[grp])
    ids_layout = set()
    for m in alvos:
        p = f"{RAIZ}/data/maps/{m}/map.json"
        if os.path.exists(p):
            ids_layout.add(json.load(open(p)).get("layout", ""))
        shutil.rmtree(f"{RAIZ}/data/maps/{m}", ignore_errors=True)

    # tira as entradas de layout que SO os fantasmas usavam
    ainda_usados = {v[1] for m, v in mapas.items() if m not in alvos}
    lay["layouts"] = [l for l in lay["layouts"]
                      if l["id"] not in (ids_layout - ainda_usados)]
    json.dump(lay, open(f"{RAIZ}/data/layouts/layouts.json", "w"), indent=2)

    # limpa map_groups.json
    for grp in list(g):
        if isinstance(g[grp], list) and grp != "group_order" and grp in orfaos:
            if set(g[grp]) & alvos:
                del g[grp]
    g["group_order"] = [x for x in g["group_order"] if x in g]
    json.dump(g, open(f"{RAIZ}/data/maps/map_groups.json", "w"), indent=2)

    print(f"\napagados {len(alvos)} mapas, "
          f"{len(ids_layout - ainda_usados)} layouts, "
          f"{len(pendurados)} nomes pendurados")
    return 0


def demo():
    """Confere que a regra distingue reuso legitimo de regiao falsa.

    O segundo caso e o que a primeira versao errou. Ele fica aqui exatamente
    porque foi o erro: 8 Centros Pokemon dividindo um layout sao vanilla.
    """
    # regiao falsa: grupo orfao, 13 cidades no mesmo map.bin de Petalburg
    falsa = {f"Cidade{i}": ("gMapGroup_Falsa", "L", "data/layouts/PetalburgCity/map.bin")
             for i in range(13)}
    falsa["PetalburgCity"] = ("gMapGroup_Hoenn", "L", "data/layouts/PetalburgCity/map.bin")
    s = fantasmas(falsa, grupos_validos={"gMapGroup_Hoenn"})
    assert len(s["gMapGroup_Falsa"]) == 13, s
    assert "gMapGroup_Hoenn" not in s, "o dono do blockdata nao e fantasma"

    # vanilla: 8 Centros Pokemon de grupos COMPILADOS dividindo um layout
    centros = {f"Cidade{i}_PokemonCenter_1F": (f"gMapGroup_Indoor{i}", "L",
                                               "data/layouts/PokemonCenter_1F/map.bin")
               for i in range(8)}
    validos = {f"gMapGroup_Indoor{i}" for i in range(8)}
    assert fantasmas(centros, grupos_validos=validos) == {}, \
        "Centro Pokemon compartilhado e projeto do jogo, nao fantasma"

    # reuso pontual (2 mapas) nao acusa nem fora de group_order
    ok = {"A": ("g", "L", "x/map.bin"), "B": ("g", "L", "x/map.bin")}
    assert fantasmas(ok) == {}, "2 usuarios e reuso legitimo"
    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
