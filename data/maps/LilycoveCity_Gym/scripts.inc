@ LilycoveCity_Gym: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 13.23) por dev_scripts/copia_planta_ex.py.

LilycoveCity_Gym_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LilycoveCity_Gym_OnTransition
	map_script MAP_SCRIPT_ON_LOAD, LilycoveCity_Gym_OnLoad
	.byte 0

@ Ginásio da EKRUTEA (Emerald EX 13.23 e 13.24), reescrito no nosso formato a partir da ROM
@ (decisão 7). Insígnia de CONTEÚDO: FLAG_INSIGNIA_HOENN_13; a vitória é o trainer flag da
@ TRAINER_HOENNEX_EKRUTEA. O EX não dá TM aqui: a líder dá um EEVEE (nível 25 no EX, 107 pela
@ função f do PLANO c.1), uma vez só (FLAG_HOENNEX_RECEIVED_EEVEE_EKRUTEA).
@
@ A MECÂNICA do EX, copiada comando a comando (sem nada inventado): o ginásio é escuro
@ (setflashlevel 3) e, a cada entrada, sorteia VAR_TEMP_1 a VAR_TEMP_4. O ON_LOAD redesenha
@ trechos das salas com setmetatile conforme o sorteio (os ids de metatile vão pelo de-para do
@ secundário novo gTileset_LilycoveGym; o comentário de cada linha guarda o id do EX). Pisar
@ diante de uma porta grava o warp dinâmico (setdynamicwarp): a porta certa leva à sala seguinte
@ (LilycoveCity_Gym_Room2) ou à sala da líder (warp 11 deste mapa); a errada põe o jogador na
@ rua, atrás do ginásio (warp 20 de LilycoveCity, célula 39,43 do EX). Na sala da líder a luz
@ acende (setflashlevel 0). O "return" do EX no fim dos trechos alcançados por goto vira "end":
@ com a pilha vazia os dois param o script do mesmo jeito (ScriptPop devolve NULL).
@ A sala do meio deste mapa (linhas 10 a 35) não tem porta que leve a ela no EX (a do 13.24 é a
@ que o jogo usa); entra com a planta, fiel, e fica fora do alcance, como lá.
LilycoveCity_Gym_EventScript_Ekrutea::
	trainerbattle_single TRAINER_HOENNEX_EKRUTEA, LilycoveCity_Gym_Text_EkruteaIntro, LilycoveCity_Gym_Text_EkruteaDefeat, LilycoveCity_Gym_EventScript_EkruteaDefeated, NO_MUSIC
	goto_if_unset FLAG_HOENNEX_RECEIVED_EEVEE_EKRUTEA, LilycoveCity_Gym_EventScript_GiveEevee
	msgbox LilycoveCity_Gym_Text_EkruteaPostBattle, MSGBOX_DEFAULT
	release
	end

LilycoveCity_Gym_EventScript_EkruteaDefeated::
	message LilycoveCity_Gym_Text_ReceivedEvolutionBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox LilycoveCity_Gym_Text_EvolutionBadgeInfo, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_HOENN_13
	settrainerflag TRAINER_HOENNEX_LILYCOVE_CITY_GYM_BEN
	settrainerflag TRAINER_HOENNEX_LILYCOVE_CITY_GYM_CASSANDRA
	settrainerflag TRAINER_HOENNEX_LILYCOVE_CITY_GYM_TINA
	settrainerflag TRAINER_HOENNEX_LILYCOVE_CITY_GYM_ROOM2_LOLA
	settrainerflag TRAINER_HOENNEX_LILYCOVE_CITY_GYM_ROOM2_CARLOS
	settrainerflag TRAINER_HOENNEX_LILYCOVE_CITY_GYM_ROOM2_SILAS
	goto LilycoveCity_Gym_EventScript_GiveEevee
	end

