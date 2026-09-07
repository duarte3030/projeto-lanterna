@ TREM MAGNETICO, lado de Saffron. Portado da fonte `hns`
@ (data/maps/SaffronCity_TrainStation/scripts.inc). As MESMAS quatro trocas do
@ lado de Goldenrod estao explicadas por extenso em
@ data/maps/GoldenrodCity_TrainStation/scripts.inc, e valem aqui igual: o gate e
@ so o `ITEM_MAGNET_TRAIN_PASS`, o trem e o `OBJ_EVENT_GFX_TRAIN_FRONT` porque o
@ `TRAIN_BACK` da fonte nao foi portado, `VAR_TRAIN` virou `VAR_TREM_MAGNETICO`,
@ e o passo unico de subida mora aqui embaixo.
@
@ O MAPA E NOVO neste repo, e por isso entrou no FIM do grupo
@ `gMapGroup_IndoorSaffron_Frlg` (indice 10 de 11) e o layout entrou no FIM de
@ `data/layouts/layouts.json`: mapa no meio do grupo moveria `mapNum` e layout no
@ meio da lista moveria `mapLayoutId`, e a save guarda os dois.
@
@ A VOLTA CHEGA POR COORDENADA, e nao por warp: a estacao de Goldenrod tem UM
@ warp so (o que devolve para a cidade), entao `warp MAP, x, y` e o unico jeito
@ de cair na plataforma. E o que a fonte tambem faz.

.set LOCALID_SAFFRON_TRAIN_STATION_ATENDENTE, 1
.set LOCALID_SAFFRON_TRAIN_STATION_TREM, 5

SaffronCity_TrainStation_Frlg_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, SaffronCity_TrainStation_Frlg_OnFrame
	.byte 0

SaffronCity_TrainStation_Frlg_OnFrame::
	map_script_2 VAR_TREM_MAGNETICO, 1, SaffronCity_TrainStation_Frlg_EventScript_DesceDoTrem
	.2byte 0

SaffronCity_TrainStation_Frlg_EventScript_Atendente::
	lock
	faceplayer
	checkitem ITEM_MAGNET_TRAIN_PASS
	goto_if_eq VAR_RESULT, TRUE, SaffronCity_TrainStation_Frlg_EventScript_Embarca
	msgbox SaffronCity_TrainStation_Frlg_Text_SemPasse, MSGBOX_DEFAULT
	closemessage
	release
	end

SaffronCity_TrainStation_Frlg_EventScript_Embarca::
	msgbox SaffronCity_TrainStation_Frlg_Text_PorAqui, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SAFFRON_TRAIN_STATION_ATENDENTE, SaffronCity_TrainStation_Frlg_Movement_AtendenteSobe
	waitmovement 0
	applymovement OBJ_EVENT_ID_PLAYER, SaffronCity_TrainStation_Frlg_Movement_AteOTrem
	waitmovement 0
	special SpawnCameraObject
	applymovement OBJ_EVENT_ID_PLAYER, SaffronCity_TrainStation_Frlg_Movement_UmPassoAcima
	waitmovement 0
	playse SE_EXIT
	waitse
	fadescreen FADE_TO_BLACK
	applymovement OBJ_EVENT_ID_CAMERA, SaffronCity_TrainStation_Frlg_Movement_CameraSobe
	waitmovement 0
	applymovement OBJ_EVENT_ID_CAMERA, SaffronCity_TrainStation_Frlg_Movement_CameraDireita
	waitmovement 0
	delay 60
	applymovement LOCALID_SAFFRON_TRAIN_STATION_TREM, SaffronCity_TrainStation_Frlg_Movement_DeslizaEsquerda
	applymovement OBJ_EVENT_ID_CAMERA, SaffronCity_TrainStation_Frlg_Movement_DeslizaEsquerda
	fadescreen FADE_FROM_BLACK
	playse SE_TRUCK_MOVE
	delay 220
	playse SE_TRUCK_STOP
	applymovement LOCALID_SAFFRON_TRAIN_STATION_TREM, SaffronCity_TrainStation_Frlg_Movement_DeslizaEsquerda
	applymovement OBJ_EVENT_ID_CAMERA, SaffronCity_TrainStation_Frlg_Movement_DeslizaEsquerda
	fadescreen FADE_TO_BLACK
	waitse
	special RemoveCameraObject
	setvar VAR_TREM_MAGNETICO, 1
	delay 60
	warp MAP_GOLDENROD_CITY_TRAIN_STATION, 19, 16
	delay 60
	end

