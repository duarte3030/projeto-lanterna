IronIslandIronRuins_MapScripts::
	.byte 0

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
IronIslandIronRuins_EventScript_DexZamazentaHero::
	lockall
	msgbox IronIslandIronRuins_Text_DexZamazentaHeroIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ZAMAZENTA_HERO, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ZAMAZENTA_HERO, 75
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ZAMAZENTA_HERO
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, IronIslandIronRuins_EventScript_DexZamazentaHeroSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, IronIslandIronRuins_EventScript_DexZamazentaHeroSome
	releaseall
	end

IronIslandIronRuins_EventScript_DexZamazentaHeroSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ZAMAZENTA_HERO
	setflag FLAG_HIDE_DEX_ZAMAZENTA_HERO
	fadescreenswapbuffers FADE_FROM_BLACK
	return

IronIslandIronRuins_Text_DexZamazentaHeroIntro:
	.string "ZAMAZENTA_HERO appeared!$"

@ <<< Dex completa <<<
