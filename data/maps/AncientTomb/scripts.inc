AncientTomb_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, AncientTomb_OnResume
	map_script MAP_SCRIPT_ON_LOAD, AncientTomb_OnLoad
	map_script MAP_SCRIPT_ON_TRANSITION, AncientTomb_OnTransition
	.byte 0

AncientTomb_OnResume:
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, AncientTomb_EventScript_TryRemoveRegisteel
	end

AncientTomb_EventScript_TryRemoveRegisteel::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
	removeobject VAR_LAST_TALKED
	return

AncientTomb_OnTransition:
	setflag FLAG_LANDMARK_ANCIENT_TOMB
	call_if_unset FLAG_DEFEATED_REGISTEEL, AncientTomb_EventScript_ShowRegisteel
	end

AncientTomb_EventScript_ShowRegisteel::
	clearflag FLAG_HIDE_REGISTEEL
	return

AncientTomb_OnLoad:
	call_if_unset FLAG_SYS_REGISTEEL_PUZZLE_COMPLETED, AncientTomb_EventScript_HideRegiEntrance
	end

AncientTomb_EventScript_HideRegiEntrance::
	setmetatile 7, 19, METATILE_Cave_EntranceCover, TRUE
	setmetatile 8, 19, METATILE_Cave_EntranceCover, TRUE
	setmetatile 9, 19, METATILE_Cave_EntranceCover, TRUE
	setmetatile 7, 20, METATILE_Cave_SealedChamberBraille_Mid, TRUE
	setmetatile 8, 20, METATILE_Cave_SealedChamberBraille_Mid, TRUE
	setmetatile 9, 20, METATILE_Cave_SealedChamberBraille_Mid, TRUE
	return

AncientTomb_EventScript_CaveEntranceMiddle::
	lockall
	goto_if_set FLAG_SYS_REGISTEEL_PUZZLE_COMPLETED, AncientTomb_EventScript_BigHoleInWall
	braillemsgbox AncientTomb_Braille_ShineInTheMiddle
	releaseall
	end

AncientTomb_EventScript_BigHoleInWall::
	msgbox gText_BigHoleInTheWall, MSGBOX_DEFAULT
	releaseall
	end

AncientTomb_EventScript_CaveEntranceSide::
	lockall
	braillemsgbox AncientTomb_Braille_ShineInTheMiddle
	releaseall
	end

AncientTomb_EventScript_Registeel::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_REGISTEEL, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setwildbattle SPECIES_REGISTEEL, 40
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special StartRegiBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, AncientTomb_EventScript_DefeatedRegisteel
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, AncientTomb_EventScript_RanFromRegisteel
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, AncientTomb_EventScript_RanFromRegisteel
	setflag FLAG_DEFEATED_REGISTEEL
	release
	end

AncientTomb_EventScript_DefeatedRegisteel::
	setflag FLAG_DEFEATED_REGISTEEL
	goto Common_EventScript_RemoveStaticPokemon
	end

AncientTomb_EventScript_RanFromRegisteel::
	setvar VAR_0x8004, SPECIES_REGISTEEL
	goto Common_EventScript_LegendaryFlewAway
	end

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
AncientTomb_EventScript_DexArticunoGalar::
	lockall
	msgbox AncientTomb_Text_DexArticunoGalarIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ARTICUNO_GALAR, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ARTICUNO_GALAR, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ARTICUNO_GALAR
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, AncientTomb_EventScript_DexArticunoGalarSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, AncientTomb_EventScript_DexArticunoGalarSome
	releaseall
	end

AncientTomb_EventScript_DexArticunoGalarSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ARTICUNO_GALAR
	setflag FLAG_HIDE_DEX_ARTICUNO_GALAR
	fadescreenswapbuffers FADE_FROM_BLACK
	return

AncientTomb_Text_DexArticunoGalarIntro:
	.string "ARTICUNO_GALAR appeared!$"

AncientTomb_EventScript_DexGiratinaAltered::
	lockall
	msgbox AncientTomb_Text_DexGiratinaAlteredIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_GIRATINA_ALTERED, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_GIRATINA_ALTERED, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_GIRATINA_ALTERED
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, AncientTomb_EventScript_DexGiratinaAlteredSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, AncientTomb_EventScript_DexGiratinaAlteredSome
	releaseall
	end

AncientTomb_EventScript_DexGiratinaAlteredSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GIRATINA_ALTERED
	setflag FLAG_HIDE_DEX_GIRATINA_ALTERED
	fadescreenswapbuffers FADE_FROM_BLACK
	return

