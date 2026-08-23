LakeVerityLowWater_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LakeVerityLowWater_OnTransition
	.byte 0

LakeVerityLowWater_EventScript_ProfRowan::
	msgbox LakeVerityLowWater_Text_ProfRowan, MSGBOX_NPC
	end

LakeVerityLowWater_Text_ProfRowan:
	.string "Rowan: Hmmm...\pNo legendary Pokémon, nothing out\nof the ordinary...\p{PLAYER}, how was Lake Valor?\nAnything to report?\pWhat? You're just going there now?\nYou've got to move faster than that!$"

LakeVerityLowWater_EventScript_Counterpart::
	msgbox LakeVerityLowWater_Text_Counterpart, MSGBOX_NPC
	end

LakeVerityLowWater_Text_Counterpart:
	.string "Lucas: Hiya, {PLAYER}!\nHow's Lake Valor?\pThere's nothing wrong here.\nThe lake is ordinary, as usual.\pThere's no legendary Pokémon,\neither...$"

@ ponytail: portao de NPC de cena com a flag RECALCULADA a cada entrada.
@ Acende sempre e so apaga se o marco ja caiu, entao nao depende de
@ linha nenhuma em new_game.inc e save antiga se comporta igual a nova.
LakeVerityLowWater_OnTransition:
	setflag FLAG_SINNOH_ESCONDE_LAKE_VERITY_LOW_WATER_PROF_ROWAN
	call_if_set FLAG_GALACTICA_CANALAVE_RIVAL, LakeVerityLowWater_EventScript_Mostra_LAKE_VERITY_LOW_WATER_PROF_ROWAN
	setflag FLAG_SINNOH_ESCONDE_LAKE_VERITY_LOW_WATER_COUNTERPART
	call_if_set FLAG_GALACTICA_CANALAVE_RIVAL, LakeVerityLowWater_EventScript_Mostra_LAKE_VERITY_LOW_WATER_COUNTERPART
	end

LakeVerityLowWater_EventScript_Mostra_LAKE_VERITY_LOW_WATER_PROF_ROWAN::
	clearflag FLAG_SINNOH_ESCONDE_LAKE_VERITY_LOW_WATER_PROF_ROWAN
	return

LakeVerityLowWater_EventScript_Mostra_LAKE_VERITY_LOW_WATER_COUNTERPART::
	clearflag FLAG_SINNOH_ESCONDE_LAKE_VERITY_LOW_WATER_COUNTERPART
	return
