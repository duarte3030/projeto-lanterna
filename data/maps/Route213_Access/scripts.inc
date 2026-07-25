Route213_Access_MapScripts::
	.byte 0

Route213_Access_EventScript_Fisherman::
	msgbox Route213_Access_Text_Fisherman, MSGBOX_NPC
	end

Route213_Access_EventScript_Tourist::
	msgbox Route213_Access_Text_Tourist, MSGBOX_NPC
	end

Route213_Access_Text_Fisherman:
	.string "PASTORIA CITY has some of the best\n"
	.string "fishing spots around.$"

Route213_Access_Text_Tourist:
	.string "I heard there's a huge marsh near\n"
	.string "here. I can't wait to see it!$"
