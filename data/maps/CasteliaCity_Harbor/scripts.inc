CasteliaCity_Harbor_MapScripts::
	.byte 0

CasteliaHarbor_EventScript_Sailor::
	lock
	faceplayer
	msgbox CasteliaHarbor_Text_WhereTo, MSGBOX_DEFAULT
	multichoice 0, 0, MULTI_BOAT_DESTINATIONS, FALSE
	switch VAR_RESULT
	case 0, CasteliaHarbor_EventScript_SailToCanalave
	case 1, CasteliaHarbor_EventScript_SailToSlateport
	case 2, CasteliaHarbor_EventScript_SailToOlivine
	msgbox CasteliaHarbor_Text_ComeAgain, MSGBOX_DEFAULT
	release
	end

CasteliaHarbor_EventScript_SailToCanalave::
	msgbox CasteliaHarbor_Text_SettingSailToCanalave, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_CANALAVE_CITY, 10, 10
	release
	end

CasteliaHarbor_EventScript_SailToSlateport::
	msgbox CasteliaHarbor_Text_SettingSailToSlateport, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_SLATEPORT_CITY_HARBOR, 8, 14
	release
	end

CasteliaHarbor_EventScript_SailToOlivine::
	msgbox CasteliaHarbor_Text_SettingSailToOlivine, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_OLIVINE_CITY_PORT_INSIDE, 8, 17
	release
	end

CasteliaHarbor_Text_WhereTo:
	.string "Bem-vindo ao Porto de Castelia City em Unova!\nPara onde gostaria de navegar?$"

CasteliaHarbor_Text_SettingSailToCanalave:
	.string "Zarpando para Canalave City em Sinnoh!$"

CasteliaHarbor_Text_SettingSailToSlateport:
	.string "Zarpando para Slateport City em Hoenn!$"

CasteliaHarbor_Text_SettingSailToOlivine:
	.string "Zarpando para Olivine City em Johto!$"

CasteliaHarbor_Text_ComeAgain:
	.string "Volte quando quiser navegar.$"
