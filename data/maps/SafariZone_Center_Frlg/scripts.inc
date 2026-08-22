SafariZone_Center_Frlg_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SafariZone_Center_OnTransition
	.byte 0

SafariZone_Center_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_SAFARI_ZONE_CENTER
	end

SafariZone_Center_EventScript_RestHouseSign::
	msgbox SafariZone_Center_Text_RestHouse, MSGBOX_SIGN
	end

SafariZone_Center_EventScript_TrainerTips::
	msgbox SafariZone_Center_Text_PressStartToCheckTime, MSGBOX_SIGN
	end

SafariZone_Center_EventScript_AreaSign::
	msgbox SafariZone_Center_Text_CenterArea, MSGBOX_SIGN
	end

SafariZone_Center_Text_RestHouse::
	.string "REST HOUSE$"

SafariZone_Center_Text_PressStartToCheckTime::
	.string "TRAINER TIPS\p"
	.string "Press START to check\n"
	.string "remaining time.$"

SafariZone_Center_Text_CenterArea::
	.string "CENTER AREA$"

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
SafariZone_Center_Frlg_EventScript_DexMeltan::
	lockall
	msgbox SafariZone_Center_Frlg_Text_DexMeltanIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_MELTAN, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_MELTAN, 30
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_MELTAN
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, SafariZone_Center_Frlg_EventScript_DexMeltanSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, SafariZone_Center_Frlg_EventScript_DexMeltanSome
	releaseall
	end

SafariZone_Center_Frlg_EventScript_DexMeltanSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_MELTAN
	setflag FLAG_HIDE_DEX_MELTAN
	fadescreenswapbuffers FADE_FROM_BLACK
	return

SafariZone_Center_Frlg_Text_DexMeltanIntro:
	.string "MELTAN appeared!$"

SafariZone_Center_Frlg_EventScript_DexMelmetal::
	lockall
	msgbox SafariZone_Center_Frlg_Text_DexMelmetalIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_MELMETAL, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_MELMETAL, 30
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_MELMETAL
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, SafariZone_Center_Frlg_EventScript_DexMelmetalSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, SafariZone_Center_Frlg_EventScript_DexMelmetalSome
	releaseall
	end

SafariZone_Center_Frlg_EventScript_DexMelmetalSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_MELMETAL
	setflag FLAG_HIDE_DEX_MELMETAL
	fadescreenswapbuffers FADE_FROM_BLACK
	return

SafariZone_Center_Frlg_Text_DexMelmetalIntro:
	.string "MELMETAL appeared!$"

@ <<< Dex completa <<<
