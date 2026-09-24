@ FallarborTown_Gym: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 5.8) por dev_scripts/copia_planta_ex.py.

FallarborTown_Gym_MapScripts::
	.byte 0

@ Ginásio da LUCY (Emerald EX 5.8), reescrito no nosso formato a partir do texto da ROM (decisão 7).
@ Insígnia de CONTEÚDO: FLAG_INSIGNIA_HOENN_12 (o motor lê as 8 de Kanto; obediência não muda).
@ A vitória é o trainer flag da TRAINER_HOENNEX_LUCY (trainerbattle_single pula a luta de novo).
@ Como no EX, a vitória sobre a líder marca os cinco treinadores do ginásio como vencidos.
@ Fora, de propósito: o EX também mexe em VAR_PETALBURG_GYM_STATE (0x4085) aqui; o nosso
@ Norman segue a contagem dos 8 ginásios originais.
FallarborTown_Gym_EventScript_Lucy::
	trainerbattle_single TRAINER_HOENNEX_LUCY, FallarborTown_Gym_Text_LucyIntro, FallarborTown_Gym_Text_LucyDefeat, FallarborTown_Gym_EventScript_LucyDefeated, NO_MUSIC
	goto_if_unset FLAG_HOENNEX_RECEIVED_TM_TOXIC_LUCY, FallarborTown_Gym_EventScript_GiveToxic
	msgbox FallarborTown_Gym_Text_LucyPostBattle, MSGBOX_DEFAULT
	release
	end

FallarborTown_Gym_EventScript_LucyDefeated::
	message FallarborTown_Gym_Text_ReceivedImmunityBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox FallarborTown_Gym_Text_ImmunityBadgeInfo, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_HOENN_12
	settrainerflag TRAINER_HOENNEX_FALLARBOR_TOWN_GYM_JJ
	settrainerflag TRAINER_HOENNEX_FALLARBOR_TOWN_GYM_IVY
	settrainerflag TRAINER_HOENNEX_FALLARBOR_TOWN_GYM_ALEXA
	settrainerflag TRAINER_HOENNEX_FALLARBOR_TOWN_GYM_LUIGI
	settrainerflag TRAINER_HOENNEX_FALLARBOR_TOWN_GYM_AKIRA
	goto FallarborTown_Gym_EventScript_GiveToxic
	end

FallarborTown_Gym_EventScript_GiveToxic::
	giveitem ITEM_TM_TOXIC
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_HOENNEX_RECEIVED_TM_TOXIC_LUCY
	msgbox FallarborTown_Gym_Text_ExplainToxic, MSGBOX_DEFAULT
	release
	end

FallarborTown_Gym_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_HOENN_12, FallarborTown_Gym_EventScript_GymGuidePostVictory
	msgbox FallarborTown_Gym_Text_GymGuideAdvice, MSGBOX_DEFAULT
	release
	end

FallarborTown_Gym_EventScript_GymGuidePostVictory::
	msgbox FallarborTown_Gym_Text_GymGuidePostVictory, MSGBOX_DEFAULT
	release
	end

FallarborTown_Gym_EventScript_GymStatue::
	lockall
	goto_if_set FLAG_INSIGNIA_HOENN_12, FallarborTown_Gym_EventScript_GymStatueCertified
	msgbox FallarborTown_Gym_Text_GymStatue, MSGBOX_SIGN
	releaseall
	end

FallarborTown_Gym_EventScript_GymStatueCertified::
	msgbox FallarborTown_Gym_Text_GymStatueCertified, MSGBOX_SIGN
	releaseall
	end

FallarborTown_Gym_Text_LucyIntro:
	.string "Hello challenger.\n"
	.string "Let me introduce myself.\p"
	.string "My name is LUCY.\p"
	.string "As a young research assistant in\n"
	.string "Professor Birch’s lab I became\l"
	.string "fascinated with POKéMON that had\l"
	.string "deadly venom running through their\l"
	.string "veins.\p"
	.string "But eventually I got bored of studying\n"
	.string "and decided to give play a try.\p"
	.string "Well?\p"
	.string "Are you ready for a lethal dose?$"

FallarborTown_Gym_Text_LucyDefeat:
	.string "Fascinating!\p"
	.string "Here you’ve earned this.$"

FallarborTown_Gym_Text_ReceivedImmunityBadge:
	.string "{PLAYER} received the IMMUNITY\n"
	.string "BADGE from LUCY.$"

FallarborTown_Gym_Text_ImmunityBadgeInfo:
	.string "Are you filling out a POKéDEX?\p"
	.string "Those are rare.\n"
	.string "You’d better take care of it!$"

FallarborTown_Gym_Text_ExplainToxic:
	.string "TM06 contains TOXIC.\p"
	.string "It will badly POISON anything hit by it.$"

FallarborTown_Gym_Text_LucyPostBattle:
	.string "Say hi to BIRCH for me.$"

FallarborTown_Gym_Text_GymGuideAdvice:
	.string "Oh hey {PLAYER}!\p"
	.string "I was just doing some research on the\n"
	.string "GYM here...\p"
	.string "Anyway LEADER LUCY is a strong POISON\n"
	.string "TYPE user, be careful using GRASS TYPES\l"
	.string "against her. But, if you come at her with\l"
	.string "some GROUND, PSYCHIC, or STEEL types\l"
	.string "you’ll take her down for sure!$"

