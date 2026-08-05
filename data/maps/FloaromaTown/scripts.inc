@ Floaroma Town. Ver Pokemon Claude/SINNOH-PADRAO.md antes de escrever script novo.
@ Textos vindos de pret/pokeplatinum (sinnoh-dados/floaroma_town.json), em ingles.

FloaromaTown_MapScripts::
	.byte 0

FloaromaTown_EventScript_BreederF::
	lock
	faceplayer
	msgbox FloaromaTown_Text_BreederF, MSGBOX_DEFAULT
	release
	end

FloaromaTown_EventScript_LassWest::
	msgbox FloaromaTown_Text_LassWest, MSGBOX_NPC
	end

FloaromaTown_EventScript_SchoolKid::
	lock
	faceplayer
	msgbox FloaromaTown_Text_SchoolKid, MSGBOX_DEFAULT
	release
	end

FloaromaTown_EventScript_Beauty::
	lock
	faceplayer
	msgbox FloaromaTown_Text_Beauty, MSGBOX_DEFAULT
	release
	end

FloaromaTown_EventScript_LassEast::
	msgbox FloaromaTown_Text_LassEast, MSGBOX_NPC
	end

FloaromaTown_EventScript_Grunt::
	lock
	faceplayer
	msgbox FloaromaTown_Text_Grunt, MSGBOX_DEFAULT
	release
	end

FloaromaTown_EventScript_Camper::
	msgbox FloaromaTown_Text_Camper, MSGBOX_NPC
	end

FloaromaTown_EventScript_TownSign::
	msgbox FloaromaTown_Text_TownSign, MSGBOX_SIGN
	end

FloaromaTown_Text_BreederF:
	.string "The flowers all around town make\n"
	.string "for a great place to raise POKéMON.$"

FloaromaTown_Text_LassWest:
	.string "Being surrounded by flowers puts me\n"
	.string "in an oddly pleasant mood.$"

FloaromaTown_Text_SchoolKid:
	.string "I wanted to get some flowers from\n"
	.string "the FLOAROMA MEADOW...\p"
	.string "But some Team Galactic guys in\n"
	.string "snazzy outfits came along and went\l"
	.string "into the meadow past these flowers.$"

FloaromaTown_Text_Beauty:
	.string "Do you know about Gracidea flowers?\p"
	.string "They're given as bouquets to express\n"
	.string "feelings of gratitude. It's an\l"
	.string "enduring tradition around these parts.$"

FloaromaTown_Text_LassEast:
	.string "This town smells like flowers no\n"
	.string "matter which way the wind blows.$"

FloaromaTown_Text_Grunt:
	.string "Aren't we TEAM GALACTIC? And we're\n"
	.string "assigned here?\p"
	.string "Standing around among flowers...\n"
	.string "this doesn't seem all that cool.$"

FloaromaTown_Text_Camper:
	.string "I pitched my tent here just to wake\n"
	.string "up smelling all these flowers.$"

FloaromaTown_Text_TownSign:
	.string "FLOAROMA TOWN\n"
	.string "A Sea of Flowers$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

FloaromaTown_EventScript_Placa2::
	msgbox FloaromaTown_Text_Placa2, MSGBOX_SIGN
	end

FloaromaTown_Text_Placa2:
	.string "Pick a Peck of Colors Flower Shop\nFree Berries Available$"

FloaromaTown_EventScript_Placa3::
	msgbox FloaromaTown_Text_Placa3, MSGBOX_SIGN
	end

FloaromaTown_Text_Placa3:
	.string "Floaroma Meadow Ahead\nHoney Available$"
