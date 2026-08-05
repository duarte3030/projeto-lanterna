@ Treinadores de rota de Route26, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

Route26_MapScripts::
	.byte 0

Route26_EventScript_Jake::
	trainerbattle_single TRAINER_JOHTO_JAKE, Route26_Text_JakeSeen, Route26_Text_JakeBeaten
	msgbox Route26_Text_JakeAfter, MSGBOX_AUTOCLOSE
	end

Route26_EventScript_Gaven::
	trainerbattle_single TRAINER_JOHTO_GAVEN, Route26_Text_GavenSeen, Route26_Text_GavenBeaten
	msgbox Route26_Text_GavenAfter, MSGBOX_AUTOCLOSE
	end

Route26_EventScript_Joyce::
	trainerbattle_single TRAINER_JOHTO_JOYCE, Route26_Text_JoyceSeen, Route26_Text_JoyceBeaten
	msgbox Route26_Text_JoyceAfter, MSGBOX_AUTOCLOSE
	end

Route26_EventScript_Richard::
	trainerbattle_single TRAINER_JOHTO_RICHARD, Route26_Text_RichardSeen, Route26_Text_RichardBeaten
	msgbox Route26_Text_RichardAfter, MSGBOX_AUTOCLOSE
	end

Route26_Text_JakeSeen:
	.string "I'm making my final preparations\n"
	.string "for the POKéMON LEAGUE.$"

Route26_Text_JakeBeaten:
	.string "I blew it!$"

Route26_Text_JakeAfter:
	.string "It's going to be tough to win at\n"
	.string "the LEAGUE.\p"
	.string "I need to do some more training.\p"
	.string "I hear that the LEAGUE's ELITE\n"
	.string "FOUR are tougher than GYM LEADERS.$"

Route26_Text_GavenSeen:
	.string "By experiencing tough battles, you\n"
	.string "gain power.$"

Route26_Text_GavenBeaten:
	.string "Gaah! Life is even tougher!$"

Route26_Text_GavenAfter:
	.string "To get to POKéMON LEAGUE, you have\n"
	.string "to get through VICTORY ROAD.\p"
	.string "But VICTORY ROAD is tough.\p"
	.string "Practically nobody goes there!$"

Route26_Text_JoyceSeen:
	.string "Since you've come this far,\n"
	.string "you must be good.\p"
	.string "I'm going to give this battle\n"
	.string "everything I've got!$"

Route26_Text_JoyceBeaten:
	.string "No! I don't believe this!$"

Route26_Text_JoyceAfter:
	.string "I've defeated eight GYM LEADERS,\n"
	.string "so I was feeling confident.\p"
	.string "I'll have to try harder next time.$"

Route26_Text_RichardSeen:
	.string "Wow, look at all those BADGES!\n"
	.string "I'm impressed.\p"
	.string "But you're not satisfied by just\n"
	.string "collecting them, right?$"

Route26_Text_RichardBeaten:
	.string "Good battle!$"

Route26_Text_RichardAfter:
	.string "People and POKéMON grow from their\n"
	.string "experiences.\p"
	.string "Don't get lazy and complacent.$"
