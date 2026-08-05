EternaForest_MapScripts::
	.byte 0

EternaForest_EventScript_BugCatcher1::
	msgbox EternaForest_Text_BugCatcher1, MSGBOX_NPC
	end

EternaForest_EventScript_BugCatcher2::
	msgbox EternaForest_Text_BugCatcher2, MSGBOX_NPC
	end

EternaForest_EventScript_Hiker::
	msgbox EternaForest_Text_Hiker, MSGBOX_NPC
	end

EternaForest_EventScript_Signboard::
	msgbox EternaForest_Text_Signboard, MSGBOX_SIGN
	end

EternaForest_EventScript_TrainerTipsSign::
	msgbox EternaForest_Text_TrainerTipsSign, MSGBOX_SIGN
	end

EternaForest_Text_BugCatcher1:
	.string "Eterna Forest is full of bug\n"
	.string "Pokémon if you know where to look.$"

EternaForest_Text_BugCatcher2:
	.string "I've been trying to catch a\n"
	.string "Kricketot all morning. No luck yet!$"

EternaForest_Text_Hiker:
	.string "Watch your step. The forest floor\n"
	.string "hides more than just tall grass.$"

EternaForest_Text_Signboard:
	.string "ETERNA FOREST\n"
	.string "Sunlight barely reaches the ground\n"
	.string "here.$"

EternaForest_Text_TrainerTipsSign:
	.string "TRAINER TIPS\n"
	.string "A sharp Trainer studies type\n"
	.string "matchups before every battle.$"

EternaForest_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_BUG_CATCHER_JACK, EternaForest_Text_Trainer1Intro, EternaForest_Text_Trainer1Defeat
	msgbox EternaForest_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

EternaForest_Text_Trainer1Intro:
	.string "What's cool, you might ask? No?\n"
	.string "I'll tell you anyway: bug Pokémon!$"

EternaForest_Text_Trainer1Defeat:
	.string "Don't ignore bug Pokémon!\n"
	.string "That really bugs me!$"

EternaForest_Text_Trainer1Post:
	.string "It would seem that coolness alone\n"
	.string "doesn't add up to any wins...$"

EternaForest_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_BUG_CATCHER_PHILLIP, EternaForest_Text_Trainer2Intro, EternaForest_Text_Trainer2Defeat
	msgbox EternaForest_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

EternaForest_Text_Trainer2Intro:
	.string "Here comes the swarm!$"

EternaForest_Text_Trainer2Defeat:
	.string "Whoooh...$"

EternaForest_Text_Trainer2Post:
	.string "There's a Pokémon ability named Swarm.$"

EternaForest_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_PSYCHIC_KODY, EternaForest_Text_Trainer3Intro, EternaForest_Text_Trainer3Defeat
	msgbox EternaForest_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

EternaForest_Text_Trainer3Intro:
	.string "A strange presence has been felt...\n"
	.string "It is emanating from...you!$"

EternaForest_Text_Trainer3Defeat:
	.string "Oh, no!\n"
	.string "My MEDITITE!$"

EternaForest_Text_Trainer3Post:
	.string "The Old Chateau... I sense...\n"
	.string "a particularly strong presence there.$"

EternaForest_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_PSYCHIC_LINDSEY, EternaForest_Text_Trainer4Intro, EternaForest_Text_Trainer4Defeat
	msgbox EternaForest_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

EternaForest_Text_Trainer4Intro:
	.string "I see it...\n"
	.string "I see it...\pI see you going down in defeat...$"

EternaForest_Text_Trainer4Defeat:
	.string "It is I that has gone down in defeat.$"

EternaForest_Text_Trainer4Post:
	.string "The Old Chateau...\n"
	.string "There should be none alive in it...\pAnd yet there is a pervasive sense of\n"
	.string "a presence...$"

EternaForest_EventScript_Trainer5::
	trainerbattle_single TRAINER_SINNOH_LASS_BRIANA, EternaForest_Text_Trainer5Intro, EternaForest_Text_Trainer5Defeat
	msgbox EternaForest_Text_Trainer5Post, MSGBOX_AUTOCLOSE
	end

EternaForest_Text_Trainer5Intro:
	.string "We're just out on a power walk!$"

EternaForest_Text_Trainer5Defeat:
	.string "Oh, you!$"

EternaForest_Text_Trainer5Post:
	.string "You can't avoid bug Pokémon ever in\n"
	.string "the forest.\pI didn't have any Antidotes with me,\n"
	.string "either. It was the worst!$"

EternaForest_EventScript_Trainer6::
	trainerbattle_single TRAINER_SINNOH_BUG_CATCHER_DONALD, EternaForest_Text_Trainer6Intro, EternaForest_Text_Trainer6Defeat
	msgbox EternaForest_Text_Trainer6Post, MSGBOX_AUTOCLOSE
	end

EternaForest_Text_Trainer6Intro:
	.string "My senses tingle...\n"
	.string "I've spotted a rare Pokémon!$"

EternaForest_Text_Trainer6Defeat:
	.string "Awawawawah...$"

EternaForest_Text_Trainer6Post:
	.string "I thought it was a rare Pokémon, but\n"
	.string "it turned out to be just a Trainer!$"

EternaForest_EventScript_Trainer7::
	trainerbattle_single TRAINER_SINNOH_PSYCHIC_ELIJAH, EternaForest_Text_Trainer7Intro, EternaForest_Text_Trainer7Defeat
	msgbox EternaForest_Text_Trainer7Post, MSGBOX_AUTOCLOSE
	end

EternaForest_Text_Trainer7Intro:
	.string "When a Trainer and a Pokémon bond\n"
	.string "as one, a wondrous power is born...$"

EternaForest_Text_Trainer7Defeat:
	.string "Urmmm...\n"
	.string "Urrrrmmmmm...$"

EternaForest_Text_Trainer7Post:
	.string "There still remain many mysteries yet\n"
	.string "to be solved in this strange world...$"

EternaForest_EventScript_Trainer8::
	trainerbattle_single TRAINER_SINNOH_PSYCHIC_RACHAEL, EternaForest_Text_Trainer8Intro, EternaForest_Text_Trainer8Defeat
	msgbox EternaForest_Text_Trainer8Post, MSGBOX_AUTOCLOSE
	end

EternaForest_Text_Trainer8Intro:
	.string "This forest is strange, you know...\n"
	.string "It seems to fill me with energy...$"

EternaForest_Text_Trainer8Defeat:
	.string "Your victory...\n"
	.string "There is nothing strange about it.$"

EternaForest_Text_Trainer8Post:
	.string "Forests are mystifying... They seem\n"
	.string "to gather such unexplainable energy.$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

EternaForest_EventScript_Placa1::
	msgbox EternaForest_Text_Placa1, MSGBOX_SIGN
	end

EternaForest_Text_Placa1:
	.string "The Eterna Forest\nWhere Time Flows Eternally$"

EternaForest_EventScript_Placa2::
	msgbox EternaForest_Text_Placa2, MSGBOX_SIGN
	end

EternaForest_Text_Placa2:
	.string "Trainer Tips!\pIn forests and caves, there are many\nitems on the ground that cannot be\pseen in the murky darkness.\pTake the time to search carefully!$"
