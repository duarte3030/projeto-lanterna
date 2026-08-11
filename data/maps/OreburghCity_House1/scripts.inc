OreburghCity_House1_MapScripts::
	.byte 0

OreburghCity_House1_EventScript_Worker::
	msgbox OreburghCity_House1_Text_Worker, MSGBOX_NPC
	end

OreburghCity_House1_Text_Worker:
	.string "I work the coal carts down at the\n"
	.string "MINE. Hard work, but honest work.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

OreburghCity_House1_EventScript_Npc1::
	msgbox OreburghCity_House1_Text_Npc1, MSGBOX_NPC
	end

OreburghCity_House1_Text_Npc1:
	.string "Roark is a user of Rock-type Pokémon.\pDon't you think Rock-type Pokémon are\nnice? I like how lumpy they are!$"

OreburghCity_House1_EventScript_Npc2::
	msgbox OreburghCity_House1_Text_Npc2, MSGBOX_NPC
	end

OreburghCity_House1_Text_Npc2:
	.string "Roark is our town's Gym Leader.\pHe may be young, but he keeps the\nmine running safely and efficiently.$"
