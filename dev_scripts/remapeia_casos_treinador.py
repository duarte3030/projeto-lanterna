#!/usr/bin/env python3
"""Reescreve o id de treinador NUMERICO e a flag de vitoria CRUA dos casos de teste.

    python3 dev_scripts/remapeia_casos_treinador.py            # tabela, nao escreve
    python3 dev_scripts/remapeia_casos_treinador.py --demo     # autoteste
    python3 dev_scripts/remapeia_casos_treinador.py --aplicar  # escreve

Por que ele existe
------------------
`dev_scripts/compacta_treinadores.py` renumerou os ids na quebra unica de save de
08/09/2026. Quase todo o repo cita treinador por NOME e nao sentiu nada, mas os
casos de `dev_scripts/testes_criticos/*.json` tocam o numero em DOIS lugares,
porque o que eles leem e escrevem e a EWRAM:

1. a PROVA: `prova.oponente` e um id cru e `prova.oponente_faixa` e um par de
   ids crus;
2. o ESTADO INICIAL: `flags` (e `prova.flags_acesas` / `prova.flags_apagadas`)
   aceita flag por numero, e a flag "ja venci este treinador" e
   `TRAINER_FLAGS_START + id`, ou seja 0x500 mais o id. Toda flag crua entre
   0x500 e 0x500 + MAX_TRAINERS_COUNT antigo (4000) e um id de treinador
   disfarcado de numero.

O segundo custou um vermelho de verdade antes de ser achado, e vale registrar
como se manifesta, porque ele NAO parece problema de numeracao: o T12.3 acende
a flag de vitoria da Reli para que quem apareca na Ponte do Nugget seja a Ali. A
flag continuou 0xB80, que era `0x500 + 1664` (Reli), e virou `0x500 + 1697`
(outro treinador qualquer). Reli voltou a estar de pe, viu o jogador primeiro, e
o caso reprovou dizendo "esperado TRAINER_LASS_ALI, obtido TRAINER_LASS_RELI".
O sintoma e "o jogo mudou"; a causa e o numero velho no caso.

Sem este remapeamento a suite ficaria vermelha por numero velho, e o vermelho
pareceria defeito de jogo.

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

IDEMPOTENCIA, e ela nao e detalhe
---------------------------------
O numero VELHO de cada campo e lido do arquivo de caso NO COMMIT `REF`, e nunca
do arquivo de hoje. Sem isso, rodar o script duas vezes traduz o que ja estava
traduzido e a faixa de Kanto vira [1367, 1733] em vez de [1367, 1766], calada.
Os campos que nao sao de treinador (texto do caso, roteiro, prova de mapa)
continuam sendo os de hoje: o script so escreve os campos que ele mesmo traduz.
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


# `include/constants/flags.h`: a flag de vitoria e TRAINER_FLAGS_START + id, e o
# teto ANTIGO de ids era 4000. Numero cru nessa faixa e id de treinador.
TRAINER_FLAGS_START = 0x500
TETO_ANTIGO = 4000


def traduz_flag(mapa, valor):
    """(valor novo, mudou) para uma flag CRUA de caso de teste.

    Fora da faixa de treinador nada muda: flag de cena e de sistema tem numero
    proprio e nenhuma delas andou nesta onda.
    """
    if isinstance(valor, str):
        if not re.fullmatch(r"0[xX][0-9A-Fa-f]+", valor):
            return valor, False   # nome de flag: o pre-processador resolve
        numero, hexa = int(valor, 16), True
    elif isinstance(valor, int):
        numero, hexa = valor, False
    else:
        return valor, False
    if not (TRAINER_FLAGS_START <= numero < TRAINER_FLAGS_START + TETO_ANTIGO):
        return valor, False
    velho = numero - TRAINER_FLAGS_START
    if velho not in mapa:
        return None, True         # id apagado: o caso precisa de gente
    novo = TRAINER_FLAGS_START + mapa[velho]
    if novo == numero:
        return valor, False
    return (f"0x{novo:X}" if hexa else novo), True


def casos_no_ref(caminho):
    """{id do caso: caso} do arquivo COMO ERA no commit REF, ou {}."""
    rel = os.path.relpath(caminho, RAIZ)
    r = subprocess.run(["git", "show", f"{REF}:{rel}"], cwd=RAIZ,
                       capture_output=True, text=True)
    if r.returncode != 0:
        return {}
    return {c["id"]: c for c in json.loads(r.stdout)}


def varre(mapa, aplicar=False):
    trocas, perdidos = [], []
    for caminho in sorted(glob.glob(os.path.join(CASOS, "*.json"))):
        dados = json.load(open(caminho, encoding="utf-8"))
        antigos = casos_no_ref(caminho)
        arquivo = os.path.basename(caminho)
        mudou = False
        for caso in dados:
            antigo = antigos.get(caso["id"])
            if antigo is None:
                continue          # caso novo: ja nasceu com numero de hoje
            prova = caso.get("prova") or {}
            prova_velha = antigo.get("prova") or {}
            for dono, velho_dono, chave in ((caso, antigo, "flags"),
                                            (prova, prova_velha, "flags_acesas"),
                                            (prova, prova_velha, "flags_apagadas")):
                lista = dono.get(chave)
                antes = velho_dono.get(chave)
                if not isinstance(lista, list) or not isinstance(antes, list):
                    continue
                if len(lista) != len(antes):
                    continue      # o caso mudou de forma: nao e assunto daqui
                for i, valor in enumerate(antes):
                    saida, andou = traduz_flag(mapa, valor)
                    if not andou:
                        continue
                    if saida is None:
                        perdidos.append((arquivo, caso["id"], chave, valor))
                        continue
                    if lista[i] != saida:
                        trocas.append((arquivo, caso["id"], chave, valor, saida))
                        lista[i] = saida
                        mudou = True
            velho = prova_velha.get("oponente")
            if isinstance(velho, int) and velho != 0:
                if velho not in mapa:
                    perdidos.append((arquivo, caso["id"], "oponente", velho))
                elif prova.get("oponente") != mapa[velho]:
                    trocas.append((arquivo, caso["id"], "oponente", velho,
                                   mapa[velho]))
                    prova["oponente"] = mapa[velho]
                    mudou = True
            faixa = prova_velha.get("oponente_faixa")
            if isinstance(faixa, list) and len(faixa) == 2 \
                    and all(isinstance(x, int) for x in faixa):
                nova = traduz_faixa(mapa, faixa[0], faixa[1])
                if nova is None:
                    perdidos.append((arquivo, caso["id"], "oponente_faixa", faixa))
                elif prova.get("oponente_faixa") != list(nova):
                    trocas.append((arquivo, caso["id"], "oponente_faixa", faixa,
                                   list(nova)))
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