LilycoveCity_Gym_EventScript_GiveEevee::
	msgbox LilycoveCity_Gym_Text_TakeThisWithYou, MSGBOX_DEFAULT
	setvar VAR_TEMP_TRANSFERRED_SPECIES, SPECIES_EEVEE
	givemon SPECIES_EEVEE, 107
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PARTY, LilycoveCity_Gym_EventScript_EeveeParty
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PC, LilycoveCity_Gym_EventScript_EeveePC
	goto Common_EventScript_NoMoreRoomForPokemon
	end

LilycoveCity_Gym_EventScript_EeveeParty::
	call LilycoveCity_Gym_EventScript_EeveeFanfare
	msgbox gText_NicknameThisPokemon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LilycoveCity_Gym_EventScript_EeveeGiven
	call Common_EventScript_GetGiftMonPartySlot
	call Common_EventScript_NameReceivedPartyMon
	goto LilycoveCity_Gym_EventScript_EeveeGiven
	end

LilycoveCity_Gym_EventScript_EeveePC::
	call LilycoveCity_Gym_EventScript_EeveeFanfare
	msgbox gText_NicknameThisPokemon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LilycoveCity_Gym_EventScript_EeveeToPC
	call Common_EventScript_NameReceivedBoxMon
	goto LilycoveCity_Gym_EventScript_EeveeToPC
	end

LilycoveCity_Gym_EventScript_EeveeToPC::
	call Common_EventScript_TransferredToPC
	goto LilycoveCity_Gym_EventScript_EeveeGiven
	end

LilycoveCity_Gym_EventScript_EeveeFanfare::
	bufferspeciesname STR_VAR_2, SPECIES_EEVEE
	playfanfare MUS_OBTAIN_ITEM
	message LilycoveCity_Gym_Text_ObtainedEevee
	waitmessage
	waitfanfare
	bufferspeciesname STR_VAR_1, SPECIES_EEVEE
	return

LilycoveCity_Gym_EventScript_EeveeGiven::
	setflag FLAG_HOENNEX_RECEIVED_EEVEE_EKRUTEA
	msgbox LilycoveCity_Gym_Text_EeveeWillGrow, MSGBOX_DEFAULT
	release
	end

LilycoveCity_Gym_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_HOENN_13, LilycoveCity_Gym_EventScript_GymGuidePostVictory
	msgbox LilycoveCity_Gym_Text_GymGuideAdvice, MSGBOX_DEFAULT
	release
	end

LilycoveCity_Gym_EventScript_GymGuidePostVictory::
	msgbox LilycoveCity_Gym_Text_GymGuidePostVictory, MSGBOX_DEFAULT
	release
	end

LilycoveCity_Gym_EventScript_GymStatue::
	lockall
	goto_if_set FLAG_INSIGNIA_HOENN_13, LilycoveCity_Gym_EventScript_GymStatueCertified
	msgbox LilycoveCity_Gym_Text_GymStatue, MSGBOX_SIGN
	releaseall
	end

LilycoveCity_Gym_EventScript_GymStatueCertified::
	msgbox LilycoveCity_Gym_Text_GymStatueCertified, MSGBOX_SIGN
	releaseall
	end

@ Mecânica do EX (luz, sorteio, setmetatile, portas), gerada da ROM comando a comando.
LilycoveCity_Gym_OnTransition::
	setflashlevel 3
	random 2
	copyvar VAR_TEMP_1, VAR_RESULT
	random 2
	copyvar VAR_TEMP_2, VAR_RESULT
	random 3
	copyvar VAR_TEMP_3, VAR_RESULT
	random 3
	copyvar VAR_TEMP_4, VAR_RESULT
	setvar VAR_TEMP_A, 0
	end

LilycoveCity_Gym_OnLoad::
	copyvar VAR_0x8000, VAR_TEMP_2
	goto_if_eq VAR_0x8000, 0, LilycoveCity_Gym_EventScript_Ex34C0B1
	goto_if_eq VAR_0x8000, 1, LilycoveCity_Gym_EventScript_Ex34C0CF
	goto LilycoveCity_Gym_EventScript_Ex34C113

