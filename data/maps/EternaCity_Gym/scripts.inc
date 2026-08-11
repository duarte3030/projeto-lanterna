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

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

EternaCity_Gym_EventScript_Npc1::
	msgbox EternaCity_Gym_Text_Npc1, MSGBOX_NPC
	end

EternaCity_Gym_Text_Npc1:
	.string "Hey, there!\nHow's it going, Champ-to-be?\pActually, that's what I said to some\nboy who zipped in here earlier, too!\pThe Gym Leader, Gardenia, is a user\nof Grass-type Pokémon.\pIt should be obvious, but Grass-type\nPokémon really hate fire.\pThey're also at a huge disadvantage\nagainst the Flying type, too.\pOh, wait a second. I should tell you\nabout the Gym itself first.\pYou can't challenge the Gym Leader\nuntil you beat all the Gym's Trainers.\pIt's a bit challenging, but just think\nof it as good training and go for it!$"

EternaCity_Gym_EventScript_Npc2::
	msgbox EternaCity_Gym_Text_Npc2, MSGBOX_NPC
	end

EternaCity_Gym_Text_Npc2:
	.string "Welcome!\nWithout further ado, let's go!$"

EternaCity_Gym_EventScript_Npc3::
	msgbox EternaCity_Gym_Text_Npc3, MSGBOX_NPC
	end

EternaCity_Gym_Text_Npc3:
	.string "My Grass-type Pokémon can dole out\nsome serious special attacks...\pI won't let you win...easily!$"

EternaCity_Gym_EventScript_Npc4::
	msgbox EternaCity_Gym_Text_Npc4, MSGBOX_NPC
	end

EternaCity_Gym_Text_Npc4:
	.string "You can't win when you're distracted by\nthe lovely aromas of Pokémon!$"
