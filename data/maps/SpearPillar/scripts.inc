@ Spear Pillar: o final da historia da Equipe Galactica.
@ Texto de pret/pokeplatinum, res/text/spear_pillar.json.
@
@ ponytail: layout emprestado do topo do Sky Pillar, que ja e um terraco de
@ pilares de pedra. O warp de entrada (16,14) e o do mapa de Hoenn, sem invencao.
@
@ O portal para o Spear Pillar distorcido NAO gasta flag nem var: o tile (13,11)
@ nasce como chao comum e o ON_LOAD so o troca por metatile de porta depois que o
@ Cyrus cai. Enquanto o metatile nao for de warp, o warp_def que ja esta la nao
@ dispara (src/field_control_avatar.c, IsWarpMetatileBehavior). Mesma tecnica da
@ porta da Elite dos Quatro.
@
@ TRAINER_SINNOH_COMMANDER_MARS_SPEAR_PILLAR,
@ TRAINER_SINNOH_COMMANDER_JUPITER_SPEAR_PILLAR e
@ TRAINER_SINNOH_GALACTIC_BOSS_CYRUS_SPEAR_PILLAR NAO existem: opponents.h e os
@ .party estao fora do escopo desta tarefa. Os nomes escritos aqui sao os que
@ eles DEVEM ter, e o time sugerido esta em PENDENCIAS-GALACTICA.md.

SpearPillar_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, SpearPillar_OnLoad
	.byte 0

SpearPillar_OnLoad:
	checktrainerflag TRAINER_SINNOH_GALACTIC_BOSS_CYRUS_SPEAR_PILLAR
	call_if TRUE, SpearPillar_EventScript_OpenPortal
	end

@ 588 e o mesmo metatile de escada que o mapa de Hoenn ja usa em (16,14) neste
@ layout. Usar o id cru evita depender de um nome de metatile que este repo pode
@ nao ter.
SpearPillar_EventScript_OpenPortal::
	setmetatile 13, 11, 588, FALSE
	return

SpearPillar_EventScript_Cyrus::
	lock
	faceplayer
	goto_if_defeated TRAINER_SINNOH_GALACTIC_BOSS_CYRUS_SPEAR_PILLAR, SpearPillar_EventScript_CyrusGone
	msgbox SpearPillar_Text_EverythingIsReady, MSGBOX_DEFAULT
	msgbox SpearPillar_Text_DialgaMasterOfTime, MSGBOX_DEFAULT
	msgbox SpearPillar_Text_PalkiaMasterOfSpace, MSGBOX_DEFAULT
	msgbox SpearPillar_Text_IWillCreateNewWorld, MSGBOX_DEFAULT
	msgbox SpearPillar_Text_NothingCanRemain, MSGBOX_DEFAULT
	msgbox SpearPillar_Text_IShouldHaveExpectedAsMuch, MSGBOX_DEFAULT
	msgbox SpearPillar_Text_CantMaintainBalance, MSGBOX_DEFAULT
	trainerbattle_single TRAINER_SINNOH_GALACTIC_BOSS_CYRUS_SPEAR_PILLAR, SpearPillar_Text_MyDreamWillBeReality, SpearPillar_Text_WhatIsThisPressure, SpearPillar_EventScript_CyrusVanishes
	end

SpearPillar_EventScript_CyrusVanishes::
	msgbox SpearPillar_Text_PokemonThatAppearsAsShadow, MSGBOX_DEFAULT
	msgbox SpearPillar_Text_IHaveHarnessedPowers, MSGBOX_DEFAULT
	msgbox SpearPillar_Text_NoMoreInterference, MSGBOX_DEFAULT
	call SpearPillar_EventScript_OpenPortal
	release
	end

SpearPillar_EventScript_CyrusGone::
	msgbox SpearPillar_Text_NoMoreInterference, MSGBOX_DEFAULT
	release
	end

@ Mars primeiro, Jupiter depois, como no original ("And I'll be next").
SpearPillar_EventScript_Mars::
	trainerbattle_single TRAINER_SINNOH_COMMANDER_MARS_SPEAR_PILLAR, SpearPillar_Text_GoThroughMeFirst, SpearPillar_Text_MarsDefeat, SpearPillar_EventScript_MarsBeaten
	msgbox SpearPillar_Text_SurprisedYouMadeIt, MSGBOX_AUTOCLOSE
	end

SpearPillar_EventScript_MarsBeaten::
	msgbox SpearPillar_Text_SurprisedYouMadeIt, MSGBOX_DEFAULT
	release
	end

SpearPillar_EventScript_Jupiter::
	trainerbattle_single TRAINER_SINNOH_COMMANDER_JUPITER_SPEAR_PILLAR, SpearPillar_Text_IllBeNext, SpearPillar_Text_JupiterDefeat, SpearPillar_EventScript_JupiterBeaten
	msgbox SpearPillar_Text_BeQuietAndWatch, MSGBOX_AUTOCLOSE
	end

SpearPillar_EventScript_JupiterBeaten::
	msgbox SpearPillar_Text_BeQuietAndWatch, MSGBOX_DEFAULT
	release
	end

SpearPillar_EventScript_Grunt::
	lock
	faceplayer
	goto_if_defeated TRAINER_SINNOH_COMMANDER_MARS_SPEAR_PILLAR, SpearPillar_EventScript_GruntLetsYouPass
	msgbox SpearPillar_Text_TakeYouDown, MSGBOX_DEFAULT
	release
	end

SpearPillar_EventScript_GruntLetsYouPass::
	msgbox SpearPillar_Text_WeLetYouPass, MSGBOX_DEFAULT
	release
	end

