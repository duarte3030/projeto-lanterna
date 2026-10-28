#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Curva de nível da campanha de Galar e Unova no cartucho 2 (continuação da
decisão 130 do Gui, 28/10/2026).

    python3 dev_scripts/curva_c2.py --aplicar   # casamento manual + reescala; escreve party, ids, Fase F
    python3 dev_scripts/curva_c2.py --demo      # invariantes no que está escrito (com par negativo)

A frente `c2-times` (`times_originais_c2.py`) trocou para o time ORIGINAL
(Shield e Black 2) os treinadores que casaram. Os que não casaram ficaram com o
time do hack em nível 200 a 255, ao lado de líderes em nível 16 a 25. Este
script fecha isso em duas etapas.

1. CASAMENTO MANUAL dos personagens nomeados de Unova que o automático perdeu
   (tabela `MANUAL_UNOVA`). Quando o personagem do BW3G não tem par no Black 2
   no mesmo papel, entra o treinador do Black 2 que ocupa o MESMO papel na
   história (cadeira da Elite Four, campeão, ginásio), e o motivo fica escrito
   no par. O tratamento é o mesmo do `times_originais_c2.py`: a constante de
   hoje passa a ter o time do Black 2, o time do hack vai para
   `<constante>_REVANCHE` e o chefe da Fase F passa a ser a revanche. O
   cabeçalho (nome, classe, retrato, IA) continua o do BW3G.
   Galar: os nomeados que não casaram são TODOS de pós-jogo do demake (torre de
   Turffield, DLC, Ballonlea e Spikemuth com time de nível 70 a 100 na fonte do
   Ultimate Plus). Ficam como estão.

2. REESCALA dos não casados que sobram (menos pós-jogo: Galar pelo motivo
   gravado em `casamento_treinadores_galar.json`; Unova, a Bianca do PWT).
   O time continua o mesmo (espécie, item, habilidade, natureza, IV e EV); muda
   o NÍVEL e os golpes. O time do hack, byte a byte, vai para a revanche.

   Regra da curva do lugar (`alvo`):
   - Busca em largura pelo grafo de mapas (conexão de borda e warp, nos dois
     sentidos), a partir do mapa do treinador, distância 0 a 3.
   - Na MENOR distância em que houver evidência: se houver treinador casado
     (time do jogo original) nos mapas daquela distância, o alvo é a MEDIANA do
     maior nível de cada time casado; se não houver, é a mediana do maior nível
     do mato ORIGINAL (tabelas que vieram do Black 2 ou do Shield, em
     `casamento_encontros_c2.json`) mais 2.
   - Sem evidência até a distância 3 (só acontece em Galar: Wild Area e Rixy
     Chamber, que não têm casado perto nem mato do Shield): o nível que o
     próprio treinador tinha no Ultimate Plus ANTES do 255
     (`up_treinadores.json`, o mesmo dado que casou Galar). Medido: onde a busca
     acha casado até a distância 2, ela e esse nível concordam a poucos níveis.
   - Cada nível do time vira `round(nivel * alvo / maior_nivel_do_time)`, com
     piso 2: o maior Pokémon do time fica exatamente no alvo e a forma interna
     do time (quem era o mais fraco continua o mais fraco) se preserva.
   - Golpes: as linhas `- MOVE_*` saem. Sem golpe escrito, o motor monta o
     moveset pelo learnset no nível novo (`GiveMonInitialMoveset`, o mesmo
     caminho que o modo LV.5 TRAINERS e o T116 usam). É o "regerar pelo
     learnset": golpe de nível 223 não sobra num Pokémon de nível 20.

   O resultado, treinador por treinador (mapa, alvo, de onde veio, distância,
   níveis antes e depois, revanche), fica em `dev_scripts/curva_c2.json`.

