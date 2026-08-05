@ Treinadores de rota de Route37, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

Route37_MapScripts::
	.byte 0

Route37_EventScript_TwinAnn::
	trainerbattle_double TRAINER_JOHTO_ANN_AND_ANNE, Route37_Text_TwinAnnSeen, Route37_Text_TwinAnnBeaten, Route104_Text_GinaNotEnoughMons
	msgbox Route37_Text_TwinAnnAfter, MSGBOX_AUTOCLOSE
	end

Route37_EventScript_TwinAnne::
	trainerbattle_double TRAINER_JOHTO_ANN_AND_ANNE, Route37_Text_TwinAnneSeen, Route37_Text_TwinAnneBeaten, Route104_Text_GinaNotEnoughMons
	msgbox Route37_Text_TwinAnneAfter, MSGBOX_AUTOCLOSE
	end

Route37_EventScript_Greg::
	trainerbattle_single TRAINER_JOHTO_GREG, Route37_Text_GregSeen, Route37_Text_GregBeaten
	msgbox Route37_Text_GregAfter, MSGBOX_AUTOCLOSE
	end

Route37_Text_TwinAnnSeen:
	.string "ANN: ANNE and I are in this\n"
	.string "together!$"

Route37_Text_TwinAnnBeaten:
	.string "ANN & ANNE: Nnn… A little too\n"
	.string "strong.$"

Route37_Text_TwinAnnAfter:
	.string "ANN: I can tell what my sister and\n"
	.string "my POKéMON are thinking.$"

Route37_Text_TwinAnneSeen:
	.string "ANNE: ANN and I are in this\n"
	.string "together!$"

Route37_Text_TwinAnneBeaten:
	.string "ANN & ANNE: Nnn… A little too\n"
	.string "strong.$"

Route37_Text_TwinAnneAfter:
	.string "ANNE: We share the same feelings as\n"
	.string "our POKéMON.$"

Route37_Text_GregSeen:
	.string "POKéMON can't do a thing if they are\n"
	.string "asleep.\p"
	.string "I'll show you how scary that is!$"

Route37_Text_GregBeaten:
	.string "I lost. That's pretty sad…$"

Route37_Text_GregAfter:
	.string "Putting POKéMON to sleep or paralyz-\n"
	.string "ing them are good battle techniques.$"

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

Route37_EventScript_Sign::
	lock
	msgbox Route37_Text_Sign, MSGBOX_SIGN
	closemessage
	release
	end

Route37_Text_Sign::
	.string "ROUTE 37\n"
	.string "ECRUTEAK CITY AHEAD$"
