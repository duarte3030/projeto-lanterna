Route212_Access_MapScripts::
	.byte 0

Route212_Access_EventScript_Clerk::
	msgbox Route212_Access_Text_Clerk, MSGBOX_NPC
	end

Route212_Access_EventScript_Traveler::
	msgbox Route212_Access_Text_Traveler, MSGBOX_NPC
	end

Route212_Access_Text_Clerk:
	.string "HEARTHOME CITY is just up ahead.\n"
	.string "Watch your step on the stairs.$"

Route212_Access_Text_Traveler:
	.string "This passage always smells like\n"
	.string "fresh mountain air.$"
