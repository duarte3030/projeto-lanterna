#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prova da curva de nível da campanha de Galar e Unova (cartucho 2).

    python3 dev_scripts/prova_curva_c2.py              # portão: falha em achado novo
    python3 dev_scripts/prova_curva_c2.py --lista      # tabela por mapa (treinador e selvagem)
    python3 dev_scripts/prova_curva_c2.py --grava-base # regrava a linha de base
    python3 dev_scripts/prova_curva_c2.py --demo       # par negativo (mutação em memória)

Lê `src/data/trainers.party`, os mapas e `src/data/wild_encounters.json`. Não
escreve nada fora de `--grava-base`.

Treinador de CAMPANHA: constante `TRAINER_UNOVA_*` ou `TRAINER_GALAR_*` que um
mapa de Unova ou Galar chama, que não é `_REVANCHE` e que não está marcada como
pós-jogo em `casamento_treinadores_<região>.json` (torre de Turffield, DLC,
youtubers de Wyndon, PWT).

Reprova (achado):
  A1  treinador de campanha com Pokémon acima do nível 100;
  A2  treinador de campanha cujo maior nível destoa mais de N (padrão 10) da
      referência do lugar. Referência: mediana do maior nível dos treinadores
      CASADOS (time do jogo original) no mesmo mapa ou em mapa vizinho (até
      distância 2 no grafo de borda e warp), sem contar o próprio treinador.
      Sem casado até a distância 2, a referência é o mato original (Black 2 ou
      Shield) do mesmo mapa ou vizinho direto, mais 2. Sem nenhuma das duas, o
      treinador entra na lista "sem referência" e não reprova.

