#!/usr/bin/env python3
"""Traz os tilesets de verdade de Johto do hns e religa os layouts a eles.

Uso:
    python3 dev_scripts/importa_tilesets_johto.py          # aplica
    python3 dev_scripts/importa_tilesets_johto.py --demo   # so os testes

POR QUE ISSO EXISTE
-------------------
`dev_scripts/fix_johto_tilesets.py` (e o `remap_johto_tilesets.py` antes dele)
percorreu layouts.json e, para todo tileset cujo nome nao estava numa lista
branca de simbolos de Hoenn, gravou um substituto: primario virou
`gTileset_GeneralSinnoh` e secundario virou `gTileset_PetalburgSinnoh`. Foi um
conserto de LINKAGEM: o build parou de reclamar de simbolo inexistente.

Só que o blockdata de Johto continuou o mesmo. Cada id de metatile passou a ser
lido numa tabela que nao e a dele. Onde a fonte tinha porta, o id resolvia para
grama, e o motor so executa warp se o comportamento do metatile embaixo do
jogador for de porta, escada ou escada rolante (`TryStartWarpEventScript` chama
`IsWarpMetatileBehavior`). Resultado medido: 12 dos 771 warps de Johto
disparavam, 1,6%.

O DETALHE QUE NAO DA PRA PULAR
------------------------------
O hns e um fork com `NUM_METATILES_IN_PRIMARY = NUM_TILES_IN_PRIMARY = 640` e
`NUM_PALS_IN_PRIMARY = 7`. Este repo usa 512/512/6 no caminho Emerald e
640/640/7 so no caminho FRLG, e o caminho FRLG tambem troca o atributo de
metatile para 4 bytes. Johto quer 640 metatiles COM atributo de 2 bytes, que nao
e nenhum dos dois.

Por isso os layouts de Johto saem daqui com `layout_version: "johto"`, que o
mapjson traduz para o campo `bigPrimary` da struct MapLayout: corte do primario
em 640, 7 paletas, e todo o resto (atributo, porta, escada, loja) igual ao de
Emerald.

Converter os tilesets para 512 foi descartado com medida, nao com opiniao: os
seis primarios de Johto usam metatiles ate o id 639 e tem 640 tiles cada. Cortar
em 512 perderia 128 metatiles que os mapas referenciam de verdade.
"""
import json
import os
import re
import shutil
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HNS = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/hns"
MARCA = "// ---- tilesets de Johto (dev_scripts/importa_tilesets_johto.py) ----"


def camel(pasta):
    """route_38_farmland -> Route38Farmland"""
    return "".join(p[:1].upper() + p[1:] for p in pasta.split("_"))


def le_fonte():
    """Devolve {simbolo_hns: (pasta_relativa, e_secundario)}.

    A pasta sai do INCBIN do proprio hns, nao de adivinhacao a partir do nome do
    simbolo. `gTileset_GoldenrodCity_TrainStation` mora em
    `secondary/goldenrod_station` e `gTileset_TrainerHill_Courtyard` mora em
    `secondary/battle_tower_outer`: qualquer regra de conversao de nome erra
    esses dois.
    """
    txt = open(f"{HNS}/src/data/tilesets/metatiles.h").read()
    m2f = dict(re.findall(
        r'gMetatiles_(\w+)\[\]\s*=\s*INCBIN_U16\("data/tilesets/(\w+/\w+)/metatiles\.bin"\)',
        txt))
    hdr = open(f"{HNS}/src/data/tilesets/headers.h").read()
    fonte = {}
    for nome, corpo in re.findall(
            r'const struct Tileset gTileset_(\w+)\s*=\s*\{(.*?)\};', hdr, re.S):
        mt = re.search(r'\.metatiles\s*=\s*gMetatiles_(\w+)', corpo)
        if mt and mt.group(1) in m2f:
            fonte["gTileset_" + nome] = (m2f[mt.group(1)],
                                         "isSecondary = TRUE" in corpo)
    return fonte


def layouts_de_johto():
    """{layout_id: entrada do layouts.json do hns} para os mapas de Johto daqui."""
    grupos = json.load(open(f"{RAIZ}/data/maps/map_groups.json"))
    hl = {l["id"]: l for l in
          json.load(open(f"{HNS}/data/layouts/layouts.json"))["layouts"]}
    ids = set()
    for grp in grupos["group_order"]:
        if "johto" not in grp.lower():
            continue
        for m in grupos.get(grp, []):
            p = f"{RAIZ}/data/maps/{m}/map.json"
            if os.path.exists(p):
                ids.add(json.load(open(p))["layout"])
    return {i: hl[i] for i in ids if i in hl}


