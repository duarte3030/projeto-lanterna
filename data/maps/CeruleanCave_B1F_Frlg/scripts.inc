CeruleanCave_B1F_Frlg_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, CeruleanCave_B1F_OnResume
	map_script MAP_SCRIPT_ON_TRANSITION, CeruleanCave_B1F_OnTransition
	.byte 0

CeruleanCave_B1F_OnResume::
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, CeruleanCave_B1F_EventScript_TryRemoveMewtwo
	end

CeruleanCave_B1F_EventScript_TryRemoveMewtwo::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
	removeobject VAR_LAST_TALKED
	return

CeruleanCave_B1F_OnTransition::
	call_if_unset FLAG_FOUGHT_MEWTWO, CeruleanCave_B1F_EventScript_ShowMewtwo
	end

CeruleanCave_B1F_EventScript_ShowMewtwo::
	clearflag FLAG_HIDE_MEWTWO
	return

CeruleanCave_B1F_EventScript_Mewtwo::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MEWTWO, CRY_MODE_ENCOUNTER
	message CeruleanCave_B1F_Text_Mew
	waitmessage
	waitmoncry
	delay 20
	playbgm MUS_RG_ENCOUNTER_GYM_LEADER, 0
	waitbuttonpress
	setwildbattle SPECIES_MEWTWO, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, CeruleanCave_B1F_EventScript_DefeatedMewtwo
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, CeruleanCave_B1F_EventScript_RanFromMewtwo
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, CeruleanCave_B1F_EventScript_RanFromMewtwo
	setflag FLAG_FOUGHT_MEWTWO
	release
	end

CeruleanCave_B1F_EventScript_DefeatedMewtwo::
	setflag FLAG_FOUGHT_MEWTWO
	goto EventScript_RemoveStaticMon
	end

CeruleanCave_B1F_EventScript_RanFromMewtwo::
	setvar VAR_0x8004, SPECIES_MEWTWO
	goto EventScript_MonFlewAway
	end

CeruleanCave_B1F_Text_Mew::
	.string "Mew!$"

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
CeruleanCave_B1F_Frlg_EventScript_DexJirachi::
	lockall
	msgbox CeruleanCave_B1F_Frlg_Text_DexJirachiIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_JIRACHI, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_JIRACHI, 30
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_JIRACHI
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, CeruleanCave_B1F_Frlg_EventScript_DexJirachiSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, CeruleanCave_B1F_Frlg_EventScript_DexJirachiSome
	releaseall
	end

CeruleanCave_B1F_Frlg_EventScript_DexJirachiSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_JIRACHI
	setflag FLAG_HIDE_DEX_JIRACHI
	fadescreenswapbuffers FADE_FROM_BLACK
	return

CeruleanCave_B1F_Frlg_Text_DexJirachiIntro:
	.string "JIRACHI appeared!$"

CeruleanCave_B1F_Frlg_EventScript_DexCobalion::
	lockall
	msgbox CeruleanCave_B1F_Frlg_Text_DexCobalionIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_COBALION, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_COBALION, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_COBALION
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, CeruleanCave_B1F_Frlg_EventScript_DexCobalionSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, CeruleanCave_B1F_Frlg_EventScript_DexCobalionSome
	releaseall
	end

CeruleanCave_B1F_Frlg_EventScript_DexCobalionSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_COBALION
	setflag FLAG_HIDE_DEX_COBALION
	fadescreenswapbuffers FADE_FROM_BLACK
	return

CeruleanCave_B1F_Frlg_Text_DexCobalionIntro:
	.string "COBALION appeared!$"

CeruleanCave_B1F_Frlg_EventScript_DexTerrakion::
	lockall
	msgbox CeruleanCave_B1F_Frlg_Text_DexTerrakionIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_TERRAKION, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_TERRAKION, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_TERRAKION
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, CeruleanCave_B1F_Frlg_EventScript_DexTerrakionSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, CeruleanCave_B1F_Frlg_EventScript_DexTerrakionSome
	releaseall
	end

CeruleanCave_B1F_Frlg_EventScript_DexTerrakionSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_TERRAKION
	setflag FLAG_HIDE_DEX_TERRAKION
	fadescreenswapbuffers FADE_FROM_BLACK
	return

CeruleanCave_B1F_Frlg_Text_DexTerrakionIntro:
	.string "TERRAKION appeared!$"

@ <<< Dex completa <<<
