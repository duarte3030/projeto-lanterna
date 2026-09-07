#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Troca os jingles de Hoenn pelos de HGSS em `src/sound.c`.

POR QUE ESTE SCRIPT EXISTE
--------------------------
Decisão 24 do Gui: os jingles de Hoenn são feios e ele quer os de HGSS no jogo
INTEIRO, não só em Johto. O ponto de troca é um só, a tabela `sFanfares[]` de
`src/sound.c`, e ela tem 18 vagas.

O que este script NÃO faz de cabeça: a DURAÇÃO. O segundo campo de cada linha
é por quantos quadros o motor segura a música de fundo antes de devolvê-la; se
ele não casar com a faixa nova, ou a trilha do mapa volta por cima do jingle,
ou fica um silêncio no fim. As durações abaixo foram LIDAS do `sFanfares[]` do
próprio Pokémon Heart & Soul
(`fontes-mapas/hns/src/sound.c`), que já toca estas faixas em produção.

Três vagas ficam como estão porque HGSS não tem faixa equivalente:
`FANFARE_AWAKEN_LEGEND` (despertar dos Regis, evento de Hoenn),
`FANFARE_SLOTS_JACKPOT` e `FANFARE_RG_POKE_FLUTE` (a `mus_hg_radio_poke_flute`
é faixa de rádio contínua no HnS, não jingle).

USO
---
    python3 dev_scripts/troca_jingles_hgss.py
    python3 dev_scripts/troca_jingles_hgss.py --dry-run
"""

import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOUND_C = os.path.join(RAIZ, "src", "sound.c")

# vaga -> (faixa de HGSS, duração em quadros medida no sFanfares do HnS)
TROCA = {
    "FANFARE_LEVEL_UP":            ("MUS_HG_LEVEL_UP", 80),
    "FANFARE_OBTAIN_ITEM":         ("MUS_HG_OBTAIN_ITEM", 160),
    "FANFARE_EVOLVED":             ("MUS_HG_EVOLVED", 240),
    "FANFARE_OBTAIN_TMHM":         ("MUS_HG_OBTAIN_TMHM", 220),
    "FANFARE_HEAL":                ("MUS_HG_HEAL", 160),
    "FANFARE_OBTAIN_BADGE":        ("MUS_HG_OBTAIN_BADGE", 340),
    "FANFARE_MOVE_DELETED":        ("MUS_HG_MOVE_DELETED", 180),
    "FANFARE_OBTAIN_BERRY":        ("MUS_HG_OBTAIN_BERRY", 120),
    "FANFARE_SLOTS_WIN":           ("MUS_HG_WIN_MINIGAME", 230),
    "FANFARE_TOO_BAD":             ("MUS_HG_CARD_FLIP_GAME_OVER", 240),
    "FANFARE_RG_OBTAIN_KEY_ITEM":  ("MUS_HG_OBTAIN_KEY_ITEM", 170),
    # HGSS tem 6 avaliações de Dex por faixa de completude; este motor tem UMA
    # vaga, então entra a do meio (a de HnS para o mesmo caso).
    "FANFARE_RG_DEX_RATING":       ("MUS_HG_DEX_RATING_4", 210),
    "FANFARE_OBTAIN_B_POINTS":     ("MUS_HG_OBTAIN_B_POINTS", 264),
    "FANFARE_OBTAIN_SYMBOL":       ("MUS_HG_OBTAIN_CASTLE_POINTS", 200),
    "FANFARE_REGISTER_MATCH_CALL": ("MUS_HG_POKEGEAR_REGISTERED", 185),
}


def main():
    seco = "--dry-run" in sys.argv
    texto = open(SOUND_C, encoding="utf-8").read()
    trocadas = 0
    for vaga, (faixa, dur) in TROCA.items():
        padrao = re.compile(
            r"(\[%s\]\s*=\s*\{\s*)(MUS_\w+)(,\s*)(\d+)(\s*\})" % vaga)
        m = padrao.search(texto)
        if not m:
            raise SystemExit("vaga %s nao encontrada em src/sound.c" % vaga)
        if m.group(2) == faixa:
            continue
        texto = padrao.sub(lambda mm: mm.group(1) + faixa + mm.group(3)
                           + str(dur) + mm.group(5), texto, count=1)
        trocadas += 1
        print("%-30s %s (%s) -> %s (%d)"
              % (vaga, m.group(2), m.group(4), faixa, dur))
    nota = ("// Jingles de HGSS (06/09/2026, onda 5 do cartucho 1). Decisao 24\n"
            "// do Gui: os jingles de Hoenn sao feios e os de HGSS valem para o\n"
            "// jogo inteiro. As duracoes vieram do sFanfares[] do Pokemon Heart\n"
            "// & Soul, que ja toca estas faixas; nao foram chutadas. Trocar\n"
            "// aqui e o unico ponto: PlayFanfare le esta tabela.\n"
            "static const struct Fanfare sFanfares[] = {")
    if "Decisao 24" not in texto:
        texto = texto.replace("static const struct Fanfare sFanfares[] = {",
                              nota, 1)
    if seco:
        print("(--dry-run) nada gravado; %d vagas mudariam" % trocadas)
        return
    open(SOUND_C, "w", encoding="utf-8").write(texto)
    print("%d vagas trocadas em src/sound.c" % trocadas)


if __name__ == "__main__":
    main()