Linha de base (`dev_scripts/prova_curva_c2_base.json`): achado já conhecido e
aceito não reprova; achado novo reprova; achado da base que sumiu é avisado.
"""
import argparse
import collections
import json
import os
import re
import statistics
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import times_originais_c2 as T  # noqa: E402
import curva_c2 as C  # noqa: E402

BASE = os.path.join(AQUI, "prova_curva_c2_base.json")
N_PADRAO = 10
DIST_CASADOS = 2
DIST_MATO = 1


def campanha(atual, refs):
    """{constante: [mapas]} dos treinadores de campanha, e o conjunto dos casados."""
    pos, casados = set(), set()
    for g in ("galar", "unova"):
        d = json.load(open(T.CASAMENTO % g, encoding="utf-8"))
        casados |= {r["constante"] for r in d["casados"]}
        for r in d["nao_casados"]:
            if r.get("curva", "").startswith("fica") or (g == "galar" and "pós-jogo" in r["motivo"]) \
                    or (g == "unova" and r["mapas"] and all(C.POS_JOGO_UNOVA.match(m) for m in r["mapas"])):
                pos.add(r["constante"])
    camp = {c: m for c, m in refs.items()
            if c in atual and not c.endswith(T.SUFIXO_REVANCHE) and c not in pos}
    return camp, casados


def mato_atual():
    """{id do mapa: maior nível de qualquer subtabela} como está no JSON hoje."""
    fora = {}
    for e in json.load(open(T.WILD, encoding="utf-8"))["wild_encounter_groups"][0]["encounters"]:
        lv = [m["max_level"] for k in ("land_mons", "water_mons", "fishing_mons", "rock_smash_mons")
              if k in e for m in e[k]["mons"]]
        if lv:
            fora[e["map"]] = max(fora.get(e["map"], 0), max(lv))
    return fora


def anel(mapa, viz, ate):
    """[(distância, [mapas])] de 0 até `ate`."""
    vistos, frente, fora = {mapa}, [mapa], []
    for d in range(ate + 1):
        fora.append((d, frente))
        nova = []
        for m in frente:
            for v in sorted(viz.get(m, ())):
                if v not in vistos:
                    vistos.add(v)
                    nova.append(v)
        frente = nova
    return fora


def mede(atual, n=N_PADRAO):
    refs = T.referencias()
    p2i, i2p, viz = C.grafo()
    camp, casados = campanha(atual, refs)
    mato_orig = C.mato_original()
    mato = mato_atual()
    # maior nível de cada casado, por mapa
    cas_mapa = collections.defaultdict(list)
    for c in casados:
        if c in camp:
            lv = max(T.niveis_do_bloco(atual[c]))
            for mp in camp[c]:
                if mp in p2i:
                    cas_mapa[p2i[mp]].append((c, lv))
    achados, sem_ref, linhas = [], [], []
    por_mapa = collections.defaultdict(list)
    for c, mapas in sorted(camp.items()):
        lv = T.niveis_do_bloco(atual[c])
        if not lv:
            continue
        topo = max(lv)
        for mp in mapas:
            por_mapa[mp].append((c, topo))
        mp = next((m for m in mapas if m in p2i), None)
        if topo > 100:
            achados.append(dict(codigo="A1", constante=c, mapa=mp, nivel=topo,
                                texto="nível %d acima de 100" % topo))
        if mp is None:
            continue
        ref = fonte = None
        for d, frente in anel(p2i[mp], viz, DIST_CASADOS):
            amostra = [x for m in frente for (k, x) in cas_mapa.get(m, []) if k != c]
            if amostra:
                ref, fonte = statistics.median(amostra), "casados a %d" % d
                break
        if ref is None:
            for d, frente in anel(p2i[mp], viz, DIST_MATO):
                sel = [mato_orig[m] for m in frente if m in mato_orig]
                if sel:
                    ref, fonte = statistics.median(sel) + C.FOLGA_SELVAGEM, "mato original a %d" % d
                    break
        if ref is None:
            sem_ref.append(c)
            continue
        if abs(topo - ref) > n:
            achados.append(dict(codigo="A2", constante=c, mapa=mp, nivel=topo, referencia=ref,
                                texto="nível %d contra %g (%s)" % (topo, ref, fonte)))
    for mp in sorted(por_mapa):
        mid = p2i.get(mp)
        t = max(x for _, x in por_mapa[mp])
        linhas.append((mp, t, mato.get(mid), mato_orig.get(mid)))
    return achados, sem_ref, linhas, mato, p2i


def chave(a):
    return "%s %s" % (a["codigo"], a["constante"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lista", action="store_true")
    ap.add_argument("--grava-base", action="store_true")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("-n", type=int, default=N_PADRAO)
    a = ap.parse_args()
    _, atual = T.le_party(T.PARTY)
    if a.demo:
        ok = True
        achados, _, _, _, _ = mede(atual, a.n)
        base = {chave(x) for x in achados}
        # mutação 1: um reescalado volta ao nível do hack
        r0 = json.load(open(C.SAIDA_JSON, encoding="utf-8"))["reescalados"][0]
        sujo = dict(atual)
        sujo[r0["constante"]] = atual[r0["revanche"]].replace(r0["revanche"], r0["constante"], 1)
        novos = {chave(x) for x in mede(sujo, a.n)[0]} - base
        caso1 = {"A1 " + r0["constante"], "A2 " + r0["constante"]} <= novos
        print("  mutação: %s de volta ao time do hack reprova A1 e A2: %s" % (r0["constante"], "ok" if caso1 else "REPROVOU"))
        # mutação 2: um casado de rota cai 15 níveis (fica no teto, destoa dos vizinhos)
        alvo = "TRAINER_UNOVA_BIKER_R9_1"
        sujo = dict(atual)
        sujo[alvo] = re.sub(r"(?m)^Level: (\d+)", lambda m: "Level: %d" % (int(m.group(1)) - 15), atual[alvo])
        novos = {chave(x) for x in mede(sujo, a.n)[0]} - base
        caso2 = ("A2 " + alvo) in novos
        print("  mutação: %s 15 níveis abaixo reprova A2: %s" % (alvo, "ok" if caso2 else "REPROVOU"))
        ok = caso1 and caso2
        print("DEMO", "VERDE" if ok else "VERMELHO")
        sys.exit(0 if ok else 1)
    achados, sem_ref, linhas, mato, p2i = mede(atual, a.n)
    if a.lista:
        print("%-40s %8s %8s %8s" % ("mapa", "treinador", "selvagem", "orig"))
        for mp, t, w, wo in linhas:
            print("%-40s %8d %8s %8s" % (mp, t, w if w is not None else "-", wo if wo is not None else "-"))
        print()
    if a.grava_base:
        json.dump(dict(sobre="Linha de base de dev_scripts/prova_curva_c2.py: achados conhecidos e aceitos. "
                             "Achado fora daqui reprova o portão.", n=a.n,
                       achados=sorted([dict(chave=chave(x), texto=x["texto"], mapa=x["mapa"]) for x in achados],
                                      key=lambda x: x["chave"])),
                  open(BASE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("linha de base gravada: %d achados" % len(achados))
        return
    base = {x["chave"] for x in json.load(open(BASE, encoding="utf-8"))["achados"]} if os.path.exists(BASE) else set()
    novos = [x for x in achados if chave(x) not in base]
    sumidos = base - {chave(x) for x in achados}
    acima = max((t for _, t, _, _ in linhas), default=0)
    salto = max((abs(x["nivel"] - x["referencia"]) for x in achados if x["codigo"] == "A2"), default=0)
    print("curva da campanha: %d mapas com treinador; maior nível de treinador de campanha %d; "
          "achados %d (%d na base, %d novos); maior salto A2 %g; sem referência %d"
          % (len(linhas), acima, len(achados), len(achados) - len(novos), len(novos), salto, len(sem_ref)))
    for x in novos:
        print("  NOVO %s %s em %s: %s" % (x["codigo"], x["constante"], x["mapa"], x["texto"]))
    for k in sorted(sumidos):
        print("  aviso: achado da base sumiu (melhorou): %s" % k)
    sys.exit(1 if novos else 0)


if __name__ == "__main__":
    main()
