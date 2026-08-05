@ NimbasaHouse do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_NimbasaHouse_MapScripts::
	.byte 0

Unova_NimbasaHouse_EventScript_Npc0::
	msgbox Unova_NimbasaHouse_Text_NimbasaHouseGiveBellText, MSGBOX_NPC
	end


Unova_NimbasaHouse_Text_NimbasaHouseGiveBellText::
	.string "You're a POKéMON"
	.string "\ntrainer, right?"
	.string "\pYou seem like the"
	.string "\nkind of trainer"
	.string "\pwho is kind to"
	.string "\nyour POKéMON."
	.string "\pHere, have this.$"

@ Placas trazidas do BW3G por dev_scripts/importa_placas_unova.py

@ jumpstd apartmentstairs do BW3G; texto de data/text/std_text.asm
Unova_EventScript_EscadaPredio::
	msgbox Unova_Text_EscadaPredio, MSGBOX_SIGN
	end

Unova_Text_EscadaPredio::
	.string "The door to the\n"
	.string "stairwell is closed.$"
