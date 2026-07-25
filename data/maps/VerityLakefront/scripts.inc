VerityLakefront_MapScripts::
	.byte 0

VerityLakefront_EventScript_Hiker::
	msgbox VerityLakefront_Text_Hiker, MSGBOX_NPC
	end

VerityLakefront_EventScript_Pokefan::
	msgbox VerityLakefront_Text_Pokefan, MSGBOX_NPC
	end

VerityLakefront_EventScript_TrainerTipsSign::
	msgbox VerityLakefront_Text_TrainerTipsSign, MSGBOX_SIGN
	end

VerityLakefront_Text_Hiker:
	.string "LAKE VERITY's calm today. They\n"
	.string "say something stirs beneath the\l"
	.string "surface, though...$"

VerityLakefront_Text_Pokefan:
	.string "I come here just to watch the\n"
	.string "water. It's peaceful.$"

VerityLakefront_Text_TrainerTipsSign:
	.string "TRAINER TIP\n"
	.string "A POKéMON's mood can change how\l"
	.string "well it battles for you.$"
