@ Textos vindos de pret/pokeplatinum (res/text/pastoria_city.json), em ingles.
@ O Collector/Arrow_Signpost de Route 212 South ficou de fora: depende de
@ MAP_HEADER condicional, que este agente nao pode inventar. Rival, Grunt_M,
@ Crasher Wake e Croagunk (NPC de cena da corrente da bomba/Croagunk) ja
@ entraram, onda 4 e leva final; ver os comentarios de cada bloco abaixo.
@ OBJ_EVENT_GFX_PARASOL_LADY e OBJ_EVENT_GFX_BEAUTY nao existem em
@ event_objects.h: trocados por WOMAN_4 e WOMAN_5. OBJ_EVENT_GFX_CRASHER_WAKE,
@ _GRUNT_M e _CROAGUNK tambem nao existem: trocados por MAN_4, MAGMA_MEMBER_M
@ e POLIWRATH (ver comentario detalhado antes de CoordEvent_Bomb).

PastoriaCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, PastoriaCity_OnTransition
	.byte 0

@ Leva final (18/08/2026). Porte do `PastoriaCity_OnTransition` da fonte
@ (scripts_pastoria_city.s:31-37), com o que existe neste porte:
@ - `SetVar VAR_PASTORIA_CITY_CROAGUNK_SCENE_STATE, 0` entra literal. Sem ele
@   o gatilho da placa (var_value 0) dispara UMA vez na vida do save e nunca
@   mais, porque a propria cena escreve 1; com ele, o sorteio de 10% volta a
@   valer a cada entrada no mapa, que e o desenho da fonte.
@ - a reposicao do rival depois da explosao entra: a fonte usa
@   `CallIfEq VAR_PASTORIA_CITY_STATE, 5`, aqui e `call_if_ge ... 5` porque o
@   valor 6 (scripts_valor_lakefront.s:364) tambem deixa o rival no mapa e a
@   fonte nao o reposiciona nesse estado. Sem isto o rival volta ao tile que
@   `PastoriaCity_EventScript_CoordEvent_RivalBattle` gravou no template
@   (`setobjectxyperm` escreve o SAVE, nao so a cena) e o gatilho
@   BlockGreatMarsh acha o rival do outro lado da cidade.
@ - `SetVar` de estado 4 e a dupla SetRivalPositionAfterGym/
@   SetCrasherWakePositionAfterGym da fonte NAO entram: a cutscene de saida do
@   ginasio nao foi portada, entao quem revela e posiciona os dois e a propria
@   cena da bomba (ver comentario dela). Registrado, nao esquecido.
@ - `SetFlag FLAG_HIDE_ROUTE_212_BLOCKADE` nao entra: o bloqueio da Route 212
@   nao existe neste porte (sem alias, sem objeto).
PastoriaCity_OnTransition::
	setvar VAR_SINNOH_PASTORIA_CROAGUNK_CENA, 0
	call_if_ge VAR_SINNOH_PASTORIA_ESTADO, 5, PastoriaCity_EventScript_PosicaoRivalPosExplosao
	goto_if_set FLAG_SINNOH_PASTORIA_GRUNT_FUGIU_LESTE, PastoriaCity_EventScript_PosicaoGruntLeste
	end

@ Fonte PastoriaCity_SetRivalPositionAfterExplosion (linha 540): 611,810, que
@ o conversor_de_coordenada de dev_scripts/importa_npcs_sinnoh.py leva a
@ (37,9), tile andavel medido em data/layouts/PastoriaCity/map.bin.
PastoriaCity_EventScript_PosicaoRivalPosExplosao::
	setobjectxyperm LOCALID_PASTORIA_CITY_RIVAL, 37, 9
	setobjectmovementtype LOCALID_PASTORIA_CITY_RIVAL, MOVEMENT_TYPE_FACE_UP
	return

