FloaromaTown_House1_MapScripts::
	.byte 0

FloaromaTown_House1_EventScript_Breeder::
	msgbox FloaromaTown_House1_Text_Breeder, MSGBOX_NPC
	end

FloaromaTown_House1_EventScript_Twin::
	msgbox FloaromaTown_House1_Text_Twin, MSGBOX_NPC
	end

FloaromaTown_House1_EventScript_Clefairy::
	msgbox FloaromaTown_House1_Text_Clefairy, MSGBOX_NPC
	end

FloaromaTown_House1_Text_Breeder:
	.string "Berries grow well in soil like the kind\n"
	.string "we have around FLOAROMA TOWN.$"

FloaromaTown_House1_Text_Twin:
	.string "Do you think it's cute how POKéMON\n"
	.string "pluck Berries?$"

FloaromaTown_House1_Text_Clefairy:
	.string "CLEFAIRY stares back at you\n"
	.string "curiously.$"
