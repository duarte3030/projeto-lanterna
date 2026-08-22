VictoryRoad_1F_Frlg_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, VictoryRoad_1F_Frlg_OnLoad
	map_script MAP_SCRIPT_ON_TRANSITION, VictoryRoad_1F_Frlg_OnTransition
	.byte 0

VictoryRoad_1F_Frlg_OnLoad::
	call_if_ne VAR_MAP_SCENE_VICTORY_ROAD_1F, 100, VictoryRoad_1F_EventScript_SetRockBarrier
	end

VictoryRoad_1F_EventScript_SetRockBarrier::
	setmetatile 12, 14, METATILE_Cave_RockBarrier_Top, 1
	setmetatile 12, 15, METATILE_Cave_RockBarrier_Bottom, 1
	return

VictoryRoad_1F_Frlg_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_VICTORY_ROAD_1F
	call VictoryRoad_1F_EventScript_SilverPorta
	end

VictoryRoad_1F_EventScript_FloorSwitch::
	lockall
	goto_if_eq VAR_MAP_SCENE_VICTORY_ROAD_1F, 100, VictoryRoad_1F_EventScript_FloorSwitchAlreadyPressed
	setmetatile 12, 14, METATILE_Cave_Floor_Ledge_Top, 0
	setmetatile 12, 15, METATILE_Cave_Floor_Ledge_Bottom, 0
	playse SE_ICE_BREAK
	special DrawWholeMapView
	waitse
	copyobjectxytoperm LOCALID_VICTORY_ROAD_1F_BOULDER
	setvar VAR_MAP_SCENE_VICTORY_ROAD_1F, 100
	releaseall
	end

VictoryRoad_1F_EventScript_FloorSwitchAlreadyPressed::
	releaseall
	end

VictoryRoad_1F_EventScript_Naomi::
	trainerbattle_single TRAINER_COOLTRAINER_NAOMI, VictoryRoad_1F_Text_NaomiIntro, VictoryRoad_1F_Text_NaomiDefeat
	msgbox VictoryRoad_1F_Text_NaomiPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_1F_EventScript_Rolando::
	trainerbattle_single TRAINER_COOLTRAINER_ROLANDO, VictoryRoad_1F_Text_RolandoIntro, VictoryRoad_1F_Text_RolandoDefeat
	msgbox VictoryRoad_1F_Text_RolandoPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_1F_Text_NaomiIntro::
	.string "I wonder if you are good enough\n"
	.string "for me?$"

VictoryRoad_1F_Text_NaomiDefeat::
	.string "I lost out…$"

VictoryRoad_1F_Text_NaomiPostBattle::
	.string "I never wanted to lose to anybody,\n"
	.string "especially to a younger kid…$"

VictoryRoad_1F_Text_RolandoIntro::
	.string "I can see you're good.\n"
	.string "Let me see exactly how good!$"

VictoryRoad_1F_Text_RolandoDefeat::
	.string "I had a chance…$"

VictoryRoad_1F_Text_RolandoPostBattle::
	.string "Tch!\n"
	.string "I concede, you are better than I!$"

@ >>> cena importada por dev_scripts/importa_chefes_faltantes.py >>>
VictoryRoad_1F_EventScript_SilverPorta::
	setflag FLAG_HIDE_SILVER_VICTORY_ROAD
	goto_if_not_defeated TRAINER_JOHTO_RIVAL_SILVER_4, Common_EventScript_NopReturn
	goto_if_defeated TRAINER_JOHTO_RIVAL_SILVER_5, Common_EventScript_NopReturn
	clearflag FLAG_HIDE_SILVER_VICTORY_ROAD
	return

VictoryRoad_1F_EventScript_Silver::
	trainerbattle_single TRAINER_JOHTO_RIVAL_SILVER_5, VictoryRoad_1F_Text_SilverSeen, VictoryRoad_1F_Text_SilverBeaten
	msgbox VictoryRoad_1F_Text_SilverAfter, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_HIDE_SILVER_VICTORY_ROAD
	removeobject LOCALID_VICTORY_ROAD_1F_SILVER
	release
	end

VictoryRoad_1F_Text_SilverSeen::
	.string "Hold it.\p"
	.string "…Are you going to take the POKéMON\n"
	.string "LEAGUE challenge?\p"
	.string "…Don't make me laugh.\p"
	.string "You're so much weaker than I am.\p"
	.string "I'm not like I was before.\p"
	.string "I now have the best and strongest\n"
	.string "POKéMON with me.\p"
	.string "I'm invincible!\p"
	.string "{PLAYER}!\n"
	.string "I challenge you!$"

VictoryRoad_1F_Text_SilverBeaten::
	.string "…I couldn't win…\p"
	.string "I gave it every-thing I had…\p"
	.string "What you possess, and what I lack…\p"
	.string "I'm beginning to understand what\n"
	.string "that dragon master said to me…$"

VictoryRoad_1F_Text_SilverAfter::
	.string "…I haven't given up on becoming the\n"
	.string "greatest trainer…\p"
	.string "I'm going to find out why I can't\n"
	.string "win and become stronger…\p"
	.string "When I do, I will challenge you.\p"
	.string "…Humph! You keep at it until then.$"
@ <<< cena importada por dev_scripts/importa_chefes_faltantes.py <<<
