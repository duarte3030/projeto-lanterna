@ PetalburgCity_House6: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 8.10) por dev_scripts/copia_planta_ex.py.

PetalburgCity_House6_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 8.10), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
PetalburgCity_House6_EventScript_ExNpc0::
	msgbox PetalburgCity_House6_Text_ExNpc0, MSGBOX_NPC
	end

PetalburgCity_House6_Text_ExNpc0:
	.string "What should I make for dinner?$"

PetalburgCity_House6_EventScript_ExNpc2::
	msgbox PetalburgCity_House6_Text_ExNpc2, MSGBOX_NPC
	end

PetalburgCity_House6_Text_ExNpc2:
	.string "My husbands food is amazing, but\n"
	.string "sometimes I wish he would cook\l"
	.string "something new.$"

