OreburghCity_PokemonCenter_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, OreburghCity_PokemonCenter_1F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

OreburghCity_PokemonCenter_1F_OnTransition:
	setrespawn HEAL_LOCATION_OREBURGH_CITY
	end

OreburghCity_PokemonCenter_1F_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_OREBURGH_PC1_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

OreburghCity_PokemonCenter_1F_EventScript_AceTrainer::
	msgbox OreburghCity_PokemonCenter_1F_Text_AceTrainer, MSGBOX_NPC
	end

OreburghCity_PokemonCenter_1F_EventScript_Gentleman::
	lock
	faceplayer
	msgbox OreburghCity_PokemonCenter_1F_Text_Gentleman, MSGBOX_DEFAULT
	release
	end

OreburghCity_PokemonCenter_1F_Text_Nurse:
	.string "Welcome to the POKéMON CENTER.\n"
	.string "We heal your POKéMON free of charge.$"

OreburghCity_PokemonCenter_1F_Text_AceTrainer:
	.string "There's a long way from here to\n"
	.string "ETERNA CITY. You should be prepared\l"
	.string "for a long journey.$"

OreburghCity_PokemonCenter_1F_Text_Gentleman:
	.string "Hmmm! What, or who, is this TEAM\n"
	.string "GALACTIC?! They make wonderful claims\l"
	.string "of a dream energy source on one hand...\p"
	.string "But rumor has it they steal POKéMON\n"
	.string "from others by force. It's a mystery!$"
