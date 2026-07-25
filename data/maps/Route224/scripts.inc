Route224_MapScripts::
	.byte 0

Route224_EventScript_AceTrainerRuben::
	lock
	faceplayer
	msgbox Route224_Text_AceTrainerRuben, MSGBOX_DEFAULT
	release
	end

Route224_EventScript_PsychicMaxwell::
	lock
	faceplayer
	msgbox Route224_Text_PsychicMaxwell, MSGBOX_DEFAULT
	release
	end

Route224_EventScript_BlackBeltCarl::
	msgbox Route224_Text_BlackBeltCarl, MSGBOX_NPC
	end

Route224_EventScript_VeteranArmando::
	lock
	faceplayer
	msgbox Route224_Text_VeteranArmando, MSGBOX_DEFAULT
	release
	end

Route224_EventScript_AceTrainerJamie::
	msgbox Route224_Text_AceTrainerJamie, MSGBOX_NPC
	end

Route224_Text_AceTrainerRuben:
	.string "This route stretches almost all\n"
	.string "the way to the POKéMON LEAGUE.$"

Route224_Text_PsychicMaxwell:
	.string "I can sense strong POKéMON\n"
	.string "resting nearby. Can you feel it?$"

Route224_Text_BlackBeltCarl:
	.string "Training my body and my POKéMON\n"
	.string "together, that's my way.$"

Route224_Text_VeteranArmando:
	.string "I've walked this route more times\n"
	.string "than I can count.$"

Route224_Text_AceTrainerJamie:
	.string "Not much farther to the EVER GRANDE\n"
	.string "gate now.$"

Route224_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_BLACK_BELT_CARL, Route224_Text_Trainer1Intro, Route224_Text_Trainer1Defeat
	msgbox Route224_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route224_Text_Trainer1Intro:
	.string "All right, my Pokémon squad!\nGet out there and kick up a storm!\p$"

Route224_Text_Trainer1Defeat:
	.string "The squad failed to hit its stride...\n$"

Route224_Text_Trainer1Post:
	.string "Hmm...\pGazing out over the sea doesn't do a\nthing for toughening up my Pokémon!\n$"

Route224_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_VETERAN_ARMANDO, Route224_Text_Trainer2Intro, Route224_Text_Trainer2Defeat
	msgbox Route224_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route224_Text_Trainer2Intro:
	.string "I've seen countless Trainers and\neven more Pokémon!\pSo, what kind of a Trainer are you?\p$"

Route224_Text_Trainer2Defeat:
	.string "I see...\nSimply outstanding.$"

Route224_Text_Trainer2Post:
	.string "I've seen countless Trainers and\neven more Pokémon.\pYou're a strong Trainer.\nMoreover, your heart is strong.\n$"


Route224_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_RUBEN, Route224_Text_Trainer3Intro, Route224_Text_Trainer3Defeat
	msgbox Route224_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route224_Text_Trainer3Intro:
	.string "There's something about you...\nYou're not just anybody.\pI challenge you!\p$"

Route224_Text_Trainer3Defeat:
	.string "You're at a different level of\nexpertise for sure!\n$"

Route224_Text_Trainer3Post:
	.string "You've won countless times...\nThat has made you very powerful.\n$"

Route224_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_PSYCHIC_MAXWELL, Route224_Text_Trainer4Intro, Route224_Text_Trainer4Defeat
	msgbox Route224_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route224_Text_Trainer4Intro:
	.string "For some reason I was drawn here,\nand it is here that I met you...\pI want to know what all this means!\p$"

Route224_Text_Trainer4Defeat:
	.string "I see...\pSo that's what it means...\n$"

Route224_Text_Trainer4Post:
	.string "I feel... I feel some sort of a mystic\npresence emanating from here...\n$"

Route224_EventScript_Trainer5::
	trainerbattle_single TRAINER_SINNOH_PSYCHIC_BRITTNEY, Route224_Text_Trainer5Intro, Route224_Text_Trainer5Defeat
	msgbox Route224_Text_Trainer5Post, MSGBOX_AUTOCLOSE
	end

Route224_Text_Trainer5Intro:
	.string "There is nothing here... And yet\nthere is a power lurking...\pWere you drawn by it, as well?\p$"

Route224_Text_Trainer5Defeat:
	.string "The power that slumbers within you...\nIt is rather marvelous indeed...\n$"

Route224_Text_Trainer5Post:
	.string "A place where nothing else exists...\pA place such as that is better suited\nto awaken the power within.\n$"

Route224_EventScript_Trainer6::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_JAMIE, Route224_Text_Trainer6Intro, Route224_Text_Trainer6Defeat
	msgbox Route224_Text_Trainer6Post, MSGBOX_AUTOCLOSE
	end

Route224_Text_Trainer6Intro:
	.string "I constantly analyze Pokémon and\nvarious battles on my laptop.\p$"

Route224_Text_Trainer6Defeat:
	.string "...Things don't always work out\naccording to my calculations...\n$"

Route224_Text_Trainer6Post:
	.string "I had a lot of fun battling with\nyou, though.\pI wonder if I can analyze the\nbattle data properly?\pI could use a rematch to get\nsome additional data.\n$"

Route224_EventScript_Trainer7::
	trainerbattle_single TRAINER_SINNOH_RUIN_MANIAC_LARRY, Route224_Text_Trainer7Intro, Route224_Text_Trainer7Defeat
	msgbox Route224_Text_Trainer7Post, MSGBOX_AUTOCLOSE
	end

Route224_Text_Trainer7Intro:
	.string "I don't care who you are--no one\ninterferes with my treasure hunting!\p$"

Route224_Text_Trainer7Defeat:
	.string "My Pokémon!\nMy treasures!\n$"

Route224_Text_Trainer7Post:
	.string "I heard there's an intriguing stone\nmonument around, so I came running.\n$"

Route224_EventScript_Trainer8::
	trainerbattle_single TRAINER_SINNOH_DRAGON_TAMER_HAYDEN, Route224_Text_Trainer8Intro, Route224_Text_Trainer8Defeat
	msgbox Route224_Text_Trainer8Post, MSGBOX_AUTOCLOSE
	end

Route224_Text_Trainer8Intro:
	.string "My dragon Pokémon chose to become\npowerful here. They sure like it!\p$"

Route224_Text_Trainer8Defeat:
	.string "Your battle style...\nSo savage...\n$"

Route224_Text_Trainer8Post:
	.string "It's been several years since I left\nthe Dragon's Den.\pI've got to say, your Pokémon are\nin the top class for toughness.$"

