@ BURNED TOWER B1F, portado de fontes-mapas/hns/data/maps/BurnedTower_B1F.
@ ponytail: RAIKOU, ENTEI e SUICUNE nao tem sprite que esta build desenha
@ (OBJ_EVENT_GFX_RAIKOU/ENTEI/SUICUNE existem no enum mas so tem entrada em
@ object_event_graphics_info_pointers.h dentro de #if IS_FRLG; usar
@ reiniciaria o jogo na tela de titulo). Igual foi feito com Dialga e Palkia
@ no Spear Pillar, a cena virou tres bg_event (sign): sem NPC visivel, so
@ cheiro/grito. No pcrystal original tambem e uma cutscene de "apareceu e
@ sumiu", entao nao perde muito nao ter sprite parado.
@ Pedra de forca portada igual ao padrao vanilla (EventScript_StrengthBoulder
@ + FLAG_TEMP_11, mesma flag que o FieryPath usa pro dele: FLAG_TEMP zera a
@ cada carregamento de mapa, reuso entre mapas diferentes e seguro).
@ Itens usam Common_EventScript_FindItem com FLAG_UNUSED_0x26A/0x26B crus
@ (flags.h esta com outro agente).
@ Nao portado: o cameo do EUSINE aqui embaixo (mesma falta de sprite do 1F) e
@ os quatro bichos de decoracao (KOFFING/MISDREAVUS/MAGMAR via
@ OBJ_EVENT_GFX_MON_BASE, que cai no fallback POKE_BALL nesta build).

BurnedTower_B1F_MapScripts::
	.byte 0

BurnedTower_B1F_EventScript_Raikou::
	lock
	playmoncry SPECIES_RAIKOU, CRY_MODE_NORMAL
	msgbox BurnedTower_B1F_Text_Raikou, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	release
	end

BurnedTower_B1F_EventScript_Entei::
	lock
	playmoncry SPECIES_ENTEI, CRY_MODE_NORMAL
	msgbox BurnedTower_B1F_Text_Entei, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	release
	end

BurnedTower_B1F_EventScript_Suicune::
	lock
	playmoncry SPECIES_SUICUNE, CRY_MODE_NORMAL
	msgbox BurnedTower_B1F_Text_Suicune, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	release
	end

BurnedTower_B1F_Text_Raikou:
	.string "A crackle of static electricity\n"
	.string "runs down your spine…\p"
	.string "Something fast and yellow leaps\n"
	.string "past in a blur. By the time you\l"
	.string "turn, RAIKOU is already gone.$"

BurnedTower_B1F_Text_Entei:
	.string "A wave of heat rolls off the\n"
	.string "scorched pillar…\p"
	.string "You catch a glimpse of ENTEI's\n"
	.string "mane before it vanishes into the\l"
	.string "shadows.$"

BurnedTower_B1F_Text_Suicune:
	.string "A cool mist drifts through the\n"
	.string "basement, though there's no\l"
	.string "water in sight…\p"
	.string "SUICUNE was here. You're sure\n"
	.string "of it.$"

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
BurnedTower_B1F_EventScript_DexRaikou::
	lockall
	msgbox BurnedTower_B1F_Text_DexRaikouIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_RAIKOU, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_RAIKOU, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_RAIKOU
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, BurnedTower_B1F_EventScript_DexRaikouSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, BurnedTower_B1F_EventScript_DexRaikouSome
	releaseall
	end

BurnedTower_B1F_EventScript_DexRaikouSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_RAIKOU
	setflag FLAG_HIDE_DEX_RAIKOU
	fadescreenswapbuffers FADE_FROM_BLACK
	return

BurnedTower_B1F_Text_DexRaikouIntro:
	.string "RAIKOU appeared!$"

BurnedTower_B1F_EventScript_DexEntei::
	lockall
	msgbox BurnedTower_B1F_Text_DexEnteiIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ENTEI, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ENTEI, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ENTEI
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, BurnedTower_B1F_EventScript_DexEnteiSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, BurnedTower_B1F_EventScript_DexEnteiSome
	releaseall
	end

BurnedTower_B1F_EventScript_DexEnteiSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ENTEI
	setflag FLAG_HIDE_DEX_ENTEI
	fadescreenswapbuffers FADE_FROM_BLACK
	return

BurnedTower_B1F_Text_DexEnteiIntro:
	.string "ENTEI appeared!$"

BurnedTower_B1F_EventScript_DexMarshadow::
	lockall
	msgbox BurnedTower_B1F_Text_DexMarshadowIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_MARSHADOW, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_MARSHADOW, 30
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_MARSHADOW
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, BurnedTower_B1F_EventScript_DexMarshadowSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, BurnedTower_B1F_EventScript_DexMarshadowSome
	releaseall
	end

BurnedTower_B1F_EventScript_DexMarshadowSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_MARSHADOW
	setflag FLAG_HIDE_DEX_MARSHADOW
	fadescreenswapbuffers FADE_FROM_BLACK
	return

BurnedTower_B1F_Text_DexMarshadowIntro:
	.string "MARSHADOW appeared!$"

BurnedTower_B1F_EventScript_DexSpectrier::
	lockall
	msgbox BurnedTower_B1F_Text_DexSpectrierIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_SPECTRIER, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_SPECTRIER, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_SPECTRIER
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, BurnedTower_B1F_EventScript_DexSpectrierSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, BurnedTower_B1F_EventScript_DexSpectrierSome
	releaseall
	end

BurnedTower_B1F_EventScript_DexSpectrierSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_SPECTRIER
	setflag FLAG_HIDE_DEX_SPECTRIER
	fadescreenswapbuffers FADE_FROM_BLACK
	return

BurnedTower_B1F_Text_DexSpectrierIntro:
	.string "SPECTRIER appeared!$"

@ <<< Dex completa <<<
