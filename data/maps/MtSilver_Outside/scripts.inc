MtSilver_Outside_MapScripts::
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

MtSilver_Outside_EventScript_Sign::
	msgbox MtSilver_Outside_Text_Sign, MSGBOX_SIGN
	end

MtSilver_Outside_Text_Sign::
	.string "MT. SILVER$"

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
MtSilver_Outside_EventScript_DexCosmog::
	lockall
	msgbox MtSilver_Outside_Text_DexCosmogIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_COSMOG, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_COSMOG, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_COSMOG
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MtSilver_Outside_EventScript_DexCosmogSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtSilver_Outside_EventScript_DexCosmogSome
	releaseall
	end

MtSilver_Outside_EventScript_DexCosmogSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_COSMOG
	setflag FLAG_HIDE_DEX_COSMOG
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MtSilver_Outside_Text_DexCosmogIntro:
	.string "COSMOG appeared!$"

MtSilver_Outside_EventScript_DexSolgaleo::
	lockall
	msgbox MtSilver_Outside_Text_DexSolgaleoIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_SOLGALEO, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_SOLGALEO, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_SOLGALEO
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MtSilver_Outside_EventScript_DexSolgaleoSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtSilver_Outside_EventScript_DexSolgaleoSome
	releaseall
	end

MtSilver_Outside_EventScript_DexSolgaleoSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_SOLGALEO
	setflag FLAG_HIDE_DEX_SOLGALEO
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MtSilver_Outside_Text_DexSolgaleoIntro:
	.string "SOLGALEO appeared!$"

MtSilver_Outside_EventScript_DexLunala::
	lockall
	msgbox MtSilver_Outside_Text_DexLunalaIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_LUNALA, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_LUNALA, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_LUNALA
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MtSilver_Outside_EventScript_DexLunalaSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtSilver_Outside_EventScript_DexLunalaSome
	releaseall
	end

MtSilver_Outside_EventScript_DexLunalaSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_LUNALA
	setflag FLAG_HIDE_DEX_LUNALA
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MtSilver_Outside_Text_DexLunalaIntro:
	.string "LUNALA appeared!$"

@ <<< Dex completa <<<
