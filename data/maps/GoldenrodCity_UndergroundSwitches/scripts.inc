@ Treinadores de rota de GoldenrodCity_UndergroundSwitches, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.
@
@ 15/08/2026: a QUARTA e ultima batalha contra o SILVER voltou para CA, que e
@ onde a fonte a poe (hns/data/maps/GoldenrodCity_UndergroundSwitches,
@ EventScript_SilverTriggerTop). Ate 12/08 ela estava na calcada de
@ GoldenrodCity porque este arquivo nao era daquela sessao; ver a secao 3 do
@ PENDENCIAS-JOHTO.md.
@
@ O objeto NAO e novo: e a vaga que ja existia (indice 6), que era uma item
@ ball muda. A save do Gui guarda INDICE de object_event, entao ninguem apaga
@ nem enfia objeto no meio; so o conteudo da vaga mudou. Ela saiu de (35,2),
@ que e PAREDE na colisao deste layout (a fonte usa aquele tile so como
@ bastidor: la o SILVER e criado com `addobject` e entra andando), para (34,3),
@ que e chao, um tile ao sul do warp de (34,2) por onde o jogador desce do
@ tunel. De frente para o norte e com raio 3, ele ve quem chega, que e
@ exatamente a emboscada do texto ("eu te vi, e vim atras de voce").
@
@ Por que raio de visao e nao a coreografia da fonte: mesma razao das outras
@ tres batalhas do rival (data/maps/CherrygroveCity/scripts.inc). E por que
@ ZERO flag nova: FLAG_HIDE_SILVER_GOLDENROD ja existia e serve aos dois
@ objetos, porque a cidade e o subterraneo nunca estao carregados ao mesmo
@ tempo, e o ON_TRANSITION de cada mapa decide antes de os objetos nascerem.

GoldenrodCity_UndergroundSwitches_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, GoldenrodCity_UndergroundSwitches_OnTransition
	map_script MAP_SCRIPT_ON_LOAD, GoldenrodCity_UndergroundSwitches_EventScript_OnLoad
	.byte 0

GoldenrodCity_UndergroundSwitches_OnTransition:
	clearflag FLAG_GOLDENROD_SWITCH_1
	clearflag FLAG_GOLDENROD_SWITCH_2
	clearflag FLAG_GOLDENROD_SWITCH_3
	setflag FLAG_HIDE_SILVER_GOLDENROD
	setvar VAR_TEMP_1, 1
	goto_if_not_defeated TRAINER_JOHTO_RIVAL_SILVER_3, GoldenrodCity_UndergroundSwitches_EventScript_SilverFim
	goto_if_defeated TRAINER_JOHTO_RIVAL_SILVER_4, GoldenrodCity_UndergroundSwitches_EventScript_SilverFim
	clearflag FLAG_HIDE_SILVER_GOLDENROD
	setvar VAR_TEMP_1, 0
GoldenrodCity_UndergroundSwitches_EventScript_SilverFim:
	end

GoldenrodCity_UndergroundSwitches_EventScript_Silver::
	trainerbattle_single TRAINER_JOHTO_RIVAL_SILVER_4, GoldenrodCity_UndergroundSwitches_Text_SilverSeen, GoldenrodCity_UndergroundSwitches_Text_SilverBeaten
	msgbox GoldenrodCity_UndergroundSwitches_Text_SilverAfter, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_HIDE_SILVER_GOLDENROD
	removeobject LOCALID_GOLDENROD_CITY_UNDERGROUND_SWITCHES_SILVER
	release
	end

@ Texto do pokecrystal (maps/GoldenrodUndergroundSwitchRoomEntrances.asm), o
@ mesmo que estava em GoldenrodCity ate 15/08/2026.
GoldenrodCity_UndergroundSwitches_Text_SilverSeen:
	.string "Hold it!\p"
	.string "I saw you, so I tailed you.\p"
	.string "I don't need you underfoot while I\n"
	.string "take care of TEAM ROCKET.\p"
	.string "…Wait a second. You beat me\n"
	.string "before, didn't you?\p"
	.string "That was just a fluke.\p"
	.string "But I repay my debts!$"

GoldenrodCity_UndergroundSwitches_Text_SilverBeaten:
	.string "…Why…\n"
	.string "Why do I lose?\p"
	.string "I've assembled the toughest\n"
	.string "POKéMON.\p"
	.string "I didn't ease up on the gas.\p"
	.string "So why do I lose?$"

