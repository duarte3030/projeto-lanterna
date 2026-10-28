#!/usr/bin/env python3
"""Tira Kanto, Johto, Hoenn e Sinnoh da branch `cartucho-2` (fase 0 do PRD de assets).

    python3 dev_scripts/remove_regioes_cartucho1.py            # relatório, não escreve
    python3 dev_scripts/remove_regioes_cartucho1.py --aplicar  # escreve

O cartucho 2 é Unova e Galar (mais Kalos, Alola e Paldea, que ainda vão entrar).
As quatro regiões do cartucho 1 ocupavam pelo menos 3,98 MB da ROM desta branch
e deixavam 1,11 MB livres. Este script tira o MUNDO delas: mapas, scripts de
mapa, layouts, tilesets, encontros e pontos de cura. Espécie e Dex não saem.

Diferença para a remoção espelhada do master (onda 1 do cartucho 1, 07/09/2026)
-------------------------------------------------------------------------------
Lá, Unova e Galar viraram TÚMULO porque a save do Gui tinha de continuar
abrindo. Aqui o cartucho 2 nunca teve ROM entregue para jogar, então o id de
mapa e o id de layout PODEM andar: o mapa sai do disco de verdade, o grupo
vazio sai de `group_order` e o layout sai de `layouts.json`.

O que fica, e por quê (o "mínimo vital")
-----------------------------------------
O motor é o do Emerald, e o código C e os scripts compartilhados citam mapa das
quatro regiões por constante (`MAP_LITTLEROOT_TOWN`, `MAP_BATTLE_FRONTIER_*`,
`MAP_SECRET_BASE_*`, `MAP_TRADE_CENTER`, ...). Referência pendurada não pode
compilar: o `mapjson` daria a constante de mapa apagado como número de um grupo
FANTASMA (`tools/mapjson/required_map_defines.json`), que nesta branch cairia
em cima de um grupo de Unova. Por isso:

1. A lista de defines fantasmas é ESVAZIADA. Constante de mapa que não existe
   vira erro de build, e não número de outro mapa.
2. Todo mapa das quatro regiões que o código que FICA ainda cita vira TÚMULO:
   o id existe, o cabeçalho existe, a geometria é o layout comum
   `LAYOUT_TOCO_VAGO` (1x1), a MAPSEC é `MAPSEC_NONE`, e não há warp, conexão,
   placa nem gatilho. O código que fica é: todo C e H versionado (sem
   comentário), os `.s` e `.inc` de `data/`, o corpo de `data/event_scripts.s`,
   os mapas de Unova e Galar, e todo script compartilhado alcançável a partir
   deles (ponto fixo por rótulo, como um linker).
3. Túmulo cujo `scripts.inc` é alcançado por esse código (o C chama um rótulo
   dele) guarda o `scripts.inc` e os `object_events` (por causa dos LOCALID_*).
   O resto do túmulo sai.
4. Layout citado por constante (`LAYOUT_*`) pelo código que fica continua na
   tabela, encolhido para a geometria do toco.

O resultado de cada execução vai para `dev_scripts/remocao_cartucho1.json`: a
lista de túmulos com QUEM cita cada um. É a lista que uma limpeza de motor
futura (Battle Frontier, base secreta, concurso, TV) usa para esvaziar.

Idempotente: rodar de novo depois de aplicar não muda nada.
"""
import collections
import json
import os
import re
import shutil
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPS = os.path.join(RAIZ, "data/maps")
FICA = ("Unova_", "Galar_")
CORTADO_POR = "cartucho 2, fase 0 do PRD de assets (28/10/2026): Kanto, Johto, Hoenn e Sinnoh são o cartucho 1"
TOCO = "TocoVago"
TOCO_ID = "LAYOUT_TOCO_VAGO"
# O par de tileset do toco precisa existir em Unova: é o do quarto do jogador.
TOCO_TILESETS = ("gTileset_Building", "gTileset_UnovaPlayersRoom")
RELATORIO = os.path.join(RAIZ, "dev_scripts/remocao_cartucho1.json")

GERADOS = {"include/constants/map_groups.h", "include/constants/map_event_ids.h",
           "include/constants/layouts.h", "src/data/map_group_count.h",
           "src/data/map_popup_names.h"}
