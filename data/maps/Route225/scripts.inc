@ Referencia de treinador de Sinnoh. Ver Pokemon Claude/SINNOH-PADRAO.md.
@ Falas vindas de pret/pokeplatinum, em ingles, como o resto do jogo.

Route225_MapScripts::
	.byte 0

Route225_EventScript_AceTrainerRodolfo::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_RODOLFO, Route225_Text_AceTrainerRodolfoIntro, Route225_Text_AceTrainerRodolfoDefeat
	msgbox Route225_Text_AceTrainerRodolfoPost, MSGBOX_AUTOCLOSE
	end

Route225_EventScript_RangerAshlee::
	trainerbattle_single TRAINER_SINNOH_RANGER_ASHLEE, Route225_Text_RangerAshleeIntro, Route225_Text_RangerAshleeDefeat
	msgbox Route225_Text_RangerAshleePost, MSGBOX_AUTOCLOSE
	end

Route225_EventScript_BirdKeeperAudrey::
	trainerbattle_single TRAINER_SINNOH_BIRD_KEEPER_AUDREY, Route225_Text_BirdKeeperAudreyIntro, Route225_Text_BirdKeeperAudreyDefeat
	msgbox Route225_Text_BirdKeeperAudreyPost, MSGBOX_AUTOCLOSE
	end

Route225_EventScript_DragonTamerGeoffrey::
	trainerbattle_single TRAINER_SINNOH_DRAGON_TAMER_GEOFFREY, Route225_Text_DragonTamerGeoffreyIntro, Route225_Text_DragonTamerGeoffreyDefeat
	msgbox Route225_Text_DragonTamerGeoffreyPost, MSGBOX_AUTOCLOSE
	end

Route225_EventScript_AceTrainerQuinn::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_QUINN, Route225_Text_AceTrainerQuinnIntro, Route225_Text_AceTrainerQuinnDefeat
	msgbox Route225_Text_AceTrainerQuinnPost, MSGBOX_AUTOCLOSE
	end

Route225_EventScript_PsychicDaisy::
	trainerbattle_single TRAINER_SINNOH_PSYCHIC_DAISY, Route225_Text_PsychicDaisyIntro, Route225_Text_PsychicDaisyDefeat
	msgbox Route225_Text_PsychicDaisyPost, MSGBOX_AUTOCLOSE
	end

Route225_EventScript_AceTrainerDeanna::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_DEANNA, Route225_Text_AceTrainerDeannaIntro, Route225_Text_AceTrainerDeannaDefeat
	msgbox Route225_Text_AceTrainerDeannaPost, MSGBOX_AUTOCLOSE
	end

Route225_EventScript_RangerDwayne::
	trainerbattle_single TRAINER_SINNOH_RANGER_DWAYNE, Route225_Text_RangerDwayneIntro, Route225_Text_RangerDwayneDefeat
	msgbox Route225_Text_RangerDwaynePost, MSGBOX_AUTOCLOSE
	end

Route225_EventScript_SignFightArea::
	msgbox Route225_Text_SignFightArea, MSGBOX_SIGN
	end

Route225_EventScript_SignSurvivalArea::
	msgbox Route225_Text_SignSurvivalArea, MSGBOX_SIGN
	end

Route225_Text_AceTrainerRodolfoIntro:
	.string "There is something missing in the\n"
	.string "way I battle...\p"
	.string "I've come here to find it.$"

Route225_Text_AceTrainerRodolfoDefeat:
	.string "I see it now...\n"
	.string "I know what I lack.$"

Route225_Text_AceTrainerRodolfoPost:
	.string "Battling you was an eye-opener.\p"
	.string "I learned something very important\n"
	.string "in that short time.$"

Route225_Text_RangerAshleeIntro:
	.string "In the embrace of Mother Nature,\n"
	.string "people and Pokémon grow strong!$"

Route225_Text_RangerAshleeDefeat:
	.string "Your Pokémon are so muscular.\n"
	.string "It makes me sigh seeing them...$"

Route225_Text_RangerAshleePost:
	.string "It doesn't matter where they grow.\p"
	.string "Pokémon can be made tougher\n"
	.string "anywhere if you set your mind to it.$"

Route225_Text_BirdKeeperAudreyIntro:
	.string "I let my bird Pokémon carry me to\n"
	.string "wherever. And so, here I am!$"

Route225_Text_BirdKeeperAudreyDefeat:
	.string "Sheesh... I arrive in a new place, and\n"
	.string "it turns out to be the Battle Zone...$"

Route225_Text_BirdKeeperAudreyPost:
	.string "I was born in the Hoenn region.\n"
	.string "I've only just recently flown here.$"

Route225_Text_DragonTamerGeoffreyIntro:
	.string "See the potential of dragon Pokémon!\n"
	.string "The Championship is within my sights!$"

Route225_Text_DragonTamerGeoffreyDefeat:
	.string "Potential doesn't mean I can win...$"

Route225_Text_DragonTamerGeoffreyPost:
	.string "A Dragon Tamer Champion...\p"
	.string "I'll need to train so much more to\n"
	.string "even come close to coming close...$"

Route225_Text_AceTrainerQuinnIntro:
	.string "I've pumped up my gang till they can't\n"
	.string "get pumped no more.\p"
	.string "They're going to school your Pokémon!$"

Route225_Text_AceTrainerQuinnDefeat:
	.string "My bunch got schooled, and how!$"

Route225_Text_AceTrainerQuinnPost:
	.string "I fed my gang Protein, Carbos...\n"
	.string "You name it, I pumped 'em full of it.$"

Route225_Text_PsychicDaisyIntro:
	.string "Right after this, you will send out your\n"
	.string "Pokémon to do battle!$"

Route225_Text_PsychicDaisyDefeat:
	.string "After this, I will reluctantly hand over\n"
	.string "the prize money to you...$"

Route225_Text_PsychicDaisyPost:
	.string "What will you do after this?\p"
	.string "Why don't you decide for yourself?\n"
	.string "It would be much more fun that way!$"

Route225_Text_AceTrainerDeannaIntro:
	.string "Worthy opponents... The search for\n"
	.string "them drives me to travel far.$"

Route225_Text_AceTrainerDeannaDefeat:
	.string "I've certainly found a tough\n"
	.string "adversary in you...$"

Route225_Text_AceTrainerDeannaPost:
	.string "How much you believe in your\n"
	.string "Pokémon...\p"
	.string "That's a critical factor in how a\n"
	.string "battle will turn out.$"

Route225_Text_RangerDwayneIntro:
	.string "We go on patrol to make sure there's\n"
	.string "nothing strange going on.\p"
	.string "And occasionally, we battle!$"

Route225_Text_RangerDwayneDefeat:
	.string "Thanks much!$"

Route225_Text_RangerDwaynePost:
	.string "Using the Pokémon ability Pickup for\n"
	.string "gathering dropped items is a good thing.\p"
	.string "I think it's ecological, even.\n"
	.string "I am cleaning up the environment!$"

Route225_Text_SignFightArea:
	.string "FIGHT AREA\n"
	.string "This way, to the south.$"

Route225_Text_SignSurvivalArea:
	.string "SURVIVAL AREA\n"
	.string "This way, to the east.$"
