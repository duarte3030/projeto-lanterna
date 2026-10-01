SevenIsland_TanobyRuins_DilfordChamber_Frlg_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SevenIsland_TanobyRuins_DilfordChamber_OnTransition
	.byte 0

SevenIsland_TanobyRuins_DilfordChamber_OnTransition::
	call EventScript_TryDarkenRuins
	end

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
SevenIsland_TanobyRuins_DilfordChamber_Frlg_EventScript_DexWoChien::
	lockall
	msgbox SevenIsland_TanobyRuins_DilfordChamber_Frlg_Text_DexWoChienIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_WO_CHIEN, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_WO_CHIEN, 100
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_WO_CHIEN
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, SevenIsland_TanobyRuins_DilfordChamber_Frlg_EventScript_DexWoChienSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, SevenIsland_TanobyRuins_DilfordChamber_Frlg_EventScript_DexWoChienSome
	releaseall
	end

SevenIsland_TanobyRuins_DilfordChamber_Frlg_EventScript_DexWoChienSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_WO_CHIEN
	setflag FLAG_HIDE_DEX_WO_CHIEN
	fadescreenswapbuffers FADE_FROM_BLACK
	return

SevenIsland_TanobyRuins_DilfordChamber_Frlg_Text_DexWoChienIntro:
	.string "WO_CHIEN appeared!$"

@ <<< Dex completa <<<
