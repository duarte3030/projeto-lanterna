@ LcHollowCaveInner: mapa copiado de Pokémon Liquid Crystal.gba (g2m103) por
@ dev_scripts/copia_mapa_rom.py. A ARTE e do hack; o JOGO (warps, NPCs,
@ encontros, treinadores, placas) e nosso e entra aqui.
@
@ Este e o andar de baixo, e e ele que liga os dois bolsoes do andar de cima:
@ quatro dos cinco degraus dele sobem para o 1F e o quinto desce para a camara.
@ A porta de (16,4) da planta do hack ficou SEM warp de proposito: ela esta numa
@ celula ilhada, sem um unico passo de ligacao com o resto do andar, e por a
@ camara atras dela seria por a camara num lugar que ninguem alcanca.

LcHollowCaveInner_MapScripts::
	.byte 0

@ ---------------------------------------------------------------- treinadores

LcHollowCaveInner_EventScript_ManiacUpper::
	trainerbattle_single TRAINER_JOHTO_LC_HOLLOW_INNER_HALL, LcHollowCaveInner_Text_ManiacSeen, LcHollowCaveInner_Text_ManiacBeaten
	msgbox LcHollowCaveInner_Text_ManiacAfter, MSGBOX_AUTOCLOSE
	end

LcHollowCaveInner_EventScript_NerdLower::
	trainerbattle_single TRAINER_JOHTO_LC_HOLLOW_INNER_DEEP, LcHollowCaveInner_Text_NerdSeen, LcHollowCaveInner_Text_NerdBeaten
	msgbox LcHollowCaveInner_Text_NerdAfter, MSGBOX_AUTOCLOSE
	end

@ ---------------------------------------------------------------- gente e placas

LcHollowCaveInner_EventScript_Surveyor::
	msgbox LcHollowCaveInner_Text_Surveyor, MSGBOX_NPC
	end

LcHollowCaveInner_EventScript_SignChamberStair::
	msgbox LcHollowCaveInner_Text_SignChamberStair, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- textos

LcHollowCaveInner_Text_ManiacSeen:
	.string "Four stairs up, one stair down.\n"
	.string "Guess which one I guard!$"

LcHollowCaveInner_Text_ManiacBeaten:
	.string "Guard is a strong word now.$"

LcHollowCaveInner_Text_ManiacAfter:
	.string "Every stair on this floor climbs\n"
	.string "back to the hall above.\p"
	.string "Every one but the deep one, and\n"
	.string "that one is worth the walk.$"

LcHollowCaveInner_Text_NerdSeen:
	.string "I mapped this floor twice and\n"
	.string "got two different maps!$"

LcHollowCaveInner_Text_NerdBeaten:
	.string "Third time, then.$"

LcHollowCaveInner_Text_NerdAfter:
	.string "The sand shifts, so the walls\n"
	.string "look like they move.\p"
	.string "They don't. I just keep counting\n"
	.string "my steps wrong.$"

LcHollowCaveInner_Text_Surveyor:
	.string "The two mouths on the ridge never\n"
	.string "meet on the upper floor.\p"
	.string "Down here they do. That is the\n"
	.string "whole trick of this cave.$"

LcHollowCaveInner_Text_SignChamberStair:
	.string "THE DEEP STAIR\n"
	.string "One room below, and nothing\l"
	.string "past it.$"
