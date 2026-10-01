AbandonedShip_CaptainsOffice_MapScripts::
	.byte 0

AbandonedShip_CaptainsOffice_EventScript_CaptSternAide::
	lock
	faceplayer
	goto_if_set FLAG_EXCHANGED_SCANNER, AbandonedShip_CaptainsOffice_EventScript_ThisIsSSCactus
	checkitem ITEM_SCANNER
	goto_if_eq VAR_RESULT, TRUE, AbandonedShip_CaptainsOffice_EventScript_CanYouDeliverScanner
	goto_if_set FLAG_ITEM_ABANDONED_SHIP_HIDDEN_FLOOR_ROOM_2_SCANNER, AbandonedShip_CaptainsOffice_EventScript_ThisIsSSCactus
	msgbox AbandonedShip_CaptainsOffice_Text_NoSuccessFindingScanner, MSGBOX_DEFAULT
	release
	end

AbandonedShip_CaptainsOffice_EventScript_CanYouDeliverScanner::
	msgbox AbandonedShip_CaptainsOffice_Text_OhCanYouDeliverScanner, MSGBOX_DEFAULT
	release
	end

AbandonedShip_CaptainsOffice_EventScript_ThisIsSSCactus::
	msgbox AbandonedShip_CaptainsOffice_Text_ThisIsSSCactus, MSGBOX_DEFAULT
	release
	end

AbandonedShip_CaptainsOffice_Text_NoSuccessFindingScanner:
	.string "I'm investigating this ship on behalf\n"
	.string "of CAPT. STERN.\p"
	.string "He also asked me to find a SCANNER,\n"
	.string "but I haven't had any success…$"

AbandonedShip_CaptainsOffice_Text_OhCanYouDeliverScanner:
	.string "Oh! That's a SCANNER!\p"
	.string "Listen, can I get you to deliver that\n"
	.string "to CAPT. STERN?\p"
	.string "I want to investigate this ship a\n"
	.string "little more.$"

AbandonedShip_CaptainsOffice_Text_ThisIsSSCactus:
	.string "This ship is called S.S. CACTUS.\n"
	.string "It seems to be from an earlier era.$"

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
AbandonedShip_CaptainsOffice_EventScript_DexGenesectDouse::
	lockall
	msgbox AbandonedShip_CaptainsOffice_Text_DexGenesectDouseIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_GENESECT_DOUSE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_GENESECT_DOUSE, 65
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_GENESECT_DOUSE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, AbandonedShip_CaptainsOffice_EventScript_DexGenesectDouseSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, AbandonedShip_CaptainsOffice_EventScript_DexGenesectDouseSome
	releaseall
	end

AbandonedShip_CaptainsOffice_EventScript_DexGenesectDouseSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GENESECT_DOUSE
	setflag FLAG_HIDE_DEX_GENESECT_DOUSE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

AbandonedShip_CaptainsOffice_Text_DexGenesectDouseIntro:
	.string "GENESECT_DOUSE appeared!$"

@ <<< Dex completa <<<
