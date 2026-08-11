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

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

OreburghCity_Flat1_F1_EventScript_Npc1::
	msgbox OreburghCity_Flat1_F1_Text_Npc1, MSGBOX_NPC
	end

OreburghCity_Flat1_F1_Text_Npc1:
	.string "There are eight Gym Leaders in the\nSinnoh region.\pThe objective for Trainers is to get\nGym Badges from them all.\pThat means you have to defeat all of\nthem in battles at their Gyms!$"

OreburghCity_Flat1_F1_EventScript_Npc2::
	msgbox OreburghCity_Flat1_F1_Text_Npc2, MSGBOX_NPC
	end

OreburghCity_Flat1_F1_Text_Npc2:
	.string "A Gym Leader isn't like just any Trainer\nyou meet.\pObviously, they're a lot tougher.\nA lot.\pI'd take as many Pokémon as possible\nif I were you.$"

OreburghCity_Flat1_F1_EventScript_Npc3::
	msgbox OreburghCity_Flat1_F1_Text_Npc3, MSGBOX_NPC
	end

OreburghCity_Flat1_F1_Text_Npc3:
	.string "Roark lets us train our Pokémon in\nthe mine.$"
