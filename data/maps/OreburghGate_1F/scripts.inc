OreburghGate_1F_MapScripts::
	.byte 0

OreburghGate_1F_EventScript_Hiker1::
	msgbox OreburghGate_1F_Text_Hiker1, MSGBOX_NPC
	end

OreburghGate_1F_EventScript_Hiker2::
	msgbox OreburghGate_1F_Text_Hiker2, MSGBOX_NPC
	end

OreburghGate_1F_Text_Hiker1:
	.string "This gate connects OREBURGH CITY to\n"
	.string "the routes beyond.\p"
	.string "Watch your step around the ledges.$"

OreburghGate_1F_Text_Hiker2:
	.string "I heard there's good training on the\n"
	.string "routes nearby.\p"
	.string "Might head that way once I catch my\n"
	.string "breath.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

OreburghGate_1F_EventScript_Npc1::
	msgbox OreburghGate_1F_Text_Npc1, MSGBOX_NPC
	end

OreburghGate_1F_Text_Npc1:
	.string "Oh! Good golly!\nThat's Oreburgh City's Gym Badge!\pAll right! Now you can use the hidden\nmove Rock Smash on small boulders!$"
