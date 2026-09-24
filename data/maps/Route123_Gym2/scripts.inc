@ Route123_Gym2: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 34.3) por dev_scripts/copia_planta_ex.py.

Route123_Gym2_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Route123_Gym2_OnLoad
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 34.3), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
Route123_Gym2_EventScript_ExTrainer0::
	trainerbattle_single TRAINER_HOENNEX_ROUTE123_GYM2_JARED, Route123_Gym2_Text_ExTrainer0Intro, Route123_Gym2_Text_ExTrainer0Defeat
	msgbox Route123_Gym2_Text_ExTrainer0PostBattle, MSGBOX_AUTOCLOSE
	end

Route123_Gym2_Text_ExTrainer0Intro:
	.string "I fished this monster up in FOOTHILL\n"
	.string "TOWN!$"

Route123_Gym2_Text_ExTrainer0Defeat:
	.string "GYARADOS!$"

Route123_Gym2_Text_ExTrainer0PostBattle:
	.string "You defeated my sea monster!$"

@ Lote G3 (onda 2): reescrito no nosso formato a partir do bytecode e do texto do EX.
Route123_Gym2_OnLoad:
	goto_if_unset FLAG_HOENNEX_ROUTE123_GYM_SWITCH_1, Route123_Gym2_OnLoad_Fim
	goto_if_set FLAG_HOENNEX_ROUTE123_GYM_SWITCH_2, Route123_Gym2_OnLoad_Dois
	@ só o interruptor da sala de cima (EX 0x834F02F)
	setmetatile 2, 17, 0x23D, FALSE
	setmetatile 3, 17, 0x201, FALSE
	setmetatile 4, 17, 0x200, FALSE
	setmetatile 5, 17, 0x23A, FALSE
	setmetatile 2, 18, 0x243, FALSE
	setmetatile 3, 18, 0x200, FALSE
	setmetatile 4, 18, 0x200, FALSE
	setmetatile 5, 18, 0x23B, FALSE
	setmetatile 3, 19, 0x200, FALSE
	setmetatile 4, 19, 0x200, FALSE
	setmetatile 5, 19, 0x23C, FALSE
	special DrawWholeMapView
	end

Route123_Gym2_OnLoad_Dois:
	@ os dois interruptores (EX 0x834EFB1)
	setmetatile 2, 17, 0x23D, TRUE
	setmetatile 3, 17, 0x201, FALSE
	setmetatile 4, 17, 0x200, FALSE
	setmetatile 5, 17, 0x23A, TRUE
	setmetatile 2, 18, 0x243, TRUE
	setmetatile 3, 18, 0x200, FALSE
	setmetatile 4, 18, 0x200, FALSE
	setmetatile 5, 18, 0x23B, TRUE
	setmetatile 3, 19, 0x200, FALSE
	setmetatile 4, 19, 0x200, FALSE
	setmetatile 5, 19, 0x23C, FALSE
	setmetatile 27, 13, 0x230, FALSE
	special DrawWholeMapView
	end

Route123_Gym2_OnLoad_Fim:
	end

Route123_Gym2_EventScript_Switch::
	goto_if_set FLAG_HOENNEX_ROUTE123_GYM_SWITCH_2, Route123_Gym2_EventScript_SwitchFim
	lockall
	setmetatile 27, 13, 0x230, FALSE
	setflag FLAG_HOENNEX_ROUTE123_GYM_SWITCH_2
	special DrawWholeMapView
	playse SE_SWITCH
	waitse
	releaseall
	end

Route123_Gym2_EventScript_SwitchFim::
	releaseall
	end

