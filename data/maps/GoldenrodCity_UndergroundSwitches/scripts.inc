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
	.byte 0

GoldenrodCity_UndergroundSwitches_OnTransition:
	setflag FLAG_HIDE_SILVER_GOLDENROD
	goto_if_not_defeated TRAINER_JOHTO_RIVAL_SILVER_3, GoldenrodCity_UndergroundSwitches_EventScript_SilverFim
	goto_if_defeated TRAINER_JOHTO_RIVAL_SILVER_4, GoldenrodCity_UndergroundSwitches_EventScript_SilverFim
	clearflag FLAG_HIDE_SILVER_GOLDENROD
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
