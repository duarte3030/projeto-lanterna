@ CHERRYGROVE CITY. Primeira batalha contra SILVER, o rival de Johto, portada
@ do pokecrystal (maps/CherrygroveCity.asm, CherrygroveRivalScene* e textos).
@
@ Duas adaptações, as duas por recurso e não por gosto:
@
@ 1. Time FIXO. No original o time do SILVER responde ao inicial do jogador:
@    são três TRAINER_ por batalha, escolhidos por VAR_STARTER_MON. Nesta build
@    o inicial vem do laboratório do ROWAN, em Sinnoh, e aquele script NÃO
@    escreve VAR_STARTER_MON (confira data/maps/SandgemTown_House1/scripts.inc:
@    ele só dá o Pokémon e liga FLAG_SYS_POKEMON_GET). Ler a var daria sempre o
@    mesmo galho, ou seja, o triângulo de tipos seria mentira. Então o SILVER
@    roubou o TOTODILE e pronto, uma batalha por encontro. Para ter o triângulo
@    de volta bastaria acrescentar um "setvar VAR_STARTER_MON, 0/1/2" nos três
@    galhos daquele arquivo e criar mais oito TRAINER_ (há 33 vagas livres).
@
@ 2. Gatilho por RAIO DE VISÃO, e não por coord_event. No original é um
@    coord_event preso a SCENE_CHERRYGROVECITY_MEET_RIVAL, que em gen 3 viraria
@    uma var de estágio. Treinador com raio de visão faz a mesma coisa de graça:
@    o motor cuida da exclamação, da aproximação e de gravar que ele já perdeu.
@    Quem controla a ORDEM dos encontros é o ON_TRANSITION abaixo.
@
@ Cortado: o galho de derrota (BATTLETYPE_CANLOSE). Em gen 3 perder é apagar,
@ então CherrygroveRivalText_YouLost e RivalCherrygroveLossText não têm onde
@ entrar. O texto de vitória é o do original.

CherrygroveCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, CherrygroveCity_OnTransition
	.byte 0

CherrygroveCity_OnTransition:
	setflag FLAG_HIDE_SILVER_CHERRYGROVE
	goto_if_unset FLAG_SILVER_NEW_BARK_DONE, CherrygroveCity_EventScript_SilverFim
	goto_if_defeated TRAINER_JOHTO_RIVAL_SILVER_1, CherrygroveCity_EventScript_SilverFim
	clearflag FLAG_HIDE_SILVER_CHERRYGROVE
CherrygroveCity_EventScript_SilverFim:
	end

CherrygroveCity_EventScript_Silver::
	trainerbattle_single TRAINER_JOHTO_RIVAL_SILVER_1, CherrygroveCity_Text_SilverSeen, CherrygroveCity_Text_SilverBeaten
	msgbox CherrygroveCity_Text_SilverAfter, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_HIDE_SILVER_CHERRYGROVE
	removeobject LOCALID_CHERRYGROVE_CITY_SILVER
	release
	end

CherrygroveCity_Text_SilverSeen:
	.string "…… …… ……\p"
	.string "You got a POKéMON at the LAB.\p"
	.string "What a waste. A wimp like you.\p"
	.string "…… …… ……\p"
	.string "Don't you get what I'm saying?\p"
	.string "Well, I too, have a good POKéMON.\p"
	.string "I'll show you what I mean!$"

CherrygroveCity_Text_SilverBeaten:
	.string "Humph. Are you happy you won?$"

CherrygroveCity_Text_SilverAfter:
	.string "…… …… ……\p"
	.string "My name's ???.\p"
	.string "I'm going to be the world's\n"
	.string "greatest POKéMON trainer.$"
