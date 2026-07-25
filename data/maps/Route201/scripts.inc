Route201_MapScripts::
	.byte 0

Route201_EventScript_Cashier::
	msgbox Route201_Text_Cashier, MSGBOX_NPC
	end

Route201_EventScript_SchoolKid::
	msgbox Route201_Text_SchoolKid, MSGBOX_NPC
	end

Route201_EventScript_Lass::
	msgbox Route201_Text_Lass, MSGBOX_NPC
	end

Route201_Text_Cashier:
	.string "Hi! I work at a POKéMON Mart.\n"
	.string "Did you know a POKéMON's health\l"
	.string "is measured by Hit Points (HP)?\p"
	.string "If a POKéMON runs out of HP, it\n"
	.string "faints and can't battle anymore.$"

Route201_Text_SchoolKid:
	.string "I'm studying all about POKéMON\n"
	.string "before I start my own journey.$"

Route201_Text_Lass:
	.string "If your POKéMON's HP is getting\n"
	.string "low, you should go to a POKéMON\l"
	.string "CENTER!$"
