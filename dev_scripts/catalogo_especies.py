#!/usr/bin/env python3
"""Catálogo das espécies, lido de `src/data/pokemon/species_info/gen_*_families.h`.

    python3 dev_scripts/catalogo_especies.py          # resumo por geração
    python3 dev_scripts/catalogo_especies.py --demo   # asserts, não toca em nada

Por que ler o species_info e não o `species.h`
----------------------------------------------
O enum de `include/constants/species.h` mistura espécie-base e FORMA na mesma
sequência: neste repo as bases de gen 1 a 8 vão de 1 a 905, as formas (mega,
gmax, regionais) ocupam 906 a 1288, e só então a gen 9 começa em 1289. Quem
classificar geração por faixa de id coloca `SPECIES_VENUSAUR_MEGA` (906) na
gen 9. O `species_info` não tem esse problema: cada arquivo `gen_N_families.h`
é a geração N por construção, e forma se distingue de base porque a forma herda
o `.natDexNum` da base (`SPECIES_VENUSAUR_MEGA` tem `NATIONAL_DEX_VENUSAUR`).

A geração TAMBÉM não sai do arquivo em que a entrada mora, e essa foi a segunda
armadilha: `gen_N_families.h` é organizado por FAMÍLIA, não por geração, então
`SPECIES_ANNIHILAPE` (gen 9) e `SPECIES_BELLOSSOM` (gen 2) vivem dentro de
`gen_1_families.h`, junto do Mankey e do Oddish de quem descendem. Contar por
arquivo dava 188 bases na gen 1, contra as 151 de verdade. A geração honesta é
a faixa do NÚMERO da Pokédex nacional, lido de `include/constants/pokedex.h`.

O que este módulo entrega, e é o que o resto do B8 consome:
    especie.gen        1 a 9, pela faixa do número de dex nacional
    especie.tipos      ('TYPE_GRASS',) ou ('TYPE_GRASS', 'TYPE_DARK')
    especie.bst        soma dos seis stats base, que é a régua de dificuldade
    especie.lenda      True para sub-legendária, restrita, mítica, UB ou paradox
    especie.base       False para mega/gmax/totem/regional/qualquer forma
    especie.familia    o `P_FAMILY_*` que liga ou desliga a entrada na build

Só entra no catálogo quem tem `.natDexNum`; entrada sem ele é placeholder.
"""
import argparse
import collections
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INFO = os.path.join(RAIZ, "src", "data", "pokemon", "species_info")

# Marcadores que provam que a entrada é FORMA e não espécie-base. Medidos com
# `grep -o '\.is[A-Za-z]*\s*=\s*TRUE'` nos nove arquivos: são os únicos campos
# booleanos de forma que aparecem lá.
FORMA = ("isMegaEvolution", "isPrimalReversion", "isGigantamax", "isTotem",
         "isAlolanForm", "isGalarianForm", "isHisuianForm", "isPaldeanForm",
         "isUltraBurst", "isTeraForm")
# Marcadores de "não é bicho de mato". Lenda entra em líder e E4, não na grama.
LENDA = ("isSubLegendary", "isRestrictedLegendary", "isMythical",
         "isUltraBeast", "isParadox")

Especie = collections.namedtuple(
    "Especie", "nome gen dex tipos bst lenda base familia stats")

# Último número de dex nacional de cada geração. Faixa, não arquivo.
FIM_DA_GEN = (151, 251, 386, 493, 649, 721, 809, 905, 1025)


def _dex_numeros():
    """{NATIONAL_DEX_X: número}. O enum de `pokedex.h` começa em NONE = 0."""
    txt = open(os.path.join(RAIZ, "include/constants/pokedex.h")).read()
    fora, n = {}, -1
    for m in re.finditer(r"^\s*(NATIONAL_DEX_[A-Z0-9_]+)\s*(?:=\s*(\d+))?\s*,",
                         txt, re.M):
        n = int(m.group(2)) if m.group(2) else n + 1
        fora.setdefault(m.group(1), n)
    return fora