@ Fonte PastoriaCity_SetGruntMEastPosition (linha 39): 637,812, que converte
@ para (64,11), fora da area andavel. Mesmo desvio ja usado dentro da cena da
@ bomba: (63,11), ultimo tile andavel da mesma linha.
PastoriaCity_EventScript_PosicaoGruntLeste::
	setobjectxyperm LOCALID_PASTORIA_CITY_GRUNT_M, 63, 11
	setobjectmovementtype LOCALID_PASTORIA_CITY_GRUNT_M, MOVEMENT_TYPE_FACE_RIGHT
	end

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

@ Bomb (var=4) e BlockGreatMarsh (var=5): ESCRITAS nesta leva (leva final,
@ 18/08/2026). As duas flags que faltavam (visibilidade do Crasher Wake e do
@ Croagunk, autorizadas pela condutora, ver include/constants/flags.h bloco
@ "B6 Sinnoh, leva final") destravaram a corrente inteira.
@
@ ALCANCE EM JOGO, medido: a corrente Bomb/BlockGreatMarsh so dispara com
@ VAR_SINNOH_PASTORIA_ESTADO em 4/5. O UNICO SetVar=1 da fonte inteira mora
@ em scripts_veilstone_city_galactic_warehouse.s:89 (cena do Looker/HM Fly),
@ que este porte NAO tem (o Warehouse foi redesenhado sem ela, comentario no
@ topo daquele arquivo). E os valores 2 (vitoria do rival, ESCRITO nesta
@ mesma leva mais acima), 3 (vitoria do ginasio) e 4 (Crasher Wake sai do
@ ginasio, `PastoriaCity_OnFrame_ExitGym` da fonte) moram em
@ PastoriaCity_Gym/scripts.inc, fora do meu escopo de arquivo nesta leva (o
@ outro executor da onda nao cobriu essa fiacao; fica pendencia registrada
@ no relatorio). Ou seja: a corrente que este bloco escreve fica correta e
@ chamavel, mas so alcancavel de verdade quando (a) o armazem de Veilstone
@ escrever o SetVar=1 e (b) PastoriaCity_Gym escrever o fecho pos-vitoria
@ que avanca 2->3->4. Ate la, so a suite pinando a var chega aqui. Mesma
@ categoria de pendencia ja documentada para VAR_SINNOH_PASTORIA_ESTADO=1
@ logo acima; nao e bug desta leva, e continuacao fora do escopo.
@
@ DESVIOS DE COORDENADA, medidos contra data/layouts/PastoriaCity/map.bin
@ (18/08/2026, mesmo conversor_de_coordenada de dev_scripts/
@ importa_npcs_sinnoh.py que ja validou 595,819->20,17 e 589,828->13,26):
@ - Grunt_M "acabei de apertar o botao" (fonte SetObjectEventPos 610,808):
@   converte para (36,7), que cai dentro do predio/muro do portao do Great
@   Marsh (linhas y=4 a y=8 inteiras bloqueadas nessa faixa de x). Nao existe
@   corredor andavel entre a fonte e a linha do gatilho (y=9) nesta versao
@   proporcional do mapa. Desviado para (37,9): mesma linha andavel do
@   gatilho, vizinho dele, ainda visualmente "saindo logo dali". `applymovement`
@   ignora colisao (o mesmo precedente de CianwoodCity_EventScript_
@   SuicuneTrigger ja citado no RivalBattle acima), entao o (36,7) da fonte
@   NAO travaria, so mostraria o Grunt em cima de parede; o desvio e so
@   estetico, registrado aqui para o S8 nao redescobrir.
@ - Grunt_M "fugiu pro leste" (fonte SetObjectEventPos 637,812, o mesmo valor
@   que soma a FLAG_SINNOH_PASTORIA_GRUNT_FUGIU_LESTE): converte para (64,11),
@   fora da area andavel (bloqueado a partir de x=64 nessa linha). Desviado
@   para (63,11), ultimo tile andavel da mesma linha, mesma logica acima.
@ - Croagunk "foge" (fonte WalkNormalNorth 5 a partir da entrada em (37,19)):
@   a caminhada de 7 tiles ao entrar cabe inteira andavel ((37,12) a (37,19)),
@   mas o passo de saida de 5 tiles a mais termina em (37,7), dentro do
@   mesmo muro do portao do Great Marsh. Mesmo raciocinio: visual (ele
@   "some" perto da parede), nao travamento; NAO redirecionado porque e a
@   ultima acao antes do RemoveObject (ninguem ve o destino exato).
@ Nenhum destes e coord_event (nao afetam andabilidade do jogador, so a
@ posicao final de NPC de cena); o item ja previsto no plano para o S8 medir
@ `coord_event` contra o tile ainda cobre so gatilho do JOGADOR, este bloco
@ de comentario e o registro equivalente para posicao de NPC.
@
@ GetPlayerMapPos (fonte, 3 ramos por x=609/611/612): a fonte usa isso para
@ escolher entre duas variacoes de passo do rival ao entrar no Great Marsh,
@ dependendo de por qual das 3 colunas o jogador se aproximou. O nosso
@ gatilho unico (36,9) so produz UMA posicao; os 3 ramos da fonte colapsam
@ em um so. Escolhido `PastoriaCity_Movement_RivalWalkToGreatMarsh` (o ramo
@ que cobre 2 dos 3 x da fonte, 609 e 612), com o mesmo raciocinio ja usado
@ para "linha 27" no RivalBattle: nao inventar geografia nova, so escolher o
@ ramo majoritario da fonte.
@
@ SetFlag FLAG_HIDE_VEILSTONE_CITY_GALACTIC_WAREHOUSE_LOOKER (fonte, fecho de
@ PastoriaCity_GoAfterThatGoon): DESCARTADO. O Looker do armazem de Veilstone
@ nao existe neste porte (o Warehouse foi redesenhado sem essa cena, ver nota
@ acima); a flag nao tem alias e nao esta no escopo de arquivo desta leva
@ (VeilstoneCity_GalacticWarehouse fora daqui). Nao e falta de portar por
@ preguica: e conteudo que nosso Warehouse redesenhado nao tem para
@ esconder.
@
@ LockObject (fonte, em cada NPC revelado no meio da cena): DESCARTADO sem
@ substituto. `lockall` no topo de cada cena ja congela todos os objetos do
@ mapa, inclusive os recem-adicionados; nao existe scrcmd equivalente por
@ objeto neste motor e nao faz falta.
@
@ ScrCmd_29F 1 (fonte, logo apos a mensagem da explosao) e a marcacao
@ `{SIZE 200}...{SIZE 100}` dentro do proprio texto de PastoriaCity_Text_
@ BigExplosion (escala de fonte pra dar enfase ao "DDDOOOMMM!!"): nenhum dos
@ dois tem equivalente neste motor (grep em asm/macros/event.inc e em todo
@ .string do repositorio, 18/08/2026); descartados, texto plano.
@
@ PlaySE SEQ_SE_DP_FW291 (explosao) -> SE_M_EXPLOSION, mesmo som ja usado
@ pela autodestruicao do Trick Master em Route110_TrickHouseEnd/scripts.inc
@ (unico precedente de "explosao" no repositorio). PlaySE SEQ_SE_DP_KAIDAN2
@ (Croagunk sumindo) -> SE_EXIT: e o UNICO som deste motor com o comentario
@ `// SE_KAIDAN` ao lado (include/constants/songs.h:17), a mesma familia de
@ efeito da fonte (kaidan = historia de fantasma), so variante numerada
@ diferente.
@
@ OBJ_EVENT_GFX_CRASHER_WAKE, _GRUNT_M e _CROAGUNK nao existem em
@ event_objects.h (mesmo buraco ja documentado no topo do arquivo pra
@ Parasol Lady/Beauty). Trocados: Grunt_M -> OBJ_EVENT_GFX_MAGMA_MEMBER_M
@ (TROCA_SPRITE de dev_scripts/valida_mapas_sinnoh.py, mesmo grunt usado em
@ toda a Equipe Galactica desta obra, ex. ValorLakefront/map.json). Crasher
@ Wake -> OBJ_EVENT_GFX_MAN_4, o MESMO sprite ja usado pro Wake líder de
@ ginasio em PastoriaCity_Gym/map.json (LOCALID_WAKE_GYM_LEADER): mantem o
@ personagem visualmente igual nos dois mapas. Croagunk (Pokemon, nao gente;
@ esta em NOMES_PROPRIOS de dev_scripts/importa_npcs_sinnoh.py junto com o
@ proprio Crasher Wake, confirmado sem sprite) -> OBJ_EVENT_GFX_POLIWRATH,
@ escolha documentada (anfibio humanoide, o mais proximo de um sapo/rã
@ disponivel na lista de sprites deste motor); nenhum precedente de Pokemon
@ como NPC generico existia nesta obra para reaproveitar.
PastoriaCity_EventScript_CoordEvent_Bomb::
	lockall
	goto PastoriaCity_EventScript_BombScene

