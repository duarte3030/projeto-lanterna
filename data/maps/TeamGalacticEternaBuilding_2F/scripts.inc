@ Predio da Equipe Galactica em Eterna, 2F.
@ Texto de pret/pokeplatinum, res/text/team_galactic_eterna_building_2f.json.
@ Layout emprestado do Mt. Pyre 3F, que ja tem as duas escadas de que o Looker
@ fala no 1F. Os buracos do chao do mapa original NAO ganharam warp_def, entao
@ nao fazem nada.

TeamGalacticEternaBuilding_2F_MapScripts::
	.byte 0

TeamGalacticEternaBuilding_2F_EventScript_Grunt1::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_TEAM_GALACTIC_ETERNA_BUILDING_2F_1, TeamGalacticEternaBuilding_2F_Text_Grunt1Intro, TeamGalacticEternaBuilding_2F_Text_Grunt1Defeat
	msgbox TeamGalacticEternaBuilding_2F_Text_WorkingToFindEnergySources, MSGBOX_AUTOCLOSE
	end

TeamGalacticEternaBuilding_2F_EventScript_Grunt2::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_TEAM_GALACTIC_ETERNA_BUILDING_2F_2, TeamGalacticEternaBuilding_2F_Text_Grunt2Intro, TeamGalacticEternaBuilding_2F_Text_Grunt2Defeat
	msgbox TeamGalacticEternaBuilding_2F_Text_ResearchOnFormsOfEnergy, MSGBOX_AUTOCLOSE
	end

TeamGalacticEternaBuilding_2F_EventScript_ProgressSign::
	msgbox TeamGalacticEternaBuilding_2F_Text_MakeProgressTogether, MSGBOX_SIGN
	end

TeamGalacticEternaBuilding_2F_Text_Grunt1Intro:
	.string "Team Galactic is working hard to\n"
	.string "find new energy sources!\p"
	.string "And you are in the way!$"

TeamGalacticEternaBuilding_2F_Text_Grunt1Defeat:
	.string "Out of the way, out of energy...$"

TeamGalacticEternaBuilding_2F_Text_WorkingToFindEnergySources:
	.string "Team Galactic is working hard to\n"
	.string "find new energy sources for the\l"
	.string "future!$"

TeamGalacticEternaBuilding_2F_Text_Grunt2Intro:
	.string "We are conducting research on new\n"
	.string "forms of energy!\p"
	.string "Research does not need visitors!$"

TeamGalacticEternaBuilding_2F_Text_Grunt2Defeat:
	.string "My research is ruined!$"

TeamGalacticEternaBuilding_2F_Text_ResearchOnFormsOfEnergy:
	.string "We are conducting research on new\n"
	.string "forms of energy!\p"
	.string "We want to harness the mysterious\n"
	.string "power of Pokémon and use it as\l"
	.string "energy!$"

TeamGalacticEternaBuilding_2F_Text_MakeProgressTogether:
	.string "Let us make progress together!\p"
	.string "             Team Galactic$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

TeamGalacticEternaBuilding_2F_EventScript_Placa1::
	msgbox TeamGalacticEternaBuilding_2F_Text_Placa1, MSGBOX_SIGN
	end

TeamGalacticEternaBuilding_2F_Text_Placa1:
	.string "Let us make progress together!\n             Team Galactic$"
