Route208_Access_MapScripts::
	.byte 0

Route208_Access_EventScript_Guard::
	msgbox Route208_Access_Text_Guard, MSGBOX_NPC
	end

Route208_Access_Text_Guard:
	.string "This gate leads out to ROUTE 208.\p"
	.string "Safe travels, Trainer.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route208_Access_EventScript_Npc1::
	msgbox Route208_Access_Text_Npc1, MSGBOX_NPC
	end

Route208_Access_Text_Npc1:
	.string "Hearthome City is a great place.\pEvery year, it gets voted the most\ndesirable place to live in Sinnoh.$"

Route208_Access_EventScript_Npc2::
	msgbox Route208_Access_Text_Npc2, MSGBOX_NPC
	end

Route208_Access_Text_Npc2:
	.string "If you say Hearthome City, I only\nsay this: Pokémon Contests!\pI'm going to enter my darling\nPokémon in them!$"

Route208_Access_EventScript_Npc3::
	msgbox Route208_Access_Text_Npc3, MSGBOX_NPC
	end

Route208_Access_Text_Npc3:
	.string "CLEFAIRY: Pippii?!$"
