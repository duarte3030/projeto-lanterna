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
