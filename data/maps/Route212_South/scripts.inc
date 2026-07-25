Route212_South_MapScripts::
	.byte 0

Route212_South_EventScript_SchoolKid::
	msgbox Route212_South_Text_SchoolKid, MSGBOX_NPC
	end

Route212_South_EventScript_Lady::
	msgbox Route212_South_Text_Lady, MSGBOX_NPC
	end

Route212_South_EventScript_Collector::
	msgbox Route212_South_Text_Collector, MSGBOX_NPC
	end

Route212_South_EventScript_Fisherman::
	msgbox Route212_South_Text_Fisherman, MSGBOX_NPC
	end

Route212_South_EventScript_ShardsSign::
	msgbox Route212_South_Text_ShardsSign, MSGBOX_SIGN
	end

Route212_South_Text_SchoolKid:
	.string "I've been ROCK SMASHing all along this\n"
	.string "route, looking for wild POKéMON hiding\l"
	.string "in the rubble.$"

Route212_South_Text_Lady:
	.string "It rains here so often that I never\n"
	.string "leave home without my umbrella.$"

Route212_South_Text_Collector:
	.string "Shards wash up along this route after\n"
	.string "it rains. I've got quite a collection\l"
	.string "going!$"

Route212_South_Text_Fisherman:
	.string "I come here to fish whenever it rains.\n"
	.string "Something about the sound helps me\l"
	.string "focus on the bite.$"

Route212_South_Text_ShardsSign:
	.string "WANTED: SHARDS!\n"
	.string "Bring your finds to the antique shop\l"
	.string "in PASTORIA for a nice reward.$"
