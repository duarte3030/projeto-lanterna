#!/usr/bin/env python3
"""Devolve o `region_map_section` certo aos mapas de Galar que foram RENOMEADOS.

Uso:
    python3 dev_scripts/conserta_mapsec_galar.py            # grava
    python3 dev_scripts/conserta_mapsec_galar.py --seco     # so relata
    python3 dev_scripts/conserta_mapsec_galar.py --demo     # autoteste, sai 1 se cair

Por que este script existe
--------------------------
`dev_scripts/mundo_galar.py` faz duas coisas em ordens diferentes: primeiro
resolve o mapa (passo G2, onde `region_map_section` sai da seção que a FONTE
declara) e só depois renomeia a pasta (passo G3, onde o grafo de warps descobre
que o mapa que o autor jogou no balde `Postwick` é na verdade a Rose Tower).
A renomeação corrige o NOME e não volta para corrigir a SEÇÃO, então 140 mapas
ficaram com o `region_map_section` do balde, `MAPSEC_GALAR_POSTWICK`.

Medido em 06/09/2026, antes deste conserto:

    grep -l MAPSEC_GALAR_POSTWICK data/maps/Galar_*/map.json | wc -l  ->  172
    140 desses 172 são renomeados (o balde), 32 são Postwick de verdade.

Os 32 legítimos são o `balde_sem_nome` de `dev_scripts/galar_mundo.json`: mapas
que nenhum warp limpo ligou a uma seção conhecida, e que por isso ficam mesmo em
`MAPSEC_GALAR_POSTWICK` até alguém dar nome a eles. Este script NÃO os toca.

A verdade é mecânica, não é palpite
-----------------------------------
Fonte: `dev_scripts/galar_mundo.json`, dois campos que o próprio
`mundo_galar.py` escreve:

  1. `renomeados`: {nome velho da pasta -> nome NOVO}, 140 entradas.
     O nome novo é o nome verdadeiro do lugar (`Galar_Postwick09` virou
     `Galar_RoseTower04` porque o grafo de warps ligou aquele mapa à Rose Tower).
  2. `secoes`: {id da seção na fonte -> {slug, mapsec_real, apelido}}, 45
     entradas em 44 slugs distintos (Wild Area tem dois ids na fonte).

A regra que liga um ao outro: tirar `Galar_` do nome novo e casar o resto contra
o slug, aceitando um número no fim e, antes dele, o sufixo de papel `Indoor` ou
`Cave` que o G3 acrescenta pelo `map_type`. Em regex, por slug:

    ^{slug}\\d*$        ou      ^{slug}(Indoor|Cave)\\d*$

Quando mais de um slug casa, vence o MAIS LONGO. Isso importa por causa das
rotas: `Galar_Route0302` casa `Route03` com `\\d*` = `02`, e a alternativa curta
não existe porque não há slug `Route` sozinho. Sem a regra do mais longo, um
slug que fosse prefixo de outro pegaria o mapa errado, e mapa na seção errada
não aparece como erro: aparece como letreiro mentindo o nome do lugar.

Com essa regra os 140 resolvem, sem sobra e sem ambiguidade (o `--demo` trava
nos dois: zero sem resolver e zero com mais de um slug do mesmo tamanho).

O que é gravado é o APELIDO (`MAPSEC_GALAR_ROSE_TOWER`), não a MAPSEC real
(`MAPSEC_GALAR_NORTH`). Os dois são o mesmo valor de u8: os 42 apelidos são
`#define` para as 6 seções reais em `include/constants/region_map_sections.h`,
porque só cabem 36 entradas novas no enum (ver o comentário em
`mundo_galar.py`). O apelido é que carrega o nome do lugar, e é dele que
`dev_scripts/nomes_popup.py` tira o letreiro de mapa.

Distribuição de destino, por MAPSEC real (conferida pelo `--demo`):

    MAPSEC_GALAR_CENTRAL         78
    MAPSEC_GALAR_NORTH           33
    MAPSEC_GALAR_SOUTH           12
    MAPSEC_GALAR_ISLE_OF_ARMOR   12
    MAPSEC_GALAR_CROWN_TUNDRA     5

Idempotência
------------
Rodar duas vezes não muda nada na segunda: o script compara o valor que quer
escrever com o que já está no arquivo e só grava quando diferem. A segunda
passada relata `0 gravados`.
"""
import argparse
import json
import os
import re
import sys
import collections

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPAS = os.path.join(RAIZ, "data/maps")
CENSO = os.path.join(RAIZ, "dev_scripts/galar_mundo.json")
CABECALHO = os.path.join(RAIZ, "include/constants/region_map_sections.h")
PREFIXO = "Galar_"
PAPEIS = ("Indoor", "Cave")


