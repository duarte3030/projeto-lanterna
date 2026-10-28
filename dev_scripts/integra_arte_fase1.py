#!/usr/bin/env python3
"""Integra no cartucho 2 a arte aprovada da fase 1 (decisão 145, 28/10/2026).

Entram SÓ assets e registros do motor. Nenhum retrato nem sprite de treinador ou NPC
que já esteja num mapa é trocado (isso depende da decisão 130 e vem depois).

O que faz:
  1. 50 retratos de treinador -> TRAINER_PIC_GALAR_* (23) e TRAINER_PIC_UNOVA_* (27).
  2. 59 folhas de NPC -> OBJ_EVENT_GFX_GALAR_* (28, 32x32) e OBJ_EVENT_GFX_UNOVA_* (31, 16x32),
     cada uma com paleta própria (tag OBJ_EVENT_PAL_TAG_*) tirada do próprio PNG.
  3. 13 fundos de batalha de Galar -> BATTLE_ENVIRONMENT_GALAR_* (ambientes novos).
  4. Copia, sem ligar ao motor, o mapa-múndi e as insígnias de Galar.

Idempotência: se o marcador `>>> arte fase 1` já está num arquivo, o script PARA sem tocar
em nada (rodar duas vezes duplicaria constantes). Para refazer, `git checkout` os arquivos.

Uso (da raiz do repo):  python3 dev_scripts/integra_arte_fase1.py [--fonte DIR]
"""
import argparse
import json
import os
import re
import shutil
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTE = os.path.expanduser("~/Projetos/pokemon-claude/fontes-mapas/prd-assets/fase1-arte")
MARCA = ">>> arte fase 1"
FIM = "<<< fim da arte fase 1"

PREFIXOS = ("leader_", "champion_", "rival_", "villain_", "dlc_", "elite4_", "player_",
            "story_", "professor_")

# nome em inglês de cada fundo de batalha, e de qual ambiente do expansion herda as regras
# de golpe (Nature Power, Secret Power, Camouflage). A arte é de Galar, a regra é a do tipo de terreno.
FUNDOS = {
    "galar_campo":           ("FIELD",          "GRASS"),
    "galar_grama_alta":      ("TALL_GRASS",     "LONG_GRASS"),
    "galar_agua":            ("WATER",          "WATER"),
    "galar_submerso":        ("UNDERWATER",     "UNDERWATER"),
    "galar_deserto":         ("DESERT",         "SAND"),
    "galar_caverna_a":       ("CAVE_A",         "CAVE"),
    "galar_caverna_b":       ("CAVE_B",         "CAVE"),
    "galar_estadio_gelo":    ("STADIUM_ICE",    "ICE"),
    "galar_estadio_grama":   ("STADIUM_GRASS",  "GRASS"),
    "galar_estadio_laranja": ("STADIUM_ORANGE", "BUILDING"),
    "galar_estadio_pokebola": ("STADIUM_POKEBALL", "BUILDING"),
    "galar_estadio_vermelho": ("STADIUM_RED",   "BUILDING"),
    "galar_tela_roxa":       ("PURPLE_SCREEN",  "PLAIN"),
}


def die(msg):
    sys.exit("ERRO: " + msg)


def le(rel):
    with open(os.path.join(RAIZ, rel), encoding="utf-8") as f:
        return f.read()


def grava(rel, txt):
    with open(os.path.join(RAIZ, rel), "w", encoding="utf-8") as f:
        f.write(txt)


def copia(src, rel_dest):
    d = os.path.join(RAIZ, rel_dest)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copyfile(src, d)


def nome_base(stem):
    for p in PREFIXOS:
        if stem.startswith(p):
            stem = stem[len(p):]
            break
    if stem.startswith("sem_nome_"):
        return "NPC_" + stem[len("sem_nome_"):]
    return stem.upper()


def camel(base):
    return "".join(p.capitalize() for p in base.split("_"))


def lista(regiao, pasta):
    d = os.path.join(FONTE, regiao, pasta)
    return [f[:-4] for f in sorted(os.listdir(d)) if f.endswith(".png")], d


