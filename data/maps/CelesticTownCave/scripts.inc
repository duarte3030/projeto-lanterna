CelesticTownCave_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, CelesticTownCave_OnTransition
	.byte 0

CelesticTownCave_EventScript_Cyrus::
	msgbox CelesticTownCave_Text_Cyrus, MSGBOX_NPC
	end

CelesticTownCave_Text_Cyrus:
	.string "Cyrus: Well? Am I wrong?\nIf you feel that way, challenge me.$"

CelesticTownCave_EventScript_Elder::
	msgbox CelesticTownCave_Text_Elder, MSGBOX_NPC
	end

CelesticTownCave_Text_Elder:
	.string "That cave painting isn't protected\nsimply because it's old.\pWe've preserved it because we value\nthe memories that it represents.\pIt is a legacy of people and Pokémon\nbeyond measure.\pA man who fails to understand that...\nWhat world could he dream of?$"

@ ponytail: portao de NPC de cena com a flag RECALCULADA a cada entrada.
@ Acende sempre e so apaga se o marco ja caiu, entao nao depende de
@ linha nenhuma em new_game.inc e save antiga se comporta igual a nova.
CelesticTownCave_OnTransition:
	setflag FLAG_SINNOH_ESCONDE_CELESTIC_TOWN_CAVE_ELDER
	call_if_set FLAG_GALACTICA_CELESTIC, CelesticTownCave_EventScript_Mostra_CELESTIC_TOWN_CAVE_ELDER
	setflag FLAG_SINNOH_ESCONDE_CELESTIC_TOWN_CAVE_CYNTHIA
	call_if_set FLAG_GALACTICA_CELESTIC, CelesticTownCave_EventScript_Mostra_CELESTIC_TOWN_CAVE_CYNTHIA
	end

CelesticTownCave_EventScript_Mostra_CELESTIC_TOWN_CAVE_ELDER::
	clearflag FLAG_SINNOH_ESCONDE_CELESTIC_TOWN_CAVE_ELDER
	return

CelesticTownCave_EventScript_Mostra_CELESTIC_TOWN_CAVE_CYNTHIA::
	clearflag FLAG_SINNOH_ESCONDE_CELESTIC_TOWN_CAVE_CYNTHIA
	return
