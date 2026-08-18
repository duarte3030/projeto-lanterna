Route202_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route202_OnTransition
	.byte 0

Route202_OnTransition::
	checkplayergender
	goto_if_eq VAR_RESULT, MALE, Route202_SetCounterpartFemale
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_BRENDAN_NORMAL
	end

Route202_SetCounterpartFemale::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_MAY_NORMAL
	end

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
@ Fonte: Route202_CoordEvent_CatchingTutorial. A contraparte demonstra como
@ capturar um Pokemon selvagem e da 5 Poke Balls ao jogador.
@
@ ponytail, cortado da fonte: o gatilho de tutorial fica atras de
@ FLAG_RECEIVED_PARCEL (missao de entregar uma encomenda ao ROWAN que nao
@ existe nesta obra) e da special StartCatchingTutorial, que tambem nao
@ existe neste motor (grep vazio em src/ e include/). Sem a batalha
@ demonstrativa de verdade, a cena vai direto da fala de aviso para o
@ presente das 5 Poke Balls, cortando o comentario "abaixe o HP antes" que
@ so faz sentido depois de ver a demonstracao.
Route202_EventScript_CoordEvent_CatchingTutorial::
	lockall
	applymovement LOCALID_COUNTERPART, Route202_Movement_CounterpartNoticePlayer
	waitmovement 0
	checkplayergender
	goto_if_eq VAR_RESULT, MALE, Route202_EventScript_DawnDemonstrate
	msgbox Route202_Text_LucasIllDemonstrateHowToCatch, MSGBOX_DEFAULT
	goto Route202_EventScript_GivePokeballs

Route202_EventScript_DawnDemonstrate::
	msgbox Route202_Text_DawnIllDemonstrateHowToCatch, MSGBOX_DEFAULT

Route202_EventScript_GivePokeballs::
	giveitem_msg Route202_Text_ReceivedPokeBalls, ITEM_POKE_BALL, 5
	applymovement LOCALID_COUNTERPART, Route202_Movement_CounterpartLeave
	waitmovement 0
	@ A contraparte foi embora de vez: acende a flag do proprio object_event
	@ (FLAG_HIDE_ROUTE_202_COUNTERPART na fonte) antes do `removeobject`,
	@ senao ela renasce a cada entrada na rota. A fonte nao acende porque la
	@ ela vai e volta pelo reveza-mapa Sandgem <-> Route202
	@ (CounterpartTalk_RemoveCounterpart e Route202_CounterpartPokeRadarEnd
	@ trocam ClearFlag entre os dois mapas); esse reveza depende da cena de
	@ PokeRadar, que e Poketch e nao existe aqui (decisao 3 do plano). Sem a
	@ volta, a saida e definitiva.
	setflag FLAG_SINNOH_ESCONDE_ROUTE_202_COUNTERPART
	removeobject LOCALID_COUNTERPART
	setvar VAR_SINNOH_R202_ESTADO, 1
	releaseall
	end

	.balign 4, 0
Route202_Movement_CounterpartNoticePlayer:
	emote_exclamation_mark
	step_end

	.balign 4, 0
Route202_Movement_CounterpartLeave:
	walk_down
	walk_down
	set_invisible
	step_end

Route202_Text_DawnIllDemonstrateHowToCatch:
	.string "{RIVAL}: Oh, that's right!\n"
	.string "{PLAYER}, I haven't shown you how to\l"
	.string "catch a Pokémon.\p"
	.string "I'll demonstrate how to catch\n"
	.string "one, so just watch me, OK?$"

Route202_Text_LucasIllDemonstrateHowToCatch:
	.string "{RIVAL}: {PLAYER}, do you know\n"
	.string "how to catch a Pokémon?\p"
	.string "I'll demonstrate how to catch\n"
	.string "one, so just watch, OK?$"

Route202_Text_ReceivedPokeBalls:
	.string "{PLAYER} received 5 POKé BALLS\n"
	.string "from {RIVAL}!$"

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

Route202_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_YOUNGSTER_TRISTAN, Route202_Text_Trainer1Intro, Route202_Text_Trainer1Defeat
	msgbox Route202_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route202_Text_Trainer1Intro:
	.string "You're a Pokémon Trainer, and so am I!\n"
	.string "Our eyes met, so battle we must!$"

Route202_Text_Trainer1Defeat:
	.string "Too strong!\n"
	.string "Too strong!$"

Route202_Text_Trainer1Post:
	.string "Don't be shy about talking to\n"
	.string "Trainers you'd like to battle.\pPokémon grow stronger and stronger\n"
	.string "from battling.$"

Route202_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_LASS_NATALIE, Route202_Text_Trainer2Intro, Route202_Text_Trainer2Defeat
	msgbox Route202_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route202_Text_Trainer2Intro:
	.string "I spy, with my little eye...\n"
	.string "A Trainer!\pA battle, please!$"

Route202_Text_Trainer2Defeat:
	.string "Oh, boo!\n"
	.string "I can't win!$"

Route202_Text_Trainer2Post:
	.string "My Pokémon are all tuckered out!\n"
	.string "I need to go to a Pokémon Center!$"

Route202_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_YOUNGSTER_LOGAN, Route202_Text_Trainer3Intro, Route202_Text_Trainer3Defeat
	msgbox Route202_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route202_Text_Trainer3Intro:
	.string "Let's have a Pokémon battle!\n"
	.string "Humph! But I'm gonna win!$"

Route202_Text_Trainer3Defeat:
	.string "You beat me?!\n"
	.string "You've got talent!$"

Route202_Text_Trainer3Post:
	.string "It was fun battling!\n"
	.string "Yup! I'm going to battle everyone!$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route202_EventScript_Placa1::
	msgbox Route202_Text_Placa1, MSGBOX_SIGN
	end

Route202_Text_Placa1:
	.string "Rt. 202\nSandgem Town$"

Route202_EventScript_Placa2::
	msgbox Route202_Text_Placa2, MSGBOX_SIGN
	end

Route202_Text_Placa2:
	.string "Rt. 202\nJubilife City$"

Route202_EventScript_Placa3::
	msgbox Route202_Text_Placa3, MSGBOX_SIGN
	end

Route202_Text_Placa3:
	.string "Trainer Tips!\pAll Pokémon that are involved in\na battle earn Exp. Points!\pThe more your Pokémon battle,\nthe stronger they will become.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route202_EventScript_Npc1::
	msgbox Route202_Text_Npc1, MSGBOX_NPC
	end

Route202_Text_Npc1:
	.string "Some Pokémon only appear in the\nmorning.\pSome only come out at night.\pI'll keep looking till I've seen them\nall!$"
