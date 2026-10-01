SpringPath_MapScripts::
	.byte 0

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
SpringPath_EventScript_DexOgerponWellspringTera::
	lockall
	msgbox SpringPath_Text_DexOgerponWellspringTeraIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_OGERPON_WELLSPRING_TERA, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_OGERPON_WELLSPRING_TERA, 80
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_OGERPON_WELLSPRING_TERA
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, SpringPath_EventScript_DexOgerponWellspringTeraSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, SpringPath_EventScript_DexOgerponWellspringTeraSome
	releaseall
	end

SpringPath_EventScript_DexOgerponWellspringTeraSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_OGERPON_WELLSPRING_TERA
	setflag FLAG_HIDE_DEX_OGERPON_WELLSPRING_TERA
	fadescreenswapbuffers FADE_FROM_BLACK
	return

SpringPath_Text_DexOgerponWellspringTeraIntro:
	.string "OGERPON_WELLSPRING_TERA appeared!$"

@ <<< Dex completa <<<
