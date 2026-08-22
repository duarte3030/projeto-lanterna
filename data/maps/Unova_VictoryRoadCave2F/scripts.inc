@ VictoryRoadCave2F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_VictoryRoadCave2F_MapScripts::
	.byte 0

Unova_VictoryRoadCave2F_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_ACE_TRAINERM_VICTORY_ROAD_INT_2, Unova_VictoryRoadCave2F_Text_AceTrainerMVictoryRoadCave2FSeenText, Unova_VictoryRoadCave2F_Text_AceTrainerMVictoryRoadCave2FBeatenText
	end

Unova_VictoryRoadCave2F_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_ACE_TRAINERF_VICTORY_ROAD_INT_1, Unova_VictoryRoadCave2F_Text_AceTrainerFVictoryRoadCave2FSeenText, Unova_VictoryRoadCave2F_Text_AceTrainerFVictoryRoadCave2FBeatenText
	end

Unova_VictoryRoadCave2F_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_PKMN_RANGERM_VICTORY_ROAD_INT, Unova_VictoryRoadCave2F_Text_PkmnRangerMVictoryRoadCave2FSeenText, Unova_VictoryRoadCave2F_Text_PkmnRangerMVictoryRoadCave2FBeatenText
	end

Unova_VictoryRoadCave2F_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_PKMN_RANGERF_VICTORY_ROAD_INT, Unova_VictoryRoadCave2F_Text_PkmnRangerFVictoryRoadCave2FSeenText, Unova_VictoryRoadCave2F_Text_PkmnRangerFVictoryRoadCave2FBeatenText
	end

Unova_VictoryRoadCave2F_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_VETERANM_VICTORY_ROAD_INT_2, Unova_VictoryRoadCave2F_Text_VeteranMVictoryRoadCave2FSeenText, Unova_VictoryRoadCave2F_Text_VeteranMVictoryRoadCave2FBeatenText
	end

Unova_VictoryRoadCave2F_EventScript_Lider10::
	trainerbattle_single TRAINER_UNOVA_BACKPACKERM_VICTORY_ROAD_INT, Unova_VictoryRoadCave2F_Text_BackpackerMVictoryRoadCave2FSeenText, Unova_VictoryRoadCave2F_Text_BackpackerMVictoryRoadCave2FBeatenText
	end


Unova_VictoryRoadCave2F_Text_AceTrainerMVictoryRoadCave2FSeenText::
	.string "It's not enough for"
	.string "\nme just to be"
	.string "\ptogether with"
	.string "\nPOKéMON! I want to"
	.string "\lwin!$"

Unova_VictoryRoadCave2F_Text_AceTrainerMVictoryRoadCave2FBeatenText::
	.string "How… How could you"
	.string "\ndefeat me this"
	.string "\lutterly?$"

Unova_VictoryRoadCave2F_Text_AceTrainerFVictoryRoadCave2FSeenText::
	.string "Our unity won't be"
	.string "\nbested by anyone!$"

Unova_VictoryRoadCave2F_Text_AceTrainerFVictoryRoadCave2FBeatenText::
	.string "We couldn't win…"
	.string "\nbut that's alright.$"

Unova_VictoryRoadCave2F_Text_PkmnRangerMVictoryRoadCave2FSeenText::
	.string "Behold the blind-"
	.string "\ning brilliance of"
	.string "\lmy many BADGEs!$"

Unova_VictoryRoadCave2F_Text_PkmnRangerMVictoryRoadCave2FBeatenText::
	.string "Your skill is too"
	.string "\nbrilliant to"
	.string "\lbehold!$"

Unova_VictoryRoadCave2F_Text_PkmnRangerFVictoryRoadCave2FSeenText::
	.string "Something about"
	.string "\nyou reminds me of"
	.string "\pthat trainer from"
	.string "\nyears ago…$"

Unova_VictoryRoadCave2F_Text_PkmnRangerFVictoryRoadCave2FBeatenText::
	.string "Yes! That mix of"
	.string "\nkindness and power"
	.string "\pis just like that"
	.string "\ntrainer!$"

