SunyshoreCityGymRoom2_MapScripts::
	.byte 0

@ Treinador do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_masmorra_sinnoh.py)

SunyshoreCityGymRoom2_EventScript_SchoolKidForrest::
	trainerbattle_single TRAINER_SINNOH_SCHOOL_KID_FORREST, SunyshoreCityGymRoom2_Text_SchoolKidForrestIntro, SunyshoreCityGymRoom2_Text_SchoolKidForrestDefeat
	msgbox SunyshoreCityGymRoom2_Text_SchoolKidForrestPost, MSGBOX_AUTOCLOSE
	end

SunyshoreCityGymRoom2_Text_SchoolKidForrestIntro:
	.string "This is the toughest Gym in Sinnoh.\pThat's why I'm here--to learn the\nbest battle techniques around!$"

SunyshoreCityGymRoom2_Text_SchoolKidForrestDefeat:
	.string "...You're tough.$"

SunyshoreCityGymRoom2_Text_SchoolKidForrestPost:
	.string "You just showed me that there's\nstill lots I need to learn.\pThe world of Pokémon is deep!$"

SunyshoreCityGymRoom2_EventScript_GuitaristJerry::
	trainerbattle_single TRAINER_SINNOH_GUITARIST_JERRY, SunyshoreCityGymRoom2_Text_GuitaristJerryIntro, SunyshoreCityGymRoom2_Text_GuitaristJerryDefeat
	msgbox SunyshoreCityGymRoom2_Text_GuitaristJerryPost, MSGBOX_AUTOCLOSE
	end

SunyshoreCityGymRoom2_Text_GuitaristJerryIntro:
	.string "I want to win!\nThat desire I pour into my guitar!\pI want to win!\nThat passion compels my Pokémon!$"

SunyshoreCityGymRoom2_Text_GuitaristJerryDefeat:
	.string "We couldn't win...\nNo encores for us...$"

SunyshoreCityGymRoom2_Text_GuitaristJerryPost:
	.string "The Trainer's desire to win!\pIf you don't lose that, there's\nno limit on what you can become!$"

SunyshoreCityGymRoom2_EventScript_PokeKidMeghan::
	trainerbattle_single TRAINER_SINNOH_POKE_KID_MEGHAN, SunyshoreCityGymRoom2_Text_PokeKidMeghanIntro, SunyshoreCityGymRoom2_Text_PokeKidMeghanDefeat
	msgbox SunyshoreCityGymRoom2_Text_PokeKidMeghanPost, MSGBOX_AUTOCLOSE
	end

SunyshoreCityGymRoom2_Text_PokeKidMeghanIntro:
	.string "Look at the way I'm dressed.\nCan't you see that I'm hardcore?$"

SunyshoreCityGymRoom2_Text_PokeKidMeghanDefeat:
	.string "I was being serious!\nDon't laugh at me! I mean it!$"

SunyshoreCityGymRoom2_Text_PokeKidMeghanPost:
	.string "I dress this way so I can get a feel for\nhow electric Pokémon think.\pWould you like to try, too?$"
