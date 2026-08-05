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
