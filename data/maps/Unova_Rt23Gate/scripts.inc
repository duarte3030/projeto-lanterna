@ Rt23Gate do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt23Gate_MapScripts::
	.byte 0

@ >>> B6 Unova, Obra 1: gatilhos de setscene (dev_scripts/gatilhos_setscene_unova.py) >>>
@ Portao entre Rt23East e Rt23Gate; so o jogador vira (o oficial nao tem
@ turnobject na fonte). `buttonsound`/`waitsfx` descartado, mesma razao dos
@ outros cracha-checks de Rt23.
Unova_Rt23Gate_EventScript_R23GateBadgeScript::
	lockall
	turnobject LOCALID_PLAYER, DIR_NORTH
	msgbox Unova_Rt23Gate_Text_R23GateOfficerStopText, MSGBOX_DEFAULT
	closemessage
	goto_if_unset FLAG_BADGE_UNOVA_HUMILAU, Unova_Rt23Gate_EventScript_R23GateBadgeSemInsignia
	msgbox Unova_Rt23Gate_Text_R23GateOfficerHaveBadgeText, MSGBOX_DEFAULT
	closemessage
	setvar VAR_UNOVA_R23_PORTAO_CENA, 1
	releaseall
	end

Unova_Rt23Gate_EventScript_R23GateBadgeSemInsignia::
	applymovement LOCALID_PLAYER, Common_Movement_WalkRight
	waitmovement 0
	releaseall
	end

@ <<< B6 Unova, Obra 1: gatilhos de setscene <<<

Unova_Rt23Gate_EventScript_Npc0::
	msgbox Unova_Rt23Gate_Text_R23GateOfficerHaveBadgeText, MSGBOX_NPC
	end


Unova_Rt23Gate_Text_R23GateOfficerStopText::
	.string "Stop! Ahead lies"
	.string "\nthe path to the"
	.string "\lPOKéMON LEAGUE."
	.string "\pOnly those who"
	.string "\nhave collected"
	.string "\pall 8 POKéMON"
	.string "\nLEAGUE GYM BADGES"
	.string "\lmay enter."
	.string "\pYou cannot pass"
	.string "\nhere unless you"
	.string "\phave the"
	.string "\nWAVEBADGE.$"

Unova_Rt23Gate_Text_R23GateOfficerHaveBadgeText::
	.string "Oh, that is the"
	.string "\nWAVEBADGE!"
	.string "\pYou may pass.$"
