@ FrozenHeights: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 27.118) por dev_scripts/copia_planta_ex.py.

FrozenHeights_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 27.118), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
FrozenHeights_EventScript_ExTrainer1::
	trainerbattle_single TRAINER_HOENNEX_FROZEN_HEIGHTS_ARCADIAN, FrozenHeights_Text_ExTrainer1Intro, FrozenHeights_Text_ExTrainer1Defeat
	msgbox FrozenHeights_Text_ExTrainer1PostBattle, MSGBOX_AUTOCLOSE
	end

FrozenHeights_Text_ExTrainer1Intro:
	.string "Prepare for my icy DRAGONS!$"

FrozenHeights_Text_ExTrainer1Defeat:
	.string "DRAGONS are weak to ICE ATTACKS!$"

FrozenHeights_Text_ExTrainer1PostBattle:
	.string "Supposedly there are even stronger ICE\n"
	.string "DRAGON TYPES in the UNOVA REGION.$"

FrozenHeights_EventScript_ExTrainer2::
	trainerbattle_single TRAINER_HOENNEX_FROZEN_HEIGHTS_PERCY, FrozenHeights_Text_ExTrainer2Intro, FrozenHeights_Text_ExTrainer2Defeat
	msgbox FrozenHeights_Text_ExTrainer2PostBattle, MSGBOX_AUTOCLOSE
	end

FrozenHeights_Text_ExTrainer2Intro:
	.string "Brrrrrrrr.\n"
	.string "It’s c-c-cold up here.$"

FrozenHeights_Text_ExTrainer2Defeat:
	.string "Say that warmed be up!$"

FrozenHeights_Text_ExTrainer2PostBattle:
	.string "Oh boy.\n"
	.string "I sh-should of brought gloves!$"

FrozenHeights_EventScript_ExTrainer3::
	trainerbattle_single TRAINER_HOENNEX_FROZEN_HEIGHTS_HAROLD, FrozenHeights_Text_ExTrainer3Intro, FrozenHeights_Text_ExTrainer3Defeat
	msgbox FrozenHeights_Text_ExTrainer3PostBattle, MSGBOX_AUTOCLOSE
	end

FrozenHeights_Text_ExTrainer3Intro:
	.string "I’m studying some ancient ruins.$"

FrozenHeights_Text_ExTrainer3Defeat:
	.string "I was distracted by a clue, that is all!$"

FrozenHeights_Text_ExTrainer3PostBattle:
	.string "There’s something strange about these\n"
	.string "rocks...$"

FrozenHeights_EventScript_ExNpc4::
	msgbox FrozenHeights_Text_ExNpc4, MSGBOX_NPC
	end

FrozenHeights_Text_ExNpc4:
	.string "The HOENN region is so hot normally.\n"
	.string "I love staying up here in the cold.\l"
	.string "Maybe I should move to SINNOH.$"

FrozenHeights_EventScript_ExNpc5::
	msgbox FrozenHeights_Text_ExNpc5, MSGBOX_NPC
	end

FrozenHeights_Text_ExNpc5:
	.string "There are BERGMITE floating in the\n"
	.string "pond.\p"
	.string "I’d bet you could catch em with a\n"
	.string "FISHING ROD.$"

FrozenHeights_EventScript_ExSign0::
	msgbox FrozenHeights_Text_ExSign0, MSGBOX_SIGN
	end

FrozenHeights_Text_ExSign0:
	.string "FROZEN HEIGHTS\p"
	.string "“HOENN’S crown!”$"

