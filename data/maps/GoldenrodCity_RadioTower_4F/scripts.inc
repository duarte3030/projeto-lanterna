@ TORRE RADIO de GOLDENROD, 4F. Portado de
@ fontes-mapas/hns/data/maps/GoldenrodCity_RadioTower_4F/scripts.inc.
@ ponytail: o 4F ficou com o PROTON, que e o reencontro do arco do Slowpoke
@ Well, e com a DJ MARY. Os dois cientistas e os dois grunts do hns sairam por
@ falta de vaga de treinador.

GoldenrodCity_RadioTower_4F_MapScripts::
	.byte 0

RadioTower4F_EventScript_Proton::
	trainerbattle_single TRAINER_JOHTO_ROCKET_PROTON_RADIO_4F, RadioTower4F_Text_ProtonSeen, RadioTower4F_Text_ProtonBeaten
	msgbox RadioTower4F_Text_ProtonAfter, MSGBOX_AUTOCLOSE
	end

RadioTower4F_EventScript_Mary::
	lock
	faceplayer
	msgbox RadioTower4F_Text_DJMary, MSGBOX_DEFAULT
	closemessage
	release
	end

RadioTower4F_Text_ProtonSeen:
	.string "PROTON: Now wait just one second!\p"
	.string "Aren't you the one who got in our\n"
	.string "way at SLOWPOKE WELL?\p"
	.string "I see… You're doing all this\n"
	.string "because you want to make me angry.\l"
	.string "Be careful!\p"
	.string "But since you seem to wish it, I'll\n"
	.string "show you the full extent of a TEAM\l"
	.string "ROCKET EXECUTIVE's wrath!$"

RadioTower4F_Text_ProtonBeaten:
	.string "Phew…$"

RadioTower4F_Text_ProtonAfter:
	.string "PROTON: You may have won this\n"
	.string "time… But all you did was make\p"
	.string "TEAM ROCKET's wrath grow.$"

RadioTower4F_Text_DJMary:
	.string "MARY: Why? Why do I have to suffer\n"
	.string "through this?\p"
	.string "MEOWTH, help me!$"

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

GoldenrodCity_RadioTower_4F4_EventScript_Sign1::
	lock
	msgbox GoldenrodCity_RadioTower_4F4_Text_Studio2Sign, MSGBOX_SIGN
	closemessage
	release
	end

GoldenrodCity_RadioTower_4F4_EventScript_Sign2::
	lock
	msgbox GoldenrodCity_RadioTower_4F4_Text_ProductionSign, MSGBOX_SIGN
	closemessage
	release
	end

GoldenrodCity_RadioTower_4F4_Text_ProductionSign::
	.string "4F PRODUCTION$"

GoldenrodCity_RadioTower_4F4_Text_Studio2Sign::
	.string "4F STUDIO 2$"
