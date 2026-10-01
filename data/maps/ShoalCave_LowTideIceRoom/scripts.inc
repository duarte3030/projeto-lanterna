ShoalCave_LowTideIceRoom_MapScripts::
	.byte 0

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
ShoalCave_LowTideIceRoom_EventScript_DexGlastrier::
	lockall
	msgbox ShoalCave_LowTideIceRoom_Text_DexGlastrierIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_GLASTRIER, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_GLASTRIER, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_GLASTRIER
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, ShoalCave_LowTideIceRoom_EventScript_DexGlastrierSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, ShoalCave_LowTideIceRoom_EventScript_DexGlastrierSome
	releaseall
	end

ShoalCave_LowTideIceRoom_EventScript_DexGlastrierSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GLASTRIER
	setflag FLAG_HIDE_DEX_GLASTRIER
	fadescreenswapbuffers FADE_FROM_BLACK
	return

ShoalCave_LowTideIceRoom_Text_DexGlastrierIntro:
	.string "GLASTRIER appeared!$"

@ <<< Dex completa <<<
