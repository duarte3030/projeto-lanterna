OreburghCity_Flat2_F2_MapScripts::
	.byte 0

OreburghCity_Flat2_F2_EventScript_Guitarist::
	msgbox OreburghCity_Flat2_F2_Text_Guitarist, MSGBOX_NPC
	end

OreburghCity_Flat2_F2_EventScript_Breeder::
	msgbox OreburghCity_Flat2_F2_Text_Breeder, MSGBOX_NPC
	end

OreburghCity_Flat2_F2_EventScript_Collector::
	msgbox OreburghCity_Flat2_F2_Text_Collector, MSGBOX_NPC
	end

OreburghCity_Flat2_F2_Text_Guitarist:
	.string "The view is good from up here, but\n"
	.string "it's a pain going outside.$"

OreburghCity_Flat2_F2_Text_Breeder:
	.string "There are so many kinds of POKéMON\n"
	.string "out there. I want to see them all!$"

OreburghCity_Flat2_F2_Text_Collector:
	.string "I keep a little journal of every\n"
	.string "POKéMON I've spotted near OREBURGH.$"
