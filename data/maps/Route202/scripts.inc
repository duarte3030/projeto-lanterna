Route202_MapScripts::
	.byte 0

Route202_EventScript_Youngster::
	msgbox Route202_Text_Youngster, MSGBOX_NPC
	end

Route202_EventScript_Tristan::
	lock
	faceplayer
	msgbox Route202_Text_Tristan, MSGBOX_DEFAULT
	release
	end

Route202_EventScript_Natalie::
	lock
	faceplayer
	msgbox Route202_Text_Natalie, MSGBOX_DEFAULT
	release
	end

Route202_EventScript_Logan::
	msgbox Route202_Text_Logan, MSGBOX_NPC
	end

Route202_Text_Youngster:
	.string "Have you tried using the POKé\n"
	.string "RADAR in the tall grass yet?$"

Route202_Text_Tristan:
	.string "I've been training here since\n"
	.string "sunrise. My POKéMON are strong!$"

Route202_Text_Natalie:
	.string "This patch of grass rustles a lot.\n"
	.string "I wonder what's hiding in there.$"

Route202_Text_Logan:
	.string "JUBILIFE CITY is just up ahead.\n"
	.string "It's the biggest city in SINNOH!$"

Route202_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_YOUNGSTER_TRISTAN, Route202_Text_Trainer1Intro, Route202_Text_Trainer1Defeat
	msgbox Route202_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route202_Text_Trainer1Intro:
	.string "You're a Pokémon Trainer, and so am I!\n"
	.string "Our eyes met, so battle we must!$"

Route202_Text_Trainer1Defeat:
	.string "Too strong!\n"
	.string "Too strong!$"

Route202_Text_Trainer1Post:
	.string "Don't be shy about talking to\n"
	.string "Trainers you'd like to battle.\pPokémon grow stronger and stronger\n"
	.string "from battling.$"

Route202_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_LASS_NATALIE, Route202_Text_Trainer2Intro, Route202_Text_Trainer2Defeat
	msgbox Route202_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route202_Text_Trainer2Intro:
	.string "I spy, with my little eye...\n"
	.string "A Trainer!\pA battle, please!$"

Route202_Text_Trainer2Defeat:
	.string "Oh, boo!\n"
	.string "I can't win!$"

Route202_Text_Trainer2Post:
	.string "My Pokémon are all tuckered out!\n"
	.string "I need to go to a Pokémon Center!$"

Route202_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_YOUNGSTER_LOGAN, Route202_Text_Trainer3Intro, Route202_Text_Trainer3Defeat
	msgbox Route202_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route202_Text_Trainer3Intro:
	.string "Let's have a Pokémon battle!\n"
	.string "Humph! But I'm gonna win!$"

Route202_Text_Trainer3Defeat:
	.string "You beat me?!\n"
	.string "You've got talent!$"

Route202_Text_Trainer3Post:
	.string "It was fun battling!\n"
	.string "Yup! I'm going to battle everyone!$"
