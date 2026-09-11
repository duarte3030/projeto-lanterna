#!/usr/bin/env python3
"""Copia UM mapa inteiro de uma ROM hack de base FireRed para dentro do repo.

Por que existe
--------------
O `fontes-mapas/romhacks/ferramentas/extrai_tileset.py` traz a ARTE de um
tileset, e o `instala_tileset.py` a declara no jogo. Nenhum dos dois traz o
MAPA: a planta (`map.bin`), a borda (`border.bin`), o tamanho, o par de
tilesets e a entrada em `layouts.json` continuavam sendo trabalho manual, e
trabalho manual em cima de ponteiro cru e exatamente onde se erra calado.

Este script fecha esse buraco. Ele le o cabecalho de mapa da ROM hack, copia a
planta BYTE A BYTE e deixa o mapa registrado no repo, pronto para receber o
JOGO que e NOSSO (warps, NPCs, encontros, treinadores, placas). Nada de script,
NPC, item ou gatilho do hack entra: o `map.json` que ele grava tem as quatro
listas de evento VAZIAS, de proposito.

O que ele NAO faz, e e proposital
---------------------------------
- Nao inventa desenho. `map.bin` e `border.bin` sao copia crua do hack.
- Nao copia evento nenhum do hack (regra 1.2 do METODO-COPIA-CIDADES.md).
- Nao mexe em mapa que ja existe. Mapa novo entra sempre no FIM do grupo
  (regra 7 do metodo), e layout novo no FIM de `layouts.json`.
- Nao escolhe o par de tilesets do repo por adivinhacao: ou voce passa
  `--ts-pri-existente`/`--ts-sec-existente` com um rotulo que ja existe, ou ele
  importa o tileset do hack com o rotulo que voce der.

O formato, medido e nao lembrado
--------------------------------
FireRed (`BPRE`), `struct MapLayout`, 0x1C bytes:

    0x00 s32 width
    0x04 s32 height
    0x08 ptr border
    0x0C ptr map (blockdata)
    0x10 ptr primaryTileset
    0x14 ptr secondaryTileset
    0x18 u8  borderWidth
    0x19 u8  borderHeight
    0x1A u16 padding

O nosso `struct MapLayout` (include/global.fieldmap.h) tem os mesmos seis
primeiros campos, depois `isFrlg`, `borderWidth`, `borderHeight`, `bigPrimary`.
O `tools/mapjson` emite `borderWidth`/`borderHeight` SO quando
`layout_version == "frlg"`; em `emerald` e `johto` ele emite `.2byte 0`, ou
seja borda 2x2 fixa. Por isso um mapa de FireRed com borda 3x2 (existe: a
floresta do Safari do Liquid Crystal e uma) SO cabe como `frlg`.

O bloco de 16 bits do blockdata e igual nas duas bases (metatile 0-9, colisao
10-11, elevacao 12-15), entao a planta copia sem conversao. O que NAO e igual:

- a fronteira de VRAM. FireRed usa 640 tiles / 640 metatiles / 7 paletas no
  primario; Emerald usa 512/512/6. Um mapa de FireRed so desenha certo se o
  layout for `frlg` (isFrlg) ou `johto` (bigPrimary), que e o que
  `GetNumMetatilesInPrimary` (src/fieldmap.c:438) le.
- o atributo de metatile. FireRed usa 4 bytes por metatile (behavior 0-8,
  terreno 9-13, encounter 24-26, camada 29-30); Emerald usa 2 (behavior 0-7,
  camada 12-15). `GetAttributeByMetatileIdAndMapLayout` escolhe pelo `isFrlg`.
  **Com `--attr 4` + `layout_version frlg` nao ha conversao e nao ha perda**, e
  esse e o padrao: e o mesmo caminho dos 64 tilesets `*_frlg` que o repo ja
  tem. Com `--attr 2` o script converte e AVISA o que perdeu (terreno e
  encounter somem, behavior >= 256 nao cabe), e ai o layout vira `johto`.

Uso
---
    copia_mapa_rom.py --rom liquid-crystal --grupo 5 --mapa 113 \
        --nome LcSafariMountain \
        --ts-pri LcOutdoor --ts-sec LcSafari \
        --grupo-alvo gMapGroup_Dungeons_Johto \
        --mapsec MAPSEC_SAFARI_ZONE --popup "SAFARI ZONE" \
        --musica MUS_HG_SAFARI_ZONE --tipo MAP_TYPE_ROUTE

    copia_mapa_rom.py --autoteste          # provas das funcoes puras
    copia_mapa_rom.py ... --demo           # diz tudo que faria, escreve zero
    copia_mapa_rom.py ... --prova-render X.png   # prova de fidelidade
"""
import argparse
import collections
import json
import os
import re
import struct
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FERR = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/romhacks/ferramentas"
sys.path.insert(0, FERR)

