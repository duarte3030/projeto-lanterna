@ Textos vindos de pret/pokeplatinum (res/text/veilstone_city.json), em ingles.
@ Counterpart (Dawn/Lucas), Grunt_M (warehouse norte/sul/southeast/storage key),
@ Crasher Wake e Looker ficaram de fora: dependem de flag de historia
@ (FLAG_HIDE_VEILSTONE_*), que este agente nao pode inventar.
@ OBJ_EVENT_GFX_GUITARIST, OBJ_EVENT_GFX_ROUGHNECK e OBJ_EVENT_GFX_LADY nao
@ existem em event_objects.h: trocados por MAN_3, MAN_5 e WOMAN_3.

VeilstoneCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, VeilstoneCity_OnTransition
	.byte 0

@ ponytail: a cena e a flag sao a mesma coisa. Os tres grunts do armazem
@ (LOCALID_GRUNT_M_WAREHOUSE_NORTH/SOUTH/SOUTHEAST na fonte, hidden_flag
@ FLAG_HIDE_VEILSTONE_GALACTIC_GRUNTS) nascem enquanto o QG (bem aqui em
@ Veilstone) nao caiu, e somem depois; mesma FLAG_GALACTICA_QG_TOMADO que o QG
@ inteiro ja usa, porque e o mesmo marco. Zero var.
VeilstoneCity_OnTransition:
	call_if_defeated TRAINER_SINNOH_COMMANDER_SATURN_GALACTIC_HQ, VeilstoneCity_EventScript_HideGalactica_qg_veilstone
	@ O counterpart revelado pela vitória da Maylene usa OBJ_EVENT_GFX_VAR_0;
	@ todo mapa que usa VAR_0 seta a var no PRÓPRIO transition (regra da onda 2,
	@ molde de Route207), senão o sprite vaza do último mapa que a escreveu.
	checkplayergender
	goto_if_eq VAR_RESULT, MALE, VeilstoneCity_SetCounterpartFemale
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_BRENDAN_NORMAL
	end

VeilstoneCity_SetCounterpartFemale::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_MAY_NORMAL
	end

VeilstoneCity_EventScript_HideGalactica_qg_veilstone::
	setflag FLAG_GALACTICA_QG_TOMADO
	return

VeilstoneCity_EventScript_Lady::
	msgbox VeilstoneCity_Text_Lady, MSGBOX_NPC
	end

VeilstoneCity_EventScript_Roughneck::
	msgbox VeilstoneCity_Text_Roughneck, MSGBOX_NPC
	end

VeilstoneCity_EventScript_MeteoriteSign::
	msgbox VeilstoneCity_Text_MeteoriteSign, MSGBOX_SIGN
	end

VeilstoneCity_EventScript_DepartmentStoreSign::
	msgbox VeilstoneCity_Text_DepartmentStoreSign, MSGBOX_SIGN
	end

VeilstoneCity_Text_Lady:
	.string "I love shopping at the department\n"
	.string "store. There's always something\l"
	.string "new to find.$"

VeilstoneCity_Text_Roughneck:
	.string "VEILSTONE is the city of stone. We\n"
	.string "even have meteorites! Anyway,\l"
	.string "enjoy your visit here.$"

VeilstoneCity_Text_MeteoriteSign:
	.string "It's a mysterious meteorite that\n"
	.string "fell from the stars...$"

VeilstoneCity_Text_DepartmentStoreSign:
	.string "VEILSTONE DEPARTMENT STORE$"

@ Historia: a Galactica em Veilstone. O QG (galactic_hq_*) e o armazem ainda nao
@ existem como mapa, entao o grunt so guarda a rua. Texto de pret/pokeplatinum,
@ res/text/lake_acuity.json e veilstone_city.json.

VeilstoneCity_EventScript_GalacticGrunt::
	msgbox VeilstoneCity_Text_GalacticGrunt, MSGBOX_NPC
	end

VeilstoneCity_EventScript_WarehouseGruntNorth::
	msgbox VeilstoneCity_Text_WarehouseGruntNorth, MSGBOX_NPC
	end

