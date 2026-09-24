@ Route122_Ex26_2: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 26.2) por dev_scripts/copia_planta_ex.py.

Route122_Ex26_2_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 26.2), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
Route122_Ex26_2_EventScript_ExTrainer0::
	trainerbattle_single TRAINER_HOENNEX_ROUTE122_EX26_2_DAMARIS, Route122_Ex26_2_Text_ExTrainer0Intro, Route122_Ex26_2_Text_ExTrainer0Defeat
	msgbox Route122_Ex26_2_Text_ExTrainer0PostBattle, MSGBOX_AUTOCLOSE
	end

Route122_Ex26_2_Text_ExTrainer0Intro:
	.string "Train with me!$"

Route122_Ex26_2_Text_ExTrainer0Defeat:
	.string "Superb!$"

Route122_Ex26_2_Text_ExTrainer0PostBattle:
	.string "I train every day!$"

Route122_Ex26_2_EventScript_ExTrainer1::
	trainerbattle_single TRAINER_HOENNEX_ROUTE122_EX26_2_COLIN, Route122_Ex26_2_Text_ExTrainer1Intro, Route122_Ex26_2_Text_ExTrainer1Defeat
	msgbox Route122_Ex26_2_Text_ExTrainer1PostBattle, MSGBOX_AUTOCLOSE
	end

Route122_Ex26_2_Text_ExTrainer1Intro:
	.string "Let’s harden our fists!$"

Route122_Ex26_2_Text_ExTrainer1Defeat:
	.string "Fists of fury!$"

Route122_Ex26_2_Text_ExTrainer1PostBattle:
	.string "Keep training, never stop!$"

