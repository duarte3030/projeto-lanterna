@ Grunts de pret/pokeplatinum (LOCALID_GRUNT_M_1/GRUNT_F/GRUNT_M_2, hidden_flag
@ FLAG_HIDE_LAKE_VALOR_GALACTIC), postos pela leva anterior sem script nem flag
@ (ficaram com "script": "0"). Texto portado agora; a cena e a flag sao a mesma
@ coisa: nascem enquanto o Saturn nao caiu na caverna do Lago Valor
@ (TRAINER_SINNOH_COMMANDER_SATURN_VALOR_CAVERN, ja batido em
@ LakeValor/scripts.inc), e somem depois. Flag nova (unica desta leva):
@ FLAG_SINNOH_LAGO_VALOR_ESVAZIADO.

LakeValorDrained_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LakeValorDrained_OnTransition
	.byte 0

LakeValorDrained_OnTransition:
	call_if_defeated TRAINER_SINNOH_COMMANDER_SATURN_VALOR_CAVERN, LakeValorDrained_EventScript_HideGalactica_lago_valor
	end

LakeValorDrained_EventScript_HideGalactica_lago_valor::
	setflag FLAG_SINNOH_LAGO_VALOR_ESVAZIADO
	return

LakeValorDrained_EventScript_GruntM1::
	msgbox LakeValorDrained_Text_GruntM1, MSGBOX_NPC
	end

LakeValorDrained_Text_GruntM1:
	.string "What do you want?\n"
	.string "You're investigating the explosion?\p"
	.string "Bah, it doesn't matter who you are.\n"
	.string "It's too late to make any\l"
	.string "difference.\p"
	.string "Things are going to get really\n"
	.string "interesting now.\p"
	.string "All the legendary Pokémon are\n"
	.string "going to be brought to our HQ in\l"
	.string "Veilstone!$"

LakeValorDrained_EventScript_GruntF::
	msgbox LakeValorDrained_Text_GruntF, MSGBOX_NPC
	end

LakeValorDrained_Text_GruntF:
	.string "Even Team Galactic has no use\n"
	.string "for MAGIKARP! Worthless, all of\l"
	.string "them!$"

LakeValorDrained_EventScript_GruntM2::
	msgbox LakeValorDrained_Text_GruntM2, MSGBOX_NPC
	end

LakeValorDrained_Text_GruntM2:
	.string "Hahaha!\n"
	.string "Next stop, Lake Verity!\p"
	.string "The closest civilization is that\n"
	.string "hick town called Twinleaf!\p"
	.string "We can roll in there completely\n"
	.string "unopposed!$"
