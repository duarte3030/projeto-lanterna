ValorLakefront_MapScripts::
	.byte 0

ValorLakefront_EventScript_Beauty::
	msgbox ValorLakefront_Text_Beauty, MSGBOX_NPC
	end

ValorLakefront_EventScript_Tourist::
	msgbox ValorLakefront_Text_Tourist, MSGBOX_NPC
	end

ValorLakefront_EventScript_Pokefan::
	msgbox ValorLakefront_Text_Pokefan, MSGBOX_NPC
	end

ValorLakefront_EventScript_RestaurantSign::
	msgbox ValorLakefront_Text_RestaurantSign, MSGBOX_SIGN
	end

ValorLakefront_Text_Beauty:
	.string "This lakefront hotel is lovely,\n"
	.string "isn't it? I could stay here\l"
	.string "forever.$"

ValorLakefront_Text_Tourist:
	.string "I heard LAKE VALOR holds a\n"
	.string "legendary POKéMON. Wish I could\l"
	.string "see it myself.$"

ValorLakefront_Text_Pokefan:
	.string "Cameramen used to film here all\n"
	.string "the time. Not so much anymore.$"

ValorLakefront_Text_RestaurantSign:
	.string "SEVEN STARS RESTAURANT\n"
	.string "Fine dining with a lake view.$"
