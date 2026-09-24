@ PetalburgWoods_RestStop: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 19.3) por dev_scripts/copia_planta_ex.py.

PetalburgWoods_RestStop_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 19.3), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
PetalburgWoods_RestStop_EventScript_ExNpc1::
	msgbox PetalburgWoods_RestStop_Text_ExNpc1, MSGBOX_NPC
	end

PetalburgWoods_RestStop_Text_ExNpc1:
	.string "Man.\p"
	.string "GYM LEADER SAM really doesn’t hold\n"
	.string "back.\p"
	.string "It’s nice of him to run this rest stop\n"
	.string "here though! It makes it easier to\l"
	.string "challenge the GYM!$"


@ EX obj 0: o menino do balcão cura o time (no EX, loadword + callstd 2, a rotina de cura
@ fora do Centro e o texto final com callstd 4). Aqui a mesma rotina nossa.
PetalburgWoods_RestStop_EventScript_ExCura::
	lock
	faceplayer
	msgbox PetalburgWoods_RestStop_Text_ExCura, MSGBOX_DEFAULT
	call Common_EventScript_OutOfCenterPartyHeal
	msgbox PetalburgWoods_RestStop_Text_ExCuraFim, MSGBOX_DEFAULT
	release
	end

PetalburgWoods_RestStop_Text_ExCura:
	.string "These WOODS can be rough.\n"
	.string "Let me see your POKéMON.$"

PetalburgWoods_RestStop_Text_ExCuraFim:
	.string "Good luck at the GYM.$"
