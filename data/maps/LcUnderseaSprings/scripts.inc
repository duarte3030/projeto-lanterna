@ LcUnderseaSprings: mapa copiado de Pokémon Liquid Crystal.gba (g4m50) por
@ dev_scripts/copia_mapa_rom.py. A ARTE é do hack; o JOGO (warps, NPCs,
@ encontros, treinadores, placas) é NOSSO e está aqui.
@
@ O nome vem do que a arte mostra e do que o atributo copiado diz: dez células
@ deste mapa têm MB_HOT_SPRINGS depois da tradução de comportamento, ou seja
@ fonte quente de verdade, não enfeite.

LcUnderseaSprings_MapScripts::
	.byte 0

LcUnderseaSprings_EventScript_Holt::
	trainerbattle_single TRAINER_JOHTO_LC_UNDERSEA_HOLT, LcUnderseaSprings_Text_HoltSeen, LcUnderseaSprings_Text_HoltBeaten
	msgbox LcUnderseaSprings_Text_HoltAfter, MSGBOX_AUTOCLOSE
	end

LcUnderseaSprings_EventScript_Peri::
	trainerbattle_single TRAINER_JOHTO_LC_UNDERSEA_PERI, LcUnderseaSprings_Text_PeriSeen, LcUnderseaSprings_Text_PeriBeaten
	msgbox LcUnderseaSprings_Text_PeriAfter, MSGBOX_AUTOCLOSE
	end

LcUnderseaSprings_EventScript_SpringsSign::
	msgbox LcUnderseaSprings_Text_SpringsSign, MSGBOX_SIGN
	end

LcUnderseaSprings_Text_HoltSeen:
	.string "I brought a boat down a staircase\n"
	.string "to get here. Don't ask.\p"
	.string "Battle me while the water's warm!$"

LcUnderseaSprings_Text_HoltBeaten:
	.string "Sunk in my own harbour.$"

LcUnderseaSprings_Text_HoltAfter:
	.string "The springs never freeze and never\n"
	.string "boil. Same heat, day and night.\p"
	.string "Sailors used to swear this cave was\n"
	.string "breathing. Standing here, I believe it.$"

LcUnderseaSprings_Text_PeriSeen:
	.string "Shh. Listen. That dripping has a\n"
	.string "rhythm to it.\p"
	.string "…Sorry. You want a battle, don't you?$"

LcUnderseaSprings_Text_PeriBeaten:
	.string "You broke the rhythm.$"

LcUnderseaSprings_Text_PeriAfter:
	.string "Water walkers, water divers, and one\n"
	.string "very lost HIKER.\p"
	.string "That's everyone I've met down here\n"
	.string "in three weeks.$"

LcUnderseaSprings_Text_SpringsSign:
	.string "WARM SPRINGS\p"
	.string "“Rest here. The next stretch is\n"
	.string "long and there is no light in it.”$"
