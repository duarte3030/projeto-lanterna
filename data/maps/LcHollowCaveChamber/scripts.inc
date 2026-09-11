@ LcHollowCaveChamber: mapa copiado de Pokémon Liquid Crystal.gba (g2m104) por
@ dev_scripts/copia_mapa_rom.py. A ARTE e do hack; o JOGO (warps, NPCs,
@ encontros, treinadores, placas) e nosso e entra aqui.
@
@ E a sala do fundo, com o piso de areia clara no meio. O unico tile de warp
@ dela, (7,14), volta para o degrau de onde se veio: uma porta, uma volta, que e
@ a regra 0 do valida_conectividade.py.

LcHollowCaveChamber_MapScripts::
	.byte 0

LcHollowCaveChamber_EventScript_SignFloor::
	msgbox LcHollowCaveChamber_Text_SignFloor, MSGBOX_SIGN
	end

LcHollowCaveChamber_Text_SignFloor:
	.string "The pale square in the middle is\n"
	.string "packed sand, not stone.\p"
	.string "Someone swept this room, and it\n"
	.string "was a long time ago.$"
