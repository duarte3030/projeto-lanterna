#!/usr/bin/env python3
"""Fecha os buracos de id de treinador e baixa o teto, na quebra unica de save.

    python3 dev_scripts/compacta_treinadores.py            # tabela, nao escreve
    python3 dev_scripts/compacta_treinadores.py --demo     # autoteste
    python3 dev_scripts/compacta_treinadores.py --aplicar  # escreve

Por que so aqui
---------------
A flag "ja venci este treinador" e `TRAINER_FLAGS_START + id`
(`include/constants/flags.h`), entao renumerar id apaga vitoria na save; e
baixar `MAX_TRAINERS_COUNT` empurra `SYSTEM_FLAGS` e todo o resto do `flags[]`
dentro do SaveBlock1. Sao duas quebras de save, e por isso isto so acontece
dentro da quebra unica (`SAVE_LAYOUT_REVISION` 1 -> 2).

O espaco de id e UM SO, e essa e a armadilha
--------------------------------------------
Os ids nao moram so em `include/constants/opponents.h`: os treinadores de Kanto
moram em `include/constants/opponents_frlg.h`, com numeros do MESMO espaco
(1653, 1400, ...). Quem renumerar so um dos dois arquivos cria colisao calada.
`dev_scripts/guarda_save.py` le apenas o primeiro, entao ele NAO enxergaria a
metade de Kanto: este script le e escreve os dois juntos.

Havia 150 numeros com dois nomes antes desta onda. Medido: em 149 deles um dos
lados e treinador so do build FRLG (`src/data/trainers_frlg.party`), sem time em
`src/data/trainers.party`, entao os dois nunca brigam no cartucho; o 150 e
`TRAINER_NONE`, que e 0 nos dois. O mapeamento aqui e feito por NUMERO VELHO, e
nao por nome, justamente para os pares que ja compartilhavam id continuarem
compartilhando.

O que sai
---------
Os 679 defines de Unova e de Galar (411 e 268), que a onda 1 deixou como buraco
inerte. Medido de duas formas independentes, com o mesmo resultado: sao
exatamente os nomes com prefixo `TRAINER_UNOVA_`/`TRAINER_GALAR_`, e sao
exatamente os nomes sem time em `trainers.party` e sem uma unica referencia em
codigo compilado (`src/`, `include/`, `data/`, `test/`, `tools/`).

A torre de treinadores de Sevii NAO tem id nesta tabela: os times dela vivem em
`src/trainer_tower_sets.c`, numerados por conta propria, entao nao ha nada para
compactar la.
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CABECALHOS = [
    "include/constants/opponents.h",
    "include/constants/opponents_frlg.h",
]
PARTY = "src/data/trainers.party"
MORTOS = ("TRAINER_UNOVA_", "TRAINER_GALAR_")
# Teto novo. 2.047 ids distintos ficam depois da limpeza (0 a 2.046), e 2200 da
# 153 vagas de folga sem carregar as 1.953 vagas mortas do teto de 4000.
TETO_NOVO = 2200

LINHA = re.compile(r"^(#define\s+)(TRAINER_\w+)(\s+)(\d+)(.*)$")


def le_defines():
    """arquivo -> lista de (indice da linha, nome, numero, coluna do numero)."""
    saida = {}
    for arq in CABECALHOS:
        linhas = open(os.path.join(RAIZ, arq)).read().splitlines()
        achados = []
        for i, linha in enumerate(linhas):
            m = LINHA.match(linha)
            if m:
                coluna = len(m.group(1)) + len(m.group(2)) + len(m.group(3))
                achados.append((i, m.group(2), int(m.group(4)), coluna))
        saida[arq] = (linhas, achados)
    return saida


def mapeamento(arquivos):
    todos = {}
    for arq, (_, achados) in arquivos.items():
        for _, nome, numero, _ in achados:
            todos[nome] = numero
    mortos = {n for n in todos if n.startswith(MORTOS)}
    vivos = {n: v for n, v in todos.items() if n not in mortos}
    numeros = sorted(set(vivos.values()))
    de_para = {velho: novo for novo, velho in enumerate(numeros)}
    return todos, mortos, vivos, de_para


def confere(todos, mortos, vivos, de_para):
    erros = []
    if de_para.get(0) != 0:
        erros.append("TRAINER_NONE deixaria de ser 0")
    if len(set(de_para.values())) != len(de_para):
        erros.append("o de-para leva dois ids velhos para o mesmo id novo")
    if max(de_para.values()) + 1 > TETO_NOVO:
        erros.append(f"teto {TETO_NOVO} menor que os {max(de_para.values()) + 1} ids vivos")
    # nome vivo com dois numeros novos e impossivel por construcao; o que precisa
    # de prova e que par que COMPARTILHAVA id continue compartilhando
    por_velho = {}
    for nome, velho in vivos.items():
        por_velho.setdefault(velho, []).append(nome)
    for velho, nomes in por_velho.items():
        if len({de_para[velho] for _ in nomes}) != 1:
            erros.append(f"par {nomes} deixou de compartilhar id")
    # nenhum morto pode ter time
    texto = open(os.path.join(RAIZ, PARTY)).read()
    comtime = set(re.findall(r"^===\s*(TRAINER_\w+)\s*===", texto, re.M))
    com = sorted(mortos & comtime)
    if com:
        erros.append(f"{len(com)} ids a apagar TEM time em trainers.party: {com[:5]}")
    return erros


def referencias_compiladas(mortos):
    """Todo uso dos nomes a apagar em codigo que o build le."""
    pastas = ("src", "include", "data", "test", "tools", "asm")
    ignora = {os.path.join(RAIZ, a) for a in CABECALHOS}
    padrao = re.compile(r"\b(TRAINER_\w+)\b")
    achados = []
    for pasta in pastas:
        for raiz, dirs, arquivos in os.walk(os.path.join(RAIZ, pasta)):
            dirs[:] = [d for d in dirs if d not in (".git", "build", "build.nosync")]
            for arquivo in arquivos:
                caminho = os.path.join(raiz, arquivo)
                if caminho in ignora:
                    continue
                if not arquivo.endswith((".c", ".h", ".inc", ".json", ".s",
                                         ".party", ".cpp", ".txt")):
                    continue
                texto = open(caminho, errors="ignore").read()
                for nome in set(padrao.findall(texto)):
                    if nome in mortos:
                        achados.append((os.path.relpath(caminho, RAIZ), nome))
    return achados


def escreve(arquivos, mortos, de_para):
    for arq, (linhas, achados) in arquivos.items():
        saida = []
        apagar = {i for i, nome, _, _ in achados if nome in mortos}
        troca = {i: (nome, de_para[num], col)
                 for i, nome, num, col in achados if nome not in mortos}
        for i, linha in enumerate(linhas):
            if i in apagar:
                continue
            if i in troca:
                nome, novo, coluna = troca[i]
                m = LINHA.match(linha)
                cabeca = m.group(1) + nome
                enchimento = max(1, coluna - len(cabeca))
                saida.append(f"{cabeca}{' ' * enchimento}{novo}{m.group(5)}")
            else:
                saida.append(linha)
        open(os.path.join(RAIZ, arq), "w").write("\n".join(saida) + "\n")

    caminho = os.path.join(RAIZ, "include/constants/opponents.h")
    texto = open(caminho).read()
    texto = re.sub(r"#define MAX_TRAINERS_COUNT_EMERALD \d+",
                   f"#define MAX_TRAINERS_COUNT_EMERALD {TETO_NOVO}", texto)
    open(caminho, "w").write(texto)


def main():
    aplicar = "--aplicar" in sys.argv
    demo = "--demo" in sys.argv

    arquivos = le_defines()
    todos, mortos, vivos, de_para = mapeamento(arquivos)
    erros = confere(todos, mortos, vivos, de_para)
    refs = referencias_compiladas(mortos)

    print(f"defines de treinador: {len(todos)} "
          f"({len(arquivos[CABECALHOS[0]][1])} em opponents.h, "
          f"{len(arquivos[CABECALHOS[1]][1])} em opponents_frlg.h)")
    print(f"a apagar (Unova e Galar): {len(mortos)}")
    print(f"a manter: {len(vivos)} nomes em {len(set(vivos.values()))} ids distintos")
    print(f"maior id: {max(todos.values())} -> {max(de_para.values())}")
    print(f"buracos fechados: {max(todos.values()) + 1 - len(de_para)}")
    velho = 4000
    print(f"MAX_TRAINERS_COUNT_EMERALD: {velho} -> {TETO_NOVO} "
          f"({TETO_NOVO - len(de_para)} vagas de folga)")
    print(f"gTrainerIndex: {velho * 2} B -> {TETO_NOVO * 2} B "
          f"({(velho - TETO_NOVO) * 2} B de volta)")
    print(f"flags[] do SaveBlock1: {(velho - TETO_NOVO) // 8} B de volta")
    if refs:
        print(f"\nRECUSADO: {len(refs)} referencias COMPILADAS aos ids a apagar")
        for caminho, nome in refs[:10]:
            print(f"    {caminho}: {nome}")
        return 1
    print("nenhuma referencia compilada aos ids a apagar.")

    if erros:
        print("\nRECUSADO:")
        for erro in erros:
            print("   ", erro)
        return 1
    print("de-para consistente: TRAINER_NONE segue 0, nenhum id novo repetido.")

    if demo:
        estragado = dict(de_para)
        estragado[max(estragado)] = 0
        if not confere(todos, mortos, vivos, estragado):
            print("DEMO REPROVOU: a checagem nao viu o de-para colidido")
            return 1
        print("DEMO OK: de-para com id repetido foi recusado")
        return 0

    if not aplicar:
        print("\n(nada foi escrito; use --aplicar)")
        return 0

    escreve(arquivos, mortos, de_para)
    print("\nAPLICADO em include/constants/opponents.h e opponents_frlg.h")
    return 0


if __name__ == "__main__":
    sys.exit(main())