@ Segunda porta de entrada pra MESMA cena: clicar o Crasher Wake antes de
@ pisar exatamente no tile do gatilho acima. Fiel a fonte (PastoriaCity_
@ CrasherWake, scripts_pastoria_city.s:725), que tambem cai no mesmo Explosion/
@ GruntMPushedTheButton/MoveGruntMEast/GoAfterThatGoon; so a INTRODUCAO
@ muda (playse+faceplayer aqui, nada la). So alcancavel quando quem escrever
@ o fecho pos-ginasio revelar o objeto (ver comentario grande acima).
PastoriaCity_EventScript_CrasherWake::
	playse SE_SELECT
	lockall
	faceplayer
	goto PastoriaCity_EventScript_BombScene

@ FIACAO DA LEVA FINAL (18/08/2026, S8). O S7 escreveu a coreografia inteira
@ supondo que o "fecho pos-ginasio" revelaria Crasher Wake e Rival; esse fecho
@ nao existia, e sem ele os `applymovement` desta cena mirariam objetos que
@ nao estao no mapa (os dois nascem escondidos por flag em
@ data/scripts/new_game.inc, e o Rival ainda leva `setflag`+`removeobject` no
@ fecho da propria batalha dele, mais acima).
@
@ A fonte revela os dois na cutscene `PastoriaCity_OnFrame_ExitGym`
@ (scripts_pastoria_city.s:477-524), que este porte nao tem. Em vez de portar
@ uma cutscene inteira fora do censo, a cena que PRECISA deles revela os dois
@ ela mesma, no molde que este proprio arquivo ja usa em
@ `PastoriaCity_EventScript_CoordEvent_RivalBattle` (clearflag +
@ setobjectxyperm + setobjectmovementtype + addobject; `setobjectxy` sozinho
@ e no-op, licao ja registrada la). O ginasio so escreve a var e as duas flags
@ da fonte (PastoriaCity_Gym/scripts.inc).
@
@ POSICOES, todas pelo conversor_de_coordenada de dev_scripts/
@ importa_npcs_sinnoh.py e conferidas em data/layouts/PastoriaCity/map.bin:
@ - Crasher Wake: fonte 611,810 (PastoriaCity_SetCrasherWakePositionAfterGym)
@   -> (37,9), andavel, vizinho leste do tile do gatilho (36,9);
@ - Rival: fonte 608,814 (PastoriaCity_SetRivalPositionAfterGym) -> (34,13),
@   andavel, de onde a rota da fonte (3 passos ao norte + 1 a leste) chega
@   colado no jogador.
@ Cosmetico conhecido: o Grunt_M entra em (37,9), o mesmo tile do Wake (o S7
@ desviou o (36,7) da fonte para ali sem saber onde o Wake ficaria). Os dois
@ sprites ficam empilhados pelo instante entre o `addobject` do Grunt e o
@ primeiro passo dele para o sul, e nada trava (`applymovement` de NPC nao le
@ colisao nem ocupacao). Nao foi mexido para nao inventar um terceiro tile.
PastoriaCity_EventScript_BombScene::
	clearflag FLAG_SINNOH_ESCONDE_PASTORIA_WAKE
	setobjectxyperm LOCALID_PASTORIA_CITY_CRASHER_WAKE, 37, 9
	setobjectmovementtype LOCALID_PASTORIA_CITY_CRASHER_WAKE, MOVEMENT_TYPE_FACE_DOWN
	addobject LOCALID_PASTORIA_CITY_CRASHER_WAKE
	clearflag FLAG_SINNOH_ESCONDE_PASTORIA_CITY_RIVAL
	setobjectxyperm LOCALID_PASTORIA_CITY_RIVAL, 34, 13
	setobjectmovementtype LOCALID_PASTORIA_CITY_RIVAL, MOVEMENT_TYPE_FACE_UP
	addobject LOCALID_PASTORIA_CITY_RIVAL
	call PastoriaCity_EventScript_Explosion
	applymovement LOCALID_PASTORIA_CITY_CRASHER_WAKE, PastoriaCity_Movement_CrasherWakeWatchGruntMExitGreatMarsh
	applymovement LOCALID_PASTORIA_CITY_RIVAL, PastoriaCity_Movement_RivalWatchGruntMExitGreatMarsh
	applymovement OBJ_EVENT_ID_PLAYER, PastoriaCity_Movement_PlayerWatchGruntMExitGreatMarsh
	applymovement LOCALID_PASTORIA_CITY_GRUNT_M, PastoriaCity_Movement_GruntMExitGreatMarsh
	waitmovement 0
	call PastoriaCity_EventScript_GruntMPushedTheButton
	applymovement LOCALID_PASTORIA_CITY_CRASHER_WAKE, PastoriaCity_Movement_CrasherWakeWatchGruntMLeave
	applymovement LOCALID_PASTORIA_CITY_RIVAL, PastoriaCity_Movement_RivalWatchGruntMLeave
	applymovement OBJ_EVENT_ID_PLAYER, PastoriaCity_Movement_PlayerWatchGruntMLeave
	applymovement LOCALID_PASTORIA_CITY_GRUNT_M, PastoriaCity_Movement_GruntMLeave
	waitmovement 0
	call PastoriaCity_EventScript_MoveGruntMEast
	msgbox PastoriaCity_Text_GreatMarshIsInvaluable, MSGBOX_DEFAULT
	applymovement LOCALID_PASTORIA_CITY_CRASHER_WAKE, PastoriaCity_Movement_CrasherWakeWalkOnSpotSouthAfterExplosion
	applymovement OBJ_EVENT_ID_PLAYER, PastoriaCity_Movement_PlayerWalkOnSpotNorth
	waitmovement 0
	call PastoriaCity_EventScript_GoAfterThatGoon
	releaseall
	end