AncientTomb_Text_DexGiratinaAlteredIntro:
	.string "GIRATINA_ALTERED appeared!$"

AncientTomb_EventScript_DexDiancie::
	lockall
	msgbox AncientTomb_Text_DexDiancieIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_DIANCIE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_DIANCIE, 30
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_DIANCIE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, AncientTomb_EventScript_DexDiancieSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, AncientTomb_EventScript_DexDiancieSome
	releaseall
	end

AncientTomb_EventScript_DexDiancieSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_DIANCIE
	setflag FLAG_HIDE_DEX_DIANCIE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

AncientTomb_Text_DexDiancieIntro:
	.string "DIANCIE appeared!$"

AncientTomb_EventScript_DexTapuLele::
	lockall
	msgbox AncientTomb_Text_DexTapuLeleIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_TAPU_LELE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_TAPU_LELE, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_TAPU_LELE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, AncientTomb_EventScript_DexTapuLeleSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, AncientTomb_EventScript_DexTapuLeleSome
	releaseall
	end

AncientTomb_EventScript_DexTapuLeleSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_TAPU_LELE
	setflag FLAG_HIDE_DEX_TAPU_LELE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

AncientTomb_Text_DexTapuLeleIntro:
	.string "TAPU_LELE appeared!$"

AncientTomb_EventScript_DexNecrozmaDawnWings::
	lockall
	msgbox AncientTomb_Text_DexNecrozmaDawnWingsIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_NECROZMA_DAWN_WINGS, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_NECROZMA_DAWN_WINGS, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_NECROZMA_DAWN_WINGS
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, AncientTomb_EventScript_DexNecrozmaDawnWingsSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, AncientTomb_EventScript_DexNecrozmaDawnWingsSome
	releaseall
	end

AncientTomb_EventScript_DexNecrozmaDawnWingsSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_NECROZMA_DAWN_WINGS
	setflag FLAG_HIDE_DEX_NECROZMA_DAWN_WINGS
	fadescreenswapbuffers FADE_FROM_BLACK
	return

AncientTomb_Text_DexNecrozmaDawnWingsIntro:
	.string "NECROZMA_DAWN_WINGS appeared!$"

AncientTomb_EventScript_DexNecrozmaDuskMane::
	lockall
	msgbox AncientTomb_Text_DexNecrozmaDuskManeIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_NECROZMA_DUSK_MANE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_NECROZMA_DUSK_MANE, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_NECROZMA_DUSK_MANE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, AncientTomb_EventScript_DexNecrozmaDuskManeSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, AncientTomb_EventScript_DexNecrozmaDuskManeSome
	releaseall
	end

AncientTomb_EventScript_DexNecrozmaDuskManeSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_NECROZMA_DUSK_MANE
	setflag FLAG_HIDE_DEX_NECROZMA_DUSK_MANE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

AncientTomb_Text_DexNecrozmaDuskManeIntro:
	.string "NECROZMA_DUSK_MANE appeared!$"

AncientTomb_EventScript_DexCalyrex::
	lockall
	msgbox AncientTomb_Text_DexCalyrexIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_CALYREX, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_CALYREX, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_CALYREX
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, AncientTomb_EventScript_DexCalyrexSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, AncientTomb_EventScript_DexCalyrexSome
	releaseall
	end

AncientTomb_EventScript_DexCalyrexSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_CALYREX
	setflag FLAG_HIDE_DEX_CALYREX
	fadescreenswapbuffers FADE_FROM_BLACK
	return

AncientTomb_Text_DexCalyrexIntro:
	.string "CALYREX appeared!$"

AncientTomb_EventScript_DexCalyrexShadow::
	lockall
	msgbox AncientTomb_Text_DexCalyrexShadowIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_CALYREX_SHADOW, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_CALYREX_SHADOW, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_CALYREX_SHADOW
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, AncientTomb_EventScript_DexCalyrexShadowSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, AncientTomb_EventScript_DexCalyrexShadowSome
	releaseall
	end

AncientTomb_EventScript_DexCalyrexShadowSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_CALYREX_SHADOW
	setflag FLAG_HIDE_DEX_CALYREX_SHADOW
	fadescreenswapbuffers FADE_FROM_BLACK
	return

AncientTomb_Text_DexCalyrexShadowIntro:
	.string "CALYREX_SHADOW appeared!$"

@ <<< Dex completa <<<
