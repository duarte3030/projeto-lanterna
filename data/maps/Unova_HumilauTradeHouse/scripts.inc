@ HumilauTradeHouse do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_HumilauTradeHouse_MapScripts::
	.byte 0

Unova_HumilauTradeHouse_EventScript_Npc0::
	msgbox Unova_HumilauTradeHouse_Text_HumilauTradeHouseNoPokeText, MSGBOX_NPC
	end


Unova_HumilauTradeHouse_Text_HumilauTradeHouseNoPokeText::
	.string "Hi, I'm looking to"
	.string "\ntrade POKéMON."
	.string "\pOh, you don't have"
	.string "\nany POKéMON?"
	.string "\lThat's too bad.$"

@ troca de Pokemon do BW3G, no molde de Route2_House_Frlg (vanilla)
Unova_HumilauTradeHouse_EventScript_Troca::
	lock
	faceplayer
	goto_if_unset FLAG_SYS_POKEMON_GET, Unova_HumilauTradeHouse_EventScript_TrocaSemPokemon
	setvar VAR_0x8008, INGAME_TRADE_UNOVA_HUMILAU
	call EventScript_GetInGameTradeSpeciesInfo
	goto_if_set FLAG_UNOVA_TROCA_HUMILAU, Unova_HumilauTradeHouse_EventScript_TrocaFeita
	msgbox Unova_Text_Troca2Intro, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Unova_HumilauTradeHouse_EventScript_TrocaNao
	call EventScript_ChooseMonForInGameTrade
	goto_if_ge VAR_0x8004, PARTY_SIZE, Unova_HumilauTradeHouse_EventScript_TrocaNao
	call EventScript_GetInGameTradeSpecies
	goto_if_ne VAR_RESULT, VAR_0x8009, Unova_HumilauTradeHouse_EventScript_TrocaErrada
	call EventScript_DoInGameTrade
	msgbox Unova_Text_Troca2Complete
	setflag FLAG_UNOVA_TROCA_HUMILAU
	release
	end

Unova_HumilauTradeHouse_EventScript_TrocaNao::
	msgbox Unova_Text_Troca2Cancel
	release
	end

Unova_HumilauTradeHouse_EventScript_TrocaErrada::
	msgbox Unova_Text_Troca2Wrong
	release
	end

Unova_HumilauTradeHouse_EventScript_TrocaFeita::
	msgbox Unova_Text_Troca2After
	release
	end

Unova_HumilauTradeHouse_EventScript_TrocaSemPokemon::
	msgbox Unova_HumilauTradeHouse_Text_HumilauTradeHouseNoPokeText
	release
	end

Unova_Text_Troca1Intro::
	.string "I collect POKéMON."
	.string "\nDo you have"
	.string "\l{STR_VAR_1}"
	.string "?"
	.string "\pWant to trade it"
	.string "\nfor my {STR_VAR_2}"
	.string "?$"

Unova_Text_Troca1Cancel::
	.string "You don't want to"
	.string "\ntrade? Aww…$"

Unova_Text_Troca1Wrong::
	.string "Huh? That's not"
	.string "\n{STR_VAR_1}"
	.string ". "
	.string "\lWhat a letdown…$"

Unova_Text_Troca1Complete::
	.string "Yay! I got myself"
	.string "\n{STR_VAR_1}"
	.string "!"
	.string "\lThanks!$"

Unova_Text_Troca1After::
	.string "Hi, how's my old"
	.string "\n{STR_VAR_2}"
	.string " doing?$"

Unova_Text_Troca2Intro::
	.string "Hi, I'm looking"
	.string "\nfor this POKéMON."
	.string "\pIf you have"
	.string "\n{STR_VAR_1}"
	.string ", would"
	.string "\pyou trade it for"
	.string "\nmy {STR_VAR_2}"
	.string "?$"

Unova_Text_Troca2Cancel::
	.string "You don't have"
	.string "\none either?"
	.string "\pGee, that's really"
	.string "\ndisappointing…$"

Unova_Text_Troca2Wrong::
	.string "You don't have"
	.string "\n{STR_VAR_1}"
	.string "? That's"
	.string "\ltoo bad, then.$"

Unova_Text_Troca2Complete::
	.string "Great! Thank you!"
	.string "\pI finally got"
	.string "\n{STR_VAR_1}"
	.string ".$"

Unova_Text_Troca2After::
	.string "Hi! The {STR_VAR_1}"
	.string "\nyou traded me is"
	.string "\ldoing great!$"

Unova_Text_Troca3Intro::
	.string "I've been"
	.string "\nsearching for a"
	.string "\lcertain POKéMON…"
	.string "\pDo you have"
	.string "\n{STR_VAR_1}"
	.string "?"
	.string "\pI'll trade you a"
	.string "\n{STR_VAR_2}"
	.string " for it.$"

Unova_Text_Troca3Cancel::
	.string "If you don't have"
	.string "\nit, then you're"
	.string "\lno use to me."
	.string "\pAway with you!$"

Unova_Text_Troca3Wrong::
	.string "If you don't have"
	.string "\nit, then you're"
	.string "\lno use to me."
	.string "\pAway with you!$"

Unova_Text_Troca3Complete::
	.string "Ah, yes. This is"
	.string "\nthe POKéMON I've"
	.string "\lbeen looking for.$"

Unova_Text_Troca3After::
	.string "Thank you for"
	.string "\nhelping me find"
	.string "\l{STR_VAR_1}"
	.string "."
	.string "\pMay the spirits"
	.string "\nsmile on you…$"

Unova_Text_Troca4Intro::
	.string "{STR_VAR_1}"
	.string "'s cute,"
	.string "\nbut I don't have"
	.string "\pit. Do you have"
	.string "\n{STR_VAR_1}"
	.string "?"
	.string "\pWant to trade it"
	.string "\nfor my {STR_VAR_2}"
	.string "?$"

Unova_Text_Troca4Cancel::
	.string "You don't want to"
	.string "\ntrade? Oh, darn…$"

Unova_Text_Troca4Wrong::
	.string "That's not"
	.string "\n{STR_VAR_1}"
	.string "."
	.string "\pPlease trade with"
	.string "\nme if you get one.$"

Unova_Text_Troca4Complete::
	.string "Wow! Thank you!"
	.string "\nI always wanted"
	.string "\l{STR_VAR_1}"
	.string "!$"

Unova_Text_Troca4After::
	.string "How is that"
	.string "\n{STR_VAR_2}"
	.string " I"
	.string "\ltraded you doing?"
	.string "\pYour {STR_VAR_1}"
	.string "'s"
	.string "\nso cute!$"
