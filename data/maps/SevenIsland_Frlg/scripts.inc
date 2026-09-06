SevenIsland_Frlg_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SevenIsland_OnTransition
	.byte 0

SevenIsland_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_SEVEN_ISLAND
	end

SevenIsland_EventScript_IslandSign::
	msgbox SevenIsland_Text_IslandSign, MSGBOX_SIGN
	end

SevenIsland_EventScript_OldWoman::
	msgbox SevenIsland_Text_IslandsMadeInSevenDays, MSGBOX_NPC
	end

SevenIsland_EventScript_Scientist::
	msgbox SevenIsland_Text_IslandVirtuallyUntouched, MSGBOX_NPC
	end

Text_SwordsDanceTeach::
	.string "Not many people come out here.\p"
	.string "If I train here, I'm convinced that\n"
	.string "I'll get stronger and stronger.\p"
	.string "Yep, stronger and stronger…\p"
	.string "How would you like to learn a move\n"
	.string "like that? It's SWORDS DANCE.$"

Text_SwordsDanceDeclined::
	.string "Well, that's fine, too.$"

Text_SwordsDanceWhichMon::
	.string "All right, pick which POKéMON\n"
	.string "I should teach it to.$"

Text_SwordsDanceTaught::
	.string "If only we could keep getting\n"
	.string "stronger and stronger, eh?$"

SevenIsland_Text_IslandSign::
	.string "SEVEN ISLAND\n"
	.string "Quest Island of Infinity$"

SevenIsland_Text_IslandsMadeInSevenDays::
	.string "These islands are called the SEVII\n"
	.string "ISLANDS because there are seven.\p"
	.string "…Or at least that's what the young\n"
	.string "people believe.\p"
	.string "The truth is, these islands are so\n"
	.string "named because they are said to\l"
	.string "have been made in seven days.$"

SevenIsland_Text_IslandVirtuallyUntouched::
	.string "This island has been left virtually\n"
	.string "untouched in its natural state.\p"
	.string "It could be a little difficult to\n"
	.string "hike around because of that.$"

@ >>> Povoamento: os 10 NPCs por cidade (dev_scripts/povoa_cidades.py) >>>
@ Lei do Gui de 07/09/2026: toda cidade do cartucho 1 tem pelo menos 10 NPCs.
@ Bloco GERADO. Para mudar fala ou posicao, edite dev_scripts/povoa_cidades.json
@ e rode `python3 dev_scripts/povoa_cidades.py --aplica`.

SevenIsland_EventScript_Povoa1::
	lock
	faceplayer
	msgbox SevenIsland_Text_Povoa1, MSGBOX_DEFAULT
	release
	end

SevenIsland_Text_Povoa1:
	.string "TRAINER TOWER is north. Floor\nafter floor, no rest between.$"

SevenIsland_EventScript_Povoa2::
	lock
	faceplayer
	msgbox SevenIsland_Text_Povoa2, MSGBOX_DEFAULT
	release
	end

SevenIsland_Text_Povoa2:
	.string "The TANOBY RUINS hold writing\nnobody has finished reading.$"

SevenIsland_EventScript_Povoa3::
	lock
	faceplayer
	msgbox SevenIsland_Text_Povoa3, MSGBOX_DEFAULT
	release
	end

SevenIsland_Text_Povoa3:
	.string "SEVAULT CANYON is south, and the\nrock down there bites.$"

SevenIsland_EventScript_Povoa4::
	lock
	faceplayer
	msgbox SevenIsland_Text_Povoa4, MSGBOX_DEFAULT
	release
	end

SevenIsland_Text_Povoa4:
	.string "Last island of the seven.\nThe road ends at the water.$"

SevenIsland_EventScript_Povoa5::
	lock
	faceplayer
	msgbox SevenIsland_Text_Povoa5, MSGBOX_DEFAULT
	release
	end

SevenIsland_Text_Povoa5:
	.string "I came for a week. That was\nfour years ago.$"

SevenIsland_EventScript_Povoa6::
	lock
	faceplayer
	msgbox SevenIsland_Text_Povoa6, MSGBOX_DEFAULT
	release
	end

SevenIsland_Text_Povoa6:
	.string "The tower keeps a record of\nevery run. Mine is bad.$"

SevenIsland_EventScript_Povoa7::
	lock
	faceplayer
	msgbox SevenIsland_Text_Povoa7, MSGBOX_DEFAULT
	release
	end

SevenIsland_Text_Povoa7:
	.string "From here you can see nothing\nbut sea. I find that restful.$"

@ <<< Povoamento: fim do bloco gerado <<<
