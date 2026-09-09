ViridianForest_Frlg_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, ViridianForest_OnTransition
	.byte 0

ViridianForest_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_VIRIDIAN_FOREST
	end

ViridianForest_EventScript_Youngster::
	msgbox ViridianForest_Text_FriendsItchingToBattle, MSGBOX_NPC
	end

ViridianForest_EventScript_Boy::
	msgbox ViridianForest_Text_RanOutOfPokeBalls, MSGBOX_NPC
	end

ViridianForest_EventScript_TrainerTips1::
	msgbox ViridianForest_Text_AvoidGrassyAreasWhenWeak, MSGBOX_SIGN
	end

ViridianForest_EventScript_TrainerTips2::
	msgbox ViridianForest_Text_UseAntidoteForPoison, MSGBOX_SIGN
	end

ViridianForest_EventScript_TrainerTips3::
	msgbox ViridianForest_Text_ContactOakViaPCToRatePokedex, MSGBOX_SIGN
	end

ViridianForest_EventScript_TrainerTips4::
	msgbox ViridianForest_Text_CantCatchOwnedMons, MSGBOX_SIGN
	end

ViridianForest_EventScript_TrainerTips5::
	msgbox ViridianForest_Text_WeakenMonsBeforeCapture, MSGBOX_SIGN
	end

ViridianForest_EventScript_ExitSign::
	msgbox ViridianForest_Text_LeavingViridianForest, MSGBOX_SIGN
	end

ViridianForest_EventScript_Rick::
	trainerbattle_single TRAINER_BUG_CATCHER_RICK, ViridianForest_Text_RickIntro, ViridianForest_Text_RickDefeat
	msgbox ViridianForest_Text_RickPostBattle, MSGBOX_AUTOCLOSE
	end

ViridianForest_EventScript_Doug::
	trainerbattle_single TRAINER_BUG_CATCHER_DOUG, ViridianForest_Text_DougIntro, ViridianForest_Text_DougDefeat
	msgbox ViridianForest_Text_DougPostBattle, MSGBOX_AUTOCLOSE
	end

ViridianForest_EventScript_Sammy::
	trainerbattle_single TRAINER_BUG_CATCHER_SAMMY, ViridianForest_Text_SammyIntro, ViridianForest_Text_SammyDefeat
	msgbox ViridianForest_Text_SammyPostBattle, MSGBOX_AUTOCLOSE
	end

ViridianForest_EventScript_Anthony::
	trainerbattle_single TRAINER_BUG_CATCHER_ANTHONY, ViridianForest_Text_AnthonyIntro, ViridianForest_Text_AnthonyDefeat
	msgbox ViridianForest_Text_AnthonyPostBattle, MSGBOX_AUTOCLOSE
	end

ViridianForest_EventScript_Charlie::
	trainerbattle_single TRAINER_BUG_CATCHER_CHARLIE, ViridianForest_Text_CharlieIntro, ViridianForest_Text_CharlieDefeat
	msgbox ViridianForest_Text_CharliePostBattle, MSGBOX_AUTOCLOSE
	end

ViridianForest_Text_FriendsItchingToBattle::
	.string "I came here with some friends to\n"
	.string "catch us some BUG POKéMON!\p"
	.string "They're all itching to get into\n"
	.string "some POKéMON battles!$"

ViridianForest_Text_RickIntro::
	.string "Hey! You have POKéMON!\n"
	.string "Come on!\l"
	.string "Let's battle 'em!$"

ViridianForest_Text_RickDefeat::
	.string "No!\nCATERPIE can't hack it!$"

ViridianForest_Text_RickPostBattle::
	.string "Ssh! You'll scare the bugs away.\n"
	.string "Another time, okay?$"

ViridianForest_Text_DougIntro::
	.string "Yo!\n"
	.string "You can't jam out if you're a\l"
	.string "POKéMON TRAINER!$"

ViridianForest_Text_DougDefeat::
	.string "Huh?\n"
	.string "I ran out of POKéMON!$"

ViridianForest_Text_DougPostBattle::
	.string "That totally stinks! I'm going to\n"
	.string "catch some stronger ones!$"

ViridianForest_Text_SammyIntro::
	.string "Hey, wait up!\n"
	.string "What's the hurry? Why the rush?$"

ViridianForest_Text_SammyDefeat::
	.string "I give!\n"
	.string "You're good at this!$"

ViridianForest_Text_SammyPostBattle::
	.string "Sometimes, you can find stuff on\n"
	.string "the ground.\p"
	.string "I'm looking for the stuff I\n"
	.string "dropped. Can you help me?$"

