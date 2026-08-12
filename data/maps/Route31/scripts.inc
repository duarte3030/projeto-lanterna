@ Treinadores de rota de Route31, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

Route31_MapScripts::
	.byte 0

Route31_EventScript_Bugcatcher_Wade::
	trainerbattle_single TRAINER_JOHTO_WADE, Route31_Text_Bugcatcher_WadeSeen, Route31_Text_Bugcatcher_WadeBeaten
	msgbox Route31_Text_Bugcatcher_WadeAfter, MSGBOX_AUTOCLOSE
	end

Route31_Text_Bugcatcher_WadeSeen:
	.string "I caught a bunch of POKéMON.\n"
	.string "Let me battle with you!$"

Route31_Text_Bugcatcher_WadeBeaten:
	.string "Awwwww…$"

Route31_Text_Bugcatcher_WadeAfter:
	.string "You can catch POKéMON even if\n"
	.string "you have six with you.\p"
	.string "If you catch one, it'll go to\n"
	.string "your BOX automatically.$"

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

Route31_EventScript_DarkCaveSign::
	lock
	msgbox Route31_Text_DarkCaveSign, MSGBOX_SIGN
	closemessage
	release
	end

Route31_EventScript_Sign::
	lock
	msgbox Route31_Text_Sign, MSGBOX_SIGN
	closemessage
	release
	end

Route31_Text_DarkCaveSign::
	.string "DARK CAVE$"

Route31_Text_Sign::
	.string "ROUTE 31\p"
	.string "VIOLET CITY - CHERRYGROVE CITY$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

Route31_EventScript_Youngster::
	lock
	faceplayer
	msgbox Route31_Text_CooltrainerM, MSGBOX_DEFAULT
	closemessage
	release
	end

Route31_Text_CooltrainerM::
	.string "DARK CAVE…\p"
	.string "If POKéMON could light it up,\n"
	.string "I'd explore it.$"

Route31_EventScript_Boy::
	lock
	faceplayer
	msgbox Route31_Text_Youngster, MSGBOX_DEFAULT
	closemessage
	release
	end

Route31_Text_Youngster::
	.string "I found a good POKéMON in DARK\n"
	.string "CAVE.\p"
	.string "I'm going to raise it to take\n"
	.string "on FALKNER.\p"
	.string "He's the leader of VIOLET\n"
	.string "CITY's GYM.$"
