@ Casa do jogador em Twinleaf, terreo. Falas do Platinum,
@ res/text/twinleaf_town_player_house_1f.json.

TwinleafTown_MainHouse_1F_MapScripts::
	.byte 0

TwinleafTown_MainHouse_1F_EventScript_Mom::
	lock
	faceplayer
	goto_if_set FLAG_SYS_POKEMON_GET, TwinleafTown_MainHouse_1F_EventScript_MomAfter
	goto_if_set FLAG_SYS_B_DASH, TwinleafTown_MainHouse_1F_EventScript_MomReminder
	msgbox TwinleafTown_MainHouse_1F_Text_MomPutTheseOn, MSGBOX_DEFAULT
	setflag FLAG_SYS_B_DASH
	message TwinleafTown_MainHouse_1F_Text_ReceivedRunningShoes
	waitmessage
	playfanfare MUS_OBTAIN_ITEM
	waitfanfare
	msgbox TwinleafTown_MainHouse_1F_Text_MomDontGoIntoTallGrass, MSGBOX_DEFAULT
	release
	end

TwinleafTown_MainHouse_1F_EventScript_MomReminder::
	msgbox TwinleafTown_MainHouse_1F_Text_MomIsntRivalWaiting, MSGBOX_DEFAULT
	release
	end

TwinleafTown_MainHouse_1F_EventScript_MomAfter::
	msgbox TwinleafTown_MainHouse_1F_Text_MomTakeAQuickRest, MSGBOX_DEFAULT
	release
	end

TwinleafTown_MainHouse_1F_Text_MomPutTheseOn:
	.string "MOM: Oh, I know!\n"
	.string "{PLAYER}, put these on.$"

TwinleafTown_MainHouse_1F_Text_ReceivedRunningShoes:
	.string "{PLAYER} received a pair of\n"
	.string "RUNNING SHOES!$"

TwinleafTown_MainHouse_1F_Text_MomDontGoIntoTallGrass:
	.string "MOM: Going to SANDGEM TOWN is like\n"
	.string "an adventure in itself, right?\p"
	.string "With those RUNNING SHOES, you can\n"
	.string "get to faraway places much faster.\p"
	.string "“Press the B Button and dash about\n"
	.string "faster than ever before!”\p"
	.string "Oh, yes! {PLAYER}!\p"
	.string "Don't go into the tall grass.\n"
	.string "Wild POKéMON might attack you.\p"
	.string "It would be OK if you had your own\n"
	.string "POKéMON, but you don't, so...\p"
	.string "Well, take care, sweetie!$"

TwinleafTown_MainHouse_1F_Text_MomIsntRivalWaiting:
	.string "MOM: What is it, dear?\n"
	.string "Isn't your friend waiting for you?$"

TwinleafTown_MainHouse_1F_Text_MomTakeAQuickRest:
	.string "MOM: Welcome home, {PLAYER}.\n"
	.string "Are you and your POKéMON healthy?\p"
	.string "Take a quick rest, dear.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

TwinleafTown_MainHouse_1F_EventScript_Placa1::
	msgbox TwinleafTown_MainHouse_1F_Text_Placa1, MSGBOX_SIGN
	end

TwinleafTown_MainHouse_1F_Text_Placa1:
	.string "Mom's favorite dessert is in\nthe refrigerator.$"

TwinleafTown_MainHouse_1F_EventScript_Placa2::
	msgbox TwinleafTown_MainHouse_1F_Text_Placa2, MSGBOX_SIGN
	end

TwinleafTown_MainHouse_1F_Text_Placa2:
	.string "Mom's kitchen is spotless!\nYou can see your face on the floor!$"

TwinleafTown_MainHouse_1F_EventScript_Placa3::
	msgbox TwinleafTown_MainHouse_1F_Text_Placa3, MSGBOX_SIGN
	end

TwinleafTown_MainHouse_1F_Text_Placa3:
	.string "Mom's kitchen is spotless!\nYou can see your face on the floor!$"

TwinleafTown_MainHouse_1F_EventScript_Placa4::
	msgbox TwinleafTown_MainHouse_1F_Text_Placa4, MSGBOX_SIGN
	end

TwinleafTown_MainHouse_1F_Text_Placa4:
	.string "This is where Mom does all her\ndelicious cooking.$"

TwinleafTown_MainHouse_1F_EventScript_Placa5::
	msgbox TwinleafTown_MainHouse_1F_Text_Placa5, MSGBOX_SIGN
	end

TwinleafTown_MainHouse_1F_Text_Placa5:
	.string "This is where Mom does all her\ndelicious cooking.$"

TwinleafTown_MainHouse_1F_EventScript_Placa6::
	msgbox TwinleafTown_MainHouse_1F_Text_Placa6, MSGBOX_SIGN
	end

TwinleafTown_MainHouse_1F_Text_Placa6:
	.string "This is where Mom does all her\ndelicious cooking.$"
