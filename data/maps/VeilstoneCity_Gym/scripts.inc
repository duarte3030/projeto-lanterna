@ Ginasio de Sinnoh com interior reaproveitado de Hoenn.

VeilstoneCity_Gym_MapScripts::
	.byte 0

VeilstoneCity_Gym_EventScript_Leader::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_SINNOH_3, VeilstoneCity_Gym_EventScript_JaVenceu
	msgbox VeilstoneCity_Gym_Text_Intro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_SINNOH_LEADER_MAYLENE, VeilstoneCity_Gym_Text_Defeat
	msgbox VeilstoneCity_Gym_Text_Post, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_SINNOH_3
	release
	end

VeilstoneCity_Gym_EventScript_JaVenceu::
	msgbox VeilstoneCity_Gym_Text_JaVenceu, MSGBOX_DEFAULT
	release
	end

VeilstoneCity_Gym_Text_Intro:
	.string "...$"

VeilstoneCity_Gym_Text_Defeat:
	.string "I shall admit defeat...\nYou are much too strong.$"

VeilstoneCity_Gym_Text_Post:
	.string "...$"

VeilstoneCity_Gym_Text_JaVenceu:
	.string "The COBBLE BADGE is already yours.$"
