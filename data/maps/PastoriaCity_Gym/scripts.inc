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

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

PastoriaCity_Gym_EventScript_Npc1::
	msgbox PastoriaCity_Gym_Text_Npc1, MSGBOX_NPC
	end

PastoriaCity_Gym_Text_Npc1:
	.string "The Gym Leader Wake... Uh, I mean\nCrasher Wake, is a master of\pWater-type Pokémon.\pI'd say you've got guts if you try\nto face down Water types with Fire-\por Ground-type Pokémon!\pBut that part I'll leave up to you!\nGo and have some good battles!$"
