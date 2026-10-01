SendoffSpring_MapScripts::
	.byte 0

@ >>> Lendarios de Sinnoh (dev_scripts/lendarios_sinnoh.py) >>>
SendoffSpring_EventScript_Cresselia::
	lockall
	msgbox SendoffSpring_Text_CresseliaIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_CRESSELIA, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_CRESSELIA, 85
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_SENDOFF_SPRING_CRESSELIA
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, SendoffSpring_EventScript_CresseliaSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, SendoffSpring_EventScript_CresseliaPreso
	releaseall
	end

@ ponytail: so apaga o bicho em VITORIA ou CAPTURA. Fugir, perder ou
@ ser teleportado deixa ele no mapa, senao uma bola errada tira o
@ lendario do save. Mesma regra do LUGIA e do SpearPillar_Dialga.
SendoffSpring_EventScript_CresseliaPreso::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_SENDOFF_SPRING_CRESSELIA
	setflag FLAG_HIDE_CRESSELIA_SINNOH
	fadescreenswapbuffers FADE_FROM_BLACK
	return

SendoffSpring_EventScript_CresseliaSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_SENDOFF_SPRING_CRESSELIA
	setflag FLAG_HIDE_CRESSELIA_SINNOH
	fadescreenswapbuffers FADE_FROM_BLACK
	msgbox SendoffSpring_Text_CresseliaSome, MSGBOX_DEFAULT
	return

SendoffSpring_Text_CresseliaIntro:
	.string "A crescent glow drifts over the\nstill water of the spring...$"

SendoffSpring_Text_CresseliaSome:
	.string "The Pokemon flew off somewhere...$"

@ <<< Lendarios de Sinnoh <<<