PastoriaCity_EventScript_Explosion::
	applymovement LOCALID_PASTORIA_CITY_RIVAL, PastoriaCity_Movement_RivalWalkToPlayerForExplosion
	waitmovement 0
	msgbox PastoriaCity_Text_DontForgetImHere, MSGBOX_DEFAULT
	applymovement OBJ_EVENT_ID_PLAYER, PastoriaCity_Movement_PlayerFaceNorth
	applymovement LOCALID_PASTORIA_CITY_CRASHER_WAKE, PastoriaCity_Movement_CrasherWakeWalkOnSpotNorth
	waitmovement 0
	msgbox PastoriaCity_Text_WheresThisGalac, MSGBOX_DEFAULT
	applymovement LOCALID_PASTORIA_CITY_RIVAL, PastoriaCity_Movement_RivalWalkOnSpotNorth
	waitmovement 0
	playse SE_M_EXPLOSION
	delay 4
	msgbox PastoriaCity_Text_BigExplosion, MSGBOX_DEFAULT
	clearflag FLAG_SINNOH_ESCONDE_PASTORIA_CITY_GRUNT_M
	setobjectxyperm LOCALID_PASTORIA_CITY_GRUNT_M, 37, 9
	setobjectmovementtype LOCALID_PASTORIA_CITY_GRUNT_M, MOVEMENT_TYPE_FACE_RIGHT
	addobject LOCALID_PASTORIA_CITY_GRUNT_M
	return

