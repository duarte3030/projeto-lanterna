@ Guarita nova da travessia VIOLET CITY <-> ROUTE 32 (23/09/2026).
@
@ Mesma razão da Gate_VioletCity_Route36: a cidade copiada tem primário
@ próprio e não pode ter conexão de mapa. Do lado da cidade, a saída é o
@ corredor de grama que o autor desenhou em (18..21,40), que ganhou setas
@ MB_SOUTH_ARROW_WARP copiadas byte a byte da grama dele; do lado da rota,
@ a linha 0 da ROUTE 32 em (20..23,0) ganhou setas MB_NORTH_ARROW_WARP.
@
@ O interior é o molde vertical da Gate_GoldenrodCity_Route34, byte a byte,
@ com a porta da cidade ao NORTE e a da rota ao SUL.

Gate_VioletCity_Route32_MapScripts::
	.byte 0

Gate_VioletCity_Route32_EventScript_Officer::
	lock
	faceplayer
	msgbox Gate_VioletCity_Route32_Text_Officer, MSGBOX_DEFAULT
	closemessage
	release
	end

Gate_VioletCity_Route32_Text_Officer::
	.string "This gate is the south way in and\n"
	.string "out of VIOLET CITY.\p"
	.string "ROUTE 32 runs down to the\n"
	.string "RUINS OF ALPH and UNION CAVE.$"
