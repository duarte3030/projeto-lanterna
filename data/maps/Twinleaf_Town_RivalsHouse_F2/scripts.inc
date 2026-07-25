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
