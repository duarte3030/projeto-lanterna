FloaromaMeadow_MapScripts::
	.byte 0

FloaromaMeadow_EventScript_Npc1::
	msgbox FloaromaMeadow_Text_Npc1, MSGBOX_NPC
	end

FloaromaMeadow_Text_Npc1:
	.string "Would you like to buy some Honey for\nattracting Pokémon? Just $100 each!$"

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
FloaromaMeadow_EventScript_DexShayminLand::
	lockall
	msgbox FloaromaMeadow_Text_DexShayminLandIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_SHAYMIN_LAND, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_SHAYMIN_LAND, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_SHAYMIN_LAND
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, FloaromaMeadow_EventScript_DexShayminLandSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, FloaromaMeadow_EventScript_DexShayminLandSome
	releaseall
	end

FloaromaMeadow_EventScript_DexShayminLandSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_SHAYMIN_LAND
	setflag FLAG_HIDE_DEX_SHAYMIN_LAND
	fadescreenswapbuffers FADE_FROM_BLACK
	return

FloaromaMeadow_Text_DexShayminLandIntro:
	.string "SHAYMIN_LAND appeared!$"

@ <<< Dex completa <<<
