@ LOJA de MAHOGANY. É a porta do esconderijo da Rocket.
@ ponytail: no hns e no pokecrystal a invasão do LANCE é uma cena disparada por
@ coord_event em VAR_MAHOGANY_TOWN_STATE, com o DRAGONITE abrindo o chão. Aqui
@ não há var nenhuma para gastar e não há sprite de DRAGONITE nesta build, então
@ a cena é disparada por CONVERSA com o LANCE, e só libera depois que o PROTON
@ cai no SLOWPOKE WELL (goto_if_defeated, que o motor grava de graça).
@ 593 é a escada para baixo do gTileset_ShopSinnoh, a mesma que a JUBILIFE TV
@ usa entre andares.

MahoganyTown_Shop_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, MahoganyTown_Shop_OnLoad
	.byte 0

MahoganyTown_Shop_OnLoad:
	goto_if_set FLAG_MAHOGANY_HIDEOUT_STAIRS, MahoganyTown_Shop_EventScript_PoeEscada
	end

MahoganyTown_Shop_EventScript_PoeEscada::
	setmetatile 7, 4, 593, FALSE
	end

MahoganyTown_Shop_EventScript_Lance::
	lock
	faceplayer
	goto_if_set FLAG_MAHOGANY_HIDEOUT_STAIRS, MahoganyTown_Shop_EventScript_LanceDepois
	goto_if_not_defeated TRAINER_JOHTO_ROCKET_PROTON, MahoganyTown_Shop_EventScript_LanceAntes
	msgbox MahoganyTown_Shop_Text_LanceRadio, MSGBOX_DEFAULT
	closemessage
	delay 20
	playse SE_M_HYPER_BEAM
	setvar VAR_0x8004, 1
	setvar VAR_0x8005, 1
	setvar VAR_0x8006, 5
	setvar VAR_0x8007, 6
	special ShakeCamera
	waitse
	delay 20
	setflag FLAG_MAHOGANY_HIDEOUT_STAIRS
	setmetatile 7, 4, 593, FALSE
	special DrawWholeMapView
	delay 20
	msgbox MahoganyTown_Shop_Text_LanceStairs, MSGBOX_DEFAULT
	closemessage
	release
	end

MahoganyTown_Shop_EventScript_LanceAntes::
	msgbox MahoganyTown_Shop_Text_LanceAntes, MSGBOX_DEFAULT
	closemessage
	release
	end

MahoganyTown_Shop_EventScript_LanceDepois::
	msgbox MahoganyTown_Shop_Text_LanceSplitUp, MSGBOX_DEFAULT
	closemessage
	release
	end

MahoganyTown_Shop_EventScript_Clerk::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart MahoganyTown_Shop_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
MahoganyTown_Shop_Pokemart:
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_MAX_REPEL
	pokemartlistend

MahoganyTown_Shop_Text_LanceAntes:
	.string "LANCE: A strange radio signal is\n"
	.string "driving POKéMON wild in JOHTO.\p"
	.string "I am tracing it. Deal with the\n"
	.string "ROCKETS at the SLOWPOKE WELL first,\l"
	.string "then come back to me.$"

MahoganyTown_Shop_Text_LanceRadio:
	.string "What took you, {PLAYER}?\p"
	.string "Just as we thought, that strange\n"
	.string "radio signal is coming from here.\p"
	.string "DRAGONITE, HYPER BEAM!$"

MahoganyTown_Shop_Text_LanceStairs:
	.string "The floor gave way, and a staircase\n"
	.string "runs down into the dark.\p"
	.string "LANCE: Excellent work finding the\n"
	.string "stairs, DRAGONITE!$"

MahoganyTown_Shop_Text_LanceSplitUp:
	.string "LANCE: {PLAYER}, we should split up\n"
	.string "to check this place.\p"
	.string "I have gone on ahead. Come down\n"
	.string "when your POKéMON are ready.$"
