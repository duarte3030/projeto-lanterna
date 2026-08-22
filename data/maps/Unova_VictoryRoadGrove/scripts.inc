@ VictoryRoadGrove do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_VictoryRoadGrove_MapScripts::
	.byte 0

Unova_VictoryRoadGrove_EventScript_Lider2::
	trainerbattle_single TRAINER_UNOVA_ACE_TRAINERM_VICTORY_ROAD_EXT_2, Unova_VictoryRoadGrove_Text_AceTrainerMVictoryRoadGroveSeenText, Unova_VictoryRoadGrove_Text_AceTrainerMVictoryRoadGroveBeatenText
	end

Unova_VictoryRoadGrove_EventScript_Lider3::
	trainerbattle_single TRAINER_UNOVA_ACE_TRAINERF_VICTORY_ROAD_EXT_1, Unova_VictoryRoadGrove_Text_AceTrainerFVictoryRoadGroveSeenText, Unova_VictoryRoadGrove_Text_AceTrainerFVictoryRoadGroveBeatenText
	end


Unova_VictoryRoadGrove_Text_AceTrainerMVictoryRoadGroveSeenText::
	.string "One, you are a"
	.string "\nPOKéMON trainer."
	.string "\pTwo, I am an ACE"
	.string "\nTRAINER. Put them"
	.string "\ptogether, and it's"
	.string "\nobvious that we're"
	.string "\lgoing to battle!$"

Unova_VictoryRoadGrove_Text_AceTrainerMVictoryRoadGroveBeatenText::
	.string "One, you won! Two,"
	.string "\nI lost…$"

Unova_VictoryRoadGrove_Text_AceTrainerFVictoryRoadGroveSeenText::
	.string "I want to show how"
	.string "\nmuch I love POKé-"
	.string "\lMON by winning!$"

Unova_VictoryRoadGrove_Text_AceTrainerFVictoryRoadGroveBeatenText::
	.string "I can't show my"
	.string "\nlove for my POKé-"
	.string "\pMON if I go and"
	.string "\nlose…$"

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
Unova_VictoryRoadGrove_EventScript_DexIronLeaves::
	lockall
	msgbox Unova_VictoryRoadGrove_Text_DexIronLeavesIntro, MSGBOX_DEFAULT
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
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_VictoryRoadGrove_EventScript_DexIronLeavesSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_VictoryRoadGrove_EventScript_DexIronLeavesSome
	releaseall
	end

Unova_VictoryRoadGrove_EventScript_DexIronLeavesSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_IRON_LEAVES
	setflag FLAG_HIDE_DEX_IRON_LEAVES
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_VictoryRoadGrove_Text_DexIronLeavesIntro:
	.string "IRON_LEAVES appeared!$"

Unova_VictoryRoadGrove_EventScript_DexIronBoulder::
	lockall
	msgbox Unova_VictoryRoadGrove_Text_DexIronBoulderIntro, MSGBOX_DEFAULT
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
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_VictoryRoadGrove_EventScript_DexIronBoulderSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_VictoryRoadGrove_EventScript_DexIronBoulderSome
	releaseall
	end

Unova_VictoryRoadGrove_EventScript_DexIronBoulderSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_IRON_BOULDER
	setflag FLAG_HIDE_DEX_IRON_BOULDER
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_VictoryRoadGrove_Text_DexIronBoulderIntro:
	.string "IRON_BOULDER appeared!$"

Unova_VictoryRoadGrove_EventScript_DexIronCrown::
	lockall
	msgbox Unova_VictoryRoadGrove_Text_DexIronCrownIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_IRON_CROWN, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_IRON_CROWN, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_IRON_CROWN
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_VictoryRoadGrove_EventScript_DexIronCrownSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_VictoryRoadGrove_EventScript_DexIronCrownSome
	releaseall
	end

Unova_VictoryRoadGrove_EventScript_DexIronCrownSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_IRON_CROWN
	setflag FLAG_HIDE_DEX_IRON_CROWN
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_VictoryRoadGrove_Text_DexIronCrownIntro:
	.string "IRON_CROWN appeared!$"

@ <<< Dex completa <<<
