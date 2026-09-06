@ Gerado por dev_scripts/mundo_galar.py (G2). Sem cena: o ponteiro de
@ map script da fonte (nenhum) esta anotado no censo para a fase de conteudo.

Galar_CrownTundra10_MapScripts::
	.byte 0

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
Galar_CrownTundra10_EventScript_DexGalarRegieleki::
	lockall
	msgbox Galar_CrownTundra10_Text_DexGalarRegielekiIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_REGIELEKI, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_REGIELEKI, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_GALAR_REGIELEKI
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Galar_CrownTundra10_EventScript_DexGalarRegielekiSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Galar_CrownTundra10_EventScript_DexGalarRegielekiSome
	releaseall
	end

Galar_CrownTundra10_EventScript_DexGalarRegielekiSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GALAR_REGIELEKI
	setflag FLAG_HIDE_DEX_GALAR_REGIELEKI
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Galar_CrownTundra10_Text_DexGalarRegielekiIntro:
	.string "REGIELEKI appeared!$"

Galar_CrownTundra10_EventScript_DexGalarRegidrago::
	lockall
	msgbox Galar_CrownTundra10_Text_DexGalarRegidragoIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_REGIDRAGO, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_REGIDRAGO, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_GALAR_REGIDRAGO
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Galar_CrownTundra10_EventScript_DexGalarRegidragoSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Galar_CrownTundra10_EventScript_DexGalarRegidragoSome
	releaseall
	end

Galar_CrownTundra10_EventScript_DexGalarRegidragoSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GALAR_REGIDRAGO
	setflag FLAG_HIDE_DEX_GALAR_REGIDRAGO
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Galar_CrownTundra10_Text_DexGalarRegidragoIntro:
	.string "REGIDRAGO appeared!$"

Galar_CrownTundra10_EventScript_DexGalarCalyrexIce::
	lockall
	msgbox Galar_CrownTundra10_Text_DexGalarCalyrexIceIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_CALYREX_ICE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_CALYREX_ICE, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_GALAR_CALYREX_ICE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Galar_CrownTundra10_EventScript_DexGalarCalyrexIceSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Galar_CrownTundra10_EventScript_DexGalarCalyrexIceSome
	releaseall
	end

Galar_CrownTundra10_EventScript_DexGalarCalyrexIceSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GALAR_CALYREX_ICE
	setflag FLAG_HIDE_DEX_GALAR_CALYREX_ICE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Galar_CrownTundra10_Text_DexGalarCalyrexIceIntro:
	.string "CALYREX_ICE appeared!$"

Galar_CrownTundra10_EventScript_DexGalarCalyrexShadow::
	lockall
	msgbox Galar_CrownTundra10_Text_DexGalarCalyrexShadowIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_CALYREX_SHADOW, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_CALYREX_SHADOW, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_GALAR_CALYREX_SHADOW
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Galar_CrownTundra10_EventScript_DexGalarCalyrexShadowSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Galar_CrownTundra10_EventScript_DexGalarCalyrexShadowSome
	releaseall
	end

Galar_CrownTundra10_EventScript_DexGalarCalyrexShadowSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GALAR_CALYREX_SHADOW
	setflag FLAG_HIDE_DEX_GALAR_CALYREX_SHADOW
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Galar_CrownTundra10_Text_DexGalarCalyrexShadowIntro:
	.string "CALYREX_SHADOW appeared!$"

Galar_CrownTundra10_EventScript_DexGalarEnamorusIncarnate::
	lockall
	msgbox Galar_CrownTundra10_Text_DexGalarEnamorusIncarnateIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ENAMORUS_INCARNATE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ENAMORUS_INCARNATE, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_GALAR_ENAMORUS_INCARNATE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Galar_CrownTundra10_EventScript_DexGalarEnamorusIncarnateSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Galar_CrownTundra10_EventScript_DexGalarEnamorusIncarnateSome
	releaseall
	end

Galar_CrownTundra10_EventScript_DexGalarEnamorusIncarnateSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GALAR_ENAMORUS_INCARNATE
	setflag FLAG_HIDE_DEX_GALAR_ENAMORUS_INCARNATE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Galar_CrownTundra10_Text_DexGalarEnamorusIncarnateIntro:
	.string "ENAMORUS_INCARNATE appeared!$"

@ <<< Dex completa <<<
