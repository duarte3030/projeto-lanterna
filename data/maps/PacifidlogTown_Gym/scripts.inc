@ PacifidlogTown_Gym: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 7.7) por dev_scripts/copia_planta_ex.py.

PacifidlogTown_Gym_MapScripts::
	.byte 0

@ Ginásio da JASMINE de Hoenn (Emerald EX 7.7), reescrito no nosso formato a partir do texto da
@ ROM (decisão 7). Treinadora NOVA (TRAINER_HOENNEX_JASMINE), distinta da Jasmine de Johto, que
@ não é tocada (decisão 89 do Gui). Insígnia de CONTEÚDO: FLAG_INSIGNIA_HOENN_14. A vitória é o
@ trainer flag da líder. Como no EX, a vitória marca os três treinadores do ginásio como vencidos.
@ Fora, de propósito: a frase do EX "With the ALLOY BADGE you can use DIVE outside of battle".
@ No nosso jogo o golpe de campo lê as insígnias de Kanto (PLANO b), então a frase seria falsa.
PacifidlogTown_Gym_EventScript_Jasmine::
	trainerbattle_single TRAINER_HOENNEX_JASMINE, PacifidlogTown_Gym_Text_JasmineIntro, PacifidlogTown_Gym_Text_JasmineDefeat, PacifidlogTown_Gym_EventScript_JasmineDefeated, NO_MUSIC
	goto_if_unset FLAG_HOENNEX_RECEIVED_TM_IRON_TAIL_JASMINE, PacifidlogTown_Gym_EventScript_GiveIronTail
	msgbox PacifidlogTown_Gym_Text_JasminePostBattle, MSGBOX_DEFAULT
	release
	end

PacifidlogTown_Gym_EventScript_JasmineDefeated::
	message PacifidlogTown_Gym_Text_ReceivedAlloyBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox PacifidlogTown_Gym_Text_AlloyBadgeTakeThis, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_HOENN_14
	settrainerflag TRAINER_HOENNEX_PACIFIDLOG_TOWN_GYM_MARCEL
	settrainerflag TRAINER_HOENNEX_PACIFIDLOG_TOWN_GYM_DAISY
	settrainerflag TRAINER_HOENNEX_PACIFIDLOG_TOWN_GYM_ERIK
	goto PacifidlogTown_Gym_EventScript_GiveIronTail
	end

PacifidlogTown_Gym_EventScript_GiveIronTail::
	giveitem ITEM_TM_IRON_TAIL
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_HOENNEX_RECEIVED_TM_IRON_TAIL_JASMINE
	msgbox PacifidlogTown_Gym_Text_ExplainIronTail, MSGBOX_DEFAULT
	release
	end

PacifidlogTown_Gym_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_HOENN_14, PacifidlogTown_Gym_EventScript_GymGuidePostVictory
	msgbox PacifidlogTown_Gym_Text_GymGuideAdvice, MSGBOX_DEFAULT
	release
	end

PacifidlogTown_Gym_EventScript_GymGuidePostVictory::
	msgbox PacifidlogTown_Gym_Text_GymGuidePostVictory, MSGBOX_DEFAULT
	release
	end

PacifidlogTown_Gym_EventScript_GymStatue::
	lockall
	goto_if_set FLAG_INSIGNIA_HOENN_14, PacifidlogTown_Gym_EventScript_GymStatueCertified
	msgbox PacifidlogTown_Gym_Text_GymStatue, MSGBOX_SIGN
	releaseall
	end

PacifidlogTown_Gym_EventScript_GymStatueCertified::
	msgbox PacifidlogTown_Gym_Text_GymStatueCertified, MSGBOX_SIGN
	releaseall
	end

PacifidlogTown_Gym_Text_JasmineIntro:
	.string "Hello challenger!\n"
	.string "My name is Jasmine.\p"
	.string "Caring for my POKéMON,\n"
	.string "I learned all of STEEL’s type\l"
	.string "advantages, all it’s strengths and\l"
	.string "weaknesses.\p"
	.string "Try to put a dent in my POKéMON.$"

PacifidlogTown_Gym_Text_JasmineDefeat:
	.string "Wow! you defeated me!\n"
	.string "You’re stronger than steel!\p"
	.string "You’ve earned the Alloy Badge!$"