LilycoveCity_Gym_EventScript_Ex34C0B1::
	goto_if_eq VAR_TEMP_1, 0, LilycoveCity_Gym_EventScript_Ex34C0ED
	setmetatile 7, 47, 0x241, TRUE  @ EX 0x2C9
	goto LilycoveCity_Gym_EventScript_Ex34C177

LilycoveCity_Gym_EventScript_Ex34C0ED::
	setmetatile 7, 47, 0x23F, FALSE  @ EX 0x2C2
	goto LilycoveCity_Gym_EventScript_Ex34C177

LilycoveCity_Gym_EventScript_Ex34C177::
	setmetatile 3, 55, 0x256, FALSE  @ EX 0x2E9
	setmetatile 3, 54, 0x23D, FALSE  @ EX 0x2C0
	setmetatile 3, 56, 0x25E, TRUE  @ EX 0x2F1
	setmetatile 4, 55, 0x269, TRUE  @ EX 0x2FF
	setmetatile 4, 54, 0x266, TRUE  @ EX 0x2FB
	setmetatile 4, 56, 0x25F, TRUE  @ EX 0x2F2
	setmetatile 2, 53, 0x263, FALSE  @ EX 0x2F7
	setmetatile 2, 55, 0x268, TRUE  @ EX 0x2FD
	setmetatile 2, 54, 0x267, TRUE  @ EX 0x2FC
	setmetatile 2, 56, 0x260, TRUE  @ EX 0x2F3
	end

LilycoveCity_Gym_EventScript_Ex34C0CF::
	goto_if_eq VAR_TEMP_1, 0, LilycoveCity_Gym_EventScript_Ex34C100
	setmetatile 3, 55, 0x241, TRUE  @ EX 0x2C9
	goto LilycoveCity_Gym_EventScript_Ex34C113

LilycoveCity_Gym_EventScript_Ex34C100::
	setmetatile 3, 55, 0x23F, TRUE  @ EX 0x2C2
	goto LilycoveCity_Gym_EventScript_Ex34C113

LilycoveCity_Gym_EventScript_Ex34C113::
	setmetatile 7, 46, 0x242, FALSE  @ EX 0x2CB
	setmetatile 7, 47, 0x23D, FALSE  @ EX 0x2C0
	setmetatile 7, 48, 0x23D, FALSE  @ EX 0x2C0
	setmetatile 8, 47, 0x265, TRUE  @ EX 0x2F9
	setmetatile 8, 48, 0x265, TRUE  @ EX 0x2F9
	setmetatile 6, 47, 0x265, TRUE  @ EX 0x2F9
	setmetatile 6, 48, 0x265, TRUE  @ EX 0x2F9
	setmetatile 8, 46, 0x267, TRUE  @ EX 0x2FC
	setmetatile 6, 46, 0x267, TRUE  @ EX 0x2FC
	setmetatile 8, 49, 0x25A, TRUE  @ EX 0x2ED
	setmetatile 6, 49, 0x259, TRUE  @ EX 0x2EC
	end

LilycoveCity_Gym_EventScript_FirstRoomDoorEast::
	goto_if_eq VAR_TEMP_1, 1, LilycoveCity_Gym_EventScript_Ex34C211
	setdynamicwarp MAP_LILYCOVE_CITY, 20
	setvar VAR_TEMP_0, 1
	end

LilycoveCity_Gym_EventScript_Ex34C211::
	setdynamicwarp MAP_LILYCOVE_CITY_GYM_ROOM2, 0
	goto LilycoveCity_Gym_EventScript_Ex34C20B

LilycoveCity_Gym_EventScript_Ex34C20B::
	setvar VAR_TEMP_0, 1
	end

LilycoveCity_Gym_EventScript_FirstRoomDoorWest::
	goto_if_eq VAR_TEMP_1, 0, LilycoveCity_Gym_EventScript_Ex34C1EB
	setdynamicwarp MAP_LILYCOVE_CITY, 20
	setvar VAR_TEMP_0, 1
	end

