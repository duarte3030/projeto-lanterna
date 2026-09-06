@ BURNED TOWER B1F, portado de fontes-mapas/hns/data/maps/BurnedTower_B1F.
@ ponytail: RAIKOU, ENTEI e SUICUNE nao tem sprite que esta build desenha
@ (OBJ_EVENT_GFX_RAIKOU/ENTEI/SUICUNE existem no enum mas so tem entrada em
@ object_event_graphics_info_pointers.h dentro de #if IS_FRLG; usar
@ reiniciaria o jogo na tela de titulo). Igual foi feito com Dialga e Palkia
@ no Spear Pillar, a cena virou tres bg_event (sign): sem NPC visivel, so
@ cheiro/grito. No pcrystal original tambem e uma cutscene de "apareceu e
@ sumiu", entao nao perde muito nao ter sprite parado.
@ Pedra de forca portada igual ao padrao vanilla (EventScript_StrengthBoulder
@ + FLAG_TEMP_11, mesma flag que o FieryPath usa pro dele: FLAG_TEMP zera a
@ cada carregamento de mapa, reuso entre mapas diferentes e seguro).
@ Itens usam Common_EventScript_FindItem com FLAG_UNUSED_0x26A/0x26B crus
@ (flags.h esta com outro agente).
@ Nao portado: o cameo do EUSINE aqui embaixo (mesma falta de sprite do 1F) e
@ os quatro bichos de decoracao (KOFFING/MISDREAVUS/MAGMAR via
@ OBJ_EVENT_GFX_MON_BASE, que cai no fallback POKE_BALL nesta build).

BurnedTower_B1F_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, BurnedTower_B1F_OnFrame
	.byte 0

@ >>> Burned Tower, 06/09/2026 (rodada 13) >>>
@ A CENA DOS TRES CAES, que estava faltando e travava Johto inteira: sem ela
@ FLAG_JOHTO_CAES_LIBERTOS nunca acendia, e sem essa flag o sabio de Ecruteak
@ nunca saia da frente da porta do ginasio do MORTY.
@
@ Os tres objetos animados sao os que JA existiam no mapa como decoracao
@ (ENTEI em (18,8), RAIKOU em (14,8), SUICUNE em (16,9), as mesmas coordenadas
@ do hns), agora com local_id e com FLAG_JOHTO_CAES_LIBERTOS no campo `flag`:
@ acesa a flag, eles nao nascem mais. NAO se mexeu nos objetos de Dex
@ (LOCALID_DEX_RAIKOU em (26,12) e LOCALID_DEX_ENTEI em (24,4)), que tem flag
@ propria e continuam sendo batalha de lendario.
@
@ ZERO var de save. Dois gatilhos, os dois com var TEMPORARIA:
@   1. ON_FRAME_TABLE em VAR_TEMP_0 = 0, que e o caso normal: a queda do 1F
@      poe o jogador em (16,12), de frente para a camara selada. A PRIMEIRA
@      linha do roteiro e `setvar VAR_TEMP_0, 1`, e ela nao e enfeite:
@      TryRunOnFrameMapScript e chamado A CADA QUADRO por
@      ProcessPlayerFieldInput (src/field_control_avatar.c:195) e devolve TRUE,
@      que congela o jogador; roteiro de ON_FRAME que nao mata a propria
@      condicao na primeira instrucao trava o jogo.
@   2. coord_event em VAR_TEMP_1 = 0 nas dez lajes de frente para a camara
@      (x de 14 a 18, linhas 11 e 12), que e a rede de seguranca para quem
@      chegar aqui pela ESCADA de (26,7) em vez de pela queda (reset no meio da
@      cena, por exemplo): dali o trio fica fora da tela, e o ON_FRAME ja
@      gastou a vez dele. Tecnica do SINNOH-PADRAO.md, secao "coord_event com
@      gatilho VAR_TEMP_0 e valor 0": o motor zera VAR_TEMP_* a cada entrada de
@      mapa, entao o gatilho esta sempre armado e quem lembra que a cena ja
@      aconteceu e a FLAG.
BurnedTower_B1F_OnFrame:
	map_script_2 VAR_TEMP_0, 0, BurnedTower_B1F_EventScript_ChegouNoPorao
	.2byte 0

