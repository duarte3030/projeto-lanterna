AcuityCavern_MapScripts::
	.byte 0

@ >>> Lendarios de Sinnoh (dev_scripts/lendarios_sinnoh.py) >>>
AcuityCavern_EventScript_Uxie::
	lockall
	msgbox AcuityCavern_Text_UxieIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_UXIE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_UXIE, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_ACUITY_CAVERN_UXIE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, AcuityCavern_EventScript_UxieSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, AcuityCavern_EventScript_UxiePreso
	releaseall
	end

@ ponytail: so apaga o bicho em VITORIA ou CAPTURA. Fugir, perder ou
@ ser teleportado deixa ele no mapa, senao uma bola errada tira o
@ lendario do save. Mesma regra do LUGIA e do SpearPillar_Dialga.
AcuityCavern_EventScript_UxiePreso::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_ACUITY_CAVERN_UXIE
	setflag FLAG_HIDE_UXIE_SINNOH
	fadescreenswapbuffers FADE_FROM_BLACK
	return

AcuityCavern_EventScript_UxieSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_ACUITY_CAVERN_UXIE
	setflag FLAG_HIDE_UXIE_SINNOH
	fadescreenswapbuffers FADE_FROM_BLACK
	msgbox AcuityCavern_Text_UxieSome, MSGBOX_DEFAULT
	return

AcuityCavern_Text_UxieIntro:
	.string "Kyouuuun!$"

AcuityCavern_Text_UxieSome:
	.string "UXIE disappeared deep into its\ncavern...$"

@ <<< Lendarios de Sinnoh <<<