Ids novos de revanche: acima do maior que existe (3379), append-only, num
bloco próprio de `opponents.h` e do `.party`. Clone com o mesmo time do hack não
ganha segunda revanche. Rodar `--aplicar` duas vezes é recusado (o bloco já
existe): o script lê o estado depois da frente `c2-times`.
"""
import argparse
import collections
import glob
import json
import os
import re
import statistics
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import times_originais_c2 as T  # noqa: E402

RAIZ = T.RAIZ
SAIDA_JSON = os.path.join(RAIZ, "dev_scripts/curva_c2.json")
MARCA_INI = "// >>> Revanches da curva: times do hack guardados (dev_scripts/curva_c2.py) >>>"
MARCA_FIM = "// <<< Revanches da curva <<<"
P_INI = "/* >>> Revanches da curva: times do hack guardados (dev_scripts/curva_c2.py) >>> */"
P_FIM = "/* <<< Revanches da curva <<< */"
PROFUNDIDADE = 3
FOLGA_SELVAGEM = 2
PISO_NIVEL = 2

# Casamento manual de Unova. Chave: constante do BW3G. Valor: (id do Black 2,
# confiança, motivo). "papel" = o Black 2 não tem o personagem naquele papel, e
# o par é quem ocupa o papel no Black 2.
_IRIS = (341, "papel", "campeão da Liga; o campeão do Black 2 é a Iris (primeira visita, 57 a 59). "
         "O BW3G tem campeão próprio, sem par no Black 2")
MANUAL_UNOVA = {
    "TRAINER_UNOVA_E4_GRIMSLEY": (40, "alta", "Elite Four, mesmo personagem: Grimsley do Black 2, primeira visita (56 a 58)"),
    "TRAINER_UNOVA_E4_MARSHAL": (39, "alta", "Elite Four, mesmo personagem: Marshal do Black 2, primeira visita (56 a 58)"),
    "TRAINER_UNOVA_E4_ELESA": (38, "papel", "cadeira da Elite Four; no Black 2 a cadeira é da Shauntal (a Elesa do Black 2 é líder "
                               "de ginásio, nível 28 a 30). Primeira visita, 56 a 58"),
    "TRAINER_UNOVA_E4_COLRESS": (41, "papel", "cadeira da Elite Four; no Black 2 a cadeira é da Caitlin (o Colress do Black 2 é "
                                 "chefe da Plasma, não da Liga). Primeira visita, 56 a 58"),
    "TRAINER_UNOVA_CHAMPION_GENESIS": _IRIS,
    "TRAINER_UNOVA_CHAMPION_JUNIPER_OSHAWOTT": _IRIS,
    "TRAINER_UNOVA_CHAMPION_JUNIPER_SNIVY": _IRIS,
    "TRAINER_UNOVA_CHAMPION_JUNIPER_TEPIG": _IRIS,
    "TRAINER_UNOVA_LEADER_CILAN": (496, "media", "mesmo personagem e mesmo lugar: o Cilan do Black 2 luta em Striaton "
                                   "(65 a 67, pós-jogo do Black 2, que é a curva do lugar)"),
    "TRAINER_UNOVA_LEADER_SHAUNTAL": (158, "papel", "líder de ginásio sem ginásio no Black 2 (Lentimas não tem); o par é o líder "
                                      "do Black 2 que o BW3G não usa e cujo nível fica mais perto da curva de Lentimas: "
                                      "Clay (31 a 33). A Shauntal do Black 2 é Elite Four"),
    "TRAINER_UNOVA_HUGH_TEPIG": (368, "papel", "rival com a linha do Tepig, em Driftveil; o par é a luta do Hugh do Black 2 com "
                                 "Pignite logo depois de Driftveil (31 a 33). A luta do Hugh em Driftveil no Black 2 é de pós-jogo"),
    "TRAINER_UNOVA_NATE_OSHAWOTT": (360, "media", "mesmo personagem; o Nate do Black 2 com a linha do Oshawott (Dewott, 23 a 25)"),
    "TRAINER_UNOVA_NATE_SNIVY": (361, "media", "mesmo personagem; o Nate do Black 2 com a linha do Snivy (Servine, 23 a 25)"),
    "TRAINER_UNOVA_NATE_TEPIG": (362, "media", "mesmo personagem; o Nate do Black 2 com a linha do Tepig (Pignite, 23 a 25)"),
    "TRAINER_UNOVA_ROSA_OSHAWOTT": (363, "media", "mesmo personagem; a Rosa do Black 2 com a linha do Oshawott (Dewott, 23 a 25)"),
    "TRAINER_UNOVA_ROSA_SNIVY": (364, "media", "mesmo personagem; a Rosa do Black 2 com a linha do Snivy (Servine, 23 a 25)"),
    "TRAINER_UNOVA_ROSA_TEPIG": (365, "media", "mesmo personagem; a Rosa do Black 2 com a linha do Tepig (Pignite, 23 a 25)"),
}
# Pós-jogo de Unova no BW3G: o PWT.
POS_JOGO_UNOVA = re.compile(r"^Unova_PWT")


# ------------------------------------------------------------------ grafo e evidência
def grafo():
    """(pasta->id, id->pasta, vizinhos por id) dos mapas de Galar e Unova."""
    p2i, i2p, viz = {}, {}, collections.defaultdict(set)
    jsons = {}
    for f in glob.glob(os.path.join(RAIZ, "data/maps/*/map.json")):
        p = f.split(os.sep)[-2]
        if p.startswith(("Unova_", "Galar_")):
            d = json.load(open(f, encoding="utf-8"))
            jsons[p] = d
            p2i[p], i2p[d["id"]] = d["id"], p
    for p, d in jsons.items():
        a = d["id"]
        for c in d.get("connections") or []:
            if c.get("map") in i2p:
                viz[a].add(c["map"])
                viz[c["map"]].add(a)
        for w in d.get("warp_events") or []:
            b = w.get("dest_map")
            if b in i2p and b != a:
                viz[a].add(b)
                viz[b].add(a)
    return p2i, i2p, viz


def mato_original():
    """{id do mapa: maior nível do mato} só das subtabelas que vieram do jogo
    original. Unova: a subtabela que o Black 2 tem naquele mapa (grama; sem
    grama, água), lida do próprio `bw2_wild_encounters.json`, porque a subtabela
    que o Black 2 não tem ficou com o nível do hack (a Rota 17 só tem água no
    Black 2, e a grama de lá continua em 219). Galar: a grama trocada pela zona
    do Shield."""
    enc = json.load(open(T.ENCONTROS, encoding="utf-8"))
    fora = {}
    unova = set(enc["unova"]["trocados"]) | set(enc["unova"]["novos"])
    bw2 = json.load(open(os.path.join(T.SAIDA, "bw2_wild_encounters.json"), encoding="utf-8"))
    for e in bw2["wild_encounter_groups"][0]["encounters"]:
        if e["map"] in unova:
            for k in ("land_mons", "water_mons"):
                if k in e:
                    fora[e["map"]] = max(m["max_level"] for m in e[k]["mons"])
                    break
    galar = {x["mapa"] for x in enc["galar"]["trocados"]}
    for e in json.load(open(T.WILD, encoding="utf-8"))["wild_encounter_groups"][0]["encounters"]:
        if e["map"] in galar and "land_mons" in e:
            fora[e["map"]] = max(m["max_level"] for m in e["land_mons"]["mons"])
    assert all(v <= 100 for v in fora.values()), "nível de mato do jogo original acima de 100"
    return fora


def casados_por_mapa(atual, p2i):
    """{id do mapa: [maior nível de cada time casado que o mapa chama]}."""
    fora = collections.defaultdict(list)
    for regiao in ("galar", "unova"):
        for r in json.load(open(T.CASAMENTO % regiao, encoding="utf-8"))["casados"]:
            lv = max(T.niveis_do_bloco(atual[r["constante"]]))
            for mp in r["mapas"]:
                if mp in p2i:
                    fora[p2i[mp]].append(lv)
    return fora


def alvo_do_mapa(mapa_id, viz, casados, mato, profundidade=PROFUNDIDADE, excluir=None):
    """(alvo, fonte, distância, mapas usados) pela regra do cabeçalho.
    `excluir` tira uma lista de níveis casados de um mapa (para medir a curva de
    um lugar sem o próprio treinador)."""
    vistos, frente = {mapa_id}, [mapa_id]
    for dist in range(profundidade + 1):
        cas = []
        usados = []
        for m in frente:
            lv = list(casados.get(m, []))
            if excluir and m == excluir[0]:
                for x in excluir[1]:
                    if x in lv:
                        lv.remove(x)
            if lv:
                cas += lv
                usados.append(m)
        if cas:
            return round(statistics.median(cas)), "casados", dist, usados
        sel = [mato[m] for m in frente if m in mato]
        if sel:
            return round(statistics.median(sel)) + FOLGA_SELVAGEM, "selvagem", dist, [m for m in frente if m in mato]
        nova = []
        for m in frente:
            for v in sorted(viz.get(m, ())):
                if v not in vistos:
                    vistos.add(v)
                    nova.append(v)
        frente = nova
        if not frente:
            break
    return None, None, None, []


# ------------------------------------------------------------------ edição de bloco
def reescala_bloco(bloco, alvo):
    """Bloco com cada `Level:` escalado para o maior ficar em `alvo` e sem `- MOVE_*`."""
    lv = T.niveis_do_bloco(bloco)
    topo = max(lv)

    def novo(m):
        return "Level: %d" % max(PISO_NIVEL, round(int(m.group(1)) * alvo / topo))
    b = re.sub(r"(?m)^Level: (\d+)", novo, bloco)
    b = re.sub(r"(?m)^- MOVE_\S*[ \t]*\n", "", b)
    return b


def time_do_bloco(bloco):
    """(cabeçalho, time, rabo). O time termina na primeira linha que abre
    comentário (`/*`): o `.party` guarda comentários de várias linhas entre
    blocos, e o `fatia` de `times_originais_c2.py` só reconhece a primeira e a
    última linha deles. O rabo leva o comentário inteiro."""
    corpo = bloco[bloco.index("\n") + 1:]
    cab, time, rabo = T.fatia(corpo)
    linhas = time + rabo
    k = next((i for i, ln in enumerate(linhas) if ln.lstrip().startswith("/*")), len(linhas))
    return cab, "\n".join(linhas[:k]).strip(), [ln for ln in linhas[k:]]


# ------------------------------------------------------------------ aplicar
def pos_jogo(r, regiao):
    if regiao == "galar":
        return "pós-jogo" in r["motivo"]
    return bool(r["mapas"]) and all(POS_JOGO_UNOVA.match(m) for m in r["mapas"])


def aplicar():
    texto, atual = T.le_party(T.PARTY)
    opp = open(T.OPPS, encoding="utf-8").read()
    if MARCA_INI in opp or P_INI in texto:
        sys.exit("o bloco de revanches da curva já existe: --aplicar já rodou nesta árvore")
    b2 = T.fonte_party("bw2_todos.party", "BW2")
    b2json = {x["id"]: x for x in json.load(open(os.path.join(T.SAIDA, "bw2_treinadores.json"), encoding="utf-8"))}
    doc_f = json.load(open(T.FASE_F, encoding="utf-8"))
    na_fase_f = {c["id"] for c in doc_f["chefes"]}
    cas = {g: json.load(open(T.CASAMENTO % g, encoding="utf-8")) for g in ("galar", "unova")}

    novos = {}          # constante -> bloco novo de campanha
    revanches = []      # (constante, bloco)
    vistos = {}         # time do hack -> constante de revanche (dedupe)

    def guarda_revanche(const, regiao):
        cab, time, _ = time_do_bloco(atual[const])
        if time not in vistos:
            nome = const + T.SUFIXO_REVANCHE
            assert nome not in atual, nome
            vistos[time] = nome
            revanches.append((nome, "=== %s ===\n" % nome + "\n".join(cab) + "\n\n" + time + "\n\n", const))
        return vistos[time]

    # 1. casamento manual de Unova (Fase F primeiro: o dono da revanche é o chefe)
    manuais = []
    nao = {r["constante"]: r for r in cas["unova"]["nao_casados"]}
    for const in sorted(MANUAL_UNOVA, key=lambda c: (c not in na_fase_f, c)):
        fid, conf, motivo = MANUAL_UNOVA[const]
        assert const in nao, "%s não está nos não casados" % const
        reg = nao.pop(const)
        rv = guarda_revanche(const, "unova")
        cab, _, rabo = time_do_bloco(atual[const])
        fc, fb = b2[fid]
        _, ftime, _ = T.fatia(fb[fb.index("\n") + 1:])
        novos[const] = ("=== %s ===\n" % const + "\n".join(cab) + "\n\n" + "\n".join(ftime).strip() + "\n\n"
                        + ("\n".join(rabo).strip() + "\n\n" if "".join(rabo).strip() else ""))
        manuais.append(dict(constante=const, nome=reg["nome"], classe=reg["classe"], mapas=reg["mapas"],
                            fonte=dict(jogo="Black 2", id=fid, constante=fc,
                                       lugares=[l["lugar"] for l in b2json[fid]["lugares"]]),
                            confianca=conf, motivo=motivo, manual=True, revanche=rv))
    cas["unova"]["casados"] = sorted(cas["unova"]["casados"] + manuais, key=lambda r: r["constante"])
    cas["unova"]["nao_casados"] = sorted(nao.values(), key=lambda r: r["constante"])

    # a curva lê os casados já com os manuais no lugar
    atual_dep = dict(atual)
    atual_dep.update(novos)
    p2i, i2p, viz = grafo()
    mato = mato_original()
    casados = collections.defaultdict(list)
    for regiao in ("galar", "unova"):
        for r in cas[regiao]["casados"]:
            lv = max(T.niveis_do_bloco(atual_dep[r["constante"]]))
            for mp in r["mapas"]:
                if mp in p2i:
                    casados[p2i[mp]].append(lv)

    # 2. reescala
    up = T.up_fonte()
    relatorio = []
    for regiao in ("galar", "unova"):
        for r in cas[regiao]["nao_casados"]:
            const = r["constante"]
            if pos_jogo(r, regiao):
                r["curva"] = "fica: pós-jogo"
                continue
            mapas = [p2i[m] for m in r["mapas"] if m in p2i]
            assert mapas, const
            # o alvo é o do primeiro mapa (cada treinador do BW3G e do demake tem um só; clones têm o deles)
            alvo, fonte, dist, usados = alvo_do_mapa(mapas[0], viz, casados, mato)
            if alvo is None and regiao == "galar":
                m = re.search(r"_(\d+)$", T.base_de(const))
                u = up.get(int(m.group(1))) if m else None
                if u and u[2]:
                    alvo, fonte, dist, usados = max(lv for _, lv in u[2]), "ultimate_plus", None, []
            assert alvo is not None, "%s sem curva em %d passos" % (const, PROFUNDIDADE)
            antes = T.niveis_do_bloco(atual[const])
            rv = guarda_revanche(const, regiao)
            novos[const] = reescala_bloco(atual[const], alvo)
            depois = T.niveis_do_bloco(novos[const])
            r["curva"] = "reescalado"
            r["revanche"] = rv
            relatorio.append(dict(constante=const, regiao=regiao, mapa=i2p[mapas[0]], alvo=alvo, fonte=fonte,
                                  distancia=dist, mapas_da_curva=[i2p[m] for m in usados],
                                  antes=antes, depois=depois, revanche=rv))

    # 3. escreve o .party: campanha no lugar, revanches num bloco próprio no fim
    out, pos = [], 0
    for c, a, b in T.blocos(texto):
        if c in novos:
            out.append(texto[pos:a])
            bl = novos[c]
            # o bloco de hoje termina com a linha em branco que separa do próximo
            out.append(bl if bl.endswith("\n\n") else bl.rstrip("\n") + "\n\n")
            pos = b
    out.append(texto[pos:])
    texto = "".join(out)
    texto = texto.rstrip("\n") + "\n\n" + P_INI + "\n" + "".join(b for _, b, _ in revanches) + P_FIM + "\n"

    # 4. ids novos acima do maior que existe
    usados = {int(v) for v in re.findall(r"(?m)^#define TRAINER_\w+\s+(\d+)", opp)}
    nid = max(i for i in usados if i < 4000) + 1
    assert nid >= 3380, nid
    linhas = []
    for nome, _, dono in revanches:
        while nid in usados:
            nid += 1
        assert nid <= T.TETO_ID, "acabou a faixa de ids de treinador"
        linhas.append("#define %-48s %d  // time do hack de %s" % (nome, nid, dono))
        nid += 1
    bloco_ids = (MARCA_INI + "\n// Curva da campanha: o não casado foi reescalado para o nível do lugar e o\n"
                 "// casado à mão leva o time do Black 2; o time do hack fica aqui, sem mapa.\n"
                 + "\n".join(linhas) + "\n" + MARCA_FIM + "\n")
    alvo_txt = "#define MAX_TRAINERS_COUNT_EMERALD"
    i = opp.rfind("\n", 0, opp.index(alvo_txt)) + 1
    opp = opp[:i] + bloco_ids + "\n" + opp[i:]

    # 5. Fase F: chefe que deixou de ter o time do hack na campanha vira a revanche
    dono = {r["constante"]: r["revanche"] for r in manuais}
    dono.update({r["constante"]: r["revanche"] for r in relatorio})
    movidos = 0
    for c in doc_f["chefes"]:
        if c["id"] in dono:
            c["id"] = dono[c["id"]]
            movidos += 1

    open(T.PARTY, "w", encoding="utf-8").write(texto)
    open(T.OPPS, "w", encoding="utf-8").write(opp)
    open(T.FASE_F, "w", encoding="utf-8").write(json.dumps(doc_f, ensure_ascii=False, indent=1))
    for g in ("galar", "unova"):
        c = cas[g]
        c["contagem"] = dict(casados=len(c["casados"]), alta=sum(x["confianca"] == "alta" for x in c["casados"]),
                             media=sum(x["confianca"] == "media" for x in c["casados"]),
                             papel=sum(x["confianca"] == "papel" for x in c["casados"]),
                             nao_casados=len(c["nao_casados"]),
                             reescalados=sum(x.get("curva") == "reescalado" for x in c["nao_casados"]),
                             pos_jogo=sum(x.get("curva") == "fica: pós-jogo" for x in c["nao_casados"]))
        json.dump(c, open(T.CASAMENTO % g, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    doc = collections.OrderedDict(
        sobre="Curva de nível da campanha do cartucho 2 (dev_scripts/curva_c2.py). Um registro por treinador "
              "não casado reescalado: mapa, alvo, de onde o alvo veio (casados ou selvagem original), distância "
              "no grafo de mapas, níveis antes e depois, e a revanche que guarda o time do hack.",
        regra="alvo = na menor distância (0 a %d) do grafo de mapas com evidência: mediana do maior nível dos times "
              "casados; sem casado, mediana do maior nível do mato original + %d; sem nada (só Galar), o maior nível "
              "do time no Ultimate Plus antes do 255. Nível novo = round(nível * alvo / "
              "maior nível do time), piso %d. Golpes regerados pelo learnset (linhas de golpe removidas)."
              % (PROFUNDIDADE, FOLGA_SELVAGEM, PISO_NIVEL),
        contagem=dict(manuais=len(manuais), reescalados=len(relatorio),
                      reescalados_galar=sum(r["regiao"] == "galar" for r in relatorio),
                      reescalados_unova=sum(r["regiao"] == "unova" for r in relatorio),
                      revanches=len(revanches), chefes_fase_f_movidos=movidos),
        manuais=[dict(constante=m["constante"], par=m["fonte"]["constante"], confianca=m["confianca"],
                      revanche=m["revanche"]) for m in manuais],
        reescalados=relatorio)
    json.dump(doc, open(SAIDA_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("manuais: %d; reescalados: Galar %d, Unova %d; revanches novas: %d (ids %s a %d); chefes da Fase F movidos: %d"
          % (len(manuais), doc["contagem"]["reescalados_galar"], doc["contagem"]["reescalados_unova"],
             len(revanches), linhas[0].split()[2] if linhas else "-", nid - 1, movidos))


# ------------------------------------------------------------------ demo
def demo():
    ok = True

    def caso(nome, cond):
        nonlocal ok
        print("  %-72s %s" % (nome, "ok" if cond else "REPROVOU"))
        ok = ok and bool(cond)

    _, atual = T.le_party(T.PARTY)
    ids = {k: int(v) for k, v in re.findall(r"(?m)^#define (TRAINER_\w+)\s+(\d+)", open(T.OPPS, encoding="utf-8").read())}
    doc = json.load(open(SAIDA_JSON, encoding="utf-8"))
    rs = doc["reescalados"]
    caso("todo reescalado tem revanche no .party com id acima de 3379",
         all(r["revanche"] in atual and ids.get(r["revanche"], 0) > 3379 for r in rs))
    caso("todo reescalado tem o maior nível igual ao alvo e nenhum acima de 100",
         all(max(T.niveis_do_bloco(atual[r["constante"]])) == r["alvo"] <= 100 for r in rs))
    caso("nenhum reescalado ficou com golpe escrito (learnset regera)",
         all(not re.search(r"(?m)^- MOVE_", atual[r["constante"]]) for r in rs))
    caso("a revanche guarda o time do hack (nível de antes)",
         all(max(T.niveis_do_bloco(atual[r["revanche"]])) >= 150 for r in rs))
    caso("espécies do reescalado iguais às da revanche (ordem e quantidade)",
         all(T.especies_do_bloco(atual[r["constante"]]) == T.especies_do_bloco(atual[r["revanche"]]) for r in rs))
    m = json.load(open(T.CASAMENTO % "unova", encoding="utf-8"))
    man = [r for r in m["casados"] if r.get("manual")]
    caso("os %d casados à mão estão nos casados e fora dos não casados" % len(MANUAL_UNOVA),
         {r["constante"] for r in man} == set(MANUAL_UNOVA)
         and not set(MANUAL_UNOVA) & {r["constante"] for r in m["nao_casados"]})
    caso("casado à mão tem o nível do Black 2 (nada acima de 79)",
         all(max(T.niveis_do_bloco(atual[r["constante"]])) <= 79 for r in man))
    ids_f = {c["id"] for c in json.load(open(T.FASE_F, encoding="utf-8"))["chefes"]}
    caso("nenhum chefe da Fase F aponta para constante sem bloco", ids_f <= set(atual))
    caso("nenhum chefe da Fase F ficou numa constante de campanha reescalada ou casada à mão",
         not ids_f & ({r["constante"] for r in rs} | set(MANUAL_UNOVA)))
    # par negativo: a regra da curva tem que enxergar um treinador fora da curva
    p2i, i2p, viz = grafo()
    cas = casados_por_mapa(atual, p2i)
    mato = mato_original()
    r0 = rs[0]
    alvo, _, _, _ = alvo_do_mapa(p2i[r0["mapa"]], viz, cas, mato)
    sujo = reescala_bloco(atual[r0["constante"]], 223)
    caso("mutação: o mesmo treinador em 223 fica a mais de 8 níveis da curva do lugar",
         abs(max(T.niveis_do_bloco(sujo)) - alvo) > 8)
    caso("reescala: [219, 221] para alvo 20 vira [20, 20] e perde os golpes",
         T.niveis_do_bloco(reescala_bloco("=== X ===\nName: A\n\nSPECIES_A\nLevel: 219\n- MOVE_TACKLE\n\n"
                                          "SPECIES_B\nLevel: 221\n", 20)) == [20, 20])
    print("DEMO", "VERDE" if ok else "VERMELHO")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.aplicar:
        aplicar()
    if a.demo:
        sys.exit(0 if demo() else 1)
    if not (a.aplicar or a.demo):
        ap.print_help()


if __name__ == "__main__":
    main()
