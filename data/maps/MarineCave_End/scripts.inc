MarineCave_End_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, MarineCave_End_OnResume
	map_script MAP_SCRIPT_ON_TRANSITION, MarineCave_End_OnTransition
	.byte 0

MarineCave_End_OnResume:
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, MarineCave_End_EventScript_TryRemoveKyogre
	end

MarineCave_End_EventScript_TryRemoveKyogre::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
	removeobject LOCALID_MARINE_CAVE_KYOGRE
	return

MarineCave_End_OnTransition:
	call_if_unset FLAG_DEFEATED_KYOGRE, MarineCave_End_EventScript_ShowKyogre
	end

MarineCave_End_EventScript_ShowKyogre::
	clearflag FLAG_HIDE_MARINE_CAVE_KYOGRE
	setvar VAR_TEMP_1, 1
	return

MarineCave_End_EventScript_Kyogre::
	lockall
	applymovement LOCALID_PLAYER, Common_Movement_FaceUp
	waitmovement 0
	applymovement LOCALID_MARINE_CAVE_KYOGRE, MarineCave_End_Movement_KyogreApproach
	waitmovement 0
	waitse
	playmoncry SPECIES_KYOGRE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setvar VAR_LAST_TALKED, LOCALID_MARINE_CAVE_KYOGRE
	setwildbattle SPECIES_KYOGRE, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_TEMP_1, 0
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, MarineCave_End_EventScript_DefeatedKyogre
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, MarineCave_End_EventScript_RanFromKyogre
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, MarineCave_End_EventScript_RanFromKyogre
	setvar VAR_SHOULD_END_ABNORMAL_WEATHER, 1
	setflag FLAG_DEFEATED_KYOGRE
	releaseall
	end

MarineCave_End_EventScript_DefeatedKyogre::
	setvar VAR_SHOULD_END_ABNORMAL_WEATHER, 1
	setflag FLAG_DEFEATED_KYOGRE
	goto Common_EventScript_RemoveStaticPokemon
	end

MarineCave_End_EventScript_RanFromKyogre::
	setvar VAR_0x8004, SPECIES_KYOGRE
	goto Common_EventScript_LegendaryFlewAway
	end

MarineCave_End_Movement_KyogreApproach:
	init_affine_anim
	walk_down_start_affine
	delay_16
	delay_16
	walk_down_affine
	delay_16
	delay_16
	walk_down_affine
	step_end

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
MarineCave_End_EventScript_DexPhione::
	lockall
	msgbox MarineCave_End_Text_DexPhioneIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_PHIONE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_PHIONE, 30
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_PHIONE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MarineCave_End_EventScript_DexPhioneSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MarineCave_End_EventScript_DexPhioneSome
	releaseall
	end

MarineCave_End_EventScript_DexPhioneSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_PHIONE
	setflag FLAG_HIDE_DEX_PHIONE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MarineCave_End_Text_DexPhioneIntro:
	.string "PHIONE appeared!$"

MarineCave_End_EventScript_DexManaphy::
	lockall
	msgbox MarineCave_End_Text_DexManaphyIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_MANAPHY, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_MANAPHY, 30
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_MANAPHY
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MarineCave_End_EventScript_DexManaphySome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MarineCave_End_EventScript_DexManaphySome
	releaseall
	end

MarineCave_End_EventScript_DexManaphySome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_MANAPHY
	setflag FLAG_HIDE_DEX_MANAPHY
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MarineCave_End_Text_DexManaphyIntro:
	.string "MANAPHY appeared!$"

MarineCave_End_EventScript_DexKeldeoOrdinary::
	lockall
	msgbox MarineCave_End_Text_DexKeldeoOrdinaryIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_KELDEO_ORDINARY, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_KELDEO_ORDINARY, 30
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_KELDEO_ORDINARY
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MarineCave_End_EventScript_DexKeldeoOrdinarySome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MarineCave_End_EventScript_DexKeldeoOrdinarySome
	releaseall
	end

MarineCave_End_EventScript_DexKeldeoOrdinarySome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_KELDEO_ORDINARY
	setflag FLAG_HIDE_DEX_KELDEO_ORDINARY
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MarineCave_End_Text_DexKeldeoOrdinaryIntro:
	.string "KELDEO_ORDINARY appeared!$"

MarineCave_End_EventScript_DexTapuFini::
	lockall
	msgbox MarineCave_End_Text_DexTapuFiniIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_TAPU_FINI, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_TAPU_FINI, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_TAPU_FINI
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MarineCave_End_EventScript_DexTapuFiniSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MarineCave_End_EventScript_DexTapuFiniSome
	releaseall
	end

MarineCave_End_EventScript_DexTapuFiniSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_TAPU_FINI
	setflag FLAG_HIDE_DEX_TAPU_FINI
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MarineCave_End_Text_DexTapuFiniIntro:
	.string "TAPU_FINI appeared!$"

@ <<< Dex completa <<<