GoldenrodCity_UndergroundSwitches_Text_SilverAfter:
	.string "…I don't understand…\p"
	.string "Is what that LANCE guy said true?\p"
	.string "That I don't treat POKéMON\n"
	.string "properly?\p"
	.string "Love…\p"
	.string "Trust…\p"
	.string "Are they really what I lack?\p"
	.string "Are they keeping me from winning?\p"
	.string "I… I just don't understand.\p"
	.string "But it's not going to end here.\p"
	.string "Not now. Not because of this.\p"
	.string "I won't give up my dream of\n"
	.string "becoming the world's best\l"
	.string "POKéMON trainer!$"

GoldenrodCity_UndergroundSwitches_EventScript_Grunt10::
	trainerbattle_single TRAINER_JOHTO_GRUNT_10, GoldenrodCity_UndergroundSwitches_Text_Grunt10Seen, GoldenrodCity_UndergroundSwitches_Text_Grunt10Beaten
	msgbox GoldenrodCity_UndergroundSwitches_Text_Grunt10After, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_UndergroundSwitches_EventScript_Grunt20::
	trainerbattle_single TRAINER_JOHTO_GRUNT_20, GoldenrodCity_UndergroundSwitches_Text_Grunt20Seen, GoldenrodCity_UndergroundSwitches_Text_Grunt20Beaten
	msgbox GoldenrodCity_UndergroundSwitches_Text_Grunt20After, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_UndergroundSwitches_EventScript_Duncan::
	trainerbattle_single TRAINER_JOHTO_DUNCAN, GoldenrodCity_UndergroundSwitches_Text_DuncanSeen, GoldenrodCity_UndergroundSwitches_Text_DuncanBeaten
	msgbox GoldenrodCity_UndergroundSwitches_Text_DuncanAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_UndergroundSwitches_EventScript_Eddie::
	trainerbattle_single TRAINER_JOHTO_EDDIE, GoldenrodCity_UndergroundSwitches_Text_EddieSeen, GoldenrodCity_UndergroundSwitches_Text_EddieBeaten
	msgbox GoldenrodCity_UndergroundSwitches_Text_EddieAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_UndergroundSwitches_EventScript_Grunt11::
	trainerbattle_single TRAINER_JOHTO_GRUNT_11, GoldenrodCity_UndergroundSwitches_Text_Grunt11Seen, GoldenrodCity_UndergroundSwitches_Text_Grunt11Beaten
	msgbox GoldenrodCity_UndergroundSwitches_Text_Grunt11After, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_UndergroundSwitches_EventScript_Grunt27::
	trainerbattle_single TRAINER_JOHTO_GRUNT_27, GoldenrodCity_UndergroundSwitches_Text_Grunt27Seen, GoldenrodCity_UndergroundSwitches_Text_Grunt27Beaten
	msgbox GoldenrodCity_UndergroundSwitches_Text_Grunt27After, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_UndergroundSwitches_Text_Grunt10Seen:
	.string "Open one shutter, another closes.\p"
	.string "Bet you can't get where you want!$"

GoldenrodCity_UndergroundSwitches_Text_Grunt10Beaten:
	.string "Drat! I was sunk by indecision!$"

GoldenrodCity_UndergroundSwitches_Text_Grunt10After:
	.string "I'm confused too… The switch on the\n"
	.string "end is the one to press first, but…$"

GoldenrodCity_UndergroundSwitches_Text_Grunt20Seen:
	.string "Kwahaha!\p"
	.string "Confounded by the shutters, are we?\p"
	.string "I'll let you in on a secret if you\n"
	.string "can beat me!$"

GoldenrodCity_UndergroundSwitches_Text_Grunt20Beaten:
	.string "Uwww… I blew it.$"

GoldenrodCity_UndergroundSwitches_Text_Grunt20After:
	.string "All right. A hint!\p"
	.string "Change the order of switching.\p"
	.string "That'll change the ways the shutters\n"
	.string "open and close.$"

GoldenrodCity_UndergroundSwitches_Text_DuncanSeen:
	.string "Fork over your goodies!$"

GoldenrodCity_UndergroundSwitches_Text_DuncanBeaten:
	.string "Mercy!$"

GoldenrodCity_UndergroundSwitches_Text_DuncanAfter:
	.string "Steal and sell! That's basic in\n"
	.string "crime, kid!$"

