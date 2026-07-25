OreburghMine_B1F_MapScripts::
	.byte 0

OreburghMine_B1F_EventScript_Miner1::
	msgbox OreburghMine_B1F_Text_Miner1, MSGBOX_NPC
	end

OreburghMine_B1F_EventScript_Miner2::
	msgbox OreburghMine_B1F_Text_Miner2, MSGBOX_NPC
	end

OreburghMine_B1F_Text_Miner1:
	.string "This mine's older than the city\n"
	.string "itself.\p"
	.string "Some of these tunnels haven't been\n"
	.string "touched in years.$"

OreburghMine_B1F_Text_Miner2:
	.string "Careful with your footing.\p"
	.string "Rockslides happen more often than\n"
	.string "the foremen like to admit.$"
