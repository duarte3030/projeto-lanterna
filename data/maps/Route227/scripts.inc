@ Referencia de treinador de Sinnoh. Ver Pokemon Claude/SINNOH-PADRAO.md.
@ Falas vindas de pret/pokeplatinum, em ingles, como o resto do jogo.

Route227_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S7: cena da fonte, rotulo Route227_CoordEvent_Buck >>>
@ Buck (LOCALID_ROUTE227_BUCK, OBJ_EVENT_GFX_HIKER: nao existe OBJ_EVENT_GFX_
@ BUCK aqui, mesmo molde de RICH_BOY pro Rival e MAGMA_MEMBER_M pro grunt) ja
@ nasce visivel (fonte nao faz ClearFlag/AddObject nesta cena, so
@ ApplyMovement); FLAG_HIDE_ROUTE_227_BUCK da fonte NAO esta no censo do S1
@ (nao e um dos 247 grupos), entao fica sem alias aqui e o objeto sem `flag`
@ de esconder (visivel sempre). Pede a patrulha da Stark Mountain; a fonte
@ nao remove ele no fim (fica plantado esperando o jogador aparecer la).
Route227_EventScript_CoordEvent_Buck::
	lockall
	applymovement LOCALID_ROUTE227_BUCK, Route227_Movement_BuckNoticePlayer
	applymovement OBJ_EVENT_ID_PLAYER, Route227_Movement_PlayerFaceBuck
	waitmovement 0
	goto Route227_EventScript_AskPatrolStarkMountain
	end

Route227_EventScript_AskPatrolStarkMountain::
	msgbox Route227_Text_PatrolStarkMountain, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Route227_EventScript_GoonsCausingTrouble
	goto_if_eq VAR_RESULT, NO, Route227_EventScript_IllKeepAsking
	end

Route227_EventScript_IllKeepAsking::
	msgbox Route227_Text_IllKeepAsking, MSGBOX_DEFAULT
	goto Route227_EventScript_AskPatrolStarkMountain
	end

Route227_EventScript_GoonsCausingTrouble::
	applymovement LOCALID_ROUTE227_BUCK, Route227_Movement_BuckWalkOnSpotNorth
	waitmovement 0
	msgbox Route227_Text_GoonsCausingTrouble, MSGBOX_DEFAULT
	applymovement LOCALID_ROUTE227_BUCK, Route227_Movement_BuckWalkOnSpotSouth
	waitmovement 0
	msgbox Route227_Text_WhatMe, MSGBOX_DEFAULT
	setvar VAR_SINNOH_R227_BUCK_ESTADO, 1
	releaseall
	end

Route227_Movement_BuckNoticePlayer:
	walk_in_place_down
	emote_exclamation_mark
	walk_down
	step_end

Route227_Movement_PlayerFaceBuck:
	face_up
	step_end

Route227_Movement_BuckWalkOnSpotNorth:
	walk_in_place_up
	step_end

Route227_Movement_BuckWalkOnSpotSouth:
	walk_in_place_down
	step_end

Route227_Text_PatrolStarkMountain:
	.string "Buck: Yo, if it isn't {PLAYER}!\n"
	.string "Out training right away, are you?\p"
	.string "So, uh, since you're training anyway,\n"
	.string "can you do me a favor?\p"
	.string "I'd like you to patrol Stark Mountain\n"
	.string "for me.$"

Route227_Text_IllKeepAsking:
	.string "I'll keep asking the same thing over and\n"
	.string "over until you say “Yes!”$"

Route227_Text_GoonsCausingTrouble:
	.string "Buck: Up past here, there's this\n"
	.string "volcano. It's Stark Mountain.\p"
	.string "Deep inside it is this special rock\n"
	.string "called the Magma Stone.\p"
	.string "I can't explain it well, but it's\n"
	.string "really important. It keeps a Pokémon\l"
	.string "asleep.\p"
	.string "But lately, I've been hearing rumors\n"
	.string "about vandals in Stark Mountain.\p"
	.string "They say goons in space suits are\n"
	.string "causing trouble there.$"

Route227_Text_WhatMe:
	.string "Huh?\n"
	.string "What, me?\p"
	.string "I was on my way to the Pokémon Center\n"
	.string "because my Pokémon's low on HP.\p"
	.string "So, if you could get up to Stark\n"
	.string "Mountain now, that'd be great. Thanks!$"

