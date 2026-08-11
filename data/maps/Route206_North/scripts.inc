Route206_North_MapScripts::
	.byte 0

Route206_North_EventScript_Guard::
	msgbox Route206_North_Text_Guard, MSGBOX_NPC
	end

Route206_North_Text_Guard:
	.string "You're at the northern crossing of\n"
	.string "ROUTE 206.\p"
	.string "Mind the cyclists coming through.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route206_North_EventScript_Npc1::
	msgbox Route206_North_Text_Npc1, MSGBOX_NPC
	end

Route206_North_Text_Npc1:
	.string "Learn how to shift gears, and you'll\nbe able to ride anywhere.$"

Route206_North_EventScript_Npc2::
	msgbox Route206_North_Text_Npc2, MSGBOX_NPC
	end

Route206_North_Text_Npc2:
	.string "Learn how to shift gears, and you'll\nbe able to ride anywhere.$"
