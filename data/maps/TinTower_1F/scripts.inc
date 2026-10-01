TinTower_1F_MapScripts::
	.byte 0

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
TinTower_1F_EventScript_DexSuicune::
	lockall
	msgbox TinTower_1F_Text_DexSuicuneIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_SUICUNE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_SUICUNE, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_SUICUNE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, TinTower_1F_EventScript_DexSuicuneSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, TinTower_1F_EventScript_DexSuicuneSome
	releaseall
	end

TinTower_1F_EventScript_DexSuicuneSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_SUICUNE
	setflag FLAG_HIDE_DEX_SUICUNE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

TinTower_1F_Text_DexSuicuneIntro:
	.string "SUICUNE appeared!$"

@ <<< Dex completa <<<
