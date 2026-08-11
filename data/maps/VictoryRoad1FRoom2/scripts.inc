VictoryRoad1FRoom2_MapScripts::
	.byte 0

@ Treinador do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_masmorra_sinnoh.py)

VictoryRoad1FRoom2_EventScript_AceTrainerMicah::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_MICAH, VictoryRoad1FRoom2_Text_AceTrainerMicahIntro, VictoryRoad1FRoom2_Text_AceTrainerMicahDefeat
	msgbox VictoryRoad1FRoom2_Text_AceTrainerMicahPost, MSGBOX_AUTOCLOSE
	end

VictoryRoad1FRoom2_Text_AceTrainerMicahIntro:
	.string "When Trainers lock eyes...\pThat's right! It's time to let\ntheir Pokémon go wild!$"

VictoryRoad1FRoom2_Text_AceTrainerMicahDefeat:
	.string "Your Pokémon have a real peppy feel to\nthem!$"

VictoryRoad1FRoom2_Text_AceTrainerMicahPost:
	.string "Whether you're talking to people or\nPokémon, it's important to always look\pthem square in the eyes.$"

VictoryRoad1FRoom2_EventScript_AceTrainerBrandi::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_BRANDI, VictoryRoad1FRoom2_Text_AceTrainerBrandiIntro, VictoryRoad1FRoom2_Text_AceTrainerBrandiDefeat
	msgbox VictoryRoad1FRoom2_Text_AceTrainerBrandiPost, MSGBOX_AUTOCLOSE
	end

VictoryRoad1FRoom2_Text_AceTrainerBrandiIntro:
	.string "I will win. I am sure of it.\nTherefore, you will lose!$"

VictoryRoad1FRoom2_Text_AceTrainerBrandiDefeat:
	.string "But...\nThis isn't possible!$"

VictoryRoad1FRoom2_Text_AceTrainerBrandiPost:
	.string "It's not that you've won.\nIt's just that I lost!\p...It's all the same.\nGo, me.$"

VictoryRoad1FRoom2_EventScript_PsychicDesiree::
	trainerbattle_single TRAINER_SINNOH_PSYCHIC_DESIREE, VictoryRoad1FRoom2_Text_PsychicDesireeIntro, VictoryRoad1FRoom2_Text_PsychicDesireeDefeat
	msgbox VictoryRoad1FRoom2_Text_PsychicDesireePost, MSGBOX_AUTOCLOSE
	end

VictoryRoad1FRoom2_Text_PsychicDesireeIntro:
	.string "Allow me to demonstrate how a true\nPsychic conducts a battle!$"

VictoryRoad1FRoom2_Text_PsychicDesireeDefeat:
	.string "Did I get to show you anything...?\nAnything at all?$"

VictoryRoad1FRoom2_Text_PsychicDesireePost:
	.string "What can psychic power be used for?\pWell, one mustn't use it for committing\ncrimes.\pBut, I don't use it for doing good,\neither.\pUsing psychic power leaves me too worn\nout!$"

VictoryRoad1FRoom2_EventScript_PsychicLandon::
	trainerbattle_single TRAINER_SINNOH_PSYCHIC_LANDON, VictoryRoad1FRoom2_Text_PsychicLandonIntro, VictoryRoad1FRoom2_Text_PsychicLandonDefeat
	msgbox VictoryRoad1FRoom2_Text_PsychicLandonPost, MSGBOX_AUTOCLOSE
	end

VictoryRoad1FRoom2_Text_PsychicLandonIntro:
	.string "Now we shall battle, and from it will\nemerge one loser...$"

VictoryRoad1FRoom2_Text_PsychicLandonDefeat:
	.string "...!$"

VictoryRoad1FRoom2_Text_PsychicLandonPost:
	.string "I can use psychic powers, but\nbattling isn't so simple...\pIt takes much more to win!$"

VictoryRoad1FRoom2_EventScript_BlackBeltEddie::
	trainerbattle_single TRAINER_SINNOH_BLACK_BELT_EDDIE, VictoryRoad1FRoom2_Text_BlackBeltEddieIntro, VictoryRoad1FRoom2_Text_BlackBeltEddieDefeat
	msgbox VictoryRoad1FRoom2_Text_BlackBeltEddiePost, MSGBOX_AUTOCLOSE
	end

