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
	@ O menu e montado em data/scripts/travessia_regioes.inc e esconde o
	@ destino ainda nao liberado. Os `case` abaixo NAO mudam: o id
	@ empilhado continua sendo o indice antigo da lista.
	call Travessia_EventScript_MenuDeDestinos
	switch VAR_RESULT
	case 0, CanalaveCity_EventScript_SailToOlivine
	case 1, CanalaveCity_EventScript_SailToSlateport
	case 2, CanalaveCity_EventScript_SailToVermilion
	case 3, CanalaveCity_EventScript_SailToVirbank
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
	.string "Welcome to CANALAVE CITY, SINNOH!\n"
	.string "Where would you like to sail?$"

CanalaveCity_Text_SettingSailToOlivine:
	.string "Setting sail for OLIVINE CITY\n"
	.string "in JOHTO!$"

CanalaveCity_Text_SettingSailToSlateport:
	.string "Setting sail for SLATEPORT CITY\n"
	.string "in HOENN!$"

CanalaveCity_Text_SettingSailToVermilion:
	.string "Setting sail for VERMILION CITY\n"
	.string "in KANTO!$"

CanalaveCity_Text_ComeAgain:
	.string "Come see me whenever you want to\nset sail.$"

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

CanalaveCity_EventScript_SailToVirbank::
	msgbox CanalaveCity_Text_SettingSailToVirbank, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_UNOVA_VIRBANK_PORT, 4, 6
	waitstate
	release
	end

CanalaveCity_Text_SettingSailToVirbank:
	.string "Setting sail for VIRBANK CITY\n"
	.string "in UNOVA!$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

CanalaveCity_EventScript_Placa1::
	msgbox CanalaveCity_Text_Placa1, MSGBOX_SIGN
	end

CanalaveCity_Text_Placa1:
	.string "Canalave Library$"

CanalaveCity_EventScript_Placa2::
	msgbox CanalaveCity_Text_Placa2, MSGBOX_SIGN
	end

CanalaveCity_Text_Placa2:
	.string "Canalave City Pokémon Gym\nLeader: Byron\pThe Man with the Steel Body!$"

CanalaveCity_EventScript_Placa3::
	msgbox CanalaveCity_Text_Placa3, MSGBOX_SIGN
	end

CanalaveCity_Text_Placa3:
	.string "Canalave Dock$"

CanalaveCity_EventScript_Placa5::
	msgbox CanalaveCity_Text_Placa5, MSGBOX_SIGN
	end

CanalaveCity_Text_Placa5:
	.string "Sailor Eldritch's House$"

CanalaveCity_EventScript_Placa6::
	msgbox CanalaveCity_Text_Placa6, MSGBOX_SIGN
	end

CanalaveCity_Text_Placa6:
	.string "Harbor Inn\nA Roost for Restless Sailors\p'Enjoy sweet dreams in our\nsumptuous beds!'$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

CanalaveCity_EventScript_Npc1::
	msgbox CanalaveCity_Text_Npc1, MSGBOX_NPC
	end

CanalaveCity_Text_Npc1:
	.string "What's up?\nYour clothes look damp.\pMaybe you took the boat to Iron Island\nto get a Hidden Machine, right?$"

CanalaveCity_EventScript_Npc2::
	msgbox CanalaveCity_Text_Npc2, MSGBOX_NPC
	end

CanalaveCity_Text_Npc2:
	.string "My PSYDUCK is very close to me.\nThat makes its Return move powerful!$"

CanalaveCity_EventScript_Npc3::
	msgbox CanalaveCity_Text_Npc3, MSGBOX_NPC
	end

CanalaveCity_Text_Npc3:
	.string "Welcome to Canalave City, the Canal\nCity!\pIn the old days, this port used to\nbe a hub of cargo transportation.$"

CanalaveCity_EventScript_Npc4::
	msgbox CanalaveCity_Text_Npc4, MSGBOX_NPC
	end

CanalaveCity_Text_Npc4:
	.string "I'm going to study at the library.\pI've taken an interest in the subject\nof time and space.$"

CanalaveCity_EventScript_Npc5::
	msgbox CanalaveCity_Text_Npc5, MSGBOX_NPC
	end

CanalaveCity_Text_Npc5:
	.string "PSYDUCK: Gua?$"

CanalaveCity_EventScript_Npc6::
	msgbox CanalaveCity_Text_Npc6, MSGBOX_NPC
	end

CanalaveCity_Text_Npc6:
	.string "The Gym Leader and Trainers of this Gym\noften go out to Iron Island.\pThey not only train their Pokémon,\nbut they work out as well.$"

CanalaveCity_EventScript_Npc7::
	msgbox CanalaveCity_Text_Npc7, MSGBOX_NPC
	end

CanalaveCity_Text_Npc7:
	.string "Do you wanna set sail?$"

CanalaveCity_EventScript_Placa8::
	msgbox CanalaveCity_Text_Placa8, MSGBOX_SIGN
	end

CanalaveCity_Text_Placa8:
	.string "Canalave City\nCargo Port$"

CanalaveCity_EventScript_Placa9::
	msgbox CanalaveCity_Text_Placa9, MSGBOX_SIGN
	end

CanalaveCity_Text_Placa9:
	.string "The door is tightly shut.\nIt appears impossible to open.$"
