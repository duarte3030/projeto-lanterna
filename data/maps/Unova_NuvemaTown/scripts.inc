@ NuvemaTown do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_NuvemaTown_MapScripts::
	.byte 0

Unova_NuvemaTown_EventScript_Placa0::
	msgbox Unova_NuvemaTown_Text_NuvemaLabSignText, MSGBOX_SIGN
	end

Unova_NuvemaTown_EventScript_Placa1::
	msgbox Unova_NuvemaTown_Text_NuvemaTownSignText, MSGBOX_SIGN
	end

Unova_NuvemaTown_EventScript_Npc0::
	msgbox Unova_NuvemaTown_Text_NuvemaTownPokefanMText, MSGBOX_NPC
	end

Unova_NuvemaTown_EventScript_Npc1::
	msgbox Unova_NuvemaTown_Text_NuvemaTownTeacherText, MSGBOX_NPC
	end


Unova_NuvemaTown_Text_NuvemaLabSignText::
	.string "NUVEMA POKéMON"
	.string "\nLAB."
	.string "\pPROF. BIANCA BEL"
	.string "\npresiding.$"

Unova_NuvemaTown_Text_NuvemaTownSignText::
	.string "NUVEMA TOWN."
	.string "\pThe start of"
	.string "\nsomething big!$"

Unova_NuvemaTown_Text_NuvemaTownPokefanMText::
	.string "A couple of years"
	.string "\nago, my daughter"
	.string "\lbecame the POKéMON"
	.string "\lPROF!"
	.string "\pI couldn't be"
	.string "\nmore proud!$"

Unova_NuvemaTown_Text_NuvemaTownTeacherText::
	.string "Welcome to NUVEMA"
	.string "\nTOWN! We may not"
	.string "\plook like much,"
	.string "\nbut we're home to"
	.string "\pUNOVA's POKéMON"
	.string "\nLAB!$"