VictoryRoad1FRoom2_Text_BlackBeltEddieIntro:
	.string "I trained all of my gnarly Pokémon\nat the Fighting Dojo in Kanto!$"

VictoryRoad1FRoom2_Text_BlackBeltEddieDefeat:
	.string "D  n     i\n  o  e     n...$"

VictoryRoad1FRoom2_Text_BlackBeltEddiePost:
	.string "We're gonna go ahead and leave...\nYou know, go train elsewhere.$"

VictoryRoad1FRoom2_EventScript_VeteranTerrell::
	trainerbattle_single TRAINER_SINNOH_VETERAN_TERRELL, VictoryRoad1FRoom2_Text_VeteranTerrellIntro, VictoryRoad1FRoom2_Text_VeteranTerrellDefeat
	msgbox VictoryRoad1FRoom2_Text_VeteranTerrellPost, MSGBOX_AUTOCLOSE
	end

VictoryRoad1FRoom2_Text_VeteranTerrellIntro:
	.string "What it means to battle...\nIts joys, its sorrows...\pI've experienced it all!$"

VictoryRoad1FRoom2_Text_VeteranTerrellDefeat:
	.string "My sorrow deepens...$"

VictoryRoad1FRoom2_Text_VeteranTerrellPost:
	.string "You may be a child, but you've taught\nme a whole lot. I thank you humbly.$"

VictoryRoad1FRoom2_EventScript_AceTrainerArthur::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_ARTHUR, VictoryRoad1FRoom2_Text_AceTrainerArthurIntro, VictoryRoad1FRoom2_Text_AceTrainerArthurDefeat
	msgbox VictoryRoad1FRoom2_Text_AceTrainerArthurPost, MSGBOX_AUTOCLOSE
	end

VictoryRoad1FRoom2_Text_AceTrainerArthurIntro:
	.string "I want my Pokémon to get a taste of\nthe sweetness that is victory.\pI can't afford to lose this one!$"

VictoryRoad1FRoom2_Text_AceTrainerArthurDefeat:
	.string "This defeat has the tang of my bitter\ntears...$"

VictoryRoad1FRoom2_Text_AceTrainerArthurPost:
	.string "I'm sorry, my Pokémon team...\pI promise, I'll get better at this so\nyou can get a taste of victory!$"

VictoryRoad1FRoom2_EventScript_AceTrainerClarice::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_CLARICE, VictoryRoad1FRoom2_Text_AceTrainerClariceIntro, VictoryRoad1FRoom2_Text_AceTrainerClariceDefeat
	msgbox VictoryRoad1FRoom2_Text_AceTrainerClaricePost, MSGBOX_AUTOCLOSE
	end

VictoryRoad1FRoom2_Text_AceTrainerClariceIntro:
	.string "Let me see what you got there, kid.\nI could give you some advice.$"

VictoryRoad1FRoom2_Text_AceTrainerClariceDefeat:
	.string "You got way too much!$"

VictoryRoad1FRoom2_Text_AceTrainerClaricePost:
	.string "Well, I don't have any advice for\nsomeone as tough as you!$"

VictoryRoad1FRoom2_EventScript_PsychicDeandre::
	trainerbattle_single TRAINER_SINNOH_PSYCHIC_DEANDRE, VictoryRoad1FRoom2_Text_PsychicDeandreIntro, VictoryRoad1FRoom2_Text_PsychicDeandreDefeat
	msgbox VictoryRoad1FRoom2_Text_PsychicDeandrePost, MSGBOX_AUTOCLOSE
	end

VictoryRoad1FRoom2_Text_PsychicDeandreIntro:
	.string "A battle is a clash of willpower!\pThe one who wants the win the most\nwill emerge the victor!$"

VictoryRoad1FRoom2_Text_PsychicDeandreDefeat:
	.string "But... I thought I could win!$"

VictoryRoad1FRoom2_Text_PsychicDeandrePost:
	.string "Psychic power...\pI know it isn't easy to believe in\nsomething that you can't see.\pBut love, friendship...\nYou can't see those, either.$"

VictoryRoad1FRoom2_EventScript_PsychicKendra::
	trainerbattle_single TRAINER_SINNOH_PSYCHIC_KENDRA, VictoryRoad1FRoom2_Text_PsychicKendraIntro, VictoryRoad1FRoom2_Text_PsychicKendraDefeat
	msgbox VictoryRoad1FRoom2_Text_PsychicKendraPost, MSGBOX_AUTOCLOSE
	end

