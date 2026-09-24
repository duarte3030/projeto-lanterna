@ Route138: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 0.62) por dev_scripts/copia_planta_ex.py.

Route138_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 0.62), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
Route138_EventScript_ExTrainer4::
	trainerbattle_single TRAINER_HOENNEX_ROUTE138_ABIGAIL, Route138_Text_ExTrainer4Intro, Route138_Text_ExTrainer4Defeat
	msgbox Route138_Text_ExTrainer4PostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_ExTrainer4Intro:
	.string "The mountains are good for GRASS\n"
	.string "POKéMON!$"

Route138_Text_ExTrainer4Defeat:
	.string "The mountains must be good for your\n"
	.string "POKéMON!$"

Route138_Text_ExTrainer4PostBattle:
	.string "I wished to meet strong POKéMON here\n"
	.string "as a kid.\p"
	.string "When I grew up, somehow all the POKéMON\n"
	.string "got stronger!$"

Route138_EventScript_ExTrainer5::
	trainerbattle_single TRAINER_HOENNEX_ROUTE138_JED, Route138_Text_ExTrainer5Intro, Route138_Text_ExTrainer5Defeat
	msgbox Route138_Text_ExTrainer5PostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_ExTrainer5Intro:
	.string "Welcome to the great north jungle!$"

Route138_Text_ExTrainer5Defeat:
	.string "Ho ho what a jungle smash!$"

Route138_Text_ExTrainer5PostBattle:
	.string "POKéMON are oddly strong here.$"

Route138_EventScript_ExTrainer8::
	trainerbattle_single TRAINER_HOENNEX_ROUTE138_BOB, Route138_Text_ExTrainer8Intro, Route138_Text_ExTrainer8Defeat
	msgbox Route138_Text_ExTrainer8PostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_ExTrainer8Intro:
	.string "Say, where are we?\n"
	.string "I don’t recognize this route?$"

Route138_Text_ExTrainer8Defeat:
	.string "I’m so lost...$"

Route138_Text_ExTrainer8PostBattle:
	.string "I keep going north but I can’t find\n"
	.string "MAUVILLE...$"


@ Eventos novos do Pokémon Emerald EX (mapa 0.62), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
Route138_EventScript_ExTrainer3::
	trainerbattle_single TRAINER_HOENNEX_ROUTE138_CHARITY, Route138_Text_ExTrainer3Intro, Route138_Text_ExTrainer3Defeat
	msgbox Route138_Text_ExTrainer3PostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_ExTrainer3Intro:
	.string "They say wishes come true here.$"

Route138_Text_ExTrainer3Defeat:
	.string "Feisty child!$"

Route138_Text_ExTrainer3PostBattle:
	.string "I’m here to wish that my husband would\n"
	.string "buy me something nice.$"

