@ Treinadores de rota de IlexForest, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

IlexForest_MapScripts::
	.byte 0

IlexForest_EventScript_BugcatcherWayne::
	trainerbattle_single TRAINER_JOHTO_WAYNE, IlexForest_Text_BugcatcherWayneSeen, IlexForest_Text_BugcatcherWayneBeaten
	msgbox IlexForest_Text_BugcatcherWayneAfter, MSGBOX_AUTOCLOSE
	end

IlexForest_Text_BugcatcherWayneSeen:
	.string "Don't sneak up on me like that!\p"
	.string "You frightened a POKéMON away!$"

IlexForest_Text_BugcatcherWayneBeaten:
	.string "I hadn't seen that POKéMON before…$"

IlexForest_Text_BugcatcherWayneAfter:
	.string "A POKéMON I've never seen before\n"
	.string "fell out of the tree when I used\l"
	.string "HEADBUTT.\p"
	.string "I ought to use HEADBUTT in other\n"
	.string "places too.$"
