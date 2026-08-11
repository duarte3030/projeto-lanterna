@ DriftveilTradeHouse do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_DriftveilTradeHouse_MapScripts::
	.byte 0



@ troca de Pokemon do BW3G, no molde de Route2_House_Frlg (vanilla)
Unova_DriftveilTradeHouse_EventScript_Troca::
	lock
	faceplayer
	setvar VAR_0x8008, INGAME_TRADE_UNOVA_DRIFTVEIL
	call EventScript_GetInGameTradeSpeciesInfo
	goto_if_set FLAG_UNOVA_TROCA_DRIFTVEIL, Unova_DriftveilTradeHouse_EventScript_TrocaFeita
	msgbox Unova_Text_Troca2Intro, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Unova_DriftveilTradeHouse_EventScript_TrocaNao
	call EventScript_ChooseMonForInGameTrade
	goto_if_ge VAR_0x8004, PARTY_SIZE, Unova_DriftveilTradeHouse_EventScript_TrocaNao
	call EventScript_GetInGameTradeSpecies
	goto_if_ne VAR_RESULT, VAR_0x8009, Unova_DriftveilTradeHouse_EventScript_TrocaErrada
	call EventScript_DoInGameTrade
	msgbox Unova_Text_Troca2Complete
	setflag FLAG_UNOVA_TROCA_DRIFTVEIL
	release
	end

Unova_DriftveilTradeHouse_EventScript_TrocaNao::
	msgbox Unova_Text_Troca2Cancel
	release
	end

Unova_DriftveilTradeHouse_EventScript_TrocaErrada::
	msgbox Unova_Text_Troca2Wrong
	release
	end

Unova_DriftveilTradeHouse_EventScript_TrocaFeita::
	msgbox Unova_Text_Troca2After
	release
	end
