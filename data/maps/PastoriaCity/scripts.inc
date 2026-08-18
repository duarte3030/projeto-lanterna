@ Textos vindos de pret/pokeplatinum (res/text/pastoria_city.json), em ingles.
@ Grunt_M, Rival, Crasher Wake, Croagunk e o Collector/Arrow_Signpost de
@ Route 212 South ficaram de fora: dependem de flag ou de MAP_HEADER
@ condicional, que este agente nao pode inventar.
@ OBJ_EVENT_GFX_PARASOL_LADY e OBJ_EVENT_GFX_BEAUTY nao existem em
@ event_objects.h: trocados por WOMAN_4 e WOMAN_5.

PastoriaCity_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
@ Os 4 gatilhos de Pastoria formam UMA corrente de historia (RivalBattle ->
@ Bomb -> BlockGreatMarsh, nessa ordem, mais o FaceBoard solto).
@
@ QUEM ESCREVE O var=1 QUE DESTRAVA ESTA CENA (medido em 18/08/2026, nao
@ presumido): `grep -rn "VAR_PASTORIA_CITY_STATE" res/field/scripts/` na fonte
@ da UM unico SetVar com valor 1, e ele mora FORA deste mapa:
@ scripts_veilstone_city_galactic_warehouse.s:89, na cena em que o Looker
@ entrega o HM Fly dentro do armazem da Galactica em Veilstone (a mesma que
@ escreve VAR_VEILSTONE_CITY_GALACTIC_WAREHOUSE_STATE, 2). Essa cena inteira
@ continua BLOQUEADA neste porte (o armazem nao tem cena escrita), entao o
@ gatilho de var=1 daqui e hoje inalcancavel no jogo de verdade e so a suite o
@ alcanca, pinando a var. NAO foi inventado escritor nenhum: quando o armazem
@ de Veilstone entrar, o `setvar VAR_SINNOH_PASTORIA_ESTADO, 1` entra junto,
@ naquele arquivo, e esta cena acorda sozinha. Os outros valores da corrente
@ tambem tem dono na fonte: 3 e do ginasio (scripts_pastoria_city_gym.s:66), 4
@ e 5 sao da propria corrente da bomba (linhas 524 e 700) e 6 e de
@ scripts_valor_lakefront.s:364 (S7).
@
@ RivalBattle (var=1): ESCRITA nesta leva (S6, onda 4, 18/08/2026). Os ids
@ TRAINER_SINNOH_RIVAL_PASTORIA_TURTWIG/_CHIMCHAR/_PIPLUP sao os
@ PRE-ATRIBUIDOS pela condutora (2508-2510, PLANO-OBRAS-SINNOH.md); citados
@ pelo nome literal aqui, quem define e o executor de treinadores desta
@ mesma onda. LOCALID_PASTORIA_CITY_RIVAL nasce escondido (setflag em
@ data/scripts/new_game.inc, mesmo molde do Route203_EventScript_CoordEvent_
@ Rival), a cena revela, luta, e esconde de volta no fecho (ganhando ou
@ perdendo): sem a corrente Bomb/BlockGreatMarsh escrita, deixar o objeto
@ visivel prendia ele parado no ponto de batalha para sempre.
@ CONSERTO 18/08/2026 (onda 4). Tres defeitos fechados aqui, todos na causa:
@ (1) `setobjectxy` ANTES do `addobject` era no-op (ScrCmd_setobjectxy chama
@ TryMoveObjectEventToMapCoords, que so mexe em objeto JA no mapa; quem escreve
@ o template e `setobjectxyperm`, SetObjEventTemplateCoords). Sem ele o rival
@ nascia no proprio tile do gatilho, (13,26), que e onde o jogador esta parado,
@ e a coreografia saia ao contrario. Molde da casa com precedente:
@ PalletTown_Frlg/scripts.inc:45 (setobjectxyperm + setobjectmovementtype +
@ addobject + applymovement).
@ (2) texto duplicado: a fonte da UM `Message PastoriaCity_Text_IllTestYou`
@ antes da luta e UM `Message PastoriaCity_Text_YouDidGetTougher` depois
@ (StartTrainerBattle da fonte nao leva texto). O `trainerbattle_single` com
@ intro repetia o primeiro e o `msgbox` do fecho repetia o segundo. Agora e
@ `trainerbattle_no_intro` (sem intro; o lose_text E o pos-vitoria da fonte),
@ exatamente o molde dos irmaos Route203/Route209_Access e do vanilla
@ Route103_EventScript_StartMayBattleTreecko.
@ (3) faltava `setvar VAR_LAST_TALKED`: emboscada por coord_event nao passa por
@ clique em objeto, e `EventScript_DoNoIntroTrainerBattle` (data/scripts/
@ trainer_battle.inc:47) faz `applymovement VAR_LAST_TALKED,
@ Movement_RevealTrainer`. Sem a var a revelacao mira o objeto errado. Mesma
@ razao documentada em Route209_Access/scripts.inc.
@ COORDENADAS: (20,17) e a conversao literal do `SetObjectEventPos
@ LOCALID_RIVAL, 595, 819` da fonte pelo conversor_de_coordenada de
@ dev_scripts/importa_npcs_sinnoh.py (conferido rodando a propria funcao em
@ 18/08/2026: 595,819 -> 20,17, e 589,828 -> 13,26, o tile do gatilho).
@ ROTA DESVIADA PARA A LINHA 27, com prova: a fonte desce 9 e anda 4 a oeste
@ pela MESMA linha do jogador, mas a conversao proporcional do layout deixou
@ (19,26), (16,26), (15,26) e (14,26) com colisao 1 em data/layouts/
@ PastoriaCity/map.bin (medido em 18/08/2026); a linha 27 esta livre de x=12 a
@ x=25. `applymovement` de NPC ignora colisao (precedente CianwoodCity_
@ EventScript_SuicuneTrigger, ja citado em Route203), entao a rota da fonte nao
@ TRAVARIA, mas mostraria o rival atravessando parede. Desce 10 ate (20,27),
@ anda 6 ate (14,27) e fecha 1 ate (13,27), colado no jogador pelo sul. Fica de
@ calibracao para o S8 (andabilidade do tile convertido, item ja previsto no
@ plano).
PastoriaCity_EventScript_CoordEvent_RivalBattle::
	lockall
	clearflag FLAG_SINNOH_ESCONDE_PASTORIA_CITY_RIVAL
	setobjectxyperm LOCALID_PASTORIA_CITY_RIVAL, 20, 17
	setobjectmovementtype LOCALID_PASTORIA_CITY_RIVAL, MOVEMENT_TYPE_FACE_LEFT
	addobject LOCALID_PASTORIA_CITY_RIVAL
	applymovement LOCALID_PASTORIA_CITY_RIVAL, PastoriaCity_Movement_RivalEnterForBattle
	waitmovement 0
	applymovement LOCALID_PASTORIA_CITY_RIVAL, PastoriaCity_Movement_RivalWalkToPlayerForBattle
	applymovement OBJ_EVENT_ID_PLAYER, PastoriaCity_Movement_PlayerFaceRivalForBattle
	waitmovement 0
	msgbox PastoriaCity_Text_IllTestYou, MSGBOX_DEFAULT
	applymovement LOCALID_PASTORIA_CITY_RIVAL, PastoriaCity_Movement_RivalWalkWest
	waitmovement 0
	setvar VAR_LAST_TALKED, LOCALID_PASTORIA_CITY_RIVAL
	switch VAR_STARTER_MON
	case 0, PastoriaCity_EventScript_RivalBattleTurtwig
	case 1, PastoriaCity_EventScript_RivalBattleChimchar
	goto PastoriaCity_EventScript_RivalBattlePiplup
	end

