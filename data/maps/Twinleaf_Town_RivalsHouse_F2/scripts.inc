Twinleaf_Town_RivalsHouse_F2_MapScripts::
	.byte 0

Twinleaf_Town_RivalsHouse_F2_EventScript_Sister::
	msgbox Twinleaf_Town_RivalsHouse_F2_Text_Sister, MSGBOX_NPC
	end

Twinleaf_Town_RivalsHouse_F2_EventScript_PCNote::
	msgbox Twinleaf_Town_RivalsHouse_F2_Text_PCNote, MSGBOX_SIGN
	end

Twinleaf_Town_RivalsHouse_F2_Text_Sister:
	.string "My brother is always in such a hurry.\n"
	.string "He forgot his bag again!$"

Twinleaf_Town_RivalsHouse_F2_Text_PCNote:
	.string "A note taped to the PC screen.\p"
	.string "Adventure Rule No. 1: The X Button\n"
	.string "opens the menu!\p"
	.string "Adventure Rule No. 2: Record your\n"
	.string "progress with SAVE.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Twinleaf_Town_RivalsHouse_F2_EventScript_Placa1::
	msgbox Twinleaf_Town_RivalsHouse_F2_Text_Placa1, MSGBOX_SIGN
	end

Twinleaf_Town_RivalsHouse_F2_Text_Placa1:
	.string "It's a Wii!\nIt's controlled by a Wii Remote!$"

Twinleaf_Town_RivalsHouse_F2_EventScript_Placa2::
	msgbox Twinleaf_Town_RivalsHouse_F2_Text_Placa2, MSGBOX_SIGN
	end

Twinleaf_Town_RivalsHouse_F2_Text_Placa2:
	.string "{PLAYER} checked the PC screen.\pAdventure Rule No. 1\nThe X Button opens the menu!\pAdventure Rule No. 2\nRecord your progress with SAVE.\pThere is nothing else on here...$"
