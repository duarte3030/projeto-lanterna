# -*- coding: utf-8 -*-
"""Fecha o lote I da onda 2: requebra por pixel, valida e faz o merge.

Le `dev_scripts/onda2_lote_i_blocos/en/NNN.txt` (so o ingles, sem `$`),
requebra contra 208 px com o requebrador de `texto_placas_sinnoh.py`, valida
contra o `pt` do bloco correspondente e grava:

  - `dev_scripts/onda2_lote_i_blocos/validacao.txt` (so contagem e indice)
  - `dev_scripts/resgate_galar_texto.json` (`{"entradas": [{"pt","en"}]}`),
    sem apagar entrada que ja esteja la.

Nenhum trecho de texto e impresso na saida: so numero e indice.
"""
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
import texto_placas_sinnoh as TXT  # noqa: E402

BLOCOS = os.path.join(RAIZ, "dev_scripts", "onda2_lote_i_blocos")
EN = os.path.join(BLOCOS, "en")
VALIDACAO = os.path.join(BLOCOS, "validacao.txt")
DESTINO = os.path.join(RAIZ, "dev_scripts", "resgate_galar_texto.json")

CHAVE = re.compile(r"\{[^}]*\}")


def itens():
    """[(indice global, pt, chaves)] na ordem dos blocos."""
    saida = []
    for nn in range(100):
        caminho = os.path.join(BLOCOS, "bloco_%02d.json" % nn)
        if not os.path.exists(caminho):
            break
        for i, it in enumerate(json.load(open(caminho, encoding="utf-8"))):
            saida.append((nn * 5 + i, it["pt"], it["chaves"]))
    return saida


def fora_do_charmap(texto):
    """Quantidade de caracteres que o charmap do repo nao tem."""
    cmap, _ = TXT._regua()
    limpo = CHAVE.sub("", texto)
    limpo = re.sub(r"\\[nlp]", "", limpo)
    return sum(1 for c in limpo if c not in cmap)


def linhas_largas(texto):
    """Quantas linhas do corpo passam de 208 px."""
    n = 0
    for caixa in texto.split("\\p"):
        for linha in re.split(r"\\[nl]", caixa):
            if TXT.largura_px(linha) > TXT.LARGURA_CAIXA:
                n += 1
    return n


def main():
    conta = dict(total=0, com_en=0, sem_en=0, ok=0,
                 token=0, paragrafo=0, charmap=0, largura=0)
    problemas = []
    entradas = []
    for idx, pt, chaves in itens():
        conta["total"] += 1
        caminho = os.path.join(EN, "%03d.txt" % idx)
        if not os.path.exists(caminho):
            conta["sem_en"] += 1
            continue
        conta["com_en"] += 1
        bruto = open(caminho, encoding="utf-8").read().strip("\n")
        en = TXT.requebra(bruto)
        ruins = []
        if CHAVE.findall(pt) != CHAVE.findall(en):
            ruins.append("token")
        if pt.count("\\p") != en.count("\\p"):
            ruins.append("paragrafo")
        if fora_do_charmap(en):
            ruins.append("charmap")
        if linhas_largas(en):
            ruins.append("largura")
        for r in ruins:
            conta[r] += 1
        if ruins:
            problemas.append((idx, chaves, ruins))
        else:
            conta["ok"] += 1
        entradas.append(dict(pt=pt, en=en))

    velhas = []
    if os.path.exists(DESTINO):
        velhas = json.load(open(DESTINO, encoding="utf-8")).get("entradas", [])
    antes = len(velhas)
    juntas = {e["pt"]: e for e in velhas}
    for e in entradas:
        juntas[e["pt"]] = e
    corpo = dict(_leia=("de-para escrito a mao para o lote I da onda 2 da "
                        "Frente A, com o GLOSSARIO-GALAR.md; o ingles ja sai "
                        "requebrado a 208 px"),
                 entradas=list(juntas.values()))
    json.dump(corpo, open(DESTINO, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    with open(VALIDACAO, "w", encoding="utf-8") as f:
        f.write("lote I, onda 2, Frente A: validacao\n")
        for k in ("total", "com_en", "sem_en", "ok",
                  "token", "paragrafo", "charmap", "largura"):
            f.write("%-11s %d\n" % (k, conta[k]))
        f.write("entradas em resgate_galar_texto.json: %d -> %d\n"
                % (antes, len(juntas)))
        f.write("\nindices com problema (indice, chaves, o que falhou)\n")
        for idx, chaves, ruins in problemas:
            f.write("%03d\t%s\t%s\n" % (idx, ",".join(chaves), ",".join(ruins)))
        if not problemas:
            f.write("(nenhum)\n")
    print(json.dumps(dict(conta, antes=antes, depois=len(juntas),
                          problemas=[p[0] for p in problemas])))


if __name__ == "__main__":
    main()
