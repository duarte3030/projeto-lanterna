#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aplica o de-para de `dev_scripts/traducao_galar.json` no texto de Galar.

Decisao 32 do Gui (`PRD-CARTUCHO-2.md`): Galar fala INGLES, por traducao FIEL
do portugues do demake, com o glossario de `GLOSSARIO-GALAR.md`. Este arquivo e
so a mao que escreve; o julgamento inteiro esta no JSON.

**Casa por ROTULO, nunca por busca de texto solto.** Procurar o portugues no
arquivo e trocar por ingles pareceria mais simples e seria pior: 38 blocos de
Galar sao literalmente `...`, 19 sao `Boa batalha. Obrigado!` e 30 sao a mesma
fala de vendedor. Busca por texto trocaria o bloco errado sem avisar. O rotulo
e unico e o proprio `.inc` diz onde ele comeca e acaba.

**O texto de Galar NAO mora em `data/maps/Galar_*/scripts.inc`.** Os 438
`scripts.inc` daquela regiao tem zero `.string`; os 1.120 blocos de fala estao
em `data/scripts/galar_fala.inc`, `galar_treinadores.inc`, `galar_objetos.inc`,
`galar_placas.inc` e `galar_cenas.inc`. O JSON guarda o caminho de cada bloco e
este script escreve so nesses arquivos.

**Idempotente.** Bloco cujo corpo ja e o `en` do JSON e contado como
`ja_aplicada` e nao e reescrito. Rodar duas vezes da o mesmo arquivo.

**Conservador.** Bloco cujo corpo de hoje nao bate byte a byte com o `pt`
guardado NAO e tocado, e sai listado. Esse e o caso que interessa quando outro
lote reescreve os `galar_*.inc` embaixo desta traducao: o relatorio do
`--dry-run` diz exatamente quais rotulos sairam do lugar, em vez de o aplicador
sobrescrever um texto novo com a traducao de um texto velho.

    python3 dev_scripts/aplica_traducao_galar.py --dry-run   # so relata
    python3 dev_scripts/aplica_traducao_galar.py --aplica     # escreve
    python3 dev_scripts/aplica_traducao_galar.py --demo       # autoteste
