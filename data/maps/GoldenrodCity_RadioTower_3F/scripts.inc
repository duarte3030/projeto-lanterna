@ TORRE RADIO de GOLDENROD, 3F. Portado de
@ fontes-mapas/hns/data/maps/GoldenrodCity_RadioTower_3F/scripts.inc.
@ O cientista MARC e o terceiro grunt entraram em 12/08/2026, quando o teto de
@ treinador subiu de 2500 para 4000 e a falta de vaga que os cortava acabou.
@ A moca do 3F e quem manda o jogador para o 5F, e a fala dela nao
@ depende mais de var: e sempre a de antes do resgate.

GoldenrodCity_RadioTower_3F_MapScripts::
	.byte 0

RadioTower3F_EventScript_Grunt1::
	trainerbattle_single TRAINER_JOHTO_ROCKET_GRUNT_RADIO_3F_1, RadioTower3F_Text_Grunt1Seen, RadioTower3F_Text_Grunt1Beaten
	msgbox RadioTower3F_Text_Grunt1After, MSGBOX_AUTOCLOSE
	end

RadioTower3F_EventScript_Grunt2::
	trainerbattle_single TRAINER_JOHTO_ROCKET_GRUNT_RADIO_3F_2, RadioTower3F_Text_Grunt2Seen, RadioTower3F_Text_Grunt2Beaten
	msgbox RadioTower3F_Text_Grunt2After, MSGBOX_AUTOCLOSE
	end

RadioTower3F_EventScript_Cooltrainer::
	lock
	faceplayer
	msgbox RadioTower3F_Text_PleaseSave, MSGBOX_DEFAULT
	closemessage
	release
	end

RadioTower3F_Text_Grunt1Seen:
	.string "I've been given strict orders.\p"
	.string "I'm to crush anyone who challenges\n"
	.string "TEAM ROCKET!$"

RadioTower3F_Text_Grunt1Beaten:
	.string "What?!$"

RadioTower3F_Text_Grunt1After:
	.string "I failed in my duties…\p"
	.string "ARCHER will be so upset…$"

RadioTower3F_Text_Grunt2Seen:
	.string "It feels great ordering POKéMON\n"
	.string "to commit crimes.$"

RadioTower3F_Text_Grunt2Beaten:
	.string "You're kidding!$"

RadioTower3F_Text_Grunt2After:
	.string "I feel lousy over losing!\p"
	.string "Darn it! I hate useless POKéMON!$"

RadioTower3F_Text_PleaseSave:
	.string "The TEAM ROCKET boss has locked\n"
	.string "himself in.\p"
	.string "But the DIRECTOR can open it.\p"
	.string "He's up on the fifth floor.\p"
	.string "Please save him!$"

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

GoldenrodCity_RadioTower_3F_EventScript_Sign1::
	lock
	msgbox GoldenrodCity_RadioTower_3F_Text_PersonnelSign, MSGBOX_SIGN
	closemessage
	release
	end

GoldenrodCity_RadioTower_3F_EventScript_Sign2::
	lock
	msgbox GoldenrodCity_RadioTower_3F_Text_PokemonMusicSign, MSGBOX_SIGN
	closemessage
	release
	end

GoldenrodCity_RadioTower_3F_Text_PersonnelSign::
	.string "3F PERSONNEL$"

GoldenrodCity_RadioTower_3F_Text_PokemonMusicSign::
	.string "POKéMON MUSIC with Host DJ BEN$"

@ Treinador do hns que faltava, ligado em 12/08/2026 por
@ dev_scripts/treinadores_faltantes_johto.py

RadioTower3F_EventScript_Grunt3::
	trainerbattle_single TRAINER_JOHTO_GRUNT_8, RadioTower3F_Text_Grunt3Seen, RadioTower3F_Text_Grunt3Beaten
	msgbox RadioTower3F_Text_Grunt3After, MSGBOX_AUTOCLOSE
	end

RadioTower3F_Text_Grunt3Seen:
	.string "Why did the shutter open? Did you\n"
	.string "have something to do with this?$"

RadioTower3F_Text_Grunt3Beaten:
	.string "I'm done for!$"

RadioTower3F_Text_Grunt3After:
	.string "What?! You made it past our men in\n"
	.string "the UNDERGROUND?\p"
	.string "How could you?$"

RadioTower3F_EventScript_Marc::
	trainerbattle_single TRAINER_JOHTO_MARC, RadioTower3F_Text_MarcSeen, RadioTower3F_Text_MarcBeaten
	msgbox RadioTower3F_Text_MarcAfter, MSGBOX_AUTOCLOSE
	end

RadioTower3F_Text_MarcSeen:
	.string "An unknown child wandering here?\p"
	.string "Who are you?$"

RadioTower3F_Text_MarcBeaten:
	.string "Tch! I took you too lightly!$"

RadioTower3F_Text_MarcAfter:
	.string "Bwahahaha…\p"
	.string "I can transmit as strong a signal\n"
	.string "as I need from here.$"
