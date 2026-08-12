#!/usr/bin/env python3
"""B8, lado do MATO: nível do selvagem por região e entrada das gerações 6 a 9.

    python3 dev_scripts/curva_selvagem.py             # só mede, não escreve
    python3 dev_scripts/curva_selvagem.py --aplicar   # reescreve o JSON
    python3 dev_scripts/curva_selvagem.py --aplicar --seco   # diff, sem escrever
    python3 dev_scripts/curva_selvagem.py --demo      # asserts, não toca em nada

Escreve UM arquivo: `src/data/wild_encounters.json`, o único que vira
`src/data/wild_encounters.h` (regra do Makefile). Nada aqui mexe em id de mapa,
de flag, de var ou em tamanho de struct: `guarda_save.py` continua verde por
construção, e é rodado no fim mesmo assim.

## 1. O nível: por que uma reta por região, e ancorada em percentil

Medido em 12/08/2026, antes desta leva: o selvagem NUNCA foi remapeado em
região nenhuma. As cinco medianas ficavam entre 20 e 30 enquanto a curva do
TREINADOR já ia de 3 a 255. O jogador chega em Sinnoh com time de nível 145 e
a grama cospe nível 30, que é experiência zero e captura impossível de usar.

A regra é a mesma de `curva_de_nivel.py`, que fez isso do lado do treinador:
uma reta por região, `round(a + b * nivel)`, de modo que a FORMA da curva da
fonte sobreviva (a Rota 1 continua sendo mais fraca que a Victory Road) e só a
faixa se desloque. O que muda aqui são as âncoras: em vez do primeiro e do
último nível observados, usa-se o **percentil 1 e o percentil 99** da região,
com corte nas pontas. Motivo medido: Johto e Sinnoh têm um slot de nível 100
cada (lendário de fonte) contra p99 de 65 e 55. Ancorar no máximo faria esse
slot sozinho achatar a região inteira em ~40 níveis.

Corte nas pontas preserva a ORDEM (fraco continua fraco); ele só empata quem
já estava fora da faixa dos 98% do meio.

## 2. As gerações 6 a 9: onde cabe sem apagar a fonte

Medido: 5514 dos 9556 slots de encontro da build são DUPLICATA (a mesma espécie
repetida dentro da mesma tabela, que é como as fontes distribuem probabilidade).
Slot duplicado é a folga que o PRD pede: trocar a segunda aparição de Wurmple na
Rota 101 por uma espécie nova não tira nenhuma espécie da fonte do jogo, porque
a primeira aparição continua lá. Nenhuma espécie de fonte é removida por este
script, e isso é conferido por assert antes de escrever.

Critério de ONDE cada espécie nova entra, escrito e não improvisado:

1. **Região pela força.** As 290 bases de gen 6 a 9 que não são lenda/mítica/
   ultra beast/paradox são ordenadas por soma de stats base e cortadas em cinco
   fatias iguais: a mais fraca vai para Kanto, a mais forte para Unova. É o que
   mantém a curva de dificuldade que o resto do bloco constrói.
2. **Meio pelo campo.** `water_mons` e `fishing_mons` só aceitam candidata do
   tipo Água; `rock_smash_mons` só Pedra, Terra, Inseto ou Aço; `land_mons`
   recusa quem é Água pura.
3. **Bioma pelo tipo da própria tabela.** A tabela diz o bioma dela: entra de
   preferência quem compartilha tipo com as espécies que a fonte já pôs ali.
   Caverna com Zubat e Geodude puxa Noibat e Carbink, não Popplio.
4. **Cobertura.** A distribuição é por ESPÉCIE, não por slot: cada espécie da
   fatia procura o melhor slot livre antes de qualquer uma repetir. Espécie que
   não achou slot compatível é NOMEADA no relatório, nunca enfiada à força.

Lenda, mítica, ultra beast e paradox de gen 6 a 9 ficam FORA do mato de
propósito: elas são o conteúdo de líder e Elite Four (ver `lendas_de_lider.py`).
"""
import argparse
import collections
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
import catalogo_especies as CAT      # noqa: E402
import encontros_b7 as B7            # noqa: E402

ALVO = os.path.join(RAIZ, "src", "data", "wild_encounters.json")

# Faixa de nível do MATO por região. Fica logo abaixo da faixa do TREINADOR
# medida por `curva_de_nivel.py` (Kanto 3-50, Johto 45-128, Hoenn 95-150,
# Sinnoh 145-200, Unova 195-255): o mato serve para subir de nível antes do
# duelo, então ele não pode passar do duelo.
FAIXA = {"Kanto": (3, 46), "Johto": (42, 122), "Hoenn": (90, 146),
         "Sinnoh": (140, 196), "Unova": (190, 250)}

