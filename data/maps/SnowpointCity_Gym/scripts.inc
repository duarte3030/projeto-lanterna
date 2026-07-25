@ Ginasio de Sinnoh com interior reaproveitado de Hoenn: o port nunca construiu
@ este predio. Ver Pokemon Claude/PLANO.md.

SnowpointCity_Gym_MapScripts::
	.byte 0

SnowpointCity_Gym_EventScript_Leader::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_SINNOH_7, SnowpointCity_Gym_EventScript_JaVenceu
	msgbox SnowpointCity_Gym_Text_Intro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_SINNOH_LEADER_CANDICE, SnowpointCity_Gym_Text_Defeat
	msgbox SnowpointCity_Gym_Text_Post, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_SINNOH_7
	release
	end

SnowpointCity_Gym_EventScript_JaVenceu::
	msgbox SnowpointCity_Gym_Text_JaVenceu, MSGBOX_DEFAULT
	release
	end

SnowpointCity_Gym_Text_Intro:
	.string "...$"

SnowpointCity_Gym_Text_Defeat:
	.string "I must say, I've warmed up to you!\nI might even admire you a little.$"

SnowpointCity_Gym_Text_Post:
	.string "...$"

SnowpointCity_Gym_Text_JaVenceu:
	.string "The ICICLE BADGE is already yours.$"
