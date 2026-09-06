@ Elevador da loja de departamento de Goldenrod.
@
@ Trazido do `hns` por dev_scripts/elevador_goldenrod.py em 06/09/2026. Até
@ aqui a árvore tinha o MAPA do elevador, a porta desenhada em (9,4) nos seis
@ andares e em (10,6) no subsolo, e o warp de cada andar apontando para ele,
@ mas NÃO tinha o roteiro: a porta nunca abria e o elevador era um cômodo que
@ ninguém visitava. A lente `dev_scripts/qa/lente_portas.py` acha o caso pela
@ regra P3, warp em célula que não dispara com porta viva colada.
@
@ Como o mecanismo funciona, e ele não usa o mapa do elevador:
@   1. o `coord_event` de (9,5) do andar (ou (10,7) no subsolo) chama
@      GoldenrodDeptElevator_EventScript_Elevator quando o jogador pisa na
@      frente da porta;
@   2. a porta abre por `opendoor`, o jogador ENTRA andando (applymovement, que
@      não consulta colisão) e a porta fecha;
@   3. o menu escolhe o andar é o `warp` leva para (9,3) do destino, que é a
@      célula DENTRO do vão do elevador, do outro lado da porta;
@   4. VAR_ELEVADOR_GOLDENROD fica em 1, e o ON_FRAME do andar de destino roda
@      GoldenrodDeptElevator_EventScript_Exit, que abre a porta, desce o
@      jogador três tiles e zera a var.
@ O warp do `map.json` para MAP_GOLDENROD_CITY_DEPARTMENT_STORE_ELEVATOR
@ continua onde a fonte o deixou e continua sem disparar, DE PROPÓSITO: o
@ elevador é cena, não mapa. Ele não foi movido para não mexer em índice de
@ warp, que é promessa de save.

GoldenrodCity_DepartmentStoreElevator_MapScripts::
	.byte 0

GoldenrodDeptElevator_OnFrame::
	map_script_2 VAR_ELEVADOR_GOLDENROD, 1, GoldenrodDeptElevator_EventScript_Exit
	.2byte 0

GoldenrodDeptElevator_EventScript_Exit::
	opendoor 9, 4
	opendoor 10, 6
	waitdooranim
	waitdooranim
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkDown
	waitmovement 0
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkDown
	waitmovement 0
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkDown
	waitmovement 0
	closedoor 9, 4
	closedoor 10, 6
	waitdooranim
	waitdooranim
	setvar VAR_ELEVADOR_GOLDENROD, 0
	release
	end

GoldenrodDeptElevator_EventScript_Elevator::
	lock
	turnobject OBJ_EVENT_ID_PLAYER, DIR_NORTH
	delay 8
	opendoor 9, 4
	opendoor 10, 6
	waitdooranim
	waitdooranim
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkUp
	waitmovement 0
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkUp
	waitmovement 0
	closedoor 9, 4
	closedoor 10, 6
	waitdooranim
	waitdooranim
	multichoice 20, 0, MULTI_JOHTO_ELEVADOR_GOLDENROD, FALSE
	switch VAR_RESULT
	case 0, GoldenrodDeptElevator_EventScript_F6
	case 1, GoldenrodDeptElevator_EventScript_F5
	case 2, GoldenrodDeptElevator_EventScript_F4
	case 3, GoldenrodDeptElevator_EventScript_F3
	case 4, GoldenrodDeptElevator_EventScript_F2
	case 5, GoldenrodDeptElevator_EventScript_F1
	case 6, GoldenrodDeptElevator_EventScript_B1F
	case 7, GoldenrodDeptElevator_EventScript_Cancelar
	case MULTI_B_PRESSED, GoldenrodDeptElevator_EventScript_Cancelar
	closemessage
	end

GoldenrodDeptElevator_EventScript_B1F::
	fadescreen FADE_TO_BLACK
	playse SE_SUCCESS
	setvar VAR_ELEVADOR_GOLDENROD, 1
	waitse
	warp MAP_GOLDENROD_CITY_DEPARTMENT_STORE_BASEMENT, 10, 5
	delay 60
	end

GoldenrodDeptElevator_EventScript_F1::
	fadescreen FADE_TO_BLACK
	playse SE_SUCCESS
	setvar VAR_ELEVADOR_GOLDENROD, 1
	waitse
	warp MAP_GOLDENROD_CITY_DEPARTMENT_STORE_1F, 9, 3
	delay 60
	end

GoldenrodDeptElevator_EventScript_F2::
	fadescreen FADE_TO_BLACK
	playse SE_SUCCESS
	setvar VAR_ELEVADOR_GOLDENROD, 1
	waitse
	warp MAP_GOLDENROD_CITY_DEPARTMENT_STORE_2F, 9, 3
	delay 60
	end

GoldenrodDeptElevator_EventScript_F3::
	fadescreen FADE_TO_BLACK
	playse SE_SUCCESS
	setvar VAR_ELEVADOR_GOLDENROD, 1
	waitse
	warp MAP_GOLDENROD_CITY_DEPARTMENT_STORE_3F, 9, 3
	delay 60
	end

GoldenrodDeptElevator_EventScript_F4::
	fadescreen FADE_TO_BLACK
	playse SE_SUCCESS
	setvar VAR_ELEVADOR_GOLDENROD, 1
	waitse
	warp MAP_GOLDENROD_CITY_DEPARTMENT_STORE_4F, 9, 3
	delay 60
	end

GoldenrodDeptElevator_EventScript_F5::
	fadescreen FADE_TO_BLACK
	playse SE_SUCCESS
	setvar VAR_ELEVADOR_GOLDENROD, 1
	waitse
	warp MAP_GOLDENROD_CITY_DEPARTMENT_STORE_5F, 9, 3
	delay 60
	end

GoldenrodDeptElevator_EventScript_F6::
	fadescreen FADE_TO_BLACK
	playse SE_SUCCESS
	setvar VAR_ELEVADOR_GOLDENROD, 1
	waitse
	warp MAP_GOLDENROD_CITY_DEPARTMENT_STORE_6F, 9, 3
	delay 60
	end

GoldenrodDeptElevator_EventScript_Cancelar::
	closemessage
	opendoor 9, 4
	opendoor 10, 6
	waitdooranim
	waitdooranim
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkDown
	waitmovement 0
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkDown
	waitmovement 0
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkDown
	waitmovement 0
	closedoor 9, 4
	closedoor 10, 6
	waitdooranim
	waitdooranim
	release
	end
