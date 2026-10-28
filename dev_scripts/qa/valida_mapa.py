#!/usr/bin/env python3
"""Os 11 portões de mapa que faltavam ao repo, com linha de base versionada.

Uso:
    python3 dev_scripts/qa/valida_mapa.py                 # portão: exit 1 só com achado NOVO
    python3 dev_scripts/qa/valida_mapa.py --lista         # todo achado, novo ou da base
    python3 dev_scripts/qa/valida_mapa.py --demo          # mutação plantada em cada portão
    python3 dev_scripts/qa/valida_mapa.py --grava-base    # regrava a base (só com motivo no commit)

Por que existe
--------------
O PRD do cartucho 2 citava um `valida_mapa.py` que nunca existiu em nenhum dos
dois repos. A trilha F do PRD de assets (28/10/2026) prototipou os portões em
`fontes-mapas/prd-assets/poc-F/f3_portoes.py`, rodou em modo leitura e achou
defeito de verdade: 30 conexões de borda sem volta (18 em Galar) e 4 casas de
Johto que o motor acha que são Sinnoh. Este arquivo é o protótipo promovido.

Os portões, cada um com letra para conversar com a lente de warps (P1 a P4):

    C1  conexão de borda sem volta: A liga em B pela direção d e B não liga em
        A pela oposta (o vizinho aparece na borda e some ao atravessar)
    C2  volta com deslocamento não simétrico (o mundo "pula" na travessia)
    C3  conexão para mapa que não existe
    V1  VMap estourado, (largura+15) x (altura+14) > 10240
        (include/fieldmap.h; o motor não carrega o mapa e não avisa)
    E1  mais de 64 object_events (OBJECT_EVENT_TEMPLATES_COUNT, sem checagem)
    E2  mais de 127 warps (o índice de destino é s8; 127 é WARP_ID_DYNAMIC)
    E3  contagem de evento acima de 255 (o cabeçalho guarda u8)
    K1  id de mapa (grupo, número) igual a MAP_DYNAMIC (127,127) ou
        MAP_UNDEFINED (255,255), include/constants/maps.h
    M1  a região que o motor deduz (GetCurrentRegion, include/regions.h: Johto
        por faixa de grupo, o resto por faixa de MAPSEC) não bate com a de
        NENHUM vizinho por warp ou conexão
    H1  heal location em mapa inexistente, fora do layout, em tile com colisão
        ou cercado (sem caminho até warp ou borda conectada)
    F3  porta partida candidata: dois warps colados levando para interiores
        diferentes. Sem a fonte ao lado dá falso positivo de idioma (escada
        colada em escada), e por isso aqui ele é só portão de NOVO achado.

A linha de base
---------------
O repo nasce com achado antigo (os 30 C1, os 4 M1). Portão que fica vermelho
para sempre é portão que ninguém lê, então `valida_mapa_base.json`, ao lado,
guarda os achados de 28/10/2026 e o portão só reprova achado que NÃO está lá.
Achado da base que sumiu é conserto: aparece como "resolvido" e não reprova;
regrave a base no mesmo commit para ele não voltar escondido.

Regra para mexer na base: só com `--grava-base`, e o commit diz por que o
achado novo é aceito. Base que cresce sem motivo vira esconderijo (risco 2 da
seção 3.6 do anexo F).

Só lê `data/maps`, `data/layouts`, `src/data/heal_locations.json`,
`src/data/region_map/region_map_sections.json` e o molde
`region_map_sections.constants.json.txt` ao lado dele. Não compila e roda numa
árvore sem build. Cerca de 1 s.
"""
import argparse
import collections
import copy
import json
import os
import re
import struct
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
BASE = os.path.join(AQUI, "valida_mapa_base.json")
OPOSTA = {"up": "down", "down": "up", "left": "right", "right": "left"}
REGRAS = ("C1", "C2", "C3", "V1", "E1", "E2", "E3", "K1", "M1", "H1", "F3")
# Regras cuja chave é só o mapa: o número dentro do texto (quantos objetos,
# quantos warps) muda sem o defeito mudar, e não pode virar "achado novo".
CHAVE_SO_MAPA = {"V1", "E1", "E2", "E3", "K1"}
VMAP_MAX = 10240
OBJETOS_MAX = 64
WARPS_MAX = 127
EVENTOS_MAX = 255
IDS_PROIBIDOS = ((127, 127), (255, 255))


