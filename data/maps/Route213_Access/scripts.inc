Route213_Access_MapScripts::
	.byte 0

Route213_Access_EventScript_Fisherman::
	msgbox Route213_Access_Text_Fisherman, MSGBOX_NPC
	end

Route213_Access_EventScript_Tourist::
	msgbox Route213_Access_Text_Tourist, MSGBOX_NPC
	end

Route213_Access_Text_Fisherman:
	.string "PASTORIA CITY has some of the best\n"
	.string "fishing spots around.$"

Route213_Access_Text_Tourist:
	.string "I heard there's a huge marsh near\n"
	.string "here. I can't wait to see it!$"

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
