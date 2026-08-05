@ Treinadores de rota de DragonsDen_Cavern, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

DragonsDen_Cavern_MapScripts::
	.byte 0

DragonsDen_Cavern_EventScript_Darin::
	trainerbattle_single TRAINER_JOHTO_DARIN, DragonsDen_Cavern_Text_DarinSeen, DragonsDen_Cavern_Text_DarinBeaten
	msgbox DragonsDen_Cavern_Text_DarinAfter, MSGBOX_AUTOCLOSE
	end

DragonsDen_Cavern_EventScript_Cara::
	trainerbattle_single TRAINER_JOHTO_CARA, DragonsDen_Cavern_Text_CaraSeen, DragonsDen_Cavern_Text_CaraBeaten
	msgbox DragonsDen_Cavern_Text_CaraAfter, MSGBOX_AUTOCLOSE
	end

DragonsDen_Cavern_EventScript_TwinLea::
	trainerbattle_double TRAINER_JOHTO_LEA_AND_PIA, DragonsDen_Cavern_Text_TwinLeaSeen, DragonsDen_Cavern_Text_TwinLeaBeaten, Route104_Text_GinaNotEnoughMons
	msgbox DragonsDen_Cavern_Text_TwinLeaAfter, MSGBOX_AUTOCLOSE
	end

DragonsDen_Cavern_EventScript_TwinPia::
	trainerbattle_double TRAINER_JOHTO_LEA_AND_PIA, DragonsDen_Cavern_Text_TwinPiaSeen, DragonsDen_Cavern_Text_TwinPiaBeaten, Route104_Text_GinaNotEnoughMons
	msgbox DragonsDen_Cavern_Text_TwinPiaAfter, MSGBOX_AUTOCLOSE
	end

DragonsDen_Cavern_Text_DarinSeen:
	.string "You! How dare you enter\n"
	.string "uninvited!$"

DragonsDen_Cavern_Text_DarinBeaten:
	.string "S-strong!$"

DragonsDen_Cavern_Text_DarinAfter:
	.string "The SHRINE ahead is home to the\n"
	.string "MASTER of our dragon-user clan.\p"
	.string "You're not allowed to just go in!$"

DragonsDen_Cavern_Text_CaraSeen:
	.string "You shouldn't be in here!$"

DragonsDen_Cavern_Text_CaraBeaten:
	.string "Oh yikes, I lost!$"

DragonsDen_Cavern_Text_CaraAfter:
	.string "Soon I'm going to get permission\n"
	.string "from our MASTER to use dragons.\p"
	.string "When I do, I'm going to become an\n"
	.string "admirable dragon trainer and gain\l"
	.string "our MASTER's approval.$"

DragonsDen_Cavern_Text_TwinLeaSeen:
	.string "It's a stranger we don't know.$"

DragonsDen_Cavern_Text_TwinLeaBeaten:
	.string "Ouchies.$"

DragonsDen_Cavern_Text_TwinLeaAfter:
	.string "It was like having to battle\n"
	.string "LANCE.$"

DragonsDen_Cavern_Text_TwinPiaSeen:
	.string "Who are you?$"

DragonsDen_Cavern_Text_TwinPiaBeaten:
	.string "Meanie.$"

DragonsDen_Cavern_Text_TwinPiaAfter:
	.string "We'll tell on you.\p"
	.string "MASTER will be angry with you.$"