# ---------------------------------------------------------------------------
# leitura
# ---------------------------------------------------------------------------
def carrega(raiz):
    grupos = json.load(open(os.path.join(raiz, "data/maps/map_groups.json")))
    mapas, por_id = {}, {}
    for gi, g in enumerate(grupos["group_order"]):
        for mi, nome in enumerate(grupos[g]):
            try:
                m = json.load(open(os.path.join(raiz, "data/maps", nome, "map.json")))
            except OSError:
                continue
            m["_g"], m["_n"], m["_pasta"] = gi, mi, nome
            mapas[nome] = m
            por_id[m["id"]] = m
    lays = {L["id"]: L for L in json.load(open(os.path.join(raiz, "data/layouts/layouts.json")))["layouts"]
            if "width" in L}
    secs = [s["id"] for s in json.load(open(os.path.join(raiz, "src/data/region_map/region_map_sections.json")))["map_sections"]]
    val = {s: i for i, s in enumerate(secs)}
    val["MAPSEC_NONE"] = len(secs)
    # Os apelidos de MAPSEC (os 65 de Johto, por exemplo) moram no molde do
    # gerador; o .h de include/constants é GERADO pelo make e não existe numa
    # árvore recém-clonada.
    h = open(os.path.join(raiz, "src/data/region_map/region_map_sections.constants.json.txt")).read()
    for _ in range(3):  # apelido de apelido
        for a, b in re.findall(r"^#define\s+(MAPSEC_\w+)\s+(MAPSEC_\w+)\s*$", h, re.M):
            if b in val:
                val[a] = val[b]
    curas = json.load(open(os.path.join(raiz, "src/data/heal_locations.json")))["heal_locations"]
    return dict(raiz=raiz, grupos=grupos, mapas=mapas, por_id=por_id, lays=lays, val=val, curas=curas,
                blocos={})


def blocos(d, L):
    if L["id"] not in d["blocos"]:
        b = open(os.path.join(d["raiz"], L["blockdata_filepath"]), "rb").read()
        d["blocos"][L["id"]] = struct.unpack(f"<{len(b) // 2}H", b)
    return d["blocos"][L["id"]]


def regiao_por_mapsec(val):
    """Espelha GetRegionForSectionId de include/regions.h."""
    def reg(x):
        if val.get("MAPSEC_PALLET_TOWN", 999) <= x < val.get("MAPSEC_SPECIAL_AREA", -1):
            return "Kanto"
        for r, a, b in (("Sinnoh", "MAPSEC_SINNOH_WEST", "MAPSEC_SINNOH_NORTH"),
                        ("Unova", "MAPSEC_UNOVA_WEST", "MAPSEC_UNOVA_NORTH"),
                        ("Galar", "MAPSEC_GALAR_SOUTH", "MAPSEC_GALAR_OTHER")):
            if a in val and b in val and val[a] <= x <= val[b]:
                return r
        return "Hoenn"
    return reg


