@ Treinadores de rota de LakeOfRage, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

@ TODO (leva de CONTEUDO, nao a de arte): a cena do Gyarados vermelho.
@ Hoje o objeto em (32, 28) e so decorativo: graphics_id
@ OBJ_EVENT_GFX_GYARADOS_VERMELHO, script "0", flag "0", parado.
@ A cena de verdade esta na fonte, em
@   fontes-mapas/hns/data/maps/LakeOfRage/scripts.inc  ->  LakeOfRage_EventScript_Gyarados
@ e o objeto de la usa flag FLAG_HIDE_LAKE_OF_RAGE_GYARADOS com
@ MOVEMENT_TYPE_WALK_SEQUENCE_RIGHT_UP_DOWN_LEFT. Quem portar a cena precisa
@ trazer a flag e o movimento junto, senao o shiny fica visivel antes da hora.

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
