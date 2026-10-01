SevenIsland_TanobyRuins_LiptooChamber_Frlg_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SevenIsland_TanobyRuins_LiptooChamber_OnTransition
	.byte 0

SevenIsland_TanobyRuins_LiptooChamber_OnTransition::
	call EventScript_TryDarkenRuins
	end

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
SevenIsland_TanobyRuins_LiptooChamber_Frlg_EventScript_DexChienPao::
	lockall
	msgbox SevenIsland_TanobyRuins_LiptooChamber_Frlg_Text_DexChienPaoIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_CHIEN_PAO, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_CHIEN_PAO, 100
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_CHIEN_PAO
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, SevenIsland_TanobyRuins_LiptooChamber_Frlg_EventScript_DexChienPaoSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, SevenIsland_TanobyRuins_LiptooChamber_Frlg_EventScript_DexChienPaoSome
	releaseall
	end

SevenIsland_TanobyRuins_LiptooChamber_Frlg_EventScript_DexChienPaoSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_CHIEN_PAO
	setflag FLAG_HIDE_DEX_CHIEN_PAO
	fadescreenswapbuffers FADE_FROM_BLACK
	return

SevenIsland_TanobyRuins_LiptooChamber_Frlg_Text_DexChienPaoIntro:
	.string "CHIEN_PAO appeared!$"

@ <<< Dex completa <<<
