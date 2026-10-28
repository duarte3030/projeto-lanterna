#!/usr/bin/env python3
"""Integra no cartucho 2 os retratos de treinador aprovados da fase 2 (decisão 153, 28/10/2026).

Entram SÓ assets e registros do motor, do mesmo jeito que a fase 1 (integra_arte_fase1.py):
  retratos 64x64, 4bpp, 15 cores + transparente -> TRAINER_PIC_<REGIAO>_<PERSONAGEM>.
Nenhum treinador passa a usá-los (Kalos, Alola e Paldea ainda não têm mapa).

Quais entram: `dev_scripts/arte_fase2_manifesto.json` (gerado por fase2-arte/_scripts/manifesto_f2.py, que também
registra por que cada duplicata ficou de fora: mesmo personagem já com retrato da fase 1, silhueta igual ou arquivo
repetido entre pacotes).

Idempotência: se o marcador `>>> arte fase 2` já está num arquivo, o script PARA sem tocar em nada.
Uso (da raiz do repo):  python3 dev_scripts/integra_arte_fase2.py [--fonte DIR]
"""
import argparse
import json
import os
import shutil
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTE = os.path.expanduser("~/Projetos/pokemon-claude/fontes-mapas/prd-assets/fase2-arte")
MARCA = ">>> arte fase 2"
FIM = "<<< fim da arte fase 2"


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


def camel(base):
    return "".join(p.capitalize() for p in base.split("_"))


def confere_png(caminho, w, h):
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
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonte", default=FONTE)
    fonte = ap.parse_args().fonte
    manifesto = json.load(open(os.path.join(RAIZ, "dev_scripts", "arte_fase2_manifesto.json"), encoding="utf-8"))
    itens = [i for i in manifesto if i["entra"]]
    consts = [i["const"] for i in itens]
    if len(set(consts)) != len(consts):
        die("nome de retrato duplicado")

    rel = "include/constants/trainers.h"
    t = le(rel)
    so_uma_vez(t, rel)
    for c in consts:
        if "    TRAINER_PIC_%s,\n" % c in t:
            die("TRAINER_PIC_%s já existe" % c)
    bloco = "    // %s (dev_scripts/integra_arte_fase2.py)\n" % MARCA
    bloco += "".join("    TRAINER_PIC_%s,\n" % c for c in consts)
    bloco += "    // %s\n" % FIM
    t = insere_antes(t, "    TRAINER_PIC_COUNT,\n", bloco, rel)
    grava(rel, t)

    rel = "src/data/graphics/trainers.h"
    t = le(rel)
    so_uma_vez(t, rel)
    inc = "// %s: retratos de Kalos, Alola, Paldea e extras (PNG 64x64, 4bpp, paleta de 16 cores no próprio PNG)\n" % MARCA
    ent = "    // %s\n" % MARCA
    simbolos = set()
    for i in itens:
        c = i["const"]
        sim = camel(c)
        if sim in simbolos:
            die("símbolo duplicado " + sim)
        simbolos.add(sim)
        orig = os.path.join(fonte, i["pasta"], "retratos", i["stem"] + ".png")
        confere_png(orig, 64, 64)
        arq = "graphics/trainers/front_pics/%s.png" % c.lower()
        copia(orig, arq)
        inc += 'const u32 gTrainerFrontPic_%s[] = INCGFX_U32("%s", ".4bpp.smol");\n' % (sim, arq)
        inc += 'const u16 gTrainerPalette_%s[] = INCGFX_U16("%s", ".gbapal");\n' % (sim, arq)
        ent += "    [TRAINER_PIC_%s] =\n    {\n        .frontPic = TRAINER_FRONT_PIC(gTrainerFrontPic_%s, gTrainerPalette_%s),\n    },\n" % (c, sim, sim)
    inc += "// %s\n\n" % FIM
    ent += "    // %s\n" % FIM
    t = insere_antes(t, "const struct TrainerPicInfo gTrainerPicInfo[TRAINER_PIC_COUNT] =\n", inc, rel)
    i = t.index("const struct TrainerPicInfo gTrainerPicInfo[TRAINER_PIC_COUNT] =\n")
    j = t.index("\n};\n", i) + 1
    t = t[:j] + ent + t[j:]
    grava(rel, t)

    por = {}
    for i in itens:
        por[i["regiao"]] = por.get(i["regiao"], 0) + 1
    print(json.dumps({"retratos": por, "total": len(itens)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
