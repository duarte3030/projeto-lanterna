RuinsOfAlph_WordsRoom1_MapScripts::
	.byte 0

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
RuinsOfAlph_WordsRoom1_EventScript_DexCalyrex::
	lockall
	msgbox RuinsOfAlph_WordsRoom1_Text_DexCalyrexIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_CALYREX, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_CALYREX, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_CALYREX
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, RuinsOfAlph_WordsRoom1_EventScript_DexCalyrexSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, RuinsOfAlph_WordsRoom1_EventScript_DexCalyrexSome
	releaseall
	end

RuinsOfAlph_WordsRoom1_EventScript_DexCalyrexSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_CALYREX
	setflag FLAG_HIDE_DEX_CALYREX
	fadescreenswapbuffers FADE_FROM_BLACK
	return

RuinsOfAlph_WordsRoom1_Text_DexCalyrexIntro:
	.string "CALYREX appeared!$"

@ <<< Dex completa <<<
