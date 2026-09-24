@ Route102_House: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 18.1) por dev_scripts/copia_planta_ex.py.

Route102_House_MapScripts::
	.byte 0

@ Decisão 7: a moradora (EX 0x834F632) dá a PERSIM BERRY, uma vez.
Route102_House_EventScript_PokefanF::
	lock
	faceplayer
	msgbox Route102_House_Text_LiveWithWild, MSGBOX_DEFAULT
	goto_if_set FLAG_RECEIVED_HOENNEX_ROUTE102_PERSIM_BERRY, Route102_House_EventScript_Fim
	msgbox Route102_House_Text_ThanksVisiting, MSGBOX_DEFAULT
	giveitem ITEM_PERSIM_BERRY
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_HOENNEX_ROUTE102_PERSIM_BERRY
Route102_House_EventScript_Fim::
	release
	end

Route102_House_Text_LiveWithWild:
	.string "I came out here to live with the wild\n"
	.string "POKéMON.$"

Route102_House_Text_ThanksVisiting:
	.string "Thanks for visiting, take this for your\n"
	.string "troubles.$"

