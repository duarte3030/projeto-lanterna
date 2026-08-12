@ Textos vindos de pret/pokeplatinum (res/text/solaceon_town.json), em ingles.
@ Ver Pokemon Claude/SINNOH-PADRAO.md antes de mexer.

SolaceonTown_MapScripts::
	.byte 0

SolaceonTown_EventScript_DayCareMan::
	msgbox SolaceonTown_Text_DayCareMan, MSGBOX_NPC
	end

SolaceonTown_EventScript_DayCareSign::
	msgbox SolaceonTown_Text_DayCareSign, MSGBOX_SIGN
	end

SolaceonTown_EventScript_NewsPressSign::
	msgbox SolaceonTown_Text_NewsPressSign, MSGBOX_SIGN
	end

SolaceonTown_Text_DayCareMan:
	.string "My wife and I look after POKéMON\n"
	.string "here at the DAY-CARE.\p"
	.string "Leave a POKéMON with us, and we'll\n"
	.string "raise it while you're off training.$"

SolaceonTown_Text_DayCareSign:
	.string "POKéMON DAY CARE\p"
	.string "Leave your POKéMON here and we'll\n"
	.string "raise it for you.$"

SolaceonTown_Text_NewsPressSign:
	.string "SOLACEON TOWN POKéMON NEWS PRESS$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

SolaceonTown_EventScript_Placa2::
	msgbox SolaceonTown_Text_Placa2, MSGBOX_SIGN
	end

SolaceonTown_Text_Placa2:
	.string "Pokémon Day Care\nLet Us Raise Your Pokémon$"

SolaceonTown_EventScript_Placa3::
	msgbox SolaceonTown_Text_Placa3, MSGBOX_SIGN
	end

SolaceonTown_Text_Placa3:
	.string "Pokémon News Press\nWanted: Pro Pokémon Catcher!$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SolaceonTown_EventScript_Npc1::
	msgbox SolaceonTown_Text_Npc1, MSGBOX_NPC
	end

SolaceonTown_Text_Npc1:
	.string "Howdy, traveling Trainer.\nTake it easy, slow, and casual.$"

SolaceonTown_EventScript_Npc2::
	msgbox SolaceonTown_Text_Npc2, MSGBOX_NPC
	end

SolaceonTown_Text_Npc2:
	.string "I'm too little, so I don't know\nhow to battle very good.\pThe nice Day-Care Lady is raising\nmy Pokémon for me.$"

SolaceonTown_EventScript_Npc3::
	msgbox SolaceonTown_Text_Npc3, MSGBOX_NPC
	end

SolaceonTown_Text_Npc3:
	.string "Breathing in this refreshing air...\nIt perks up Pokémon, don't you think?$"

SolaceonTown_EventScript_Npc4::
	msgbox SolaceonTown_Text_Npc4, MSGBOX_NPC
	end

SolaceonTown_Text_Npc4:
	.string "Every Sunday, I visit the Lost\nTower...$"

SolaceonTown_EventScript_Npc5::
	msgbox SolaceonTown_Text_Npc5, MSGBOX_NPC
	end

SolaceonTown_Text_Npc5:
	.string "Your encounters with Pokémon can\nbe considered your shared history.\pThis here's a Pokétch app called\nPokémon History.\pUse it to see your history of\nPokémon catches.$"

SolaceonTown_EventScript_Npc6::
	msgbox SolaceonTown_Text_Npc6, MSGBOX_NPC
	end

SolaceonTown_Text_Npc6:
	.string "There used to be nothing here but\na road that went straight through.\pOver time, Pokémon and people just\ngathered, and the town came to be.$"

SolaceonTown_EventScript_Placa7::
	msgbox SolaceonTown_Text_Placa7, MSGBOX_SIGN
	end

SolaceonTown_Text_Placa7:
	.string "Solaceon Town\nFree of Worry!$"
