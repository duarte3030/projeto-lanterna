Route213_Access_MapScripts::
	.byte 0

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route213_Access_EventScript_Npc1::
	msgbox Route213_Access_Text_Npc1, MSGBOX_NPC
	end

Route213_Access_Text_Npc1:
	.string "Footprints are left in the sand\nwhen you walk on a beach.\pPokémon seem to enjoy leaving\nfootprints as much as people.$"

Route213_Access_EventScript_Npc2::
	msgbox Route213_Access_Text_Npc2, MSGBOX_NPC
	end

Route213_Access_Text_Npc2:
	.string "Listen, do you know about the Battle\nFrontier?$"
