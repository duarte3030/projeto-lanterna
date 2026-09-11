#!/usr/bin/env python3
"""Merge de três vias para arquivo em que os DOIS lados só INSERIRAM linhas.

Por que existe
--------------
As branches desta frente acrescentam entrada no FIM da mesma lista (layouts.json,
wild_encounters.json, trainers.party, os três .h de tileset, flags.h, opponents.h,
event_scripts.s, CREDITS.md). O merge do git marca isso como um conflito só, com o
bloco de um lado, o bloco do outro, e a CAUDA compartilhada (o fecho da última
entrada) FORA do conflito. Resolver "os dois lados, um depois do outro" com
copia e cola quebra o arquivo: a cauda fecha só a última entrada, e a entrada do
primeiro lado fica aberta.

Este script não olha os marcadores. Ele lê as TRÊS versões (base, nossa, deles),
confere que cada lado só INSERIU em relação à base (se alguém apagou ou trocou
linha, ele RECUSA e manda resolver à mão) e reconstrói o arquivo aplicando as
inserções dos dois lados na mesma posição da base.

Uso:
    python3 merge3_insercoes.py <base.txt> <nosso.txt> <deles.txt> <saida.txt>
"""
import difflib
import sys


def insercoes(base, lado):
    """Lista de (posicao_na_base, linhas_inseridas). Recusa apagamento e troca."""
    sm = difflib.SequenceMatcher(None, base, lado, autojunk=False)
    fora = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if tag == "insert":
            fora.append((i1, lado[j1:j2]))
        elif tag == "replace":
            # troca = apagamento mais insercao; so aceito quando o pedaco da base
            # reaparece INTEIRO dentro do pedaco do lado (insercao no meio dele).
            if base[i1:i2] == lado[j1:j1 + (i2 - i1)]:
                fora.append((i2, lado[j1 + (i2 - i1):j2]))
            elif base[i1:i2] == lado[j2 - (i2 - i1):j2]:
                fora.append((i1, lado[j1:j2 - (i2 - i1)]))
            else:
                raise SystemExit(
                    "RECUSADO: um dos lados TROCOU linhas da base (linhas %d a %d); "
                    "resolva este arquivo a mao." % (i1 + 1, i2))
        elif tag == "delete":
            raise SystemExit(
                "RECUSADO: um dos lados APAGOU linhas da base (linhas %d a %d); "
                "resolva este arquivo a mao." % (i1 + 1, i2))
    return fora


def main():
    if len(sys.argv) != 5:
        raise SystemExit(__doc__)
    caminhos = sys.argv[1:4]
    base, nosso, deles = [open(c, encoding="utf-8").read().splitlines(keepends=True)
                          for c in caminhos]
    ins_n = insercoes(base, nosso)
    ins_d = insercoes(base, deles)
    # Na MESMA posicao da base, o nosso vem primeiro e o deles depois: a ordem
    # entre dois blocos NOVOS nao muda o jogo (sao entradas no fim de lista), mas
    # precisa ser estavel para o arquivo sair igual se alguem repetir a operacao.
    todas = sorted([(p, 0, ls) for p, ls in ins_n] + [(p, 1, ls) for p, ls in ins_d],
                   key=lambda t: (t[0], t[1]))
    saida = []
    i = 0
    for pos, _, linhas in todas:
        saida.extend(base[i:pos])
        saida.extend(linhas)
        i = pos
    saida.extend(base[i:])
    open(sys.argv[4], "w", encoding="utf-8").writelines(saida)
    print("%s: %d bloco(s) nosso(s) e %d bloco(s) deles, %d linhas de saida"
          % (sys.argv[4], len(ins_n), len(ins_d), len(saida)))


if __name__ == "__main__":
    main()
