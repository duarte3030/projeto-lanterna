Route223_MapScripts::
	.byte 0

Route223_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_WESLEY, Route223_Text_Trainer1Intro, Route223_Text_Trainer1Defeat
	msgbox Route223_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route223_Text_Trainer1Intro:
	.string "I've decided!\nI'm off to the Pokémon League if I win!\p$"

Route223_Text_Trainer1Defeat:
	.string "Blblblblugh...$"

Route223_Text_Trainer1Post:
	.string "It's OK. Just let me float away\n"
	.string "like driftwood...$"

Route223_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_RICARDO, Route223_Text_Trainer2Intro, Route223_Text_Trainer2Defeat
	msgbox Route223_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route223_Text_Trainer2Intro:
	.string "It might not look like it, but I'm\ntraveling now.\p$"

Route223_Text_Trainer2Defeat:
	.string "You've got the upper hand on me.$"

Route223_Text_Trainer2Post:
	.string "But you can be sure that there will\n"
	.string "be bigger challenges in front of you.\p"
	.string "Go! Go as far as you can! You alone can\n"
	.string "broaden your horizons.$"

Route223_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_FRANCISCO, Route223_Text_Trainer3Intro, Route223_Text_Trainer3Defeat
	msgbox Route223_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route223_Text_Trainer3Intro:
	.string "The sea around these parts is harsh.\nAs am I!\p$"

Route223_Text_Trainer3Defeat:
	.string "The world is so harsh...$"

Route223_Text_Trainer3Post:
	.string "What? You've got that many Gym\n"
	.string "Badges? No wonder you're so tough...$"

Route223_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_COLTON, Route223_Text_Trainer4Intro, Route223_Text_Trainer4Defeat
	msgbox Route223_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route223_Text_Trainer4Intro:
	.string "To swim every sea there is...\nThat's my dream!\p$"

Route223_Text_Trainer4Defeat:
	.string "Boo!\n"
	.string "I'm not done with my dream!$"

Route223_Text_Trainer4Post:
	.string "What is the sea like in places like the\n"
	.string "Kanto and Hoenn regions?$"

Route223_EventScript_Trainer5::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_TROY, Route223_Text_Trainer5Intro, Route223_Text_Trainer5Defeat
	msgbox Route223_Text_Trainer5Post, MSGBOX_AUTOCLOSE
	end

Route223_Text_Trainer5Intro:
	.string "Yes, I know I can surf, but I'd\nrather swim instead.\pIt does seem weird, I agree.\p$"

Route223_Text_Trainer5Defeat:
	.string "Kaploosh!$"

Route223_Text_Trainer5Post:
	.string "If you don't know how, I'm willing to\n"
	.string "show you how to swim.$"

Route223_EventScript_Trainer6::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_OSCAR, Route223_Text_Trainer6Intro, Route223_Text_Trainer6Defeat
	msgbox Route223_Text_Trainer6Post, MSGBOX_AUTOCLOSE
	end

Route223_Text_Trainer6Intro:
	.string "I train at a Pokémon Gym, too.\pDon't think you're going to win\neasily!\p$"

Route223_Text_Trainer6Defeat:
	.string "Master Wake...\n"
	.string "I mean, Crasher Wake, sorry!$"

Route223_Text_Trainer6Post:
	.string "What to do... Train at the Gym again,\n"
	.string "or train by myself...$"

Route223_EventScript_Trainer7::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_MIRANDA, Route223_Text_Trainer7Intro, Route223_Text_Trainer7Defeat
	msgbox Route223_Text_Trainer7Post, MSGBOX_AUTOCLOSE
	end

Route223_Text_Trainer7Intro:
	.string "I'm determined to go to the Pokémon\nLeague, no matter how hard it is.\p$"

Route223_Text_Trainer7Defeat:
	.string "Th-this is so hard...$"

Route223_Text_Trainer7Post:
	.string "Losing won't make me quit.\n"
	.string "I mean, this is my dream!\p"
	.string "The Pokémon League isn't going\n"
	.string "anywhere, either.$"

Route223_EventScript_Trainer8::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_AUBREE, Route223_Text_Trainer8Intro, Route223_Text_Trainer8Defeat
	msgbox Route223_Text_Trainer8Post, MSGBOX_AUTOCLOSE
	end