def _gen_do_dex(n):
    for i, fim in enumerate(FIM_DA_GEN, start=1):
        if n <= fim:
            return i
    return len(FIM_DA_GEN)


def _blocos(txt):
    """Fatia o arquivo em (SPECIES_X, corpo), do `[SPECIES_X] = {` até o `},`.

    Corte por chave contada, não por regex de bloco: o corpo tem `{` de
    `MON_TYPES(...)`, de `.abilities = { ... }` e das strings de descrição.
    """
    for m in re.finditer(r"^\s*\[(SPECIES_[A-Z0-9_]+)\]\s*=\s*$", txt, re.M):
        i = txt.index("{", m.end())
        nivel, j = 0, i
        while j < len(txt):
            if txt[j] == "{":
                nivel += 1
            elif txt[j] == "}":
                nivel -= 1
                if nivel == 0:
                    break
            j += 1
        yield m.group(1), txt[i:j]


def _familia_de(txt, pos):
    """O `#if P_FAMILY_*` aberto na posição `pos`, ou None."""
    ult = None
    for m in re.finditer(r"^#if\s+(P_FAMILY_[A-Z0-9_]+)", txt[:pos], re.M):
        ult = m.group(1)
    return ult


STATS = ("baseHP", "baseAttack", "baseDefense",
         "baseSpeed", "baseSpAttack", "baseSpDefense")


def carrega():
    """{nome: Especie} com TODA entrada que tem natDexNum, base e forma."""
    dexnum = _dex_numeros()
    fora = {}
    for gen in range(1, 10):
        caminho = os.path.join(INFO, f"gen_{gen}_families.h")
        txt = open(caminho, encoding="utf-8").read()
        for nome, corpo in _blocos(txt):
            dex = re.search(r"\.natDexNum\s*=\s*NATIONAL_DEX_([A-Z0-9_]+)", corpo)
            if not dex:
                continue  # placeholder sem dex: não é espécie jogável
            stats = {}
            for s in STATS:
                m = re.search(r"\.%s\s*=\s*(\d+)" % s, corpo)
                stats[s] = int(m.group(1)) if m else 0
            tipos = ()
            m = re.search(r"\.types\s*=\s*MON_TYPES\(([^)]*)\)", corpo)
            if m:
                tipos = tuple(t.strip() for t in m.group(1).split(",") if t.strip())
            forma = any(re.search(r"\.%s\s*=\s*TRUE" % f, corpo) for f in FORMA)
            # A forma também se denuncia pelo dex herdado: SPECIES_VENUSAUR_MEGA
            # tem NATIONAL_DEX_VENUSAUR. Vale para gmax/regional que não marcam
            # booleano nenhum (SPECIES_DEOXYS_ATTACK e afins).
            base = not forma and nome == "SPECIES_" + dex.group(1)
            n = dexnum["NATIONAL_DEX_" + dex.group(1)]
            fora[nome] = Especie(
                nome=nome, gen=_gen_do_dex(n), dex=n, tipos=tipos,
                bst=sum(stats.values()),
                lenda=any(re.search(r"\.%s\s*=\s*TRUE" % f, corpo) for f in LENDA),
                base=base,
                familia=_familia_de(txt, txt.index(corpo)),
                stats=stats)

    # 65 espécies não têm entrada com o nome "cru": o Unown só existe como
    # `SPECIES_UNOWN_A`, o Flabébé como `SPECIES_FLABEBE_RED`, o Aegislash como
    # `SPECIES_AEGISLASH_SHIELD`. Sem este remendo elas sumiam do catálogo e
    # nunca entrariam em encontro nenhum. Para cada número de dex órfão, a
    # PRIMEIRA entrada não marcada como forma (a ordem do arquivo é a ordem do
    # enum) vira a representante, que é a forma padrão em todos os casos.
    tem = {e.dex for e in fora.values() if e.base}
    for nome, e in list(fora.items()):
        if e.dex in tem or e.base:
            continue
        if re.search(r"_(MEGA|GMAX|TOTEM)", nome):
            continue
        fora[nome] = e._replace(base=True)
        tem.add(e.dex)
    return fora


