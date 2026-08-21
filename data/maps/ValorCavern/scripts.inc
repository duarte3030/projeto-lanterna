ValorCavern_MapScripts::
	.byte 0

@ >>> Lendarios de Sinnoh (dev_scripts/lendarios_sinnoh.py) >>>
ValorCavern_EventScript_Azelf::
	lockall
	msgbox ValorCavern_Text_AzelfIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_AZELF, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_AZELF, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_VALOR_CAVERN_AZELF
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, ValorCavern_EventScript_AzelfSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, ValorCavern_EventScript_AzelfPreso
	releaseall
	end

@ ponytail: so apaga o bicho em VITORIA ou CAPTURA. Fugir, perder ou
@ ser teleportado deixa ele no mapa, senao uma bola errada tira o
@ lendario do save. Mesma regra do LUGIA e do SpearPillar_Dialga.
ValorCavern_EventScript_AzelfPreso::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_VALOR_CAVERN_AZELF
	setflag FLAG_HIDE_AZELF_SINNOH
	fadescreenswapbuffers FADE_FROM_BLACK
	return

ValorCavern_EventScript_AzelfSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_VALOR_CAVERN_AZELF
	setflag FLAG_HIDE_AZELF_SINNOH
	fadescreenswapbuffers FADE_FROM_BLACK
	msgbox ValorCavern_Text_AzelfSome, MSGBOX_DEFAULT
	return

ValorCavern_Text_AzelfIntro:
	.string "Kyuuun...$"

ValorCavern_Text_AzelfSome:
	.string "AZELF disappeared deep into\nthe cavern...$"

@ <<< Lendarios de Sinnoh <<<
