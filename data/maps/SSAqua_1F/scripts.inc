SSAqua_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SSAqua_1F_OnTransition
	.byte 0

@ Primeira vez a bordo. As quatro flags e o valor 1 sao os mesmos de
@ `OlivinePort_EventScript_Sailor_MaidenVoyage` do hns, e a ordem importa:
@ o avo tem que estar VISIVEL (flag apagada) ja quando o mapa carrega, porque
@ `SSAqua_1F_Trigger_Grandpa` faz `applymovement` nele. Com ele escondido o
@ objeto nao existe, o `waitmovement 0` nunca volta e o jogo trava de pe no
@ corredor. Medido no emulador em 05/08/2026, nao deduzido.
@ Numa save antiga toda flag vale 0, entao a inicializacao tem que ser em jogo,
@ e o VAR_SSAQUA_STATE >= 1 impede que ela repita depois que o enredo andou.
SSAqua_1F_OnTransition::
	goto_if_ge VAR_SSAQUA_STATE, 1, SSAqua_1F_OnTransition_Fim
	clearflag FLAG_HIDE_SSAQUA_1F_GRANDPA
	setflag FLAG_HIDE_SSAQUA_ROOM_SSE_GRANDDAUGHTER
	clearflag FLAG_HIDE_SSAQUA_SAILOR
	clearflag FLAG_HIDE_SSAQUA_CAPTAINS_ROOM_GRANDDAUGHTER
	setvar VAR_SSAQUA_STATE, 1
SSAqua_1F_OnTransition_Fim::
	end

SSAqua_1F_EventScript_DoorSailor::
	lock
	faceplayer
	goto_if_set FLAG_SSAQUA_RUMO_KANTO, SSAqua_1F_EventScript_DoorSailorVermilion
	msgbox SSAqua_1F_Text_SailorDoorArrivedOlivine, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, TRUE, SSAqua_1F_EventScript_LeaveBoatOlivine
	goto SSAqua_1F_EventScript_StayAboard

SSAqua_1F_EventScript_DoorSailorVermilion::
	msgbox SSAqua_1F_Text_SailorDoorArrived, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, TRUE, SSAqua_1F_EventScript_LeaveBoatVermilion
	goto SSAqua_1F_EventScript_StayAboard

SSAqua_1F_EventScript_StayAboard::
	msgbox SSAqua_1F_Text_Sailor1_ToVermilion, MSGBOX_DEFAULT
	closemessage
	release
	end

SSAqua_1F_EventScript_LeaveBoatVermilion::
	closemessage
	warp MAP_VERMILION_CITY, 15, 10
	waitstate
	release
	end

SSAqua_1F_EventScript_LeaveBoatOlivine::
	closemessage
	warp MAP_OLIVINE_CITY_PORT_INSIDE, 8, 17
	waitstate
	release
	end

SSAqua_1F_Text_SailorDoorArrivedOlivine:
	.string "We have arrived in OLIVINE CITY.\n"
	.string "Would you like to disembark?$"

.set LOCALID_SSAQUA_1F_DOORSAILOR, 4
.set LOCALID_SSAQUA_1F_GRANDPA, 2

SSAqua_1F_EventScript_RoomSailor::
	msgbox SSAqua_1F_Text_Sailor2_FirstTime, MSGBOX_NPC
	end

SSAqua_1F_EventScript_Sailor3::
	msgbox SSAqua_1F_Text_Sailor3, MSGBOX_NPC
	end

SSAqua_1F_Trigger_Grandpa::
	lock
	clearflag FLAG_HIDE_SSAQUA_1F_GRANDPA
	getplayerxy VAR_TEMP_0, VAR_TEMP_1
	call_if_eq VAR_TEMP_0, 28, SSAqua_1F_EventScript_GrandpaEnterLeft
	call_if_eq VAR_TEMP_0, 29, SSAqua_1F_EventScript_GrandpaEnterRight
	applymovement OBJ_EVENT_ID_PLAYER, SSAqua_1F_Movement_PlayerSlideRight
	waitmovement 0
	applymovement LOCALID_SSAQUA_1F_GRANDPA, Common_Movement_WalkRight
	waitmovement 0
	msgbox SSAqua_1F_Text_Grandpa, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SSAQUA_1F_GRANDPA, SSAqua_1F_Movement_GrandpaLeave
	waitmovement 0
	playse SE_DOOR
	removeobject LOCALID_SSAQUA_1F_GRANDPA
	
	setflag FLAG_HIDE_SSAQUA_1F_GRANDPA		@flagheap
	setflag FLAG_HIDE_SSAQUA_ROOM_SSE_GRANDDAUGHTER

	clearflag FLAG_HIDE_SSAQUA_SAILOR
	clearflag FLAG_HIDE_SSAQUA_CAPTAINS_ROOM_GRANDDAUGHTER

	setvar VAR_SSAQUA_STATE, 2
	release
	end

SSAqua_1F_EventScript_GrandpaEnterLeft::
	applymovement LOCALID_SSAQUA_1F_GRANDPA, SSAqua_1F_Movement_GrandpaEnterLeft
	waitmovement 0
	return

SSAqua_1F_EventScript_GrandpaEnterRight::
	applymovement LOCALID_SSAQUA_1F_GRANDPA, SSAqua_1F_Movement_GrandpaEnterRight
	waitmovement 0
	return

SSAqua_1F_Movement_GrandpaEnterLeft:
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	step_end

SSAqua_1F_Movement_GrandpaEnterRight:
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	step_end

SSAqua_1F_Movement_PlayerSlideRight:
	face_left
	lock_facing_direction
	walk_fast_right
	unlock_facing_direction
	step_end

SSAqua_1F_Movement_GrandpaLeave:
	walk_fast_down
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	step_end

SSAqua_1F_Text_Sailor1_ToVermilion:
    .string "FAST SHIP S.S.AQUA is en route to\n"
    .string "VERMILION CITY.\p"
    .string "We will make an announcement when\n"
    .string "we arrive.$"

SSAqua_1F_Text_Sailor1_ToOlivine:
    .string "FAST SHIP S.S.AQUA is en route to\n"
    .string "OLIVINE CITY.\p"
    .string "We will make an announcement when\n"
    .string "we arrive.$"

SSAqua_1F_Text_Sailor2_FirstTime:
    .string "Here's your cabin.\p"
    .string "If your POKéMON are hurt, take a\n"
    .string "nap in the bed.\p"
    .string "That will heal them.$"

SSAqua_1F_Text_Sailor3:
    .string "The passengers are all trainers.\p"
    .string "They're all itching to battle in\n"
    .string "their cabins.$"

SSAqua_1F_Text_Grandpa:
    .string "Whoa! Excuse me. I was in a hurry!\p"
    .string "My granddaughter is missing!\p"
    .string "She's just a wee girl. If you see\n"
    .string "her, please let me know!$"

SSAqua_1F_Text_Sailor1_InOlivine:
    .string "FAST SHIP S.S.AQUA has arrived in\n"
    .string "OLIVINE CITY.$"

SSAqua_1F_Text_Sailor1_InVermilion:
    .string "FAST SHIP S.S.AQUA has arrived in\n"
    .string "VERMILION CITY.$"


SSAqua_1F_Text_SailorDoorArrived:
    .string "We have arrived in VERMILION CITY.\n"
    .string "Would you like to disembark?$"
