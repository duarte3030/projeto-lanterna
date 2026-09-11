@ LcSilverCaveOutside: mapa copiado de Pokémon Liquid Crystal.gba (g3m75) por
@ dev_scripts/copia_mapa_rom.py. A ARTE é do hack; o JOGO (warps, NPCs,
@ encontros, treinadores, placas) é NOSSO e está aqui. Nada do enredo do hack
@ entrou.

LcSilverCaveOutside_MapScripts::
	.byte 0

@ A PORTA da área. O guia é o par do guia de MtSilver_Outside: as duas bocas de
@ caverna daquele mapa estão em patamares que o jogador não alcança (medido:
@ 309 tiles alcançáveis a partir do Centro Pokémon, e nenhum deles encosta em
@ (14,4) nem em (7,15)), então a ligação é warp de script, no molde do
@ marinheiro de PalletTown_Frlg.
LcSilverCaveOutside_EventScript_Guide::
	lock
	faceplayer
	msgbox LcSilverCaveOutside_Text_GuideAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LcSilverCaveOutside_EventScript_GuideNo
	msgbox LcSilverCaveOutside_Text_GuideGo, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	warp MAP_MT_SILVER_OUTSIDE, 24, 17
	waitstate
	release
	end

LcSilverCaveOutside_EventScript_GuideNo::
	msgbox LcSilverCaveOutside_Text_GuideNo, MSGBOX_DEFAULT
	release
	end

LcSilverCaveOutside_EventScript_Norvald::
	trainerbattle_single TRAINER_JOHTO_LC_SILVER_NORVALD, LcSilverCaveOutside_Text_NorvaldSeen, LcSilverCaveOutside_Text_NorvaldBeaten
	msgbox LcSilverCaveOutside_Text_NorvaldAfter, MSGBOX_AUTOCLOSE
	end

LcSilverCaveOutside_EventScript_Sena::
	trainerbattle_single TRAINER_JOHTO_LC_SILVER_SENA, LcSilverCaveOutside_Text_SenaSeen, LcSilverCaveOutside_Text_SenaBeaten
	msgbox LcSilverCaveOutside_Text_SenaAfter, MSGBOX_AUTOCLOSE
	end

LcSilverCaveOutside_EventScript_Ruarc::
	trainerbattle_single TRAINER_JOHTO_LC_SILVER_RUARC, LcSilverCaveOutside_Text_RuarcSeen, LcSilverCaveOutside_Text_RuarcBeaten
	msgbox LcSilverCaveOutside_Text_RuarcAfter, MSGBOX_AUTOCLOSE
	end

LcSilverCaveOutside_EventScript_SignValley::
	msgbox LcSilverCaveOutside_Text_SignValley, MSGBOX_SIGN
	end

LcSilverCaveOutside_Text_GuideAsk:
	.string "Heading back over the ridge to\n"
	.string "MT.SILVER?$"

LcSilverCaveOutside_Text_GuideGo:
	.string "Rope on. Watch the loose stones.$"

LcSilverCaveOutside_Text_GuideNo:
	.string "Suit yourself. The CENTRE is warm\n"
	.string "and the cave is not.$"

LcSilverCaveOutside_Text_NorvaldSeen:
	.string "Not many people find this valley.\n"
	.string "Show me you belong in it!$"

LcSilverCaveOutside_Text_NorvaldBeaten:
	.string "You climbed right over me.$"

LcSilverCaveOutside_Text_NorvaldAfter:
	.string "The ridge cuts the wind off, so the\n"
	.string "grass here grows all year.\p"
	.string "That is why the POKéMON come down\n"
	.string "from the peak to feed.$"

LcSilverCaveOutside_Text_SenaSeen:
	.string "Everything in SILVER CAVE is old\n"
	.string "and strong. Are you?$"

LcSilverCaveOutside_Text_SenaBeaten:
	.string "Older and stronger than me, then.$"

LcSilverCaveOutside_Text_SenaAfter:
	.string "The stream runs out of the cave\n"
	.string "mouth, not into it.\p"
	.string "There is water in there somewhere,\n"
	.string "and a long way down.$"

LcSilverCaveOutside_Text_RuarcSeen:
	.string "The cave mouth is that way. You\n"
	.string "get past me first.$"

LcSilverCaveOutside_Text_RuarcBeaten:
	.string "Go on, then. Mind the dark.$"

LcSilverCaveOutside_Text_RuarcAfter:
	.string "Three levels, and the last one is\n"
	.string "three rooms that don't join up.\p"
	.string "You walk back out the way you\n"
	.string "walked in. Every time.$"

LcSilverCaveOutside_Text_SignValley:
	.string "SILVER CAVE\n"
	.string "Trainers only past this point.\l"
	.string "The mountain does not forgive.$"