Route223_Text_Trainer8Intro:
	.string "Excuse me for wearing my bikini!\p$"

Route223_Text_Trainer8Defeat:
	.string "Was I multitasking too much, battling\n"
	.string "and swimming at the same time?$"

Route223_Text_Trainer8Post:
	.string "When I'm in my bikini, I'm at a loss\n"
	.string "about where to carry my Poké Balls!$"

Route223_EventScript_Trainer9::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_PAIGE, Route223_Text_Trainer9Intro, Route223_Text_Trainer9Defeat
	msgbox Route223_Text_Trainer9Post, MSGBOX_AUTOCLOSE
	end

Route223_Text_Trainer9Intro:
	.string "Deep breathing before battle!\nBreathe in...and out!\p$"

Route223_Text_Trainer9Defeat:
	.string "Breathe in...and out.\n"
	.string "Breathe in...and out!$"

Route223_Text_Trainer9Post:
	.string "Deep breathing after battle, too!\n"
	.string "Breathe in...and out!$"

Route223_EventScript_Trainer10::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_CRYSTAL, Route223_Text_Trainer10Intro, Route223_Text_Trainer10Defeat
	msgbox Route223_Text_Trainer10Post, MSGBOX_AUTOCLOSE
	end

Route223_Text_Trainer10Intro:
	.string "Your Pokémon doesn't seem to be tiring\nat all from carrying you on its back.\pLet me see how strong it is!\p$"

Route223_Text_Trainer10Defeat:
	.string "I can't take any more...\n"
	.string "I'm all tired out!$"

Route223_Text_Trainer10Post:
	.string "While floating here, I think about\n"
	.string "everything and nothing.\p"
	.string "Like how I should battle next, and\n"
	.string "what's for dinner tomorrow, and...$"

Route223_EventScript_Trainer11::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_CASSANDRA, Route223_Text_Trainer11Intro, Route223_Text_Trainer11Defeat
	msgbox Route223_Text_Trainer11Post, MSGBOX_AUTOCLOSE
	end

Route223_Text_Trainer11Intro:
	.string "Did you know, I was crowned the\nchampion of a swimsuit contest!\pSo now, I'm trying to win a title\nat a Pokémon Contest!\p$"

Route223_Text_Trainer11Defeat:
	.string "I'm speechless!\n"
	.string "I never lose when I'm in my swimsuit!$"

Route223_Text_Trainer11Post:
	.string "I shouldn't be worried about what bikini\n"
	.string "to wear.\p"
	.string "The first thing to do is consider what\n"
	.string "Pokémon I should be using!$"

Route223_EventScript_Trainer12::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_GABRIELLE, Route223_Text_Trainer12Intro, Route223_Text_Trainer12Defeat
	msgbox Route223_Text_Trainer12Post, MSGBOX_AUTOCLOSE
	end

Route223_Text_Trainer12Intro:
	.string "My favorite kind of guy is someone\nthat looks good out on the open sea!\p$"

Route223_Text_Trainer12Defeat:
	.string "The tide is going out...$"

Route223_Text_Trainer12Post:
	.string "Don't get me wrong, it's not as if I\n"
	.string "don't like mountain men.\p"
	.string "But, you know, my most favorite kind of\n"
	.string "guy looks great with Pokémon!$"

Route223_EventScript_Trainer13::
	trainerbattle_single TRAINER_SINNOH_SAILOR_ZACHARIAH, Route223_Text_Trainer13Intro, Route223_Text_Trainer13Defeat
	msgbox Route223_Text_Trainer13Post, MSGBOX_AUTOCLOSE
	end

Route223_Text_Trainer13Intro:
	.string "I came out here because I wanted to\nsee the Pokémon League for myself.\p$"

Route223_Text_Trainer13Defeat:
	.string "I'm shocked...\n"
	.string "No, really, I am.$"

Route223_Text_Trainer13Post:
	.string "The way I battle now, well, I can\n"
	.string "only look at the Pokémon League!\p"
	.string "You, go on! You go to the Pokémon\n"
	.string "League for me, too!$"

