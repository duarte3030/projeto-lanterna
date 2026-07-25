Route225_Access_MapScripts::
	.byte 0

Route225_Access_EventScript_Camper::
	msgbox Route225_Access_Text_Camper, MSGBOX_NPC
	end

Route225_Access_EventScript_Hiker::
	msgbox Route225_Access_Text_Hiker, MSGBOX_NPC
	end

Route225_Access_Text_Camper:
	.string "The SURVIVAL AREA is rough terrain.\n"
	.string "Come prepared!$"

Route225_Access_Text_Hiker:
	.string "Wild POKéMON out here are tougher\n"
	.string "than most places I've been.$"
