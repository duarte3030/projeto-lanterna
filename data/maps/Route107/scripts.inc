Route107_MapScripts::
	.byte 0

Route107_EventScript_Darrin::
	trainerbattle_single TRAINER_DARRIN, Route107_Text_DarrinIntro, Route107_Text_DarrinDefeated
	msgbox Route107_Text_DarrinPostBattle, MSGBOX_AUTOCLOSE
	end

Route107_EventScript_Tony::
	trainerbattle_single TRAINER_TONY_1, Route107_Text_TonyIntro, Route107_Text_TonyDefeated, Route107_EventScript_TonyRegisterMatchCallAfterBattle
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route107_EventScript_TonyRematch
	msgbox Route107_Text_TonyPostBattle, MSGBOX_DEFAULT
	release
	end

Route107_EventScript_TonyRegisterMatchCallAfterBattle::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox Route107_Text_TonyRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_TONY_1
	release
	end

Route107_EventScript_TonyRematch::
	trainerbattle_rematch TRAINER_TONY_1, Route107_Text_TonyRematchIntro, Route107_Text_TonyRematchDefeated
	msgbox Route107_Text_TonyRematchPostBattle, MSGBOX_AUTOCLOSE
	end

Route107_EventScript_Denise::
	trainerbattle_single TRAINER_DENISE, Route107_Text_DeniseIntro, Route107_Text_DeniseDefeated
	msgbox Route107_Text_DenisePostBattle, MSGBOX_AUTOCLOSE
	end

Route107_EventScript_Beth::
	trainerbattle_single TRAINER_BETH, Route107_Text_BethIntro, Route107_Text_BethDefeated
	msgbox Route107_Text_BethPostBattle, MSGBOX_AUTOCLOSE
	end

Route107_EventScript_Lisa::
	trainerbattle_double TRAINER_LISA_AND_RAY, Route107_Text_LisaIntro, Route107_Text_LisaDefeated, Route107_Text_LisaNotEnoughPokemon
	msgbox Route107_Text_LisaPostBattle, MSGBOX_AUTOCLOSE
	end

Route107_EventScript_Ray::
	trainerbattle_double TRAINER_LISA_AND_RAY, Route107_Text_RayIntro, Route107_Text_RayDefeated, Route107_Text_RayNotEnoughPokemon
	msgbox Route107_Text_RayPostBattle, MSGBOX_AUTOCLOSE
	end

Route107_EventScript_Camron::
	trainerbattle_single TRAINER_CAMRON, Route107_Text_CamronIntro, Route107_Text_CamronDefeated
	msgbox Route107_Text_CamronPostBattle, MSGBOX_AUTOCLOSE
	end


@ Eventos novos do Pokémon Emerald EX (mapa 0.24), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
Route107_EventScript_ExTrainer7::
	trainerbattle_single TRAINER_HOENNEX_ROUTE107_HARISON, Route107_Text_ExTrainer7Intro, Route107_Text_ExTrainer7Defeat
	msgbox Route107_Text_ExTrainer7PostBattle, MSGBOX_AUTOCLOSE
	end

Route107_Text_ExTrainer7Intro:
	.string "Some POKéMON can only be caught with\n"
	.string "nicer FISHING RODS.$"

Route107_Text_ExTrainer7Defeat:
	.string "Haven’t seen a CORSOLA before have ya?$"

Route107_Text_ExTrainer7PostBattle:
	.string "There are lots of POKéMON hiding\n"
	.string "underwater.\p"
	.string "Depending on what FISHING ROD you use,\n"
	.string "different POKéMON can be caught.$"

Route107_EventScript_ExNpc8::
	msgbox Route107_Text_ExNpc8, MSGBOX_NPC
	end

Route107_Text_ExNpc8:
	.string "My daddy takes me out here to fish!\p"
	.string "He looks for rare POKéMON!$"

Route107_EventScript_ExTrainer10::
	trainerbattle_single TRAINER_HOENNEX_ROUTE107_DENNIS, Route107_Text_ExTrainer10Intro, Route107_Text_ExTrainer10Defeat
	msgbox Route107_Text_ExTrainer10PostBattle, MSGBOX_AUTOCLOSE
	end

Route107_Text_ExTrainer10Intro:
	.string "Splish-splash\n"
	.string "Splish-splash\p"
	.string "Hey this is my secret training spot!$"

Route107_Text_ExTrainer10Defeat:
	.string "Splish-splash\n"
	.string "Splish splash\p"
	.string "Wow you’re pretty cool!$"

Route107_Text_ExTrainer10PostBattle:
	.string "Splish-splash\n"
	.string "Splish-splash\p"
	.string "I’m training here to enter a COOL\n"
	.string "CONTEST with my HERACROSS!$"