@ <<< B6 Sinnoh S7: cena da fonte <<<

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
@ BLOQUEADO: precisa de LOCALID_CRASHER_WAKE, e FLAG_HIDE_ROUTE_227_CRASHER_
@ WAKE (fonte) nao esta no censo do S1 (nao e um dos 247 grupos de
@ hidden_flag; `grep` em dev_scripts/maquina_sinnoh.json confirma zero
@ ocorrencias). Mesmo buraco do Crasher Wake em PastoriaCity e Villa (ver
@ comentario la); sem endereco de flag da condutora, plantar o objeto
@ permanentemente visivel do boot do jogo era bug novo, e nao plantar deixa
@ o gatilho sem cena. Volta ao plano.
Route227_EventScript_CoordEvent_WakeRival::
	end

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

Route227_EventScript_AceTrainerSaul::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_SAUL, Route227_Text_AceTrainerSaulIntro, Route227_Text_AceTrainerSaulDefeat
	msgbox Route227_Text_AceTrainerSaulPost, MSGBOX_AUTOCLOSE
	end

Route227_EventScript_RangerFelicia::
	trainerbattle_single TRAINER_SINNOH_RANGER_FELICIA, Route227_Text_RangerFeliciaIntro, Route227_Text_RangerFeliciaDefeat
	msgbox Route227_Text_RangerFeliciaPost, MSGBOX_AUTOCLOSE
	end

Route227_EventScript_BlackBeltGriffin::
	trainerbattle_single TRAINER_SINNOH_BLACK_BELT_GRIFFIN, Route227_Text_BlackBeltGriffinIntro, Route227_Text_BlackBeltGriffinDefeat
	msgbox Route227_Text_BlackBeltGriffinPost, MSGBOX_AUTOCLOSE
	end

Route227_EventScript_AceTrainerMikayla::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_MIKAYLA, Route227_Text_AceTrainerMikaylaIntro, Route227_Text_AceTrainerMikaylaDefeat
	msgbox Route227_Text_AceTrainerMikaylaPost, MSGBOX_AUTOCLOSE
	end

Route227_EventScript_SignArrow::
	msgbox Route227_Text_SignArrow, MSGBOX_SIGN
	end

Route227_Text_AceTrainerSaulIntro:
	.string "I've got the urge to battle with you.\n"
	.string "Hope you're willing to oblige!$"

Route227_Text_AceTrainerSaulDefeat:
	.string "I shouldn't have paid attention\n"
	.string "to my urge...$"

Route227_Text_AceTrainerSaulPost:
	.string "So long as my partner's alongside me,\n"
	.string "I'm willing to take on the world!$"

Route227_Text_RangerFeliciaIntro:
	.string "We've grown strong together in\n"
	.string "nature and in the concrete jungle.\p"
	.string "We make everywhere we go our\n"
	.string "playground!$"

Route227_Text_RangerFeliciaDefeat:
	.string "You're really tough, aren't you?!$"

Route227_Text_RangerFeliciaPost:
	.string "Look around you at this wildly\n"
	.string "contorted terrain.\p"
	.string "It's no wonder that Pokémon would\n"
	.string "grow tough in a place like this.$"

Route227_Text_BlackBeltGriffinIntro:
	.string "I have meditated under a waterfall\n"
	.string "to temper my spirit.\p"
	.string "Allow me to demonstrate its strength!$"

Route227_Text_BlackBeltGriffinDefeat:
	.string "Ha-choo! Sniffle...$"

Route227_Text_BlackBeltGriffinPost:
	.string "All that time under the waterfall...\n"
	.string "Seems I've caught a cold.$"

Route227_Text_AceTrainerMikaylaIntro:
	.string "The world is huge, and there are\n"
	.string "so many different Pokémon!\p"
	.string "What kinds of Pokémon are with you?\n"
	.string "Please, I want to have a look!$"

Route227_Text_AceTrainerMikaylaDefeat:
	.string "Wow, there are Pokémon that\n"
	.string "wonderful!$"

Route227_Text_AceTrainerMikaylaPost:
	.string "There is always something to like\n"
	.string "about any Pokémon.\p"
	.string "It's so hard to decide which ones\n"
	.string "I should raise.$"

Route227_Text_SignArrow:
	.string "ROUTE 226\n"
	.string "This way, to the south.$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route227_EventScript_Placa1::
	msgbox Route227_Text_Placa1, MSGBOX_SIGN
	end

Route227_Text_Placa1:
	.string "Rt. 227\nStark Mountain$"
