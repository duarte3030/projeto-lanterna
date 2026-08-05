#!/usr/bin/env python3
"""Mede e escalona a curva de nível das cinco regiões, lendo src/data/trainers.party.

Uso:
    python3 dev_scripts/curva_de_nivel.py               # só mede, não escreve nada
    python3 dev_scripts/curva_de_nivel.py --aplicar     # aplica a tabela ALVO
    python3 dev_scripts/curva_de_nivel.py --aplicar --seco   # mostra o diff sem escrever

Por que uma tabela e não 1981 edições na mão
--------------------------------------------
São 2128 blocos de treinador. Editar um por um é trabalho mecânico que repete,
e trabalho mecânico que repete vira script. A regra é uma linha por região:
cada nível vira `round(a + b * nivel)`, com `a` e `b` tirados de duas âncoras
(o nível do primeiro treinador da região e o do último). Assim a FORMA da curva
original de cada jogo é preservada (o treinador fraco continua sendo o fraco da
região), e só a faixa se desloca para caber na ordem cronológica nova.

Região de cada treinador, e como é decidida (nunca por chute):
    - nome começa com TRAINER_JOHTO_   -> Johto
    - nome começa com TRAINER_SINNOH_  -> Sinnoh
    - id em 1400..1799                 -> Kanto  (include/constants/opponents_frlg.h)
    - id em 1800..2199                 -> Unova
    - o resto                          -> Hoenn  (os treinadores originais)

O id vem dos headers, não do arquivo de times: `trainers.party` só tem o nome.
"""
import argparse
import os
import re
import statistics
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTY = os.path.join(RAIZ, "src", "data", "trainers.party")

# Ordem cronológica (decisão 66) e a faixa de nível que cada região passa a ter.
# O topo de uma região é o piso da seguinte: o jogador não perde poder ao trocar
# de continente, e o primeiro treinador da região nova não é um paredão.
ALVO = {
    "Kanto":  (3, 40),
    "Johto":  (22, 58),
    "Hoenn":  (40, 72),
    "Sinnoh": (58, 86),
    "Unova":  (72, 100),
}
# O piso da região seguinte fica ABAIXO do teto da anterior de propósito: quem
# desembarca numa região nova chega mais forte que os primeiros treinadores dela
# e sobe até o topo da faixa lutando. Sem essa sobreposição, cada travessia de
# barco seria um paredão. O inicial de cada região é entregue no piso menos 2
# (Johto 20, Hoenn 38, Sinnoh 55, Unova 70), para nascer útil e não pronto.
ORDEM = ["Kanto", "Johto", "Hoenn", "Sinnoh", "Unova"]

CABECA = re.compile(r"^=== (TRAINER_[A-Z0-9_]+) ===\s*$")
NIVEL = re.compile(r"^(\s*Level:\s*)(\d+)\s*$")


def ids_dos_headers():
    """Nome -> id. Os dois headers têm nomes distintos, então um simples update
    basta; o de Kanto vem por último porque é ele que define a faixa 1400-1799."""
    tabela = {}
    for arq in ("opponents.h", "opponents_frlg.h"):
        caminho = os.path.join(RAIZ, "include", "constants", arq)
        if not os.path.exists(caminho):
            continue
        tabela.update({n: int(v) for n, v in
                       re.findall(r"^#define (TRAINER_[A-Z0-9_]+)\s+(\d+)\s*$",
                                  open(caminho).read(), re.M)})
    return tabela


def regiao(nome, ids):
    if nome.startswith("TRAINER_JOHTO_"):
        return "Johto"
    if nome.startswith("TRAINER_SINNOH_"):
        return "Sinnoh"
    # O prefixo vem antes do id porque os 8 líderes de Unova (TRAINER_UNOVA_
    # LEADER_*) ainda não têm #define em opponents.h: pelo id eles sumiriam da
    # medição, e são justamente os treinadores mais altos da última região.
    if nome.startswith("TRAINER_UNOVA_"):
        return "Unova"
    id_ = ids.get(nome)
    if id_ is None:
        return None
    if 1400 <= id_ <= 1799:
        return "Kanto"
    if 1800 <= id_ <= 2199:
        return "Unova"
    return "Hoenn"


