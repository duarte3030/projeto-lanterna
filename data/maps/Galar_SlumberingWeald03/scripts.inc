@ Gerado por dev_scripts/mundo_galar.py (G2). Sem cena: o ponteiro de
@ map script da fonte (0x071CC20) esta anotado no censo para a fase de conteudo.

Galar_SlumberingWeald03_MapScripts::
	.byte 0

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
Galar_SlumberingWeald03_EventScript_DexGalarZacianHero::
	lockall
	msgbox Galar_SlumberingWeald03_Text_DexGalarZacianHeroIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ZACIAN_HERO, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ZACIAN_HERO, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_GALAR_ZACIAN_HERO
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Galar_SlumberingWeald03_EventScript_DexGalarZacianHeroSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Galar_SlumberingWeald03_EventScript_DexGalarZacianHeroSome
	releaseall
	end

Galar_SlumberingWeald03_EventScript_DexGalarZacianHeroSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GALAR_ZACIAN_HERO
	setflag FLAG_HIDE_DEX_GALAR_ZACIAN_HERO
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Galar_SlumberingWeald03_Text_DexGalarZacianHeroIntro:
	.string "ZACIAN_HERO appeared!$"

Galar_SlumberingWeald03_EventScript_DexGalarZamazentaHero::
	lockall
	msgbox Galar_SlumberingWeald03_Text_DexGalarZamazentaHeroIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ZAMAZENTA_HERO, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ZAMAZENTA_HERO, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_GALAR_ZAMAZENTA_HERO
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Galar_SlumberingWeald03_EventScript_DexGalarZamazentaHeroSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Galar_SlumberingWeald03_EventScript_DexGalarZamazentaHeroSome
	releaseall
	end

Galar_SlumberingWeald03_EventScript_DexGalarZamazentaHeroSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GALAR_ZAMAZENTA_HERO
	setflag FLAG_HIDE_DEX_GALAR_ZAMAZENTA_HERO
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Galar_SlumberingWeald03_Text_DexGalarZamazentaHeroIntro:
	.string "ZAMAZENTA_HERO appeared!$"

@ <<< Dex completa <<<
