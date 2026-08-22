@ Treinadores de rota de IlexForest, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

IlexForest_MapScripts::
	.byte 0

IlexForest_EventScript_BugcatcherWayne::
	trainerbattle_single TRAINER_JOHTO_WAYNE, IlexForest_Text_BugcatcherWayneSeen, IlexForest_Text_BugcatcherWayneBeaten
	msgbox IlexForest_Text_BugcatcherWayneAfter, MSGBOX_AUTOCLOSE
	end

IlexForest_Text_BugcatcherWayneSeen:
	.string "Don't sneak up on me like that!\p"
	.string "You frightened a POKéMON away!$"

IlexForest_Text_BugcatcherWayneBeaten:
	.string "I hadn't seen that POKéMON before…$"

IlexForest_Text_BugcatcherWayneAfter:
	.string "A POKéMON I've never seen before\n"
	.string "fell out of the tree when I used\l"
	.string "HEADBUTT.\p"
	.string "I ought to use HEADBUTT in other\n"
	.string "places too.$"

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

IlexForest_EventScript_Sign::
	lock
	msgbox IlexForest_Text_Signpost MSGBOX_SIGN
	closemessage
	release
	end

IlexForest_Text_Signpost::
	.string "ILEX FOREST is so overgrown with\n"
	.string "trees that you can't see the sky.\p"
	.string "Please watch out for items that may\n"
	.string "have been dropped.$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

IlexForest_EventScript_Picnicker::
	lock
	faceplayer
	msgbox IlexForest_Text_Lass, MSGBOX_DEFAULT
	closemessage
	release
	end

IlexForest_Text_Lass::
	.string "Did something happen to the\n"
	.string "forest's guardian?$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

IlexForest_EventScript_Boss::
	lock
	faceplayer
	msgbox IlexForest_Text_CharcoalMasterTalkAfter, MSGBOX_DEFAULT
	closemessage
	release
	end

IlexForest_Text_CharcoalMasterTalkAfter::
	.string "Do you want to apprentice as a\n"
	.string "charcoal maker with me?\p"
	.string "You'll be first-rate in ten years!$"

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
IlexForest_EventScript_DexCelebi::
	lockall
	msgbox IlexForest_Text_DexCelebiIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_CELEBI, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_CELEBI, 30
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_CELEBI
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, IlexForest_EventScript_DexCelebiSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, IlexForest_EventScript_DexCelebiSome
	releaseall
	end

IlexForest_EventScript_DexCelebiSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_CELEBI
	setflag FLAG_HIDE_DEX_CELEBI
	fadescreenswapbuffers FADE_FROM_BLACK
	return

IlexForest_Text_DexCelebiIntro:
	.string "CELEBI appeared!$"

IlexForest_EventScript_DexTapuBulu::
	lockall
	msgbox IlexForest_Text_DexTapuBuluIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_TAPU_BULU, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_TAPU_BULU, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_TAPU_BULU
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, IlexForest_EventScript_DexTapuBuluSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, IlexForest_EventScript_DexTapuBuluSome
	releaseall
	end

IlexForest_EventScript_DexTapuBuluSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_TAPU_BULU
	setflag FLAG_HIDE_DEX_TAPU_BULU
	fadescreenswapbuffers FADE_FROM_BLACK
	return

IlexForest_Text_DexTapuBuluIntro:
	.string "TAPU_BULU appeared!$"

IlexForest_EventScript_DexZarude::
	lockall
	msgbox IlexForest_Text_DexZarudeIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ZARUDE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ZARUDE, 30
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ZARUDE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, IlexForest_EventScript_DexZarudeSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, IlexForest_EventScript_DexZarudeSome
	releaseall
	end

IlexForest_EventScript_DexZarudeSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ZARUDE
	setflag FLAG_HIDE_DEX_ZARUDE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

IlexForest_Text_DexZarudeIntro:
	.string "ZARUDE appeared!$"

IlexForest_EventScript_DexOkidogi::
	lockall
	msgbox IlexForest_Text_DexOkidogiIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_OKIDOGI, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_OKIDOGI, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_OKIDOGI
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, IlexForest_EventScript_DexOkidogiSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, IlexForest_EventScript_DexOkidogiSome
	releaseall
	end

IlexForest_EventScript_DexOkidogiSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_OKIDOGI
	setflag FLAG_HIDE_DEX_OKIDOGI
	fadescreenswapbuffers FADE_FROM_BLACK
	return

IlexForest_Text_DexOkidogiIntro:
	.string "OKIDOGI appeared!$"

IlexForest_EventScript_DexMunkidori::
	lockall
	msgbox IlexForest_Text_DexMunkidoriIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_MUNKIDORI, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_MUNKIDORI, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_MUNKIDORI
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, IlexForest_EventScript_DexMunkidoriSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, IlexForest_EventScript_DexMunkidoriSome
	releaseall
	end

IlexForest_EventScript_DexMunkidoriSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_MUNKIDORI
	setflag FLAG_HIDE_DEX_MUNKIDORI
	fadescreenswapbuffers FADE_FROM_BLACK
	return

IlexForest_Text_DexMunkidoriIntro:
	.string "MUNKIDORI appeared!$"

IlexForest_EventScript_DexFezandipiti::
	lockall
	msgbox IlexForest_Text_DexFezandipitiIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_FEZANDIPITI, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_FEZANDIPITI, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_FEZANDIPITI
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, IlexForest_EventScript_DexFezandipitiSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, IlexForest_EventScript_DexFezandipitiSome
	releaseall
	end

IlexForest_EventScript_DexFezandipitiSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_FEZANDIPITI
	setflag FLAG_HIDE_DEX_FEZANDIPITI
	fadescreenswapbuffers FADE_FROM_BLACK
	return

IlexForest_Text_DexFezandipitiIntro:
	.string "FEZANDIPITI appeared!$"

@ <<< Dex completa <<<
