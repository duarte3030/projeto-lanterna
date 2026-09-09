IcePath_1F_MapScripts::
	.byte 0

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
IcePath_1F_EventScript_DexArceusIce::
	lockall
	msgbox IcePath_1F_Text_DexArceusIceIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ARCEUS_ICE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ARCEUS_ICE, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ARCEUS_ICE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, IcePath_1F_EventScript_DexArceusIceSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, IcePath_1F_EventScript_DexArceusIceSome
	releaseall
	end

IcePath_1F_EventScript_DexArceusIceSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ARCEUS_ICE
	setflag FLAG_HIDE_DEX_ARCEUS_ICE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

IcePath_1F_Text_DexArceusIceIntro:
	.string "ARCEUS_ICE appeared!$"

IcePath_1F_EventScript_DexArceusSteel::
	lockall
	msgbox IcePath_1F_Text_DexArceusSteelIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ARCEUS_STEEL, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ARCEUS_STEEL, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ARCEUS_STEEL
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, IcePath_1F_EventScript_DexArceusSteelSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, IcePath_1F_EventScript_DexArceusSteelSome
	releaseall
	end

IcePath_1F_EventScript_DexArceusSteelSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ARCEUS_STEEL
	setflag FLAG_HIDE_DEX_ARCEUS_STEEL
	fadescreenswapbuffers FADE_FROM_BLACK
	return

IcePath_1F_Text_DexArceusSteelIntro:
	.string "ARCEUS_STEEL appeared!$"

@ <<< Dex completa <<<
