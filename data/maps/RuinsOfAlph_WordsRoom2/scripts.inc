RuinsOfAlph_WordsRoom2_MapScripts::
	.byte 0

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
RuinsOfAlph_WordsRoom2_EventScript_DexCalyrexIce::
	lockall
	msgbox RuinsOfAlph_WordsRoom2_Text_DexCalyrexIceIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_CALYREX_ICE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_CALYREX_ICE, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_CALYREX_ICE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, RuinsOfAlph_WordsRoom2_EventScript_DexCalyrexIceSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, RuinsOfAlph_WordsRoom2_EventScript_DexCalyrexIceSome
	releaseall
	end

RuinsOfAlph_WordsRoom2_EventScript_DexCalyrexIceSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_CALYREX_ICE
	setflag FLAG_HIDE_DEX_CALYREX_ICE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

RuinsOfAlph_WordsRoom2_Text_DexCalyrexIceIntro:
	.string "CALYREX_ICE appeared!$"

@ <<< Dex completa <<<