"""
from __future__ import print_function

import argparse
import collections
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PADRAO = os.path.join(REPO, "dev_scripts", "traducao_galar.json")

# Um bloco de texto: rotulo sozinho na linha, e as `.string` coladas embaixo.
# `re.M` porque o casamento e por linha; o `+` no fim para no primeiro comando
# que nao e `.string`, que e onde o bloco acaba.
def _bloco(rotulo):
    return re.compile(r'^(%s)(::?)[ \t]*\n((?:[ \t]*\.string ".*"[ \t]*\n)+)'
                      % re.escape(rotulo), re.M)


RE_STRING = re.compile(r'\.string "(.*)"')


def corpo_do_bloco(miolo):
    """Junta as `.string` de um bloco. Devolve o corpo SEM o `$` do fim."""
    inteiro = "".join(RE_STRING.findall(miolo))
    return inteiro[:-1] if inteiro.endswith("$") else inteiro, inteiro.endswith("$")


def escreve_bloco(rotulo, dois_pontos, corpo, indent="\t"):
    """Corpo (sem `$`) -> as linhas `.string` do bloco, com o `$` no fim."""
    partes = re.split(r"(\\[nlp])", corpo)
    linhas, i = [], 0
    while i < len(partes):
        pedaco = partes[i] + (partes[i + 1] if i + 1 < len(partes) else "")
        linhas.append(pedaco)
        i += 2
    if not linhas:
        linhas = [""]
    linhas[-1] += "$"
    texto = "".join('%s.string "%s"\n' % (indent, l) for l in linhas)
    return "%s%s\n%s" % (rotulo, dois_pontos, texto)


def aplica(caminho_json, escreve, raiz=REPO):
    dados = json.load(open(caminho_json, encoding="utf-8"))
    entradas = dados["entradas"]

    por_arquivo = collections.defaultdict(list)
    for e in entradas:
        por_arquivo[e["arquivo"]].append(e)

    conta = collections.Counter()
    recusa = collections.defaultdict(list)
    tocados = []

    for rel, lista in sorted(por_arquivo.items()):
        p = os.path.join(raiz, rel)
        if not os.path.exists(p):
            conta["arquivo_sumiu"] += len(lista)
            recusa["arquivo_sumiu"].append("%s (%d entradas)" % (rel, len(lista)))
            continue
        texto = open(p, encoding="utf-8").read()
        original = texto
        for e in lista:
            rx = _bloco(e["rotulo"])
            achados = list(rx.finditer(texto))
            if not achados:
                conta["rotulo_nao_achado"] += 1
                recusa["rotulo_nao_achado"].append("%s:%s" % (rel, e["rotulo"]))
                continue
            if len(achados) > 1:
                conta["rotulo_ambiguo"] += 1
                recusa["rotulo_ambiguo"].append(
                    "%s:%s (%d vezes)" % (rel, e["rotulo"], len(achados)))
                continue
            m = achados[0]
            corpo, tem_cifrao = corpo_do_bloco(m.group(3))
            if corpo == e["en"]:
                conta["ja_aplicada"] += 1
                continue
            if corpo != e["pt"]:
                conta["texto_mudou"] += 1
                recusa["texto_mudou"].append(
                    "%s:%s\n      json pt: %r\n      arquivo: %r"
                    % (rel, e["rotulo"], e["pt"][:70], corpo[:70]))
                continue
            if not tem_cifrao:
                conta["sem_cifrao"] += 1
                recusa["sem_cifrao"].append("%s:%s" % (rel, e["rotulo"]))
                continue
            novo = escreve_bloco(e["rotulo"], m.group(2), e["en"])
            texto = texto[:m.start()] + novo + texto[m.end():]
            conta["casa"] += 1
        if texto != original:
            tocados.append(rel)
            if escreve:
                open(p, "w", encoding="utf-8").write(texto)

    return conta, recusa, tocados, len(entradas)


def relata(conta, recusa, tocados, total, escreve, limite):
    print("=== aplica_traducao_galar ===")
    print("entradas no JSON        : %d" % total)
    print("casam e seriam trocadas : %d" % conta["casa"])
    print("ja aplicadas (idempot.) : %d" % conta["ja_aplicada"])
    nao = sum(conta[k] for k in ("rotulo_nao_achado", "rotulo_ambiguo",
                                 "texto_mudou", "sem_cifrao", "arquivo_sumiu"))
    print("NAO casam               : %d" % nao)
    for k in ("rotulo_nao_achado", "rotulo_ambiguo", "texto_mudou",
              "sem_cifrao", "arquivo_sumiu"):
        if conta[k]:
            print("  %-20s %d" % (k, conta[k]))
            for linha in recusa[k][:limite]:
                print("    - %s" % linha)
            if len(recusa[k]) > limite:
                print("    ... (%d a mais)" % (len(recusa[k]) - limite))
    print("arquivos afetados       : %d %s" % (len(tocados), tocados))
    if not escreve:
        print("NADA FOI ESCRITO (--dry-run). Rode com --aplica para valer.")
    return 0 if nao == 0 else 1


def demo():
    """Autoteste em arvore de mentira: casa, e idempotente, e recusa o que mudou."""
    import shutil
    import tempfile
    tmp = tempfile.mkdtemp(prefix="aplica_galar_demo_")
    os.makedirs(os.path.join(tmp, "data", "scripts"))
    alvo = os.path.join(tmp, "data", "scripts", "galar_fala.inc")
    open(alvo, "w", encoding="utf-8").write(
        'QA_Um::\n\t.string "Ola, tudo bem?$"\n\n'
        'QA_Dois::\n\t.string "Voce ja viu o ginasio?$"\n\n'
        'QA_Tres::\n\t.string "Alguem trocou este texto$"\n')
    jj = os.path.join(tmp, "traducao.json")
    json.dump({"entradas": [
        {"arquivo": "data/scripts/galar_fala.inc", "rotulo": "QA_Um",
         "pt": "Ola, tudo bem?", "en": "Hello, how are you?"},
        {"arquivo": "data/scripts/galar_fala.inc", "rotulo": "QA_Dois",
         "pt": "Voce ja viu o ginasio?", "en": "Have you seen the Gym?"},
        {"arquivo": "data/scripts/galar_fala.inc", "rotulo": "QA_Tres",
         "pt": "Este e o texto que o JSON guardou", "en": "This is the text"},
        {"arquivo": "data/scripts/galar_fala.inc", "rotulo": "QA_Fantasma",
         "pt": "nao existe", "en": "does not exist"},
    ]}, open(jj, "w"), ensure_ascii=False)

    erros = []
    c, _, _, _ = aplica(jj, escreve=False, raiz=tmp)
    if (c["casa"], c["texto_mudou"], c["rotulo_nao_achado"]) != (2, 1, 1):
        erros.append("dry-run contou %s" % dict(c))
    if 'Hello' in open(alvo, encoding="utf-8").read():
        erros.append("--dry-run ESCREVEU no arquivo")

    c, _, _, _ = aplica(jj, escreve=True, raiz=tmp)
    conteudo = open(alvo, encoding="utf-8").read()
    if '.string "Hello, how are you?$"' not in conteudo:
        erros.append("nao escreveu a traducao: %r" % conteudo)
    if 'Alguem trocou este texto' not in conteudo:
        erros.append("sobrescreveu bloco que nao batia com o pt")

    c2, _, _, _ = aplica(jj, escreve=True, raiz=tmp)
    if c2["casa"] != 0 or c2["ja_aplicada"] != 2:
        erros.append("nao e idempotente: %s" % dict(c2))
    if open(alvo, encoding="utf-8").read() != conteudo:
        erros.append("segunda passada mudou o arquivo")

    shutil.rmtree(tmp, ignore_errors=True)
    if erros:
        for e in erros:
            print("DEMO VERMELHO:", e)
        return 1
    print("DEMO VERDE")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=JSON_PADRAO)
    ap.add_argument("--raiz", default=REPO)
    ap.add_argument("--dry-run", action="store_true", default=True)
    ap.add_argument("--aplica", action="store_true")
    ap.add_argument("--limite", type=int, default=20)
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        return demo()
    escreve = a.aplica
    conta, recusa, tocados, total = aplica(a.json, escreve, a.raiz)
    return relata(conta, recusa, tocados, total, escreve, a.limite)


if __name__ == "__main__":
    sys.exit(main())
