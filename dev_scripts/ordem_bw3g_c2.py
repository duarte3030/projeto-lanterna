#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Curva de nível de Unova pela ORDEM DE PROGRESSÃO do BW3G (cartucho 2, 28/10/2026).

    python3 dev_scripts/ordem_bw3g_c2.py --progressao  # grava dev_scripts/progressao_unova_bw3g.json
    python3 dev_scripts/ordem_bw3g_c2.py --aplicar     # reescala treinadores e mato de Unova
    python3 dev_scripts/ordem_bw3g_c2.py --demo        # invariantes no que está escrito (com par negativo)

A frente `c2-curva` (`curva_c2.py`) mediu a curva pelo LUGAR do Black 2. O mapa
do cartucho 2 é o do BW3G, que começa em Humilau: o ginásio 1 (Marlon) ficou em
49 a 51 e o Cheren (ginásio 5) em 11 a 13. Aqui a curva segue a ORDEM em que o
jogador percorre o BW3G, com a escala do Black 2.

Ordem dos ginásios, lida do próprio BW3G (nada de memória):
  - `constants/engine_flags.asm`, bloco `wJohtoBadges`: a ordem das insígnias;
  - `maps/*Gym*.asm`: que mapa dá cada insígnia (`setflag ENGINE_*BADGE`) e quem
    é o líder (`loadtrainer`);
  - `maps/Rt23East.asm`: os seis guardas da Rota 23 conferem as insígnias 2 a 7
    nessa mesma ordem (bloqueio de rota);
  - `data/trainers/parties.asm`: o maior nível de cada líder sobe de ginásio
    em ginásio (13, 18, 28, 36, 40, 42, 53, 63).
Resultado: Marlon, Shauntal, Burgh, Roxie, Cheren, Cilan, Skyla, Drayden.

Escala: o ginásio N do BW3G vale o ginásio N do Black 2 (Cheren 13, Roxie 18,
Burgh 24, Elesa 30, Clay 33, Skyla 39, Drayden 48, Marlon 51), a Elite Four vale
58 e o campeão 59. Entre um ginásio e o seguinte, a posição relativa do BW3G se
mantém: `curva(n)` é a interpolação linear, pelos pontos (nível do BW3G, nível do
Black 2) dos ginásios, do nível `n` que o BW3G dá ao treinador ou ao mato. O
trecho de cada mapa (entre o ginásio k e o k+1) sai do maior nível do BW3G no
mapa, e fica escrito em `progressao_unova_bw3g.json` com a evidência.

Treinadores (só Unova; Galar segue a ordem do Shield, ver `--progressao`):
  - líder: o time continua o do Black 2 (espécie, item, habilidade); o maior
    nível vai para o do ginásio de MESMO NÚMERO no Black 2;
  - os outros: maior nível = curva(maior nível do mesmo treinador no BW3G);
  - em todos, cada nível vira round(nível * alvo / maior), piso 2. Se algum
    Pokémon mudou mais de 5 níveis, os golpes escritos saem e o motor regera
    pelo learnset no nível novo.
  - Revanche: o time anterior que não existe em lugar nenhum (time do Black 2
    no nível do lugar do Black 2) vai para `<constante>_REVANCHE_B2`, ids a
    partir de 3801. O time do hack já está em `_REVANCHE` e não se duplica; o
    não casado só tinha um múltiplo de nível dele.
