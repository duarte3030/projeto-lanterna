Route216_MapScripts::
	.byte 0

Route216_EventScript_LodgeSign::
	msgbox Route216_Text_LodgeSign, MSGBOX_SIGN
	end

Route216_Text_LodgeSign:
	.string "SNOWBOUND LODGE\n"
	.string "Warm up before continuing on to\l"
	.string "MT. CORONET.$"

Route216_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_BLACK_BELT_PHILIP, Route216_Text_Trainer1Intro, Route216_Text_Trainer1Defeat
	msgbox Route216_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route216_Text_Trainer1Intro:
	.string "I can withstand this cold. That means\nI can take any kind of attack!\p$"

Route216_Text_Trainer1Defeat:
	.string "Huh? It's over, you say?$"

Route216_Text_Trainer1Post:
	.string "Oh, gosh, this is bad! I think I'm\n"
	.string "losing feeling all over my body!$"


Route216_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_BLAKE, Route216_Text_Trainer2Intro, Route216_Text_Trainer2Defeat
	msgbox Route216_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route216_Text_Trainer2Intro:
	.string "I'm an elite battler, but cold is\nmy nemesis!\p$"

Route216_Text_Trainer2Defeat:
	.string "But, how...?\n"
	.string "Am I weak at battling, too?$"

Route216_Text_Trainer2Post:
	.string "I'd rather be asleep in the lodge's\n"
	.string "bed...\p"
	.string "I can't take this cold...$"

Route216_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_LAURA, Route216_Text_Trainer3Intro, Route216_Text_Trainer3Defeat
	msgbox Route216_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route216_Text_Trainer3Intro:
	.string "I'm fully kitted up and equipped!\nAnytime will be fine!\p$"

Route216_Text_Trainer3Defeat:
	.string "Hunh?!$"

Route216_Text_Trainer3Post:
	.string "Perhaps I should maybe change into\n"
	.string "a more comfy outfit...$"

Route216_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_SKIER_BRADLEY, Route216_Text_Trainer4Intro, Route216_Text_Trainer4Defeat
	msgbox Route216_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route216_Text_Trainer4Intro:
	.string "I'm skiing right now, but OK.\nAs we Skiers say, “Spur thing!”\p$"

Route216_Text_Trainer4Defeat:
	.string "...I've hit an ice patch!$"

Route216_Text_Trainer4Post:
	.string "I quite enjoyed that battle!\n"
	.string "Let us meet again. Slalom!$"

Route216_EventScript_Trainer5::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_GARRETT, Route216_Text_Trainer5Intro, Route216_Text_Trainer5Defeat
	msgbox Route216_Text_Trainer5Post, MSGBOX_AUTOCLOSE
	end

Route216_Text_Trainer5Intro:
	.string "I always play for keeps!\nThis isn't practice!\p$"

Route216_Text_Trainer5Defeat:
	.string "Good job!\n"
	.string "That was an excellent battle.$"

Route216_Text_Trainer5Post:
	.string "If you don't play for keeps, you'll\n"
	.string "lose battles you should be dominating.$"

Route216_EventScript_Trainer6::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_MARIA, Route216_Text_Trainer6Intro, Route216_Text_Trainer6Defeat
	msgbox Route216_Text_Trainer6Post, MSGBOX_AUTOCLOSE
	end

Route216_Text_Trainer6Intro:
	.string "To be ready to answer any call!\nTo be ready to accept any challenge!\pThat is the way of a Trainer!\p$"

Route216_Text_Trainer6Defeat:
	.string "Oh, yeah?\n"
	.string "Eat snowball, punk!$"

Route216_Text_Trainer6Post:
	.string "You can make all the preparations in\n"
	.string "the world, but if it doesn't work, it\p"
	.string "doesn't work.$"

Route216_EventScript_Trainer7::
	trainerbattle_single TRAINER_SINNOH_SKIER_KAITLYN, Route216_Text_Trainer7Intro, Route216_Text_Trainer7Defeat
	msgbox Route216_Text_Trainer7Post, MSGBOX_AUTOCLOSE
	end

Route216_Text_Trainer7Intro:
	.string "The fun things about winter!\nOne, skiing! Two, Pokémon!\p$"

Route216_Text_Trainer7Defeat:
	.string "Snivel...$"

Route216_Text_Trainer7Post:
	.string "If it was skiing, I wouldn't lose.\n"
	.string "I should go ski with my Pokémon...$"

Route216_EventScript_Trainer8::
	trainerbattle_single TRAINER_SINNOH_SKIER_EDWARD, Route216_Text_Trainer8Intro, Route216_Text_Trainer8Defeat
	msgbox Route216_Text_Trainer8Post, MSGBOX_AUTOCLOSE
	end

Route216_Text_Trainer8Intro:
	.string "Are you a novice?\nOr around midlevel?\p$"

Route216_Text_Trainer8Defeat:
	.string "I never expected you to be an\n"
	.string "expert...$"

Route216_Text_Trainer8Post:
	.string "You know how to play your Pokémon\n"
	.string "with an edge!$"

Route216_EventScript_Trainer9::
	trainerbattle_single TRAINER_SINNOH_SKIER_ANDREA, Route216_Text_Trainer9Intro, Route216_Text_Trainer9Defeat
	msgbox Route216_Text_Trainer9Post, MSGBOX_AUTOCLOSE
	end

Route216_Text_Trainer9Intro:
	.string "How do you expect to battle in this\nheavy snow?\p$"

Route216_Text_Trainer9Defeat:
	.string "The winds of victory shifted...$"

Route216_Text_Trainer9Post:
	.string "It's so cold here, but here you are,\n"
	.string "so full of energy.\p"
	.string "I guess you kids are made tougher\n"
	.string "than people my age.$"


@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route216_EventScript_Placa1::
	msgbox Route216_Text_Placa1, MSGBOX_SIGN
	end

Route216_Text_Placa1:
	.string "Rt. 216\nMt. Coronet$"

Route216_EventScript_Placa2::
	msgbox Route216_Text_Placa2, MSGBOX_SIGN
	end

Route216_Text_Placa2:
	.string "Snowbound Lodge\nA Warm Bed and Little Else$"
