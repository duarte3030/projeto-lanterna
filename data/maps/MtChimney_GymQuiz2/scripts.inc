@ MtChimney_GymQuiz2: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 33.3) por dev_scripts/copia_planta_ex.py.

MtChimney_GymQuiz2_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MtChimney_GymQuiz2_OnTransition
	.byte 0

@ Lote G3 (onda 2): reescrito no nosso formato a partir do bytecode e do texto do EX.
MtChimney_GymQuiz2_OnTransition:
	call_if_set FLAG_HOENNEX_MT_CHIMNEY_GYM_QUIZ_2, MtChimney_GymQuiz2_EventScript_SaiDoCaminho
	end

MtChimney_GymQuiz2_EventScript_SaiDoCaminho::
	setobjectxyperm 1, 1, 4
	return

MtChimney_GymQuiz2_EventScript_Quiz::
	faceplayer
	lock
	goto_if_set FLAG_HOENNEX_MT_CHIMNEY_GYM_QUIZ_2, MtChimney_GymQuiz2_EventScript_JaRespondeu
	msgbox MtChimney_GymQuiz2_Text_Pergunta, MSGBOX_DEFAULT
	dynmultichoice 0, 0, TRUE, 6, 0, DYN_MULTICHOICE_CB_NONE, MtChimney_GymQuiz2_Text_Opcao0, MtChimney_GymQuiz2_Text_Opcao1, MtChimney_GymQuiz2_Text_Opcao2
	closemessage
	goto_if_eq VAR_RESULT, 1, MtChimney_GymQuiz2_EventScript_Certo
	playse MUS_TOO_BAD
	waitse
	trainerbattle_single TRAINER_HOENNEX_MT_CHIMNEY_GYM_NICOLAS, MtChimney_GymQuiz2_Text_Errou, MtChimney_GymQuiz2_Text_DerrotaErrou, MtChimney_GymQuiz2_EventScript_DepoisDaLuta, NO_MUSIC
	releaseall
	end

MtChimney_GymQuiz2_EventScript_DepoisDaLuta::
	applymovement 1, MtChimney_GymQuiz2_Movement_SaiDoCaminho
	waitmovement 0
	setflag FLAG_HOENNEX_MT_CHIMNEY_GYM_QUIZ_2
	releaseall
	end

MtChimney_GymQuiz2_EventScript_Certo::
	playse SE_DING_DONG
	waitse
	msgbox MtChimney_GymQuiz2_Text_Certo, MSGBOX_AUTOCLOSE
	setflag FLAG_HOENNEX_MT_CHIMNEY_GYM_QUIZ_2
	applymovement 1, MtChimney_GymQuiz2_Movement_SaiDoCaminho
	waitmovement 0
	releaseall
	end

MtChimney_GymQuiz2_EventScript_JaRespondeu::
	trainerbattle_single TRAINER_HOENNEX_MT_CHIMNEY_GYM_NICOLAS, MtChimney_GymQuiz2_Text_DeNovo, MtChimney_GymQuiz2_Text_DerrotaDeNovo
	msgbox MtChimney_GymQuiz2_Text_Pos, MSGBOX_NPC
	releaseall
	end

MtChimney_GymQuiz2_Movement_SaiDoCaminho:
	face_left
	walk_slow_left
	step_end

MtChimney_GymQuiz2_Text_Pergunta:
	.string "Question.\p"
	.string "Where is BLAINE from?$"

MtChimney_GymQuiz2_Text_Opcao0:
	.string "JOHTO$"

MtChimney_GymQuiz2_Text_Opcao1:
	.string "KANTO$"

MtChimney_GymQuiz2_Text_Opcao2:
	.string "HOENN$"

MtChimney_GymQuiz2_Text_Errou:
	.string "Incorrect!$"

MtChimney_GymQuiz2_Text_DerrotaErrou:
	.string "Fiery!$"

MtChimney_GymQuiz2_Text_Certo:
	.string "Correct!$"

MtChimney_GymQuiz2_Text_DeNovo:
	.string "Hungry for a battle!?$"

MtChimney_GymQuiz2_Text_DerrotaDeNovo:
	.string "Fiery!$"

MtChimney_GymQuiz2_Text_Pos:
	.string "Do you like the quiz?\p"
	.string "BLAINE loves em.$"

