@ >>> O portão de Johto do Safari ganha script de entrada (fila de bugs, 08/09) >>>
@
@ Este portão NÃO tinha script nenhum: quem entrava no Safari por Johto passava
@ pela porta de (9,1) andando, sem pagar a taxa, sem acender o
@ VAR_SAFARI_ZONE_STATE, sem receber as 30 Safari Balls e sem o contador de 500
@ passos. O Safari de Johto É o Safari de Hoenn (os dois portões desembocam no
@ MESMO MAP_SAFARI_ZONE_SOUTH), então o molde deste script é o do portão de
@ Hoenn, data/maps/Route121_SafariZoneEntrance/scripts.inc, e os TEXTOS são os
@ mesmos, reaproveitados de data/scripts/safari_zone.inc.
@
@ Por que o gatilho fica em (9,2), e não no balcão: (9,1) é o ÚNICO tile
@ atravessável da linha 1 (lido de data/layouts/SafariZoneGate_SafariZoneEntrance/
@ map.bin, 19x15), e (9,2) é o único tile de onde se chega nele. Gatilho em
@ frente ao balcão, como o de Hoenn, deixaria a porta livre para quem desse a
@ volta. Quem volta do Safari cai em (9,2) já dentro do script de saída, que o
@ leva para (9,4) antes de devolver o controle, então o gatilho não dispara em
@ cima de quem está SAINDO.
@
@ DIFERENÇA DELIBERADA em relação a Hoenn: aqui NÃO se cobra a POKéBLOCK CASE.
@ O único lugar que entrega a caixa é o saguão de concurso
@ (LilycoveCity_ContestLobby_EventScript_GivePokeblockCase, em
@ data/scripts/contest_hall.inc), que só existe em Hoenn, e Johto vem ANTES de
@ Hoenn na ordem do cartucho 1: cobrar a caixa trancaria o Safari de Johto na
@ primeira jogada. Os alimentadores de Pokéblock lá dentro
@ continuam existindo e abrem a lista vazia para quem não tem caixa, que é o
@ mesmo que já acontece com quem entra sem nenhum Pokéblock feito.
SafariZoneGate_SafariZoneEntrance_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, SafariZoneGate_SafariZoneEntrance_OnFrame
	.byte 0

SafariZoneGate_SafariZoneEntrance_OnFrame:
	map_script_2 VAR_SAFARI_ZONE_STATE, 1, SafariZoneGate_SafariZoneEntrance_EventScript_ExitSafariZone
	.2byte 0

@ VAR_SAFARI_ZONE_STATE valendo 1 quer dizer "o jogador acabou de sair do
@ Safari". As três saídas (atendente da porta sul, fim de tempo, fim de bolas)
@ deixam o jogador em (9,2) por causa do `setdynamicwarp` lá embaixo; daqui ele
@ desce dois tiles, para (9,4), e só então recebe o controle.
SafariZoneGate_SafariZoneEntrance_EventScript_ExitSafariZone::
	lockall
	applymovement LOCALID_PLAYER, SafariZoneGate_SafariZoneEntrance_Movement_ExitSafariZone
	waitmovement 0
	setvar VAR_SAFARI_ZONE_STATE, 0
	releaseall
	end

SafariZoneGate_SafariZoneEntrance_Movement_ExitSafariZone:
	walk_down
	walk_down
	step_end

SafariZoneGate_SafariZoneEntrance_EventScript_EntranceCounterTrigger::
	lockall
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	showmoneybox 0, 0
	msgbox Route121_SafariZoneEntrance_Text_WouldYouLikeToPlay, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, SafariZoneGate_SafariZoneEntrance_EventScript_TryEnterSafariZone
	msgbox Route121_SafariZoneEntrance_Text_PlayAnotherTime, MSGBOX_DEFAULT
	goto SafariZoneGate_SafariZoneEntrance_EventScript_MovePlayerBackFromCounter
	end

