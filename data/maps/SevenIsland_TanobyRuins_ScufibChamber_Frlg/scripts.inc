SevenIsland_TanobyRuins_ScufibChamber_Frlg_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SevenIsland_TanobyRuins_ScufibChamber_OnTransition
	.byte 0

SevenIsland_TanobyRuins_ScufibChamber_OnTransition::
	call EventScript_TryDarkenRuins
	end

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
SevenIsland_TanobyRuins_ScufibChamber_Frlg_EventScript_DexChiYu::
	lockall
	msgbox SevenIsland_TanobyRuins_ScufibChamber_Frlg_Text_DexChiYuIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_CHI_YU, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_CHI_YU, 100
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_CHI_YU
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, SevenIsland_TanobyRuins_ScufibChamber_Frlg_EventScript_DexChiYuSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, SevenIsland_TanobyRuins_ScufibChamber_Frlg_EventScript_DexChiYuSome
	releaseall
	end

SevenIsland_TanobyRuins_ScufibChamber_Frlg_EventScript_DexChiYuSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_CHI_YU
	setflag FLAG_HIDE_DEX_CHI_YU
	fadescreenswapbuffers FADE_FROM_BLACK
	return

SevenIsland_TanobyRuins_ScufibChamber_Frlg_Text_DexChiYuIntro:
	.string "CHI_YU appeared!$"

@ <<< Dex completa <<<
