#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Importa as batalhas de chefe que a FONTE tem e este repo nao tinha.

Uso:
    python3 dev_scripts/importa_chefes_faltantes.py --seco     # mede, nao escreve
    python3 dev_scripts/importa_chefes_faltantes.py --demo     # planta erro e prova o guarda
    python3 dev_scripts/importa_chefes_faltantes.py --aplicar  # escreve

Por que um script novo e nao os importadores de regiao
------------------------------------------------------
`importa_treinadores_johto.py` e `importa_unova.py` importam treinador de ROTA e
recusam de proposito bloco que nao comeca com `trainerbattle_` (o cabecalho do
primeiro diz isso com todas as letras: "Rival, Eusine e as irmas Kimono sao cena
com movimento, camera e var de enredo"). As seis batalhas de baixo sao
exatamente essas cenas. Ensinar cena a um importador de rota seria trocar o
motivo de ele existir; um segundo script, com tabela declarativa, e menor.

O que ele NAO faz, de proposito: time competitivo. Ele deixa o time DA FONTE no
`.party`, e quem escreve o time de chefe continua sendo `fase_f_chefes.py`, que
e idempotente e tem guarda. Este script so acrescenta a LINHA na tabela da Fase F.

Idempotencia: tudo que ele escreve vive entre marcadores e e reescrito por
inteiro; rodar duas vezes da diff zero. O `--demo` prova isso rodando duas vezes
em copia.

A fonte, medida em 22/08/2026 (e a medicao esta em PLANO-FASE-F.md)
------------------------------------------------------------------
- Johto, demake HGSS (`fontes-mapas/hns`): o rival tem SETE encontros, nao
  quatro, e cada um tem TRES constantes (uma por inicial:
  `TRAINER_RIVAL_{CYNDAQUIL,TOTODILE,CHIKORITA}_1..7`). Este repo importou os
  quatro primeiros e so a linha do TOTODILE (ver opponents.h:1393). Faltavam o
  5 (VictoryRoadKanto_1F), o 6 (MtMoon_Cave) e o 7 (IndigoPlateau_PokemonCenter).
- Unova, BW3G (`fontes-mapas/bw3g`): **Ghetsis e o Shadow Triad NAO existem como
  treinador** (so como texto e como nome de musica). Existem, com time proprio:
  `N` (`N1`, maps/NsRoom.asm:29), `RYOKU1` (maps/AccumulaTown.asm:43),
  `HUGH_{SNIVY,TEPIG,OSHAWOTT}` (maps/DriftveilShelter.asm:165-171),
  `BIANCA1`, `NATE_*`, `ROSA_*` e `CHEREN2`.
  Nao entram nesta leva, e o motivo esta escrito no plano: a Bianca vive na
  moldura de torneio do PWT (`scene_script`, `priorityjump`, `warpcheck`), a
  Nate/Rosa sao seis variantes atras de um ramo de genero + inicial, e o
  `CHEREN2` e revanche, que o plano ja tinha posto fora de escopo.

O nivel de cada batalha nova nao foi escolhido a dedo: veio do MESMO ajuste
linear que os irmaos dela ja obedecem (a conta esta em `NIVEL_MEDIDO`).
"""
import argparse
import collections
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTY = os.path.join(RAIZ, 'src', 'data', 'trainers.party')
OPPO = os.path.join(RAIZ, 'include', 'constants', 'opponents.h')
FLAGS = os.path.join(RAIZ, 'include', 'constants', 'flags.h')
FASEF = os.path.join(RAIZ, 'dev_scripts', 'fase_f_chefes.json')

MARCA_OPPO = 'chefes que faltavam de Johto e Unova (importa_chefes_faltantes.py)'
MARCA_FLAGS = 'esconde o SILVER nos tres mapas novos (importa_chefes_faltantes.py)'
MARCA_INC = 'cena importada por dev_scripts/importa_chefes_faltantes.py'

IA = ['AI_FLAG_SMART_TRAINER', 'AI_FLAG_HP_AWARE', 'AI_FLAG_TRY_TO_2HKO',
      'AI_FLAG_POWERFUL_STATUS', 'AI_FLAG_PREDICTION', 'AI_FLAG_ASSUMPTIONS',
      'AI_FLAG_KNOW_OPPONENT_PARTY', 'AI_FLAG_ACE_POKEMON']

IVS = '31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe'

NIVEL_MEDIDO = """
Johto, o SILVER: os quatro aces que ja existem sao 45, 60, 68 e 82, contra os
aces 5, 18, 24 e 40 da fonte. Minimos quadrados nesses quatro pares da
nivel = 40,69 + 1,0601 * fonte, com residuo de no maximo 2 niveis. Aplicado aos
aces 48, 64 e 68 da fonte, sai 92, 109 e 113. Os dois ultimos passam do teto de
100 da faixa de Johto, e passam de proposito: sao batalhas de POS-JOGO, e a
`TRAINER_JOHTO_GIOVANNI` ja esta em 114 com a palavra do Gui ("a curva pode ter
outliers coerentes", 22/08/2026).

Unova, os sabios da Plasma: os cinco primeiros combates ja importados sao
Giallo 30->219, Bronius 36->224, Gorm 45->232 e Zinzolin 57->242. A mesma conta
da nivel = 192,5 + 0,885 * fonte, que reproduz os QUATRO exatamente. O ace 40 do
`RYOKU1` cai em 228.

Unova, N e HUGH: os dois tem ace 73 na fonte, e a mesma reta daria 257, acima do
MAX_LEVEL desta build. Os dois SATURAM em 255. Nao ha desempate a inventar: as
duas batalhas sao de pos-jogo e os dois times da fonte tem a mesma forma
(cinco entre 68 e 70, ace 73).
"""


def curto(e):
    return e['id'].replace('TRAINER_UNOVA_', '').replace('TRAINER_JOHTO_', '')


def mon(especie, nivel, item, hab, nat, evs, golpes):
    return {'especie': especie, 'nivel': nivel, 'item': item, 'habilidade': hab,
            'natureza': nat, 'ivs': IVS, 'evs': evs, 'golpes': golpes}


ATK = '252 Atk / 252 Spe / 4 HP'
SPA = '252 SpA / 252 Spe / 4 HP'
DEF = '252 HP / 252 Def / 4 SpD'
BULK = '252 HP / 252 SpA / 4 SpD'

# Blocos reaproveitados dos times que o SILVER ja tem em fase_f_chefes.json.
# Copiar aqui e melhor do que reescrever: sao sets ja aprovados pelo guarda.
def crobat(n):
    return mon('SPECIES_CROBAT', n, 'ITEM_HEAVY_DUTY_BOOTS', 'ABILITY_INFILTRATOR',
               'NATURE_JOLLY', ATK, ['MOVE_BRAVE_BIRD', 'MOVE_U_TURN', 'MOVE_ROOST', 'MOVE_DEFOG'])


def feraligatr(n):
    return mon('SPECIES_FERALIGATR', n, 'ITEM_LIFE_ORB', 'ABILITY_SHEER_FORCE',
               'NATURE_ADAMANT', ATK,
               ['MOVE_DRAGON_DANCE', 'MOVE_LIQUIDATION', 'MOVE_ICE_PUNCH', 'MOVE_CRUNCH'])


def lugia(n):
    return mon('SPECIES_LUGIA', n, 'ITEM_HEAVY_DUTY_BOOTS', 'ABILITY_MULTISCALE',
               'NATURE_BOLD', DEF,
               ['MOVE_AEROBLAST', 'MOVE_ROOST', 'MOVE_CALM_MIND', 'MOVE_WHIRLWIND'])


def victreebel(n):
    return mon('SPECIES_VICTREEBEL', n, 'ITEM_LIFE_ORB', 'ABILITY_CHLOROPHYLL',
               'NATURE_MODEST', SPA,
               ['MOVE_GROWTH', 'MOVE_GIGA_DRAIN', 'MOVE_SLUDGE_BOMB', 'MOVE_SLEEP_POWDER'])


def houndoom(n):
    return mon('SPECIES_HOUNDOOM', n, 'ITEM_LIFE_ORB', 'ABILITY_FLASH_FIRE',
               'NATURE_TIMID', SPA,
               ['MOVE_NASTY_PLOT', 'MOVE_DARK_PULSE', 'MOVE_FIRE_BLAST', 'MOVE_SLUDGE_BOMB'])


def tyranitar(n):
    return mon('SPECIES_TYRANITAR', n, 'ITEM_TYRANITARITE', 'ABILITY_SAND_STREAM',
               'NATURE_ADAMANT', ATK,
               ['MOVE_DRAGON_DANCE', 'MOVE_STONE_EDGE', 'MOVE_CRUNCH', 'MOVE_EARTHQUAKE'])


def ursaluna(n):
    return mon('SPECIES_URSALUNA_BLOODMOON', n, 'ITEM_LIFE_ORB', 'ABILITY_MINDS_EYE',
               'NATURE_MODEST', BULK,
               ['MOVE_BLOOD_MOON', 'MOVE_EARTH_POWER', 'MOVE_CALM_MIND', 'MOVE_MOONLIGHT'])


def time_silver(base, primeiro):
    """base = nivel do ace; o resto entra ate 4 abaixo, como o resto da Fase F."""
    return [primeiro(base - 4), victreebel(base - 4), houndoom(base - 3),
            feraligatr(base - 2), lugia(base - 1), tyranitar(base)]


# Time do RYOKU2 (fase_f_chefes.json), 14 niveis abaixo. Mesma pessoa, mesmo
# lendario (a regra deixa repetir dentro da MESMA identidade) e mesmo gimmick Z.
def time_ryoku(base):
    return [
        mon('SPECIES_FERROTHORN', base - 4, 'ITEM_LEFTOVERS', 'ABILITY_IRON_BARBS',
            'NATURE_RELAXED', DEF,
            ['MOVE_SPIKES', 'MOVE_LEECH_SEED', 'MOVE_POWER_WHIP', 'MOVE_GYRO_BALL']),
        mon('SPECIES_AMOONGUSS', base - 4, 'ITEM_BLACK_SLUDGE', 'ABILITY_REGENERATOR',
            'NATURE_BOLD', DEF,
            ['MOVE_SPORE', 'MOVE_GIGA_DRAIN', 'MOVE_SLUDGE_BOMB', 'MOVE_CLEAR_SMOG']),
        mon('SPECIES_ROSERADE', base - 3, 'ITEM_BLACK_SLUDGE', 'ABILITY_TECHNICIAN',
            'NATURE_TIMID', SPA,
            ['MOVE_SPIKES', 'MOVE_GIGA_DRAIN', 'MOVE_SLUDGE_BOMB', 'MOVE_SLEEP_POWDER']),
        mon('SPECIES_TANGROWTH', base - 2, 'ITEM_ASSAULT_VEST', 'ABILITY_REGENERATOR',
            'NATURE_RELAXED', DEF,
            ['MOVE_GIGA_DRAIN', 'MOVE_POWER_WHIP', 'MOVE_EARTHQUAKE', 'MOVE_KNOCK_OFF']),
        mon('SPECIES_WO_CHIEN', base - 1, 'ITEM_LEFTOVERS', 'ABILITY_TABLETS_OF_RUIN',
            'NATURE_CALM', DEF,
            ['MOVE_LEECH_SEED', 'MOVE_GIGA_DRAIN', 'MOVE_KNOCK_OFF', 'MOVE_PROTECT']),
        mon('SPECIES_DECIDUEYE', base, 'ITEM_DECIDIUM_Z', 'ABILITY_LONG_REACH',
            'NATURE_ADAMANT', ATK,
            ['MOVE_SPIRIT_SHACKLE', 'MOVE_LEAF_BLADE', 'MOVE_SHADOW_SNEAK', 'MOVE_SWORDS_DANCE']),
    ]


def time_n(base):
    """Time da fonte (maps/NsRoom.asm) com o VOLCARONA cedendo a vaga ao lendario.

    O gimmick e Z e nao Mega porque NENHUMA das seis especies da fonte tem Mega
    em form_change_tables.h (medido); dar Mega exigiria trocar o elenco, que e o
    mesmo motivo pelo qual o RYOKU2 ja usa Z."""
    return [
        mon('SPECIES_KLINKLANG', base - 4, 'ITEM_LEFTOVERS', 'ABILITY_CLEAR_BODY',
            'NATURE_ADAMANT', ATK,
            ['MOVE_SHIFT_GEAR', 'MOVE_GEAR_GRIND', 'MOVE_WILD_CHARGE', 'MOVE_SUBSTITUTE']),
        mon('SPECIES_ARCHEOPS', base - 4, 'ITEM_LIFE_ORB', 'ABILITY_DEFEATIST',
            'NATURE_JOLLY', ATK,
            ['MOVE_ROCK_SLIDE', 'MOVE_ACROBATICS', 'MOVE_EARTHQUAKE', 'MOVE_U_TURN']),
        mon('SPECIES_VANILLUXE', base - 3, 'ITEM_LIFE_ORB', 'ABILITY_SNOW_WARNING',
            'NATURE_MODEST', SPA,
            ['MOVE_AURORA_VEIL', 'MOVE_BLIZZARD', 'MOVE_FREEZE_DRY', 'MOVE_FLASH_CANNON']),
        mon('SPECIES_CARRACOSTA', base - 2, 'ITEM_WHITE_HERB', 'ABILITY_SOLID_ROCK',
            'NATURE_ADAMANT', ATK,
            ['MOVE_SHELL_SMASH', 'MOVE_LIQUIDATION', 'MOVE_STONE_EDGE', 'MOVE_AQUA_JET']),
        mon('SPECIES_KYUREM_WHITE', base - 1, 'ITEM_CHOICE_SPECS', 'ABILITY_TURBOBLAZE',
            'NATURE_MODEST', SPA,
            ['MOVE_ICE_BEAM', 'MOVE_DRACO_METEOR', 'MOVE_FUSION_FLARE', 'MOVE_EARTH_POWER']),
        mon('SPECIES_ZOROARK', base, 'ITEM_DARKINIUM_Z', 'ABILITY_ILLUSION',
            'NATURE_TIMID', SPA,
            ['MOVE_NASTY_PLOT', 'MOVE_DARK_PULSE', 'MOVE_FLAMETHROWER', 'MOVE_SLUDGE_BOMB']),
    ]


def time_hugh(base):
    """Time da fonte (HUGH_TEPIG) com o BOUFFALANT cedendo a vaga ao lendario.

    Das tres variantes de inicial da fonte, a do TEPIG e a escolhida por MEDICAO
    e nao por gosto: o EMBOAR e o unico Pokemon do elenco do HUGH que tem Mega
    na form_change_tables.h junto do EELEKTROSS, e e ele que ocupa o slot de ace
    na fonte. Com SNIVY ou OSHAWOTT o ace ficaria sem gimmick."""
    return [
        mon('SPECIES_UNFEZANT', base - 4, 'ITEM_LIFE_ORB', 'ABILITY_SUPER_LUCK',
            'NATURE_JOLLY', ATK,
            ['MOVE_BRAVE_BIRD', 'MOVE_FACADE', 'MOVE_U_TURN', 'MOVE_ROOST']),
        mon('SPECIES_LIEPARD', base - 4, 'ITEM_FOCUS_SASH', 'ABILITY_PRANKSTER',
            'NATURE_JOLLY', ATK,
            ['MOVE_ENCORE', 'MOVE_THUNDER_WAVE', 'MOVE_KNOCK_OFF', 'MOVE_U_TURN']),
        mon('SPECIES_FLYGON', base - 3, 'ITEM_CHOICE_SCARF', 'ABILITY_LEVITATE',
            'NATURE_JOLLY', ATK,
            ['MOVE_EARTHQUAKE', 'MOVE_OUTRAGE', 'MOVE_U_TURN', 'MOVE_STONE_EDGE']),
        mon('SPECIES_EELEKTROSS', base - 2, 'ITEM_ASSAULT_VEST', 'ABILITY_LEVITATE',
            'NATURE_MODEST', BULK,
            ['MOVE_THUNDERBOLT', 'MOVE_FLAMETHROWER', 'MOVE_GIGA_DRAIN', 'MOVE_KNOCK_OFF']),
        mon('SPECIES_LANDORUS_THERIAN', base - 1, 'ITEM_LEFTOVERS', 'ABILITY_INTIMIDATE',
            'NATURE_IMPISH', DEF,
            ['MOVE_EARTHQUAKE', 'MOVE_U_TURN', 'MOVE_STEALTH_ROCK', 'MOVE_KNOCK_OFF']),
        mon('SPECIES_EMBOAR', base, 'ITEM_EMBOARITE', 'ABILITY_RECKLESS',
            'NATURE_ADAMANT', ATK,
            ['MOVE_FLARE_BLITZ', 'MOVE_CLOSE_COMBAT', 'MOVE_WILD_CHARGE', 'MOVE_SUCKER_PUNCH']),
    ]


T = '\t'

def time_bianca(base):
    """Time da fonte (BIANCA1, parties.asm:4075) com o lendario ACRESCENTADO.

    Ela tem 5 na fonte e a regra 1 deixa a primeira batalha de rival seguir a
    contagem da fonte; como o ace passa de 40, a regra 2 exige lendario, e o
    lendario entra como sexta vaga em vez de expulsar um Pokemon da fonte.
    Gimmick Z e nao Mega: nenhuma das cinco especies dela tem Mega."""
    return [
        mon('SPECIES_STOUTLAND', base - 4, 'ITEM_CHOICE_BAND', 'ABILITY_INTIMIDATE',
            'NATURE_ADAMANT', ATK,
            ['MOVE_RETALIATE', 'MOVE_CRUNCH', 'MOVE_PLAY_ROUGH', 'MOVE_WILD_CHARGE']),
        mon('SPECIES_SERVINE', base - 4, 'ITEM_EVIOLITE', 'ABILITY_CONTRARY',
            'NATURE_TIMID', DEF,
            ['MOVE_LEAF_STORM', 'MOVE_GIGA_DRAIN', 'MOVE_GLARE', 'MOVE_SUBSTITUTE']),
        mon('SPECIES_PIGNITE', base - 3, 'ITEM_EVIOLITE', 'ABILITY_THICK_FAT',
            'NATURE_ADAMANT', ATK,
            ['MOVE_FLARE_BLITZ', 'MOVE_BRICK_BREAK', 'MOVE_ROCK_SLIDE', 'MOVE_BULK_UP']),
        mon('SPECIES_DEWOTT', base - 2, 'ITEM_EVIOLITE', 'ABILITY_SHELL_ARMOR',
            'NATURE_ADAMANT', ATK,
            ['MOVE_AQUA_JET', 'MOVE_LIQUIDATION', 'MOVE_ICE_BEAM', 'MOVE_SWORDS_DANCE']),
        mon('SPECIES_CRESSELIA', base - 1, 'ITEM_LEFTOVERS', 'ABILITY_LEVITATE',
            'NATURE_BOLD', DEF,
            ['MOVE_MOONLIGHT', 'MOVE_CALM_MIND', 'MOVE_PSYSHOCK', 'MOVE_MOONBLAST']),
        mon('SPECIES_MUSHARNA', base, 'ITEM_PSYCHIUM_Z', 'ABILITY_SYNCHRONIZE',
            'NATURE_MODEST', BULK,
            ['MOVE_CALM_MIND', 'MOVE_PSYCHIC', 'MOVE_DAZZLING_GLEAM', 'MOVE_MOONLIGHT']),
    ]


def time_cheren2(base):
    """Time da fonte (CHEREN2, parties.asm:3731) com o lendario acrescentado.

    O lendario e o MESMO REGIGIGAS do TRAINER_UNOVA_LEADER_CHEREN, e isso e a
    regra e nao descuido: a proibicao de repetir lendario vale entre pessoas
    DIFERENTES, e este e o mesmo Cheren. Gimmick Z porque nenhuma das cinco
    especies tem Mega, e Dynamax esta fora (a cota de 5 do Gui ja esta gasta, e
    o Cheren lider e um dos cinco)."""
    return [
        mon('SPECIES_WATCHOG', base - 4, 'ITEM_LIFE_ORB', 'ABILITY_ANALYTIC',
            'NATURE_ADAMANT', ATK,
            ['MOVE_CRUNCH', 'MOVE_RETALIATE', 'MOVE_LOW_KICK', 'MOVE_SUCKER_PUNCH']),
        mon('SPECIES_WIGGLYTUFF', base - 4, 'ITEM_LEFTOVERS', 'ABILITY_COMPETITIVE',
            'NATURE_MODEST', BULK,
            ['MOVE_DAZZLING_GLEAM', 'MOVE_THUNDERBOLT', 'MOVE_ICE_BEAM', 'MOVE_WISH']),
        mon('SPECIES_BRAVIARY', base - 3, 'ITEM_CHOICE_SCARF', 'ABILITY_DEFIANT',
            'NATURE_ADAMANT', ATK,
            ['MOVE_BRAVE_BIRD', 'MOVE_CLOSE_COMBAT', 'MOVE_U_TURN', 'MOVE_ROCK_SLIDE']),
        mon('SPECIES_BOUFFALANT', base - 2, 'ITEM_ASSAULT_VEST', 'ABILITY_SAP_SIPPER',
            'NATURE_ADAMANT', ATK,
            ['MOVE_HEAD_CHARGE', 'MOVE_EARTHQUAKE', 'MOVE_WILD_CHARGE', 'MOVE_ZEN_HEADBUTT']),
        mon('SPECIES_REGIGIGAS', base - 1, 'ITEM_FLAME_ORB', 'ABILITY_SLOW_START',
            'NATURE_ADAMANT', ATK,
            ['MOVE_FACADE', 'MOVE_KNOCK_OFF', 'MOVE_DRAIN_PUNCH', 'MOVE_THUNDER_WAVE']),
        mon('SPECIES_STOUTLAND', base, 'ITEM_NORMALIUM_Z', 'ABILITY_SCRAPPY',
            'NATURE_ADAMANT', ATK,
            ['MOVE_GIGA_IMPACT', 'MOVE_CRUNCH', 'MOVE_PLAY_ROUGH', 'MOVE_WILD_CHARGE']),
    ]


def time_nate_rosa(base, inicial):
    """Time da fonte (NATE_*/ROSA_*, parties.asm:5189 e :5274, IDENTICOS mon a mon)
    com o AMOONGUSS cedendo a vaga ao lendario.

    Quem sai e o Amoonguss e nao o Froslass, e a escolha e por MEDICAO: das seis
    especies da fonte, o FROSLASS e a UNICA com Mega na form_change_tables.h
    (`ITEM_FROSLASSITE`), e sem ele estas seis batalhas ficariam sem gimmick
    nenhum. Por isso o slot do gimmick e o 3, e nao o ace.

    Nem DARMANITAN nem MELOETTA levam linha `Ability:`: as duas sao escritas por
    macro no species_info e a habilidade nao da para ler dali. O motor cai no
    slot 0, que e o mesmo caminho que o Gengar do Silver ja usa."""
    return [
        mon('SPECIES_DARMANITAN', base - 4, 'ITEM_CHOICE_SCARF', None,
            'NATURE_JOLLY', ATK,
            ['MOVE_FLARE_BLITZ', 'MOVE_EARTHQUAKE', 'MOVE_U_TURN', 'MOVE_ROCK_SLIDE']),
        mon('SPECIES_KINGDRA', base - 4, 'ITEM_LEFTOVERS', 'ABILITY_SNIPER',
            'NATURE_MODEST', BULK,
            ['MOVE_HYDRO_PUMP', 'MOVE_DRACO_METEOR', 'MOVE_ICE_BEAM', 'MOVE_RAIN_DANCE']),
        mon('SPECIES_KROOKODILE', base - 3, 'ITEM_LIFE_ORB', 'ABILITY_MOXIE',
            'NATURE_JOLLY', ATK,
            ['MOVE_EARTHQUAKE', 'MOVE_KNOCK_OFF', 'MOVE_STONE_EDGE', 'MOVE_SWORDS_DANCE']),
        mon('SPECIES_FROSLASS', base - 2, 'ITEM_FROSLASSITE', 'ABILITY_CURSED_BODY',
            'NATURE_TIMID', SPA,
            ['MOVE_SPIKES', 'MOVE_ICE_BEAM', 'MOVE_SHADOW_BALL', 'MOVE_DESTINY_BOND']),
        mon('SPECIES_MELOETTA', base - 1, 'ITEM_LEFTOVERS', None,
            'NATURE_MODEST', BULK,
            ['MOVE_CALM_MIND', 'MOVE_PSYSHOCK', 'MOVE_DAZZLING_GLEAM', 'MOVE_SHADOW_BALL']),
        INICIAIS_NATE_ROSA[inicial](base),
    ]


def _serperior(n):
    return mon('SPECIES_SERPERIOR', n, 'ITEM_LEFTOVERS', 'ABILITY_CONTRARY',
               'NATURE_TIMID', SPA,
               ['MOVE_LEAF_STORM', 'MOVE_GIGA_DRAIN', 'MOVE_GLARE', 'MOVE_SUBSTITUTE'])


def _emboar(n):
    return mon('SPECIES_EMBOAR', n, 'ITEM_LIFE_ORB', 'ABILITY_RECKLESS',
               'NATURE_ADAMANT', ATK,
               ['MOVE_FLARE_BLITZ', 'MOVE_CLOSE_COMBAT', 'MOVE_WILD_CHARGE', 'MOVE_SUCKER_PUNCH'])


def _samurott(n):
    return mon('SPECIES_SAMUROTT', n, 'ITEM_LIFE_ORB', 'ABILITY_SHELL_ARMOR',
               'NATURE_ADAMANT', ATK,
               ['MOVE_SWORDS_DANCE', 'MOVE_LIQUIDATION', 'MOVE_MEGAHORN', 'MOVE_AQUA_JET'])


INICIAIS_NATE_ROSA = {'SNIVY': _serperior, 'TEPIG': _emboar, 'OSHAWOTT': _samurott}


# ------------------------------------------------------------------ a tabela
# `cena` = 'npc_novo'    -> cria object_event, flag de esconder e portao no
#                           ON_TRANSITION do mapa (padrao das quatro batalhas de
#                           SILVER que ja existem: ver CherrygroveCity/scripts.inc)
# `cena` = 'npc_existente' -> o NPC ja veio no import de Unova e so o `msgbox`
#                           dele vira batalha. Nada de flag nova, nada de objeto
#                           novo: a fonte ja pos o bicho no lugar certo.
TABELA = [
    {
        'id': 'TRAINER_JOHTO_RIVAL_SILVER_5', 'num': 2523, 'cena': 'npc_novo',
        'nome': 'Silver', 'classe': 'TRAINER_CLASS_RIVAL_LATE_FRLG',
        'pic': 'TRAINER_PIC_RIVAL_LATE_FRLG', 'genero': 'Male',
        'fonte': 'hns TRAINER_RIVAL_TOTODILE_5 (VictoryRoadKanto_1F/scripts.inc:70)',
        'mapa': 'VictoryRoad_1F_Frlg', 'prefixo': 'VictoryRoad_1F',
        'ontransition': 'VictoryRoad_1F_Frlg_OnTransition',
        'localid': 'LOCALID_VICTORY_ROAD_1F_SILVER',
        'flag': 'FLAG_HIDE_SILVER_VICTORY_ROAD', 'flag_crua': 'FLAG_UNUSED_0x1D03',
        'gfx': 'OBJ_EVENT_GFX_RED', 'x': 8, 'y': 20, 'elev': 3,
        'olhar': 'MOVEMENT_TYPE_FACE_RIGHT',
        'depois_de': 'TRAINER_JOHTO_RIVAL_SILVER_4',
        'regiao': 'johto', 'papel': 'rival', 'identidade': 'silver',
        'ace': 92, 'gimmick': 'mega', 'slot': 5, 'lendario': 'SPECIES_LUGIA',
        'time': time_silver(92, crobat),
        'texto': {
            'seen': ['Hold it.\\p', '…Are you going to take the POKéMON\\n',
                     'LEAGUE challenge?\\p', '…Don\'t make me laugh.\\p',
                     'You\'re so much weaker than I am.\\p',
                     'I\'m not like I was before.\\p',
                     'I now have the best and strongest\\n', 'POKéMON with me.\\p',
                     'I\'m invincible!\\p', '{PLAYER}!\\n', 'I challenge you!$'],
            'beaten': ['…I couldn\'t win…\\p', 'I gave it every-thing I had…\\p',
                       'What you possess, and what I lack…\\p',
                       'I\'m beginning to understand what\\n',
                       'that dragon master said to me…$'],
            'after': ['…I haven\'t given up on becoming the\\n',
                      'greatest trainer…\\p',
                      'I\'m going to find out why I can\'t\\n',
                      'win and become stronger…\\p',
                      'When I do, I will challenge you.\\p',
                      '…Humph! You keep at it until then.$'],
        },
    },
    {
        'id': 'TRAINER_JOHTO_RIVAL_SILVER_6', 'num': 2524, 'cena': 'npc_novo',
        'nome': 'Silver', 'classe': 'TRAINER_CLASS_RIVAL_LATE_FRLG',
        'pic': 'TRAINER_PIC_RIVAL_LATE_FRLG', 'genero': 'Male',
        'fonte': 'hns TRAINER_RIVAL_TOTODILE_6 (MtMoon_Cave/scripts.inc:46)',
        'mapa': 'MtMoon_1F_Frlg', 'prefixo': 'MtMoon_1F',
        'ontransition': 'MtMoon_1F_OnTransition',
        'localid': 'LOCALID_MT_MOON_1F_SILVER',
        'flag': 'FLAG_HIDE_SILVER_MT_MOON', 'flag_crua': 'FLAG_UNUSED_0x1D04',
        # (5,9) era o posto natural e foi MEDIDO como ruim: o TRAINER_HIKER_MARCOS
        # de (7,10) e MOVEMENT_TYPE_WANDER_AROUND com raio de visao 1, e a suite
        # pegou ele abrindo batalha ANTES do Silver (T143.5, primeira rodada).
        # (4,6) fica encostado no warp 0, do outro lado da sala.
        'gfx': 'OBJ_EVENT_GFX_RED', 'x': 4, 'y': 6, 'elev': 3,
        'olhar': 'MOVEMENT_TYPE_FACE_RIGHT',
        'depois_de': 'TRAINER_JOHTO_RIVAL_SILVER_5',
        'regiao': 'johto', 'papel': 'rival', 'identidade': 'silver',
        'ace': 109, 'gimmick': 'mega', 'slot': 5, 'lendario': 'SPECIES_LUGIA',
        'time': time_silver(109, ursaluna),
        'texto': {
            'seen': ['..................................\\p',
                     'It\'s been a while, {PLAYER}.\\p',
                     '…Since I lost to you, I thought about\\n',
                     'what I was lacking with my POKéMON…\\p',
                     'And we came up with an answer.\\p',
                     '{PLAYER}, now we\'ll show you!$'],
            'beaten': ['..................................\\p',
                       'I thought I raised my POKéMON to be the\\n',
                       'best they could be…\\p',
                       '…But it still wasn\'t enough…$'],
            'after': ['..................................\\p',
                      '…You won, fair and square.\\p',
                      'I admit it. But this isn\'t the end.\\p',
                      'I\'m going to be the greatest POKéMON\\n',
                      'trainer ever.\\p',
                      'Because these guys are behind me.$'],
        },
    },
    {
        'id': 'TRAINER_JOHTO_RIVAL_SILVER_7', 'num': 2525, 'cena': 'npc_novo',
        'nome': 'Silver', 'classe': 'TRAINER_CLASS_RIVAL_LATE_FRLG',
        'pic': 'TRAINER_PIC_RIVAL_LATE_FRLG', 'genero': 'Male',
        'fonte': 'hns TRAINER_RIVAL_TOTODILE_7 (IndigoPlateau_PokemonCenter/scripts.inc:84)',
        'mapa': 'IndigoPlateau_PokemonCenter_1F_Frlg', 'prefixo': 'IndigoPlateau_PokemonCenter_1F',
        'ontransition': 'IndigoPlateau_PokemonCenter_1F_OnTransition',
        'localid': 'LOCALID_INDIGO_PLATEAU_POKEMON_CENTER_1F_SILVER',
        'flag': 'FLAG_HIDE_SILVER_INDIGO', 'flag_crua': 'FLAG_UNUSED_0x1D05',
        'gfx': 'OBJ_EVENT_GFX_RED', 'x': 11, 'y': 13, 'elev': 3,
        'olhar': 'MOVEMENT_TYPE_FACE_DOWN',
        'depois_de': 'TRAINER_JOHTO_RIVAL_SILVER_6',
        'regiao': 'johto', 'papel': 'rival', 'identidade': 'silver',
        'ace': 113, 'gimmick': 'mega', 'slot': 5, 'lendario': 'SPECIES_LUGIA',
        'time': time_silver(113, ursaluna),
        'texto': {
            'seen': ['Hold it.\\p', 'You\'re going to take the POKéMON\\n',
                     'LEAGUE challenge now?\\p', 'That\'s not going to happen.\\p',
                     'My super-well-trained POKéMON\\n', 'are going to pound you.\\p',
                     '{PLAYER}!\\n', 'I challenge you!$'],
            'beaten': ['…\\p', 'OK--I lost…$'],
            'after': ['…Darn… I still can\'t win…\\p',
                      'I… I have to think more about my\\n', 'POKéMON…\\p',
                      'Humph! Try not to lose!$'],
        },
    },
    {
        'id': 'TRAINER_UNOVA_RYOKU1', 'num': 2526, 'cena': 'npc_existente',
        'nome': 'RYOKU', 'classe': 'Expert', 'pic': 'Expert M', 'genero': 'Male',
        'fonte': 'bw3g RYOKU1 (data/trainers/parties.asm:4161, maps/AccumulaTown.asm:43)',
        'mapa': 'Unova_AccumulaTown', 'prefixo': 'Unova_AccumulaTown',
        'rotulo_npc': 'Unova_AccumulaTown_EventScript_Npc8',
        'texto_seen': 'Unova_AccumulaTown_Text_AccumulaTownRyokuIntroText',
        'regiao': 'unova', 'papel': 'vilao', 'equipe': 'plasma',
        'tema': ['TYPE_GRASS'], 'identidade': 'ryoku',
        'ace': 228, 'gimmick': 'z', 'slot': 5, 'lendario': 'SPECIES_WO_CHIEN',
        'time': time_ryoku(228),
        'texto': {
            'beaten': ['Oh dear…$'],
            'after': ['RYOKU: I-I must\\n', 'retreat! Here,\\l', 'take it!$'],
        },
    },
    {
        'id': 'TRAINER_UNOVA_N', 'num': 2527, 'cena': 'npc_existente',
        'nome': 'N', 'classe': 'TRAINER_CLASS_CHAMPION', 'pic': 'TRAINER_PIC_CHAMPION_WALLACE',
        'genero': 'Male',
        'fonte': 'bw3g N1 (data/trainers/parties.asm:4989, maps/NsRoom.asm:29)',
        'mapa': 'Unova_NsRoom', 'prefixo': 'Unova_NsRoom',
        'rotulo_npc': 'Unova_NsRoom_EventScript_Npc0',
        'texto_seen': 'Unova_NsRoom_Text_NsRoomIntroText',
        # O N MUDA DE LUGAR, e o motivo foi medido: o unico warp do NsRoom e um
        # `MB_NON_ANIMATED_DOOR` em (0,4) (varredura de comportamento do layout
        # inteiro: nenhum outro tile do mapa dispara warp), e porta larga o
        # jogador UM tile ao sul, em (0,5). O (0,5) so faz fronteira com (1,5) e
        # (0,6), que sao parede, e com o proprio (0,4): pisar ali e sair. Com o N
        # da fonte em (5,2) ele era inalcancavel.
        # Mover o WARP nao resolve, e isso tambem e medicao e nao palpite: nenhum
        # outro tile do mapa tem comportamento de warp, entao warp em coordenada
        # nova nao dispararia e o jogador ficaria preso para sempre. Por isso o N
        # vai para (0,4), a porta, que e o unico tile alcancavel a partir de
        # (0,5). Ele bloqueia a saida ate a batalha e some depois, exatamente como
        # a fonte faz (`disappear NSROOM_N`, maps/NsRoom.asm:43).
        'x': 0, 'y': 4, 'elev': 0, 'olhar': 'MOVEMENT_TYPE_FACE_DOWN',
        'localid': 'LOCALID_UNOVA_NS_ROOM_N',
        'flag': 'FLAG_HIDE_UNOVA_N', 'flag_crua': 'FLAG_UNUSED_0x1D06',
        'regiao': 'unova', 'papel': 'rival', 'identidade': 'n',
        'ace': 255, 'gimmick': 'z', 'slot': 5, 'lendario': 'SPECIES_KYUREM_WHITE',
        'time': time_n(255),
        'texto': {
            'beaten': ['I see… So that\'s\\n', 'the kind of\\l', 'trainer you are…$'],
            'after': ['Your POKéMON…\\p', 'I can hear them.\\p',
                      'You truly are a\\n', 'kind and noble\\l', 'trainer.$'],
        },
    },
    {
        'id': 'TRAINER_UNOVA_HUGH_TEPIG', 'num': 2528, 'cena': 'npc_existente',
        'nome': 'Hugh', 'classe': 'TRAINER_CLASS_RIVAL_LATE_FRLG',
        'pic': 'TRAINER_PIC_RIVAL_LATE_FRLG', 'genero': 'Male',
        'fonte': 'bw3g HUGH_TEPIG (data/trainers/parties.asm:4875, maps/DriftveilShelter.asm:237)',
        'mapa': 'Unova_DriftveilShelter', 'prefixo': 'Unova_DriftveilShelter',
        'rotulo_npc': 'Unova_DriftveilShelter_EventScript_Npc4',
        'texto_seen': 'Unova_DriftveilShelter_Text_DriftveilShelterHughRematchText',
        'regiao': 'unova', 'papel': 'rival', 'identidade': 'hugh',
        'ace': 255, 'gimmick': 'mega', 'slot': 5, 'lendario': 'SPECIES_LANDORUS_THERIAN',
        'time': time_hugh(255),
        'texto': {
            'beaten': ['Ugh… This power.$'],
            'after': ['Hmph… You really\\n', 'are strong enough\\l',
                      'to have bested\\l', 'TEAM PLASMA.\\p',
                      'You and I should\\n', 'have a rematch\\l', 'someday.$'],
        },
    },

    # ---- leva 2 (22/08/2026): as tres que a medicao achou e a primeira leva
    # tinha deixado de fora. Todas as tres tem NPC no mapa desde o import de
    # Unova; o que falta e script. Os `objeto_idx` vem do map.json de hoje.
    {
        'id': 'TRAINER_UNOVA_BIANCA', 'num': 2529, 'cena': 'npc_mudo',
        'nome': 'Bianca', 'classe': 'TRAINER_CLASS_RIVAL_LATE_FRLG',
        'pic': 'TRAINER_PIC_RIVAL_LATE_FRLG', 'genero': 'Female',
        'fonte': 'bw3g BIANCA1 (parties.asm:4075, maps/PWTBattleRoom.asm:39)',
        'mapa': 'Unova_PWTBattleRoom', 'prefixo': 'Unova_PWTBattleRoom',
        'objeto_idx': 1,
        'localid': 'LOCALID_UNOVA_PWT_BIANCA',
        'flag': 'FLAG_HIDE_UNOVA_BIANCA', 'flag_crua': 'FLAG_UNUSED_0x1D07',
        'regiao': 'unova', 'papel': 'rival', 'identidade': 'bianca',
        'ace': 232, 'gimmick': 'z', 'slot': 5, 'lendario': 'SPECIES_CRESSELIA',
        'time': time_bianca(232),
        'texto': {
            'seen': ['BIANCA: Now I\'ll\\n', 'get to see first\l',
                     'hand how strong of\l', 'a trainer you\'ve\l',
                     'become, {PLAYER}!$'],
            'beaten': ['Oh! You are good!$'],
            'after': ['BIANCA: Wow, you\\n', 'are good! MARLON\l',
                      'sure was right to\l', 'pick you to be a\l',
                      'POKéMON trainer!$'],
        },
    },
    {
        'id': 'TRAINER_UNOVA_CHEREN_2', 'num': 2530, 'cena': 'npc_mudo',
        'nome': 'Cheren', 'classe': 'TRAINER_CLASS_LEADER',
        'pic': 'TRAINER_PIC_LEADER_NORMAN', 'genero': 'Male',
        'fonte': 'bw3g CHEREN2 (parties.asm:3731, maps/OpelucidBattleHouse.asm:171)',
        'mapa': 'Unova_OpelucidBattleHouse', 'prefixo': 'Unova_OpelucidBattleHouse',
        # o objeto 4 e o unico dos quatro empilhados em (5,2) sem script; os
        # outros tres sao Marlon, Burgh e Cilan e ja falam. Ele sai do monte para
        # (4,2) porque `GetObjectEventIdByPosition` devolve o PRIMEIRO objeto do
        # tile, e no monte quem responderia ao A seria sempre o Marlon.
        'objeto_idx': 4, 'x': 4, 'y': 2, 'elev': 3,
        'olhar': 'MOVEMENT_TYPE_FACE_DOWN',
        'localid': 'LOCALID_UNOVA_OPELUCID_CHEREN',
        'flag': 'FLAG_HIDE_UNOVA_CHEREN_2', 'flag_crua': 'FLAG_UNUSED_0x1D08',
        'regiao': 'unova', 'papel': 'lider', 'identidade': 'cheren',
        'ace': 253, 'gimmick': 'z', 'slot': 5, 'lendario': 'SPECIES_REGIGIGAS',
        'time': time_cheren2(253),
        'texto': {
            'seen': ['Ah, {PLAYER}.\\n', 'Welcome to the\l', 'BATTLE HOUSE.\p',
                     'How\'d you like to\\n', 'be my opponent\l', 'today?$'],
            'beaten': ['I see, so that was\\n', 'your strategy.$'],
            'after': ['If you want to be\\n', 'a great POKéMON\l',
                      'trainer, you\'ve got\l', 'to keep improving\l',
                      'yourself.$'],
        },
    },
    {
        'id': 'TRAINER_UNOVA_NATE_SNIVY', 'num': 2531, 'cena': 'ramo',
        'nome': 'Nate', 'classe': 'TRAINER_CLASS_RIVAL_LATE_FRLG',
        'pic': 'TRAINER_PIC_RIVAL_LATE_FRLG', 'genero': 'Male',
        'fonte': 'bw3g NATE_SNIVY (parties.asm:5189, maps/NimbasaParkOutside.asm:141)',
        'mapa': 'Unova_NimbasaParkOutside', 'prefixo': 'Unova_NimbasaParkOutside',
        'ramo': 'NateRosa', 'ramo_genero': 'MALE', 'ramo_starter': 1,
        'regiao': 'unova', 'papel': 'rival', 'identidade': 'nate_rosa',
        'ace': 255, 'gimmick': 'mega', 'slot': 3, 'lendario': 'SPECIES_MELOETTA',
        'time': time_nate_rosa(255, 'SNIVY'),
        'lider_do_ramo': True,
        'rotulo_npc': 'Unova_NimbasaParkOutside_EventScript_Npc4',
        'rotulos_extra': ['Unova_NimbasaParkOutside_EventScript_Npc5'],
        'texto_seen': 'Unova_NimbasaParkOutside_Text_NimbasaParkOutsideNateRosaText',
        'objetos_idx': [4, 5], 'x': 6, 'y': 9, 'elev': 3,
        'olhar': 'MOVEMENT_TYPE_FACE_LEFT',
        'localid': 'LOCALID_UNOVA_NIMBASA_NATE',
        'localid_extra': ['LOCALID_UNOVA_NIMBASA_ROSA'],
        'flag': 'FLAG_HIDE_UNOVA_NATE_ROSA', 'flag_crua': 'FLAG_UNUSED_0x1D09',
        'texto': {
            'beaten': ['...!$'],
            'after': ['......$'],
        },
    },
    {
        'id': 'TRAINER_UNOVA_NATE_TEPIG', 'num': 2532, 'cena': 'ramo',
        'nome': 'Nate', 'classe': 'TRAINER_CLASS_RIVAL_LATE_FRLG',
        'pic': 'TRAINER_PIC_RIVAL_LATE_FRLG', 'genero': 'Male',
        'fonte': 'bw3g NATE_TEPIG (parties.asm:5217, maps/NimbasaParkOutside.asm:135)',
        'mapa': 'Unova_NimbasaParkOutside', 'prefixo': 'Unova_NimbasaParkOutside',
        'ramo': 'NateRosa', 'ramo_genero': 'MALE', 'ramo_starter': None,
        'regiao': 'unova', 'papel': 'rival', 'identidade': 'nate_rosa',
        'ace': 255, 'gimmick': 'mega', 'slot': 3, 'lendario': 'SPECIES_MELOETTA',
        'time': time_nate_rosa(255, 'TEPIG'),
    },
    {
        'id': 'TRAINER_UNOVA_NATE_OSHAWOTT', 'num': 2533, 'cena': 'ramo',
        'nome': 'Nate', 'classe': 'TRAINER_CLASS_RIVAL_LATE_FRLG',
        'pic': 'TRAINER_PIC_RIVAL_LATE_FRLG', 'genero': 'Male',
        'fonte': 'bw3g NATE_OSHAWOTT (parties.asm:5245, maps/NimbasaParkOutside.asm:138)',
        'mapa': 'Unova_NimbasaParkOutside', 'prefixo': 'Unova_NimbasaParkOutside',
        'ramo': 'NateRosa', 'ramo_genero': 'MALE', 'ramo_starter': 0,
        'regiao': 'unova', 'papel': 'rival', 'identidade': 'nate_rosa',
        'ace': 255, 'gimmick': 'mega', 'slot': 3, 'lendario': 'SPECIES_MELOETTA',
        'time': time_nate_rosa(255, 'OSHAWOTT'),
    },
    {
        'id': 'TRAINER_UNOVA_ROSA_SNIVY', 'num': 2534, 'cena': 'ramo',
        'nome': 'Rosa', 'classe': 'TRAINER_CLASS_RIVAL_LATE_FRLG',
        'pic': 'TRAINER_PIC_RIVAL_LATE_FRLG', 'genero': 'Female',
        'fonte': 'bw3g ROSA_SNIVY (parties.asm:5274, maps/NimbasaParkOutside.asm:156)',
        'mapa': 'Unova_NimbasaParkOutside', 'prefixo': 'Unova_NimbasaParkOutside',
        'ramo': 'NateRosa', 'ramo_genero': 'FEMALE', 'ramo_starter': 1,
        'regiao': 'unova', 'papel': 'rival', 'identidade': 'nate_rosa',
        'ace': 255, 'gimmick': 'mega', 'slot': 3, 'lendario': 'SPECIES_MELOETTA',
        'time': time_nate_rosa(255, 'SNIVY'),
    },
    {
        'id': 'TRAINER_UNOVA_ROSA_TEPIG', 'num': 2535, 'cena': 'ramo',
        'nome': 'Rosa', 'classe': 'TRAINER_CLASS_RIVAL_LATE_FRLG',
        'pic': 'TRAINER_PIC_RIVAL_LATE_FRLG', 'genero': 'Female',
        'fonte': 'bw3g ROSA_TEPIG (parties.asm:5302, maps/NimbasaParkOutside.asm:150)',
        'mapa': 'Unova_NimbasaParkOutside', 'prefixo': 'Unova_NimbasaParkOutside',
        'ramo': 'NateRosa', 'ramo_genero': 'FEMALE', 'ramo_starter': None,
        'regiao': 'unova', 'papel': 'rival', 'identidade': 'nate_rosa',
        'ace': 255, 'gimmick': 'mega', 'slot': 3, 'lendario': 'SPECIES_MELOETTA',
        'time': time_nate_rosa(255, 'TEPIG'),
    },
    {
        'id': 'TRAINER_UNOVA_ROSA_OSHAWOTT', 'num': 2536, 'cena': 'ramo',
        'nome': 'Rosa', 'classe': 'TRAINER_CLASS_RIVAL_LATE_FRLG',
        'pic': 'TRAINER_PIC_RIVAL_LATE_FRLG', 'genero': 'Female',
        'fonte': 'bw3g ROSA_OSHAWOTT (parties.asm:5330, maps/NimbasaParkOutside.asm:153)',
        'mapa': 'Unova_NimbasaParkOutside', 'prefixo': 'Unova_NimbasaParkOutside',
        'ramo': 'NateRosa', 'ramo_genero': 'FEMALE', 'ramo_starter': 0,
        'regiao': 'unova', 'papel': 'rival', 'identidade': 'nate_rosa',
        'ace': 255, 'gimmick': 'mega', 'slot': 3, 'lendario': 'SPECIES_MELOETTA',
        'time': time_nate_rosa(255, 'OSHAWOTT'),
    },
]


def rotula(tabela):
    """Preenche os rotulos de texto de cada entrada. Feito aqui e nao na tabela
    porque sao derivados do id e do mapa, e repetir isso a mao e como o guarda
    de id com comentario: parece igual e um dia nao e."""
    for e in tabela:
        base = e['ramo'] if e.get('ramo') else curto(e)
        e['rot_seen'] = '%s_Text_%sSeen' % (e['prefixo'], base)
        e['rot_beaten'] = '%s_Text_%sBeaten' % (e['prefixo'], base)
        e['rot_depois'] = '%s_Text_%sDepois' % (e['prefixo'], base)
    return tabela


# ------------------------------------------------------------------ guarda
def verifica(tabela):
    """Reprovacoes. Lista vazia = da para aplicar."""
    erros = []
    oppo = open(OPPO, encoding='utf-8').read()
    frlg = open(os.path.join(RAIZ, 'include', 'constants', 'opponents_frlg.h'),
                encoding='utf-8').read()
    # O `(?:\s*(?://|/\*).*)?$` no fim NAO e enfeite: metade das constantes de
    # treinador deste repo tem comentario na mesma linha (`... 1358  // Cherrygrove`),
    # e sem ele a varredura enxergava so a outra metade. O --demo pegou isto.
    usados = {int(v): n for n, v in
              re.findall(r'^#define (TRAINER_[A-Z0-9_]+)\s+(\d+)\s*(?:(?://|/\*).*)?$',
                         oppo + frlg, re.M)}
    party = open(PARTY, encoding='utf-8').read()
    flags = open(FLAGS, encoding='utf-8').read()
    vistos = set()

    for e in tabela:
        if e['num'] in usados and usados[e['num']] != e['id']:
            erros.append('%s: id %d ja e do %s' % (e['id'], e['num'], usados[e['num']]))
        if e['num'] in vistos:
            erros.append('%s: id %d repetido dentro da propria tabela' % (e['id'], e['num']))
        vistos.add(e['num'])

        inc = os.path.join(RAIZ, 'data', 'maps', e['mapa'], 'scripts.inc')
        if not os.path.exists(inc):
            erros.append('%s: o mapa %s nao existe neste repo' % (e['id'], e['mapa']))
            continue
        texto_inc = open(inc, encoding='utf-8').read()

        if e.get('flag'):
            if re.search(r'^#define\s+%s\s' % re.escape(e['flag_crua']), flags, re.M) is None:
                erros.append('%s: %s nao existe em flags.h' % (e['id'], e['flag_crua']))
            apelidada = re.search(r'^#define\s+(?!%s\b)[A-Z0-9_]+\s+%s\s*(//.*)?$'
                                  % (re.escape(e['flag']), re.escape(e['flag_crua'])),
                                  flags, re.M)
            if apelidada:
                erros.append('%s: %s ja tem apelido (%s)'
                             % (e['id'], e['flag_crua'], apelidada.group(0).split()[1]))
        if e['cena'] == 'npc_novo':
            mapa = json.load(open(os.path.join(RAIZ, 'data', 'maps', e['mapa'], 'map.json'),
                                  encoding='utf-8'))
            for o in mapa.get('object_events', []):
                if o.get('local_id') == e['localid']:
                    continue
                if (o['x'], o['y']) == (e['x'], e['y']):
                    erros.append('%s: ja existe objeto em (%d,%d) de %s'
                                 % (e['id'], e['x'], e['y'], e['mapa']))
            for w in mapa.get('warp_events', []):
                if (w['x'], w['y']) == (e['x'], e['y']):
                    erros.append('%s: (%d,%d) e warp em %s' % (e['id'], e['x'], e['y'], e['mapa']))
            if not colisao_livre(e['mapa'], e['x'], e['y']):
                erros.append('%s: (%d,%d) tem colisao em %s; o NPC ficaria dentro da parede'
                             % (e['id'], e['x'], e['y'], e['mapa']))
            alvo = e['ontransition']
            if alvo not in texto_inc:
                erros.append('%s: %s nao tem %s para pendurar o portao'
                             % (e['id'], e['mapa'], alvo))
        elif e['cena'] in ('npc_mudo', 'ramo'):
            objetos = json.load(open(os.path.join(RAIZ, 'data', 'maps', e['mapa'],
                                                  'map.json'),
                                     encoding='utf-8')).get('object_events', [])
            idxs = e.get('objetos_idx') or ([e['objeto_idx']]
                                            if 'objeto_idx' in e else [])
            for i in idxs:
                if i >= len(objetos):
                    erros.append('%s: %s nao tem objeto de indice %d'
                                 % (e['id'], e['mapa'], i))
                elif e['cena'] == 'npc_mudo' and objetos[i].get('script') not in (
                        '0', '%s_EventScript_%s' % (e['prefixo'], curto(e))):
                    erros.append('%s: o objeto %d de %s ja tem script (%s)'
                                 % (e['id'], i, e['mapa'], objetos[i].get('script')))
            if e['cena'] == 'ramo' and e.get('lider_do_ramo'):
                for r in [e['rotulo_npc']] + list(e.get('rotulos_extra', [])):
                    if r + '::' not in texto_inc:
                        erros.append('%s: %s nao tem o rotulo %s'
                                     % (e['id'], e['mapa'], r))
        else:
            if e['rotulo_npc'] + '::' not in texto_inc:
                erros.append('%s: %s nao tem o rotulo %s'
                             % (e['id'], e['mapa'], e['rotulo_npc']))
            if e['texto_seen'] + '::' not in texto_inc:
                erros.append('%s: %s nao tem o texto %s'
                             % (e['id'], e['mapa'], e['texto_seen']))
        if '=== %s ===' % e['id'] in party and MARCA_INC not in party:
            erros.append('%s: ja existe bloco no trainers.party e nao e nosso' % e['id'])
    return erros


def colisao_livre(mapa, x, y):
    """Le o blockdata do layout: bits 10-11 do u16 sao a colisao, 0 = passavel.

    A mesma leitura de valida_warp_tile.py:299. Sem isto o NPC pode nascer dentro
    da parede, e nada no build reclama."""
    import struct
    layouts = json.load(open(os.path.join(RAIZ, 'data', 'layouts', 'layouts.json'),
                             encoding='utf-8'))
    byid = {l['id']: l for l in layouts['layouts'] if l}
    d = json.load(open(os.path.join(RAIZ, 'data', 'maps', mapa, 'map.json'), encoding='utf-8'))
    lay = byid[d['layout']]
    w, h = lay['width'], lay['height']
    if not (0 <= x < w and 0 <= y < h):
        return False
    blk = open(os.path.join(RAIZ, lay['blockdata_filepath']), 'rb').read()
    i = (y * w + x) * 2
    return ((struct.unpack('<H', blk[i:i + 2])[0] >> 10) & 3) == 0


# ------------------------------------------------------------------ escrita
def entre_marcas(texto, ini, fim, corpo):
    """Substitui (ou acrescenta) o bloco entre `ini` e `fim`. Idempotente."""
    novo = '%s\n%s\n%s\n' % (ini, corpo.rstrip('\n'), fim)
    padrao = re.compile(re.escape(ini) + r'.*?' + re.escape(fim) + r'\n?', re.S)
    if padrao.search(texto):
        # lambda e nao string: o corpo tem `\p` e `\n` do charmap, e o re.sub
        # com string tenta interpretar isso como escape ("bad escape \p"). Este
        # bug so aparece na SEGUNDA rodada, que e o que --aplicar duas vezes pega.
        return padrao.sub(lambda _: novo, texto)
    return texto.rstrip('\n') + '\n\n' + novo


def escreve_opponents(tabela):
    texto = open(OPPO, encoding='utf-8').read()
    linhas = []
    for e in tabela:
        linhas.append('#define %-52s %d  // %s' % (e['id'], e['num'], e['fonte']))
    corpo = '\n'.join(linhas)
    ini = '// >>> %s >>>' % MARCA_OPPO
    fim = '// <<< %s <<<' % MARCA_OPPO
    bloco = '%s\n%s\n%s\n' % (ini, corpo, fim)
    padrao = re.compile(re.escape(ini) + r'.*?' + re.escape(fim) + r'\n', re.S)
    if padrao.search(texto):
        novo = padrao.sub(bloco, texto)
    else:
        alvo = '#define MAX_TRAINERS_COUNT_EMERALD'
        novo = texto.replace(alvo, bloco + '\n' + alvo, 1)
    if novo != texto:
        open(OPPO, 'w', encoding='utf-8').write(novo)
    return novo != texto


def escreve_flags(tabela):
    novos = [e for e in tabela if e.get('flag')]
    if not novos:
        return False
    texto = open(FLAGS, encoding='utf-8').read()
    linhas = ['// Apelidar FLAG_UNUSED nao mexe em FLAGS_COUNT: a save nao muda.']
    for e in novos:
        linhas.append('#define %-40s %s  // %s' % (e['flag'], e['flag_crua'], e['mapa']))
    novo = entre_marcas(texto, '// >>> %s >>>' % MARCA_FLAGS,
                        '// <<< %s <<<' % MARCA_FLAGS, '\n'.join(linhas))
    if novo != texto:
        open(FLAGS, 'w', encoding='utf-8').write(novo)
    return novo != texto


def bloco_party(e):
    linhas = ['=== %s ===' % e['id'],
              'Name: %s' % e['nome'],
              'Class: %s' % e['classe'],
              'Pic: %s' % e['pic'],
              'Gender: %s' % e['genero'],
              'Double Battle: No',
              'AI: %s' % ' / '.join(IA)]
    for m in e['time']:
        linhas.append('')
        linhas.append('%s @ %s' % (m['especie'], m['item']))
        linhas.append('Level: %d' % m['nivel'])
        if m['habilidade']:
            linhas.append('Ability: %s' % m['habilidade'])
        linhas.append('Nature: %s' % m['natureza'])
        linhas.append('IVs: %s' % m['ivs'])
        linhas.append('EVs: %s' % m['evs'])
        linhas += ['- %s' % g for g in m['golpes']]
    return '\n'.join(linhas)


def escreve_party(tabela):
    """CRIA o bloco que falta e nunca reescreve o que ja existe.

    Reescrever seria briga: depois deste script quem manda no time de chefe e o
    `fase_f_chefes.py`, e as duas ferramentas escrevendo o MESMO bloco davam
    diff a cada rodada alternada (medido: `--aplicar` de um sempre sujava o
    outro). Aqui o importador so abre a vaga; o time e do outro."""
    texto = open(PARTY, encoding='utf-8').read()
    faltam = [e for e in tabela if '=== %s ===' % e['id'] not in texto]
    if not faltam:
        return False
    corpo = '\n\n'.join(bloco_party(e) for e in faltam)
    ini, fim = ('/* >>> %s >>> */' % MARCA_INC, '/* <<< %s <<< */' % MARCA_INC)
    if ini in texto:
        # o bloco de marcas ja existe: acrescenta ANTES do fechamento
        novo = texto.replace(fim, corpo + '\n' + fim, 1)
    else:
        novo = entre_marcas(texto, ini, fim, corpo)
    open(PARTY, 'w', encoding='utf-8').write(novo)
    return True


def texto_asm(rotulo, linhas):
    return '\n'.join(['%s::' % rotulo] + [T + '.string "%s"' % l for l in linhas])


def cena_npc_novo(e):
    p, tid = e['prefixo'], e['id']
    return '\n'.join([
        '%s_EventScript_SilverPorta::' % p,
        T + 'setflag %s' % e['flag'],
        T + 'goto_if_not_defeated %s, Common_EventScript_NopReturn' % e['depois_de'],
        T + 'goto_if_defeated %s, Common_EventScript_NopReturn' % tid,
        T + 'clearflag %s' % e['flag'],
        T + 'return',
        '',
        '%s_EventScript_Silver::' % p,
        T + 'trainerbattle_single %s, %s_Text_SilverSeen, %s_Text_SilverBeaten' % (tid, p, p),
        T + 'msgbox %s_Text_SilverAfter, MSGBOX_DEFAULT' % p,
        T + 'closemessage',
        T + 'setflag %s' % e['flag'],
        T + 'removeobject %s' % e['localid'],
        T + 'release',
        T + 'end',
        '',
        texto_asm('%s_Text_SilverSeen' % p, e['texto']['seen']),
        '',
        texto_asm('%s_Text_SilverBeaten' % p, e['texto']['beaten']),
        '',
        texto_asm('%s_Text_SilverAfter' % p, e['texto']['after']),
    ])


def fecho(e):
    """As linhas que somem com o NPC depois da batalha.

    A flag e SO ACESA, nunca apagada, entao nao precisa de ON_TRANSITION. O
    `removeobject` sozinho nao bastaria: ele vale ate o mapa recarregar, e na
    volta o NPC estaria de pe e ja derrotado, ou seja sem batalha nenhuma para
    tira-lo de novo. Isto e o `disappear` que a fonte tambem faz."""
    if not e.get('flag'):
        return []
    saida = [T + 'closemessage', T + 'setflag %s' % e['flag']]
    for lid in [e['localid']] + list(e.get('localid_extra', [])):
        saida.append(T + 'removeobject %s' % lid)
    return saida


def leaf(e, rotulo, seen, dono=None):
    """A batalha em si, igual nos tres modos de NPC ja existente.

    `dono` existe por causa do ramo: as SEIS variantes de Nate/Rosa somem pelos
    MESMOS dois objetos e pela MESMA flag, que vivem so na entrada lider. Sem
    isto, cinco das seis venciam e deixavam o NPC de pe."""
    d = dono or e
    return [
        '%s::' % rotulo,
        T + 'trainerbattle_single %s, %s, %s' % (e['id'], seen, d['rot_beaten']),
        T + 'msgbox %s, MSGBOX_DEFAULT' % d['rot_depois'],
    ] + fecho(d) + [T + 'release', T + 'end']


def cena_ramo(grupo):
    """UMA cena para as seis variantes de Nate/Rosa.

    O ramo e o da fonte, comando a comando (maps/NimbasaParkOutside.asm:127-156):
    primeiro o genero do jogador, depois o inicial, e o inicial NAO testa os
    tres: dois `goto_if_eq` e o terceiro cai por fallthrough, como os dois
    `checkevent` de la. O mapa inicial->rival tambem e o da fonte, e da a
    vantagem de tipo ao JOGADOR: Snivy (VAR_STARTER_MON 0) enfrenta a variante
    OSHAWOTT, Tepig (1) enfrenta a SNIVY, Oshawott (2) enfrenta a TEPIG. E o
    mesmo mapa que o Unova_ChampionsRoom ja usa para a Juniper."""
    lider = grupo[0]
    p = lider['prefixo']
    rot = '%s_EventScript_%s' % (p, lider['ramo'])
    rot_f = rot + 'Feminino'
    seen = lider['texto_seen']

    def leque(genero, rotulo):
        linhas = ['%s::' % rotulo]
        fallback = None
        for e in grupo:
            if e['ramo_genero'] != genero:
                continue
            if e['ramo_starter'] is None:
                fallback = e
            else:
                linhas.append(T + 'goto_if_eq VAR_STARTER_MON, %d, %s_EventScript_%s'
                              % (e['ramo_starter'], p, curto(e)))
        linhas.append(T + 'goto %s_EventScript_%s' % (p, curto(fallback)))
        return linhas

    saida = ['%s::' % rot, T + 'checkplayergender',
             T + 'goto_if_eq VAR_RESULT, FEMALE, %s' % rot_f]
    saida += leque('MALE', '%s_EventScript_%sMasculino' % (p, lider['ramo']))[1:]
    saida += ['', ] + leque('FEMALE', rot_f)
    for e in grupo:
        saida += [''] + leaf(e, '%s_EventScript_%s' % (p, curto(e)), seen, lider)
    saida += ['', texto_asm(lider['rot_beaten'], lider['texto']['beaten']),
              '', texto_asm(lider['rot_depois'], lider['texto']['after'])]
    return '\n'.join(saida)


def cena_npc_mudo(e):
    """NPC que o import de mapa deixou com `script: "0"`: nada a substituir, o
    campo `script` do map.json passa a apontar para a cena."""
    return '\n'.join(
        leaf(e, '%s_EventScript_%s' % (e['prefixo'], curto(e)), e['rot_seen'])
        + ['', texto_asm(e['rot_seen'], e['texto']['seen']),
           '', texto_asm(e['rot_beaten'], e['texto']['beaten']),
           '', texto_asm(e['rot_depois'], e['texto']['after'])])


def cena_npc_existente(e):
    """NPC que ja falava: o `msgbox` dele vira `goto` para a batalha."""
    return '\n'.join(
        leaf(e, '%s_EventScript_%s' % (e['prefixo'], curto(e)), e['texto_seen'])
        + ['', texto_asm(e['rot_beaten'], e['texto']['beaten']),
           '', texto_asm(e['rot_depois'], e['texto']['after'])])


def pendura_portao(texto, e):
    """Insere `call <prefixo>_EventScript_SilverPorta` antes do `end` do
    ON_TRANSITION que o mapa JA tem. Um mapa so honra UM handler por tipo, entao
    acrescentar uma segunda linha `map_script MAP_SCRIPT_ON_TRANSITION` seria
    trabalho perdido e silencioso."""
    chamada = T + 'call %s_EventScript_SilverPorta' % e['prefixo']
    if chamada in texto:
        return texto
    rot = e['ontransition']
    m = re.search(r'^%s::?\n(.*?)^(\tend\n)' % re.escape(rot), texto, re.S | re.M)
    if not m:
        raise SystemExit('nao achei o corpo de %s' % rot)
    return texto[:m.start(2)] + chamada + '\n' + texto[m.start(2):]


def escreve_scripts(tabela):
    mexeu = False
    por_mapa = collections.OrderedDict()
    for e in tabela:
        por_mapa.setdefault(e['mapa'], []).append(e)
    for mapa, entradas in por_mapa.items():
        caminho = os.path.join(RAIZ, 'data', 'maps', mapa, 'scripts.inc')
        original = open(caminho, encoding='utf-8').read()
        texto = original
        corpos = []
        ramos = collections.OrderedDict()
        for e in entradas:
            if e['cena'] == 'npc_novo':
                texto = pendura_portao(texto, e)
                corpos.append(cena_npc_novo(e))
            elif e['cena'] == 'npc_mudo':
                corpos.append(cena_npc_mudo(e))
            elif e['cena'] == 'ramo':
                ramos.setdefault(e['ramo'], []).append(e)
            else:
                texto = liga_npc(texto, e)
                corpos.append(cena_npc_existente(e))
        for nome, grupo in ramos.items():
            lider = grupo[0]
            rot = '%s_EventScript_%s' % (lider['prefixo'], nome)
            for r in [lider['rotulo_npc']] + list(lider.get('rotulos_extra', [])):
                texto = liga_npc(texto, lider, rotulo=r, destino=rot)
            corpos.append(cena_ramo(grupo))
        novo = entre_marcas(texto, '@ >>> %s >>>' % MARCA_INC,
                            '@ <<< %s <<<' % MARCA_INC, '\n\n'.join(corpos))
        if novo != original:
            open(caminho, 'w', encoding='utf-8').write(novo)
            mexeu = True
    return mexeu


def liga_npc(texto, e, rotulo=None, destino=None):
    """Troca o corpo `msgbox X, MSGBOX_NPC / end` do NPC por um `goto`."""
    rotulo = rotulo or e['rotulo_npc']
    destino = destino or '%s_EventScript_%s' % (e['prefixo'], curto(e))
    velho = '%s::\n%smsgbox %s, MSGBOX_NPC\n%send\n' % (rotulo, T, e['texto_seen'], T)
    novo = '%s::\n%sgoto %s\n' % (rotulo, T, destino)
    if velho in texto:
        return texto.replace(velho, novo, 1)
    if novo in texto:
        return texto
    raise SystemExit('%s: nao reconheci o corpo de %s' % (e['id'], rotulo))


def reposiciona(e):
    """Mexe em NPC que o import de mapa ja tinha posto: posicao, local_id, flag
    e, no modo `npc_mudo`, o proprio campo `script`.

    Acha o objeto pelo INDICE declarado quando ele existe, senao pelo script.
    Indice de object_event e o que `removeobject` usa, entao a ORDEM da lista
    nunca muda aqui: so o conteudo das entradas."""
    caminho = os.path.join(RAIZ, 'data', 'maps', e['mapa'], 'map.json')
    original = open(caminho, encoding='utf-8').read()
    d = json.loads(original, object_pairs_hook=collections.OrderedDict)
    objetos = d.get('object_events', [])
    idxs = e.get('objetos_idx') or ([e['objeto_idx']] if 'objeto_idx' in e else [])
    lids = [e['localid']] + list(e.get('localid_extra', []))
    if not idxs:
        alvos = [e.get('rotulo_npc'), '%s_EventScript_%s' % (e['prefixo'], curto(e))]
        idxs = [i for i, o in enumerate(objetos)
                if o.get('script') in alvos or o.get('local_id') == e['localid']][:1]
    if not idxs:
        raise SystemExit('%s: nao achei o objeto de %s' % (e['id'], e['mapa']))
    for k, i in enumerate(idxs):
        o = objetos[i]
        o['local_id'] = lids[k] if k < len(lids) else lids[-1]
        if 'x' in e:
            o['x'], o['y'] = e['x'], e['y']
            o['elevation'] = e['elev']
            o['movement_type'] = e['olhar']
        if e.get('flag'):
            o['flag'] = e['flag']
        if e['cena'] == 'npc_mudo':
            o['script'] = '%s_EventScript_%s' % (e['prefixo'], curto(e))
        elif e['cena'] == 'ramo':
            o['script'] = '%s_EventScript_%s' % (e['prefixo'], e['ramo'])
    saida = json.dumps(d, ensure_ascii=False, indent=2) + '\n'
    if saida == original:
        return False
    open(caminho, 'w', encoding='utf-8').write(saida)
    return True


def escreve_mapas(tabela):
    mexeu = False
    for e in tabela:
        if e['cena'] != 'npc_novo':
            # so o LIDER do ramo mexe em objeto; as outras cinco variantes
            # compartilham os mesmos dois NPCs
            if e['cena'] == 'ramo' and not e.get('lider_do_ramo'):
                continue
            # NPC que so trocou de fala nao mexe em objeto nenhum: sem posicao
            # nova, sem flag e sem script novo, nao ha o que reescrever
            if e['cena'] == 'npc_existente' and 'x' not in e and not e.get('flag'):
                continue
            mexeu = reposiciona(e) or mexeu
            continue
        caminho = os.path.join(RAIZ, 'data', 'maps', e['mapa'], 'map.json')
        original = open(caminho, encoding='utf-8').read()
        d = json.loads(original, object_pairs_hook=collections.OrderedDict)
        objetos = d.setdefault('object_events', [])
        novo = collections.OrderedDict([
            ('local_id', e['localid']),
            ('graphics_id', e['gfx']),
            ('x', e['x']), ('y', e['y']), ('elevation', e['elev']),
            ('movement_type', e['olhar']),
            ('movement_range_x', 0), ('movement_range_y', 0),
            ('trainer_type', 'TRAINER_TYPE_NONE'),
            ('trainer_sight_or_berry_tree_id', '0'),
            ('script', '%s_EventScript_Silver' % e['prefixo']),
            ('flag', e['flag']),
        ])
        for i, o in enumerate(objetos):
            if o.get('local_id') == e['localid']:
                objetos[i] = novo
                break
        else:
            objetos.append(novo)
        saida = json.dumps(d, ensure_ascii=False, indent=2) + '\n'
        if saida != original:
            open(caminho, 'w', encoding='utf-8').write(saida)
            mexeu = True
    return mexeu


def escreve_fase_f(tabela):
    original = open(FASEF, encoding='utf-8').read()
    d = json.loads(original, object_pairs_hook=collections.OrderedDict)
    porid = {c['id']: i for i, c in enumerate(d['chefes'])}
    for e in tabela:
        linha = collections.OrderedDict([
            ('id', e['id']), ('regiao', e['regiao']), ('papel', e['papel']),
            ('identidade', e['identidade']), ('ace', e['ace']),
            ('gimmick', e['gimmick']), ('gimmick_slot', e['slot']),
            ('lendario', e['lendario']), ('ai', IA), ('time', e['time']),
        ])
        if e['papel'] == 'vilao':
            linha['equipe'] = e['equipe']
            linha['tema'] = e['tema']
        if e['id'] in porid:
            d['chefes'][porid[e['id']]] = linha
        else:
            d['chefes'].append(linha)
    saida = json.dumps(d, ensure_ascii=False, indent=1) + '\n'
    if saida != original:
        open(FASEF, 'w', encoding='utf-8').write(saida)
    return saida != original


# ------------------------------------------------------------------ demo
def demo():
    """Mutacoes plantadas. Cada uma TEM de reprovar."""
    base = verifica(TABELA)
    if base:
        print('DEMO ABORTADA: a tabela de verdade ja esta reprovando:')
        for e in base:
            print('  ' + e)
        return 1
    casos = []

    t = json.loads(json.dumps(TABELA))
    t[0]['num'] = 1358  # TRAINER_JOHTO_RIVAL_SILVER_1
    casos.append(('id de treinador que ja tem dono', t))

    t = json.loads(json.dumps(TABELA))
    t[1]['x'], t[1]['y'] = 0, 9  # parede solida do MtMoon_1F_Frlg
    casos.append(('NPC dentro da parede', t))

    t = json.loads(json.dumps(TABELA))
    t[4]['rotulo_npc'] = 'Unova_NsRoom_EventScript_NaoExiste'
    casos.append(('NPC existente que nao existe', t))

    ruim = 0
    for nome, mutante in casos:
        erros = verifica(mutante)
        if erros:
            print('OK    %-38s reprovado: %s' % (nome, erros[0]))
        else:
            print('FALHA %-38s PASSOU e nao devia' % nome)
            ruim += 1
    print('\ndemo: %d/%d mutacoes reprovadas' % (len(casos) - ruim, len(casos)))
    return 1 if ruim else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seco', action='store_true')
    ap.add_argument('--demo', action='store_true')
    ap.add_argument('--aplicar', action='store_true')
    args = ap.parse_args()

    if args.demo:
        return demo()

    erros = verifica(TABELA)
    if erros:
        print('REPROVADO (%d):' % len(erros))
        for e in erros:
            print('  ' + e)
        return 1

    if not args.aplicar:
        print(NIVEL_MEDIDO.strip())
        print()
        for e in TABELA:
            print('%-32s id %d  %-38s ace %3d  %-5s  %s'
                  % (e['id'], e['num'], e['mapa'], e['ace'], e['gimmick'],
                     e['lendario'].replace('SPECIES_', '')))
        print('\n%d batalhas; nada foi escrito (use --aplicar)' % len(TABELA))
        return 0

    mexeu = [escreve_opponents(TABELA), escreve_flags(TABELA), escreve_party(TABELA),
             escreve_mapas(TABELA), escreve_scripts(TABELA), escreve_fase_f(TABELA)]
    nomes = ['opponents.h', 'flags.h', 'trainers.party', 'map.json', 'scripts.inc',
             'fase_f_chefes.json']
    for n, m in zip(nomes, mexeu):
        print('%-20s %s' % (n, 'escrito' if m else 'ja estava como devia'))
    print('\nagora rode: python3 dev_scripts/fase_f_chefes.py --demo && '
          'python3 dev_scripts/fase_f_chefes.py --aplicar')
    return 0


rotula(TABELA)

if __name__ == '__main__':
    sys.exit(main())
