@ GOLDENROD CITY.
@
@ A quarta e ultima batalha contra o SILVER esteve AQUI, na calcada da entrada
@ sul do subterraneo, entre 06/08 e 15/08/2026. Ela voltou para o lugar da
@ fonte, data/maps/GoldenrodCity_UndergroundSwitches/scripts.inc, onde o mapa e
@ a vaga de objeto ja existiam.
@
@ O que sobrou aqui, e por que sobrou: o objeto do SILVER continua na lista
@ (indice 40, o ultimo), com grafico e script zerados, porque a save do Gui
@ guarda INDICE de object_event e apagar renumeraria todo mundo depois dele.
@ Ele sai por FLAG, e e so isso que este ON_TRANSITION faz: acende
@ FLAG_HIDE_SILVER_GOLDENROD toda vez que a cidade carrega, antes de os objetos
@ nascerem, e nunca mais apaga. A MESMA flag serve ao SILVER de la embaixo (o
@ ON_TRANSITION de la a apaga quando e a hora), e os dois nunca estao
@ carregados ao mesmo tempo.

GoldenrodCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, GoldenrodCity_OnTransition
	.byte 0

GoldenrodCity_OnTransition:
	setflag FLAG_HIDE_SILVER_GOLDENROD
	end

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

GoldenrodCity_EventScript_NameRaterSign::
	msgbox GoldenrodCity_Text_NameRaterSign, MSGBOX_SIGN
	end

GoldenrodCity_EventScript_SignBike::
	lock
	msgbox GoldenrodCity_Text_BikeShopSign, MSGBOX_SIGN
	closemessage
	release
	end

GoldenrodCity_EventScript_SignDept::
	lock
	msgbox GoldenrodCity_Text_DeptStoreSign, MSGBOX_SIGN
	closemessage
	release
	end

GoldenrodCity_EventScript_SignFlower::
	lock
	msgbox GoldenrodCity_Text_FlowerShopSign, MSGBOX_SIGN
	closemessage
	release
	end

GoldenrodCity_EventScript_SignGameCorner::
	lock
	msgbox GoldenrodCity_Text_GameCornerSign, MSGBOX_SIGN
	closemessage
	release
	end

GoldenrodCity_EventScript_SignGym::
	lock
	msgbox GoldenrodCity_Text_GymSign, MSGBOX_SIGN
	closemessage
	release
	end

GoldenrodCity_EventScript_SignRadio::
	lock
	msgbox GoldenrodCity_Text_RadioTowerSign, MSGBOX_SIGN
	closemessage
	release
	end

GoldenrodCity_EventScript_SignTrain::
	lock
	msgbox GoldenrodCity_Text_StationSign, MSGBOX_SIGN
	closemessage
	release
	end

GoldenrodCity_EventScript_SignUnderground::
	lock
	msgbox GoldenrodCity_Text_UndergroundSouthSign, MSGBOX_SIGN
	closemessage
	release
	end

GoldenrodCity_Text_BikeShopSign::
	.string "The World is a Cycle Path!\n"
	.string "BIKE SHOP$"

GoldenrodCity_Text_DeptStoreSign::
	.string "Full Selection of POKéMON Goods!\p"
	.string "GOLDENROD CITY DEPT.STORE$"

GoldenrodCity_Text_FlowerShopSign::
	.string "Blooming Beautiful FLOWER SHOP$"

GoldenrodCity_Text_GameCornerSign::
	.string "Your Playground!\p"
	.string "GOLDENROD CITY GAME CORNER$"

GoldenrodCity_Text_GymSign::
	.string "GOLDENROD CITY POKéMON GYM\n"
	.string "LEADER: WHITNEY\p"
	.string "The Incredibly Pretty Girl!$"

GoldenrodCity_Text_NameRaterSign::
	.string "NAME RATER\p"
	.string "Get Your POKéMON Nicknames Rated$"

