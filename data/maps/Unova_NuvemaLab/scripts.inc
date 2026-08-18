@ NuvemaLab do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@ Cenas do laboratorio escritas a mao em 15/08/2026 (B6 Unova, Obra 1, bloco A6),
@ no molde de data/maps/Unova_ChampionsRoom/scripts.inc.
@
@ AS DUAS CENAS DE ENTRADA. A fonte tem `NuvemaLabScript1` (coord_event 2,9) e
@ `NuvemaLabScript2` (coord_event 3,9); a unica diferenca entre elas e o
@ caminho que o jogador anda ate parar em (2,5) diante da BIANCA, e dai as duas
@ caem no mesmo corpo (`NuvemaLabScript`), que aqui e
@ Unova_NuvemaLab_EventScript_NuvemaLabCena. O `jump` da fonte virou `goto` e o
@ fallthrough da segunda foi preservado.
@
@ ROTAS DO JOGADOR, conferidas contra data/layouts/.../map.bin: (2,9) sobe
@ quatro e para em (2,5), livre; (3,9) faz cima, esquerda, cima, cima, cima e
@ para no mesmo (2,5). As duas passam POR CIMA de (2,7), que nesta ROM tem a
@ Poke Bola do SNIVY (objeto da decisao 68 do Gui, que nao existe no BW3G):
@ `applymovement` e movimento forcado e ignora colisao, entao o jogador
@ atravessa e termina num tile livre. O mesmo vale para a saida da JUNIPER, que
@ desce a coluna 2 ate a porta (2,11) cruzando (2,10), parede no map.bin.
@
@ ESCONDER A JUNIPER SEM FLAG NOVA. A fonte faz `disappear NUVEMALAB_JUNIPER`,
@ que e o EVENT_NUVEMA_LAB_JUNIPER do proprio object_event. Esse EVENT_ nao
@ esta na tabela de flags do PLANO-OBRAS-UNOVA.md (a varredura pegou os
@ `setevent`/`clearevent` escritos nos scripts, e `disappear` nao escreve o nome
@ do evento) e a janela de save esta fechada, entao ZERO flag nova. O objeto
@ dela passa a usar FLAG_UNOVA_CENA_JUNIPER, o mesmo bit que
@ data/maps/Unova_ChampionsRoom/scripts.inc ja usa para esconder a JUNIPER de
@ la. Isso e seguro porque TODO mapa que usa esse bit o REESCREVE no proprio
@ ON_TRANSITION antes de os objetos nascerem: o bit nao carrega estado de um
@ mapa para o outro, ele so diz "a JUNIPER esta escondida AQUI, agora".
@
@ Ids locais (indice no map.json + 1):
@   1 = BIANCA   2,3 = assistentes   4 = JUNIPER   5,6,7 = Poke Bolas iniciais

Unova_NuvemaLab_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Unova_NuvemaLab_OnTransition
	.byte 0

@ Roda ANTES de InitMap() criar os object_events (tecnica 2 do SINNOH-PADRAO.md).
@ DEPENDENCIA COMPARTILHADA, nao mexer aqui sozinho: FLAG_UNOVA_CENA_JUNIPER e o
@ MESMO bit em Unova_NuvemaLab, Unova_P2LabEntrance, Unova_ChampionsRoom,
@ Unova_UndellaTown (MARLON da cena de chegada), Unova_CasteliaCityStreets
@ (CHEREN da cena da insígnia), Unova_FloccesyTown (JUNIPER), Unova_NacreneCity
@ (LENORA) e Unova_PWTOutside (CHEREN e BIANCA juntos). Os três últimos
@ entraram em 16/08/2026, quando o ON_LOAD + removeobject deles foi trocado por
@ ON_TRANSITION (ON_LOAD roda dentro de InitMap(), antes de os objetos
@ nascerem, e o removeobject de lá nunca fazia nada). O
@ contrato que faz isso funcionar e "todo mapa que usa o bit o REESCREVE no seu
@ proprio ON_TRANSITION, antes de os objetos nascerem". Quem tirar ou condicionar
@ esta escrita em UM dos oito quebra os outros sete (o NPC de cena nasce ou
@ some no mapa errado). Mudou um, confira os oito.
Unova_NuvemaLab_OnTransition:
	goto_if_eq VAR_UNOVA_NUVEMA_LAB_CENA, 0, Unova_NuvemaLab_EventScript_TransicaoAntesDaCena
	setflag FLAG_UNOVA_CENA_JUNIPER
	end

