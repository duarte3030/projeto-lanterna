@ TORRE RADIO de GOLDENROD, 4F. Portado de
@ fontes-mapas/hns/data/maps/GoldenrodCity_RadioTower_4F/scripts.inc.
@ O 4F tem o PROTON, que e o reencontro do arco do Slowpoke Well, a DJ MARY, os
@ dois grunts e o cientista RICH. Os tres ultimos entraram em 12/08/2026, com o
@ teto de treinador em 4000; antes eram cortados por falta de vaga. O segundo
@ cientista do hns nao existe: o 4F da fonte tem RICH e mais nenhum.

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

@ Treinador do hns que faltava, ligado em 12/08/2026 por
@ dev_scripts/treinadores_faltantes_johto.py

RadioTower4F_EventScript_Grunt1::
	trainerbattle_single TRAINER_JOHTO_GRUNT_9, RadioTower4F_Text_Grunt1Seen, RadioTower4F_Text_Grunt1Beaten
	msgbox RadioTower4F_Text_Grunt1After, MSGBOX_AUTOCLOSE
	end

RadioTower4F_Text_Grunt1Seen:
	.string "You plan to rescue the DIRECTOR?\p"
	.string "That won't be possible because I'm\n"
	.string "going to beat you!$"

RadioTower4F_Text_Grunt1Beaten:
	.string "No! Unbelievable!$"

RadioTower4F_Text_Grunt1After:
	.string "I don't believe it! I was beaten!$"

RadioTower4F_EventScript_Grunt2::
	trainerbattle_single TRAINER_JOHTO_GRUNT_28, RadioTower4F_Text_Grunt2Seen, RadioTower4F_Text_Grunt2Beaten
	msgbox RadioTower4F_Text_Grunt2After, MSGBOX_AUTOCLOSE
	end

RadioTower4F_Text_Grunt2Seen:
	.string "Don't I think POKéMON are cute?\p"
	.string "I'll think my POKéMON are cute--\p"
	.string "after they beat yours!$"

RadioTower4F_Text_Grunt2Beaten:
	.string "Oh, no! They're so useless!$"

RadioTower4F_Text_Grunt2After:
	.string "I love my beautiful self!\p"
	.string "Who cares about POKéMON?$"

RadioTower4F_EventScript_Rich::
	trainerbattle_single TRAINER_JOHTO_RICH, RadioTower4F_Text_RichSeen, RadioTower4F_Text_RichBeaten
	msgbox RadioTower4F_Text_RichAfter, MSGBOX_AUTOCLOSE
	end

RadioTower4F_Text_RichSeen:
	.string "Most excellent.\p"
	.string "This RADIO TOWER will fulfill our\n"
	.string "grand design.$"

RadioTower4F_Text_RichBeaten:
	.string "Hmmm…\p"
	.string "All grand plans come with snags.$"

RadioTower4F_Text_RichAfter:
	.string "Do you honestly believe you can stop\n"
	.string "TEAM ROCKET?$"
