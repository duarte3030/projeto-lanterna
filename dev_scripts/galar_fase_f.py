#!/usr/bin/env python3
"""FASE F para Galar: os chefes da sexta regiao entram na tabela.

    python3 dev_scripts/galar_fase_f.py            # so mede e relata
    python3 dev_scripts/galar_fase_f.py --aplicar  # escreve fase_f_chefes.json
    python3 dev_scripts/galar_fase_f.py --demo     # autoteste

Depois de `--aplicar`, quem escreve o `.party` continua sendo
`python3 dev_scripts/fase_f_chefes.py --aplicar`. Este script so ACRESCENTA
Galar aa `dev_scripts/fase_f_chefes.json`, de forma idempotente (apaga o que ja
estiver marcado como regiao `galar` e reescreve).

## A IRONIA, e ela fica registrada

Galar e a regiao do DYNAMAX. E a cota de Dynamax da Fase F (5 no jogo inteiro)
ja foi gasta em Whitney, Chuck, Norman, Roark e Cheren, e a de Terastal (6) em
Lance-2, Drake, Steven, Lucian, Cynthia e Genesis. A regra do Gui era "Dynamax e
o que eu menos gosto, deixa pouco disso", e pouco foi gasto ANTES de Galar
existir. Entao **os chefes de Galar lutam com Mega e Z**, e nenhum deles
Dinamaxa. Foi decidido assim de proposito: mexer na cota agora seria reabrir uma
regra do Gui sem ele pedir.

## Um time por PESSOA, nao por batalha

A regra de lendario da Fase F ja e por identidade ("Silver carrega o mesmo Lugia
nas quatro batalhas dele porque e a mesma pessoa"). Aqui o time INTEIRO e por
pessoa: as cinco batalhas do Hop levam o mesmo esquadrao. Isso e simplificacao
declarada, e o preco esta medido: 17 times escritos cobrem as %d batalhas.

## Nivel 255 em tudo, inclusive no chefe

Decisao do Gui de 22/08/2026: Galar e regiao plana de pos-jogo. Nao ha ace num
nivel e resto quatro abaixo; e 255 do primeiro ao sexto.

## Habilidade NAO e declarada, e isso e escolha

`src/battle_main.c` tem `assertf(abilityNum < maxAbilityNum, ...)`: habilidade
declarada errada nao e aviso, e crash em tempo de execucao. O `.party` aceita o
bloco sem a linha `Ability:` e o motor cai no slot 0, que e sempre valido. Como
nenhum destes 17 times depende de habilidade escondida para funcionar, a linha
nao e escrita. Quem quiser afinar, afina uma a uma conferindo `.abilities`.
"""
import argparse
import collections
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))

import fase_f_chefes as FF   # noqa: E402

JSON = f"{RAIZ}/dev_scripts/fase_f_chefes.json"
OPPS = f"{RAIZ}/include/constants/opponents.h"
REGIAO = "galar"
NIVEL = 255

IVS = "31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe"
EV = {"fis": "252 Atk / 252 Spe / 4 HP",
      "esp": "252 SpA / 252 Spe / 4 HP",
      "duro": "252 HP / 252 Def / 4 SpD",
      "duro_esp": "252 HP / 252 SpD / 4 Def"}
AI = ["AI_FLAG_SMART_TRAINER", "AI_FLAG_HP_AWARE", "AI_FLAG_TRY_TO_2HKO",
      "AI_FLAG_POWERFUL_STATUS", "AI_FLAG_PREDICTION", "AI_FLAG_ASSUMPTIONS",
      "AI_FLAG_KNOW_OPPONENT_PARTY", "AI_FLAG_ACE_POKEMON"]

# (especie, item, natureza, molde de EV, quatro golpes)
T = collections.namedtuple("T", "esp item nat ev golpes")


def m(*g):
    return ["MOVE_" + x for x in g]


