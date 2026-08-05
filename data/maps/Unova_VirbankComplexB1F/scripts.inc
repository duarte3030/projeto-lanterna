@ VirbankComplexB1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_VirbankComplexB1F_MapScripts::
	.byte 0

Unova_VirbankComplexB1F_EventScript_Placa0::
	msgbox Unova_VirbankComplexB1F_Text_VirbankComplexOpenDoorText, MSGBOX_SIGN
	end

Unova_VirbankComplexB1F_EventScript_Placa1::
	msgbox Unova_VirbankComplexB1F_Text_VirbankComplexOpenDoorText, MSGBOX_SIGN
	end

Unova_VirbankComplexB1F_EventScript_Npc0::
	msgbox Unova_VirbankComplexB1F_Text_ScientistFVirbankComplexB1FSeenText, MSGBOX_NPC
	end


Unova_VirbankComplexB1F_Text_VirbankComplexOpenDoorText::
	.string "The door opened!$"

Unova_VirbankComplexB1F_Text_ScientistFVirbankComplexB1FSeenText::
	.string "TEAM PLASMA is"
	.string "\nstudying things"
	.string "\pyou couldn't"
	.string "\npossibly under-"
	.string "\pstand. For that"
	.string "\npurpose, please"
	.string "\phand over your"
	.string "\nPOKéMON.$"