def le_censo():
    return json.load(open(CENSO, encoding="utf-8"))


def slugs_por_nome(censo):
    """slug -> {'slug','mapsec_real','apelido'}, sem repetir (Wild Area tem 2 ids)."""
    por_slug = {}
    for secao in censo["secoes"].values():
        por_slug.setdefault(secao["slug"], secao)
    return por_slug


def resolve(nome_da_pasta, por_slug):
    """(secao, candidatos) do nome NOVO da pasta. secao None quando não resolve."""
    if not nome_da_pasta.startswith(PREFIXO):
        return None, []
    resto = nome_da_pasta[len(PREFIXO):]
    papel = "|".join(PAPEIS)
    casaram = [s for s in por_slug
               if re.fullmatch(re.escape(s) + r"\d*", resto)
               or re.fullmatch(re.escape(s) + r"(?:%s)\d*" % papel, resto)]
    if not casaram:
        return None, []
    maior = max(len(s) for s in casaram)
    empatados = [s for s in casaram if len(s) == maior]
    return por_slug[empatados[0]], empatados


def plano(censo=None):
    """[(pasta, mapsec_atual, apelido_certo, mapsec_real)] dos 140 renomeados."""
    censo = censo or le_censo()
    por_slug = slugs_por_nome(censo)
    linhas, sem_resolver, ambiguos, sem_pasta = [], [], [], []
    for _velho, novo in sorted(censo["renomeados"].items()):
        caminho = os.path.join(MAPAS, novo, "map.json")
        if not os.path.exists(caminho):
            sem_pasta.append(novo)
            continue
        secao, empatados = resolve(novo, por_slug)
        if secao is None:
            sem_resolver.append(novo)
            continue
        if len(empatados) > 1:
            ambiguos.append((novo, empatados))
            continue
        atual = json.load(open(caminho, encoding="utf-8")).get("region_map_section")
        linhas.append((novo, atual, secao["apelido"], secao["mapsec_real"]))
    return linhas, sem_resolver, ambiguos, sem_pasta


def grava(pasta, apelido):
    """Escreve só o campo `region_map_section`. Devolve True se o arquivo mudou."""
    caminho = os.path.join(MAPAS, pasta, "map.json")
    with open(caminho, encoding="utf-8") as f:
        doc = json.load(f)
    if doc.get("region_map_section") == apelido:
        return False
    doc["region_map_section"] = apelido
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return True


def conta_postwick():
    n = 0
    for pasta in sorted(os.listdir(MAPAS)):
        if not pasta.startswith(PREFIXO):
            continue
        caminho = os.path.join(MAPAS, pasta, "map.json")
        if not os.path.exists(caminho):
            continue
        if json.load(open(caminho, encoding="utf-8")).get(
                "region_map_section") == "MAPSEC_GALAR_POSTWICK":
            n += 1
    return n