TIMES = {
    # ---------------------------------------------------------- lideres ----
    "milo": dict(tipo="Grass", lendario="SPECIES_ZARUDE", gimmick="mega",
                 slot=4, time=[
        T("SPECIES_ELDEGOSS", "ITEM_LEFTOVERS", "NATURE_BOLD", "duro",
          m("LEECH_SEED", "GIGA_DRAIN", "SYNTHESIS", "TOXIC")),
        T("SPECIES_RILLABOOM", "ITEM_CHOICE_BAND", "NATURE_ADAMANT", "fis",
          m("WOOD_HAMMER", "KNOCK_OFF", "EARTHQUAKE", "U_TURN")),
        T("SPECIES_FERROTHORN", "ITEM_ROCKY_HELMET", "NATURE_RELAXED", "duro",
          m("SPIKES", "GYRO_BALL", "LEECH_SEED", "KNOCK_OFF")),
        T("SPECIES_WHIMSICOTT", "ITEM_FOCUS_SASH", "NATURE_TIMID", "esp",
          m("TAILWIND", "MOONBLAST", "ENERGY_BALL", "ENCORE")),
        T("SPECIES_VENUSAUR", "ITEM_VENUSAURITE", "NATURE_MODEST", "esp",
          m("SLUDGE_BOMB", "GIGA_DRAIN", "SLEEP_POWDER", "SYNTHESIS")),
        T("SPECIES_ZARUDE", "ITEM_LIFE_ORB", "NATURE_JOLLY", "fis",
          m("POWER_WHIP", "KNOCK_OFF", "CLOSE_COMBAT", "SWORDS_DANCE"))]),
    "nessa": dict(tipo="Water", lendario="SPECIES_MANAPHY", gimmick="mega",
                  slot=4, time=[
        T("SPECIES_DREDNAW", "ITEM_LIFE_ORB", "NATURE_ADAMANT", "fis",
          m("LIQUIDATION", "STONE_EDGE", "EARTHQUAKE", "SWORDS_DANCE")),
        T("SPECIES_TOXAPEX", "ITEM_BLACK_SLUDGE", "NATURE_BOLD", "duro",
          m("SCALD", "RECOVER", "TOXIC", "HAZE")),
        T("SPECIES_BARRASKEWDA", "ITEM_CHOICE_BAND", "NATURE_JOLLY", "fis",
          m("LIQUIDATION", "CLOSE_COMBAT", "WATERFALL", "AQUA_JET")),
        T("SPECIES_GYARADOS", "ITEM_LEFTOVERS", "NATURE_ADAMANT", "fis",
          m("DRAGON_DANCE", "WATERFALL", "CRUNCH", "EARTHQUAKE")),
        T("SPECIES_BLASTOISE", "ITEM_BLASTOISINITE", "NATURE_MODEST", "esp",
          m("HYDRO_PUMP", "ICE_BEAM", "DARK_PULSE", "AURA_SPHERE")),
        T("SPECIES_MANAPHY", "ITEM_LEFTOVERS", "NATURE_TIMID", "esp",
          m("TAIL_GLOW", "SURF", "ICE_BEAM", "ENERGY_BALL"))]),
    "kabu": dict(tipo="Fire", lendario="SPECIES_ENTEI", gimmick="mega",
                 slot=4, time=[
        T("SPECIES_CENTISKORCH", "ITEM_LIFE_ORB", "NATURE_MODEST", "esp",
          m("FLAMETHROWER", "BUG_BUZZ", "GIGA_DRAIN", "WILL_O_WISP")),
        T("SPECIES_ARCANINE", "ITEM_CHOICE_BAND", "NATURE_ADAMANT", "fis",
          m("FLARE_BLITZ", "EXTREME_SPEED", "WILD_CHARGE", "CLOSE_COMBAT")),
        T("SPECIES_NINETALES", "ITEM_LEFTOVERS", "NATURE_TIMID", "esp",
          m("FLAMETHROWER", "NASTY_PLOT", "SOLAR_BEAM", "WILL_O_WISP")),
        T("SPECIES_INFERNAPE", "ITEM_LIFE_ORB", "NATURE_JOLLY", "fis",
          m("FLARE_BLITZ", "CLOSE_COMBAT", "THUNDER_PUNCH", "SWORDS_DANCE")),
        T("SPECIES_CHARIZARD", "ITEM_CHARIZARDITE_Y", "NATURE_TIMID", "esp",
          m("HEAT_WAVE", "SOLAR_BEAM", "AIR_SLASH", "ROOST")),
        T("SPECIES_ENTEI", "ITEM_CHOICE_BAND", "NATURE_ADAMANT", "fis",
          m("SACRED_FIRE", "EXTREME_SPEED", "STONE_EDGE", "FLARE_BLITZ"))]),
    "bea": dict(tipo="Fighting", lendario="SPECIES_TERRAKION", gimmick="mega",
                slot=4, time=[
        T("SPECIES_MACHAMP", "ITEM_LEFTOVERS", "NATURE_ADAMANT", "duro",
          m("DYNAMIC_PUNCH", "KNOCK_OFF", "EARTHQUAKE", "BULLET_PUNCH")),
        T("SPECIES_HAWLUCHA", "ITEM_LIFE_ORB", "NATURE_JOLLY", "fis",
          m("SWORDS_DANCE", "CLOSE_COMBAT", "ACROBATICS", "STONE_EDGE")),
        T("SPECIES_CONKELDURR", "ITEM_FLAME_ORB", "NATURE_ADAMANT", "duro",
          m("DRAIN_PUNCH", "MACH_PUNCH", "KNOCK_OFF", "FACADE")),
        T("SPECIES_SIRFETCHD", "ITEM_LEFTOVERS", "NATURE_ADAMANT", "fis",
          m("CLOSE_COMBAT", "KNOCK_OFF", "SWORDS_DANCE", "BRAVE_BIRD")),
        T("SPECIES_LUCARIO", "ITEM_LUCARIONITE", "NATURE_JOLLY", "fis",
          m("CLOSE_COMBAT", "METEOR_MASH", "EXTREME_SPEED", "SWORDS_DANCE")),
        T("SPECIES_TERRAKION", "ITEM_CHOICE_SCARF", "NATURE_JOLLY", "fis",
          m("CLOSE_COMBAT", "STONE_EDGE", "EARTHQUAKE", "ROCK_SLIDE"))]),
    "allister": dict(tipo="Ghost", lendario="SPECIES_SPECTRIER", gimmick="mega",
                     slot=4, time=[
        T("SPECIES_DUSKNOIR", "ITEM_LEFTOVERS", "NATURE_ADAMANT", "duro",
          m("SHADOW_PUNCH", "EARTHQUAKE", "WILL_O_WISP", "PAIN_SPLIT")),
        T("SPECIES_MIMIKYU", "ITEM_LIFE_ORB", "NATURE_JOLLY", "fis",
          m("SWORDS_DANCE", "PLAY_ROUGH", "SHADOW_CLAW", "SHADOW_SNEAK")),
        T("SPECIES_CHANDELURE", "ITEM_CHOICE_SCARF", "NATURE_TIMID", "esp",
          m("SHADOW_BALL", "FLAMETHROWER", "ENERGY_BALL", "TRICK")),
        T("SPECIES_DRAGAPULT", "ITEM_CHOICE_BAND", "NATURE_JOLLY", "fis",
          m("PHANTOM_FORCE", "DRAGON_CLAW", "U_TURN", "SUCKER_PUNCH")),
        T("SPECIES_GENGAR", "ITEM_GENGARITE", "NATURE_TIMID", "esp",
          m("SHADOW_BALL", "SLUDGE_BOMB", "FOCUS_BLAST", "NASTY_PLOT")),
        T("SPECIES_SPECTRIER", "ITEM_LIFE_ORB", "NATURE_TIMID", "esp",
          m("SHADOW_BALL", "NASTY_PLOT", "DARK_PULSE", "SUBSTITUTE"))]),
    "opal": dict(tipo="Fairy", lendario="SPECIES_ZACIAN", gimmick="mega",
                 slot=4, time=[
        T("SPECIES_TOGEKISS", "ITEM_LEFTOVERS", "NATURE_TIMID", "esp",
          m("AIR_SLASH", "DAZZLING_GLEAM", "ROOST", "THUNDER_WAVE")),
        T("SPECIES_ALCREMIE", "ITEM_LEFTOVERS", "NATURE_CALM", "duro_esp",
          m("DAZZLING_GLEAM", "CALM_MIND", "RECOVER", "PSYCHIC")),
        T("SPECIES_WEEZING", "ITEM_BLACK_SLUDGE", "NATURE_BOLD", "duro",
          m("SLUDGE_BOMB", "WILL_O_WISP", "PAIN_SPLIT", "TOXIC")),
        T("SPECIES_SYLVEON", "ITEM_CHOICE_SPECS", "NATURE_MODEST", "duro_esp",
          m("HYPER_VOICE", "MOONBLAST", "PSYSHOCK", "SHADOW_BALL")),
        T("SPECIES_GARDEVOIR", "ITEM_GARDEVOIRITE", "NATURE_TIMID", "esp",
          m("MOONBLAST", "PSYCHIC", "FOCUS_BLAST", "CALM_MIND")),
        T("SPECIES_ZACIAN", "ITEM_LIFE_ORB", "NATURE_JOLLY", "fis",
          m("PLAY_ROUGH", "IRON_HEAD", "CLOSE_COMBAT", "SWORDS_DANCE"))]),
    "gordie": dict(tipo="Rock", lendario="SPECIES_REGIROCK", gimmick="mega",
                   slot=4, time=[
        T("SPECIES_COALOSSAL", "ITEM_LEFTOVERS", "NATURE_ADAMANT", "duro",
          m("STONE_EDGE", "FLARE_BLITZ", "EARTHQUAKE", "STEALTH_ROCK")),
        T("SPECIES_BARBARACLE", "ITEM_LIFE_ORB", "NATURE_ADAMANT", "fis",
          m("SHELL_SMASH", "STONE_EDGE", "LIQUIDATION", "EARTHQUAKE")),
        T("SPECIES_TYRANITAR", "ITEM_CHOICE_BAND", "NATURE_ADAMANT", "fis",
          m("STONE_EDGE", "CRUNCH", "EARTHQUAKE", "ICE_PUNCH")),
        T("SPECIES_GIGALITH", "ITEM_LEFTOVERS", "NATURE_ADAMANT", "duro",
          m("STONE_EDGE", "EARTHQUAKE", "EXPLOSION", "STEALTH_ROCK")),
        T("SPECIES_AGGRON", "ITEM_AGGRONITE", "NATURE_ADAMANT", "duro",
          m("HEAVY_SLAM", "STONE_EDGE", "EARTHQUAKE", "IRON_HEAD")),
        T("SPECIES_REGIROCK", "ITEM_LEFTOVERS", "NATURE_ADAMANT", "duro",
          m("STONE_EDGE", "EARTHQUAKE", "CURSE", "DRAIN_PUNCH"))]),
    "melony": dict(tipo="Ice", lendario="SPECIES_GLASTRIER", gimmick="z",
                   slot=4, time=[
        T("SPECIES_FROSMOTH", "ITEM_FOCUS_SASH", "NATURE_TIMID", "esp",
          m("QUIVER_DANCE", "BUG_BUZZ", "ICE_BEAM", "GIGA_DRAIN")),
        T("SPECIES_ABOMASNOW", "ITEM_LIFE_ORB", "NATURE_ADAMANT", "fis",
          m("BLIZZARD", "WOOD_HAMMER", "EARTHQUAKE", "ICE_SHARD")),
        T("SPECIES_WEAVILE", "ITEM_CHOICE_BAND", "NATURE_JOLLY", "fis",
          m("ICICLE_CRASH", "KNOCK_OFF", "ICE_SHARD", "LOW_KICK")),
        T("SPECIES_MAMOSWINE", "ITEM_LIFE_ORB", "NATURE_ADAMANT", "fis",
          m("ICICLE_CRASH", "EARTHQUAKE", "ICE_SHARD", "STONE_EDGE")),
        T("SPECIES_LAPRAS", "ITEM_ICIUM_Z", "NATURE_MODEST", "duro_esp",
          m("FREEZE_DRY", "SURF", "ICE_BEAM", "THUNDERBOLT")),
        T("SPECIES_GLASTRIER", "ITEM_LEFTOVERS", "NATURE_ADAMANT", "duro",
          m("ICICLE_CRASH", "HIGH_HORSEPOWER", "CLOSE_COMBAT", "SWORDS_DANCE"))]),
    "piers": dict(tipo="Dark", lendario="SPECIES_DARKRAI", gimmick="z",
                  slot=4, time=[
        T("SPECIES_MALAMAR", "ITEM_LEFTOVERS", "NATURE_ADAMANT", "duro",
          m("SUPERPOWER", "KNOCK_OFF", "PSYCHO_CUT", "REST")),
        T("SPECIES_SCRAFTY", "ITEM_LEFTOVERS", "NATURE_ADAMANT", "duro",
          m("DRAIN_PUNCH", "KNOCK_OFF", "DRAGON_DANCE", "ICE_PUNCH")),
        T("SPECIES_SKUNTANK", "ITEM_BLACK_SLUDGE", "NATURE_ADAMANT", "fis",
          m("GUNK_SHOT", "CRUNCH", "SUCKER_PUNCH", "FIRE_BLAST")),
        T("SPECIES_TOXICROAK", "ITEM_LIFE_ORB", "NATURE_JOLLY", "fis",
          m("GUNK_SHOT", "DRAIN_PUNCH", "SUCKER_PUNCH", "SWORDS_DANCE")),
        T("SPECIES_OBSTAGOON", "ITEM_DARKINIUM_Z", "NATURE_ADAMANT", "fis",
          m("KNOCK_OFF", "CLOSE_COMBAT", "FACADE", "PARTING_SHOT")),
        T("SPECIES_DARKRAI", "ITEM_LIFE_ORB", "NATURE_TIMID", "esp",
          m("DARK_PULSE", "NASTY_PLOT", "SLUDGE_BOMB", "FOCUS_BLAST"))]),
    "raihan": dict(tipo="Dragon", lendario="SPECIES_DIALGA", gimmick="mega",
                   slot=4, time=[
        T("SPECIES_FLYGON", "ITEM_CHOICE_SCARF", "NATURE_JOLLY", "fis",
          m("EARTHQUAKE", "DRAGON_CLAW", "U_TURN", "STONE_EDGE")),
        T("SPECIES_GOODRA", "ITEM_ASSAULT_VEST", "NATURE_MODEST", "duro_esp",
          m("DRACO_METEOR", "FIRE_BLAST", "THUNDERBOLT", "SLUDGE_BOMB")),
        T("SPECIES_DURALUDON", "ITEM_LIFE_ORB", "NATURE_MODEST", "esp",
          m("FLASH_CANNON", "DRACO_METEOR", "THUNDERBOLT", "DRAGON_PULSE")),
        T("SPECIES_TURTONATOR", "ITEM_LEFTOVERS", "NATURE_MODEST", "duro_esp",
          m("FLAMETHROWER", "DRAGON_PULSE", "SHELL_SMASH", "EARTH_POWER")),
        T("SPECIES_SALAMENCE", "ITEM_SALAMENCITE", "NATURE_ADAMANT", "fis",
          m("DRAGON_DANCE", "DOUBLE_EDGE", "EARTHQUAKE", "DRAGON_CLAW")),
        T("SPECIES_DIALGA", "ITEM_LEFTOVERS", "NATURE_MODEST", "duro_esp",
          m("DRACO_METEOR", "FLASH_CANNON", "THUNDERBOLT", "EARTH_POWER"))]),
    # ------------------------------------------------------ rival/campeao --
    "hop": dict(tipo="misto", lendario="SPECIES_ZAMAZENTA", gimmick="mega",
                slot=4, time=[
        T("SPECIES_CINDERACE", "ITEM_LIFE_ORB", "NATURE_JOLLY", "fis",
          m("FLARE_BLITZ", "HIGH_JUMP_KICK", "U_TURN", "SUCKER_PUNCH")),
        T("SPECIES_CORVIKNIGHT", "ITEM_LEFTOVERS", "NATURE_IMPISH", "duro",
          m("BRAVE_BIRD", "IRON_HEAD", "ROOST", "BULK_UP")),
        T("SPECIES_SNORLAX", "ITEM_LEFTOVERS", "NATURE_ADAMANT", "duro",
          m("BODY_SLAM", "CURSE", "EARTHQUAKE", "REST")),
        T("SPECIES_INTELEON", "ITEM_CHOICE_SPECS", "NATURE_TIMID", "esp",
          m("HYDRO_PUMP", "ICE_BEAM", "DARK_PULSE", "U_TURN")),
        T("SPECIES_METAGROSS", "ITEM_METAGROSSITE", "NATURE_JOLLY", "fis",
          m("METEOR_MASH", "ZEN_HEADBUTT", "EARTHQUAKE", "ICE_PUNCH")),
        T("SPECIES_ZAMAZENTA", "ITEM_LEFTOVERS", "NATURE_JOLLY", "fis",
          m("IRON_HEAD", "CLOSE_COMBAT", "CRUNCH", "SWORDS_DANCE"))]),
    "bede": dict(tipo="Fairy", lendario="SPECIES_CALYREX", gimmick="mega",
                 slot=4, time=[
        T("SPECIES_HATTERENE", "ITEM_LIFE_ORB", "NATURE_QUIET", "duro_esp",
          m("PSYCHIC", "DAZZLING_GLEAM", "MYSTICAL_FIRE", "TRICK_ROOM")),
        T("SPECIES_GALLADE", "ITEM_LIFE_ORB", "NATURE_JOLLY", "fis",
          m("CLOSE_COMBAT", "PSYCHO_CUT", "SWORDS_DANCE", "SHADOW_SNEAK")),
        T("SPECIES_MR_MIME", "ITEM_FOCUS_SASH", "NATURE_TIMID", "esp",
          m("PSYCHIC", "DAZZLING_GLEAM", "NASTY_PLOT", "FOCUS_BLAST")),
        T("SPECIES_CLEFABLE", "ITEM_LEFTOVERS", "NATURE_BOLD", "duro",
          m("MOONBLAST", "SOFT_BOILED", "CALM_MIND", "THUNDER_WAVE")),
        T("SPECIES_MAWILE", "ITEM_MAWILITE", "NATURE_ADAMANT", "fis",
          m("PLAY_ROUGH", "IRON_HEAD", "SWORDS_DANCE", "SUCKER_PUNCH")),
        T("SPECIES_CALYREX", "ITEM_LEFTOVERS", "NATURE_TIMID", "esp",
          m("PSYCHIC", "GIGA_DRAIN", "CALM_MIND", "LEECH_SEED"))]),
    "marnie": dict(tipo="Dark", lendario="SPECIES_URSHIFU", gimmick="z",
                   slot=4, time=[
        T("SPECIES_GRIMMSNARL", "ITEM_LIGHT_CLAY", "NATURE_CAREFUL", "duro_esp",
          m("SUCKER_PUNCH", "PLAY_ROUGH", "BULK_UP", "THUNDER_WAVE")),
        T("SPECIES_LIEPARD", "ITEM_LIFE_ORB", "NATURE_JOLLY", "fis",
          m("KNOCK_OFF", "SUCKER_PUNCH", "U_TURN", "PLAY_ROUGH")),
        T("SPECIES_KROOKODILE", "ITEM_CHOICE_BAND", "NATURE_JOLLY", "fis",
          m("EARTHQUAKE", "KNOCK_OFF", "STONE_EDGE", "CRUNCH")),
        T("SPECIES_HYDREIGON", "ITEM_CHOICE_SPECS", "NATURE_TIMID", "esp",
          m("DARK_PULSE", "DRACO_METEOR", "FLASH_CANNON", "FIRE_BLAST")),
        T("SPECIES_URSHIFU", "ITEM_FIGHTINIUM_Z", "NATURE_JOLLY", "fis",
          m("CLOSE_COMBAT", "SUCKER_PUNCH", "U_TURN", "SWORDS_DANCE")),
        T("SPECIES_UMBREON", "ITEM_LEFTOVERS", "NATURE_CALM", "duro_esp",
          m("FOUL_PLAY", "WISH", "PROTECT", "TOXIC"))]),
    "leon": dict(tipo="misto", lendario="SPECIES_ETERNATUS", gimmick="mega",
                 slot=4, time=[
        T("SPECIES_AEGISLASH", "ITEM_LEFTOVERS", "NATURE_QUIET", "duro_esp",
          m("SHADOW_BALL", "FLASH_CANNON", "SHADOW_SNEAK", "SWORDS_DANCE")),
        T("SPECIES_DRAGAPULT", "ITEM_CHOICE_SPECS", "NATURE_TIMID", "esp",
          m("SHADOW_BALL", "DRACO_METEOR", "FIRE_BLAST", "U_TURN")),
        T("SPECIES_HAXORUS", "ITEM_LIFE_ORB", "NATURE_JOLLY", "fis",
          m("DRAGON_DANCE", "OUTRAGE", "EARTHQUAKE", "POISON_JAB")),
        T("SPECIES_RHYPERIOR", "ITEM_LEFTOVERS", "NATURE_ADAMANT", "duro",
          m("EARTHQUAKE", "STONE_EDGE", "MEGAHORN", "ROCK_POLISH")),
        T("SPECIES_CHARIZARD", "ITEM_CHARIZARDITE_X", "NATURE_ADAMANT", "fis",
          m("DRAGON_DANCE", "FLARE_BLITZ", "EARTHQUAKE", "DRAGON_CLAW")),
        T("SPECIES_ETERNATUS", "ITEM_LIFE_ORB", "NATURE_TIMID", "esp",
          m("SLUDGE_BOMB", "FLAMETHROWER", "DRACO_METEOR", "RECOVER"))]),
    # ------------------------------------------------------------ viloes ---
    "rose": dict(tipo="Steel", lendario="SPECIES_REGIELEKI", gimmick="mega",
                 slot=4, equipe="macro_cosmos",
                 tema=["TYPE_STEEL", "TYPE_ELECTRIC"], time=[
        T("SPECIES_COPPERAJAH", "ITEM_LEFTOVERS", "NATURE_ADAMANT", "duro",
          m("HEAVY_SLAM", "EARTHQUAKE", "PLAY_ROUGH", "STEALTH_ROCK")),
        T("SPECIES_MAGNEZONE", "ITEM_CHOICE_SPECS", "NATURE_MODEST", "esp",
          m("THUNDERBOLT", "FLASH_CANNON", "VOLT_SWITCH", "THUNDER_WAVE")),
        T("SPECIES_KLINKLANG", "ITEM_LEFTOVERS", "NATURE_ADAMANT", "fis",
          m("IRON_HEAD", "WILD_CHARGE", "SUBSTITUTE", "PROTECT")),
        T("SPECIES_ROTOM", "ITEM_LEFTOVERS", "NATURE_TIMID", "esp",
          m("THUNDERBOLT", "SHADOW_BALL", "VOLT_SWITCH", "WILL_O_WISP")),
        T("SPECIES_STEELIX", "ITEM_STEELIXITE", "NATURE_ADAMANT", "duro",
          m("HEAVY_SLAM", "EARTHQUAKE", "STONE_EDGE", "STEALTH_ROCK")),
        T("SPECIES_REGIELEKI", "ITEM_LIFE_ORB", "NATURE_TIMID", "esp",
          m("THUNDERBOLT", "VOLT_SWITCH", "THUNDER_WAVE", "EXPLOSION"))]),
    "oleana": dict(tipo="Poison", lendario="SPECIES_REGIDRAGO", gimmick="mega",
                   slot=4, equipe="macro_cosmos",
                   tema=["TYPE_POISON", "TYPE_STEEL"], time=[
        T("SPECIES_GARBODOR", "ITEM_BLACK_SLUDGE", "NATURE_ADAMANT", "duro",
          m("GUNK_SHOT", "EXPLOSION", "TOXIC_SPIKES", "DRAIN_PUNCH")),
        T("SPECIES_SALAZZLE", "ITEM_LIFE_ORB", "NATURE_TIMID", "esp",
          m("SLUDGE_WAVE", "FLAMETHROWER", "NASTY_PLOT", "TOXIC")),
        T("SPECIES_BRONZONG", "ITEM_LEFTOVERS", "NATURE_SASSY", "duro",
          m("GYRO_BALL", "EARTHQUAKE", "STEALTH_ROCK", "TOXIC")),
        T("SPECIES_DRAPION", "ITEM_LEFTOVERS", "NATURE_JOLLY", "fis",
          m("KNOCK_OFF", "POISON_JAB", "EARTHQUAKE", "SWORDS_DANCE")),
        T("SPECIES_BEEDRILL", "ITEM_BEEDRILLITE", "NATURE_JOLLY", "fis",
          m("POISON_JAB", "U_TURN", "DRILL_RUN", "KNOCK_OFF")),
        T("SPECIES_REGIDRAGO", "ITEM_CHOICE_SCARF", "NATURE_ADAMANT", "fis",
          m("DRAGON_CLAW", "OUTRAGE", "EARTHQUAKE", "CRUNCH"))]),
    "team_yell": dict(tipo="Dark", lendario="SPECIES_KUBFU", gimmick="mega",
                      slot=4, equipe="team_yell", tema=["TYPE_DARK"], time=[
        T("SPECIES_LIEPARD", "ITEM_LIFE_ORB", "NATURE_JOLLY", "fis",
          m("KNOCK_OFF", "SUCKER_PUNCH", "U_TURN", "PLAY_ROUGH")),
        T("SPECIES_THIEVUL", "ITEM_LEFTOVERS", "NATURE_TIMID", "esp",
          m("DARK_PULSE", "NASTY_PLOT", "PSYCHIC", "SUBSTITUTE")),
        T("SPECIES_SCRAFTY", "ITEM_LEFTOVERS", "NATURE_ADAMANT", "duro",
          m("DRAIN_PUNCH", "KNOCK_OFF", "DRAGON_DANCE", "ICE_PUNCH")),
        T("SPECIES_OBSTAGOON", "ITEM_CHOICE_BAND", "NATURE_ADAMANT", "fis",
          m("KNOCK_OFF", "CLOSE_COMBAT", "FACADE", "U_TURN")),
        T("SPECIES_HOUNDOOM", "ITEM_HOUNDOOMINITE", "NATURE_TIMID", "esp",
          m("DARK_PULSE", "FLAMETHROWER", "NASTY_PLOT", "SLUDGE_BOMB")),
        T("SPECIES_KUBFU", "ITEM_LIFE_ORB", "NATURE_JOLLY", "fis",
          m("CLOSE_COMBAT", "IRON_HEAD", "SWORDS_DANCE", "AERIAL_ACE"))]),
}

