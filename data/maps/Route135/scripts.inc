@ Route135: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 0.59) por dev_scripts/copia_planta_ex.py.

Route135_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 0.59), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
Route135_EventScript_ExTrainer0::
	trainerbattle_single TRAINER_HOENNEX_ROUTE135_SANDY, Route135_Text_ExTrainer0Intro, Route135_Text_ExTrainer0Defeat
	msgbox Route135_Text_ExTrainer0PostBattle, MSGBOX_AUTOCLOSE
	end

Route135_Text_ExTrainer0Intro:
	.string "Watch out for my bear POKéMON!$"

Route135_Text_ExTrainer0Defeat:
	.string "Hey wait a second what’s a bear?$"

Route135_Text_ExTrainer0PostBattle:
	.string "Do you know how to make a campfire?$"

Route135_EventScript_ExTrainer1::
	trainerbattle_single TRAINER_HOENNEX_ROUTE135_KENNETH, Route135_Text_ExTrainer1Intro, Route135_Text_ExTrainer1Defeat
	msgbox Route135_Text_ExTrainer1PostBattle, MSGBOX_AUTOCLOSE
	end

Route135_Text_ExTrainer1Intro:
	.string "I like to collect feathers!$"

Route135_Text_ExTrainer1Defeat:
	.string "You got my feathers everywhere!$"

Route135_Text_ExTrainer1PostBattle:
	.string "Why don’t people have feathers?$"

Route135_EventScript_ExNpc2::
	msgbox Route135_Text_ExNpc2, MSGBOX_NPC
	end

Route135_Text_ExNpc2:
	.string "The beach is just on the other side of\n"
	.string "this ROUTE, but I can’t cross all this\l"
	.string "tall grass without a POKéMON.\p"
	.string "It’s so unfair!$"

Route135_EventScript_ExSign0::
	msgbox Route135_Text_ExSign0, MSGBOX_SIGN
	end

Route135_Text_ExSign0:
	.string "ROUTE 103.5\n"
	.string "{LEFT_ARROW} ROUTE 104.$"

Route135_EventScript_ExSign1::
	msgbox Route135_Text_ExSign1, MSGBOX_SIGN
	end

Route135_Text_ExSign1:
	.string "ROUTE 103.5\n"
	.string "{RIGHT_ARROW} PETALBURG CITY.$"

