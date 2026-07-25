@ Referencia de treinador de Sinnoh. Ver Pokemon Claude/SINNOH-PADRAO.md.
@ Falas vindas de pret/pokeplatinum, em ingles, como o resto do jogo.

Route203_MapScripts::
	.byte 0

Route203_EventScript_Lass::
	msgbox Route203_Text_Lass, MSGBOX_NPC
	end

Route203_EventScript_Sebastian::
	lock
	faceplayer
	msgbox Route203_Text_Sebastian, MSGBOX_DEFAULT
	release
	end

Route203_EventScript_Michael::
	lock
	faceplayer
	msgbox Route203_Text_Michael, MSGBOX_DEFAULT
	release
	end

Route203_EventScript_Kaitlin::
	msgbox Route203_Text_Kaitlin, MSGBOX_NPC
	end

Route203_EventScript_Dallas::
	lock
	faceplayer
	msgbox Route203_Text_Dallas, MSGBOX_DEFAULT
	release
	end

Route203_Text_Lass:
	.string "OREBURGH CITY is west of here.\n"
	.string "They say the GYM there is tough.$"

Route203_Text_Sebastian:
	.string "JUBILIFE CITY was amazing! So\n"
	.string "many people and POKéMON!$"

Route203_Text_Michael:
	.string "I like to walk through the tall\n"
	.string "grass looking for wild POKéMON.$"

Route203_Text_Kaitlin:
	.string "I got lost wandering around this\n"
	.string "route. It's bigger than it looks!$"

Route203_Text_Dallas:
	.string "The OREBURGH GATE is just ahead.\n"
	.string "It leads straight to the mine.$"

Route203_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_YOUNGSTER_SEBASTIAN, Route203_Text_Trainer1Intro, Route203_Text_Trainer1Defeat
	msgbox Route203_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route203_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_YOUNGSTER_MICHAEL, Route203_Text_Trainer2Intro, Route203_Text_Trainer2Defeat
	msgbox Route203_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route203_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_LASS_KAITLIN, Route203_Text_Trainer3Intro, Route203_Text_Trainer3Defeat
	msgbox Route203_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route203_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_YOUNGSTER_DALLAS, Route203_Text_Trainer4Intro, Route203_Text_Trainer4Defeat
	msgbox Route203_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route203_EventScript_Trainer5::
	trainerbattle_single TRAINER_SINNOH_LASS_MADELINE, Route203_Text_Trainer5Intro, Route203_Text_Trainer5Defeat
	msgbox Route203_Text_Trainer5Post, MSGBOX_AUTOCLOSE
	end

Route203_Text_Trainer1Intro:
	.string "Before I challenge the Pokémon Gym\nLeader, I'll test my strength on you!$"

Route203_Text_Trainer1Defeat:
	.string "I guess it means I'm not ready for\nthe Gym challenge yet...$"

Route203_Text_Trainer1Post:
	.string "I guess if you don't have a single\nGym Badge, you're a total nobody...$"

Route203_Text_Trainer2Intro:
	.string "I get my get-up-and-go from my\nPokémon!Here we go!\nKRICKETOT! ZUBAT!$"

Route203_Text_Trainer2Defeat:
	.string "Ack! My Pokémon...$"

Route203_Text_Trainer2Post:
	.string "Keep out of the grass or dodge the\neyes of Trainers...?I always have a tough time choosing.$"

Route203_Text_Trainer3Intro:
	.string "I found a Trainer while looking for\nsome Pokémon!$"

Route203_Text_Trainer3Defeat:
	.string "Hunh? You're finished so soon?$"

Route203_Text_Trainer3Post:
	.string "I walk through tall grass until I\nfind the Pokémon I want.$"

Route203_Text_Trainer4Intro:
	.string "I'm never apart from my SHINX.\nOur bond is strong!$"

Route203_Text_Trainer4Defeat:
	.string "So sad...\nAnd so crushed...$"

Route203_Text_Trainer4Post:
	.string "I don't bear grudges over losing.\nBut I promise I'll get tougher!$"

Route203_Text_Trainer5Intro:
	.string "I got a nifty-keen Gym Badge from\nthe Gym Leader in Oreburgh City!$"

Route203_Text_Trainer5Defeat:
	.string "Oh, I lost! Lalala!$"

Route203_Text_Trainer5Post:
	.string "I'm collecting lots of Gym Badges.\nThey're so sparkly and pretty!$"