# Quem e quem: (classe da fonte, nome da fonte) -> (identidade, papel).
# Sai do comentario que `treinadores_galar.py` escreve em cada #define, entao
# nao ha lista de id digitada a mao aqui: se a numeracao mudar, isto acompanha.
QUEM = {
    ("Leader", "Milo"): ("milo", "lider"),
    ("Leader", "Nessa"): ("nessa", "lider"),
    ("Leader", "Kabu"): ("kabu", "lider"),
    ("Leader", "Bea"): ("bea", "lider"),
    ("Leader", "Allister"): ("allister", "lider"),
    ("Leader", "Opal"): ("opal", "lider"),
    ("Leader", "Gordie"): ("gordie", "lider"),
    ("Leader", "Melony"): ("melony", "lider"),
    ("Leader", "Piers"): ("piers", "lider"),
    ("Leader", "Raihan"): ("raihan", "lider"),
    ("Elite Four", "Raihan"): ("raihan", "e4"),
    ("Rival", "Hop"): ("hop", "rival"),
    ("Rival", "HOP"): ("hop", "rival"),
    ("Rival", "Bede"): ("bede", "rival"),
    ("Leader", "Bede"): ("bede", "e4"),
    ("Rival", "Marnie"): ("marnie", "rival"),
    ("Rival", "Leon"): ("leon", "campeao"),
    ("Macro Cosmos", "Rose"): ("rose", "vilao"),
    ("Macro Cosmos", "Olena"): ("oleana", "vilao"),
    ("TEAM YELL", "kevin"): ("team_yell", "vilao"),
    ("TEAM YELL", "JONH"): ("team_yell", "vilao"),
    ("TEAM YELL", "Ana"): ("team_yell", "vilao"),
    ("TEAM YELL", "Grunt"): ("team_yell", "vilao"),
    ("TEAM YELL", "RICK"): ("team_yell", "vilao"),
    ("TEAM YELL", "kissa"): ("team_yell", "vilao"),
    ("TEAM YELL", "ravana"): ("team_yell", "vilao"),
}
CLASSES_COMPOSTAS = ("Elite Four", "TEAM YELL", "Macro Cosmos")


