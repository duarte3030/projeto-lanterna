FloaromaTown_Mart_MapScripts::
	.byte 0

FloaromaTown_Mart_EventScript_Cashier::
	msgbox FloaromaTown_Mart_Text_Cashier, MSGBOX_NPC
	end

FloaromaTown_Mart_EventScript_Beauty::
	msgbox FloaromaTown_Mart_Text_Beauty, MSGBOX_NPC
	end

FloaromaTown_Mart_EventScript_SchoolKid::
	msgbox FloaromaTown_Mart_Text_SchoolKid, MSGBOX_NPC
	end

FloaromaTown_Mart_Text_Cashier:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

FloaromaTown_Mart_Text_Beauty:
	.string "This MART always has fresh Berries\n"
	.string "from the fields nearby.$"

FloaromaTown_Mart_Text_SchoolKid:
	.string "I'm saving my allowance to buy\n"
	.string "some POKé BALLS here!$"
