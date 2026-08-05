@ VirbankPort do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_VirbankPort_MapScripts::
	.byte 0

Unova_VirbankPort_EventScript_Npc0::
	msgbox Unova_VirbankPort_Text_VirbankPortRideText, MSGBOX_NPC
	end

Unova_VirbankPort_EventScript_Marinheiro::
	lock
	faceplayer
	msgbox Unova_VirbankPort_Text_ParaOnde, MSGBOX_DEFAULT
	multichoice 0, 0, MULTI_BOAT_DESTINATIONS, FALSE
	switch VAR_RESULT
	case 0, Unova_VirbankPort_EventScript_ZarparOlivine
	case 1, Unova_VirbankPort_EventScript_ZarparSlateport
	case 2, Unova_VirbankPort_EventScript_ZarparVermilion
	case 4, Unova_VirbankPort_EventScript_ZarparCanalave
	msgbox Unova_VirbankPort_Text_Volte, MSGBOX_DEFAULT
	release
	end

Unova_VirbankPort_EventScript_ZarparOlivine::
	msgbox Unova_VirbankPort_Text_ZarparOlivine, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_OLIVINE_CITY_PORT_INSIDE, 8, 17
	release
	end

Unova_VirbankPort_Text_ZarparOlivine:
	.string "Zarpando para Olivine City em Johto!$"

Unova_VirbankPort_EventScript_ZarparSlateport::
	msgbox Unova_VirbankPort_Text_ZarparSlateport, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_SLATEPORT_CITY_HARBOR, 8, 14
	release
	end

Unova_VirbankPort_Text_ZarparSlateport:
	.string "Zarpando para Slateport City em Hoenn!$"

Unova_VirbankPort_EventScript_ZarparVermilion::
	msgbox Unova_VirbankPort_Text_ZarparVermilion, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_VERMILION_CITY, 15, 10
	release
	end

Unova_VirbankPort_Text_ZarparVermilion:
	.string "Zarpando para Vermilion City em Kanto!$"

Unova_VirbankPort_EventScript_ZarparCanalave::
	msgbox Unova_VirbankPort_Text_ZarparCanalave, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_CANALAVE_CITY, 10, 10
	release
	end

Unova_VirbankPort_Text_ZarparCanalave:
	.string "Zarpando para Canalave City em Sinnoh!$"

Unova_VirbankPort_Text_ParaOnde:
	.string "Bem-vindo ao Porto de Virbank City em Unova!\nPara onde gostaria de navegar?$"

Unova_VirbankPort_Text_Volte:
	.string "Volte quando quiser zarpar!$"



Unova_VirbankPort_Text_VirbankPortRideText::
	.string "We'll soon set"
	.string "\nsail for CASTELIA."
	.string "\pAre you coming on"
	.string "\nboard?$"