def elenco():
    """[(constante, identidade, papel)] lido de opponents.h."""
    fora = []
    for const, _id, _f, resto in re.findall(
            r"#define (TRAINER_GALAR_\w+)\s+(\d+)\s+// fonte (\d+), (.+)",
            open(OPPS).read()):
        classe, nome = None, None
        for k in CLASSES_COMPOSTAS:
            if resto.startswith(k + " "):
                classe, nome = k, resto[len(k) + 1:]
                break
        if classe is None:
            classe, _, nome = resto.partition(" ")
        chave = (classe, nome.strip())
        if chave in QUEM:
            ident, papel = QUEM[chave]
            fora.append((const, ident, papel))
    return fora


def monta(const, ident, papel):
    d = TIMES[ident]
    c = dict(id=const, regiao=REGIAO, papel=papel, identidade=ident,
             ace=NIVEL, gimmick=d["gimmick"], gimmick_slot=d["slot"],
             lendario=d["lendario"], ai=list(AI), time=[])
    if papel == "vilao":
        c["equipe"] = d["equipe"]
        c["tema"] = list(d["tema"])
    for t in d["time"]:
        c["time"].append(dict(especie=t.esp, nivel=NIVEL, item=t.item,
                              natureza=t.nat, ivs=IVS, evs=EV[t.ev],
                              golpes=list(t.golpes)))
    return c


