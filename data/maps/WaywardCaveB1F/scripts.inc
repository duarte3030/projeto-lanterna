WaywardCaveB1F_MapScripts::
	.byte 0

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
WaywardCaveB1F_EventScript_DexOgerponCornerstone::
	lockall
	msgbox WaywardCaveB1F_Text_DexOgerponCornerstoneIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_OGERPON_CORNERSTONE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_OGERPON_CORNERSTONE, 65
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_OGERPON_CORNERSTONE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, WaywardCaveB1F_EventScript_DexOgerponCornerstoneSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, WaywardCaveB1F_EventScript_DexOgerponCornerstoneSome
	releaseall
	end

WaywardCaveB1F_EventScript_DexOgerponCornerstoneSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_OGERPON_CORNERSTONE
	setflag FLAG_HIDE_DEX_OGERPON_CORNERSTONE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

WaywardCaveB1F_Text_DexOgerponCornerstoneIntro:
	.string "OGERPON_CORNERSTONE appeared!$"

@ <<< Dex completa <<<
