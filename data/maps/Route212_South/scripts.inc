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

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route212_South_EventScript_Placa1::
	msgbox Route212_South_Text_Placa1, MSGBOX_SIGN
	end

Route212_South_Text_Placa1:
	.string "Rt. 212\nPastoria City$"

Route212_South_EventScript_Placa2::
	msgbox Route212_South_Text_Placa2, MSGBOX_SIGN
	end

Route212_South_Text_Placa2:
	.string "Shards Wanted\nPokémon Moves Taught$"

Route212_South_EventScript_Placa3::
	msgbox Route212_South_Text_Placa3, MSGBOX_SIGN
	end

Route212_South_Text_Placa3:
	.string "Trainer Tips\pIf you get stuck in the bog, you can\ncount on being there a while.\pThere's no need to panic.\nJust struggle and squirm for a bit.\pBicycles cannot be ridden on marshy\nground, incidentally.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route212_South_EventScript_Npc1::
	msgbox Route212_South_Text_Npc1, MSGBOX_NPC
	end

Route212_South_Text_Npc1:
	.string "You can zip across fallen logs like\nbridges on your Bike.$"

Route212_South_EventScript_Npc2::
	msgbox Route212_South_Text_Npc2, MSGBOX_NPC
	end

Route212_South_Text_Npc2:
	.string "...Am I stuck in the bog?\pOf course not. How silly!\nThis is a full-body mud pack.\pIf it weren't, I would be squirming\nand struggling to get out!$"

Route212_South_EventScript_Npc3::
	msgbox Route212_South_Text_Npc3, MSGBOX_NPC
	end

Route212_South_Text_Npc3:
	.string "You've been to the Great Marsh?\nHow about the Pokémon Mansion?\pWherever I go, I get to meet new and\ndifferent Pokémon.\pI feel so privileged and happy about\nthat.$"
