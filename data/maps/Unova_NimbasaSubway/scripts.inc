@ NimbasaSubway do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_NimbasaSubway_MapScripts::
	.byte 0

Unova_NimbasaSubway_EventScript_Npc0::
	msgbox Unova_NimbasaSubway_Text_NimbasaSubwayAskRideText, MSGBOX_NPC
	end

Unova_NimbasaSubway_EventScript_Npc1::
	msgbox Unova_NimbasaSubway_Text_NimbasaSubwayGentlemanText, MSGBOX_NPC
	end


Unova_NimbasaSubway_Text_NimbasaSubwayAskRideText::
	.string "We'll soon depart"
	.string "\nfor ASPERTIA."
	.string "\pAre you coming"
	.string "\naboard?$"

Unova_NimbasaSubway_Text_NimbasaSubwayGentlemanText::
	.string "This used to be a"
	.string "\nBATTLE SUBWAY."
	.string "\pBut the need grew"
	.string "\nfor a regular"
	.string "\lsubway to take"
	.string "\ppeople and POKéMON"
	.string "\nto far corners of"
	.string "\lUNOVA.$"
