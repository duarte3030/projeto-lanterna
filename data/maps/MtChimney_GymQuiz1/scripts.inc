@ MtChimney_GymQuiz1: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 33.2) por dev_scripts/copia_planta_ex.py.

MtChimney_GymQuiz1_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MtChimney_GymQuiz1_OnTransition
	.byte 0

@ Lote G3 (onda 2): reescrito no nosso formato a partir do bytecode e do texto do EX.
MtChimney_GymQuiz1_OnTransition:
	call_if_set FLAG_HOENNEX_MT_CHIMNEY_GYM_QUIZ_1, MtChimney_GymQuiz1_EventScript_SaiDoCaminho
	end

MtChimney_GymQuiz1_EventScript_SaiDoCaminho::
	setobjectxyperm 1, 1, 4
	return

MtChimney_GymQuiz1_EventScript_Quiz::
	faceplayer
	lock
	goto_if_set FLAG_HOENNEX_MT_CHIMNEY_GYM_QUIZ_1, MtChimney_GymQuiz1_EventScript_JaRespondeu
	msgbox MtChimney_GymQuiz1_Text_Pergunta, MSGBOX_DEFAULT
	dynmultichoice 0, 0, TRUE, 6, 0, DYN_MULTICHOICE_CB_NONE, MtChimney_GymQuiz1_Text_Opcao0, MtChimney_GymQuiz1_Text_Opcao1, MtChimney_GymQuiz1_Text_Opcao2
	closemessage
	goto_if_eq VAR_RESULT, 2, MtChimney_GymQuiz1_EventScript_Certo
	playse MUS_TOO_BAD
	waitse
	trainerbattle_single TRAINER_HOENNEX_MT_CHIMNEY_GYM_KYLE, MtChimney_GymQuiz1_Text_Errou, MtChimney_GymQuiz1_Text_DerrotaErrou, MtChimney_GymQuiz1_EventScript_DepoisDaLuta, NO_MUSIC
	releaseall
	end

MtChimney_GymQuiz1_EventScript_DepoisDaLuta::
	applymovement 1, MtChimney_GymQuiz1_Movement_SaiDoCaminho
	waitmovement 0
	setflag FLAG_HOENNEX_MT_CHIMNEY_GYM_QUIZ_1
	releaseall
	end

MtChimney_GymQuiz1_EventScript_Certo::
	playse SE_DING_DONG
	waitse
	msgbox MtChimney_GymQuiz1_Text_Certo, MSGBOX_AUTOCLOSE
	setflag FLAG_HOENNEX_MT_CHIMNEY_GYM_QUIZ_1
	applymovement 1, MtChimney_GymQuiz1_Movement_SaiDoCaminho
	waitmovement 0
	releaseall
	end

MtChimney_GymQuiz1_EventScript_JaRespondeu::
	trainerbattle_single TRAINER_HOENNEX_MT_CHIMNEY_GYM_KYLE, MtChimney_GymQuiz1_Text_DeNovo, MtChimney_GymQuiz1_Text_DerrotaDeNovo
	msgbox MtChimney_GymQuiz1_Text_Pos, MSGBOX_NPC
	releaseall
	end

MtChimney_GymQuiz1_Movement_SaiDoCaminho:
	face_left
	walk_slow_left
	step_end

MtChimney_GymQuiz1_Text_Pergunta:
	.string "Question.\p"
	.string "What type is FIRE SUPER EFFECTIVE\n"
	.string "against?$"

MtChimney_GymQuiz1_Text_Opcao0:
	.string "ROCK$"

MtChimney_GymQuiz1_Text_Opcao1:
	.string "FIRE$"

MtChimney_GymQuiz1_Text_Opcao2:
	.string "STEEL$"

MtChimney_GymQuiz1_Text_Errou:
	.string "Ehhh.\n"
	.string "Wrong!$"

MtChimney_GymQuiz1_Text_DerrotaErrou:
	.string "Your heat makes up for your lack of\n"
	.string "knowledge.$"

MtChimney_GymQuiz1_Text_Certo:
	.string "Correct!$"

MtChimney_GymQuiz1_Text_DeNovo:
	.string "Oh you still wanna battle?$"

MtChimney_GymQuiz1_Text_DerrotaDeNovo:
	.string "Your heat is crazy man.$"

MtChimney_GymQuiz1_Text_Pos:
	.string "Good luck with Blaine.$"

