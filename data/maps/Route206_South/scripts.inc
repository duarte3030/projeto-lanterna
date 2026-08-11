Route206_South_MapScripts::
	.byte 0

Route206_South_EventScript_Guard::
	msgbox Route206_South_Text_Guard, MSGBOX_NPC
	end

Route206_South_Text_Guard:
	.string "Southern gate of ROUTE 206.\p"
	.string "Watch for CYCLING ROAD traffic on\n"
	.string "your way.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route206_South_EventScript_Npc1::
	msgbox Route206_South_Text_Npc1, MSGBOX_NPC
	end

Route206_South_Text_Npc1:
	.string "Learn how to shift gears, and you'll\nbe able to ride anywhere.$"

Route206_South_EventScript_Npc2::
	msgbox Route206_South_Text_Npc2, MSGBOX_NPC
	end

Route206_South_Text_Npc2:
	.string "Learn how to shift gears, and you'll\nbe able to ride anywhere.$"

Route206_South_EventScript_Npc3::
	msgbox Route206_South_Text_Npc3, MSGBOX_NPC
	end

Route206_South_Text_Npc3:
	.string "What's a Bicycle without this?\pYou've got to have a Flag!\nIt's a Pokémon Accessory!$"
