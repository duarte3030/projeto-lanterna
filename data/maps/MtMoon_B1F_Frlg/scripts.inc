MtMoon_B1F_Frlg_MapScripts::
	.byte 0

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
MtMoon_B1F_Frlg_EventScript_DexArceusFairy::
	lockall
	msgbox MtMoon_B1F_Frlg_Text_DexArceusFairyIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ARCEUS_FAIRY, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ARCEUS_FAIRY, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ARCEUS_FAIRY
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MtMoon_B1F_Frlg_EventScript_DexArceusFairySome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtMoon_B1F_Frlg_EventScript_DexArceusFairySome
	releaseall
	end

MtMoon_B1F_Frlg_EventScript_DexArceusFairySome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ARCEUS_FAIRY
	setflag FLAG_HIDE_DEX_ARCEUS_FAIRY
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MtMoon_B1F_Frlg_Text_DexArceusFairyIntro:
	.string "ARCEUS_FAIRY appeared!$"

@ <<< Dex completa <<<
