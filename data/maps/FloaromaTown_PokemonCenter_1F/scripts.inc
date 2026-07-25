FloaromaTown_PokemonCenter_1F_MapScripts::
	.byte 0

FloaromaTown_PokemonCenter_1F_EventScript_Nurse::
	msgbox FloaromaTown_PokemonCenter_1F_Text_Nurse, MSGBOX_NPC
	end

FloaromaTown_PokemonCenter_1F_EventScript_AceTrainer::
	msgbox FloaromaTown_PokemonCenter_1F_Text_AceTrainer, MSGBOX_NPC
	end

FloaromaTown_PokemonCenter_1F_EventScript_BattleGirl::
	msgbox FloaromaTown_PokemonCenter_1F_Text_BattleGirl, MSGBOX_NPC
	end

FloaromaTown_PokemonCenter_1F_Text_Nurse:
	.string "Welcome to the POKéMON CENTER.\n"
	.string "We heal your POKéMON free of charge.$"

FloaromaTown_PokemonCenter_1F_Text_AceTrainer:
	.string "There've been problems with the\n"
	.string "electric power lately. Is there some\l"
	.string "trouble at the VALLEY WINDWORKS?$"

FloaromaTown_PokemonCenter_1F_Text_BattleGirl:
	.string "I train hard so I never lose a battle.\n"
	.string "FLOAROMA TOWN is a great place to\l"
	.string "relax between matches.$"