def validas():
    """Nomes que o `species.h` de fato define. Régua de validação de escrita."""
    txt = open(os.path.join(RAIZ, "include/constants/species.h")).read()
    return set(re.findall(r"\bSPECIES_[A-Z0-9_]+", txt))


def demo():
    cat = carrega()
    v = validas()
    assert len(cat) > 1300, len(cat)
    faltam = [n for n in cat if n not in v]
    assert not faltam, faltam[:5]

    # A armadilha que motivou o módulo: mega de gen 1 não pode virar gen 9.
    assert cat["SPECIES_VENUSAUR_MEGA"].gen == 1
    assert not cat["SPECIES_VENUSAUR_MEGA"].base
    assert cat["SPECIES_VENUSAUR"].base and cat["SPECIES_VENUSAUR"].gen == 1
    assert cat["SPECIES_SPRIGATITO"].gen == 9 and cat["SPECIES_SPRIGATITO"].base

    # Tipo e stat vindos do arquivo, não de memória.
    assert cat["SPECIES_SPRIGATITO"].tipos == ("TYPE_GRASS",)
    assert cat["SPECIES_SPRIGATITO"].bst == 310, cat["SPECIES_SPRIGATITO"].bst
    assert cat["SPECIES_GRENINJA"].tipos == ("TYPE_WATER", "TYPE_DARK")

    # Lenda: quem é e quem não é.
    # Xerneas e Zygarde so existem como FORMA nomeada; o remendo de
    # representante e o que os mantem no catalogo.
    assert cat["SPECIES_XERNEAS_NEUTRAL"].lenda
    assert cat["SPECIES_XERNEAS_NEUTRAL"].base, "forma padrao vira base"
    assert cat["SPECIES_ZYGARDE_50"].lenda
    assert cat["SPECIES_MAGEARNA"].lenda            # mítica
    assert cat["SPECIES_NIHILEGO"].lenda            # ultra beast
    assert cat["SPECIES_GREAT_TUSK"].lenda          # paradox
    assert not cat["SPECIES_TALONFLAME"].lenda

    # Mutação: se o parser de tipos quebrar, o casamento de bioma vira sorteio.
    quebrado = dict(cat)
    quebrado["SPECIES_GRENINJA"] = cat["SPECIES_GRENINJA"]._replace(tipos=())
    assert not quebrado["SPECIES_GRENINJA"].tipos
    assert cat["SPECIES_GRENINJA"].tipos, "carrega() nao pode devolver tipo vazio"

    novas = [e for e in cat.values() if e.gen >= 6 and e.base and not e.lenda]
    assert len(novas) > 250, len(novas)
    print(f"demo OK: {len(cat)} entradas, {len(novas)} bases gen 6-9 sem lenda")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        return demo()
    cat = carrega()
    print(f"{'gen':>4} {'entradas':>9} {'bases':>6} {'lendas':>7} {'formas':>7}")
    for g in range(1, 10):
        e = [x for x in cat.values() if x.gen == g]
        print(f"{g:>4} {len(e):>9} {sum(x.base for x in e):>6} "
              f"{sum(x.lenda and x.base for x in e):>7} "
              f"{sum(not x.base for x in e):>7}")
    novas = [x for x in cat.values() if x.gen >= 6 and x.base]
    print(f"\ngen 6-9 base: {len(novas)}, das quais "
          f"{sum(x.lenda for x in novas)} lendas/míticas/UB/paradox")


if __name__ == "__main__":
    sys.exit(main())