def constantes(caminho, prefixo):
    return set(re.findall(r"\b%s_[A-Z0-9_]+\b" % prefixo, open(caminho).read()))


def confere(chefes):
    """Reprovacoes de CONSTANTE (o valida() da Fase F cuida do resto)."""
    esp = constantes(f"{RAIZ}/include/constants/species.h", "SPECIES")
    itens = constantes(f"{RAIZ}/include/constants/items.h", "ITEM")
    golpes = constantes(f"{RAIZ}/include/constants/moves.h", "MOVE")
    nat = constantes(f"{RAIZ}/include/constants/pokemon.h", "NATURE")
    tipos = constantes(f"{RAIZ}/include/constants/pokemon.h", "TYPE")
    erros = []
    for c in chefes:
        for t in c["tema"] if c.get("tema") else []:
            if t not in tipos:
                erros.append("%s: tipo %s nao existe" % (c["id"], t))
        for mo in c["time"]:
            if mo["especie"] not in esp:
                erros.append("%s: %s nao existe" % (c["id"], mo["especie"]))
            if mo["item"] not in itens:
                erros.append("%s: %s nao existe" % (c["id"], mo["item"]))
            if mo["natureza"] not in nat:
                erros.append("%s: %s nao existe" % (c["id"], mo["natureza"]))
            for g in mo["golpes"]:
                if g not in golpes:
                    erros.append("%s: %s nao existe" % (c["id"], g))
    return sorted(set(erros))


