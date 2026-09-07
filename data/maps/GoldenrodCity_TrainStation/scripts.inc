@ TREM MAGNETICO, Goldenrod <-> Saffron. Portado da fonte `hns`
@ (data/maps/GoldenrodCity_TrainStation/scripts.inc), com quatro trocas, e nenhuma
@ delas escondida:
@
@ 1. A CONDICAO E SO O PASSE. Na fonte os dois atendentes cruzam
@    `checkitem ITEM_PASS` com a flag `FLAG_RETURNED_MACHINE_PART`, que la e
@    "o jogador consertou a Usina e o trem voltou a andar". Esse arco de Kanto
@    nao foi portado para ca, e a flag nao existe: gate que aponta para flag
@    inexistente nao trava nada, so mente. Aqui o unico gate e o
@    `ITEM_MAGNET_TRAIN_PASS`, que a Copycat de Saffron entrega.
@ 2. O TREM E O `OBJ_EVENT_GFX_TRAIN_FRONT` DOS DOIS LADOS. A fonte usa
@    `TRAIN_BACK` (o vagao de tras) do lado de Saffron, e esse sprite NAO foi
@    portado nesta leva. O nosso `train_front.png` ja e o `train_mid.png` da
@    fonte, ou seja um vagao do meio, que serve nas duas pontas sem apontar
@    para o lado errado.
@ 3. `VAR_TRAIN` (0x406E la) virou `VAR_TREM_MAGNETICO`, apelido de
@    `VAR_UNUSED_0x4083`. Apelidar VAR_UNUSED nao mexe em VARS_COUNT.
@ 4. `Common_Movement_WalkUp1` nao existe neste repo; o passo unico esta
@    definido aqui embaixo, no proprio arquivo.
@
@ COMO A VIAGEM FUNCIONA, e por que ela nao precisa de mapa de vagao: o layout
@ tem 154 de largura e carrega AS DUAS PONTAS DO TRILHO. A cena sobe a camera
@ ate a plataforma (linha 5), desliza 134 tiles ate a outra ponta e so entao
@ da o `warp`. Nenhum vagao e mapa; o que existe e camera.

.set LOCALID_GOLDENROD_TRAIN_STATION_ATENDENTE, 1
.set LOCALID_GOLDENROD_TRAIN_STATION_TREM, 7

GoldenrodCity_TrainStation_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, GoldenrodCity_TrainStation_OnFrame
	.byte 0

@ Roda no quadro em que o mapa aparece, e SO quando a var vale 1, ou seja
@ quando o jogador acabou de chegar de trem. Porta continua sendo porta: nao
@ ha coord_event nenhum aqui.
GoldenrodCity_TrainStation_OnFrame::
	map_script_2 VAR_TREM_MAGNETICO, 1, GoldenrodCity_TrainStation_EventScript_DesceDoTrem
	.2byte 0

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

GoldenrodCity_TrainStation_EventScript_Atendente::
	lock
	faceplayer
	checkitem ITEM_MAGNET_TRAIN_PASS
	goto_if_eq VAR_RESULT, TRUE, GoldenrodCity_TrainStation_EventScript_Embarca
	msgbox GoldenrodCity_TrainStation_Text_SemPasse, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodCity_TrainStation_EventScript_Embarca::
	msgbox GoldenrodCity_TrainStation_Text_PorAqui, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_GOLDENROD_TRAIN_STATION_ATENDENTE, GoldenrodCity_TrainStation_Movement_AtendenteSobe
	waitmovement 0
	applymovement OBJ_EVENT_ID_PLAYER, GoldenrodCity_TrainStation_Movement_AteOTrem
	waitmovement 0
	special SpawnCameraObject
	applymovement OBJ_EVENT_ID_PLAYER, GoldenrodCity_TrainStation_Movement_UmPassoAcima
	waitmovement 0
	playse SE_EXIT
	waitse
	fadescreen FADE_TO_BLACK
	applymovement OBJ_EVENT_ID_CAMERA, GoldenrodCity_TrainStation_Movement_CameraSobe
	waitmovement 0
	applymovement OBJ_EVENT_ID_CAMERA, GoldenrodCity_TrainStation_Movement_CameraEsquerda
	waitmovement 0
	delay 60
	applymovement LOCALID_GOLDENROD_TRAIN_STATION_TREM, GoldenrodCity_TrainStation_Movement_DeslizaDireita
	applymovement OBJ_EVENT_ID_CAMERA, GoldenrodCity_TrainStation_Movement_DeslizaDireita
	fadescreen FADE_FROM_BLACK
	playse SE_TRUCK_MOVE
	delay 220
	playse SE_TRUCK_STOP
	applymovement LOCALID_GOLDENROD_TRAIN_STATION_TREM, GoldenrodCity_TrainStation_Movement_DeslizaDireita
	applymovement OBJ_EVENT_ID_CAMERA, GoldenrodCity_TrainStation_Movement_DeslizaDireita
	fadescreen FADE_TO_BLACK
	waitse
	special RemoveCameraObject
	setvar VAR_TREM_MAGNETICO, 1
	delay 60
	warp MAP_SAFFRON_CITY_TRAIN_STATION, 1
	delay 60
	end