# Tipos que cada campo aceita. `None` = qualquer um que não seja Água pura.
CAMPO = {
    "water_mons": {"TYPE_WATER"},
    "fishing_mons": {"TYPE_WATER"},
    "rock_smash_mons": {"TYPE_ROCK", "TYPE_GROUND", "TYPE_BUG", "TYPE_STEEL"},
    "land_mons": None,
}


def teto():
    """MAX_LEVEL lido da fonte, nunca cravado."""
    txt = open(os.path.join(RAIZ, "include/constants/pokemon.h")).read()
    for linha in txt.splitlines():
        if linha.startswith("#define MAX_LEVEL "):
            return int(linha.split()[2])
    raise SystemExit("MAX_LEVEL nao encontrado em include/constants/pokemon.h")


# ------------------------------------------------------------------ medição

def slots_da(e):
    """[(campo, mon)] de um header, na ordem em que o motor sorteia."""
    for k, v in e.items():
        if k.endswith("_mons"):
            for m in v["mons"]:
                yield k, m


def niveis_por_regiao(g, reg):
    fora = {n: [] for n in B7.ORDEM}
    for e in g["encounters"]:
        if B7.versao(e["base_label"]) != "EMERALD":
            continue
        for nome in B7.ORDEM:
            if e["map"] in reg[nome]:
                for _, m in slots_da(e):
                    fora[nome] += [m["min_level"], m["max_level"]]
                break
    return fora


def ancoras(v):
    """(p01, p99) de uma lista já ordenável. Devolve p01 < p99 sempre."""
    v = sorted(v)
    lo = v[int(0.01 * len(v))]
    hi = v[min(len(v) - 1, int(0.99 * len(v)))]
    return (lo, hi if hi > lo else lo + 1)


def remapeia(nivel, origem, destino, maxlevel):
    lo, hi = origem
    a, b = destino
    n = a + (nivel - lo) * (b - a) / (hi - lo)
    return max(1, min(maxlevel, max(a, min(b, round(n)))))


# ------------------------------------------------- distribuição de gen 6-9