# Teto do motor: sBackupMapData tem MAX_MAP_DATA_SIZE entradas e
# InitMapLayoutData (src/fieldmap.c:180) monta (width + MAP_OFFSET_W) por
# (height + MAP_OFFSET_H). Mapa que estoura isso carrega com o fundo todo
# MAPGRID_UNDEFINED, ou seja tela preta andavel, sem erro nenhum no build.
MAX_MAP_DATA_SIZE = 10240
MAP_OFFSET_W = 15
MAP_OFFSET_H = 14

# Fronteiras de VRAM, de include/fieldmap.h
SPLIT_FRLG = 640
SPLIT_EMERALD = 512
NUM_METATILES_TOTAL = 1024


# --------------------------------------------------------------- funcoes puras

def cabe_na_memoria(w, h):
    """(w + 15) * (h + 14) <= 10240, a conta que o InitMapLayoutData faz."""
    return (w + MAP_OFFSET_W) * (h + MAP_OFFSET_H) <= MAX_MAP_DATA_SIZE


def censo_blocos(blob, w, h):
    """Le o blockdata e devolve o que precisa ser conferido antes de copiar.

    Cada bloco e u16: metatile nos bits 0-9, colisao em 10-11, elevacao em
    12-15. Identico em FireRed e Emerald: por isso a planta copia crua.
    """
    if len(blob) != w * h * 2:
        raise ValueError("blockdata com %d bytes, esperava %d" % (len(blob), w * h * 2))
    palavras = struct.unpack("<%dH" % (w * h), blob)
    metatiles = [p & 0x3FF for p in palavras]
    return {
        "n": len(palavras),
        "max_metatile": max(metatiles),
        "min_metatile": min(metatiles),
        "distintos": len(set(metatiles)),
        "colisao": dict(collections.Counter((p >> 10) & 3 for p in palavras)),
        "elevacao": dict(collections.Counter(p >> 12 for p in palavras)),
    }


def id_layout(nome):
    """LcSafariMountain -> LAYOUT_LC_SAFARI_MOUNTAIN."""
    return "LAYOUT_" + re.sub(r"(?<!^)(?=[A-Z])", "_", nome).upper()


def id_mapa(nome):
    """LcSafariMountain -> MAP_LC_SAFARI_MOUNTAIN."""
    return "MAP_" + re.sub(r"(?<!^)(?=[A-Z])", "_", nome).upper()


def snake(nome):
    return re.sub(r"[^a-z0-9_]", "_", re.sub(r"(?<!^)(?=[A-Z])", "_", nome).lower())


# ------------------------------------------------------------------ leitura da ROM

def acha_rom(alvo):
    if os.path.isfile(alvo):
        return alvo
    pasta = os.path.join(os.path.dirname(FERR), alvo)
    if os.path.isdir(pasta):
        gbas = [f for f in sorted(os.listdir(pasta)) if f.lower().endswith(".gba")]
        if gbas:
            return os.path.join(pasta, gbas[0])
    print("ERRO: nao achei ROM para '%s'" % alvo, file=sys.stderr)
    sys.exit(1)


def le_cabecalho(rom, gmg, grupo, mapa):
    """Cabecalho de mapa em (grupo, mapa), com a borda que o gbamap nao le.

    O `gbamap.parse_layout` para nos seis ponteiros; borderWidth e borderHeight
    moram em 0x18 e 0x19 e sao justamente o que decide se o layout pode ser
    `frlg` ou nao.
    """
    base_ptr = rom.u32(gmg + grupo * 4)
    if not rom.valido(base_ptr):
        raise ValueError("grupo %d nao existe em gMapGroups 0x%06X" % (grupo, gmg))
    p = rom.u32(rom.deref(base_ptr) + mapa * 4)
    if not rom.valido(p):
        raise ValueError("mapa %d do grupo %d nao aponta para cabecalho" % (mapa, grupo))
    h = rom.parse_header(rom.deref(p))
    if h is None:
        raise ValueError("g%dm%d nao parseia como cabecalho de mapa" % (grupo, mapa))
    lo = h["layout"]["off"]
    h["layout"]["border_w"] = rom.rom[lo + 0x18]
    h["layout"]["border_h"] = rom.rom[lo + 0x19]
    return h


