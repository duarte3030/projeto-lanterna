CherrygroveCity_PokemonCenter_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, CherrygroveCity_PokemonCenter_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

CherrygroveCity_PokemonCenter_OnTransition:
	setrespawn HEAL_LOCATION_CHERRYGROVE_CITY
	end

CherrygroveCity_PokemonCenter_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_CHERRYGROVE_PC_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

CherrygroveCity_PokemonCenter_EventScript_Lass::
	lock
	faceplayer
	msgbox CherrygroveCity_PokemonCenter_Text_Lass, MSGBOX_DEFAULT
	closemessage
	release
	end

CherrygroveCity_PokemonCenter_EventScript_Fisher::
	lock
	faceplayer
	msgbox CherrygroveCity_PokemonCenter_Text_Fisher, MSGBOX_DEFAULT
	closemessage
	release
	end

CherrygroveCity_PokemonCenter_EventScript_Gentleman::
	lock
	faceplayer
	msgbox CherrygroveCity_PokemonCenter_Text_Gentleman, MSGBOX_DEFAULT
	closemessage
	release
	end

CherrygroveCity_PokemonCenter_Text_Lass:
	.string "They say a watched pot never\n"
	.string "boils. But watching the clock\l"
	.string "in the POKéCENTER makes time fly!$"

CherrygroveCity_PokemonCenter_Text_Fisher:
	.string "It's great. I can store any number\n"
	.string "of POKéMON, and it's all free.$"

CherrygroveCity_PokemonCenter_Text_Gentleman:
	.string "That PC is free for any\n"
	.string "trainer to use.$"
