MtCoronet6F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MtCoronet6F_OnTransition
	.byte 0

MtCoronet6F_EventScript_GalacticGruntMtCoronet6f::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_MT_CORONET_6F, MtCoronet6F_Text_GalacticGruntMtCoronet6fIntro, MtCoronet6F_Text_GalacticGruntMtCoronet6fDefeat
	msgbox MtCoronet6F_Text_GalacticGruntMtCoronet6fPost, MSGBOX_AUTOCLOSE
	end

MtCoronet6F_Text_GalacticGruntMtCoronet6fIntro:
	.string "You've worked so hard to get here.\nYou should be proud of yourself!\pAnd now, I'll send you packing home\nwith only that happy thought!$"

MtCoronet6F_Text_GalacticGruntMtCoronet6fDefeat:
	.string "Wh-- How dare you! That's how you\nrespond to my generosity?$"

MtCoronet6F_Text_GalacticGruntMtCoronet6fPost:
	.string "We couldn't stop you...\nWe'll be discarded as useless...\pOur boss is ruthless that way...$"

@ ponytail: a cena e a flag sao a mesma coisa. Estes objetos nascem enquanto
@ derrotar o Cyrus no Spear Pillar nao aconteceu, e somem depois; o motor ja grava a flag de
@ derrotado do gatilho, e este ON_TRANSITION so a traduz. Zero var.
MtCoronet6F_OnTransition:
	call_if_defeated TRAINER_SINNOH_GALACTIC_BOSS_CYRUS_SPEAR_PILLAR, MtCoronet6F_EventScript_HideGalactica_mt_coronet
	end

MtCoronet6F_EventScript_HideGalactica_mt_coronet::
	setflag FLAG_GALACTICA_MT_CORONET
	return

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
MtCoronet6F_EventScript_DexMiraidon::
	lockall
	msgbox MtCoronet6F_Text_DexMiraidonIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_MIRAIDON, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_MIRAIDON, 80
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_MIRAIDON
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MtCoronet6F_EventScript_DexMiraidonSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtCoronet6F_EventScript_DexMiraidonSome
	releaseall
	end

MtCoronet6F_EventScript_DexMiraidonSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_MIRAIDON
	setflag FLAG_HIDE_DEX_MIRAIDON
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MtCoronet6F_Text_DexMiraidonIntro:
	.string "MIRAIDON appeared!$"

@ <<< Dex completa <<<
