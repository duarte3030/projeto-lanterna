@ Rt13 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt13_MapScripts::
	.byte 0

Unova_Rt13_EventScript_Placa0::
	msgbox Unova_Rt13_Text_R13SignText, MSGBOX_SIGN
	end

Unova_Rt13_EventScript_Placa1::
	msgbox Unova_Rt13_Text_R13UndellaSignText, MSGBOX_SIGN
	end

Unova_Rt13_EventScript_Npc0::
	msgbox Unova_Rt13_Text_R13Blocker1Text, MSGBOX_NPC
	end

Unova_Rt13_EventScript_Npc1::
	msgbox Unova_Rt13_Text_R13Blocker2Text, MSGBOX_NPC
	end

Unova_Rt13_EventScript_Npc2::
	msgbox Unova_Rt13_Text_R13Blocker3Text, MSGBOX_NPC
	end

Unova_Rt13_EventScript_Npc3::
	msgbox Unova_Rt13_Text_R13Blocker4Text, MSGBOX_NPC
	end

Unova_Rt13_EventScript_Npc4::
	msgbox Unova_Rt13_Text_YoungsterR13SeenText, MSGBOX_NPC
	end

Unova_Rt13_EventScript_Npc5::
	msgbox Unova_Rt13_Text_LassR13SeenText, MSGBOX_NPC
	end

Unova_Rt13_EventScript_Npc6::
	msgbox Unova_Rt13_Text_SchoolKidMR13SeenText, MSGBOX_NPC
	end

Unova_Rt13_EventScript_Npc7::
	msgbox Unova_Rt13_Text_SchoolKidFR13SeenText, MSGBOX_NPC
	end


Unova_Rt13_Text_R13SignText::
	.string "GIANT CHASM"
	.string "\pBeware of wild"
	.string "\nPOKéMON!$"

Unova_Rt13_Text_R13UndellaSignText::
	.string "ROUTE 13"
	.string "\pA beachside"
	.string "\nstroll from"
	.string "\pUNDELLA TOWN to"
	.string "\nLACUNOSA TOWN.$"

Unova_Rt13_Text_R13Blocker1Text::
	.string "Hey, watch out!"
	.string "\pWe're in the"
	.string "\nmiddle of a POKé-"
	.string "\lMON battle!$"

Unova_Rt13_Text_R13Blocker2Text::
	.string "PATRAT: Prah!$"

Unova_Rt13_Text_R13Blocker3Text::
	.string "PURRLOIN: Prrr-$"

Unova_Rt13_Text_R13Blocker4Text::
	.string "Stop bothering"
	.string "\nme! I'll battle"
	.string "\pyou when I'm"
	.string "\nfinished.$"

Unova_Rt13_Text_YoungsterR13SeenText::
	.string "You can tell how"
	.string "\nmuch your opponent"
	.string "\lwants to fight by"
	.string "\plooking into their"
	.string "\neyes, don't you"
	.string "\lthink?$"

Unova_Rt13_Text_LassR13SeenText::
	.string "Hey, you! Have you"
	.string "\nseen my cute POKé-"
	.string "\lMON? Take a look!$"

Unova_Rt13_Text_SchoolKidMR13SeenText::
	.string "I'm the strongest"
	.string "\ntrainer in my"
	.string "\lclass!$"

Unova_Rt13_Text_SchoolKidFR13SeenText::
	.string "My favorite class"
	.string "\nis math!$"
