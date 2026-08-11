SandgemTown_RivalHouse_F1_MapScripts::
	.byte 0

SandgemTown_RivalHouse_F1_EventScript_Expert::
	msgbox SandgemTown_RivalHouse_F1_Text_Expert, MSGBOX_NPC
	end

SandgemTown_RivalHouse_F1_EventScript_Twin::
	msgbox SandgemTown_RivalHouse_F1_Text_Twin, MSGBOX_NPC
	end

SandgemTown_RivalHouse_F1_Text_Expert:
	.string "Ah, so that ROWAN fellow is back?\n"
	.string "He's quite the remarkable man.\p"
	.string "He's been studying POKéMON since\n"
	.string "way, way back.$"

SandgemTown_RivalHouse_F1_Text_Twin:
	.string "Oh, hi! There was news on TV saying\n"
	.string "there's a massive outbreak of\l"
	.string "POKéMON! That'd be great for filling\n"
	.string "up your POKéDEX!$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SandgemTown_RivalHouse_F1_EventScript_Npc1::
	msgbox SandgemTown_RivalHouse_F1_Text_Npc1, MSGBOX_NPC
	end

SandgemTown_RivalHouse_F1_Text_Npc1:
	.string "Ah, so that Rowan fellow is back?\nHe's quite the remarkable man.\pHe's been studying Pokémon since way,\nway back.\pMy son and grandchild help Rowan\nwith his studies now.$"
