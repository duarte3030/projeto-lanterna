@ LcSilverCaveEntrance: mapa copiado de Pokémon Liquid Crystal.gba (g4m98) por
@ dev_scripts/copia_mapa_rom.py. A ARTE é do hack; o JOGO é NOSSO.

LcSilverCaveEntrance_MapScripts::
	.byte 0

LcSilverCaveEntrance_EventScript_Bergen::
	trainerbattle_single TRAINER_JOHTO_LC_SILVER_BERGEN, LcSilverCaveEntrance_Text_BergenSeen, LcSilverCaveEntrance_Text_BergenBeaten
	msgbox LcSilverCaveEntrance_Text_BergenAfter, MSGBOX_AUTOCLOSE
	end

LcSilverCaveEntrance_EventScript_Halvar::
	trainerbattle_single TRAINER_JOHTO_LC_SILVER_HALVAR, LcSilverCaveEntrance_Text_HalvarSeen, LcSilverCaveEntrance_Text_HalvarBeaten
	msgbox LcSilverCaveEntrance_Text_HalvarAfter, MSGBOX_AUTOCLOSE
	end

LcSilverCaveEntrance_EventScript_Isolde::
	trainerbattle_single TRAINER_JOHTO_LC_SILVER_ISOLDE, LcSilverCaveEntrance_Text_IsoldeSeen, LcSilverCaveEntrance_Text_IsoldeBeaten
	msgbox LcSilverCaveEntrance_Text_IsoldeAfter, MSGBOX_AUTOCLOSE
	end

LcSilverCaveEntrance_EventScript_SignEntrance::
	msgbox LcSilverCaveEntrance_Text_SignEntrance, MSGBOX_SIGN
	end

LcSilverCaveEntrance_Text_BergenSeen:
	.string "First level, and you're already\n"
	.string "out of daylight. Good.$"

LcSilverCaveEntrance_Text_BergenBeaten:
	.string "Down I go, then.$"

LcSilverCaveEntrance_Text_BergenAfter:
	.string "The floor slopes up all the way to\n"
	.string "the north door.\p"
	.string "Everything that falls in here ends\n"
	.string "up back at the mouth eventually.$"

LcSilverCaveEntrance_Text_HalvarSeen:
	.string "Lost? Everyone is, the first time.$"

LcSilverCaveEntrance_Text_HalvarBeaten:
	.string "You knew exactly where you were\n"
	.string "going.$"

LcSilverCaveEntrance_Text_HalvarAfter:
	.string "Count the ledges, not the turns.\n"
	.string "The turns lie to you.$"

LcSilverCaveEntrance_Text_IsoldeSeen:
	.string "I hear the mountain from here.\n"
	.string "You will not like what it says.$"

LcSilverCaveEntrance_Text_IsoldeBeaten:
	.string "It said your name. I should have\n"
	.string "listened.$"

LcSilverCaveEntrance_Text_IsoldeAfter:
	.string "There is running water two levels\n"
	.string "down, and it is warm.\p"
	.string "Warm water under a snow peak.\n"
	.string "Think about that.$"

LcSilverCaveEntrance_Text_SignEntrance:
	.string "SILVER CAVE, FIRST LEVEL\n"
	.string "One way up, one way back.\l"
	.string "Rope and a lamp, or turn around.$"
