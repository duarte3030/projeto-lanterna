@ FoothillTown: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 0.17) por dev_scripts/copia_planta_ex.py.

FoothillTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, FoothillTown_OnTransition
	.byte 0

FoothillTown_OnTransition:
	setflag FLAG_VISITED_FOOTHILL_TOWN
	end

@ Eventos novos do Pokémon Emerald EX (mapa 0.17), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
FoothillTown_EventScript_ExNpc0::
	msgbox FoothillTown_Text_ExNpc0, MSGBOX_NPC
	end

FoothillTown_Text_ExNpc0:
	.string "In the hut, just up the hill, there’s the\n"
	.string "man that caught a powerful POKéMON\l"
	.string "from this lake.$"

FoothillTown_EventScript_ExNpc1::
	msgbox FoothillTown_Text_ExNpc1, MSGBOX_NPC
	end

FoothillTown_Text_ExNpc1:
	.string "This lake is much deeper than it seems.\n"
	.string "I tied a weight to my line and it went\l"
	.string "super deep!$"

FoothillTown_EventScript_ExNpc2::
	msgbox FoothillTown_Text_ExNpc2, MSGBOX_NPC
	end

FoothillTown_Text_ExNpc2:
	.string "Could this lake really house such a\n"
	.string "large creature?$"

FoothillTown_EventScript_ExNpc3::
	msgbox FoothillTown_Text_ExNpc3, MSGBOX_NPC
	end

FoothillTown_Text_ExNpc3:
	.string "Weak POKéMON...\n"
	.string "Powerful POKéMON...\p"
	.string "I think the difference is in the\n"
	.string "TRAINER.$"

FoothillTown_EventScript_ExNpc4::
	msgbox FoothillTown_Text_ExNpc4, MSGBOX_NPC
	end

FoothillTown_Text_ExNpc4:
	.string "Some MARTS have special ITEMS that are\n"
	.string "only sold at one store.$"

FoothillTown_EventScript_ExNpc5::
	msgbox FoothillTown_Text_ExNpc5, MSGBOX_NPC
	end

FoothillTown_Text_ExNpc5:
	.string "There’s a strange couple living in this\n"
	.string "house...\p"
	.string "I’m practicing my reflexes in case they\n"
	.string "try anything!$"

FoothillTown_EventScript_ExNpc6::
	msgbox FoothillTown_Text_ExNpc6, MSGBOX_NPC
	end

FoothillTown_Text_ExNpc6:
	.string "Do you run around in the TALL GRASS\n"
	.string "very often?\n"
	.string "I do!\p"
	.string "But running into WILD POKéMON\n"
	.string "sometimes makes me run late.$"

FoothillTown_EventScript_ExNpc7::
	msgbox FoothillTown_Text_ExNpc7, MSGBOX_NPC
	end

FoothillTown_Text_ExNpc7:
	.string "An old lady and her POKéMON used to live\n"
	.string "in the house up the ledge over there.\p"
	.string "But it has been abandoned ever since\n"
	.string "she passed.$"

FoothillTown_EventScript_ExNpc8::
	msgbox FoothillTown_Text_ExNpc8, MSGBOX_NPC
	end

FoothillTown_Text_ExNpc8:
	.string "I think this town is going to continue\n"
	.string "to grow.\p"
	.string "If they finish RUSTBORO TUNNEL than\n"
	.string "FOOTHILL TOWN will get lots of\l"
	.string "travelers!$"

FoothillTown_EventScript_ExNpc9::
	msgbox FoothillTown_Text_ExNpc9, MSGBOX_NPC
	end

FoothillTown_Text_ExNpc9:
	.string "Gotta keep running!\n"
	.string "Gotta keep running!\l"
	.string "Gotta keep running!$"

FoothillTown_EventScript_ExNpc10::
	msgbox FoothillTown_Text_ExNpc10, MSGBOX_NPC
	end

FoothillTown_Text_ExNpc10:
	.string "GASP GASP...\p"
	.string "I’ve gotta take a break...$"

FoothillTown_EventScript_ExSign0::
	msgbox FoothillTown_Text_ExSign0, MSGBOX_SIGN
	end

FoothillTown_Text_ExSign0:
	.string "“Selected items for your convenience!”\n"
	.string "POKéMON MART$"

FoothillTown_EventScript_ExSign1::
	msgbox FoothillTown_Text_ExSign1, MSGBOX_SIGN
	end

FoothillTown_Text_ExSign1:
	.string "“Selected items for your convenience!”\n"
	.string "POKéMON MART$"

FoothillTown_EventScript_ExSign2::
	msgbox FoothillTown_Text_ExSign2, MSGBOX_SIGN
	end

FoothillTown_Text_ExSign2:
	.string "“Rejuvenate your tired partners!”\n"
	.string "POKéMON CENTER$"

FoothillTown_EventScript_ExSign3::
	msgbox FoothillTown_Text_ExSign3, MSGBOX_SIGN
	end

FoothillTown_Text_ExSign3:
	.string "“Rejuvenate your tired partners!”\n"
	.string "POKéMON CENTER$"

FoothillTown_EventScript_ExSign4::
	msgbox FoothillTown_Text_ExSign4, MSGBOX_SIGN
	end

FoothillTown_Text_ExSign4:
	.string "FISHING DOJO.$"

FoothillTown_EventScript_ExSign5::
	msgbox FoothillTown_Text_ExSign5, MSGBOX_SIGN
	end

FoothillTown_Text_ExSign5:
	.string "FOOTHILL TOWN.$"

