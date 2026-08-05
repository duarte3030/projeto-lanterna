@ Predio da Equipe Galactica em Eterna, 3F.
@ Texto de pret/pokeplatinum, res/text/team_galactic_eterna_building_3f.json.
@ Layout emprestado do Mt. Pyre 4F.

TeamGalacticEternaBuilding_3F_MapScripts::
	.byte 0

TeamGalacticEternaBuilding_3F_EventScript_Grunt::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_TEAM_GALACTIC_ETERNA_BUILDING_3F, TeamGalacticEternaBuilding_3F_Text_GruntIntro, TeamGalacticEternaBuilding_3F_Text_GruntDefeat
	msgbox TeamGalacticEternaBuilding_3F_Text_OrdinaryPeopleCantUnderstand, MSGBOX_AUTOCLOSE
	end

TeamGalacticEternaBuilding_3F_EventScript_PathSign::
	msgbox TeamGalacticEternaBuilding_3F_Text_FollowThisPath, MSGBOX_SIGN
	end

TeamGalacticEternaBuilding_3F_Text_GruntIntro:
	.string "Ordinary people like you can't\n"
	.string "understand Team Galactic's grand\l"
	.string "designs!\p"
	.string "I will explain it with Pokémon!$"

TeamGalacticEternaBuilding_3F_Text_GruntDefeat:
	.string "That explained nothing at all...$"

TeamGalacticEternaBuilding_3F_Text_OrdinaryPeopleCantUnderstand:
	.string "Ordinary people like you can't\n"
	.string "understand Team Galactic's grand\l"
	.string "designs!\p"
	.string "Come to think of it... I don't\n"
	.string "even know what's going on...$"

TeamGalacticEternaBuilding_3F_Text_FollowThisPath:
	.string "Question not and follow this path!\n"
	.string "The road to success!$"
