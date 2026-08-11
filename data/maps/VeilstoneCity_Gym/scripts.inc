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

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

VeilstoneCity_Gym_EventScript_Npc1::
	msgbox VeilstoneCity_Gym_Text_Npc1, MSGBOX_NPC
	end

VeilstoneCity_Gym_Text_Npc1:
	.string "Hey, there!\nHow's it going, Champ-to-be?\pThe Gym Leader is a user of\nFighting-type Pokémon.\pShe'd be a terror against Normal-type\nPokémon.\pBut! And it's a big but!\nJust between you and me...\pMaylene, the Gym Leader, said Flying-\nand Psychic-type Pokémon could be\preal trouble for her!\pIf you want to battle her, smack the\npunching bags along the rails.\pYou have to hit those bags hard!$"

VeilstoneCity_Gym_EventScript_Placa2::
	msgbox VeilstoneCity_Gym_Text_Placa2, MSGBOX_SIGN
	end

VeilstoneCity_Gym_Text_Placa2:
	.string "One day at a time.$"

VeilstoneCity_Gym_EventScript_Placa3::
	msgbox VeilstoneCity_Gym_Text_Placa3, MSGBOX_SIGN
	end

VeilstoneCity_Gym_Text_Placa3:
	.string "A good deed for every day.$"

VeilstoneCity_Gym_EventScript_Placa4::
	msgbox VeilstoneCity_Gym_Text_Placa4, MSGBOX_SIGN
	end

VeilstoneCity_Gym_Text_Placa4:
	.string "Treasure every encounter,\nfor it is unique.$"
