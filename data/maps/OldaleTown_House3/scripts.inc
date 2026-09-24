@ OldaleTown_House3: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 2.5) por dev_scripts/copia_planta_ex.py.

OldaleTown_House3_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 2.5), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
OldaleTown_House3_EventScript_ExNpc0::
	msgbox OldaleTown_House3_Text_ExNpc0, MSGBOX_NPC
	end

OldaleTown_House3_Text_ExNpc0:
	.string "OLDALE TOWN is such a peaceful place.\n"
	.string "My family has been here three\l"
	.string "generations.$"

OldaleTown_House3_EventScript_ExNpc1::
	msgbox OldaleTown_House3_Text_ExNpc1, MSGBOX_NPC
	end

OldaleTown_House3_Text_ExNpc1:
	.string "If I do this long enough there will be\n"
	.string "permanent marks on the rug!$"

