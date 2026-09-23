@ Guarita nova da travessia OLIVINE CITY <-> ROUTE 39 (11/09/2026).
@
@ Ela nasce da decisão do Fable, pergunta 81 da frente: a saída norte de Olivine
@ era um par de setas na borda do mapa e vira uma GUARITA, com guarda e fala.
@ O interior é o MESMO molde vertical da Gate_GoldenrodCity_Route35, byte a byte
@ (15x12, gTileset_JohtoBuilding mais gTileset_GateStandard), porque a
@ orientação é a mesma das duas travessias: a CIDADE ao sul e a ROTA ao norte.
@ Por isso o warp 0, o da cidade, fica em (7,9) e o warp 1, o da rota, em (7,1).
@
@ Do lado da CIDADE a porta foi encaixada no desenho do próprio autor do
@ Scorched Silver: o prédio de telhado verde que ele desenhou duas vezes em
@ (32,16) e (37,16) foi copiado célula a célula para o alto do caminho de areia,
@ e a porta dele, o metatile 245, é a que abre esta guarita. Zero pixel novo.
@ Do lado da ROTA a travessia continua sendo o par de setas da borda sul, que é
@ exatamente o arranjo da guarita gêmea de Goldenrod com a Route 35.

Gate_OlivineCity_Route39_MapScripts::
	.byte 0

Gate_OlivineCity_Route39_EventScript_Officer::
	lock
	faceplayer
	msgbox Gate_OlivineCity_Route39_Text_Officer, MSGBOX_DEFAULT
	closemessage
	release
	end

Gate_OlivineCity_Route39_Text_Officer::
	.string "This gate is the north way in and\n"
	.string "out of OLIVINE CITY.\p"
	.string "ROUTE 39 runs up to the dairy farms\n"
	.string "from here.\p"
	.string "Watch your step on the way through!$"
