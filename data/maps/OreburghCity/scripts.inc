@ Texto vindo de pret/pokeplatinum, em ingles, como o resto do jogo.

OreburghCity_MapScripts::
	.byte 0

OreburghCity_EventScript_Hiker::
	msgbox OreburghCity_Text_Hiker, MSGBOX_NPC
	end

OreburghCity_EventScript_SchoolKid::
	msgbox OreburghCity_Text_SchoolKid, MSGBOX_NPC
	end

OreburghCity_EventScript_Pokefan::
	msgbox OreburghCity_Text_Pokefan, MSGBOX_NPC
	end

OreburghCity_EventScript_Rival::
	lock
	faceplayer
	msgbox OreburghCity_Text_Rival, MSGBOX_DEFAULT
	release
	end

OreburghCity_EventScript_Youngster::
	msgbox OreburghCity_Text_Youngster, MSGBOX_NPC
	end

OreburghCity_EventScript_Worker::
	msgbox OreburghCity_Text_Worker, MSGBOX_NPC
	end

OreburghCity_EventScript_Guitarist::
	msgbox OreburghCity_Text_Guitarist, MSGBOX_NPC
	end

OreburghCity_EventScript_BattleGirl::
	msgbox OreburghCity_Text_BattleGirl, MSGBOX_NPC
	end

OreburghCity_EventScript_CitySign::
	msgbox OreburghCity_Text_CitySign, MSGBOX_SIGN
	end

OreburghCity_EventScript_GymSign::
	msgbox OreburghCity_Text_GymSign, MSGBOX_SIGN
	end

OreburghCity_Text_Hiker:
	.string "The GYM LEADER went off to work in\n"
	.string "the mine.$"

OreburghCity_Text_SchoolKid:
	.string "The GYM LEADER is young, but he's\n"
	.string "the mine's safety supervisor.\p"
	.string "He's an expert in more than just\n"
	.string "one field!$"

OreburghCity_Text_Pokefan:
	.string "This town is small, but the miners\n"
	.string "keep it lively.$"

OreburghCity_Text_Rival:
	.string "Hunh? Oh, it's you! You finally got\n"
	.string "here? You're slow like always.\p"
	.string "But anyway, the GYM LEADER's tough!\n"
	.string "Like, seriously serious!\p"
	.string "Anyway, he's gone off to the coal\n"
	.string "mine. If you want to take him on,\l"
	.string "you'd better go off to the mine!$"

OreburghCity_Text_Youngster:
	.string "Is that guy in front of the GYM your\n"
	.string "friend? He's sort of twitchy and\l"
	.string "impatient.$"

OreburghCity_Text_Worker:
	.string "There's no question. This is hard,\n"
	.string "hard work.\p"
	.string "But working alongside POKéMON...\n"
	.string "it gives me a boost somehow.$"

OreburghCity_Text_Guitarist:
	.string "Everyone goes off on adventures,\n"
	.string "and then they gradually grow up...$"

OreburghCity_Text_BattleGirl:
	.string "Feeling hale and hearty puts a\n"
	.string "smile on my face. And that makes\l"
	.string "me happy.$"

OreburghCity_Text_CitySign:
	.string "OREBURGH CITY\n"
	.string "The Historic Mining Town$"

OreburghCity_Text_GymSign:
	.string "OREBURGH CITY POKéMON GYM\n"
	.string "LEADER: ROARK\p"
	.string "The Cliff Crag Pokémon Gym$"
