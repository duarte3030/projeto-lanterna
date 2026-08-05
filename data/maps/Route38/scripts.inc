@ Treinadores de rota de Route38, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

Route38_MapScripts::
	.byte 0

Route38_EventScript_Toby::
	trainerbattle_single TRAINER_JOHTO_TOBY, Route38_Text_TobySeen, Route38_Text_TobyBeaten
	msgbox Route38_Text_TobyAfter, MSGBOX_AUTOCLOSE
	end

Route38_EventScript_Chad::
	trainerbattle_single TRAINER_JOHTO_CHAD, Route38_Text_ChadSeen, Route38_Text_ChadBeaten
	msgbox Route38_Text_ChadAfter, MSGBOX_AUTOCLOSE
	end

Route38_EventScript_Dana::
	trainerbattle_single TRAINER_JOHTO_DANA, Route38_Text_DanaSeen, Route38_Text_DanaBeaten
	msgbox Route38_Text_DanaAfter, MSGBOX_AUTOCLOSE
	end

Route38_EventScript_Valerie::
	trainerbattle_single TRAINER_JOHTO_VALERIE, Route38_Text_ValerieSeen, Route38_Text_ValerieBeaten
	msgbox Route38_Text_ValerieAfter, MSGBOX_AUTOCLOSE
	end

Route38_EventScript_Harry::
	trainerbattle_single TRAINER_JOHTO_HARRY, Route38_Text_HarrySeen, Route38_Text_HarryBeaten
	msgbox Route38_Text_HarryAfter, MSGBOX_AUTOCLOSE
	end

Route38_EventScript_Olivia::
	trainerbattle_single TRAINER_JOHTO_OLIVIA, Route38_Text_OliviaSeen, Route38_Text_OliviaBeaten
	msgbox Route38_Text_OliviaAfter, MSGBOX_AUTOCLOSE
	end

Route38_Text_TobySeen:
	.string "Fly high into the sky,\n"
	.string "my beloved bird POKéMON!$"

Route38_Text_TobyBeaten:
	.string "I feel like just flying\n"
	.string "away now.$"

Route38_Text_TobyAfter:
	.string "I plan to train in CIANWOOD CITY\n"
	.string "to teach my POKéMON how to FLY.$"

Route38_Text_ChadSeen:
	.string "Let me try something\n"
	.string "I learned today.$"

Route38_Text_ChadBeaten:
	.string "I didn't study enough,\n"
	.string "I guess.$"

Route38_Text_ChadAfter:
	.string "I have to take so many\n"
	.string "tests, I don't have much\l"
	.string "time for POKéMON.\p"
	.string "So when I do get to play,\n"
	.string "I really concentrate.$"

Route38_Text_DanaSeen:
	.string "You seem to be good at\n"
	.string "POKéMON.\p"
	.string "If you are, how about\n"
	.string "giving me some advice?$"

Route38_Text_DanaBeaten:
	.string "I see. So you can battle\n"
	.string "that way.$"

Route38_Text_DanaAfter:
	.string "I know something good!\p"
	.string "MOOMOO FARM's milk is\n"
	.string "famous for its flavor.$"

Route38_Text_ValerieSeen:
	.string "Hi! Aren't you a cute\n"
	.string "trainer!\p"
	.string "May I see your POKéMON?$"

Route38_Text_ValerieBeaten:
	.string "I'm glad I got to see\n"
	.string "your POKéMON!$"

Route38_Text_ValerieAfter:
	.string "When I see POKéMON, it\n"
	.string "seems to soothe my nerves.$"

Route38_Text_HarrySeen:
	.string "I've been overseas, so I\n"
	.string "know about all sorts of\l"
	.string "POKéMON!$"

Route38_Text_HarryBeaten:
	.string "Your skill is world class!$"

Route38_Text_HarryAfter:
	.string "All kinds of people around\n"
	.string "the world live happily with\l"
	.string "POKéMON.$"

Route38_Text_OliviaSeen:
	.string "Don't you think my POKéMON\n"
	.string "and I are beautiful?$"

Route38_Text_OliviaBeaten:
	.string "We drink MOOMOO MILK every\n"
	.string "day.$"

Route38_Text_OliviaAfter:
	.string "MOOMOO MILK is good for\n"
	.string "beauty and health,\p"
	.string "but inconveniently, they\n"
	.string "only sell one bottle at a time.$"

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

Route38_EventScript_Sign1::
	lock
	msgbox Route38_Text_Sign, MSGBOX_SIGN
	closemessage
	release
	end

Route38_EventScript_Sign2::
	lock
	msgbox Route38_Text_WaterSign, MSGBOX_SIGN
	closemessage
	release
	end

Route38_Text_Sign::
	.string "ROUTE 38\p"
	.string "OLIVINE CITY - ECRUTEAK CITY$"

Route38_Text_WaterSign::
	.string "NO SWIMMING OR FISHING.\n"
	.string "WATER FOR FARMING ONLY.\p"
	.string "-ECRUTEAK COUNCIL$"
