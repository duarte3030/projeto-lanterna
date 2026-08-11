Route209_MapScripts::
	.byte 0

Route209_EventScript_Fisherman::
	msgbox Route209_Text_Fisherman, MSGBOX_NPC
	end

Route209_EventScript_Breeder::
	msgbox Route209_Text_Breeder, MSGBOX_NPC
	end

Route209_EventScript_Cowgirl::
	msgbox Route209_Text_Cowgirl, MSGBOX_NPC
	end

Route209_EventScript_PokeKid::
	msgbox Route209_Text_PokeKid, MSGBOX_NPC
	end

Route209_Text_Fisherman:
	.string "Try fishing wherever there is a\n"
	.string "body of water.$"

Route209_Text_Breeder:
	.string "Solaceon Town has a great\n"
	.string "Pokémon Day Care nearby.$"

Route209_Text_Cowgirl:
	.string "I herd Miltank around here.\n"
	.string "They're gentle, mostly.$"

Route209_Text_PokeKid:
	.string "My Pikachu can find berries\n"
	.string "faster than I can!$"

Route209_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_BREEDER_ALBERT, Route209_Text_Trainer1Intro, Route209_Text_Trainer1Defeat
	msgbox Route209_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route209_Text_Trainer1Intro:
	.string "Let me see how much you've raised\n"
	.string "your Pokémon.$"

Route209_Text_Trainer1Defeat:
	.string "Good stuff! Your Pokémon are in\n"
	.string "impeccable condition.$"

Route209_Text_Trainer1Post:
	.string "It's obvious you raise your Pokémon\n"
	.string "with a lot of love.$"

Route209_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_BREEDER_JENNIFER, Route209_Text_Trainer2Intro, Route209_Text_Trainer2Defeat
	msgbox Route209_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route209_Text_Trainer2Intro:
	.string "Please, let me battle the Pokémon\n"
	.string "you've raised!$"

Route209_Text_Trainer2Defeat:
	.string "Giggle...\n"
	.string "They're raised with a lot of care!$"

Route209_Text_Trainer2Post:
	.string "Raise your Pokémon with lots of love,\n"
	.string "and they'll bond closely with you.$"

Route209_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_COWGIRL_SHELLEY, Route209_Text_Trainer3Intro, Route209_Text_Trainer3Defeat
	msgbox Route209_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route209_Text_Trainer3Intro:
	.string "Say, honey, where'd you come from?\n"
	.string "What kinds of Pokémon are you with?$"

Route209_Text_Trainer3Defeat:
	.string "Fancy folks like you have fancy\n"
	.string "Pokémon too, it looks like.$"

Route209_Text_Trainer3Post:
	.string "While working the ranch, I get to raise\n"
	.string "my Pokémon, too.\pI'd say it's the best of both worlds!$"

Route209_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_JOGGER_RICHARD, Route209_Text_Trainer4Intro, Route209_Text_Trainer4Defeat
	msgbox Route209_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route209_Text_Trainer4Intro:
	.string "I jog every morning to keep my\n"
	.string "Pokémon fit.$"

Route209_Text_Trainer4Defeat:
	.string "Oops!\n"
	.string "You threw off my running rhythm.$"

Route209_Text_Trainer4Post:
	.string "Nothing beats being fit and healthy!\pCome on, won't you run with me?\n"
	.string "To a better tomorrow!$"

Route209_EventScript_Trainer5::
	trainerbattle_single TRAINER_SINNOH_JOGGER_RAUL, Route209_Text_Trainer5Intro, Route209_Text_Trainer5Defeat
	msgbox Route209_Text_Trainer5Post, MSGBOX_AUTOCLOSE
	end

Route209_Text_Trainer5Intro:
	.string "Jogging is about rhythm.\n"
	.string "Battling is about rhythm, too!$"

Route209_Text_Trainer5Defeat:
	.string "It's a goal of sorts, I'd say!$"

Route209_Text_Trainer5Post:
	.string "If I get out of rhythm, I can't get my\n"
	.string "act together.$"

Route209_EventScript_Trainer6::
	trainerbattle_single TRAINER_SINNOH_POKE_KID_DANIELLE, Route209_Text_Trainer6Intro, Route209_Text_Trainer6Defeat
	msgbox Route209_Text_Trainer6Post, MSGBOX_AUTOCLOSE
	end

Route209_Text_Trainer6Intro:
	.string "Hi, hi!\n"
	.string "I'm a Pokémon!$"

Route209_Text_Trainer6Defeat:
	.string "So sad...\n"
	.string "So bitter...$"

Route209_Text_Trainer6Post:
	.string "I don't want to be a Trainer.\n"
	.string "I want to be a Pokémon!$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route209_EventScript_Placa1::
	msgbox Route209_Text_Placa1, MSGBOX_SIGN
	end

Route209_Text_Placa1:
	.string "Rt. 209\nHearthome City$"

Route209_EventScript_Placa2::
	msgbox Route209_Text_Placa2, MSGBOX_SIGN
	end

Route209_Text_Placa2:
	.string "Rt. 209\nSolaceon Town$"

Route209_EventScript_Placa3::
	msgbox Route209_Text_Placa3, MSGBOX_SIGN
	end

Route209_Text_Placa3:
	.string "Trainer Tips\pYou may register one of the Key\nItems in your Bag for instant use.\pSimply press the Y Button to use the\nregistered item instantly.$"

Route209_EventScript_Placa6::
	msgbox Route209_Text_Placa6, MSGBOX_SIGN
	end

Route209_Text_Placa6:
	.string "There is a broken, crumbling tower\nmade of stone...\pThere seems to be a spot that would\nbe a perfect fit for the Odd Keystone.\pWould you like to use the Odd\nKeystone?$"

Route209_EventScript_Placa7::
	msgbox Route209_Text_Placa7, MSGBOX_SIGN
	end

Route209_Text_Placa7:
	.string "There is a broken, crumbling tower\nmade of stone...\pThere seems to be a spot that would\nbe a perfect fit for the Odd Keystone.\pWould you like to use the Odd\nKeystone?$"

Route209_EventScript_Placa8::
	msgbox Route209_Text_Placa8, MSGBOX_SIGN
	end

Route209_Text_Placa8:
	.string "There is a broken, crumbling tower\nmade of stone...\pThere seems to be a spot that would\nbe a perfect fit for the Odd Keystone.\pWould you like to use the Odd\nKeystone?$"

Route209_EventScript_Placa9::
	msgbox Route209_Text_Placa9, MSGBOX_SIGN
	end

Route209_Text_Placa9:
	.string "There is a broken, crumbling tower\nmade of stone...\pThere seems to be a spot that would\nbe a perfect fit for the Odd Keystone.\pWould you like to use the Odd\nKeystone?$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route209_EventScript_Npc1::
	msgbox Route209_Text_Npc1, MSGBOX_NPC
	end

Route209_Text_Npc1:
	.string "Where departed Pokémon sleep...\nThis is the Lost Tower.$"