LilycoveCity_Gym_EventScript_Ex34C1EB::
	setdynamicwarp MAP_LILYCOVE_CITY_GYM_ROOM2, 0
	goto LilycoveCity_Gym_EventScript_Ex34C1E5

LilycoveCity_Gym_EventScript_Ex34C1E5::
	setvar VAR_TEMP_0, 1
	end

LilycoveCity_Gym_EventScript_StepAwayFromDoor::
	setvar VAR_TEMP_0, 0
	end

LilycoveCity_Gym_EventScript_LastDoorMiddle::
	goto_if_eq VAR_TEMP_3, 2, LilycoveCity_Gym_EventScript_Ex34D442
	setdynamicwarp MAP_LILYCOVE_CITY, 20
	setvar VAR_TEMP_0, 1
	end

LilycoveCity_Gym_EventScript_Ex34D442::
	setdynamicwarp MAP_LILYCOVE_CITY_GYM, 11
	goto LilycoveCity_Gym_EventScript_Ex34D43C

LilycoveCity_Gym_EventScript_Ex34D43C::
	setvar VAR_TEMP_0, 1
	end

LilycoveCity_Gym_EventScript_LastDoorEast::
	goto_if_eq VAR_TEMP_3, 1, LilycoveCity_Gym_EventScript_Ex34D468
	setdynamicwarp MAP_LILYCOVE_CITY, 20
	setvar VAR_TEMP_0, 1
	end

LilycoveCity_Gym_EventScript_Ex34D468::
	setdynamicwarp MAP_LILYCOVE_CITY_GYM, 11
	goto LilycoveCity_Gym_EventScript_Ex34D462

LilycoveCity_Gym_EventScript_Ex34D462::
	setvar VAR_TEMP_0, 1
	end

LilycoveCity_Gym_EventScript_LastDoorWest::
	goto_if_eq VAR_TEMP_3, 0, LilycoveCity_Gym_EventScript_Ex34D41C
	setdynamicwarp MAP_LILYCOVE_CITY, 20
	setvar VAR_TEMP_0, 1
	end

LilycoveCity_Gym_EventScript_Ex34D41C::
	setdynamicwarp MAP_LILYCOVE_CITY_GYM, 11
	goto LilycoveCity_Gym_EventScript_Ex34D416

LilycoveCity_Gym_EventScript_Ex34D416::
	setvar VAR_TEMP_0, 1
	end

LilycoveCity_Gym_EventScript_LeaderRoomLights::
	setflashlevel 0
	setvar VAR_TEMP_A, 1
	end

LilycoveCity_Gym_Text_EkruteaIntro:
	.string "Teehee...\p"
	.string "Hello there!\p"
	.string "My name is Ekrutea!\n"
	.string "I have five older sisters who taught me\l"
	.string "how precious little EEVEEs could be!\p"
	.string "But, they all settled for only one\n"
	.string "element!\p"
	.string "I decided to master them all.\p"
	.string "Are you ready for the ultimate Eevee\n"
	.string "Master?\p"
	.string "Let’s dance!$"

LilycoveCity_Gym_Text_EkruteaDefeat:
	.string "That was beautiful!\p"
	.string "You defeated all my Eevees!\p"
	.string "Perhaps you are the true master of the\n"
	.string "elements!$"

LilycoveCity_Gym_Text_ReceivedEvolutionBadge:
	.string "{PLAYER} received the EVOLUTION\n"
	.string "BADGE from EKRUTEA.$"

LilycoveCity_Gym_Text_EvolutionBadgeInfo:
	.string "The EVOLUTION BADGE shows your\n"
	.string "mastery over many different kinds of\l"
	.string "POKéMON.$"

LilycoveCity_Gym_Text_TakeThisWithYou:
	.string "This might be strange,\n"
	.string "but I want you to take this with you.$"

