@ QG da Galactica, B2F.
@ Texto de pret/pokeplatinum, res/text/galactic_hq_b2f.json.
@ Layout e fiacao de paineis copiados do Esconderijo Aqua B2F, com o painel de
@ (32,20) redirecionado para o laboratorio.

GalacticHQ_B2F_MapScripts::
	.byte 0

GalacticHQ_B2F_EventScript_Grunt1::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_GALACTIC_HQ_B2F_1, GalacticHQ_B2F_Text_Grunt1Intro, GalacticHQ_B2F_Text_Grunt1Defeat
	msgbox GalacticHQ_B2F_Text_FreeAllPokemon, MSGBOX_AUTOCLOSE
	end

GalacticHQ_B2F_EventScript_Grunt2::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_GALACTIC_HQ_B2F_2, GalacticHQ_B2F_Text_Grunt2Intro, GalacticHQ_B2F_Text_Grunt2Defeat
	msgbox GalacticHQ_B2F_Text_Grunt2PostBattle, MSGBOX_AUTOCLOSE
	end

GalacticHQ_B2F_EventScript_SpeechGrunt::
	msgbox GalacticHQ_B2F_Text_ToGetIntoSpeech, MSGBOX_NPC
	end

@ Cientista de pret/pokeplatinum (LOCALID_SCIENTIST_M, hidden_flag
@ FLAG_HIDE_GALACTIC_HQ_TEAM_GALACTIC); some quando FLAG_GALACTICA_QG_TOMADO
@ acende, junto com os cientistas do laboratorio. Fala igual a da fonte, que ja
@ mora em GalacticHQ_B2F_Text_FreeAllPokemon (mesma linha do texto pos-batalha
@ do Grunt1).
GalacticHQ_B2F_EventScript_Scientist::
	msgbox GalacticHQ_B2F_Text_FreeAllPokemon, MSGBOX_NPC
	end

GalacticHQ_B2F_Text_Grunt1Intro:
	.string "Nobody comes down here without\n"
	.string "Master Cyrus saying so!$"

GalacticHQ_B2F_Text_Grunt1Defeat:
	.string "How did you get so strong?$"

GalacticHQ_B2F_Text_FreeAllPokemon:
	.string "Team Galactic will set free all\n"
	.string "Pokémon, all of nature!\p"
	.string "Uwahahaha!\n"
	.string "Team Galactic will then own it\l"
	.string "all!$"

GalacticHQ_B2F_Text_Grunt2Intro:
	.string "The warp panels keep out anyone\n"
	.string "who does not belong here.\p"
	.string "Anyone but you, apparently!$"

GalacticHQ_B2F_Text_Grunt2Defeat:
	.string "The panels failed. So did I.$"

GalacticHQ_B2F_Text_Grunt2PostBattle:
	.string "The door is locked.\n"
	.string "A special key is needed.$"

GalacticHQ_B2F_Text_ToGetIntoSpeech:
	.string "OK, to get into Master Cyrus's\n"
	.string "speech... Uh, where was it now?\p"
	.string "At the Galactic Veilstone\n"
	.string "Building, that much I'm sure\l"
	.string "about.\p"
	.string "Go in through the door beside the\n"
	.string "reception counter, I think it was?\p"
	.string "Uh? What'd I do with that key\n"
	.string "anyway? Where's it gone?$"
