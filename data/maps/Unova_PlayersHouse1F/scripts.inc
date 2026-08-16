@ PlayersHouse1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@ Cenas de abertura escritas a mao em 15/08/2026 (B6 Unova, Obra 1, bloco A6),
@ no molde de data/maps/Unova_ChampionsRoom/scripts.inc.
@
@ A CENA DA MAE. A fonte tem `MeetMomLeftScript` (que so acende
@ EVENT_TEMPORARY_UNTIL_MAP_RELOAD_1 e CAI no proximo) e `MeetMomRightScript`,
@ disparados pelos dois `coord_event` de (8,4) e (9,4). O fallthrough da fonte
@ esta preservado aqui: quem pisa em (8,4) acende o bit e continua no mesmo
@ corpo, exatamente como la.
@
@ PARA QUE SERVE O BIT: ele diz de QUAL tile o jogador veio. De (8,4) ele ja
@ esta encostado na MAE (7,4), entao ela so vira a cabeca; de (9,4) ela precisa
@ dar um passo lento para a direita para chegar perto. No fim, o movimento e
@ desfeito na mesma medida. O bit de RECARGA_2 e a terceira porta da fonte ("o
@ jogador comecou a cena FALANDO com a MAE", `MomScript` -> `MeetMomTalked
@ Script`): esse caminho e do script do NPC, que NAO faz parte destas duas
@ cenas e continua sendo o msgbox simples de Npc0/Npc2; a porta fica escrita
@ para o dia em que `MomScript` for portado, e por isso o bit e apagado no fim.
@ No gen 2 esses dois EVENT_TEMPORARY_UNTIL_MAP_RELOAD sao zerados pelo motor
@ a cada recarga de mapa; aqui sao flag comum e quem zera e a propria cena.
@
@ A PROTECAO DA ABERTURA, e por que ela importa nesta ROM. No BW3G esta e a
@ primeira casa do jogo; aqui UNOVA e a QUINTA regiao, e o jogador chega de
@ barco em VIRBANK (data/scripts/travessia_regioes.inc: o destino UNOVA so
@ aparece no menu com FLAG_ELITE_SINNOH_VENCIDA). HUMILAU, onde esta casa fica
@ (o warp de saida cai em MAP_UNOVA_HUMILAU_CITY), e alcancada andando, muito
@ depois. Entao a cena NAO roda na chegada em Unova: ela roda na primeira vez
@ que o jogador entra nesta casa e pisa em (8,4)/(9,4), e VAR_UNOVA_CASA_
@ JOGADOR_1F_CENA passa a 1 (SCENE_FINISHED) DENTRO da cena, antes de qualquer
@ movimento de volta, entao nem uma reentrada no meio dela reabre o gatilho.
@ Nada aqui move o jogador, nada aqui warpa e o fecho e `releaseall`/`end` nos
@ tres caminhos: no pior caso a cena e uma caixa de texto, nunca uma prisao.
@
@ O QUE FOI DESCARTADO, e o motivo (decisao 7 do PLANO-OBRAS-UNOVA.md, secao
@ "Tabela de conversao gen 2 -> este motor"):
@   `special SetDayOfWeek`, `special InitialSetDSTFlag` e `special
@   InitialClearDSTFlag` sao o acerto de relogio do gen 2 e nao tem equivalente
@   aqui; sairam SEM substituto inventado. Com eles saem os dois `yesorno` que
@   so existiam para alimenta-los e os TRES textos que so falam desse menu
@   (WhatDayIsItText, IsItDSTText e MomGivesXtranText, este ultimo "adjust your
@   clock for Daylight Saving Time in the XTRANSCIEVER menu"). O recado que
@   MomGivesXtranText fecha ("hurry on over to MARLON's house") ja esta, com as
@   mesmas palavras, dentro de MarlonLookingForYouText, que fica.
@   `stringtotext GearName` + `jumpstd receiveitem` + `setflag ENGINE_POKEGEAR`
@   + `setflag ENGINE_PHONE_CARD` + `addcellnum PHONE_MOM`: o XTRANSCEIVER e o
@   POKEGEAR do gen 2 e este motor nao tem POKEGEAR nem lista telefonica
@   (`grep -rn "POKEGEAR\|addcellnum\|XTRANSC" src include data` nao acha nada),
@   entao nao ha item nem sistema para entregar. A MAE continua MANDANDO levar
@   o aparelho na fala, que e a parte que sobrevive sem mecanica.
@   `special RestartMapMusic` vira `fadedefaultbgm`, e `playmusic MUSIC_MOM`
@   vira `playbgm MUS_LITTLEROOT` (tema da cidade natal desta build; a fonte
@   tem uma faixa propria que nao existe aqui).
@
@ OS QUATRO OBJETOS DE MAE DA FONTE VIRARAM DOIS. A fonte tem MOM1 em (7,4)
@ escondida por EVENT_PLAYERS_HOUSE_MOM_1 e TRES copias por EVENT_PLAYERS_HOUSE
@ _MOM_2, uma por horario do dia (MORN em (2,2), DAY em (7,4), NITE em (0,2));
@ quem separa as tres la e o campo de HORARIO do `object_event` do gen 2, que o
@ `object_event` deste motor NAO tem (data/maps/*/map.json nao tem esse campo).
@ Mantidas as duas que a maquina de flags consegue distinguir, a de cena e a de
@ DAY, que estao NO MESMO tile (7,4) com o mesmo sprite e o mesmo script: a
@ troca do fim da cena e invisivel para o jogador, que e o efeito certo. As
@ copias de MORN e NITE foram REMOVIDAS do map.json (com os scripts Npc1 e Npc3,
@ que ficariam orfaos): com flag 0 elas apareciam TODAS juntas, tres MAEs na
@ mesma sala, e nao ha flag sobrando para esconde-las (janela de save fechada).
@ EVENT_PLAYERS_HOUSE_MOM_2 nasce ACESA no gen 2 (`setevent` no bloco de
@ inicializacao de engine/events/std_scripts.asm, linha 563); aqui quem garante
@ esse estado inicial e o ON_TRANSITION abaixo, lendo a var da cena.

Unova_PlayersHouse1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Unova_PlayersHouse1F_OnTransition
	.byte 0

@ Roda ANTES de InitMap() criar os object_events (tecnica 2 do SINNOH-PADRAO.md),
@ entao a flag escrita aqui ja decide quem nasce.
Unova_PlayersHouse1F_OnTransition:
	goto_if_eq VAR_UNOVA_CASA_JOGADOR_1F_CENA, 0, Unova_PlayersHouse1F_EventScript_TransicaoAntesDaCena
	@ cena ja rodou: fica a MAE de depois (id 2), no mesmo tile
	setflag FLAG_UNOVA_CASA_JOGADOR_MAE_1
	clearflag FLAG_UNOVA_CASA_JOGADOR_MAE_2
	end

Unova_PlayersHouse1F_EventScript_TransicaoAntesDaCena::
	clearflag FLAG_UNOVA_CASA_JOGADOR_MAE_1
	setflag FLAG_UNOVA_CASA_JOGADOR_MAE_2
	end

@ `MeetMomLeftScript` da fonte: acende o bit de "vim pelo tile da esquerda" e
@ CAI no proximo rotulo, igual a fonte.
Unova_PlayersHouse1F_EventScript_MeetMomLeftScript::
	setflag FLAG_UNOVA_TEMP_ATE_RECARGA_1
	@ cai no proximo

@ `MeetMomRightScript` da fonte.
Unova_PlayersHouse1F_EventScript_MeetMomRightScript::
	lockall
	playbgm MUS_LITTLEROOT, FALSE
	applymovement 1, Common_Movement_ExclamationMark
	waitmovement 0
	turnobject LOCALID_PLAYER, DIR_WEST
	goto_if_set FLAG_UNOVA_TEMP_ATE_RECARGA_1, Unova_PlayersHouse1F_EventScript_MaeSoVira
	applymovement 1, Unova_PlayersHouse1F_Movement_MaeAndaAteOJogador
	waitmovement 0
	goto Unova_PlayersHouse1F_EventScript_MeetMomScript

Unova_PlayersHouse1F_EventScript_MaeSoVira::
	applymovement 1, Unova_PlayersHouse1F_Movement_MaeViraParaOJogador
	waitmovement 0
	@ cai no proximo

@ `MeetMomScript` da fonte, ja sem o trecho de relogio.
Unova_PlayersHouse1F_EventScript_MeetMomScript::
	msgbox Unova_PlayersHouse1F_Text_MarlonLookingForYou, MSGBOX_DEFAULT
	closemessage
	@ `setscene SCENE_FINISHED` da fonte. Vem ANTES do movimento de volta de
	@ proposito: a partir daqui o gatilho de (8,4)/(9,4) esta desarmado.
	setvar VAR_UNOVA_CASA_JOGADOR_1F_CENA, 1
	@ `setevent EVENT_PLAYERS_HOUSE_MOM_1` + `clearevent EVENT_PLAYERS_HOUSE_MOM_2`
	@ da fonte: a troca so aparece na proxima entrada do mapa (o ON_TRANSITION e
	@ quem cria objeto), e como as duas MAEs dividem o tile (7,4) ninguem ve nada.
	setflag FLAG_UNOVA_CASA_JOGADOR_MAE_1
	clearflag FLAG_UNOVA_CASA_JOGADOR_MAE_2
	goto_if_set FLAG_UNOVA_TEMP_ATE_RECARGA_1, Unova_PlayersHouse1F_EventScript_MaeVoltaOlhando
	@ `.FromLeft`/`.Finish` da fonte: RECARGA_2 aceso e o caminho de quem comecou
	@ a cena falando com a MAE (`MomScript`), em que ela nao saiu do lugar.
	goto_if_set FLAG_UNOVA_TEMP_ATE_RECARGA_2, Unova_PlayersHouse1F_EventScript_MeetMomFim
	applymovement 1, Unova_PlayersHouse1F_Movement_MaeVoltaAndando
	waitmovement 0
	goto Unova_PlayersHouse1F_EventScript_MeetMomFim

Unova_PlayersHouse1F_EventScript_MaeVoltaOlhando::
	applymovement 1, Unova_PlayersHouse1F_Movement_MaeVoltaOlhar
	waitmovement 0
	@ cai no proximo

@ `.Finish` da fonte.
Unova_PlayersHouse1F_EventScript_MeetMomFim::
	fadedefaultbgm
	turnobject 1, DIR_WEST
	@ o motor daqui nao zera flag em recarga de mapa; a cena zera as suas
	clearflag FLAG_UNOVA_TEMP_ATE_RECARGA_1
	clearflag FLAG_UNOVA_TEMP_ATE_RECARGA_2
	releaseall
	end

@ `MomTurnsTowardPlayerMovement` da fonte.
Unova_PlayersHouse1F_Movement_MaeViraParaOJogador:
	face_right
	step_end

@ `MomWalksToPlayerMovement` da fonte: (7,4) -> (8,4), ao lado de quem pisou em (9,4).
Unova_PlayersHouse1F_Movement_MaeAndaAteOJogador:
	walk_slow_right
	step_end

@ `MomTurnsBackMovement` da fonte.
Unova_PlayersHouse1F_Movement_MaeVoltaOlhar:
	face_left
	step_end

@ `MomWalksBackMovement` da fonte: (8,4) -> (7,4).
Unova_PlayersHouse1F_Movement_MaeVoltaAndando:
	walk_slow_left
	step_end

@ `MarlonLookingForYouText` da fonte, palavra a palavra (inclusive o
@ "XTRANSCIEVER" trocado que a fonte escreve nesta caixa), so requebrado para a
@ largura da caixa deste motor.
Unova_PlayersHouse1F_Text_MarlonLookingForYou::
	.string "Oh, {PLAYER}! It's about time\n"
	.string "you got up!\p"
	.string "MARLON, the GYM LEADER stopped\n"
	.string "by asking for you.\p"
	.string "Go stop by his house and see\n"
	.string "what he needs.\p"
	.string "Oh! And before you go out, make\n"
	.string "sure you take your XTRANSCIEVER\l"
	.string "with you.$"


Unova_PlayersHouse1F_EventScript_Placa0::
	msgbox Unova_PlayersHouse1F_Text_StoveText, MSGBOX_SIGN
	end

Unova_PlayersHouse1F_EventScript_Placa1::
	msgbox Unova_PlayersHouse1F_Text_SinkText, MSGBOX_SIGN
	end

Unova_PlayersHouse1F_EventScript_Placa2::
	msgbox Unova_PlayersHouse1F_Text_FridgeText, MSGBOX_SIGN
	end

Unova_PlayersHouse1F_EventScript_Placa3::
	msgbox Unova_PlayersHouse1F_Text_TVText, MSGBOX_SIGN
	end

Unova_PlayersHouse1F_EventScript_Npc0::
	msgbox Unova_PlayersHouse1F_Text_MarlonIsWaitingText, MSGBOX_NPC
	end

@ Npc1 e Npc3 sairam junto com as copias de MORN e NITE da MAE (ver o cabecalho):
@ eram o mesmo msgbox de Npc0/Npc2, e sem objeto ficariam orfaos.
Unova_PlayersHouse1F_EventScript_Npc2::
	msgbox Unova_PlayersHouse1F_Text_MarlonIsWaitingText, MSGBOX_NPC
	end

Unova_PlayersHouse1F_EventScript_Npc4::
	msgbox Unova_PlayersHouse1F_Text_NeighborMornIntroText, MSGBOX_NPC
	end


Unova_PlayersHouse1F_Text_StoveText::
	.string "Mom's specialty!"
	.string "\pVOLCANO"
	.string "\nBAKE MEAT!$"

Unova_PlayersHouse1F_Text_SinkText::
	.string "The sink is spot-"
	.string "\nless. Mom likes it"
	.string "\lclean.$"

Unova_PlayersHouse1F_Text_FridgeText::
	.string "Let's see what's"
	.string "\nin the fridge…"
	.string "\pFRESH WATER and"
	.string "\ntasty LEMONADE!$"

Unova_PlayersHouse1F_Text_TVText::
	.string "There's a movie on"
	.string "\nTV: Stars dot the"
	.string "\psky as two boys"
	.string "\nride on a train…"
	.string "\pI'd better get"
	.string "\nrolling too!$"

Unova_PlayersHouse1F_Text_MarlonIsWaitingText::
	.string "MARLON is wait-"
	.string "\ning for you."
	.string "\pYou remember where"
	.string "\nhe lives, right?"
	.string "\pIt's the house"
	.string "\nclosest to shore."
	.string "\pHurry up, baby!$"

Unova_PlayersHouse1F_Text_NeighborMornIntroText::
	.string "Good morning,"
	.string "\n{PLAYER}!"
	.string "\pYour mom and I"
	.string "\nhave a date at"
	.string "\pthe MARINE TUBE"
	.string "\nlater today!$"