SpearPillar_Text_TakeYouDown:
	.string "Our boss is about to do something\n"
	.string "spectacular!\p"
	.string "Don't get in the way!\n"
	.string "Of course you will, won't you?\p"
	.string "That's why the two of us will team\n"
	.string "up to take you down in an epic\l"
	.string "duel!$"

SpearPillar_Text_WeLetYouPass:
	.string "We are not capable of slowing you.\p"
	.string "We will let you pass so you can\n"
	.string "get pulverized by our bosses!$"

SpearPillar_Text_GoThroughMeFirst:
	.string "Mars: Where do you think you're\n"
	.string "going?\p"
	.string "I won't let you disturb our boss.\p"
	.string "If you're not going to listen,\n"
	.string "you'll have to go through me\l"
	.string "first.\p"
	.string "After all, you've made me look bad\n"
	.string "more times than I care to\l"
	.string "remember!$"

SpearPillar_Text_IllBeNext:
	.string "Jupiter: And I'll be next.\p"
	.string "You might be tough, but this time,\n"
	.string "the gloves are coming off!$"

SpearPillar_Text_MarsDefeat:
	.string "Mars: You... You are impossible!$"

SpearPillar_Text_JupiterDefeat:
	.string "Jupiter: Ha! The gloves came off\n"
	.string "and it changed nothing.$"

SpearPillar_Text_SurprisedYouMadeIt:
	.string "Mars: I'm surprised you made it\n"
	.string "here. You can stay if you won't\l"
	.string "meddle.$"

SpearPillar_Text_BeQuietAndWatch:
	.string "Jupiter: Be quiet and watch what\n"
	.string "our boss is about to do.$"

SpearPillar_Text_EverythingIsReady:
	.string "Cyrus: ...\p"
	.string "...Everything is ready for the\n"
	.string "creation of a new world.\p"
	.string "Now, all will end.\n"
	.string "And everything will begin.\p"
	.string "With this, the Red Chain made from\n"
	.string "the crystals of the three lake\l"
	.string "Pokémon...\p"
	.string "And this, the Red Chain I\n"
	.string "replicated with technological\l"
	.string "means...\p"
	.string "With these Red Chains I will pry\n"
	.string "open the portal to another\l"
	.string "dimension.\p"
	.string "I command that you unleash your\n"
	.string "power for me...$"

SpearPillar_Text_DialgaMasterOfTime:
	.string "DIALGA, the mythical Pokémon, and\n"
	.string "the master of time!$"

SpearPillar_Text_PalkiaMasterOfSpace:
	.string "...And the other.\p"
	.string "PALKIA, the mythical Pokémon, and\n"
	.string "the master of space and\l"
	.string "dimensions!$"

SpearPillar_Text_IWillCreateNewWorld:
	.string "Cyrus: I've waited so long for\n"
	.string "this moment, DIALGA and PALKIA.\p"
	.string "Shaping this world is a double\n"
	.string "spiral of time and space.\p"
	.string "Yes, the very things that you have\n"
	.string "the ability to control!\p"
	.string "You will do my bidding!\n"
	.string "I will have your abilities as\l"
	.string "mine!\p"
	.string "With the power I wield, I will\n"
	.string "create an entirely new world!$"

SpearPillar_Text_NothingCanRemain:
	.string "The incomplete and ugly world we\n"
	.string "have now can disappear.\p"
	.string "I am resetting everything to zero.\n"
	.string "Nothing can remain.\p"
	.string "It is all for making the ultimate\n"
	.string "world. A world of complete\l"
	.string "perfection.\p"
	.string "Nothing so vague and incomplete as\n"
	.string "spirit can remain.$"

SpearPillar_Text_IShouldHaveExpectedAsMuch:
	.string "Cyrus: ...I should have expected\n"
	.string "as much.\p"
	.string "UXIE, “The Being of Knowledge.”\p"
	.string "AZELF, “The Being of Willpower.”\p"
	.string "And MESPRIT, “The Being of\n"
	.string "Emotion”...$"

SpearPillar_Text_CantMaintainBalance:
	.string "The Pokémon have come to protect\n"
	.string "Sinnoh? Pathetic and worthless.\p"
	.string "It takes the three of them, the\n"
	.string "three lake Pokémon that symbolize\l"
	.string "spirit, to balance either the\l"
	.string "Pokémon of time or space.\p"
	.string "But they can't maintain balance\n"
	.string "against the two.\p"
	.string "Not when both DIALGA and PALKIA\n"
	.string "are here.\p"
	.string "Their coming here is in vain.\n"
	.string "So much meaningless drama.$"

SpearPillar_Text_MyDreamWillBeReality:
	.string "Now, {PLAYER}.\p"
	.string "You've constantly interfered with\n"
	.string "my plans, but you will be\l"
	.string "forgiven.\p"
	.string "After all, there will remain no\n"
	.string "spirit for all time when I am\l"
	.string "done.\p"
	.string "All spirit will disappear.\n"
	.string "It will be ripped away...\p"
	.string "From you!\n"
	.string "From your Pokémon!\p"
	.string "From those precious to you...!\p"
	.string "It is time!\n"
	.string "My dream will be my reality!$"

SpearPillar_Text_WhatIsThisPressure:
	.string "What is this pressure I feel...?\n"
	.string "Something...is enraged?$"

SpearPillar_Text_PokemonThatAppearsAsShadow:
	.string "Cyrus: Interesting.\p"
	.string "So, there is a Pokémon that can\n"
	.string "only appear as a shadow.$"

SpearPillar_Text_IHaveHarnessedPowers:
	.string "Regardless, the effort is rash and\n"
	.string "foolish.\p"
	.string "I have harnessed the powers of\n"
	.string "DIALGA and PALKIA...$"

SpearPillar_Text_NoMoreInterference:
	.string "I, Cyrus, won't have any more\n"
	.string "interferererererere...!$"
