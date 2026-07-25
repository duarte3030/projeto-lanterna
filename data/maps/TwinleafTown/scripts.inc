@ Mapa de referencia de Sinnoh. O padrao usado aqui vale para os outros 132:
@ ver Pokemon Claude/SINNOH-PADRAO.md antes de escrever qualquer script novo.
@ Textos vindos de pret/pokeplatinum, em ingles, como o resto do jogo.

TwinleafTown_MapScripts::
	.byte 0

TwinleafTown_EventScript_Breeder::
	msgbox TwinleafTown_Text_Breeder, MSGBOX_NPC
	end

TwinleafTown_EventScript_Guitarist::
	lock
	faceplayer
	msgbox TwinleafTown_Text_Guitarist, MSGBOX_DEFAULT
	release
	end

TwinleafTown_EventScript_Rival::
	lock
	faceplayer
	msgbox TwinleafTown_Text_Rival, MSGBOX_DEFAULT
	release
	end

TwinleafTown_EventScript_Collector::
	msgbox TwinleafTown_Text_Collector, MSGBOX_NPC
	end

TwinleafTown_EventScript_TownSign::
	msgbox TwinleafTown_Text_TownSign, MSGBOX_SIGN
	end

TwinleafTown_Text_Breeder:
	.string "It's true that wild POKéMON attack\n"
	.string "people sometimes...\p"
	.string "But POKéMON also open their hearts\n"
	.string "to you, so you can become friends.$"

TwinleafTown_Text_Guitarist:
	.string "Everyone goes off on adventures,\n"
	.string "and then they gradually grow up...$"

TwinleafTown_Text_Rival:
	.string "You're finally up!\p"
	.string "Come on, we're going to see the\n"
	.string "PROFESSOR. Try to keep up!$"

TwinleafTown_Text_Collector:
	.string "This town is small, but the air here\n"
	.string "is the freshest in all of SINNOH.$"

TwinleafTown_Text_TownSign:
	.string "TWINLEAF TOWN\n"
	.string "A Town Whose Leaves Are Always Fresh$"
