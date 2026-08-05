@ Referencia de treinador de Sinnoh. Ver Pokemon Claude/SINNOH-PADRAO.md.
@ Falas vindas de pret/pokeplatinum, em ingles, como o resto do jogo.

Route226_MapScripts::
	.byte 0

Route226_EventScript_SwimmerLydia::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_LYDIA, Route226_Text_SwimmerLydiaIntro, Route226_Text_SwimmerLydiaDefeat
	msgbox Route226_Text_SwimmerLydiaPost, MSGBOX_AUTOCLOSE
	end

Route226_EventScript_AceTrainerGraham::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_GRAHAM, Route226_Text_AceTrainerGrahamIntro, Route226_Text_AceTrainerGrahamDefeat
	msgbox Route226_Text_AceTrainerGrahamPost, MSGBOX_AUTOCLOSE
	end

Route226_EventScript_BirdKeeperGeneva::
	trainerbattle_single TRAINER_SINNOH_BIRD_KEEPER_GENEVA, Route226_Text_BirdKeeperGenevaIntro, Route226_Text_BirdKeeperGenevaDefeat
	msgbox Route226_Text_BirdKeeperGenevaPost, MSGBOX_AUTOCLOSE
	end

Route226_EventScript_SwimmerWade::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_WADE, Route226_Text_SwimmerWadeIntro, Route226_Text_SwimmerWadeDefeat
	msgbox Route226_Text_SwimmerWadePost, MSGBOX_AUTOCLOSE
	end

Route226_EventScript_DragonTamerStanley::
	trainerbattle_single TRAINER_SINNOH_DRAGON_TAMER_STANLEY, Route226_Text_DragonTamerStanleyIntro, Route226_Text_DragonTamerStanleyDefeat
	msgbox Route226_Text_DragonTamerStanleyPost, MSGBOX_AUTOCLOSE
	end

Route226_EventScript_SignSurvivalArea::
	msgbox Route226_Text_SignSurvivalArea, MSGBOX_SIGN
	end

Route226_Text_SwimmerLydiaIntro:
	.string "I want to be with my water Pokémon!\n"
	.string "That's why I swim!$"

Route226_Text_SwimmerLydiaDefeat:
	.string "Glub glub...\n"
	.string "I'm sinking...$"

Route226_Text_SwimmerLydiaPost:
	.string "I thought that everyone would be all\n"
	.string "dedicated to training out here.\p"
	.string "But most people are really laid back.\n"
	.string "It's not like what I imagined.\p"
	.string "I guess being with Pokémon, people get\n"
	.string "all mellowed out.$"

Route226_Text_AceTrainerGrahamIntro:
	.string "I took great pains raising my partners.\n"
	.string "I'll show you how strong I made them!$"

Route226_Text_AceTrainerGrahamDefeat:
	.string "It needs to be leveled more?!$"

Route226_Text_AceTrainerGrahamPost:
	.string "My Pokémon...\p"
	.string "They're the first friends I ever\n"
	.string "caught. They mean everything to me!$"

Route226_Text_BirdKeeperGenevaIntro:
	.string "My Pokémon grew up in the arms of\n"
	.string "Mother Nature. They're tough!$"

Route226_Text_BirdKeeperGenevaDefeat:
	.string "How could you be tougher than\n"
	.string "Mother Nature?$"

Route226_Text_BirdKeeperGenevaPost:
	.string "Most of the time, my Pokémon return\n"
	.string "to their Poké Balls right away.\p"
	.string "But sometimes, they just fall asleep\n"
	.string "on top of my head. That gets messy.$"

Route226_Text_SwimmerWadeIntro:
	.string "Me and my Pokémon are pumped up\n"
	.string "and ready to go all out!$"

Route226_Text_SwimmerWadeDefeat:
	.string "Our muscles are deflating...$"

Route226_Text_SwimmerWadePost:
	.string "Overwhelm with our dazzling physiques!\n"
	.string "That was our game plan...$"

Route226_Text_DragonTamerStanleyIntro:
	.string "How do you do?\n"
	.string "I'm Stanley, and I'm a Dragon Tamer.\p"
	.string "What do you say we let our Pokémon\n"
	.string "have it out? Sound OK to you?$"

Route226_Text_DragonTamerStanleyDefeat:
	.string "Victory!\n"
	.string "That is, victory for you...$"

Route226_Text_DragonTamerStanleyPost:
	.string "It seems to me, there's this certain\n"
	.string "image that goes with a Dragon Tamer.\p"
	.string "But me, I'd much sooner take it easy,\n"
	.string "take it slow, and take it my own way.\p"
	.string "I figure there's more than my style\n"
	.string "that I need to work on first.$"

Route226_Text_SignSurvivalArea:
	.string "SURVIVAL AREA\n"
	.string "This way, to the west.$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route226_EventScript_Placa1::
	msgbox Route226_Text_Placa1, MSGBOX_SIGN
	end

Route226_Text_Placa1:
	.string "Rt. 226\nSurvival Area$"

Route226_EventScript_Placa2::
	msgbox Route226_Text_Placa2, MSGBOX_SIGN
	end

Route226_Text_Placa2:
	.string "Rt. 227\nRt. 228$"
