@ PinwheelForest do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_PinwheelForest_MapScripts::
	.byte 0

Unova_PinwheelForest_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_PKMN_RANGERM_PINWHEEL_1, Unova_PinwheelForest_Text_PkmnRangerMPinwheel1SeenText, Unova_PinwheelForest_Text_PkmnRangerMPinwheel1BeatenText
	end

Unova_PinwheelForest_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_PKMN_RANGERM_PINWHEEL_2, Unova_PinwheelForest_Text_PkmnRangerMPinwheel2SeenText, Unova_PinwheelForest_Text_PkmnRangerMPinwheel2BeatenText
	end

Unova_PinwheelForest_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_PKMN_RANGERF_PINWHEEL_1, Unova_PinwheelForest_Text_PkmnRangerFPinwheel1SeenText, Unova_PinwheelForest_Text_PkmnRangerFPinwheel1BeatenText
	end

Unova_PinwheelForest_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_PKMN_RANGERF_PINWHEEL_2, Unova_PinwheelForest_Text_PkmnRangerFPinwheel2SeenText, Unova_PinwheelForest_Text_PkmnRangerFPinwheel2BeatenText
	end

Unova_PinwheelForest_EventScript_Lider10::
	trainerbattle_single TRAINER_UNOVA_YOUNGSTER_PINWHEEL, Unova_PinwheelForest_Text_YoungsterPinwheelSeenText, Unova_PinwheelForest_Text_YoungsterPinwheelBeatenText
	end

Unova_PinwheelForest_EventScript_Lider11::
	trainerbattle_single TRAINER_UNOVA_PSYCHICM_PINWHEEL, Unova_PinwheelForest_Text_PsychicMPinwheelSeenText, Unova_PinwheelForest_Text_PsychicMPinwheelBeatenText
	end

Unova_PinwheelForest_EventScript_Lider12::
	trainerbattle_single TRAINER_UNOVA_HEX_MANIAC_PINWHEEL, Unova_PinwheelForest_Text_HexManiacPinwheelSeenText, Unova_PinwheelForest_Text_HexManiacPinwheelBeatenText
	end

Unova_PinwheelForest_EventScript_Lider13::
	trainerbattle_single TRAINER_UNOVA_LASS_PINWHEEL, Unova_PinwheelForest_Text_LassPinwheelSeenText, Unova_PinwheelForest_Text_LassPinwheelBeatenText
	end

Unova_PinwheelForest_EventScript_Npc14::
	msgbox Unova_PinwheelForest_Text_PinwheelOfficerText, MSGBOX_NPC
	end

Unova_PinwheelForest_EventScript_Npc15::
	msgbox Unova_PinwheelForest_Text_PinwheelOfficerText, MSGBOX_NPC
	end

@ B6 Unova, Fase B (18/08/2026): os dois postos de bloqueio da fonte
@ (PinwheelOfficer1WalkScript@37-39,20 / PinwheelOfficer2WalkScript@36-38,25).
@ Sem checkevent na fonte: bloqueio permanente por desenho, nao par de portao
@ com desbloqueio em algum lugar. Reaproveita o mesmo texto do NPC 14/15 (o
@ oficial parado) e o mesmo VAR_TEMP_0/0 de sempre disparar (tecnica 1 do
@ SINNOH-PADRAO.md). Zero flag e zero var novas.
Unova_PinwheelForest_EventScript_OfficerBloqueiaNorte::
	lock
	turnobject LOCALID_PLAYER, DIR_WEST
	msgbox Unova_PinwheelForest_Text_PinwheelOfficerText, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PLAYER, Common_Movement_WalkUp
	waitmovement 0
	release
	end

Unova_PinwheelForest_EventScript_OfficerBloqueiaSul::
	lock
	turnobject LOCALID_PLAYER, DIR_EAST
	msgbox Unova_PinwheelForest_Text_PinwheelOfficerText, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PLAYER, Common_Movement_WalkDown
	waitmovement 0
	release
	end


Unova_PinwheelForest_Text_PkmnRangerMPinwheel1SeenText::
	.string "Onward, my bug"
	.string "\nPOKéMON swarm!$"

Unova_PinwheelForest_Text_PkmnRangerMPinwheel1BeatenText::
	.string "Pretty cool, huh?"
	.string "\nMy bug-type POKé-"
	.string "\lMON are the best!$"

Unova_PinwheelForest_Text_PkmnRangerMPinwheel2SeenText::
	.string "Hey, hey, hey! It's"
	.string "\nall because of"
	.string "\phavin' love for"
	.string "\nPOKéMON, right?"
	.string "\pYeah, you know"
	.string "\nwhat I mean!$"