GoldenrodCity_UndergroundSwitches_Text_EddieSeen:
	.string "They ditched this project before they\n"
	.string "finished.\p"
	.string "I'm searching for leftover loot.$"

GoldenrodCity_UndergroundSwitches_Text_EddieBeaten:
	.string "Over the top!$"

GoldenrodCity_UndergroundSwitches_Text_EddieAfter:
	.string "UNDERGROUND WAREHOUSE?\p"
	.string "What do you want to go there for?\p"
	.string "There's nothing down there.$"

GoldenrodCity_UndergroundSwitches_Text_Grunt11Seen:
	.string "I don't care if you're lost.\p"
	.string "You show up here, you're nothing but\n"
	.string "a victim!$"

GoldenrodCity_UndergroundSwitches_Text_Grunt11Beaten:
	.string "Urk! Yeah, think you're cool, huh?$"

GoldenrodCity_UndergroundSwitches_Text_Grunt11After:
	.string "You must have ice in your veins to\n"
	.string "dis TEAM ROCKET.$"

GoldenrodCity_UndergroundSwitches_Text_Grunt27Seen:
	.string "Are you lost? No, you can't be.\p"
	.string "You don't have that scared look.\p"
	.string "I'll give you something to be\n"
	.string "scared about!$"

GoldenrodCity_UndergroundSwitches_Text_Grunt27Beaten:
	.string "How could you?$"

GoldenrodCity_UndergroundSwitches_Text_Grunt27After:
	.string "Go wherever you'd like! Get lost!\n"
	.string "See if I care!$"

@ OS PAINÉIS, refeitos em 24/09/2026 no desenho do GS Chronicles (g1m52).
@ ------------------------------------------------------------------------
@ A lógica é a do SCRIPT DO AUTOR, lida do bytecode dele (bg 0 a 3 e o
@ ON_LOAD do mapa): cada painel LIGA e DESLIGA um conjunto fixo de persianas,
@ e o interruptor de emergência de (23,13) abre para sempre a persiana de
@ (20,12). A lógica antiga (ordem 3-2-1 e seis "paredes" do Heart & Soul)
@ pintava coordenadas da planta ANTIGA, que no desenho novo caem dentro das
@ paredes do autor, e por isso não havia como mantê-la.
@
@ Persianas, pelo canto de cima à esquerda:
@   verticais (3 células): V1 (6,7)  V2 (12,7)  V3 (6,13)  V4 (12,13)  V5 (18,13)
@   horizontais (3x2):     H1 (2,6)  H2 (2,12)  H3 (8,12)  H4 (14,12)  H5 (14,6)
@   emergência (3x2):      E (20,12)
@ Metatiles, todos do par copiado do autor (dev_scripts/copia_cidade.py com
@ --extra-metatiles 0x204,0x20c,0x242): vertical aberta 8/16/5, fechada
@ 9/17/46; horizontal aberta 5 e 42/43/43, fechada 52/53/54 e 57/58/59.
@
@ As flags dos painéis voltam a zero a cada entrada no salão, como as do
@ autor (flags temporárias do CFRU), e o ON_LOAD fecha V1 e V5 como o dele.
@ Solução medida (dev_scripts/testes_criticos/298_*): painel 2, painel 3,
@ painel 3 de novo.
GoldenrodCity_UndergroundSwitches_EventScript_Panel1::
	lockall
	goto_if_set FLAG_GOLDENROD_SWITCH_1, GoldenrodCity_UndergroundSwitches_EventScript_Panel1Off
	setflag FLAG_GOLDENROD_SWITCH_1
	playse SE_CLICK
	msgbox GoldenrodUnderground_Text_Switch1, MSGBOX_DEFAULT
	closemessage
	setmetatile 6, 7, 8, TRUE
	setmetatile 6, 8, 16, TRUE
	setmetatile 6, 9, 5, FALSE
	setmetatile 12, 7, 9, TRUE
	setmetatile 12, 8, 17, TRUE
	setmetatile 12, 9, 46, TRUE
	setmetatile 2, 12, 52, FALSE
	setmetatile 3, 12, 53, FALSE
	setmetatile 4, 12, 54, FALSE
	setmetatile 2, 13, 57, TRUE
	setmetatile 3, 13, 58, TRUE
	setmetatile 4, 13, 59, TRUE
	setmetatile 8, 12, 52, FALSE
	setmetatile 9, 12, 53, FALSE
	setmetatile 10, 12, 54, FALSE
	setmetatile 8, 13, 57, TRUE
	setmetatile 9, 13, 58, TRUE
	setmetatile 10, 13, 59, TRUE
	setmetatile 6, 13, 9, TRUE
	setmetatile 6, 14, 17, TRUE
	setmetatile 6, 15, 46, TRUE
	special DrawWholeMapView
	waitse
	releaseall
	end

