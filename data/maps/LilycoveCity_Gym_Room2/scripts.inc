@ LilycoveCity_Gym_Room2: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 13.24) por dev_scripts/copia_planta_ex.py.

LilycoveCity_Gym_Room2_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LilycoveCity_Gym_Room2_OnTransition
	map_script MAP_SCRIPT_ON_LOAD, LilycoveCity_Gym_Room2_OnLoad
	.byte 0

@ Segunda sala do ginásio da Ekrutea (EX 13.24): a mesma mecânica do LilycoveCity_Gym (luz,
@ sorteio, setmetatile pelo de-para do gTileset_LilycoveGym, portas por warp dinâmico), gerada
@ da ROM comando a comando. Os gatilhos das portas usam os scripts do LilycoveCity_Gym, como
@ no EX (os mesmos endereços).
LilycoveCity_Gym_Room2_OnTransition::
	setflashlevel 3
	random 2
	copyvar VAR_TEMP_1, VAR_RESULT
	random 2
	copyvar VAR_TEMP_2, VAR_RESULT
	random 3
	copyvar VAR_TEMP_3, VAR_RESULT
	random 3
	copyvar VAR_TEMP_4, VAR_RESULT
	end

LilycoveCity_Gym_Room2_OnLoad::
	copyvar VAR_0x8000, VAR_TEMP_4
	goto_if_eq VAR_0x8000, 0, LilycoveCity_Gym_Room2_EventScript_Ex34D161
	goto_if_eq VAR_0x8000, 1, LilycoveCity_Gym_Room2_EventScript_Ex34D18A
	goto_if_eq VAR_0x8000, 2, LilycoveCity_Gym_Room2_EventScript_Ex34D1B3
	goto LilycoveCity_Gym_Room2_EventScript_Ex34D24E

LilycoveCity_Gym_Room2_EventScript_Ex34D161::
	goto_if_eq VAR_TEMP_3, 0, LilycoveCity_Gym_Room2_EventScript_Ex34D1DC
	goto_if_eq VAR_TEMP_3, 1, LilycoveCity_Gym_Room2_EventScript_Ex34D1EF
	setmetatile 13, 9, 0x23D, TRUE  @ EX 0x2C0
	goto LilycoveCity_Gym_Room2_EventScript_Ex34D2D4

LilycoveCity_Gym_Room2_EventScript_Ex34D1DC::
	setmetatile 13, 9, 0x23F, FALSE  @ EX 0x2C2
	goto LilycoveCity_Gym_Room2_EventScript_Ex34D2D4

LilycoveCity_Gym_Room2_EventScript_Ex34D2D4::
	setmetatile 22, 16, 0x278, TRUE  @ EX 0x311
	setmetatile 22, 15, 0x278, TRUE  @ EX 0x311
	setmetatile 22, 14, 0x279, TRUE  @ EX 0x312
	setmetatile 22, 13, 0x26E, TRUE  @ EX 0x304
	setmetatile 22, 12, 0x279, TRUE  @ EX 0x312
	setmetatile 22, 11, 0x26C, FALSE  @ EX 0x302
	setmetatile 21, 11, 0x26F, TRUE  @ EX 0x305
	setmetatile 21, 12, 0x273, TRUE  @ EX 0x30B
	setmetatile 21, 13, 0x26B, FALSE  @ EX 0x301
	setmetatile 21, 14, 0x271, TRUE  @ EX 0x309
	setmetatile 20, 13, 0x26B, FALSE  @ EX 0x301
	setmetatile 20, 14, 0x271, TRUE  @ EX 0x309
	setmetatile 21, 15, 0x23E, FALSE  @ EX 0x2C1
	setmetatile 19, 13, 0x26D, FALSE  @ EX 0x303
	setmetatile 19, 14, 0x273, TRUE  @ EX 0x30B
	setmetatile 18, 13, 0x23E, FALSE  @ EX 0x2C1
	setmetatile 18, 14, 0x23E, FALSE  @ EX 0x2C1
	setmetatile 17, 13, 0x270, TRUE  @ EX 0x306
	setmetatile 17, 14, 0x274, TRUE  @ EX 0x30C
	goto_if_eq VAR_TEMP_4, 0, LilycoveCity_Gym_Room2_EventScript_Ex34D38C
	end

