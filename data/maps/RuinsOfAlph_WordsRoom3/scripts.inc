RuinsOfAlph_WordsRoom3_MapScripts::
	.byte 0

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
RuinsOfAlph_WordsRoom3_EventScript_DexCalyrexShadow::
	lockall
	msgbox RuinsOfAlph_WordsRoom3_Text_DexCalyrexShadowIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_CALYREX_SHADOW, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_CALYREX_SHADOW, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_CALYREX_SHADOW
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, RuinsOfAlph_WordsRoom3_EventScript_DexCalyrexShadowSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, RuinsOfAlph_WordsRoom3_EventScript_DexCalyrexShadowSome
	releaseall
	end

RuinsOfAlph_WordsRoom3_EventScript_DexCalyrexShadowSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_CALYREX_SHADOW
	setflag FLAG_HIDE_DEX_CALYREX_SHADOW
	fadescreenswapbuffers FADE_FROM_BLACK
	return

RuinsOfAlph_WordsRoom3_Text_DexCalyrexShadowIntro:
	.string "CALYREX_SHADOW appeared!$"

@ <<< Dex completa <<<