PastoriaCity_EventScript_GruntMPushedTheButton::
	msgbox PastoriaCity_Text_ThatWasRough, MSGBOX_DEFAULT
	applymovement LOCALID_PASTORIA_CITY_CRASHER_WAKE, PastoriaCity_Movement_CrasherWakeWatchGruntMExitGreatMarsh
	waitmovement 0
	msgbox PastoriaCity_Text_WhatveYouDone, MSGBOX_DEFAULT
	applymovement LOCALID_PASTORIA_CITY_GRUNT_M, PastoriaCity_Movement_GruntMWalkOnSpotNorth
	waitmovement 0
	msgbox PastoriaCity_Text_IPushedTheButton, MSGBOX_DEFAULT
	return

PastoriaCity_EventScript_MoveGruntMEast::
	removeobject LOCALID_PASTORIA_CITY_GRUNT_M
	clearflag FLAG_SINNOH_ESCONDE_PASTORIA_CITY_GRUNT_M
	setobjectxyperm LOCALID_PASTORIA_CITY_GRUNT_M, 63, 11
	setobjectmovementtype LOCALID_PASTORIA_CITY_GRUNT_M, MOVEMENT_TYPE_FACE_RIGHT
	addobject LOCALID_PASTORIA_CITY_GRUNT_M
	return

