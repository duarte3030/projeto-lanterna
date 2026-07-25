@ Ginasio de Eterna. Interior reaproveitado de Hoenn: o port de Sinnoh nunca
@ construiu este predio. Ver Pokemon Claude/PLANO.md.

EternaCity_Gym_MapScripts::
	.byte 0

EternaCity_Gym_EventScript_Gardenia::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_SINNOH_2, EternaCity_Gym_EventScript_JaVenceu
	msgbox EternaCity_Gym_Text_Intro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_SINNOH_LEADER_GARDENIA, EternaCity_Gym_Text_Defeat
	msgbox EternaCity_Gym_Text_Post, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_SINNOH_2
	release
	end

EternaCity_Gym_EventScript_JaVenceu::
	msgbox EternaCity_Gym_Text_JaVenceu, MSGBOX_DEFAULT
	release
	end

EternaCity_Gym_Text_Intro:
	.string "...$"

EternaCity_Gym_Text_Defeat:
	.string "Amazing!\nYou're very good, aren't you?$"

EternaCity_Gym_Text_Post:
	.string "...$"

EternaCity_Gym_Text_JaVenceu:
	.string "The FOREST BADGE is yours.\nGrow strong, like a tree!$"