TOK = re.compile(r"\b[A-Za-z_]\w*\b")
COM_C = re.compile(r"//[^\n]*|/\*.*?\*/", re.S)
COM_ASM = re.compile(r"@[^\n]*")
INC = re.compile(r'^\s*\.include\s+"(data/(?:scripts|text|maps)/[^"]+)"\s*$')


def le(p):
    return open(os.path.join(RAIZ, p), encoding="utf-8", errors="replace").read()


def grava_json(p, d):
    with open(os.path.join(RAIZ, p), "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")


def fica(m):
    return m.startswith(FICA)


# ----------------------------------------------------------------- leitura
def carrega_mapas():
    g = json.load(open(f"{MAPS}/map_groups.json", encoding="utf-8"))
    mapas = {}
    for k in g["group_order"]:
        for m in g[k]:
            mapas[m] = json.load(open(f"{MAPS}/{m}/map.json", encoding="utf-8"))
    return g, mapas


def tokens_c():
    """{arquivo: tokens} de todo C/H versionado, sem comentário e sem gerado."""
    arqs = subprocess.run(["git", "ls-files", "src", "include"], cwd=RAIZ,
                          capture_output=True, text=True).stdout.split()
    out = {}
    for a in arqs:
        if a.endswith((".c", ".h")) and a not in GERADOS and os.path.exists(os.path.join(RAIZ, a)):
            out[a] = set(TOK.findall(COM_C.sub(" ", le(a))))
    return out


def unidades_asm():
    """Os .include de data/event_scripts.s, o corpo dele e os outros .s/.inc de data/."""
    linhas = le("data/event_scripts.s").splitlines()
    units, corpo = [], []
    for l in linhas:
        m = INC.match(l)
        if m:
            units.append(m.group(1))
        else:
            corpo.append(l)
    rotulo, tok = {}, {}
    for u in units:
        if not os.path.exists(os.path.join(RAIZ, u)):
            continue
        t = COM_ASM.sub("", le(u))
        for m in re.finditer(r"^\s*(\w+)::?", t, re.M):
            rotulo.setdefault(m.group(1), u)
        tok[u] = set(TOK.findall(t))
    raiz = set(TOK.findall(COM_ASM.sub("", "\n".join(corpo))))
    for a in sorted(os.listdir(os.path.join(RAIZ, "data"))):
        if a.endswith((".s", ".inc")) and a != "event_scripts.s":
            raiz |= set(TOK.findall(COM_ASM.sub("", le(f"data/{a}"))))
    return units, rotulo, tok, raiz


