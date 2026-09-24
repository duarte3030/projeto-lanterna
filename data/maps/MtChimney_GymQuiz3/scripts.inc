@ MtChimney_GymQuiz3: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 33.4) por dev_scripts/copia_planta_ex.py.

MtChimney_GymQuiz3_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MtChimney_GymQuiz3_OnTransition
	.byte 0

@ Lote G3 (onda 2): reescrito no nosso formato a partir do bytecode e do texto do EX.
MtChimney_GymQuiz3_OnTransition:
	call_if_set FLAG_HOENNEX_MT_CHIMNEY_GYM_QUIZ_3, MtChimney_GymQuiz3_EventScript_SaiDoCaminho
	end

MtChimney_GymQuiz3_EventScript_SaiDoCaminho::
	setobjectxyperm 1, 1, 4
	return

MtChimney_GymQuiz3_EventScript_Quiz::
	faceplayer
	lock
	goto_if_set FLAG_HOENNEX_MT_CHIMNEY_GYM_QUIZ_3, MtChimney_GymQuiz3_EventScript_JaRespondeu
	msgbox MtChimney_GymQuiz3_Text_Pergunta, MSGBOX_DEFAULT
	dynmultichoice 0, 0, TRUE, 6, 0, DYN_MULTICHOICE_CB_NONE, MtChimney_GymQuiz3_Text_Opcao0, MtChimney_GymQuiz3_Text_Opcao1, MtChimney_GymQuiz3_Text_Opcao2
	closemessage
	goto_if_eq VAR_RESULT, 0, MtChimney_GymQuiz3_EventScript_Certo
	playse MUS_TOO_BAD
	waitse
	trainerbattle_single TRAINER_HOENNEX_MT_CHIMNEY_GYM_WILLIAM, MtChimney_GymQuiz3_Text_Errou, MtChimney_GymQuiz3_Text_DerrotaErrou, MtChimney_GymQuiz3_EventScript_DepoisDaLuta, NO_MUSIC
	releaseall
	end

MtChimney_GymQuiz3_EventScript_DepoisDaLuta::
	applymovement 1, MtChimney_GymQuiz3_Movement_SaiDoCaminho
	waitmovement 0
	setflag FLAG_HOENNEX_MT_CHIMNEY_GYM_QUIZ_3
	releaseall
	end

MtChimney_GymQuiz3_EventScript_Certo::
	playse SE_DING_DONG
	waitse
	msgbox MtChimney_GymQuiz3_Text_Certo, MSGBOX_AUTOCLOSE
	setflag FLAG_HOENNEX_MT_CHIMNEY_GYM_QUIZ_3
	applymovement 1, MtChimney_GymQuiz3_Movement_SaiDoCaminho
	waitmovement 0
	releaseall
	end

MtChimney_GymQuiz3_EventScript_JaRespondeu::
	trainerbattle_single TRAINER_HOENNEX_MT_CHIMNEY_GYM_WILLIAM, MtChimney_GymQuiz3_Text_DeNovo, MtChimney_GymQuiz3_Text_DerrotaDeNovo
	msgbox MtChimney_GymQuiz3_Text_Pos, MSGBOX_NPC
	releaseall
	end

MtChimney_GymQuiz3_Movement_SaiDoCaminho:
	face_left
	walk_slow_left
	step_end

MtChimney_GymQuiz3_Text_Pergunta:
	.string "Question.\p"
	.string "Who is the strongest GYM LEADER?$"

MtChimney_GymQuiz3_Text_Opcao0:
	.string "BLAINE$"

MtChimney_GymQuiz3_Text_Opcao1:
	.string "JUAN$"

MtChimney_GymQuiz3_Text_Opcao2:
	.string "ME$"

MtChimney_GymQuiz3_Text_Errou:
	.string "You dare!$"

MtChimney_GymQuiz3_Text_DerrotaErrou:
	.string "Tch...$"

MtChimney_GymQuiz3_Text_Certo:
	.string "Correct!$"

MtChimney_GymQuiz3_Text_DeNovo:
	.string "I’m up to battle if you are!$"

MtChimney_GymQuiz3_Text_DerrotaDeNovo:
	.string "Tch...$"

MtChimney_GymQuiz3_Text_Pos:
	.string "Go on.$"

