VictoryRoad_2F_Frlg_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, VictoryRoad_2F_OnLoad
	.byte 0

VictoryRoad_2F_OnLoad::
	call_if_ne VAR_MAP_SCENE_VICTORY_ROAD_2F_BOULDER1, 100, VictoryRoad_2F_EventScript_SetRockBarrier1
	call_if_ne VAR_MAP_SCENE_VICTORY_ROAD_2F_BOULDER2, 100, VictoryRoad_2F_EventScript_SetRockBarrier2
	end

VictoryRoad_2F_EventScript_SetRockBarrier1::
	setmetatile 13, 10, METATILE_Cave_RockBarrier_Top, 1
	setmetatile 13, 11, METATILE_Cave_RockBarrier_Bottom, 1
	return

VictoryRoad_2F_EventScript_SetRockBarrier2::
	setmetatile 33, 16, METATILE_Cave_RockBarrier_Top, 1
	setmetatile 33, 17, METATILE_Cave_RockBarrier_Bottom, 1
	return

VictoryRoad_2F_EventScript_FloorSwitch1::
	lockall
	goto_if_eq VAR_MAP_SCENE_VICTORY_ROAD_2F_BOULDER1, 100, VictoryRoad_2F_EventScript_FloorSwitch1AlreadyPressed
	setmetatile 13, 10, METATILE_Cave_Floor_Ledge_Top, 0
	setmetatile 13, 11, METATILE_Cave_Floor_Ledge_Bottom, 0
	playse SE_ICE_BREAK
	special DrawWholeMapView
	waitse
	copyobjectxytoperm LOCALID_VICTORY_ROAD_2F_BOULDER1
	setvar VAR_MAP_SCENE_VICTORY_ROAD_2F_BOULDER1, 100
	releaseall
	end

VictoryRoad_2F_EventScript_FloorSwitch1AlreadyPressed::
	releaseall
	end

VictoryRoad_2F_EventScript_FloorSwitch2::
	lockall
	goto_if_eq VAR_MAP_SCENE_VICTORY_ROAD_2F_BOULDER2, 100, VictoryRoad_2F_EventScript_FloorSwitch2AlreadyPressed
	setmetatile 33, 16, METATILE_Cave_Floor_Ledge_Top, 0
	setmetatile 33, 17, METATILE_Cave_Floor_Ledge_Bottom, 0
	playse SE_ICE_BREAK
	special DrawWholeMapView
	waitse
	copyobjectxytoperm LOCALID_VICTORY_ROAD_2F_BOULDER2
	setvar VAR_MAP_SCENE_VICTORY_ROAD_2F_BOULDER2, 100
	releaseall
	end

VictoryRoad_2F_EventScript_FloorSwitch2AlreadyPressed::
	releaseall
	end

VictoryRoad_2F_EventScript_Dawson::
	trainerbattle_single TRAINER_POKEMANIAC_DAWSON, VictoryRoad_2F_Text_DawsonIntro, VictoryRoad_2F_Text_DawsonDefeat
	msgbox VictoryRoad_2F_Text_DawsonPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_2F_EventScript_Daisuke::
	trainerbattle_single TRAINER_BLACK_BELT_DAISUKE, VictoryRoad_2F_Text_DaisukeIntro, VictoryRoad_2F_Text_DaisukeDefeat
	msgbox VictoryRoad_2F_Text_DaisukePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_2F_EventScript_Nelson::
	trainerbattle_single TRAINER_JUGGLER_NELSON, VictoryRoad_2F_Text_NelsonIntro, VictoryRoad_2F_Text_NelsonDefeat
	msgbox VictoryRoad_2F_Text_NelsonPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_2F_EventScript_Gregory::
	trainerbattle_single TRAINER_JUGGLER_GREGORY, VictoryRoad_2F_Text_GregoryIntro, VictoryRoad_2F_Text_GregoryDefeat
	msgbox VictoryRoad_2F_Text_GregoryPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_2F_EventScript_Vincent::
	trainerbattle_single TRAINER_TAMER_VINCENT, VictoryRoad_2F_Text_VincentIntro, VictoryRoad_2F_Text_VincentDefeat
	msgbox VictoryRoad_2F_Text_VincentPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_2F_Text_DawsonIntro::
	.string "If you can get through here,\n"
	.string "you can go meet the ELITE FOUR.$"

VictoryRoad_2F_Text_DawsonDefeat::
	.string "No!\n"
	.string "Unbelievable!$"

VictoryRoad_2F_Text_DawsonPostBattle::
	.string "I can beat you when it comes to\n"
	.string "knowledge about POKéMON!$"

VictoryRoad_2F_Text_DaisukeIntro::
	.string "This here is VICTORY ROAD.\n"
	.string "It's the final test for TRAINERS!$"

