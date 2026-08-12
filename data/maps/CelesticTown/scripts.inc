@ Textos vindos de pret/pokeplatinum (res/text/celestic_town.json), em ingles.
@ Grunt_M, Elder e Cynthia ENTRARAM em 12/08/2026, com a cena junto
@ (dev_scripts/cena_galactica_sinnoh.py, bloco B6). Os FLAG_HIDE_CELESTIC_TOWN_*
@ do Platinum viraram FLAG_GALACTICA_CELESTIC e FLAG_CELESTIC_CYNTHIA_ESCONDIDA;
@ ver SINNOH-PADRAO.md. Esta cabeca dizia que eles estavam de fora e agora
@ estaria mentindo.

CelesticTown_MapScripts::
	.byte 0

CelesticTown_EventScript_TownSign::
	msgbox CelesticTown_Text_TownSign, MSGBOX_SIGN
	end

CelesticTown_Text_TownSign:
	.string "CELESTIC TOWN\n"
	.string "A Timeworn Town$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

CelesticTown_EventScript_Npc1::
	msgbox CelesticTown_Text_Npc1, MSGBOX_NPC
	end

CelesticTown_Text_Npc1:
	.string "Howdy!\nStudying up on local history?$"

CelesticTown_EventScript_Npc2::
	msgbox CelesticTown_Text_Npc2, MSGBOX_NPC
	end

CelesticTown_Text_Npc2:
	.string "Hey, do you know what they say?\pThey say a Pokémon created the\nSinnoh region.$"

CelesticTown_EventScript_Npc3::
	msgbox CelesticTown_Text_Npc3, MSGBOX_NPC
	end

CelesticTown_Text_Npc3:
	.string "There's no Pokémon Mart in this\ntown...\pInstead, you can buy and sell items\nin this house here.$"

CelesticTown_EventScript_Placa4::
	msgbox CelesticTown_Text_Placa4, MSGBOX_SIGN
	end

CelesticTown_Text_Placa4:
	.string "Celestic Town\nThe Past Lives$"

CelesticTown_EventScript_Placa5::
	msgbox CelesticTown_Text_Placa5, MSGBOX_SIGN
	end

CelesticTown_Text_Placa5:
	.string "A giant etching of a Pokémon-like\ncreature covers the wall...\pThere is some fading text etched\nin as well...\pThe flow of time never stops...\nThe past, future, and present...$"

CelesticTown_EventScript_Placa6::
	msgbox CelesticTown_Text_Placa6, MSGBOX_SIGN
	end

CelesticTown_Text_Placa6:
	.string "A giant etching of a Pokémon-like\ncreature covers the wall...\pThere is some fading text etched\nin as well...\pThe flow of time never stops...\nThe past, future, and present...$"

CelesticTown_EventScript_Placa7::
	msgbox CelesticTown_Text_Placa7, MSGBOX_SIGN
	end

CelesticTown_Text_Placa7:
	.string "A giant etching of a Pokémon-like\ncreature covers the wall...\pThere is some fading text etched\nin as well...\pThe flow of time never stops...\nThe past, future, and present...$"

CelesticTown_EventScript_Placa8::
	msgbox CelesticTown_Text_Placa8, MSGBOX_SIGN
	end

CelesticTown_Text_Placa8:
	.string "A giant etching of a Pokémon-like\ncreature covers the wall...\pThere is some fading text etched\nin as well...\pSpace is ever-expanding dimensions...\nOur spirits, too, are as space...$"

CelesticTown_EventScript_Placa9::
	msgbox CelesticTown_Text_Placa9, MSGBOX_SIGN
	end

CelesticTown_Text_Placa9:
	.string "A giant etching of a Pokémon-like\ncreature covers the wall...\pThere is some fading text etched\nin as well...\pSpace is ever-expanding dimensions...\nOur spirits, too, are as space...$"

CelesticTown_EventScript_Placa10::
	msgbox CelesticTown_Text_Placa10, MSGBOX_SIGN
	end

CelesticTown_Text_Placa10:
	.string "A giant etching of a Pokémon-like\ncreature covers the wall...\pThere is some fading text etched\nin as well...\pSpace is ever-expanding dimensions...\nOur spirits, too, are as space...$"

@ ponytail: UMA flag para a cena inteira. FLAG_GALACTICA_CELESTIC esconde o
@ grunt E os seis do show da Rota 218, e a mesma derrota APAGA a flag que
@ segurava a Cynthia. No Platinum quem libera a Rota 218 e a fala da Cynthia,
@ um passo depois; aqui e a derrota do grunt, um passo antes. O encurtamento e
@ deliberado: economiza uma flag e nao muda a ordem em que o jogador ve as
@ coisas, porque a Cynthia nasce no mesmo instante.
CelesticTown_EventScript_GalacticGrunt::
	lock
	faceplayer
	msgbox CelesticTown_Text_CenaMessWithMe, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, CelesticTown_EventScript_GruntVerySmart
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_CELESTIC_TOWN, CelesticTown_Text_CenaYouDare, CelesticTown_Text_CenaTooMuch, CelesticTown_EventScript_GruntBeaten
	end

