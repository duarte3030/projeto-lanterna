SkyPillar_4F_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, CaveHole_CheckFallDownHole
	map_script MAP_SCRIPT_ON_TRANSITION, SkyPillar_4F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, SkyPillar_4F_SetHoleWarp
	.byte 0

SkyPillar_4F_OnTransition:
	call_if_lt VAR_SKY_PILLAR_STATE, 2, SkyPillar_4F_EventScript_CleanFloor
#ifdef UBFIX
	setvar VAR_ICE_STEP_COUNT, 1
#else
	copyvar VAR_ICE_STEP_COUNT, 1, warn=FALSE
#endif
	end

SkyPillar_4F_EventScript_CleanFloor::
	setmaplayoutindex LAYOUT_SKY_PILLAR_4F_CLEAN
	return

SkyPillar_4F_SetHoleWarp:
	setstepcallback STEP_CB_CRACKED_FLOOR
	setholewarp MAP_SKY_PILLAR_3F
	end

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
SkyPillar_4F_EventScript_DexThundurusIncarnate::
	lockall
	msgbox SkyPillar_4F_Text_DexThundurusIncarnateIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_THUNDURUS_INCARNATE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_THUNDURUS_INCARNATE, 80
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_THUNDURUS_INCARNATE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, SkyPillar_4F_EventScript_DexThundurusIncarnateSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, SkyPillar_4F_EventScript_DexThundurusIncarnateSome
	releaseall
	end

SkyPillar_4F_EventScript_DexThundurusIncarnateSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_THUNDURUS_INCARNATE
	setflag FLAG_HIDE_DEX_THUNDURUS_INCARNATE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

SkyPillar_4F_Text_DexThundurusIncarnateIntro:
	.string "THUNDURUS_INCARNATE appeared!$"

@ <<< Dex completa <<<