PacifidlogTown_Gym_Text_ReceivedAlloyBadge:
	.string "{PLAYER} received the ALLOY BADGE\n"
	.string "from JASMINE.$"

PacifidlogTown_Gym_Text_AlloyBadgeTakeThis:
	.string "Here take TM23 IRON TAIL.$"

PacifidlogTown_Gym_Text_ExplainIronTail:
	.string "IRON TAIL smashes your foe with\n"
	.string "tempered steel!$"

PacifidlogTown_Gym_Text_JasminePostBattle:
	.string "Good luck with the POKéMON LEAGUE!\p"
	.string "I’m rooting for you!$"

PacifidlogTown_Gym_Text_GymGuideAdvice:
	.string "Welcome {PLAYER}!\n"
	.string "Hailing all the way from the JOHTO\l"
	.string "REGION, it’s JASMINE!\p"
	.string "Her STEELIE gaze can break the spirit\n"
	.string "of the toughest TRAINERS!\p"
	.string "Be careful to bring FIRE and GROUND\n"
	.string "TYPES or she’ll be hard to beat!$"

PacifidlogTown_Gym_Text_GymGuidePostVictory:
	.string "Hey {PLAYER}.\p"
	.string "JASMINE has asked me to stop saying\n"
	.string "she has a STEELIE gaze...\p"
	.string "Apparently it’s considered slander...$"

PacifidlogTown_Gym_Text_GymStatue:
	.string "PACIFIDLOG TOWN POKéMON GYM$"

PacifidlogTown_Gym_Text_GymStatueCertified:
	.string "PACIFIDLOG TOWN POKéMON GYM\p"
	.string "JASMINE’S CERTIFIED TRAINERS:\n"
	.string "{PLAYER}$"

@ Eventos novos do Pokémon Emerald EX (mapa 7.7), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
PacifidlogTown_Gym_EventScript_ExTrainer1::
	trainerbattle_single TRAINER_HOENNEX_PACIFIDLOG_TOWN_GYM_MARCEL, PacifidlogTown_Gym_Text_ExTrainer1Intro, PacifidlogTown_Gym_Text_ExTrainer1Defeat
	msgbox PacifidlogTown_Gym_Text_ExTrainer1PostBattle, MSGBOX_AUTOCLOSE
	end

PacifidlogTown_Gym_Text_ExTrainer1Intro:
	.string "What’s your tensile strength?$"

PacifidlogTown_Gym_Text_ExTrainer1Defeat:
	.string "Strong child!$"

PacifidlogTown_Gym_Text_ExTrainer1PostBattle:
	.string "STEEL your strength young one!$"

PacifidlogTown_Gym_EventScript_ExTrainer2::
	trainerbattle_single TRAINER_HOENNEX_PACIFIDLOG_TOWN_GYM_DAISY, PacifidlogTown_Gym_Text_ExTrainer2Intro, PacifidlogTown_Gym_Text_ExTrainer2Defeat
	msgbox PacifidlogTown_Gym_Text_ExTrainer2PostBattle, MSGBOX_AUTOCLOSE
	end

PacifidlogTown_Gym_Text_ExTrainer2Intro:
	.string "Hi! I’m Daisy from Jubilife City!$"

PacifidlogTown_Gym_Text_ExTrainer2Defeat:
	.string "Ouch!$"

PacifidlogTown_Gym_Text_ExTrainer2PostBattle:
	.string "You Hoenn trainers sure are strong!$"

PacifidlogTown_Gym_EventScript_ExTrainer4::
	trainerbattle_single TRAINER_HOENNEX_PACIFIDLOG_TOWN_GYM_ERIK, PacifidlogTown_Gym_Text_ExTrainer4Intro, PacifidlogTown_Gym_Text_ExTrainer4Defeat
	msgbox PacifidlogTown_Gym_Text_ExTrainer4PostBattle, MSGBOX_AUTOCLOSE
	end

PacifidlogTown_Gym_Text_ExTrainer4Intro:
	.string "Don’t embarrass me in front of JASMINE!$"

PacifidlogTown_Gym_Text_ExTrainer4Defeat:
	.string "HEY!$"

PacifidlogTown_Gym_Text_ExTrainer4PostBattle:
	.string "Why’d JASMINE have to get married...$"

