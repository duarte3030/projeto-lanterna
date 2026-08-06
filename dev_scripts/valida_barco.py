#!/usr/bin/env python3
"""Confere que os cinco portos e a lista unica de destinos continuam batendo.

Roda sem ROM e sem emulador: e fato de compilacao, lido da fonte.

Por que existe
--------------
O barco que liga as cinco regioes usa UMA lista de destinos,
`MULTI_CINCO_REGIOES_BARCO` (apelidada `MULTI_BOAT_DESTINATIONS`), e cada porto
faz `switch VAR_RESULT` com os `case` da lista, pulando o proprio indice. Nada
no compilador liga uma coisa a outra: se alguem acrescentar um destino no meio
da lista, os cinco `switch` passam a mandar o jogador para o lugar errado, em
silencio, e so um teste de emulador por travessia pegaria.

Foi assim que o bug original nasceu: o menu apontava para
`MULTI_BRINEY_OFF_DEWFORD`, de duas entradas (DEWFORD e Sair), enquanto os
scripts faziam `switch` em tres casos. O jogo compilava e zarpava para o
destino errado.

Este validador afirma, item a item:
  1. a lista tem os destinos esperados, nesta ordem, com "Sair" no fim;
  2. cada porto tem exatamente os `case` dos OUTROS quatro destinos, e nenhum
     `case` para si mesmo;
  3. o script de cada `case` desembarca no mapa que o nome do item promete;
  4. todo `warpsilent` tem `waitstate` logo depois (sem ele o script termina
     com um warp em andamento e o jogo cai no assert de src/script.c:79).
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# indice -> (nome no menu, mapa de desembarque)
DESTINOS = [
    ("OLIVINE",   "MAP_OLIVINE_CITY_PORT_INSIDE"),
    ("SLATEPORT", "MAP_SLATEPORT_CITY_HARBOR"),
    ("VERMILION", "MAP_VERMILION_CITY"),
    ("VIRBANK",   "MAP_UNOVA_VIRBANK_PORT"),
    ("CANALAVE",  "MAP_CANALAVE_CITY"),
]

# A travessia Olivine <-> Vermilion passa POR DENTRO do S.S. Aqua desde
# 05/08/2026: o porto embarca o jogador em MAP_SSAQUA_1F e quem desembarca do
# outro lado e o marinheiro da porta. A regra 3 continua valendo, so que em dois
# saltos, e ganhou duas exigencias que o teleporte direto nao tinha:
#   - o sentido da viagem tem que ser posto (FLAG_SSAQUA_RUMO_KANTO), senao o
#     marinheiro da porta desembarca no lado errado;
#   - a porta do cais (setdynamicwarp) tem que voltar para o proprio porto,
#     senao sair pela porta vira teleporte de graca para o outro continente.
# (pasta, indice) -> (comando de sentido, rotulo de desembarque no navio)
VIA_NAVIO = {
    ("OlivineCity_PortInside", 2): ("setflag", "SSAqua_1F_EventScript_LeaveBoatVermilion"),
    ("VermilionCity_Frlg", 0): ("clearflag", "SSAqua_1F_EventScript_LeaveBoatOlivine"),
}
NAVIO = "MAP_SSAQUA_1F"

# pasta do porto -> indice que ele PULA, por ser ele mesmo
PORTOS = {
    "OlivineCity_PortInside": 0,
    "SlateportCity_Harbor": 1,
    "VermilionCity_Frlg": 2,
    "Unova_VirbankPort": 3,
    "CanalaveCity": 4,
}


def falha(msgs, texto):
    print(f"[FALHA] {texto}")
    msgs.append(texto)


def main():
    erros = []

    # 1. a lista de destinos
    fonte = open(os.path.join(RAIZ, "src/data/script_menu.h")).read()
    m = re.search(r"MultichoiceList_CincoRegioesBarco\[\]\s*=\s*\{(.*?)\};", fonte, re.S)
    if not m:
        falha(erros, "MultichoiceList_CincoRegioesBarco nao existe em src/data/script_menu.h")
        return 1
    itens = re.findall(r'COMPOUND_STRING\("([^"]+)"\)|\{(gText_Exit)\}', m.group(1))
    lista = [a or b for a, b in itens]
    esperada = [d for d, _ in DESTINOS] + ["gText_Exit"]
    if lista != esperada:
        falha(erros, f"a lista de destinos mudou: {lista}, esperado {esperada}")

    # o apelido tem que apontar para essa lista, e nao para o menu do Briney
    cab = open(os.path.join(RAIZ, "include/constants/script_menu.h")).read()
    if not re.search(r"#define\s+MULTI_BOAT_DESTINATIONS\s+MULTI_CINCO_REGIOES_BARCO", cab):
        falha(erros, "MULTI_BOAT_DESTINATIONS nao aponta para MULTI_CINCO_REGIOES_BARCO")

    # 2, 3 e 4: cada porto
    for pasta, proprio in PORTOS.items():
        caminho = os.path.join(RAIZ, "data/maps", pasta, "scripts.inc")
        texto = open(caminho).read()

        bloco = re.search(r"multichoice[^\n]*MULTI_BOAT_DESTINATIONS[^\n]*\n\tswitch VAR_RESULT\n((?:\tcase \d+, \w+\n)+)",
                          texto)
        if not bloco:
            falha(erros, f"{pasta}: nao achei o switch do MULTI_BOAT_DESTINATIONS")
            continue
        casos = {int(n): r for n, r in re.findall(r"\tcase (\d+), (\w+)", bloco.group(1))}

        esperados = {i for i in range(len(DESTINOS))} - {proprio}
        if set(casos) != esperados:
            falha(erros, f"{pasta}: os case sao {sorted(casos)}, esperado {sorted(esperados)} "
                         f"(todos os destinos menos o indice {proprio}, que e ele mesmo)")

        for idx, rotulo in casos.items():
            if idx >= len(DESTINOS):
                continue
            nome, mapa = DESTINOS[idx]
            corpo = re.search(rf"^{rotulo}::\n(.*?)\n\tend\n", texto, re.S | re.M)
            if not corpo:
                falha(erros, f"{pasta}: case {idx} chama {rotulo}, que nao existe")
                continue
            w = re.search(r"warpsilent (MAP_[A-Z0-9_]+)", corpo.group(1))
            via = VIA_NAVIO.get((pasta, idx))
            if via and w and w.group(1) == NAVIO:
                comando, saida = via
                proprio = DESTINOS[PORTOS[pasta]][1]
                if not re.search(rf"\b{comando} FLAG_SSAQUA_RUMO_KANTO\b", corpo.group(1)):
                    falha(erros, f"{pasta}: {rotulo} embarca no navio sem "
                                 f"'{comando} FLAG_SSAQUA_RUMO_KANTO': o marinheiro "
                                 "da porta desembarca no lado errado")
                if not re.search(rf"setdynamicwarp {proprio}\b", corpo.group(1)):
                    falha(erros, f"{pasta}: {rotulo} nao aponta a porta do cais de "
                                 f"volta para {proprio} (setdynamicwarp)")
                navio = open(os.path.join(RAIZ, "data/maps/SSAqua_1F/scripts.inc"),
                             encoding="utf-8").read()
                bloco = re.search(rf"^{saida}::\n(.*?)\n\tend\n", navio, re.S | re.M)
                if not bloco:
                    falha(erros, f"SSAqua_1F: {saida} nao existe")
                elif not re.search(rf"\bwarp {mapa}\b", bloco.group(1)):
                    falha(erros, f"SSAqua_1F: o item {idx} do menu de {pasta} diz "
                                 f"{nome}, mas {saida} nao desembarca em {mapa}")
                continue
            if not w:
                falha(erros, f"{pasta}: {rotulo} nao tem warpsilent")
            elif w.group(1) != mapa:
                falha(erros, f"{pasta}: o item {idx} do menu diz {nome}, mas {rotulo} "
                             f"desembarca em {w.group(1)} (deveria ser {mapa})")

        # 4. warpsilent sem waitstate derruba o jogo em src/script.c:79
        for linha, prox in re.findall(r"\twarpsilent ([^\n]+)\n\t(\w+)", texto):
            if prox != "waitstate":
                falha(erros, f"{pasta}: 'warpsilent {linha}' sem waitstate logo depois "
                             f"(veio '{prox}')")

    if erros:
        print(f"\n{len(erros)} problema(s) no barco entre regioes")
        return 1
    print(f"barco entre regioes: {len(DESTINOS)} destinos, {len(PORTOS)} portos, "
          "todos os case batendo com a lista")
    return 0


if __name__ == "__main__":
    sys.exit(main())
