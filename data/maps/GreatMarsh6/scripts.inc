GreatMarsh6_MapScripts::
	.byte 0

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
GreatMarsh6_EventScript_DexArceusPoison::
	lockall
	msgbox GreatMarsh6_Text_DexArceusPoisonIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ARCEUS_POISON, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ARCEUS_POISON, 65
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ARCEUS_POISON
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, GreatMarsh6_EventScript_DexArceusPoisonSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GreatMarsh6_EventScript_DexArceusPoisonSome
	releaseall
	end

GreatMarsh6_EventScript_DexArceusPoisonSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ARCEUS_POISON
	setflag FLAG_HIDE_DEX_ARCEUS_POISON
	fadescreenswapbuffers FADE_FROM_BLACK
	return

GreatMarsh6_Text_DexArceusPoisonIntro:
	.string "ARCEUS_POISON appeared!$"

@ <<< Dex completa <<<
