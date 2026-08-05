@ TORRE RADIO de GOLDENROD, 1F. Portado de
@ fontes-mapas/hns/data/maps/GoldenrodCity_RadioTower_1F/scripts.inc.
@ ponytail: o QUIZ do RADIO e a WHITNEY sairam (dependem de FLAG_ENABLE_RADIO,
@ de ITEM_RADIO e de VAR_GOLDENROD_CITY_STATE, que nao existem aqui). O que
@ ficou e o portao do arco: o grunt em cima da escada para o 2F. Ele so some
@ depois de perder, e para isso pede FLAG_HIDE_GOLDENROD_RADIO_TOWER_1F_ROCKET.

GoldenrodCity_RadioTower_1F_MapScripts::
	.byte 0

RadioTower1F_EventScript_Grunt::
	lock
	faceplayer
	msgbox RadioTower1F_Text_GruntSeen, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_JOHTO_ROCKET_GRUNT_RADIO_1F, RadioTower1F_Text_GruntBeaten
	msgbox RadioTower1F_Text_GruntAfter, MSGBOX_AUTOCLOSE
	turnobject LOCALID_RADIO_TOWER_1F_GRUNT, DIR_EAST
	delay 30
	playse SE_EXIT
	setflag FLAG_HIDE_GOLDENROD_RADIO_TOWER_1F_ROCKET
	removeobject LOCALID_RADIO_TOWER_1F_GRUNT
	release
	end

RadioTower1F_EventScript_Lass::
	lock
	faceplayer
	msgbox RadioTower1F_Text_Lass, MSGBOX_DEFAULT
	closemessage
	release
	end

RadioTower1F_EventScript_Youngster::
	lock
	faceplayer
	msgbox RadioTower1F_Text_Youngster, MSGBOX_DEFAULT
	closemessage
	release
	end

RadioTower1F_EventScript_Reception::
	lock
	faceplayer
	msgbox RadioTower1F_Text_ReceptionistWelcome, MSGBOX_DEFAULT
	msgbox RadioTower1F_Text_ReceptionistNoTours, MSGBOX_DEFAULT
	closemessage
	release
	end

RadioTower1F_Text_GruntSeen:
	.string "We've finally taken over the\n"
	.string "RADIO TOWER!\p"
	.string "Now everyone will get to experience\n"
	.string "the true terror of TEAM ROCKET!\p"
	.string "We'll show you how scary we are!$"

RadioTower1F_Text_GruntBeaten:
	.string "Too strong! I'm sorry boss…$"

RadioTower1F_Text_GruntAfter:
	.string "You're too strong.\p"
	.string "Our plan could be ruined. I must\n"
	.string "warn the others…$"

RadioTower1F_Text_Lass:
	.string "BEN is a fabulous DJ.\p"
	.string "His sweet voice makes me melt!$"

RadioTower1F_Text_Youngster:
	.string "I love MARY, from POKéMON TALK.\p"
	.string "I only know what she sounds like,\n"
	.string "though.$"

RadioTower1F_Text_ReceptionistWelcome:
	.string "Welcome!$"

RadioTower1F_Text_ReceptionistNoTours:
	.string "Hello. I'm sorry, but we're not\n"
	.string "offering any tours today.$"

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

GoldenrodCity_RadioTower_1F_EventScript_Sign::
	lock
	msgbox RadioTower1F_Text_Directory, MSGBOX_SIGN
	closemessage
	release
	end

RadioTower1F_Text_Directory::
    .string "1F RECEPTION\n"
    .string "2F SALES\p"
    .string "3F PERSONNEL\n"
    .string "4F PRODUCTION\p"
    .string "5F DIRECTOR'S OFFICE$"