SaffronCity_TrainStation_Frlg_EventScript_DesceDoTrem::
	lock
	applymovement LOCALID_SAFFRON_TRAIN_STATION_ATENDENTE, SaffronCity_TrainStation_Frlg_Movement_AtendenteSobe
	applymovement OBJ_EVENT_ID_PLAYER, SaffronCity_TrainStation_Frlg_Movement_DesceDoTrem
	waitmovement 0
	waitmovement 0
	setvar VAR_TREM_MAGNETICO, 0
	applymovement LOCALID_SAFFRON_TRAIN_STATION_ATENDENTE, SaffronCity_TrainStation_Frlg_Movement_AtendenteDesce
	waitmovement 0
	release
	end

SaffronCity_TrainStation_Frlg_EventScript_Nerd::
	msgbox SaffronCity_TrainStation_Frlg_Text_Nerd, MSGBOX_NPC
	end

SaffronCity_TrainStation_Frlg_EventScript_Lass::
	msgbox SaffronCity_TrainStation_Frlg_Text_Lass, MSGBOX_NPC
	end

SaffronCity_TrainStation_Frlg_EventScript_Professora::
	msgbox SaffronCity_TrainStation_Frlg_Text_Professora, MSGBOX_NPC
	end

SaffronCity_TrainStation_Frlg_Movement_UmPassoAcima:
	walk_up
	step_end

SaffronCity_TrainStation_Frlg_Movement_DesceDoTrem:
	walk_down
	walk_left
	walk_left
	walk_left
	walk_down
	walk_down
	walk_down
	step_end

SaffronCity_TrainStation_Frlg_Movement_AtendenteSobe:
	face_up
	walk_up
	walk_left
	face_right
	step_end

SaffronCity_TrainStation_Frlg_Movement_AtendenteDesce:
	walk_right
	walk_down
	step_end

SaffronCity_TrainStation_Frlg_Movement_AteOTrem:
	walk_up
	walk_up
	walk_up
	walk_right
	walk_right
	walk_right
	walk_up
	walk_up
	step_end

SaffronCity_TrainStation_Frlg_Movement_CameraSobe:
	slide_up
	slide_up
	slide_up
	slide_up
	slide_up
	slide_up
	slide_up
	slide_up
	slide_up
	slide_up
	slide_up
	step_end

SaffronCity_TrainStation_Frlg_Movement_CameraDireita:
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	step_end

SaffronCity_TrainStation_Frlg_Movement_DeslizaEsquerda:
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	slide_left
	step_end

SaffronCity_TrainStation_Frlg_Text_SemPasse:
	.string "Hi. Do you have a rail PASS?\p"
	.string "Only people with a PASS can ride\n"
	.string "the MAGNET TRAIN.$"

SaffronCity_TrainStation_Frlg_Text_PorAqui:
	.string "May I see your rail PASS, please?\p"
	.string "OK. Right this way, please.$"

SaffronCity_TrainStation_Frlg_Text_Nerd:
	.string "The MAGNET TRAIN is a super-modern\n"
	.string "rail liner that uses electricity\p"
	.string "and magnets to float above the\n"
	.string "tracks. That's why it's so fast.$"

SaffronCity_TrainStation_Frlg_Text_Lass:
	.string "Hi. Do you have a rail PASS?\n"
	.string "I have one.\p"
	.string "All the people in SAFFRON who ride\n"
	.string "the MAGNET TRAIN have PASSES.$"

SaffronCity_TrainStation_Frlg_Text_Professora:
	.string "Before the MAGNET TRAIN STATION\n"
	.string "was built, there was a house there.\p"
	.string "A little girl named COPYCAT used\n"
	.string "to live there.$"