ViridianForest_Text_AnthonyIntro::
	.string "I might be little, but I won't like\n"
	.string "it if you go easy on me!$"

ViridianForest_Text_AnthonyDefeat::
	.string "Oh, boo.\n"
	.string "Nothing went right.$"

ViridianForest_Text_AnthonyPostBattle::
	.string "I lost some of my allowance…$"

ViridianForest_Text_CharlieIntro::
	.string "Did you know that POKéMON evolve?$"

ViridianForest_Text_CharlieDefeat::
	.string "Oh!\n"
	.string "I lost!$"

ViridianForest_Text_CharliePostBattle::
	.string "BUG POKéMON evolve quickly.\n"
	.string "They're a lot of fun!$"

ViridianForest_Text_RanOutOfPokeBalls::
	.string "I was throwing POKé BALLS to\n"
	.string "catch POKéMON, and I ran out.\p"
	.string "That's why you can never have too\n"
	.string "many POKé BALLS.$"

ViridianForest_Text_AvoidGrassyAreasWhenWeak::
	.string "TRAINER TIPS\p"
	.string "If your POKéMON are weak and you\n"
	.string "want to avoid battles, stay away\l"
	.string "from grassy areas!$"

ViridianForest_Text_UseAntidoteForPoison::
	.string "For poison, use ANTIDOTE!\n"
	.string "Get it at POKéMON MARTS!$"

ViridianForest_Text_ContactOakViaPCToRatePokedex::
	.string "TRAINER TIPS\p"
	.string "Contact PROF. OAK via a PC to\n"
	.string "get your POKéDEX evaluated!$"

ViridianForest_Text_CantCatchOwnedMons::
	.string "TRAINER TIPS\p"
	.string "You can't catch a POKéMON that\n"
	.string "belongs to someone else.\p"
	.string "Throw POKé BALLS only at wild\n"
	.string "POKéMON to catch them!$"

ViridianForest_Text_WeakenMonsBeforeCapture::
	.string "TRAINER TIPS\p"
	.string "Weaken POKéMON before attempting\n"
	.string "capture!\p"
	.string "When healthy, they may escape!$"

ViridianForest_Text_LeavingViridianForest::
	.string "LEAVING VIRIDIAN FOREST\n"
	.string "PEWTER CITY AHEAD$"

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
ViridianForest_Frlg_EventScript_DexArceusBug::
	lockall
	msgbox ViridianForest_Frlg_Text_DexArceusBugIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ARCEUS_BUG, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ARCEUS_BUG, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ARCEUS_BUG
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, ViridianForest_Frlg_EventScript_DexArceusBugSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, ViridianForest_Frlg_EventScript_DexArceusBugSome
	releaseall
	end

ViridianForest_Frlg_EventScript_DexArceusBugSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ARCEUS_BUG
	setflag FLAG_HIDE_DEX_ARCEUS_BUG
	fadescreenswapbuffers FADE_FROM_BLACK
	return

ViridianForest_Frlg_Text_DexArceusBugIntro:
	.string "ARCEUS_BUG appeared!$"

ViridianForest_Frlg_EventScript_DexArceusGrass::
	lockall
	msgbox ViridianForest_Frlg_Text_DexArceusGrassIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ARCEUS_GRASS, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ARCEUS_GRASS, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ARCEUS_GRASS
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, ViridianForest_Frlg_EventScript_DexArceusGrassSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, ViridianForest_Frlg_EventScript_DexArceusGrassSome
	releaseall
	end

ViridianForest_Frlg_EventScript_DexArceusGrassSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ARCEUS_GRASS
	setflag FLAG_HIDE_DEX_ARCEUS_GRASS
	fadescreenswapbuffers FADE_FROM_BLACK
	return

ViridianForest_Frlg_Text_DexArceusGrassIntro:
	.string "ARCEUS_GRASS appeared!$"

ViridianForest_Frlg_EventScript_DexVirizion::
	lockall
	msgbox ViridianForest_Frlg_Text_DexVirizionIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_VIRIZION, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_VIRIZION, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_VIRIZION
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, ViridianForest_Frlg_EventScript_DexVirizionSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, ViridianForest_Frlg_EventScript_DexVirizionSome
	releaseall
	end

ViridianForest_Frlg_EventScript_DexVirizionSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_VIRIZION
	setflag FLAG_HIDE_DEX_VIRIZION
	fadescreenswapbuffers FADE_FROM_BLACK
	return

