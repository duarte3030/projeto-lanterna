@ LcRoute100Coast: mapa copiado de Pokémon Liquid Crystal.gba (g3m94) por
@ dev_scripts/copia_mapa_rom.py. A ARTE é do hack; o JOGO (NPCs, encontros,
@ treinadores, placas, conexão) é NOSSO e está aqui.
@ Os quatro warps do hack, os pares de seta (11,12)/(11,13) e (90,16)/(90,17),
@ NÃO entraram: os dois levavam ao mesmo mapa de túnel do enredo deles, que não
@ vem para este cartucho. No lugar de cada par vai placa em inglês, no molde das
@ portas fechadas de Johto (data/scripts/portas_fechadas.inc).

LcRoute100Coast_MapScripts::
	.byte 0

@ A PORTA da Route 100. No hack ela se alcança surfando da Route 27; aqui a
@ travessia a pé ou a Surf está PROIBIDA, porque o primário desta rota é o
@ gTileset_LcOutdoor e o das nossas rotas de Johto é o JohtoNorthEast, e
@ LoadMapFromCameraTransition (src/overworld.c:911) só recarrega o SECUNDÁRIO.
@ Por isso a ligação é o barco, o mesmo molde do marinheiro de PalletTown_Frlg.
LcRoute100Coast_EventScript_Sailor::
	lock
	faceplayer
	msgbox LcRoute100Coast_Text_SailorAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LcRoute100Coast_EventScript_SailorNo
	msgbox LcRoute100Coast_Text_SailorGo, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	warp MAP_ROUTE27, 31, 21
	waitstate
	release
	end

LcRoute100Coast_EventScript_SailorNo::
	msgbox LcRoute100Coast_Text_SailorNo, MSGBOX_DEFAULT
	release
	end

LcRoute100Coast_EventScript_Ossian::
	trainerbattle_single TRAINER_JOHTO_LC_ROUTE100_OSSIAN, LcRoute100Coast_Text_OssianSeen, LcRoute100Coast_Text_OssianBeaten
	msgbox LcRoute100Coast_Text_OssianAfter, MSGBOX_AUTOCLOSE
	end

LcRoute100Coast_EventScript_Padrig::
	trainerbattle_single TRAINER_JOHTO_LC_ROUTE100_PADRIG, LcRoute100Coast_Text_PadrigSeen, LcRoute100Coast_Text_PadrigBeaten
	msgbox LcRoute100Coast_Text_PadrigAfter, MSGBOX_AUTOCLOSE
	end

LcRoute100Coast_EventScript_Nessa::
	trainerbattle_single TRAINER_JOHTO_LC_ROUTE100_NESSA, LcRoute100Coast_Text_NessaSeen, LcRoute100Coast_Text_NessaBeaten
	msgbox LcRoute100Coast_Text_NessaAfter, MSGBOX_AUTOCLOSE
	end

LcRoute100Coast_EventScript_Corrin::
	trainerbattle_single TRAINER_JOHTO_LC_ROUTE100_CORRIN, LcRoute100Coast_Text_CorrinSeen, LcRoute100Coast_Text_CorrinBeaten
	msgbox LcRoute100Coast_Text_CorrinAfter, MSGBOX_AUTOCLOSE
	end

LcRoute100Coast_EventScript_SignWestTunnel::
	msgbox LcRoute100Coast_Text_SignWestTunnel, MSGBOX_SIGN
	end

LcRoute100Coast_EventScript_SignEastTunnel::
	msgbox LcRoute100Coast_Text_SignEastTunnel, MSGBOX_SIGN
	end

LcRoute100Coast_Text_SailorAsk:
	.string "Back to ROUTE 27?$"

LcRoute100Coast_Text_SailorGo:
	.string "Hop in. Mind the swell.$"

LcRoute100Coast_Text_SailorNo:
	.string "Take your time. The tide won't turn\n"
	.string "until evening.$"

LcRoute100Coast_Text_OssianSeen:
	.string "Nobody fishes this far out. Nobody\n"
	.string "but me.$"

LcRoute100Coast_Text_OssianBeaten:
	.string "And now nobody beats me but you.$"

LcRoute100Coast_Text_OssianAfter:
	.string "ROUTE 100 is all open water past\n"
	.string "that headland.\p"
	.string "Rocks the whole way. Watch your\n"
	.string "keel and watch your POKéMON.$"

LcRoute100Coast_Text_PadrigSeen:
	.string "You swam out here? Then you can\n"
	.string "swim back. After this.$"

LcRoute100Coast_Text_PadrigBeaten:
	.string "Go on, get your feet wet.$"

LcRoute100Coast_Text_PadrigAfter:
	.string "The forest on this cliff has no path\n"
	.string "through it. None at all.\p"
	.string "Everyone who comes here comes by\n"
	.string "water.$"

LcRoute100Coast_Text_NessaSeen:
	.string "The current runs east. So does\n"
	.string "everyone who gets tired.$"

LcRoute100Coast_Text_NessaBeaten:
	.string "You're not tired, clearly.$"

LcRoute100Coast_Text_NessaAfter:
	.string "Keep going east and you'll find the\n"
	.string "old station on the reef.\p"
	.string "It's shut. Has been for years.$"

LcRoute100Coast_Text_CorrinSeen:
	.string "My birds circle the whole route.\n"
	.string "Nothing gets past them.$"

LcRoute100Coast_Text_CorrinBeaten:
	.string "You did.$"

LcRoute100Coast_Text_CorrinAfter:
	.string "There are two tunnel mouths in this\n"
	.string "cliff, one at each end.\p"
	.string "Both were bricked up before I was\n"
	.string "born. Nobody remembers why.$"

LcRoute100Coast_Text_SignWestTunnel:
	.string "WEST TUNNEL\n"
	.string "Closed. The roof came down and\l"
	.string "was never dug out.$"

LcRoute100Coast_Text_SignEastTunnel:
	.string "EAST TUNNEL\n"
	.string "Closed. Use the water.$"
