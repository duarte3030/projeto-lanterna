@ Ginasio de referencia de Sinnoh. Lider com insignia, no padrao usado pelos
@ outros sete. Falas vindas de pret/pokeplatinum.

OreburghCity_Gym_MapScripts::
	.byte 0

OreburghCity_Gym_EventScript_Guide::
	lock
	faceplayer
	msgbox OreburghCity_Gym_Text_Guide, MSGBOX_DEFAULT
	release
	end

OreburghCity_Gym_EventScript_Visitor::
	msgbox OreburghCity_Gym_Text_Visitor, MSGBOX_NPC
	end

OreburghCity_Gym_EventScript_Sign::
	msgbox OreburghCity_Gym_Text_Sign, MSGBOX_SIGN
	end

OreburghCity_Gym_Text_Guide:
	.string "Howdy! How's it going, Champ-to-be?\p"
	.string "The GYM LEADER is a user of ROCK-\n"
	.string "type POKéMON. Listen, ROCK-type\l"
	.string "POKéMON really hate water, and\l"
	.string "they're also weak to GRASS moves.\p"
	.string "But don't think it'll be easy. You\n"
	.string "don't get to be a GYM LEADER\l"
	.string "without covering for weaknesses.\p"
	.string "That's all the advice I can give.\n"
	.string "Thanks for listening!$"

OreburghCity_Gym_Text_Visitor:
	.string "I came to watch ROARK train. He's\n"
	.string "not battling challengers just yet.$"

OreburghCity_Gym_Text_Sign:
	.string "OREBURGH CITY POKéMON GYM\n"
	.string "Leader: Roark$"

OreburghCity_Gym_EventScript_Roark::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_SINNOH_1, OreburghCity_Gym_EventScript_RoarkDerrotado
	msgbox OreburghCity_Gym_Text_RoarkIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_SINNOH_LEADER_ROARK, OreburghCity_Gym_Text_RoarkDefeat
	msgbox OreburghCity_Gym_Text_RoarkPost, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_SINNOH_1
	release
	end

OreburghCity_Gym_EventScript_RoarkDerrotado::
	msgbox OreburghCity_Gym_Text_RoarkJaVenceu, MSGBOX_DEFAULT
	release
	end

OreburghCity_Gym_Text_RoarkIntro:
	.string "...$"

OreburghCity_Gym_Text_RoarkDefeat:
	.string "W-what? That can't be!\nMy buffed-up Pokémon!$"

OreburghCity_Gym_Text_RoarkPost:
	.string "...$"

OreburghCity_Gym_Text_RoarkJaVenceu:
	.string "The COAL BADGE is yours.\nKeep digging deeper, challenger!$"