Mato (só mapas de campanha de Unova; o PWT fica): cada subtabela cujo maior
nível passa da curva do mapa (curva do maior nível do BW3G naquela subtabela,
ou o teto do trecho quando o BW3G não tem a tabela) é escalada para baixo; a
espécie fica.
"""
import argparse
import collections
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import times_originais_c2 as T  # noqa: E402
import curva_c2 as C  # noqa: E402

RAIZ = T.RAIZ
BW3G = os.path.join(T.FONTES, "bw3g")
PROG = os.path.join(AQUI, "progressao_unova_bw3g.json")
RELATORIO = os.path.join(AQUI, "ordem_bw3g_c2.json")
SUFIXO = "_REVANCHE_B2"
PRIMEIRO_ID = 3801
MARCA_INI = "// >>> Revanches da ordem do BW3G: times do Black 2 no nível do lugar (dev_scripts/ordem_bw3g_c2.py) >>>"
MARCA_FIM = "// <<< Revanches da ordem do BW3G <<<"
P_INI = "/* >>> Revanches da ordem do BW3G: times do Black 2 no nível do lugar (dev_scripts/ordem_bw3g_c2.py) >>> */"
P_FIM = "/* <<< Revanches da ordem do BW3G <<< */"
LIMIAR_GOLPES = 5
PISO = 2

# Líder do BW3G -> constante desta build.
LIDER_CONST = {k: "TRAINER_UNOVA_LEADER_" + k for k in
               ("MARLON", "SHAUNTAL", "BURGH", "ROXIE", "CHEREN", "CILAN", "SKYLA", "DRAYDEN")}
# Ordem dos ginásios do Black 2 (id em bw2_treinadores.json), do 1 ao 8.
B2_GINASIOS = [156, 157, 154, 153, 158, 155, 159, 160]   # Cheren, Roxie, Burgh, Elesa, Clay, Skyla, Drayden, Marlon
B2_E4, B2_CAMPEAO = 40, 341                              # Grimsley (primeira visita) e Iris
# Treinadores nomeados que o gerador de rota não cobre: grupo e índice do time no parties.asm.
NOMEADOS = {"TRAINER_UNOVA_N": ("NGroup", 0), "TRAINER_UNOVA_BIANCA": ("BiancaGroup", 0),
            "TRAINER_UNOVA_CHEREN_2": ("CherenGroup", 1),
            "TRAINER_UNOVA_E4_GRIMSLEY": ("GrimsleyGroup", 0), "TRAINER_UNOVA_E4_MARSHAL": ("MarshalGroup", 0),
            "TRAINER_UNOVA_E4_ELESA": ("ElesaGroup", 0), "TRAINER_UNOVA_E4_COLRESS": ("ColressGroup", 0),
            "TRAINER_UNOVA_CHAMPION_GENESIS": ("GenesisGroup", 0),
            "TRAINER_UNOVA_CHAMPION_JUNIPER_SNIVY": ("JuniperGroup", 0),
            "TRAINER_UNOVA_CHAMPION_JUNIPER_TEPIG": ("JuniperGroup", 1),
            "TRAINER_UNOVA_CHAMPION_JUNIPER_OSHAWOTT": ("JuniperGroup", 2)}


# ------------------------------------------------------------------ leitura do BW3G
def le_parties():
    """{Grupo: [[(nível, espécie)], ...]} do parties.asm, na ordem do arquivo."""
    fora, cur = {}, None
    for ln in open(os.path.join(BW3G, "data/trainers/parties.asm"), encoding="utf-8", errors="replace"):
        m = re.match(r"^(\w+Group):", ln)
        if m:
            cur = fora.setdefault(m.group(1), [])
            continue
        if cur is None:
            continue
        if re.match(r'\s*db\s+"', ln):
            cur.append([])
            continue
        m = re.match(r"\s*db\s+(\d+),\s*([A-Z][A-Z0-9_]*)", ln)
        if m and cur:
            cur[-1].append((int(m.group(1)), m.group(2)))
    return fora


def ordem_dos_ginasios():
    """[(insígnia, mapa do ginásio, líder, maior nível do líder no BW3G)] na ordem do jogo,
    com as provas cruzadas (ordem das insígnias, guardas da Rota 23, nível crescente)."""
    txt = open(os.path.join(BW3G, "constants/engine_flags.asm"), encoding="utf-8").read()
    bloco = txt[txt.index("; wJohtoBadges"):txt.index("; wKantoBadges")]
    insignias = re.findall(r"const (ENGINE_\w+BADGE)", bloco)
    assert len(insignias) == 8, insignias
    gin = {}
    for f in sorted(os.listdir(os.path.join(BW3G, "maps"))):
        if "Gym" not in f or not f.endswith(".asm"):
            continue
        s = open(os.path.join(BW3G, "maps", f), encoding="utf-8", errors="replace").read()
        m = re.search(r"setflag (ENGINE_\w+BADGE)", s)
        if not m:
            continue
        lt = re.findall(r"loadtrainer (\w+), \1\d", s)
        gin[m.group(1)] = (f[:-4], lt[0] if lt else None)
    # a ordem vem dos guardas da Rota 23 (insígnias 2 a 7, um guarda por insígnia, em fila);
    # a 1 e a 8 são as que os guardas não pedem, na ponta do bloco da RAM
    r23 = open(os.path.join(BW3G, "maps/Rt23East.asm"), encoding="utf-8").read()
    guardas = []
    for x in re.findall(r"checkflag (ENGINE_\w+BADGE)", r23):
        if x not in guardas:
            guardas.append(x)
    assert len(guardas) == 6 and set(guardas) < set(insignias), guardas
    fora_dos_guardas = [x for x in insignias if x not in guardas]
    assert fora_dos_guardas == [insignias[0], insignias[-1]], fora_dos_guardas
    ordem = [insignias[0]] + guardas + [insignias[-1]]
    parties = le_parties()
    fora = []
    for ins in ordem:
        mapa, lider = gin[ins]
        if lider is None:   # Mistralton: o líder está no 2F
            s = open(os.path.join(BW3G, "maps", mapa.replace("1F", "2F") + ".asm"), encoding="utf-8").read()
            lider = re.findall(r"loadtrainer (\w+), \1\d", s)[0]
        g = lider.capitalize() + "Group"
        ace = max(lv for lv, _ in parties[g][0])
        fora.append(dict(insignia=ins, mapa=mapa, lider=lider, nivel_bw3g=ace))
    # prova cruzada: o nível do líder sobe na ordem achada
    niveis = [g["nivel_bw3g"] for g in fora]
    assert niveis == sorted(niveis) and len(set(niveis)) == 8, niveis
    return fora


def mapas_bw3g():
    """{camel: CONST} do BW3G (mesmo pareamento do importador de Unova)."""
    import importa_unova as iu
    return {camel: const for _, mapas in iu.le_grupos() for (camel, const, *_resto) in mapas}


def mato_bw3g():
    """{CONST do mapa: {"grama": maior, "agua": maior}} do BW3G."""
    fora = collections.defaultdict(dict)
    for arq, tipo in (("johto_grass.asm", "grama"), ("johto_water.asm", "agua")):
        cur = None
        for ln in open(os.path.join(BW3G, "data/wild", arq), encoding="utf-8"):
            if ln.lstrip().startswith(";"):
                continue
            m = re.match(r"\s*map_id\s+(\w+)", ln)
            if m:
                cur = m.group(1)
                continue
            m = re.match(r"\s*db\s+(\d+),\s*([A-Z][A-Z0-9_]+)\s*$", ln)
            if m and cur:
                fora[cur][tipo] = max(fora[cur].get(tipo, 0), int(m.group(1)))
    return fora


def treinadores_bw3g():
    """{constante desta build: maior nível do mesmo treinador no BW3G}. O par é
    pela lista de constantes de cada classe do BW3G, o mesmo leitor que gerou
    os treinadores de Unova (`gera_treinadores_unova.py`); os nomeados que ele
    não cobre vêm da tabela NOMEADOS. Os líderes ficam de fora (curva própria)."""
    import gera_treinadores_unova as G
    classes, times = G.le_classes(), G.le_times()
    fora = {}
    for cl, lst in classes.items():
        g = G.grupo_de(cl, times)
        if not g:
            continue
        for i, co in enumerate(lst):
            if i < len(times[g]) and times[g][i]["mons"]:
                fora.setdefault("TRAINER_UNOVA_" + co, max(l for l, _ in times[g][i]["mons"]))
    parties = le_parties()
    for const, (g, i) in NOMEADOS.items():
        fora[const] = max(lv for lv, _ in parties[g][i])
    for c in LIDER_CONST.values():
        fora.pop(c, None)
    return fora


# ------------------------------------------------------------------ curva
def pontos():
    """[(nível BW3G, nível Black 2)] dos marcos: início, 8 ginásios, Elite Four, campeão."""
    b2 = {x["id"]: x for x in json.load(open(os.path.join(T.SAIDA, "bw2_treinadores.json"), encoding="utf-8"))}

    def topo(i):
        return max(m["nivel"] for m in b2[i]["time"])
    gins = ordem_dos_ginasios()
    parties = le_parties()
    e4 = max(lv for lv, _ in parties["GrimsleyGroup"][0])
    camp = max(lv for t in parties["JuniperGroup"] for lv, _ in t)
    pts = [(0, 0)] + [(g["nivel_bw3g"], topo(i)) for g, i in zip(gins, B2_GINASIOS)]
    pts += [(e4, topo(B2_E4)), (camp, topo(B2_CAMPEAO))]
    return pts


def curva(n, pts):
    """Interpolação linear de `n` (nível do BW3G) nos marcos; acima do último, o último."""
    if n >= pts[-1][0]:
        return pts[-1][1]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= n <= x1:
            return max(PISO, round(y0 + (y1 - y0) * (n - x0) / (x1 - x0)))
    return PISO


def trecho_de(n, pts):
    """Trecho do nível `n` do BW3G: 0 antes do ginásio 1, k entre o ginásio k e o
    k+1, 8 entre o Drayden e a Liga, 9 na Liga. O treinador do ginásio k (abaixo
    do líder) fica no trecho k-1, que é quando o jogador o enfrenta."""
    if n >= pts[9][0]:                   # nível da Elite Four em diante
        return 9
    return sum(1 for x, _ in pts[1:9] if n > x)


def progressao():
    gins = ordem_dos_ginasios()
    pts = pontos()
    camel_const = mapas_bw3g()
    mato = mato_bw3g()
    trn = treinadores_bw3g()
    por_mapa = collections.defaultdict(list)
    for c, mps in T.referencias().items():
        if c in trn:
            for mp in mps:
                por_mapa[mp].append(trn[c])
    p2i, i2p, viz = C.grafo()
    mapas = {}
    for pasta in sorted(p for p in p2i if p.startswith("Unova_")):
        camel = pasta[len("Unova_"):]
        const = camel_const.get(camel)
        w = mato.get(const, {})
        t = max(por_mapa.get(pasta, []), default=None)
        ref = t if t is not None else max(w.values(), default=None)
        if ref is None:
            continue
        mapas[pasta] = dict(bw3g=const, treinador_bw3g=t, grama_bw3g=w.get("grama"), agua_bw3g=w.get("agua"),
                            trecho=trecho_de(ref, pts), fonte="treinador" if t is not None else "mato")
    # mapa sem evidência própria herda o trecho do vizinho mais perto (para o mato e para o relatório)
    for pasta in sorted(p for p in p2i if p.startswith("Unova_")):
        if pasta in mapas:
            continue
        vistos, frente, d = {p2i[pasta]}, [p2i[pasta]], 0
        while frente and d < 4:
            d += 1
            nova = []
            for m in frente:
                for v in sorted(viz.get(m, ())):
                    if v not in vistos:
                        vistos.add(v)
                        nova.append(v)
            frente = nova
            achados = [mapas[i2p[m]]["trecho"] for m in frente if i2p[m] in mapas and mapas[i2p[m]]["fonte"] != "vizinho"]
            if achados:
                mapas[pasta] = dict(bw3g=camel_const.get(pasta[6:]), trecho=min(achados), fonte="vizinho",
                                    distancia=d)
                break
    nomes = ["antes do ginásio 1"] + ["entre o ginásio %d e o %d" % (k, k + 1) for k in range(1, 8)] \
        + ["entre o ginásio 8 e a Liga", "Liga"]
    trechos = []
    for k in range(10):
        lo_b, hi_b = pts[k][1], pts[min(k + 1, len(pts) - 1)][1]
        trechos.append(dict(trecho=k, nome=nomes[k], bw3g=[pts[k][0], pts[min(k + 1, len(pts) - 1)][0]],
                            black2=[max(PISO, lo_b), hi_b],
                            mapas=sorted(m for m, v in mapas.items() if v["trecho"] == k)))
    doc = collections.OrderedDict(
        sobre="Ordem de progressão do BW3G no cartucho 2 (dev_scripts/ordem_bw3g_c2.py --progressao). "
              "Cada mapa de Unova com treinador ou mato fica num trecho: k = entre o ginásio k e o k+1 "
              "(0 antes do primeiro, 8 entre o oitavo e a Liga, 9 a Liga). Evidência: o maior nível que o "
              "próprio BW3G dá aos treinadores do mapa (ou ao mato, sem treinador); sem nenhum dos dois, o "
              "trecho do vizinho mais perto no grafo de borda e warp.",
        ginasios=[dict(numero=i + 1, **g, nivel_black2=pts[i + 1][1]) for i, g in enumerate(gins)],
        provas=["constants/engine_flags.asm (wJohtoBadges): Wave, Spooky, Insect, Toxic, Garnish, Basic, Jet, "
                "Legend; maps/Rt23East.asm: guardas pedem Spooky, Insect, Toxic, Basic, Garnish, Jet nessa ordem; "
                "o maior nível do líder sobe de ginásio em ginásio (parties.asm)",
                "a ordem das insígnias na RAM (Garnish antes de Basic) não é a do jogo: o guarda 4 da Rota 23 pede "
                "a Basic e o 5 a Garnish, e o Cheren (40) vem antes do Cilan (42)"],
        pontos_da_curva=[dict(bw3g=x, black2=y) for x, y in pts],
        trechos=trechos, mapas=mapas,
        galar="O Ultimate Plus segue a ordem do Shield: Milo, Nessa, Kabu, Bea ou Allister, Opal, Gordie ou "
              "Melony, Piers, Raihan (Turffield, Hulbury, Motostoke, Stow-on-Side, Ballonlea, Circhester, "
              "Spikemuth, Hammerlocke), e o nível do demake antes do 255 sobe nessa ordem (Bea 36, Opal 39, "
              "Gordie 43, Piers 47; Hop 21, 33, 37, 41, 49). A curva de Galar por lugar já é a curva por ordem.")
    return doc


# ------------------------------------------------------------------ aplicar
def campanha_unova(atual):
    """{constante: [mapas]} dos treinadores de campanha de Unova (sem revanche e sem o PWT)."""
    refs = T.referencias()
    d = json.load(open(T.CASAMENTO % "unova", encoding="utf-8"))
    pos = {r["constante"] for r in d["nao_casados"]
           if r.get("curva", "").startswith("fica") or (r["mapas"] and all(C.POS_JOGO_UNOVA.match(m) for m in r["mapas"]))}
    casados = {r["constante"] for r in d["casados"]}
    camp = {c: m for c, m in refs.items() if c.startswith("TRAINER_UNOVA_") and c in atual
            and not re.search(r"_REVANCHE(_B2)?$", c) and c not in pos
            and not all(C.POS_JOGO_UNOVA.match(x) for x in m)}
    return camp, casados


def alvos(prog, trn, camp):
    """{constante: (alvo, de onde)}."""
    nivel_lider = {LIDER_CONST[g["lider"]]: (g["nivel_black2"], "ginásio %d do Black 2" % g["numero"])
                   for g in prog["ginasios"]}
    pts = [(p["bw3g"], p["black2"]) for p in prog["pontos_da_curva"]]
    liga = {"E4": (pts[9][1], "Elite Four do Black 2"), "CHAMPION": (pts[10][1], "campeã do Black 2")}
    fora = {}
    for c in camp:
        m = re.match(r"TRAINER_UNOVA_(E4|CHAMPION)_", c)
        if c in nivel_lider:
            fora[c] = nivel_lider[c]
        elif m:
            fora[c] = liga[m.group(1)]
        elif c in trn:
            fora[c] = (curva(trn[c], pts), "curva(%d do BW3G)" % trn[c])
    return fora


def reescala(bloco, alvo):
    """(bloco novo, golpes regerados?) com o maior nível em `alvo`."""
    lv = T.niveis_do_bloco(bloco)
    topo = max(lv)
    novos = [max(PISO, round(x * alvo / topo)) for x in lv]
    it = iter(novos)
    b = re.sub(r"(?m)^Level: (\d+)", lambda m: "Level: %d" % next(it), bloco)
    regera = max(abs(a - n) for a, n in zip(lv, novos)) > LIMIAR_GOLPES
    if regera:
        b = re.sub(r"(?m)^- MOVE_\S*[ \t]*\n", "", b)
    return b, regera


def cap_do_mato(info, prog, pts):
    """{subtabela: teto} do mapa, pela curva do BW3G (ou o teto do trecho)."""
    teto_trecho = prog["trechos"][info["trecho"]]["black2"][1]
    g = curva(info["grama_bw3g"], pts) if info.get("grama_bw3g") else None
    a = curva(info["agua_bw3g"], pts) if info.get("agua_bw3g") else None
    land = g or teto_trecho
    water = a or g or teto_trecho
    return {"land_mons": land, "water_mons": water, "fishing_mons": max(land, water),
            "rock_smash_mons": max(land, water)}


def aplicar():
    prog = progressao()
    json.dump(prog, open(PROG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    pts = [(p["bw3g"], p["black2"]) for p in prog["pontos_da_curva"]]
    texto, atual = T.le_party(T.PARTY)
    opp = open(T.OPPS, encoding="utf-8").read()
    if MARCA_INI in opp or P_INI in texto:
        sys.exit("o bloco de revanches da ordem do BW3G já existe: --aplicar já rodou nesta árvore")
    camp, casados = campanha_unova(atual)
    trn = treinadores_bw3g()
    alv = alvos(prog, trn, camp)
    sem = sorted(set(camp) - set(alv))
    novos, revanches, vistos, rel = {}, [], {}, []
    for c in sorted(alv):
        alvo, fonte = alv[c]
        antes = T.niveis_do_bloco(atual[c])
        if not antes or max(antes) == alvo:
            continue
        b, regera = reescala(atual[c], alvo)
        novos[c] = b
        rv = None
        if c in casados and abs(max(antes) - alvo) > LIMIAR_GOLPES:
            cab, time, _ = C.time_do_bloco(atual[c])
            if time not in vistos:
                nome = c + SUFIXO
                assert nome not in atual, nome
                vistos[time] = nome
                revanches.append((nome, "=== %s ===\n" % nome + "\n".join(cab) + "\n\n" + time + "\n\n", c))
            rv = vistos[time]
        rel.append(dict(constante=c, mapas=camp[c], alvo=alvo, fonte=fonte, antes=antes,
                        depois=T.niveis_do_bloco(b), golpes_regerados=regera, casado=c in casados, revanche=rv))
    # .party
    out, pos = [], 0
    for c, a, b in T.blocos(texto):
        if c in novos:
            out.append(texto[pos:a])
            bl = novos[c]
            out.append(bl if bl.endswith("\n\n") else bl.rstrip("\n") + "\n\n")
            pos = b
    out.append(texto[pos:])
    texto = "".join(out)
    if revanches:
        texto = texto.rstrip("\n") + "\n\n" + P_INI + "\n" + "".join(b for _, b, _ in revanches) + P_FIM + "\n"
    # ids
    usados = {int(v) for v in re.findall(r"(?m)^#define TRAINER_\w+\s+(\d+)", opp)}
    nid = PRIMEIRO_ID
    linhas = []
    for nome, _, dono in revanches:
        while nid in usados:
            nid += 1
        assert nid <= T.TETO_ID, "acabou a faixa de ids de treinador (%d revanches)" % len(revanches)
        linhas.append("#define %-48s %d  // time do Black 2 no nível do lugar, de %s" % (nome, nid, dono))
        nid += 1
    if linhas:
        bloco_ids = (MARCA_INI + "\n// Curva pela ordem do BW3G: o casado foi para o nível do trecho; o time do\n"
                     "// Black 2 no nível do lugar do Black 2 fica aqui, sem mapa.\n"
                     + "\n".join(linhas) + "\n" + MARCA_FIM + "\n")
        alvo_txt = "#define MAX_TRAINERS_COUNT_EMERALD"
        i = opp.rfind("\n", 0, opp.index(alvo_txt)) + 1
        opp = opp[:i] + bloco_ids + "\n" + opp[i:]
    # mato
    wild = json.load(open(T.WILD, encoding="utf-8"))
    p2i, i2p, _ = C.grafo()
    mato_rel = []
    for e in wild["wild_encounter_groups"][0]["encounters"]:
        pasta = i2p.get(e["map"])
        if not pasta or not pasta.startswith("Unova_") or C.POS_JOGO_UNOVA.match(pasta):
            continue
        info = prog["mapas"].get(pasta)
        if not info:
            continue
        caps = cap_do_mato(info, prog, pts)
        for k, cap in caps.items():
            if k not in e:
                continue
            mons = e[k]["mons"]
            topo = max(m["max_level"] for m in mons)
            if topo <= cap:
                continue
            for m in mons:
                m["min_level"] = max(PISO, round(m["min_level"] * cap / topo))
                m["max_level"] = max(m["min_level"], round(m["max_level"] * cap / topo))
            mato_rel.append(dict(mapa=pasta, subtabela=k, trecho=info["trecho"], antes=topo, depois=cap))
    open(T.PARTY, "w", encoding="utf-8").write(texto)
    open(T.OPPS, "w", encoding="utf-8").write(opp)
    with open(T.WILD, "w", encoding="utf-8") as f:
        json.dump(wild, f, ensure_ascii=False, indent=2)
        f.write("\n")
    doc = collections.OrderedDict(
        sobre="Reescala de Unova pela ordem do BW3G (dev_scripts/ordem_bw3g_c2.py --aplicar). Um registro por "
              "treinador que mudou de nível e por subtabela de mato que desceu para a curva.",
        contagem=dict(treinadores=len(rel), lideres=sum(r["constante"] in LIDER_CONST.values() for r in rel),
                      revanches=len(revanches), golpes_regerados=sum(r["golpes_regerados"] for r in rel),
                      sem_nivel_do_bw3g=len(sem), mato_subtabelas=len(mato_rel),
                      mato_mapas=len({m["mapa"] for m in mato_rel})),
        ids_revanche=[linhas[0].split()[2], nid - 1] if linhas else [],
        sem_nivel_do_bw3g=sem, treinadores=rel, mato=mato_rel)
    json.dump(doc, open(RELATORIO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("treinadores reescalados: %d (líderes %d, golpes regerados %d); revanches novas: %d %s; "
          "sem nível do BW3G: %d; mato: %d subtabelas em %d mapas"
          % (len(rel), doc["contagem"]["lideres"], doc["contagem"]["golpes_regerados"], len(revanches),
             doc["ids_revanche"], len(sem), len(mato_rel), doc["contagem"]["mato_mapas"]))


# ------------------------------------------------------------------ demo
def demo():
    ok = True

    def caso(nome, cond):
        nonlocal ok
        print("  %-78s %s" % (nome, "ok" if cond else "REPROVOU"))
        ok = ok and bool(cond)

    prog = json.load(open(PROG, encoding="utf-8"))
    pts = [(p["bw3g"], p["black2"]) for p in prog["pontos_da_curva"]]
    rel = json.load(open(RELATORIO, encoding="utf-8"))
    _, atual = T.le_party(T.PARTY)
    gins = prog["ginasios"]
    caso("ordem: Marlon, Shauntal, Burgh, Roxie, Cheren, Cilan, Skyla, Drayden",
         [g["lider"] for g in gins] == ["MARLON", "SHAUNTAL", "BURGH", "ROXIE", "CHEREN", "CILAN", "SKYLA", "DRAYDEN"])
    caso("ordem recalculada do BW3G bate com a gravada",
         [g["lider"] for g in ordem_dos_ginasios()] == [g["lider"] for g in gins])
    caso("líder N tem o maior nível do ginásio N do Black 2",
         all(max(T.niveis_do_bloco(atual[LIDER_CONST[g["lider"]]])) == g["nivel_black2"] for g in gins))
    caso("o maior nível dos líderes sobe de ginásio em ginásio",
         [max(T.niveis_do_bloco(atual[LIDER_CONST[g["lider"]]])) for g in gins]
         == sorted(max(T.niveis_do_bloco(atual[LIDER_CONST[g["lider"]]])) for g in gins))
    caso("curva: marcos exatos e monotônica",
         all(curva(x, pts) == max(PISO, y) for x, y in pts[1:])
         and all(curva(n, pts) <= curva(n + 1, pts) for n in range(0, 80)))
    camp, _ = campanha_unova(atual)
    trn = treinadores_bw3g()
    alv = alvos(prog, trn, camp)
    caso("todo treinador de campanha de Unova com nível do BW3G está no alvo",
         all(max(T.niveis_do_bloco(atual[c])) == a for c, (a, _) in alv.items() if T.niveis_do_bloco(atual[c])))
    caso("nenhum treinador de campanha de Unova acima de 100",
         all(max(T.niveis_do_bloco(atual[c]), default=0) <= 100 for c in camp))
    ids = {k: int(v) for k, v in re.findall(r"(?m)^#define (TRAINER_\w+)\s+(\d+)", open(T.OPPS, encoding="utf-8").read())}
    caso("toda revanche nova tem bloco e id de 3801 a 3999",
         all(r["revanche"] in atual and PRIMEIRO_ID <= ids.get(r["revanche"], 0) <= T.TETO_ID
             for r in rel["treinadores"] if r["revanche"]))
    caso("revanche nova guarda o nível de antes",
         all(T.niveis_do_bloco(atual[r["revanche"]]) == r["antes"] for r in rel["treinadores"] if r["revanche"]))
    wild = json.load(open(T.WILD, encoding="utf-8"))
    p2i, i2p, _ = C.grafo()
    acima = []
    for e in wild["wild_encounter_groups"][0]["encounters"]:
        pasta = i2p.get(e["map"])
        info = prog["mapas"].get(pasta or "")
        if not info or C.POS_JOGO_UNOVA.match(pasta):
            continue
        for k, cap in cap_do_mato(info, prog, pts).items():
            if k in e and max(m["max_level"] for m in e[k]["mons"]) > cap:
                acima.append((pasta, k))
    caso("nenhuma subtabela de mato de campanha de Unova acima da curva do mapa", not acima)
    # par negativo: a régua enxerga o Marlon de volta no 51 e um mato de volta no 236
    sujo = re.sub(r"(?m)^Level: (\d+)", "Level: 51", atual[LIDER_CONST["MARLON"]])
    caso("mutação: Marlon no 51 sai do alvo do ginásio 1", max(T.niveis_do_bloco(sujo)) != gins[0]["nivel_black2"])
    info = prog["mapas"]["Unova_DragonspiralTower2F"]
    caso("mutação: mato da Dragonspiral 2F no 236 passa do teto do mapa",
         236 > cap_do_mato(info, prog, pts)["land_mons"])
    print("DEMO", "VERDE" if ok else "VERMELHO")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--progressao", action="store_true")
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.progressao:
        json.dump(progressao(), open(PROG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("gravado", PROG)
    if a.aplicar:
        aplicar()
    if a.demo:
        sys.exit(0 if demo() else 1)
    if not (a.progressao or a.aplicar or a.demo):
        ap.print_help()


if __name__ == "__main__":
    main()