# ------------------------------------------------------------------- a copia

MAPJSON_MODELO = {
    "id": None,
    "name": None,
    "layout": None,
    "music": "MUS_ROUTE118",
    "region": "REGION_HOENN",
    "region_map_section": "MAPSEC_NONE",
    "requires_flash": False,
    "weather": "WEATHER_NONE",
    "map_type": "MAP_TYPE_ROUTE",
    "allow_cycling": False,
    "allow_escaping": False,
    "allow_running": False,
    "show_map_name": True,
    "battle_scene": "MAP_BATTLE_SCENE_NORMAL",
    "connections": None,
    "object_events": [],
    "warp_events": [],
    "coord_events": [],
    "bg_events": [],
}

SCRIPTS_MODELO = """@ %(nome)s: mapa copiado de %(hack)s (g%(g)dm%(m)d) por
@ dev_scripts/copia_mapa_rom.py. A ARTE e do hack; o JOGO (warps, NPCs,
@ encontros, treinadores, placas) e nosso e entra aqui.

%(nome)s_MapScripts::
\t.byte 0
"""


def copia(a):
    from gbamap import Rom
    import extrai_tileset as ET
    sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
    import comportamento_frlg as CF

    caminho = acha_rom(a.rom)
    rom = Rom(caminho)
    frlg = rom.frlg
    gmg = int(a.gmg, 16) if a.gmg else None
    if gmg is None:
        gmg, como = rom.acha_mapgroups()
        if gmg is None:
            print("ERRO: nao achei gMapGroups. Passe --gmg.", file=sys.stderr)
            sys.exit(1)
    else:
        como = "--gmg"

    h = le_cabecalho(rom, gmg, a.grupo, a.mapa)
    L = h["layout"]
    w, hh, bw, bh = L["w"], L["h"], L["border_w"], L["border_h"]

    print("FONTE  %s (%s), gMapGroups 0x%06X (%s)" % (os.path.basename(caminho), rom.code, gmg, como))
    print("  g%dm%d  %dx%d  borda %dx%d  ts1=0x%06X ts2=0x%06X  layout=0x%06X blockdata=0x%06X"
          % (a.grupo, a.mapa, w, hh, bw, bh, L["ts1"], L["ts2"], L["off"], L["blockdata"]))

    # --- PROVA NEGATIVA 1: o mapa cabe no motor?
    if not cabe_na_memoria(w, hh):
        print("ERRO: (%d+%d)*(%d+%d) = %d passa de MAX_MAP_DATA_SIZE %d. O mapa carregaria "
              "com o fundo inteiro MAPGRID_UNDEFINED, sem erro nenhum no build."
              % (w, MAP_OFFSET_W, hh, MAP_OFFSET_H, (w + MAP_OFFSET_W) * (hh + MAP_OFFSET_H),
                 MAX_MAP_DATA_SIZE), file=sys.stderr)
        sys.exit(1)
    print("  memoria: (%d+15)*(%d+14) = %d de %d  OK"
          % (w, hh, (w + MAP_OFFSET_W) * (hh + MAP_OFFSET_H), MAX_MAP_DATA_SIZE))

    # --- PROVA NEGATIVA 2: borda 3x2 so existe em layout frlg
    attr_bytes = int(a.attr)
    versao = "frlg" if attr_bytes == 4 else ("johto" if frlg else "emerald")
    if (bw, bh) != (2, 2) and versao != "frlg":
        print("ERRO: borda %dx%d e o tools/mapjson so emite borderWidth/Height em "
              "layout_version frlg. Com --attr 2 a borda viraria 2x2 calada." % (bw, bh),
              file=sys.stderr)
        sys.exit(1)

    # --- planta e borda, copia crua
    blob = rom.rom[L["blockdata"]:L["blockdata"] + w * hh * 2]
    borda = rom.rom[L["border"]:L["border"] + bw * bh * 2]
    censo = censo_blocos(blob, w, hh)
    print("  blocos: %d, %d metatiles distintos, maior id %d, colisao %s, elevacao %s"
          % (censo["n"], censo["distintos"], censo["max_metatile"],
             censo["colisao"], censo["elevacao"]))

    split = SPLIT_FRLG if frlg else SPLIT_EMERALD
    n_sec = NUM_METATILES_TOTAL - split
    if censo["max_metatile"] >= NUM_METATILES_TOTAL:
        print("ERRO: metatile %d >= %d." % (censo["max_metatile"], NUM_METATILES_TOTAL), file=sys.stderr)
        sys.exit(1)

    nome = a.nome
    lay_id = a.layout_id or id_layout(nome)
    map_id = id_mapa(nome)
    rel_layout = "data/layouts/%s" % nome
    rel_mapa = "data/maps/%s" % nome

    # --- tilesets
    pri_label = a.ts_pri_existente or a.ts_pri
    sec_label = a.ts_sec_existente or a.ts_sec
    if not pri_label or not sec_label:
        print("ERRO: preciso de --ts-pri/--ts-sec (importar do hack) ou "
              "--ts-pri-existente/--ts-sec-existente (reusar rotulo do repo).", file=sys.stderr)
        sys.exit(1)

    acoes = []
    a_importar = []
    if a.ts_pri:
        a_importar.append((a.ts_pri, L["ts1"], False))
    if a.ts_sec:
        a_importar.append((a.ts_sec, L["ts2"], True))

    for label, off, secundario in a_importar:
        lado = "secondary" if secundario else "primary"
        destino = os.path.join(RAIZ, "data/tilesets/%s/%s" % (lado, snake(label)))
        if os.path.isdir(destino):
            acoes.append("tileset %s ja existe em disco, nao reimporto" % label)
            continue
        acoes.append("importar tileset 0x%06X -> %s (%s)" % (off, label, lado))
        if a.demo:
            continue
        tmp = os.path.join("/tmp", "copia_mapa_%s_%s" % (os.getpid(), snake(label)))
        ET.extrai(caminho, off, tmp, secundario, label, split, str(attr_bytes))
        # O comportamento de metatile do FireRed NAO quer dizer a mesma coisa que
        # o nosso a partir de 0x10, e o FireRed decide encontro selvagem pelo
        # ATRIBUTO, que o nosso motor nao le. Sem esta passada, escada de pedra
        # vira agua e a grama do hack nao gera Pokemon nenhum, tudo isso com
        # build verde e render identico. Motivo completo em comportamento_frlg.py.
        # Roda AQUI, na pasta extraida em /tmp, porque a traducao nao e
        # idempotente: cada import comeca da ROM e passa por ela uma vez so.
        if attr_bytes == 4 and not a.sem_comportamento:
            alvo = os.path.join(tmp, "metatile_attributes.bin")
            convertido, rel = CF.converte(open(alvo, "rb").read(), com_encontro=True)
            open(alvo, "wb").write(convertido)
            print("   comportamento FRLG -> nosso:")
            CF.relata(rel, CF.enum_nosso())
        r = subprocess.run([sys.executable, os.path.join(FERR, "instala_tileset.py"),
                            tmp, label, "--repo", RAIZ] + (["--sec"] if secundario else []),
                           capture_output=True, text=True)
        if r.returncode:
            print("ERRO do instala_tileset: %s%s" % (r.stdout, r.stderr), file=sys.stderr)
            sys.exit(1)
        print("   " + r.stdout.strip().splitlines()[-1])

    # --- PROVA NEGATIVA 3: o secundario tem metatile para o maior id usado?
    if not a.demo and a.ts_sec:
        p_meta = os.path.join(RAIZ, "data/tilesets/secondary/%s/metatiles.bin" % snake(a.ts_sec))
        n = os.path.getsize(p_meta) // 16
        usado = censo["max_metatile"] - split + 1
        if censo["max_metatile"] >= split and usado > n:
            print("ERRO: a planta usa metatile secundario %d e o tileset so tem %d."
                  % (usado - 1, n), file=sys.stderr)
            sys.exit(1)
        print("  secundario: %d metatiles, planta usa ate %d  OK" % (n, max(0, usado)))

    acoes.append("%s/map.bin (%d B) e border.bin (%d B)" % (rel_layout, len(blob), len(borda)))
    acoes.append("layouts.json: entrada %s no FIM, layout_version=%s borda %dx%d"
                 % (lay_id, versao, bw, bh))
    acoes.append("%s/map.json (%s) com as quatro listas de evento VAZIAS" % (rel_mapa, map_id))
    acoes.append("%s/scripts.inc (so o rotulo _MapScripts)" % rel_mapa)
    acoes.append("map_groups.json: %s no FIM de %s" % (nome, a.grupo_alvo))
    acoes.append("event_scripts.s: include do scripts.inc no fim")

    if a.demo:
        print("\nDEMO, nada foi escrito:")
        for x in acoes:
            print("  " + x)
        return

    os.makedirs(os.path.join(RAIZ, rel_layout), exist_ok=True)
    open(os.path.join(RAIZ, rel_layout, "map.bin"), "wb").write(blob)
    open(os.path.join(RAIZ, rel_layout, "border.bin"), "wb").write(borda)

    p_lay = os.path.join(RAIZ, "data/layouts/layouts.json")
    dados = json.load(open(p_lay, encoding="utf-8"))
    if any(l.get("id") == lay_id for l in dados["layouts"]):
        print("ERRO: %s ja existe em layouts.json." % lay_id, file=sys.stderr)
        sys.exit(1)
    entrada = {
        "id": lay_id,
        "name": nome + "_Layout",
        "width": w,
        "height": hh,
        "border_width": bw,
        "border_height": bh,
        "primary_tileset": "gTileset_" + pri_label,
        "secondary_tileset": "gTileset_" + sec_label,
        "border_filepath": rel_layout + "/border.bin",
        "blockdata_filepath": rel_layout + "/map.bin",
        "layout_version": versao,
    }
    if versao != "frlg":
        del entrada["border_width"], entrada["border_height"]
    dados["layouts"].append(entrada)
    json.dump(dados, open(p_lay, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    open(p_lay, "a", encoding="utf-8").write("\n")

    os.makedirs(os.path.join(RAIZ, rel_mapa), exist_ok=True)
    mj = dict(MAPJSON_MODELO)
    mj["id"], mj["name"], mj["layout"] = map_id, nome, lay_id
    mj["music"] = a.musica
    mj["region"] = a.regiao
    mj["region_map_section"] = a.mapsec
    mj["map_type"] = a.tipo
    mj["weather"] = a.clima
    mj["requires_flash"] = bool(a.flash)
    mj["allow_running"] = bool(a.corre)
    mj["allow_cycling"] = bool(a.bicicleta)
    mj["allow_escaping"] = bool(a.fuga)
    if a.popup:
        mj["map_name_popup"] = a.popup
    mj["connections"] = None
    json.dump(mj, open(os.path.join(RAIZ, rel_mapa, "map.json"), "w", encoding="utf-8"),
              indent=2, ensure_ascii=False)
    open(os.path.join(RAIZ, rel_mapa, "map.json"), "a", encoding="utf-8").write("\n")

    open(os.path.join(RAIZ, rel_mapa, "scripts.inc"), "w", encoding="utf-8").write(
        SCRIPTS_MODELO % {"nome": nome, "hack": os.path.basename(caminho),
                          "g": a.grupo, "m": a.mapa})

    p_gr = os.path.join(RAIZ, "data/maps/map_groups.json")
    gr = json.load(open(p_gr, encoding="utf-8"))
    if a.grupo_alvo not in gr:
        print("ERRO: grupo %s nao existe em map_groups.json" % a.grupo_alvo, file=sys.stderr)
        sys.exit(1)
    if nome in gr[a.grupo_alvo]:
        print("ERRO: %s ja esta em %s" % (nome, a.grupo_alvo), file=sys.stderr)
        sys.exit(1)
    gr[a.grupo_alvo].append(nome)   # FIM do grupo: regra 7 do metodo
    json.dump(gr, open(p_gr, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    open(p_gr, "a", encoding="utf-8").write("\n")

    p_ev = os.path.join(RAIZ, "data/event_scripts.s")
    linha = '\t.include "%s/scripts.inc"\n' % rel_mapa
    texto = open(p_ev, encoding="utf-8").read()
    if linha not in texto:
        open(p_ev, "a", encoding="utf-8").write(linha)

    for x in acoes:
        print("  " + x)
    print("PRONTO: %s (%s) copiado de g%dm%d." % (nome, map_id, a.grupo, a.mapa))


# ------------------------------------------------------------- prova de render

def prova_render(a, saida):
    """Desenha o mapa do HACK e o mapa COPIADO e compara pixel a pixel.

    E a unica prova que vale: build verde e portao de planta nao olham imagem
    nenhuma (licao da secao 0.ae do ESTADO).
    """
    from PIL import Image
    from gbamap import Rom
    import render_hack

    caminho = acha_rom(a.rom)
    rom = Rom(caminho)
    gmg = int(a.gmg, 16) if a.gmg else rom.acha_mapgroups()[0]
    h = le_cabecalho(rom, gmg, a.grupo, a.mapa)

    sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
    import render_maps
    layouts = render_maps.carregar_layouts()

    # O render do repo pinta o fundo com a cor 0 da paleta 0 do primario (e o
    # backdrop do BG do hardware); o render_hack pinta de preto. Sem igualar os
    # dois, todo tile de duas camadas transparentes conta como diferenca e a
    # prova vira ruido. Aqui o fundo do render do HACK passa a ser o mesmo.
    import json as _json
    mapa_json = _json.load(open(os.path.join(RAIZ, "data/maps", a.nome, "map.json"), encoding="utf-8"))
    lay = layouts[mapa_json["layout"]]
    ts_pri = render_maps.carregar_tileset(lay["primary_tileset"])
    fundo = ts_pri["paletas"][0][0]
    original_new = render_hack.Image.new
    render_hack.Image.new = lambda modo, tam, cor=(0, 0, 0): original_new(
        modo, tam, fundo if cor == (0, 0, 0) else cor)
    try:
        img_hack = render_hack.Render(rom).mapa(h)
    finally:
        render_hack.Image.new = original_new

    caminho_nosso = render_maps.renderizar_mapa(a.nome, layouts, {})
    img_nosso = Image.open(caminho_nosso).convert("RGB")

    if img_hack.size != img_nosso.size:
        print("DIFERE no tamanho: hack %s, copia %s" % (img_hack.size, img_nosso.size))
        return 1
    dif = 0
    ph, pn = img_hack.convert("RGB").load(), img_nosso.load()
    for y in range(img_hack.size[1]):
        for x in range(img_hack.size[0]):
            if ph[x, y] != pn[x, y]:
                dif += 1
    total = img_hack.size[0] * img_hack.size[1]
    lado = Image.new("RGB", (img_hack.size[0] * 2 + 8, img_hack.size[1]), (20, 20, 20))
    lado.paste(img_hack, (0, 0))
    lado.paste(img_nosso, (img_hack.size[0] + 8, 0))
    lado.save(saida)
    print("prova de render: %d de %d pixels diferentes (%.4f%%) -> %s"
          % (dif, total, 100.0 * dif / total, saida))
    return 0 if dif == 0 else 2


# ------------------------------------------------------------------- autoteste

def autoteste():
    falhas = []

    ok = (cabe_na_memoria(58, 50) and cabe_na_memoria(132, 54)
          and not cabe_na_memoria(200, 200) and cabe_na_memoria(60, 120)
          and not cabe_na_memoria(150, 150))
    # o caso exato do teto: 10240 cabe, 10241 nao
    ok = ok and cabe_na_memoria(1, 10240 // 16 - 14)
    if not ok:
        falhas.append("cabe_na_memoria")
    print("1. teto de MAX_MAP_DATA_SIZE ((w+15)*(h+14) <= 10240): %s" % ("OK" if ok else "FALHOU"))

    blob = struct.pack("<4H", 0x0001, 0x0402, 0x1003, 0xFFFF)
    c = censo_blocos(blob, 2, 2)
    ok = (c["max_metatile"] == 0x3FF and c["min_metatile"] == 1 and c["distintos"] == 4
          and c["colisao"] == {0: 2, 1: 1, 3: 1} and c["elevacao"] == {0: 2, 1: 1, 15: 1})
    if not ok:
        falhas.append("censo_blocos")
    print("2. bloco de 16 bits (metatile 0-9, colisao 10-11, elevacao 12-15): %s"
          % ("OK" if ok else "FALHOU"))

    erro = None
    try:
        censo_blocos(b"\x00" * 6, 2, 2)
    except ValueError as e:
        erro = str(e)
    ok = erro is not None
    if not ok:
        falhas.append("censo_blocos aceita blockdata truncado")
    print("3. blockdata de tamanho errado e FALHA DURA, nao mapa pela metade: %s"
          % ("OK" if ok else "FALHOU"))

    ok = (id_layout("LcSafariMountain") == "LAYOUT_LC_SAFARI_MOUNTAIN"
          and id_mapa("LcSafariMountain") == "MAP_LC_SAFARI_MOUNTAIN"
          and snake("LcSafariMountain") == "lc_safari_mountain")
    if not ok:
        falhas.append("nomes")
    print("4. CamelCase -> LAYOUT_/MAP_/snake: %s" % ("OK" if ok else "FALHOU"))

    # 5. a leitura da borda na ROM de verdade, se ela estiver aqui
    try:
        from gbamap import Rom
        p = acha_rom("liquid-crystal")
        r = Rom(p)
        h = le_cabecalho(r, 0x3526A8, 5, 115)
        ok = (h["layout"]["w"], h["layout"]["h"],
              h["layout"]["border_w"], h["layout"]["border_h"]) == (69, 56, 3, 2)
        detalhe = "g5m115 = %dx%d borda %dx%d" % (h["layout"]["w"], h["layout"]["h"],
                                                  h["layout"]["border_w"], h["layout"]["border_h"])
    except SystemExit:
        ok, detalhe = True, "ROM ausente, pulado"
    if not ok:
        falhas.append("borda na ROM")
    print("5. borderWidth/Height em 0x18/0x19 (%s): %s" % (detalhe, "OK" if ok else "FALHOU"))

    print("\n%s" % ("autoteste PASSOU" if not falhas else "autoteste REPROVOU: " + ", ".join(falhas)))
    return 0 if not falhas else 1


def main():
    if "--autoteste" in sys.argv:
        sys.exit(autoteste())
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--rom", required=True, help="slug em fontes-mapas/romhacks/ ou caminho .gba")
    ap.add_argument("--grupo", type=int, required=True)
    ap.add_argument("--mapa", type=int, required=True)
    ap.add_argument("--gmg", default=None, help="offset hex de gMapGroups (padrao: descobre)")
    ap.add_argument("--nome", required=True, help="nome CamelCase do mapa novo")
    ap.add_argument("--layout-id", default=None)
    ap.add_argument("--ts-pri", default=None, help="rotulo novo: importa o primario do hack")
    ap.add_argument("--ts-sec", default=None, help="rotulo novo: importa o secundario do hack")
    ap.add_argument("--ts-pri-existente", default=None, help="rotulo que ja existe no repo")
    ap.add_argument("--ts-sec-existente", default=None)
    ap.add_argument("--grupo-alvo", default="gMapGroup_Dungeons_Johto")
    ap.add_argument("--mapsec", default="MAPSEC_NONE")
    ap.add_argument("--regiao", default="REGION_HOENN",
                    help="REGION_KANTO/JOHTO/HOENN/SINNOH; o mapjson assume HOENN se faltar")
    ap.add_argument("--popup", default=None)
    ap.add_argument("--musica", default="MUS_ROUTE118")
    ap.add_argument("--tipo", default="MAP_TYPE_ROUTE")
    ap.add_argument("--clima", default="WEATHER_NONE")
    ap.add_argument("--attr", choices=("2", "4"), default="4")
    ap.add_argument("--sem-comportamento", action="store_true",
                    help="NAO traduz o comportamento de metatile do FireRed para o nosso "
                         "(so para investigar; o padrao e traduzir, ver comportamento_frlg.py)")
    ap.add_argument("--flash", action="store_true")
    ap.add_argument("--corre", action="store_true")
    ap.add_argument("--bicicleta", action="store_true")
    ap.add_argument("--fuga", action="store_true")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--prova-render", default=None, metavar="PNG")
    a = ap.parse_args()
    if a.prova_render:
        sys.exit(prova_render(a, a.prova_render))
    copia(a)


if __name__ == "__main__":
    main()
