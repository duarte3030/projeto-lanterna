Route204_MapScripts::
	.byte 0

Route204_EventScript_AceTrainer::
	lock
	faceplayer
	msgbox Route204_Text_AceTrainer, MSGBOX_DEFAULT
	release
	end

Route204_EventScript_YoungsterNorth::
	msgbox Route204_Text_YoungsterNorth, MSGBOX_NPC
	end

Route204_EventScript_Brandon::
	lock
	faceplayer
	msgbox Route204_Text_Brandon, MSGBOX_DEFAULT
	release
	end

Route204_EventScript_YoungsterSouth::
	msgbox Route204_Text_YoungsterSouth, MSGBOX_NPC
	end

Route204_EventScript_Sarah::
	lock
	faceplayer
	msgbox Route204_Text_Sarah, MSGBOX_DEFAULT
	release
	end

Route204_Text_AceTrainer:
	.string "Hi, are you the flirty type?\p"
	.string "I teach at the TRAINERS' SCHOOL,\n"
	.string "and I'd like to give you a lesson.$"

Route204_Text_YoungsterNorth:
	.string "FLOAROMA TOWN is full of flowers.\n"
	.string "It smells great all year round.$"

Route204_Text_Brandon:
	.string "I caught so many Bug POKéMON\n"
	.string "on this route, my Bag is full!$"

Route204_Text_YoungsterSouth:
	.string "RAVAGED PATH is nearby. It's all\n"
	.string "caved in from an old rockslide.$"

Route204_Text_Sarah:
	.string "I've been camping out here for\n"
	.string "days. The POKéMON are friendly.$"

Route204_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_BUG_CATCHER_BRANDON, Route204_Text_Trainer1Intro, Route204_Text_Trainer1Defeat
	msgbox Route204_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route204_Text_Trainer1Intro:
	.string "Hey, hey, let me show off my bug\n"
	.string "Pokémon!$"

Route204_Text_Trainer1Defeat:
	.string "I'm not going to be able to explain\n"
	.string "the charms of bug Pokémon this way!$"

Route204_Text_Trainer1Post:
	.string "Bug Pokémon grow quickly, and they do\n"
	.string "stuff like poison and paralyze, and\pthey're cute and yet cool.\pYou gotta believe me. They're good!$"

Route204_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_AROMA_LADY_TAYLOR, Route204_Text_Trainer2Intro, Route204_Text_Trainer2Defeat
	msgbox Route204_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route204_Text_Trainer2Intro:
	.string "What kind of person are you, to be\n"
	.string "drawn here by the scent of flowers?$"

Route204_Text_Trainer2Defeat:
	.string "It was a strong Trainer who was drawn\n"
	.string "here by the scent of flowers!$"

Route204_Text_Trainer2Post:
	.string "By the way, have you collected new\n"
	.string "apps from the Pokétch Company?$"
