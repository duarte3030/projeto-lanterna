@ OldaleTown_CommunityCenter: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 2.7) por dev_scripts/copia_planta_ex.py.

OldaleTown_CommunityCenter_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 2.7), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
OldaleTown_CommunityCenter_EventScript_ExNpc0::
	msgbox OldaleTown_CommunityCenter_Text_ExNpc0, MSGBOX_NPC
	end

OldaleTown_CommunityCenter_Text_ExNpc0:
	.string "Welcome to the OLDALE TOWN community\n"
	.string "center.\l"
	.string "I made this as a place for young people\l"
	.string "to gather and have fun. But for some\l"
	.string "reason only my kids come here.$"

OldaleTown_CommunityCenter_EventScript_ExNpc1::
	msgbox OldaleTown_CommunityCenter_Text_ExNpc1, MSGBOX_NPC
	end

OldaleTown_CommunityCenter_Text_ExNpc1:
	.string "I’m looking for a picture book with\n"
	.string "POKéMON in it. But all these only have\l"
	.string "words in them.$"

OldaleTown_CommunityCenter_EventScript_ExNpc2::
	msgbox OldaleTown_CommunityCenter_Text_ExNpc2, MSGBOX_NPC
	end

OldaleTown_CommunityCenter_Text_ExNpc2:
	.string "Dad wants my friends to hang out here,\n"
	.string "but the only thing to do here is read\l"
	.string "his textbooks.$"

