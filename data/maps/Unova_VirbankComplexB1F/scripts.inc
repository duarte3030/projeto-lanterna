@ VirbankComplexB1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_VirbankComplexB1F_MapScripts::
	.byte 0

Unova_VirbankComplexB1F_EventScript_Placa0::
	msgbox Unova_VirbankComplexB1F_Text_VirbankComplexOpenDoorText, MSGBOX_SIGN
	end

Unova_VirbankComplexB1F_EventScript_Placa1::
	msgbox Unova_VirbankComplexB1F_Text_VirbankComplexOpenDoorText, MSGBOX_SIGN
	end

Unova_VirbankComplexB1F_EventScript_Lider0::
	trainerbattle_single TRAINER_UNOVA_SCIENTISTF_VIRBANK_COMPLEX_1, Unova_VirbankComplexB1F_Text_ScientistFVirbankComplexB1FSeenText, Unova_VirbankComplexB1F_Text_ScientistFVirbankComplexB1FBeatenText
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

Unova_VirbankComplexB1F_Text_ScientistFVirbankComplexB1FBeatenText::
	.string "What? You can"
	.string "\nactually draw out"
	.string "\pthe power of your"
	.string "\nPOKéMON?$"
