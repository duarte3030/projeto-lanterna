Route122_MapScripts::
	.byte 0


@ Eventos novos do Pokémon Emerald EX (mapa 0.39), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
Route122_EventScript_ExTrainer0::
	trainerbattle_single TRAINER_HOENNEX_ROUTE122_SERENA, Route122_Text_ExTrainer0Intro, Route122_Text_ExTrainer0Defeat
	msgbox Route122_Text_ExTrainer0PostBattle, MSGBOX_AUTOCLOSE
	end

Route122_Text_ExTrainer0Intro:
	.string "Why are you in my garden!?$"

Route122_Text_ExTrainer0Defeat:
	.string "Jeepers!$"

Route122_Text_ExTrainer0PostBattle:
	.string "I Keep a supply of herbs for the BASE\n"
	.string "CAMP.$"

Route122_EventScript_ExTrainer1::
	trainerbattle_single TRAINER_HOENNEX_ROUTE122_CLAIRA, Route122_Text_ExTrainer1Intro, Route122_Text_ExTrainer1Defeat
	msgbox Route122_Text_ExTrainer1PostBattle, MSGBOX_AUTOCLOSE
	end

Route122_Text_ExTrainer1Intro:
	.string "MT. PYRE drew us all here.\p"
	.string "What’s drawing you here?$"

Route122_Text_ExTrainer1Defeat:
	.string "Interesting.$"

Route122_Text_ExTrainer1PostBattle:
	.string "This town isn’t an official town.\p"
	.string "You should expect to get challenged to\n"
	.string "battle.$"

Route122_EventScript_ExTrainer2::
	trainerbattle_single TRAINER_HOENNEX_ROUTE122_NEIL, Route122_Text_ExTrainer2Intro, Route122_Text_ExTrainer2Defeat
	msgbox Route122_Text_ExTrainer2PostBattle, MSGBOX_AUTOCLOSE
	end

Route122_Text_ExTrainer2Intro:
	.string "I caught a strange one in the SAFARI\n"
	.string "ZONE.$"

Route122_Text_ExTrainer2Defeat:
	.string "Very... Fishy...$"

Route122_Text_ExTrainer2PostBattle:
	.string "I wonder how to catch more\n"
	.string "BASCULEGION.$"

Route122_EventScript_ExNpc4::
	msgbox Route122_Text_ExNpc4, MSGBOX_NPC
	end

Route122_Text_ExNpc4:
	.string "I’m here to visit my FLAAFY on MT. PYRE.\p"
	.string "But.. It’s hard, ya know?$"

Route122_EventScript_ExSign1::
	msgbox Route122_Text_ExSign1, MSGBOX_SIGN
	end

Route122_Text_ExSign1:
	.string "MT. PYRE BASE CAMP\n"
	.string "Come in and be healed.$"