CelesticTown_EventScript_GruntVerySmart::
	msgbox CelesticTown_Text_CenaVerySmart, MSGBOX_DEFAULT
	release
	end

CelesticTown_EventScript_GruntBeaten::
	setflag FLAG_GALACTICA_CELESTIC
	clearflag FLAG_CELESTIC_CYNTHIA_ESCONDIDA
	removeobject LOCALID_CELESTIC_TOWN_GALACTIC_GRUNT
	addobject LOCALID_CELESTIC_TOWN_CYNTHIA
	release
	end

CelesticTown_EventScript_Elder::
	lock
	faceplayer
	goto_if_set FLAG_GALACTICA_CELESTIC, CelesticTown_EventScript_ElderThanks
	msgbox CelesticTown_Text_CenaOddSpaceman, MSGBOX_DEFAULT
	release
	end

CelesticTown_EventScript_ElderThanks::
	msgbox CelesticTown_Text_CenaOldCharm, MSGBOX_DEFAULT
	msgbox CelesticTown_Text_CenaLookAround, MSGBOX_DEFAULT
	msgbox CelesticTown_Text_CenaExamineRuins, MSGBOX_DEFAULT
	release
	end

CelesticTown_EventScript_Cynthia::
	lock
	faceplayer
	msgbox CelesticTown_Text_CenaAllRight, MSGBOX_DEFAULT
	msgbox CelesticTown_Text_CenaHarmless, MSGBOX_DEFAULT
	msgbox CelesticTown_Text_CenaLibrary, MSGBOX_DEFAULT
	release
	end

CelesticTown_Text_CenaAllRight:
	.string "Cynthia: Was everything all right here?\pYou saw those strange people with\na Galactic Bomb, didn't you?$"

CelesticTown_Text_CenaExamineRuins:
	.string "You've gone to the trouble of visiting\nCelestic Town.\pWhy not take a little more time to\nexamine the ruins?$"

CelesticTown_Text_CenaHarmless:
	.string "But those Team Galactic people...!\nI thought they were harmless.\pThe bizarre ways they dress, and all\ntheir wild claims about making a new\puniverse...\pI thought it was just silly talk.\nNothing to take seriously.\pBut they're surprisingly more trouble\nthan expected.\pTrying to monopolize Pokémon just isn't\nacceptable!$"

CelesticTown_Text_CenaLibrary:
	.string "By the way, were the ruins fun to\nexplore?\pIf you're interested, there is a library\nin Canalave City.\pIt's stocked with ancient books.\nYou can look up Sinnoh history there.\pIt might help you complete your\nPokédex, too.\pThe quickest way to Canalave City\nis to go west from Jubilife City.$"

CelesticTown_Text_CenaLookAround:
	.string "This Old Charm is something made in\nCelestic Town long, long ago.\pIt was made in honor of a mythical\ndeity said to have created Sinnoh.\pThese Old Charms are still discovered\nnow and again.\pSince you're in Celestic Town, why not\nlook around inside the ruins?$"

CelesticTown_Text_CenaMessWithMe:
	.string "This town is insignificant!\nThere's nothing of value here.\pIt doesn't need to exist, so I'll\nblow it up with a Galactic Bomb!\pIf you try to mess with me, I'll shut\nyou down with a Pokémon battle.\pSo, what's it going to be?\nAre you going to mess with me?$"

CelesticTown_Text_CenaOddSpaceman:
	.string "There's an odd spaceman\nin front of the ruins.\pThere isn't anything there, but that\nonly seemed to make him get angry.\pHe's saying he will blow the town\nup with a bomb...\pThe nerve of it all...\pIf only I were younger, I'd punish\nthat spaceman with my Pokémon...$"

CelesticTown_Text_CenaOldCharm:
	.string "Oh, you were magnificent!\nAren't you quite the Trainer?\pAs the elder of Celestic Town, I give\nyou my thanks.\pOh? That Old Charm...\nMay I see that, dear?\p...\nWhat's that?\pYou say Cynthia entrusted you with\nit to deliver to me?\pThat Cynthia...\nShe's my granddaughter.$"

CelesticTown_Text_CenaTooMuch:
	.string "Too much to handle...\nI can't do anything here...\pThis place is nothing!\nI'll be happily rid of this place!$"

CelesticTown_Text_CenaVerySmart:
	.string "That's right! Very smart!\nYou know what's good for you!\pTeam Galactic has come out to the\nboonies like this for everyone's sake.\pYour cooperation is appreciated.\nNow, where is my partner...?$"

CelesticTown_Text_CenaYouDare:
	.string "You dare to oppose Team Galactic?\pThat means you're taking on the\nworld... No, the universe, even!$"
