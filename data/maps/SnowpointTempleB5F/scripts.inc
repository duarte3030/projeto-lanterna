SnowpointTempleB5F_MapScripts::
	.byte 0

@ >>> Lendarios de Sinnoh (dev_scripts/lendarios_sinnoh.py) >>>
SnowpointTempleB5F_EventScript_Regigigas::
	lockall
	msgbox SnowpointTempleB5F_Text_RegigigasIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_REGIGIGAS, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_REGIGIGAS, 1
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_SNOWPOINT_TEMPLE_B5_F_REGIGIGAS
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, SnowpointTempleB5F_EventScript_RegigigasSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, SnowpointTempleB5F_EventScript_RegigigasPreso
	releaseall
	end

@ ponytail: so apaga o bicho em VITORIA ou CAPTURA. Fugir, perder ou
@ ser teleportado deixa ele no mapa, senao uma bola errada tira o
@ lendario do save. Mesma regra do LUGIA e do SpearPillar_Dialga.
SnowpointTempleB5F_EventScript_RegigigasPreso::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_SNOWPOINT_TEMPLE_B5_F_REGIGIGAS
	setflag FLAG_HIDE_REGIGIGAS_SINNOH
	fadescreenswapbuffers FADE_FROM_BLACK
	return

SnowpointTempleB5F_EventScript_RegigigasSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_SNOWPOINT_TEMPLE_B5_F_REGIGIGAS
	setflag FLAG_HIDE_REGIGIGAS_SINNOH
	fadescreenswapbuffers FADE_FROM_BLACK
	msgbox SnowpointTempleB5F_Text_RegigigasSome, MSGBOX_DEFAULT
	return

SnowpointTempleB5F_Text_RegigigasIntro:
	.string "...Zut zutt!$"

SnowpointTempleB5F_Text_RegigigasSome:
	.string "REGIGIGAS disappeared from view...$"

@ <<< Lendarios de Sinnoh <<<