Unova_PinwheelForest_Text_PkmnRangerMPinwheel2BeatenText::
	.string "Man, your love for"
	.string "\nPOKéMON hit me"
	.string "\plike a ton of"
	.string "\nbricks!$"

Unova_PinwheelForest_Text_PkmnRangerFPinwheel1SeenText::
	.string "I hold no grudge,"
	.string "\nwhether I win or"
	.string "\plose. The point of"
	.string "\nbattle is to train"
	.string "\pmy POKéMON, after"
	.string "\nall.$"

Unova_PinwheelForest_Text_PkmnRangerFPinwheel1BeatenText::
	.string "Aww… But I really"
	.string "\nwanted to win!$"

Unova_PinwheelForest_Text_PkmnRangerFPinwheel2SeenText::
	.string "Get great powers"
	.string "\ndrawn from nature"
	.string "\pwithout opposing"
	.string "\nit. That is the"
	.string "\pstrength of POKé-"
	.string "\nMON RANGERs!$"

Unova_PinwheelForest_Text_PkmnRangerFPinwheel2BeatenText::
	.string "What great power!"
	.string "\nYour POKéMON are"
	.string "\lmarvelous!$"

Unova_PinwheelForest_Text_YoungsterPinwheelSeenText::
	.string "The forest is full"
	.string "\nof little hollows"
	.string "\pand hillocks, and"
	.string "\nwalking in it is"
	.string "\lso fun!$"

Unova_PinwheelForest_Text_YoungsterPinwheelBeatenText::
	.string "Your POKéMON are"
	.string "\nso cool!$"

Unova_PinwheelForest_Text_PsychicMPinwheelSeenText::
	.string "This is a power"
	.string "\nspot! It awakens"
	.string "\pyour dormant"
	.string "\npower!$"

Unova_PinwheelForest_Text_PsychicMPinwheelBeatenText::
	.string "Did you spot my"
	.string "\nweakness?$"

Unova_PinwheelForest_Text_HexManiacPinwheelSeenText::
	.string "You… Who are you?"
	.string "\pThere is another"
	.string "\nperson here aside"
	.string "\lfrom me?$"

Unova_PinwheelForest_Text_HexManiacPinwheelBeatenText::
	.string "So, you are a"
	.string "\nnormal person… A"
	.string "\pnormal POKéMON"
	.string "\ntrainer…$"

Unova_PinwheelForest_Text_LassPinwheelSeenText::
	.string "Oh! And I just"
	.string "\nheard a POKéMON,"
	.string "\ltoo! Oh, boo…$"

Unova_PinwheelForest_Text_LassPinwheelBeatenText::
	.string "Your POKéMON seem"
	.string "\nkinda happy,"
	.string "\ltrainer!$"

Unova_PinwheelForest_Text_PinwheelOfficerText::
	.string "There's been a"
	.string "\nrobbery in NACRENE"
	.string "\lCITY."
	.string "\pWe're not letting"
	.string "\nanyone through"
	.string "\lright now.$"

@ Placas trazidas do BW3G por dev_scripts/importa_placas_unova.py

Unova_EventScript_GrutaTier2::
	lockall
	msgbox Unova_Text_AchouGruta, MSGBOX_DEFAULT
	randomelement ITEM_RED_SHARD, ITEM_BLUE_SHARD, ITEM_GREEN_SHARD, ITEM_YELLOW_SHARD, ITEM_DAMP_ROCK, ITEM_HEAT_ROCK, ITEM_SMOOTH_ROCK, ITEM_ICY_ROCK, ITEM_BIG_PEARL, ITEM_BIG_PEARL, ITEM_PROTEIN, ITEM_IRON, ITEM_CARBOS, ITEM_CALCIUM, ITEM_HP_UP, ITEM_ELIXIR
	giveitem VAR_RESULT
	releaseall
	end

@ Gruta escondida do BW3G (tier 2). ponytail: la ela reenche
@ todo dia; aqui e uma flag e o item sai uma vez so.
Unova_PinwheelForest_EventScript_Gruta4B6::
	goto_if_set FLAG_UNOVA_GRUTA_PINWHEELFOREST, Unova_EventScript_GrutaVazia
	setflag FLAG_UNOVA_GRUTA_PINWHEELFOREST
	goto Unova_EventScript_GrutaTier2

