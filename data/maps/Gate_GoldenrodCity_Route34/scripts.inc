@ Guarita nova da travessia GOLDENROD CITY <-> ROUTE 34 (11/09/2026).
@
@ Ela existe porque a Goldenrod copiada do GS Chronicles tem par de tilesets
@ PRÓPRIO, e travessia por conexão só recarrega o tileset SECUNDÁRIO
@ (LoadMapFromCameraTransition, src/overworld.c:911). Com primário próprio, a
@ rota vizinha passaria a ser desenhada com as paletas da cidade. As duas
@ conexões da cidade saíram e as duas travessias viraram warp com fade: a do
@ norte já tinha guarita (Gate_GoldenrodCity_Route35) e a do sul ganhou esta.
@
@ O interior é o mesmo molde vertical da guarita do norte, com a porta da cidade
@ ao NORTE e a da rota ao SUL, que é o sentido certo desta travessia.

Gate_GoldenrodCity_Route34_MapScripts::
	.byte 0

Gate_GoldenrodCity_Route34_EventScript_Officer::
	lock
	faceplayer
	msgbox Gate_GoldenrodCity_Route34_Text_Officer, MSGBOX_DEFAULT
	closemessage
	release
	end

Gate_GoldenrodCity_Route34_Text_Officer::
	.string "This gate is the south way in and\n"
	.string "out of GOLDENROD CITY.\p"
	.string "ROUTE 34 runs down to ILEX FOREST\n"
	.string "from here.\p"
	.string "Mind the traffic on your way\n"
	.string "through!$"
