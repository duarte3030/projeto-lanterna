@ CasteliaTradeHouse2 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_CasteliaTradeHouse2_MapScripts::
	.byte 0



@ Placas trazidas do BW3G por dev_scripts/importa_placas_unova.py

@ troca de Pokemon do BW3G, no molde de Route2_House_Frlg (vanilla)
Unova_CasteliaTradeHouse2_EventScript_Troca::
	lock
	faceplayer
	setvar VAR_0x8008, INGAME_TRADE_UNOVA_CASTELIA_2
	call EventScript_GetInGameTradeSpeciesInfo
	goto_if_set FLAG_UNOVA_TROCA_CASTELIA_2, Unova_CasteliaTradeHouse2_EventScript_TrocaFeita
	msgbox Unova_Text_Troca1Intro, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Unova_CasteliaTradeHouse2_EventScript_TrocaNao
	call EventScript_ChooseMonForInGameTrade
	goto_if_ge VAR_0x8004, PARTY_SIZE, Unova_CasteliaTradeHouse2_EventScript_TrocaNao
	call EventScript_GetInGameTradeSpecies
	goto_if_ne VAR_RESULT, VAR_0x8009, Unova_CasteliaTradeHouse2_EventScript_TrocaErrada
	call EventScript_DoInGameTrade
	msgbox Unova_Text_Troca1Complete
	setflag FLAG_UNOVA_TROCA_CASTELIA_2
	release
	end

Unova_CasteliaTradeHouse2_EventScript_TrocaNao::
	msgbox Unova_Text_Troca1Cancel
	release
	end

Unova_CasteliaTradeHouse2_EventScript_TrocaErrada::
	msgbox Unova_Text_Troca1Wrong
	release
	end

Unova_CasteliaTradeHouse2_EventScript_TrocaFeita::
	msgbox Unova_Text_Troca1After
	release
	end
