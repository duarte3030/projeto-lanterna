Route220_MapScripts::
	.byte 0

Route220_EventScript_SwimmerErik::
	msgbox Route220_Text_SwimmerErik, MSGBOX_NPC
	end

Route220_EventScript_SwimmerJessica::
	msgbox Route220_Text_SwimmerJessica, MSGBOX_NPC
	end

Route220_EventScript_SwimmerKatelyn::
	msgbox Route220_Text_SwimmerKatelyn, MSGBOX_NPC
	end

Route220_Text_SwimmerErik:
	.string "The water here is perfect for\n"
	.string "keeping a POKéMON's stamina up.$"

Route220_Text_SwimmerJessica:
	.string "I love diving near TWINLEAF TOWN.\n"
	.string "The current is calm today.$"

Route220_Text_SwimmerKatelyn:
	.string "Careful where you swim! Some spots\n"
	.string "drop off really deep.$"

Route220_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_ERIK, Route220_Text_Trainer1Intro, Route220_Text_Trainer1Defeat
	msgbox Route220_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route220_Text_Trainer1Intro:
	.string "On your marks, get set, go!\p...When I say that, let's start.\p$"

Route220_Text_Trainer1Defeat:
	.string "Yow-ow-ow-ow!\nMy leg's cramped up!\n$"

Route220_Text_Trainer1Post:
	.string "I forgot to do my stretching\nexercises...\n$"

Route220_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_VINCENT, Route220_Text_Trainer2Intro, Route220_Text_Trainer2Defeat
	msgbox Route220_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route220_Text_Trainer2Intro:
	.string "OK! Get your breathing in order!\nOK! You're ready to go!\p$"

Route220_Text_Trainer2Defeat:
	.string "I let my momentum falter...\n$"

Route220_Text_Trainer2Post:
	.string "Listen, I have something important to\nsay to you.\pDon't drown in your own talent.\n$"

Route220_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_JESSICA, Route220_Text_Trainer3Intro, Route220_Text_Trainer3Defeat
	msgbox Route220_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route220_Text_Trainer3Intro:
	.string "Swimming is a workout for your entire\nbody.\pJump in and swim!\nSwim, you!\p$"

Route220_Text_Trainer3Defeat:
	.string "Sunk like a stone!\n$"

Route220_Text_Trainer3Post:
	.string "Well, Pokémon's one thing, but you\nshould take up swimming, too!\n$"

Route220_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_ERICA, Route220_Text_Trainer4Intro, Route220_Text_Trainer4Defeat
	msgbox Route220_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route220_Text_Trainer4Intro:
	.string "The human body floats more easily in\nthe sea, so it's easy to swim!\p$"

Route220_Text_Trainer4Defeat:
	.string "The sea is salty, but all I taste is\nbitterness...\n$"

Route220_Text_Trainer4Post:
	.string "I've got that sinking feeling...\n$"

Route220_EventScript_Trainer5::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_ADRIAN, Route220_Text_Trainer5Intro, Route220_Text_Trainer5Defeat
	msgbox Route220_Text_Trainer5Post, MSGBOX_AUTOCLOSE
	end

Route220_Text_Trainer5Intro:
	.string "I only live to swim. Teach me what's\nso fun about Pokémon!\p$"

Route220_Text_Trainer5Defeat:
	.string "Oh, yeah, that was fun!\nI learned something good!\n$"

Route220_Text_Trainer5Post:
	.string "It's what I live for!\nPokémon!\n$"

Route220_EventScript_Trainer6::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_KATELYN, Route220_Text_Trainer6Intro, Route220_Text_Trainer6Defeat
	msgbox Route220_Text_Trainer6Post, MSGBOX_AUTOCLOSE
	end

Route220_Text_Trainer6Intro:
	.string "I may not look it now, but I'm a\nstar. I'm always with my Pokémon.\p$"

Route220_Text_Trainer6Defeat:
	.string "I lost, but at least I had fun.\n$"

Route220_Text_Trainer6Post:
	.string "If it were an underwater Pokémon\nshow, I would have shined.\n$"

Route220_EventScript_Trainer7::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_CLAIRE, Route220_Text_Trainer7Intro, Route220_Text_Trainer7Defeat
	msgbox Route220_Text_Trainer7Post, MSGBOX_AUTOCLOSE
	end

Route220_Text_Trainer7Intro:
	.string "I bought a new bikini!\nIt's this year's newest model!\p$"

Route220_Text_Trainer7Defeat:
	.string "Psssssh!\n$"

Route220_Text_Trainer7Post:
	.string "I bought the wrong size of bikini.\nIt's a little too snug...\n$"