GoldenrodCity_UndergroundSwitches_EventScript_Panel1Off::
	clearflag FLAG_GOLDENROD_SWITCH_1
	playse SE_BANG
	msgbox GoldenrodUnderground_Text_Switch1Off, MSGBOX_DEFAULT
	closemessage
	setmetatile 6, 7, 9, TRUE
	setmetatile 6, 8, 17, TRUE
	setmetatile 6, 9, 46, TRUE
	setmetatile 12, 7, 8, TRUE
	setmetatile 12, 8, 16, TRUE
	setmetatile 12, 9, 5, FALSE
	setmetatile 2, 12, 5, FALSE
	setmetatile 3, 12, 5, FALSE
	setmetatile 4, 12, 5, FALSE
	setmetatile 2, 13, 42, FALSE
	setmetatile 3, 13, 43, FALSE
	setmetatile 4, 13, 43, FALSE
	setmetatile 8, 12, 5, FALSE
	setmetatile 9, 12, 5, FALSE
	setmetatile 10, 12, 5, FALSE
	setmetatile 8, 13, 42, FALSE
	setmetatile 9, 13, 43, FALSE
	setmetatile 10, 13, 43, FALSE
	setmetatile 6, 13, 8, TRUE
	setmetatile 6, 14, 16, TRUE
	setmetatile 6, 15, 5, FALSE
	special DrawWholeMapView
	waitse
	releaseall
	end

GoldenrodCity_UndergroundSwitches_EventScript_Panel2::
	lockall
	goto_if_set FLAG_GOLDENROD_SWITCH_2, GoldenrodCity_UndergroundSwitches_EventScript_Panel2Off
	setflag FLAG_GOLDENROD_SWITCH_2
	playse SE_CLICK
	msgbox GoldenrodUnderground_Text_Switch2, MSGBOX_DEFAULT
	closemessage
	setmetatile 6, 7, 8, TRUE
	setmetatile 6, 8, 16, TRUE
	setmetatile 6, 9, 5, FALSE
	setmetatile 2, 6, 52, FALSE
	setmetatile 3, 6, 53, FALSE
	setmetatile 4, 6, 54, FALSE
	setmetatile 2, 7, 57, TRUE
	setmetatile 3, 7, 58, TRUE
	setmetatile 4, 7, 59, TRUE
	setmetatile 2, 12, 52, FALSE
	setmetatile 3, 12, 53, FALSE
	setmetatile 4, 12, 54, FALSE
	setmetatile 2, 13, 57, TRUE
	setmetatile 3, 13, 58, TRUE
	setmetatile 4, 13, 59, TRUE
	setmetatile 14, 12, 52, FALSE
	setmetatile 15, 12, 53, FALSE
	setmetatile 16, 12, 54, FALSE
	setmetatile 14, 13, 57, TRUE
	setmetatile 15, 13, 58, TRUE
	setmetatile 16, 13, 59, TRUE
	setmetatile 12, 13, 9, TRUE
	setmetatile 12, 14, 17, TRUE
	setmetatile 12, 15, 46, TRUE
	setmetatile 18, 13, 8, TRUE
	setmetatile 18, 14, 16, TRUE
	setmetatile 18, 15, 5, FALSE
	special DrawWholeMapView
	waitse
	releaseall
	end