ViridianForest_Frlg_Text_DexVirizionIntro:
	.string "VIRIZION appeared!$"

ViridianForest_Frlg_EventScript_DexGenesect::
	lockall
	msgbox ViridianForest_Frlg_Text_DexGenesectIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_GENESECT, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_GENESECT, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_GENESECT
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, ViridianForest_Frlg_EventScript_DexGenesectSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, ViridianForest_Frlg_EventScript_DexGenesectSome
	releaseall
	end

ViridianForest_Frlg_EventScript_DexGenesectSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GENESECT
	setflag FLAG_HIDE_DEX_GENESECT
	fadescreenswapbuffers FADE_FROM_BLACK
	return

ViridianForest_Frlg_Text_DexGenesectIntro:
	.string "GENESECT appeared!$"

ViridianForest_Frlg_EventScript_DexGenesectBurn::
	lockall
	msgbox ViridianForest_Frlg_Text_DexGenesectBurnIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_GENESECT_BURN, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_GENESECT_BURN, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_GENESECT_BURN
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, ViridianForest_Frlg_EventScript_DexGenesectBurnSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, ViridianForest_Frlg_EventScript_DexGenesectBurnSome
	releaseall
	end

ViridianForest_Frlg_EventScript_DexGenesectBurnSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GENESECT_BURN
	setflag FLAG_HIDE_DEX_GENESECT_BURN
	fadescreenswapbuffers FADE_FROM_BLACK
	return

ViridianForest_Frlg_Text_DexGenesectBurnIntro:
	.string "GENESECT_BURN appeared!$"

ViridianForest_Frlg_EventScript_DexGenesectChill::
	lockall
	msgbox ViridianForest_Frlg_Text_DexGenesectChillIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_GENESECT_CHILL, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_GENESECT_CHILL, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_GENESECT_CHILL
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, ViridianForest_Frlg_EventScript_DexGenesectChillSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, ViridianForest_Frlg_EventScript_DexGenesectChillSome
	releaseall
	end

ViridianForest_Frlg_EventScript_DexGenesectChillSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GENESECT_CHILL
	setflag FLAG_HIDE_DEX_GENESECT_CHILL
	fadescreenswapbuffers FADE_FROM_BLACK
	return

ViridianForest_Frlg_Text_DexGenesectChillIntro:
	.string "GENESECT_CHILL appeared!$"

ViridianForest_Frlg_EventScript_DexGenesectDouse::
	lockall
	msgbox ViridianForest_Frlg_Text_DexGenesectDouseIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_GENESECT_DOUSE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_GENESECT_DOUSE, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_GENESECT_DOUSE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, ViridianForest_Frlg_EventScript_DexGenesectDouseSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, ViridianForest_Frlg_EventScript_DexGenesectDouseSome
	releaseall
	end

ViridianForest_Frlg_EventScript_DexGenesectDouseSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GENESECT_DOUSE
	setflag FLAG_HIDE_DEX_GENESECT_DOUSE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

ViridianForest_Frlg_Text_DexGenesectDouseIntro:
	.string "GENESECT_DOUSE appeared!$"

ViridianForest_Frlg_EventScript_DexGenesectShock::
	lockall
	msgbox ViridianForest_Frlg_Text_DexGenesectShockIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_GENESECT_SHOCK, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_GENESECT_SHOCK, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_GENESECT_SHOCK
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, ViridianForest_Frlg_EventScript_DexGenesectShockSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, ViridianForest_Frlg_EventScript_DexGenesectShockSome
	releaseall
	end

ViridianForest_Frlg_EventScript_DexGenesectShockSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GENESECT_SHOCK
	setflag FLAG_HIDE_DEX_GENESECT_SHOCK
	fadescreenswapbuffers FADE_FROM_BLACK
	return

ViridianForest_Frlg_Text_DexGenesectShockIntro:
	.string "GENESECT_SHOCK appeared!$"

ViridianForest_Frlg_EventScript_DexXerneasNeutral::
	lockall
	msgbox ViridianForest_Frlg_Text_DexXerneasNeutralIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_XERNEAS_NEUTRAL, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_XERNEAS_NEUTRAL, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_XERNEAS_NEUTRAL
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, ViridianForest_Frlg_EventScript_DexXerneasNeutralSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, ViridianForest_Frlg_EventScript_DexXerneasNeutralSome
	releaseall
	end

ViridianForest_Frlg_EventScript_DexXerneasNeutralSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_XERNEAS_NEUTRAL
	setflag FLAG_HIDE_DEX_XERNEAS_NEUTRAL
	fadescreenswapbuffers FADE_FROM_BLACK
	return

