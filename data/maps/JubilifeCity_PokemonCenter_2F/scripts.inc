JubilifeCity_PokemonCenter_2F_MapScripts::
	.byte 0

JubilifeCity_PokemonCenter_2F_EventScript_ClerkWest::
	msgbox JubilifeCity_PokemonCenter_2F_Text_ClerkWest, MSGBOX_NPC
	end

JubilifeCity_PokemonCenter_2F_EventScript_ClerkMid::
	msgbox JubilifeCity_PokemonCenter_2F_Text_ClerkMid, MSGBOX_NPC
	end

JubilifeCity_PokemonCenter_2F_EventScript_ClerkEast::
	msgbox JubilifeCity_PokemonCenter_2F_Text_ClerkEast, MSGBOX_NPC
	end

JubilifeCity_PokemonCenter_2F_Text_ClerkWest:
	.string "The link services aren't ready to\n"
	.string "use yet. Please check back soon.$"

JubilifeCity_PokemonCenter_2F_Text_ClerkMid:
	.string "Trainers from all over come up here\n"
	.string "to trade and battle with friends.$"

JubilifeCity_PokemonCenter_2F_Text_ClerkEast:
	.string "Feel free to look around, but the\n"
	.string "counters are closed for now.$"
