OreburghCity_PokemonCenter_1F_MapScripts::
	.byte 0

OreburghCity_PokemonCenter_1F_EventScript_Nurse::
	msgbox OreburghCity_PokemonCenter_1F_Text_Nurse, MSGBOX_NPC
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
