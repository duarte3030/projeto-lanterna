@ Gerado por dev_scripts/mundo_galar.py (G2). Sem cena: o ponteiro de
@ map script da fonte (0x07528F4) esta anotado no censo para a fase de conteudo.

Galar_RoseTower01_MapScripts::
	.byte 0

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
Galar_RoseTower01_EventScript_DexGalarEternatus::
	lockall
	msgbox Galar_RoseTower01_Text_DexGalarEternatusIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ETERNATUS, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ETERNATUS, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_GALAR_ETERNATUS
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Galar_RoseTower01_EventScript_DexGalarEternatusSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Galar_RoseTower01_EventScript_DexGalarEternatusSome
	releaseall
	end

Galar_RoseTower01_EventScript_DexGalarEternatusSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GALAR_ETERNATUS
	setflag FLAG_HIDE_DEX_GALAR_ETERNATUS
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Galar_RoseTower01_Text_DexGalarEternatusIntro:
	.string "ETERNATUS appeared!$"

@ <<< Dex completa <<<
