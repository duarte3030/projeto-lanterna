JubilifeCity_PokemonSchool_MapScripts::
	.byte 0

JubilifeCity_PokemonSchool_EventScript_Teacher::
	lock
	faceplayer
	msgbox JubilifeCity_PokemonSchool_Text_Teacher, MSGBOX_DEFAULT
	release
	end

JubilifeCity_PokemonSchool_EventScript_Kid1::
	msgbox JubilifeCity_PokemonSchool_Text_Kid1, MSGBOX_NPC
	end

JubilifeCity_PokemonSchool_EventScript_Kid2::
	msgbox JubilifeCity_PokemonSchool_Text_Kid2, MSGBOX_NPC
	end

JubilifeCity_PokemonSchool_EventScript_Kid3::
	msgbox JubilifeCity_PokemonSchool_Text_Kid3, MSGBOX_NPC
	end

JubilifeCity_PokemonSchool_Text_Teacher:
	.string "Welcome! This is where young\n"
	.string "TRAINERS learn the basics.\p"
	.string "Feel free to look around the\n"
	.string "classroom.$"

JubilifeCity_PokemonSchool_Text_Kid1:
	.string "Today we're learning about TYPE\n"
	.string "match-ups!$"

JubilifeCity_PokemonSchool_Text_Kid2:
	.string "I want to be just like the POKéMON\n"
	.string "Professor someday.$"

JubilifeCity_PokemonSchool_Text_Kid3:
	.string "Psst! Don't tell the teacher, but I'd\n"
	.string "rather be battling right now.$"
