AcuityLakefront_MapScripts::
	.byte 0

AcuityLakefront_EventScript_Hiker::
	msgbox AcuityLakefront_Text_Hiker, MSGBOX_NPC
	end

AcuityLakefront_EventScript_Pokefan::
	msgbox AcuityLakefront_Text_Pokefan, MSGBOX_NPC
	end

AcuityLakefront_EventScript_Lass::
	msgbox AcuityLakefront_Text_Lass, MSGBOX_NPC
	end

AcuityLakefront_EventScript_Gentleman::
	msgbox AcuityLakefront_Text_Gentleman, MSGBOX_NPC
	end

AcuityLakefront_Text_Hiker:
	.string "The snow up here never really\n"
	.string "melts. Bundle up if you're heading\l"
	.string "further north.$"

AcuityLakefront_Text_Pokefan:
	.string "SNOWPOINT CITY is just past the\n"
	.string "lake. Almost there!$"

AcuityLakefront_Text_Lass:
	.string "Brr! I love the cold, but even\n"
	.string "I need a break sometimes.$"

AcuityLakefront_Text_Gentleman:
	.string "LAKE ACUITY is said to be the\n"
	.string "calmest of the three lakes.$"
