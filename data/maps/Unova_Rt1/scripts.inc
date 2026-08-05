@ Rt1 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt1_MapScripts::
	.byte 0

Unova_Rt1_EventScript_Placa0::
	msgbox Unova_Rt1_Text_R1SignText, MSGBOX_SIGN
	end

Unova_Rt1_EventScript_Npc3::
	msgbox Unova_Rt1_Text_PkmnRangerMR1SeenText, MSGBOX_NPC
	end

Unova_Rt1_EventScript_Npc4::
	msgbox Unova_Rt1_Text_PkmnRangerFR1SeenText, MSGBOX_NPC
	end

Unova_Rt1_EventScript_Npc5::
	msgbox Unova_Rt1_Text_MaidR1SeenText, MSGBOX_NPC
	end

Unova_Rt1_EventScript_Npc6::
	msgbox Unova_Rt1_Text_BlackbeltR1SeenText, MSGBOX_NPC
	end

Unova_Rt1_EventScript_Npc7::
	msgbox Unova_Rt1_Text_BattleGirlR1SeenText, MSGBOX_NPC
	end

Unova_Rt1_EventScript_Npc8::
	msgbox Unova_Rt1_Text_TwinsR1SeenText, MSGBOX_NPC
	end

Unova_Rt1_EventScript_Npc9::
	msgbox Unova_Rt1_Text_TwinsR1SeenText, MSGBOX_NPC
	end


Unova_Rt1_Text_R1SignText::
	.string "ROUTE 1."
	.string "\pNorth to ACCUMULA"
	.string "\nTOWN, south to"
	.string "\lNUVEMA TOWN.$"

Unova_Rt1_Text_PkmnRangerMR1SeenText::
	.string "I choose a move,"
	.string "\nand my POKéMON"
	.string "\lwill do the move."
	.string "\pIn a moment, that"
	.string "\nmove will reach"
	.string "\lyour POKéMON!$"

Unova_Rt1_Text_PkmnRangerFR1SeenText::
	.string "Hm? You're headed"
	.string "\nfor the JUNIPER"
	.string "\pPOKéMON LAB, aren't"
	.string "\nyou? Didn't you"
	.string "\pknow? There's a new"
	.string "\nPROF. there now!$"

Unova_Rt1_Text_MaidR1SeenText::
	.string "What? A battle at"
	.string "\na place like this?"
	.string "\pEveryone is"
	.string "\nwatching us!$"

Unova_Rt1_Text_BlackbeltR1SeenText::
	.string "This is my path!$"

Unova_Rt1_Text_BattleGirlR1SeenText::
	.string "Let me test what"
	.string "\nfighting style is"
	.string "\lmore effective!$"

Unova_Rt1_Text_TwinsR1SeenText::
	.string "My sister and I"
	.string "\nare of one mind!$"
