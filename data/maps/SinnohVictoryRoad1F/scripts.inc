SinnohVictoryRoad1F_MapScripts::
	.byte 0

@ Treinador do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_masmorra_sinnoh.py)

SinnohVictoryRoad1F_EventScript_PsychicBryce::
	trainerbattle_single TRAINER_SINNOH_PSYCHIC_BRYCE, SinnohVictoryRoad1F_Text_PsychicBryceIntro, SinnohVictoryRoad1F_Text_PsychicBryceDefeat
	msgbox SinnohVictoryRoad1F_Text_PsychicBrycePost, MSGBOX_AUTOCLOSE
	end

SinnohVictoryRoad1F_Text_PsychicBryceIntro:
	.string "I am a Psychic!\nI can see your future!$"

SinnohVictoryRoad1F_Text_PsychicBryceDefeat:
	.string "So be it! I will now divulge what\nI know of your future... Hmm!$"

SinnohVictoryRoad1F_Text_PsychicBrycePost:
	.string "I see it now!\pYou will battle the Elite Four of the\nPokémon League!$"

SinnohVictoryRoad1F_EventScript_BlackBeltMiles::
	trainerbattle_single TRAINER_SINNOH_BLACK_BELT_MILES, SinnohVictoryRoad1F_Text_BlackBeltMilesIntro, SinnohVictoryRoad1F_Text_BlackBeltMilesDefeat
	msgbox SinnohVictoryRoad1F_Text_BlackBeltMilesPost, MSGBOX_AUTOCLOSE
	end

SinnohVictoryRoad1F_Text_BlackBeltMilesIntro:
	.string "My Pokémon knows karate!\nI'm warning you, it's a tough one!$"

SinnohVictoryRoad1F_Text_BlackBeltMilesDefeat:
	.string "I've met my match in strength!$"

SinnohVictoryRoad1F_Text_BlackBeltMilesPost:
	.string "I've made it this far in life using the\nkarate I learned on the Internet!$"

SinnohVictoryRoad1F_EventScript_BirdKeeperHana::
	trainerbattle_single TRAINER_SINNOH_BIRD_KEEPER_HANA, SinnohVictoryRoad1F_Text_BirdKeeperHanaIntro, SinnohVictoryRoad1F_Text_BirdKeeperHanaDefeat
	msgbox SinnohVictoryRoad1F_Text_BirdKeeperHanaPost, MSGBOX_AUTOCLOSE
	end

SinnohVictoryRoad1F_Text_BirdKeeperHanaIntro:
	.string "I keep battling so I can soar\never higher into the skies!$"

SinnohVictoryRoad1F_Text_BirdKeeperHanaDefeat:
	.string "It seems I've been grounded...$"

SinnohVictoryRoad1F_Text_BirdKeeperHanaPost:
	.string "The wings of freedom...\pI know I'll find them if I can win\nmy way through the Pokémon League...$"

SinnohVictoryRoad1F_EventScript_AceTrainerMariah::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_MARIAH, SinnohVictoryRoad1F_Text_AceTrainerMariahIntro, SinnohVictoryRoad1F_Text_AceTrainerMariahDefeat
	msgbox SinnohVictoryRoad1F_Text_AceTrainerMariahPost, MSGBOX_AUTOCLOSE
	end

SinnohVictoryRoad1F_Text_AceTrainerMariahIntro:
	.string "Show me how you've battled to get\nhere! Let's do this!$"

SinnohVictoryRoad1F_Text_AceTrainerMariahDefeat:
	.string "So, that's how you battled...?$"

SinnohVictoryRoad1F_Text_AceTrainerMariahPost:
	.string "Once you emerge from Victory Road,\nthe Pokémon League lies directly\pahead...\pBut many Trainers fail to ever find\ntheir way on Victory Road...$"

SinnohVictoryRoad1F_EventScript_VeteranEdgar::
	trainerbattle_single TRAINER_SINNOH_VETERAN_EDGAR, SinnohVictoryRoad1F_Text_VeteranEdgarIntro, SinnohVictoryRoad1F_Text_VeteranEdgarDefeat
	msgbox SinnohVictoryRoad1F_Text_VeteranEdgarPost, MSGBOX_AUTOCLOSE
	end

SinnohVictoryRoad1F_Text_VeteranEdgarIntro:
	.string "I can sense that your Pokémon have\na lot of trust in you.\pYou and your Pokémon...\nYou seem to be aglow.$"

SinnohVictoryRoad1F_Text_VeteranEdgarDefeat:
	.string "Ah, I understand it now!$"

SinnohVictoryRoad1F_Text_VeteranEdgarPost:
	.string "Neither Pokémon nor people live\nforever.\pBut it is the very frailty of life that\nallows us to shine!$"

SinnohVictoryRoad1F_EventScript_DragonTamerClinton::
	trainerbattle_single TRAINER_SINNOH_DRAGON_TAMER_CLINTON, SinnohVictoryRoad1F_Text_DragonTamerClintonIntro, SinnohVictoryRoad1F_Text_DragonTamerClintonDefeat
	msgbox SinnohVictoryRoad1F_Text_DragonTamerClintonPost, MSGBOX_AUTOCLOSE
	end

SinnohVictoryRoad1F_Text_DragonTamerClintonIntro:
	.string "This is a place where tough Trainers\nnaturally congregate.\pIt's ideal for training!$"

SinnohVictoryRoad1F_Text_DragonTamerClintonDefeat:
	.string "That's why I like it here; I get to\nbattle tough characters like you.$"

SinnohVictoryRoad1F_Text_DragonTamerClintonPost:
	.string "When two roads diverge, you must\nchoose the path less traveled...$"
