MtEmber_RubyPath_B5F_Frlg_MapScripts::
	.byte 0

MtEmber_RubyPath_B5F_EventScript_BrailleMessage::
	lockall
	setvar VAR_0x8005, 130
	braillemessage_wait Braille_Text_Everything
	braillemessage_wait Braille_Text_HasMeaning1
	braillemessage_wait Braille_Text_Existence
	braillemessage_wait Braille_Text_HasMeaning2
	braillemessage_wait Braille_Text_BeingAlive
	braillemessage_wait Braille_Text_HasMeaning3
	braillemessage_wait Braille_Text_HaveDreams
	braillemsgbox Braille_Text_UsePower
	releaseall
	end

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
MtEmber_RubyPath_B5F_Frlg_EventScript_DexKoraidon::
	lockall
	msgbox MtEmber_RubyPath_B5F_Frlg_Text_DexKoraidonIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_KORAIDON, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_KORAIDON, 85
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_KORAIDON
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MtEmber_RubyPath_B5F_Frlg_EventScript_DexKoraidonSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtEmber_RubyPath_B5F_Frlg_EventScript_DexKoraidonSome
	releaseall
	end

MtEmber_RubyPath_B5F_Frlg_EventScript_DexKoraidonSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_KORAIDON
	setflag FLAG_HIDE_DEX_KORAIDON
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MtEmber_RubyPath_B5F_Frlg_Text_DexKoraidonIntro:
	.string "KORAIDON appeared!$"

@ <<< Dex completa <<<
