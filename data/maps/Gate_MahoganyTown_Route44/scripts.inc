@ Guarita nova da travessia MAHOGANY TOWN <-> ROUTE 44 (24/09/2026).
@
@ A Mahogany copiada do Scorched Silver fica no secundário gTileset_MahoganyTownCopiaSec,
@ e a Route44 divide o secundário com Blackthorn; a conexão direta faria a
@ travessia recarregar o secundário errado (contrato 3.1). A saída leste vira esta
@ guarita. O interior é o MESMO molde horizontal da Gate_EcruteakCity_Route42,
@ byte a byte (13x9, gTileset_JohtoBuilding mais gTileset_GateStandard), porque a
@ orientação é a mesma: a CIDADE a oeste, warp 0 em (1,5), e a ROTA a leste, warp
@ 1 em (11,5). Do lado da cidade são as duas setas da estrada do autor, em (39,14)
@ e (39,15); do lado da rota, a seta oeste em (0,15) da Route44.

Gate_MahoganyTown_Route44_MapScripts::
	.byte 0

Gate_MahoganyTown_Route44_EventScript_Officer::
	lock
	faceplayer
	msgbox Gate_MahoganyTown_Route44_Text_Officer, MSGBOX_DEFAULT
	closemessage
	release
	end

Gate_MahoganyTown_Route44_Text_Officer::
	.string "This gate is the east way in and\n"
	.string "out of MAHOGANY TOWN.\p"
	.string "ROUTE 44 leads on to the ICE PATH\n"
	.string "and BLACKTHORN CITY.\p"
	.string "Bundle up, it's cold out there!$"
