@ LentimasAirport do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_LentimasAirport_MapScripts::
	.byte 0

Unova_LentimasAirport_EventScript_Npc0::
	msgbox Unova_LentimasAirport_Text_LentimasAirportRideText, MSGBOX_NPC
	end

@ B6 Unova, Fase B (18/08/2026): Script_ArriveFromMistralton@5,1 da fonte.
@ Sem checkevent, so recepcao de chegada de voo. Cortado de proposito (nao
@ muda o jogo): o `show_person` da fonte no PLAYER (id local 1 = a
@ RECEPCIONISTA, Npc0), que so existe para desfazer a invisibilidade do
@ jogador durante a transicao do gen2; o motor daqui ja mostra o jogador
@ normalmente no warp-in. VAR_TEMP_0/0 de sempre disparar. Zero flag e
@ zero var novas.
Unova_LentimasAirport_EventScript_Chegada::
	lock
	applymovement 1, Unova_LentimasAirport_Movement_RecepcionistaChega
	applymovement LOCALID_PLAYER, Unova_LentimasAirport_Movement_JogadorChega
	waitmovement 0
	applymovement 1, Unova_LentimasAirport_Movement_RecepcionistaVolta
	waitmovement 0
	msgbox Unova_LentimasAirport_Text_LentimasAirportArrivedText, MSGBOX_DEFAULT
	closemessage
	release
	end

Unova_LentimasAirport_Movement_RecepcionistaChega::
	walk_down
	walk_left
	face_right
	step_end

Unova_LentimasAirport_Movement_JogadorChega::
	walk_down
	walk_down
	walk_down
	face_up
	step_end

Unova_LentimasAirport_Movement_RecepcionistaVolta::
	walk_right
	walk_up
	face_down
	step_end

Unova_LentimasAirport_EventScript_Npc1::
	msgbox Unova_LentimasAirport_Text_LentimasAirportLassText, MSGBOX_NPC
	end

Unova_LentimasAirport_EventScript_Npc2::
	msgbox Unova_LentimasAirport_Text_LentimasAirportKrokorokText, MSGBOX_NPC
	end


Unova_LentimasAirport_Text_LentimasAirportRideText::
	.string "Welcome to the"
	.string "\nLENTIMAS TOWN"
	.string "\lairport."
	.string "\pWe offer flights"
	.string "\nto MISTRALTON"
	.string "\lCITY."
	.string "\pAre you coming"
	.string "\non board?$"

Unova_LentimasAirport_Text_LentimasAirportLassText::
	.string "I'm fine even"
	.string "\nright by a volcano"
	.string "\pthanks to my lil"
	.string "\nKROKOROK! It"
	.string "\lreally rocks!$"

Unova_LentimasAirport_Text_LentimasAirportKrokorokText::
	.string "Krakaah!$"

Unova_LentimasAirport_Text_LentimasAirportArrivedText::
	.string "Thank you for"
	.string "\nflying MISTRALTON"
	.string "\lAIRWAYS."
	.string "\pEnjoy your trip!$"
