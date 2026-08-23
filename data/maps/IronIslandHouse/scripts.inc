IronIslandHouse_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, IronIslandHouse_OnTransition
	.byte 0

IronIslandHouse_EventScript_Byron::
	msgbox IronIslandHouse_Text_Byron, MSGBOX_NPC
	end

IronIslandHouse_Text_Byron:
	.string "Byron: Hm?\nYou're in training, then?\pYou know, my son trains as hard as\nyou do.\pBut I still treat him as if he were\na child.\pIt's ridiculous, really.\nHe is a proper Gym Leader and all.\pIt's always tricky between a father\nand son, it seems.\pHumph, I've wasted your time.\nTake this as my apology!$"

@ ponytail: portao de NPC de cena com a flag RECALCULADA a cada entrada.
@ Acende sempre e so apaga se o marco ja caiu, entao nao depende de
@ linha nenhuma em new_game.inc e save antiga se comporta igual a nova.
IronIslandHouse_OnTransition:
	setflag FLAG_SINNOH_ESCONDE_IRON_ISLAND_HOUSE_BYRON
	call_if_defeated TRAINER_SINNOH_LEADER_BYRON, IronIslandHouse_EventScript_Mostra_IRON_ISLAND_HOUSE_BYRON
	end

IronIslandHouse_EventScript_Mostra_IRON_ISLAND_HOUSE_BYRON::
	clearflag FLAG_SINNOH_ESCONDE_IRON_ISLAND_HOUSE_BYRON
	return