# ----------------------------------------------------------------- o ponto fixo
def decide():
    g, mapas = carrega_mapas()
    id_de = {m: d["id"] for m, d in mapas.items()}
    mapa_do_id = {v: k for k, v in id_de.items()}
    sai = {m for m in mapas if not fica(m)}
    tc = tokens_c()
    units, rotulo, utok, raiz_asm = unidades_asm()
    unit_do_mapa = {u.split("/")[2]: u for u in units if u.startswith("data/maps/")}

    raiz_tok = set(raiz_asm)
    for t in tc.values():
        raiz_tok |= t
    alcanca = {unit_do_mapa[m] for m in mapas if fica(m) and m in unit_do_mapa}
    json_tok = set()
    for m in mapas:
        if fica(m):
            json_tok |= set(TOK.findall(json.dumps(mapas[m])))
    tumulos_com_objetos = set()
    while True:
        base = raiz_tok | json_tok
        for m in tumulos_com_objetos:
            base |= set(TOK.findall(json.dumps(mapas[m]["object_events"])))
        reach = set(alcanca) | {rotulo[t] for t in base if t in rotulo}
        fila = list(reach)
        while fila:
            u = fila.pop()
            for t in utok.get(u, ()):
                v = rotulo.get(t)
                if v and v not in reach:
                    reach.add(v)
                    fila.append(v)
        todos = set(base)
        for u in reach:
            todos |= utok.get(u, set())
        script_vivo = {u.split("/")[2] for u in reach if u.startswith("data/maps/")} & sai
        # LOCALID_* nasce do `local_id` dos object_events (map_event_ids.h,
        # gerado). Se o código que fica cita o LOCALID de um mapa que sai
        # (src/contest_util.c cita LOCALID_CONTESTANT_1..4), o túmulo guarda
        # os objetos, senão a constante some e o build quebra.
        localid = {m for m in sai if any(o.get("local_id") in todos for o in mapas[m].get("object_events") or [])}
        # Ponto de cura citado pelo código prende o mapa dele como túmulo.
        cura = set()
        for h in json.loads(le("src/data/heal_locations.json"))["heal_locations"]:
            if h["id"] in todos:
                cura |= {mapa_do_id[x] for x in (h["map"], h.get("respawn_map")) if x in mapa_do_id and mapa_do_id[x] in sai}
        # Túmulo que só guarda objetos por LOCALID fica com os objetos, mas sem
        # script nem flag (ver aplica): os scripts deles não entram no
        # alcance, senão cada túmulo puxaria o próprio scripts.inc em cascata.
        tumulos = ({mapa_do_id[t] for t in todos if t in mapa_do_id and mapa_do_id[t] in sai}
                   | script_vivo | localid | cura)
        if script_vivo <= tumulos_com_objetos:
            break
        tumulos_com_objetos |= script_vivo

    # quem cita cada túmulo (para o relatório e para a limpeza de motor futura)
    quem = collections.defaultdict(set)
    for a, t in tc.items():
        for x in t:
            if x in mapa_do_id and mapa_do_id[x] in tumulos:
                quem[mapa_do_id[x]].add(a)
    for u in reach:
        for x in utok.get(u, ()):
            if x in mapa_do_id and mapa_do_id[x] in tumulos and not u.endswith(f"/{mapa_do_id[x]}/scripts.inc"):
                quem[mapa_do_id[x]].add(u)
    for m in script_vivo:
        quem[m].add("(o scripts.inc dele é chamado por código que fica)")
    for m in localid:
        quem[m].add("(o código que fica cita LOCALID_* de objeto dele)")
    for m in cura:
        quem[m].add("(ponto de cura citado pelo código que fica)")
    return dict(g=g, mapas=mapas, sai=sai, tumulos=tumulos, script_vivo=script_vivo,
                com_obj=tumulos_com_objetos | localid,
                so_localid=localid - tumulos_com_objetos,
                reach=reach, units=units, todos=todos, quem=quem, unit_do_mapa=unit_do_mapa)


# ----------------------------------------------------------------- escrita
def poda_tabela_de_voo(sai_ids, aplicar):
    """src/region_map.c: as linhas de sMapHealLocations das quatro regiões saem.

    A tabela é indexada por MAPSEC com inicializador designado, então tirar a
    linha deixa a entrada zerada (HEAL_LOCATION_NONE), que é o que o mapa de voo
    já trata como "sem voo". Sem isto, uma tabela de VOO de Hoenn e Kanto
    seguraria ~90 mapas e ~90 pontos de cura como túmulo.
    """
    p = "src/region_map.c"
    t = le(p)
    linhas = t.split("\n")
    novo, tirou = [], 0
    for l in linhas:
        m = re.match(r"\s*\[MAPSEC_\w+\]\s*=\s*\{MAP_GROUP\((MAP_\w+)\)", l)
        if m and m.group(1) in sai_ids:
            tirou += 1
            continue
        novo.append(l)
    # Com todas as linhas fora, a tabela ficaria `[][3] = {}` (tamanho zero) e
    # o -Warray-bounds quebra o build. O tamanho explícito MAPSEC_COUNT mantém
    # o comportamento: toda entrada não listada já era zero.
    t2 = "\n".join(novo).replace("static const u8 sMapHealLocations[][3] =",
                                  "static const u8 sMapHealLocations[MAPSEC_COUNT][3] =")
    if tirou and aplicar:
        open(os.path.join(RAIZ, p), "w", encoding="utf-8").write(t2)
    return tirou


def esvazia_defines_fantasmas(aplicar):
    p = "tools/mapjson/required_map_defines.json"
    d = json.loads(le(p))
    n = (len(d.get("required_maps", [])), len(d.get("required_layouts", [])))
    if aplicar and any(n):
        grava_json(p, {"required_maps": [], "required_layouts": []})
    return n


