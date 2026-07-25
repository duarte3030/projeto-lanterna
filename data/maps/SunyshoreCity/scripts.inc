SunyshoreCity_MapScripts::
	.byte 0

SunyshoreCity_EventScript_Jasmine::
	lock
	faceplayer
	msgbox SunyshoreCity_Text_Jasmine, MSGBOX_DEFAULT
	release
	end

SunyshoreCity_EventScript_Sailor1::
	msgbox SunyshoreCity_Text_Sailor1, MSGBOX_NPC
	end

SunyshoreCity_EventScript_PokefanF::
	msgbox SunyshoreCity_Text_PokefanF, MSGBOX_NPC
	end

SunyshoreCity_EventScript_BreederF::
	msgbox SunyshoreCity_Text_BreederF, MSGBOX_NPC
	end

SunyshoreCity_EventScript_Worker::
	msgbox SunyshoreCity_Text_Worker, MSGBOX_NPC
	end

SunyshoreCity_EventScript_Sailor2::
	msgbox SunyshoreCity_Text_Sailor2, MSGBOX_NPC
	end

SunyshoreCity_Text_Jasmine:
	.string "...This city makes me feel at\n"
	.string "home somehow.\p"
	.string "It's next to the sea, and there's\n"
	.string "a lighthouse...$"

SunyshoreCity_Text_Sailor1:
	.string "The sea breeze here is the best\n"
	.string "in all of SINNOH.$"

SunyshoreCity_Text_PokefanF:
	.string "I love this city. The lighthouse\n"
	.string "lights up so pretty at night.$"

SunyshoreCity_Text_BreederF:
	.string "My POKéMON love the salty air\n"
	.string "here. It's good for their coats.$"

SunyshoreCity_Text_Worker:
	.string "We're always fixing something\n"
	.string "around this city. Never a dull day.$"

SunyshoreCity_Text_Sailor2:
	.string "Ships come and go from SUNYSHORE\n"
	.string "all day long.$"