PastoriaCity_EventScript_RivalBattleTurtwig::
	trainerbattle_no_intro TRAINER_SINNOH_RIVAL_PASTORIA_TURTWIG, PastoriaCity_Text_YouDidGetTougher
	goto PastoriaCity_EventScript_RivalBeaten
	end

PastoriaCity_EventScript_RivalBattleChimchar::
	trainerbattle_no_intro TRAINER_SINNOH_RIVAL_PASTORIA_CHIMCHAR, PastoriaCity_Text_YouDidGetTougher
	goto PastoriaCity_EventScript_RivalBeaten
	end

PastoriaCity_EventScript_RivalBattlePiplup::
	trainerbattle_no_intro TRAINER_SINNOH_RIVAL_PASTORIA_PIPLUP, PastoriaCity_Text_YouDidGetTougher
	goto PastoriaCity_EventScript_RivalBeaten
	end

PastoriaCity_EventScript_RivalBeaten::
	applymovement LOCALID_PASTORIA_CITY_RIVAL, PastoriaCity_Movement_RivalLeaveAfterBattle
	waitmovement 0
	setflag FLAG_SINNOH_ESCONDE_PASTORIA_CITY_RIVAL
	removeobject LOCALID_PASTORIA_CITY_RIVAL
	setvar VAR_SINNOH_PASTORIA_ESTADO, 2
	releaseall
	end

