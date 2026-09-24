Route133_MapScripts::
	.byte 0

Route133_EventScript_Franklin::
	trainerbattle_single TRAINER_FRANKLIN, Route133_Text_FranklinIntro, Route133_Text_FranklinDefeat
	msgbox Route133_Text_FranklinPostBattle, MSGBOX_AUTOCLOSE
	end

Route133_EventScript_Debra::
	trainerbattle_single TRAINER_DEBRA, Route133_Text_DebraIntro, Route133_Text_DebraDefeat
	msgbox Route133_Text_DebraPostBattle, MSGBOX_AUTOCLOSE
	end

Route133_EventScript_Linda::
	trainerbattle_single TRAINER_LINDA, Route133_Text_LindaIntro, Route133_Text_LindaDefeat
	msgbox Route133_Text_LindaPostBattle, MSGBOX_AUTOCLOSE
	end

Route133_EventScript_Warren::
	trainerbattle_single TRAINER_WARREN, Route133_Text_WarrenIntro, Route133_Text_WarrenDefeat
	msgbox Route133_Text_WarrenPostBattle, MSGBOX_AUTOCLOSE
	end

Route133_EventScript_Beck::
	trainerbattle_single TRAINER_BECK, Route133_Text_BeckIntro, Route133_Text_BeckDefeat
	msgbox Route133_Text_BeckPostBattle, MSGBOX_AUTOCLOSE
	end

Route133_EventScript_Mollie::
	trainerbattle_single TRAINER_MOLLIE, Route133_Text_MollieIntro, Route133_Text_MollieDefeat
	msgbox Route133_Text_MolliePostBattle, MSGBOX_AUTOCLOSE
	end

Route133_EventScript_Conor::
	trainerbattle_single TRAINER_CONOR, Route133_Text_ConorIntro, Route133_Text_ConorDefeat
	msgbox Route133_Text_ConorPostBattle, MSGBOX_AUTOCLOSE
	end


@ Eventos novos do Pokémon Emerald EX (mapa 0.50), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
Route133_EventScript_ExTrainer11::
	trainerbattle_single TRAINER_HOENNEX_ROUTE133_MIRIAM, Route133_Text_ExTrainer11Intro, Route133_Text_ExTrainer11Defeat
	msgbox Route133_Text_ExTrainer11PostBattle, MSGBOX_AUTOCLOSE
	end

Route133_Text_ExTrainer11Intro:
	.string "Have you seen the sunrise here?$"

Route133_Text_ExTrainer11Defeat:
	.string "What an exquisite showing.$"

Route133_Text_ExTrainer11PostBattle:
	.string "I swam out here before dawn to see the\n"
	.string "sunrise.$"