def varre(linhas, ids):
    """Devolve [(regiao, indice_da_linha, nivel)] e o conjunto de nomes sem região."""
    atual, sem_regiao, achados = None, set(), []
    for i, linha in enumerate(linhas):
        m = CABECA.match(linha)
        if m:
            atual = regiao(m.group(1), ids)
            if atual is None:
                sem_regiao.add(m.group(1))
            continue
        m = NIVEL.match(linha)
        if m and atual:
            achados.append((atual, i, int(m.group(2))))
    return achados, sem_regiao


def resumo(achados):
    por_regiao = {}
    for reg, _, nivel in achados:
        por_regiao.setdefault(reg, []).append(nivel)
    return por_regiao


def imprime(titulo, por_regiao):
    print(f"\n{titulo}")
    print(f"{'região':8} {'mons':>6} {'mín':>5} {'média':>7} {'mediana':>8} {'máx':>5}")
    for reg in ORDEM:
        v = por_regiao.get(reg)
        if not v:
            print(f"{reg:8} {'(nenhum)':>6}")
            continue
        print(f"{reg:8} {len(v):6d} {min(v):5d} {statistics.mean(v):7.1f} "
              f"{statistics.median(v):8.1f} {max(v):5d}")


def transforma(nivel, origem, destino):
    """Mapeia linearmente [o_min, o_max] em [d_min, d_max], preservando a forma."""
    o_min, o_max = origem
    d_min, d_max = destino
    if o_max == o_min:
        return d_min
    novo = d_min + (nivel - o_min) * (d_max - d_min) / (o_max - o_min)
    return max(2, min(100, round(novo)))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--aplicar", action="store_true")
    p.add_argument("--seco", action="store_true", help="com --aplicar, não escreve")
    args = p.parse_args()

    ids = ids_dos_headers()
    linhas = open(PARTY).read().splitlines(keepends=True)
    achados, sem_regiao = varre(linhas, ids)
    antes = resumo(achados)
    imprime("CURVA ATUAL (nível de cada Pokémon de treinador)", antes)
    if sem_regiao:
        print(f"\n{len(sem_regiao)} treinadores sem id nos headers (ignorados): "
              f"{sorted(sem_regiao)[:5]}...")

    if not args.aplicar:
        return 0

    # Guarda de idempotência: rodar duas vezes remapearia a faixa já convertida
    # de novo e achataria tudo. Se a região já está na faixa alvo, ela é pulada.
    ja_feitas = [reg for reg, v in antes.items()
                 if reg in ALVO and abs(min(v) - ALVO[reg][0]) <= 1
                 and abs(max(v) - ALVO[reg][1]) <= 1]
    if ja_feitas:
        print(f"\nJÁ NA FAIXA ALVO, não vou mexer: {', '.join(ja_feitas)}")

    origem = {reg: (min(v), max(v)) for reg, v in antes.items()}
    trocas = 0
    for reg, i, nivel in achados:
        if reg not in ALVO or reg in ja_feitas:
            continue
        novo = transforma(nivel, origem[reg], ALVO[reg])
        if novo != nivel:
            m = NIVEL.match(linhas[i])
            linhas[i] = f"{m.group(1)}{novo}\n"
            trocas += 1

    achados2, _ = varre(linhas, ids)
    imprime("CURVA DEPOIS", resumo(achados2))
    print(f"\n{trocas} níveis alterados de {len(achados)}")
    if args.seco:
        print("(--seco: nada escrito)")
        return 0
    with open(PARTY, "w") as f:
        f.writelines(linhas)
    print(f"escrito em {PARTY}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
