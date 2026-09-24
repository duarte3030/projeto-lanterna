@ Route136: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 0.60) por dev_scripts/copia_planta_ex.py.

Route136_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 0.60), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
Route136_EventScript_ExTrainer0::
	trainerbattle_single TRAINER_HOENNEX_ROUTE136_SEBASTIAN, Route136_Text_ExTrainer0Intro, Route136_Text_ExTrainer0Defeat
	msgbox Route136_Text_ExTrainer0PostBattle, MSGBOX_AUTOCLOSE
	end

Route136_Text_ExTrainer0Intro:
	.string "How many FLYING TYPES can you name?$"

Route136_Text_ExTrainer0Defeat:
	.string "Holy Ho-Oh!$"

Route136_Text_ExTrainer0PostBattle:
	.string "You wanna know how many FLYING TYPES\n"
	.string "there are!?\p"
	.string "Let’s see, SWABLU, SKARMORY, STARLY...\p"
	.string "(He seems like he’ll be at it for a while.)$"

Route136_EventScript_ExTrainer1::
	trainerbattle_single TRAINER_HOENNEX_ROUTE136_SER, Route136_Text_ExTrainer1Intro, Route136_Text_ExTrainer1Defeat
	msgbox Route136_Text_ExTrainer1PostBattle, MSGBOX_AUTOCLOSE
	end

Route136_Text_ExTrainer1Intro:
	.string "Well looky here...\n"
	.string "What POKéMON do you have?$"

Route136_Text_ExTrainer1Defeat:
	.string "My precious POKéMON!$"

Route136_Text_ExTrainer1PostBattle:
	.string "Your POKéMON were way too strong!$"

Route136_EventScript_ExTrainer2::
	trainerbattle_single TRAINER_HOENNEX_ROUTE136_LOO, Route136_Text_ExTrainer2Intro, Route136_Text_ExTrainer2Defeat
	msgbox Route136_Text_ExTrainer2PostBattle, MSGBOX_AUTOCLOSE
	end

Route136_Text_ExTrainer2Intro:
	.string "How about a POKéMON showcase!$"

Route136_Text_ExTrainer2Defeat:
	.string "Oh no!\n"
	.string "My babies...$"

Route136_Text_ExTrainer2PostBattle:
	.string "My favorite part of battle is showing\n"
	.string "off my POKéMON.\p"
	.string "I think I might try to enter a CONTEST\n"
	.string "to show them off even more!$"

Route136_EventScript_ExTrainer3::
	trainerbattle_single TRAINER_HOENNEX_ROUTE136_RORRI, Route136_Text_ExTrainer3Intro, Route136_Text_ExTrainer3Defeat
	msgbox Route136_Text_ExTrainer3PostBattle, MSGBOX_AUTOCLOSE
	end

Route136_Text_ExTrainer3Intro:
	.string "Hey!\n"
	.string "Watch where you’re going!$"

Route136_Text_ExTrainer3Defeat:
	.string "You almost tripped back there!$"

Route136_Text_ExTrainer3PostBattle:
	.string "If you don’t want to get lost,\n"
	.string "keep an eye on the road ahead$"

Route136_EventScript_ExTrainer4::
	trainerbattle_single TRAINER_HOENNEX_ROUTE136_SIDNEY, Route136_Text_ExTrainer4Intro, Route136_Text_ExTrainer4Defeat
	msgbox Route136_Text_ExTrainer4PostBattle, MSGBOX_AUTOCLOSE
	end

Route136_Text_ExTrainer4Intro:
	.string "Can you imagine a world without\n"
	.string "POKéMON?$"

Route136_Text_ExTrainer4Defeat:
	.string "Sieze the day!$"

Route136_Text_ExTrainer4PostBattle:
	.string "Can you imagine a world without\n"
	.string "POKéMON?\n"
	.string "I bet there might still be adventure.$"

Route136_EventScript_ExTrainer5::
	trainerbattle_single TRAINER_HOENNEX_ROUTE136_DONATELLO, Route136_Text_ExTrainer5Intro, Route136_Text_ExTrainer5Defeat
	msgbox Route136_Text_ExTrainer5PostBattle, MSGBOX_AUTOCLOSE
	end

Route136_Text_ExTrainer5Intro:
	.string "How’d you find me back here?$"

Route136_Text_ExTrainer5Defeat:
	.string "I come back here to get away from my\n"
	.string "family.$"

Route136_Text_ExTrainer5PostBattle:
	.string "Does your family ever annoy you?$"

Route136_EventScript_ExTrainer6::
	trainerbattle_single TRAINER_HOENNEX_ROUTE136_RAPHAEL, Route136_Text_ExTrainer6Intro, Route136_Text_ExTrainer6Defeat
	msgbox Route136_Text_ExTrainer6PostBattle, MSGBOX_AUTOCLOSE
	end

Route136_Text_ExTrainer6Intro:
	.string "If you beat me, I’ll tell you a story.$"

Route136_Text_ExTrainer6Defeat:
	.string "You still wanna hear a story?$"

Route136_Text_ExTrainer6PostBattle:
	.string "In another REGION theres a FLYING TYPE\n"
	.string "POKéMON that, whenever it awakens,\l"
	.string "drains the life energy of anything\l"
	.string "around it!\p"
	.string "It’s said it once powered a great\n"
	.string "weapon.$"

Route136_EventScript_ExNpc8::
	msgbox Route136_Text_ExNpc8, MSGBOX_NPC
	end

Route136_Text_ExNpc8:
	.string "These hills are a great place to stop\n"
	.string "and relax.$"

Route136_EventScript_ExNpc9::
	msgbox Route136_Text_ExNpc9, MSGBOX_NPC
	end

Route136_Text_ExNpc9:
	.string "One day I’m going to be a POKéMON\n"
	.string "TRAINER!$"

Route136_EventScript_ExSign2::
	msgbox Route136_Text_ExSign2, MSGBOX_SIGN
	end

Route136_Text_ExSign2:
	.string "TRAINER TIPS\p"
	.string "Different types of POKéBALLS are\n"
	.string "better at catching certain types of\l"
	.string "POKéMON.$"