BurnedTower_B1F_EventScript_ChegouNoPorao::
	setvar VAR_TEMP_0, 1
	goto BurnedTower_B1F_EventScript_SoltaCaes

BurnedTower_B1F_Trigger_Caes::
	setvar VAR_TEMP_1, 1
	goto BurnedTower_B1F_EventScript_SoltaCaes

BurnedTower_B1F_EventScript_SoltaCaes::
	goto_if_set FLAG_JOHTO_CAES_LIBERTOS, BurnedTower_B1F_EventScript_SoltaCaesFim
	goto_if_not_defeated TRAINER_JOHTO_RIVAL_SILVER_3, BurnedTower_B1F_EventScript_SoltaCaesFim
	lock
	turnobject OBJ_EVENT_ID_PLAYER, DIR_NORTH
	delay 30
	playse SE_PIN
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_ExclamationMark
	waitmovement 0
	delay 30
	msgbox BurnedTower_B1F_Text_CaesAcordam, MSGBOX_DEFAULT
	closemessage

	playmoncry SPECIES_ENTEI, CRY_MODE_NORMAL
	applymovement LOCALID_BURNED_TOWER_B1F_ENTEI, BurnedTower_B1F_Movement_Acorda
	waitmovement 0
	waitmoncry
	playmoncry SPECIES_RAIKOU, CRY_MODE_NORMAL
	applymovement LOCALID_BURNED_TOWER_B1F_RAIKOU, BurnedTower_B1F_Movement_Acorda
	waitmovement 0
	waitmoncry
	playmoncry SPECIES_SUICUNE, CRY_MODE_NORMAL
	applymovement LOCALID_BURNED_TOWER_B1F_SUICUNE, BurnedTower_B1F_Movement_Acorda
	waitmovement 0
	waitmoncry

	playse SE_LEDGE
	applymovement LOCALID_BURNED_TOWER_B1F_ENTEI, BurnedTower_B1F_Movement_EnteiFoge
	waitmovement 0
	playse SE_LEDGE
	applymovement LOCALID_BURNED_TOWER_B1F_RAIKOU, BurnedTower_B1F_Movement_RaikouFoge
	waitmovement 0
	playmoncry SPECIES_SUICUNE, CRY_MODE_NORMAL
	applymovement LOCALID_BURNED_TOWER_B1F_SUICUNE, BurnedTower_B1F_Movement_SuicuneFoge
	waitmovement 0
	waitmoncry

	setflag FLAG_JOHTO_CAES_LIBERTOS
	removeobject LOCALID_BURNED_TOWER_B1F_ENTEI
	removeobject LOCALID_BURNED_TOWER_B1F_RAIKOU
	removeobject LOCALID_BURNED_TOWER_B1F_SUICUNE
	delay 40
	msgbox BurnedTower_B1F_Text_CaesFogem, MSGBOX_DEFAULT
	closemessage
	release
	end

BurnedTower_B1F_EventScript_SoltaCaesFim::
	end

BurnedTower_B1F_Movement_Acorda:
	jump_in_place_down
	jump_in_place_down
	jump_in_place_down
	step_end

BurnedTower_B1F_Movement_EnteiFoge:
	jump_down
	jump_2_right
	jump_2_right
	jump_2_right
	jump_2_right
	step_end

BurnedTower_B1F_Movement_RaikouFoge:
	jump_down
	jump_2_left
	jump_2_left
	jump_2_left
	jump_2_left
	step_end

BurnedTower_B1F_Movement_SuicuneFoge:
	jump_2_down
	delay_8
	jump_in_place_right_left
	jump_in_place_right_left
	jump_left
	jump_2_down
	jump_2_down
	jump_2_down
	step_end

BurnedTower_B1F_Text_CaesAcordam:
	.string "Three shapes stir in the sealed\n"
	.string "chamber ahead…\p"
	.string "They were sleeping in the ashes\n"
	.string "all this time!$"

BurnedTower_B1F_Text_CaesFogem:
	.string "The three POKéMON scattered in\n"
	.string "every direction and were gone.\p"
	.string "They are loose in JOHTO now.\p"
	.string "Back in ECRUTEAK, the old sage at\n"
	.string "the GYM door will want to hear\l"
	.string "about this.$"
@ <<< Burned Tower <<<

