#!/usr/bin/env python3
"""Reescreve o id de treinador NUMERICO dos casos de teste depois da compactacao.

    python3 dev_scripts/remapeia_casos_treinador.py            # tabela, nao escreve
    python3 dev_scripts/remapeia_casos_treinador.py --demo     # autoteste
    python3 dev_scripts/remapeia_casos_treinador.py --aplicar  # escreve

Por que ele existe
------------------
`dev_scripts/compacta_treinadores.py` renumerou os ids na quebra unica de save de
08/09/2026. Quase todo o repo cita treinador por NOME e nao sentiu nada, mas 73
casos de `dev_scripts/testes_criticos/*.json` provam pelo NUMERO, porque o que
eles leem e a EWRAM: `prova.oponente` e um id cru e `prova.oponente_faixa` e um
par de ids crus. Sem este remapeamento a suite ficaria vermelha por causa de
numero velho, e o vermelho pareceria defeito de jogo.

Como o de-para e reconstruido, e por que ele e confiavel
--------------------------------------------------------
Pelo NOME: os dois cabecalhos (`opponents.h` e `opponents_frlg.h`) sao lidos no
commit `REF` (o passo 2 desta mesma onda, antes da compactacao) e na arvore de
hoje. Nome que existe nos dois lados da o par (numero velho, numero novo). Nome
que sumiu e Unova ou Galar, e nao pode aparecer em caso nenhum.

FAIXA e o caso delicado, e a conta e outra: a compactacao preserva a ORDEM, entao
uma faixa velha `[a, b]` continua descrevendo exatamente o mesmo CONJUNTO de
treinadores se o limite de baixo virar o id novo do primeiro id vivo `>= a` e o
de cima o id novo do ultimo id vivo `<= b`. Mapear cada ponta pelo id mais
proximo daria faixa errada quando a ponta caiu num buraco.
"""
import glob
import json
import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASOS = os.path.join(RAIZ, "dev_scripts/testes_criticos")
CABECALHOS = ["include/constants/opponents.h", "include/constants/opponents_frlg.h"]
# Passo 2 da quebra unica de save: o ultimo commit ANTES da compactacao de ids.
REF = "0279a0270c"


def numeros(texto):
    return {n: int(v) for n, v in
            re.findall(r"^#define\s+(TRAINER_\w+)\s+(\d+)", texto, re.M)}


def de_para():
    velho, novo = {}, {}
    for arq in CABECALHOS:
        antigo = subprocess.run(["git", "show", f"{REF}:{arq}"], cwd=RAIZ,
                                capture_output=True, text=True, check=True).stdout
        velho.update(numeros(antigo))
        novo.update(numeros(open(os.path.join(RAIZ, arq)).read()))
    mapa = {}
    for nome, v in velho.items():
        if nome in novo:
            mapa[v] = novo[nome]
    return mapa, velho, novo


def traduz_faixa(mapa, lo, hi):
    """A faixa nova que descreve o MESMO conjunto de treinadores."""
    vivos = sorted(v for v in mapa if lo <= v <= hi)
    if not vivos:
        return None
    return mapa[vivos[0]], mapa[vivos[-1]]


def varre(mapa, aplicar=False):
    trocas, perdidos = [], []
    for caminho in sorted(glob.glob(os.path.join(CASOS, "*.json"))):
        dados = json.load(open(caminho, encoding="utf-8"))
        mudou = False
        for caso in dados:
            prova = caso.get("prova") or {}
            if isinstance(prova.get("oponente"), int) and prova["oponente"] != 0:
                velho = prova["oponente"]
                if velho not in mapa:
                    perdidos.append((os.path.basename(caminho), caso["id"],
                                     "oponente", velho))
                    continue
                if mapa[velho] != velho:
                    trocas.append((os.path.basename(caminho), caso["id"],
                                   "oponente", velho, mapa[velho]))
                    prova["oponente"] = mapa[velho]
                    mudou = True
            faixa = prova.get("oponente_faixa")
            if isinstance(faixa, list) and len(faixa) == 2 \
                    and all(isinstance(x, int) for x in faixa):
                nova = traduz_faixa(mapa, faixa[0], faixa[1])
                if nova is None:
                    perdidos.append((os.path.basename(caminho), caso["id"],
                                     "oponente_faixa", faixa))
                    continue
                if list(nova) != faixa:
                    trocas.append((os.path.basename(caminho), caso["id"],
                                   "oponente_faixa", faixa, list(nova)))
                    prova["oponente_faixa"] = list(nova)
                    mudou = True
        if mudou and aplicar:
            json.dump(dados, open(caminho, "w", encoding="utf-8"),
                      indent=2, ensure_ascii=False)
            open(caminho, "a", encoding="utf-8").write("\n")
    return trocas, perdidos


def main():
    aplicar = "--aplicar" in sys.argv
    demo = "--demo" in sys.argv

    mapa, velho, novo = de_para()
    print(f"nomes no commit {REF}: {len(velho)}; hoje: {len(novo)}; "
          f"de-para por nome: {len(mapa)} ids")
    trocas, perdidos = varre(mapa, aplicar=False)
    print(f"provas numericas a trocar: {len(trocas)}")
    for arquivo, caso, campo, antes, depois in trocas[:80]:
        print(f"    {arquivo} {caso} {campo}: {antes} -> {depois}")
    if perdidos:
        print(f"\nRECUSADO: {len(perdidos)} provas citam id que SUMIU")
        for linha in perdidos:
            print("   ", linha)
        return 1
    print("nenhuma prova cita id apagado.")

    if demo:
        # A conta que a versao ingenua erraria: ponta de faixa que caiu num
        # buraco tem de andar para o vizinho VIVO de dentro da faixa, e nao
        # virar o id mais proximo por acaso.
        buraco = next((v for v in range(max(mapa) + 1) if v not in mapa), None)
        if buraco is None:
            print("DEMO REPROVOU: nao ha buraco no espaco velho para testar")
            return 1
        alvo = traduz_faixa(mapa, buraco, buraco)
        if alvo is not None:
            print(f"DEMO REPROVOU: faixa [{buraco},{buraco}] so tem id morto "
                  f"e mesmo assim virou {alvo}")
            return 1
        print(f"DEMO OK: faixa formada so pelo id morto {buraco} nao vira faixa nenhuma")
        return 0

    if not aplicar:
        print("\n(nada foi escrito; use --aplicar)")
        return 0

    varre(mapa, aplicar=True)
    print(f"\nAPLICADO: {len(trocas)} provas reescritas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
