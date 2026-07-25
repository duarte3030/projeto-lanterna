FightArea_MapScripts::
	.byte 0

FightArea_EventScript_Sailor::
	msgbox FightArea_Text_Sailor, MSGBOX_NPC
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
