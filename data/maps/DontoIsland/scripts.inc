@ DontoIsland: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 27.113) por dev_scripts/copia_planta_ex.py.

DontoIsland_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 27.113), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
DontoIsland_EventScript_ExTrainer2::
	trainerbattle_single TRAINER_HOENNEX_DONTO_ISLAND_JOAN, DontoIsland_Text_ExTrainer2Intro, DontoIsland_Text_ExTrainer2Defeat
	msgbox DontoIsland_Text_ExTrainer2PostBattle, MSGBOX_AUTOCLOSE
	end

DontoIsland_Text_ExTrainer2Intro:
	.string "What makes a DRAGON a DRAGON?$"

DontoIsland_Text_ExTrainer2Defeat:
	.string "Zip it kid.$"

DontoIsland_Text_ExTrainer2PostBattle:
	.string "Is a DONPHAN a dragon?$"

DontoIsland_EventScript_ExTrainer3::
	trainerbattle_single TRAINER_HOENNEX_DONTO_ISLAND_PRICE, DontoIsland_Text_ExTrainer3Intro, DontoIsland_Text_ExTrainer3Defeat
	msgbox DontoIsland_Text_ExTrainer3PostBattle, MSGBOX_AUTOCLOSE
	end

DontoIsland_Text_ExTrainer3Intro:
	.string "I can’t find anything on this island!$"

DontoIsland_Text_ExTrainer3Defeat:
	.string "Now I can’t win a battle...$"

DontoIsland_Text_ExTrainer3PostBattle:
	.string "I’ve heard there are ruins on this\n"
	.string "island, but I can’t find anything.$"

DontoIsland_EventScript_ExTrainer4::
	trainerbattle_single TRAINER_HOENNEX_DONTO_ISLAND_DARRIUS, DontoIsland_Text_ExTrainer4Intro, DontoIsland_Text_ExTrainer4Defeat
	msgbox DontoIsland_Text_ExTrainer4PostBattle, MSGBOX_AUTOCLOSE
	end

DontoIsland_Text_ExTrainer4Intro:
	.string "Ahoy! What an island this is!$"

DontoIsland_Text_ExTrainer4Defeat:
	.string "Yo, ho ho!$"

DontoIsland_Text_ExTrainer4PostBattle:
	.string "Say, how do I get off this island?$"

DontoIsland_EventScript_ExTrainer5::
	trainerbattle_single TRAINER_HOENNEX_DONTO_ISLAND_SETH, DontoIsland_Text_ExTrainer5Intro, DontoIsland_Text_ExTrainer5Defeat
	msgbox DontoIsland_Text_ExTrainer5PostBattle, MSGBOX_AUTOCLOSE
	end

DontoIsland_Text_ExTrainer5Intro:
	.string "There’s signs of relics nearby.$"

DontoIsland_Text_ExTrainer5Defeat:
	.string "I must find the secret’s of this island!$"

DontoIsland_Text_ExTrainer5PostBattle:
	.string "Somewhere is something strange on this\n"
	.string "island.$"

DontoIsland_EventScript_ExTrainer6::
	trainerbattle_single TRAINER_HOENNEX_DONTO_ISLAND_MARIUS, DontoIsland_Text_ExTrainer6Intro, DontoIsland_Text_ExTrainer6Defeat
	msgbox DontoIsland_Text_ExTrainer6PostBattle, MSGBOX_AUTOCLOSE
	end

DontoIsland_Text_ExTrainer6Intro:
	.string "From the skies my POKéMON attack!$"

DontoIsland_Text_ExTrainer6Defeat:
	.string "You beat our best!$"

DontoIsland_Text_ExTrainer6PostBattle:
	.string "Where do your POKéMON come from?$"

DontoIsland_EventScript_ExTrainer7::
	trainerbattle_single TRAINER_HOENNEX_DONTO_ISLAND_RAYMOND, DontoIsland_Text_ExTrainer7Intro, DontoIsland_Text_ExTrainer7Defeat
	msgbox DontoIsland_Text_ExTrainer7PostBattle, MSGBOX_AUTOCLOSE
	end

DontoIsland_Text_ExTrainer7Intro:
	.string "Welcome to Donto Island punk.\n"
	.string "Prepare to feel my wrath!$"

DontoIsland_Text_ExTrainer7Defeat:
	.string "You cheated somehow!$"

DontoIsland_Text_ExTrainer7PostBattle:
	.string "I left TEAM AQUA.\n"
	.string "They had nothing for me.\p"
	.string "I’m going to lay low here till things cool\n"
	.string "down out there.$"

DontoIsland_EventScript_ExSign0::
	msgbox DontoIsland_Text_ExSign0, MSGBOX_SIGN
	end

DontoIsland_Text_ExSign0:
	.string "DONTO ISLAND$"

