@ Rt7 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt7_MapScripts::
	.byte 0

Unova_Rt7_EventScript_Placa0::
	msgbox Unova_Rt7_Text_R7SignText, MSGBOX_SIGN
	end

Unova_Rt7_EventScript_Placa1::
	msgbox Unova_Rt7_Text_R7TowerSignText, MSGBOX_SIGN
	end

Unova_Rt7_EventScript_Npc4::
	msgbox Unova_Rt7_Text_R7AmoongussText, MSGBOX_NPC
	end

Unova_Rt7_EventScript_Npc5::
	msgbox Unova_Rt7_Text_R7AmoongussText, MSGBOX_NPC
	end

Unova_Rt7_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_NURSERY_AIDE_R7, Unova_Rt7_Text_NurseryAideR7SeenText, Unova_Rt7_Text_NurseryAideR7BeatenText
	end

Unova_Rt7_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_SCHOOL_KIDM_R7, Unova_Rt7_Text_SchoolKidMR7SeenText, Unova_Rt7_Text_SchoolKidMR7BeatenText
	end

Unova_Rt7_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_SCHOOL_KIDF_R7, Unova_Rt7_Text_SchoolKidFR7SeenText, Unova_Rt7_Text_SchoolKidFR7BeatenText
	end

Unova_Rt7_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_PKMN_BREEDERM_R7, Unova_Rt7_Text_PkmnBreederMR7SeenText, Unova_Rt7_Text_PkmnBreederMR7BeatenText
	end

Unova_Rt7_EventScript_Lider10::
	trainerbattle_single TRAINER_UNOVA_PKMN_BREEDERF_R7, Unova_Rt7_Text_PkmnBreederFR7SeenText, Unova_Rt7_Text_PkmnBreederFR7BeatenText
	end


Unova_Rt7_Text_R7SignText::
	.string "ROUTE 7."
	.string "\nNorth to"
	.string "\lCELESTIAL TOWER.$"

Unova_Rt7_Text_R7TowerSignText::
	.string "CELESTIAL TOWER."
	.string "\pPurify your"
	.string "\nspirit.$"

Unova_Rt7_Text_R7AmoongussText::
	.string "Ooong!$"

Unova_Rt7_Text_NurseryAideR7SeenText::
	.string "Well, well, well…"
	.string "\nIf it isn't a lost"
	.string "\lPOKéMON!$"

Unova_Rt7_Text_NurseryAideR7BeatenText::
	.string "Sorry! I mistook"
	.string "\nyou for a POKéMON!$"

Unova_Rt7_Text_SchoolKidMR7SeenText::
	.string "Can you keep up"
	.string "\nwithout having"
	.string "\lyour head spin?$"

Unova_Rt7_Text_SchoolKidMR7BeatenText::
	.string "Oh… My head is"
	.string "\nspinning…$"

Unova_Rt7_Text_SchoolKidFR7SeenText::
	.string "My victory is"
	.string "\ncoming into view!$"

Unova_Rt7_Text_SchoolKidFR7BeatenText::
	.string "Ahh, how could I"
	.string "\npossibly lose?$"

Unova_Rt7_Text_PkmnBreederMR7SeenText::
	.string "I have a request"
	.string "\nfor you! Please"
	.string "\lbattle me!$"

Unova_Rt7_Text_PkmnBreederMR7BeatenText::
	.string "I'm happy my POKé-"
	.string "\nMON got some good"
	.string "\lexperience.$"

Unova_Rt7_Text_PkmnBreederFR7SeenText::
	.string "I'm proud of my"
	.string "\nPOKéMON, which I"
	.string "\praised with love"
	.string "\nand care!$"

Unova_Rt7_Text_PkmnBreederFR7BeatenText::
	.string "Looks like I lost"
	.string "\nto you in the"
	.string "\plove and care"
	.string "\ndepartment!$"
