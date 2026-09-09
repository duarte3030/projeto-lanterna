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

SinnohVictoryRoad1F_EventScript_Collector::
	msgbox SinnohVictoryRoad1F_Text_Collector, MSGBOX_NPC
	end

SinnohVictoryRoad1F_Text_Collector:
	.string "Let me size you up...\pAim for the Pokémon League!\nThat's all you should be thinking about.$"

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
SinnohVictoryRoad1F_EventScript_DexArceusDark::
	lockall
	msgbox SinnohVictoryRoad1F_Text_DexArceusDarkIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ARCEUS_DARK, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ARCEUS_DARK, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ARCEUS_DARK
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, SinnohVictoryRoad1F_EventScript_DexArceusDarkSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, SinnohVictoryRoad1F_EventScript_DexArceusDarkSome
	releaseall
	end

SinnohVictoryRoad1F_EventScript_DexArceusDarkSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ARCEUS_DARK
	setflag FLAG_HIDE_DEX_ARCEUS_DARK
	fadescreenswapbuffers FADE_FROM_BLACK
	return

SinnohVictoryRoad1F_Text_DexArceusDarkIntro:
	.string "ARCEUS_DARK appeared!$"

SinnohVictoryRoad1F_EventScript_DexArceusFighting::
	lockall
	msgbox SinnohVictoryRoad1F_Text_DexArceusFightingIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ARCEUS_FIGHTING, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ARCEUS_FIGHTING, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ARCEUS_FIGHTING
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, SinnohVictoryRoad1F_EventScript_DexArceusFightingSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, SinnohVictoryRoad1F_EventScript_DexArceusFightingSome
	releaseall
	end

SinnohVictoryRoad1F_EventScript_DexArceusFightingSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ARCEUS_FIGHTING
	setflag FLAG_HIDE_DEX_ARCEUS_FIGHTING
	fadescreenswapbuffers FADE_FROM_BLACK
	return

SinnohVictoryRoad1F_Text_DexArceusFightingIntro:
	.string "ARCEUS_FIGHTING appeared!$"

SinnohVictoryRoad1F_EventScript_DexArceusGhost::
	lockall
	msgbox SinnohVictoryRoad1F_Text_DexArceusGhostIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ARCEUS_GHOST, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ARCEUS_GHOST, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ARCEUS_GHOST
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, SinnohVictoryRoad1F_EventScript_DexArceusGhostSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, SinnohVictoryRoad1F_EventScript_DexArceusGhostSome
	releaseall
	end

SinnohVictoryRoad1F_EventScript_DexArceusGhostSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ARCEUS_GHOST
	setflag FLAG_HIDE_DEX_ARCEUS_GHOST
	fadescreenswapbuffers FADE_FROM_BLACK
	return

SinnohVictoryRoad1F_Text_DexArceusGhostIntro:
	.string "ARCEUS_GHOST appeared!$"

SinnohVictoryRoad1F_EventScript_DexArceusNormal::
	lockall
	msgbox SinnohVictoryRoad1F_Text_DexArceusNormalIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ARCEUS_NORMAL, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ARCEUS_NORMAL, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ARCEUS_NORMAL
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, SinnohVictoryRoad1F_EventScript_DexArceusNormalSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, SinnohVictoryRoad1F_EventScript_DexArceusNormalSome
	releaseall
	end

SinnohVictoryRoad1F_EventScript_DexArceusNormalSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ARCEUS_NORMAL
	setflag FLAG_HIDE_DEX_ARCEUS_NORMAL
	fadescreenswapbuffers FADE_FROM_BLACK
	return

SinnohVictoryRoad1F_Text_DexArceusNormalIntro:
	.string "ARCEUS_NORMAL appeared!$"

SinnohVictoryRoad1F_EventScript_DexArceusPsychic::
	lockall
	msgbox SinnohVictoryRoad1F_Text_DexArceusPsychicIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ARCEUS_PSYCHIC, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ARCEUS_PSYCHIC, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ARCEUS_PSYCHIC
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, SinnohVictoryRoad1F_EventScript_DexArceusPsychicSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, SinnohVictoryRoad1F_EventScript_DexArceusPsychicSome
	releaseall
	end

SinnohVictoryRoad1F_EventScript_DexArceusPsychicSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ARCEUS_PSYCHIC
	setflag FLAG_HIDE_DEX_ARCEUS_PSYCHIC
	fadescreenswapbuffers FADE_FROM_BLACK
	return

SinnohVictoryRoad1F_Text_DexArceusPsychicIntro:
	.string "ARCEUS_PSYCHIC appeared!$"

@ <<< Dex completa <<<