SafariZoneGate_SafariZoneEntrance_EventScript_TryEnterSafariZone::
	call SafariZoneGate_SafariZoneEntrance_EventScript_CheckHasRoomForPokemon
	checkmoney 500
	goto_if_eq VAR_RESULT, 0, SafariZoneGate_SafariZoneEntrance_EventScript_NotEnoughMoney
	playse SE_SHOP
	msgbox Route121_SafariZoneEntrance_Text_ThatWillBe500Please, MSGBOX_DEFAULT
	removemoney 500
	updatemoneybox
	msgbox Route121_SafariZoneEntrance_Text_HereAreYourSafariBalls, MSGBOX_DEFAULT
	playfanfare MUS_OBTAIN_ITEM
	message Route121_SafariZoneEntrance_Text_Received30SafariBalls
	waitfanfare
	msgbox Route121_SafariZoneEntrance_Text_PleaseEnjoyYourself, MSGBOX_DEFAULT
	closemessage
	hidemoneybox
	applymovement LOCALID_PLAYER, SafariZoneGate_SafariZoneEntrance_Movement_EnterSafariZone
	waitmovement 0
@ EnterSafariMode (src/safari_zone.c) é quem acende FLAG_SYS_SAFARI_MODE, põe as
@ 30 Safari Balls em gNumSafariBalls e os 500 passos em gSafariZoneStepCounter.
	special EnterSafariMode
	setvar VAR_SAFARI_ZONE_STATE, 2
	clearflag FLAG_GOOD_LUCK_SAFARI_ZONE
@ O retorno, gravado no `dynamicWarp` do SaveBlock1 (custo de save zero): as três
@ saídas do Safari leem daqui em vez de um mapa escrito à mão, e é por isso que
@ quem entra por Johto volta para Johto. Tem de ser AQUI porque `warp` de script
@ não passa pelo `SetupWarp`, o único ponto em que o motor grava esse retorno
@ sozinho. (9,2) é o tile em frente à porta, e o script de saída lá em cima
@ recolhe o jogador de lá. Motivo completo em src/field_specials.c.
	setdynamicwarp MAP_SAFARI_ZONE_GATE_SAFARI_ZONE_ENTRANCE, 9, 2
@ >>> O Safari de Johto deixa de ser o Safari de Hoenn (frente D, 11/09/2026) >>>
@ Era `warp MAP_SAFARI_ZONE_SOUTH, 32, 33`, ou seja quem pagava aqui caía no
@ Safari de HOENN, o mesmo mapa que a Rota 121 recebe. Agora Johto tem as TRÊS
@ áreas copiadas do Pokémon Liquid Crystal, e quem paga ESCOLHE em qual entra.
@
@ O `TRUE` do multichoice é `ignoreBPress`, e ele não é enfeite: o jogador JÁ
@ PAGOU os 500 e já recebeu as 30 SAFARI BALLS duas mensagens acima. Se B
@ cancelasse, o script cairia no fim sem warp nenhum e o jogador ficaria dentro
@ do portão, em modo Safari, com o dinheiro gasto e sem área. Sem saída para B,
@ toda escolha é uma área.
@
@ A ORDEM dos `case` é a ordem de MultichoiceList_SafariJohtoAreas
@ (src/data/script_menu.h): `multichoice` devolve o ÍNDICE DA LINHA, então
@ linha 0 é MOUNTAIN, linha 1 é FOREST e linha 2 é WATER. Reordenar a lista sem
@ reordenar estes três `case` troca o destino em silêncio.
@
@ TROCAR DE ÁREA sai de graça: este bloco inteiro roda TODA VEZ que se paga a
@ taxa, então quem sai de uma área e paga de novo cai no menu de novo. Não há
@ estado guardado de "área escolhida", e por isso não há nada a acrescentar no
@ save.
	msgbox SafariZoneGate_SafariZoneEntrance_Text_WhichArea, MSGBOX_DEFAULT
	multichoice 18, 6, MULTI_SAFARI_JOHTO_AREAS, TRUE
	switch VAR_RESULT
	case 0, SafariZoneGate_SafariZoneEntrance_EventScript_EnterMountain
	case 1, SafariZoneGate_SafariZoneEntrance_EventScript_EnterForest
	case 2, SafariZoneGate_SafariZoneEntrance_EventScript_EnterWater
@ Rede de segurança: `multichoice` com ignoreBPress não devolve MULTI_B_PRESSED,
@ mas um `switch` sem saída deixaria o jogador preso se algum dia a lista
@ crescer e alguém esquecer de acrescentar o `case`. A montanha é o destino
@ padrão.
	goto SafariZoneGate_SafariZoneEntrance_EventScript_EnterMountain
	end