def main():
    fonte = le_fonte()
    lays = layouts_de_johto()
    print(f"layouts de Johto com equivalente no hns: {len(lays)}")

    precisa = set()
    for L in lays.values():
        precisa.add(L["primary_tileset"])
        precisa.add(L["secondary_tileset"])

    hdr_dest = open(f"{RAIZ}/src/data/tilesets/headers.h").read()
    mt_dest = open(f"{RAIZ}/src/data/tilesets/metatiles.h").read()
    # O que uma execucao anterior ja importou. Sem isso, rodar de novo veria a
    # propria pasta como colisao de nome e importaria `x_johto_johto`.
    ja = {}
    if MARCA in mt_dest:
        for n, d in re.findall(
                r'gMetatiles_(\w+)\[\] = INCBIN_U16\("data/tilesets/(\w+/\w+)/metatiles\.bin"\)',
                mt_dest[mt_dest.index(MARCA):]):
            ja["gTileset_" + n] = d
    ocupados = set(re.findall(r'const struct Tileset (gTileset_\w+)', hdr_dest)) - set(ja)
    # `[-1]`, nao `[1]`. Com `[1]` o conjunto virava {"tilesets"} (o caminho e
    # `data/tilesets/secondary/x`), nenhuma colisao era detectada, e o copy
    # SOBRESCREVEU data/tilesets/secondary/{bike_shop,pokemon_day_care,
    # sootopolis_gym} com a versao do hns. Sao tilesets de Hoenn usados por mapa
    # de Hoenn: o estrago era silencioso e so aparecia como grafico errado em
    # outro mapa. `ja` usa a forma curta `secondary/x` e a varredura usa a forma
    # longa, entao so `[-1]` serve para as duas.
    pastas_ocupadas = {d.split("/")[-1] for d in
                       re.findall(r'INCBIN_U16\("(data/tilesets/\w+/\w+)/metatiles\.bin"\)', mt_dest)
                       } - {d.split("/")[-1] for d in ja.values()}

    # simbolo do hns -> (simbolo daqui, subpasta, pasta daqui, pasta no hns, secundario)
    plano = {}
    for ts in sorted(precisa):
        if ts not in fonte:
            print(f"  IGNORADO (sem pasta no hns): {ts}")
            continue
        rel, sec = fonte[ts]
        sub, pasta = rel.split("/")
        if pasta in pastas_ocupadas:
            pasta += "_johto"   # o nome ja existe aqui com conteudo de Hoenn
        simbolo = "gTileset_" + camel(pasta)
        while simbolo in ocupados:
            simbolo += "Johto"
        plano[ts] = (simbolo, sub, pasta, rel, sec)

    print(f"tilesets no plano: {len(plano)}")

    # 1. copiar os arquivos. anim/ e .pla ficam de fora: nenhum callback de
    #    animacao de Johto existe aqui, e arquivo solto vira regra de build orfa.
    for _, sub, pasta, rel, _ in plano.values():
        dst = f"{RAIZ}/data/tilesets/{sub}/{pasta}"
        src = f"{HNS}/data/tilesets/{rel}"
        os.makedirs(f"{dst}/palettes", exist_ok=True)
        for f in ("metatiles.bin", "metatile_attributes.bin", "tiles.png"):
            shutil.copy2(f"{src}/{f}", f"{dst}/{f}")
        for f in sorted(os.listdir(f"{src}/palettes")):
            if f.endswith(".pal"):
                shutil.copy2(f"{src}/palettes/{f}", f"{dst}/palettes/{f}")

    # 2. registrar em metatiles.h, graphics.h e headers.h
    mt = ["", MARCA]
    gx = ["", MARCA]
    hd = ["", MARCA]
    for simbolo, sub, pasta, _, sec in sorted(plano.values()):
        n = simbolo.replace("gTileset_", "")
        d = f"data/tilesets/{sub}/{pasta}"
        # ARMADILHA: nem todo tileset do hns tem as 16 paletas. Varios secundarios
        # param na 12, que e a ultima que o motor le (NUM_PALS_TOTAL == 13).
        # Emitir INCGFX de arquivo que nao existe faz o gbagfx derrubar o build.
        pals = sorted(f for f in os.listdir(f"{RAIZ}/{d}/palettes") if f.endswith(".pal"))
        mt.append(f'const u16 gMetatiles_{n}[] = INCBIN_U16("{d}/metatiles.bin");')
        mt.append(f'const u16 gMetatileAttributes_{n}[] = INCBIN_U16("{d}/metatile_attributes.bin");')
        gx.append(f"const u16 ALIGNED(4) gTilesetPalettes_{n}[][16] =")
        gx.append("{")
        gx += [f'    INCGFX_U16("{d}/palettes/{p}", ".gbapal"),' for p in pals]
        gx.append("};")
        gx.append(f'const u32 gTilesetTiles_{n}[] = INCGFX_U32("{d}/tiles.png", ".4bpp.smol");')
        gx.append("")
        hd += [f"const struct Tileset {simbolo} =", "{",
               "    .isCompressed = TRUE,",
               f"    .isSecondary = {'TRUE' if sec else 'FALSE'},",
               f"    .tiles = gTilesetTiles_{n},",
               f"    .palettes = gTilesetPalettes_{n},",
               f"    .metatiles = gMetatiles_{n},",
               f"    .metatileAttributes = gMetatileAttributes_{n},",
               "    .callback = NULL,", "};", ""]
    for arq, linhas in (("metatiles.h", mt), ("graphics.h", gx), ("headers.h", hd)):
        p = f"{RAIZ}/src/data/tilesets/{arq}"
        txt = open(p).read()
        if MARCA in txt:            # re-execucao: troca o bloco inteiro
            txt = txt[:txt.index(MARCA)].rstrip() + "\n"
        open(p, "w").write(txt.rstrip() + "\n" + "\n".join(linhas) + "\n")

    # 3. religar os layouts e marcar o corte de primario em 640
    lj = json.load(open(f"{RAIZ}/data/layouts/layouts.json"))
    por_id = {l["id"]: l for l in lj["layouts"]}
    mudados = 0
    for lid, L in lays.items():
        alvo = por_id.get(lid)
        if not alvo:
            continue
        p, s = plano.get(L["primary_tileset"]), plano.get(L["secondary_tileset"])
        if not p or not s:
            print(f"  IGNORADO (tileset sem plano): {lid}")
            continue
        alvo["primary_tileset"], alvo["secondary_tileset"] = p[0], s[0]
        alvo["layout_version"] = "johto"
        mudados += 1
    json.dump(lj, open(f"{RAIZ}/data/layouts/layouts.json", "w"), indent=2)
    print(f"layouts religados: {mudados}")
    return 0


