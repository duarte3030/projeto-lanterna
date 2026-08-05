@ Predio da Equipe Galactica em Eterna, 1F.
@ Texto de pret/pokeplatinum, res/text/team_galactic_eterna_building_1f.json.
@ Layout emprestado do Instituto Meteorologico da Rota 119.
@
@ Os dois grunts com TRAINER_..._ETERNA_BUILDING_1F_1 e _1F_2 ja estao em uso na
@ rua, em data/maps/EternaCity/scripts.inc. Dentro do predio as batalhas usam os
@ treinadores de 2F e 3F, que estavam livres.

TeamGalacticEternaBuilding_1F_MapScripts::
	.byte 0

TeamGalacticEternaBuilding_1F_EventScript_Looker::
	lock
	faceplayer
	msgbox TeamGalacticEternaBuilding_1F_Text_HelloItIsMe, MSGBOX_DEFAULT
	msgbox TeamGalacticEternaBuilding_1F_Text_InvestigationIntoTeamGalactic, MSGBOX_DEFAULT
	release
	end

TeamGalacticEternaBuilding_1F_EventScript_Grunt::
	msgbox TeamGalacticEternaBuilding_1F_Text_WelcomeToTeamGalactic, MSGBOX_NPC
	end

TeamGalacticEternaBuilding_1F_EventScript_Grunt2::
	msgbox TeamGalacticEternaBuilding_1F_Text_SightsSetOnTheStars, MSGBOX_NPC
	end

TeamGalacticEternaBuilding_1F_EventScript_PathSign::
	msgbox TeamGalacticEternaBuilding_1F_Text_PathLeadsToGlory, MSGBOX_SIGN
	end

TeamGalacticEternaBuilding_1F_Text_HelloItIsMe:
	.string "Looker: Hello! It is me! Me!\n"
	.string "Hahaha! I have startled you, yes?\p"
	.string "I am, after all, an officer of the\n"
	.string "International Police.\p"
	.string "It is only natural that I be a\n"
	.string "master of disguise.$"

TeamGalacticEternaBuilding_1F_Text_InvestigationIntoTeamGalactic:
	.string "Looker: Now, I have been\n"
	.string "conducting my investigation into\l"
	.string "Team Galactic.\p"
	.string "But I have no clue as to who they\n"
	.string "are or what it is they wish to do.\p"
	.string "The minions, they appear ignorant\n"
	.string "of the intentions of their boss.\p"
	.string "Also, a word of advice.\p"
	.string "This building, it has two stairs.\n"
	.string "One of them, a trap it must be.\p"
	.string "But the crooks of Team Galactic,\n"
	.string "they do not appear, how shall I\l"
	.string "say, smart.\p"
	.string "There should be an easy way to\n"
	.string "tell the stairs apart!$"

TeamGalacticEternaBuilding_1F_Text_WelcomeToTeamGalactic:
	.string "Welcome to Team Galactic. Are you\n"
	.string "here to donate your Pokémon?\p"
	.string "What? You're not?\n"
	.string "Then kindly get off our property!\p"
	.string "Do we have to bring the pain like\n"
	.string "we did with the Cycle Shop\l"
	.string "manager?$"

TeamGalacticEternaBuilding_1F_Text_SightsSetOnTheStars:
	.string "As a group, Team Galactic has its\n"
	.string "sights set on the stars, not on\l"
	.string "this world!$"

TeamGalacticEternaBuilding_1F_Text_PathLeadsToGlory:
	.string "The path you chose leads to glory.$"
