Route218_East_MapScripts::
	.byte 0

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route218_East_EventScript_Npc1::
	msgbox Route218_East_Text_Npc1, MSGBOX_NPC
	end

Route218_East_Text_Npc1:
	.string "Route 218 up ahead is a great fishing\nhole that's almost unknown to people.$"

Route218_East_EventScript_Npc2::
	msgbox Route218_East_Text_Npc2, MSGBOX_NPC
	end

Route218_East_Text_Npc2:
	.string "Yes, sir!\nAn Old Rod is a good thing!\pYou think so too, am I right?$"
