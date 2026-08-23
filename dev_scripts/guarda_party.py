#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guarda: os 236 chefes da Fase F que estao em src/data/trainers.party batem,
byte a byte, com dev_scripts/fase_f_chefes.json, que e a fonte da verdade deles.

Nasceu de um acidente que estava a UM comando de acontecer, e que a 0.r
registrou como "hoje e disciplina de quem roda, e nao guarda":
`treinadores_galar.py --aplicar` regera o bloco de Galar do `.party` inteiro, e
38 dos 236 chefes da Fase F moram dentro desse bloco. Quem rodasse o gerador e
esquecesse `fase_f_chefes.py --aplicar` em seguida trocava 38 times de chefe
por time cru (so especie e Level: 255) sem erro de build nenhum: o arquivo
continua valido, a ROM continua compilando, e o unico sintoma seria o lider de
ginasio brigando com Pokemon sem golpe, item nem gimmick.

    python3 dev_scripts/guarda_party.py          # verde/vermelho
    python3 dev_scripts/guarda_party.py --demo   # planta um chefe cru e exige vermelho

O gerador tambem aprendeu a nao pisar (`times_preservados`), entao o acidente
tem dois freios independentes. Este aqui e o que pega tambem a edicao a mao e
qualquer outro script futuro que resolva reescrever o `.party`.

Nao valida a tabela (isso e `fase_f_chefes.py --demo`, que le o motor): so
compara o arquivo com o que a tabela mandaria escrever, usando o MESMO escritor
de `fase_f_chefes`, para nao existir um segundo parser que possa discordar do
primeiro.
"""
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, 'dev_scripts'))
import fase_f_chefes as FF  # noqa: E402


def blocos(texto):
    """{constante: bloco inteiro, do '=== X ===' ate o proximo}."""
    ms = list(re.finditer(r'(?m)^=== (\S+) ===[ \t]*$', texto))
    return {m.group(1): texto[m.start():
                              ms[k + 1].start() if k + 1 < len(ms) else len(texto)]
            for k, m in enumerate(ms)}


def verifica(texto=None, doc=None):
    """Lista de reprovacoes, em texto. Lista vazia = arquivo fiel a tabela."""
    doc = json.load(open(FF.JSON, encoding='utf-8')) if doc is None else doc
    texto = open(FF.PARTY, encoding='utf-8').read() if texto is None else texto
    tem = blocos(texto)
    erros = ['%s: chefe da tabela sem bloco nenhum no .party' % c['id']
             for c in doc['chefes'] if c['id'] not in tem]
    esperado = blocos(FF.escreve(doc, texto)[0])
    for c in doc['chefes']:
        tid = c['id']
        if tid in tem and esperado.get(tid) != tem[tid]:
            crus = sum(1 for ln in tem[tid].split('\n') if ln.startswith('- MOVE_'))
            erros.append('%s (%s): o time no .party nao e o da tabela '
                         '(%d golpes escritos, a tabela pede %d)'
                         % (tid, c['regiao'], crus, 4 * len(c['time'])))
    return erros


def demo():
    """Duas mutacoes plantadas, e a segunda e o acidente de verdade."""
    ok = True

    def caso(nome, cond):
        nonlocal ok
        print('  %-62s %s' % (nome, 'ok' if cond else 'REPROVOU'))
        ok = ok and cond

    doc = json.load(open(FF.JSON, encoding='utf-8'))
    texto = open(FF.PARTY, encoding='utf-8').read()
    caso('o .party de hoje passa (senao o resto nao prova nada)',
         verifica(texto, doc) == [])

    # 1: um chefe qualquer perde um golpe. Reprova por diferenca.
    alvo = doc['chefes'][0]['id']
    b = blocos(texto)[alvo]
    sujo = texto.replace(b, b.replace('- MOVE_', '- MOVE_TACKLE @ ', 1), 1)
    e = verifica(sujo, doc)
    caso('um golpe trocado num chefe reprova', any(alvo in x for x in e))

    # 2: O ACIDENTE. Um chefe de Galar volta ao molde cru que
    # `treinadores_galar.bloco_party` escrevia: cabecalho, especie e Level 255,
    # sem AI, sem golpe, sem item.
    galar = next(c for c in doc['chefes'] if c['regiao'] == 'galar')
    b = blocos(texto)[galar['id']]
    cab = [ln for ln in b.split('\n')
           if re.match(r'^(=== |Name:|Class:|Pic:|Gender:|Double Battle:)', ln)]
    cru = '\n'.join(cab + [x for m in galar['time']
                           for x in ('', m['especie'], 'Level: 255')] + ['', ''])
    e = verifica(texto.replace(b, cru, 1), doc)
    caso('um chefe de Galar com o time CRU reprova',
         any(galar['id'] in x for x in e))
    caso('e so ele reprova, nao o arquivo inteiro', len(e) == 1)

    print('\n%s' % ('demo verde' if ok else 'DEMO REPROVOU'))
    return 0 if ok else 1


def main():
    if '--demo' in sys.argv:
        return demo()
    doc = json.load(open(FF.JSON, encoding='utf-8'))
    erros = verifica(doc=doc)
    if not erros:
        print('chefes da Fase F: %d conferidos em %s, todos como a tabela manda'
              % (len(doc['chefes']), os.path.relpath(FF.PARTY, RAIZ)))
        return 0
    print('%d CHEFE(S) DA FASE F FORA DA TABELA:' % len(erros))
    for e in erros:
        print('  ' + e)
    print('\nConserto: python3 dev_scripts/fase_f_chefes.py --aplicar')
    return 1


if __name__ == '__main__':
    sys.exit(main())
