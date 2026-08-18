Route202_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
Route202_EventScript_CoordEvent_CatchingTutorial::
	@ TODO S3: cena da fonte, rotulo Route202_CoordEvent_CatchingTutorial
	end

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

Route202_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_YOUNGSTER_TRISTAN, Route202_Text_Trainer1Intro, Route202_Text_Trainer1Defeat
	msgbox Route202_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route202_Text_Trainer1Intro:
	.string "You're a Pokémon Trainer, and so am I!\n"
	.string "Our eyes met, so battle we must!$"

Route202_Text_Trainer1Defeat:
	.string "Too strong!\n"
	.string "Too strong!$"

Route202_Text_Trainer1Post:
	.string "Don't be shy about talking to\n"
	.string "Trainers you'd like to battle.\pPokémon grow stronger and stronger\n"
	.string "from battling.$"

Route202_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_LASS_NATALIE, Route202_Text_Trainer2Intro, Route202_Text_Trainer2Defeat
	msgbox Route202_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route202_Text_Trainer2Intro:
	.string "I spy, with my little eye...\n"
	.string "A Trainer!\pA battle, please!$"

Route202_Text_Trainer2Defeat:
	.string "Oh, boo!\n"
	.string "I can't win!$"

Route202_Text_Trainer2Post:
	.string "My Pokémon are all tuckered out!\n"
	.string "I need to go to a Pokémon Center!$"

Route202_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_YOUNGSTER_LOGAN, Route202_Text_Trainer3Intro, Route202_Text_Trainer3Defeat
	msgbox Route202_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route202_Text_Trainer3Intro:
	.string "Let's have a Pokémon battle!\n"
	.string "Humph! But I'm gonna win!$"

Route202_Text_Trainer3Defeat:
	.string "You beat me?!\n"
	.string "You've got talent!$"

Route202_Text_Trainer3Post:
	.string "It was fun battling!\n"
	.string "Yup! I'm going to battle everyone!$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route202_EventScript_Placa1::
	msgbox Route202_Text_Placa1, MSGBOX_SIGN
	end

Route202_Text_Placa1:
	.string "Rt. 202\nSandgem Town$"

Route202_EventScript_Placa2::
	msgbox Route202_Text_Placa2, MSGBOX_SIGN
	end

Route202_Text_Placa2:
	.string "Rt. 202\nJubilife City$"

Route202_EventScript_Placa3::
	msgbox Route202_Text_Placa3, MSGBOX_SIGN
	end

Route202_Text_Placa3:
	.string "Trainer Tips!\pAll Pokémon that are involved in\na battle earn Exp. Points!\pThe more your Pokémon battle,\nthe stronger they will become.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route202_EventScript_Npc1::
	msgbox Route202_Text_Npc1, MSGBOX_NPC
	end

Route202_Text_Npc1:
	.string "Some Pokémon only appear in the\nmorning.\pSome only come out at night.\pI'll keep looking till I've seen them\nall!$"
