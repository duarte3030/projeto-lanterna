@ LcNewIslandEntrance: mapa copiado de Pokémon Liquid Crystal.gba (g4m30) por
@ dev_scripts/copia_mapa_rom.py. A ARTE e do hack; o JOGO e nosso.
@ Esta e a sala do CAIS: o barco de CINNABAR ISLAND chega aqui, e o marinheiro
@ daqui leva de volta. A ligacao com Kanto e warp de SCRIPT nos dois sentidos,
@ pelo mesmo motivo da Outskirt Island (primario proprio, secao 3.1 do metodo).

LcNewIslandEntrance_MapScripts::
	.byte 0

LcNewIslandEntrance_EventScript_Sailor::
	lock
	faceplayer
	msgbox LcNewIslandEntrance_Text_SailorAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LcNewIslandEntrance_EventScript_SailorStay
	msgbox LcNewIslandEntrance_Text_SailorGo, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	warp MAP_CINNABAR_ISLAND, 19, 14
	waitstate
	release
	end

LcNewIslandEntrance_EventScript_SailorStay::
	msgbox LcNewIslandEntrance_Text_SailorStay, MSGBOX_DEFAULT
	release
	end

LcNewIslandEntrance_EventScript_SignHall::
	msgbox LcNewIslandEntrance_Text_SignHall, MSGBOX_SIGN
	end

LcNewIslandEntrance_Text_SailorAsk:
	.string "Sail back to CINNABAR ISLAND?$"

LcNewIslandEntrance_Text_SailorGo:
	.string "Good. I don't like this place.$"

LcNewIslandEntrance_Text_SailorStay:
	.string "I'll keep the engine warm.$"

LcNewIslandEntrance_Text_SignHall:
	.string "RECEPTION\n"
	.string "Guests of NEW ISLAND, leave your\l"
	.string "boats at the stage.$"
