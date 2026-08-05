@ Treinadores de rota de Route40, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

Route40_MapScripts::
	.byte 0

Route40_EventScript_Simon::
	trainerbattle_single TRAINER_JOHTO_SIMON, Route40_Text_SimonSeen, Route40_Text_SimonBeaten
	msgbox Route40_Text_SimonAfter, MSGBOX_AUTOCLOSE
	end

Route40_EventScript_Randall::
	trainerbattle_single TRAINER_JOHTO_RANDALL, Route40_Text_RandallSeen, Route40_Text_RandallBeaten
	msgbox Route40_Text_RandallAfter, MSGBOX_AUTOCLOSE
	end

Route40_EventScript_Elaine::
	trainerbattle_single TRAINER_JOHTO_ELAINE, Route40_Text_ElaineSeen, Route40_Text_ElaineBeaten
	msgbox Route40_Text_ElaineAfter, MSGBOX_AUTOCLOSE
	end

Route40_EventScript_Paula::
	trainerbattle_single TRAINER_JOHTO_PAULA, Route40_Text_PaulaSeen, Route40_Text_PaulaBeaten
	msgbox Route40_Text_PaulaAfter, MSGBOX_AUTOCLOSE
	end

Route40_Text_SimonSeen:
	.string "You have to warm up before\n"
	.string "going into the water.\p"
	.string "That's basic.$"

Route40_Text_SimonBeaten:
	.string "OK! Uncle! I give!$"

Route40_Text_SimonAfter:
	.string "CIANWOOD CITY is a good\n"
	.string "distance away from here.$"

Route40_Text_RandallSeen:
	.string "Hey, you're young and fit!\p"
	.string "Don't ride your POKéMON!\n"
	.string "Swim!$"

Route40_Text_RandallBeaten:
	.string "Uh-oh. I lost…$"

Route40_Text_RandallAfter:
	.string "Swimming exercises your\n"
	.string "entire body. It's healthy.$"

Route40_Text_ElaineSeen:
	.string "Are you going to CIANWOOD?\p"
	.string "How about a quick battle\n"
	.string "first?$"

Route40_Text_ElaineBeaten:
	.string "I lost that one!$"

Route40_Text_ElaineAfter:
	.string "I'd say I'm a better swimmer\n"
	.string "than you. Yeah!$"

Route40_Text_PaulaSeen:
	.string "No inner tube for me.\p"
	.string "I'm hanging on to a sea\n"
	.string "POKéMON!$"

Route40_Text_PaulaBeaten:
	.string "Ooh, I'm feeling dizzy!$"

Route40_Text_PaulaAfter:
	.string "While I float like this,\n"
	.string "the waves carry me along.$"