GoldenrodCity_TrainStation_EventScript_DesceDoTrem::
	lock
	applymovement LOCALID_GOLDENROD_TRAIN_STATION_ATENDENTE, GoldenrodCity_TrainStation_Movement_AtendenteSobe
	applymovement OBJ_EVENT_ID_PLAYER, GoldenrodCity_TrainStation_Movement_DesceDoTrem
	waitmovement 0
	waitmovement 0
	setvar VAR_TREM_MAGNETICO, 0
	applymovement LOCALID_GOLDENROD_TRAIN_STATION_ATENDENTE, GoldenrodCity_TrainStation_Movement_AtendenteDesce
	waitmovement 0
	release
	end

GoldenrodCity_TrainStation_Movement_UmPassoAcima:
	walk_up
	step_end

GoldenrodCity_TrainStation_Movement_DesceDoTrem:
	walk_down
	walk_left
	walk_left
	walk_left
	walk_down
	walk_down
	walk_down
	step_end

GoldenrodCity_TrainStation_Movement_AtendenteSobe:
	face_up
	walk_up
	walk_left
	face_right
	step_end

GoldenrodCity_TrainStation_Movement_AtendenteDesce:
	walk_right
	walk_down
	step_end

GoldenrodCity_TrainStation_Movement_AteOTrem:
	walk_up
	walk_up
	walk_up
	walk_right
	walk_right
	walk_right
	walk_up
	walk_up
	step_end

GoldenrodCity_TrainStation_Movement_CameraSobe:
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

GoldenrodCity_TrainStation_Movement_CameraEsquerda:
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

GoldenrodCity_TrainStation_Movement_DeslizaDireita:
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	slide_right
	step_end

GoldenrodCity_TrainStation_Text_SemPasse:
	.string "The MAGNET TRAIN needs a rail PASS.\p"
	.string "Sorry. You don't have one.$"

GoldenrodCity_TrainStation_Text_PorAqui:
	.string "May I see your rail PASS, please?\p"
	.string "OK. Right this way, please.$"

GoldenrodCity_TrainStation_EventScript_Gent::
	lock
	faceplayer
	msgbox GoldenrodMagnetTrainStation_Text_GentlemanPresident, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodMagnetTrainStation_Text_GentlemanPresident::
    .string "I'm the PRESIDENT.\p"
    .string "My dream was to build a train that\n"
    .string "is faster than any POKéMON.\p"
    .string "It really brings JOHTO much closer\n"
    .string "to KANTO.$"

GoldenrodCity_TrainStation_EventScript_Boy::
	lock
	msgbox GoldenrodCity_TrainStation_Text_Boy, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodCity_TrainStation_Text_Boy::
	.string "You brought the MAGNET TRAIN PASS,\n"
	.string "right?$"

GoldenrodCity_TrainStation_EventScript_Psychic::
	lock
	msgbox GoldenrodCity_TrainStation_Text_Psychic, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodCity_TrainStation_Text_Psychic::
	.string "I thought you had it!$"
