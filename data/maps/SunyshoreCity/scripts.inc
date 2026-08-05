SunyshoreCity_MapScripts::
	.byte 0

SunyshoreCity_EventScript_Jasmine::
	lock
	faceplayer
	msgbox SunyshoreCity_Text_Jasmine, MSGBOX_DEFAULT
	release
	end

SunyshoreCity_EventScript_Sailor1::
	msgbox SunyshoreCity_Text_Sailor1, MSGBOX_NPC
	end

SunyshoreCity_EventScript_PokefanF::
	msgbox SunyshoreCity_Text_PokefanF, MSGBOX_NPC
	end

SunyshoreCity_EventScript_BreederF::
	msgbox SunyshoreCity_Text_BreederF, MSGBOX_NPC
	end

SunyshoreCity_EventScript_Worker::
	msgbox SunyshoreCity_Text_Worker, MSGBOX_NPC
	end

SunyshoreCity_EventScript_Sailor2::
	msgbox SunyshoreCity_Text_Sailor2, MSGBOX_NPC
	end

SunyshoreCity_Text_Jasmine:
	.string "...This city makes me feel at\n"
	.string "home somehow.\p"
	.string "It's next to the sea, and there's\n"
	.string "a lighthouse...$"

SunyshoreCity_Text_Sailor1:
	.string "The sea breeze here is the best\n"
	.string "in all of SINNOH.$"

SunyshoreCity_Text_PokefanF:
	.string "I love this city. The lighthouse\n"
	.string "lights up so pretty at night.$"

SunyshoreCity_Text_BreederF:
	.string "My POKéMON love the salty air\n"
	.string "here. It's good for their coats.$"

SunyshoreCity_Text_Worker:
	.string "We're always fixing something\n"
	.string "around this city. Never a dull day.$"

SunyshoreCity_Text_Sailor2:
	.string "Ships come and go from SUNYSHORE\n"
	.string "all day long.$"

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
