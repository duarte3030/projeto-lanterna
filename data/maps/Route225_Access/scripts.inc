Route225_Access_MapScripts::
	.byte 0

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route225_Access_EventScript_Npc1::
	msgbox Route225_Access_Text_Npc1, MSGBOX_NPC
	end

Route225_Access_Text_Npc1:
	.string "To the north is the Survival Area and\nthen Stark Mountain.\pThe road there is too tough for me to\ntravel, though.$"

Route225_Access_EventScript_Npc2::
	msgbox Route225_Access_Text_Npc2, MSGBOX_NPC
	end

Route225_Access_Text_Npc2:
	.string "Are you stocked up on Poké Balls?\pIn the tall grass past here, you'll find\ninteresting Pokémon.\pLike, Pokémon you never see anywhere\nelse in Sinnoh!$"
