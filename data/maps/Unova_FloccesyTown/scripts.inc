@ FloccesyTown do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_FloccesyTown_MapScripts::
	.byte 0

Unova_FloccesyTown_EventScript_Placa0::
	msgbox Unova_FloccesyTown_Text_FloccesyTownSignText, MSGBOX_SIGN
	end

Unova_FloccesyTown_EventScript_Npc2::
	msgbox Unova_FloccesyTown_Text_FloccesyTownTwinText, MSGBOX_NPC
	end

Unova_FloccesyTown_EventScript_Npc3::
	msgbox Unova_FloccesyTown_Text_FloccesyTownPokefanMText, MSGBOX_NPC
	end

Unova_FloccesyTown_EventScript_Npc4::
	msgbox Unova_FloccesyTown_Text_FloccesyTownBlockerText, MSGBOX_NPC
	end


Unova_FloccesyTown_Text_FloccesyTownSignText::
	.string "FLOCCESY TOWN"
	.string "\pProphecy flocks"
	.string "\nhere!$"

Unova_FloccesyTown_Text_FloccesyTownTwinText::
	.string "I want to go to"
	.string "\nthe ranch! I want"
	.string "\lto get some milk!$"

Unova_FloccesyTown_Text_FloccesyTownPokefanMText::
	.string "Welcome to our"
	.string "\nlittle town. It"
	.string "\pain't much, but"
	.string "\nthe ranch outside"
	.string "\pof town delivers"
	.string "\nmilk all over"
	.string "\lUNOVA.$"

Unova_FloccesyTown_Text_FloccesyTownBlockerText::
	.string "Mister ALDER isn't"
	.string "\nhome right now."
	.string "\pAw man, I wanted"
	.string "\nto train with him!$"
