@ Treinadores de rota de GoldenrodCity_UndergroundTunnel, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

GoldenrodCity_UndergroundTunnel_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, GoldenrodCity_UndergroundTunnel_OnLoad
	.byte 0

@ A PERSIANA DE SERVICO em (22,9), e por que ela nao repinta nada
@ ----------------------------------------------------------------
@ O autor do GS Chronicles desenhou UMA persiana de metal, com cadeado laranja,
@ e ela ja chega ANDAVEL no `map.bin` dele: quem tranca a passagem la e um
@ objeto parado em cima. O tileset dele NAO tem a versao aberta dessa persiana
@ (conferido metatile a metatile no secundario `0x2D4E6C`), e nos nao inventamos
@ desenho (contrato, regra zero). Entao a persiana fica FECHADA sempre, na arte
@ do autor, e quem abre a passagem e o ROTEIRO: o jogador encara a persiana,
@ aperta A, e com a BASEMENT KEY o script leva ele para dentro.
@
@ O ON_LOAD marca a celula como IMPASSAVEL a cada carga do mapa, com o MESMO
@ metatile (o 43 do par de tilesets novo deste mapa, medido nas duas celulas de
@ persiana). E o mesmo arranjo que este mapa ja tinha antes da copia, quando a
@ porta era uma parede em (12,10) com placa e `warp` por script.
@
@ A SEGUNDA persiana, em (16,27), fica ABERTA, como no mapa do autor: ela e a
@ entrada do terceiro salao do deposito (`UndergroundWarehouse`) e e a UNICA que
@ esse mapa tem, entao tranca-la deixaria o salao inalcancavel.
GoldenrodCity_UndergroundTunnel_OnLoad:
	setmetatile 22, 9, 43, TRUE
	end

GoldenrodCity_UndergroundTunnel_EventScript_Eric::
	trainerbattle_single TRAINER_JOHTO_ERIC, GoldenrodCity_UndergroundTunnel_Text_EricSeen, GoldenrodCity_UndergroundTunnel_Text_EricBeaten
	msgbox GoldenrodCity_UndergroundTunnel_Text_EricAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_UndergroundTunnel_EventScript_Teru::
	trainerbattle_single TRAINER_JOHTO_TERU, GoldenrodCity_UndergroundTunnel_Text_TeruSeen, GoldenrodCity_UndergroundTunnel_Text_TeruBeaten
	msgbox GoldenrodCity_UndergroundTunnel_Text_TeruAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_UndergroundTunnel_EventScript_Issac::
	trainerbattle_single TRAINER_JOHTO_ISSAC, GoldenrodCity_UndergroundTunnel_Text_IssacSeen, GoldenrodCity_UndergroundTunnel_Text_IssacBeaten
	msgbox GoldenrodCity_UndergroundTunnel_Text_IssacAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_UndergroundTunnel_EventScript_Donald::
	trainerbattle_single TRAINER_JOHTO_DONALD, GoldenrodCity_UndergroundTunnel_Text_DonaldSeen, GoldenrodCity_UndergroundTunnel_Text_DonaldBeaten
	msgbox GoldenrodCity_UndergroundTunnel_Text_DonaldAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_UndergroundTunnel_Text_EricSeen:
	.string "I got booted out of the GAME CORNER.\p"
	.string "I was trying to cheat using my\n"
	.string "POKéMON…$"

GoldenrodCity_UndergroundTunnel_Text_EricBeaten:
	.string "…Grumble…$"

GoldenrodCity_UndergroundTunnel_Text_EricAfter:
	.string "I guess I have to do things fair and\n"
	.string "square…$"

GoldenrodCity_UndergroundTunnel_Text_TeruSeen:
	.string "Do you consider type alignments in\n"
	.string "battle?\p"
	.string "If you know your type advantages,\n"
	.string "you'll do better in battle.$"

GoldenrodCity_UndergroundTunnel_Text_TeruBeaten:
	.string "Ow, ow, ow!$"

GoldenrodCity_UndergroundTunnel_Text_TeruAfter:
	.string "I know my POKéMON type alignments.\p"
	.string "But I only use one type of POKéMON.$"

GoldenrodCity_UndergroundTunnel_Text_IssacSeen:
	.string "My POKéMON just got a haircut!\p"
	.string "I'll show you how strong it is!$"

GoldenrodCity_UndergroundTunnel_Text_IssacBeaten:
	.string "Aiyeeee!$"

GoldenrodCity_UndergroundTunnel_Text_IssacAfter:
	.string "Your POKéMON will like you more if\n"
	.string "you give them haircuts.$"

GoldenrodCity_UndergroundTunnel_Text_DonaldSeen:
	.string "I think you have some rare POKéMON\n"
	.string "with you.\p"
	.string "Let me see them!$"

GoldenrodCity_UndergroundTunnel_Text_DonaldBeaten:
	.string "Gaah! I lost! That makes me mad!$"

GoldenrodCity_UndergroundTunnel_Text_DonaldAfter:
	.string "When I was walking near the BIKE\n"
	.string "SHOP last night, I felt like I was\l"
	.string "being watched from the rooftops...$"

@ Placas e mecanica portadas do hns por completa_placas_johto.py
GoldenrodCity_UndergroundTunnel_EventScript_Door::
	lock
	goto_if_set FLAG_UNLOCKED_GOLDENROD_UNDERGROUND_DOOR, GoldenrodCity_UndergroundTunnel_EventScript_DoorAlreadyOpened
	checkitem ITEM_BASEMENT_KEY
	goto_if_eq VAR_RESULT, TRUE, GoldenrodCity_UndergroundTunnel_EventScript_OpenDoor
	msgbox GoldenrodUnderground_Text_DoorsLocked, MSGBOX_DEFAULT
	closemessage
	release
	end
GoldenrodCity_UndergroundTunnel_EventScript_OpenDoor::
	msgbox GoldenrodUnderground_Text_KeyOpenedDoor, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_UNLOCKED_GOLDENROD_UNDERGROUND_DOOR
	playse SE_BANG
	waitse
	goto GoldenrodCity_UndergroundTunnel_EventScript_DoorEnter
GoldenrodCity_UndergroundTunnel_EventScript_DoorAlreadyOpened::
	msgbox GoldenrodUnderground_Text_DoorIsOpen, MSGBOX_DEFAULT
	closemessage
	goto GoldenrodCity_UndergroundTunnel_EventScript_DoorEnter
GoldenrodCity_UndergroundTunnel_EventScript_DoorEnter::
	warp MAP_GOLDENROD_CITY_UNDERGROUND_SWITCHES, 1
	waitstate
	release
	end
GoldenrodUnderground_Text_DoorsLocked:
    .string "The door's locked…$"
GoldenrodUnderground_Text_DoorIsOpen:
    .string "The door is open.$"
GoldenrodUnderground_Text_KeyOpenedDoor:
    .string "The BASEMENT KEY opened the door.$"
