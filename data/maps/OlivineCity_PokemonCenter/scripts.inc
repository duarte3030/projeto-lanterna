OlivineCity_PokemonCenter_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, OlivineCity_PokemonCenter_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

OlivineCity_PokemonCenter_OnTransition:
	setrespawn HEAL_LOCATION_OLIVINE_CITY
	end

OlivineCity_PokemonCenter_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_OLIVINE_PC_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

OlivineCity_PokemonCenter_EventScript_Fisher::
	lock
	faceplayer
	msgbox OlivineCity_PokemonCenter_Text_Fisher, MSGBOX_DEFAULT
	closemessage
	release
	end

OlivineCity_PokemonCenter_EventScript_Teacher::
	lock
	faceplayer
	msgbox OlivineCity_PokemonCenter_Text_Teacher, MSGBOX_DEFAULT
	closemessage
	release
	end

OlivineCity_PokemonCenter_Text_Fisher:
	.string "The SAILOR in the OLIVINE CAFE\n"
	.string "next door is really generous.\p"
	.string "He taught my POKéMON STRENGTH.\p"
	.string "Now it can move big boulders\n"
	.string "without breaking a sweat.$"

OlivineCity_PokemonCenter_Text_Teacher:
	.string "There's a person in CIANWOOD\n"
	.string "CITY across the sea.\p"
	.string "I heard him bragging about his\n"
	.string "rare POKéMON all the time.$"
