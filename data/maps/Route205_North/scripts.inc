Route205_North_MapScripts::
	.byte 0

Route205_North_EventScript_Fisherman::
	msgbox Route205_North_Text_Fisherman, MSGBOX_NPC
	end

Route205_North_EventScript_Andrew::
	lock
	faceplayer
	msgbox Route205_North_Text_Andrew, MSGBOX_DEFAULT
	release
	end

Route205_North_EventScript_Joseph::
	lock
	faceplayer
	msgbox Route205_North_Text_Joseph, MSGBOX_DEFAULT
	release
	end

Route205_North_EventScript_Zachary::
	lock
	faceplayer
	msgbox Route205_North_Text_Zachary, MSGBOX_DEFAULT
	release
	end

Route205_North_Text_Fisherman:
	.string "The fishing's great around here.\n"
	.string "I've caught some good POKéMON.$"

Route205_North_Text_Andrew:
	.string "I come out here every day to\n"
	.string "fish. It's the best spot around!$"

Route205_North_Text_Joseph:
	.string "Patience is the key to fishing.\n"
	.string "Just like it is with POKéMON.$"

Route205_North_Text_Zachary:
	.string "ETERNA CITY is right over there.\n"
	.string "You can see it from the water.$"

Route205_North_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_FISHERMAN_ANDREW, Route205_North_Text_Trainer1Intro, Route205_North_Text_Trainer1Defeat
	msgbox Route205_North_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route205_North_Text_Trainer1Intro:
	.string "Nothing's biting...\n"
	.string "I could use a break, I suppose.$"

Route205_North_Text_Trainer1Defeat:
	.string "Well, that didn't do anything for me...$"

Route205_North_Text_Trainer1Post:
	.string "!\pYank your fishing rod when that\n"
	.string "appears. That's how you fish.$"

Route205_North_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_FISHERMAN_JOSEPH, Route205_North_Text_Trainer2Intro, Route205_North_Text_Trainer2Defeat
	msgbox Route205_North_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route205_North_Text_Trainer2Intro:
	.string "How about that!\n"
	.string "I've netted me a feisty Trainer!$"

Route205_North_Text_Trainer2Defeat:
	.string "I let a big win slip away...$"

Route205_North_Text_Trainer2Post:
	.string "Do you have a fishing rod?\n"
	.string "Catch some big ones!$"

Route205_North_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_FISHERMAN_ZACHARY, Route205_North_Text_Trainer3Intro, Route205_North_Text_Trainer3Defeat
	msgbox Route205_North_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route205_North_Text_Trainer3Intro:
	.string "I fished up some tough Pokémon!\n"
	.string "Let's have ourselves a battle!$"

Route205_North_Text_Trainer3Defeat:
	.string "Losing to a kid has me gasping like\n"
	.string "a MAGIKARP...$"

Route205_North_Text_Trainer3Post:
	.string "My feet are tangled, too!\n"
	.string "Ouch! Ouch!$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route205_North_EventScript_Placa1::
	msgbox Route205_North_Text_Placa1, MSGBOX_SIGN
	end

Route205_North_Text_Placa1:
	.string "Rt. 205\nEterna Forest$"

Route205_North_EventScript_Placa2::
	msgbox Route205_North_Text_Placa2, MSGBOX_SIGN
	end

Route205_North_Text_Placa2:
	.string "Rt. 205\nEterna City$"
