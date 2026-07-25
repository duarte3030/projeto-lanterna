@ Ginasio de Sinnoh com interior reaproveitado de Hoenn: o port nunca construiu
@ este predio. Ver Pokemon Claude/PLANO.md.

SunyshoreCity_Gym_MapScripts::
	.byte 0

SunyshoreCity_Gym_EventScript_Leader::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_SINNOH_8, SunyshoreCity_Gym_EventScript_JaVenceu
	msgbox SunyshoreCity_Gym_Text_Intro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_SINNOH_LEADER_VOLKNER, SunyshoreCity_Gym_Text_Defeat
	msgbox SunyshoreCity_Gym_Text_Post, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_SINNOH_8
	release
	end

SunyshoreCity_Gym_EventScript_JaVenceu::
	msgbox SunyshoreCity_Gym_Text_JaVenceu, MSGBOX_DEFAULT
	release
	end

SunyshoreCity_Gym_Text_Intro:
	.string "...$"

SunyshoreCity_Gym_Text_Defeat:
	.string "You've got me beat...Your desire and the noble way\nyour Pokémon battled for you...I even felt thrilled during our\nmatch.That was a very good battle.$"

SunyshoreCity_Gym_Text_Post:
	.string "...$"

SunyshoreCity_Gym_Text_JaVenceu:
	.string "The BEACON BADGE is already yours.$"