@ Fonte: WalkFastSouth 9 + WalkOnSpotFastWest + EmoteExclamationMark. Aqui
@ desce 10 (de (20,17) ate (20,27), a linha andavel; ver cabecalho).
PastoriaCity_Movement_RivalEnterForBattle:
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_in_place_left
	emote_exclamation_mark
	step_end

@ Fonte: WalkFastWest 4 + WalkOnSpotFastWest. Aqui 6, porque a conversao
@ proporcional esticou a distancia de 6 tiles (fonte) para 7 (aqui).
PastoriaCity_Movement_RivalWalkToPlayerForBattle:
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_in_place_left
	step_end

@ Fonte: Delay4 13 + WalkOnSpotNormalEast. O rival chega pelo SUL nesta rota
@ (ver cabecalho), entao o jogador vira para baixo em vez de para a direita.
PastoriaCity_Movement_PlayerFaceRivalForBattle:
	delay_16
	delay_16
	delay_16
	delay_8
	walk_in_place_down
	step_end

PastoriaCity_Movement_RivalWalkWest:
	walk_left
	step_end

@ Fonte: WalkFastEast 5 + WalkFastNorth 9, ou seja a volta exata ao ponto de
@ nascimento. Aqui 7 e 10, pela mesma conta da ida.
PastoriaCity_Movement_RivalLeaveAfterBattle:
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	step_end

@ Texto literal de res/text/pastoria_city.json (BARRY: {STRVAR_1 3,0,0},
@ jogador: {STRVAR_1 3,1,0}), requebrado. A fonte nao da texto de derrota
@ proprio pra esta luta (StartTrainerBattle sem paramtros de mensagem); reusa
@ o mesmo texto do pos-vitoria como lose_text, mesmo molde do Cedric de
@ Canalave (CanalaveCity_EventScript_RivalTurtwig e irmaos).
PastoriaCity_Text_IllTestYou:
	.string "BARRY: Whoops!\p"
	.string "Hehehe! I'm not always going to\n"
	.string "plow into you every time we meet!\p"
	.string "So how's it going, {PLAYER}?\n"
	.string "Buffing up your Pokémon, eh?\p"
	.string "I'll test you and your Pokémon\n"
	.string "out to see how buff and tough\l"
	.string "you are!$"

PastoriaCity_Text_YouDidGetTougher:
	.string "BARRY: Heh, yeah, maybe you did\n"
	.string "get a bit tougher since last time.\p"
	.string "That even shocked me a bit, so\n"
	.string "yeah, I got beat 'cause I was\l"
	.string "careless.\p"
	.string "Oh, yeah, I joined Mr. Wake as\n"
	.string "an apprentice!\p"
	.string "Like, I want my own theme song!$"

