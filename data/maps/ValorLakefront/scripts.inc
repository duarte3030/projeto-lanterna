ValorLakefront_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S7: cena da fonte, rotulo ValorLakefront_CoordEvent_BlockSunyshore >>>
@ Collector (LOCALID_VALOR_LAKEFRONT_COLLECTOR) ja nasce visivel (fonte nao
@ clearflag/addobject aqui, so ApplyMovement) e nunca some (RemoveObject
@ nao existe no fecho da fonte), fica plantado bloqueando a estrada.
@ FECHO: existe na fonte e NAO esta portado, igual ao caso de Pastoria. Quem
@ desarma e `SandgemTownLab_ObtainSunyshoresBadge`
@ (res/field/scripts/scripts_sandgem_town_pokemon_research_lab.s:110-111): a
@ conversa com o Rowan depois da 8a insignia faz `SetFlag
@ FLAG_HIDE_VALOR_LAKEFRONT_COLLECTOR` + `SetVar
@ VAR_VALOR_LAKEFRONT_BLOCK_SUNYSHORE_STATE, 1` na mesma respiracao (grep no
@ pokeplatinum inteiro: sao os UNICOS toques nessa flag e nessa var). Essa
@ cena do laboratorio nao existe neste porte, entao aqui o bloqueio nao
@ desarma; o objeto ja leva a flag no map.json para o dia em que ela entrar,
@ e a pendencia esta no plano.
@ ponytail: a fonte ramifica em 3 variantes de X (789/790/791) so pra
@ calibrar quantos tiles o Collector/jogador andam; aqui uma rota unica
@ (variante X790, a do meio), mesmo molde de simplificacao documentado em
@ SunyshoreCity_CoordEvent_RivalAndJasmine.
@
@ CONSERTO DE GEOMETRIA (onda 5, 18/08/2026), medido no map.bin, nao no olho:
@ - a fonte tem o Collector em (724,788) e o gatilho em (724, 789 a 791),
@   width 1 / length 3: o gatilho e a SECAO INTEIRA de uma estrada leste-
@   oeste (por isso o jogador leva empurrao pra OESTE, nao pro sul), e o
@   corpo do Collector tapa a quarta faixa;
@ - a conversao proporcional pos o Collector em (45,55), colisao 1 (parede),
@   e o realocador de gatilho do S1 espalhou as tres casas em (45,53),
@   (45,57) e (45,58). A (45,53) fica num bolso sem saida: a coluna 45 so e
@   andavel ate y=53, tem parede em 54, 55 e 56, e volta a ser andavel em
@   57, 58 e 59. Gatilho la nao barrava nada;
@ - agora as tres casas sao (45,57), (45,58) e (45,59), que sao EXATAMENTE
@   as tres unicas casas andaveis da coluna 45 (conferido no map.bin de
@   LAYOUT_VALOR_LAKEFRONT): quem vem do oeste pela estrada sul pisa numa
@   delas, sem desvio. O Collector foi para (46,58), na estrada, uma casa a
@   leste da coluna, encostado como na fonte.
@ LIMITE DITO: o nosso ValorLakefront tem DUAS saidas para MAP_ROUTE222 (a
@ estrada de Sunyshore), a sul (borda direita, linhas 57 a 61) e a norte
@ (corredor de uma casa de altura na linha 39, alcancado pelo corredor
@ vertical x=49). Este bloqueio fecha a sul. Fechar as duas pedia um segundo
@ bloqueador que a fonte nao tem, entao fica registrado no plano em vez de
@ inventado.
ValorLakefront_EventScript_CoordEvent_BlockSunyshore::
	lockall
	applymovement LOCALID_VALOR_LAKEFRONT_COLLECTOR, ValorLakefront_Movement_CollectorExclamationMark
	waitmovement 0
	applymovement LOCALID_VALOR_LAKEFRONT_COLLECTOR, ValorLakefront_Movement_CollectorWalkWest
	applymovement OBJ_EVENT_ID_PLAYER, ValorLakefront_Movement_PlayerGetPushedWest
	waitmovement 0
	msgbox ValorLakefront_Text_SunyshoreHadBlackout, MSGBOX_DEFAULT
	applymovement LOCALID_VALOR_LAKEFRONT_COLLECTOR, ValorLakefront_Movement_CollectorWalkBack
	waitmovement 0
	releaseall
	end

ValorLakefront_Movement_CollectorExclamationMark:
	emote_exclamation_mark
	delay_16
	step_end

