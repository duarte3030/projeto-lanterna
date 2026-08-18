OlivineCity_PortInside_MapScripts::
	.byte 0

OlivinePort_EventScript_Sailor::
	lock
	faceplayer
	msgbox OlivinePort_Text_WhereTo, MSGBOX_DEFAULT
	@ O menu e montado em data/scripts/travessia_regioes.inc e esconde o
	@ destino ainda nao liberado. Os `case` abaixo NAO mudam: o id
	@ empilhado continua sendo o indice antigo da lista.
	call Travessia_EventScript_MenuDeDestinos
	switch VAR_RESULT
	case 1, OlivinePort_EventScript_SailToSlateport
	case 2, OlivinePort_EventScript_SailToVermilion
	case 3, OlivinePort_EventScript_SailToVirbank
	case 4, OlivinePort_EventScript_SailToCanalave
	@ G5 de Galar: destino 6, atras de FLAG_GALAR_QA_ANDAR. O roteiro e um so,
	@ compartilhado pelos cinco portos (data/scripts/travessia_regioes.inc).
	case 6, Travessia_EventScript_ZarparParaGalar
	msgbox OlivinePort_Text_ComeAgain, MSGBOX_DEFAULT
	release
	end

@ Kanto e a unica travessia que passa POR DENTRO do navio: o S.S. Aqua liga
@ Olivine a Vermilion, e nenhum dos outros tres portos. FLAG_SSAQUA_RUMO_KANTO
@ diz ao marinheiro da porta em que lado desembarcar; o setdynamicwarp faz a
@ porta do cais devolver o jogador a este porto, para desistir da viagem.
OlivinePort_EventScript_SailToVermilion::
	msgbox OlivinePort_Text_SettingSailToVermilion, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_SSAQUA_RUMO_KANTO
	setdynamicwarp MAP_OLIVINE_CITY_PORT_INSIDE, 8, 17
	warpsilent MAP_SSAQUA_1F, 29, 3
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
	.string "Welcome to OLIVINE CITY, JOHTO!\n"
	.string "Where would you like to sail?$"

OlivinePort_Text_SettingSailToVermilion:
	.string "Setting sail for VERMILION CITY\n"
	.string "in KANTO!$"

OlivinePort_Text_SettingSailToSlateport:
	.string "Setting sail for SLATEPORT CITY\n"
	.string "in HOENN!$"

OlivinePort_Text_SettingSailToCanalave:
	.string "Setting sail for CANALAVE CITY\n"
	.string "in SINNOH!$"

OlivinePort_Text_ComeAgain:
	.string "Come see me whenever you want to\nsail between the regions.$"

OlivinePort_EventScript_SailToVirbank::
	msgbox OlivinePort_Text_SettingSailToVirbank, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_UNOVA_VIRBANK_PORT, 4, 6
	waitstate
	release
	end

OlivinePort_Text_SettingSailToVirbank:
	.string "Setting sail for VIRBANK CITY\n"
	.string "in UNOVA!$"
