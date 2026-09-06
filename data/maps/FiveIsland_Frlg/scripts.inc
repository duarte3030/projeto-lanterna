FiveIsland_Frlg_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, FiveIsland_OnTransition
	.byte 0

FiveIsland_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_FIVE_ISLAND
	end

FiveIsland_EventScript_IslandSign::
	msgbox FiveIsland_Text_IslandSign, MSGBOX_SIGN
	end

FiveIsland_EventScript_BugCatcher::
	msgbox FiveIsland_Text_WeirdBuildingInMeadow, MSGBOX_NPC
	end

FiveIsland_EventScript_Fisher::
	msgbox FiveIsland_Text_BeenGettingBusierAroundHere, MSGBOX_NPC
	end

FiveIsland_Text_IslandSign::
	.string "FIVE ISLAND\n"
	.string "Chrono Island: Where Time Goes$"

FiveIsland_Text_WeirdBuildingInMeadow::
	.string "Oh, this stinks. I wanted to play in\n"
	.string "the MEADOW.\p"
	.string "But they put up a weird building\n"
	.string "on it, so I can't play there.$"

FiveIsland_Text_BeenGettingBusierAroundHere::
	.string "It's been getting busier around\n"
	.string "these parts lately.\p"
	.string "I haven't been catching many good\n"
	.string "fish lately, either.$"

@ >>> Povoamento: os 10 NPCs por cidade (dev_scripts/povoa_cidades.py) >>>
@ Lei do Gui de 07/09/2026: toda cidade do cartucho 1 tem pelo menos 10 NPCs.
@ Bloco GERADO. Para mudar fala ou posicao, edite dev_scripts/povoa_cidades.json
@ e rode `python3 dev_scripts/povoa_cidades.py --aplica`.

FiveIsland_EventScript_Povoa1::
	lock
	faceplayer
	msgbox FiveIsland_Text_Povoa1, MSGBOX_DEFAULT
	release
	end

FiveIsland_Text_Povoa1:
	.string "FIVE ISLE MEADOW is east.\nBerries grow wild out there.$"

FiveIsland_EventScript_Povoa2::
	lock
	faceplayer
	msgbox FiveIsland_Text_Povoa2, MSGBOX_DEFAULT
	release
	end

FiveIsland_Text_Povoa2:
	.string "The WATER LABYRINTH is north.\nPeople trade odd Pokémon there.$"

FiveIsland_EventScript_Povoa3::
	lock
	faceplayer
	msgbox FiveIsland_Text_Povoa3, MSGBOX_DEFAULT
	release
	end

FiveIsland_Text_Povoa3:
	.string "The harbour is the only way in\nand the only way out.$"

FiveIsland_EventScript_Povoa4::
	lock
	faceplayer
	msgbox FiveIsland_Text_Povoa4, MSGBOX_DEFAULT
	release
	end

FiveIsland_Text_Povoa4:
	.string "Five islands down, two to go.\nThat is how I count my life.$"

FiveIsland_EventScript_Povoa5::
	lock
	faceplayer
	msgbox FiveIsland_Text_Povoa5, MSGBOX_DEFAULT
	release
	end

FiveIsland_Text_Povoa5:
	.string "It rains here more than on the\nother islands. I like it.$"

FiveIsland_EventScript_Povoa6::
	lock
	faceplayer
	msgbox FiveIsland_Text_Povoa6, MSGBOX_DEFAULT
	release
	end

FiveIsland_Text_Povoa6:
	.string "Berries a Pokémon holds get\neaten in battle, on their own.$"

FiveIsland_EventScript_Povoa7::
	lock
	faceplayer
	msgbox FiveIsland_Text_Povoa7, MSGBOX_DEFAULT
	release
	end

FiveIsland_Text_Povoa7:
	.string "I found a shell on the beach\nshaped like a POKé BALL.$"

FiveIsland_EventScript_Povoa8::
	lock
	faceplayer
	msgbox FiveIsland_Text_Povoa8, MSGBOX_DEFAULT
	release
	end

FiveIsland_Text_Povoa8:
	.string "Nothing hurries here. Not even\nthe ferry.$"

@ <<< Povoamento: fim do bloco gerado <<<
