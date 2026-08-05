@ Treinadores de rota de GoldenrodCity_UndergroundStorage, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

GoldenrodCity_UndergroundStorage_MapScripts::
	.byte 0

GoldenrodCity_UndergroundStorage_EventScript_Grunt19::
	trainerbattle_single TRAINER_JOHTO_GRUNT_19, GoldenrodCity_UndergroundStorage_Text_Grunt19Seen, GoldenrodCity_UndergroundStorage_Text_Grunt19Beaten
	msgbox GoldenrodCity_UndergroundStorage_Text_Grunt19After, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_UndergroundStorage_EventScript_Grunt12::
	trainerbattle_single TRAINER_JOHTO_GRUNT_12, GoldenrodCity_UndergroundStorage_Text_Grunt12Seen, GoldenrodCity_UndergroundStorage_Text_Grunt12Beaten
	msgbox GoldenrodCity_UndergroundStorage_Text_Grunt12After, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_UndergroundStorage_EventScript_Eto::
	trainerbattle_single TRAINER_JOHTO_ETO_3, GoldenrodCity_UndergroundStorage_Text_EtoSeen, GoldenrodCity_UndergroundStorage_Text_EtoBeaten
	msgbox GoldenrodCity_UndergroundStorage_Text_EtoAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_UndergroundStorage_Text_Grunt19Seen:
	.string "How did you get this far?\p"
	.string "I guess it can't be helped. I'll\n"
	.string "dispose of you.$"

GoldenrodCity_UndergroundStorage_Text_Grunt19Beaten:
	.string "I got disposed of…$"

GoldenrodCity_UndergroundStorage_Text_Grunt19After:
	.string "TEAM ROCKET will keep going, waiting\n"
	.string "for the return of GIOVANNI.\p"
	.string "We'll do whatever it takes.$"

GoldenrodCity_UndergroundStorage_Text_Grunt12Seen:
	.string "You're not going any farther!\p"
	.string "I don't show mercy to my enemies,\n"
	.string "not even brats!$"

GoldenrodCity_UndergroundStorage_Text_Grunt12Beaten:
	.string "Blast it!$"

GoldenrodCity_UndergroundStorage_Text_Grunt12After:
	.string "I lost…\p"
	.string "Please forgive me, GIOVANNI!$"

GoldenrodCity_UndergroundStorage_Text_EtoSeen:
	.string "Hyuck-hyuck-hyuck! Look who it is!\p"
	.string "Ready? I'm really tough now!$"

GoldenrodCity_UndergroundStorage_Text_EtoBeaten:
	.string "Hyuck-hyuck-hyuck! You're so good!\p"
	.string "This TEAM ROCKET thing is just\n"
	.string "a job, but I can see it hurts others.\p"
	.string "That's it, I'm leaving.\p"
	.string "Thank you so much. Sorry GIOVANNI!$"

GoldenrodCity_UndergroundStorage_Text_EtoAfter:
	.string "Hyuck-hyuck-hyuck! That was a blast!\n"
	.string "I'll remember you!$"
