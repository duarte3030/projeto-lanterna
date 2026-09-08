#!/usr/bin/env python3
"""Apaga de VERDADE os mapas que viraram tumulo, na quebra unica de save.

    python3 dev_scripts/remove_tumulos.py            # tabela, nao escreve
    python3 dev_scripts/remove_tumulos.py --demo     # autoteste com mutacao plantada
    python3 dev_scripts/remove_tumulos.py --aplicar  # escreve

Por que ele so pode rodar UMA vez, e so nesta onda
---------------------------------------------------
`remove_mapas_cortados.py` transformou mapa cortado em TUMULO: a entrada
continua na tabela, o id nao anda, e o que saiu foi o peso. Isso existia porque
a save do Gui guarda dois INDICES que o nome do mapa nao protege:

1. `SaveBlock1.location.mapGroup` / `mapNum` (0x04), que e a POSICAO do mapa
   dentro do grupo em `data/maps/map_groups.json`.
2. `SaveBlock1.mapLayoutId` (0x32), que e o ordinal do layout dentro de
   `data/layouts/layouts.json` contando SO quem tem `border_filepath` no disco
   (`tools/mapjson/mapjson.cpp:895`).

Este script anda os dois de proposito. Ele so pode rodar dentro da quebra unica
de save (`SAVE_LAYOUT_REVISION` 1 -> 2), e nunca depois dela.

O que ele apaga
---------------
- a pasta `data/maps/<Mapa>/` inteira de todo mapa com o campo `cortado_por`;
- o nome do mapa da lista do grupo em `data/maps/map_groups.json`;
- a linha `.include "data/maps/<Mapa>/scripts.inc"` de `data/event_scripts.s`;
- a entrada do layout em `data/layouts/layouts.json`, mas SO do layout que
  nenhum mapa VIVO usa (os 7 compartilhados ficam: os moldes de Oreburgh,
  `LAYOUT_ROUTE208_ACCESS` e `LAYOUT_ROUTE226_ACCESS`);
- a pasta de geometria do layout apagado, incluindo `data/layouts/TocoVago`
  quando nenhum layout que fica apontar mais para ela.

O que ele NAO toca, e por que
-----------------------------
- `warp_events` de mapa VIVO com o campo `porta_original` citando mapa
  apagado: `porta_original` e METADADO, nunca compilado (o `mapjson` le so
  x, y, elevation, dest_map e dest_warp_id). Conferido antes de apagar: nenhum
  `dest_map` de mapa vivo aponta para tumulo, so `porta_original`. O registro
  de onde a porta dava fica, e vale mais do que a limpeza.
- `tools/mapjson/required_map_defines.json`: os `MAP_TRAINER_TOWER_*` e os
  `LAYOUT_TRAINER_TOWER_*` continuam listados la, e e por isso que
  `src/trainer_tower.c` e `src/field_specials.c` seguem compilando depois do
  apagamento (o gerador emite o define no grupo fantasma 118 e o layout como
  0xFFFF).
"""
import json
import os
import shutil
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPAS = os.path.join(RAIZ, "data/maps")
GRUPOS = os.path.join(MAPAS, "map_groups.json")
LAYOUTS = os.path.join(RAIZ, "data/layouts/layouts.json")
EVENT_SCRIPTS = os.path.join(RAIZ, "data/event_scripts.s")


def levanta():
    """Devolve (grupos, layouts, info_de_mapa, tumulos)."""
    grupos = json.load(open(GRUPOS))
    layouts = json.load(open(LAYOUTS))
    info = {}
    for grupo in grupos["group_order"]:
        for nome in grupos[grupo]:
            info[nome] = json.load(open(f"{MAPAS}/{nome}/map.json"))
    tumulos = {n for n, d in info.items() if "cortado_por" in d}
    return grupos, layouts, info, tumulos


def plano(grupos, layouts, info, tumulos):
    """O que sai, medido: mapas, layouts, pastas de geometria."""
    uso = {}
    for nome, dado in info.items():
        uso.setdefault(dado["layout"], []).append(nome)
    layouts_a_sair = sorted(
        lid for lid, mapas in uso.items() if all(m in tumulos for m in mapas)
    )
    por_id = {e["id"]: e for e in layouts["layouts"]}
    pastas = set()
    for lid in layouts_a_sair:
        entrada = por_id.get(lid)
        if not entrada:
            continue
        for chave in ("border_filepath", "blockdata_filepath"):
            caminho = entrada.get(chave)
            if caminho:
                pastas.add(os.path.dirname(caminho))
    # pasta compartilhada com layout que FICA nao pode sair
    fica = {e["id"] for e in layouts["layouts"] if e["id"] not in set(layouts_a_sair)}
    for entrada in layouts["layouts"]:
        if entrada["id"] not in fica:
            continue
        for chave in ("border_filepath", "blockdata_filepath"):
            caminho = entrada.get(chave)
            if caminho:
                pastas.discard(os.path.dirname(caminho))
    return layouts_a_sair, sorted(pastas)


