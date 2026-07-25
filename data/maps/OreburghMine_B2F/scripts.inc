OreburghMine_B2F_MapScripts::
	.byte 0

OreburghMine_B2F_EventScript_Miner1::
	msgbox OreburghMine_B2F_Text_Miner1, MSGBOX_NPC
	end

OreburghMine_B2F_EventScript_Miner2::
	msgbox OreburghMine_B2F_Text_Miner2, MSGBOX_NPC
	end

OreburghMine_B2F_Text_Miner1:
	.string "The deeper tunnels wind on forever.\p"
	.string "I still get turned around down\n"
	.string "here.$"

OreburghMine_B2F_Text_Miner2:
	.string "Found a nice vein of ore a while\n"
	.string "back.\p"
	.string "The company's still working through\n"
	.string "it.$"