def demo():
    """Os dois pontos que quebram calado: nome de pasta e corte do primario."""
    assert camel("johto_general") == "JohtoGeneral"
    assert camel("route_38_farmland") == "Route38Farmland", camel("route_38_farmland")

    fonte = le_fonte()
    # a pasta NAO sai do nome do simbolo: estes tres provam isso
    assert fonte["gTileset_GoldenrodCity_TrainStation"][0] == "secondary/goldenrod_station"
    assert fonte["gTileset_TrainerHill_Courtyard"][0] == "secondary/battle_tower_outer"
    assert fonte["gTileset_Johto_General"] == ("primary/johto_general", False)

    # o corte tem que ser 640: se fosse 512, estes metatiles cairiam no secundario
    n = os.path.getsize(f"{HNS}/data/tilesets/primary/johto_general/metatiles.bin") // 16
    assert n == 640, n

    # INVARIANTE QUE JA FOI VIOLADA: nenhuma pasta de tileset pode ser apontada
    # por dois simbolos. Quando `pastas_ocupadas` lia o segmento errado do
    # caminho, o import copiou o bike_shop do hns POR CIMA do bike_shop de
    # Hoenn, e nada acusou: os dois simbolos passaram a apontar para a mesma
    # pasta, com o conteudo do segundo. Isso encontra o caso na hora.
    # (o vanilla ja compartilha `primary/building` entre dois simbolos de
    # proposito, entao a regra vale so para o que ESTE script importou)
    mt = open(f"{RAIZ}/src/data/tilesets/metatiles.h").read()
    padrao = r'gMetatiles_(\w+)\[\] = INCBIN_U16\("data/tilesets/(\w+/\w+)/metatiles\.bin"\)'
    antes = mt[:mt.index(MARCA)] if MARCA in mt else mt
    de_fora = {d for _, d in re.findall(padrao, antes)}
    if MARCA in mt:
        for sim, d in re.findall(padrao, mt[mt.index(MARCA):]):
            assert d not in de_fora, f"{sim} sobrescreveu o tileset de {d}"
    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
