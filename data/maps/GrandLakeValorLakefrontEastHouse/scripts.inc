GrandLakeValorLakefrontEastHouse_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, GrandLakeValorLakefrontEastHouse_OnTransition
	.byte 0

GrandLakeValorLakefrontEastHouse_EventScript_Beauty::
	msgbox GrandLakeValorLakefrontEastHouse_Text_Beauty, MSGBOX_NPC
	end

GrandLakeValorLakefrontEastHouse_Text_Beauty:
	.string "Thanks for helping me out.\nHere's something for your trouble!$"

@ ponytail: portao de NPC de cena com a flag RECALCULADA a cada entrada.
@ Acende sempre e so apaga se o marco ja caiu, entao nao depende de
@ linha nenhuma em new_game.inc e save antiga se comporta igual a nova.
GrandLakeValorLakefrontEastHouse_OnTransition:
	setflag FLAG_SINNOH_ESCONDE_GRAND_LAKE_VALOR_LAKEFRONT_EAST_HOUSE_BEAUTY
	call_if_set FLAG_SINNOH_LAGO_VALOR_ESVAZIADO, GrandLakeValorLakefrontEastHouse_EventScript_Mostra_GRAND_LAKE_VALOR_LAKEFRONT_EAST_HOUSE_BEAUTY
	end

GrandLakeValorLakefrontEastHouse_EventScript_Mostra_GRAND_LAKE_VALOR_LAKEFRONT_EAST_HOUSE_BEAUTY::
	clearflag FLAG_SINNOH_ESCONDE_GRAND_LAKE_VALOR_LAKEFRONT_EAST_HOUSE_BEAUTY
	return
