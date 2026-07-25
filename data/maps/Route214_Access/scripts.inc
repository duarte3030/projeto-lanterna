Route214_Access_MapScripts::
	.byte 0

Route214_Access_EventScript_Hiker::
	msgbox Route214_Access_Text_Hiker, MSGBOX_NPC
	end

Route214_Access_EventScript_Lass::
	msgbox Route214_Access_Text_Lass, MSGBOX_NPC
	end

Route214_Access_Text_Hiker:
	.string "VEILSTONE CITY's got that big\n"
	.string "meteorite. Worth a look!$"

Route214_Access_Text_Lass:
	.string "This path connects right up to\n"
	.string "VEILSTONE. Handy shortcut.$"
