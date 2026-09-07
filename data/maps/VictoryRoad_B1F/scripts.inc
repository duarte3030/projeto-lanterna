VictoryRoad_B1F_MapScripts::
	.byte 0

VictoryRoad_B1F_EventScript_Samuel::
	trainerbattle_single TRAINER_SAMUEL, VictoryRoad_B1F_Text_SamuelIntro, VictoryRoad_B1F_Text_SamuelDefeat
	msgbox VictoryRoad_B1F_Text_SamuelPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B1F_EventScript_Shannon::
	trainerbattle_single TRAINER_SHANNON, VictoryRoad_B1F_Text_ShannonIntro, VictoryRoad_B1F_Text_ShannonDefeat
	msgbox VictoryRoad_B1F_Text_ShannonPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B1F_EventScript_Michelle::
	trainerbattle_single TRAINER_MICHELLE, VictoryRoad_B1F_Text_MichelleIntro, VictoryRoad_B1F_Text_MichelleDefeat
	msgbox VictoryRoad_B1F_Text_MichellePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B1F_EventScript_Mitchell::
	trainerbattle_single TRAINER_MITCHELL, VictoryRoad_B1F_Text_MitchellIntro, VictoryRoad_B1F_Text_MitchellDefeat
	msgbox VictoryRoad_B1F_Text_MitchellPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B1F_EventScript_Halle::
	trainerbattle_single TRAINER_HALLE, VictoryRoad_B1F_Text_HalleIntro, VictoryRoad_B1F_Text_HalleDefeat
	msgbox VictoryRoad_B1F_Text_HallePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B1F_Text_SamuelIntro:
	.string "The thought that I'm getting closer to\n"
	.string "the POKéMON LEAGUE…\p"
	.string "I'm getting stage fright…$"

VictoryRoad_B1F_Text_SamuelDefeat:
	.string "I couldn't do a thing…$"

VictoryRoad_B1F_Text_SamuelPostBattle:
	.string "The POKéMON LEAGUE became distant\n"
	.string "again… What a letdown…$"

VictoryRoad_B1F_Text_ShannonIntro:
	.string "To win your way through the POKéMON\n"
	.string "LEAGUE, you need the trust of your\l"
	.string "POKéMON.$"

VictoryRoad_B1F_Text_ShannonDefeat:
	.string "Your relationship is based on\n"
	.string "solid trust.$"

VictoryRoad_B1F_Text_ShannonPostBattle:
	.string "By being together all the time, trust\n"
	.string "grows between POKéMON and TRAINERS.$"

VictoryRoad_B1F_Text_MichelleIntro:
	.string "This isn't the goal. It's only a place\n"
	.string "on the way to the POKéMON LEAGUE.$"

VictoryRoad_B1F_Text_MichelleDefeat:
	.string "That's the way!$"

VictoryRoad_B1F_Text_MichellePostBattle:
	.string "You'll do fine, for sure!\n"
	.string "Your POKéMON are all eager to go!$"

VictoryRoad_B1F_Text_MitchellIntro:
	.string "My POKéMON are cosmically\n"
	.string "awe inspiring!$"

VictoryRoad_B1F_Text_MitchellDefeat:
	.string "I've never met anyone like you before.$"

VictoryRoad_B1F_Text_MitchellPostBattle:
	.string "Even outside of battle, I sense\n"
	.string "incredible power emanating from you\l"
	.string "and your POKéMON.$"

VictoryRoad_B1F_Text_HalleIntro:
	.string "Okay, no need to get your back up!\n"
	.string "Relax, let's take it easy!$"

VictoryRoad_B1F_Text_HalleDefeat:
	.string "Whoa!\n"
	.string "Wonderful!$"

VictoryRoad_B1F_Text_HallePostBattle:
	.string "Sure, this is VICTORY ROAD.\p"
	.string "But it's not all that different from\n"
	.string "the path you've taken so far.\p"
	.string "Try to enjoy things the rest of\n"
	.string "the way!$"

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
VictoryRoad_B1F_EventScript_DexIronTreads::
	lockall
	msgbox VictoryRoad_B1F_Text_DexIronTreadsIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_IRON_TREADS, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_IRON_TREADS, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_IRON_TREADS
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, VictoryRoad_B1F_EventScript_DexIronTreadsSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, VictoryRoad_B1F_EventScript_DexIronTreadsSome
	releaseall
	end

VictoryRoad_B1F_EventScript_DexIronTreadsSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_IRON_TREADS
	setflag FLAG_HIDE_DEX_IRON_TREADS
	fadescreenswapbuffers FADE_FROM_BLACK
	return

VictoryRoad_B1F_Text_DexIronTreadsIntro:
	.string "IRON_TREADS appeared!$"

VictoryRoad_B1F_EventScript_DexIronBundle::
	lockall
	msgbox VictoryRoad_B1F_Text_DexIronBundleIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_IRON_BUNDLE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_IRON_BUNDLE, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_IRON_BUNDLE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, VictoryRoad_B1F_EventScript_DexIronBundleSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, VictoryRoad_B1F_EventScript_DexIronBundleSome
	releaseall
	end

VictoryRoad_B1F_EventScript_DexIronBundleSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_IRON_BUNDLE
	setflag FLAG_HIDE_DEX_IRON_BUNDLE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

VictoryRoad_B1F_Text_DexIronBundleIntro:
	.string "IRON_BUNDLE appeared!$"

