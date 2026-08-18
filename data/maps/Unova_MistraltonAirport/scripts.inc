@ MistraltonAirport do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_MistraltonAirport_MapScripts::
	.byte 0

Unova_MistraltonAirport_EventScript_Npc0::
	msgbox Unova_MistraltonAirport_Text_MistraltonAirportRideText, MSGBOX_NPC
	end

@ B6 Unova, Fase B (18/08/2026): Script_ArriveFromLentimas@7,5 da fonte,
@ irma de Unova_LentimasAirport (mesmo padrao, mesma recepcionista id local
@ 1). Cortado de proposito (nao muda o jogo): o `show_person` no PLAYER,
@ mesmo motivo. VAR_TEMP_0/0 de sempre disparar. Zero flag e zero var novas.
Unova_MistraltonAirport_EventScript_Chegada::
	lock
	applymovement 1, Unova_MistraltonAirport_Movement_RecepcionistaChega
	applymovement LOCALID_PLAYER, Unova_MistraltonAirport_Movement_JogadorChega
	waitmovement 0
	applymovement 1, Unova_MistraltonAirport_Movement_RecepcionistaVolta
	waitmovement 0
	msgbox Unova_MistraltonAirport_Text_MistraltonAirportArrivedText, MSGBOX_DEFAULT
	closemessage
	release
	end

Unova_MistraltonAirport_Movement_RecepcionistaChega::
	walk_down
	walk_left
	face_right
	step_end

Unova_MistraltonAirport_Movement_JogadorChega::
	walk_down
	walk_down
	walk_down
	face_up
	step_end

Unova_MistraltonAirport_Movement_RecepcionistaVolta::
	walk_right
	walk_up
	face_down
	step_end

Unova_MistraltonAirport_EventScript_Npc1::
	msgbox Unova_MistraltonAirport_Text_MistraltonAirportPokefanFText, MSGBOX_NPC
	end

Unova_MistraltonAirport_EventScript_Npc2::
	msgbox Unova_MistraltonAirport_Text_MistraltonAirportOfficerText, MSGBOX_NPC
	end

Unova_MistraltonAirport_EventScript_Npc3::
	msgbox Unova_MistraltonAirport_Text_MistraltonAirportAskHeartScaleText, MSGBOX_NPC
	end


Unova_MistraltonAirport_Text_MistraltonAirportRideText::
	.string "Welcome to the"
	.string "\nMISTRALTON CITY"
	.string "\lairport."
	.string "\pWe offer flights"
	.string "\nto LENTIMAS TOWN."
	.string "\pAre you coming"
	.string "\non board?$"

Unova_MistraltonAirport_Text_MistraltonAirportPokefanFText::
	.string "I'm planning my"
	.string "\ntrip to LENTIMAS"
	.string "\lTOWN."
	.string "\pIt will be nice to"
	.string "\nspend some time"
	.string "\pout in the"
	.string "\nmountains.$"

Unova_MistraltonAirport_Text_MistraltonAirportOfficerText::
	.string "We mostly ship out"
	.string "\ncargo planes, but"
	.string "\lYou can take a"
	.string "\ppassenger flight"
	.string "\nif you have a"
	.string "\lBOARDINGPASS.$"

Unova_MistraltonAirport_Text_MistraltonAirportArrivedText::
	.string "Thank you for"
	.string "\nflying MISTRALTON"
	.string "\lAIRWAYS."
	.string "\pEnjoy your trip!$"

Unova_MistraltonAirport_Text_MistraltonAirportAskHeartScaleText::
	.string "Hi, I'm looking"
	.string "\nfor HEART SCALES!"
	.string "\pIf you have a"
	.string "\nHEART SCALE, would"
	.string "\pyou mind giving it"
	.string "\nto me in exchange"
	.string "\lfor a SHARD?$"
