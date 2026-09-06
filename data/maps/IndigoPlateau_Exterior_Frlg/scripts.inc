IndigoPlateau_Exterior_Frlg_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, IndigoPlateau_Exterior_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, IndigoPlateau_Exterior_OnFrame
	.byte 0

IndigoPlateau_Exterior_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_INDIGO_PLATEAU_EXTERIOR
	call_if_eq VAR_MAP_SCENE_INDIGO_PLATEAU_EXTERIOR, 1, IndigoPlateau_Exterior_EventScript_PlayCreditsMusic
	end

IndigoPlateau_Exterior_EventScript_PlayCreditsMusic::
	playbgm MUS_CREDITS, 0
	return

IndigoPlateau_Exterior_OnFrame::
	map_script_2 VAR_MAP_SCENE_INDIGO_PLATEAU_EXTERIOR, 1, IndigoPlateau_Exterior_EventScript_Credits
	.2byte 0


@ After beating the champion, you are warped to the main
@ entrance of Indigo Plateau. This script starts running
@ immediately after your walking animation.
@ The script is timed to the music.
IndigoPlateau_Exterior_EventScript_Credits::
	lockall
	delay 105

	@ Rival exits building. Spawn a dummy object to lock the camera.
	opendoor 11, 6
	waitdooranim
	special SpawnCameraObject
	addobject LOCALID_CREDITS_RIVAL
	applymovement LOCALID_CREDITS_RIVAL, IndigoPlateau_Exterior_Movement_RivalExitBuilding
	applymovement LOCALID_PLAYER, IndigoPlateau_Exterior_Movement_PushPlayerOutOfWay
	waitmovement 0
	closedoor 11, 6
	waitdooranim

	@ Rival runs off
	applymovement LOCALID_PLAYER, IndigoPlateau_Exterior_Movement_PlayerWatchRivalLeave
	applymovement LOCALID_CREDITS_RIVAL, IndigoPlateau_Exterior_Movement_RivalLeave
	waitmovement 0
	delay 100

	@ Oak exits building
	opendoor 11, 6
	waitdooranim
	addobject LOCALID_CREDITS_PROF_OAK
	applymovement LOCALID_CREDITS_PROF_OAK, IndigoPlateau_Exterior_Movement_OakExitBuilding
	waitmovement 0
	closedoor 11, 6
	waitdooranim
	delay 160

	@ Oak looks at player, then walks off
	applymovement LOCALID_PLAYER, IndigoPlateau_Exterior_Movement_PlayerWatchOakLeave
	applymovement LOCALID_CREDITS_PROF_OAK, IndigoPlateau_Exterior_Movement_OakLeave
	waitmovement 0
	delay 100

	@ Player begin to leave
	applymovement LOCALID_PLAYER, IndigoPlateau_Exterior_Movement_PlayerBeginLeave
	waitmovement 0
	delay 155
	applymovement LOCALID_PLAYER, IndigoPlateau_Exterior_Movement_PlayerFaceLeague
	waitmovement 0
	delay 90

	@ Player runs off
	applymovement LOCALID_PLAYER, IndigoPlateau_Exterior_Movement_PlayerTurnAround
	waitmovement 0
	applymovement LOCALID_PLAYER, IndigoPlateau_Exterior_Movement_PlayerLeave
	waitmovement 0

	@ Reset the map state and roll the credits
	special RemoveCameraObject
	setvar VAR_MAP_SCENE_INDIGO_PLATEAU_EXTERIOR, 0
	removeobject LOCALID_CREDITS_RIVAL
	removeobject LOCALID_CREDITS_PROF_OAK
	special CB2_StartCreditsSequence
	waitstate
	releaseall
	end

IndigoPlateau_Exterior_Movement_PlayerLeave::
	player_run_down
	player_run_down
	player_run_down
	player_run_down
	player_run_down
	player_run_down
	step_end

@ Unused
IndigoPlateau_Exterior_Movement_PlayerExitBuilding::
	walk_down
	walk_down
	step_end

IndigoPlateau_Exterior_Movement_PlayerWatchRivalLeave::
	delay_16
	delay_4
	walk_in_place_faster_down
	step_end

IndigoPlateau_Exterior_Movement_PlayerWatchOakLeave::
	delay_8
	walk_in_place_faster_right
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	walk_in_place_faster_down
	step_end

