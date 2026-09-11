@ LcSafariForest: mapa copiado de Pokémon Liquid Crystal.gba (g5m115) por
@ dev_scripts/copia_mapa_rom.py. A ARTE é do hack; o JOGO (warps, NPCs,
@ encontros, itens, placas) é NOSSO e está aqui.
@
@ Mesma dança de atendente da montanha, com as coordenadas desta área: a porta
@ é (25,49), o atendente espera ao lado em (24,49) enquanto o jogador pousa, e
@ depois ocupa a porta. O motivo de cada linha está no comentário de
@ data/maps/LcSafariMountain/scripts.inc, que é o irmão mais velho deste.

LcSafariForest_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LcSafariForest_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, LcSafariForest_OnFrame
	.byte 0

LcSafariForest_OnFrame:
	map_script_2 VAR_SAFARI_ZONE_STATE, 2, LcSafariForest_EventScript_EnterSafariZone
	.2byte 0

LcSafariForest_EventScript_EnterSafariZone::
	lockall
	applymovement LOCALID_PLAYER, LcSafariForest_Movement_PlayerEnter
	waitmovement 0
	applymovement LOCALID_LC_SAFARI_FOREST_EXIT_ATTENDANT, LcSafariForest_Movement_ExitAttendantBlockDoor
	waitmovement 0
	setobjectxyperm LOCALID_LC_SAFARI_FOREST_EXIT_ATTENDANT, 25, 49
	setvar VAR_SAFARI_ZONE_STATE, 0
	releaseall
	end

LcSafariForest_OnTransition:
	call_if_eq VAR_SAFARI_ZONE_STATE, 2, LcSafariForest_EventScript_SetExitAttendantAside
	end

LcSafariForest_EventScript_SetExitAttendantAside::
	setobjectxyperm LOCALID_LC_SAFARI_FOREST_EXIT_ATTENDANT, 24, 49
	return

LcSafariForest_Movement_PlayerEnter:
	walk_up
	step_end

LcSafariForest_Movement_ExitAttendantBlockDoor:
	walk_right
	walk_in_place_faster_up
	step_end

LcSafariForest_EventScript_ExitAttendant::
	lock
	faceplayer
	goto_if_unset FLAG_GOOD_LUCK_SAFARI_ZONE, LcSafariForest_EventScript_GoodLuck
	msgbox LcSafariForest_Text_StillHaveTimeExit, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, LcSafariForest_EventScript_ExitEarly
	msgbox LcSafariForest_Text_EnjoyTheRestOfYourAdventure, MSGBOX_DEFAULT
	release
	end

LcSafariForest_EventScript_GoodLuck::
	setflag FLAG_GOOD_LUCK_SAFARI_ZONE
	msgbox LcSafariForest_Text_GoodLuck, MSGBOX_DEFAULT
	release
	end

LcSafariForest_EventScript_ExitEarly::
	msgbox LcSafariForest_Text_ExitEarlyThankYouForPlaying, MSGBOX_DEFAULT
	closemessage
	goto SafariZone_EventScript_Exit
	end

LcSafariForest_EventScript_BugCatcher::
	msgbox LcSafariForest_Text_BugCatcher, MSGBOX_NPC
	end

LcSafariForest_EventScript_Girl::
	msgbox LcSafariForest_Text_Girl, MSGBOX_NPC
	end

LcSafariForest_EventScript_GateSign::
	msgbox LcSafariForest_Text_GateSign, MSGBOX_SIGN
	end

LcSafariForest_EventScript_ThicketSign::
	msgbox LcSafariForest_Text_ThicketSign, MSGBOX_SIGN
	end

LcSafariForest_Text_StillHaveTimeExit::
	.string "You still have time left. Would you like\n"
	.string "to leave the FOREST AREA now?$"

LcSafariForest_Text_EnjoyTheRestOfYourAdventure::
	.string "Then get back in there!\n"
	.string "The trees hide more than they show.$"

LcSafariForest_Text_GoodLuck::
	.string "Welcome to the FOREST AREA!\p"
	.string "Every path between those trees leads\n"
	.string "somewhere. Good luck!$"

LcSafariForest_Text_ExitEarlyThankYouForPlaying::
	.string "Okay.\p"
	.string "I'll take back your remaining SAFARI\n"
	.string "BALLS.\p"
	.string "Thank you for playing.\n"
	.string "We hope to see you again.$"

LcSafariForest_Text_BugCatcher::
	.string "I've been counting the trees all day.\p"
	.string "I lost count at two hundred, but I did\n"
	.string "find three bug POKéMON on the way.$"

LcSafariForest_Text_Girl::
	.string "Listen. Hear that?\p"
	.string "Bird POKéMON, up in the branches.\n"
	.string "They come down when it's quiet.$"

LcSafariForest_Text_GateSign::
	.string "SAFARI ZONE\n"
	.string "FOREST AREA\p"
	.string "“Grass, bug and flying POKéMON.\n"
	.string "Please do not feed the trees.”$"

LcSafariForest_Text_ThicketSign::
	.string "“Dead end. The thicket is too dense\n"
	.string "to squeeze through here.”$"
