@ Route122_Ex26_1: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 26.1) por dev_scripts/copia_planta_ex.py.

Route122_Ex26_1_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 26.1), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
Route122_Ex26_1_EventScript_ExTrainer0::
	trainerbattle_single TRAINER_HOENNEX_ROUTE122_EX26_1_AUSTIN, Route122_Ex26_1_Text_ExTrainer0Intro, Route122_Ex26_1_Text_ExTrainer0Defeat
	msgbox Route122_Ex26_1_Text_ExTrainer0PostBattle, MSGBOX_AUTOCLOSE
	end

Route122_Ex26_1_Text_ExTrainer0Intro:
	.string "Theres no rules against battling in this\n"
	.string "town!$"

Route122_Ex26_1_Text_ExTrainer0Defeat:
	.string "Crushed!$"

Route122_Ex26_1_Text_ExTrainer0PostBattle:
	.string "I’ve never been good to following rules.\p"
	.string "That’s why this town’s perfect!$"

Route122_Ex26_1_EventScript_ExTrainer1::
	trainerbattle_single TRAINER_HOENNEX_ROUTE122_EX26_1_RAYLER, Route122_Ex26_1_Text_ExTrainer1Intro, Route122_Ex26_1_Text_ExTrainer1Defeat
	msgbox Route122_Ex26_1_Text_ExTrainer1PostBattle, MSGBOX_AUTOCLOSE
	end

Route122_Ex26_1_Text_ExTrainer1Intro:
	.string "My KADABRA is reacting oddly to you.$"

Route122_Ex26_1_Text_ExTrainer1Defeat:
	.string "I sense power from you.$"

Route122_Ex26_1_Text_ExTrainer1PostBattle:
	.string "I can see a bright future for you.$"

Route122_Ex26_1_EventScript_ExNpc2::
	msgbox Route122_Ex26_1_Text_ExNpc2, MSGBOX_NPC
	end

Route122_Ex26_1_Text_ExNpc2:
	.string "My dad sometimes catches POKéMON in\n"
	.string "the SAFARI ZONE.\p"
	.string "Sometimes he breaks the rules and\n"
	.string "battles there...$"