SafariZoneGate_SafariZoneEntrance_EventScript_EnterMountain::
	warp MAP_LC_SAFARI_MOUNTAIN, 9, 44
	waitstate
	end

SafariZoneGate_SafariZoneEntrance_EventScript_EnterForest::
	warp MAP_LC_SAFARI_FOREST, 25, 49
	waitstate
	end

SafariZoneGate_SafariZoneEntrance_EventScript_EnterWater::
	warp MAP_LC_SAFARI_WATER, 43, 44
	waitstate
	end

SafariZoneGate_SafariZoneEntrance_Text_WhichArea::
	.string "The SAFARI ZONE has three areas.\p"
	.string "Which one shall I open for you?$"
@ <<< O Safari de Johto deixa de ser o Safari de Hoenn <<<

SafariZoneGate_SafariZoneEntrance_EventScript_CheckHasRoomForPokemon::
	getpartysize
	goto_if_ne VAR_RESULT, PARTY_SIZE, SafariZoneGate_SafariZoneEntrance_EventScript_HasRoomForPokemon
	specialvar VAR_RESULT, ScriptCheckFreePokemonStorageSpace
	goto_if_eq VAR_RESULT, 1, SafariZoneGate_SafariZoneEntrance_EventScript_HasRoomForPokemon
	msgbox Route121_SafariZoneEntrance_Text_PCIsFull, MSGBOX_DEFAULT
	goto SafariZoneGate_SafariZoneEntrance_EventScript_MovePlayerBackFromCounter
	end

SafariZoneGate_SafariZoneEntrance_EventScript_HasRoomForPokemon::
	return

SafariZoneGate_SafariZoneEntrance_EventScript_NotEnoughMoney::
	msgbox Route121_SafariZoneEntrance_Text_NotEnoughMoney, MSGBOX_DEFAULT
	goto SafariZoneGate_SafariZoneEntrance_EventScript_MovePlayerBackFromCounter
	end

SafariZoneGate_SafariZoneEntrance_EventScript_MovePlayerBackFromCounter::
	closemessage
	hidemoneybox
	applymovement LOCALID_PLAYER, SafariZoneGate_SafariZoneEntrance_Movement_BackAwayFromCounter
	waitmovement 0
	releaseall
	end

SafariZoneGate_SafariZoneEntrance_Movement_BackAwayFromCounter:
	walk_down
	step_end

SafariZoneGate_SafariZoneEntrance_Movement_EnterSafariZone:
	walk_up
	delay_16
	step_end
@ <<< O portão de Johto do Safari ganha script de entrada <<<

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

Route121_SafariZoneGate_SafariZoneEntrance_EventScript_WelcomeAttendant::
	msgbox Route121_SafariZoneGate_SafariZoneEntrance_Text_WelcomeToSafariZone, MSGBOX_NPC
	end

Route121_SafariZoneGate_SafariZoneEntrance_Text_WelcomeToSafariZone::
	.string "Welcome to the SAFARI ZONE!\p"
	.string "Here, you may witness many kinds of\n"
	.string "POKéMON rarely seen in JOHTO.\p"
	.string "And, you'll see them in their wild,\n"
	.string "untamed state in natural habitats.\p"
	.string "What's more, we've thrown open the\n"
	.string "gates to POKéMON TRAINERS.\p"
	.string "You're encouraged to catch POKéMON\n"
	.string "for keeps!\p"
	.string "Come in and enjoy the SAFARI ZONE!$"

Route121_SafariZoneGate_SafariZoneEntrance_Text_WelcomeFirstTime::
	.string "Welcome to the SAFARI ZONE!\n"
	.string "Is it your first time here?$"

SafariZoneGate_SafariZoneEntrance_EventScript_InfoAttendantFala::
	msgbox Route121_SafariZoneGate_SafariZoneEntrance_Text_WelcomeFirstTime, MSGBOX_NPC
	end

SafariZoneGate_SafariZoneEntrance_EventScript_Boy::
	lock
	faceplayer
	msgbox SafariZoneGate_SafariZoneEntrance_Text_Boy, MSGBOX_DEFAULT
	closemessage
	release
	end

SafariZoneGate_SafariZoneEntrance_Text_Boy::
	.string "I heard the new zone they\n"
	.string "are working on has dragons!$"