FallarborTown_Gym_Text_GymGuidePostVictory:
	.string "Good job {PLAYER}.\p"
	.string "At this point I knew you’d win!$"

FallarborTown_Gym_Text_GymStatue:
	.string "FALLARBOR TOWN POKéMON GYM$"

@ No EX a estátua diz "ERIKA'S CERTIFIED TRAINERS" (erro de cópia do autor): aqui, LUCY.
FallarborTown_Gym_Text_GymStatueCertified:
	.string "FALLARBOR TOWN POKéMON GYM\p"
	.string "LUCY’S CERTIFIED TRAINERS:\n"
	.string "{PLAYER}$"

@ Eventos novos do Pokémon Emerald EX (mapa 5.8), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
FallarborTown_Gym_EventScript_ExTrainer2::
	trainerbattle_single TRAINER_HOENNEX_FALLARBOR_TOWN_GYM_JJ, FallarborTown_Gym_Text_ExTrainer2Intro, FallarborTown_Gym_Text_ExTrainer2Defeat
	msgbox FallarborTown_Gym_Text_ExTrainer2PostBattle, MSGBOX_AUTOCLOSE
	end

FallarborTown_Gym_Text_ExTrainer2Intro:
	.string "Ready to be stung?$"

FallarborTown_Gym_Text_ExTrainer2Defeat:
	.string "Ouch!$"

FallarborTown_Gym_Text_ExTrainer2PostBattle:
	.string "Always pack ANTIDOTE!$"

FallarborTown_Gym_EventScript_ExTrainer3::
	trainerbattle_single TRAINER_HOENNEX_FALLARBOR_TOWN_GYM_IVY, FallarborTown_Gym_Text_ExTrainer3Intro, FallarborTown_Gym_Text_ExTrainer3Defeat
	msgbox FallarborTown_Gym_Text_ExTrainer3PostBattle, MSGBOX_AUTOCLOSE
	end

FallarborTown_Gym_Text_ExTrainer3Intro:
	.string "Plants can be poisonous too!$"

FallarborTown_Gym_Text_ExTrainer3Defeat:
	.string "Shriveled up!$"

FallarborTown_Gym_Text_ExTrainer3PostBattle:
	.string "I like the atmosphere here!$"

FallarborTown_Gym_EventScript_ExTrainer4::
	trainerbattle_single TRAINER_HOENNEX_FALLARBOR_TOWN_GYM_ALEXA, FallarborTown_Gym_Text_ExTrainer4Intro, FallarborTown_Gym_Text_ExTrainer4Defeat
	msgbox FallarborTown_Gym_Text_ExTrainer4PostBattle, MSGBOX_AUTOCLOSE
	end

FallarborTown_Gym_Text_ExTrainer4Intro:
	.string "I’m Lucy’s oldest friend!$"

FallarborTown_Gym_Text_ExTrainer4Defeat:
	.string "Wow!$"

FallarborTown_Gym_Text_ExTrainer4PostBattle:
	.string "Lucy and I met in RUSTBORO CITY!$"

FallarborTown_Gym_EventScript_ExTrainer5::
	trainerbattle_single TRAINER_HOENNEX_FALLARBOR_TOWN_GYM_LUIGI, FallarborTown_Gym_Text_ExTrainer5Intro, FallarborTown_Gym_Text_ExTrainer5Defeat
	msgbox FallarborTown_Gym_Text_ExTrainer5PostBattle, MSGBOX_AUTOCLOSE
	end

FallarborTown_Gym_Text_ExTrainer5Intro:
	.string "I came when I heard there were BUGS in\n"
	.string "the games here!$"

FallarborTown_Gym_Text_ExTrainer5Defeat:
	.string "Turns out the games don’t have real\n"
	.string "BUGS in them...$"

FallarborTown_Gym_Text_ExTrainer5PostBattle:
	.string "I want to play a game with BUGS in it.$"

FallarborTown_Gym_EventScript_ExTrainer6::
	trainerbattle_single TRAINER_HOENNEX_FALLARBOR_TOWN_GYM_AKIRA, FallarborTown_Gym_Text_ExTrainer6Intro, FallarborTown_Gym_Text_ExTrainer6Defeat
	msgbox FallarborTown_Gym_Text_ExTrainer6PostBattle, MSGBOX_AUTOCLOSE
	end

FallarborTown_Gym_Text_ExTrainer6Intro:
	.string "I’m going to give you a Game Over!$"

FallarborTown_Gym_Text_ExTrainer6Defeat:
	.string "Oh no! Game Over!$"

FallarborTown_Gym_Text_ExTrainer6PostBattle:
	.string "I wanna play a ninja game!$"

FallarborTown_Gym_EventScript_ExNpc7::
	msgbox FallarborTown_Gym_Text_ExNpc7, MSGBOX_NPC
	end

FallarborTown_Gym_Text_ExNpc7:
	.string "Huh?...\n"
	.string "Battle?...\p"
	.string "Oh no I’m not a TRAINER\n"
	.string "I’m just here to play games.$"

