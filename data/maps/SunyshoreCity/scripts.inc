SunyshoreCity_MapScripts::
	.byte 0

SunyshoreCity_EventScript_Jasmine::
	lock
	faceplayer
	msgbox SunyshoreCity_Text_Jasmine, MSGBOX_DEFAULT
	release
	end

SunyshoreCity_EventScript_BreederF::
	msgbox SunyshoreCity_Text_BreederF, MSGBOX_NPC
	end

SunyshoreCity_Text_Jasmine:
	.string "...This city makes me feel at\n"
	.string "home somehow.\p"
	.string "It's next to the sea, and there's\n"
	.string "a lighthouse...$"

SunyshoreCity_Text_BreederF:
	.string "My POKéMON love the salty air\n"
	.string "here. It's good for their coats.$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

SunyshoreCity_EventScript_Placa1::
	msgbox SunyshoreCity_Text_Placa1, MSGBOX_SIGN
	end

SunyshoreCity_Text_Placa1:
	.string "Sunyshore Market\nA Selection of the World's Seals$"

SunyshoreCity_EventScript_Placa3::
	msgbox SunyshoreCity_Text_Placa3, MSGBOX_SIGN
	end

SunyshoreCity_Text_Placa3:
	.string "Sunyshore City Pokémon Gym\nLeader: Volkner\pThe Shining, Shocking Star$"

SunyshoreCity_EventScript_Placa4::
	msgbox SunyshoreCity_Text_Placa4, MSGBOX_SIGN
	end

SunyshoreCity_Text_Placa4:
	.string "Vista Lighthouse\nThe Beacon That Lights Sinnoh$"

SunyshoreCity_EventScript_Placa5::
	msgbox SunyshoreCity_Text_Placa5, MSGBOX_SIGN
	end

SunyshoreCity_Text_Placa5:
	.string "Julia's House\nDelightful Ribbons for Pokémon$"

SunyshoreCity_EventScript_Placa6::
	msgbox SunyshoreCity_Text_Placa6, MSGBOX_SIGN
	end

SunyshoreCity_Text_Placa6:
	.string "Pokémon Rock\nSunyshore's Heritage Site$"

SunyshoreCity_EventScript_Placa7::
	msgbox SunyshoreCity_Text_Placa7, MSGBOX_SIGN
	end

SunyshoreCity_Text_Placa7:
	.string "It's a blank sign painted white.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SunyshoreCity_EventScript_Npc1::
	msgbox SunyshoreCity_Text_Npc1, MSGBOX_NPC
	end

SunyshoreCity_Text_Npc1:
	.string "That giant rock...\nIsn't it really a Pokémon?$"

SunyshoreCity_EventScript_Npc2::
	msgbox SunyshoreCity_Text_Npc2, MSGBOX_NPC
	end

SunyshoreCity_Text_Npc2:
	.string "The city uses a lot of electricity,\nespecially the lighthouse and the Gym.\pThey finally decided to turn all the\ncity's roads into giant solar panels.\pSunyshore is the Sunshine City, so\nthe system works perfectly.$"

SunyshoreCity_EventScript_Npc3::
	msgbox SunyshoreCity_Text_Npc3, MSGBOX_NPC
	end

SunyshoreCity_Text_Npc3:
	.string "This is a major port town.\nAnd...\pIt's the gateway to the Pokémon\nLeague.$"

SunyshoreCity_EventScript_Npc4::
	msgbox SunyshoreCity_Text_Npc4, MSGBOX_NPC
	end

SunyshoreCity_Text_Npc4:
	.string "The Gym Leader uses too much\nelectricity!\pHe needs to think about the city's\npower needs, too!$"

SunyshoreCity_EventScript_Npc5::
	msgbox SunyshoreCity_Text_Npc5, MSGBOX_NPC
	end

SunyshoreCity_Text_Npc5:
	.string "Whatever the environment, people\nand Pokémon adapt to live there.\pThat's what we all do to survive.$"

SunyshoreCity_EventScript_Placa2::
	msgbox SunyshoreCity_Text_Placa2, MSGBOX_SIGN
	end

SunyshoreCity_Text_Placa2:
	.string "Sunyshore City\nSolar Powered!$"
