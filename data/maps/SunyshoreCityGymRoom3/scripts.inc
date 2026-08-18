SunyshoreCityGymRoom3_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
SunyshoreCityGymRoom3_EventScript_BottomButtons::
	@ TODO S?: cena da fonte, rotulo SunyshoreGymRoom3_BottomButtons
	end

SunyshoreCityGymRoom3_EventScript_TopButtons::
	@ TODO S?: cena da fonte, rotulo SunyshoreGymRoom3_TopButtons
	end

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

@ Treinador do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_masmorra_sinnoh.py)

SunyshoreCityGymRoom3_EventScript_AceTrainerDestiny::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_DESTINY, SunyshoreCityGymRoom3_Text_AceTrainerDestinyIntro, SunyshoreCityGymRoom3_Text_AceTrainerDestinyDefeat
	msgbox SunyshoreCityGymRoom3_Text_AceTrainerDestinyPost, MSGBOX_AUTOCLOSE
	end

SunyshoreCityGymRoom3_Text_AceTrainerDestinyIntro:
	.string "I'm not just looking for tough\nTrainers to battle.\pI've been battling here because\nI want to feel the rush!$"

SunyshoreCityGymRoom3_Text_AceTrainerDestinyDefeat:
	.string "Your power is thrilling...\nI'm thrilled down to my toes!$"

SunyshoreCityGymRoom3_Text_AceTrainerDestinyPost:
	.string "I'm so glad that there are Pokémon!\pThere isn't much else that gives me\nthe thrill that Pokémon do!$"

SunyshoreCityGymRoom3_EventScript_GuitaristPreston::
	trainerbattle_single TRAINER_SINNOH_GUITARIST_PRESTON, SunyshoreCityGymRoom3_Text_GuitaristPrestonIntro, SunyshoreCityGymRoom3_Text_GuitaristPrestonDefeat
	msgbox SunyshoreCityGymRoom3_Text_GuitaristPrestonPost, MSGBOX_AUTOCLOSE
	end

SunyshoreCityGymRoom3_Text_GuitaristPrestonIntro:
	.string "Spark!\pThis is what our Gym Leader did\nto the Gym out of boredom!$"

SunyshoreCityGymRoom3_Text_GuitaristPrestonDefeat:
	.string "Spark...$"

SunyshoreCityGymRoom3_Text_GuitaristPrestonPost:
	.string "We were lacking energy...\pNo, we lacked more than that. We\ndidn't want the win enough.$"

SunyshoreCityGymRoom3_EventScript_GuitaristLonnie::
	trainerbattle_single TRAINER_SINNOH_GUITARIST_LONNIE, SunyshoreCityGymRoom3_Text_GuitaristLonnieIntro, SunyshoreCityGymRoom3_Text_GuitaristLonnieDefeat
	msgbox SunyshoreCityGymRoom3_Text_GuitaristLonniePost, MSGBOX_AUTOCLOSE
	end

SunyshoreCityGymRoom3_Text_GuitaristLonnieIntro:
	.string "Whether you're a Trainer or a\nGuitarist, it takes dedication to\pimprove your mad skills!$"

SunyshoreCityGymRoom3_Text_GuitaristLonnieDefeat:
	.string "My skills seem to have let me down.\nI must have been out of tune!$"

SunyshoreCityGymRoom3_Text_GuitaristLonniePost:
	.string "The way you battle, I can feel the\nvery heart of rock and roll.\pTell me, are you maybe a fan of\nrocking out?$"

SunyshoreCityGymRoom3_EventScript_AceTrainerZachery::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_ZACHERY, SunyshoreCityGymRoom3_Text_AceTrainerZacheryIntro, SunyshoreCityGymRoom3_Text_AceTrainerZacheryDefeat
	msgbox SunyshoreCityGymRoom3_Text_AceTrainerZacheryPost, MSGBOX_AUTOCLOSE
	end

SunyshoreCityGymRoom3_Text_AceTrainerZacheryIntro:
	.string "Wow! I'm surprised you've come this\nfar, but you'll have to turn back.\pThere isn't any chance that you\ncould ever beat me!$"

SunyshoreCityGymRoom3_Text_AceTrainerZacheryDefeat:
	.string "What makes your Pokémon\nso special?$"

SunyshoreCityGymRoom3_Text_AceTrainerZacheryPost:
	.string "As a challenger, you're one tough\nTrainer.$"
