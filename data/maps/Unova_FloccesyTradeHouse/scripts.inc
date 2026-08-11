@ FloccesyTradeHouse do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_FloccesyTradeHouse_MapScripts::
	.byte 0



@ troca de Pokemon do BW3G, no molde de Route2_House_Frlg (vanilla)
Unova_FloccesyTradeHouse_EventScript_Troca::
	lock
	faceplayer
	setvar VAR_0x8008, INGAME_TRADE_UNOVA_FLOCCESY
	call EventScript_GetInGameTradeSpeciesInfo
	goto_if_set FLAG_UNOVA_TROCA_FLOCCESY, Unova_FloccesyTradeHouse_EventScript_TrocaFeita
	msgbox Unova_Text_Troca4Intro, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Unova_FloccesyTradeHouse_EventScript_TrocaNao
	call EventScript_ChooseMonForInGameTrade
	goto_if_ge VAR_0x8004, PARTY_SIZE, Unova_FloccesyTradeHouse_EventScript_TrocaNao
	call EventScript_GetInGameTradeSpecies
	goto_if_ne VAR_RESULT, VAR_0x8009, Unova_FloccesyTradeHouse_EventScript_TrocaErrada
	call EventScript_DoInGameTrade
	msgbox Unova_Text_Troca4Complete
	setflag FLAG_UNOVA_TROCA_FLOCCESY
	release
	end

Unova_FloccesyTradeHouse_EventScript_TrocaNao::
	msgbox Unova_Text_Troca4Cancel
	release
	end

Unova_FloccesyTradeHouse_EventScript_TrocaErrada::
	msgbox Unova_Text_Troca4Wrong
	release
	end

Unova_FloccesyTradeHouse_EventScript_TrocaFeita::
	msgbox Unova_Text_Troca4After
	release
	end