VictoryRoad_B1F_EventScript_DexIronHands::
	lockall
	msgbox VictoryRoad_B1F_Text_DexIronHandsIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_IRON_HANDS, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_IRON_HANDS, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_IRON_HANDS
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, VictoryRoad_B1F_EventScript_DexIronHandsSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, VictoryRoad_B1F_EventScript_DexIronHandsSome
	releaseall
	end

VictoryRoad_B1F_EventScript_DexIronHandsSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_IRON_HANDS
	setflag FLAG_HIDE_DEX_IRON_HANDS
	fadescreenswapbuffers FADE_FROM_BLACK
	return

VictoryRoad_B1F_Text_DexIronHandsIntro:
	.string "IRON_HANDS appeared!$"

VictoryRoad_B1F_EventScript_DexIronJugulis::
	lockall
	msgbox VictoryRoad_B1F_Text_DexIronJugulisIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_IRON_JUGULIS, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_IRON_JUGULIS, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_IRON_JUGULIS
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, VictoryRoad_B1F_EventScript_DexIronJugulisSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, VictoryRoad_B1F_EventScript_DexIronJugulisSome
	releaseall
	end

VictoryRoad_B1F_EventScript_DexIronJugulisSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_IRON_JUGULIS
	setflag FLAG_HIDE_DEX_IRON_JUGULIS
	fadescreenswapbuffers FADE_FROM_BLACK
	return

VictoryRoad_B1F_Text_DexIronJugulisIntro:
	.string "IRON_JUGULIS appeared!$"

VictoryRoad_B1F_EventScript_DexIronMoth::
	lockall
	msgbox VictoryRoad_B1F_Text_DexIronMothIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_IRON_MOTH, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_IRON_MOTH, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_IRON_MOTH
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, VictoryRoad_B1F_EventScript_DexIronMothSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, VictoryRoad_B1F_EventScript_DexIronMothSome
	releaseall
	end

VictoryRoad_B1F_EventScript_DexIronMothSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_IRON_MOTH
	setflag FLAG_HIDE_DEX_IRON_MOTH
	fadescreenswapbuffers FADE_FROM_BLACK
	return

VictoryRoad_B1F_Text_DexIronMothIntro:
	.string "IRON_MOTH appeared!$"

VictoryRoad_B1F_EventScript_DexIronThorns::
	lockall
	msgbox VictoryRoad_B1F_Text_DexIronThornsIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_IRON_THORNS, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_IRON_THORNS, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_IRON_THORNS
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, VictoryRoad_B1F_EventScript_DexIronThornsSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, VictoryRoad_B1F_EventScript_DexIronThornsSome
	releaseall
	end

VictoryRoad_B1F_EventScript_DexIronThornsSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_IRON_THORNS
	setflag FLAG_HIDE_DEX_IRON_THORNS
	fadescreenswapbuffers FADE_FROM_BLACK
	return

VictoryRoad_B1F_Text_DexIronThornsIntro:
	.string "IRON_THORNS appeared!$"

VictoryRoad_B1F_EventScript_DexIronValiant::
	lockall
	msgbox VictoryRoad_B1F_Text_DexIronValiantIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_IRON_VALIANT, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_IRON_VALIANT, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_IRON_VALIANT
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, VictoryRoad_B1F_EventScript_DexIronValiantSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, VictoryRoad_B1F_EventScript_DexIronValiantSome
	releaseall
	end

VictoryRoad_B1F_EventScript_DexIronValiantSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_IRON_VALIANT
	setflag FLAG_HIDE_DEX_IRON_VALIANT
	fadescreenswapbuffers FADE_FROM_BLACK
	return

VictoryRoad_B1F_Text_DexIronValiantIntro:
	.string "IRON_VALIANT appeared!$"

VictoryRoad_B1F_EventScript_DexIronLeaves::
	lockall
	msgbox VictoryRoad_B1F_Text_DexIronLeavesIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_IRON_LEAVES, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_IRON_LEAVES, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_IRON_LEAVES
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, VictoryRoad_B1F_EventScript_DexIronLeavesSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, VictoryRoad_B1F_EventScript_DexIronLeavesSome
	releaseall
	end

VictoryRoad_B1F_EventScript_DexIronLeavesSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_IRON_LEAVES
	setflag FLAG_HIDE_DEX_IRON_LEAVES
	fadescreenswapbuffers FADE_FROM_BLACK
	return

VictoryRoad_B1F_Text_DexIronLeavesIntro:
	.string "IRON_LEAVES appeared!$"

VictoryRoad_B1F_EventScript_DexIronBoulder::
	lockall
	msgbox VictoryRoad_B1F_Text_DexIronBoulderIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_IRON_BOULDER, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_IRON_BOULDER, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_IRON_BOULDER
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, VictoryRoad_B1F_EventScript_DexIronBoulderSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, VictoryRoad_B1F_EventScript_DexIronBoulderSome
	releaseall
	end

VictoryRoad_B1F_EventScript_DexIronBoulderSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_IRON_BOULDER
	setflag FLAG_HIDE_DEX_IRON_BOULDER
	fadescreenswapbuffers FADE_FROM_BLACK
	return

VictoryRoad_B1F_Text_DexIronBoulderIntro:
	.string "IRON_BOULDER appeared!$"

@ <<< Dex completa <<<
