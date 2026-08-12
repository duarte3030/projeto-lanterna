SandgemTown_PokemonCenter_2F_MapScripts::
	.byte 0

SandgemTown_PokemonCenter_2F_EventScript_Teala1::
	msgbox SandgemTown_PokemonCenter_2F_Text_Teala1, MSGBOX_NPC
	end

SandgemTown_PokemonCenter_2F_EventScript_Teala2::
	msgbox SandgemTown_PokemonCenter_2F_Text_Teala2, MSGBOX_NPC
	end

SandgemTown_PokemonCenter_2F_Text_Teala1:
	.string "This terminal connects TRAINERS\n"
	.string "all over SINNOH.$"

SandgemTown_PokemonCenter_2F_Text_Teala2:
	.string "Feel free to use the terminal to\n"
	.string "trade with other TRAINERS.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SandgemTown_PokemonCenter_2F_EventScript_Npc1::
	msgbox SandgemTown_PokemonCenter_2F_Text_Npc1, MSGBOX_NPC
	end

SandgemTown_PokemonCenter_2F_Text_Npc1:
	.string "What kind of Trainer's sign will get\npeople laughing?$"
