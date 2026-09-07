SixIsland_Frlg_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SixIsland_OnTransition
	.byte 0

SixIsland_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_SIX_ISLAND
	end

SixIsland_EventScript_Hiker::
	msgbox SixIsland_Text_ThatWayToWaterPathRuinValley, MSGBOX_NPC
	end

SixIsland_EventScript_Boy::
	msgbox SixIsland_Text_SkyAtNightIsFantastic, MSGBOX_NPC
	end

SixIsland_EventScript_IslandSign::
	msgbox SixIsland_Text_IslandSign, MSGBOX_SIGN
	end

SixIsland_Text_IslandSign::
	.string "SIX ISLAND\n"
	.string "Fortune Island of Aged Wisdom$"

SixIsland_Text_ThatWayToWaterPathRuinValley::
	.string "Keep going this way and you'll get\n"
	.string "to the WATER PATH.\p"
	.string "Stay on that and you'll get to\n"
	.string "the RUIN VALLEY.$"

SixIsland_Text_SkyAtNightIsFantastic::
	.string "When you're this far away from the\n"
	.string "city, the sky at night is fantastic.$"

@ >>> Povoamento: os 10 NPCs por cidade (dev_scripts/povoa_cidades.py) >>>
@ Lei do Gui de 07/09/2026: toda cidade do cartucho 1 tem pelo menos 10 NPCs.
@ Bloco GERADO. Para mudar fala ou posicao, edite dev_scripts/povoa_cidades.json
@ e rode `python3 dev_scripts/povoa_cidades.py --aplica`.

SixIsland_EventScript_Povoa1::
	lock
	faceplayer
	msgbox SixIsland_Text_Povoa1, MSGBOX_DEFAULT
	release
	end

SixIsland_Text_Povoa1:
	.string "The WATER PATH east splits in\nthree. Choose wrong and you swim.$"

SixIsland_EventScript_Povoa2::
	lock
	faceplayer
	msgbox SixIsland_Text_Povoa2, MSGBOX_DEFAULT
	release
	end

SixIsland_Text_Povoa2:
	.string "PATTERN BUSH is a maze of hedges\nand bug catchers.$"

SixIsland_EventScript_Povoa3::
	lock
	faceplayer
	msgbox SixIsland_Text_Povoa3, MSGBOX_DEFAULT
	release
	end

SixIsland_Text_Povoa3:
	.string "ALTERING CAVE changes what lives\ninside it. Nobody agrees why.$"

SixIsland_EventScript_Povoa4::
	lock
	faceplayer
	msgbox SixIsland_Text_Povoa4, MSGBOX_DEFAULT
	release
	end

SixIsland_Text_Povoa4:
	.string "The DOTTED HOLE is sealed.\nOnly the right key opens it.$"

SixIsland_EventScript_Povoa5::
	lock
	faceplayer
	msgbox SixIsland_Text_Povoa5, MSGBOX_DEFAULT
	release
	end

SixIsland_Text_Povoa5:
	.string "I swim the channel every morning.\nThe current is honest work.$"

SixIsland_EventScript_Povoa6::
	lock
	faceplayer
	msgbox SixIsland_Text_Povoa6, MSGBOX_DEFAULT
	release
	end

SixIsland_Text_Povoa6:
	.string "Six is my favourite number now\nthat I live here.$"

SixIsland_EventScript_Povoa7::
	lock
	faceplayer
	msgbox SixIsland_Text_Povoa7, MSGBOX_DEFAULT
	release
	end

SixIsland_Text_Povoa7:
	.string "Sleep in the PokéCENTER, not on\nthe beach. Trust me.$"

SixIsland_EventScript_Povoa8::
	lock
	faceplayer
	msgbox SixIsland_Text_Povoa8, MSGBOX_DEFAULT
	release
	end

SixIsland_Text_Povoa8:
	.string "The sunsets here are the reason\nI never left.$"

@ <<< Povoamento: fim do bloco gerado <<<