def autoteste():
    """Trava os fatos que fazem este script ser mecânico, e não palpite."""
    censo = le_censo()
    falhou = []

    def confere(o_que, deu, esperado):
        ok = deu == esperado
        print("  %-52s %s  (%s)" % (o_que, "OK" if ok else "CAIU", deu))
        if not ok:
            falhou.append((o_que, deu, esperado))

    linhas, sem_resolver, ambiguos, sem_pasta = plano(censo)
    confere("renomeados no censo", len(censo["renomeados"]), 140)
    confere("resolvidos", len(linhas), 140)
    confere("sem resolver", sem_resolver, [])
    confere("ambiguos (dois slugs do mesmo tamanho)", ambiguos, [])
    confere("pasta do nome novo que nao existe em disco", sem_pasta, [])

    # O balde legitimo nao pode ser tocado: os 32 do `balde_sem_nome` continuam
    # em MAPSEC_GALAR_POSTWICK, e nenhum deles esta no plano.
    balde = set(censo["balde_sem_nome"])
    confere("balde_sem_nome", len(balde), 32)
    confere("balde dentro do plano (tem que ser 0)",
            len([l for l in linhas if l[0] in balde]), 0)

    # A distribuicao de destino, medida em 06/09/2026.
    reais = collections.Counter(l[3] for l in linhas)
    confere("destino CENTRAL", reais["MAPSEC_GALAR_CENTRAL"], 78)
    confere("destino NORTH", reais["MAPSEC_GALAR_NORTH"], 33)
    confere("destino SOUTH", reais["MAPSEC_GALAR_SOUTH"], 12)
    confere("destino ISLE_OF_ARMOR", reais["MAPSEC_GALAR_ISLE_OF_ARMOR"], 12)
    confere("destino CROWN_TUNDRA", reais["MAPSEC_GALAR_CROWN_TUNDRA"], 5)

    # Todo apelido que vamos escrever tem que EXISTIR no cabecalho. Sem isto o
    # conserto compila errado, e o erro so aparece no build.
    texto = open(CABECALHO, encoding="utf-8").read()
    existem = set(re.findall(r"MAPSEC_GALAR_[A-Z0-9_]+", texto))
    faltando = sorted({l[2] for l in linhas} - existem)
    confere("apelidos que o cabecalho nao tem", faltando, [])

    # A regra do slug mais longo, no caso que a motivou.
    por_slug = slugs_por_nome(censo)
    confere("Galar_Route0302 resolve para ROUTE03",
            (resolve("Galar_Route0302", por_slug)[0] or {}).get("apelido"),
            "MAPSEC_GALAR_ROUTE03")
    confere("Galar_TurffieldIndoor07 resolve para TURFFIELD",
            (resolve("Galar_TurffieldIndoor07", por_slug)[0] or {}).get("apelido"),
            "MAPSEC_GALAR_TURFFIELD")
    confere("Galar_CrownTundraIndoor01 resolve para CROWN_TUNDRA",
            (resolve("Galar_CrownTundraIndoor01", por_slug)[0] or {}).get("apelido"),
            "MAPSEC_GALAR_CROWN_TUNDRA")

    print("\n%s" % ("autoteste: tudo de pe" if not falhou
                    else "autoteste: %d caiu" % len(falhou)))
    return 1 if falhou else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seco", action="store_true", help="nao escreve nada")
    ap.add_argument("--demo", action="store_true", help="autoteste")
    ap.add_argument("--autoteste", action="store_true", help="autoteste")
    args = ap.parse_args()

    if args.demo or args.autoteste:
        return autoteste()

    linhas, sem_resolver, ambiguos, sem_pasta = plano()
    if sem_resolver or ambiguos or sem_pasta:
        print("PAREI: a regra nao fecha.")
        for x in sem_resolver:
            print("  sem slug:", x)
        for x, e in ambiguos:
            print("  ambiguo:", x, e)
        for x in sem_pasta:
            print("  pasta sumida:", x)
        return 1

    print("POSTWICK antes: %d" % conta_postwick())
    mudar = [l for l in linhas if l[1] != l[2]]
    gravados = 0
    if not args.seco:
        for pasta, _atual, apelido, _real in mudar:
            gravados += grava(pasta, apelido)
    print("renomeados no plano: %d" % len(linhas))
    print("ja estavam certos:   %d" % (len(linhas) - len(mudar)))
    print("%s: %d" % ("gravariam" if args.seco else "gravados", gravados
                      if not args.seco else len(mudar)))
    reais = collections.Counter(l[3] for l in linhas)
    for k in sorted(reais):
        print("  %-28s %3d" % (k, reais[k]))
    print("POSTWICK depois: %d" % conta_postwick())
    return 0


if __name__ == "__main__":
    sys.exit(main())
