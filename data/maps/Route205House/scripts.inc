Route205House_MapScripts::
	.byte 0

Route205House_EventScript_Npc1::
	msgbox Route205House_Text_Npc1, MSGBOX_NPC
	end

Route205House_Text_Npc1:
	.string "You seem to be tired...\nRest a while.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route205House_EventScript_Npc2::
	msgbox Route205House_Text_Npc2, MSGBOX_NPC
	end

Route205House_Text_Npc2:
	.string "Repels are useful, don't you think?\pWhen you use a Repel, weak Pokémon\nwon't come out.\p...But that also means there won't be\nany Pokémon to capture.$"
