VioletCity_PokemonCenter_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, VioletCity_PokemonCenter_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

VioletCity_PokemonCenter_OnTransition:
	setrespawn HEAL_LOCATION_VIOLET_CITY
	end

VioletCity_PokemonCenter_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_VIOLET_PC_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

VioletCity_PokemonCenter_EventScript_Gentleman::
	lock
	faceplayer
	msgbox VioletCity_PokemonCenter_Text_Gentleman, MSGBOX_DEFAULT
	closemessage
	release
	end

VioletCity_PokemonCenter_EventScript_Man::
	lock
	faceplayer
	msgbox VioletCity_PokemonCenter_Text_Man, MSGBOX_DEFAULT
	closemessage
	release
	end

VioletCity_PokemonCenter_EventScript_Kid::
	lock
	faceplayer
	msgbox VioletCity_PokemonCenter_Text_Kid, MSGBOX_DEFAULT
	closemessage
	release
	end

VioletCity_PokemonCenter_EventScript_Bookwoman::
	lock
	faceplayer
	msgbox VioletCity_PokemonCenter_Text_Bookwoman, MSGBOX_DEFAULT
	closemessage
	release
	end

VioletCity_PokemonCenter_Text_Gentleman:
	.string "It was around three years ago.\p"
	.string "TEAM ROCKET was up to no good\n"
	.string "with POKéMON.\p"
	.string "But justice prevailed--a young\n"
	.string "kid broke 'em up.$"

VioletCity_PokemonCenter_Text_Man:
	.string "POKéMON are smart. They won't\n"
	.string "obey a trainer they don't respect.\p"
	.string "Without the right GYM BADGES,\n"
	.string "they will just do as they please.$"

VioletCity_PokemonCenter_Text_Kid:
	.string "A guy named BILL made the\n"
	.string "POKéMON PC storage system.$"

VioletCity_PokemonCenter_Text_Bookwoman:
	.string "While my POKéMON are recovering\n"
	.string "I love to read a good book.$"