@ Bomb (var=4) e BlockGreatMarsh (var=5): BLOQUEADOS. As DUAS flags fora do
@ padrao FLAG_HIDE_* que travavam esta corrente ja tem endereco reservado
@ (decisao da condutora, 18/08/2026; ver include/constants/flags.h, bloco
@ "B6 Sinnoh S6, onda 4"): FLAG_SINNOH_PASTORIA_GRUNT_FUGIU_LESTE (fonte
@ FLAG_PASTORIA_CITY_GRUNT_M_MOVED_EAST) e FLAG_SINNOH_PASTORIA_CROAGUNK_
@ BLOQUEADO (fonte FLAG_BLOCK_PASTORIA_CITY_CROAGUNK_EVENT, usada so no
@ ginasio/FaceBoard/Valor Lakefront, nenhum dos tres neste mapa). Mas a
@ corrente INTEIRA (~15 sub-rotulos na fonte) continua girando em torno do
@ Crasher Wake: ele reage ao Grunt_M fugindo, pergunta "o que voce fez?!",
@ observa e depois entra no Great Marsh atras do grunt (PastoriaCity_
@ GoAfterThatGoon). LOCALID_CRASHER_WAKE nao esta no censo do S1 (FLAG_HIDE_
@ PASTORIA_CITY_CRASHER_WAKE nao e um dos 247 grupos de hidden_flag; `grep`
@ em dev_scripts/fila_b6.json confirma zero ocorrencias) e ele ja existe
@ dentro do ginasio (PastoriaCity_Gym, treinador de verdade, fora do meu
@ escopo). Trazer ele pra este mapa sem flag autorizada plantava bloqueio
@ permanente OU forcava reescrever a cena cortando o personagem que ela
@ inteira gira em torno dele; nenhuma das duas e "nao inventar". Volta ao
@ plano para autorizar o objeto/flag do Crasher Wake em PastoriaCity antes
@ de escrever a corrente. Termina tambem com SetFlag FLAG_HIDE_VEILSTONE_
@ CITY_GALACTIC_WAREHOUSE_LOOKER, flag de OUTRO mapa (VeilstoneCity, fora do
@ meu escopo nesta leva).
PastoriaCity_EventScript_CoordEvent_Bomb::
	end

PastoriaCity_EventScript_CoordEvent_BlockGreatMarsh::
	end

@ FaceBoard, Croagunk (var=0): BLOQUEADO. Precisa de FLAG_BLOCK_PASTORIA_
@ CITY_CROAGUNK_EVENT, tambem fora da tabela do plano (nao e FLAG_HIDE_*):
@ acende em scripts_pastoria_city_gym.s (ginasio, ainda que nao seja
@ batalha do lider) e apaga em scripts_valor_lakefront.s (S7). Volta ao
@ plano.
PastoriaCity_EventScript_CoordEvent_FaceBoard::
	end

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

PastoriaCity_EventScript_ParasolLady::
	msgbox PastoriaCity_Text_ParasolLady, MSGBOX_NPC
	end

PastoriaCity_EventScript_AceTrainer1::
	msgbox PastoriaCity_Text_AceTrainer1, MSGBOX_NPC
	end

PastoriaCity_EventScript_AceTrainer2::
	msgbox PastoriaCity_Text_AceTrainer2, MSGBOX_NPC
	end

PastoriaCity_EventScript_GreatMarshSign::
	msgbox PastoriaCity_Text_GreatMarshSign, MSGBOX_SIGN
	end

PastoriaCity_EventScript_GymSign::
	msgbox PastoriaCity_Text_GymSign, MSGBOX_SIGN
	end

PastoriaCity_Text_ParasolLady:
	.string "Someone gave me a Berry, so I\n"
	.string "planted it and grew some more.\p"
	.string "Then I took the Berries and cooked\n"
	.string "them into Poffins. All the work\l"
	.string "is worth it when I see how happy\l"
	.string "they make my POKéMON!$"

PastoriaCity_Text_AceTrainer1:
	.string "PASTORIA POKéMON are tough. The\n"
	.string "marsh air toughens them right up.$"

