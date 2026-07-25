Route218_East_MapScripts::
	.byte 0

Route218_East_EventScript_Gentleman::
	msgbox Route218_East_Text_Gentleman, MSGBOX_NPC
	end

Route218_East_EventScript_Woman::
	msgbox Route218_East_Text_Woman, MSGBOX_NPC
	end

Route218_East_Text_Gentleman:
	.string "JUBILIFE CITY's TV station is\n"
	.string "just up ahead.$"

Route218_East_Text_Woman:
	.string "This route always has some kind\n"
	.string "of broadcast crew filming.$"
