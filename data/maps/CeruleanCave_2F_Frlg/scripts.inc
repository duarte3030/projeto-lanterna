CeruleanCave_2F_Frlg_MapScripts::
	.byte 0

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
CeruleanCave_2F_Frlg_EventScript_DexVirizion::
	lockall
	msgbox CeruleanCave_2F_Frlg_Text_DexVirizionIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_VIRIZION, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_VIRIZION, 85
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_VIRIZION
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, CeruleanCave_2F_Frlg_EventScript_DexVirizionSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, CeruleanCave_2F_Frlg_EventScript_DexVirizionSome
	releaseall
	end

CeruleanCave_2F_Frlg_EventScript_DexVirizionSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_VIRIZION
	setflag FLAG_HIDE_DEX_VIRIZION
	fadescreenswapbuffers FADE_FROM_BLACK
	return

CeruleanCave_2F_Frlg_Text_DexVirizionIntro:
	.string "VIRIZION appeared!$"

@ <<< Dex completa <<<
