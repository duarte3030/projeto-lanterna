@ Rt12VillageBridgeGate do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt12VillageBridgeGate_MapScripts::
	.byte 0

Unova_Rt12VillageBridgeGate_EventScript_Npc0::
	msgbox Unova_Rt12VillageBridgeGate_Text_R12VillageBridgeGateOfficerText, MSGBOX_NPC
	end

@ B6 Unova, Fase B (18/08/2026): irma remota de Unova_Rt5BridgeGate/
@ Unova_DriftveilBridgeGate, mesma familia de ponte-com-portao. A var ja
@ existe (VAR_UNOVA_R12_VILLAGE_BRIDGE_PORTAO_CENA, tabela remota do
@ PLANO-OBRAS-UNOVA.md) e ja e escrita para 1 por
@ Unova_SeasideCaveChamber/scripts.inc:134, entao o gatilho so PRECISA ler,
@ nunca escrever. Zero flag e zero var novas.
Unova_Rt12VillageBridgeGate_EventScript_PonteFechada::
	lock
	turnobject LOCALID_PLAYER, DIR_NORTH
	msgbox Unova_Rt12VillageBridgeGate_Text_R12VillageBridgeGateBridgeOutText, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PLAYER, Common_Movement_WalkRight
	waitmovement 0
	release
	end


Unova_Rt12VillageBridgeGate_Text_R12VillageBridgeGateOfficerText::
	.string "The bridge has"
	.string "\nfinally been"
	.string "\lfixed!"
	.string "\pGo on ahead.$"

Unova_Rt12VillageBridgeGate_Text_R12VillageBridgeGateBridgeOutText::
	.string "Wait! Sorry, the"
	.string "\nVILLAGE BRIDGE"
	.string "\pis closed off"
	.string "\nright now."
	.string "\pThe path has been"
	.string "\nflooded."
	.string "\pIt’s going to"
	.string "\ntake some time"
	.string "\pbefore the path"
	.string "\nis cleared, so"
	.string "\lcome back later.$"
