@ Referencia de treinador de Sinnoh. Ver Pokemon Claude/SINNOH-PADRAO.md.
@ Falas vindas de pret/pokeplatinum, em ingles, como o resto do jogo.

Route203_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
Route203_EventScript_CoordEvent_Rival::
	@ TODO S4: cena da fonte, rotulo Route203_CoordEvent_Rival
	end

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

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


@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route203_EventScript_Placa1::
	msgbox Route203_Text_Placa1, MSGBOX_SIGN
	end

Route203_Text_Placa1:
	.string "Rt. 203\nJubilife City$"

Route203_EventScript_Placa2::
	msgbox Route203_Text_Placa2, MSGBOX_SIGN
	end

Route203_Text_Placa2:
	.string "Rt. 203\nOreburgh City$"

Route203_EventScript_Placa3::
	msgbox Route203_Text_Placa3, MSGBOX_SIGN
	end

Route203_Text_Placa3:
	.string "Trainer Tips!\pIf a Pokémon is about to evolve,\nit can be instantly stopped.\pPress the B Button during evolution\nto startle the Pokémon into stopping.\pThat is how evolution can be\ncanceled.$"

Route203_EventScript_Placa4::
	msgbox Route203_Text_Placa4, MSGBOX_SIGN
	end

Route203_Text_Placa4:
	.string "Trainer Tips!\pPokémon moves use energy called\nPower Points, or PP for short.\pIf the PP of moves runs low, head for\nany Pokémon Center.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route203_EventScript_Npc1::
	msgbox Route203_Text_Npc1, MSGBOX_NPC
	end

Route203_Text_Npc1:
	.string "Your favorite Pokémon should be placed\nat the top left of your party list.\pThat way, it will be the first to go out\nin a battle.$"
