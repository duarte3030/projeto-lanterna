@ Rt5BridgeGate do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt5BridgeGate_MapScripts::
	.byte 0

@ >>> B6 Unova, Obra 1: gatilhos de setscene (dev_scripts/gatilhos_setscene_unova.py) >>>
@ Irma de Unova_DriftveilBridgeGate: so abre com FLAG_UNOVA_DRIFTVEIL_BLOQUEIO
@ (checkevent EVENT_DRIFTVEIL_BLOCKER na fonte). Mesma receita de earthquake
@ ja usada em Unova_VirbankComplexElevator e em Unova_DriftveilBridgeGate.
Unova_Rt5BridgeGate_EventScript_Rt5BridgeGateBadgeScript::
	lockall
	turnobject LOCALID_PLAYER, DIR_NORTH
	goto_if_unset FLAG_UNOVA_DRIFTVEIL_BLOQUEIO, Unova_Rt5BridgeGate_EventScript_PonteFechada
	msgbox Unova_Rt5BridgeGate_Text_Rt5BridgeGateOfficerRaiseBridgeText, MSGBOX_DEFAULT
	closemessage
	playse SE_ELEVATOR
	setvar VAR_0x8004, 1
	setvar VAR_0x8005, 0
	setvar VAR_0x8006, 12
	setvar VAR_0x8007, 3
	special ShakeScreen
	delay 60
	waitse
	msgbox Unova_Rt5BridgeGate_Text_Rt5BridgeGateOfficerText, MSGBOX_DEFAULT
	closemessage
	setvar VAR_UNOVA_R5_PORTAO_PONTE_CENA, 1
	setvar VAR_UNOVA_DRIFTVEIL_PORTAO_PONTE_CENA, 1
	releaseall
	end

Unova_Rt5BridgeGate_EventScript_PonteFechada::
	msgbox Unova_Rt5BridgeGate_Text_Rt5BridgeGateOfficerStopText, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PLAYER, Common_Movement_WalkRight
	waitmovement 0
	releaseall
	end

@ <<< B6 Unova, Obra 1: gatilhos de setscene <<<

Unova_Rt5BridgeGate_EventScript_Npc0::
	msgbox Unova_Rt5BridgeGate_Text_Rt5BridgeGateOfficerText, MSGBOX_NPC
	end


Unova_Rt5BridgeGate_Text_Rt5BridgeGateOfficerStopText::
	.string "Sorry buddy, the"
	.string "\nDRAWBRIDGE is"
	.string "\lraised right now."
	.string "\pI would call and"
	.string "\nask for the BRIDGE"
	.string "\lto be lowered, but"
	.string "\pthe attendant in"
	.string "\nDRIFTVEIL CITY"
	.string "\lisn't answering"
	.string "\lmy calls."
	.string "\pI wonder if"
	.string "\nsomething is going"
	.string "\lon over there…$"

Unova_Rt5BridgeGate_Text_Rt5BridgeGateOfficerRaiseBridgeText::
	.string "Oh, you want to"
	.string "\ncross? Let me call"
	.string "\lthe operator in"
	.string "\lDRIFTVEIL CITY."
	.string "\pOkay, it will be"
	.string "\nlowered now.$"

Unova_Rt5BridgeGate_Text_Rt5BridgeGateOfficerText::
	.string "The BRIDGE has"
	.string "\nnow been lowered."
	.string "\pIt will take you"
	.string "\nto DRIFTVEIL CITY.$"
