@ VerdanturfTown_Gym: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 6.9) por dev_scripts/copia_planta_ex.py.

VerdanturfTown_Gym_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 6.9), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
VerdanturfTown_Gym_EventScript_ExTrainer5::
	trainerbattle_single TRAINER_HOENNEX_VERDANTURF_TOWN_GYM_RACHYL, VerdanturfTown_Gym_Text_ExTrainer5Intro, VerdanturfTown_Gym_Text_ExTrainer5Defeat
	msgbox VerdanturfTown_Gym_Text_ExTrainer5PostBattle, MSGBOX_AUTOCLOSE
	end

VerdanturfTown_Gym_Text_ExTrainer5Intro:
	.string "It was big news when VERDANTURF got a\n"
	.string "GYM!$"

VerdanturfTown_Gym_Text_ExTrainer5Defeat:
	.string "The GYM is good for the local economy.$"

VerdanturfTown_Gym_Text_ExTrainer5PostBattle:
	.string "I just hope the GYM doesn’t change\n"
	.string "VERDANTURF too much.$"

VerdanturfTown_Gym_EventScript_ExTrainer6::
	trainerbattle_single TRAINER_HOENNEX_VERDANTURF_TOWN_GYM_SANDY, VerdanturfTown_Gym_Text_ExTrainer6Intro, VerdanturfTown_Gym_Text_ExTrainer6Defeat
	msgbox VerdanturfTown_Gym_Text_ExTrainer6PostBattle, MSGBOX_AUTOCLOSE
	end

VerdanturfTown_Gym_Text_ExTrainer6Intro:
	.string "Were you born and raised in this region?$"

VerdanturfTown_Gym_Text_ExTrainer6Defeat:
	.string "Wow what a battle!$"

VerdanturfTown_Gym_Text_ExTrainer6PostBattle:
	.string "I was born in BLACKTHORN but met ERIKA\n"
	.string "when I moved to HOENN!$"

VerdanturfTown_Gym_EventScript_ExTrainer7::
	trainerbattle_single TRAINER_HOENNEX_VERDANTURF_TOWN_GYM_KADENCE, VerdanturfTown_Gym_Text_ExTrainer7Intro, VerdanturfTown_Gym_Text_ExTrainer7Defeat
	msgbox VerdanturfTown_Gym_Text_ExTrainer7PostBattle, MSGBOX_AUTOCLOSE
	end

VerdanturfTown_Gym_Text_ExTrainer7Intro:
	.string "ERIKA gave me my first POKéMON.$"

VerdanturfTown_Gym_Text_ExTrainer7Defeat:
	.string "Even ERIKA’S POKéMON couldn’t beat\n"
	.string "you!$"

VerdanturfTown_Gym_Text_ExTrainer7PostBattle:
	.string "GRASS TYPE POKéMON are the BEST!$"

VerdanturfTown_Gym_EventScript_ExTrainer8::
	trainerbattle_single TRAINER_HOENNEX_VERDANTURF_TOWN_GYM_RIVER, VerdanturfTown_Gym_Text_ExTrainer8Intro, VerdanturfTown_Gym_Text_ExTrainer8Defeat
	msgbox VerdanturfTown_Gym_Text_ExTrainer8PostBattle, MSGBOX_AUTOCLOSE
	end

VerdanturfTown_Gym_Text_ExTrainer8Intro:
	.string "No boys are allowed in this GYM!$"

VerdanturfTown_Gym_Text_ExTrainer8Defeat:
	.string "This GYM is a haven for us girlies.$"

VerdanturfTown_Gym_Text_ExTrainer8PostBattle:
	.string "Are you going to challenge ERIKA?$"

VerdanturfTown_Gym_EventScript_ExTrainer9::
	trainerbattle_single TRAINER_HOENNEX_VERDANTURF_TOWN_GYM_RYLEE, VerdanturfTown_Gym_Text_ExTrainer9Intro, VerdanturfTown_Gym_Text_ExTrainer9Defeat
	msgbox VerdanturfTown_Gym_Text_ExTrainer9PostBattle, MSGBOX_AUTOCLOSE
	end

VerdanturfTown_Gym_Text_ExTrainer9Intro:
	.string "It’s nice training in an all female GYM!$"

