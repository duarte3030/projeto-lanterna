MtSilver_Outside_MapScripts::
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

MtSilver_Outside_EventScript_Sign::
	msgbox MtSilver_Outside_Text_Sign, MSGBOX_SIGN
	end

MtSilver_Outside_Text_Sign::
	.string "MT. SILVER$"

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
MtSilver_Outside_EventScript_DexThundurusIncarnate::
	lockall
	msgbox MtSilver_Outside_Text_DexThundurusIncarnateIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_THUNDURUS_INCARNATE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_THUNDURUS_INCARNATE, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_THUNDURUS_INCARNATE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MtSilver_Outside_EventScript_DexThundurusIncarnateSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtSilver_Outside_EventScript_DexThundurusIncarnateSome
	releaseall
	end

MtSilver_Outside_EventScript_DexThundurusIncarnateSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_THUNDURUS_INCARNATE
	setflag FLAG_HIDE_DEX_THUNDURUS_INCARNATE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MtSilver_Outside_Text_DexThundurusIncarnateIntro:
	.string "THUNDURUS_INCARNATE appeared!$"

MtSilver_Outside_EventScript_DexCosmog::
	lockall
	msgbox MtSilver_Outside_Text_DexCosmogIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_COSMOG, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_COSMOG, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_COSMOG
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MtSilver_Outside_EventScript_DexCosmogSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtSilver_Outside_EventScript_DexCosmogSome
	releaseall
	end

MtSilver_Outside_EventScript_DexCosmogSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_COSMOG
	setflag FLAG_HIDE_DEX_COSMOG
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MtSilver_Outside_Text_DexCosmogIntro:
	.string "COSMOG appeared!$"

MtSilver_Outside_EventScript_DexSolgaleo::
	lockall
	msgbox MtSilver_Outside_Text_DexSolgaleoIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_SOLGALEO, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_SOLGALEO, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_SOLGALEO
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MtSilver_Outside_EventScript_DexSolgaleoSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtSilver_Outside_EventScript_DexSolgaleoSome
	releaseall
	end

MtSilver_Outside_EventScript_DexSolgaleoSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_SOLGALEO
	setflag FLAG_HIDE_DEX_SOLGALEO
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MtSilver_Outside_Text_DexSolgaleoIntro:
	.string "SOLGALEO appeared!$"

MtSilver_Outside_EventScript_DexLunala::
	lockall
	msgbox MtSilver_Outside_Text_DexLunalaIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_LUNALA, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_LUNALA, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_LUNALA
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MtSilver_Outside_EventScript_DexLunalaSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtSilver_Outside_EventScript_DexLunalaSome
	releaseall
	end

MtSilver_Outside_EventScript_DexLunalaSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_LUNALA
	setflag FLAG_HIDE_DEX_LUNALA
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MtSilver_Outside_Text_DexLunalaIntro:
	.string "LUNALA appeared!$"

MtSilver_Outside_EventScript_DexMiraidon::
	lockall
	msgbox MtSilver_Outside_Text_DexMiraidonIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_MIRAIDON, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_MIRAIDON, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_MIRAIDON
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MtSilver_Outside_EventScript_DexMiraidonSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtSilver_Outside_EventScript_DexMiraidonSome
	releaseall
	end

MtSilver_Outside_EventScript_DexMiraidonSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_MIRAIDON
	setflag FLAG_HIDE_DEX_MIRAIDON
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MtSilver_Outside_Text_DexMiraidonIntro:
	.string "MIRAIDON appeared!$"

@ <<< Dex completa <<<

@ >>> Porta da SILVER CAVE, copiada do Liquid Crystal (frente D, onda 2) >>>
@ A Silver Cave entra como ÁREA NOVA AO LADO do Mt. Silver (resposta 75a): este
@ mapa fica INTACTO e a área nova é uma a mais. A ligação é warp de SCRIPT, no
@ molde do marinheiro de PalletTown_Frlg, e NÃO conexão de mapa: o primário do
@ vale copiado é o gTileset_LcOutdoor e o deste mapa é o JohtoNorthEast, e
@ LoadMapFromCameraTransition (src/overworld.c:911) só recarrega o SECUNDÁRIO ao
@ atravessar, então a pé o vale desenharia o Mt. Silver com o tileset errado
@ (seção 3.1 do METODO-COPIA-CIDADES.md).
@ Warp de EVENTO também não servia: as duas bocas de caverna deste mapa, (14,3)
@ e (7,16), são as mesmas do Common_EventScript_BocaFechada (pergunta 46) e
@ estão em patamares ISOLADOS. Medido nesta árvore: a partir do Centro Pokémon
@ o jogador alcança 309 dos 1.584 tiles, e nenhum deles encosta em (14,4),
@ (7,15) ou (7,17). Abrir uma delas exigiria mexer no desenho DESTE mapa.
MtSilver_Outside_EventScript_SilverCaveGuide::
	lock
	faceplayer
	msgbox MtSilver_Outside_Text_SilverCaveGuideAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, MtSilver_Outside_EventScript_SilverCaveGuideNo
	msgbox MtSilver_Outside_Text_SilverCaveGuideGo, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	warp MAP_LC_SILVER_CAVE_OUTSIDE, 24, 21
	waitstate
	release
	end

MtSilver_Outside_EventScript_SilverCaveGuideNo::
	msgbox MtSilver_Outside_Text_SilverCaveGuideNo, MSGBOX_DEFAULT
	release
	end

MtSilver_Outside_Text_SilverCaveGuideAsk:
	.string "There's a valley on the far side of\n"
	.string "this ridge. SILVER CAVE.\p"
	.string "I can rope you over. Coming?$"

MtSilver_Outside_Text_SilverCaveGuideGo:
	.string "Then keep up, and keep quiet.$"

MtSilver_Outside_Text_SilverCaveGuideNo:
	.string "I'll be here. The ridge isn't going\n"
	.string "anywhere.$"
@ <<< Porta da SILVER CAVE <<<
