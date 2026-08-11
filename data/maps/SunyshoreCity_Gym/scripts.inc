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

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SunyshoreCity_Gym_EventScript_Npc1::
	msgbox SunyshoreCity_Gym_Text_Npc1, MSGBOX_NPC
	end

SunyshoreCity_Gym_Text_Npc1:
	.string "Hey, there!\nHow's it going, Champ-to-be?\pLet me check out your Trainer Case.\nLet's see how many Badges you have.\pOne, two, three...\nWhoa! Wow! You've already got seven!\pThat means if you can beat this Gym\nLeader, you're on your way to the\pPokémon League next.\pThat also means this is the last time\nI get to give you advice.\pThis is it, kiddo!\nListen carefully...one last time!\pThe Gym Leader here is a master of\nElectric-type Pokémon!\pThat's all I have to say.\nThe rest is up to you!$"

SunyshoreCity_Gym_EventScript_Placa2::
	msgbox SunyshoreCity_Gym_Text_Placa2, MSGBOX_SIGN
	end

SunyshoreCity_Gym_Text_Placa2:
	.string "Sunyshore City Pokémon Gym\pLeader: Volkner$"

SunyshoreCity_Gym_EventScript_Placa3::
	msgbox SunyshoreCity_Gym_Text_Placa3, MSGBOX_SIGN
	end

SunyshoreCity_Gym_Text_Placa3:
	.string "Sunyshore City Pokémon Gym\pLeader: Volkner$"

@ Treinador do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_masmorra_sinnoh.py)

SunyshoreCity_Gym_EventScript_SchoolKidTiera::
	trainerbattle_single TRAINER_SINNOH_SCHOOL_KID_TIERA, SunyshoreCity_Gym_Text_SchoolKidTieraIntro, SunyshoreCity_Gym_Text_SchoolKidTieraDefeat
	msgbox SunyshoreCity_Gym_Text_SchoolKidTieraPost, MSGBOX_AUTOCLOSE
	end

SunyshoreCity_Gym_Text_SchoolKidTieraIntro:
	.string "Can you make it to the Gym Leader?\nYou sure now?$"

SunyshoreCity_Gym_Text_SchoolKidTieraDefeat:
	.string "The gears spin round and round...\nI spin down and out...$"

SunyshoreCity_Gym_Text_SchoolKidTieraPost:
	.string "Our Gym's trick walkways are sure\nto make your head spin!$"
