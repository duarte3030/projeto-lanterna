OreburghCity_Flat1_F1_MapScripts::
	.byte 0

OreburghCity_Flat1_F1_EventScript_Pokefan::
	msgbox OreburghCity_Flat1_F1_Text_Pokefan, MSGBOX_NPC
	end

OreburghCity_Flat1_F1_EventScript_Hiker::
	msgbox OreburghCity_Flat1_F1_Text_Hiker, MSGBOX_NPC
	end

OreburghCity_Flat1_F1_EventScript_Visitor::
	msgbox OreburghCity_Flat1_F1_Text_Visitor, MSGBOX_NPC
	end

OreburghCity_Flat1_F1_Text_Pokefan:
	.string "This building is close to the MINE,\n"
	.string "so a lot of miners live here.$"

OreburghCity_Flat1_F1_Text_Hiker:
	.string "My legs are sore from climbing all\n"
	.string "those stairs in the MINE today.$"

OreburghCity_Flat1_F1_Text_Visitor:
	.string "I'm just visiting a friend who\n"
	.string "lives on the floor above.$"
