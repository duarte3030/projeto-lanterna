@ RelicCastleB1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_RelicCastleB1F_MapScripts::
	.byte 0

Unova_RelicCastleB1F_EventScript_Lider1::
	trainerbattle_single TRAINER_UNOVA_PSYCHICF_RELIC_CASTLE_1, Unova_RelicCastleB1F_Text_PsychicFRelicCastleB1FSeenText, Unova_RelicCastleB1F_Text_PsychicFRelicCastleB1FBeatenText
	end


Unova_RelicCastleB1F_Text_PsychicFRelicCastleB1FSeenText::
	.string "My psychic type"
	.string "\nPOKéMON just"
	.string "\pstarted making"
	.string "\nnoises. Is that"
	.string "\pbecause we're in"
	.string "\nthe ruins… or is"
	.string "\lit because of you?$"

Unova_RelicCastleB1F_Text_PsychicFRelicCastleB1FBeatenText::
	.string "So… strong! Who"
	.string "\nare you?$"

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
Unova_RelicCastleB1F_EventScript_DexZapdosGalar::
	lockall
	msgbox Unova_RelicCastleB1F_Text_DexZapdosGalarIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ZAPDOS_GALAR, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ZAPDOS_GALAR, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ZAPDOS_GALAR
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_RelicCastleB1F_EventScript_DexZapdosGalarSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_RelicCastleB1F_EventScript_DexZapdosGalarSome
	releaseall
	end

Unova_RelicCastleB1F_EventScript_DexZapdosGalarSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ZAPDOS_GALAR
	setflag FLAG_HIDE_DEX_ZAPDOS_GALAR
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_RelicCastleB1F_Text_DexZapdosGalarIntro:
	.string "ZAPDOS_GALAR appeared!$"

Unova_RelicCastleB1F_EventScript_DexCobalion::
	lockall
	msgbox Unova_RelicCastleB1F_Text_DexCobalionIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_COBALION, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_COBALION, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_COBALION
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_RelicCastleB1F_EventScript_DexCobalionSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_RelicCastleB1F_EventScript_DexCobalionSome
	releaseall
	end

Unova_RelicCastleB1F_EventScript_DexCobalionSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_COBALION
	setflag FLAG_HIDE_DEX_COBALION
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_RelicCastleB1F_Text_DexCobalionIntro:
	.string "COBALION appeared!$"

Unova_RelicCastleB1F_EventScript_DexNaganadel::
	lockall
	msgbox Unova_RelicCastleB1F_Text_DexNaganadelIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_NAGANADEL, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_NAGANADEL, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_NAGANADEL
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_RelicCastleB1F_EventScript_DexNaganadelSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_RelicCastleB1F_EventScript_DexNaganadelSome
	releaseall
	end

Unova_RelicCastleB1F_EventScript_DexNaganadelSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_NAGANADEL
	setflag FLAG_HIDE_DEX_NAGANADEL
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_RelicCastleB1F_Text_DexNaganadelIntro:
	.string "NAGANADEL appeared!$"

Unova_RelicCastleB1F_EventScript_DexZamazentaHero::
	lockall
	msgbox Unova_RelicCastleB1F_Text_DexZamazentaHeroIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ZAMAZENTA_HERO, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ZAMAZENTA_HERO, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ZAMAZENTA_HERO
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_RelicCastleB1F_EventScript_DexZamazentaHeroSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_RelicCastleB1F_EventScript_DexZamazentaHeroSome
	releaseall
	end

Unova_RelicCastleB1F_EventScript_DexZamazentaHeroSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ZAMAZENTA_HERO
	setflag FLAG_HIDE_DEX_ZAMAZENTA_HERO
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_RelicCastleB1F_Text_DexZamazentaHeroIntro:
	.string "ZAMAZENTA_HERO appeared!$"

Unova_RelicCastleB1F_EventScript_DexEternatus::
	lockall
	msgbox Unova_RelicCastleB1F_Text_DexEternatusIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ETERNATUS, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ETERNATUS, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ETERNATUS
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_RelicCastleB1F_EventScript_DexEternatusSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_RelicCastleB1F_EventScript_DexEternatusSome
	releaseall
	end

Unova_RelicCastleB1F_EventScript_DexEternatusSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ETERNATUS
	setflag FLAG_HIDE_DEX_ETERNATUS
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_RelicCastleB1F_Text_DexEternatusIntro:
	.string "ETERNATUS appeared!$"

Unova_RelicCastleB1F_EventScript_DexKubfu::
	lockall
	msgbox Unova_RelicCastleB1F_Text_DexKubfuIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_KUBFU, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_KUBFU, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_KUBFU
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_RelicCastleB1F_EventScript_DexKubfuSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_RelicCastleB1F_EventScript_DexKubfuSome
	releaseall
	end

Unova_RelicCastleB1F_EventScript_DexKubfuSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_KUBFU
	setflag FLAG_HIDE_DEX_KUBFU
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_RelicCastleB1F_Text_DexKubfuIntro:
	.string "KUBFU appeared!$"

Unova_RelicCastleB1F_EventScript_DexUrshifuSingleStrike::
	lockall
	msgbox Unova_RelicCastleB1F_Text_DexUrshifuSingleStrikeIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_URSHIFU_SINGLE_STRIKE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_URSHIFU_SINGLE_STRIKE, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_URSHIFU_SINGLE_STRIKE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_RelicCastleB1F_EventScript_DexUrshifuSingleStrikeSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_RelicCastleB1F_EventScript_DexUrshifuSingleStrikeSome
	releaseall
	end

Unova_RelicCastleB1F_EventScript_DexUrshifuSingleStrikeSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_URSHIFU_SINGLE_STRIKE
	setflag FLAG_HIDE_DEX_URSHIFU_SINGLE_STRIKE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_RelicCastleB1F_Text_DexUrshifuSingleStrikeIntro:
	.string "URSHIFU_SINGLE_STRIKE appeared!$"

Unova_RelicCastleB1F_EventScript_DexKoraidon::
	lockall
	msgbox Unova_RelicCastleB1F_Text_DexKoraidonIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_KORAIDON, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_KORAIDON, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_KORAIDON
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_RelicCastleB1F_EventScript_DexKoraidonSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_RelicCastleB1F_EventScript_DexKoraidonSome
	releaseall
	end

Unova_RelicCastleB1F_EventScript_DexKoraidonSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_KORAIDON
	setflag FLAG_HIDE_DEX_KORAIDON
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_RelicCastleB1F_Text_DexKoraidonIntro:
	.string "KORAIDON appeared!$"

Unova_RelicCastleB1F_EventScript_DexPecharunt::
	lockall
	msgbox Unova_RelicCastleB1F_Text_DexPecharuntIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_PECHARUNT, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_PECHARUNT, 30
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_PECHARUNT
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_RelicCastleB1F_EventScript_DexPecharuntSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_RelicCastleB1F_EventScript_DexPecharuntSome
	releaseall
	end

Unova_RelicCastleB1F_EventScript_DexPecharuntSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_PECHARUNT
	setflag FLAG_HIDE_DEX_PECHARUNT
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_RelicCastleB1F_Text_DexPecharuntIntro:
	.string "PECHARUNT appeared!$"

@ <<< Dex completa <<<
