@ TORRE RADIO de GOLDENROD, 2F. Portado de
@ fontes-mapas/hns/data/maps/GoldenrodCity_RadioTower_2F/scripts.inc.
@ Os QUATRO grunts do hns estao aqui: os dois primeiros vieram na leva de
@ portes e os outros dois em 12/08/2026, quando MAX_TRAINERS_COUNT_EMERALD
@ subiu de 2500 para 4000 e as 14 vagas que travavam o porte viraram 1559.
@ Buena e o policial continuam de fora: dependiam de VAR_GOLDENROD_CITY_STATE
@ e de sprite que esta build nao desenha.
@ Todo Rocket da torre some com FLAG_HIDE_GOLDENROD_ROCKETS, ligada quando o
@ ARCHER cai no 5F.

GoldenrodCity_RadioTower_2F_MapScripts::
	.byte 0

RadioTower2F_EventScript_Grunt1::
	trainerbattle_single TRAINER_JOHTO_ROCKET_GRUNT_RADIO_2F_1, RadioTower2F_Text_Grunt1Seen, RadioTower2F_Text_Grunt1Beaten
	msgbox RadioTower2F_Text_Grunt1After, MSGBOX_AUTOCLOSE
	end

RadioTower2F_EventScript_Grunt2::
	trainerbattle_single TRAINER_JOHTO_ROCKET_GRUNT_RADIO_2F_2, RadioTower2F_Text_Grunt2Seen, RadioTower2F_Text_Grunt2Beaten
	msgbox RadioTower2F_Text_Grunt2After, MSGBOX_AUTOCLOSE
	end

RadioTower2F_EventScript_Teacher::
	lock
	faceplayer
	msgbox RadioTower2F_Text_Teacher, MSGBOX_DEFAULT
	closemessage
	release
	end

RadioTower2F_EventScript_Boy::
	lock
	faceplayer
	msgbox RadioTower2F_Text_SuperNerd, MSGBOX_DEFAULT
	closemessage
	release
	end

RadioTower2F_Text_Grunt1Seen:
	.string "Three years ago, TEAM ROCKET was\n"
	.string "forced to disband.\p"
	.string "But we're making a comeback here!$"

RadioTower2F_Text_Grunt1Beaten:
	.string "Gwah! Don't get cute!$"

RadioTower2F_Text_Grunt1After:
	.string "We won't let you ruin our plans\n"
	.string "for our comeback!$"

RadioTower2F_Text_Grunt2Seen:
	.string "Hey, hey! Keep out of our way!$"

RadioTower2F_Text_Grunt2Beaten:
	.string "Arggh. I give up.$"

RadioTower2F_Text_Grunt2After:
	.string "Our EXECUTIVES are trying to take\n"
	.string "this place over.\p"
	.string "They have some big plan. I wonder\n"
	.string "what that is?$"

RadioTower2F_Text_Teacher:
	.string "Lullabies on the radio may make\n"
	.string "POKéMON sleep.$"

RadioTower2F_Text_SuperNerd:
	.string "You can listen to the radio\n"
	.string "anywhere. Tune in!$"

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

GoldenrodCity_RadioTower_2F_EventScript_Sign1::
	lock
	msgbox GoldenrodCity_RadioTower_2F_Text_SalesSign, MSGBOX_SIGN
	closemessage
	release
	end

GoldenrodCity_RadioTower_2F_EventScript_Sign2::
	lock
	msgbox GoldenrodCity_RadioTower_2F_Text_OakTalkSign, MSGBOX_SIGN
	closemessage
	release
	end

GoldenrodCity_RadioTower_2F_Text_OakTalkSign::
	.string "PROF.OAK'S POKéMON TALK\p"
	.string "The Hottest Show on the Air!$"

GoldenrodCity_RadioTower_2F_Text_SalesSign::
	.string "2F SALES$"

@ Treinador do hns que faltava, ligado em 12/08/2026 por
@ dev_scripts/treinadores_faltantes_johto.py

RadioTower2F_EventScript_Grunt3::
	trainerbattle_single TRAINER_JOHTO_GRUNT_4, RadioTower2F_Text_Grunt3Seen, RadioTower2F_Text_Grunt3Beaten
	msgbox RadioTower2F_Text_Grunt3After, MSGBOX_AUTOCLOSE
	end

RadioTower2F_Text_Grunt3Seen:
	.string "We're TEAM ROCKET, the exploiters\n"
	.string "of POKéMON!\p"
	.string "We love being evil! Scared?$"

RadioTower2F_Text_Grunt3Beaten:
	.string "You think you're a hero?$"

RadioTower2F_Text_Grunt3After:
	.string "We're not always evil. We just do\n"
	.string "whatever we like.$"

RadioTower2F_EventScript_Grunt4::
	trainerbattle_single TRAINER_JOHTO_GRUNT_26, RadioTower2F_Text_Grunt4Seen, RadioTower2F_Text_Grunt4Beaten
	msgbox RadioTower2F_Text_Grunt4After, MSGBOX_AUTOCLOSE
	end

RadioTower2F_Text_Grunt4Seen:
	.string "Hahaha!\p"
	.string "How boring. It was far too easy\n"
	.string "to take over this place!\p"
	.string "Come on, keep me amused!$"

RadioTower2F_Text_Grunt4Beaten:
	.string "Wh-who are you?$"

RadioTower2F_Text_Grunt4After:
	.string "You beat me, and I won't forget\n"
	.string "it!$"
