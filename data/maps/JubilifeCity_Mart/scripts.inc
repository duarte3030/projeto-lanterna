JubilifeCity_Mart_MapScripts::
	.byte 0

JubilifeCity_Mart_EventScript_Cashier::
	msgbox JubilifeCity_Mart_Text_Cashier, MSGBOX_NPC
	end

JubilifeCity_Mart_EventScript_Guitarist::
	msgbox JubilifeCity_Mart_Text_Guitarist, MSGBOX_NPC
	end

JubilifeCity_Mart_EventScript_Pokefan::
	msgbox JubilifeCity_Mart_Text_Pokefan, MSGBOX_NPC
	end

JubilifeCity_Mart_Text_Cashier:
	.string "Welcome to the POKéMON MART!\p"
	.string "Sorry, we're not able to sell\n"
	.string "anything just yet.$"

JubilifeCity_Mart_Text_Guitarist:
	.string "I stop by here every day just to\n"
	.string "look at the new items.$"

JubilifeCity_Mart_Text_Pokefan:
	.string "This MART always has the freshest\n"
	.string "stock in all of JUBILIFE CITY.$"
