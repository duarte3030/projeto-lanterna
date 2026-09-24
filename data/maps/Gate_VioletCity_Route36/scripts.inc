@ Guarita nova da travessia VIOLET CITY <-> ROUTE 36 (23/09/2026).
@
@ A Violet copiada do GS Chronicles tem par de tilesets PRÓPRIO, e travessia
@ por conexão só recarrega o tileset SECUNDÁRIO (LoadMapFromCameraTransition,
@ src/overworld.c:911). As três conexões da cidade saíram e as três
@ travessias viraram warp com fade. O autor já desenhou esta guarita na borda
@ oeste da cidade, com o par de MB_WEST_ARROW_WARP em (1,15) e (1,16).
@
@ O interior é o molde horizontal da Gate_Route31_VioletCity, byte a byte, com
@ a porta da ROUTE 36 a OESTE e a da cidade a LESTE.

Gate_VioletCity_Route36_MapScripts::
	.byte 0

Gate_VioletCity_Route36_EventScript_Officer::
	lock
	faceplayer
	msgbox Gate_VioletCity_Route36_Text_Officer, MSGBOX_DEFAULT
	closemessage
	release
	end

Gate_VioletCity_Route36_Text_Officer::
	.string "This gate is the west way in and\n"
	.string "out of VIOLET CITY.\p"
	.string "ROUTE 36 heads toward the\n"
	.string "NATIONAL PARK from here.$"
