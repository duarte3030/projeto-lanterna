Route105_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Route105_OnLoad
	map_script MAP_SCRIPT_ON_TRANSITION, Route105_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Route105_OnFrame
	.byte 0

Route105_OnLoad:
	call_if_unset FLAG_REGI_DOORS_OPENED, Route105_CloseRegiEntrance
	call_if_eq VAR_ABNORMAL_WEATHER_LOCATION, ABNORMAL_WEATHER_ROUTE_105_NORTH, AbnormalWeather_EventScript_PlaceTilesRoute105North
	call_if_eq VAR_ABNORMAL_WEATHER_LOCATION, ABNORMAL_WEATHER_ROUTE_105_SOUTH, AbnormalWeather_EventScript_PlaceTilesRoute105South
	end

Route105_CloseRegiEntrance::
	setmetatile 9, 19, METATILE_General_RockWall_RockBase, TRUE
	setmetatile 9, 20, METATILE_General_RockWall_SandBase, TRUE
	return

Route105_OnTransition:
	call_if_eq VAR_SHOULD_END_ABNORMAL_WEATHER, 1, AbnormalWeather_EventScript_HideMapNamePopup
	call_if_eq VAR_ABNORMAL_WEATHER_LOCATION, ABNORMAL_WEATHER_ROUTE_105_NORTH, AbnormalWeather_StartKyogreWeather
	call_if_eq VAR_ABNORMAL_WEATHER_LOCATION, ABNORMAL_WEATHER_ROUTE_105_SOUTH, AbnormalWeather_StartKyogreWeather
	end

Route105_OnFrame:
	map_script_2 VAR_SHOULD_END_ABNORMAL_WEATHER, 1, AbnormalWeather_EventScript_EndEventAndCleanup_1
	.2byte 0

Route105_EventScript_Foster::
	trainerbattle_single TRAINER_FOSTER, Route105_Text_FosterIntro, Route105_Text_FosterDefeated
	msgbox Route105_Text_FosterPostBattle, MSGBOX_AUTOCLOSE
	end

Route105_EventScript_Luis::
	trainerbattle_single TRAINER_LUIS, Route105_Text_LuisIntro, Route105_Text_LuisDefeated
	msgbox Route105_Text_LuisPostBattle, MSGBOX_AUTOCLOSE
	end

Route105_EventScript_Dominik::
	trainerbattle_single TRAINER_DOMINIK, Route105_Text_DominikIntro, Route105_Text_DominikDefeated
	msgbox Route105_Text_DominikPostBattle, MSGBOX_AUTOCLOSE
	end

Route105_EventScript_Beverly::
	trainerbattle_single TRAINER_BEVERLY, Route105_Text_BeverlyIntro, Route105_Text_BeverlyDefeated
	msgbox Route105_Text_PostBattle, MSGBOX_AUTOCLOSE
	end

Route105_EventScript_Imani::
	trainerbattle_single TRAINER_IMANI, Route105_Text_ImaniIntro, Route105_Text_ImaniDefeated
	msgbox Route105_Text_ImaniPostBattle, MSGBOX_AUTOCLOSE
	end

Route105_EventScript_Josue::
	trainerbattle_single TRAINER_JOSUE, Route105_Text_JosueIntro, Route105_Text_JosueDefeated
	msgbox Route105_Text_JosuePostBattle, MSGBOX_AUTOCLOSE
	end

Route105_EventScript_Andres::
	trainerbattle_single TRAINER_ANDRES_1, Route105_Text_AndresIntro, Route105_Text_AndresDefeated, Route105_EventScript_AndresRegisterMatchCallAfterBattle
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route105_EventScript_AndresRematch
	msgbox Route105_Text_AndresPostBattle, MSGBOX_DEFAULT
	release
	end

Route105_EventScript_AndresRegisterMatchCallAfterBattle::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox Route105_Text_AndresRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_ANDRES_1
	release
	end

Route105_EventScript_AndresRematch::
	trainerbattle_rematch TRAINER_ANDRES_1, Route105_Text_AndresRematchIntro, Route105_Text_AndresRematchDefeated
	msgbox Route105_Text_AndresRematchPostBattle, MSGBOX_AUTOCLOSE
	end

Route104_Text_DadPokenavCall:
	.string "… … … … … …\n"
	.string "… … … … … Beep!\p"
	.string "DAD: Oh, {PLAYER}?\p"
	.string "… … … … … …\n"
	.string "Where are you now?\l"
	.string "It sounds windy wherever you are.\p"
	.string "I just heard from DEVON's MR. STONE\n"
	.string "about your POKéNAV, so I decided\l"
	.string "to give you a call.\p"
	.string "It sounds like you're doing fine,\n"
	.string "so that's fine with me.\p"
	.string "You take care now.\p"
	.string "… … … … … …\n"
	.string "… … … … … Click!$"

Route104_Text_RegisteredDadInPokenav:
	.string "Registered DAD NORMAN\n"
	.string "in the POKéNAV.$"

@ Eventos novos do Pokémon Emerald EX (mapa 0.22), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
Route105_EventScript_ExTrainer8::
	trainerbattle_single TRAINER_HOENNEX_ROUTE105_ROSIE, Route105_Text_ExTrainer8Intro, Route105_Text_ExTrainer8Defeat
	msgbox Route105_Text_ExTrainer8PostBattle, MSGBOX_AUTOCLOSE
	end

Route105_Text_ExTrainer8Intro:
	.string "I’m training for the IRON MON!$"

Route105_Text_ExTrainer8Defeat:
	.string "Wow!\n"
	.string "Clearly I need to train more!$"

Route105_Text_ExTrainer8PostBattle:
	.string "What are you training for?$"

Route105_EventScript_ExTrainer9::
	trainerbattle_single TRAINER_HOENNEX_ROUTE105_JOSHUA, Route105_Text_ExTrainer9Intro, Route105_Text_ExTrainer9Defeat
	msgbox Route105_Text_ExTrainer9PostBattle, MSGBOX_AUTOCLOSE
	end

Route105_Text_ExTrainer9Intro:
	.string "I’m so tired of treading water...$"

Route105_Text_ExTrainer9Defeat:
	.string "I genuinely need help!$"

Route105_Text_ExTrainer9PostBattle:
	.string "I don’t know much longer I can stay\n"
	.string "afloat...$"

Route105_EventScript_ExTrainer10::
	trainerbattle_single TRAINER_HOENNEX_ROUTE105_TAYLOR, Route105_Text_ExTrainer10Intro, Route105_Text_ExTrainer10Defeat
	msgbox Route105_Text_ExTrainer10PostBattle, MSGBOX_AUTOCLOSE
	end

Route105_Text_ExTrainer10Intro:
	.string "The guy i’m swimming with such a baby!$"

Route105_Text_ExTrainer10Defeat:
	.string "Wow you’re good!$"

Route105_Text_ExTrainer10PostBattle:
	.string "I like your POKémMON!$"

Route105_EventScript_ExTrainer11::
	trainerbattle_single TRAINER_HOENNEX_ROUTE105_KENDALL, Route105_Text_ExTrainer11Intro, Route105_Text_ExTrainer11Defeat
	msgbox Route105_Text_ExTrainer11PostBattle, MSGBOX_AUTOCLOSE
	end

Route105_Text_ExTrainer11Intro:
	.string "What a nice beach for a BBQ!$"

Route105_Text_ExTrainer11Defeat:
	.string "Hot stuff!$"

Route105_Text_ExTrainer11PostBattle:
	.string "Man, I could sure use some BBQ!$"

