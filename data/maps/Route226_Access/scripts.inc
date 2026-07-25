Route226_Access_MapScripts::
	.byte 0

Route226_Access_EventScript_Sailor::
	msgbox Route226_Access_Text_Sailor, MSGBOX_NPC
	end

Route226_Access_EventScript_Beauty::
	msgbox Route226_Access_Text_Beauty, MSGBOX_NPC
	end

Route226_Access_Text_Sailor:
	.string "This stretch of coast leads right\n"
	.string "into the SURVIVAL AREA.$"

Route226_Access_Text_Beauty:
	.string "The sea breeze here is just\n"
	.string "wonderful, don't you think?$"
