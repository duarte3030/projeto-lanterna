@ LcNewIslandHall: mapa copiado de Pokémon Liquid Crystal.gba (g4m31) por
@ dev_scripts/copia_mapa_rom.py. A ARTE e do hack; o JOGO e nosso.

LcNewIslandHall_MapScripts::
	.byte 0

LcNewIslandHall_EventScript_West::
	trainerbattle_single TRAINER_KANTO_LC_NEW_ISLAND_WEST, LcNewIslandHall_Text_WestSeen, LcNewIslandHall_Text_WestBeaten
	msgbox LcNewIslandHall_Text_WestAfter, MSGBOX_AUTOCLOSE
	end

LcNewIslandHall_EventScript_East::
	trainerbattle_single TRAINER_KANTO_LC_NEW_ISLAND_EAST, LcNewIslandHall_Text_EastSeen, LcNewIslandHall_Text_EastBeaten
	msgbox LcNewIslandHall_Text_EastAfter, MSGBOX_AUTOCLOSE
	end

LcNewIslandHall_EventScript_South::
	trainerbattle_single TRAINER_KANTO_LC_NEW_ISLAND_SOUTH, LcNewIslandHall_Text_SouthSeen, LcNewIslandHall_Text_SouthBeaten
	msgbox LcNewIslandHall_Text_SouthAfter, MSGBOX_AUTOCLOSE
	end

LcNewIslandHall_EventScript_Core::
	trainerbattle_single TRAINER_KANTO_LC_NEW_ISLAND_CORE, LcNewIslandHall_Text_CoreSeen, LcNewIslandHall_Text_CoreBeaten
	msgbox LcNewIslandHall_Text_CoreAfter, MSGBOX_AUTOCLOSE
	end

LcNewIslandHall_EventScript_Steward::
	msgbox LcNewIslandHall_Text_Steward, MSGBOX_NPC
	end

LcNewIslandHall_EventScript_SignHall::
	msgbox LcNewIslandHall_Text_SignHall, MSGBOX_SIGN
	end

LcNewIslandHall_Text_WestSeen:
	.string "The west wing is mine until\n"
	.string "somebody takes it!$"

LcNewIslandHall_Text_WestBeaten:
	.string "Then take it.$"

LcNewIslandHall_Text_WestAfter:
	.string "Every door in this hall opens\n"
	.string "onto the island, not onto the\l"
	.string "next room.\p"
	.string "You leave to go deeper. That is\n"
	.string "the joke of the place.$"

LcNewIslandHall_Text_EastSeen:
	.string "Nobody invited you to the east\n"
	.string "wing. Nobody invited me either!$"

LcNewIslandHall_Text_EastBeaten:
	.string "Fair is fair.$"

LcNewIslandHall_Text_EastAfter:
	.string "The stairs at the far end go up\n"
	.string "to the east terrace.\p"
	.string "From there you can see the whole\n"
	.string "roof, and it is all one building.$"

LcNewIslandHall_Text_SouthSeen:
	.string "You made it past the south\n"
	.string "corridor? Then battle me!$"

LcNewIslandHall_Text_SouthBeaten:
	.string "Strong. Very strong.$"

LcNewIslandHall_Text_SouthAfter:
	.string "I train here because nothing\n"
	.string "here is easy, not even walking.$"

LcNewIslandHall_Text_CoreSeen:
	.string "This is the middle of the house.\n"
	.string "Earn it!$"

LcNewIslandHall_Text_CoreBeaten:
	.string "Earned.$"

LcNewIslandHall_Text_CoreAfter:
	.string "There is a room under the east\n"
	.string "terrace that nobody uses.\p"
	.string "The ladder in it goes down to\n"
	.string "the inner court.$"

LcNewIslandHall_Text_Steward:
	.string "Welcome to the hall. Please do\n"
	.string "not touch the instruments.\p"
	.string "The guests have all gone out\n"
	.string "onto the island. They always do.$"

LcNewIslandHall_Text_SignHall:
	.string "GREAT HALL\n"
	.string "Each door leads back outside.\l"
	.string "Count them before you wander.$"