def novo_doc(chefes):
    doc = json.load(open(JSON))
    doc["chefes"] = [c for c in doc["chefes"] if c["regiao"] != REGIAO] + chefes
    return doc


def demo():
    ok = True

    def caso(nome, cond):
        nonlocal ok
        print("  %-62s %s" % (nome, "ok" if cond else "REPROVOU"))
        ok = ok and cond

    el = elenco()
    caso("o elenco acha os 10 lideres de Galar",
         len({i for _, i, p in el if p == "lider"}) == 10)
    caso("acha os tres rivais e o campeao",
         {i for _, i, p in el if p in ("rival", "campeao")}
         >= {"hop", "bede", "marnie", "leon"})
    caso("acha os tres viloes", {i for _, i, p in el if p == "vilao"}
         == {"rose", "oleana", "team_yell"})
    chefes = [monta(c, i, p) for c, i, p in el]
    caso("nenhuma constante inventada", not confere(chefes))
    doc = novo_doc(chefes)
    erros = FF.valida(doc)
    caso("o guarda da Fase F aprova a tabela inteira", not erros)
    if erros:
        for e in erros[:8]:
            print("      %s" % e)
    conta = collections.Counter(c["gimmick"] for c in chefes)
    caso("zero Dynamax e zero Tera novos em Galar",
         conta["dynamax"] == 0 and conta["tera"] == 0)
    caso("todo chefe de Galar esta no nivel 255",
         all(mo["nivel"] == 255 for c in chefes for mo in c["time"]))
    lends = collections.defaultdict(set)
    for c in chefes:
        lends[c["lendario"]].add(c["identidade"])
    caso("nenhum lendario repete entre pessoas em Galar",
         all(len(v) == 1 for v in lends.values()))
    # PAR NEGATIVO: dois chefes com o mesmo lendario tem de reprovar.
    sujo = json.loads(json.dumps(doc))
    galar = [c for c in sujo["chefes"] if c["regiao"] == REGIAO]
    a, b = next(c for c in galar if c["identidade"] == "milo"), \
        next(c for c in galar if c["identidade"] == "nessa")
    b["lendario"] = a["lendario"]
    b["time"][5]["especie"] = a["lendario"]
    caso("dois chefes de Galar com o MESMO lendario REPROVAM",
         any("repetido" in e for e in FF.valida(sujo)))
    print("\n%s" % ("demo verde" if ok else "DEMO REPROVOU"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        return demo()
    el = elenco()
    chefes = [monta(c, i, p) for c, i, p in el]
    erros = confere(chefes) + FF.valida(novo_doc(chefes))
    print("chefes de Galar: %d batalhas, %d pessoas, %d Pokemon"
          % (len(chefes), len({i for _, i, _ in el}), 6 * len(chefes)))
    papel = collections.Counter(c["papel"] for c in chefes)
    print("por papel: %s" % dict(papel))
    print("gimmick: %s" % dict(collections.Counter(c["gimmick"] for c in chefes)))
    print("lendarios: %s" % ", ".join(sorted(
        {c["lendario"].replace("SPECIES_", "") for c in chefes})))
    if erros:
        print("REPROVACOES (%d):" % len(erros))
        for e in erros[:20]:
            print("   %s" % e)
        return 1
    if a.aplicar:
        doc = novo_doc(chefes)
        json.dump(doc, open(JSON, "w"), ensure_ascii=False, indent=1)
        print("escrito em %s (%d chefes no total)" % (JSON, len(doc["chefes"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