# ---------------------------------------------------------------------------
# os portões
# ---------------------------------------------------------------------------
def portoes(d):
    mapas, por_id, lays, val, grupos = d["mapas"], d["por_id"], d["lays"], d["val"], d["grupos"]
    ach = []

    def a(regra, mapa, texto):
        ach.append((regra, mapa, texto))

    for nome, m in mapas.items():
        L = lays.get(m["layout"])
        for c in m.get("connections") or []:
            if c["direction"] not in OPOSTA:
                continue  # dive e emerge: ligação vertical, régua própria
            b = por_id.get(c["map"])
            if b is None:
                a("C3", nome, f"conexão {c['direction']} para {c['map']}, que não existe")
                continue
            volta = [x for x in (b.get("connections") or [])
                     if x["map"] == m["id"] and x["direction"] == OPOSTA[c["direction"]]]
            if not volta:
                a("C1", nome, f"liga em {b['_pasta']} por {c['direction']}, e {b['_pasta']} "
                              f"não liga de volta por {OPOSTA[c['direction']]}")
            elif all(int(x["offset"]) != -int(c["offset"]) for x in volta):
                a("C2", nome, f"{c['direction']} {b['_pasta']} offset {c['offset']}, volta com offset "
                              f"{[x['offset'] for x in volta]} (esperado {-int(c['offset'])})")
        if L and (L["width"] + 15) * (L["height"] + 14) > VMAP_MAX:
            a("V1", nome, f"layout {L['width']}x{L['height']}: VMap "
                          f"{(L['width'] + 15) * (L['height'] + 14)} > {VMAP_MAX}")
        n_obj, n_w = len(m.get("object_events") or []), len(m.get("warp_events") or [])
        if n_obj > OBJETOS_MAX:
            a("E1", nome, f"{n_obj} object_events (teto {OBJETOS_MAX})")
        if n_w > WARPS_MAX:
            a("E2", nome, f"{n_w} warps (teto {WARPS_MAX})")
        for k in ("object_events", "warp_events", "coord_events", "bg_events"):
            if len(m.get(k) or []) > EVENTOS_MAX:
                a("E3", nome, f"{k}: {len(m[k])}")
        if (m["_g"], m["_n"]) in IDS_PROIBIDOS:
            a("K1", nome, f"id ({m['_g']},{m['_n']}) colide com MAP_DYNAMIC/MAP_UNDEFINED")
        ws = m.get("warp_events") or []
        vistos = set()
        for i, w1 in enumerate(ws):
            for w2 in ws[i + 1:]:
                if (w1["dest_map"] != w2["dest_map"] and abs(w1["x"] - w2["x"]) <= 1
                        and abs(w1["y"] - w2["y"]) <= 1):
                    d1, d2 = por_id.get(w1["dest_map"]), por_id.get(w2["dest_map"])
                    par = frozenset((w1["dest_map"], w2["dest_map"]))
                    if (d1 and d2 and par not in vistos
                            and "INDOOR" in d1.get("map_type", "") and "INDOOR" in d2.get("map_type", "")):
                        vistos.add(par)
                        a("F3", nome, f"({w1['x']},{w1['y']})->{d1['_pasta']} colado em "
                                      f"({w2['x']},{w2['y']})->{d2['_pasta']}")

    # M1
    go = grupos["group_order"]
    def grupo_de(pasta):
        return next(i for i, g in enumerate(go) if pasta in grupos[g])
    try:
        j0, j1 = grupo_de("NewBarkTown"), grupo_de("WorldHub2")
    except StopIteration:
        j0 = j1 = -1
    neutras = {val.get(k) for k in ("MAPSEC_SPECIAL_AREA", "MAPSEC_NONE", "MAPSEC_DYNAMIC")}
    reg_de = regiao_por_mapsec(val)

    def reg_motor(m):
        if j0 <= m["_g"] <= j1:
            return "Johto"
        ms = val.get(m.get("region_map_section"))
        if ms is None or ms in neutras:
            return None
        return reg_de(ms)
    for nome, m in mapas.items():
        r = reg_motor(m)
        if r is None:
            continue
        viz = {reg_motor(por_id[w["dest_map"]]) for w in (m.get("warp_events") or []) if w["dest_map"] in por_id}
        viz |= {reg_motor(por_id[c["map"]]) for c in (m.get("connections") or []) if c["map"] in por_id}
        viz.discard(None)
        if viz and r not in viz:
            a("M1", nome, f"MAPSEC {m.get('region_map_section')} dá {r}; vizinhos são {sorted(viz)}")

    # H1
    for h in d["curas"]:
        m = por_id.get(h["map"])
        if m is None:
            a("H1", h["id"], f"mapa {h['map']} não existe")
            continue
        if h.get("respawn_map") and h["respawn_map"] not in por_id:
            a("H1", h["id"], f"respawn_map {h['respawn_map']} não existe")
        L = lays.get(m["layout"])
        if not L:
            continue
        W, H, x, y = L["width"], L["height"], h["x"], h["y"]
        if not (0 <= x < W and 0 <= y < H):
            a("H1", h["id"], f"({x},{y}) fora do layout {W}x{H} de {m['_pasta']}")
            continue
        bl = blocos(d, L)
        livre = lambda i, j: (bl[j * W + i] >> 10) & 3 == 0
        if not livre(x, y):
            a("H1", h["id"], f"({x},{y}) em {m['_pasta']} é tile com colisão")
            continue
        alvos = {(w["x"], w["y"]) for w in m.get("warp_events") or []}
        lados = {c["direction"] for c in m.get("connections") or []}
        fila, visto, ok = [(x, y)], {(x, y)}, False
        while fila and not ok:
            i, j = fila.pop()
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                u, v = i + di, j + dj
                if (u, v) in alvos:
                    ok = True
                    break
                if not (0 <= u < W and 0 <= v < H):
                    if ("left" if u < 0 else "right" if u >= W else "up" if v < 0 else "down") in lados:
                        ok = True
                        break
                    continue
                if (u, v) not in visto and livre(u, v):
                    visto.add((u, v))
                    fila.append((u, v))
        if not ok:
            a("H1", h["id"], f"({x},{y}) em {m['_pasta']} não alcança warp nem borda conectada")
    return ach


