@ LcSilverCaveMain: mapa copiado de Pokémon Liquid Crystal.gba (g4m96) por
@ dev_scripts/copia_mapa_rom.py. A ARTE é do hack; o JOGO é NOSSO.
@ O quinto warp do hack, em (4,14), NÃO entrou: lá ele saía para um mapa de
@ Johto do enredo deles, e o bolsão de 28 tiles em volta dele não se liga ao
@ resto do mapa (medido nesta árvore), então o jogador nunca chega lá. Sem warp
@ e sem placa, ele é cenário.

LcSilverCaveMain_MapScripts::
	.byte 0

LcSilverCaveMain_EventScript_Eirik::
	trainerbattle_single TRAINER_JOHTO_LC_SILVER_EIRIK, LcSilverCaveMain_Text_EirikSeen, LcSilverCaveMain_Text_EirikBeaten
	msgbox LcSilverCaveMain_Text_EirikAfter, MSGBOX_AUTOCLOSE
	end

LcSilverCaveMain_EventScript_Maret::
	trainerbattle_single TRAINER_JOHTO_LC_SILVER_MARET, LcSilverCaveMain_Text_MaretSeen, LcSilverCaveMain_Text_MaretBeaten
	msgbox LcSilverCaveMain_Text_MaretAfter, MSGBOX_AUTOCLOSE
	end

LcSilverCaveMain_EventScript_Tovald::
	trainerbattle_single TRAINER_JOHTO_LC_SILVER_TOVALD, LcSilverCaveMain_Text_TovaldSeen, LcSilverCaveMain_Text_TovaldBeaten
	msgbox LcSilverCaveMain_Text_TovaldAfter, MSGBOX_AUTOCLOSE
	end

LcSilverCaveMain_EventScript_Kelda::
	trainerbattle_single TRAINER_JOHTO_LC_SILVER_KELDA, LcSilverCaveMain_Text_KeldaSeen, LcSilverCaveMain_Text_KeldaBeaten
	msgbox LcSilverCaveMain_Text_KeldaAfter, MSGBOX_AUTOCLOSE
	end

LcSilverCaveMain_EventScript_SignMain::
	msgbox LcSilverCaveMain_Text_SignMain, MSGBOX_SIGN
	end

LcSilverCaveMain_Text_EirikSeen:
	.string "Water on the second level. Nobody\n"
	.string "believes me until they see it.$"

LcSilverCaveMain_Text_EirikBeaten:
	.string "Soaked and beaten.$"

LcSilverCaveMain_Text_EirikAfter:
	.string "Three doors on this level, and all\n"
	.string "three go to the same dead ends.\p"
	.string "Different dead ends, mind. Each one\n"
	.string "worth the walk.$"

LcSilverCaveMain_Text_MaretSeen:
	.string "You'll need SURF past here, and\n"
	.string "nerve as well.$"

LcSilverCaveMain_Text_MaretBeaten:
	.string "You had both. I only had one.$"

LcSilverCaveMain_Text_MaretAfter:
	.string "The falls come out of the rock and\n"
	.string "go straight back into it.\p"
	.string "Nobody has found where the water\n"
	.string "ends up.$"

LcSilverCaveMain_Text_TovaldSeen:
	.string "Turn back at the falls if you're\n"
	.string "sensible. You're not, are you?$"

LcSilverCaveMain_Text_TovaldBeaten:
	.string "No, you're not.$"

LcSilverCaveMain_Text_TovaldAfter:
	.string "The ice on the walls never melts,\n"
	.string "and the water never freezes.\p"
	.string "I gave up asking why.$"

LcSilverCaveMain_Text_KeldaSeen:
	.string "Every crystal in this wall grew\n"
	.string "here. Don't chip at them.$"

LcSilverCaveMain_Text_KeldaBeaten:
	.string "Fine. Take the path, leave the\n"
	.string "stone.$"

LcSilverCaveMain_Text_KeldaAfter:
	.string "The three rooms above are older\n"
	.string "than the cave around them.\p"
	.string "Somebody cut them. Nobody will say\n"
	.string "who.$"

LcSilverCaveMain_Text_SignMain:
	.string "SILVER CAVE, SECOND LEVEL\n"
	.string "Deep water ahead.\l"
	.string "Three doors, three dead ends.$"
