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

@ Historia: o grunt que corre com a bomba para o Lago Valor.
@ Texto de pret/pokeplatinum, res/text/valor_lakefront.json.

ValorLakefront_EventScript_GalacticGrunt::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_LAKE_VALOR_3, ValorLakefront_Text_GruntIntro, ValorLakefront_Text_GruntDefeat
	msgbox ValorLakefront_Text_GruntPostBattle, MSGBOX_AUTOCLOSE
	end

ValorLakefront_Text_GruntIntro:
	.string "...Pant...pant...\p"
	.string "Gweh! You were eavesdropping!\n"
	.string "I was only talking to myself!\p"
	.string "Aww, no...\n"
	.string "You're still on my tail...?\l"
	.string "The lake's within sight...\p"
	.string "You leave me no choice...\n"
	.string "My Pokémon will KO you...$"

ValorLakefront_Text_GruntDefeat:
	.string "I can't battle anymore...\n"
	.string "I'm running on fumes...$"

ValorLakefront_Text_GruntPostBattle:
	.string "I'll have to give this to the\n"
	.string "Commander...\p"
	.string "I wish...\n"
	.string "I got to use it at the lake...$"