def chave(regra, mapa, texto):
    return f"{regra} {mapa}" if regra in CHAVE_SO_MAPA else f"{regra} {mapa}: {texto}"


def folga(d):
    """Régua de folga, não reprova: quanto falta para o grupo 127 nascer MAP_DYNAMIC."""
    go, g = d["grupos"]["group_order"], d["grupos"]
    linhas = [f"{len(d['mapas'])} mapas, {len(go)} grupos de 255, maior grupo com "
              f"{max(len(g[x]) for x in go)} mapas"]
    if len(go) > 127:
        n = len(g[go[127]])
        linhas.append(f"grupo 127 ({go[127]}): {n} mapas; o mapa de índice 127 seria MAP_DYNAMIC, "
                      f"folga {127 - n}")
    return linhas


# ---------------------------------------------------------------------------
# --demo: uma mutação plantada por portão, na memória
# ---------------------------------------------------------------------------
def mutacoes(d):
    """Cada função recebe uma cópia profunda dos dados e planta UM defeito."""
    mapas, por_id = d["mapas"], d["por_id"]
    # um par de conexões que fecha hoje, para o C1 e o C2
    par = None
    for nome, m in sorted(mapas.items()):
        for c in m.get("connections") or []:
            b = por_id.get(c["map"])
            if c["direction"] in OPOSTA and b:
                v = [x for x in b.get("connections") or []
                     if x["map"] == m["id"] and x["direction"] == OPOSTA[c["direction"]]
                     and int(x["offset"]) == -int(c["offset"])]
                if len(v) == 1:
                    par = (nome, b["_pasta"], c["direction"])
                    break
        if par:
            break
    alvo = par[0]
    interiores = sorted(n for n, m in mapas.items() if "INDOOR" in m.get("map_type", ""))[:2]
    # mapa de Unova com vizinho de Unova, para o M1 trocar a MAPSEC por uma de Galar
    unova = next(n for n, m in sorted(mapas.items())
                 if m.get("region_map_section", "").startswith("MAPSEC_UNOVA") and (m.get("warp_events")))

    def c1(x):
        a, b, dr = par
        x["mapas"][b]["connections"] = [c for c in x["mapas"][b]["connections"]
                                        if not (c["map"] == x["mapas"][a]["id"] and c["direction"] == OPOSTA[dr])]

    def c2(x):
        a, b, dr = par
        for c in x["mapas"][a]["connections"]:
            if c["map"] == x["mapas"][b]["id"] and c["direction"] == dr:
                c["offset"] = int(c["offset"]) + 3

    def c3(x):
        x["mapas"][alvo].setdefault("connections", []).append(
            {"map": "MAP_QUE_NAO_EXISTE", "direction": "up", "offset": 0})

    def v1(x):
        x["lays"][x["mapas"][alvo]["layout"]]["width"] = 200

    def e1(x):
        x["mapas"][alvo]["object_events"] = [{}] * (OBJETOS_MAX + 1)

    def e2(x):
        x["mapas"][alvo]["warp_events"] = [{"x": 0, "y": 0, "dest_map": "MAP_QUE_NAO_EXISTE"}] * (WARPS_MAX + 1)

    def e3(x):
        x["mapas"][alvo]["bg_events"] = [{}] * (EVENTOS_MAX + 1)

    def k1(x):
        x["mapas"][alvo]["_g"], x["mapas"][alvo]["_n"] = 127, 127

    def m1(x):
        x["mapas"][unova]["region_map_section"] = "MAPSEC_GALAR_SOUTH"

    def h1(x):
        x["curas"][0]["x"] = 9999

    def f3(x):
        destinos = [x["mapas"][i]["id"] for i in interiores]
        x["mapas"][alvo].setdefault("warp_events", []).extend(
            [{"x": 500, "y": 500, "dest_map": destinos[0], "dest_warp_id": "0"},
             {"x": 501, "y": 500, "dest_map": destinos[1], "dest_warp_id": "0"}])
    return dict(C1=c1, C2=c2, C3=c3, V1=v1, E1=e1, E2=e2, E3=e3, K1=k1, M1=m1, H1=h1, F3=f3)


