PokemonMansion_B1F_Frlg_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, PokemonMansion_B1F_OnLoad
	.byte 0

PokemonMansion_B1F_OnLoad::
	call_if_set FLAG_POKEMON_MANSION_SWITCH_STATE, PokemonMansion_EventScript_PressSwitch_B1F
	end

PokemonMansion_B1F_EventScript_Statue::
	lockall
	setvar VAR_0x8004, 3
	call PokemonMansion_EventScript_SecretSwitch
	playse SE_UNLOCK
	special DrawWholeMapView
	waitse
	releaseall
	end

PokemonMansion_B1F_EventScript_DiarySep1st::
	msgbox PokemonMansion_B1F_Text_MewtwoIsFarTooPowerful, MSGBOX_SIGN
	end

PokemonMansion_B1F_EventScript_Lewis::
	trainerbattle_single TRAINER_BURGLAR_LEWIS, PokemonMansion_B1F_Text_LewisIntro, PokemonMansion_B1F_Text_LewisDefeat
	msgbox PokemonMansion_B1F_Text_LewisPostBattle, MSGBOX_AUTOCLOSE
	end

PokemonMansion_B1F_EventScript_Ivan::
	trainerbattle_single TRAINER_SCIENTIST_IVAN, PokemonMansion_B1F_Text_IvanIntro, PokemonMansion_B1F_Text_IvanDefeat
	msgbox PokemonMansion_B1F_Text_IvanPostBattle, MSGBOX_AUTOCLOSE
	end

PokemonMansion_B1F_Text_LewisIntro::
	.string "Uh-oh…\n"
	.string "Where am I now?$"

PokemonMansion_B1F_Text_LewisDefeat::
	.string "Awooh!$"

PokemonMansion_B1F_Text_LewisPostBattle::
	.string "You can find stuff lying around.\n"
	.string "The residents must've left them.$"

PokemonMansion_B1F_Text_IvanIntro::
	.string "This place is ideal for a lab.\n"
	.string "Look at all this space.$"

PokemonMansion_B1F_Text_IvanDefeat::
	.string "What was that for?$"

PokemonMansion_B1F_Text_IvanPostBattle::
	.string "I like it here.\n"
	.string "It's conducive to my studies.$"

PokemonMansion_B1F_Text_MewtwoIsFarTooPowerful::
	.string "Diary: Sept. 1\n"
	.string "MEWTWO is far too powerful.\p"
	.string "We have failed to curb its vicious\n"
	.string "tendencies…$"

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
PokemonMansion_B1F_Frlg_EventScript_DexGenesect::
	lockall
	msgbox PokemonMansion_B1F_Frlg_Text_DexGenesectIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_GENESECT, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_GENESECT, 65
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_GENESECT
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, PokemonMansion_B1F_Frlg_EventScript_DexGenesectSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, PokemonMansion_B1F_Frlg_EventScript_DexGenesectSome
	releaseall
	end

PokemonMansion_B1F_Frlg_EventScript_DexGenesectSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GENESECT
	setflag FLAG_HIDE_DEX_GENESECT
	fadescreenswapbuffers FADE_FROM_BLACK
	return

PokemonMansion_B1F_Frlg_Text_DexGenesectIntro:
	.string "GENESECT appeared!$"

@ <<< Dex completa <<<
