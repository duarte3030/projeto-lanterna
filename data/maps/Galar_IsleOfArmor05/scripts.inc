@ Gerado por dev_scripts/mundo_galar.py (G2). Sem cena: o ponteiro de
@ map script da fonte (0x071D26C) esta anotado no censo para a fase de conteudo.

Galar_IsleOfArmor05_MapScripts::
	.byte 0

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
Galar_IsleOfArmor05_EventScript_DexGalarKubfu::
	lockall
	msgbox Galar_IsleOfArmor05_Text_DexGalarKubfuIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_KUBFU, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_KUBFU, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_GALAR_KUBFU
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Galar_IsleOfArmor05_EventScript_DexGalarKubfuSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Galar_IsleOfArmor05_EventScript_DexGalarKubfuSome
	releaseall
	end

Galar_IsleOfArmor05_EventScript_DexGalarKubfuSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GALAR_KUBFU
	setflag FLAG_HIDE_DEX_GALAR_KUBFU
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Galar_IsleOfArmor05_Text_DexGalarKubfuIntro:
	.string "KUBFU appeared!$"

@ <<< Dex completa <<<
