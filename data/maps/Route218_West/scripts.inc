Route218_West_MapScripts::
	.byte 0

Route218_West_EventScript_Sailor::
	msgbox Route218_West_Text_Sailor, MSGBOX_NPC
	end

Route218_West_Text_Sailor:
	.string "CANALAVE CITY's harbor is right\n"
	.string "past this passage.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route218_West_EventScript_Npc1::
	msgbox Route218_West_Text_Npc1, MSGBOX_NPC
	end

Route218_West_Text_Npc1:
	.string "Boy...\nI sure am thirsty...$"