ValorLakefront_Movement_CollectorWalkWest:
	walk_left
	step_end

ValorLakefront_Movement_PlayerGetPushedWest:
	lock_facing_direction
	walk_left
	unlock_facing_direction
	step_end

@ Volta pra casa dele, (46,58), e fica de cara pro oeste (pra estrada), como
@ o `FaceSouth` dos ValorLakefront_Movement_CollectorWalkBackX* da fonte, que
@ la e "de cara pra estrada" na orientacao de la.
ValorLakefront_Movement_CollectorWalkBack:
	walk_right
	walk_in_place_left
	step_end

ValorLakefront_Text_SunyshoreHadBlackout:
	.string "Stop, stop!\n"
	.string "Yes, you!\p"
	.string "Sunyshore City, which is down this\n"
	.string "road, had a major blackout!\p"
	.string "Crews are working on restoring\n"
	.string "power, but the road's closed now.$"

@ <<< B6 Sinnoh S7: cena da fonte <<<

ValorLakefront_EventScript_Beauty::
	msgbox ValorLakefront_Text_Beauty, MSGBOX_NPC
	end

ValorLakefront_EventScript_Tourist::
	msgbox ValorLakefront_Text_Tourist, MSGBOX_NPC
	end

ValorLakefront_EventScript_Pokefan::
	msgbox ValorLakefront_Text_Pokefan, MSGBOX_NPC
	end

ValorLakefront_EventScript_RestaurantSign::
	msgbox ValorLakefront_Text_RestaurantSign, MSGBOX_SIGN
	end

ValorLakefront_Text_Beauty:
	.string "This lakefront hotel is lovely,\n"
	.string "isn't it? I could stay here\l"
	.string "forever.$"

ValorLakefront_Text_Tourist:
	.string "I heard LAKE VALOR holds a\n"
	.string "legendary POKéMON. Wish I could\l"
	.string "see it myself.$"

ValorLakefront_Text_Pokefan:
	.string "Cameramen used to film here all\n"
	.string "the time. Not so much anymore.$"

ValorLakefront_Text_RestaurantSign:
	.string "SEVEN STARS RESTAURANT\n"
	.string "Fine dining with a lake view.$"

@ Historia: o grunt que corre com a bomba para o Lago Valor.
@ Texto de pret/pokeplatinum, res/text/valor_lakefront.json.
@ Fecho da corrente do Croagunk (onda 5/8, 18/08/2026): a fonte
@ (scripts_valor_lakefront.s:118, ValorLakefront_RemoveGruntM) apaga
@ FLAG_BLOCK_PASTORIA_CITY_CROAGUNK_EVENT so depois que o grunt sai
@ derrotado, no fim da cadeia GruntMNorth->RemoveGruntM. Aqui a cadeia
@ inteira de movimento/estados foi condensada num unico trainerbattle_single
@ (decisao ja tomada nesta cena); o clearflag entra no mesmo ponto logico,
@ apos a mensagem final do grunt derrotado. Quem acende
@ FLAG_SINNOH_PASTORIA_CROAGUNK_BLOQUEADO e o ginasio de Pastoria
@ (PastoriaCity_Gym/scripts.inc:60); quem checa e a placa do FaceBoard
@ (PastoriaCity/scripts.inc:696). Sem este clearflag o Croagunk da placa
@ ficava bloqueado para sempre depois do arco.
ValorLakefront_EventScript_GalacticGrunt::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_LAKE_VALOR_3, ValorLakefront_Text_GruntIntro, ValorLakefront_Text_GruntDefeat
	msgbox ValorLakefront_Text_GruntPostBattle, MSGBOX_AUTOCLOSE
	clearflag FLAG_SINNOH_PASTORIA_CROAGUNK_BLOQUEADO
	end

ValorLakefront_Text_GruntIntro:
	.string "...Pant...pant...\p"
	.string "Gweh! You were eavesdropping!\n"
	.string "I was only talking to myself!\p"
	.string "Aww, no...\n"
	.string "You're still on my tail...?\l"
	.string "The lake's within sight...\p"
	.string "You leave me no choice...\n"
	.string "My Pokémon will KO you...$"

ValorLakefront_Text_GruntDefeat:
	.string "I can't battle anymore...\n"
	.string "I'm running on fumes...$"

ValorLakefront_Text_GruntPostBattle:
	.string "I'll have to give this to the\n"
	.string "Commander...\p"
	.string "I wish...\n"
	.string "I got to use it at the lake...$"