def aplica(D, aplicar):
    g, mapas, sai, tumulos = D["g"], D["mapas"], D["sai"], D["tumulos"]
    apagados = sorted(sai - tumulos)
    res = collections.OrderedDict()

    # 1. pastas de mapa
    for m in apagados:
        if aplicar:
            shutil.rmtree(f"{MAPS}/{m}")
    res["mapas apagados"] = len(apagados)

    # 2. túmulos
    stub = 0
    for m in sorted(tumulos):
        d = mapas[m]
        novo = dict(d)
        novo["layout"] = TOCO_ID
        novo["region_map_section"] = "MAPSEC_NONE"
        novo["connections"] = None
        if m not in D["com_obj"]:
            novo["object_events"] = []
        elif m in D["so_localid"]:
            # só a posição na lista importa (ela vira o LOCALID); o objeto
            # não tem mais script, flag nem visão de treinador.
            for o in novo["object_events"]:
                if "script" in o:
                    o["script"] = "0x0"
                if "flag" in o:
                    o["flag"] = "0"
                if "trainer_type" in o:
                    o["trainer_type"] = "TRAINER_TYPE_NONE"
                    o["trainer_sight_or_berry_tree_id"] = "0"
        novo["warp_events"] = []
        novo["coord_events"] = []
        novo["bg_events"] = []
        for k in ("destinos_dinamicos", "map_name_popup", "shared_events_map", "shared_scripts_map"):
            novo.pop(k, None)
        novo["cortado_por"] = CORTADO_POR
        if aplicar:
            grava_json(f"data/maps/{m}/map.json", novo)
        if m not in D["script_vivo"]:
            stub += 1
            if aplicar:
                open(f"{MAPS}/{m}/scripts.inc", "w", encoding="utf-8").write(
                    "@ TÚMULO: mapa do cartucho 1 que o motor ainda cita por constante\n"
                    "@ (dev_scripts/remove_regioes_cartucho1.py). O rótulo abaixo fica\n"
                    "@ porque header.inc, gerado, aponta para ele.\n\n"
                    f"{m}_MapScripts::\n\t.byte 0\n")
    res["túmulos"] = len(tumulos)
    res["túmulos com scripts.inc vivo"] = len(D["script_vivo"])
    res["túmulos que guardam objetos (LOCALID ou script)"] = len(D["com_obj"])

    # 3. map_groups.json: tira os apagados, e grupo vazio sai da ordem
    ng = {"group_order": []}
    vazios = []
    for k in g["group_order"]:
        lst = [m for m in g[k] if m in mapas and (fica(m) or m in tumulos)]
        if lst:
            ng["group_order"].append(k)
            ng[k] = lst
        else:
            vazios.append(k)
    for k, v in g.items():
        if k != "group_order" and k not in ng and k not in vazios and k not in g["group_order"]:
            ng[k] = v
    res["grupos"] = f"{len(g['group_order'])} -> {len(ng['group_order'])}"
    if aplicar:
        grava_json("data/maps/map_groups.json", ng)

    # 4. event_scripts.s: só fica o que é alcançado, mais o stub de cada túmulo
    vivos = set(D["reach"]) | {f"data/maps/{m}/scripts.inc" for m in tumulos}
    linhas = le("data/event_scripts.s").split("\n")
    novo, tiradas, arquivos = [], 0, []
    for l in linhas:
        mm = INC.match(l)
        if mm and mm.group(1) not in vivos:
            tiradas += 1
            if not mm.group(1).startswith("data/maps/"):
                arquivos.append(mm.group(1))
            continue
        novo.append(l)
    res["includes tirados de event_scripts.s"] = tiradas
    res["scripts e textos compartilhados apagados"] = sorted(arquivos)
    if aplicar:
        open(os.path.join(RAIZ, "data/event_scripts.s"), "w", encoding="utf-8").write("\n".join(novo))
        for a in arquivos:
            os.remove(os.path.join(RAIZ, a))

    # 5. layouts
    restantes = {m: mapas[m] for m in mapas if fica(m) or m in tumulos}
    usados = {d["layout"] for m, d in restantes.items() if m not in tumulos}
    citados = {t for t in D["todos"] if t.startswith("LAYOUT_")}
    L = json.loads(le("data/layouts/layouts.json"))
    nl, tirados, encolhidos = [], 0, []
    for x in L["layouts"]:
        i = x.get("id")
        if i == TOCO_ID:
            continue
        if i in usados:
            nl.append(x)
        elif i in citados:
            y = dict(x)
            y.update(width=1, height=1, primary_tileset=TOCO_TILESETS[0], secondary_tileset=TOCO_TILESETS[1],
                     border_filepath=f"data/layouts/{TOCO}/border.bin",
                     blockdata_filepath=f"data/layouts/{TOCO}/map.bin")
            nl.append(y)
            encolhidos.append(i)
        else:
            tirados += 1
    nl.append({"id": TOCO_ID, "name": f"{TOCO}_Layout", "width": 1, "height": 1,
               "primary_tileset": TOCO_TILESETS[0], "secondary_tileset": TOCO_TILESETS[1],
               "border_filepath": f"data/layouts/{TOCO}/border.bin",
               "blockdata_filepath": f"data/layouts/{TOCO}/map.bin", "layout_version": "emerald"})
    vivos_bin = {x[k] for x in nl for k in ("border_filepath", "blockdata_filepath")}
    apaga_bin = sorted({x[k] for x in L["layouts"] for k in ("border_filepath", "blockdata_filepath")
                        if x.get(k)} - vivos_bin)
    res["layouts"] = f"{len(L['layouts'])} -> {len(nl)} ({tirados} apagados, {len(encolhidos)} citados por constante e encolhidos)"
    res["arquivos de geometria apagados"] = len(apaga_bin)
    if aplicar:
        os.makedirs(os.path.join(RAIZ, f"data/layouts/{TOCO}"), exist_ok=True)
        open(os.path.join(RAIZ, f"data/layouts/{TOCO}/border.bin"), "wb").write(b"\x01\x00" * 4)
        open(os.path.join(RAIZ, f"data/layouts/{TOCO}/map.bin"), "wb").write(b"\x01\x00")
        L["layouts"] = nl
        grava_json("data/layouts/layouts.json", L)
        for p in apaga_bin:
            if os.path.exists(os.path.join(RAIZ, p)):
                os.remove(os.path.join(RAIZ, p))
        for dp in sorted({os.path.dirname(p) for p in apaga_bin}):
            ap = os.path.join(RAIZ, dp)
            if os.path.isdir(ap) and not os.listdir(ap):
                os.rmdir(ap)

    # 6. encontros: tabela de mapa que não fica sai (túmulo não tem mato)
    W = json.loads(le("src/data/wild_encounters.json"))
    ids_vivos = {d["id"] for m, d in restantes.items() if m not in tumulos}
    tirou = 0
    for grp in W["wild_encounter_groups"]:
        if not grp.get("for_maps"):
            continue
        antes = len(grp["encounters"])
        grp["encounters"] = [e for e in grp["encounters"]
                             if e.get("map") in ids_vivos or e.get("base_label") in D["todos"]]
        tirou += antes - len(grp["encounters"])
    res["tabelas de encontro tiradas"] = tirou
    if aplicar:
        grava_json("src/data/wild_encounters.json", W)

    # 7. pontos de cura
    H = json.loads(le("src/data/heal_locations.json"))
    ids_rest = {d["id"] for d in restantes.values()}
    fora, presos = [], []
    nh = []
    for h in H["heal_locations"]:
        if h["map"] in ids_vivos:
            nh.append(h)
        elif h["id"] in D["todos"]:
            presos.append(h["id"])
            if h["map"] in ids_rest:
                h2 = {k: v for k, v in h.items() if k not in ("respawn_map", "respawn_npc")}
                h2["x"], h2["y"] = 0, 0
                nh.append(h2)
        else:
            fora.append(h["id"])
    res["pontos de cura"] = f"{len(H['heal_locations'])} -> {len(nh)}"
    res["pontos de cura citados pelo código e presos em túmulo"] = presos
    if aplicar:
        H["heal_locations"] = nh
        grava_json("src/data/heal_locations.json", H)
    return res


