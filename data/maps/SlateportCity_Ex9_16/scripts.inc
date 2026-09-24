@ SlateportCity_Ex9_16: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 9.16) por dev_scripts/copia_planta_ex.py.

SlateportCity_Ex9_16_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 9.16), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
SlateportCity_Ex9_16_EventScript_ExNpc0::
	msgbox SlateportCity_Ex9_16_Text_ExNpc0, MSGBOX_NPC
	end

SlateportCity_Ex9_16_Text_ExNpc0:
	.string "I just can’t beat LEADER GRETA!\p"
	.string "Maybe I should head to GRANITE CAVE\n"
	.string "and catch a FIGHTING TYPE POKéMON.$"

SlateportCity_Ex9_16_EventScript_ExNpc1::
	msgbox SlateportCity_Ex9_16_Text_ExNpc1, MSGBOX_NPC
	end

SlateportCity_Ex9_16_Text_ExNpc1:
	.string "GRETA is a powerful trainer.\n"
	.string "She even uses rare POKéMON from the\l"
	.string "other side of the HOENN REGION!$"

