Route215_Access_MapScripts::
	.byte 0

Route215_Access_EventScript_Fisherman::
	msgbox Route215_Access_Text_Fisherman, MSGBOX_NPC
	end

Route215_Access_EventScript_Picnicker::
	msgbox Route215_Access_Text_Picnicker, MSGBOX_NPC
	end

Route215_Access_Text_Fisherman:
	.string "The waters out on ROUTE 215 are\n"
	.string "great for fishing.$"

Route215_Access_Text_Picnicker:
	.string "I always stop here to rest before\n"
	.string "heading into VEILSTONE.$"
