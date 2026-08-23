LakeAcuityLowWater_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LakeAcuityLowWater_OnTransition
	.byte 0

@ ponytail: portao de NPC de cena com a flag RECALCULADA a cada entrada.
@ Acende sempre e so apaga se o marco ja caiu, entao nao depende de
@ linha nenhuma em new_game.inc e save antiga se comporta igual a nova.
LakeAcuityLowWater_OnTransition:
	setflag FLAG_SINNOH_ESCONDE_LAKE_ACUITY_LOW_WATER_RIVAL
	call_if_set FLAG_GALACTICA_CANALAVE_RIVAL, LakeAcuityLowWater_EventScript_Mostra_LAKE_ACUITY_LOW_WATER_RIVAL
	end

LakeAcuityLowWater_EventScript_Mostra_LAKE_ACUITY_LOW_WATER_RIVAL::
	clearflag FLAG_SINNOH_ESCONDE_LAKE_ACUITY_LOW_WATER_RIVAL
	return
