@ NimbasaSubway do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_NimbasaSubway_MapScripts::
	.byte 0

Unova_NimbasaSubway_EventScript_Npc0::
	msgbox Unova_NimbasaSubway_Text_NimbasaSubwayAskRideText, MSGBOX_NPC
	end

@ B6 Unova, Fase B (18/08/2026): Script_ArriveFromAspertia@11,6 da fonte
@ (o `;playmusic` da fonte ja vem comentado la, nao entra aqui). Sem
@ checkevent, so recepcao de chegada. Oficial e id local 1 (Npc0). VAR_TEMP_0/0
@ de sempre disparar. Zero flag e zero var novas.
Unova_NimbasaSubway_EventScript_Chegada::
	lock
	applymovement 1, Unova_NimbasaSubway_Movement_OficialChega
	applymovement LOCALID_PLAYER, Unova_NimbasaSubway_Movement_JogadorChega
	waitmovement 0
	applymovement 1, Unova_NimbasaSubway_Movement_OficialVolta
	waitmovement 0
	msgbox Unova_NimbasaSubway_Text_NimbasaSubwayArrivedText, MSGBOX_DEFAULT
	closemessage
	release
	end

Unova_NimbasaSubway_Movement_OficialChega::
	walk_up
	walk_up
	walk_right
	face_left
	step_end

Unova_NimbasaSubway_Movement_JogadorChega::
	walk_left
	walk_left
	walk_down
	walk_down
	walk_down
	walk_down
	face_up
	step_end

Unova_NimbasaSubway_Movement_OficialVolta::
	walk_left
	walk_down
	walk_down
	step_end

Unova_NimbasaSubway_EventScript_Npc1::
	msgbox Unova_NimbasaSubway_Text_NimbasaSubwayGentlemanText, MSGBOX_NPC
	end


Unova_NimbasaSubway_Text_NimbasaSubwayAskRideText::
	.string "We'll soon depart"
	.string "\nfor ASPERTIA."
	.string "\pAre you coming"
	.string "\naboard?$"

Unova_NimbasaSubway_Text_NimbasaSubwayArrivedText::
	.string "We have arrived in"
	.string "\nNIMBASA."
	.string "\pWe hope to see you"
	.string "\nagain.$"

Unova_NimbasaSubway_Text_NimbasaSubwayGentlemanText::
	.string "This used to be a"
	.string "\nBATTLE SUBWAY."
	.string "\pBut the need grew"
	.string "\nfor a regular"
	.string "\lsubway to take"
	.string "\ppeople and POKéMON"
	.string "\nto far corners of"
	.string "\lUNOVA.$"
