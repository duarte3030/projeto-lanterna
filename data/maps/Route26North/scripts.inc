Route26North_MapScripts::
	.byte 0

@ Treinador do hns que faltava, ligado em 12/08/2026 por
@ dev_scripts/treinadores_faltantes_johto.py

Route26North_EventScript_Beth::
	trainerbattle_single TRAINER_JOHTO_BETH, Route26North_Text_BethSeen, Route26North_Text_BethBeaten
	msgbox Route26North_Text_BethAfter, MSGBOX_AUTOCLOSE
	end

Route26North_Text_BethSeen:
	.string "I lost to a trainer named {RIVAL}.\p"
	.string "He was really strong, but…\p"
	.string "It was as if he absolutely had to\n"
	.string "win at any cost.\p"
	.string "I felt sorry for his POKéMON.$"

Route26North_Text_BethBeaten:
	.string "POKéMON aren't tools of war.$"

Route26North_Text_BethAfter:
	.string "POKéMON are in-valuable, lifelong\n"
	.string "partners.$"
