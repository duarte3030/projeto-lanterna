@ HauntedWoods_Inner: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 27.115) por dev_scripts/copia_planta_ex.py.

HauntedWoods_Inner_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 27.115), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
HauntedWoods_Inner_EventScript_ExNpc1::
	msgbox HauntedWoods_Inner_Text_ExNpc1, MSGBOX_NPC
	end

HauntedWoods_Inner_Text_ExNpc1:
	.string "GHOST POKéMON gather here due to the\n"
	.string "strong emotions that fill this place.\p"
	.string "GHOSTs thrive on strong emotions.$"

HauntedWoods_Inner_EventScript_ExNpc2::
	msgbox HauntedWoods_Inner_Text_ExNpc2, MSGBOX_NPC
	end

HauntedWoods_Inner_Text_ExNpc2:
	.string "I come out here to clean the graves.\p"
	.string "Many of them are older than I am and\n"
	.string "have no one to care for them.\p"
	.string "I hope they will be cared for when I’m\n"
	.string "gone.$"

HauntedWoods_Inner_EventScript_ExNpc3::
	msgbox HauntedWoods_Inner_Text_ExNpc3, MSGBOX_NPC
	end

HauntedWoods_Inner_Text_ExNpc3:
	.string "SNIFF...\n"
	.string "I guess some things can’t last\l"
	.string "forever...$"

