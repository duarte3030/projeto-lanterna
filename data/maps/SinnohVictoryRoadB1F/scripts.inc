SinnohVictoryRoadB1F_MapScripts::
	.byte 0

@ Treinador do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_masmorra_sinnoh.py)

SinnohVictoryRoadB1F_EventScript_DoubleTeamJoAndPat::
	trainerbattle_double TRAINER_SINNOH_DOUBLE_TEAM_JO_AND_PAT, SinnohVictoryRoadB1F_Text_DoubleTeamJoAndPatIntro, SinnohVictoryRoadB1F_Text_DoubleTeamJoAndPatDefeat, SinnohVictoryRoadB1F_Text_DoubleTeamJoAndPatNoPartner
	msgbox SinnohVictoryRoadB1F_Text_DoubleTeamJoAndPatPost, MSGBOX_AUTOCLOSE
	end

SinnohVictoryRoadB1F_Text_DoubleTeamJoAndPatIntro:
	.string "Pat: It's a doubles team of aces!\nWe're gonna overwhelm you!$"

SinnohVictoryRoadB1F_Text_DoubleTeamJoAndPatDefeat:
	.string "Pat: You and your Pokémon will gain\npower by helping each other out.$"

SinnohVictoryRoadB1F_Text_DoubleTeamJoAndPatPost:
	.string "Pat: The combination of you and\nyour awesome Pokémon...\pIt's the ultimate tag team!$"

SinnohVictoryRoadB1F_Text_DoubleTeamJoAndPatNoPartner:
	.string "Pat: If you don't mind, we're hoping\nfor some two-on-two battle action.$"

SinnohVictoryRoadB1F_EventScript_DragonTamerOndrej::
	trainerbattle_single TRAINER_SINNOH_DRAGON_TAMER_ONDREJ, SinnohVictoryRoadB1F_Text_DragonTamerOndrejIntro, SinnohVictoryRoadB1F_Text_DragonTamerOndrejDefeat
	msgbox SinnohVictoryRoadB1F_Text_DragonTamerOndrejPost, MSGBOX_AUTOCLOSE
	end

SinnohVictoryRoadB1F_Text_DragonTamerOndrejIntro:
	.string "I take Pokémon that are tough to begin\nwith and toughen them up even more.\pYou can help me!$"

SinnohVictoryRoadB1F_Text_DragonTamerOndrejDefeat:
	.string "There's no way I could have won!$"

SinnohVictoryRoadB1F_Text_DragonTamerOndrejPost:
	.string "How should I teach the most powerful\nof the Dragon-type moves...?$"

SinnohVictoryRoadB1F_EventScript_PsychicValencia::
	trainerbattle_single TRAINER_SINNOH_PSYCHIC_VALENCIA, SinnohVictoryRoadB1F_Text_PsychicValenciaIntro, SinnohVictoryRoadB1F_Text_PsychicValenciaDefeat
	msgbox SinnohVictoryRoadB1F_Text_PsychicValenciaPost, MSGBOX_AUTOCLOSE
	end

SinnohVictoryRoadB1F_Text_PsychicValenciaIntro:
	.string "I am a Psychic!\nI can see your past!$"

SinnohVictoryRoadB1F_Text_PsychicValenciaDefeat:
	.string "Your past...\nYou've been through a lot...$"

SinnohVictoryRoadB1F_Text_PsychicValenciaPost:
	.string "Let me guess.\nHave you met any legendary Pokémon?$"

SinnohVictoryRoadB1F_EventScript_AceTrainerHenry::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_HENRY, SinnohVictoryRoadB1F_Text_AceTrainerHenryIntro, SinnohVictoryRoadB1F_Text_AceTrainerHenryDefeat
	msgbox SinnohVictoryRoadB1F_Text_AceTrainerHenryPost, MSGBOX_AUTOCLOSE
	end

SinnohVictoryRoadB1F_Text_AceTrainerHenryIntro:
	.string "Victory Road... Somehow, it feels as\nif my journey is now coming to an end.\pBut, before the final chapter is\nwritten, I must pen your defeat!$"

SinnohVictoryRoadB1F_Text_AceTrainerHenryDefeat:
	.string "That wasn't how I planned the final\nchapter to go in my writing class...$"

SinnohVictoryRoadB1F_Text_AceTrainerHenryPost:
	.string "If you don't give up, you can reach\nyour goal.\pThat perseverance is what's important\nto Trainers. That's in my book, too.$"