LilycoveCity_Gym_Room2_EventScript_Ex34D38C::
	goto LilycoveCity_Gym_Room2_EventScript_Ex34D396

LilycoveCity_Gym_Room2_EventScript_Ex34D396::
	setmetatile 0, 16, 0x26D, FALSE  @ EX 0x303
	setmetatile 1, 16, 0x26B, FALSE  @ EX 0x301
	setmetatile 2, 16, 0x26C, FALSE  @ EX 0x302
	setmetatile 0, 17, 0x273, TRUE  @ EX 0x30B
	setmetatile 1, 17, 0x271, TRUE  @ EX 0x309
	setmetatile 2, 17, 0x279, TRUE  @ EX 0x312
	setmetatile 0, 18, 0x23E, FALSE  @ EX 0x2C1
	setmetatile 1, 18, 0x23E, FALSE  @ EX 0x2C1
	setmetatile 2, 18, 0x270, TRUE  @ EX 0x306
	setmetatile 0, 19, 0x23E, FALSE  @ EX 0x2C1
	setmetatile 1, 19, 0x23E, FALSE  @ EX 0x2C1
	setmetatile 2, 19, 0x274, TRUE  @ EX 0x30C
	end

LilycoveCity_Gym_Room2_EventScript_Ex34D1EF::
	setmetatile 13, 9, 0x241, TRUE  @ EX 0x2C9
	goto LilycoveCity_Gym_Room2_EventScript_Ex34D2D4

LilycoveCity_Gym_Room2_EventScript_Ex34D18A::
	goto_if_eq VAR_TEMP_3, 0, LilycoveCity_Gym_Room2_EventScript_Ex34D202
	goto_if_eq VAR_TEMP_3, 1, LilycoveCity_Gym_Room2_EventScript_Ex34D215
	setmetatile 21, 14, 0x23D, TRUE  @ EX 0x2C0
	goto LilycoveCity_Gym_Room2_EventScript_Ex34D24E

LilycoveCity_Gym_Room2_EventScript_Ex34D202::
	setmetatile 21, 14, 0x23F, FALSE  @ EX 0x2C2
	goto LilycoveCity_Gym_Room2_EventScript_Ex34D24E

LilycoveCity_Gym_Room2_EventScript_Ex34D24E::
	setmetatile 12, 7, 0x26B, FALSE  @ EX 0x301
	setmetatile 12, 8, 0x271, TRUE  @ EX 0x309
	setmetatile 12, 9, 0x23E, FALSE  @ EX 0x2C1
	setmetatile 13, 7, 0x26A, FALSE  @ EX 0x300
	setmetatile 13, 8, 0x277, TRUE  @ EX 0x310
	setmetatile 13, 9, 0x270, TRUE  @ EX 0x306
	setmetatile 13, 10, 0x274, TRUE  @ EX 0x30C
	setmetatile 14, 7, 0x26E, TRUE  @ EX 0x304
	setmetatile 14, 8, 0x272, TRUE  @ EX 0x30A
	setmetatile 14, 9, 0x23E, FALSE  @ EX 0x2C1
	goto_if_eq VAR_TEMP_4, 1, LilycoveCity_Gym_Room2_EventScript_Ex34D2C0
	goto_if_eq VAR_TEMP_4, 2, LilycoveCity_Gym_Room2_EventScript_Ex34D2CA
	end

LilycoveCity_Gym_Room2_EventScript_Ex34D2C0::
	goto LilycoveCity_Gym_Room2_EventScript_Ex34D396

LilycoveCity_Gym_Room2_EventScript_Ex34D2CA::
	goto LilycoveCity_Gym_Room2_EventScript_Ex34D2D4

