#!/usr/bin/env python3
"""Lente dos LENDÁRIOS: nível pelo lugar (50 a 100) e nenhum em cidade.

POR QUE ELA EXISTE
------------------
Respostas 111 e 112 do Gui, 01/10/2026 (ESTADO 0.ar): os lendários saíram de
Canalave, do Mt. Silver de fora, de Cianwood, de Floaroma, de Snowpoint, da
Viridian Forest e do gramado das Ruínas de Alph, e "lendário é nível 50 a 100",
escalonado pela dificuldade de acesso. A régua mora em
`dev_scripts/niveis_lendarios.py` e o inventário em
`dev_scripts/inventario_lendarios.py`; esta lente só os liga ao `roda_qa`.

    L1  nível fora de 50..100
    L2  nível diferente do que a tabela do lugar manda (ou lugar sem nível)
    L3  encontro de lendário em mapa de cidade (presente de laboratório pode)

USO
---
    python3 dev_scripts/qa/lente_lendarios.py           # varre e imprime
    python3 dev_scripts/qa/lente_lendarios.py --demo    # autoteste com mutação
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ACIMA = os.path.dirname(AQUI)
if ACIMA not in sys.path:
    sys.path.insert(0, ACIMA)

import inventario_lendarios as INV  # noqa: E402

REGIAO = {}


def _regiao(mapa):
    if not REGIAO:
        import distribui_dex as DD
        REGIAO["_"] = DD.regiao_do_mapa
    if mapa.startswith("errante"):
        return "Hoenn"
    return REGIAO["_"](mapa)


def _regra(texto):
    if "fora de" in texto:
        return "L1"
    if "cidade" in texto:
        return "L3"
    return "L2"


def varre():
    linhas = INV.varre()
    erros = INV.guarda(linhas, INV.mapas_de_cidade())
    achados = []
    for e in erros:
        mapa = e.split(" em ", 1)[1].split()[0] if " em " in e else "?"
        achados.append(dict(regra=_regra(e), classe="trava", regiao=_regiao(mapa),
                            mapa=mapa, texto=e))
    return achados, dict(pontos=len(linhas))


def demo():
    return INV.demo()


if __name__ == "__main__":
    if "--demo" in sys.argv:
        sys.exit(demo())
    ach, censo = varre()
    for a in ach:
        print(f"  {a['regra']} {a['texto']}")
    print(f"LENDÁRIOS: {censo['pontos']} pontos, {len(ach)} achado(s)")
    sys.exit(1 if ach else 0)
