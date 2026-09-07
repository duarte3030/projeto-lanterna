#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Importa o pacote de trilhas de Johto (HGSS) e de Sinnoh (DPPt/Platinum).

POR QUE ESTE SCRIPT EXISTE
--------------------------
Trazer uma faixa para esta base é mecânico, mas são SETE arquivos por faixa e
qualquer um deles esquecido falha de um jeito diferente e caro:

1. o `.mid` em `sound/songs/midi/` (o `Makefile` faz wildcard, então o `.o`
   nasce sozinho);
2. a linha em `sound/songs/midi/midi.cfg` com os argumentos do `mid2agb`. SEM
   ela o build passa com um `warning` perdido no meio de 38 mil linhas de log e
   só quebra no LINK;
3. a linha `song <nome>, MUSIC_PLAYER_*, <prio>` em `sound/song_table.inc`, na
   POSIÇÃO exata do id;
4. o `#define MUS_<NOME> <id>` em `include/constants/songs.h`, casando com a
   posição da tabela. Índice deslocado NÃO quebra o build: só faz a cidade
   tocar a música da caverna;
5. o voicegroup, que aqui é por NOME (`voice_group hgss` -> símbolo
   `voicegroup_hgss`, argumento `-G_hgss`) e na fonte é numerado (`-G229`);
6. as amostras `.aif` novas em `sound/direct_sound_samples/`;
7. o símbolo de cada amostra em `sound/direct_sound_data.inc`.

Fazer isso à mão 170 vezes é onde o erro nasce. O script é idempotente: rodar
duas vezes não duplica nada.

FONTE
-----
`/Users/duarte/Projetos/pokemon-claude/fontes-mapas/hns` (Pokémon Heart & Soul,
de Lil Dill), que por sua vez usa o pacote de sequências do CyanSMP64. Nenhuma
das fontes declara licença e o material é copyright de Nintendo/Game Freak/
Creatures: o regime é o do ecossistema pret, distribui-se patch, nunca ROM.

USO
---
    python3 dev_scripts/importa_musica_ds.py            # importa de verdade
    python3 dev_scripts/importa_musica_ds.py --dry-run  # só diz o que faria
