Route222_Access_MapScripts::
	.byte 0

Route222_Access_EventScript_Tuber::
	msgbox Route222_Access_Text_Tuber, MSGBOX_NPC
	end

Route222_Access_EventScript_Pokefan::
	msgbox Route222_Access_Text_Pokefan, MSGBOX_NPC
	end

Route222_Access_Text_Tuber:
	.string "SUNYSHORE CITY's beaches are the\n"
	.string "best place to relax!$"

Route222_Access_Text_Pokefan:
	.string "That city runs entirely on solar\n"
	.string "power. Pretty amazing, huh?$"