BurnedTower_B1F_EventScript_Raikou::
	lock
	playmoncry SPECIES_RAIKOU, CRY_MODE_NORMAL
	msgbox BurnedTower_B1F_Text_Raikou, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	release
	end

BurnedTower_B1F_EventScript_Entei::
	lock
	playmoncry SPECIES_ENTEI, CRY_MODE_NORMAL
	msgbox BurnedTower_B1F_Text_Entei, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	release
	end

BurnedTower_B1F_EventScript_Suicune::
	lock
	playmoncry SPECIES_SUICUNE, CRY_MODE_NORMAL
	msgbox BurnedTower_B1F_Text_Suicune, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	release
	end

BurnedTower_B1F_Text_Raikou:
	.string "A crackle of static electricity\n"
	.string "runs down your spine…\p"
	.string "Something fast and yellow leaps\n"
	.string "past in a blur. By the time you\l"
	.string "turn, RAIKOU is already gone.$"

BurnedTower_B1F_Text_Entei:
	.string "A wave of heat rolls off the\n"
	.string "scorched pillar…\p"
	.string "You catch a glimpse of ENTEI's\n"
	.string "mane before it vanishes into the\l"
	.string "shadows.$"

BurnedTower_B1F_Text_Suicune:
	.string "A cool mist drifts through the\n"
	.string "basement, though there's no\l"
	.string "water in sight…\p"
	.string "SUICUNE was here. You're sure\n"
	.string "of it.$"

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
BurnedTower_B1F_EventScript_DexRaikou::
	lockall
	msgbox BurnedTower_B1F_Text_DexRaikouIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_RAIKOU, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_RAIKOU, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_RAIKOU
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, BurnedTower_B1F_EventScript_DexRaikouSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, BurnedTower_B1F_EventScript_DexRaikouSome
	releaseall
	end

BurnedTower_B1F_EventScript_DexRaikouSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_RAIKOU
	setflag FLAG_HIDE_DEX_RAIKOU
	fadescreenswapbuffers FADE_FROM_BLACK
	return

BurnedTower_B1F_Text_DexRaikouIntro:
	.string "RAIKOU appeared!$"

BurnedTower_B1F_EventScript_DexEntei::
	lockall
	msgbox BurnedTower_B1F_Text_DexEnteiIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ENTEI, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ENTEI, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ENTEI
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, BurnedTower_B1F_EventScript_DexEnteiSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, BurnedTower_B1F_EventScript_DexEnteiSome
	releaseall
	end

BurnedTower_B1F_EventScript_DexEnteiSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ENTEI
	setflag FLAG_HIDE_DEX_ENTEI
	fadescreenswapbuffers FADE_FROM_BLACK
	return

BurnedTower_B1F_Text_DexEnteiIntro:
	.string "ENTEI appeared!$"

BurnedTower_B1F_EventScript_DexMarshadow::
	lockall
	msgbox BurnedTower_B1F_Text_DexMarshadowIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_MARSHADOW, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_MARSHADOW, 30
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_MARSHADOW
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, BurnedTower_B1F_EventScript_DexMarshadowSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, BurnedTower_B1F_EventScript_DexMarshadowSome
	releaseall
	end

BurnedTower_B1F_EventScript_DexMarshadowSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_MARSHADOW
	setflag FLAG_HIDE_DEX_MARSHADOW
	fadescreenswapbuffers FADE_FROM_BLACK
	return

BurnedTower_B1F_Text_DexMarshadowIntro:
	.string "MARSHADOW appeared!$"

BurnedTower_B1F_EventScript_DexSpectrier::
	lockall
	msgbox BurnedTower_B1F_Text_DexSpectrierIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_SPECTRIER, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_SPECTRIER, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_SPECTRIER
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, BurnedTower_B1F_EventScript_DexSpectrierSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, BurnedTower_B1F_EventScript_DexSpectrierSome
	releaseall
	end

BurnedTower_B1F_EventScript_DexSpectrierSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_SPECTRIER
	setflag FLAG_HIDE_DEX_SPECTRIER
	fadescreenswapbuffers FADE_FROM_BLACK
	return

BurnedTower_B1F_Text_DexSpectrierIntro:
	.string "SPECTRIER appeared!$"

@ <<< Dex completa <<<
