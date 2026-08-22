Route214_MapScripts::
	.byte 0

Route214_EventScript_LakeValorSign::
	msgbox Route214_Text_LakeValorSign, MSGBOX_SIGN
	end

Route214_Text_LakeValorSign:
	.string "LAKE VALOR\n"
	.string "Straight ahead.$"

Route214_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_PI_CARLOS, Route214_Text_Trainer1Intro, Route214_Text_Trainer1Defeat
	msgbox Route214_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route214_Text_Trainer1Intro:
	.string "When I toss this coin, you call it.\nHeads, we battle.\pTails, we battle!\pNow, how will this play out, my friend?\p$"

Route214_Text_Trainer1Defeat:
	.string "The coin came up tails, and like it, my\nPokémon is facedown...\n$"

Route214_Text_Trainer1Post:
	.string "I flipped a coin when I was ten.\nI decided to live in Sinnoh then.\n$"

Route214_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_BEAUTY_DEVON, Route214_Text_Trainer2Intro, Route214_Text_Trainer2Defeat
	msgbox Route214_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route214_Text_Trainer2Intro:
	.string "Oh? A little kid like you is going to\nteach me about Pokémon?\p$"

Route214_Text_Trainer2Defeat:
	.string "Wow, is that right?\n$"

Route214_Text_Trainer2Post:
	.string "There are so many kinds of Pokémon.\nI can't decide which one to pamper.\n$"


Route214_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_COLLECTOR_DOUGLAS, Route214_Text_Trainer3Intro, Route214_Text_Trainer3Defeat
	msgbox Route214_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route214_Text_Trainer3Intro:
	.string "For the sake of my collection, I\ntake on people I know I can't beat.\pThat's what a Collector does.\p$"

Route214_Text_Trainer3Defeat:
	.string "That attack right then was remarkable!\nYou ought to be proud of it!\n$"

Route214_Text_Trainer3Post:
	.string "I take pride in having Pokémon that\nothers don't.\pOh, I'm also proud about winning second\nprize in one of Jubilife TV's drawings.\n$"

Route214_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_COLLECTOR_BRADY, Route214_Text_Trainer4Intro, Route214_Text_Trainer4Defeat
	msgbox Route214_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route214_Text_Trainer4Intro:
	.string "What's that?!\pYou say you have a Pokédex?\nAn authentic one!\p$"

Route214_Text_Trainer4Defeat:
	.string "Your Pokédex fills me with such envy,\nenvy, envy...\n$"

Route214_Text_Trainer4Post:
	.string "There's all kinds of Trainers with all\nsorts of Pokémon with them.\pThe more you battle, the more your\nPokédex is filled!\n$"

Route214_EventScript_Trainer5::
	trainerbattle_single TRAINER_SINNOH_RUIN_MANIAC_BRYAN, Route214_Text_Trainer5Intro, Route214_Text_Trainer5Defeat
	msgbox Route214_Text_Trainer5Post, MSGBOX_AUTOCLOSE
	end

Route214_Text_Trainer5Intro:
	.string "Ah-ha! I found me a Trainer!\pI challenge you to battle with\nthe Pokémon I've found!\p$"

Route214_Text_Trainer5Defeat:
	.string "It's a challenge trying to win with\nPokémon one isn't familiar with...\n$"

Route214_Text_Trainer5Post:
	.string "Discovery is the treasure I seek.\nCollecting a lot is my life!\n$"

Route214_EventScript_Trainer6::
	trainerbattle_single TRAINER_SINNOH_RUIN_MANIAC_RONALD, Route214_Text_Trainer6Intro, Route214_Text_Trainer6Defeat
	msgbox Route214_Text_Trainer6Post, MSGBOX_AUTOCLOSE
	end

Route214_Text_Trainer6Intro:
	.string "I travel all over the world in search of\nmysteries.\p$"

Route214_Text_Trainer6Defeat:
	.string "Gasp... One more... Gasp...\nIt's like I went on a diet...\n$"

Route214_Text_Trainer6Post:
	.string "There are mysteries waiting for me\nto investigate around the world.\pThis is no time to be feeling sorry\nfor myself.\n$"

Route214_EventScript_Trainer7::
	trainerbattle_single TRAINER_SINNOH_COLLECTOR_JAMAL, Route214_Text_Trainer7Intro, Route214_Text_Trainer7Defeat
	msgbox Route214_Text_Trainer7Post, MSGBOX_AUTOCLOSE
	end

Route214_Text_Trainer7Intro:
	.string "To find my favorite Pokémon, I'll go\neast, west, or any which way!\p$"

Route214_Text_Trainer7Defeat:
	.string "But they're rare Pokémon!\n$"

Route214_Text_Trainer7Post:
	.string "If you're trying to find the Pokémon\nyou want, you need to go everywhere!\pNot just east and west, either.\nSouth and north are important, too!$"

Route214_EventScript_Trainer8::
	trainerbattle_single TRAINER_SINNOH_PSYCHIC_MITCHELL, Route214_Text_Trainer8Intro, Route214_Text_Trainer8Defeat
	msgbox Route214_Text_Trainer8Post, MSGBOX_AUTOCLOSE
	end

Route214_Text_Trainer8Intro:
	.string "I'd sensed the presence of a\nTrainer for a while. It was you!\p$"

Route214_Text_Trainer8Defeat:
	.string "Defeating you will be no easy matter.\n$"

Route214_Text_Trainer8Post:
	.string "Is it possible to become more\npowerful by understanding Pokémon?\n$"

Route214_EventScript_Trainer9::
	trainerbattle_single TRAINER_SINNOH_PSYCHIC_ABIGAIL, Route214_Text_Trainer9Intro, Route214_Text_Trainer9Defeat
	msgbox Route214_Text_Trainer9Post, MSGBOX_AUTOCLOSE
	end

Route214_Text_Trainer9Intro:
	.string "There!\nBehind you!\p$"

Route214_Text_Trainer9Defeat:
	.string "My plan to spook you didn't go over\nwell at all.\n$"

Route214_Text_Trainer9Post:
	.string "You might be tough, but let down\nyour guard at your own risk!\n$"


@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route214_EventScript_Placa1::
	msgbox Route214_Text_Placa1, MSGBOX_SIGN
	end

Route214_Text_Placa1:
	.string "Rt. 214\nVeilstone City$"

Route214_EventScript_Placa2::
	msgbox Route214_Text_Placa2, MSGBOX_SIGN
	end

Route214_Text_Placa2:
	.string "Rt. 214\nLake Valor$"

@ >>> porta fechada (remove_mapas_cortados.py) >>>
Route214_EventScript_PortaFechada::
	msgbox Route214_Text_PortaFechada, MSGBOX_SIGN
	end

Route214_Text_PortaFechada:
	.string "Fechado. Área em obras.$"
@ <<< porta fechada <<<