VerdanturfTown_Gym_Text_ExTrainer9Defeat:
	.string "Well it was nice.$"

VerdanturfTown_Gym_Text_ExTrainer9PostBattle:
	.string "I can train here with all my friends!$"

VerdanturfTown_Gym_EventScript_ExTrainer10::
	trainerbattle_single TRAINER_HOENNEX_VERDANTURF_TOWN_GYM_PATRICIA, VerdanturfTown_Gym_Text_ExTrainer10Intro, VerdanturfTown_Gym_Text_ExTrainer10Defeat
	msgbox VerdanturfTown_Gym_Text_ExTrainer10PostBattle, MSGBOX_AUTOCLOSE
	end

VerdanturfTown_Gym_Text_ExTrainer10Intro:
	.string "Isn’t this GYM lovely?$"

VerdanturfTown_Gym_Text_ExTrainer10Defeat:
	.string "A great battle!$"

VerdanturfTown_Gym_Text_ExTrainer10PostBattle:
	.string "The bushes here flower once a year.$"

VerdanturfTown_Gym_EventScript_ExTrainer11::
	trainerbattle_single TRAINER_HOENNEX_VERDANTURF_TOWN_GYM_JANNICE, VerdanturfTown_Gym_Text_ExTrainer11Intro, VerdanturfTown_Gym_Text_ExTrainer11Defeat
	msgbox VerdanturfTown_Gym_Text_ExTrainer11PostBattle, MSGBOX_AUTOCLOSE
	end

VerdanturfTown_Gym_Text_ExTrainer11Intro:
	.string "Prepare yourself for my GRASS POKéMON.$"

VerdanturfTown_Gym_Text_ExTrainer11Defeat:
	.string "My BAYLEEF!$"

VerdanturfTown_Gym_Text_ExTrainer11PostBattle:
	.string "ERIKA is an expert healer.\n"
	.string "She heals all our POKéMON after\l"
	.string "battles!$"


@ Líder, guia e estátuas do ginásio do EX (mapa 6.9), reescritos no nosso formato a partir do
@ texto da ROM (lote G1 da onda 2). A vitória é goto_if_defeated no líder; a insígnia é FLAG_INSIGNIA_HOENN_11.

VerdanturfTown_Gym_EventScript_Erika::
	trainerbattle_single TRAINER_HOENNEX_ERIKA, VerdanturfTown_Gym_Text_ErikaIntro, VerdanturfTown_Gym_Text_ErikaDefeat, VerdanturfTown_Gym_EventScript_ErikaDefeated, NO_MUSIC
	goto_if_unset FLAG_HOENNEX_RECEIVED_TM_GIGA_DRAIN, VerdanturfTown_Gym_EventScript_GiveErikaItem
	msgbox VerdanturfTown_Gym_Text_ErikaPostBattle, MSGBOX_NPC
	release
	end

VerdanturfTown_Gym_EventScript_ErikaDefeated::
	message VerdanturfTown_Gym_Text_ReceivedErikaBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox VerdanturfTown_Gym_Text_ErikaBadgeInfo, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_HOENN_11
	settrainerflag TRAINER_HOENNEX_VERDANTURF_TOWN_GYM_RACHYL
	settrainerflag TRAINER_HOENNEX_VERDANTURF_TOWN_GYM_SANDY
	settrainerflag TRAINER_HOENNEX_VERDANTURF_TOWN_GYM_KADENCE
	settrainerflag TRAINER_HOENNEX_VERDANTURF_TOWN_GYM_RIVER
	settrainerflag TRAINER_HOENNEX_VERDANTURF_TOWN_GYM_RYLEE
	settrainerflag TRAINER_HOENNEX_VERDANTURF_TOWN_GYM_PATRICIA
	settrainerflag TRAINER_HOENNEX_VERDANTURF_TOWN_GYM_JANNICE
	call_if_eq VAR_PETALBURG_GYM_STATE, 6, Common_EventScript_ReadyPetalburgGymForBattle
	goto VerdanturfTown_Gym_EventScript_GiveErikaItem
	end

VerdanturfTown_Gym_EventScript_GiveErikaItem::
	giveitem ITEM_TM_GIGA_DRAIN
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_HOENNEX_RECEIVED_TM_GIGA_DRAIN
	msgbox VerdanturfTown_Gym_Text_ExplainErikaItem, MSGBOX_NPC
	release
	end