@ Leva de treinadores da Fase B (18/08/2026): TRAINER_UNOVA_INFER4_{SNIVY,
@ TEPIG,OSHAWOTT} (2170-2172) já existem, e a batalha está escrita abaixo
@ (Unova_PinwheelForest_EventScript_CenaInfer). LIGADA pela fiação final
@ (18/08/2026): objeto plantado em (14,27) com "local_id":
@ "LOCALID_PINWHEELFOREST_INFER" (gráfico OBJ_EVENT_GFX_MAXIE, o mesmo
@ SPRITE_INFER -> equivalente de dev_scripts/tabela_sprites_bw3g.py);
@ dois coord_event/trigger em (8,26) e (8,27), mesma
@ coordenada da fonte (mapa sem offset, conferido pelos coord_event dos
@ oficiais já plantados nesta mesma leva), técnica 1 do SINNOH-PADRAO.md
@ (VAR_TEMP_0 == 0, sempre dispara). `setvar VAR_LAST_TALKED, LOCALID_
@ PINWHEELFOREST_INFER` acrescentado logo apos o `lockall`, igual ao
@ molde de Route209_Access_EventScript_CoordEvent_Rival de Sinnoh
@ (emboscada por coordevent precisa disso pra trainerbattle_no_intro
@ revelar o objeto certo).
@ Switch por VAR_STARTER_MON (0=Snivy/1=Tepig/2=Oshawott, mesmo alias que
@ Unova_NuvemaLab já grava), molde de Route203_EventScript_CoordEvent_
@ Rival de Sinnoh. Regra da casa conferida contra maps/PinwheelForest.asm
@ da fonte: o sufixo INFER4_X nomeia o Pokémon DO INFER (contra-tipo), não
@ o do jogador — jogador com Oshawott leva INFER4_SNIVY (Servine, grama
@ bate água), jogador com Snivy leva INFER4_TEPIG (Pignite, fogo bate
@ grama), jogador com Tepig leva INFER4_OSHAWOTT (Dewott, água bate fogo).
@ Sem flag/var nova de "já venceu": `goto_if_defeated` cobre as 3
@ variantes juntas (mesmo trainer "moral", ids diferentes so pelo time).
@
@ COMO A INFER SOME DEPOIS DE DERROTADA, com ZERO flag nova (conserto de
@ 18/08/2026). A nota anterior daqui dizia que "a fonte nunca seta nem limpa
@ EVENT_PINWHEEL_FOREST_INFER em lugar nenhum". É FALSO, e o objeto ficava
@ plantado para sempre por causa disso: `maps/PinwheelForest.asm:96` tem
@ `disappear PINWHEELFOREST_INFER` no fecho da cena, e no gen 2 `disappear`
@ ACENDE justamente o event flag do object_event (o último campo da linha 571
@ da fonte é EVENT_PINWHEEL_FOREST_INFER). O mesmo vale para o BRONIUS em
@ `maps/VirbankComplexB1F.asm:82`.
@ Aqui isso vira o par que a casa já usa nas cenas da Obra 1
@ (Unova_GiantChasm1F e Unova_DragonspiralTower6F): `removeobject` no fecho
@ some com ela NESTA visita, e o campo `flag` do object_event some com ela nas
@ próximas. A flag é a de treinador derrotado do próprio motor,
@ TRAINER_FLAGS_START + TRAINER_UNOVA_INFER4_SNIVY, mesma régua de custo zero
@ de Unova_PkmnLeagueMain.
@ POR QUE AS TRÊS `setflag` no fecho, e não a flag de quem foi lutado: o
@ object_event tem UM campo `flag` só, e a batalha tem TRÊS variantes; o motor
@ acende apenas a do id efetivamente derrotado, então em 2 das 3 partidas a
@ flag do campo ficaria apagada e a INFER renasceria na próxima entrada. Como
@ as três variantes já são o MESMO encontro para todo efeito neste arquivo (os
@ três `goto_if_defeated` acima são um OU), acender as três no fecho deixa o
@ estado coerente e torna irrelevante qual delas mora no campo `flag`.
@
@ COREOGRAFIA (18/08/2026), da fonte, rotas conferidas tile a tile em
@ data/layouts/Unova_PinwheelForest/map.bin (todas colisão 0, elevação 3,
@ igual à do objeto):
@   `PinwheelInferScript1` (gatilho (8,26)) usa `PinwheelInferArriveMovement1`
@   (step UP + 5x LEFT: (14,27) -> (14,26) -> (9,26)) e `...Script2` (gatilho
@   (8,27)) usa `...ArriveMovement2` (5x LEFT: (14,27) -> (9,27)). É por isso
@   que a fonte tem DOIS rótulos: cada tile de gatilho tem a sua aproximação,
@   e as duas terminam ao lado do jogador. A INFER anda para oeste, portanto
@   termina virada para o jogador sem precisar de `face_`.
@   `PinwheelInferLeaveMovement` (5x big_step RIGHT) devolve ela a (14,26) ou
@   (14,27) antes do `disappear`.
Unova_PinwheelForest_EventScript_Infer1::
	goto_if_defeated TRAINER_UNOVA_INFER4_SNIVY, Unova_PinwheelForest_EventScript_InferFim
	goto_if_defeated TRAINER_UNOVA_INFER4_TEPIG, Unova_PinwheelForest_EventScript_InferFim
	goto_if_defeated TRAINER_UNOVA_INFER4_OSHAWOTT, Unova_PinwheelForest_EventScript_InferFim
	lockall
	applymovement LOCALID_PINWHEELFOREST_INFER, Unova_PinwheelForest_Movement_InferChega1
	waitmovement 0
	goto Unova_PinwheelForest_EventScript_CenaInfer

