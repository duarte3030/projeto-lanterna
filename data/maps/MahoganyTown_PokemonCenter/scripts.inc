MahoganyTown_PokemonCenter_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MahoganyTown_PokemonCenter_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

MahoganyTown_PokemonCenter_OnTransition:
	setrespawn HEAL_LOCATION_MAHOGANY_TOWN
	end

MahoganyTown_PokemonCenter_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_MAHOGANY_PC_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

MahoganyTown_PokemonCenter_EventScript_Hiker::
	msgbox MahoganyTown_PokemonCenter_Text_Hiker, MSGBOX_NPC
	end

MahoganyTown_PokemonCenter_EventScript_Boy::
	msgbox MahoganyTown_PokemonCenter_Text_Boy, MSGBOX_NPC
	end

MahoganyTown_PokemonCenter_EventScript_Girl::
	msgbox MahoganyTown_PokemonCenter_Text_Girl, MSGBOX_NPC
	end

MahoganyTown_PokemonCenter_Text_Hiker:
	.string "What's this? TEAM ROCKET has come\n"
	.string "back?\p"
	.string "I saw some men in black at LAKE OF\n"
	.string "RAGE…$"

MahoganyTown_PokemonCenter_Text_Boy:
	.string "I stop my POKéMON from evolving too\n"
	.string "early.\p"
	.string "I make them learn certain moves\n"
	.string "before I let them evolve.$"

MahoganyTown_PokemonCenter_Text_Girl:
	.string "POKéMON do become stronger when they\n"
	.string "evolve,\p"
	.string "but they also learn moves more\n"
	.string "slowly.$"
