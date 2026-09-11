@ LcSafariWater: mapa copiado de Pokémon Liquid Crystal.gba (g5m116) por
@ dev_scripts/copia_mapa_rom.py. A ARTE é do hack; o JOGO (warps, NPCs,
@ encontros, itens, placas) é NOSSO e está aqui.
@
@ Mesma dança de atendente das outras duas áreas, com as coordenadas desta: a
@ porta é (43,44) e o atendente espera em (42,44) enquanto o jogador pousa. O
@ motivo de cada linha está no comentário de
@ data/maps/LcSafariMountain/scripts.inc.
@
@ ESTA ÁREA É ÁGUA, e isso é desenho, não defeito: a língua de terra da entrada
@ tem 19 tiles e todo o resto do mapa é mar. Medido por
@ dev_scripts/prova_alcance_safari_johto.py: a pé se chega a 16 tiles (os 19
@ menos o que os objetos ocupam), e de Surf a 1.154. Por isso a Big Pearl fica
@ na ilhota do meio do lago, que só se alcança nadando, e a Pearl fica na praia
@ da entrada, que se alcança a pé.

LcSafariWater_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LcSafariWater_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, LcSafariWater_OnFrame
	.byte 0

LcSafariWater_OnFrame:
	map_script_2 VAR_SAFARI_ZONE_STATE, 2, LcSafariWater_EventScript_EnterSafariZone
	.2byte 0

LcSafariWater_EventScript_EnterSafariZone::
	lockall
	applymovement LOCALID_PLAYER, LcSafariWater_Movement_PlayerEnter
	waitmovement 0
	applymovement LOCALID_LC_SAFARI_WATER_EXIT_ATTENDANT, LcSafariWater_Movement_ExitAttendantBlockDoor
	waitmovement 0
	setobjectxyperm LOCALID_LC_SAFARI_WATER_EXIT_ATTENDANT, 43, 44
	setvar VAR_SAFARI_ZONE_STATE, 0
	releaseall
	end

LcSafariWater_OnTransition:
	call_if_eq VAR_SAFARI_ZONE_STATE, 2, LcSafariWater_EventScript_SetExitAttendantAside
	end

LcSafariWater_EventScript_SetExitAttendantAside::
	setobjectxyperm LOCALID_LC_SAFARI_WATER_EXIT_ATTENDANT, 42, 44
	return

LcSafariWater_Movement_PlayerEnter:
	walk_up
	step_end

LcSafariWater_Movement_ExitAttendantBlockDoor:
	walk_right
	walk_in_place_faster_up
	step_end

LcSafariWater_EventScript_ExitAttendant::
	lock
	faceplayer
	goto_if_unset FLAG_GOOD_LUCK_SAFARI_ZONE, LcSafariWater_EventScript_GoodLuck
	msgbox LcSafariWater_Text_StillHaveTimeExit, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, LcSafariWater_EventScript_ExitEarly
	msgbox LcSafariWater_Text_EnjoyTheRestOfYourAdventure, MSGBOX_DEFAULT
	release
	end

LcSafariWater_EventScript_GoodLuck::
	setflag FLAG_GOOD_LUCK_SAFARI_ZONE
	msgbox LcSafariWater_Text_GoodLuck, MSGBOX_DEFAULT
	release
	end

LcSafariWater_EventScript_ExitEarly::
	msgbox LcSafariWater_Text_ExitEarlyThankYouForPlaying, MSGBOX_DEFAULT
	closemessage
	goto SafariZone_EventScript_Exit
	end

LcSafariWater_EventScript_Fisherman::
	msgbox LcSafariWater_Text_Fisherman, MSGBOX_NPC
	end

LcSafariWater_EventScript_GateSign::
	msgbox LcSafariWater_Text_GateSign, MSGBOX_SIGN
	end

LcSafariWater_Text_StillHaveTimeExit::
	.string "You still have time left. Would you like\n"
	.string "to leave the WATER AREA now?$"

LcSafariWater_Text_EnjoyTheRestOfYourAdventure::
	.string "Good. The far islet is the best spot,\n"
	.string "if you can get across to it.$"

LcSafariWater_Text_GoodLuck::
	.string "Welcome to the WATER AREA!\p"
	.string "The beach ends three steps from here.\n"
	.string "After that, you'll need to SURF.\p"
	.string "Good luck!$"

LcSafariWater_Text_ExitEarlyThankYouForPlaying::
	.string "Okay.\p"
	.string "I'll take back your remaining SAFARI\n"
	.string "BALLS.\p"
	.string "Thank you for playing.\n"
	.string "We hope to see you again.$"

LcSafariWater_Text_Fisherman::
	.string "I've been casting here since sunrise.\p"
	.string "The deep water hides the good ones.\n"
	.string "A rod gets you what a BALL can't.$"

LcSafariWater_Text_GateSign::
	.string "SAFARI ZONE\n"
	.string "WATER AREA\p"
	.string "“Water and poison POKéMON.\n"
	.string "SURF at your own pace.”$"
