JubilifeCity_PokemonCenter_1F_MapScripts::
	.byte 0

JubilifeCity_PokemonCenter_1F_EventScript_Nurse::
	msgbox JubilifeCity_PokemonCenter_1F_Text_Nurse, MSGBOX_NPC
	end

JubilifeCity_PokemonCenter_1F_EventScript_SchoolKid::
	msgbox JubilifeCity_PokemonCenter_1F_Text_SchoolKid, MSGBOX_NPC
	end

JubilifeCity_PokemonCenter_1F_EventScript_Twin::
	msgbox JubilifeCity_PokemonCenter_1F_Text_Twin, MSGBOX_NPC
	end

JubilifeCity_PokemonCenter_1F_Text_Nurse:
	.string "Welcome to the Pokémon Center!\p"
	.string "I'm sorry, I can't heal your POKéMON\n"
	.string "just yet. Please come back later.$"

JubilifeCity_PokemonCenter_1F_Text_SchoolKid:
	.string "JUBILIFE CITY is the biggest city\n"
	.string "in SINNOH. I still get lost here!$"

JubilifeCity_PokemonCenter_1F_Text_Twin:
	.string "My sister and I always meet up at\n"
	.string "the POKéMON CENTER after school.$"
