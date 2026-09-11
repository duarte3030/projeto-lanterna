@ LcUnderseaChasm: mapa copiado de Pokémon Liquid Crystal.gba (g4m51) por
@ dev_scripts/copia_mapa_rom.py. A ARTE é do hack; o JOGO (warps, NPCs,
@ encontros, treinadores, placas) é NOSSO e está aqui.
@
@ É o mapa com correnteza: 265 células com MB_EASTWARD_CURRENT e as três irmãs
@ depois da tradução de comportamento, mais 63 de MB_WATERFALL. Isso veio do
@ hack byte a byte, não foi plantado aqui.
@
@ As três descidas da cachoeira em (61,44), (62,44) e (63,44) NÃO tinham warp no
@ hack, embora sejam MB_SOUTH_ARROW_WARP com colisão 0 na arte. Elas são as
@ portas das três regiões do lado leste (a galeria do rio, a câmara nordeste e a
@ poça sudeste), que no hack só se alcançavam por warps para Cianwood, para o
@ Cinnabar Volcano e para a Route 100, ou seja por mapas do enredo do Liquid
@ Crystal, que não entram aqui.

LcUnderseaChasm_MapScripts::
	.byte 0

LcUnderseaChasm_EventScript_Orla::
	trainerbattle_single TRAINER_JOHTO_LC_UNDERSEA_ORLA, LcUnderseaChasm_Text_OrlaSeen, LcUnderseaChasm_Text_OrlaBeaten
	msgbox LcUnderseaChasm_Text_OrlaAfter, MSGBOX_AUTOCLOSE
	end

LcUnderseaChasm_EventScript_Sorrel::
	trainerbattle_single TRAINER_JOHTO_LC_UNDERSEA_SORREL, LcUnderseaChasm_Text_SorrelSeen, LcUnderseaChasm_Text_SorrelBeaten
	msgbox LcUnderseaChasm_Text_SorrelAfter, MSGBOX_AUTOCLOSE
	end

LcUnderseaChasm_EventScript_ChasmSign::
	msgbox LcUnderseaChasm_Text_ChasmSign, MSGBOX_SIGN
	end

LcUnderseaChasm_Text_OrlaSeen:
	.string "Don't step in the current unless you\n"
	.string "mean to go where it goes.$"

LcUnderseaChasm_Text_OrlaBeaten:
	.string "And now I'm going downstream.$"

LcUnderseaChasm_Text_OrlaAfter:
	.string "The river runs east and drops twice.\n"
	.string "Both drops are one way.\p"
	.string "Whatever you leave at the top of them\n"
	.string "stays at the top.$"

LcUnderseaChasm_Text_SorrelSeen:
	.string "A river with no rain feeding it, in a\n"
	.string "cave with no sky.\p"
	.string "I have stopped asking. Battle me.$"

LcUnderseaChasm_Text_SorrelBeaten:
	.string "Questions and defeats, one after\n"
	.string "the other.$"

LcUnderseaChasm_Text_SorrelAfter:
	.string "It flows east and it never empties,\n"
	.string "so something east of here is filling\n"
	.string "it.\p"
	.string "Go and find out. I am too old to swim\n"
	.string "against that.$"

LcUnderseaChasm_Text_ChasmSign:
	.string "THE CHASM\p"
	.string "“The falls take you east and will not\n"
	.string "bring you back.\n"
	.string "Go down only when you are ready.”$"