IndigoPlateau_Exterior_Movement_PlayerBeginLeave::
	walk_right
	delay_16
	walk_down
	walk_down
	delay_16
	delay_16
	step_end

IndigoPlateau_Exterior_Movement_PlayerTurnAround::
	walk_in_place_faster_down
	step_end

IndigoPlateau_Exterior_Movement_PushPlayerOutOfWay::
	face_right
	lock_facing_direction
	walk_left
	unlock_facing_direction
	step_end

IndigoPlateau_Exterior_Movement_PlayerFaceLeague::
	walk_in_place_faster_up
	step_end

IndigoPlateau_Exterior_Movement_RivalLeave::
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	step_end

IndigoPlateau_Exterior_Movement_RivalExitBuilding::
	walk_fast_down
	step_end

IndigoPlateau_Exterior_Movement_OakLeave::
	walk_in_place_faster_left
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	walk_in_place_faster_down
	delay_16
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

IndigoPlateau_Exterior_Movement_OakExitBuilding::
	walk_down
	step_end

@ >>> Povoamento: os 10 NPCs por cidade (dev_scripts/povoa_cidades.py) >>>
@ Lei do Gui de 07/09/2026: toda cidade do cartucho 1 tem pelo menos 10 NPCs.
@ Bloco GERADO. Para mudar fala ou posicao, edite dev_scripts/povoa_cidades.json
@ e rode `python3 dev_scripts/povoa_cidades.py --aplica`.

IndigoPlateau_Exterior_EventScript_Povoa1::
	lock
	faceplayer
	msgbox IndigoPlateau_Exterior_Text_Povoa1, MSGBOX_DEFAULT
	release
	end

IndigoPlateau_Exterior_Text_Povoa1:
	.string "Past this door the ELITE FOUR\nare waiting. No second tries.$"

IndigoPlateau_Exterior_EventScript_Povoa2::
	lock
	faceplayer
	msgbox IndigoPlateau_Exterior_Text_Povoa2, MSGBOX_DEFAULT
	release
	end

IndigoPlateau_Exterior_Text_Povoa2:
	.string "I climbed VICTORY ROAD twice.\nI turned back twice.$"

IndigoPlateau_Exterior_EventScript_Povoa3::
	lock
	faceplayer
	msgbox IndigoPlateau_Exterior_Text_Povoa3, MSGBOX_DEFAULT
	release
	end

IndigoPlateau_Exterior_Text_Povoa3:
	.string "Heal here. There is nowhere to\nrest once you go in.$"

IndigoPlateau_Exterior_EventScript_Povoa4::
	lock
	faceplayer
	msgbox IndigoPlateau_Exterior_Text_Povoa4, MSGBOX_DEFAULT
	release
	end

IndigoPlateau_Exterior_Text_Povoa4:
	.string "Four champions in a row, then\nthe CHAMPION. Think about that.$"

IndigoPlateau_Exterior_EventScript_Povoa5::
	lock
	faceplayer
	msgbox IndigoPlateau_Exterior_Text_Povoa5, MSGBOX_DEFAULT
	release
	end

IndigoPlateau_Exterior_Text_Povoa5:
	.string "The wind up here never stops.\nIt clears the head.$"

IndigoPlateau_Exterior_EventScript_Povoa6::
	lock
	faceplayer
	msgbox IndigoPlateau_Exterior_Text_Povoa6, MSGBOX_DEFAULT
	release
	end

IndigoPlateau_Exterior_Text_Povoa6:
	.string "I cover every challenger who\nwalks through that gate.$"

IndigoPlateau_Exterior_EventScript_Povoa7::
	lock
	faceplayer
	msgbox IndigoPlateau_Exterior_Text_Povoa7, MSGBOX_DEFAULT
	release
	end

IndigoPlateau_Exterior_Text_Povoa7:
	.string "Bring full restores. Bring more\nthan you think you need.$"

IndigoPlateau_Exterior_EventScript_Povoa8::
	lock
	faceplayer
	msgbox IndigoPlateau_Exterior_Text_Povoa8, MSGBOX_DEFAULT
	release
	end

IndigoPlateau_Exterior_Text_Povoa8:
	.string "My brother went in this morning.\nI am still standing here.$"

@ <<< Povoamento: fim do bloco gerado <<<
