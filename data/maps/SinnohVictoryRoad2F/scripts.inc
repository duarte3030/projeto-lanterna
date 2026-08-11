SinnohVictoryRoad2F_MapScripts::
	.byte 0

@ Treinador do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_masmorra_sinnoh.py)

SinnohVictoryRoad2F_EventScript_AceTrainerOmar::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_OMAR, SinnohVictoryRoad2F_Text_AceTrainerOmarIntro, SinnohVictoryRoad2F_Text_AceTrainerOmarDefeat
	msgbox SinnohVictoryRoad2F_Text_AceTrainerOmarPost, MSGBOX_AUTOCLOSE
	end

SinnohVictoryRoad2F_Text_AceTrainerOmarIntro:
	.string "You... One look at you tells me\nyou're a real contender!$"

SinnohVictoryRoad2F_Text_AceTrainerOmarDefeat:
	.string "You're as tough as you look.$"

SinnohVictoryRoad2F_Text_AceTrainerOmarPost:
	.string "One day, people will run to the other\nside of the road when I walk by 'em.\pIt's a goal of mine I'm working on.$"

SinnohVictoryRoad2F_EventScript_AceTrainerSydney::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_SYDNEY, SinnohVictoryRoad2F_Text_AceTrainerSydneyIntro, SinnohVictoryRoad2F_Text_AceTrainerSydneyDefeat
	msgbox SinnohVictoryRoad2F_Text_AceTrainerSydneyPost, MSGBOX_AUTOCLOSE
	end

SinnohVictoryRoad2F_Text_AceTrainerSydneyIntro:
	.string "This total stranger'll be a good way\nto see if I have what it takes to own\pthe Pokémon League's Elite Four!$"

SinnohVictoryRoad2F_Text_AceTrainerSydneyDefeat:
	.string "That battle just now must make you\ntougher than everyone in the world.$"

SinnohVictoryRoad2F_Text_AceTrainerSydneyPost:
	.string "It doesn't appear as if anyone could\neven try to stand against your might.\pThe Elite Four should just surrender.$"

SinnohVictoryRoad2F_EventScript_VeteranClayton::
	trainerbattle_single TRAINER_SINNOH_VETERAN_CLAYTON, SinnohVictoryRoad2F_Text_VeteranClaytonIntro, SinnohVictoryRoad2F_Text_VeteranClaytonDefeat
	msgbox SinnohVictoryRoad2F_Text_VeteranClaytonPost, MSGBOX_AUTOCLOSE
	end

SinnohVictoryRoad2F_Text_VeteranClaytonIntro:
	.string "Let me see how well your Pokémon can\nbattle!$"

SinnohVictoryRoad2F_Text_VeteranClaytonDefeat:
	.string "Brilliant!$"

SinnohVictoryRoad2F_Text_VeteranClaytonPost:
	.string "Rather than navigating Victory Road,\nI have a much better time putting\pyoung Trainers like you to the test.$"

SinnohVictoryRoad2F_EventScript_DoubleTeamAlAndKay::
	trainerbattle_double TRAINER_SINNOH_DOUBLE_TEAM_AL_AND_KAY, SinnohVictoryRoad2F_Text_DoubleTeamAlAndKayIntro, SinnohVictoryRoad2F_Text_DoubleTeamAlAndKayDefeat, SinnohVictoryRoad2F_Text_DoubleTeamAlAndKayNoPartner
	msgbox SinnohVictoryRoad2F_Text_DoubleTeamAlAndKayPost, MSGBOX_AUTOCLOSE
	end

SinnohVictoryRoad2F_Text_DoubleTeamAlAndKayIntro:
	.string "Al: I intend to perfect my Double\nBattle technique.\pThat will make me better all around.$"

SinnohVictoryRoad2F_Text_DoubleTeamAlAndKayDefeat:
	.string "Al: You! You're an expert\ndouble battler, too!$"

SinnohVictoryRoad2F_Text_DoubleTeamAlAndKayPost:
	.string "Al: Your mastery over several\nPokémon at once...\pYou're a remarkable Trainer!$"

SinnohVictoryRoad2F_Text_DoubleTeamAlAndKayNoPartner:
	.string "Al: You have but one Pokémon?\pI would say that you are taking\nVictory Road too lightly, kid.$"