PastoriaCity_EventScript_GoAfterThatGoon::
	msgbox PastoriaCity_Text_DoNotFollowMe, MSGBOX_DEFAULT
	applymovement LOCALID_PASTORIA_CITY_CRASHER_WAKE, PastoriaCity_Movement_CrasherWakeEnterGreatMarsh
	applymovement OBJ_EVENT_ID_PLAYER, PastoriaCity_Movement_PlayerWatchCrasherWakeEnterGreatMarsh
	waitmovement 0
	@ Leva final: a fonte so faz `RemoveObject` aqui, e o Wake dela volta a
	@ nascer na entrada seguinte do mapa (a flag continua apagada). Aqui isso
	@ nao pode ficar assim: o objeto do Wake carrega
	@ `PastoriaCity_EventScript_CrasherWake` como script de clique, que e a
	@ SEGUNDA porta desta mesma cena, e um Wake de pe depois da explosao
	@ deixaria a cutscene inteira replayavel. `setflag` antes do `removeobject`,
	@ mesmo molde do fecho de PastoriaCity_EventScript_RivalBeaten.
	setflag FLAG_SINNOH_ESCONDE_PASTORIA_WAKE
	removeobject LOCALID_PASTORIA_CITY_CRASHER_WAKE
	applymovement LOCALID_PASTORIA_CITY_RIVAL, PastoriaCity_Movement_RivalWalkToGreatMarsh
	waitmovement 0
	setvar VAR_SINNOH_PASTORIA_ESTADO, 5
	setflag FLAG_SINNOH_PASTORIA_GRUNT_FUGIU_LESTE
	msgbox PastoriaCity_Text_GoAfterThatGoon, MSGBOX_DEFAULT
	return

	.balign 4, 0
PastoriaCity_Movement_RivalWalkToPlayerForExplosion:
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_right
	step_end

	.balign 4, 0
PastoriaCity_Movement_PlayerFaceNorth:
	face_up
	step_end

	.balign 4, 0
PastoriaCity_Movement_CrasherWakeWalkOnSpotNorth:
	walk_in_place_up
	step_end

	.balign 4, 0
PastoriaCity_Movement_RivalWalkOnSpotNorth:
	walk_in_place_up
	step_end

	.balign 4, 0
PastoriaCity_Movement_GruntMExitGreatMarsh:
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	step_end

	.balign 4, 0
PastoriaCity_Movement_PlayerWatchGruntMExitGreatMarsh:
	walk_fast_down
	walk_fast_right
	walk_in_place_down
	step_end

	.balign 4, 0
PastoriaCity_Movement_RivalWatchGruntMExitGreatMarsh:
	walk_in_place_down
	step_end

	.balign 4, 0
