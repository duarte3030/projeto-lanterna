Route210_North_MapScripts::
	.byte 0

Route210_North_EventScript_AceTrainerErnest::
	msgbox Route210_North_Text_AceTrainerErnest, MSGBOX_NPC
	end

Route210_North_EventScript_AceTrainerAlyssa::
	msgbox Route210_North_Text_AceTrainerAlyssa, MSGBOX_NPC
	end

Route210_North_EventScript_Veteran::
	msgbox Route210_North_Text_Veteran, MSGBOX_NPC
	end

Route210_North_EventScript_BlackBelt::
	msgbox Route210_North_Text_BlackBelt, MSGBOX_NPC
	end

Route210_North_Text_AceTrainerErnest:
	.string "Celestic Town is just west\n"
	.string "of here. Old ruins, they say.$"

Route210_North_Text_AceTrainerAlyssa:
	.string "This route always has great\n"
	.string "wild Pokémon to find.$"

Route210_North_Text_Veteran:
	.string "I've caught Pokémon on every\n"
	.string "route in Sinnoh. Almost.$"

Route210_North_Text_BlackBelt:
	.string "Feel that mountain air.\n"
	.string "Great for training.$"

Route210_North_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_ERNEST, Route210_North_Text_Trainer1Intro, Route210_North_Text_Trainer1Defeat
	msgbox Route210_North_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route210_North_Text_Trainer1Intro:
	.string "You seem to have a lot of confidence.\n"
	.string "Let's see if it's justified!$"

Route210_North_Text_Trainer1Defeat:
	.string "Haha!\n"
	.string "A total loss for me!$"

Route210_North_Text_Trainer1Post:
	.string "You seem to have an abundance of\n"
	.string "talent. It's pretty amazing.$"

Route210_North_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_ALYSSA, Route210_North_Text_Trainer2Intro, Route210_North_Text_Trainer2Defeat
	msgbox Route210_North_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route210_North_Text_Trainer2Intro:
	.string "As an Ace Trainer, I have to take\n"
	.string "battles in stride.\pI need to stay cool and calm whether\n"
	.string "I win or lose.$"

Route210_North_Text_Trainer2Defeat:
	.string "Aiyeeeeh!\n"
	.string "We lost!$"

Route210_North_Text_Trainer2Post:
	.string "How dare you beat us!\n"
	.string "Go away! Go!$"

Route210_North_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_NINJA_BOY_JOEL, Route210_North_Text_Trainer3Intro, Route210_North_Text_Trainer3Defeat
	msgbox Route210_North_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route210_North_Text_Trainer3Intro:
	.string "I just startled you!\pWhile you're still struggling to\n"
	.string "recover, I'll already be the winner!$"

Route210_North_Text_Trainer3Defeat:
	.string "Oh, what's that?\n"
	.string "You're supposed to be fumbling more.$"

Route210_North_Text_Trainer3Post:
	.string "I wanted a better reaction from you.\n"
	.string "Now I feel silly for hiding!$"

Route210_North_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_NINJA_BOY_NATHAN, Route210_North_Text_Trainer4Intro, Route210_North_Text_Trainer4Defeat
	msgbox Route210_North_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route210_North_Text_Trainer4Intro:
	.string "We ninjas appear where you least\n"
	.string "expect us!$"

Route210_North_Text_Trainer4Defeat:
	.string "I didn't expect to lose...$"

Route210_North_Text_Trainer4Post:
	.string "While hiding, I think about what Pokémon\n"
	.string "must be thinking inside their Poké Balls.$"

Route210_North_EventScript_Trainer5::
	trainerbattle_single TRAINER_SINNOH_NINJA_BOY_DAVIDO, Route210_North_Text_Trainer5Intro, Route210_North_Text_Trainer5Defeat
	msgbox Route210_North_Text_Trainer5Post, MSGBOX_AUTOCLOSE
	end

