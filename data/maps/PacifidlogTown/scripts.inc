PacifidlogTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, PacifidlogTown_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, PacifidlogTown_OnResume
	.byte 0

PacifidlogTown_OnTransition:
	setflag FLAG_VISITED_PACIFIDLOG_TOWN
	end

PacifidlogTown_OnResume:
	setstepcallback STEP_CB_PACIFIDLOG_BRIDGE
	end

PacifidlogTown_EventScript_NinjaBoy::
	msgbox PacifidlogTown_Text_NeatHousesOnWater, MSGBOX_NPC
	end

PacifidlogTown_EventScript_Girl::
	msgbox PacifidlogTown_Text_FastRunningCurrent, MSGBOX_NPC
	end

PacifidlogTown_EventScript_Fisherman::
	msgbox PacifidlogTown_Text_SkyPillarTooScary, MSGBOX_NPC
	end

PacifidlogTown_EventScript_TownSign::
	msgbox PacifidlogTown_Text_TownSign, MSGBOX_SIGN
	end

PacifidlogTown_Text_FastRunningCurrent:
	.string "The sea between PACIFIDLOG and\n"
	.string "SLATEPORT has a fast-running tide.\p"
	.string "If you decide to SURF, you could end\n"
	.string "up swept away somewhere else.$"

PacifidlogTown_Text_NeatHousesOnWater:
	.string "See, isn't it neat?\n"
	.string "These houses are on water!\p"
	.string "I was born here!$"

PacifidlogTown_Text_SkyPillarTooScary:
	.string "The SKY PILLAR?\p"
	.string "…Oh, you must mean that tall, tall\n"
	.string "tower a little further out.\p"
	.string "If you asked me, I wouldn't climb it.\n"
	.string "It's too scary to get up that high.\p"
	.string "Life at sea level in PACIFIDLOG,\n"
	.string "that suits me fine.$"

PacifidlogTown_Text_TownSign:
	.string "PACIFIDLOG TOWN\p"
	.string "“Where the morning sun smiles upon\n"
	.string "the waters.”$"

@ >>> Povoamento: os 10 NPCs por cidade (dev_scripts/povoa_cidades.py) >>>
@ Lei do Gui de 07/09/2026: toda cidade do cartucho 1 tem pelo menos 10 NPCs.
@ Bloco GERADO. Para mudar fala ou posicao, edite dev_scripts/povoa_cidades.json
@ e rode `python3 dev_scripts/povoa_cidades.py --aplica`.

PacifidlogTown_EventScript_Povoa1::
	lock
	faceplayer
	msgbox PacifidlogTown_Text_Povoa1, MSGBOX_DEFAULT
	release
	end

PacifidlogTown_Text_Povoa1:
	.string "The whole town floats on logs.\nMind your step at night.$"

PacifidlogTown_EventScript_Povoa2::
	lock
	faceplayer
	msgbox PacifidlogTown_Text_Povoa2, MSGBOX_DEFAULT
	release
	end

PacifidlogTown_Text_Povoa2:
	.string "The currents past town push you\nwhere they please. Mind them.$"

PacifidlogTown_EventScript_Povoa3::
	lock
	faceplayer
	msgbox PacifidlogTown_Text_Povoa3, MSGBOX_DEFAULT
	release
	end

PacifidlogTown_Text_Povoa3:
	.string "No grass, no trees, no roads.\nJust water and neighbours.$"

PacifidlogTown_EventScript_Povoa4::
	lock
	faceplayer
	msgbox PacifidlogTown_Text_Povoa4, MSGBOX_DEFAULT
	release
	end

PacifidlogTown_Text_Povoa4:
	.string "ROUTE 131 east, ROUTE 132 west.\nBoth need SURF.$"

PacifidlogTown_EventScript_Povoa5::
	lock
	faceplayer
	msgbox PacifidlogTown_Text_Povoa5, MSGBOX_DEFAULT
	release
	end

PacifidlogTown_Text_Povoa5:
	.string "I learned to swim before I\nlearned to walk here.$"

PacifidlogTown_EventScript_Povoa6::
	lock
	faceplayer
	msgbox PacifidlogTown_Text_Povoa6, MSGBOX_DEFAULT
	release
	end

PacifidlogTown_Text_Povoa6:
	.string "Storms shake the logs, and the\nhouses hold. Every time.$"

PacifidlogTown_EventScript_Povoa7::
	lock
	faceplayer
	msgbox PacifidlogTown_Text_Povoa7, MSGBOX_DEFAULT
	release
	end

PacifidlogTown_Text_Povoa7:
	.string "The fish here come right up to\nthe boards. They are not shy.$"

@ <<< Povoamento: fim do bloco gerado <<<
