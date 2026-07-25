OreburghCity_Flat1_F2_MapScripts::
	.byte 0

OreburghCity_Flat1_F2_EventScript_Youngster::
	msgbox OreburghCity_Flat1_F2_Text_Youngster, MSGBOX_NPC
	end

OreburghCity_Flat1_F2_EventScript_Gentleman::
	msgbox OreburghCity_Flat1_F2_Text_Gentleman, MSGBOX_NPC
	end

OreburghCity_Flat1_F2_EventScript_Scientist::
	msgbox OreburghCity_Flat1_F2_Text_Scientist, MSGBOX_NPC
	end

OreburghCity_Flat1_F2_Text_Youngster:
	.string "My dad works at the MINE. He comes\n"
	.string "home covered in coal dust!$"

OreburghCity_Flat1_F2_Text_Gentleman:
	.string "A quiet flat with a good view of\n"
	.string "the GYM. I couldn't ask for more.$"

OreburghCity_Flat1_F2_Text_Scientist:
	.string "I'm studying the rock strata around\n"
	.string "OREBURGH. Fascinating stuff.$"
