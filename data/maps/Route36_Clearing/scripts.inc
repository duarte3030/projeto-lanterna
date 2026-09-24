@ Clareira entre a guarita da Rota 36 e as Ruínas de Alph, copiada do mapa
@ `g1m36` do Pokémon GS Chronicles. A arte é do autor, byte a byte; o jogo é o
@ nosso (dev_scripts/pacote_gsc_jogo.py).
Route36_Clearing_MapScripts::
	.byte 0

Route36_Clearing_EventScript_Wade::
	trainerbattle_single TRAINER_JOHTO_CLAREIRA_ROUTE36_WADE, Route36_Clearing_Text_WadeSeen, Route36_Clearing_Text_WadeBeaten
	msgbox Route36_Clearing_Text_WadeAfter, MSGBOX_AUTOCLOSE
	end

Route36_Clearing_Text_WadeSeen:
	.string "Shh! The bugs in this grass are the\n"
	.string "rarest around. Don't scare them off!$"

Route36_Clearing_Text_WadeBeaten:
	.string "You scared them off anyway…$"

Route36_Clearing_Text_WadeAfter:
	.string "The RUINS OF ALPH are just past these\n"
	.string "trees. Nobody knows who built them.$"
