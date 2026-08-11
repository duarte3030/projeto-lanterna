Route211_East_MapScripts::
	.byte 0

Route211_East_EventScript_AceTrainer::
	msgbox Route211_East_Text_AceTrainer, MSGBOX_NPC
	end

Route211_East_EventScript_BirdKeeper::
	msgbox Route211_East_Text_BirdKeeper, MSGBOX_NPC
	end

Route211_East_EventScript_BlackBelt::
	msgbox Route211_East_Text_BlackBelt, MSGBOX_NPC
	end

Route211_East_EventScript_RuinManiac::
	msgbox Route211_East_Text_RuinManiac, MSGBOX_NPC
	end

Route211_East_Text_AceTrainer:
	.string "I'm strong! I'm strong! I'm\n"
	.string "strong! ...Am I really?\p"
	.string "Wah! You startled me good!$"

Route211_East_Text_BirdKeeper:
	.string "I love watching the bird\n"
	.string "Pokémon soar over this ridge.$"

Route211_East_Text_BlackBelt:
	.string "Training in the mountains\n"
	.string "makes you tough.$"

Route211_East_Text_RuinManiac:
	.string "I dig for ruins around here.\n"
	.string "Found some interesting shards.$"

Route211_East_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_BIRD_KEEPER_KATHERINE, Route211_East_Text_Trainer1Intro, Route211_East_Text_Trainer1Defeat
	msgbox Route211_East_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route211_East_Text_Trainer1Intro:
	.string "I go everywhere with my NOCTOWL.\n"
	.string "We're gonna show you owl best! Ha!$"

Route211_East_Text_Trainer1Defeat:
	.string "We did our best. That's what\n"
	.string "matters. Right?$"

Route211_East_Text_Trainer1Post:
	.string "Even on cold days, just being with\n"
	.string "my NOCTOWL keeps me warm!$"

Route211_East_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_NINJA_BOY_NICK, Route211_East_Text_Trainer2Intro, Route211_East_Text_Trainer2Defeat
	msgbox Route211_East_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route211_East_Text_Trainer2Intro:
	.string "Speed is a ninja's best weapon!\n"
	.string "Can you keep up?$"

Route211_East_Text_Trainer2Defeat:
	.string "I did a lot to conceal myself, too...$"

Route211_East_Text_Trainer2Post:
	.string "I'll wait here for a weaker-looking\n"
	.string "Trainer and then ambush them!$"

Route211_East_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_BLACK_BELT_SEAN, Route211_East_Text_Trainer3Intro, Route211_East_Text_Trainer3Defeat
	msgbox Route211_East_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route211_East_Text_Trainer3Intro:
	.string "Hah! Hah!\n"
	.string "I'm psyched for this! Here goes!$"

Route211_East_Text_Trainer3Defeat:
	.string "I don't get why we can't win.$"

Route211_East_Text_Trainer3Post:
	.string "I don't reminisce over yesterday.\n"
	.string "I don't think about tomorrow.\pI only live today to the fullest.\pThat's my policy!$"

Route211_East_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_RUIN_MANIAC_HARRY, Route211_East_Text_Trainer4Intro, Route211_East_Text_Trainer4Defeat
	msgbox Route211_East_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route211_East_Text_Trainer4Intro:
	.string "Whilst exploring the ruins, I spotted\n"
	.string "a Trainer! I must investigate!$"

Route211_East_Text_Trainer4Defeat:
	.string "My investigation has revealed the\n"
	.string "Trainer to be tough! Ouch...$"

Route211_East_Text_Trainer4Post:
	.string "Celestic Town is an old town.\n"
	.string "I'm sure to find something cool.$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route211_East_EventScript_Placa1::
	msgbox Route211_East_Text_Placa1, MSGBOX_SIGN
	end

Route211_East_Text_Placa1:
	.string "Trainer Tips\pEven Veterans can get lost inside of\nMt. Coronet.\pTrainers should check their supply\nof medicine and items before trying\pto venture through.$"

Route211_East_EventScript_Placa2::
	msgbox Route211_East_Text_Placa2, MSGBOX_SIGN
	end

Route211_East_Text_Placa2:
	.string "Rt. 211\nMt. Coronet$"

Route211_East_EventScript_Placa3::
	msgbox Route211_East_Text_Placa3, MSGBOX_SIGN
	end

Route211_East_Text_Placa3:
	.string "Rt. 211\nCelestic Town$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route211_East_EventScript_Npc1::
	msgbox Route211_East_Text_Npc1, MSGBOX_NPC
	end

Route211_East_Text_Npc1:
	.string "I'm strong!\nI'm strong!\pI'm strong!\pI'm strong!\pI'm strong!\pI'm strong!\pI'm strong!\pI'm strong!\p...Am I really?\pNo, I am strong!\pI'm strong!\pOK! I'm all good to go!$"
