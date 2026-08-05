BlackthornCity_PokemonCenter_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, BlackthornCity_PokemonCenter_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

BlackthornCity_PokemonCenter_OnTransition:
	setrespawn HEAL_LOCATION_BLACKTHORN_CITY
	end

BlackthornCity_PokemonCenter_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_BLACKTHORN_PC_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

BlackthornCity_PokemonCenter_EventScript_Gentleman::
	msgbox BlackthornCity_PokemonCenter_Text_Gentleman, MSGBOX_NPC
	end

BlackthornCity_PokemonCenter_EventScript_Twin::
	msgbox BlackthornCity_PokemonCenter_Text_Twin, MSGBOX_NPC
	end

BlackthornCity_PokemonCenter_Text_Gentleman:
	.string "Deep inside far-off INDIGO\n"
	.string "PLATEAU is the POKéMON LEAGUE.\p"
	.string "I hear the best trainers gather\n"
	.string "there from around the country.$"

BlackthornCity_PokemonCenter_Text_Twin:
	.string "There was this move I just had\n"
	.string "to teach my POKéMON.\p"
	.string "So I got the MOVE DELETER to make\n"
	.string "it forget an HM move.$"
