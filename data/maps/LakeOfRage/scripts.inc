@ Treinadores de rota de LakeOfRage, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

@ FEITO em 18/08/2026: a cena do Gyarados vermelho esta no bloco marcado no FIM
@ deste arquivo, portada de
@   fontes-mapas/hns/data/maps/LakeOfRage/scripts.inc -> LakeOfRage_EventScript_Gyarados
@ pelo dev_scripts/porta_cenas_johto.py (--cenas). NAO editar a mao: o bloco
@ entre as marcas `>>> B6 Johto: cena portada do hns` e reescrito por inteiro a
@ cada rodada da ferramenta, e conserto a mao seria apagado calado. O que muda
@ mora em CENAS/PODA/TROCA de la, que e onde estao escritos os cortes (LANCE,
@ ESCAMA VERMELHA, var de Mahogany) e a substituicao do `setwildbattleshiny`,
@ comando que este motor nao tem.
@ O objeto de (32,28) deixou de ser decorativo: ganhou o script e a flag
@ FLAG_HIDE_LAKE_OF_RAGE_GYARADOS, que a propria cena acende ao vencer ou
@ capturar. Fica PARADO de proposito (a fonte usa
@ MOVEMENT_TYPE_WALK_SEQUENCE_RIGHT_UP_DOWN_LEFT); o motivo esta na cena.

LakeOfRage_MapScripts::
	.byte 0

LakeOfRage_EventScript_Andre::
	trainerbattle_single TRAINER_JOHTO_ANDRE, LakeOfRage_Text_AndreSeen, LakeOfRage_Text_AndreBeaten
	msgbox LakeOfRage_Text_AndreAfter, MSGBOX_AUTOCLOSE
	end

LakeOfRage_EventScript_Raymond::
	trainerbattle_single TRAINER_JOHTO_RAYMOND, LakeOfRage_Text_RaymondSeen, LakeOfRage_Text_RaymondBeaten
	msgbox LakeOfRage_Text_RaymondAfter, MSGBOX_AUTOCLOSE
	end

LakeOfRage_EventScript_Aaron::
	trainerbattle_single TRAINER_JOHTO_AARON, LakeOfRage_Text_AaronSeen, LakeOfRage_Text_AaronBeaten
	msgbox LakeOfRage_Text_AaronAfter, MSGBOX_AUTOCLOSE
	end

LakeOfRage_EventScript_Lois::
	trainerbattle_single TRAINER_JOHTO_LOIS, LakeOfRage_Text_LoisSeen, LakeOfRage_Text_LoisBeaten
	msgbox LakeOfRage_Text_LoisAfter, MSGBOX_AUTOCLOSE
	end

LakeOfRage_Text_AndreSeen:
	.string "Let me battle with the POKéMON I\n"
	.string "just caught!$"

LakeOfRage_Text_AndreBeaten:
	.string "I might be an expert angler, but\n"
	.string "I stink as a POKéMON trainer…$"

LakeOfRage_Text_AndreAfter:
	.string "I won't lose as an angler! I catch\n"
	.string "POKéMON all day.$"

LakeOfRage_Text_RaymondSeen:
	.string "No matter what I do, all I catch\n"
	.string "are the same POKéMON…$"

LakeOfRage_Text_RaymondBeaten:
	.string "My line's all tangled up…$"

LakeOfRage_Text_RaymondAfter:
	.string "Why can't I catch any good\n"
	.string "POKéMON?$"

LakeOfRage_Text_AaronSeen:
	.string "If a trainer spots another trainer,\n"
	.string "he has to make a challenge.\p"
	.string "That is our destiny.$"

LakeOfRage_Text_AaronBeaten:
	.string "Whew… Good battle.$"

LakeOfRage_Text_AaronAfter:
	.string "POKéMON and their trainer become\n"
	.string "powerful through constant battling.$"

LakeOfRage_Text_LoisSeen:
	.string "What happened to the red\n"
	.string "GYARADOS?\p"
	.string "It's gone?\p"
	.string "Oh, darn. I came here for\n"
	.string "nothing?\p"
	.string "I know--let's battle!$"

LakeOfRage_Text_LoisBeaten:
	.string "Good going!$"

LakeOfRage_Text_LoisAfter:
	.string "Come to think of it, I've seen a\n"
	.string "pink BUTTERFREE.$"

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

LakeOfRage_EventScript_Sign1::
	msgbox LakeOfRage_Text_Sign, MSGBOX_SIGN
	end

LakeOfRage_EventScript_Sign2::
	msgbox LakeOfRage_Text_FishingGuruSign, MSGBOX_SIGN
	end

LakeOfRage_Text_FishingGuruSign::
    .string "FISHING GURU'S HOUSE$"

LakeOfRage_Text_Sign::
    .string "LAKE OF RAGE,\n"
    .string "also known as GYARADOS LAKE.$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

LakeOfRage_EventScript_Lass::
	msgbox LakeOfRage_Text_CooltrainerF, MSGBOX_NPC
	end

LakeOfRage_Text_CooltrainerF::
    .string "Did my eyes deceive me? I saw a\n"
    .string "red GYARADOS in the LAKE…\p"
    .string "But I thought GYARADOS were\n"
    .string "usually blue?$"

LakeOfRage_EventScript_Nerd::
	msgbox LakeOfRage_Text_SuperNerd, MSGBOX_NPC
	end

LakeOfRage_Text_SuperNerd::
    .string "I heard this lake was made by\n"
    .string "rampaging GYARADOS.\p"
    .string "I wonder if there is any\n"
    .string "connection to their mass outbreak\l"
    .string "now?$"

@ >>> B6 Johto: cena portada do hns (porta_cenas_johto.py) >>>
@ o GYARADOS VERMELHO do meio do lago: fala com ele e ele ataca (shiny, nível 30); vencer OU capturar tira o objeto do mapa para sempre
.set LOCALID_LAKEOFRAGE_LAKEOFRAGE_GYARADOS, 8

LakeOfRage_EventScript_Ran_Gyarados::
	release
	end

LakeOfRage_EventScript_Defeated_Gyarados::
	setflag FLAG_HIDE_LAKE_OF_RAGE_GYARADOS
	removeobject LOCALID_LAKEOFRAGE_LAKEOFRAGE_GYARADOS
	release
	end

LakeOfRage_EventScript_Gyarados::
	lock
	faceplayer
	msgbox LakeOfRage_Text_GyaradosCry, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_GYARADOS, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setflag FLAG_JOHTO_SHINY_FORCADO
	setwildbattle SPECIES_GYARADOS, 30
	clearflag FLAG_JOHTO_SHINY_FORCADO
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, LakeOfRage_EventScript_Defeated_Gyarados
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, LakeOfRage_EventScript_Ran_Gyarados
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, LakeOfRage_EventScript_Ran_Gyarados
	goto LakeOfRage_EventScript_Defeated_Gyarados

LakeOfRage_Text_GyaradosCry::
    .string "GYARADOS: Gyashaa!$"

@ <<< B6 Johto: cena portada do hns <<<
