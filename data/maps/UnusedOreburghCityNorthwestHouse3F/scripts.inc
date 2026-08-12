UnusedOreburghCityNorthwestHouse3F_MapScripts::
	.byte 0

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

UnusedOreburghCityNorthwestHouse3F_EventScript_Npc1::
	msgbox UnusedOreburghCityNorthwestHouse3F_Text_Npc1, MSGBOX_NPC
	end

UnusedOreburghCityNorthwestHouse3F_Text_Npc1:
	.string "PSYDUCK: Duuuck?$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

UnusedOreburghCityNorthwestHouse3F_EventScript_Npc2::
	bufferitemname STR_VAR_1, ITEM_HARD_STONE
	msgbox UnusedOreburghCityNorthwestHouse3F_Text_Npc2, MSGBOX_NPC
	end

UnusedOreburghCityNorthwestHouse3F_Text_Npc2:
	.string "Do you make your Pokémon hold items?\pIf you'd like, let one hold this\n{STR_VAR_1}.$"