Unova_NuvemaLab_EventScript_TransicaoAntesDaCena::
	clearflag FLAG_UNOVA_CENA_JUNIPER
	end

@ `NuvemaLabScript1` da fonte (coord_event 2,9).
Unova_NuvemaLab_EventScript_NuvemaLabScript1::
	lockall
	applymovement LOCALID_PLAYER, Unova_NuvemaLab_Movement_JogadorPelaEsquerda
	waitmovement 0
	goto Unova_NuvemaLab_EventScript_NuvemaLabCena

@ `NuvemaLabScript2` da fonte (coord_event 3,9), que CAI no corpo comum.
Unova_NuvemaLab_EventScript_NuvemaLabScript2::
	lockall
	applymovement LOCALID_PLAYER, Unova_NuvemaLab_Movement_JogadorPelaDireita
	waitmovement 0
	@ cai no proximo

@ `NuvemaLabScript` da fonte.
Unova_NuvemaLab_EventScript_NuvemaLabCena::
	msgbox Unova_NuvemaLab_Text_BiancaIntro, MSGBOX_DEFAULT
	closemessage
	applymovement 1, Common_Movement_ExclamationMark
	waitmovement 0
	msgbox Unova_NuvemaLab_Text_BiancaGift, MSGBOX_DEFAULT
	closemessage
	giveitem ITEM_HM03
	msgbox Unova_NuvemaLab_Text_BiancaHM, MSGBOX_DEFAULT
	closemessage
	msgbox Unova_NuvemaLab_Text_JuniperLeave, MSGBOX_DEFAULT
	closemessage
	applymovement 4, Unova_NuvemaLab_Movement_JuniperVaiEmbora
	waitmovement 0
	playse SE_DOOR
	setflag FLAG_UNOVA_CENA_JUNIPER
	removeobject 4
	waitse
	@ `setscene SCENE_FINISHED` da fonte
	setvar VAR_UNOVA_NUVEMA_LAB_CENA, 1
	releaseall
	end

@ `NuvemaLabPlayerMovement1` da fonte: (2,9) -> (2,5).
Unova_NuvemaLab_Movement_JogadorPelaEsquerda:
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

@ `NuvemaLabPlayerMovement2` da fonte: (3,9) -> (2,5).
Unova_NuvemaLab_Movement_JogadorPelaDireita:
	walk_up
	walk_left
	walk_up
	walk_up
	walk_up
	step_end

@ `NuvemaLabJuniperMovement` da fonte: (1,4) -> porta em (2,11).
Unova_NuvemaLab_Movement_JuniperVaiEmbora:
	walk_down
	walk_down
	walk_right
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

@ `NuvemaLabBiancaIntroText` da fonte, palavra a palavra.
Unova_NuvemaLab_Text_BiancaIntro::
	.string "BIANCA: Oh, hi {PLAYER}!\p"
	.string "It's me, PROF. BIANCA! It's so\n"
	.string "good to finally meet you!\p"
	.string "PROF.JUNIPER had just stopped\n"
	.string "by for a visit.\p"
	.string "JUNIPER: Good to see you,\n"
	.string "{PLAYER}.\p"
	.string "It's fortunate that you've come.\p"
	.string "The reason I came out here is to\n"
	.string "follow up on a tip about TEAM\l"
	.string "PLASMA.\p"
	.string "I've learned that TEAM PLASMA\n"
	.string "had a secret lab on an island\l"
	.string "nearby NUVEMA TOWN.\p"
	.string "I thought it may give us some\n"
	.string "answers to what they're\l"
	.string "planning.\p"
	.string "If you'd like to help, it would\n"
	.string "be much appreciated, {PLAYER}.$"

