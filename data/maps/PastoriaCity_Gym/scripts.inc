@ Ginasio de Sinnoh com interior reaproveitado de Hoenn.

PastoriaCity_Gym_MapScripts::
	.byte 0

PastoriaCity_Gym_EventScript_Leader::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_SINNOH_4, PastoriaCity_Gym_EventScript_JaVenceu
	msgbox PastoriaCity_Gym_Text_Intro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_SINNOH_LEADER_WAKE, PastoriaCity_Gym_Text_Defeat
	msgbox PastoriaCity_Gym_Text_Post, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_SINNOH_4
	release
	end

PastoriaCity_Gym_EventScript_JaVenceu::
	msgbox PastoriaCity_Gym_Text_JaVenceu, MSGBOX_DEFAULT
	release
	end

PastoriaCity_Gym_Text_Intro:
	.string "...$"

PastoriaCity_Gym_Text_Defeat:
	.string "Hunwah!\nIt's gone and ended!How will I say this... I want more!\nI wanted to battle a lot more!$"

PastoriaCity_Gym_Text_Post:
	.string "...$"

PastoriaCity_Gym_Text_JaVenceu:
	.string "The FEN BADGE is already yours.$"
