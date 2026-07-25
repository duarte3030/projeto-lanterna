@ Ginasio de Sinnoh com interior reaproveitado de Hoenn: o port nunca construiu
@ este predio. Ver Pokemon Claude/PLANO.md.

CanalaveCity_Gym_MapScripts::
	.byte 0

CanalaveCity_Gym_EventScript_Leader::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_SINNOH_6, CanalaveCity_Gym_EventScript_JaVenceu
	msgbox CanalaveCity_Gym_Text_Intro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_SINNOH_LEADER_BYRON, CanalaveCity_Gym_Text_Defeat
	msgbox CanalaveCity_Gym_Text_Post, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_SINNOH_6
	release
	end

CanalaveCity_Gym_EventScript_JaVenceu::
	msgbox CanalaveCity_Gym_Text_JaVenceu, MSGBOX_DEFAULT
	release
	end

CanalaveCity_Gym_Text_Intro:
	.string "...$"

CanalaveCity_Gym_Text_Defeat:
	.string "Hmm!\nMy sturdy Pokémon, defeated!$"

CanalaveCity_Gym_Text_Post:
	.string "...$"

CanalaveCity_Gym_Text_JaVenceu:
	.string "The MINE BADGE is already yours.$"
