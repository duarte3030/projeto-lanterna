@ Floaroma Town. Ver Pokemon Claude/SINNOH-PADRAO.md antes de escrever script novo.
@ Textos vindos de pret/pokeplatinum (sinnoh-dados/floaroma_town.json), em ingles.

FloaromaTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, FloaromaTown_OnTransition
	.byte 0

@ ponytail: a cena e a flag sao a mesma coisa. Os dois grunts entediados
@ (LOCALID_GRUNT_M_WEST/EAST na fonte, hidden_flag FLAG_HIDE_FLOAROMA_TOWN_GRUNTS)
@ nascem enquanto a Mars nao caiu na usina, e somem depois; mesma
@ FLAG_GALACTICA_WINDWORKS que a Valley Windworks ja usa, porque e o mesmo
@ marco (Floaroma fica no caminho da usina). Zero var.
FloaromaTown_OnTransition:
	call_if_defeated TRAINER_SINNOH_COMMANDER_MARS_VALLEY_WINDWORKS, FloaromaTown_EventScript_HideGalactica_windworks
	end

FloaromaTown_EventScript_HideGalactica_windworks::
	setflag FLAG_GALACTICA_WINDWORKS
	return

FloaromaTown_EventScript_Grunt::
	lock
	faceplayer
	msgbox FloaromaTown_Text_Grunt, MSGBOX_DEFAULT
	release
	end

FloaromaTown_EventScript_TownSign::
	msgbox FloaromaTown_Text_TownSign, MSGBOX_SIGN
	end

FloaromaTown_Text_Grunt:
	.string "Aren't we TEAM GALACTIC? And we're\n"
	.string "assigned here?\p"
	.string "Standing around among flowers...\n"
	.string "this doesn't seem all that cool.$"

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

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

FloaromaTown_EventScript_Npc1::
	msgbox FloaromaTown_Text_Npc1, MSGBOX_NPC
	end

FloaromaTown_Text_Npc1:
	.string "Welcome to Floaroma, the town of\nflowers, flowers, and more flowers!\pYou should plant some flowers of\nyour own, too. Yay for flowers!$"

FloaromaTown_EventScript_Npc2::
	msgbox FloaromaTown_Text_Npc2, MSGBOX_NPC
	end

FloaromaTown_Text_Npc2:
	.string "I simply love it here...\nThe atmosphere is so uplifting.\pYou came to get emotionally healed\ntoo, didn't you?$"

FloaromaTown_EventScript_Npc3::
	msgbox FloaromaTown_Text_Npc3, MSGBOX_NPC
	end

FloaromaTown_Text_Npc3:
	.string "I wanted to get some flowers from\nthe Floaroma Meadow...\pBut some Team Galactic guys in snazzy\noutfits came along...$"

FloaromaTown_EventScript_Npc4::
	msgbox FloaromaTown_Text_Npc4, MSGBOX_NPC
	end

FloaromaTown_Text_Npc4:
	.string "Oh, a SHAYMIN?\pIf you have that Pokémon, then you\nalso should have some Gracidea flowers.\pI've got a whole bunch, so you can have\nsome.$"

FloaromaTown_EventScript_Npc5::
	msgbox FloaromaTown_Text_Npc5, MSGBOX_NPC
	end

FloaromaTown_Text_Npc5:
	.string "The Berries you pick can be used as\nfood for Pokémon.\pYou can also trade them in at the\nflorist's.\pThey'll exchange Berries for\nAccessories to dress up your Pokémon.$"

FloaromaTown_EventScript_Npc6::
	msgbox FloaromaTown_Text_Npc6, MSGBOX_NPC
	end

FloaromaTown_Text_Npc6:
	.string "I got drawn here by the sweet scent\nof Honey...\pSeriously, what's that? What am I?\nA Pokémon or something? Mmm... Honey.$"

FloaromaTown_EventScript_Placa7::
	msgbox FloaromaTown_Text_Placa7, MSGBOX_SIGN
	end

FloaromaTown_Text_Placa7:
	.string "Floaroma Town\nVivid & Scented$"