VictoryRoad_2F_Text_DaisukeDefeat::
	.string "Atcho!$"

VictoryRoad_2F_Text_DaisukePostBattle::
	.string "If you get stuck, try moving some\n"
	.string "boulders around.$"

VictoryRoad_2F_Text_NelsonIntro::
	.string "Ah, so you wish to challenge the\n"
	.string "ELITE FOUR?$"

VictoryRoad_2F_Text_NelsonDefeat::
	.string "You got me!$"

VictoryRoad_2F_Text_NelsonPostBattle::
	.string "{RIVAL} also came through here.$"

VictoryRoad_2F_Text_VincentIntro::
	.string "Come on!\n"
	.string "I'll whip you!$"

VictoryRoad_2F_Text_VincentDefeat::
	.string "I got whipped!$"

VictoryRoad_2F_Text_VincentPostBattle::
	.string "You earned the right to be on\n"
	.string "VICTORY ROAD…$"

VictoryRoad_2F_Text_GregoryIntro::
	.string "Is VICTORY ROAD too tough?$"

VictoryRoad_2F_Text_GregoryDefeat::
	.string "Well done!$"

VictoryRoad_2F_Text_GregoryPostBattle::
	.string "Many TRAINERS give up their\n"
	.string "challenge here and go home.$"

@ Unused, old text for Moltres
VictoryRoad_2F_Text_Gyaoo::
	.string "ギヤーオ！$"

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
VictoryRoad_2F_Frlg_EventScript_DexGreatTusk::
	lockall
	msgbox VictoryRoad_2F_Frlg_Text_DexGreatTuskIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_GREAT_TUSK, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_GREAT_TUSK, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_GREAT_TUSK
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, VictoryRoad_2F_Frlg_EventScript_DexGreatTuskSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, VictoryRoad_2F_Frlg_EventScript_DexGreatTuskSome
	releaseall
	end

VictoryRoad_2F_Frlg_EventScript_DexGreatTuskSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GREAT_TUSK
	setflag FLAG_HIDE_DEX_GREAT_TUSK
	fadescreenswapbuffers FADE_FROM_BLACK
	return

VictoryRoad_2F_Frlg_Text_DexGreatTuskIntro:
	.string "GREAT_TUSK appeared!$"

VictoryRoad_2F_Frlg_EventScript_DexScreamTail::
	lockall
	msgbox VictoryRoad_2F_Frlg_Text_DexScreamTailIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_SCREAM_TAIL, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_SCREAM_TAIL, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_SCREAM_TAIL
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, VictoryRoad_2F_Frlg_EventScript_DexScreamTailSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, VictoryRoad_2F_Frlg_EventScript_DexScreamTailSome
	releaseall
	end

VictoryRoad_2F_Frlg_EventScript_DexScreamTailSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_SCREAM_TAIL
	setflag FLAG_HIDE_DEX_SCREAM_TAIL
	fadescreenswapbuffers FADE_FROM_BLACK
	return

VictoryRoad_2F_Frlg_Text_DexScreamTailIntro:
	.string "SCREAM_TAIL appeared!$"

VictoryRoad_2F_Frlg_EventScript_DexBruteBonnet::
	lockall
	msgbox VictoryRoad_2F_Frlg_Text_DexBruteBonnetIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_BRUTE_BONNET, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_BRUTE_BONNET, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_BRUTE_BONNET
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, VictoryRoad_2F_Frlg_EventScript_DexBruteBonnetSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, VictoryRoad_2F_Frlg_EventScript_DexBruteBonnetSome
	releaseall
	end

VictoryRoad_2F_Frlg_EventScript_DexBruteBonnetSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_BRUTE_BONNET
	setflag FLAG_HIDE_DEX_BRUTE_BONNET
	fadescreenswapbuffers FADE_FROM_BLACK
	return

VictoryRoad_2F_Frlg_Text_DexBruteBonnetIntro:
	.string "BRUTE_BONNET appeared!$"

VictoryRoad_2F_Frlg_EventScript_DexFlutterMane::
	lockall
	msgbox VictoryRoad_2F_Frlg_Text_DexFlutterManeIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_FLUTTER_MANE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_FLUTTER_MANE, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_FLUTTER_MANE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, VictoryRoad_2F_Frlg_EventScript_DexFlutterManeSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, VictoryRoad_2F_Frlg_EventScript_DexFlutterManeSome
	releaseall
	end

VictoryRoad_2F_Frlg_EventScript_DexFlutterManeSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_FLUTTER_MANE
	setflag FLAG_HIDE_DEX_FLUTTER_MANE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

VictoryRoad_2F_Frlg_Text_DexFlutterManeIntro:
	.string "FLUTTER_MANE appeared!$"

