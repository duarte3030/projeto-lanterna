@ Textos vindos de pret/pokeplatinum (res/text/canalave_city.json), em ingles.
@ Rival_Bridge, Counterpart (Dawn/Lucas), Prof_Rowan, Sailor e Rival_Library
@ ficaram de fora: dependem de flag de historia (FLAG_HIDE_CANALAVE_CITY_*),
@ que este agente nao pode inventar.

CanalaveCity_MapScripts::
	.byte 0

CanalaveCity_EventScript_Collector::
	msgbox CanalaveCity_Text_Collector, MSGBOX_NPC
	end

CanalaveCity_EventScript_Lass::
	msgbox CanalaveCity_Text_Lass, MSGBOX_NPC
	end

CanalaveCity_EventScript_BreederM::
	msgbox CanalaveCity_Text_BreederM, MSGBOX_NPC
	end

CanalaveCity_EventScript_AceTrainer::
	msgbox CanalaveCity_Text_AceTrainer, MSGBOX_NPC
	end

CanalaveCity_EventScript_OldMan::
	msgbox CanalaveCity_Text_OldMan, MSGBOX_NPC
	end

CanalaveCity_EventScript_SailorEldritch::
	lock
	faceplayer
	msgbox CanalaveCity_Text_WhereTo, MSGBOX_DEFAULT
	multichoice 0, 0, MULTI_BOAT_FROM_CANALAVE, FALSE
	switch VAR_RESULT
	case 0, CanalaveCity_EventScript_SailToOlivine
	case 1, CanalaveCity_EventScript_SailToSlateport
	case 2, CanalaveCity_EventScript_SailToVermilion
	msgbox CanalaveCity_Text_ComeAgain, MSGBOX_DEFAULT
	release
	end

CanalaveCity_EventScript_SailToOlivine::
	msgbox CanalaveCity_Text_SettingSailToOlivine, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_OLIVINE_CITY_PORT_INSIDE, 8, 17
	waitstate
	release
	end

CanalaveCity_EventScript_SailToSlateport::
	msgbox CanalaveCity_Text_SettingSailToSlateport, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_SLATEPORT_CITY_HARBOR, 8, 14
	waitstate
	release
	end

CanalaveCity_EventScript_SailToVermilion::
	msgbox CanalaveCity_Text_SettingSailToVermilion, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_VERMILION_CITY, 15, 10
	waitstate
	release
	end

CanalaveCity_Text_WhereTo:
	.string "Bem-vindo ao Porto de Canalave City em Sinnoh!\nPara onde gostaria de navegar?$"

CanalaveCity_Text_SettingSailToOlivine:
	.string "Zarpando para Olivine City em Johto!$"

CanalaveCity_Text_SettingSailToSlateport:
	.string "Zarpando para Slateport City em Hoenn!$"

CanalaveCity_Text_SettingSailToVermilion:
	.string "Zarpando para Vermilion City em Kanto!$"

CanalaveCity_Text_ComeAgain:
	.string "Volte quando quiser navegar.$"

CanalaveCity_EventScript_GymSign::
	msgbox CanalaveCity_Text_GymSign, MSGBOX_SIGN
	end

CanalaveCity_EventScript_LibrarySign::
	msgbox CanalaveCity_Text_LibrarySign, MSGBOX_SIGN
	end

CanalaveCity_Text_Collector:
	.string "What's up? Your clothes look damp.\n"
	.string "Maybe you took the boat to IRON\l"
	.string "ISLAND to get a Hidden Machine,\l"
	.string "right?$"

CanalaveCity_Text_Lass:
	.string "My PSYDUCK is very close to me.\n"
	.string "That makes its Return move\l"
	.string "powerful!$"

CanalaveCity_Text_BreederM:
	.string "Welcome to CANALAVE CITY, the\n"
	.string "Canal City! In the old days, this\l"
	.string "port used to be a hub of cargo\l"
	.string "transportation.$"

CanalaveCity_Text_AceTrainer:
	.string "I'm going to study at the library.\n"
	.string "I've taken an interest in the\l"
	.string "subject of time and space.$"

CanalaveCity_Text_OldMan:
	.string "The GYM LEADER and Trainers of\n"
	.string "this GYM often go out to IRON\l"
	.string "ISLAND. They not only train their\l"
	.string "POKéMON, but they work out as\l"
	.string "well.$"

CanalaveCity_Text_SailorEldritch:
	.string "Do you wanna set sail?\p"
	.string "You just tell me whenever you\n"
	.string "need to set sail!$"

CanalaveCity_Text_GymSign:
	.string "CANALAVE CITY POKéMON GYM\p"
	.string "The Steel-Type Sturdiness Style!$"

CanalaveCity_Text_LibrarySign:
	.string "CANALAVE LIBRARY$"
