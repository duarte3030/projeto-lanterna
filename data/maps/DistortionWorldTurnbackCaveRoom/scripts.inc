DistortionWorldTurnbackCaveRoom_MapScripts::
	.byte 0

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
DistortionWorldTurnbackCaveRoom_EventScript_DexPoipole::
	lockall
	msgbox DistortionWorldTurnbackCaveRoom_Text_DexPoipoleIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_POIPOLE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_POIPOLE, 100
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_POIPOLE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, DistortionWorldTurnbackCaveRoom_EventScript_DexPoipoleSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, DistortionWorldTurnbackCaveRoom_EventScript_DexPoipoleSome
	releaseall
	end

DistortionWorldTurnbackCaveRoom_EventScript_DexPoipoleSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_POIPOLE
	setflag FLAG_HIDE_DEX_POIPOLE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

DistortionWorldTurnbackCaveRoom_Text_DexPoipoleIntro:
	.string "POIPOLE appeared!$"

@ <<< Dex completa <<<
