OreburghCity_Mart_MapScripts::
	.byte 0

OreburghCity_Mart_EventScript_Cashier::
	msgbox OreburghCity_Mart_Text_Cashier, MSGBOX_NPC
	end

OreburghCity_Mart_EventScript_Hiker::
	msgbox OreburghCity_Mart_Text_Hiker, MSGBOX_NPC
	end

OreburghCity_Mart_EventScript_Collector::
	msgbox OreburghCity_Mart_Text_Collector, MSGBOX_NPC
	end

OreburghCity_Mart_Text_Cashier:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

OreburghCity_Mart_Text_Hiker:
	.string "The OREBURGH MINE is right nearby.\n"
	.string "I always stock up here before I go in.$"

OreburghCity_Mart_Text_Collector:
	.string "I collect rare items from all over\n"
	.string "SINNOH. This MART always has something\l"
	.string "new for my collection.$"