VerdanturfTown_Gym_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_defeated TRAINER_HOENNEX_ERIKA, VerdanturfTown_Gym_EventScript_GymGuidePostVictory
	msgbox VerdanturfTown_Gym_Text_GymGuideAdvice, MSGBOX_DEFAULT
	release
	end

VerdanturfTown_Gym_EventScript_GymGuidePostVictory::
	msgbox VerdanturfTown_Gym_Text_GymGuidePostVictory, MSGBOX_DEFAULT
	release
	end

VerdanturfTown_Gym_EventScript_LeftGymStatue::
	lockall
	goto_if_set FLAG_INSIGNIA_HOENN_11, VerdanturfTown_Gym_EventScript_GymStatueCertified
	goto VerdanturfTown_Gym_EventScript_GymStatue
	end

VerdanturfTown_Gym_EventScript_RightGymStatue::
	lockall
	goto_if_set FLAG_INSIGNIA_HOENN_11, VerdanturfTown_Gym_EventScript_GymStatueCertified
	goto VerdanturfTown_Gym_EventScript_GymStatue
	end

VerdanturfTown_Gym_EventScript_GymStatueCertified::
	msgbox VerdanturfTown_Gym_Text_GymStatueCertified, MSGBOX_SIGN
	releaseall
	end

VerdanturfTown_Gym_EventScript_GymStatue::
	msgbox VerdanturfTown_Gym_Text_GymStatue, MSGBOX_SIGN
	releaseall
	end

VerdanturfTown_Gym_Text_ErikaIntro:
	.string "Why hello there challenger.\p"
	.string "I must not have been paying attention\n"
	.string "when you came in.\p"
	.string "I apologize, let me introduce myself.\p"
	.string "My name is Erika.\n"
	.string "I moved here recently from the Kanto\l"
	.string "region to establish this sanctuary for\l"
	.string "women and GRASS TYPE POKéMON.\p"
	.string "I see you have four BADGES already.\p"
	.string "Very well, I think I have the perfect\n"
	.string "team to challenge you.\p"
	.string "Well are you ready?\n"
	.string "Here we come!$"

VerdanturfTown_Gym_Text_ErikaDefeat:
	.string "I must say that victory was a breath of\n"
	.string "fresh air!\p"
	.string "Here, take the FRAGRENCE BADGE!$"

VerdanturfTown_Gym_Text_ErikaPostBattle:
	.string "Blessings for your journeys.$"

VerdanturfTown_Gym_Text_ReceivedErikaBadge:
	.string "{PLAYER} received the FRAGRANCE\n"
	.string "BADGE from ERIKA.$"

VerdanturfTown_Gym_Text_ErikaBadgeInfo:
	.string "With the FRAGRANCE BADGE POKéMON up to\n"
	.string "level 40 obey you diligently.$"

VerdanturfTown_Gym_Text_ExplainErikaItem:
	.string "TM19, contains GIGA DRAIN.\p"
	.string "It heals uses the opponents energy to\n"
	.string "heal it’s user.\p"
	.string "Use it well.$"

VerdanturfTown_Gym_Text_GymGuideAdvice:
	.string "Champ-to-be shhh...\p"
	.string "They say if I’m too loud in here they’ll\n"
	.string "kick me out...\p"
	.string "This ERIKA is a strict lady that uses\n"
	.string "GRASS TYPE POKéMON.\p"
	.string "If you bring a WATER or FLYING TYPE\n"
	.string "you’re sure to lose but FIRE or ICE\l"
	.string "TYPES could be a big help!$"

VerdanturfTown_Gym_Text_GymGuidePostVictory:
	.string "{PLAYER}!\n"
	.string "That was Out-A-This-World!\p"
	.string "I’m sure my hollering helped you battle\n"
	.string "like no one has before!$"

VerdanturfTown_Gym_Text_GymStatue:
	.string "VERDANTURF CITY POKéMON GYM$"

VerdanturfTown_Gym_Text_GymStatueCertified:
	.string "VERDANTURF CITY POKéMON GYM\p"
	.string "ERIKA’S CERTIFIED TRAINERS:\n"
	.string "{PLAYER}$"