Route210_North_Text_Trainer5Intro:
	.string "A ninja can use all kinds of skills.\n"
	.string "Like this and like that!$"

Route210_North_Text_Trainer5Defeat:
	.string "Hmm...\n"
	.string "My ninja techniques failed to work...$"

Route210_North_Text_Trainer5Post:
	.string "There's a ninja Gym Leader somewhere\n"
	.string "far away.\pI should become a devotee of theirs.$"

Route210_North_EventScript_Trainer6::
	trainerbattle_single TRAINER_SINNOH_DRAGON_TAMER_PATRICK, Route210_North_Text_Trainer6Intro, Route210_North_Text_Trainer6Defeat
	msgbox Route210_North_Text_Trainer6Post, MSGBOX_AUTOCLOSE
	end

Route210_North_Text_Trainer6Intro:
	.string "Try not to be shocked when you lay your\n"
	.string "eyes on my Pokémon!$"

Route210_North_Text_Trainer6Defeat:
	.string "Oh, my...\n"
	.string "Good golly 'n' gosh...$"

Route210_North_Text_Trainer6Post:
	.string "A dragon Pokémon's real power is\n"
	.string "nothing like mine!$"

Route210_North_EventScript_Trainer7::
	trainerbattle_single TRAINER_SINNOH_BIRD_KEEPER_BRIANNA, Route210_North_Text_Trainer7Intro, Route210_North_Text_Trainer7Defeat
	msgbox Route210_North_Text_Trainer7Post, MSGBOX_AUTOCLOSE
	end

Route210_North_Text_Trainer7Intro:
	.string "I'll teach you about the charms of\n"
	.string "bird Pokémon!$"

Route210_North_Text_Trainer7Defeat:
	.string "Well, that was surprising!$"

Route210_North_Text_Trainer7Post:
	.string "The sight of you battling...\n"
	.string "It was simply a wonder to watch!$"

Route210_North_EventScript_Trainer10::
	trainerbattle_single TRAINER_SINNOH_VETERAN_BRIAN, Route210_North_Text_Trainer10Intro, Route210_North_Text_Trainer10Defeat
	msgbox Route210_North_Text_Trainer10Post, MSGBOX_AUTOCLOSE
	end

Route210_North_Text_Trainer10Intro:
	.string "Very well. I've decided.\pI'll battle one last time, with you,\n"
	.string "then I'm retiring as a Trainer.$"

Route210_North_Text_Trainer10Defeat:
	.string "I've lost, but...\n"
	.string "What is this rush I feel?!$"

Route210_North_Text_Trainer10Post:
	.string "Yes! This is fun!\n"
	.string "Pokémon are fun!\pRetire? Perish that thought!\pI'll become a lot tougher.\n"
	.string "Next time, victory is mine!$"

Route210_North_EventScript_Trainer11::
	trainerbattle_single TRAINER_SINNOH_BLACK_BELT_ADAM, Route210_North_Text_Trainer11Intro, Route210_North_Text_Trainer11Defeat
	msgbox Route210_North_Text_Trainer11Post, MSGBOX_AUTOCLOSE
	end

Route210_North_Text_Trainer11Intro:
	.string "This buff physique isn't just for\n"
	.string "show!$"

Route210_North_Text_Trainer11Defeat:
	.string "B-but!\n"
	.string "My buff physique!$"

Route210_North_Text_Trainer11Post:
	.string "Why? Is it because my training isn't\n"
	.string "enough?!$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route210_North_EventScript_Placa1::
	msgbox Route210_North_Text_Placa1, MSGBOX_SIGN
	end

Route210_North_Text_Placa1:
	.string "Rt. 210\nCelestic Town$"

Route210_North_EventScript_Placa2::
	msgbox Route210_North_Text_Placa2, MSGBOX_SIGN
	end

Route210_North_Text_Placa2:
	.string "Grandma Wilma's House$"
