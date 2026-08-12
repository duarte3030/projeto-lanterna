SandgemTown_PokemonCenter_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SandgemTown_PokemonCenter_1F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

SandgemTown_PokemonCenter_1F_OnTransition:
	setrespawn HEAL_LOCATION_SANDGEM_TOWN
	end

SandgemTown_PokemonCenter_1F_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_SANDGEM_POKECENTER1F_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

SandgemTown_PokemonCenter_1F_Text_Nurse:
	.string "Welcome to the SANDGEM TOWN\n"
	.string "POKéMON CENTER!\p"
	.string "We hope your POKéMON are doing\n"
	.string "well today.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SandgemTown_PokemonCenter_1F_EventScript_Npc1::
	msgbox SandgemTown_PokemonCenter_1F_Text_Npc1, MSGBOX_NPC
	end

SandgemTown_PokemonCenter_1F_Text_Npc1:
	.string "Talk to that nice lady at the counter\nand hand her your Pokémon.\pShe'll heal your Pokémon to perfect\nhealth in no time at all!$"

SandgemTown_PokemonCenter_1F_EventScript_Npc2::
	msgbox SandgemTown_PokemonCenter_1F_Text_Npc2, MSGBOX_NPC
	end

SandgemTown_PokemonCenter_1F_Text_Npc2:
	.string "Do you see that PC over there?\nThat fancy blue one?\pIf you've got Pokémon with you,\nit's free to use.$"

SandgemTown_PokemonCenter_1F_EventScript_Npc3::
	msgbox SandgemTown_PokemonCenter_1F_Text_Npc3, MSGBOX_NPC
	end

SandgemTown_PokemonCenter_1F_Text_Npc3:
	.string "The top floor of any Pokémon Center\nis the Pokémon Communication Club.\pThere, you can have all sorts of fun\nwith your friends.$"
