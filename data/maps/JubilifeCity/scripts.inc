@ Mapa de referencia de Sinnoh. O padrao usado aqui vale para os outros 132:
@ ver Pokemon Claude/SINNOH-PADRAO.md antes de escrever qualquer script novo.
@ Textos vindos de pret/pokeplatinum, em ingles, como o resto do jogo.

JubilifeCity_MapScripts::
	.byte 0

JubilifeCity_EventScript_AceTrainerF::
	msgbox JubilifeCity_Text_AceTrainerF, MSGBOX_NPC
	end

JubilifeCity_EventScript_AceTrainerM1::
	msgbox JubilifeCity_Text_AceTrainerM1, MSGBOX_NPC
	end

JubilifeCity_EventScript_SchoolKidM1::
	lock
	faceplayer
	msgbox JubilifeCity_Text_SchoolKidM1, MSGBOX_DEFAULT
	release
	end

JubilifeCity_EventScript_Twin::
	msgbox JubilifeCity_Text_Twin, MSGBOX_NPC
	end

JubilifeCity_EventScript_ExpertM1::
	lock
	faceplayer
	msgbox JubilifeCity_Text_ExpertM1, MSGBOX_DEFAULT
	release
	end

JubilifeCity_EventScript_SchoolKidM2::
	msgbox JubilifeCity_Text_SchoolKidM2, MSGBOX_NPC
	end

JubilifeCity_EventScript_ExpertM2::
	lock
	faceplayer
	msgbox JubilifeCity_Text_ExpertM2, MSGBOX_DEFAULT
	release
	end

JubilifeCity_EventScript_AceTrainerM2::
	msgbox JubilifeCity_Text_AceTrainerM2, MSGBOX_NPC
	end

JubilifeCity_EventScript_AceTrainerM3::
	msgbox JubilifeCity_Text_AceTrainerM3, MSGBOX_NPC
	end

JubilifeCity_EventScript_KidWithNds1::
	msgbox JubilifeCity_Text_KidWithNds1, MSGBOX_NPC
	end

JubilifeCity_EventScript_KidWithNds2::
	msgbox JubilifeCity_Text_KidWithNds2, MSGBOX_NPC
	end

JubilifeCity_EventScript_CitySign::
	msgbox JubilifeCity_Text_CitySign, MSGBOX_SIGN
	end

JubilifeCity_EventScript_MartSign::
	msgbox JubilifeCity_Text_MartSign, MSGBOX_SIGN
	end

JubilifeCity_EventScript_SchoolSign::
	msgbox JubilifeCity_Text_SchoolSign, MSGBOX_SIGN
	end

JubilifeCity_Text_AceTrainerF:
	.string "This city is huge... I could use it\n"
	.string "to train my legs as much as my\l"
	.string "POKéMON!$"

JubilifeCity_Text_AceTrainerM1:
	.string "Jubilife's got Trainers on every\n"
	.string "corner. Keep your guard up if you\l"
	.string "don't want to get challenged!$"

JubilifeCity_Text_SchoolKidM1:
	.string "The way you look... You're obviously\n"
	.string "a Trainer!\p"
	.string "What type of POKéMON do you like\n"
	.string "best? I bet it says a lot about you!$"

JubilifeCity_Text_Twin:
	.string "Me and my sister came all the way\n"
	.string "to JUBILIFE just to see the TV\l"
	.string "station. Isn't that exciting?$"

JubilifeCity_Text_ExpertM1:
	.string "Hello, Trainer! Do you know much\n"
	.string "about POKéMON?\p"
	.string "There's a TRAINERS' SCHOOL here in\n"
	.string "town. Even if you know a lot, you\l"
	.string "may still discover something new!$"

JubilifeCity_Text_SchoolKidM2:
	.string "I'm still practicing, but someday\n"
	.string "I'll be a great POKéMON Trainer!$"

JubilifeCity_Text_ExpertM2:
	.string "JUBILIFE CITY was built on land\n"
	.string "carved out of a mountain. The people\l"
	.string "of OREBURGH CITY helped out.\p"
	.string "Have you visited the TV station yet?\n"
	.string "You could be a star! Or at least\l"
	.string "dream of being one!$"

JubilifeCity_Text_AceTrainerM2:
	.string "I like to walk this whole city end\n"
	.string "to end. Good way to scout for tough\l"
	.string "Trainers to battle.$"

JubilifeCity_Text_AceTrainerM3:
	.string "The POKÉTCH COMPANY has its main\n"
	.string "office right here in JUBILIFE.\l"
	.string "Pretty neat, huh?$"

JubilifeCity_Text_KidWithNds1:
	.string "I'm trying to beat this game before\n"
	.string "dinner! No time to chat!$"

JubilifeCity_Text_KidWithNds2:
	.string "Wanna trade high scores sometime?$"

JubilifeCity_Text_CitySign:
	.string "JUBILIFE CITY\n"
	.string "The City of Vibrant People and\l"
	.string "POKéMON$"

JubilifeCity_Text_MartSign:
	.string "JUBILIFE CITY MART$"

JubilifeCity_Text_SchoolSign:
	.string "TRAINERS' SCHOOL$"
