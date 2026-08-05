@ QG da Galactica, B1F: o labirinto de paineis de teleporte.
@ Texto de pret/pokeplatinum, res/text/galactic_hq_b1f.json.
@
@ ponytail: layout E as 25 entradas de warp vieram do Esconderijo Aqua sem
@ mudanca nenhuma, exceto os quatro destinos que saem do mapa. Copiar a fiacao
@ inteira e o que mantem o quebra-cabeca de paineis solucionavel: o jogador
@ entra em (29,1), que e exatamente onde o jogo original o coloca.

GalacticHQ_B1F_MapScripts::
	.byte 0

GalacticHQ_B1F_EventScript_GruntiestGrunt::
	msgbox GalacticHQ_B1F_Text_GruntiestOfGrunts, MSGBOX_NPC
	end

GalacticHQ_B1F_Text_GruntiestOfGrunts:
	.string "I'm a Team Galactic member.\n"
	.string "But I don't even have a Pokémon!\p"
	.string "I'm the gruntiest of the grunts!\p"
	.string "It's my fault, though. I still\n"
	.string "don't know how the warp panels\l"
	.string "connect.$"