Unova_VictoryRoadCave2F_Text_VeteranMVictoryRoadCave2FSeenText::
	.string "The endless cycle"
	.string "\nof wins and"
	.string "\plosses… Will it"
	.string "\nalways continue?$"

Unova_VictoryRoadCave2F_Text_VeteranMVictoryRoadCave2FBeatenText::
	.string "Every win and loss"
	.string "\nis a precious"
	.string "\lmemory.$"

Unova_VictoryRoadCave2F_Text_BackpackerMVictoryRoadCave2FSeenText::
	.string "I'm gonna numb you"
	.string "\nand your POKéMON!$"

Unova_VictoryRoadCave2F_Text_BackpackerMVictoryRoadCave2FBeatenText::
	.string "Unbelievable! I"
	.string "\nwas the one struck"
	.string "\lnumb…$"

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
Unova_VictoryRoadCave2F_EventScript_DexVirizion::
	lockall
	msgbox Unova_VictoryRoadCave2F_Text_DexVirizionIntro, MSGBOX_DEFAULT
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
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_VictoryRoadCave2F_EventScript_DexVirizionSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_VictoryRoadCave2F_EventScript_DexVirizionSome
	releaseall
	end

Unova_VictoryRoadCave2F_EventScript_DexVirizionSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_VIRIZION
	setflag FLAG_HIDE_DEX_VIRIZION
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_VictoryRoadCave2F_Text_DexVirizionIntro:
	.string "VIRIZION appeared!$"

Unova_VictoryRoadCave2F_EventScript_DexGreatTusk::
	lockall
	msgbox Unova_VictoryRoadCave2F_Text_DexGreatTuskIntro, MSGBOX_DEFAULT
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
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_VictoryRoadCave2F_EventScript_DexGreatTuskSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_VictoryRoadCave2F_EventScript_DexGreatTuskSome
	releaseall
	end

Unova_VictoryRoadCave2F_EventScript_DexGreatTuskSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GREAT_TUSK
	setflag FLAG_HIDE_DEX_GREAT_TUSK
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_VictoryRoadCave2F_Text_DexGreatTuskIntro:
	.string "GREAT_TUSK appeared!$"

Unova_VictoryRoadCave2F_EventScript_DexScreamTail::
	lockall
	msgbox Unova_VictoryRoadCave2F_Text_DexScreamTailIntro, MSGBOX_DEFAULT
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
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_VictoryRoadCave2F_EventScript_DexScreamTailSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_VictoryRoadCave2F_EventScript_DexScreamTailSome
	releaseall
	end

Unova_VictoryRoadCave2F_EventScript_DexScreamTailSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_SCREAM_TAIL
	setflag FLAG_HIDE_DEX_SCREAM_TAIL
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_VictoryRoadCave2F_Text_DexScreamTailIntro:
	.string "SCREAM_TAIL appeared!$"

Unova_VictoryRoadCave2F_EventScript_DexBruteBonnet::
	lockall
	msgbox Unova_VictoryRoadCave2F_Text_DexBruteBonnetIntro, MSGBOX_DEFAULT
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
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_VictoryRoadCave2F_EventScript_DexBruteBonnetSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_VictoryRoadCave2F_EventScript_DexBruteBonnetSome
	releaseall
	end

Unova_VictoryRoadCave2F_EventScript_DexBruteBonnetSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_BRUTE_BONNET
	setflag FLAG_HIDE_DEX_BRUTE_BONNET
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_VictoryRoadCave2F_Text_DexBruteBonnetIntro:
	.string "BRUTE_BONNET appeared!$"

Unova_VictoryRoadCave2F_EventScript_DexFlutterMane::
	lockall
	msgbox Unova_VictoryRoadCave2F_Text_DexFlutterManeIntro, MSGBOX_DEFAULT
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
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_VictoryRoadCave2F_EventScript_DexFlutterManeSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_VictoryRoadCave2F_EventScript_DexFlutterManeSome
	releaseall
	end

Unova_VictoryRoadCave2F_EventScript_DexFlutterManeSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_FLUTTER_MANE
	setflag FLAG_HIDE_DEX_FLUTTER_MANE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_VictoryRoadCave2F_Text_DexFlutterManeIntro:
	.string "FLUTTER_MANE appeared!$"

