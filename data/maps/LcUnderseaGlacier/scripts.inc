@ LcUnderseaGlacier: mapa copiado de Pokémon Liquid Crystal.gba (g4m103) por
@ dev_scripts/copia_mapa_rom.py. A ARTE é do hack; o JOGO (warps, NPCs,
@ encontros, treinadores, placas) é NOSSO e está aqui.
@
@ Seis câmaras de gelo separadas, de 7 a 12 células cada, ligadas SÓ por escada:
@ são doze warps num mapa de 48x34 e nenhuma das câmaras toca a outra por chão.
@ A ordem em que elas se abrem é a do hack, e a corrente inteira é
@ Gallery -> (5,6) -> (8,7)/(4,21) -> (4,19)/(25,7) -> (22,5)/(41,20) ->
@ (38,21)/(22,19) -> (24,20)/(38,5) -> (38,7) -> LcUnderseaAlcove.

LcUnderseaGlacier_MapScripts::
	.byte 0

LcUnderseaGlacier_EventScript_GlacierSign::
	msgbox LcUnderseaGlacier_Text_GlacierSign, MSGBOX_SIGN
	end

LcUnderseaGlacier_Text_GlacierSign:
	.string "Ice, under the sea, in a cave that is\n"
	.string "warm on every other side.\p"
	.string "Six rooms, six ladders, one way\n"
	.string "through. Count them.$"