VeilstoneCity_Text_WarehouseGruntNorth:
	.string "Grunt 1: Hey, you! Yeah, you!\p"
	.string "This is Team Galactic's\n"
	.string "warehouse! It ain't no\l"
	.string "playground for kids!$"

VeilstoneCity_EventScript_WarehouseGruntSouth::
	msgbox VeilstoneCity_Text_WarehouseGruntSouth, MSGBOX_NPC
	end

VeilstoneCity_Text_WarehouseGruntSouth:
	.string "Grunt 2: This is the awesome\n"
	.string "Team Galactic's awesome\l"
	.string "warehouse!\p"
	.string "A little kid like you should be\n"
	.string "playing at the Pokémon Gym.\p"
	.string "After all, the Gym Leader happens\n"
	.string "to be a kid just like you!$"

VeilstoneCity_EventScript_WarehouseGruntSoutheast::
	msgbox VeilstoneCity_Text_WarehouseGruntSoutheast, MSGBOX_NPC
	end

VeilstoneCity_Text_WarehouseGruntSoutheast:
	.string "We have the Hidden Machine that\n"
	.string "teaches Fly stored in the\l"
	.string "warehouse.\p"
	.string "They said I can use it if I show\n"
	.string "them that I deserve it.$"

VeilstoneCity_Text_GalacticGrunt:
	.string "This is Team Galactic's turf.\p"
	.string "Our headquarters is right here in\n"
	.string "Veilstone, but don't waste your\l"
	.string "time. You'll never get in.\p"
	.string "Now, if you'll excuse me.$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

VeilstoneCity_EventScript_Placa2::
	msgbox VeilstoneCity_Text_Placa2, MSGBOX_SIGN
	end

VeilstoneCity_Text_Placa2:
	.string "Galactic Warehouse\nNO TRESPASSING!$"

VeilstoneCity_EventScript_Placa3::
	msgbox VeilstoneCity_Text_Placa3, MSGBOX_SIGN
	end

VeilstoneCity_Text_Placa3:
	.string "Galactic Veilstone Building\nWe Dream of the Universe!$"

VeilstoneCity_EventScript_Placa4::
	msgbox VeilstoneCity_Text_Placa4, MSGBOX_SIGN
	end

VeilstoneCity_Text_Placa4:
	.string "Veilstone Department Store\nA Shop Full of Dreams!$"

VeilstoneCity_EventScript_Placa5::
	msgbox VeilstoneCity_Text_Placa5, MSGBOX_SIGN
	end

VeilstoneCity_Text_Placa5:
	.string "Veilstone City Pokémon Gym\nLeader: Maylene\pThe Barefoot, Fighting Genius!$"

VeilstoneCity_EventScript_Placa6::
	msgbox VeilstoneCity_Text_Placa6, MSGBOX_SIGN
	end

VeilstoneCity_Text_Placa6:
	.string "Veilstone Game Corner\nAim for an Explosion of Luck!$"

VeilstoneCity_EventScript_Placa7::
	msgbox VeilstoneCity_Text_Placa7, MSGBOX_SIGN
	end

VeilstoneCity_Text_Placa7:
	.string "Prize Exchange\nCoins Exchanged for Prizes!$"

VeilstoneCity_EventScript_Placa8::
	msgbox VeilstoneCity_Text_Placa8, MSGBOX_SIGN
	end

VeilstoneCity_Text_Placa8:
	.string "Visit Beautiful Lake Valor!\nRight off Rt. 214!$"

VeilstoneCity_EventScript_Placa11::
	msgbox VeilstoneCity_Text_Placa11, MSGBOX_SIGN
	end

VeilstoneCity_Text_Placa11:
	.string "Touching the meteorite boosted\nthe Speed of a certain Pokémon.$"

VeilstoneCity_EventScript_Placa12::
	msgbox VeilstoneCity_Text_Placa12, MSGBOX_SIGN
	end