VictoryRoad1FRoom2_Text_PsychicKendraIntro:
	.string "I see it!\nI see a victory for me!$"

VictoryRoad1FRoom2_Text_PsychicKendraDefeat:
	.string "The future...is different!\nWhy?!$"

VictoryRoad1FRoom2_Text_PsychicKendraPost:
	.string "Your efforts have altered the very\npath of the future!$"

VictoryRoad1FRoom2_EventScript_BirdKeeperAutumn::
	trainerbattle_single TRAINER_SINNOH_BIRD_KEEPER_AUTUMN, VictoryRoad1FRoom2_Text_BirdKeeperAutumnIntro, VictoryRoad1FRoom2_Text_BirdKeeperAutumnDefeat
	msgbox VictoryRoad1FRoom2_Text_BirdKeeperAutumnPost, MSGBOX_AUTOCLOSE
	end

VictoryRoad1FRoom2_Text_BirdKeeperAutumnIntro:
	.string "The sharp vision of my bird Pokémon\nwill see through your weaknesses!$"

VictoryRoad1FRoom2_Text_BirdKeeperAutumnDefeat:
	.string "Don't you have an Achilles' heel?$"

VictoryRoad1FRoom2_Text_BirdKeeperAutumnPost:
	.string "I want to become stronger, but only\nwith my favorite Pokémon.$"

VictoryRoad1FRoom2_EventScript_DragonTamerJoe::
	trainerbattle_single TRAINER_SINNOH_DRAGON_TAMER_JOE, VictoryRoad1FRoom2_Text_DragonTamerJoeIntro, VictoryRoad1FRoom2_Text_DragonTamerJoeDefeat
	msgbox VictoryRoad1FRoom2_Text_DragonTamerJoePost, MSGBOX_AUTOCLOSE
	end

VictoryRoad1FRoom2_Text_DragonTamerJoeIntro:
	.string "Learning how to manage tough Pokémon\nis the shortcut to getting tough.$"

VictoryRoad1FRoom2_Text_DragonTamerJoeDefeat:
	.string "I lost? But how is that possible?!$"

VictoryRoad1FRoom2_Text_DragonTamerJoePost:
	.string "Getting the best out of any Pokémon...\nThat's what makes a good Trainer...$"

VictoryRoad1FRoom2_EventScript_BlackBeltWillie::
	trainerbattle_single TRAINER_SINNOH_BLACK_BELT_WILLIE, VictoryRoad1FRoom2_Text_BlackBeltWillieIntro, VictoryRoad1FRoom2_Text_BlackBeltWillieDefeat
	msgbox VictoryRoad1FRoom2_Text_BlackBeltWilliePost, MSGBOX_AUTOCLOSE
	end

VictoryRoad1FRoom2_Text_BlackBeltWillieIntro:
	.string "Judo chop!\nPokémon battle!$"

VictoryRoad1FRoom2_Text_BlackBeltWillieDefeat:
	.string "Wrroar!\nJudo chop defeated!$"

VictoryRoad1FRoom2_Text_BlackBeltWilliePost:
	.string "I'll forget that we lost!\p...Wait, if I did that, we'd never\nlearn from our mistakes...$"

VictoryRoad1FRoom2_EventScript_VeteranBrenden::
	trainerbattle_single TRAINER_SINNOH_VETERAN_BRENDEN, VictoryRoad1FRoom2_Text_VeteranBrendenIntro, VictoryRoad1FRoom2_Text_VeteranBrendenDefeat
	msgbox VictoryRoad1FRoom2_Text_VeteranBrendenPost, MSGBOX_AUTOCLOSE
	end

VictoryRoad1FRoom2_Text_VeteranBrendenIntro:
	.string "I'll wheel out some wicked Pokémon\nand even wickeder moves!$"

VictoryRoad1FRoom2_Text_VeteranBrendenDefeat:
	.string "All I can manage now is to wheeze\nout a few meek sighs...$"

VictoryRoad1FRoom2_Text_VeteranBrendenPost:
	.string "I don't see what my age has to do\nwith playing with Pokémon, frankly.$"
