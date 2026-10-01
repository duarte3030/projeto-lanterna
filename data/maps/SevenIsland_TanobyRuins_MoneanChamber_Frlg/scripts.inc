SevenIsland_TanobyRuins_MoneanChamber_Frlg_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SevenIsland_TanobyRuins_MoneanChamber_OnTransition
	.byte 0

SevenIsland_TanobyRuins_MoneanChamber_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_SEVEN_ISLAND_TANOBY_RUINS_MONEAN_CHAMBER
	call EventScript_TryDarkenRuins
	end

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
SevenIsland_TanobyRuins_MoneanChamber_Frlg_EventScript_DexTingLu::
	lockall
	msgbox SevenIsland_TanobyRuins_MoneanChamber_Frlg_Text_DexTingLuIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_TING_LU, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_TING_LU, 100
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_TING_LU
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, SevenIsland_TanobyRuins_MoneanChamber_Frlg_EventScript_DexTingLuSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, SevenIsland_TanobyRuins_MoneanChamber_Frlg_EventScript_DexTingLuSome
	releaseall
	end

SevenIsland_TanobyRuins_MoneanChamber_Frlg_EventScript_DexTingLuSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_TING_LU
	setflag FLAG_HIDE_DEX_TING_LU
	fadescreenswapbuffers FADE_FROM_BLACK
	return

SevenIsland_TanobyRuins_MoneanChamber_Frlg_Text_DexTingLuIntro:
	.string "TING_LU appeared!$"

@ <<< Dex completa <<<
