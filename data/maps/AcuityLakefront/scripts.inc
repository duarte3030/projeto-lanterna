AcuityLakefront_MapScripts::
	.byte 0

AcuityLakefront_EventScript_Hiker::
	msgbox AcuityLakefront_Text_Hiker, MSGBOX_NPC
	end

AcuityLakefront_EventScript_Pokefan::
	msgbox AcuityLakefront_Text_Pokefan, MSGBOX_NPC
	end

AcuityLakefront_EventScript_Lass::
	msgbox AcuityLakefront_Text_Lass, MSGBOX_NPC
	end

AcuityLakefront_EventScript_Gentleman::
	msgbox AcuityLakefront_Text_Gentleman, MSGBOX_NPC
	end

AcuityLakefront_Text_Hiker:
	.string "The snow up here never really\n"
	.string "melts. Bundle up if you're heading\l"
	.string "further north.$"

AcuityLakefront_Text_Pokefan:
	.string "SNOWPOINT CITY is just past the\n"
	.string "lake. Almost there!$"

AcuityLakefront_Text_Lass:
	.string "Brr! I love the cold, but even\n"
	.string "I need a break sometimes.$"

AcuityLakefront_Text_Gentleman:
	.string "LAKE ACUITY is said to be the\n"
	.string "calmest of the three lakes.$"

@ Historia: a guarda da Galactica no caminho do Lago Acuity.
@ Texto de pret/pokeplatinum, res/text/acuity_lakefront.json. So conversa: em
@ Platinum esses dois nao batalham, e o Lago Acuity depende da insignia de
@ Snowpoint (FLAG_INSIGNIA_SINNOH_7), que ja existe.

AcuityLakefront_EventScript_GalacticGrunt1::
	msgbox AcuityLakefront_Text_GalacticGrunt1, MSGBOX_NPC
	end

AcuityLakefront_EventScript_GalacticGrunt2::
	msgbox AcuityLakefront_Text_GalacticGrunt2, MSGBOX_NPC
	end

AcuityLakefront_Text_GalacticGrunt1:
	.string "We're here to make sure Snowpoint's\n"
	.string "Gym Leader doesn't disturb us!\p"
	.string "You're here to see the lake Pokémon,\n"
	.string "too?\p"
	.string "You must be bored to fight your\n"
	.string "way through the snow to get here...$"

AcuityLakefront_Text_GalacticGrunt2:
	.string "The Pokémon of the three lakes\n"
	.string "appear to be connected somehow.\p"
	.string "When they blew up Lake Valor, a\n"
	.string "cavern appeared in the middle of\l"
	.string "this lake!$"
