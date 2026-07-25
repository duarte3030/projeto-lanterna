@ Ginasio de Sinnoh com interior reaproveitado de Hoenn.

HearthomeCity_Gym_MapScripts::
	.byte 0

HearthomeCity_Gym_EventScript_Leader::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_SINNOH_5, HearthomeCity_Gym_EventScript_JaVenceu
	msgbox HearthomeCity_Gym_Text_Intro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_SINNOH_LEADER_FANTINA, HearthomeCity_Gym_Text_Defeat
	msgbox HearthomeCity_Gym_Text_Post, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_SINNOH_5
	release
	end

HearthomeCity_Gym_EventScript_JaVenceu::
	msgbox HearthomeCity_Gym_Text_JaVenceu, MSGBOX_DEFAULT
	release
	end

HearthomeCity_Gym_Text_Intro:
	.string "...$"

HearthomeCity_Gym_Text_Defeat:
	.string "You are so fantastically strong.\nI know now why I have lost.$"

HearthomeCity_Gym_Text_Post:
	.string "...$"

HearthomeCity_Gym_Text_JaVenceu:
	.string "The RELIC BADGE is already yours.$"
