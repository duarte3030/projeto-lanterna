Route134_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, Route134_OnResume
	.byte 0

Route134_OnResume:
	setdivewarp MAP_UNDERWATER_ROUTE134, 61, 31
	end

Route134_EventScript_Jack::
	trainerbattle_single TRAINER_JACK, Route134_Text_JackIntro, Route134_Text_JackDefeat
	msgbox Route134_Text_JackPostBattle, MSGBOX_AUTOCLOSE
	end

Route134_EventScript_Laurel::
	trainerbattle_single TRAINER_LAUREL, Route134_Text_LaurelIntro, Route134_Text_LaurelDefeat
	msgbox Route134_Text_LaurelPostBattle, MSGBOX_AUTOCLOSE
	end

Route134_EventScript_Alex::
	trainerbattle_single TRAINER_ALEX, Route134_Text_AlexIntro, Route134_Text_AlexDefeat
	msgbox Route134_Text_AlexPostBattle, MSGBOX_AUTOCLOSE
	end

Route134_EventScript_Aaron::
	trainerbattle_single TRAINER_AARON, Route134_Text_AaronIntro, Route134_Text_AaronDefeat
	msgbox Route134_Text_AaronPostBattle, MSGBOX_AUTOCLOSE
	end

Route134_EventScript_Hitoshi::
	trainerbattle_single TRAINER_HITOSHI, Route134_Text_HitoshiIntro, Route134_Text_HitoshiDefeat
	msgbox Route134_Text_HitoshiPostBattle, MSGBOX_AUTOCLOSE
	end

Route134_EventScript_Hudson::
	trainerbattle_single TRAINER_HUDSON, Route134_Text_HudsonIntro, Route134_Text_HudsonDefeat
	msgbox Route134_Text_HudsonPostBattle, MSGBOX_AUTOCLOSE
	end

Route134_EventScript_Reyna::
	trainerbattle_single TRAINER_REYNA, Route134_Text_ReynaIntro, Route134_Text_ReynaDefeat
	msgbox Route134_Text_ReynaPostBattle, MSGBOX_AUTOCLOSE
	end

Route134_EventScript_Marley::
	trainerbattle_single TRAINER_MARLEY, Route134_Text_MarleyIntro, Route134_Text_MarleyDefeat
	msgbox Route134_Text_MarleyPostBattle, MSGBOX_AUTOCLOSE
	end

Route134_EventScript_Kelvin::
	trainerbattle_single TRAINER_KELVIN, Route134_Text_KelvinIntro, Route134_Text_KelvinDefeat
	msgbox Route134_Text_KelvinPostBattle, MSGBOX_AUTOCLOSE
	end


@ Eventos novos do Pokémon Emerald EX (mapa 0.51), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
Route134_EventScript_ExTrainer12::
	trainerbattle_single TRAINER_HOENNEX_ROUTE134_KIRO, Route134_Text_ExTrainer12Intro, Route134_Text_ExTrainer12Defeat
	msgbox Route134_Text_ExTrainer12PostBattle, MSGBOX_AUTOCLOSE
	end

Route134_Text_ExTrainer12Intro:
	.string "It is essential for a ninja to be able to\n"
	.string "swim!$"

Route134_Text_ExTrainer12Defeat:
	.string "Maybe I’m not a true ninja...$"

Route134_Text_ExTrainer12PostBattle:
	.string "I’m scared to get in the water!$"

Route134_EventScript_ExTrainer13::
	trainerbattle_single TRAINER_HOENNEX_ROUTE134_CLETUS, Route134_Text_ExTrainer13Intro, Route134_Text_ExTrainer13Defeat
	msgbox Route134_Text_ExTrainer13PostBattle, MSGBOX_AUTOCLOSE
	end

Route134_Text_ExTrainer13Intro:
	.string "Say kiddo, what’s the fastest route to\n"
	.string "Pacifilog?$"

Route134_Text_ExTrainer13Defeat:
	.string "East, huh?$"

Route134_Text_ExTrainer13PostBattle:
	.string "Now which way is East?$"

