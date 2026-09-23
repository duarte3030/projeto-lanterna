@ LcCinnabarVolcanoVent: mapa copiado de Pokémon Liquid Crystal.gba (g5m44) por
@ dev_scripts/copia_mapa_rom.py. A ARTE e do hack; o JOGO (warps, NPCs,
@ encontros, treinadores, placas) e nosso e entra aqui.
@
@ A camara de cinzas fica ATRAS da porta de (20,7) da cratera. O unico tile de
@ warp desta planta e o (8,30), MB_SOUTH_ARROW_WARP, e ele volta para aquela
@ porta: uma porta, uma volta, que e a regra 0 do valida_conectividade.py.

LcCinnabarVolcanoVent_MapScripts::
	.byte 0

@ ---------------------------------------------------------------- treinadores

LcCinnabarVolcanoVent_EventScript_SuperNerdShaft::
	trainerbattle_single TRAINER_KANTO_LC_VOLCANO_VENT_SCIENTIST, LcCinnabarVolcanoVent_Text_ScientistSeen, LcCinnabarVolcanoVent_Text_ScientistBeaten
	msgbox LcCinnabarVolcanoVent_Text_ScientistAfter, MSGBOX_AUTOCLOSE
	end

LcCinnabarVolcanoVent_EventScript_HikerShaft::
	trainerbattle_single TRAINER_KANTO_LC_VOLCANO_VENT_HIKER, LcCinnabarVolcanoVent_Text_HikerSeen, LcCinnabarVolcanoVent_Text_HikerBeaten
	msgbox LcCinnabarVolcanoVent_Text_HikerAfter, MSGBOX_AUTOCLOSE
	end

@ ---------------------------------------------------------------- gente e placas

LcCinnabarVolcanoVent_EventScript_AshWatcher::
	msgbox LcCinnabarVolcanoVent_Text_AshWatcher, MSGBOX_NPC
	end

LcCinnabarVolcanoVent_EventScript_SignMouth::
	msgbox LcCinnabarVolcanoVent_Text_SignMouth, MSGBOX_SIGN
	end

LcCinnabarVolcanoVent_EventScript_SignAshBed::
	msgbox LcCinnabarVolcanoVent_Text_SignAshBed, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- textos

LcCinnabarVolcanoVent_Text_ScientistSeen:
	.string "Don't touch the samples!\n"
	.string "Battle me instead.$"

LcCinnabarVolcanoVent_Text_ScientistBeaten:
	.string "My readings say I lost.$"

LcCinnabarVolcanoVent_Text_ScientistAfter:
	.string "The ash in this shaft is older\n"
	.string "than the town below.\p"
	.string "Sift it and you find shells. This\n"
	.string "was seabed once.$"

LcCinnabarVolcanoVent_Text_HikerSeen:
	.string "Nobody climbs my shaft without\n"
	.string "earning it!$"

LcCinnabarVolcanoVent_Text_HikerBeaten:
	.string "Earned, then. Go on up.$"

LcCinnabarVolcanoVent_Text_HikerAfter:
	.string "Watch the loose stones. They roll\n"
	.string "quiet and they roll fast.$"

LcCinnabarVolcanoVent_Text_AshWatcher:
	.string "I walk up here every morning.\p"
	.string "When the ash is warm underfoot,\n"
	.string "I go straight back down and tell\l"
	.string "the LAB. It has been cold for\l"
	.string "years now.$"

LcCinnabarVolcanoVent_Text_SignMouth:
	.string "ASH CHAMBER\n"
	.string "Back down the steps for the\l"
	.string "crater.$"

LcCinnabarVolcanoVent_Text_SignAshBed:
	.string "The ash bed. Soft going, and\n"
	.string "something always stirs in it.$"