Unova_PinwheelForest_EventScript_Infer2::
	goto_if_defeated TRAINER_UNOVA_INFER4_SNIVY, Unova_PinwheelForest_EventScript_InferFim
	goto_if_defeated TRAINER_UNOVA_INFER4_TEPIG, Unova_PinwheelForest_EventScript_InferFim
	goto_if_defeated TRAINER_UNOVA_INFER4_OSHAWOTT, Unova_PinwheelForest_EventScript_InferFim
	lockall
	applymovement LOCALID_PINWHEELFOREST_INFER, Unova_PinwheelForest_Movement_InferChega2
	waitmovement 0

Unova_PinwheelForest_EventScript_CenaInfer::
	setvar VAR_LAST_TALKED, LOCALID_PINWHEELFOREST_INFER
	msgbox Unova_PinwheelForest_Text_InferIntro, MSGBOX_DEFAULT
	call_if_eq VAR_STARTER_MON, 0, Unova_PinwheelForest_EventScript_InferBattleTepig
	call_if_eq VAR_STARTER_MON, 1, Unova_PinwheelForest_EventScript_InferBattleOshawott
	call_if_eq VAR_STARTER_MON, 2, Unova_PinwheelForest_EventScript_InferBattleSnivy
	msgbox Unova_PinwheelForest_Text_InferAfter, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PINWHEELFOREST_INFER, Unova_PinwheelForest_Movement_InferSai
	waitmovement 0
	setflag TRAINER_FLAGS_START+TRAINER_UNOVA_INFER4_SNIVY
	setflag TRAINER_FLAGS_START+TRAINER_UNOVA_INFER4_TEPIG
	setflag TRAINER_FLAGS_START+TRAINER_UNOVA_INFER4_OSHAWOTT
	removeobject LOCALID_PINWHEELFOREST_INFER
Unova_PinwheelForest_EventScript_InferFim::
	releaseall
	end

@ `PinwheelInferArriveMovement1` da fonte: step UP + 5x step LEFT.
Unova_PinwheelForest_Movement_InferChega1:
	walk_up
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

@ `PinwheelInferArriveMovement2` da fonte: 5x step LEFT.
Unova_PinwheelForest_Movement_InferChega2:
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

@ `PinwheelInferLeaveMovement` da fonte: 5x big_step RIGHT.
Unova_PinwheelForest_Movement_InferSai:
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	step_end

Unova_PinwheelForest_EventScript_InferBattleSnivy::
	trainerbattle_no_intro TRAINER_UNOVA_INFER4_SNIVY, Unova_PinwheelForest_Text_InferWin
	return

Unova_PinwheelForest_EventScript_InferBattleTepig::
	trainerbattle_no_intro TRAINER_UNOVA_INFER4_TEPIG, Unova_PinwheelForest_Text_InferWin
	return

Unova_PinwheelForest_EventScript_InferBattleOshawott::
	trainerbattle_no_intro TRAINER_UNOVA_INFER4_OSHAWOTT, Unova_PinwheelForest_Text_InferWin
	return

Unova_PinwheelForest_Text_InferIntro:
	.string "INFER: You again?\p"
	.string "I don't have time to deal with\n"
	.string "you right now.\p"
	.string "What? A robbery? What, you think\n"
	.string "I have something to do with it?\p"
	.string "Tch! The nerve! I'll beat you\n"
	.string "down right here!$"

Unova_PinwheelForest_Text_InferWin:
	.string "H-how can this be?$"

Unova_PinwheelForest_Text_InferAfter:
	.string "I-I don't understand. How can I\n"
	.string "keep losing?\p"
	.string "I promise you, I'm going to keep\n"
	.string "getting stronger, and beat you!\p"
	.string "Don't follow me!$"