PastoriaCity_Movement_CrasherWakeWatchGruntMExitGreatMarsh:
	walk_in_place_down
	step_end

	.balign 4, 0
PastoriaCity_Movement_GruntMWalkOnSpotNorth:
	walk_in_place_up
	step_end

	.balign 4, 0
PastoriaCity_Movement_GruntMLeave:
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	step_end

	.balign 4, 0
PastoriaCity_Movement_CrasherWakeWatchGruntMLeave:
	delay_8
	walk_in_place_right
	step_end

	.balign 4, 0
PastoriaCity_Movement_RivalWatchGruntMLeave:
	walk_in_place_right
	step_end

	.balign 4, 0
PastoriaCity_Movement_PlayerWatchGruntMLeave:
	delay_8
	walk_in_place_right
	step_end

	.balign 4, 0
PastoriaCity_Movement_CrasherWakeWalkOnSpotSouthAfterExplosion:
	walk_in_place_down
	step_end

	.balign 4, 0
PastoriaCity_Movement_PlayerWalkOnSpotNorth:
	walk_in_place_up
	step_end

	.balign 4, 0
PastoriaCity_Movement_CrasherWakeEnterGreatMarsh:
	walk_up
	walk_up
	step_end

	.balign 4, 0
PastoriaCity_Movement_PlayerWatchCrasherWakeEnterGreatMarsh:
	delay_8
	face_up
	step_end

	.balign 4, 0
PastoriaCity_Movement_RivalWalkToGreatMarsh:
	walk_fast_right
	walk_fast_right
	walk_fast_up
	step_end

PastoriaCity_Text_DontForgetImHere:
	.string "BARRY: Hey!\p"
	.string "What am I, chopped liver?\n"
	.string "Don't forget I'm here, too!$"

PastoriaCity_Text_WheresThisGalac:
	.string "Wake: So, where's this Galac...$"

PastoriaCity_Text_BigExplosion:
	.string "DDDOOOMMM!!$"

PastoriaCity_Text_ThatWasRough:
	.string "Grunt: Fweh! That was rough.$"

PastoriaCity_Text_WhatveYouDone:
	.string "Wake: YOU!\n"
	.string "What've you done?!$"

PastoriaCity_Text_IPushedTheButton:
	.string "Grunt: What've I done, you're asking?\n"
	.string "Well, technically speaking, it wasn't me.\p"
	.string "The package that arrived, see, that\n"
	.string "was a bomb, named the Galactic Bomb.\p"
	.string "Me, I was told to push the button.\n"
	.string "So I did. Like, “Poink!”\p"
	.string "Oh, that's right! Mustn't forget!\n"
	.string "The test results need reporting!\p"
	.string "Cheerio, then!\n"
	.string "You daft codger, your mask's absurd!$"

PastoriaCity_Text_GreatMarshIsInvaluable:
	.string "Wake: The Great Marsh is invaluable...$"

PastoriaCity_Text_DoNotFollowMe:
	.string "You two! Do NOT follow me!\n"
	.string "Don't let anyone else in, either!\p"
	.string "There'd be big trouble if there's any\n"
	.string "of that bomb left!$"

PastoriaCity_Text_GoAfterThatGoon:
	.string "BARRY: Hey! {PLAYER}!\n"
	.string "You go after that Galactic goon!\p"
	.string "I'm staying here like Master said!\n"
	.string "Gotta keep others from going in!\p"
	.string "Don't let that Galactic guy get away!$"