"""

import os
import re
import shutil
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTE = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/hns"

MIDI_DIR = os.path.join(RAIZ, "sound", "songs", "midi")
MIDI_CFG = os.path.join(MIDI_DIR, "midi.cfg")
SONG_TABLE = os.path.join(RAIZ, "sound", "song_table.inc")
SONGS_H = os.path.join(RAIZ, "include", "constants", "songs.h")
VG_DIR = os.path.join(RAIZ, "sound", "voicegroups")
VG_INDEX = os.path.join(RAIZ, "sound", "voice_groups.inc")
SAMPLES_DIR = os.path.join(RAIZ, "sound", "direct_sound_samples")
DSD = os.path.join(RAIZ, "sound", "direct_sound_data.inc")
KEYSPLIT_DS = os.path.join(RAIZ, "sound", "keysplit_tables_ds.inc")
SOUND_DATA_S = os.path.join(RAIZ, "data", "sound_data.s")

MARCA = "importa_musica_ds.py"

# ---------------------------------------------------------------------------
# A LISTA CURADA
# ---------------------------------------------------------------------------
# Regra da curadoria: entra a faixa que ALGUM mapa ou ALGUMA batalha vai tocar.
#
# Johto: as 33 primeiras são exatamente os apelidos `MUS_HG_*` que os 236
# `map.json` de Johto já citam hoje (contados com Python sobre o campo `music`),
# mais 5 que os `scripts.inc` de Johto já chamam por nome, mais 2 de mapa que a
# parte B vai pendurar (Victory Road e Liga), mais o conjunto de batalha e
# vitória que a PARTE C precisa que exista em `songs.h`.
#
# Sinnoh: os 230 mapas de Sinnoh existem hoje sem nenhuma faixa própria. As
# cidades e rotas vêm com o par `_DAY`/`_NIGHT` inteiro, por ordem desta onda
# (o plano recomendava só o dia; a ordem da onda mandou trazer os dois lados e
# dizer quanto custou). Cada faixa aqui tem mapa correspondente conferido em
# `data/maps/map_groups.json`.

JOHTO_MAPA = [
    # cidades (7 temas para as 10 cidades; ver JOHTO_APELIDOS abaixo)
    "new_bark", "cherrygrove", "violet", "azalea", "goldenrod", "ecruteak",
    "cianwood",
    # rotas
    "route26", "route29", "route30", "route34", "route38", "route42", "route47",
    # masmorras
    "sprout_tower", "union_cave", "ruins_of_alph", "national_park",
    "burned_tower", "bell_tower", "lighthouse", "ice_path", "dragons_den",
    "rock_tunnel", "victory_road",
    # interiores
    "poke_center", "poke_mart", "gym", "elm_lab", "dance_theater",
    "game_corner", "safari_zone_gate", "ss_aqua", "pokemon_league",
    # cenas que os scripts.inc de Johto já chamam pelo nome
    "rocket_takeover", "kimono_girl_dance", "rival_exit", "encounter_rival",
]

JOHTO_BATALHA = [
    "vs_wild", "vs_trainer", "vs_gym_leader", "vs_rival", "vs_champion",
    "vs_rocket", "vs_ho_oh", "vs_lugia",
    "victory_wild", "victory_trainer", "victory_gym_leader",
]

# Jingles de HGSS. Decisão 24 do Gui: os jingles de Hoenn são feios e os de
# HGSS valem para o jogo INTEIRO, não só para Johto.
#
# A lista tem 15, não 33, e a razão é a regra da curadoria: só entra o jingle
# que tem uma vaga REAL no motor desta base. `src/sound.c` tem 18 vagas em
# `sFanfares[]`; 15 delas ganham a versão de HGSS aqui (ver
# `dev_scripts/troca_jingles_hgss.py`, que faz a troca e traz a duração de
# cada uma medida pelo próprio HnS, não chutada). Os outros 18 jingles `ME` de
# HGSS servem sistemas que esta ROM não tem (Pokéathlon, Concurso de Insetos,
# Voltorb Flip, Pokéwalker, modo parceiro) e ficariam ocupando ROM sem tocar
# uma vez. As 3 vagas que sobram (`AWAKEN_LEGEND`, `SLOTS_JACKPOT`,
# `RG_POKE_FLUTE`) não têm equivalente de HGSS e continuam com a faixa de
# Hoenn/Kanto.
JOHTO_JINGLE = [
    "level_up", "obtain_item", "obtain_key_item", "obtain_tmhm",
    "obtain_badge", "obtain_berry", "obtain_b_points", "obtain_castle_points",
    "evolved", "heal", "move_deleted", "pokegear_registered",
    "win_minigame", "card_flip_game_over", "dex_rating_4",
]

# Os jingles vão no player SE2, que é o dos fanfarras nesta base (medido em
# sound/song_table.inc:376: `song mus_level_up, MUSIC_PLAYER_SE2, 2`).
# ATENÇÃO: a ordem da onda dizia SE1; medido, é SE2, e é exatamente por isso
# que NUM_TRACKS_SE2 subiu de 9 para 11 em sound/music_player_table.inc.
SE2 = set(JOHTO_JINGLE)

SINNOH_PAR = [  # entram como <nome>_day e <nome>_night
    "twinleaf", "sandgem", "jubilife", "oreburgh", "floaroma", "eterna",
    "hearthome", "solaceon", "veilstone", "canalave", "snowpoint", "sunyshore",
    "fight_area", "valor_lakefront", "pokemon_league", "poke_center",
    "route201", "route203", "route205", "route206", "route209", "route210",
    "route216", "route225", "route228",
]

SINNOH_UNICO = [
    "oreburgh_gate", "oreburgh_mine", "eterna_forest", "old_chateau",
    "mt_coronet", "lake", "lake_caverns", "lake_event", "stark_mountain",
    "spear_pillar", "galactic_hq", "galactic_hq_basement",
    "galactic_eterna_building", "victory_road", "inside_pokemon_league",
    "hall_of_fame_room", "poke_mart", "gym", "game_corner", "rowan_lab",
]

SINNOH_BATALHA = [
    "vs_wild", "vs_trainer", "vs_gym_leader", "vs_rival", "vs_champion",
    "vs_elite_four", "vs_galactic", "vs_galactic_commander",
    "vs_galactic_boss", "vs_dialga_palkia", "vs_uxie_mesprit_azelf",
    "vs_legend",
    "victory_wild", "victory_trainer", "victory_gym_leader",
    "victory_elite_four", "victory_champion", "victory_galactic",
    "victory_road",
]

# Platinum. `mus_pl_fight_area_day` entra porque um `map.json` de Johto já cita
# `MUS_PL_FIGHT_AREA_DAY` hoje; o resto é o Mundo Distorcido, que tem 10 mapas
# em `data/maps` (DistortionWorld*) e hoje toca faixa de Hoenn.
PLATINUM = [
    "fight_area_day", "distortion_world", "vs_giratina", "giratina_appears_1",
    "looker",
]

# As 3 cidades de Johto e as 2 de Sinnoh que NÃO têm tema próprio no jogo
# original. A atribuição abaixo não é chute: foi lida no `map.json` da própria
# fonte (`fontes-mapas/hns/data/maps/OlivineCity/map.json` -> MUS_HG_VIOLET,
# MahoganyTown -> MUS_HG_CHERRYGROVE, BlackthornCity -> MUS_HG_AZALEA).
APELIDOS = {
    "MUS_HG_OLIVINE": "MUS_HG_VIOLET",
    "MUS_HG_MAHOGANY": "MUS_HG_CHERRYGROVE",
    "MUS_HG_BLACKTHORN": "MUS_HG_AZALEA",
    # Sinnoh: Pastoria e Celestic não têm tema em DPPt.
    "MUS_DP_PASTORIA_DAY": "MUS_DP_SOLACEON_DAY",
    "MUS_DP_PASTORIA_NIGHT": "MUS_DP_SOLACEON_NIGHT",
    "MUS_DP_CELESTIC_DAY": "MUS_DP_SOLACEON_DAY",
    "MUS_DP_CELESTIC_NIGHT": "MUS_DP_SOLACEON_NIGHT",
}

# Renome dos voicegroups: a fonte numera, esta base nomeia.
VG_NOME = {229: "hgss", 191: "dppt"}


def nome_vg(n):
    return VG_NOME.get(n, "ds_%d" % n)


def lista_faixas():
    """Devolve [(nome_do_arquivo_sem_extensao, player)] na ordem de entrada."""
    faixas = []
    for n in JOHTO_MAPA + JOHTO_BATALHA:
        faixas.append(("mus_hg_" + n, "MUSIC_PLAYER_BGM", 0))
    for n in JOHTO_JINGLE:
        if n in SE2:
            faixas.append(("mus_hg_" + n, "MUSIC_PLAYER_SE2", 2))
        else:
            faixas.append(("mus_hg_" + n, "MUSIC_PLAYER_BGM", 0))
    for n in SINNOH_PAR:
        faixas.append(("mus_dp_%s_day" % n, "MUSIC_PLAYER_BGM", 0))
        faixas.append(("mus_dp_%s_night" % n, "MUSIC_PLAYER_BGM", 0))
    for n in SINNOH_UNICO + SINNOH_BATALHA:
        faixas.append(("mus_dp_" + n, "MUSIC_PLAYER_BGM", 0))
    for n in PLATINUM:
        faixas.append(("mus_pl_" + n, "MUSIC_PLAYER_BGM", 0))
    # Uma faixa pode aparecer em duas listas por descuido (victory_road é
    # masmorra E vitória em Sinnoh). Duas linhas iguais em song_table.inc
    # empurram TODOS os ids seguintes e o make ainda reclama de regra dupla
    # no midi.cfg. Dedupe, mantendo a ordem da primeira aparição.
    vistos, unicas = set(), []
    for f in faixas:
        if f[0] in vistos:
            continue
        vistos.add(f[0])
        unicas.append(f)
    return unicas


def regras_mid2agb():
    txt = open(os.path.join(FONTE, "songs.mk")).read()
    return dict(re.findall(
        r"\$\(MID_SUBDIR\)/(\w+)\.s:.*?\n\t\$\(MID\) \$< \$@ (.*)", txt))


def fecho_voicegroups(raizes):
    """Resolve, em cadeia, todos os voicegroups que as raízes alcançam."""
    vistos = set()
    fila = list(raizes)
    conteudo = {}
    while fila:
        n = fila.pop()
        if n in vistos:
            continue
        vistos.add(n)
        p = os.path.join(FONTE, "sound", "voicegroups", "voicegroup%d.inc" % n)
        if not os.path.exists(p):
            raise SystemExit("voicegroup%d.inc não existe na fonte" % n)
        txt = open(p).read()
        conteudo[n] = txt
        for m in re.finditer(r"\bvoicegroup(\d+)\b", txt):
            k = int(m.group(1))
            if k not in vistos:
                fila.append(k)
    return conteudo


def main():
    seco = "--dry-run" in sys.argv
    faixas = lista_faixas()
    regras = regras_mid2agb()

    # --- 0. conferências de sanidade antes de tocar em qualquer arquivo -----
    faltando = [f for f, _, _ in faixas
                if not os.path.exists(
                    os.path.join(FONTE, "sound", "songs", "midi", f + ".mid"))]
    if faltando:
        raise SystemExit("faixas sem .mid na fonte: %s" % ", ".join(faltando))
    sem_regra = [f for f, _, _ in faixas if f not in regras]
    if sem_regra:
        raise SystemExit("faixas sem regra em songs.mk: %s" % ", ".join(sem_regra))

    vgs = fecho_voicegroups([191, 229])
    print("faixas curadas: %d  voicegroups no fecho: %d" % (len(faixas), len(vgs)))

    # --- 1. amostras que os voicegroups pedem ------------------------------
    simbolos = set()
    for txt in vgs.values():
        simbolos |= set(re.findall(r"DirectSoundWaveData_(\w+)", txt))
    ja_existem = set(re.findall(r"DirectSoundWaveData_(\w+)::",
                                open(DSD).read()))
    novos = sorted(simbolos - ja_existem)
    colididos = sorted(simbolos & ja_existem)
    print("amostras pedidas: %d, já no repo: %d, novas: %d"
          % (len(simbolos), len(colididos), len(novos)))
    if colididos:
        print("  reaproveitadas (mesmo símbolo já existe aqui): %s"
              % ", ".join(colididos))

    # o .inc da fonte diz qual arquivo cada símbolo usa
    fonte_dsd = open(os.path.join(FONTE, "sound", "direct_sound_data.inc")).read()
    arquivo_de = dict(re.findall(
        r"DirectSoundWaveData_(\w+)::\s*\n\s*\.incbin \"sound/direct_sound_samples/(\S+?)\.bin\"",
        fonte_dsd))
    sem_arquivo = [s for s in novos if s not in arquivo_de]
    if sem_arquivo:
        raise SystemExit("amostras sem entrada no .inc da fonte: %s"
                         % ", ".join(sem_arquivo))

    if seco:
        print("(--dry-run) pararia aqui")
        return

    # --- 2. copiar .mid ----------------------------------------------------
    for f, _, _ in faixas:
        shutil.copy2(os.path.join(FONTE, "sound", "songs", "midi", f + ".mid"),
                     os.path.join(MIDI_DIR, f + ".mid"))

    # --- 3. midi.cfg -------------------------------------------------------
    linhas = [l for l in open(MIDI_CFG).read().splitlines() if l.strip()]
    ja = {l.split(":")[0] for l in linhas}
    for f, _, _ in faixas:
        if f + ".mid" in ja:
            continue
        args = regras[f]
        args = re.sub(r"-G(\d+)",
                      lambda m: "-G_" + nome_vg(int(m.group(1))), args)
        linhas.append("%-40s %s" % (f + ".mid:", args))
    linhas.sort()
    open(MIDI_CFG, "w").write("\n".join(linhas) + "\n")

    # --- 4. voicegroups ----------------------------------------------------
    destino = os.path.join(VG_DIR, "ds")
    os.makedirs(destino, exist_ok=True)
    for n in sorted(vgs):
        txt = vgs[n]
        # o rótulo do próprio grupo vira a chamada da macro `voice_group`
        txt = re.sub(r"^voicegroup%d::.*$" % n,
                     "\tvoice_group %s" % nome_vg(n), txt, flags=re.M)
        # as referências viram o símbolo nomeado
        txt = re.sub(r"\bvoicegroup(\d+)\b",
                     lambda m: "voicegroup_" + nome_vg(int(m.group(1))), txt)
        cab = ("@ Importado de %s/sound/voicegroups/voicegroup%d.inc\n"
               "@ por dev_scripts/%s. Renomeado de numerado para nomeado,\n"
               "@ que é a convenção desta base (`voice_group nome` gera o\n"
               "@ símbolo `voicegroup_nome`, que o mid2agb recebe como -G_nome).\n"
               % ("fontes-mapas/hns", n, MARCA))
        open(os.path.join(destino, nome_vg(n) + ".inc"), "w").write(cab + txt)

    idx = open(VG_INDEX).read()
    if MARCA not in idx:
        bloco = ["", "@ >>> soundfont de HGSS e de DPPt (%s) >>>" % MARCA]
        for n in sorted(vgs):
            bloco.append('.include "sound/voicegroups/ds/%s.inc"' % nome_vg(n))
        bloco.append("@ <<< soundfont de HGSS e de DPPt (%s) <<<" % MARCA)
        open(VG_INDEX, "w").write(idx.rstrip("\n") + "\n" + "\n".join(bloco) + "\n")

    # --- 5. tabelas de keysplit da fonte ----------------------------------
    ks = open(os.path.join(FONTE, "sound", "keysplit_tables.inc")).read()
    # só o que é definição de KeySplitTableN (a fonte não usa a macro `keysplit`)
    corte = ks.index(".set KeySplitTable1,")
    cab = ("@ Tabelas de keysplit do pacote de HGSS/DPPt, importadas de\n"
           "@ fontes-mapas/hns/sound/keysplit_tables.inc por dev_scripts/%s.\n"
           "@ Ficam em arquivo separado porque a fonte usa a forma crua\n"
           "@ `.set KeySplitTableN, . - 36` e esta base usa a macro `keysplit`\n"
           "@ com nome (keysplit_piano e afins). Os nomes não colidem.\n\n"
           % MARCA)
    open(KEYSPLIT_DS, "w").write(cab + ks[corte:])

    sd = open(SOUND_DATA_S).read()
    if "keysplit_tables_ds.inc" not in sd:
        sd = sd.replace('\t.include "sound/keysplit_tables.inc"\n',
                        '\t.include "sound/keysplit_tables.inc"\n'
                        '\t.include "sound/keysplit_tables_ds.inc"\n', 1)
        open(SOUND_DATA_S, "w").write(sd)

    # --- 6. amostras -------------------------------------------------------
    for s in novos:
        arq = arquivo_de[s]
        orig = os.path.join(FONTE, "sound", "direct_sound_samples", arq + ".aif")
        if not os.path.exists(orig):
            raise SystemExit("amostra %s.aif não está na fonte" % arq)
        shutil.copy2(orig, os.path.join(SAMPLES_DIR, arq + ".aif"))

    dsd = open(DSD).read()
    if MARCA not in dsd:
        bloco = ["", "@ >>> amostras de HGSS e de DPPt (%s) >>>" % MARCA]
        for s in novos:
            bloco.append("\t.align 2")
            bloco.append("DirectSoundWaveData_%s::" % s)
            bloco.append('\t.incbin "sound/direct_sound_samples/%s.bin"'
                         % arquivo_de[s])
            bloco.append("")
        bloco.append("@ <<< amostras de HGSS e de DPPt (%s) <<<" % MARCA)
        open(DSD, "w").write(dsd.rstrip("\n") + "\n" + "\n".join(bloco) + "\n")

    # --- 7. song_table.inc e songs.h ---------------------------------------
    st = open(SONG_TABLE).read()
    ja_tab = set(re.findall(r"^\tsong (\w+),", st, flags=re.M))
    novas_faixas = [f for f in faixas if f[0] not in ja_tab]
    if novas_faixas:
        # o id de cada faixa nova é a posição dela no fim da tabela
        base = len(re.findall(r"^\tsong ", st, flags=re.M))
        linhas_st = ["", "@ >>> faixas de HGSS e de DPPt (%s) >>>" % MARCA]
        defines = ["", "// >>> faixas de HGSS e de DPPt (%s) >>>" % MARCA]
        for i, (f, player, prio) in enumerate(novas_faixas):
            linhas_st.append("\tsong %s, %s, %d" % (f, player, prio))
            defines.append("#define %-34s %d" % (f.upper(), base + i))
        linhas_st.append("@ <<< faixas de HGSS e de DPPt (%s) <<<" % MARCA)
        defines.append("// <<< faixas de HGSS e de DPPt (%s) <<<" % MARCA)
        marcador = "\n\t.align 2\ndummy_song_header:"
        assert marcador in st
        st = st.replace(marcador, "\n".join(linhas_st) + marcador, 1)
        open(SONG_TABLE, "w").write(st)

        sh = open(SONGS_H).read()
        extra = ["", "// Apelidos das cidades sem tema próprio no jogo original.",
                 "// A atribuição saiu do map.json da própria fonte, não de memória",
                 "// (fontes-mapas/hns/data/maps/OlivineCity/map.json e vizinhos)."]
        for k, v in APELIDOS.items():
            extra.append("#define %-34s %s" % (k, v))
        extra.append("")
        # O bloco tem de entrar ANTES da lista de apelidos `#ifndef`: assim cada
        # `#ifndef MUS_HG_*` que existe hoje fica inerte sozinho, sem apagar uma
        # linha do que a rodada 13 escreveu, e o apelido volta a valer se algum
        # dia a faixa real sair.
        ancora = "#ifndef MUS_HG_BELL_TOWER"
        assert ancora in sh
        sh = sh.replace(ancora, "\n".join(defines + extra) + "\n" + ancora, 1)
        # `MUS_HG_SS_AQUA` era definido sem guarda no fim do arquivo por
        # dev_scripts/import_ssaqua.py; agora existe faixa real e a linha antiga
        # redefiniria o id. Vira `#ifndef` para virar inerte.
        velho = ("// >>> S.S. Aqua (dev_scripts/import_ssaqua.py) >>>\n"
                 "#define MUS_HG_SS_AQUA MUS_ABANDONED_SHIP\n"
                 "// <<< S.S. Aqua (dev_scripts/import_ssaqua.py) <<<")
        if velho in sh:
            sh = sh.replace(velho,
                            "// >>> S.S. Aqua (dev_scripts/import_ssaqua.py) >>>\n"
                            "// Inerte desde 06/09/2026: mus_hg_ss_aqua entrou como faixa real.\n"
                            "#ifndef MUS_HG_SS_AQUA\n"
                            "#define MUS_HG_SS_AQUA MUS_ABANDONED_SHIP\n"
                            "#endif\n"
                            "// <<< S.S. Aqua (dev_scripts/import_ssaqua.py) <<<", 1)
        open(SONGS_H, "w").write(sh)

    print("pronto: %d faixas novas, %d amostras novas, %d voicegroups"
          % (len(novas_faixas), len(novos), len(vgs)))


if __name__ == "__main__":
    main()
