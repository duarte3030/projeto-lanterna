#!/usr/bin/env python3
"""Confere o que entrou na ROM, nao o que esta escrito no JSON.

Uso:
    python3 dev_scripts/valida_rom.py

Existe por causa do erro mais caro da sessao de 05/08/2026.

Kanto tinha 421 mapas em map_groups.json, 344 layouts em layouts.json, warp de
barco funcionando e constante MAP_VERMILION_CITY apontando para a pasta certa.
O `valida_conectividade.py` dizia que Kanto era alcancavel. **Kanto nao estava na
ROM.** O gerador de mapas descartava tudo em silencio, porque os mapas vinham
marcados REGION_KANTO e os layouts vinham marcados layout_version=frlg, e o
filtro do upstream existe para buildar Emerald OU FireRed, nunca os dois.

O sintoma no jogo era tela preta com o sprite do jogador em cima. Sprite e OAM e
nao depende de layout.

Nenhum validador pegou porque **todos liam o JSON**. Contar linha de JSON nao
prova nada sobre a ROM. Este script fecha esse buraco comparando as duas pontas:
o que foi declarado e o que o build de fato emitiu.

O que ele confere:
  1. mapa declarado em map_groups.json que nao virou cabecalho em data/maps/headers.inc
  2. layout declarado em layouts.json que nao virou entrada em data/layouts/layouts.inc
  3. tileset citado por um layout que nao existe como simbolo na ROM
  4. blockdata citado por um layout cujo arquivo nao existe em disco
"""
import json
import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def simbolos_da_rom():
    """Nomes globais dentro do ELF. Vazio se ainda nao buildou."""
    elf = f"{RAIZ}/pokeemerald.elf"
    if not os.path.exists(elf):
        return None
    dka = os.environ.get("DEVKITARM", "")
    nm = f"{dka}/bin/arm-none-eabi-nm"
    if not os.path.exists(nm):
        nm = "nm"
    try:
        r = subprocess.run([nm, elf], capture_output=True, text=True, timeout=120)
    except Exception:
        return None
    return {l.split()[-1] for l in r.stdout.splitlines() if l.split()}


def le(caminho):
    p = f"{RAIZ}/{caminho}"
    return open(p, errors="ignore").read() if os.path.exists(p) else ""