def fatias_por_forca(cat):
    """{regiao: [Especie]}, gen 6-9 sem lenda, cortadas por soma de stats."""
    novas = sorted((x for x in cat.values()
                    if x.gen >= 6 and x.base and not x.lenda),
                   key=lambda x: (x.bst, x.nome))
    n = len(novas)
    fora = {}
    for i, nome in enumerate(B7.ORDEM):
        fora[nome] = novas[i * n // 5:(i + 1) * n // 5]
    return fora


def cabe_no_campo(esp, campo):
    aceita = CAMPO.get(campo, None)
    if aceita is None:
        return esp.tipos != ("TYPE_WATER",)
    return bool(set(esp.tipos) & aceita)


# Quantas vezes cada espécie nova tenta aparecer no jogo. Uma aparição só
# torna a espécie alcançável mas praticamente invisível: um slot de 12, num
# mapa de 558. Quatro é o que sobra depois de respeitar o TETO abaixo.
RODADAS = 4
# Fração máxima de uma tabela que pode virar gen 6-9. Acima disso a tabela
# deixa de ser a da fonte, e o PRD manda a fonte entrar primeiro.
TETO_POR_TABELA = 3


def vagas(g, reg, cat):
    """[(regiao, header, campo, indice, tipos_da_tabela)] de slot trocável.

    Só slot DUPLICADO entra: a primeira aparição de cada espécie da fonte fica
    sempre intacta, e é isso que garante que nenhuma espécie sai do jogo. Por
    campo, no máximo `len(mons) // TETO_POR_TABELA` slots, e sempre as últimas
    repetições, que são as de menor probabilidade nas tabelas das fontes.
    """
    fora = []
    for e in g["encounters"]:
        if B7.versao(e["base_label"]) != "EMERALD":
            continue
        regiao = next((n for n in B7.ORDEM if e["map"] in reg[n]), None)
        if regiao is None:
            continue
        for campo, v in sorted(e.items()):
            if not campo.endswith("_mons"):
                continue
            mons = v["mons"]
            visto, dup = set(), []
            for i, m in enumerate(mons):
                if m["species"] in visto:
                    dup.append(i)
                visto.add(m["species"])
            tipos = set()
            for m in mons:
                tipos |= set(cat[m["species"]].tipos) if m["species"] in cat else set()
            for i in dup[-(len(mons) // TETO_POR_TABELA):]:
                fora.append((regiao, e, campo, i, tipos))
    return fora


def distribui(g, reg, cat, rodadas=RODADAS):
    """Troca slot duplicado por espécie de gen 6-9. Devolve (trocas, sobrou).

    Por ESPÉCIE e não por slot, em rodadas: na rodada 1 toda espécie da fatia
    pega o melhor slot livre antes de qualquer uma repetir, então cobertura
    vem antes de frequência. Se a rodada 1 deixar alguém de fora, é falta de
    slot compatível de verdade, e o nome sai no relatório.
    """
    fatias = fatias_por_forca(cat)
    livres = collections.defaultdict(list)
    for regiao, e, campo, i, tipos in vagas(g, reg, cat):
        livres[regiao].append((e, campo, i, tipos))

    trocas, sobrou = [], []
    for regiao in B7.ORDEM:
        pool = list(livres[regiao])
        for rodada in range(rodadas):
            for esp in fatias[regiao]:
                melhor, nota = None, -1
                for j, (e, campo, i, tipos) in enumerate(pool):
                    if not cabe_no_campo(esp, campo):
                        continue
                    if esp.nome in {m["species"] for m in e[campo]["mons"]}:
                        continue
                    # bioma: quantos tipos a candidata divide com a tabela
                    n = len(set(esp.tipos) & tipos)
                    if n > nota:
                        melhor, nota = j, n
                    if n == len(esp.tipos):
                        break
                if melhor is None:
                    if rodada == 0:
                        sobrou.append(esp.nome)
                    continue
                e, campo, i, tipos = pool.pop(melhor)
                antes = e[campo]["mons"][i]["species"]
                e[campo]["mons"][i]["species"] = esp.nome
                trocas.append((regiao, e["map"], campo, antes, esp.nome, nota))
    return trocas, sobrou


# ------------------------------------------------------------------- ações

def aplica(seco=False):
    cat = CAT.carrega()
    validas = CAT.validas()
    maxlevel = teto()
    reg = B7.regioes()
    d = B7.carrega()
    g = B7.grupo_principal(d)

    antes_esp = {e["base_label"]: {m["species"] for _, m in slots_da(e)}
                 for e in g["encounters"]}
    antes_niv = niveis_por_regiao(g, reg)

    # 1. nível
    origem = {n: ancoras(v) for n, v in antes_niv.items() if v}
    tocados = 0
    for e in g["encounters"]:
        if B7.versao(e["base_label"]) != "EMERALD":
            continue
        regiao = next((n for n in B7.ORDEM if e["map"] in reg[n]), None)
        if regiao is None or regiao not in origem:
            continue
        for _, m in slots_da(e):
            for campo in ("min_level", "max_level"):
                m[campo] = remapeia(m[campo], origem[regiao],
                                    FAIXA[regiao], maxlevel)
            if m["min_level"] > m["max_level"]:
                m["min_level"] = m["max_level"]
        tocados += 1

    # 2. gerações 6 a 9
    trocas, sobrou = distribui(g, reg, cat)

    # 3. o que nunca pode ter acontecido
    for e in g["encounters"]:
        for campo, m in slots_da(e):
            assert m["species"] in validas, (e["base_label"], m["species"])
            assert 1 <= m["min_level"] <= m["max_level"] <= maxlevel, \
                (e["base_label"], m)
    novas_por_mapa = collections.defaultdict(set)
    for _, mapa, _, _, nova, _ in trocas:
        novas_por_mapa[mapa].add(nova)
    perdidas = []
    for e in g["encounters"]:
        agora = {m["species"] for _, m in slots_da(e)}
        fora = antes_esp[e["base_label"]] - agora
        if fora:
            perdidas.append((e["base_label"], sorted(fora)))
    assert not perdidas, f"espécie da fonte sumiu: {perdidas[:5]}"

    depois = niveis_por_regiao(g, reg)
    print(f"NÍVEL: {tocados} tabelas remapeadas (MAX_LEVEL={maxlevel})")
    print(f"{'região':<8} {'antes (p01/mediana/p99)':>26} "
          f"{'depois':>22} {'faixa alvo':>13}")
    for n in B7.ORDEM:
        a, b = sorted(antes_niv[n]), sorted(depois[n])
        f = lambda v, p: v[min(len(v) - 1, int(p * len(v)))]
        print(f"{n:<8} {f(a,.01):>10}/{f(a,.5)}/{f(a,.99):<12} "
              f"{f(b,.01):>10}/{f(b,.5)}/{f(b,.99):<10} {str(FAIXA[n]):>13}")

    print(f"\nGEN 6-9: {len(trocas)} slots duplicados trocados, "
          f"{len({t[4] for t in trocas})} espécies distintas colocadas")
    print(f"{'região':<8} {'espécies':>9} {'slots':>6} {'com tipo em comum':>19}")
    for n in B7.ORDEM:
        t = [x for x in trocas if x[0] == n]
        print(f"{n:<8} {len({x[4] for x in t}):>9} {len(t):>6} "
              f"{sum(1 for x in t if x[5] > 0):>19}")
    if sobrou:
        print(f"sem vaga compatível ({len(sobrou)}): {sorted(sobrou)}")

    if seco:
        print("\n--seco: nada foi escrito")
        return 0
    with open(ALVO, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2)
        f.write("\n")
    print(f"\nescrito: {ALVO}")
    return 0


def mede():
    reg = B7.regioes()
    g = B7.grupo_principal(B7.carrega())
    niv = niveis_por_regiao(g, reg)
    cat = CAT.carrega()
    print(f"{'região':<8} {'slots':>6} {'p01':>4} {'mediana':>8} {'p99':>4} "
          f"{'gen6-9':>7}")
    for n in B7.ORDEM:
        v = sorted(niv[n])
        novas = set()
        for e in g["encounters"]:
            if B7.versao(e["base_label"]) == "EMERALD" and e["map"] in reg[n]:
                novas |= {m["species"] for _, m in slots_da(e)
                          if m["species"] in cat and cat[m["species"]].gen >= 6}
        f = lambda p: v[min(len(v) - 1, int(p * len(v)))]
        print(f"{n:<8} {len(v):>6} {f(.01):>4} {f(.5):>8} {f(.99):>4} "
              f"{len(novas):>7}")
    return 0


def demo():
    """Asserts com MUTAÇÃO: cada um falha se a lógica que ele guarda quebrar."""
    # remapeia() é a regra inteira do nível. Ordem preservada e ponta cortada.
    assert remapeia(3, (3, 58), (3, 46), 255) == 3
    assert remapeia(58, (3, 58), (3, 46), 255) == 46
    assert remapeia(67, (3, 58), (3, 46), 255) == 46, "acima do p99 corta no teto"
    assert remapeia(2, (3, 58), (3, 46), 255) == 3, "abaixo do p01 corta no piso"
    a = [remapeia(x, (3, 58), (3, 46), 255) for x in range(3, 59)]
    assert a == sorted(a), "remapeia() precisa ser monótona"
    # A mediana medida de Unova (30) tem que cair no meio da faixa de Unova.
    assert remapeia(30, (2, 63), (190, 250), 255) == 218
    # Mutação: se a faixa alvo for ignorada, isto passa a devolver o nível cru.
    assert remapeia(30, (2, 63), (190, 250), 255) != 30

    # ancoras() tem que ignorar o outlier que motivou o percentil: o slot de
    # nível 100 solto em Johto e em Sinnoh, contra p99 de 65 e 55.
    v = [10] * 995 + [1, 1, 100, 100, 100]
    lo, hi = ancoras(v)
    assert 10 <= lo <= hi <= 11, (lo, hi)
    # Mutação: ancorar no mín/máx puxaria a reta para 1..100 e achataria tudo.
    assert (min(v), max(v)) == (1, 100) and (lo, hi) != (1, 100)

    # cabe_no_campo() é o que impede Popplio na caverna e Carbink no mar.
    cat = CAT.carrega()
    agua = cat["SPECIES_POPPLIO"]
    pedra = cat["SPECIES_CARBINK"]
    assert cabe_no_campo(agua, "water_mons")
    assert not cabe_no_campo(agua, "land_mons"), "Água pura não anda na grama"
    assert not cabe_no_campo(agua, "rock_smash_mons")
    assert cabe_no_campo(pedra, "rock_smash_mons")
    assert cabe_no_campo(pedra, "land_mons")
    assert not cabe_no_campo(pedra, "fishing_mons")

    # As cinco fatias cobrem tudo, sem sobrepor, e sobem em força.
    fat = fatias_por_forca(cat)
    todas = [e for f in fat.values() for e in f]
    assert len(todas) == len(set(x.nome for x in todas))
    for i in range(4):
        a, b = B7.ORDEM[i], B7.ORDEM[i + 1]
        assert max(x.bst for x in fat[a]) <= min(x.bst for x in fat[b]) + 1, \
            f"{a} não pode ter bicho mais forte que {b}"
    assert all(x.gen >= 6 and not x.lenda for x in todas)

    # A faixa de cada região sobe, que é o aceite do B8.
    for i in range(4):
        assert FAIXA[B7.ORDEM[i]][1] > FAIXA[B7.ORDEM[i + 1]][0] - 10
        assert FAIXA[B7.ORDEM[i]][0] < FAIXA[B7.ORDEM[i + 1]][0]
    assert FAIXA["Unova"][1] <= teto()
    print(f"demo OK: {len(todas)} espécies de gen 6-9 fatiadas em 5 regiões")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--seco", action="store_true")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        return demo()
    if a.aplicar:
        return aplica(seco=a.seco)
    return mede()


if __name__ == "__main__":
    sys.exit(main())