def confere_png(caminho, w, h):
    """4bpp indexado, tamanho exato e 16 cores (só o PLTE; sem Pillow, o repo não exige)."""
    with open(caminho, "rb") as f:
        d = f.read()
    ww, hh, prof, tipo = struct.unpack(">IIBB", d[16:26])
    if (ww, hh, prof, tipo) != (w, h, 4, 3):
        die("%s: esperado %dx%d 4bpp indexado, veio %dx%d %dbpp tipo %d" % (caminho, w, h, ww, hh, prof, tipo))


def so_uma_vez(txt, rel):
    if MARCA in txt:
        die("%s já tem o marcador '%s'; nada foi alterado" % (rel, MARCA))


def insere_antes(txt, ancora, bloco, rel):
    if txt.count(ancora) != 1:
        die("%s: âncora %r aparece %d vezes (esperado 1)" % (rel, ancora, txt.count(ancora)))
    return txt.replace(ancora, bloco + ancora)


def main():
    global FONTE
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonte", default=FONTE)
    FONTE = ap.parse_args().fonte
    resumo = {}

    # ------------------------------------------------------------------ 1. retratos
    retratos = []  # (regiao_up, base, stem, regiao_dir)
    for regiao, up in (("galar", "GALAR"), ("unova", "UNOVA")):
        stems, d = lista(regiao, "retratos")
        for s in stems:
            confere_png(os.path.join(d, s + ".png"), 64, 64)
            retratos.append((up, nome_base(s), s, regiao))
    consts = ["%s_%s" % (u, b) for u, b, _, _ in retratos]
    if len(set(consts)) != len(consts):
        die("nome de retrato duplicado")

    rel = "include/constants/trainers.h"
    t = le(rel)
    so_uma_vez(t, rel)
    bloco = "    // %s (dev_scripts/integra_arte_fase1.py)\n" % MARCA
    bloco += "".join("    TRAINER_PIC_%s,\n" % c for c in consts)
    bloco += "    // %s\n" % FIM
    t = insere_antes(t, "    TRAINER_PIC_COUNT,\n", bloco, rel)
    grava(rel, t)

    rel = "src/data/graphics/trainers.h"
    t = le(rel)
    so_uma_vez(t, rel)
    inc = "// %s: retratos de Galar (PNG 64x64, 4bpp, paleta de 16 cores no próprio PNG)\n" % MARCA
    for u, b, s, regiao in retratos:
        sim = u.capitalize() + camel(b)
        arq = "graphics/trainers/front_pics/%s_%s.png" % (u.lower(), b.lower())
        copia(os.path.join(FONTE, regiao, "retratos", s + ".png"), arq)
        inc += 'const u32 gTrainerFrontPic_%s[] = INCGFX_U32("%s", ".4bpp.smol");\n' % (sim, arq)
        inc += 'const u16 gTrainerPalette_%s[] = INCGFX_U16("%s", ".gbapal");\n' % (sim, arq)
    inc += "// %s\n\n" % FIM
    t = insere_antes(t, "const struct TrainerPicInfo gTrainerPicInfo[TRAINER_PIC_COUNT] =\n", inc, rel)
    # entradas da tabela: antes do "};" que fecha gTrainerPicInfo
    i = t.index("const struct TrainerPicInfo gTrainerPicInfo[TRAINER_PIC_COUNT] =\n")
    j = t.index("\n};\n", i) + 1
    ent = "    // %s\n" % MARCA
    for u, b, s, regiao in retratos:
        sim = u.capitalize() + camel(b)
        ent += "    [TRAINER_PIC_%s_%s] =\n    {\n        .frontPic = TRAINER_FRONT_PIC(gTrainerFrontPic_%s, gTrainerPalette_%s),\n    },\n" % (u, b, sim, sim)
    ent += "    // %s\n" % FIM
    t = t[:j] + ent + t[j:]
    grava(rel, t)
    resumo["retratos"] = {"galar": sum(1 for r in retratos if r[0] == "GALAR"),
                          "unova": sum(1 for r in retratos if r[0] == "UNOVA")}

    # ------------------------------------------------------------------ 2. NPCs
    npcs = []  # (up, base, stem, regiao, pasta, largura_px, mw)
    for regiao, up, pasta, wq in (("galar", "GALAR", "npcs", 32), ("unova", "UNOVA", "npcs_16x32", 16)):
        stems, d = lista(regiao, pasta)
        for s in stems:
            confere_png(os.path.join(d, s + ".png"), wq * 9, 32)
            npcs.append((up, nome_base(s), s, regiao, pasta, wq))
    ids = ["%s_%s" % (n[0], n[1]) for n in npcs]
    if len(set(ids)) != len(ids):
        die("nome de NPC duplicado")

    # tags de paleta: 0x1600+ Galar, 0x1700+ Unova (0x1200 é clima, 0x1400 sombras de field effect,
    # 0x1100-0x1167 são as tags de objeto do próprio jogo; nada do repo usa 0x16xx nem 0x17xx).
    tags = {}
    cont = {"GALAR": 0x1600, "UNOVA": 0x1700}
    for u, b, *_ in npcs:
        tags[(u, b)] = cont[u]
        cont[u] += 1

    rel = "include/constants/event_objects.h"
    t = le(rel)
    so_uma_vez(t, rel)
    blk = ("// %s: sprites de NPC de Galar (32x32) e Unova (16x32). Entram no FIM do enum,\n"
           "// onde não deslocam id de gráfico já gravado em map.json.\n" % MARCA)
    blk += "".join("    OBJ_EVENT_GFX_%s_%s,\n" % (u, b) for u, b, *_ in npcs)
    blk += "// %s\n" % FIM
    t = insere_antes(t, "    NUM_OBJ_EVENT_GFX,\n", blk, rel)
    tg = ("// %s: uma paleta de 16 cores por folha, tirada do próprio PNG.\n"
          "// Faixas 0x1600 (Galar) e 0x1700 (Unova). CADA tag distinta numa mesma tela\n"
          "// ocupa um dos 16 slots de paleta de OBJ; ver ESTADO-CARTUCHO-2.md.\n" % MARCA)
    tg += "".join("#define OBJ_EVENT_PAL_TAG_%s_%s 0x%04X\n" % (u, b, tags[(u, b)]) for u, b, *_ in npcs)
    tg += "// %s\n\n" % FIM
    t = insere_antes(t, "#if OW_FOLLOWERS_POKEBALLS\n// Vanilla\n", tg, rel)
    grava(rel, t)

    rel = "src/data/object_events/object_event_graphics.h"
    t = le(rel)
    so_uma_vez(t, rel)
    g = "\n// %s: NPCs de Galar (32x32) e Unova (16x32), cru de propósito (ver comprime_overworld.py)\n" % MARCA
    for u, b, s, regiao, pasta, wq in npcs:
        sim = u.capitalize() + camel(b)
        arq = "graphics/object_events/pics/people/%s/%s.png" % (regiao, b.lower())
        copia(os.path.join(FONTE, regiao, pasta, s + ".png"), arq)
        mw = wq // 8
        g += 'const u32 gObjectEventPic_%s[] = INCGFX_U32("%s", ".4bpp", "-mwidth %d -mheight 4");\n' % (sim, arq, mw)
        g += 'const u16 gObjectEventPal_%s[] = INCGFX_U16("%s", ".gbapal");\n' % (sim, arq)
    g += "// %s\n" % FIM
    grava(rel, t.rstrip("\n") + "\n" + g)

    rel = "src/data/object_events/object_event_pic_tables.h"
    t = le(rel)
    so_uma_vez(t, rel)
    p = "\n// %s\n" % MARCA
    for u, b, s, regiao, pasta, wq in npcs:
        sim = u.capitalize() + camel(b)
        p += "static const struct SpriteFrameImage sPicTable_%s[] = {\n    overworld_ascending_frames(gObjectEventPic_%s, %d, 4),\n};\n\n" % (sim, sim, wq // 8)
    p += "// %s\n" % FIM
    grava(rel, t.rstrip("\n") + "\n" + p)

    rel = "src/data/object_events/object_event_graphics_info.h"
    t = le(rel)
    so_uma_vez(t, rel)
    gi = "\n// %s\n" % MARCA
    for u, b, s, regiao, pasta, wq in npcs:
        sim = u.capitalize() + camel(b)
        gi += ("const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_%s = {\n"
               "    .tileTag = TAG_NONE,\n"
               "    .paletteTag = OBJ_EVENT_PAL_TAG_%s_%s,\n"
               "    .reflectionPaletteTag = OBJ_EVENT_PAL_TAG_NONE,\n"
               "    .size = %d,\n"
               "    .width = %d,\n"
               "    .height = 32,\n"
               "    .paletteSlot = PALSLOT_NPC_SPECIAL,\n"
               "    .shadowSize = SHADOW_SIZE_M,\n"
               "    .inanimate = FALSE,\n"
               "    .compressed = FALSE,\n"
               "    .tracks = TRACKS_FOOT,\n"
               "    .oam = &gObjectEventBaseOam_%dx32,\n"
               "    .subspriteTables = sOamTables_%dx32,\n"
               "    .anims = sAnimTable_Standard,\n"
               "    .images = sPicTable_%s,\n"
               "};\n\n") % (sim, u, b, wq * 32 // 2, wq, wq, wq, sim)
    gi += "// %s\n" % FIM
    grava(rel, t.rstrip("\n") + "\n" + gi)

    rel = "src/data/object_events/object_event_graphics_info_pointers.h"
    t = le(rel)
    so_uma_vez(t, rel)
    ex = "// %s\n" % MARCA
    ex += "".join("extern const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_%s%s;\n"
                  % (u.capitalize(), camel(b)) for u, b, *_ in npcs)
    ex += "// %s\n" % FIM
    t = insere_antes(t, "const struct ObjectEventGraphicsInfo *const gObjectEventGraphicsInfoPointers[NUM_OBJ_EVENT_GFX] = {\n", ex, rel)
    tab = "    // %s\n" % MARCA
    tab += "".join("    [OBJ_EVENT_GFX_%s_%s] = &gObjectEventGraphicsInfo_%s%s,\n" % (u, b, u.capitalize(), camel(b))
                   for u, b, *_ in npcs)
    tab += "    // %s\n" % FIM
    i = t.index("gObjectEventGraphicsInfoPointers[NUM_OBJ_EVENT_GFX] = {\n")
    j = t.index("\n};\n", i) + 1
    t = t[:j] + tab + t[j:]
    grava(rel, t)

    rel = "src/event_object_movement.c"
    t = le(rel)
    so_uma_vez(t, rel)
    linhas = "    // %s: sem estas linhas LoadObjectEventPalette não acha o tag e o sprite\n" % MARCA
    linhas += "    // desenha com a paleta de outro objeto.\n"
    for u, b, *_ in npcs:
        linhas += "    {gObjectEventPal_%s%s, OBJ_EVENT_PAL_TAG_%s_%s},\n" % (u.capitalize(), camel(b), u, b)
    linhas += "    // %s\n" % FIM
    # ANTES do terminador da tabela (`#ifdef BUGFIX {NULL, NONE} #else {} #endif`): entrada
    # depois dele nunca seria achada, e FindObjectEventPaletteIndexByTag pararia nele.
    t = insere_antes(t, "#ifdef BUGFIX\n    {NULL,                                  OBJ_EVENT_PAL_TAG_NONE},\n", linhas, rel)
    grava(rel, t)
    resumo["npcs"] = {"galar": sum(1 for n in npcs if n[0] == "GALAR"),
                      "unova": sum(1 for n in npcs if n[0] == "UNOVA")}

    # ------------------------------------------------------------------ 3. fundos de batalha
    stems = sorted(f for f in os.listdir(os.path.join(FONTE, "galar", "fundos")) if f.startswith("galar_"))
    if set(stems) != set(FUNDOS):
        die("fundos diferentes do esperado: %s" % sorted(set(stems) ^ set(FUNDOS)))
    be = le("src/data/battle_environment.h")

    def molde(nome):
        m = re.search(r"    \[BATTLE_ENVIRONMENT_%s\] =\n    \{.*?\n    \},\n" % nome, be, re.S)
        if not m:
            die("ambiente-molde %s não achado" % nome)
        return m.group(0)

    enum_c, gfx_c, ext_c, ent_c = [], [], [], []
    for pasta in sorted(FUNDOS):
        ing, molde_nome = FUNDOS[pasta]
        sim = "Galar" + camel(ing)
        dest = "graphics/battle_environment/galar_%s" % ing.lower()
        for a in ("tiles.png", "anim_tiles.png", "map.bin", "anim_map.bin", "palette.pal"):
            copia(os.path.join(FONTE, "galar", "fundos", pasta, a), dest + "/" + a)
        enum_c.append("    BATTLE_ENVIRONMENT_GALAR_%s,\n" % ing)
        gfx_c.append(
            'const u32 gBattleEnvironmentTiles_{s}[] = INCGFX_U32("{d}/tiles.png", ".4bpp.smol");\n'
            'const u32 gBattleEnvironmentTilemap_{s}[] = INCGFX_U32("{d}/map.bin", ".smolTM");\n'
            'const u16 gBattleEnvironmentPalette_{s}[] = INCGFX_U16("{d}/palette.pal", ".gbapal");\n'
            'const u32 gBattleEnvironmentAnimTiles_{s}[] = INCGFX_U32("{d}/anim_tiles.png", ".4bpp.smol");\n'
            'const u32 gBattleEnvironmentAnimTilemap_{s}[] = INCGFX_U32("{d}/anim_map.bin", ".smolTM");\n'.format(s=sim, d=dest))
        ext_c.append(
            "extern const u32 gBattleEnvironmentTiles_{s}[];\nextern const u32 gBattleEnvironmentTilemap_{s}[];\n"
            "extern const u16 gBattleEnvironmentPalette_{s}[];\nextern const u32 gBattleEnvironmentAnimTiles_{s}[];\n"
            "extern const u32 gBattleEnvironmentAnimTilemap_{s}[];\n".format(s=sim))
        # entrada: regras de golpe do molde, arte nova
        m = molde(molde_nome)
        m = re.sub(r"    \[BATTLE_ENVIRONMENT_%s\] =" % molde_nome, "    [BATTLE_ENVIRONMENT_GALAR_%s] =" % ing, m)
        m = re.sub(r'\.name = _\("[^"]*"\)', '.name = _("Galar %s")' % ing.title().replace("_", " "), m)
        slide = re.search(r"\.battleIntroSlide = ([A-Za-z0-9_]+),", m)
        slide = slide.group(1) if slide else "BUILDING_BATTLE_INTRO_SLIDE"
        m = re.sub(r"        \.(entry|background|palette|battleIntroSlide) = .*\n", "", m)
        m = m.rstrip()
        assert m.endswith("},")
        m = m[:-2].rstrip() + "\n" + (
            "        .entry = ENVIRONMENT_ENTRY(%s),\n"
            "        .background = ENVIRONMENT_BACKGROUND(%s),\n"
            "        .palette = gBattleEnvironmentPalette_%s,\n"
            "        .battleIntroSlide = %s,\n    },\n\n") % (sim, sim, sim, slide)
        ent_c.append(m)

    rel = "include/constants/battle.h"
    t = le(rel)
    so_uma_vez(t, rel)
    t = insere_antes(t, "    BATTLE_ENVIRONMENT_COUNT,\n",
                     "    // %s (ambientes de Galar, arte da fase 1)\n" % MARCA + "".join(enum_c) + "    // %s\n" % FIM, rel)
    grava(rel, t)

    rel = "src/data/graphics/battle_environment.h"
    t = le(rel)
    so_uma_vez(t, rel)
    grava(rel, t.rstrip("\n") + "\n\n// %s\n" % MARCA + "\n".join(gfx_c) + "// %s\n" % FIM)

    rel = "include/graphics.h"
    t = le(rel)
    so_uma_vez(t, rel)
    ancora = "extern const u16 gBattleEnvironmentPalette_Cave[];\n"
    t = insere_antes(t, ancora, "// %s\n" % MARCA + "".join(ext_c) + "// %s\n" % FIM, rel)
    grava(rel, t)

    rel = "src/data/battle_environment.h"
    so_uma_vez(be, rel)
    i = be.index("const struct BattleEnvironment gBattleEnvironmentInfo[BATTLE_ENVIRONMENT_COUNT] =")
    j = be.index("\n};\n", i) + 1
    be = be[:j] + "\n    // %s\n" % MARCA + "".join(ent_c).rstrip("\n") + "\n    // %s\n" % FIM + be[j:]
    grava(rel, be)
    resumo["fundos"] = len(FUNDOS)

    # ------------------------------------------------------------------ 4. mapa-múndi e insígnias (só cópia)
    for a in ("map_galar.png", "map_galar.pal", "map_galar.bin"):
        copia(os.path.join(FONTE, "galar", "mapa", a), "graphics/pokenav/region_map/" + a)
    copia(os.path.join(FONTE, "galar", "insignias", "badges_galar.png"), "graphics/trainer_card/galar/badges.png")
    resumo["mapa_insignias"] = "copiados, sem ligar ao motor"

    print(json.dumps(resumo, ensure_ascii=False))


if __name__ == "__main__":
    main()
