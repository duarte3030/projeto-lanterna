@ HauntedWoods: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 27.114) por dev_scripts/copia_planta_ex.py.

HauntedWoods_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 27.114), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
HauntedWoods_EventScript_ExTrainer3::
	trainerbattle_single TRAINER_HOENNEX_HAUNTED_WOODS_BRUCE, HauntedWoods_Text_ExTrainer3Intro, HauntedWoods_Text_ExTrainer3Defeat
	msgbox HauntedWoods_Text_ExTrainer3PostBattle, MSGBOX_AUTOCLOSE
	end

HauntedWoods_Text_ExTrainer3Intro:
	.string "This was a terrible place to train!$"

HauntedWoods_Text_ExTrainer3Defeat:
	.string "These wild GHOST POKéMON are too\n"
	.string "strong!$"

HauntedWoods_Text_ExTrainer3PostBattle:
	.string "My FIGHTING TYPE POKéMON can’t even\n"
	.string "hit these GHOSTs!$"

HauntedWoods_EventScript_ExTrainer4::
	trainerbattle_single TRAINER_HOENNEX_HAUNTED_WOODS_TYLER, HauntedWoods_Text_ExTrainer4Intro, HauntedWoods_Text_ExTrainer4Defeat
	msgbox HauntedWoods_Text_ExTrainer4PostBattle, MSGBOX_AUTOCLOSE
	end

HauntedWoods_Text_ExTrainer4Intro:
	.string "I can’t see a thing in this fog.$"

HauntedWoods_Text_ExTrainer4Defeat:
	.string "Hey not fair!$"

HauntedWoods_Text_ExTrainer4PostBattle:
	.string "This fog must be coming from the river\n"
	.string "near by.$"

HauntedWoods_EventScript_ExTrainer5::
	trainerbattle_single TRAINER_HOENNEX_HAUNTED_WOODS_SHIELE, HauntedWoods_Text_ExTrainer5Intro, HauntedWoods_Text_ExTrainer5Defeat
	msgbox HauntedWoods_Text_ExTrainer5PostBattle, MSGBOX_AUTOCLOSE
	end

HauntedWoods_Text_ExTrainer5Intro:
	.string "Prepare to face the power of the mind!$"

HauntedWoods_Text_ExTrainer5Defeat:
	.string "Wow, you’re super strong.$"

HauntedWoods_Text_ExTrainer5PostBattle:
	.string "Have you heard about the PSYCHIC\n"
	.string "TWINs that live on the other side of\l"
	.string "the region?\p"
	.string "I hope to meet them some day.$"

HauntedWoods_EventScript_ExTrainer6::
	trainerbattle_single TRAINER_HOENNEX_HAUNTED_WOODS_DEBRA, HauntedWoods_Text_ExTrainer6Intro, HauntedWoods_Text_ExTrainer6Defeat
	msgbox HauntedWoods_Text_ExTrainer6PostBattle, MSGBOX_AUTOCLOSE
	end

HauntedWoods_Text_ExTrainer6Intro:
	.string "These WOODS are infested with GHOST\n"
	.string "POKéMON.$"

HauntedWoods_Text_ExTrainer6Defeat:
	.string "I sense much sadness here.$"

HauntedWoods_Text_ExTrainer6PostBattle:
	.string "Take heed traveler, GHOST TYPEs can be\n"
	.string "tricky.$"

HauntedWoods_EventScript_ExTrainer7::
	trainerbattle_single TRAINER_HOENNEX_HAUNTED_WOODS_SARAH, HauntedWoods_Text_ExTrainer7Intro, HauntedWoods_Text_ExTrainer7Defeat
	msgbox HauntedWoods_Text_ExTrainer7PostBattle, MSGBOX_AUTOCLOSE
	end

HauntedWoods_Text_ExTrainer7Intro:
	.string "Not all ghosts are scary!\p"
	.string "See look at my VULPIX$"

HauntedWoods_Text_ExTrainer7Defeat:
	.string "My VULPIX is cute!$"

HauntedWoods_Text_ExTrainer7PostBattle:
	.string "Not all ghosts are scary,\n"
	.string "but at the same time not all GHOSTS are\l"
	.string "cute.$"

