SandgemTown_PokemonCenter_1F_MapScripts::
	.byte 0

SandgemTown_PokemonCenter_1F_EventScript_Nurse::
	lock
	faceplayer
	msgbox SandgemTown_PokemonCenter_1F_Text_Nurse, MSGBOX_DEFAULT
	release
	end

SandgemTown_PokemonCenter_1F_EventScript_Expert::
	msgbox SandgemTown_PokemonCenter_1F_Text_Expert, MSGBOX_NPC
	end

SandgemTown_PokemonCenter_1F_EventScript_Lass::
	msgbox SandgemTown_PokemonCenter_1F_Text_Lass, MSGBOX_NPC
	end

SandgemTown_PokemonCenter_1F_Text_Nurse:
	.string "Welcome to the SANDGEM TOWN\n"
	.string "POKéMON CENTER!\p"
	.string "We hope your POKéMON are doing\n"
	.string "well today.$"

SandgemTown_PokemonCenter_1F_Text_Expert:
	.string "I've heard the professor here studies\n"
	.string "POKéMON habitats. Fascinating work.$"

SandgemTown_PokemonCenter_1F_Text_Lass:
	.string "I always stop here before heading\n"
	.string "out on ROUTE 202.$"
