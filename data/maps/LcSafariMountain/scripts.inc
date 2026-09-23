@ LcSafariMountain: mapa copiado de Pokémon Liquid Crystal.gba (g5m113) por
@ dev_scripts/copia_mapa_rom.py. A ARTE é do hack; o JOGO (warps, NPCs,
@ encontros, itens, placas) é NOSSO e está aqui.
@
@ A DANÇA DO ATENDENTE, copiada de data/maps/SafariZone_South/scripts.inc e
@ adaptada às coordenadas desta área. A porta é (9,44), o único warp do mapa, e
@ o atendente FICA EM CIMA dela: é ele que impede o jogador de sair andando sem
@ devolver as Safari Balls. Na hora em que o jogador chega, o atendente ainda
@ não pode estar ali (o jogador pousa nesse mesmo tile), então o OnTransition o
@ põe em (8,44), ao lado, ANTES de o mapa desenhar; o OnFrame sobe o jogador
@ para (9,43) e só então o atendente ocupa a porta.
@
@ Por que a SAÍDA não repete a coreografia de Hoenn. Lá o atendente sai do
@ caminho e o jogador anda até a porta, em dois casos escritos à mão
@ (DIR_NORTH e DIR_EAST), porque em Hoenn só existem esses dois tiles de onde
@ falar com ele. Aqui a porta tem TRÊS vizinhos andáveis, (8,44), (9,43) e
@ (10,44), e um quarto caso escrito à mão seria mais uma chance de o atendente
@ tentar andar para cima do jogador. `SafariZone_EventScript_Exit`
@ (data/scripts/safari_zone.inc) já faz o warp inteiro, lendo o `dynamicWarp`
@ que o balcão do portão gravou, de onde quer que o jogador esteja. Menos
@ coreografia, mesma saída, e é a MESMA saída do fim de tempo e do fim de bolas.

LcSafariMountain_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LcSafariMountain_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, LcSafariMountain_OnFrame
	.byte 0

LcSafariMountain_OnFrame:
	map_script_2 VAR_SAFARI_ZONE_STATE, 2, LcSafariMountain_EventScript_EnterSafariZone
	.2byte 0

LcSafariMountain_EventScript_EnterSafariZone::
	lockall
	applymovement LOCALID_PLAYER, LcSafariMountain_Movement_PlayerEnter
	waitmovement 0
	applymovement LOCALID_LC_SAFARI_MOUNTAIN_EXIT_ATTENDANT, LcSafariMountain_Movement_ExitAttendantBlockDoor
	waitmovement 0
	setobjectxyperm LOCALID_LC_SAFARI_MOUNTAIN_EXIT_ATTENDANT, 9, 44
	setvar VAR_SAFARI_ZONE_STATE, 0
	releaseall
	end

LcSafariMountain_OnTransition:
	call_if_eq VAR_SAFARI_ZONE_STATE, 2, LcSafariMountain_EventScript_SetExitAttendantAside
	end

LcSafariMountain_EventScript_SetExitAttendantAside::
	setobjectxyperm LOCALID_LC_SAFARI_MOUNTAIN_EXIT_ATTENDANT, 8, 44
	return

LcSafariMountain_Movement_PlayerEnter:
	walk_up
	step_end

LcSafariMountain_Movement_ExitAttendantBlockDoor:
	walk_right
	walk_in_place_faster_up
	step_end

LcSafariMountain_EventScript_ExitAttendant::
	lock
	faceplayer
	goto_if_unset FLAG_GOOD_LUCK_SAFARI_ZONE, LcSafariMountain_EventScript_GoodLuck
	msgbox LcSafariMountain_Text_StillHaveTimeExit, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, LcSafariMountain_EventScript_ExitEarly
	msgbox LcSafariMountain_Text_EnjoyTheRestOfYourAdventure, MSGBOX_DEFAULT
	release
	end

LcSafariMountain_EventScript_GoodLuck::
	setflag FLAG_GOOD_LUCK_SAFARI_ZONE
	msgbox LcSafariMountain_Text_GoodLuck, MSGBOX_DEFAULT
	release
	end

LcSafariMountain_EventScript_ExitEarly::
	msgbox LcSafariMountain_Text_ExitEarlyThankYouForPlaying, MSGBOX_DEFAULT
	closemessage
	goto SafariZone_EventScript_Exit
	end

LcSafariMountain_EventScript_Hiker::
	msgbox LcSafariMountain_Text_Hiker, MSGBOX_NPC
	end

LcSafariMountain_EventScript_BlackBelt::
	msgbox LcSafariMountain_Text_BlackBelt, MSGBOX_NPC
	end

LcSafariMountain_EventScript_GateSign::
	msgbox LcSafariMountain_Text_GateSign, MSGBOX_SIGN
	end

LcSafariMountain_EventScript_RidgeSign::
	msgbox LcSafariMountain_Text_RidgeSign, MSGBOX_SIGN
	end

LcSafariMountain_Text_StillHaveTimeExit::
	.string "You still have time left. Would you like\n"
	.string "to leave the MOUNTAIN AREA now?$"

LcSafariMountain_Text_EnjoyTheRestOfYourAdventure::
	.string "Then keep climbing!\n"
	.string "The ridge is worth the walk.$"

LcSafariMountain_Text_GoodLuck::
	.string "Welcome to the MOUNTAIN AREA!\p"
	.string "Watch your step on the rock stairs,\n"
	.string "and good luck out there!$"

LcSafariMountain_Text_ExitEarlyThankYouForPlaying::
	.string "Okay.\p"
	.string "I'll take back your remaining SAFARI\n"
	.string "BALLS.\p"
	.string "Thank you for playing.\n"
	.string "We hope to see you again.$"

LcSafariMountain_Text_Hiker::
	.string "This whole slope is loose sand.\p"
	.string "The POKéMON that live up here are\n"
	.string "hard as the rock they sleep on.$"

LcSafariMountain_Text_BlackBelt::
	.string "I train here every morning.\p"
	.string "Climb all the way to the top and you'll\n"
	.string "see why the fighting types love it.$"

LcSafariMountain_Text_GateSign::
	.string "SAFARI ZONE\n"
	.string "MOUNTAIN AREA\p"
	.string "“Rock, ground and fighting POKéMON.\n"
	.string "Mind the stairs.”$"

LcSafariMountain_Text_RidgeSign::
	.string "“Beyond this ridge, the sand gets\n"
	.string "deeper and the POKéMON get rarer.”$"
