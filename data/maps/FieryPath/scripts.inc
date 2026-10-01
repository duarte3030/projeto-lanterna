FieryPath_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, FieryPath_OnTransition
	.byte 0

FieryPath_OnTransition:
	call_if_unset FLAG_LANDMARK_FIERY_PATH, FieryPath_EventScript_MoveScottToFallarbor
	setflag FLAG_LANDMARK_FIERY_PATH
	end

FieryPath_EventScript_MoveScottToFallarbor::
	setflag FLAG_HIDE_VERDANTURF_TOWN_SCOTT
	clearflag FLAG_HIDE_FALLARBOR_TOWN_BATTLE_TENT_SCOTT
	return

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
FieryPath_EventScript_DexOgerponHearthflame::
	lockall
	msgbox FieryPath_Text_DexOgerponHearthflameIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_OGERPON_HEARTHFLAME, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_OGERPON_HEARTHFLAME, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_OGERPON_HEARTHFLAME
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, FieryPath_EventScript_DexOgerponHearthflameSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, FieryPath_EventScript_DexOgerponHearthflameSome
	releaseall
	end

FieryPath_EventScript_DexOgerponHearthflameSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_OGERPON_HEARTHFLAME
	setflag FLAG_HIDE_DEX_OGERPON_HEARTHFLAME
	fadescreenswapbuffers FADE_FROM_BLACK
	return

FieryPath_Text_DexOgerponHearthflameIntro:
	.string "OGERPON_HEARTHFLAME appeared!$"

@ <<< Dex completa <<<
