@ PetalburgCity_House4: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 8.8) por dev_scripts/copia_planta_ex.py.

PetalburgCity_House4_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 8.8), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
PetalburgCity_House4_EventScript_ExNpc0::
	msgbox PetalburgCity_House4_Text_ExNpc0, MSGBOX_NPC
	end

PetalburgCity_House4_Text_ExNpc0:
	.string "I sure love to read!$"

PetalburgCity_House4_EventScript_ExNpc1::
	msgbox PetalburgCity_House4_Text_ExNpc1, MSGBOX_NPC
	end

PetalburgCity_House4_Text_ExNpc1:
	.string "I bought all these books for my son.\p"
	.string "I hope that he will grow up to be a\n"
	.string "scientist!$"

