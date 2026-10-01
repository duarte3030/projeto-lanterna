SevenIsland_TanobyRuins_RixyChamber_Frlg_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SevenIsland_TanobyRuins_RixyChamber_OnTransition
	.byte 0

SevenIsland_TanobyRuins_RixyChamber_OnTransition::
	call EventScript_TryDarkenRuins
	end

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
SevenIsland_TanobyRuins_RixyChamber_Frlg_EventScript_DexNecrozma::
	lockall
	msgbox SevenIsland_TanobyRuins_RixyChamber_Frlg_Text_DexNecrozmaIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_NECROZMA, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_NECROZMA, 100
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_NECROZMA
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, SevenIsland_TanobyRuins_RixyChamber_Frlg_EventScript_DexNecrozmaSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, SevenIsland_TanobyRuins_RixyChamber_Frlg_EventScript_DexNecrozmaSome
	releaseall
	end

SevenIsland_TanobyRuins_RixyChamber_Frlg_EventScript_DexNecrozmaSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_NECROZMA
	setflag FLAG_HIDE_DEX_NECROZMA
	fadescreenswapbuffers FADE_FROM_BLACK
	return

SevenIsland_TanobyRuins_RixyChamber_Frlg_Text_DexNecrozmaIntro:
	.string "NECROZMA appeared!$"

@ <<< Dex completa <<<
