@ Predio da Equipe Galactica em Eterna, 3F.
@ Texto de pret/pokeplatinum, res/text/team_galactic_eterna_building_3f.json.
@ Layout emprestado do Mt. Pyre 4F.

TeamGalacticEternaBuilding_3F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, TeamGalacticEternaBuilding_3F_OnTransition
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

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

TeamGalacticEternaBuilding_3F_EventScript_Placa1::
	msgbox TeamGalacticEternaBuilding_3F_Text_Placa1, MSGBOX_SIGN
	end

TeamGalacticEternaBuilding_3F_Text_Placa1:
	.string "Question not and follow this path!\nThe road to success!$"

TeamGalacticEternaBuilding_3F_EventScript_ScientistTravon::
	trainerbattle_single TRAINER_SINNOH_SCIENTIST_TRAVON, TeamGalacticEternaBuilding_3F_Text_ScientistTravonIntro, TeamGalacticEternaBuilding_3F_Text_ScientistTravonDefeat
	msgbox TeamGalacticEternaBuilding_3F_Text_ScientistTravonPost, MSGBOX_AUTOCLOSE
	end

TeamGalacticEternaBuilding_3F_Text_ScientistTravonIntro:
	.string "Our mission is to implement our\noperations without question.\pIt is all for the new world order\nthat our boss will lead!$"

TeamGalacticEternaBuilding_3F_Text_ScientistTravonDefeat:
	.string "This won't go unpunished...$"

TeamGalacticEternaBuilding_3F_Text_ScientistTravonPost:
	.string "I'm willing to do anything to get ahead\nin Team Galactic.\pOne day you'll see what we are all\nabout.\pIt's wonder, compassion, splendor,\nhumor, power, awe, and tragedy!$"

@ ponytail: a cena e a flag sao a mesma coisa. Estes objetos nascem enquanto
@ derrotar a Jupiter no 4F do predio de Eterna nao aconteceu, e somem depois; o motor ja grava a flag de
@ derrotado do gatilho, e este ON_TRANSITION so a traduz. Zero var.
TeamGalacticEternaBuilding_3F_OnTransition:
	call_if_defeated TRAINER_SINNOH_COMMANDER_JUPITER_ETERNA_BUILDING, TeamGalacticEternaBuilding_3F_EventScript_HideGalactica_eterna
	end

TeamGalacticEternaBuilding_3F_EventScript_HideGalactica_eterna::
	setflag FLAG_GALACTICA_ETERNA
	return