ViridianForest_Frlg_Text_DexXerneasNeutralIntro:
	.string "XERNEAS_NEUTRAL appeared!$"

ViridianForest_Frlg_EventScript_DexKartana::
	lockall
	msgbox ViridianForest_Frlg_Text_DexKartanaIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_KARTANA, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_KARTANA, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_KARTANA
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, ViridianForest_Frlg_EventScript_DexKartanaSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, ViridianForest_Frlg_EventScript_DexKartanaSome
	releaseall
	end

ViridianForest_Frlg_EventScript_DexKartanaSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_KARTANA
	setflag FLAG_HIDE_DEX_KARTANA
	fadescreenswapbuffers FADE_FROM_BLACK
	return

ViridianForest_Frlg_Text_DexKartanaIntro:
	.string "KARTANA appeared!$"

ViridianForest_Frlg_EventScript_DexEnamorusIncarnate::
	lockall
	msgbox ViridianForest_Frlg_Text_DexEnamorusIncarnateIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ENAMORUS_INCARNATE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ENAMORUS_INCARNATE, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ENAMORUS_INCARNATE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, ViridianForest_Frlg_EventScript_DexEnamorusIncarnateSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, ViridianForest_Frlg_EventScript_DexEnamorusIncarnateSome
	releaseall
	end

ViridianForest_Frlg_EventScript_DexEnamorusIncarnateSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ENAMORUS_INCARNATE
	setflag FLAG_HIDE_DEX_ENAMORUS_INCARNATE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

ViridianForest_Frlg_Text_DexEnamorusIncarnateIntro:
	.string "ENAMORUS_INCARNATE appeared!$"

ViridianForest_Frlg_EventScript_DexOgerponCornerstone::
	lockall
	msgbox ViridianForest_Frlg_Text_DexOgerponCornerstoneIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_OGERPON_CORNERSTONE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_OGERPON_CORNERSTONE, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_OGERPON_CORNERSTONE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, ViridianForest_Frlg_EventScript_DexOgerponCornerstoneSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, ViridianForest_Frlg_EventScript_DexOgerponCornerstoneSome
	releaseall
	end

ViridianForest_Frlg_EventScript_DexOgerponCornerstoneSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_OGERPON_CORNERSTONE
	setflag FLAG_HIDE_DEX_OGERPON_CORNERSTONE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

ViridianForest_Frlg_Text_DexOgerponCornerstoneIntro:
	.string "OGERPON_CORNERSTONE appeared!$"

ViridianForest_Frlg_EventScript_DexOgerponCornerstoneTera::
	lockall
	msgbox ViridianForest_Frlg_Text_DexOgerponCornerstoneTeraIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_OGERPON_CORNERSTONE_TERA, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_OGERPON_CORNERSTONE_TERA, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_OGERPON_CORNERSTONE_TERA
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, ViridianForest_Frlg_EventScript_DexOgerponCornerstoneTeraSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, ViridianForest_Frlg_EventScript_DexOgerponCornerstoneTeraSome
	releaseall
	end

ViridianForest_Frlg_EventScript_DexOgerponCornerstoneTeraSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_OGERPON_CORNERSTONE_TERA
	setflag FLAG_HIDE_DEX_OGERPON_CORNERSTONE_TERA
	fadescreenswapbuffers FADE_FROM_BLACK
	return

ViridianForest_Frlg_Text_DexOgerponCornerstoneTeraIntro:
	.string "OGERPON_CORNERSTONE_TERA appeared!$"

ViridianForest_Frlg_EventScript_DexOgerponHearthflame::
	lockall
	msgbox ViridianForest_Frlg_Text_DexOgerponHearthflameIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_OGERPON_HEARTHFLAME, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_OGERPON_HEARTHFLAME, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_OGERPON_HEARTHFLAME
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, ViridianForest_Frlg_EventScript_DexOgerponHearthflameSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, ViridianForest_Frlg_EventScript_DexOgerponHearthflameSome
	releaseall
	end

ViridianForest_Frlg_EventScript_DexOgerponHearthflameSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_OGERPON_HEARTHFLAME
	setflag FLAG_HIDE_DEX_OGERPON_HEARTHFLAME
	fadescreenswapbuffers FADE_FROM_BLACK
	return

ViridianForest_Frlg_Text_DexOgerponHearthflameIntro:
	.string "OGERPON_HEARTHFLAME appeared!$"

