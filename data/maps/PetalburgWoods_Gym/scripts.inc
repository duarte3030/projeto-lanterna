@ PetalburgWoods_Gym: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 19.2) por dev_scripts/copia_planta_ex.py.

PetalburgWoods_Gym_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 19.2), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
PetalburgWoods_Gym_EventScript_ExTrainer1::
	trainerbattle_single TRAINER_HOENNEX_PETALBURG_WOODS_GYM_NIKO, PetalburgWoods_Gym_Text_ExTrainer1Intro, PetalburgWoods_Gym_Text_ExTrainer1Defeat
	msgbox PetalburgWoods_Gym_Text_ExTrainer1PostBattle, MSGBOX_AUTOCLOSE
	end

PetalburgWoods_Gym_Text_ExTrainer1Intro:
	.string "HIAH!\p"
	.string "Did I spook ya?$"

PetalburgWoods_Gym_Text_ExTrainer1Defeat:
	.string "EEK!\n"
	.string "You’re scary strong!$"

PetalburgWoods_Gym_Text_ExTrainer1PostBattle:
	.string "These logs are great for hiding behind.$"

PetalburgWoods_Gym_EventScript_ExTrainer2::
	trainerbattle_single TRAINER_HOENNEX_PETALBURG_WOODS_GYM_WIGGLES, PetalburgWoods_Gym_Text_ExTrainer2Intro, PetalburgWoods_Gym_Text_ExTrainer2Defeat
	msgbox PetalburgWoods_Gym_Text_ExTrainer2PostBattle, MSGBOX_AUTOCLOSE
	end

PetalburgWoods_Gym_Text_ExTrainer2Intro:
	.string "I’m so excited!\n"
	.string "This is my first match as a GYM TRAINER!$"

PetalburgWoods_Gym_Text_ExTrainer2Defeat:
	.string "Wow what a match!$"

PetalburgWoods_Gym_Text_ExTrainer2PostBattle:
	.string "One day I’ll challenge SAM!$"

PetalburgWoods_Gym_EventScript_ExTrainer3::
	trainerbattle_single TRAINER_HOENNEX_PETALBURG_WOODS_GYM_CLYDE, PetalburgWoods_Gym_Text_ExTrainer3Intro, PetalburgWoods_Gym_Text_ExTrainer3Defeat
	msgbox PetalburgWoods_Gym_Text_ExTrainer3PostBattle, MSGBOX_AUTOCLOSE
	end

PetalburgWoods_Gym_Text_ExTrainer3Intro:
	.string "You’ve come far enough!$"

PetalburgWoods_Gym_Text_ExTrainer3Defeat:
	.string "What?$"

PetalburgWoods_Gym_Text_ExTrainer3PostBattle:
	.string "We weren’t enough...$"

PetalburgWoods_Gym_EventScript_ExTrainer4::
	trainerbattle_single TRAINER_HOENNEX_PETALBURG_WOODS_GYM_MORGAN, PetalburgWoods_Gym_Text_ExTrainer4Intro, PetalburgWoods_Gym_Text_ExTrainer4Defeat
	msgbox PetalburgWoods_Gym_Text_ExTrainer4PostBattle, MSGBOX_AUTOCLOSE
	end

PetalburgWoods_Gym_Text_ExTrainer4Intro:
	.string "Sorry buddy,\n"
	.string "you’re not making it to SAM today!$"

PetalburgWoods_Gym_Text_ExTrainer4Defeat:
	.string "My bugs weren’t enough!$"

PetalburgWoods_Gym_Text_ExTrainer4PostBattle:
	.string "Hey don’t tell him I let you get by.$"

PetalburgWoods_Gym_EventScript_ExTrainer6::
	trainerbattle_single TRAINER_HOENNEX_PETALBURG_WOODS_GYM_CLYVE, PetalburgWoods_Gym_Text_ExTrainer6Intro, PetalburgWoods_Gym_Text_ExTrainer6Defeat
	msgbox PetalburgWoods_Gym_Text_ExTrainer6PostBattle, MSGBOX_AUTOCLOSE
	end

