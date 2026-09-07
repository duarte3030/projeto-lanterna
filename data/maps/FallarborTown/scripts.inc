FallarborTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, FallarborTown_OnTransition
	.byte 0

FallarborTown_OnTransition:
	setflag FLAG_VISITED_FALLARBOR_TOWN
	setvar VAR_CONTEST_HALL_STATE, 0
	clearflag FLAG_CONTEST_SKETCH_CREATED
	end

FallarborTown_EventScript_ExpertM::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_EVIL_TEAM_MT_CHIMNEY, FallarborTown_EventScript_ExpertMNormal
	msgbox FallarborTown_Text_ShadyCharactersCozmosHome, MSGBOX_DEFAULT
	release
	end

FallarborTown_EventScript_ExpertMNormal::
	msgbox FallarborTown_Text_RegionKnownForMeteors, MSGBOX_DEFAULT
	release
	end

FallarborTown_EventScript_Girl::
	msgbox FallarborTown_Text_MyPreciousAzurill, MSGBOX_NPC
	end

FallarborTown_EventScript_Gentleman::
	msgbox FallarborTown_Text_HaveYouChallengedFlannery, MSGBOX_NPC
	end

FallarborTown_EventScript_Azurill::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_AZURILL, CRY_MODE_NORMAL
	msgbox FallarborTown_Text_Azurill, MSGBOX_DEFAULT
	waitmoncry
	release
	end

FallarborTown_EventScript_BattleTentSign::
	msgbox FallarborTown_Text_BattleTentSign, MSGBOX_SIGN
	end

FallarborTown_EventScript_TownSign::
	msgbox FallarborTown_Text_TownSign, MSGBOX_SIGN
	end

FallarborTown_EventScript_MoveTutorSign::
	msgbox FallarborTown_Text_MoveTutorSign, MSGBOX_SIGN
	end

FallarborTown_Text_ShadyCharactersCozmosHome:
	.string "Something's happening,\n"
	.string "and I don't like it!\p"
	.string "I've seen shady characters wandering\n"
	.string "in and out of PROF. COZMO's home…$"

FallarborTown_Text_RegionKnownForMeteors:
	.string "This region's been known for meteors\n"
	.string "since the olden days.\p"
	.string "They say METEOR FALLS was gouged out\n"
	.string "by a falling meteorite long ago.$"

FallarborTown_Text_MyPreciousAzurill:
	.string "See! Take a look!\n"
	.string "This is my precious AZURILL!\p"
	.string "It's slick and smooth and plushy, too!$"

FallarborTown_Text_Azurill:
	.string "AZURILL: Rooreelooo.$"

FallarborTown_Text_HaveYouChallengedFlannery:
	.string "Have you already challenged FLANNERY,\n"
	.string "the LEADER of LAVARIDGE GYM?\p"
	.string "The girl's grandfather was famous.\n"
	.string "He was one of the ELITE FOUR in the\l"
	.string "POKéMON LEAGUE at one point.\p"
	.string "It wouldn't surprise me to see FLANNERY\n"
	.string "become a great TRAINER in her own\l"
	.string "right.$"

FallarborTown_Text_BattleTentSign:
	.string "BATTLE TENT FALLARBOR SITE\n"
	.string "“May the Greatest Teams Gather!”$"

FallarborTown_Text_TownSign:
	.string "FALLARBOR TOWN\n"
	.string "“A farm community with small gardens.”$"

FallarborTown_Text_MoveTutorSign:
	.string "MOVE TUTOR'S HOUSE\n"
	.string "“New moves taught to POKéMON.”$"

@ >>> Povoamento: os 10 NPCs por cidade (dev_scripts/povoa_cidades.py) >>>
@ Lei do Gui de 07/09/2026: toda cidade do cartucho 1 tem pelo menos 10 NPCs.
@ Bloco GERADO. Para mudar fala ou posicao, edite dev_scripts/povoa_cidades.json
@ e rode `python3 dev_scripts/povoa_cidades.py --aplica`.

FallarborTown_EventScript_Povoa1::
	lock
	faceplayer
	msgbox FallarborTown_Text_Povoa1, MSGBOX_DEFAULT
	release
	end

FallarborTown_Text_Povoa1:
	.string "PROF. COZMO studies the sky\nfrom this dusty little town.$"

FallarborTown_EventScript_Povoa2::
	lock
	faceplayer
	msgbox FallarborTown_Text_Povoa2, MSGBOX_DEFAULT
	release
	end

FallarborTown_Text_Povoa2:
	.string "Ash falls here when the volcano\nstirs. We sweep, and go on.$"

FallarborTown_EventScript_Povoa3::
	lock
	faceplayer
	msgbox FallarborTown_Text_Povoa3, MSGBOX_DEFAULT
	release
	end

FallarborTown_Text_Povoa3:
	.string "The MOVE RELEARNER lives here.\nForgotten moves come back.$"

FallarborTown_EventScript_Povoa4::
	lock
	faceplayer
	msgbox FallarborTown_Text_Povoa4, MSGBOX_DEFAULT
	release
	end

FallarborTown_Text_Povoa4:
	.string "ROUTE 114 west, ROUTE 113 east.\nThe ash road is east.$"

FallarborTown_EventScript_Povoa5::
	lock
	faceplayer
	msgbox FallarborTown_Text_Povoa5, MSGBOX_DEFAULT
	release
	end

FallarborTown_Text_Povoa5:
	.string "The BATTLE TENT takes anyone.\nWinning is another matter.$"

FallarborTown_EventScript_Povoa6::
	lock
	faceplayer
	msgbox FallarborTown_Text_Povoa6, MSGBOX_DEFAULT
	release
	end

FallarborTown_Text_Povoa6:
	.string "Soot from the ash road can be\ncollected. Glass is made from it.$"

FallarborTown_EventScript_Povoa7::
	lock
	faceplayer
	msgbox FallarborTown_Text_Povoa7, MSGBOX_DEFAULT
	release
	end

FallarborTown_Text_Povoa7:
	.string "I wrote my name in the ash and\nthe wind took it.$"

@ <<< Povoamento: fim do bloco gerado <<<