Unova_VictoryRoadCave2F_EventScript_DexSlitherWing::
	lockall
	msgbox Unova_VictoryRoadCave2F_Text_DexSlitherWingIntro, MSGBOX_DEFAULT
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
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_VictoryRoadCave2F_EventScript_DexSlitherWingSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_VictoryRoadCave2F_EventScript_DexSlitherWingSome
	releaseall
	end

Unova_VictoryRoadCave2F_EventScript_DexSlitherWingSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_SLITHER_WING
	setflag FLAG_HIDE_DEX_SLITHER_WING
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_VictoryRoadCave2F_Text_DexSlitherWingIntro:
	.string "SLITHER_WING appeared!$"

Unova_VictoryRoadCave2F_EventScript_DexSandyShocks::
	lockall
	msgbox Unova_VictoryRoadCave2F_Text_DexSandyShocksIntro, MSGBOX_DEFAULT
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
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_VictoryRoadCave2F_EventScript_DexSandyShocksSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_VictoryRoadCave2F_EventScript_DexSandyShocksSome
	releaseall
	end

Unova_VictoryRoadCave2F_EventScript_DexSandyShocksSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_SANDY_SHOCKS
	setflag FLAG_HIDE_DEX_SANDY_SHOCKS
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_VictoryRoadCave2F_Text_DexSandyShocksIntro:
	.string "SANDY_SHOCKS appeared!$"

Unova_VictoryRoadCave2F_EventScript_DexRoaringMoon::
	lockall
	msgbox Unova_VictoryRoadCave2F_Text_DexRoaringMoonIntro, MSGBOX_DEFAULT
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
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_VictoryRoadCave2F_EventScript_DexRoaringMoonSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_VictoryRoadCave2F_EventScript_DexRoaringMoonSome
	releaseall
	end

Unova_VictoryRoadCave2F_EventScript_DexRoaringMoonSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ROARING_MOON
	setflag FLAG_HIDE_DEX_ROARING_MOON
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_VictoryRoadCave2F_Text_DexRoaringMoonIntro:
	.string "ROARING_MOON appeared!$"

Unova_VictoryRoadCave2F_EventScript_DexWalkingWake::
	lockall
	msgbox Unova_VictoryRoadCave2F_Text_DexWalkingWakeIntro, MSGBOX_DEFAULT
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
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_VictoryRoadCave2F_EventScript_DexWalkingWakeSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_VictoryRoadCave2F_EventScript_DexWalkingWakeSome
	releaseall
	end

Unova_VictoryRoadCave2F_EventScript_DexWalkingWakeSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_WALKING_WAKE
	setflag FLAG_HIDE_DEX_WALKING_WAKE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_VictoryRoadCave2F_Text_DexWalkingWakeIntro:
	.string "WALKING_WAKE appeared!$"

Unova_VictoryRoadCave2F_EventScript_DexGougingFire::
	lockall
	msgbox Unova_VictoryRoadCave2F_Text_DexGougingFireIntro, MSGBOX_DEFAULT
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
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_VictoryRoadCave2F_EventScript_DexGougingFireSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_VictoryRoadCave2F_EventScript_DexGougingFireSome
	releaseall
	end

Unova_VictoryRoadCave2F_EventScript_DexGougingFireSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GOUGING_FIRE
	setflag FLAG_HIDE_DEX_GOUGING_FIRE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_VictoryRoadCave2F_Text_DexGougingFireIntro:
	.string "GOUGING_FIRE appeared!$"

Unova_VictoryRoadCave2F_EventScript_DexRagingBolt::
	lockall
	msgbox Unova_VictoryRoadCave2F_Text_DexRagingBoltIntro, MSGBOX_DEFAULT
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
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_VictoryRoadCave2F_EventScript_DexRagingBoltSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_VictoryRoadCave2F_EventScript_DexRagingBoltSome
	releaseall
	end

Unova_VictoryRoadCave2F_EventScript_DexRagingBoltSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_RAGING_BOLT
	setflag FLAG_HIDE_DEX_RAGING_BOLT
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_VictoryRoadCave2F_Text_DexRagingBoltIntro:
	.string "RAGING_BOLT appeared!$"

@ <<< Dex completa <<<