LilycoveCity_Gym_Room2_EventScript_Ex34D215::
	setmetatile 21, 14, 0x241, TRUE  @ EX 0x2C9
	goto LilycoveCity_Gym_Room2_EventScript_Ex34D24E

LilycoveCity_Gym_Room2_EventScript_Ex34D1B3::
	goto_if_eq VAR_TEMP_3, 0, LilycoveCity_Gym_Room2_EventScript_Ex34D228
	goto_if_eq VAR_TEMP_3, 1, LilycoveCity_Gym_Room2_EventScript_Ex34D23B
	setmetatile 1, 18, 0x23D, TRUE  @ EX 0x2C0
	goto LilycoveCity_Gym_Room2_EventScript_Ex34D24E

LilycoveCity_Gym_Room2_EventScript_Ex34D228::
	setmetatile 1, 18, 0x23F, FALSE  @ EX 0x2C2
	goto LilycoveCity_Gym_Room2_EventScript_Ex34D24E

LilycoveCity_Gym_Room2_EventScript_Ex34D23B::
	setmetatile 1, 18, 0x241, TRUE  @ EX 0x2C9
	goto LilycoveCity_Gym_Room2_EventScript_Ex34D24E

@ Eventos novos do Pokémon Emerald EX (mapa 13.24), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
LilycoveCity_Gym_Room2_EventScript_ExTrainer0::
	trainerbattle_single TRAINER_HOENNEX_LILYCOVE_CITY_GYM_ROOM2_LOLA, LilycoveCity_Gym_Room2_Text_ExTrainer0Intro, LilycoveCity_Gym_Room2_Text_ExTrainer0Defeat
	msgbox LilycoveCity_Gym_Room2_Text_ExTrainer0PostBattle, MSGBOX_AUTOCLOSE
	end

LilycoveCity_Gym_Room2_Text_ExTrainer0Intro:
	.string "Did you know?\n"
	.string "This gym doesn’t have a singular type!$"

LilycoveCity_Gym_Room2_Text_ExTrainer0Defeat:
	.string "Wow, so many badges!$"

LilycoveCity_Gym_Room2_Text_ExTrainer0PostBattle:
	.string "Can you guess what we all have in\n"
	.string "common?$"

LilycoveCity_Gym_Room2_EventScript_ExTrainer1::
	trainerbattle_single TRAINER_HOENNEX_LILYCOVE_CITY_GYM_ROOM2_CARLOS, LilycoveCity_Gym_Room2_Text_ExTrainer1Intro, LilycoveCity_Gym_Room2_Text_ExTrainer1Defeat
	msgbox LilycoveCity_Gym_Room2_Text_ExTrainer1PostBattle, MSGBOX_AUTOCLOSE
	end

LilycoveCity_Gym_Room2_Text_ExTrainer1Intro:
	.string "Prepare to be shocked!$"

LilycoveCity_Gym_Room2_Text_ExTrainer1Defeat:
	.string "Zap!$"

LilycoveCity_Gym_Room2_Text_ExTrainer1PostBattle:
	.string "EEVEEs are for power!$"

LilycoveCity_Gym_Room2_EventScript_ExTrainer2::
	trainerbattle_single TRAINER_HOENNEX_LILYCOVE_CITY_GYM_ROOM2_SILAS, LilycoveCity_Gym_Room2_Text_ExTrainer2Intro, LilycoveCity_Gym_Room2_Text_ExTrainer2Defeat
	msgbox LilycoveCity_Gym_Room2_Text_ExTrainer2PostBattle, MSGBOX_AUTOCLOSE
	end

LilycoveCity_Gym_Room2_Text_ExTrainer2Intro:
	.string "Have you been sent outside yet?$"

LilycoveCity_Gym_Room2_Text_ExTrainer2Defeat:
	.string "Amazing!$"

LilycoveCity_Gym_Room2_Text_ExTrainer2PostBattle:
	.string "This place is not what you’d expect!$"

