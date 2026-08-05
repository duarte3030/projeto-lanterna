OlivineCity_PortInside_MapScripts::
	.byte 0

OlivinePort_EventScript_Sailor::
	lock
	faceplayer
	msgbox OlivinePort_Text_WhereTo, MSGBOX_DEFAULT
	multichoice 0, 0, MULTI_BOAT_DESTINATIONS, FALSE
	switch VAR_RESULT
	case 1, OlivinePort_EventScript_SailToSlateport
	case 2, OlivinePort_EventScript_SailToVermilion
	case 3, OlivinePort_EventScript_SailToVirbank
	case 4, OlivinePort_EventScript_SailToCanalave
	msgbox OlivinePort_Text_ComeAgain, MSGBOX_DEFAULT
	release
	end

OlivinePort_EventScript_SailToVermilion::
	msgbox OlivinePort_Text_SettingSailToVermilion, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_VERMILION_CITY, 15, 10
	waitstate
	release
	end

OlivinePort_EventScript_SailToSlateport::
	msgbox OlivinePort_Text_SettingSailToSlateport, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_SLATEPORT_CITY_HARBOR, 8, 14
	waitstate
	release
	end

OlivinePort_EventScript_SailToCanalave::
	msgbox OlivinePort_Text_SettingSailToCanalave, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_CANALAVE_CITY, 17, 49
	waitstate
	release
	end

OlivinePort_Text_WhereTo:
	.string "Bem-vindo ao Porto de Olivine City em Johto!\nPara onde gostaria de navegar?$"

OlivinePort_Text_SettingSailToVermilion:
	.string "Zarpando para Vermilion City em Kanto!$"

OlivinePort_Text_SettingSailToSlateport:
	.string "Zarpando para Slateport City em Hoenn!$"

OlivinePort_Text_SettingSailToCanalave:
	.string "Zarpando para Canalave City em Sinnoh!$"

OlivinePort_Text_ComeAgain:
	.string "Volte quando quiser navegar entre as regioes.$"

OlivinePort_EventScript_SailToVirbank::
	msgbox OlivinePort_Text_SettingSailToVirbank, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_UNOVA_VIRBANK_PORT, 4, 6
	waitstate
	release
	end

OlivinePort_Text_SettingSailToVirbank:
	.string "Zarpando para Virbank City em Unova!$"
