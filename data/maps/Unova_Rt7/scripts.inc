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

Unova_Rt7_EventScript_Npc6::
	msgbox Unova_Rt7_Text_NurseryAideR7SeenText, MSGBOX_NPC
	end

Unova_Rt7_EventScript_Npc7::
	msgbox Unova_Rt7_Text_SchoolKidMR7SeenText, MSGBOX_NPC
	end

Unova_Rt7_EventScript_Npc8::
	msgbox Unova_Rt7_Text_SchoolKidFR7SeenText, MSGBOX_NPC
	end

Unova_Rt7_EventScript_Npc9::
	msgbox Unova_Rt7_Text_PkmnBreederMR7SeenText, MSGBOX_NPC
	end

Unova_Rt7_EventScript_Npc10::
	msgbox Unova_Rt7_Text_PkmnBreederFR7SeenText, MSGBOX_NPC
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

Unova_Rt7_Text_SchoolKidMR7SeenText::
	.string "Can you keep up"
	.string "\nwithout having"
	.string "\lyour head spin?$"

Unova_Rt7_Text_SchoolKidFR7SeenText::
	.string "My victory is"
	.string "\ncoming into view!$"

Unova_Rt7_Text_PkmnBreederMR7SeenText::
	.string "I have a request"
	.string "\nfor you! Please"
	.string "\lbattle me!$"

Unova_Rt7_Text_PkmnBreederFR7SeenText::
	.string "I'm proud of my"
	.string "\nPOKéMON, which I"
	.string "\praised with love"
	.string "\nand care!$"