LilycoveCity_Gym_Text_ObtainedEevee:
	.string "{PLAYER} obtained a EEVEE.$"

LilycoveCity_Gym_Text_EeveeWillGrow:
	.string "I can tell you are a kind trainer so I\n"
	.string "know that EEVEE will grow up nice and\l"
	.string "strong!.\p"
	.string "I wonder what your EEVEE with become!$"

LilycoveCity_Gym_Text_EkruteaPostBattle:
	.string "I enjoyed our dance!$"

LilycoveCity_Gym_Text_GymGuideAdvice:
	.string "{PLAYER} be careful exploring this\n"
	.string "GYM!\p"
	.string "Some of the doors lead outside!\n"
	.string "Another oddity,\n"
	.string "I can’t seem to find a type for this\l"
	.string "GYM!\p"
	.string "Only thing I’ve got is that a lot of\n"
	.string "trainers use the same family of\l"
	.string "POKéMON...$"

LilycoveCity_Gym_Text_GymGuidePostVictory:
	.string "{PLAYER} the victor!\p"
	.string "Keep pushing you’re starting to get\n"
	.string "close!$"

LilycoveCity_Gym_Text_GymStatue:
	.string "LILYCOVE CITY POKéMON GYM$"

LilycoveCity_Gym_Text_GymStatueCertified:
	.string "LILYCOVE CITY POKéMON GYM\p"
	.string "EKRUTEA’S CERTIFIED TRAINERS:\n"
	.string "{PLAYER}$"

@ Eventos novos do Pokémon Emerald EX (mapa 13.23), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
LilycoveCity_Gym_EventScript_ExTrainer2::
	trainerbattle_single TRAINER_HOENNEX_LILYCOVE_CITY_GYM_BEN, LilycoveCity_Gym_Text_ExTrainer2Intro, LilycoveCity_Gym_Text_ExTrainer2Defeat
	msgbox LilycoveCity_Gym_Text_ExTrainer2PostBattle, MSGBOX_AUTOCLOSE
	end

LilycoveCity_Gym_Text_ExTrainer2Intro:
	.string "These doors keep sending me outside.$"

LilycoveCity_Gym_Text_ExTrainer2Defeat:
	.string "Brrrr!$"

LilycoveCity_Gym_Text_ExTrainer2PostBattle:
	.string "I wonder if there’s a hint for which\n"
	.string "door is correct?$"

LilycoveCity_Gym_EventScript_ExTrainer3::
	trainerbattle_single TRAINER_HOENNEX_LILYCOVE_CITY_GYM_CASSANDRA, LilycoveCity_Gym_Text_ExTrainer3Intro, LilycoveCity_Gym_Text_ExTrainer3Defeat
	msgbox LilycoveCity_Gym_Text_ExTrainer3PostBattle, MSGBOX_AUTOCLOSE
	end

LilycoveCity_Gym_Text_ExTrainer3Intro:
	.string "What’s your favorite Evolution of\n"
	.string "EEVEE?$"

LilycoveCity_Gym_Text_ExTrainer3Defeat:
	.string "My precious DELCATTY$"

LilycoveCity_Gym_Text_ExTrainer3PostBattle:
	.string "I can’t find my way out of here.$"

LilycoveCity_Gym_EventScript_ExTrainer4::
	trainerbattle_single TRAINER_HOENNEX_LILYCOVE_CITY_GYM_TINA, LilycoveCity_Gym_Text_ExTrainer4Intro, LilycoveCity_Gym_Text_ExTrainer4Defeat
	msgbox LilycoveCity_Gym_Text_ExTrainer4PostBattle, MSGBOX_AUTOCLOSE
	end

LilycoveCity_Gym_Text_ExTrainer4Intro:
	.string "Prepared to be scared!$"

LilycoveCity_Gym_Text_ExTrainer4Defeat:
	.string "Yikes!$"

LilycoveCity_Gym_Text_ExTrainer4PostBattle:
	.string "EEVEEs are for the dark!$"