ViridianForest_Frlg_EventScript_DexOgerponHearthflameTera::
	lockall
	msgbox ViridianForest_Frlg_Text_DexOgerponHearthflameTeraIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_OGERPON_HEARTHFLAME_TERA, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_OGERPON_HEARTHFLAME_TERA, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_OGERPON_HEARTHFLAME_TERA
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, ViridianForest_Frlg_EventScript_DexOgerponHearthflameTeraSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, ViridianForest_Frlg_EventScript_DexOgerponHearthflameTeraSome
	releaseall
	end

ViridianForest_Frlg_EventScript_DexOgerponHearthflameTeraSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_OGERPON_HEARTHFLAME_TERA
	setflag FLAG_HIDE_DEX_OGERPON_HEARTHFLAME_TERA
	fadescreenswapbuffers FADE_FROM_BLACK
	return

ViridianForest_Frlg_Text_DexOgerponHearthflameTeraIntro:
	.string "OGERPON_HEARTHFLAME_TERA appeared!$"

ViridianForest_Frlg_EventScript_DexOgerponTeal::
	lockall
	msgbox ViridianForest_Frlg_Text_DexOgerponTealIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_OGERPON_TEAL, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_OGERPON_TEAL, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_OGERPON_TEAL
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, ViridianForest_Frlg_EventScript_DexOgerponTealSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, ViridianForest_Frlg_EventScript_DexOgerponTealSome
	releaseall
	end

ViridianForest_Frlg_EventScript_DexOgerponTealSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_OGERPON_TEAL
	setflag FLAG_HIDE_DEX_OGERPON_TEAL
	fadescreenswapbuffers FADE_FROM_BLACK
	return

ViridianForest_Frlg_Text_DexOgerponTealIntro:
	.string "OGERPON_TEAL appeared!$"

ViridianForest_Frlg_EventScript_DexOgerponTealTera::
	lockall
	msgbox ViridianForest_Frlg_Text_DexOgerponTealTeraIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_OGERPON_TEAL_TERA, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_OGERPON_TEAL_TERA, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_OGERPON_TEAL_TERA
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, ViridianForest_Frlg_EventScript_DexOgerponTealTeraSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, ViridianForest_Frlg_EventScript_DexOgerponTealTeraSome
	releaseall
	end

ViridianForest_Frlg_EventScript_DexOgerponTealTeraSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_OGERPON_TEAL_TERA
	setflag FLAG_HIDE_DEX_OGERPON_TEAL_TERA
	fadescreenswapbuffers FADE_FROM_BLACK
	return

ViridianForest_Frlg_Text_DexOgerponTealTeraIntro:
	.string "OGERPON_TEAL_TERA appeared!$"

ViridianForest_Frlg_EventScript_DexOgerponWellspring::
	lockall
	msgbox ViridianForest_Frlg_Text_DexOgerponWellspringIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_OGERPON_WELLSPRING, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_OGERPON_WELLSPRING, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_OGERPON_WELLSPRING
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, ViridianForest_Frlg_EventScript_DexOgerponWellspringSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, ViridianForest_Frlg_EventScript_DexOgerponWellspringSome
	releaseall
	end

ViridianForest_Frlg_EventScript_DexOgerponWellspringSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_OGERPON_WELLSPRING
	setflag FLAG_HIDE_DEX_OGERPON_WELLSPRING
	fadescreenswapbuffers FADE_FROM_BLACK
	return

ViridianForest_Frlg_Text_DexOgerponWellspringIntro:
	.string "OGERPON_WELLSPRING appeared!$"

ViridianForest_Frlg_EventScript_DexOgerponWellspringTera::
	lockall
	msgbox ViridianForest_Frlg_Text_DexOgerponWellspringTeraIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_OGERPON_WELLSPRING_TERA, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_OGERPON_WELLSPRING_TERA, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_OGERPON_WELLSPRING_TERA
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, ViridianForest_Frlg_EventScript_DexOgerponWellspringTeraSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, ViridianForest_Frlg_EventScript_DexOgerponWellspringTeraSome
	releaseall
	end

ViridianForest_Frlg_EventScript_DexOgerponWellspringTeraSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_OGERPON_WELLSPRING_TERA
	setflag FLAG_HIDE_DEX_OGERPON_WELLSPRING_TERA
	fadescreenswapbuffers FADE_FROM_BLACK
	return

ViridianForest_Frlg_Text_DexOgerponWellspringTeraIntro:
	.string "OGERPON_WELLSPRING_TERA appeared!$"

@ <<< Dex completa <<<