def confere_referencias(info, tumulos):
    """Nenhum mapa VIVO pode apontar para tumulo em campo COMPILADO."""
    ids = {info[n]["id"] for n in tumulos}
    achados = []
    for nome, dado in info.items():
        if nome in tumulos:
            continue
        for i, warp in enumerate(dado.get("warp_events") or []):
            if warp.get("dest_map") in ids:
                achados.append(f"{nome} warp {i} -> {warp['dest_map']}")
        conexoes = dado.get("connections") or []
        for i, con in enumerate(conexoes):
            if con.get("map") in ids:
                achados.append(f"{nome} conexao {i} -> {con['map']}")
    return achados


def bytes_de(pastas):
    total = 0
    for pasta in pastas:
        caminho = os.path.join(RAIZ, pasta)
        for raiz, _, arquivos in os.walk(caminho):
            for arquivo in arquivos:
                total += os.path.getsize(os.path.join(raiz, arquivo))
    return total


def aplica(grupos, layouts, info, tumulos, layouts_a_sair, pastas):
    fora = set(layouts_a_sair)
    for grupo in grupos["group_order"]:
        grupos[grupo] = [n for n in grupos[grupo] if n not in tumulos]
    layouts["layouts"] = [e for e in layouts["layouts"] if e["id"] not in fora]

    linhas = open(EVENT_SCRIPTS).read().splitlines(keepends=True)
    alvos = {f'.include "data/maps/{n}/scripts.inc"' for n in tumulos}
    saida = [linha for linha in linhas if linha.strip() not in alvos]
    tiradas = len(linhas) - len(saida)

    json.dump(grupos, open(GRUPOS, "w"), indent=2)
    open(GRUPOS, "a").write("\n")
    json.dump(layouts, open(LAYOUTS, "w"), indent=2)
    open(LAYOUTS, "a").write("\n")
    open(EVENT_SCRIPTS, "w").writelines(saida)

    for nome in tumulos:
        shutil.rmtree(f"{MAPAS}/{nome}")
    for pasta in pastas:
        caminho = os.path.join(RAIZ, pasta)
        if os.path.isdir(caminho):
            shutil.rmtree(caminho)
    return tiradas


def main():
    aplicar = "--aplicar" in sys.argv
    demo = "--demo" in sys.argv

    grupos, layouts, info, tumulos = levanta()
    achados = confere_referencias(info, tumulos)
    layouts_a_sair, pastas = plano(grupos, layouts, info, tumulos)

    print(f"mapas com cortado_por: {len(tumulos)}")
    por_corte = {}
    for nome in tumulos:
        por_corte.setdefault(info[nome]["cortado_por"], 0)
        por_corte[info[nome]["cortado_por"]] += 1
    for corte, quantos in sorted(por_corte.items(), key=lambda x: -x[1]):
        print(f"  {quantos:4d}  {corte}")
    print(f"layouts que nenhum mapa vivo usa: {len(layouts_a_sair)}")
    compartilhados = sorted(
        lid
        for lid, mapas in
        {d["layout"]: [n for n, dd in info.items() if dd["layout"] == d["layout"]]
         for d in info.values()}.items()
        if any(m in tumulos for m in mapas) and not all(m in tumulos for m in mapas)
    )
    print(f"layouts compartilhados com mapa vivo (ficam): {len(compartilhados)}")
    for lid in compartilhados:
        print(f"    {lid}")
    print(f"pastas de geometria a apagar: {len(pastas)} ({bytes_de(pastas)} B)")

    tamanho_mapas = bytes_de([f"data/maps/{n}" for n in tumulos])
    print(f"bytes em data/maps das pastas apagadas: {tamanho_mapas}")

    if achados:
        print(f"\nRECUSADO: {len(achados)} referencias COMPILADAS a tumulo:")
        for linha in achados[:20]:
            print("   ", linha)
        return 1
    print("\nnenhum mapa vivo aponta para tumulo em campo compilado.")

    if demo:
        # autoteste: planta um warp vivo apontando para tumulo e exige recusa
        vivo = next(n for n in info if n not in tumulos and info[n].get("warp_events"))
        alvo = info[next(iter(tumulos))]["id"]
        copia = json.loads(json.dumps(info))
        copia[vivo]["warp_events"][0]["dest_map"] = alvo
        if not confere_referencias(copia, tumulos):
            print("DEMO REPROVOU: a checagem nao viu o warp plantado")
            return 1
        print("DEMO OK: warp plantado para tumulo foi recusado")
        return 0

    if not aplicar:
        print("\n(nada foi escrito; use --aplicar)")
        return 0

    tiradas = aplica(grupos, layouts, info, tumulos, layouts_a_sair, pastas)
    print(f"\nAPLICADO: {len(tumulos)} mapas, {len(layouts_a_sair)} layouts, "
          f"{tiradas} linhas de data/event_scripts.s, {len(pastas)} pastas de geometria")
    return 0


if __name__ == "__main__":
    sys.exit(main())
