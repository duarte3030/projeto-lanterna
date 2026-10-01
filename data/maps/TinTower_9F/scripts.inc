TinTower_9F_MapScripts::
	.byte 0

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
TinTower_9F_EventScript_DexArceusFlying::
	lockall
	msgbox TinTower_9F_Text_DexArceusFlyingIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ARCEUS_FLYING, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ARCEUS_FLYING, 75
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ARCEUS_FLYING
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, TinTower_9F_EventScript_DexArceusFlyingSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, TinTower_9F_EventScript_DexArceusFlyingSome
	releaseall
	end

TinTower_9F_EventScript_DexArceusFlyingSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ARCEUS_FLYING
	setflag FLAG_HIDE_DEX_ARCEUS_FLYING
	fadescreenswapbuffers FADE_FROM_BLACK
	return

TinTower_9F_Text_DexArceusFlyingIntro:
	.string "ARCEUS_FLYING appeared!$"

@ <<< Dex completa <<<
