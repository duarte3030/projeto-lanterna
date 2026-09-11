@ LcUnderseaShrine: mapa copiado de Pokémon Liquid Crystal.gba (g4m5) por
@ dev_scripts/copia_mapa_rom.py. A ARTE é do hack; o JOGO (warps, NPCs,
@ encontros, treinadores, placas) é NOSSO e está aqui.
@
@ É o único dos nove que usa o primário LcIndoor (0x2D4BB4 na ROM do hack), e
@ por isso a arte muda de pedra vermelha para areia e cantaria.
@
@ A porta em (35,9) leva ao armário de cinco células que fica perdido no meio da
@ LcUnderseaDepths (34,100). O hack deixava os dois tiles sem par: (35,9)
@ apontava para g0m0, que é destino nulo, e (34,100) não tinha warp nenhum. Os
@ dois têm MB_NON_ANIMATED_DOOR e colisão 0, ou seja são porta de verdade na
@ arte, e agora são uma passagem só.

LcUnderseaShrine_MapScripts::
	.byte 0

LcUnderseaShrine_EventScript_Maris::
	trainerbattle_single TRAINER_JOHTO_LC_UNDERSEA_MARIS, LcUnderseaShrine_Text_MarisSeen, LcUnderseaShrine_Text_MarisBeaten
	msgbox LcUnderseaShrine_Text_MarisAfter, MSGBOX_AUTOCLOSE
	end

LcUnderseaShrine_EventScript_ShrineSign::
	msgbox LcUnderseaShrine_Text_ShrineSign, MSGBOX_SIGN
	end

LcUnderseaShrine_Text_MarisSeen:
	.string "Stop. Look at the floor you are\n"
	.string "standing on.\p"
	.string "Somebody cut that. Under the sea.\n"
	.string "Now battle me, and mind the walls.$"

LcUnderseaShrine_Text_MarisBeaten:
	.string "Beaten in my own reading room.$"

LcUnderseaShrine_Text_MarisAfter:
	.string "I have copied every mark in this\n"
	.string "chamber twice and they still make\n"
	.string "no sentence.\p"
	.string "Perhaps they were never meant to be\n"
	.string "read by anyone who could walk here.$"

LcUnderseaShrine_Text_ShrineSign:
	.string "The stone is cut too straight to be\n"
	.string "the sea's work.\p"
	.string "Whatever this room was for, the water\n"
	.string "came afterwards.$"
