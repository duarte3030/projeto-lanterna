@ LcSilverCaveDepths: mapa copiado de Pokémon Liquid Crystal.gba (g4m97) por
@ dev_scripts/copia_mapa_rom.py. A ARTE é do hack; o JOGO é NOSSO.
@ Os 11% de preto do render deste mapa são ARTE do hack, não defeito: são 308
@ células do metatile 695 do secundário novo, com colisão 1, que o autor usou
@ como vazio sólido em volta da câmara do noroeste. Medido na ROM em 11/09/2026.

LcSilverCaveDepths_MapScripts::
	.byte 0

LcSilverCaveDepths_EventScript_Sigrid::
	trainerbattle_single TRAINER_JOHTO_LC_SILVER_SIGRID, LcSilverCaveDepths_Text_SigridSeen, LcSilverCaveDepths_Text_SigridBeaten
	msgbox LcSilverCaveDepths_Text_SigridAfter, MSGBOX_AUTOCLOSE
	end

LcSilverCaveDepths_EventScript_Brann::
	trainerbattle_single TRAINER_JOHTO_LC_SILVER_BRANN, LcSilverCaveDepths_Text_BrannSeen, LcSilverCaveDepths_Text_BrannBeaten
	msgbox LcSilverCaveDepths_Text_BrannAfter, MSGBOX_AUTOCLOSE
	end

LcSilverCaveDepths_EventScript_SignDepths::
	msgbox LcSilverCaveDepths_Text_SignDepths, MSGBOX_SIGN
	end

LcSilverCaveDepths_Text_SigridSeen:
	.string "You came up the ladder, so you\n"
	.string "already know there is no other\l"
	.string "way out of this room.$"

LcSilverCaveDepths_Text_SigridBeaten:
	.string "Then go back down it.$"

LcSilverCaveDepths_Text_SigridAfter:
	.string "The hall above us is cut square.\n"
	.string "Square, in a cave.\p"
	.string "Whoever did it carried the stone\n"
	.string "out. There is none left here.$"

LcSilverCaveDepths_Text_BrannSeen:
	.string "This room holds the strongest ones.\n"
	.string "Me included.$"

LcSilverCaveDepths_Text_BrannBeaten:
	.string "Not any more, it seems.$"

LcSilverCaveDepths_Text_BrannAfter:
	.string "Three rooms, three ladders, and not\n"
	.string "one passage between them.\p"
	.string "The mountain keeps them apart on\n"
	.string "purpose. That is what I think.$"

LcSilverCaveDepths_Text_SignDepths:
	.string "SILVER CAVE, THIRD LEVEL\n"
	.string "This room ends here.\l"
	.string "Go back down for the next one.$"
