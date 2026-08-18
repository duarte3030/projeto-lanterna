@ CasteliaBridgeGate do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_CasteliaBridgeGate_MapScripts::
	.byte 0

Unova_CasteliaBridgeGate_EventScript_Npc0::
	msgbox Unova_CasteliaBridgeGate_Text_CasteliaBridgeGateOfficerText, MSGBOX_NPC
	end

Unova_CasteliaBridgeGate_EventScript_Npc1::
	msgbox Unova_CasteliaBridgeGate_Text_CasteliaBridgeGateOfficerText, MSGBOX_NPC
	end

@ B6 Unova, Fase B (18/08/2026): CasteliaBridgeGateStopScript@6,3/6,4 da
@ fonte. Sem checkevent e sem setmapscene em NENHUM .asm do bw3g (varrido:
@ zero setmapscene para CASTELIA_BRIDGE_GATE no fonte inteiro). A SKYARROW
@ BRIDGE fica fechada por construcao para sempre, permanente por desenho
@ desde a origem, nao pendencia de mecanica faltando. VAR_TEMP_0/0 de
@ sempre disparar. Zero flag e zero var novas.
Unova_CasteliaBridgeGate_EventScript_PonteFechada::
	lock
	turnobject LOCALID_PLAYER, DIR_NORTH
	msgbox Unova_CasteliaBridgeGate_Text_CasteliaBridgeGateOfficerStopText, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PLAYER, Common_Movement_WalkLeft
	waitmovement 0
	release
	end


Unova_CasteliaBridgeGate_Text_CasteliaBridgeGateOfficerText::
	.string "Be careful if"
	.string "\nyou're planning to"
	.string "\pcross the SKY-"
	.string "\nARROW BRIDGE!$"

Unova_CasteliaBridgeGate_Text_CasteliaBridgeGateOfficerStopText::
	.string "Sorry, the SKY-"
	.string "\nARROW BRIDGE is"
	.string "\pclosed to pedes-"
	.string "\ntrian traffic"
	.string "\lright now due to"
	.string "\lconstruction.$"
