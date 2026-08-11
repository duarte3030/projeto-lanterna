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

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

OreburghMine_B1F_EventScript_Npc1::
	msgbox OreburghMine_B1F_Text_Npc1, MSGBOX_NPC
	end

OreburghMine_B1F_Text_Npc1:
	.string "Everyone that works in the coal mine\nkeeps their own Pokémon with them.\pYou may be challenged to battles!\nHahaha!$"

OreburghMine_B1F_EventScript_Npc2::
	msgbox OreburghMine_B1F_Text_Npc2, MSGBOX_NPC
	end

OreburghMine_B1F_Text_Npc2:
	.string "I found what I thought were some\nrocks, then they started moving!\pThey were Pokémon that looked just\nlike rocks!$"
