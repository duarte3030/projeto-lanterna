#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Liga o elevador da loja de departamento de Goldenrod nos sete andares.

Uso:
    python3 dev_scripts/elevador_goldenrod.py --aplicar
    python3 dev_scripts/elevador_goldenrod.py --demo

Por que existe
--------------
Achado da lente `dev_scripts/qa/lente_portas.py` (regra P3) em 06/09/2026,
respondendo a pergunta do Gui "da para entrar em TODAS as casas da ROM": os seis
andares e o subsolo da loja de departamento de Goldenrod tem a PORTA do elevador
desenhada, `MB_ANIMATED_DOOR` em (9,4) e em (10,6), e tem o warp para
`MAP_GOLDENROD_CITY_DEPARTMENT_STORE_ELEVATOR` uma célula ACIMA da porta, em
(9,3), que é parede com colisão 1. Warp em tile solido nunca dispara e porta sem
warp nunca abre: a porta do elevador não fazia nada em nenhum andar.

O mecanismo certo estava na fonte e não foi importado. No `hns`, o elevador NÃO
e mapa: e cena. Um `coord_event` na frente da porta chama o roteiro, o roteiro
abre a porta com `opendoor`, entra com `applymovement` (que não consulta
colisão), mostra o menu de andares e usa `warp` de script. O que faltava aqui
eram três coisas, e este programa poe as três:

  1. o `coord_event` em (9,5) de cada andar, e em (10,7) do subsolo;
  2. a linha `map_script MAP_SCRIPT_ON_FRAME_TABLE, GoldenrodDeptElevator_OnFrame`
     no `_MapScripts` de cada um, que é quem roda a cena de SAIDA ao chegar;
  3. o `.inc` do elevador, escrito a mão em
     data/maps/GoldenrodCity_DepartmentStoreElevator/scripts.inc.

O que este programa NÃO faz, de propósito
-----------------------------------------
Não move o warp de (9,3) para (9,4). Índice de warp é promessa permanente de
save (seção 5 do ESTADO), e mover a célula do warp 2 não consertaria nada:
mesmo em cima da porta ele levaria ao mapa do elevador, que não tem menu nem
volta. O warp fica onde a fonte o deixou, morto, e quem abre a porta é a cena.
`lente_portas` para de acusar os dois porque le `opendoor` do próprio `.inc`.

