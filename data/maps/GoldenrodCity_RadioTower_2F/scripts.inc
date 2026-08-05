@ TORRE RADIO de GOLDENROD, 2F. Portado de
@ fontes-mapas/hns/data/maps/GoldenrodCity_RadioTower_2F/scripts.inc.
@ ponytail: dos quatro grunts do hns ficaram dois, porque so restam 14 vagas de
@ treinador no jogo inteiro (MAX_TRAINERS_COUNT). Buena e o policial sairam:
@ dependiam de VAR_GOLDENROD_CITY_STATE e de sprite que esta build nao desenha.
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
