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

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SnowpointCity_Gym_EventScript_Npc1::
	msgbox SnowpointCity_Gym_Text_Npc1, MSGBOX_NPC
	end

SnowpointCity_Gym_Text_Npc1:
	.string "Hey, there!\nHow's it going, Champ-to-be?\pDo you see the big snowballs placed\nhere and there?\pYou need to slide on the ice with\nenough momentum to crush them.\pThe Gym Leader is a user of\nIce-type Pokémon.\pMelt her defenses with scorching-\nhot Fire-type moves!\pIt's all about focus with this Gym.\nBear down and focus!$"