DECL = re.compile(r"^(?:extern )?const (?:u8|u16|u32) (?:ALIGNED\(4\) )?(\w+)\[", re.M)


def _declaracoes(texto):
    """Quebra graphics.h / metatiles.h em declarações de topo.

    `extern const ... ASSET_ALIAS(x)` é declaração também (dedupe_assets.py):
    um tileset que fica pode ser APELIDO da arte de um que sai, e apagar o dono
    do símbolo quebraria o apelido. Por isso cada parte guarda de quem depende.
    """
    partes = re.split(r"(?=^(?:extern )?const )", texto, flags=re.M)
    out = []
    for pt in partes:
        m = DECL.match(pt)
        deps = set(re.findall(r"(?:ASSET_ALIAS|ARRAY_COUNT)\((\w+)\)", pt))
        out.append((m.group(1) if m else None, deps, pt))
    return out


def tilesets(aplicar):
    """Tileset que nenhum layout restante usa e que o C não cita sai da ROM."""
    L = json.loads(le("data/layouts/layouts.json"))
    usados = {x.get(k) for x in L["layouts"] for k in ("primary_tileset", "secondary_tileset")}
    tc = tokens_c()
    PREFIXOS = ("gTileset_", "gTilesetTiles_", "gTilesetPalettes_", "gMetatiles_", "gMetatileAttributes_")
    citados = set()
    for a, t in tc.items():
        if not a.startswith("src/data/tilesets/") and a != "include/tilesets.h":
            citados |= {x for x in t if x.startswith(PREFIXOS)}
    hdr = le("src/data/tilesets/headers.h")
    blocos = {m.group(1): m.group(0) for m in
              re.finditer(r"const struct Tileset gTileset_(\w+) =\s*\{.*?\};", hdr, re.S)}
    # Fora dos blocos, headers.h também cita tileset: gTilesetPointer_SecretBase
    # aponta para gTileset_SecretBase, que decoration.c (motor) usa.
    resto = hdr
    for b in blocos.values():
        resto = resto.replace(b, "")
    citados |= {x for x in re.findall(r"\w+", resto) if x.startswith(PREFIXOS)}
    sai = sorted(n for n in blocos if f"gTileset_{n}" not in usados and f"gTileset_{n}" not in citados)
    campos = lambda b: set(re.findall(r"\.(?:tiles|palettes|metatiles|metatileAttributes)\s*=\s*(\w+)", b))
    # o que FICA: campos dos tilesets que ficam, mais o que o C cita, fechado por apelido
    fica_sim = set(citados)
    for n, b in blocos.items():
        if n not in sai:
            fica_sim |= campos(b)
    textos = {p: le(p) for p in ("src/data/tilesets/graphics.h", "src/data/tilesets/metatiles.h")}
    decl = {p: _declaracoes(t) for p, t in textos.items()}
    deps = {}
    for p in decl:
        for nome, d, _ in decl[p]:
            if nome:
                deps[nome] = d
    fila = list(fica_sim)
    while fila:
        x = fila.pop()
        for y in deps.get(x, ()):
            if y not in fica_sim:
                fica_sim.add(y)
                fila.append(y)
    candidatos = set()
    for n in sai:
        candidatos |= campos(blocos[n])
    simbolos = {x for x in candidatos if x not in fica_sim}
    caminhos_fora, caminhos_vivos = set(), set()
    # Caminho citado por QUALQUER outro arquivo de código continua vivo: os
    # quadros de animação moram em src/tileset_anims.c e src/data/tilesets/
    # anims_unova.h, e apagar a pasta do tileset levaria a pasta anim/ junto.
    # O que o tileset apagado deixa de usar ali o --gc-sections do linker tira.
    for a in subprocess.run(["git", "ls-files", "src", "include"], cwd=RAIZ,
                            capture_output=True, text=True).stdout.split():
        if a.endswith((".c", ".h")) and a not in textos and os.path.exists(os.path.join(RAIZ, a)):
            caminhos_vivos |= set(re.findall(r'"(data/tilesets/[^"]+)"', le(a)))
    novos = {}
    for p, ds in decl.items():
        corpo = []
        for nome, d, pt in ds:
            refs = set(re.findall(r'"(data/tilesets/[^"]+)"', pt))
            if nome in simbolos:
                caminhos_fora |= refs
                continue
            caminhos_vivos |= refs
            corpo.append(pt)
        novos[p] = re.sub(r"\n{3,}", "\n\n", "".join(corpo))
    novo_hdr = hdr
    for n in sai:
        novo_hdr = novo_hdr.replace(blocos[n], "")
    novo_hdr = re.sub(r"\n{3,}", "\n\n", novo_hdr)
    inc = le("include/tilesets.h")
    for n in sai:
        inc = re.sub(rf"\nextern const struct Tileset gTileset_{n};[^\n]*", "", inc)
    for x in simbolos:
        inc = re.sub(rf"\nextern const \w+ (?:ALIGNED\(4\) )?{x}\[\](?:\[16\])?;[^\n]*", "", inc)
    def base(c):
        return re.sub(r"\.(4bpp|8bpp|gbapal|lz|smol|fastSmol|smolTM)(\.\w+)*$", "", c)
    vivos_base = {base(c) for c in caminhos_vivos}
    fora = {base(c) for c in caminhos_fora} - vivos_base
    apagados = 0
    if aplicar:
        for p, t in novos.items():
            open(os.path.join(RAIZ, p), "w", encoding="utf-8").write(t)
        open(os.path.join(RAIZ, "src/data/tilesets/headers.h"), "w", encoding="utf-8").write(novo_hdr)
        open(os.path.join(RAIZ, "include/tilesets.h"), "w", encoding="utf-8").write(inc)
        pastas = set()
        for b in fora:
            for ext in ("", ".png", ".pal", ".bin"):
                ap = os.path.join(RAIZ, b + ext)
                if os.path.isfile(ap):
                    os.remove(ap)
                    apagados += 1
                    pastas.add(os.path.dirname(ap))
        # pasta que ficou só com resto (sem nenhum caminho vivo dentro) sai inteira
        raiz_ts = os.path.join(RAIZ, "data/tilesets")
        vivos_abs = [os.path.join(RAIZ, c) for c in caminhos_vivos] + [os.path.join(RAIZ, b) for b in vivos_base]
        for pasta in sorted(pastas, key=len, reverse=True):
            while pasta.startswith(raiz_ts + os.sep) and os.path.dirname(pasta) not in (
                    raiz_ts, os.path.join(raiz_ts, "primary"), os.path.join(raiz_ts, "secondary")):
                pasta = os.path.dirname(pasta)
            if os.path.isdir(pasta) and not any(v.startswith(pasta + os.sep) for v in vivos_abs):
                shutil.rmtree(pasta)
    return sai, len(simbolos), apagados