`coord_event` NÃO entra na save: o que a save guarda e (mapGroup, mapNum),
índice de OBJETO e número de flag. Acrescentar gatilho é acrescentar var por
apelido de `VAR_UNUSED` não mexem em nenhum dos três, e o `guarda_save.py`
confirma.
"""
import argparse
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# mapa -> (x, y) do gatilho, que é a célula da FRENTE da porta do elevador.
ANDARES = {
    "GoldenrodCity_DepartmentStore_1F": (9, 5),
    "GoldenrodCity_DepartmentStore_2F": (9, 5),
    "GoldenrodCity_DepartmentStore_3F": (9, 5),
    "GoldenrodCity_DepartmentStore_4F": (9, 5),
    "GoldenrodCity_DepartmentStore_5F": (9, 5),
    "GoldenrodCity_DepartmentStore_6F": (9, 5),
    "GoldenrodCity_DepartmentStoreBasement": (10, 7),
}
GATILHO = "GoldenrodDeptElevator_EventScript_Elevator"
ON_FRAME = "\tmap_script MAP_SCRIPT_ON_FRAME_TABLE, GoldenrodDeptElevator_OnFrame\n"


def caminho_json(m):
    return os.path.join(REPO, "data/maps", m, "map.json")


def caminho_inc(m):
    return os.path.join(REPO, "data/maps", m, "scripts.inc")


def pendencias():
    """Lista de (mapa, o que falta). Vazia quando tudo já está ligado."""
    falta = []
    for m, (x, y) in ANDARES.items():
        d = json.load(open(caminho_json(m), encoding="utf-8"))
        if not any(c.get("script") == GATILHO for c in d.get("coord_events") or []):
            falta.append((m, f"coord_event em ({x},{y})"))
        if "GoldenrodDeptElevator_OnFrame" not in open(caminho_inc(m), encoding="utf-8").read():
            falta.append((m, "map_script ON_FRAME_TABLE"))
    return falta


def aplica():
    mexidos = 0
    for m, (x, y) in ANDARES.items():
        p = caminho_json(m)
        d = json.load(open(p, encoding="utf-8"))
        coord = d.get("coord_events") or []
        if not any(c.get("script") == GATILHO for c in coord):
            coord.append({
                "type": "trigger",
                "x": x, "y": y, "elevation": 3,
                # VAR_TEMP_0 vale 0 em toda entrada de mapa: o gatilho é sempre
                # armado, e quem impede o laco e o `applymovement` da cena, que
                # atravessa a célula sem disparar coord_event.
                "var": "VAR_TEMP_0", "var_value": "0",
                "script": GATILHO,
            })
            d["coord_events"] = coord
            with open(p, "w", encoding="utf-8") as f:
                json.dump(d, f, indent=2, ensure_ascii=False)
                f.write("\n")
            mexidos += 1
        p = caminho_inc(m)
        texto = open(p, encoding="utf-8").read()
        if "GoldenrodDeptElevator_OnFrame" not in texto:
            alvo = f"{m}_MapScripts::\n"
            if alvo not in texto:
                raise SystemExit(f"{m}: nao achei o rotulo {alvo.strip()}")
            texto = texto.replace(alvo, alvo + ON_FRAME, 1)
            open(p, "w", encoding="utf-8").write(texto)
            mexidos += 1
    print(f"{mexidos} arquivo(s) mexido(s)")
    return 0


def demo():
    """Autoteste: as três peças tem que estar no lugar e apontar uma para a outra."""
    ruim = 0

    def falso(msg):
        nonlocal ruim
        ruim = 1
        print(f"  elevador_goldenrod DEMO: {msg}")

    f = pendencias()
    if f:
        falso(f"faltam {len(f)} pecas: {f[:3]}")
    inc = open(os.path.join(
        REPO, "data/maps/GoldenrodCity_DepartmentStoreElevator/scripts.inc"),
        encoding="utf-8").read()
    for rotulo in (GATILHO, "GoldenrodDeptElevator_OnFrame",
                   "GoldenrodDeptElevator_EventScript_Exit",
                   "GoldenrodDeptElevator_EventScript_B1F",
                   "GoldenrodDeptElevator_EventScript_F6"):
        if rotulo + "::" not in inc:
            falso(f"o .inc do elevador nao define {rotulo}")
    # os sete destinos do menu tem que ser sete mapas DIFERENTES, senao um andar
    # leva ao outro e ninguém percebe
    destinos = [l.split()[1].rstrip(",") for l in inc.splitlines()
                if l.strip().startswith("warp MAP_")]
    if len(set(destinos)) != 7:
        falso(f"o menu tem {len(set(destinos))} destinos distintos, esperava 7")
    # a var tem que ser apelido de VAR_UNUSED: alocar var nova quebraria a save
    vars_h = open(os.path.join(REPO, "include/constants/vars.h"), encoding="utf-8").read()
    if "#define VAR_ELEVADOR_GOLDENROD" not in vars_h:
        falso("VAR_ELEVADOR_GOLDENROD nao esta declarada")
    elif "VAR_UNUSED_" not in [l for l in vars_h.splitlines()
                               if l.startswith("#define VAR_ELEVADOR_GOLDENROD")][0]:
        falso("VAR_ELEVADOR_GOLDENROD nao e apelido de VAR_UNUSED: mexe na save")
    if not ruim:
        print("demo ok")
    return ruim


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        sys.exit(demo())
    if a.aplicar:
        sys.exit(aplica())
    for m, o in pendencias():
        print(f"  falta {o:34} em {m}")
    print("nada pendente" if not pendencias() else "")