def demo(d):
    limpos = {chave(*x) for x in portoes(d)}
    falhas = 0
    for regra, planta in mutacoes(d).items():
        x = copy.deepcopy({k: v for k, v in d.items() if k != "blocos"})
        x["blocos"] = d["blocos"]
        x["por_id"] = {m["id"]: m for m in x["mapas"].values()}
        planta(x)
        x["por_id"] = {m["id"]: m for m in x["mapas"].values()}
        novos = [k for k in (chave(*a) for a in portoes(x)) if k not in limpos]
        disparou = any(k.startswith(regra + " ") for k in novos)
        print(f"  {regra}: {'dispara' if disparou else 'NÃO DISPAROU'}  ({len(novos)} achado(s) novo(s))")
        falhas += not disparou
    print("demo:", "ok, os 11 portões disparam com o defeito plantado" if not falhas
          else f"{falhas} portão(ões) cegos")
    return falhas


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--raiz", default=RAIZ)
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--lista", action="store_true")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--grava-base", action="store_true")
    o = ap.parse_args()

    d = carrega(o.raiz)
    if o.demo:
        sys.exit(1 if demo(d) else 0)
    ach = portoes(d)
    chaves = sorted({chave(*x) for x in ach})
    cont = collections.Counter(r for r, *_ in ach)
    for linha in folga(d):
        print(linha)
    print("achados:", ", ".join(f"{r} {cont.get(r, 0)}" for r in REGRAS))

    if o.grava_base:
        json.dump({"leia": "Achados aceitos pelo valida_mapa.py. Só muda com --grava-base e motivo no "
                           "commit. Achado fora desta lista reprova o portão.",
                   "achados": chaves}, open(o.base, "w"), ensure_ascii=False, indent=1)
        open(o.base, "a").write("\n")
        print(f"base gravada: {len(chaves)} achados em {os.path.relpath(o.base, o.raiz)}")
        return

    base = set(json.load(open(o.base))["achados"]) if os.path.exists(o.base) else set()
    novos = [k for k in chaves if k not in base]
    resolvidos = sorted(base - set(chaves))
    if o.lista:
        for k in chaves:
            print(("NOVO  " if k in novos else "base  ") + k)
    for k in resolvidos:
        print("resolvido (tire da base com --grava-base): " + k)
    if novos:
        if not o.lista:
            for k in novos:
                print("NOVO  " + k)
        print(f"valida_mapa: {len(novos)} achado(s) NOVO(S) fora da base. REPROVADO.")
        sys.exit(1)
    print(f"valida_mapa: 0 achados novos ({len(chaves)} na base, {len(resolvidos)} resolvidos). OK.")


if __name__ == "__main__":
    main()
