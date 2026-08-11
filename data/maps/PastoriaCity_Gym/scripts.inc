@ Ginasio de Sinnoh com interior reaproveitado de Hoenn.

PastoriaCity_Gym_MapScripts::
	.byte 0

PastoriaCity_Gym_EventScript_Leader::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_SINNOH_4, PastoriaCity_Gym_EventScript_JaVenceu
	msgbox PastoriaCity_Gym_Text_Intro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_SINNOH_LEADER_WAKE, PastoriaCity_Gym_Text_Defeat
	msgbox PastoriaCity_Gym_Text_Post, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_SINNOH_4
	release
	end

PastoriaCity_Gym_EventScript_JaVenceu::
	msgbox PastoriaCity_Gym_Text_JaVenceu, MSGBOX_DEFAULT
	release
	end

PastoriaCity_Gym_Text_Intro:
	.string "...$"

PastoriaCity_Gym_Text_Defeat:
	.string "Hunwah!\nIt's gone and ended!How will I say this... I want more!\nI wanted to battle a lot more!$"

PastoriaCity_Gym_Text_Post:
	.string "...$"

PastoriaCity_Gym_Text_JaVenceu:
	.string "The FEN BADGE is already yours.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

PastoriaCity_Gym_EventScript_Npc1::
	msgbox PastoriaCity_Gym_Text_Npc1, MSGBOX_NPC
	end

PastoriaCity_Gym_Text_Npc1:
	.string "The Gym Leader Wake... Uh, I mean\nCrasher Wake, is a master of\pWater-type Pokémon.\pI'd say you've got guts if you try\nto face down Water types with Fire-\por Ground-type Pokémon!\pBut that part I'll leave up to you!\nGo and have some good battles!$"

@ Treinador do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_masmorra_sinnoh.py)

PastoriaCity_Gym_EventScript_TuberJacky::
	trainerbattle_single TRAINER_SINNOH_TUBER_JACKY, PastoriaCity_Gym_Text_TuberJackyIntro, PastoriaCity_Gym_Text_TuberJackyDefeat
	msgbox PastoriaCity_Gym_Text_TuberJackyPost, MSGBOX_AUTOCLOSE
	end

PastoriaCity_Gym_Text_TuberJackyIntro:
	.string "My body isn't the only thing I\nwork on toughening up here.\pI also work on my Pokémon and my\nspirit!$"

PastoriaCity_Gym_Text_TuberJackyDefeat:
	.string "Wow, Trainer! You just might be\ntougher than our Gym Leader!$"

PastoriaCity_Gym_Text_TuberJackyPost:
	.string "Maybe I'll do like Wake,\pI mean, Crasher Wake, and wear\nthe same kind of mask.$"

PastoriaCity_Gym_EventScript_SailorDamian::
	trainerbattle_single TRAINER_SINNOH_SAILOR_DAMIAN, PastoriaCity_Gym_Text_SailorDamianIntro, PastoriaCity_Gym_Text_SailorDamianDefeat
	msgbox PastoriaCity_Gym_Text_SailorDamianPost, MSGBOX_AUTOCLOSE
	end

PastoriaCity_Gym_Text_SailorDamianIntro:
	.string "I've been around the world, going from\nplace to place training Pokémon.\pIt's this Gym I've chosen to make my\nhome!\pYou can bet it's tough!$"

PastoriaCity_Gym_Text_SailorDamianDefeat:
	.string "You!\nYou're truly top-class tough!$"

PastoriaCity_Gym_Text_SailorDamianPost:
	.string "If you were to go around the world,\nI'm sure you'd meet tougher Pokémon.$"

PastoriaCity_Gym_EventScript_TuberCaitlyn::
	trainerbattle_single TRAINER_SINNOH_TUBER_CAITLYN, PastoriaCity_Gym_Text_TuberCaitlynIntro, PastoriaCity_Gym_Text_TuberCaitlynDefeat
	msgbox PastoriaCity_Gym_Text_TuberCaitlynPost, MSGBOX_AUTOCLOSE
	end

PastoriaCity_Gym_Text_TuberCaitlynIntro:
	.string "I want to become a strong Trainer\nlike Crasher Wake!$"

PastoriaCity_Gym_Text_TuberCaitlynDefeat:
	.string "Groan...\nYou're too much.$"

PastoriaCity_Gym_Text_TuberCaitlynPost:
	.string "Maybe I'll do like Wake...\pI mean, Crasher Wake, and use\nthe same kinds of Pokémon.$"

PastoriaCity_Gym_EventScript_SailorSamson::
	trainerbattle_single TRAINER_SINNOH_SAILOR_SAMSON, PastoriaCity_Gym_Text_SailorSamsonIntro, PastoriaCity_Gym_Text_SailorSamsonDefeat
	msgbox PastoriaCity_Gym_Text_SailorSamsonPost, MSGBOX_AUTOCLOSE
	end

PastoriaCity_Gym_Text_SailorSamsonIntro:
	.string "Like the raging sea, I crash down\nand wash away everything before me!\pThat's just how I roll!$"

PastoriaCity_Gym_Text_SailorSamsonDefeat:
	.string "That wave didn't even wash\nmy hands...$"

PastoriaCity_Gym_Text_SailorSamsonPost:
	.string "I'm now becalmed like a waveless\nsea...$"

PastoriaCity_Gym_EventScript_FishermanErick::
	trainerbattle_single TRAINER_SINNOH_FISHERMAN_ERICK, PastoriaCity_Gym_Text_FishermanErickIntro, PastoriaCity_Gym_Text_FishermanErickDefeat
	msgbox PastoriaCity_Gym_Text_FishermanErickPost, MSGBOX_AUTOCLOSE
	end

PastoriaCity_Gym_Text_FishermanErickIntro:
	.string "I've landed the most fish Pokémon\nin the world. I'm next!$"

PastoriaCity_Gym_Text_FishermanErickDefeat:
	.string "Being number one in the world doesn't\nmean a thing...$"

PastoriaCity_Gym_Text_FishermanErickPost:
	.string "I figure I got too wrapped up in\nfishing and neglected training.$"

PastoriaCity_Gym_EventScript_FishermanWalter::
	trainerbattle_single TRAINER_SINNOH_FISHERMAN_WALTER, PastoriaCity_Gym_Text_FishermanWalterIntro, PastoriaCity_Gym_Text_FishermanWalterDefeat
	msgbox PastoriaCity_Gym_Text_FishermanWalterPost, MSGBOX_AUTOCLOSE
	end

PastoriaCity_Gym_Text_FishermanWalterIntro:
	.string "I wield the stupendous power of water!\nDon't think you can win!$"

PastoriaCity_Gym_Text_FishermanWalterDefeat:
	.string "But the kid wins anyway!\nI'm just bowled over!$"

PastoriaCity_Gym_Text_FishermanWalterPost:
	.string "The water rising and falling is tricky,\nbut don't let it annoy you.\pIf you lose sight of yourself, that's\nwhen you're set to lose.$"
