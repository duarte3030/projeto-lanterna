SafariZone_Southwest_MapScripts::
	.byte 0

SafariZone_Southwest_EventScript_Woman::
	msgbox SafariZone_Southwest_Text_Woman, MSGBOX_NPC
	end

SafariZone_Southwest_EventScript_RestHouseSign::
	msgbox SafariZone_Southwest_Text_RestHouseSign, MSGBOX_SIGN
	end


@ Eventos novos do Pokémon Emerald EX (mapa 29.2), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
SafariZone_Southwest_EventScript_ExNpc2::
	msgbox SafariZone_Southwest_Text_ExNpc2, MSGBOX_NPC
	end

SafariZone_Southwest_Text_ExNpc2:
	.string "I made a whole bunch of POKéBLOCKs, but\n"
	.string "none of the POKéMON seem to like them...\p"
	.string "They must have the wrong NATURE for\n"
	.string "the POKéBLOCKs...$"

SafariZone_Southwest_EventScript_ExNpc4::
	msgbox SafariZone_Southwest_Text_ExNpc4, MSGBOX_NPC
	end

SafariZone_Southwest_Text_ExNpc4:
	.string "I saw a POKéMON with fire on it’s tail on\n"
	.string "top of this cliff.\p"
	.string "But, I can’t find a way up!$"

