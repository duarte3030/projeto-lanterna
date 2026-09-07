CeruleanCave_1F_Frlg_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, CeruleanCave_1F_OnTransition
	.byte 0

CeruleanCave_1F_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_CERULEAN_CAVE_1F
	end

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
CeruleanCave_1F_Frlg_EventScript_DexCelesteela::
	lockall
	msgbox CeruleanCave_1F_Frlg_Text_DexCelesteelaIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_CELESTEELA, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_CELESTEELA, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_CELESTEELA
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, CeruleanCave_1F_Frlg_EventScript_DexCelesteelaSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, CeruleanCave_1F_Frlg_EventScript_DexCelesteelaSome
	releaseall
	end

CeruleanCave_1F_Frlg_EventScript_DexCelesteelaSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_CELESTEELA
	setflag FLAG_HIDE_DEX_CELESTEELA
	fadescreenswapbuffers FADE_FROM_BLACK
	return

CeruleanCave_1F_Frlg_Text_DexCelesteelaIntro:
	.string "CELESTEELA appeared!$"

CeruleanCave_1F_Frlg_EventScript_DexMagearnaOriginal::
	lockall
	msgbox CeruleanCave_1F_Frlg_Text_DexMagearnaOriginalIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_MAGEARNA_ORIGINAL, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_MAGEARNA_ORIGINAL, 30
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_MAGEARNA_ORIGINAL
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, CeruleanCave_1F_Frlg_EventScript_DexMagearnaOriginalSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, CeruleanCave_1F_Frlg_EventScript_DexMagearnaOriginalSome
	releaseall
	end

CeruleanCave_1F_Frlg_EventScript_DexMagearnaOriginalSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_MAGEARNA_ORIGINAL
	setflag FLAG_HIDE_DEX_MAGEARNA_ORIGINAL
	fadescreenswapbuffers FADE_FROM_BLACK
	return

CeruleanCave_1F_Frlg_Text_DexMagearnaOriginalIntro:
	.string "MAGEARNA_ORIGINAL appeared!$"

CeruleanCave_1F_Frlg_EventScript_DexStakataka::
	lockall
	msgbox CeruleanCave_1F_Frlg_Text_DexStakatakaIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_STAKATAKA, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_STAKATAKA, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_STAKATAKA
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, CeruleanCave_1F_Frlg_EventScript_DexStakatakaSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, CeruleanCave_1F_Frlg_EventScript_DexStakatakaSome
	releaseall
	end

CeruleanCave_1F_Frlg_EventScript_DexStakatakaSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_STAKATAKA
	setflag FLAG_HIDE_DEX_STAKATAKA
	fadescreenswapbuffers FADE_FROM_BLACK
	return

CeruleanCave_1F_Frlg_Text_DexStakatakaIntro:
	.string "STAKATAKA appeared!$"

@ <<< Dex completa <<<