GoldenrodCity_UndergroundSwitches_EventScript_Panel2Off::
	clearflag FLAG_GOLDENROD_SWITCH_2
	playse SE_BANG
	msgbox GoldenrodUnderground_Text_Switch2Off, MSGBOX_DEFAULT
	closemessage
	setmetatile 6, 7, 9, TRUE
	setmetatile 6, 8, 17, TRUE
	setmetatile 6, 9, 46, TRUE
	setmetatile 2, 6, 5, FALSE
	setmetatile 3, 6, 5, FALSE
	setmetatile 4, 6, 5, FALSE
	setmetatile 2, 7, 42, FALSE
	setmetatile 3, 7, 43, FALSE
	setmetatile 4, 7, 43, FALSE
	setmetatile 2, 12, 5, FALSE
	setmetatile 3, 12, 5, FALSE
	setmetatile 4, 12, 5, FALSE
	setmetatile 2, 13, 42, FALSE
	setmetatile 3, 13, 43, FALSE
	setmetatile 4, 13, 43, FALSE
	setmetatile 14, 12, 5, FALSE
	setmetatile 15, 12, 5, FALSE
	setmetatile 16, 12, 5, FALSE
	setmetatile 14, 13, 42, FALSE
	setmetatile 15, 13, 43, FALSE
	setmetatile 16, 13, 43, FALSE
	setmetatile 12, 13, 8, TRUE
	setmetatile 12, 14, 16, TRUE
	setmetatile 12, 15, 5, FALSE
	setmetatile 18, 13, 9, TRUE
	setmetatile 18, 14, 17, TRUE
	setmetatile 18, 15, 46, TRUE
	special DrawWholeMapView
	waitse
	releaseall
	end

GoldenrodCity_UndergroundSwitches_EventScript_Panel3::
	lockall
	goto_if_set FLAG_GOLDENROD_SWITCH_3, GoldenrodCity_UndergroundSwitches_EventScript_Panel3Off
	setflag FLAG_GOLDENROD_SWITCH_3
	playse SE_CLICK
	msgbox GoldenrodUnderground_Text_Switch3, MSGBOX_DEFAULT
	closemessage
	setmetatile 12, 7, 9, TRUE
	setmetatile 12, 8, 17, TRUE
	setmetatile 12, 9, 46, TRUE
	setmetatile 6, 13, 9, TRUE
	setmetatile 6, 14, 17, TRUE
	setmetatile 6, 15, 46, TRUE
	setmetatile 12, 13, 9, TRUE
	setmetatile 12, 14, 17, TRUE
	setmetatile 12, 15, 46, TRUE
	setmetatile 14, 6, 52, FALSE
	setmetatile 15, 6, 53, FALSE
	setmetatile 16, 6, 54, FALSE
	setmetatile 14, 7, 57, TRUE
	setmetatile 15, 7, 58, TRUE
	setmetatile 16, 7, 59, TRUE
	setmetatile 8, 12, 52, FALSE
	setmetatile 9, 12, 53, FALSE
	setmetatile 10, 12, 54, FALSE
	setmetatile 8, 13, 57, TRUE
	setmetatile 9, 13, 58, TRUE
	setmetatile 10, 13, 59, TRUE
	setmetatile 14, 12, 52, FALSE
	setmetatile 15, 12, 53, FALSE
	setmetatile 16, 12, 54, FALSE
	setmetatile 14, 13, 57, TRUE
	setmetatile 15, 13, 58, TRUE
	setmetatile 16, 13, 59, TRUE
	special DrawWholeMapView
	waitse
	releaseall
	end

GoldenrodCity_UndergroundSwitches_EventScript_Panel3Off::
	clearflag FLAG_GOLDENROD_SWITCH_3
	playse SE_BANG
	msgbox GoldenrodUnderground_Text_Switch3Off, MSGBOX_DEFAULT
	closemessage
	setmetatile 12, 7, 8, TRUE
	setmetatile 12, 8, 16, TRUE
	setmetatile 12, 9, 5, FALSE
	setmetatile 6, 13, 8, TRUE
	setmetatile 6, 14, 16, TRUE
	setmetatile 6, 15, 5, FALSE
	setmetatile 12, 13, 8, TRUE
	setmetatile 12, 14, 16, TRUE
	setmetatile 12, 15, 5, FALSE
	setmetatile 14, 6, 5, FALSE
	setmetatile 15, 6, 5, FALSE
	setmetatile 16, 6, 5, FALSE
	setmetatile 14, 7, 42, FALSE
	setmetatile 15, 7, 43, FALSE
	setmetatile 16, 7, 43, FALSE
	setmetatile 8, 12, 5, FALSE
	setmetatile 9, 12, 5, FALSE
	setmetatile 10, 12, 5, FALSE
	setmetatile 8, 13, 42, FALSE
	setmetatile 9, 13, 43, FALSE
	setmetatile 10, 13, 43, FALSE
	setmetatile 14, 12, 5, FALSE
	setmetatile 15, 12, 5, FALSE
	setmetatile 16, 12, 5, FALSE
	setmetatile 14, 13, 42, FALSE
	setmetatile 15, 13, 43, FALSE
	setmetatile 16, 13, 43, FALSE
	special DrawWholeMapView
	waitse
	releaseall
	end

