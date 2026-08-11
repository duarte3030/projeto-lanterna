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
	@ O menu e montado em data/scripts/travessia_regioes.inc e esconde o
	@ destino ainda nao liberado. Os `case` abaixo NAO mudam: o id
	@ empilhado continua sendo o indice antigo da lista.
	call Travessia_EventScript_MenuDeDestinos
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
	waitstate
	release
	end

Unova_VirbankPort_Text_ZarparOlivine:
	.string "Setting sail for OLIVINE CITY\n"
	.string "in JOHTO!$"

Unova_VirbankPort_EventScript_ZarparSlateport::
	msgbox Unova_VirbankPort_Text_ZarparSlateport, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_SLATEPORT_CITY_HARBOR, 8, 14
	waitstate
	release
	end

Unova_VirbankPort_Text_ZarparSlateport:
	.string "Setting sail for SLATEPORT CITY\n"
	.string "in HOENN!$"

Unova_VirbankPort_EventScript_ZarparVermilion::
	msgbox Unova_VirbankPort_Text_ZarparVermilion, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_VERMILION_CITY, 15, 10
	waitstate
	release
	end

Unova_VirbankPort_Text_ZarparVermilion:
	.string "Setting sail for VERMILION CITY\n"
	.string "in KANTO!$"

Unova_VirbankPort_EventScript_ZarparCanalave::
	msgbox Unova_VirbankPort_Text_ZarparCanalave, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_CANALAVE_CITY, 17, 49
	waitstate
	release
	end

Unova_VirbankPort_Text_ZarparCanalave:
	.string "Setting sail for CANALAVE CITY\n"
	.string "in SINNOH!$"

Unova_VirbankPort_Text_ParaOnde:
	.string "Welcome to VIRBANK CITY, UNOVA!\n"
	.string "Where would you like to sail?$"

Unova_VirbankPort_Text_Volte:
	.string "Come see me whenever you want to\nset sail!$"



Unova_VirbankPort_Text_VirbankPortRideText::
	.string "We'll soon set"
	.string "\nsail for CASTELIA."
	.string "\pAre you coming on"
	.string "\nboard?$"
