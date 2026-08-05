@ Treinadores de rota de Route30, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

Route30_MapScripts::
	.byte 0

Route30_EventScript_Youngster_Joey::
	trainerbattle_single TRAINER_JOHTO_JOEY, Route30_Text_Youngster_JoeySeen, Route30_Text_Youngster_JoeyBeaten
	msgbox Route30_Text_Youngster_JoeyAfter, MSGBOX_AUTOCLOSE
	end

Route30_EventScript_Youngster_Mikey::
	trainerbattle_single TRAINER_JOHTO_MIKEY, Route30_Text_Youngster_MikeySeen, Route30_Text_Youngster_MikeyBeaten
	msgbox Route30_Text_Youngster_MikeyAfter, MSGBOX_AUTOCLOSE
	end

Route30_EventScript_Bugcatcher_Don::
	trainerbattle_single TRAINER_JOHTO_DON, Route30_Text_Bugcatcher_DonSeen, Route30_Text_Bugcatcher_DonBeaten
	msgbox Route30_Text_Bugcatcher_DonAfter, MSGBOX_AUTOCLOSE
	end

Route30_Text_Youngster_JoeySeen:
	.string "I just lost, so I'm trying to\n"
	.string "find more POKéMON.\p"
	.string "Wait! You look weak! Come on,\n"
	.string "let's battle!$"

Route30_Text_Youngster_JoeyBeaten:
	.string "Ack! I lost again!\n"
	.string "Doggone it!$"

Route30_Text_Youngster_JoeyAfter:
	.string "Do I have to have more POKéMON\n"
	.string "in order to battle better?\p"
	.string "No! I'm sticking with this one\n"
	.string "no matter what!$"

Route30_Text_Youngster_MikeySeen:
	.string "You're a POKéMON trainer,\n"
	.string "right?\p"
	.string "Then you have to battle!$"

Route30_Text_Youngster_MikeyBeaten:
	.string "That's strange.\n"
	.string "I won before.$"

Route30_Text_Youngster_MikeyAfter:
	.string "Becoming a good trainer is\n"
	.string "really tough.\p"
	.string "I'm going to battle other\n"
	.string "people to get better.$"

Route30_Text_Bugcatcher_DonSeen:
	.string "Instead of a bug POKéMON,\n"
	.string "I found a trainer!$"

Route30_Text_Bugcatcher_DonBeaten:
	.string "Argh! You're too strong!$"

Route30_Text_Bugcatcher_DonAfter:
	.string "I ran out of POKé BALLS while\n"
	.string "I was catching POKéMON.\p"
	.string "I should've bought some more…$"
