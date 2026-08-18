VerityLakefront_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
@ Fonte: VerityLakefront_CoordEvent_WereAtTheLake. Da fonte, o jogador (e o
@ LOCALID_FOLLOWER, o rival andando junto) chegam na beira e entram no lago.
@ ponytail: LOCALID_FOLLOWER e o mecanismo de seguidor da decisao 5 do plano
@ (adiado, sem desenho de dupla andando); a fala continua (o {RIVAL} fica
@ implicito, sem objeto animado ao lado) e o jogador entra sozinho. O warp de
@ destino usa a MESMA coordenada do warp estatico ja existente deste mapa
@ para MAP_LAKE_VERITY_LOW_WATER (dest_warp_id 0), em vez de inventar
@ coordenada nova.
VerityLakefront_EventScript_CoordEvent_WereAtTheLake::
	lockall
	msgbox VerityLakefront_Text_WereAtTheLake, MSGBOX_DEFAULT
	setvar VAR_SINNOH_VERITY_BEIRA_ESTADO, 1
	releaseall
	playse SE_M_SURF
	fadescreen FADE_TO_BLACK
	warp MAP_LAKE_VERITY_LOW_WATER, 39, 47
	fadescreen FADE_FROM_BLACK
	end

VerityLakefront_Text_WereAtTheLake:
	.string "{RIVAL}: We're at the lake!$"

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

VerityLakefront_EventScript_Hiker::
	msgbox VerityLakefront_Text_Hiker, MSGBOX_NPC
	end

VerityLakefront_EventScript_Pokefan::
	msgbox VerityLakefront_Text_Pokefan, MSGBOX_NPC
	end

VerityLakefront_EventScript_TrainerTipsSign::
	msgbox VerityLakefront_Text_TrainerTipsSign, MSGBOX_SIGN
	end

VerityLakefront_Text_Hiker:
	.string "LAKE VERITY's calm today. They\n"
	.string "say something stirs beneath the\l"
	.string "surface, though...$"

VerityLakefront_Text_Pokefan:
	.string "I come here just to watch the\n"
	.string "water. It's peaceful.$"

VerityLakefront_Text_TrainerTipsSign:
	.string "TRAINER TIP\n"
	.string "A POKéMON's mood can change how\l"
	.string "well it battles for you.$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

VerityLakefront_EventScript_Placa1::
	msgbox VerityLakefront_Text_Placa1, MSGBOX_SIGN
	end

VerityLakefront_Text_Placa1:
	.string "Lake Verity Ahead\pAccording to legend, this lake is home\nto the Pokémon said to be 'The Being of\pEmotion.'\pIt is because of this Pokémon that\npeople can experience sorrow and joy.$"
