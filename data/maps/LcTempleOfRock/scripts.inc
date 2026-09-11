@ LcTempleOfRock: mapa copiado de Pokémon Liquid Crystal.gba (g2m32) por
@ dev_scripts/copia_mapa_rom.py. A ARTE e do hack; o JOGO (warps, NPCs,
@ encontros, treinadores, placas) e nosso e entra aqui.

LcTempleOfRock_MapScripts::
	.byte 0

LcTempleOfRock_EventScript_RuinManiacQuarry::
	trainerbattle_single TRAINER_JOHTO_LC_TEMPLE_QUARRY, LcTempleOfRock_Text_QuarrySeen, LcTempleOfRock_Text_QuarryBeaten
	msgbox LcTempleOfRock_Text_QuarryAfter, MSGBOX_AUTOCLOSE
	end

LcTempleOfRock_EventScript_HikerBoulder::
	trainerbattle_single TRAINER_JOHTO_LC_TEMPLE_BOULDER, LcTempleOfRock_Text_BoulderSeen, LcTempleOfRock_Text_BoulderBeaten
	msgbox LcTempleOfRock_Text_BoulderAfter, MSGBOX_AUTOCLOSE
	end

LcTempleOfRock_EventScript_PsychicKeeper::
	trainerbattle_single TRAINER_JOHTO_LC_TEMPLE_KEEPER, LcTempleOfRock_Text_KeeperSeen, LcTempleOfRock_Text_KeeperBeaten
	msgbox LcTempleOfRock_Text_KeeperAfter, MSGBOX_AUTOCLOSE
	end

LcTempleOfRock_EventScript_Caretaker::
	msgbox LcTempleOfRock_Text_Caretaker, MSGBOX_NPC
	end

LcTempleOfRock_EventScript_Scholar::
	msgbox LcTempleOfRock_Text_Scholar, MSGBOX_NPC
	end

LcTempleOfRock_EventScript_SignEntrance::
	msgbox LcTempleOfRock_Text_SignEntrance, MSGBOX_SIGN
	end

LcTempleOfRock_EventScript_SignLowerHall::
	msgbox LcTempleOfRock_Text_SignLowerHall, MSGBOX_SIGN
	end

LcTempleOfRock_EventScript_SignAltar::
	msgbox LcTempleOfRock_Text_SignAltar, MSGBOX_SIGN
	end

LcTempleOfRock_Text_QuarrySeen:
	.string "Every stone in here was cut by\n"
	.string "hand. Show me you respect that!$"

LcTempleOfRock_Text_QuarryBeaten:
	.string "Cracked like soft limestone…$"

LcTempleOfRock_Text_QuarryAfter:
	.string "I've measured every block in this\n"
	.string "TEMPLE. Not one of them is loose.\p"
	.string "Whoever raised it knew stone\n"
	.string "better than we ever will.$"

LcTempleOfRock_Text_BoulderSeen:
	.string "Nobody walks up my corridor\n"
	.string "without a battle!$"

LcTempleOfRock_Text_BoulderBeaten:
	.string "You went straight through me!$"

LcTempleOfRock_Text_BoulderAfter:
	.string "This passage runs from the lower\n"
	.string "hall to the upper one.\p"
	.string "Hikers call it the throat of the\n"
	.string "TEMPLE. One way up, one way down.$"

LcTempleOfRock_Text_KeeperSeen:
	.string "The stones remember. So do I.\n"
	.string "State your business!$"

LcTempleOfRock_Text_KeeperBeaten:
	.string "The altar keeps its silence.$"

LcTempleOfRock_Text_KeeperAfter:
	.string "The rock here is older than the\n"
	.string "DRAGON'S DEN outside.\p"
	.string "My POKéMON were born of it, and\n"
	.string "they answer to it.$"

LcTempleOfRock_Text_Caretaker:
	.string "So the old cave mouth in the\n"
	.string "DRAGON'S DEN is open again.\p"
	.string "Mind your footing, and don't take\n"
	.string "a single stone from the altar.$"

LcTempleOfRock_Text_Scholar:
	.string "Look at the walls: no mortar, no\n"
	.string "seams, no tool marks.\p"
	.string "Some say ONIX carved the halls\n"
	.string "and people only swept them out.$"

LcTempleOfRock_Text_SignEntrance:
	.string "TEMPLE OF ROCK\n"
	.string "Enter quietly. Leave it as you\l"
	.string "found it.$"

LcTempleOfRock_Text_SignLowerHall:
	.string "LOWER HALL\n"
	.string "The stone ring was laid first.\l"
	.string "Everything above rests on it.$"

LcTempleOfRock_Text_SignAltar:
	.string "THE ALTAR\n"
	.string "One block of rock, never cut,\l"
	.string "never moved.$"
