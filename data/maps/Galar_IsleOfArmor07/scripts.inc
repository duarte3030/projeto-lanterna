@ Gerado por dev_scripts/mundo_galar.py (G2). Sem cena: o ponteiro de
@ map script da fonte (nenhum) esta anotado no censo para a fase de conteudo.

Galar_IsleOfArmor07_MapScripts::
	.byte 0

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
Galar_IsleOfArmor07_EventScript_DexGalarZarude::
	lockall
	msgbox Galar_IsleOfArmor07_Text_DexGalarZarudeIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ZARUDE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ZARUDE, 30
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_GALAR_ZARUDE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Galar_IsleOfArmor07_EventScript_DexGalarZarudeSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Galar_IsleOfArmor07_EventScript_DexGalarZarudeSome
	releaseall
	end

Galar_IsleOfArmor07_EventScript_DexGalarZarudeSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GALAR_ZARUDE
	setflag FLAG_HIDE_DEX_GALAR_ZARUDE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Galar_IsleOfArmor07_Text_DexGalarZarudeIntro:
	.string "ZARUDE appeared!$"

@ <<< Dex completa <<<
