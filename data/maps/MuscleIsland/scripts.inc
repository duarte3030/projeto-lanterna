@ MuscleIsland: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 27.112) por dev_scripts/copia_planta_ex.py.

MuscleIsland_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 27.112), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
MuscleIsland_EventScript_ExTrainer0::
	trainerbattle_single TRAINER_HOENNEX_MUSCLE_ISLAND_LARRY, MuscleIsland_Text_ExTrainer0Intro, MuscleIsland_Text_ExTrainer0Defeat
	msgbox MuscleIsland_Text_ExTrainer0PostBattle, MSGBOX_AUTOCLOSE
	end

MuscleIsland_Text_ExTrainer0Intro:
	.string "Well hello there!\p"
	.string "I’m the Big Kahuna of Muscle Island!\p"
	.string "You can call me Livin’ Large Larry!\p"
	.string "Tell me kiddo,\n"
	.string "are you ready to get the main even\l"
	.string "underway!$"

MuscleIsland_Text_ExTrainer0Defeat:
	.string "Ka-Blamo!\n"
	.string "That was one heck of a show!\p"
	.string "I guess you’re the new Big Kahuna!$"

MuscleIsland_Text_ExTrainer0PostBattle:
	.string "Look everyone, it’s the Big Kahuna of\n"
	.string "Muscle Island, the great {PLAYER}!$"

MuscleIsland_EventScript_ExTrainer1::
	trainerbattle_single TRAINER_HOENNEX_MUSCLE_ISLAND_SHAKIRA, MuscleIsland_Text_ExTrainer1Intro, MuscleIsland_Text_ExTrainer1Defeat
	msgbox MuscleIsland_Text_ExTrainer1PostBattle, MSGBOX_AUTOCLOSE
	end

MuscleIsland_Text_ExTrainer1Intro:
	.string "I’ve done 500 burpees a day, I’m ready!$"

MuscleIsland_Text_ExTrainer1Defeat:
	.string "I wasn’t ready!$"

MuscleIsland_Text_ExTrainer1PostBattle:
	.string "Tomorrow I’ll do even more burpees$"

MuscleIsland_EventScript_ExTrainer2::
	trainerbattle_single TRAINER_HOENNEX_MUSCLE_ISLAND_BRENDEN, MuscleIsland_Text_ExTrainer2Intro, MuscleIsland_Text_ExTrainer2Defeat
	msgbox MuscleIsland_Text_ExTrainer2PostBattle, MSGBOX_AUTOCLOSE
	end

MuscleIsland_Text_ExTrainer2Intro:
	.string "Watch me flex my muscles!$"

MuscleIsland_Text_ExTrainer2Defeat:
	.string "Now’s that’s a show!$"

MuscleIsland_Text_ExTrainer2PostBattle:
	.string "You’re too young to lift weights!$"

MuscleIsland_EventScript_ExTrainer3::
	trainerbattle_single TRAINER_HOENNEX_MUSCLE_ISLAND_DARRIUS, MuscleIsland_Text_ExTrainer3Intro, MuscleIsland_Text_ExTrainer3Defeat
	msgbox MuscleIsland_Text_ExTrainer3PostBattle, MSGBOX_AUTOCLOSE
	end

MuscleIsland_Text_ExTrainer3Intro:
	.string "Let’s move some rubble!$"

MuscleIsland_Text_ExTrainer3Defeat:
	.string "Rahahahaha!$"

MuscleIsland_Text_ExTrainer3PostBattle:
	.string "How much can your POKéMON lift?$"

MuscleIsland_EventScript_ExTrainer4::
	trainerbattle_single TRAINER_HOENNEX_MUSCLE_ISLAND_QUINN, MuscleIsland_Text_ExTrainer4Intro, MuscleIsland_Text_ExTrainer4Defeat
	msgbox MuscleIsland_Text_ExTrainer4PostBattle, MSGBOX_AUTOCLOSE
	end

MuscleIsland_Text_ExTrainer4Intro:
	.string "I’m concentrating!$"

MuscleIsland_Text_ExTrainer4Defeat:
	.string "You broke my concentration!$"

MuscleIsland_Text_ExTrainer4PostBattle:
	.string "I must return to my mediation.$"

MuscleIsland_EventScript_ExTrainer5::
	trainerbattle_single TRAINER_HOENNEX_MUSCLE_ISLAND_DON, MuscleIsland_Text_ExTrainer5Intro, MuscleIsland_Text_ExTrainer5Defeat
	msgbox MuscleIsland_Text_ExTrainer5PostBattle, MSGBOX_AUTOCLOSE
	end

MuscleIsland_Text_ExTrainer5Intro:
	.string "Welcome to Muscle Island kid!\p"
	.string "Think you got the strength to succeed?$"

MuscleIsland_Text_ExTrainer5Defeat:
	.string "Now that’s power!$"

MuscleIsland_Text_ExTrainer5PostBattle:
	.string "Come lift weights with us kid!$"

MuscleIsland_EventScript_ExTrainer6::
	trainerbattle_single TRAINER_HOENNEX_MUSCLE_ISLAND_FRANK, MuscleIsland_Text_ExTrainer6Intro, MuscleIsland_Text_ExTrainer6Defeat
	msgbox MuscleIsland_Text_ExTrainer6PostBattle, MSGBOX_AUTOCLOSE
	end

MuscleIsland_Text_ExTrainer6Intro:
	.string "My POKéMON’s can knock down oak trees!$"

MuscleIsland_Text_ExTrainer6Defeat:
	.string "My POKéMON weren’t strong enough!$"

MuscleIsland_Text_ExTrainer6PostBattle:
	.string "How many push-ups did you do today?$"

MuscleIsland_EventScript_ExTrainer10::
	trainerbattle_single TRAINER_HOENNEX_MUSCLE_ISLAND_ROCKY, MuscleIsland_Text_ExTrainer10Intro, MuscleIsland_Text_ExTrainer10Defeat
	msgbox MuscleIsland_Text_ExTrainer10PostBattle, MSGBOX_AUTOCLOSE
	end

MuscleIsland_Text_ExTrainer10Intro:
	.string "Hi-Ya!$"

MuscleIsland_Text_ExTrainer10Defeat:
	.string "Wha-Whua$"

MuscleIsland_Text_ExTrainer10PostBattle:
	.string "Yow!$"

MuscleIsland_EventScript_ExNpc11::
	msgbox MuscleIsland_Text_ExNpc11, MSGBOX_NPC
	end

MuscleIsland_Text_ExNpc11:
	.string "I came here to get stronger...\p"
	.string "There’s no food or fresh water here, how\n"
	.string "can I train without that...\p"
	.string "These people are crazy...$"

MuscleIsland_EventScript_ExNpc12::
	msgbox MuscleIsland_Text_ExNpc12, MSGBOX_NPC
	end

MuscleIsland_Text_ExNpc12:
	.string "Huff, huff...\p"
	.string "We all came here to learn from the Big\n"
	.string "Kahuna!$"

MuscleIsland_EventScript_ExSign0::
	msgbox MuscleIsland_Text_ExSign0, MSGBOX_SIGN
	end

MuscleIsland_Text_ExSign0:
	.string "Welcome to MUSCLE ISLAND.\n"
	.string "Kahuna led paradise for trainers!$"

