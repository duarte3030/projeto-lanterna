Route211_West_MapScripts::
	.byte 0

Route211_West_EventScript_BirdKeeper::
	msgbox Route211_West_Text_BirdKeeper, MSGBOX_NPC
	end

Route211_West_EventScript_Hiker::
	msgbox Route211_West_Text_Hiker, MSGBOX_NPC
	end

Route211_West_EventScript_NinjaBoy::
	msgbox Route211_West_Text_NinjaBoy, MSGBOX_NPC
	end

Route211_West_Text_BirdKeeper:
	.string "Eterna City is close now.\n"
	.string "Almost through the mountain.$"

Route211_West_Text_Hiker:
	.string "Mt. Coronet splits Sinnoh\n"
	.string "right down the middle.$"

Route211_West_Text_NinjaBoy:
	.string "Heh, you found me. I like to\n"
	.string "hide in the tall grass.$"
