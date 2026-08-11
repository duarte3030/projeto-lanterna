Route209_Access_MapScripts::
	.byte 0

Route209_Access_EventScript_Guard::
	msgbox Route209_Access_Text_Guard, MSGBOX_NPC
	end

Route209_Access_Text_Guard:
	.string "This gate leads out to ROUTE 209.\p"
	.string "Watch your step on the way out.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route209_Access_EventScript_Npc1::
	msgbox Route209_Access_Text_Npc1, MSGBOX_NPC
	end

Route209_Access_Text_Npc1:
	.string "There's a wrecked stone pillar up\nahead.\pI wonder what it is?\nIt's got me very curious.$"