@ `NuvemaLabBiancaGiftText` da fonte.
Unova_NuvemaLab_Text_BiancaGift::
	.string "BIANCA: Oh, that reminds me!\p"
	.string "I have a gift for you, {PLAYER}!$"

@ `NuvemaLabBiancaHMText` da fonte.
Unova_NuvemaLab_Text_BiancaHM::
	.string "BIANCA: HM03 is SURF.\p"
	.string "It's a powerful water-type\n"
	.string "attack, and a POKéMON that\l"
	.string "knows SURF can be used to cross\l"
	.string "the water!\p"
	.string "You'll need the GYM BADGE from\n"
	.string "STRIATON CITY to use it though.$"

@ `NuvemaLabJuniperLeaveText` da fonte.
Unova_NuvemaLab_Text_JuniperLeave::
	.string "JUNIPER: Well PROF, I'd better\n"
	.string "be off.\p"
	.string "The LAB is located on ROUTE 17,\n"
	.string "just west of ROUTE 1.\p"
	.string "Feel free to join me if you'd\n"
	.string "like, {PLAYER}!$"

Unova_NuvemaLab_EventScript_Placa2::
	msgbox Unova_NuvemaLab_Text_BiancasLabFridgeText, MSGBOX_SIGN
	end

Unova_NuvemaLab_EventScript_Placa3::
	msgbox Unova_NuvemaLab_Text_BiancasLabSinkText, MSGBOX_SIGN
	end

Unova_NuvemaLab_EventScript_Placa4::
	msgbox Unova_NuvemaLab_Text_BiancasLabStoveText, MSGBOX_SIGN
	end

Unova_NuvemaLab_EventScript_Placa5::
	msgbox Unova_NuvemaLab_Text_BiancasLabPCText, MSGBOX_SIGN
	end

Unova_NuvemaLab_EventScript_Npc0::
	msgbox Unova_NuvemaLab_Text_BiancaLabP2LocationText, MSGBOX_NPC
	end

Unova_NuvemaLab_EventScript_Npc1::
	msgbox Unova_NuvemaLab_Text_BiancasAssistant1Text, MSGBOX_NPC
	end

Unova_NuvemaLab_EventScript_Npc2::
	msgbox Unova_NuvemaLab_Text_BiancasAssistant2Text, MSGBOX_NPC
	end


Unova_NuvemaLab_Text_BiancasLabFridgeText::
	.string "It's the PROF's"
	.string "\nfridge!"
	.string "\pBetter not snoop"
	.string "\naround in here…$"

Unova_NuvemaLab_Text_BiancasLabSinkText::
	.string "There are dishes"
	.string "\nand glass bottles"
	.string "\lin the sink."
	.string "\pSomeone should"
	.string "\nreally clean this"
	.string "\lup!$"

Unova_NuvemaLab_Text_BiancasLabStoveText::
	.string "It looks like the"
	.string "\nstove hasn't been"
	.string "\lused in a while…$"

Unova_NuvemaLab_Text_BiancasLabPCText::
	.string "There's an e-mail"
	.string "\nmessage on the PC."
	.string "\p…"
	.string "\pPROF.BIANCA, I"
	.string "\ngot news about"
	.string "\lthat thing…"
	.string "\pThere was a break"
	.string "\nin at my GYM. I"
	.string "\lthink someone was"
	.string "\ptryin' ta get"
	.string "\ntheir hands on"
	.string "\lthat thing."
	.string "\pI'm gonna move"
	.string "\nit to a more"
	.string "\lsecure place."
	.string "\pOnly members of"
	.string "\nthe POKéMON league"
	.string "\lwill be able to"
	.string "\lget to it."
	.string "\pThis thing is"
	.string "\nturnin' out to be"
	.string "\la load of trouble…"
	.string "\pThanks for the"
	.string "\nPOKéDEX, by the"
	.string "\lway. {PLAYER}"
	.string "\lis a natural!"
	.string "\pGood vibes,"
	.string "\n-MARLON$"