PetalburgWoods_Gym_Text_ExTrainer6Intro:
	.string "But we’ll stop you!$"

PetalburgWoods_Gym_Text_ExTrainer6Defeat:
	.string "How?$"

PetalburgWoods_Gym_Text_ExTrainer6PostBattle:
	.string "Go ahead.$"


@ Líder, guia e estátuas do ginásio do EX (mapa 19.2), reescritos no nosso formato a partir do
@ texto da ROM (lote G1 da onda 2). A vitória é goto_if_defeated no líder; a insígnia é FLAG_INSIGNIA_HOENN_9.

PetalburgWoods_Gym_EventScript_Sam::
	trainerbattle_single TRAINER_HOENNEX_SAM, PetalburgWoods_Gym_Text_SamIntro, PetalburgWoods_Gym_Text_SamDefeat, PetalburgWoods_Gym_EventScript_SamDefeated, NO_MUSIC
	goto_if_unset FLAG_HOENNEX_RECEIVED_HM_CUT_SAM, PetalburgWoods_Gym_EventScript_GiveSamItem
	msgbox PetalburgWoods_Gym_Text_SamPostBattle, MSGBOX_DEFAULT
	release
	end

PetalburgWoods_Gym_EventScript_SamDefeated::
	message PetalburgWoods_Gym_Text_ReceivedSamBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox PetalburgWoods_Gym_Text_SamBadgeInfo, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_HOENN_9
	settrainerflag TRAINER_HOENNEX_PETALBURG_WOODS_GYM_NIKO
	settrainerflag TRAINER_HOENNEX_PETALBURG_WOODS_GYM_WIGGLES
	settrainerflag TRAINER_HOENNEX_PETALBURG_WOODS_GYM_CLYDE
	settrainerflag TRAINER_HOENNEX_PETALBURG_WOODS_GYM_MORGAN
	settrainerflag TRAINER_HOENNEX_PETALBURG_WOODS_GYM_CLYVE
	call_if_eq VAR_PETALBURG_GYM_STATE, 6, Common_EventScript_ReadyPetalburgGymForBattle
	goto PetalburgWoods_Gym_EventScript_GiveSamItem
	end

PetalburgWoods_Gym_EventScript_GiveSamItem::
	giveitem ITEM_HM_CUT
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_HOENNEX_RECEIVED_HM_CUT_SAM
	msgbox PetalburgWoods_Gym_Text_ExplainSamItem, MSGBOX_DEFAULT
	release
	end

PetalburgWoods_Gym_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_defeated TRAINER_HOENNEX_SAM, PetalburgWoods_Gym_EventScript_GymGuidePostVictory
	msgbox PetalburgWoods_Gym_Text_GymGuideAdvice, MSGBOX_DEFAULT
	release
	end

PetalburgWoods_Gym_EventScript_GymGuidePostVictory::
	msgbox PetalburgWoods_Gym_Text_GymGuidePostVictory, MSGBOX_DEFAULT
	release
	end

PetalburgWoods_Gym_EventScript_LeftGymStatue::
	lockall
	goto_if_set FLAG_INSIGNIA_HOENN_9, PetalburgWoods_Gym_EventScript_GymStatueCertified
	goto PetalburgWoods_Gym_EventScript_GymStatue
	end

PetalburgWoods_Gym_EventScript_RightGymStatue::
	lockall
	goto_if_set FLAG_INSIGNIA_HOENN_9, PetalburgWoods_Gym_EventScript_GymStatueCertified
	goto PetalburgWoods_Gym_EventScript_GymStatue
	end

PetalburgWoods_Gym_EventScript_GymStatueCertified::
	msgbox PetalburgWoods_Gym_Text_GymStatueCertified, MSGBOX_DEFAULT
	releaseall
	end