GoldenrodCity_Text_RadioTowerSign::
	.string "GOLDENROD CITY RADIO TOWER$"

GoldenrodCity_Text_StationSign::
	.string "GOLDENROD CITY STATION$"

GoldenrodCity_Text_UndergroundSouthSign::
	.string "UNDERGROUND ENTRANCE$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

GoldenrodCity_EventScript_Rocket6::
	lock
	faceplayer
	msgbox GoldenrodCity_Text_Rocket6, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodCity_Text_Rocket6::
	.string "Come and taste the terror of\n"
	.string "TEAM ROCKET!$"

GoldenrodCity_EventScript_Rocket4::
	lock
	faceplayer
	msgbox GoldenrodCity_Text_Rocket4, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodCity_Text_Rocket4::
	.string "Our dream will soon come true…\p"
	.string "It was a long, hard struggle…$"

GoldenrodCity_EventScript_Rocket5::
	lock
	faceplayer
	msgbox GoldenrodCity_Text_Rocket5, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodCity_Text_Rocket5::
	.string "Hey, brat! You don't belong here!\n"
	.string "Get lost already!$"

GoldenrodCity_EventScript_Rocket1::
	lock
	faceplayer
	msgbox GoldenrodCity_Text_Rocket1, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodCity_Text_Rocket1::
	.string "Stay out of the way!\n"
	.string "Beat it, kid!$"

GoldenrodCity_EventScript_Rocket2::
	lock
	faceplayer
	msgbox GoldenrodCity_Text_Rocket2, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodCity_Text_Rocket2::
	.string "Take over the RADIO TOWER…\p"
	.string "What? It's none of your business!$"

GoldenrodCity_EventScript_Rocket3::
	lock
	faceplayer
	msgbox GoldenrodCity_Text_Rocket3, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodCity_Text_Rocket3::
	.string "POKéMON? They're just tools\n"
	.string "we use to make money!$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

GoldenrodCity_EventScript_Lass::
	lock
	faceplayer
	msgbox GoldenrodCity_Text_Lass, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodCity_Text_Lass::
	.string "That man inside rates your\n"
	.string "POKéMON nicknames.\p"
	.string "He can even rename them.$"

GoldenrodCity_EventScript_Gramps::
	lock
	faceplayer
	msgbox GoldenrodCity_Text_Gramps, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodCity_Text_Gramps::
	.string "Whew! This town is so big,\n"
	.string "I can't find anything at all.$"

GoldenrodCity_EventScript_Youngster::
	msgbox GoldenrodCity_Text_Youngster1, MSGBOX_NPC
	end

GoldenrodCity_Text_Youngster1::
	.string "I know there's a new BIKE SHOP,\n"
	.string "but I can't find it anywhere.$"

GoldenrodCity_EventScript_Youngster2::
	msgbox GoldenrodCity_Text_Youngster2, MSGBOX_NPC
	end

GoldenrodCity_Text_Youngster2::
	.string "E-he-he-he…\p"
	.string "I got in trouble for playing in\n"
	.string "the DEPT.STORE basement.$"

GoldenrodCity_Text_RocketScout1::
	.string "So this is the RADIO TOWER…$"

GoldenrodCity_EventScript_RocketScoutFala::
	msgbox GoldenrodCity_Text_RocketScout1, MSGBOX_NPC
	end

GoldenrodCity_EventScript_PokefanM::
	lock
	faceplayer
	msgbox GoldenrodCity_Text_PokefanM, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodCity_Text_PokefanM::
	.string "They built the new RADIO TOWER\n"
	.string "to replace the old creaky one.$"

GoldenrodCity_EventScript_Woman::
	lock
	faceplayer
	msgbox GoldenrodCity_Text_Woman, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodCity_Text_Woman::
	.string "I used to train in WHITNEY's GYM,\n"
	.string "but all her crying gave me a\l"
	.string "headache.$"
