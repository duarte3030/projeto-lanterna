Route220_MapScripts::
	.byte 0

Route220_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_ERIK, Route220_Text_Trainer1Intro, Route220_Text_Trainer1Defeat
	msgbox Route220_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route220_Text_Trainer1Intro:
	.string "On your marks, get set, go!\p...When I say that, let's start.\p$"

Route220_Text_Trainer1Defeat:
	.string "Yow-ow-ow-ow!\n"
	.string "My leg's cramped up!$"

Route220_Text_Trainer1Post:
	.string "I forgot to do my stretching\n"
	.string "exercises...$"

Route220_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_VINCENT, Route220_Text_Trainer2Intro, Route220_Text_Trainer2Defeat
	msgbox Route220_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route220_Text_Trainer2Intro:
	.string "OK! Get your breathing in order!\nOK! You're ready to go!\p$"

Route220_Text_Trainer2Defeat:
	.string "I let my momentum falter...$"

Route220_Text_Trainer2Post:
	.string "Listen, I have something important to\n"
	.string "say to you.\p"
	.string "Don't drown in your own talent.$"

Route220_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_JESSICA, Route220_Text_Trainer3Intro, Route220_Text_Trainer3Defeat
	msgbox Route220_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route220_Text_Trainer3Intro:
	.string "Swimming is a workout for your entire\nbody.\pJump in and swim!\nSwim, you!\p$"

Route220_Text_Trainer3Defeat:
	.string "Sunk like a stone!$"

Route220_Text_Trainer3Post:
	.string "Well, Pokémon's one thing, but you\n"
	.string "should take up swimming, too!$"

Route220_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_ERICA, Route220_Text_Trainer4Intro, Route220_Text_Trainer4Defeat
	msgbox Route220_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route220_Text_Trainer4Intro:
	.string "The human body floats more easily in\nthe sea, so it's easy to swim!\p$"

Route220_Text_Trainer4Defeat:
	.string "The sea is salty, but all I taste is\n"
	.string "bitterness...$"

Route220_Text_Trainer4Post:
	.string "I've got that sinking feeling...$"

Route220_EventScript_Trainer5::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_ADRIAN, Route220_Text_Trainer5Intro, Route220_Text_Trainer5Defeat
	msgbox Route220_Text_Trainer5Post, MSGBOX_AUTOCLOSE
	end

Route220_Text_Trainer5Intro:
	.string "I only live to swim. Teach me what's\nso fun about Pokémon!\p$"

Route220_Text_Trainer5Defeat:
	.string "Oh, yeah, that was fun!\n"
	.string "I learned something good!$"

Route220_Text_Trainer5Post:
	.string "It's what I live for!\n"
	.string "Pokémon!$"

Route220_EventScript_Trainer6::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_KATELYN, Route220_Text_Trainer6Intro, Route220_Text_Trainer6Defeat
	msgbox Route220_Text_Trainer6Post, MSGBOX_AUTOCLOSE
	end

Route220_Text_Trainer6Intro:
	.string "I may not look it now, but I'm a\nstar. I'm always with my Pokémon.\p$"

Route220_Text_Trainer6Defeat:
	.string "I lost, but at least I had fun.$"

Route220_Text_Trainer6Post:
	.string "If it were an underwater Pokémon\n"
	.string "show, I would have shined.$"

Route220_EventScript_Trainer7::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_CLAIRE, Route220_Text_Trainer7Intro, Route220_Text_Trainer7Defeat
	msgbox Route220_Text_Trainer7Post, MSGBOX_AUTOCLOSE
	end

Route220_Text_Trainer7Intro:
	.string "I bought a new bikini!\nIt's this year's newest model!\p$"

Route220_Text_Trainer7Defeat:
	.string "Psssssh!$"

Route220_Text_Trainer7Post:
	.string "I bought the wrong size of bikini.\n"
	.string "It's a little too snug...$"