PetalburgWoods_Gym_EventScript_GymStatue::
	msgbox PetalburgWoods_Gym_Text_GymStatue, MSGBOX_DEFAULT
	releaseall
	end

PetalburgWoods_Gym_Text_SamIntro:
	.string "Greetings novice.\p"
	.string "I hail from a distant land where I\n"
	.string "relentlessly trained my BUG TYPE\l"
	.string "POKéMON in a forest much like this one.\p"
	.string "But when KOGA left his GYM, the INDIGO\n"
	.string "LEAGUE chose hs weak daughter over me.\p"
	.string "My POKéMON and I left but were welcomed\n"
	.string "here in HOENN.\p"
	.string "Prepare yourself novice, or taste my\n"
	.string "blade!$"

PetalburgWoods_Gym_Text_SamDefeat:
	.string "Well well well...\p"
	.string "You actually beat my swarm of BUG TYPE\n"
	.string "POKéMON.\p"
	.string "I wonder if you’ll go all the way. But\n"
	.string "thats for later. Now, because of your\l"
	.string "strength, you’ve earned the POKéMON\l"
	.string "LEAGUE BUZZ BADGE!$"

PetalburgWoods_Gym_Text_SamPostBattle:
	.string "Remember to visit MR. BRINEY on ROUTE\n"
	.string "104.$"

PetalburgWoods_Gym_Text_ReceivedSamBadge:
	.string "{PLAYER} received the BUZZ BADGE\n"
	.string "from SAM.$"

PetalburgWoods_Gym_Text_SamBadgeInfo:
	.string "The BUZZ BADGE allows your POKéMON to\n"
	.string "CUT down small trees.\p"
	.string "Now take this.$"

PetalburgWoods_Gym_Text_ExplainSamItem:
	.string "HM01, contains CUT.\p"
	.string "It make your POKéMON able to cut\n"
	.string "through small bushes.\p"
	.string "I have long used these bushes to hide\n"
	.string "my domain, but you have earned the\l"
	.string "right to enter freely!\p"
	.string "If you want to continue the GYM\n"
	.string "CHALLENGE, you will need to go to\l"
	.string "DEWFORD TOWN.\p"
	.string "There is a man named MR. BRINEY that\n"
	.string "lives in an humble shack on the coast of\l"
	.string "ROUTE 104.\p"
	.string "I’ll tell him to help you on your path.$"

PetalburgWoods_Gym_Text_GymGuideAdvice:
	.string "Yo, how’s it going\n"
	.string "CHAMP-IN-THE-MAKING!\p"
	.string "Listen closely and I’ll give you the\n"
	.string "run-down on this place.\p"
	.string "LEADER SAM is a no nonsense BUG TYPE\n"
	.string "trainer, and, even though you can’t\l"
	.string "seem ’em, this GYM is full of traps!\p"
	.string "Watch your path, because there are\n"
	.string "trainers hidden in the walls that will\l"
	.string "challenge you if you walk past em.\p"
	.string "As for SAM, be careful using GRASS TYPE\n"
	.string "POKéMON against him. His BUGs will tear\l"
	.string "them up.\p"
	.string "Instead use a FLYING TYPE or FIRE TYPE\n"
	.string "POKéMON. If you do you’ll be sure to win!\p"
	.string "Go get ’em CHAMP-IN-THE-MAKING$"

PetalburgWoods_Gym_Text_GymGuidePostVictory:
	.string "Outstanding!\n"
	.string "Another amazing battle!\p"
	.string "You battled out there like a master!\p"
	.string "With the two of us you’ll have sixteen\n"
	.string "badges in no time!\p"
	.string "See you soon {PLAYER}!$"

PetalburgWoods_Gym_Text_GymStatue:
	.string "PETALBURG WOODS POKéMON GYM$"

PetalburgWoods_Gym_Text_GymStatueCertified:
	.string "PETALBURG WOODS POKéMON GYM\p"
	.string "SAM’S CERTIFIED TRAINERS:\n"
	.string "{PLAYER}$"