GoldenrodCity_UndergroundSwitches_EventScript_Emergency::
	lockall
	goto_if_set FLAG_GOLDENROD_SWITCH_EMERGENCY, GoldenrodCity_UndergroundSwitches_EventScript_EmergencyJa
	setflag FLAG_GOLDENROD_SWITCH_EMERGENCY
	playse SE_CLICK
	msgbox GoldenrodUnderground_Text_Emergency, MSGBOX_DEFAULT
	closemessage
	setmetatile 20, 12, 5, FALSE
	setmetatile 21, 12, 5, FALSE
	setmetatile 22, 12, 5, FALSE
	setmetatile 20, 13, 42, FALSE
	setmetatile 21, 13, 43, FALSE
	setmetatile 22, 13, 43, FALSE
	special DrawWholeMapView
	waitse
	releaseall
	end

GoldenrodCity_UndergroundSwitches_EventScript_EmergencyJa::
	msgbox GoldenrodUnderground_Text_EmergencyJa, MSGBOX_DEFAULT
	closemessage
	releaseall
	end

@ ON_LOAD: o estado de toda entrada no salão, como o do autor.
GoldenrodCity_UndergroundSwitches_EventScript_OnLoad::
	setmetatile 6, 7, 9, TRUE
	setmetatile 6, 8, 17, TRUE
	setmetatile 6, 9, 46, TRUE
	setmetatile 18, 13, 9, TRUE
	setmetatile 18, 14, 17, TRUE
	setmetatile 18, 15, 46, TRUE
	goto_if_unset FLAG_GOLDENROD_SWITCH_EMERGENCY, GoldenrodCity_UndergroundSwitches_EventScript_OnLoadFim
	setmetatile 20, 12, 5, FALSE
	setmetatile 21, 12, 5, FALSE
	setmetatile 22, 12, 5, FALSE
	setmetatile 20, 13, 42, FALSE
	setmetatile 21, 13, 43, FALSE
	setmetatile 22, 13, 43, FALSE
GoldenrodCity_UndergroundSwitches_EventScript_OnLoadFim:
	end

@ O SILVER nos gatilhos do autor, (23,3) e (23,4). VAR_TEMP_1 é temporária:
@ o ON_TRANSITION a põe em 1 quando o duelo não está disponível, e o próprio
@ roteiro a põe em 1 depois do duelo.
GoldenrodCity_UndergroundSwitches_EventScript_SilverTrigger::
	lockall
	goto_if_defeated TRAINER_JOHTO_RIVAL_SILVER_4, GoldenrodCity_UndergroundSwitches_EventScript_SilverTriggerFim
	applymovement LOCALID_GOLDENROD_CITY_UNDERGROUND_SWITCHES_SILVER, Common_Movement_ExclamationMark
	waitmovement 0
	msgbox GoldenrodCity_UndergroundSwitches_Text_SilverSeen, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_JOHTO_RIVAL_SILVER_4, GoldenrodCity_UndergroundSwitches_Text_SilverBeaten
	msgbox GoldenrodCity_UndergroundSwitches_Text_SilverAfter, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_HIDE_SILVER_GOLDENROD
	removeobject LOCALID_GOLDENROD_CITY_UNDERGROUND_SWITCHES_SILVER
GoldenrodCity_UndergroundSwitches_EventScript_SilverTriggerFim:
	setvar VAR_TEMP_1, 1
	releaseall
	end

GoldenrodUnderground_Text_Switch1:
    .string "SWITCH 1 activated.$"
GoldenrodUnderground_Text_Switch2:
    .string "SWITCH 2 activated.$"
GoldenrodUnderground_Text_Switch3:
    .string "SWITCH 3 activated.$"
GoldenrodUnderground_Text_Switch1Off:
    .string "SWITCH 1 deactivated.$"
GoldenrodUnderground_Text_Switch2Off:
    .string "SWITCH 2 deactivated.$"
GoldenrodUnderground_Text_Switch3Off:
    .string "SWITCH 3 deactivated.$"
GoldenrodUnderground_Text_Emergency:
    .string "EMERGENCY SWITCH activated.\nThe shutter by the door opened!$"
GoldenrodUnderground_Text_EmergencyJa:
    .string "The EMERGENCY SWITCH is already on.$"
