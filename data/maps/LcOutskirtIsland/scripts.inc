@ LcOutskirtIsland: mapa copiado de Pokémon Liquid Crystal.gba (g3m50) por
@ dev_scripts/copia_mapa_rom.py. A ARTE e do hack; o JOGO (warps, NPCs,
@ encontros, treinadores, placas) e nosso e entra aqui.
@
@ A ilha nao tem conexao de mapa com Kanto, de proposito: o primario dela e o
@ gTileset_LcOutdoor e o de Kanto e outro, e travessia por conexao so recarrega
@ o tileset SECUNDARIO (secao 3.1 do METODO-COPIA-CIDADES.md). A entrada e a
@ saida sao o barco do marinheiro, um warp de script dos dois lados, no mesmo
@ molde do marinheiro que liga Canalave a Olivine.

LcOutskirtIsland_MapScripts::
	.byte 0

@ ---------------------------------------------------------------- o barco

LcOutskirtIsland_EventScript_Sailor::
	lock
	faceplayer
	msgbox LcOutskirtIsland_Text_SailorAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LcOutskirtIsland_EventScript_SailorStay
	msgbox LcOutskirtIsland_Text_SailorGo, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	warp MAP_PALLET_TOWN, 5, 19
	waitstate
	release
	end

LcOutskirtIsland_EventScript_SailorStay::
	msgbox LcOutskirtIsland_Text_SailorStay, MSGBOX_DEFAULT
	release
	end

@ ---------------------------------------------------------------- treinadores

LcOutskirtIsland_EventScript_Castaway::
	trainerbattle_single TRAINER_KANTO_LC_OUTSKIRT_CASTAWAY, LcOutskirtIsland_Text_CastawaySeen, LcOutskirtIsland_Text_CastawayBeaten
	msgbox LcOutskirtIsland_Text_CastawayAfter, MSGBOX_AUTOCLOSE
	end

LcOutskirtIsland_EventScript_Gull::
	trainerbattle_single TRAINER_KANTO_LC_OUTSKIRT_GULL, LcOutskirtIsland_Text_GullSeen, LcOutskirtIsland_Text_GullBeaten
	msgbox LcOutskirtIsland_Text_GullAfter, MSGBOX_AUTOCLOSE
	end

LcOutskirtIsland_EventScript_Ridge::
	trainerbattle_single TRAINER_KANTO_LC_OUTSKIRT_RIDGE, LcOutskirtIsland_Text_RidgeSeen, LcOutskirtIsland_Text_RidgeBeaten
	msgbox LcOutskirtIsland_Text_RidgeAfter, MSGBOX_AUTOCLOSE
	end

LcOutskirtIsland_EventScript_Tide::
	trainerbattle_single TRAINER_KANTO_LC_OUTSKIRT_TIDE, LcOutskirtIsland_Text_TideSeen, LcOutskirtIsland_Text_TideBeaten
	msgbox LcOutskirtIsland_Text_TideAfter, MSGBOX_AUTOCLOSE
	end

@ ---------------------------------------------------------------- gente e placas

LcOutskirtIsland_EventScript_Beachcomber::
	msgbox LcOutskirtIsland_Text_Beachcomber, MSGBOX_NPC
	end

LcOutskirtIsland_EventScript_SignLanding::
	msgbox LcOutskirtIsland_Text_SignLanding, MSGBOX_SIGN
	end

LcOutskirtIsland_EventScript_SignPeak::
	msgbox LcOutskirtIsland_Text_SignPeak, MSGBOX_SIGN
	end

LcOutskirtIsland_EventScript_SignSouthShore::
	msgbox LcOutskirtIsland_Text_SignSouthShore, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- texto, em INGLES

LcOutskirtIsland_Text_SailorAsk:
	.string "Sail back to PALLET TOWN?$"

LcOutskirtIsland_Text_SailorGo:
	.string "Mind the swell. Here we go!$"

LcOutskirtIsland_Text_SailorStay:
	.string "Take your time. The tide won't\n"
	.string "turn before evening.$"

LcOutskirtIsland_Text_CastawaySeen:
	.string "Three days on this beach and you\n"
	.string "are the first face I've seen!$"

LcOutskirtIsland_Text_CastawayBeaten:
	.string "Washed up all over again…$"

LcOutskirtIsland_Text_CastawayAfter:
	.string "My raft broke up on the reef out\n"
	.string "west. The current here is cruel.\p"
	.string "If you swim off this island, swim\n"
	.string "north. Never south.$"

LcOutskirtIsland_Text_GullSeen:
	.string "Nobody camps this far out unless\n"
	.string "they mean it. Show me you mean it!$"

LcOutskirtIsland_Text_GullBeaten:
	.string "My tent pegs held. I didn't.$"

LcOutskirtIsland_Text_GullAfter:
	.string "The grass up here grows thick\n"
	.string "because no road ever crossed it.\p"
	.string "Step in and something will look\n"
	.string "back at you.$"

LcOutskirtIsland_Text_RidgeSeen:
	.string "I climbed the ridge for the view\n"
	.string "and stayed for the battles!$"

LcOutskirtIsland_Text_RidgeBeaten:
	.string "The view is still worth it.$"

LcOutskirtIsland_Text_RidgeAfter:
	.string "From the top you can see the whole\n"
	.string "island at once.\p"
	.string "It's small. It's just far.$"

LcOutskirtIsland_Text_TideSeen:
	.string "The fishing is good here because\n"
	.string "nobody comes. Now somebody came!$"

LcOutskirtIsland_Text_TideBeaten:
	.string "Line snapped. Fair enough.$"

LcOutskirtIsland_Text_TideAfter:
	.string "Cast off the south shore at slack\n"
	.string "water and you'll never go hungry.\p"
	.string "Cast at the turn and the current\n"
	.string "takes your rod.$"

LcOutskirtIsland_Text_Beachcomber:
	.string "I walk this beach every morning\n"
	.string "and it gives me something back.\p"
	.string "Shells, glass, a crate once.\n"
	.string "The sea keeps no secrets long.$"

LcOutskirtIsland_Text_SignLanding:
	.string "OUTSKIRT ISLAND\n"
	.string "Landing beach. No harbour, no\l"
	.string "shelter, no help.$"

LcOutskirtIsland_Text_SignPeak:
	.string "THE RIDGE\n"
	.string "From here the mainland is a\l"
	.string "rumour on the water.$"

LcOutskirtIsland_Text_SignSouthShore:
	.string "SOUTH SHORE\n"
	.string "Open sea from this line on.\l"
	.string "Surf only with a full team.$"
