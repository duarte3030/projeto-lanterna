FiveIsland_LostCave_Room14_Frlg_MapScripts::
	.byte 0

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
FiveIsland_LostCave_Room14_Frlg_EventScript_DexPecharunt::
	lockall
	msgbox FiveIsland_LostCave_Room14_Frlg_Text_DexPecharuntIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_PECHARUNT, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_PECHARUNT, 95
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_PECHARUNT
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, FiveIsland_LostCave_Room14_Frlg_EventScript_DexPecharuntSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, FiveIsland_LostCave_Room14_Frlg_EventScript_DexPecharuntSome
	releaseall
	end

FiveIsland_LostCave_Room14_Frlg_EventScript_DexPecharuntSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_PECHARUNT
	setflag FLAG_HIDE_DEX_PECHARUNT
	fadescreenswapbuffers FADE_FROM_BLACK
	return

FiveIsland_LostCave_Room14_Frlg_Text_DexPecharuntIntro:
	.string "PECHARUNT appeared!$"

@ <<< Dex completa <<<
