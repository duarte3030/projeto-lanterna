@ Treinadores de rota de Route36, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

Route36_MapScripts::
	.byte 0

Route36_EventScript_Mark::
	trainerbattle_single TRAINER_JOHTO_MARK, Route36_Text_MarkSeen, Route36_Text_MarkBeaten
	msgbox Route36_Text_MarkAfter, MSGBOX_AUTOCLOSE
	end

Route36_EventScript_Schoolboy::
	trainerbattle_single TRAINER_JOHTO_ALAN, Route36_Text_SchoolboySeen, Route36_Text_SchoolboyBeaten
	msgbox Route36_Text_SchoolboyAfter, MSGBOX_AUTOCLOSE
	end

Route36_Text_MarkSeen:
	.string "I'm going to read your thoughts!$"

Route36_Text_MarkBeaten:
	.string "I misread you!$"

Route36_Text_MarkAfter:
	.string "I'd be strong if only I could tell\n"
	.string "what my opponent was thinking.$"

Route36_Text_SchoolboySeen:
	.string "Thanks to my studies, I'm ready\n"
	.string "for any POKéMON!$"

Route36_Text_SchoolboyBeaten:
	.string "Oops! Computation error?$"

Route36_Text_SchoolboyAfter:
	.string "Darn. I study five hours a day too.\p"
	.string "There's more to learning than just\n"
	.string "reading books.$"

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

Route36_EventScript_Sign::
	lock
	msgbox Route36_Text_Sign_RuinsNorth, MSGBOX_SIGN
	closemessage
	release
	end

Route36_EventScript_Sign2::
	lock
	msgbox Route36_Text_Tips1, MSGBOX_SIGN
	closemessage
	release
	end

Route36_Text_Sign_RuinsNorth::
	.string "RUINS OF ALPH\n"
	.string "NORTH ENTRANCE$"

Route36_Text_Tips1::
	.string "TRAINER TIPS\n"
	.string "POKéMON stats vary--even within\l"
	.string "the same species.\p"
	.string "Their stats may be similar at first.\p"
	.string "However, differences will become\n"
	.string "pronounced as the POKéMON grow.$"
