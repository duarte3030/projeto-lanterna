VerityCavern_MapScripts::
	.byte 0

@ >>> Lendarios de Sinnoh (dev_scripts/lendarios_sinnoh.py) >>>
VerityCavern_EventScript_Mesprit::
	lockall
	msgbox VerityCavern_Text_MespritIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_MESPRIT, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_MESPRIT, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_VERITY_CAVERN_MESPRIT
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, VerityCavern_EventScript_MespritSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, VerityCavern_EventScript_MespritPreso
	releaseall
	end

@ ponytail: so apaga o bicho em VITORIA ou CAPTURA. Fugir, perder ou
@ ser teleportado deixa ele no mapa, senao uma bola errada tira o
@ lendario do save. Mesma regra do LUGIA e do SpearPillar_Dialga.
VerityCavern_EventScript_MespritPreso::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_VERITY_CAVERN_MESPRIT
	setflag FLAG_HIDE_MESPRIT_SINNOH
	fadescreenswapbuffers FADE_FROM_BLACK
	return

VerityCavern_EventScript_MespritSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_VERITY_CAVERN_MESPRIT
	setflag FLAG_HIDE_MESPRIT_SINNOH
	fadescreenswapbuffers FADE_FROM_BLACK
	msgbox VerityCavern_Text_MespritSome, MSGBOX_DEFAULT
	return

VerityCavern_Text_MespritIntro:
	.string "Kyauun.$"

VerityCavern_Text_MespritSome:
	.string "MESPRIT flew off somewhere...$"

@ <<< Lendarios de Sinnoh <<<
