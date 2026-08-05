@ TORRE RADIO de GOLDENROD, 3F. Portado de
@ fontes-mapas/hns/data/maps/GoldenrodCity_RadioTower_3F/scripts.inc.
@ ponytail: o cientista MARC e o terceiro grunt sairam por falta de vaga de
@ treinador. A moca do 3F e quem manda o jogador para o 5F, e a fala dela nao
@ depende mais de var: e sempre a de antes do resgate.

GoldenrodCity_RadioTower_3F_MapScripts::
	.byte 0

RadioTower3F_EventScript_Grunt1::
	trainerbattle_single TRAINER_JOHTO_ROCKET_GRUNT_RADIO_3F_1, RadioTower3F_Text_Grunt1Seen, RadioTower3F_Text_Grunt1Beaten
	msgbox RadioTower3F_Text_Grunt1After, MSGBOX_AUTOCLOSE
	end

RadioTower3F_EventScript_Grunt2::
	trainerbattle_single TRAINER_JOHTO_ROCKET_GRUNT_RADIO_3F_2, RadioTower3F_Text_Grunt2Seen, RadioTower3F_Text_Grunt2Beaten
	msgbox RadioTower3F_Text_Grunt2After, MSGBOX_AUTOCLOSE
	end

RadioTower3F_EventScript_Cooltrainer::
	lock
	faceplayer
	msgbox RadioTower3F_Text_PleaseSave, MSGBOX_DEFAULT
	closemessage
	release
	end

RadioTower3F_Text_Grunt1Seen:
	.string "I've been given strict orders.\p"
	.string "I'm to crush anyone who challenges\n"
	.string "TEAM ROCKET!$"

RadioTower3F_Text_Grunt1Beaten:
	.string "What?!$"

RadioTower3F_Text_Grunt1After:
	.string "I failed in my duties…\p"
	.string "ARCHER will be so upset…$"

RadioTower3F_Text_Grunt2Seen:
	.string "It feels great ordering POKéMON\n"
	.string "to commit crimes.$"

RadioTower3F_Text_Grunt2Beaten:
	.string "You're kidding!$"

RadioTower3F_Text_Grunt2After:
	.string "I feel lousy over losing!\p"
	.string "Darn it! I hate useless POKéMON!$"

RadioTower3F_Text_PleaseSave:
	.string "The TEAM ROCKET boss has locked\n"
	.string "himself in.\p"
	.string "But the DIRECTOR can open it.\p"
	.string "He's up on the fifth floor.\p"
	.string "Please save him!$"