PastoriaCity_Text_AceTrainer2:
	.string "I've battled all over PASTORIA.\n"
	.string "Care to test your skills with me?$"

PastoriaCity_Text_GreatMarshSign:
	.string "GREAT MARSH$"

PastoriaCity_Text_GymSign:
	.string "PASTORIA CITY POKéMON GYM\p"
	.string "The Water-Type Technique Style!$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

PastoriaCity_EventScript_Placa2::
	msgbox PastoriaCity_Text_Placa2, MSGBOX_SIGN
	end

PastoriaCity_Text_Placa2:
	.string "Pastoria City Pokémon Gym\nLeader: Crasher Wake\pThe Torrential Masked Master!$"

PastoriaCity_EventScript_Placa3::
	msgbox PastoriaCity_Text_Placa3, MSGBOX_SIGN
	end

PastoriaCity_Text_Placa3:
	.string "Pastoria Great Marsh\nObservatory Gate$"

PastoriaCity_EventScript_Placa4::
	msgbox PastoriaCity_Text_Placa4, MSGBOX_SIGN
	end

PastoriaCity_Text_Placa4:
	.string "Try the Safari Game in\nPastoria's Great Marsh!$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

PastoriaCity_EventScript_Npc1::
	msgbox PastoriaCity_Text_Npc1, MSGBOX_NPC
	end

PastoriaCity_Text_Npc1:
	.string "Some Trainers deliberately prevent\ntheir Pokémon from evolving.\pThey wait until the Pokémon levels up\nand learns certain moves.$"

PastoriaCity_EventScript_Npc2::
	msgbox PastoriaCity_Text_Npc2, MSGBOX_NPC
	end

PastoriaCity_Text_Npc2:
	.string "Pastoria's Gym Leader is awesome with\nhis water attacks.\pYou'll know what I mean when you\nchallenge him.$"

PastoriaCity_EventScript_Npc3::
	msgbox PastoriaCity_Text_Npc3, MSGBOX_NPC
	end

PastoriaCity_Text_Npc3:
	.string "CLEFAIRY: Fiiih?!$"

PastoriaCity_EventScript_Npc4::
	msgbox PastoriaCity_Text_Npc4, MSGBOX_NPC
	end

PastoriaCity_Text_Npc4:
	.string "The Great Marsh keeps the weather\ncool in the summertime.\pThis is a good town for Water-type\nPokémon.$"

PastoriaCity_EventScript_Npc5::
	msgbox PastoriaCity_Text_Npc5, MSGBOX_NPC
	end

PastoriaCity_Text_Npc5:
	.string "Here where I am standing, I'm\nsmack-dab in the middle of town.$"

PastoriaCity_EventScript_Npc6::
	msgbox PastoriaCity_Text_Npc6, MSGBOX_NPC
	end

PastoriaCity_Text_Npc6:
	.string "I study rare Pokémon that appear\nonly in the Great Marsh.$"

PastoriaCity_EventScript_Npc7::
	msgbox PastoriaCity_Text_Npc7, MSGBOX_NPC
	end

PastoriaCity_Text_Npc7:
	.string "I'm visiting here to see the Great\nMarsh.\pI'm staying at the lakeside hotel.$"

PastoriaCity_EventScript_Npc8::
	msgbox PastoriaCity_Text_Npc8, MSGBOX_NPC
	end

PastoriaCity_Text_Npc8:
	.string "I can't use the hidden move Surf until\nI beat the local Gym Leader.$"

PastoriaCity_EventScript_Npc9::
	msgbox PastoriaCity_Text_Npc9, MSGBOX_NPC
	end

PastoriaCity_Text_Npc9:
	.string "Have you been to the Pokémon Mansion?\nIt's on Route 212.\pThe owner, Mr. Backlot, likes to brag\nabout his herd of rare Pokémon.$"

PastoriaCity_EventScript_Placa10::
	msgbox PastoriaCity_Text_Placa10, MSGBOX_SIGN
	end

PastoriaCity_Text_Placa10:
	.string "Pastoria City\nThe Marsh City$"