VictoryRoad_2F_Frlg_EventScript_DexSlitherWing::
	lockall
	msgbox VictoryRoad_2F_Frlg_Text_DexSlitherWingIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_SLITHER_WING, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_SLITHER_WING, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_SLITHER_WING
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, VictoryRoad_2F_Frlg_EventScript_DexSlitherWingSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, VictoryRoad_2F_Frlg_EventScript_DexSlitherWingSome
	releaseall
	end

VictoryRoad_2F_Frlg_EventScript_DexSlitherWingSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_SLITHER_WING
	setflag FLAG_HIDE_DEX_SLITHER_WING
	fadescreenswapbuffers FADE_FROM_BLACK
	return

VictoryRoad_2F_Frlg_Text_DexSlitherWingIntro:
	.string "SLITHER_WING appeared!$"

VictoryRoad_2F_Frlg_EventScript_DexSandyShocks::
	lockall
	msgbox VictoryRoad_2F_Frlg_Text_DexSandyShocksIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_SANDY_SHOCKS, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_SANDY_SHOCKS, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_SANDY_SHOCKS
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, VictoryRoad_2F_Frlg_EventScript_DexSandyShocksSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, VictoryRoad_2F_Frlg_EventScript_DexSandyShocksSome
	releaseall
	end

VictoryRoad_2F_Frlg_EventScript_DexSandyShocksSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_SANDY_SHOCKS
	setflag FLAG_HIDE_DEX_SANDY_SHOCKS
	fadescreenswapbuffers FADE_FROM_BLACK
	return

VictoryRoad_2F_Frlg_Text_DexSandyShocksIntro:
	.string "SANDY_SHOCKS appeared!$"

VictoryRoad_2F_Frlg_EventScript_DexRoaringMoon::
	lockall
	msgbox VictoryRoad_2F_Frlg_Text_DexRoaringMoonIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ROARING_MOON, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ROARING_MOON, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ROARING_MOON
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, VictoryRoad_2F_Frlg_EventScript_DexRoaringMoonSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, VictoryRoad_2F_Frlg_EventScript_DexRoaringMoonSome
	releaseall
	end

VictoryRoad_2F_Frlg_EventScript_DexRoaringMoonSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ROARING_MOON
	setflag FLAG_HIDE_DEX_ROARING_MOON
	fadescreenswapbuffers FADE_FROM_BLACK
	return

VictoryRoad_2F_Frlg_Text_DexRoaringMoonIntro:
	.string "ROARING_MOON appeared!$"

VictoryRoad_2F_Frlg_EventScript_DexWalkingWake::
	lockall
	msgbox VictoryRoad_2F_Frlg_Text_DexWalkingWakeIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_WALKING_WAKE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_WALKING_WAKE, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_WALKING_WAKE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, VictoryRoad_2F_Frlg_EventScript_DexWalkingWakeSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, VictoryRoad_2F_Frlg_EventScript_DexWalkingWakeSome
	releaseall
	end

VictoryRoad_2F_Frlg_EventScript_DexWalkingWakeSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_WALKING_WAKE
	setflag FLAG_HIDE_DEX_WALKING_WAKE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

VictoryRoad_2F_Frlg_Text_DexWalkingWakeIntro:
	.string "WALKING_WAKE appeared!$"

VictoryRoad_2F_Frlg_EventScript_DexGougingFire::
	lockall
	msgbox VictoryRoad_2F_Frlg_Text_DexGougingFireIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_GOUGING_FIRE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_GOUGING_FIRE, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_GOUGING_FIRE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, VictoryRoad_2F_Frlg_EventScript_DexGougingFireSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, VictoryRoad_2F_Frlg_EventScript_DexGougingFireSome
	releaseall
	end

VictoryRoad_2F_Frlg_EventScript_DexGougingFireSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GOUGING_FIRE
	setflag FLAG_HIDE_DEX_GOUGING_FIRE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

VictoryRoad_2F_Frlg_Text_DexGougingFireIntro:
	.string "GOUGING_FIRE appeared!$"

VictoryRoad_2F_Frlg_EventScript_DexRagingBolt::
	lockall
	msgbox VictoryRoad_2F_Frlg_Text_DexRagingBoltIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_RAGING_BOLT, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_RAGING_BOLT, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_RAGING_BOLT
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, VictoryRoad_2F_Frlg_EventScript_DexRagingBoltSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, VictoryRoad_2F_Frlg_EventScript_DexRagingBoltSome
	releaseall
	end

VictoryRoad_2F_Frlg_EventScript_DexRagingBoltSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_RAGING_BOLT
	setflag FLAG_HIDE_DEX_RAGING_BOLT
	fadescreenswapbuffers FADE_FROM_BLACK
	return

VictoryRoad_2F_Frlg_Text_DexRagingBoltIntro:
	.string "RAGING_BOLT appeared!$"

@ <<< Dex completa <<<