VeilstoneCity_Text_Placa12:
	.string "Touching the meteorite heightened\nthe defensive capabilities of\pa certain Pokémon.$"

VeilstoneCity_EventScript_Placa13::
	msgbox VeilstoneCity_Text_Placa13, MSGBOX_SIGN
	end

VeilstoneCity_Text_Placa13:
	.string "Touching the meteorite heightened\nthe offensive capabilities of\pa certain Pokémon.$"

VeilstoneCity_EventScript_Placa14::
	msgbox VeilstoneCity_Text_Placa14, MSGBOX_SIGN
	end

VeilstoneCity_Text_Placa14:
	.string "Touching the meteorite balanced out\nthe attributes of a certain Pokémon.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

VeilstoneCity_EventScript_Npc1::
	msgbox VeilstoneCity_Text_Npc1, MSGBOX_NPC
	end

VeilstoneCity_Text_Npc1:
	.string "Yeah, Team Galactic is hiding all sorts\nof good stuff in their warehouse.\pI hear they even have a Hidden\nMachine in there!$"

VeilstoneCity_EventScript_Npc2::
	msgbox VeilstoneCity_Text_Npc2, MSGBOX_NPC
	end

VeilstoneCity_Text_Npc2:
	.string "The Game Corner is dangerous!\pWhy is it dangerous?\nIt's so fun, I lose track of time!$"

VeilstoneCity_EventScript_Npc3::
	msgbox VeilstoneCity_Text_Npc3, MSGBOX_NPC
	end

VeilstoneCity_Text_Npc3:
	.string "I got a TM as a prize from the\nGame Corner.\pI used it on my Pokémon right away!$"

VeilstoneCity_EventScript_Npc4::
	msgbox VeilstoneCity_Text_Npc4, MSGBOX_NPC
	end

VeilstoneCity_Text_Npc4:
	.string "I came to this city just so I could\ngo shopping at the department store.\pBut with all these rock walls around,\nthis place feels kind of cold.$"

VeilstoneCity_EventScript_Npc5::
	msgbox VeilstoneCity_Text_Npc5, MSGBOX_NPC
	end

VeilstoneCity_Text_Npc5:
	.string "I bought a new parasol.\pBut I don't want it to get rained on,\nso I watch the TV weather reports.$"

VeilstoneCity_EventScript_Npc6::
	msgbox VeilstoneCity_Text_Npc6, MSGBOX_NPC
	end

VeilstoneCity_Text_Npc6:
	.string "Maylene is Veilstone's Gym Leader.\nThen, there's Wake in Pastoria...\pThey're way too tough for me.\nI can't even come close to them.$"

VeilstoneCity_EventScript_Npc7::
	msgbox VeilstoneCity_Text_Npc7, MSGBOX_NPC
	end

VeilstoneCity_Text_Npc7:
	.string "Do you know where one might find\na Coin Case?\pI heard that there's a clown giving\n'em away, but...$"

VeilstoneCity_EventScript_Npc8::
	msgbox VeilstoneCity_Text_Npc8, MSGBOX_NPC
	end

VeilstoneCity_Text_Npc8:
	.string "Veilstone is the city of stone.\nWe even have meteorites!\pThis has nothing to do with anything,\nbut take this Technical Machine!$"

VeilstoneCity_EventScript_Npc9::
	msgbox VeilstoneCity_Text_Npc9, MSGBOX_NPC
	end

VeilstoneCity_Text_Npc9:
	.string "A man spoke to me in a foreign language.\nHe really surprised me!\pI think he was asking if I liked Pokémon\nor something.$"

VeilstoneCity_EventScript_Npc10::
	msgbox VeilstoneCity_Text_Npc10, MSGBOX_NPC
	end

VeilstoneCity_Text_Npc10:
	.string "Salut, Trainer!\nTu aimes les Pokémon?$"

VeilstoneCity_EventScript_Placa1::
	msgbox VeilstoneCity_Text_Placa1, MSGBOX_SIGN
	end

VeilstoneCity_Text_Placa1:
	.string "Veilstone City\nHewn from Rock$"