def orfaos_sem_layout(aplicar):
    """Pastas de mapa fora de map_groups.json (o Makefile compila todo
    map.json por curinga) cujo layout saiu. As 4 de hoje são casas não usadas
    de Kanto (Route6/19/23, SevenIsland); sem layout, o mapjson falha."""
    import shutil
    g = json.loads(le(f"{MAPS}/map_groups.json"))
    em = {m for k in g["group_order"] for m in g[k]}
    lay = {l["id"] for l in json.loads(le("data/layouts/layouts.json"))["layouts"] if "id" in l}
    fora = []
    for d in sorted(os.listdir(MAPS)):
        p = f"{MAPS}/{d}/map.json"
        if d in em or not os.path.exists(p):
            continue
        if json.loads(le(p)).get("layout") not in lay:
            fora.append(d)
            if aplicar:
                shutil.rmtree(f"{MAPS}/{d}")
    return fora


def main():
    aplicar = "--aplicar" in sys.argv
    g, mapas = carrega_mapas()
    sai_ids = {d["id"] for m, d in mapas.items() if not fica(m)}
    n_voo = poda_tabela_de_voo(sai_ids, aplicar)
    fant = esvazia_defines_fantasmas(aplicar)
    D = decide()
    res = aplica(D, aplicar)
    res["linhas tiradas da tabela de voo (region_map.c)"] = n_voo
    res["defines fantasmas esvaziados (mapas, layouts)"] = fant
    if aplicar:
        ts, ns, na = tilesets(True)
        res["tilesets apagados"] = len(ts)
        res["símbolos de arte de tileset apagados"] = ns
        res["arquivos de tileset apagados"] = na
        res["pastas órfãs (fora de grupo) sem layout apagadas"] = orfaos_sem_layout(True)
    for k, v in res.items():
        if isinstance(v, list) and len(v) > 12:
            print(f"{k}: {len(v)} ({', '.join(v[:12])}, ...)")
        else:
            print(f"{k}: {v}")
    rel = {
        "gerado_por": "dev_scripts/remove_regioes_cartucho1.py",
        "tumulos": {m: sorted(D["quem"].get(m, [])) for m in sorted(D["tumulos"])},
        "tumulos_com_scripts_vivo": sorted(D["script_vivo"]),
        "tumulos_com_objetos": sorted(D["com_obj"]),
        "resumo": {k: v for k, v in res.items()},
    }
    if aplicar:
        grava_json("dev_scripts/remocao_cartucho1.json", rel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
