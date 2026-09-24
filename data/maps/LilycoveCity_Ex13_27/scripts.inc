@ LilycoveCity_Ex13_27: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 13.27) por dev_scripts/copia_planta_ex.py.

LilycoveCity_Ex13_27_MapScripts::
	.byte 0

@ Troca e neta do EX (13.27), reescritas no nosso formato a partir do bytecode e do texto
@ da ROM (decisão 7 do Fable). O EX usa a flag 0x16F e a temporária 0x1; aqui
@ FLAG_HOENNEX_LILYCOVE_TROCA_KONA (faixa do lote C) e FLAG_TEMP_1.
LilycoveCity_Ex13_27_EventScript_ExTroca::
	lock
	faceplayer
	goto_if_set FLAG_HOENNEX_LILYCOVE_TROCA_KONA, LilycoveCity_Ex13_27_EventScript_ExTrocaFeita
	ingame_trade INGAME_TRADE_HAKAMO_O, LilycoveCity_Ex13_27_Text_ExQuerTrocar, LilycoveCity_Ex13_27_EventScript_ExRecusa, LilycoveCity_Ex13_27_EventScript_ExNaoEFomantis, LilycoveCity_Ex13_27_Text_ExObrigada
	setflag FLAG_HOENNEX_LILYCOVE_TROCA_KONA
	setflag FLAG_TEMP_1
	release
	end

LilycoveCity_Ex13_27_EventScript_ExTrocaFeita::
	msgbox LilycoveCity_Ex13_27_Text_ExDeAlola, MSGBOX_DEFAULT
	release
	end

LilycoveCity_Ex13_27_EventScript_ExRecusa::
	msgbox LilycoveCity_Ex13_27_Text_ExQuePena, MSGBOX_DEFAULT
	release
	end

LilycoveCity_Ex13_27_EventScript_ExNaoEFomantis::
	msgbox LilycoveCity_Ex13_27_Text_ExNaoEFomantis, MSGBOX_DEFAULT
	release
	end

LilycoveCity_Ex13_27_EventScript_ExNeta::
	goto_if_unset FLAG_HOENNEX_LILYCOVE_TROCA_KONA, LilycoveCity_Ex13_27_EventScript_ExNetaSemFomantis
	goto_if_set FLAG_TEMP_1, LilycoveCity_Ex13_27_EventScript_ExNetaSemFomantis
	msgbox LilycoveCity_Ex13_27_Text_ExMeuFomantis, MSGBOX_NPC
	end

LilycoveCity_Ex13_27_EventScript_ExNetaSemFomantis::
	msgbox LilycoveCity_Ex13_27_Text_ExSempreQuis, MSGBOX_NPC
	end

LilycoveCity_Ex13_27_Text_ExQuerTrocar:
	.string "My granddaughter is having a very hard\n"
	.string "time catching a FOMANTIS, would you\l"
	.string "trade one for my HAKAMO-O?$"

LilycoveCity_Ex13_27_Text_ExQuePena:
	.string "A shame,\n"
	.string "It’s probably best for her to catch it\l"
	.string "herself.$"

LilycoveCity_Ex13_27_Text_ExNaoEFomantis:
	.string "Oh! That isn’t a FOMANTIS.\p"
	.string "Come back if you get one!$"

LilycoveCity_Ex13_27_Text_ExObrigada:
	.string "Thank you very much dear.\n"
	.string "Take good care of my KONA.$"

LilycoveCity_Ex13_27_Text_ExDeAlola:
	.string "You came all the way from LITTLEROOT\n"
	.string "child?\p"
	.string "Why, I came all the way from the ALOLA\n"
	.string "REGION!$"

LilycoveCity_Ex13_27_Text_ExMeuFomantis:
	.string "My FOMANTIS is the best!\p"
	.string "Hmm, it’s POKéBALL shook when wou came\n"
	.string "in...$"

LilycoveCity_Ex13_27_Text_ExSempreQuis:
	.string "I’ve always wanted a FOMANTIS from the\n"
	.string "SAFARI ZONE.\p"
	.string "But they always run away when I get\n"
	.string "close!$"
