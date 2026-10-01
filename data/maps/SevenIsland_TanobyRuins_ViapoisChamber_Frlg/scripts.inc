SevenIsland_TanobyRuins_ViapoisChamber_Frlg_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SevenIsland_TanobyRuins_ViapoisChamber_OnTransition
	.byte 0

SevenIsland_TanobyRuins_ViapoisChamber_OnTransition::
	call EventScript_TryDarkenRuins
	end

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
SevenIsland_TanobyRuins_ViapoisChamber_Frlg_EventScript_DexCosmoem::
	lockall
	msgbox SevenIsland_TanobyRuins_ViapoisChamber_Frlg_Text_DexCosmoemIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_COSMOEM, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_COSMOEM, 100
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_COSMOEM
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, SevenIsland_TanobyRuins_ViapoisChamber_Frlg_EventScript_DexCosmoemSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, SevenIsland_TanobyRuins_ViapoisChamber_Frlg_EventScript_DexCosmoemSome
	releaseall
	end

SevenIsland_TanobyRuins_ViapoisChamber_Frlg_EventScript_DexCosmoemSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_COSMOEM
	setflag FLAG_HIDE_DEX_COSMOEM
	fadescreenswapbuffers FADE_FROM_BLACK
	return

SevenIsland_TanobyRuins_ViapoisChamber_Frlg_Text_DexCosmoemIntro:
	.string "COSMOEM appeared!$"

@ <<< Dex completa <<<