@ BlockGreatMarsh (var=5): ESCRITA nesta leva. Rival barra a entrada do Great
@ Marsh ate a corrente avancar (nada alem da S7 escreve o proximo valor, 6,
@ de scripts_valor_lakefront.s:364, fora do meu escopo). Sem movimento de
@ NPC novo, so o proprio Rival ja presente no mapa; nenhuma coordenada nova.
PastoriaCity_EventScript_CoordEvent_BlockGreatMarsh::
	lockall
	applymovement OBJ_EVENT_ID_PLAYER, PastoriaCity_Movement_PlayerWalkOnSpotEast
	applymovement LOCALID_PASTORIA_CITY_RIVAL, PastoriaCity_Movement_RivalWalkOnSpotWest
	waitmovement 0
	msgbox PastoriaCity_Text_WhyArentYouGone, MSGBOX_DEFAULT
	applymovement OBJ_EVENT_ID_PLAYER, PastoriaCity_Movement_PlayerGetPushedSouth
	applymovement LOCALID_PASTORIA_CITY_RIVAL, PastoriaCity_Movement_RivalPushBackPlayer
	waitmovement 0
	releaseall
	end

	.balign 4, 0
PastoriaCity_Movement_PlayerWalkOnSpotEast:
	walk_in_place_right
	step_end

	.balign 4, 0
PastoriaCity_Movement_RivalWalkOnSpotWest:
	walk_in_place_left
	step_end

	.balign 4, 0
PastoriaCity_Movement_PlayerGetPushedSouth:
	walk_down
	step_end

	.balign 4, 0
PastoriaCity_Movement_RivalPushBackPlayer:
	walk_left
	walk_right
	walk_in_place_up
	step_end

PastoriaCity_Text_WhyArentYouGone:
	.string "BARRY: What's the matter?!\n"
	.string "Why aren't you gone already?!\p"
	.string "Go after that Galactic goon!$"

@ FaceBoard, Croagunk (var=0): ESCRITA nesta leva. 10% de chance de o
@ Croagunk pular na frente do jogador ao passar pela placa (GetRandom/
@ GoToIfGe 90 da fonte == randompercentage 10 aqui, mesma probabilidade).
@ FLAG_SINNOH_PASTORIA_CROAGUNK_BLOQUEADO (fonte FLAG_BLOCK_PASTORIA_CITY_
@ CROAGUNK_EVENT) so acende no ginasio e so apaga em Valor Lakefront, nenhum
@ dos dois neste escopo; fica sempre limpa aqui, entao a cena nunca fica
@ bloqueada nesta leva (comportamento correto: a fonte tambem comeca limpa).
PastoriaCity_EventScript_CoordEvent_FaceBoard::
	lockall
	goto_if_set FLAG_SINNOH_PASTORIA_CROAGUNK_BLOQUEADO, PastoriaCity_EventScript_FaceBoardEnd
	setvar VAR_SINNOH_PASTORIA_CROAGUNK_CENA, 1
	randompercentage 10
	goto_if_eq VAR_RESULT, TRUE, PastoriaCity_EventScript_CroagunkScene
	goto PastoriaCity_EventScript_FaceBoardEnd

PastoriaCity_EventScript_FaceBoardEnd::
	releaseall
	end

PastoriaCity_EventScript_CroagunkScene::
	clearflag FLAG_SINNOH_ESCONDE_PASTORIA_CROAGUNK
	addobject LOCALID_PASTORIA_CITY_CROAGUNK
	applymovement OBJ_EVENT_ID_PLAYER, PastoriaCity_Movement_PlayerWalkOnSpotSouth
	applymovement LOCALID_PASTORIA_CITY_CROAGUNK, PastoriaCity_Movement_CroagunkEnter
	waitmovement 0
	playmoncry SPECIES_CROAGUNK, CRY_MODE_ENCOUNTER
	waitmoncry
	delay_16
	delay_8
	delay_4
	delay_2
	applymovement LOCALID_PASTORIA_CITY_CROAGUNK, PastoriaCity_Movement_CroagunkLeave
	waitmovement 0
	playse SE_EXIT
	removeobject LOCALID_PASTORIA_CITY_CROAGUNK
	waitse
	releaseall
	end

	.balign 4, 0
PastoriaCity_Movement_PlayerWalkOnSpotSouth:
	walk_in_place_down
	step_end

	.balign 4, 0
PastoriaCity_Movement_CroagunkEnter:
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_in_place_left
	step_end

	.balign 4, 0
PastoriaCity_Movement_CroagunkLeave:
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

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
