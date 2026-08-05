@ QG da Galactica, 2F: alojamento dos grunts.
@ Texto de pret/pokeplatinum, res/text/galactic_hq_2f.json.
@ Layout emprestado do Centro Espacial de Mossdeep. Warps sao os do mapa de Hoenn.

GalacticHQ_2F_MapScripts::
	.byte 0

GalacticHQ_2F_EventScript_Grunt1::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_GALACTIC_HQ_2F_1, GalacticHQ_2F_Text_Grunt1Intro, GalacticHQ_2F_Text_Grunt1Defeat
	msgbox GalacticHQ_2F_Text_Grunt1PostBattle, MSGBOX_AUTOCLOSE
	end

GalacticHQ_2F_EventScript_Grunt2::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_GALACTIC_HQ_2F_2, GalacticHQ_2F_Text_Grunt2Intro, GalacticHQ_2F_Text_Grunt2Defeat
	msgbox GalacticHQ_2F_Text_Grunt2PostBattle, MSGBOX_AUTOCLOSE
	end

GalacticHQ_2F_EventScript_Grunt3::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_GALACTIC_HQ_2F_3, GalacticHQ_2F_Text_Grunt3Intro, GalacticHQ_2F_Text_Grunt3Defeat
	msgbox GalacticHQ_2F_Text_TeamGalacticCredo, MSGBOX_AUTOCLOSE
	end

GalacticHQ_2F_EventScript_NapRoomSign::
	msgbox GalacticHQ_2F_Text_TeamGalacticNapRoom, MSGBOX_SIGN
	end

GalacticHQ_2F_EventScript_TVRoomSign::
	msgbox GalacticHQ_2F_Text_TeamGalacticTVRoom, MSGBOX_SIGN
	end

@ O relatorio das placas de Eterna. Duas telas, sem escolha: perguntar
@ "quer continuar lendo?" custaria uma var de resposta, e o texto e curto.
GalacticHQ_2F_EventScript_Report::
	lockall
	msgbox GalacticHQ_2F_Text_ReadReport, MSGBOX_DEFAULT
	msgbox GalacticHQ_2F_Text_StatuePlateText1, MSGBOX_DEFAULT
	msgbox GalacticHQ_2F_Text_StatuePlateText2, MSGBOX_DEFAULT
	msgbox GalacticHQ_2F_Text_PutReportBack, MSGBOX_DEFAULT
	releaseall
	end

GalacticHQ_2F_Text_Grunt1Intro:
	.string "This is the Team Galactic nap\n"
	.string "room. You are not a member.\p"
	.string "Out!$"

GalacticHQ_2F_Text_Grunt1Defeat:
	.string "So much for my nap...$"

GalacticHQ_2F_Text_Grunt1PostBattle:
	.string "There is a report about the\n"
	.string "Pokémon statues of Eterna lying\l"
	.string "around here somewhere.$"

GalacticHQ_2F_Text_Grunt2Intro:
	.string "Onward to a new universe!\n"
	.string "Team Galactic!$"

GalacticHQ_2F_Text_Grunt2Defeat:
	.string "The new universe can wait...$"

GalacticHQ_2F_Text_Grunt2PostBattle:
	.string "Health and prosperity through the\n"
	.string "partaking of favorite foods!$"

GalacticHQ_2F_Text_Grunt3Intro:
	.string "Everything belongs to Team\n"
	.string "Galactic! Including this floor!$"

GalacticHQ_2F_Text_Grunt3Defeat:
	.string "Ugh... Not everything, then.$"

GalacticHQ_2F_Text_TeamGalacticCredo:
	.string "The Team Galactic credo!\n"
	.string "Everything belongs to Team\l"
	.string "Galactic!\p"
	.string "Look beyond the world, space will\n"
	.string "become Team Galactic's!$"

GalacticHQ_2F_Text_TeamGalacticNapRoom:
	.string "Team Galactic Nap Room\p"
	.string "Ensure the bed is unoccupied\n"
	.string "before getting into it!$"

GalacticHQ_2F_Text_TeamGalacticTVRoom:
	.string "Team Galactic TV Room\p"
	.string "State-of-the-art audio & video\n"
	.string "system for member use only!\p"
	.string "Onward to a new universe!\n"
	.string "Team Galactic!$"

GalacticHQ_2F_Text_ReadReport:
	.string "There is a report titled “The\n"
	.string "Pokémon Statues of Eterna.”$"

GalacticHQ_2F_Text_StatuePlateText1:
	.string "Pokémon statue plate text no. 1\n"
	.string "(from stolen plate):\p"
	.string "“The creation of DIALGA,\n"
	.string "the giver of time...\p"
	.string "“In laughter, there is tears...\n"
	.string "And, likewise it is with time.\p"
	.string "“The same time flows on.\n"
	.string "For it is the blessing of DIALGA.”$"

GalacticHQ_2F_Text_StatuePlateText2:
	.string "Pokémon statue plate text no. 2\n"
	.string "(from stolen plate):\p"
	.string "“The birth of PALKIA.\n"
	.string "The creator of parallel\l"
	.string "dimensions...\p"
	.string "“Alive, yet not alive...\n"
	.string "Everything drifts in space...\p"
	.string "“To arrive in the same universe.\n"
	.string "It is the blessing of PALKIA.”$"

GalacticHQ_2F_Text_PutReportBack:
	.string "The blue text has been extracted\n"
	.string "using a high-tech device made by\l"
	.string "the boss.$"