def main():
    grupos = json.load(open(f"{RAIZ}/data/maps/map_groups.json"))
    layouts = json.load(open(f"{RAIZ}/data/layouts/layouts.json"))["layouts"]

    headers_inc = le("data/maps/headers.inc")
    layouts_inc = le("data/layouts/layouts.inc")
    if not headers_inc or not layouts_inc:
        print("arquivos gerados ausentes. Rode `make` antes.")
        return 0

    problemas = []

    # 1. mapa declarado que nao virou cabecalho.
    # headers.inc e uma lista de `.include "data/maps/<Nome>/header.inc"`, nao
    # de rotulos `Nome::`. Procurar rotulo aqui devolvia "0 mapas na ROM", que
    # e falso positivo total: o jeito de nao confiar num validador e ele acusar
    # o jogo inteiro.
    declarados = [m for g in grupos["group_order"] for m in grupos.get(g, [])]
    emitidos = set(re.findall(r'\.include\s+"data/maps/([^/]+)/header\.inc"',
                              headers_inc))
    sumidos = [m for m in declarados if m not in emitidos]
    if sumidos:
        problemas.append(
            (f"{len(sumidos)} mapas declarados NAO entraram na ROM", sumidos))

    # 2. layout declarado que nao virou entrada.
    # Separar dois casos que a primeira versao juntava, e por isso o gate acusava
    # 146 problemas antigos a cada rodada, escondendo os novos:
    #   - SEM DADO EM DISCO: layout declarado no JSON cujo border.bin nem existe.
    #     Sao restos de variante (Suicune, Raikou, Modern, Old) que nunca tiveram
    #     geometria. Nao e regressao, e o gerador pula de proposito.
    #   - COM DADO E MESMO ASSIM FORA: esse e o bug de verdade, o que derrubou
    #     Kanto. O arquivo existe e o build nao emitiu.
    nomes_inc = set(re.findall(r"^(\w+)::", layouts_inc, re.M))
    sem_dado, com_dado = [], []
    for l in layouts:
        if l["name"] in nomes_inc:
            continue
        bp = l.get("border_filepath", "")
        (com_dado if bp and os.path.exists(f"{RAIZ}/{bp}") else sem_dado).append(l["name"])
    lay_sumidos = sem_dado + com_dado
    if com_dado:
        problemas.append(
            (f"{len(com_dado)} layouts TEM dado em disco e NAO entraram na ROM",
             com_dado))
    if sem_dado:
        print(f"(informativo: {len(sem_dado)} layouts declarados sem border.bin em "
              f"disco, restos de variante; o gerador pula de proposito)")

    # 3. tileset citado que nao existe como simbolo
    simbolos = simbolos_da_rom()
    if simbolos:
        citados = set()
        for l in layouts:
            for k in ("primary_tileset", "secondary_tileset"):
                v = l.get(k)
                # "0" e ausencia legitima de tileset secundario (UnusedOutdoorArea)
                if v and v != "0":
                    citados.add(v)
        faltando = sorted(t for t in citados if t not in simbolos)
        if faltando:
            problemas.append(
                (f"{len(faltando)} tilesets citados NAO existem na ROM", faltando))

    # 4. blockdata citado sem arquivo em disco.
    # So e problema se o layout CHEGOU na ROM assim: aí o jogo tem uma entrada
    # apontando para nada. Layout sem dado que tambem ficou fora da tabela ja foi
    # contado como informativo no item 2, e repetir aqui era o que fazia o gate
    # acusar 146 itens antigos toda vez.
    sem_arquivo = [l["name"] for l in layouts
                   if l.get("blockdata_filepath")
                   and not os.path.exists(f"{RAIZ}/{l['blockdata_filepath']}")
                   and l["name"] in nomes_inc]
    if sem_arquivo:
        problemas.append(
            (f"{len(sem_arquivo)} layouts NA ROM com blockdata inexistente",
             sem_arquivo))

    print(f"declarados: {len(declarados)} mapas, {len(layouts)} layouts")
    print(f"na ROM:     {len(declarados)-len(sumidos)} mapas, "
          f"{len(layouts)-len(lay_sumidos)} layouts")
    if not problemas:
        print("\nTUDO QUE FOI DECLARADO ENTROU NA ROM.")
        return 0

    for titulo, lista in problemas:
        print(f"\n=== {titulo} ===")
        for x in lista[:12]:
            print(f"   {x}")
        if len(lista) > 12:
            print(f"   ... e mais {len(lista)-12}")
    print("\nMapa declarado que nao entra na ROM vira tela preta no jogo, "
          "e nenhum validador de JSON enxerga isso.")
    return 1


def demo():
    """A regra que importa: declarado sem emitido acusa, e emitido nao acusa.

    A segunda asserção existe porque a primeira versao lia headers.inc
    procurando rotulo `Nome::`, e o arquivo e uma lista de `.include`. Resultado:
    "0 de 1615 mapas na ROM", ou seja, acusou o jogo inteiro. Validador que
    acusa tudo e tao inutil quanto o que nao acusa nada.
    """
    inc = ('\t.include "data/maps/TwinleafTown/header.inc"\n'
           '\t.include "data/maps/NewBarkTown/header.inc"\n')
    emit = set(re.findall(r'\.include\s+"data/maps/([^/]+)/header\.inc"', inc))
    assert emit == {"TwinleafTown", "NewBarkTown"}, emit

    decl = ["PalletTown", "TwinleafTown"]
    assert [m for m in decl if m not in emit] == ["PalletTown"]
    assert [m for m in ["TwinleafTown", "NewBarkTown"] if m not in emit] == []
    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
