FightArea_MapScripts::
	.byte 0

FightArea_EventScript_Sailor::
	lock
	faceplayer
@ ponytail: par da viagem que abre em Snowpoint depois da Liga. Sem esta volta o
@ jogador ficava preso na Battle Zone, que e o mesmo bug que Johto tinha antes de
@ o marinheiro de Olivine existir.
	msgbox FightArea_Text_SailorOferece, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FightArea_EventScript_SailorRecusa
	msgbox FightArea_Text_SailorZarpa, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_SNOWPOINT_CITY, 20, 40
	waitstate
	release
	end

FightArea_EventScript_SailorRecusa::
	msgbox FightArea_Text_Sailor, MSGBOX_DEFAULT
	release
	end

FightArea_EventScript_Fisherman::
	msgbox FightArea_Text_Fisherman, MSGBOX_NPC
	end

FightArea_EventScript_Camper::
	msgbox FightArea_Text_Camper, MSGBOX_NPC
	end

FightArea_EventScript_AceTrainerM::
	msgbox FightArea_Text_AceTrainerM, MSGBOX_NPC
	end

FightArea_EventScript_AceTrainerF::
	msgbox FightArea_Text_AceTrainerF, MSGBOX_NPC
	end

FightArea_EventScript_Twin::
	msgbox FightArea_Text_Twin, MSGBOX_NPC
	end

FightArea_Text_Sailor:
	.string "Ahoy! Ships leave from the harbor\n"
	.string "near here for SNOWPOINT CITY.$"

FightArea_Text_Fisherman:
	.string "Hmm! A Super Rod is really good!\n"
	.string "Wouldn't you agree?$"

FightArea_Text_Camper:
	.string "I bring my POKéMON here to train\n"
	.string "against tough opponents.$"

FightArea_Text_AceTrainerM:
	.string "TRAINERS from all over SINNOH\n"
	.string "gather at the FIGHT AREA.$"

FightArea_Text_AceTrainerF:
	.string "I've fought here a dozen times.\n"
	.string "Still haven't won it all!$"

FightArea_Text_Twin:
	.string "My sister and I love watching the\n"
	.string "tough TRAINERS battle here!$"

FightArea_Text_SailorOferece:
	.string "Quer que eu leve voce de volta para\n"
	.string "Snowpoint City?$"

FightArea_Text_SailorZarpa:
	.string "Zarpando para Snowpoint City!$"
