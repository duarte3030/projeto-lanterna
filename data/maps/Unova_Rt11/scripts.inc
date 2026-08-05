@ Rt11 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt11_MapScripts::
	.byte 0

Unova_Rt11_EventScript_Npc4::
	msgbox Unova_Rt11_Text_R11AmoongussText, MSGBOX_NPC
	end

Unova_Rt11_EventScript_Npc5::
	msgbox Unova_Rt11_Text_R11AmoongussText, MSGBOX_NPC
	end

Unova_Rt11_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_BACKERSM_R11, Unova_Rt11_Text_BackersMR11SeenText, Unova_Rt11_Text_BackersMR11BeatenText
	end

Unova_Rt11_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_BACKERSM_R11, Unova_Rt11_Text_BackersMR11SeenText, Unova_Rt11_Text_BackersMR11BeatenText
	end

Unova_Rt11_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_BACKERSF_R11, Unova_Rt11_Text_BackersFR11SeenText, Unova_Rt11_Text_BackersFR11BeatenText
	end

Unova_Rt11_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_BACKERSF_R11, Unova_Rt11_Text_BackersFR11SeenText, Unova_Rt11_Text_BackersFR11BeatenText
	end


Unova_Rt11_Text_R11AmoongussText::
	.string "Ooong!$"

Unova_Rt11_Text_BackersMR11SeenText::
	.string "Sports and POKé-"
	.string "\nMON battles are"
	.string "\pdramas that don't"
	.string "\nneed scripts!$"

Unova_Rt11_Text_BackersMR11BeatenText::
	.string "We were the"
	.string "\nunderdogs…$"

Unova_Rt11_Text_BackersFR11SeenText::
	.string "Knowing what a"
	.string "\ntruly heated"
	.string "\pbattle is all"
	.string "\nabout is the key"
	.string "\pto truly passion-"
	.string "\nate cheering!$"

Unova_Rt11_Text_BackersFR11BeatenText::
	.string "I cheered as best"
	.string "\nas I could…$"