Unova_NuvemaLab_Text_BiancaLabP2LocationText::
	.string "BIANCA: Are you"
	.string "\ngoing to join"
	.string "\pPROF.JUNIPER at"
	.string "\nthat secret lab?"
	.string "\pYou can reach"
	.string "\nROUTE 17 if you"
	.string "\pgo north, then"
	.string "\ncross the water"
	.string "\lto the west.$"

Unova_NuvemaLab_Text_BiancasAssistant1Text::
	.string "Whew, I've got a"
	.string "\nlot to keep up"
	.string "\pwith. The PROF's"
	.string "\nalways busy with"
	.string "\lsomething!$"

Unova_NuvemaLab_Text_BiancasAssistant2Text::
	.string "The PROF is young,"
	.string "\nbut she's done a"
	.string "\lgreat job so far!$"

@ Trecho devolvido em 06/08/2026: o commit das placas (febde977c3)
@ reescreveu este arquivo a partir da fonte do BW3G e levou junto os
@ scripts dos tres iniciais, que nao vem do BW3G e sim da decisao 68 do Gui.
Unova_NuvemaLab_EventScript_BallSnivy::
	lock
	faceplayer
	showmonpic SPECIES_SNIVY, 10, 3
	bufferspeciesname STR_VAR_1, SPECIES_SNIVY
	msgbox Unova_NuvemaLab_Text_WillYouTakeThisOne, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Unova_NuvemaLab_EventScript_DeclinedStarter
	hidemonpic
	givemon SPECIES_SNIVY, 70
	setvar VAR_STARTER_MON, 0
	goto Unova_NuvemaLab_EventScript_ChoseStarter

Unova_NuvemaLab_EventScript_BallTepig::
	lock
	faceplayer
	showmonpic SPECIES_TEPIG, 10, 3
	bufferspeciesname STR_VAR_1, SPECIES_TEPIG
	msgbox Unova_NuvemaLab_Text_WillYouTakeThisOne, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Unova_NuvemaLab_EventScript_DeclinedStarter
	hidemonpic
	givemon SPECIES_TEPIG, 70
	setvar VAR_STARTER_MON, 1
	goto Unova_NuvemaLab_EventScript_ChoseStarter

Unova_NuvemaLab_EventScript_BallOshawott::
	lock
	faceplayer
	showmonpic SPECIES_OSHAWOTT, 10, 3
	bufferspeciesname STR_VAR_1, SPECIES_OSHAWOTT
	msgbox Unova_NuvemaLab_Text_WillYouTakeThisOne, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Unova_NuvemaLab_EventScript_DeclinedStarter
	hidemonpic
	givemon SPECIES_OSHAWOTT, 70
	setvar VAR_STARTER_MON, 2
	goto Unova_NuvemaLab_EventScript_ChoseStarter

Unova_NuvemaLab_EventScript_DeclinedStarter::
	hidemonpic
	release
	end

Unova_NuvemaLab_EventScript_ChoseStarter::
	setflag FLAG_INICIAL_UNOVA
	setflag FLAG_SYS_POKEMON_GET
	message Unova_NuvemaLab_Text_ReceivedStarter
	waitmessage
	playfanfare MUS_OBTAIN_ITEM
	waitfanfare
	msgbox gText_NicknameThisPokemon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Unova_NuvemaLab_EventScript_AfterStarter
	setvar VAR_0x8004, 0
	call Common_EventScript_NameReceivedPartyMon
	goto Unova_NuvemaLab_EventScript_AfterStarter

Unova_NuvemaLab_EventScript_AfterStarter::
	removeobject LOCALID_JUNIPER_LAB_BALL_SNIVY
	removeobject LOCALID_JUNIPER_LAB_BALL_TEPIG
	removeobject LOCALID_JUNIPER_LAB_BALL_OSHAWOTT
	release
	end

@ Aviso mecanico, nao e fala do BW3G.
Unova_NuvemaLab_Text_WillYouTakeThisOne::
	.string "This POKé BALL holds a\n"
	.string "{STR_VAR_1}.\p"
	.string "Will you take this one?$"

@ Aviso mecanico, nao e fala do BW3G.
Unova_NuvemaLab_Text_ReceivedStarter::
	.string "{PLAYER} received the\n"
	.string "{STR_VAR_1}!$"
