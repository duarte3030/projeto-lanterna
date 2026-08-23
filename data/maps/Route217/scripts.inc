Route217_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
@ BLOQUEADO (S6, 18/08/2026). Route217_CoordEvent_Maylene (script 4) e so
@ dialogo (a lider do ginasio de Veilstone cruzando a Route 217 a pe rumo a
@ Snowpoint, sem batalha), mas precisa de LOCALID_MAYLENE novo e a fonte
@ esconde ele por FLAG_HIDE_ROUTE_217_MAYLENE. Essa flag NAO esta no censo
@ do S1 (`python3 -c` em dev_scripts/maquina_sinnoh.json e fila_b6.json: zero
@ ocorrencias de MAYLENE), diferente de todo o resto dos 247 grupos de
@ hidden_flag; a leitura mais provavel e que o gerador excluiu de proposito
@ objeto de lider de ginasio (mesma familia do time/batalha, decisao 2 do
@ Gui, fora desta obra). Trazer o objeto sem flag autorizada plantava
@ bloqueio permanente (regra do plano) ou obrigava a inventar flag fora do
@ orcamento. Fecho tambem cortado por seguranca: a fonte termina com SetFlag
@ FLAG_HIDE_VEILSTONE_CITY_GYM_MAYLENE (evento de OUTRO mapa, VeilstoneCity_
@ Gym, fora do meu escopo nesta leva). Volta ao plano para autorizacao da
@ flag antes de escrever.
Route217_EventScript_CoordEvent_Maylene::
	end

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

Route217_EventScript_ArrowSign::
	msgbox Route217_Text_ArrowSign, MSGBOX_SIGN
	end

Route217_Text_ArrowSign:
	.string "SNOWPOINT CITY\n"
	.string "Straight ahead.$"

Route217_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_NINJA_BOY_MATTHEW, Route217_Text_Trainer1Intro, Route217_Text_Trainer1Defeat
	msgbox Route217_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route217_Text_Trainer1Intro:
	.string "Poof!\pYou've got a good eye spotting me!\p$"

Route217_Text_Trainer1Defeat:
	.string "You also saw through my weak\n"
	.string "spots...$"

Route217_Text_Trainer1Post:
	.string "I'll play with my Pokémon--even in a\n"
	.string "blizzard!$"

Route217_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_NINJA_BOY_ETHAN, Route217_Text_Trainer2Intro, Route217_Text_Trainer2Defeat
	msgbox Route217_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route217_Text_Trainer2Intro:
	.string "There are several clans of ninjas.\nAre you from the Iga clan? Or Kouga?\p$"

Route217_Text_Trainer2Defeat:
	.string "I'm not much of a ninja either way...$"

Route217_Text_Trainer2Post:
	.string "I wonder why everyone stops being\n"
	.string "a ninja when they grow up?$"

Route217_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_BLACK_BELT_LUKE, Route217_Text_Trainer3Intro, Route217_Text_Trainer3Defeat
	msgbox Route217_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route217_Text_Trainer3Intro:
	.string "I dress light wherever I go.\nHiyah!\p$"

Route217_Text_Trainer3Defeat:
	.string "Achoo!$"

Route217_Text_Trainer3Post:
	.string "Maybe I'll dress warm and come back.\n"
	.string "Hiyah!$"


Route217_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_SKIER_SHAWN, Route217_Text_Trainer4Intro, Route217_Text_Trainer4Defeat
	msgbox Route217_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route217_Text_Trainer4Intro:
	.string "I'll show you the techniques I had\ndrummed into me at ski school!\p$"

Route217_Text_Trainer4Defeat:
	.string "I don't believe it...\n"
	.string "My techniques were rebuffed...$"

Route217_Text_Trainer4Post:
	.string "Maybe I should've studied at the\n"
	.string "Trainers' school instead...$"

Route217_EventScript_Trainer5::
	trainerbattle_single TRAINER_SINNOH_SKIER_LEXIE, Route217_Text_Trainer5Intro, Route217_Text_Trainer5Defeat
	msgbox Route217_Text_Trainer5Post, MSGBOX_AUTOCLOSE
	end

Route217_Text_Trainer5Intro:
	.string "I've been skiing with Pokémon since\nI was just five years old.\p$"

Route217_Text_Trainer5Defeat:
	.string "Hunh, what...?\n"
	.string "I repeat, hunh, what...?$"

Route217_Text_Trainer5Post:
	.string "The scenery doesn't change very much\n"
	.string "around here. Don't go getting lost!$"

Route217_EventScript_Trainer6::
	trainerbattle_single TRAINER_SINNOH_SKIER_BJORN, Route217_Text_Trainer6Intro, Route217_Text_Trainer6Defeat
	msgbox Route217_Text_Trainer6Post, MSGBOX_AUTOCLOSE
	end

Route217_Text_Trainer6Intro:
	.string "We Skiers feel Mother Nature through\nthe soles of our feet!\p$"

Route217_Text_Trainer6Defeat:
	.string "I got a good taste of your power!$"

Route217_Text_Trainer6Post:
	.string "Trainers get an appreciation of life\n"
	.string "through Pokémon. At least I think so.$"

Route217_EventScript_Trainer7::
	trainerbattle_single TRAINER_SINNOH_SKIER_MADISON, Route217_Text_Trainer7Intro, Route217_Text_Trainer7Defeat
	msgbox Route217_Text_Trainer7Post, MSGBOX_AUTOCLOSE
	end

Route217_Text_Trainer7Intro:
	.string "Rainy days make me feel blue...\pBut the instant it starts to snow,\nI'm as happy as can be!\p$"

Route217_Text_Trainer7Defeat:
	.string "The conditions weren't very good.$"

Route217_Text_Trainer7Post:
	.string "Can any of your Pokémon use that\n"
	.string "hidden move to climb cliffs?$"

Route217_EventScript_Trainer8::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_DALTON, Route217_Text_Trainer8Intro, Route217_Text_Trainer8Defeat
	msgbox Route217_Text_Trainer8Post, MSGBOX_AUTOCLOSE
	end

Route217_Text_Trainer8Intro:
	.string "This cold is but nothing compared\nto the fire that burns in my heart!\p$"

Route217_Text_Trainer8Defeat:
	.string "Your heart burns as hot as mine!$"

Route217_Text_Trainer8Post:
	.string "The weather clears up sometimes.\n"
	.string "The view is breathtaking then.$"

Route217_EventScript_Trainer9::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_OLIVIA, Route217_Text_Trainer9Intro, Route217_Text_Trainer9Defeat
	msgbox Route217_Text_Trainer9Post, MSGBOX_AUTOCLOSE
	end

Route217_Text_Trainer9Intro:
	.string "Wh-what is it?\nP-Pokémon battle?!\p$"

Route217_Text_Trainer9Defeat:
	.string "Whew...\n"
	.string "You are alive, aren't you?$"

Route217_Text_Trainer9Post:
	.string "Around these parts, perhaps because\n"
	.string "of all the snow, there are many\p"
	.string "folktales of hauntings...$"


@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route217_EventScript_Placa1::
	msgbox Route217_Text_Placa1, MSGBOX_SIGN
	end

Route217_Text_Placa1:
	.string "Rt. 217\nLake Acuity$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route217_EventScript_Npc1::
	msgbox Route217_Text_Npc1, MSGBOX_NPC
	end

Route217_Text_Npc1:
	.string "I'm using the Dowsing Machine on\nmy Pokétch.\pI'm looking for things buried under\nthe snow.$"
