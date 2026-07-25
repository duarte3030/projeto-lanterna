Route208_MapScripts::
	.byte 0

Route208_EventScript_BlackBelt::
	msgbox Route208_Text_BlackBelt, MSGBOX_NPC
	end

Route208_EventScript_Hiker::
	msgbox Route208_Text_Hiker, MSGBOX_NPC
	end

Route208_EventScript_Breeder::
	msgbox Route208_Text_Breeder, MSGBOX_NPC
	end

Route208_EventScript_Artist::
	msgbox Route208_Text_Artist, MSGBOX_NPC
	end

Route208_Text_BlackBelt:
	.string "...Don't say a word. Just take it.$"

Route208_Text_Hiker:
	.string "Route 209 has an old stone tower\n"
	.string "underground. Ever seen it?$"

Route208_Text_Breeder:
	.string "My Pokémon are always happiest\n"
	.string "when we're out on the trail.$"

Route208_Text_Artist:
	.string "I'm sketching the cliffs today.\n"
	.string "The light here is perfect.$"

Route208_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_HIKER_ROBERT, Route208_Text_Trainer1Intro, Route208_Text_Trainer1Defeat
	msgbox Route208_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route208_Text_Trainer1Intro:
	.string "Gahahaha! You're just a little kid!\pHow're you supposed to beat a big\n"
	.string "man like me?$"

Route208_Text_Trainer1Defeat:
	.string "Oh my, a big man like me got schooled\n"
	.string "by a little kid like you!$"

Route208_Text_Trainer1Post:
	.string "Wow, you're sure impressive!\pI guess it makes no difference if\n"
	.string "you're young or old in battles.$"

Route208_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_HIKER_ALEXANDER, Route208_Text_Trainer2Intro, Route208_Text_Trainer2Defeat
	msgbox Route208_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route208_Text_Trainer2Intro:
	.string "They call me the Echo Man!\n"
	.string "Battle with me! Yahoo!$"

Route208_Text_Trainer2Defeat:
	.string "Ohh... Yo...\n"
	.string "Yodelay...$"

Route208_Text_Trainer2Post:
	.string "Here's good advice from the Echo Man!\pIf you're at a loss as to where you\n"
	.string "should be going, check the Town Map!$"

Route208_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_HIKER_JONATHAN, Route208_Text_Trainer3Intro, Route208_Text_Trainer3Defeat
	msgbox Route208_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route208_Text_Trainer3Intro:
	.string "If I beat you, will you share some\n"
	.string "food with me?$"

Route208_Text_Trainer3Defeat:
	.string "We were starved for food, and now\n"
	.string "we're starved for a win...$"

Route208_Text_Trainer3Post:
	.string "Sigh... I feel even hungrier...\n"
	.string "Maybe I'll chow down some Berries...\pBut that's kind of gross.\n"
	.string "What am I, a Pokémon?$"

Route208_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_BLACK_BELT_KYLE, Route208_Text_Trainer4Intro, Route208_Text_Trainer4Defeat
	msgbox Route208_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route208_Text_Trainer4Intro:
	.string "This karate man's going to pulverize\n"
	.string "you!$"

Route208_Text_Trainer4Defeat:
	.string "We got pulverized...$"

Route208_Text_Trainer4Post:
	.string "It's obvious I need to train myself\n"
	.string "and my Pokémon harder.\pHey, if you've got a Vs. Seeker, you'd\n"
	.string "better put it to good use.\pNothing beats some repeated battling\n"
	.string "for toughening up your Pokémon.$"

Route208_EventScript_Trainer5::
	trainerbattle_single TRAINER_SINNOH_FISHERMAN_CODY, Route208_Text_Trainer5Intro, Route208_Text_Trainer5Defeat
	msgbox Route208_Text_Trainer5Post, MSGBOX_AUTOCLOSE
	end

Route208_Text_Trainer5Intro:
	.string "Muhihi...\n"
	.string "I'll haul you up and out!$"

Route208_Text_Trainer5Defeat:
	.string "Restraint is my favorite word.\n"
	.string "Like...from crushing my opponents.$"

Route208_Text_Trainer5Post:
	.string "You need a Good Rod if you want to\n"
	.string "catch good Pokémon.$"

Route208_EventScript_Trainer6::
	trainerbattle_single TRAINER_SINNOH_AROMA_LADY_HANNAH, Route208_Text_Trainer6Intro, Route208_Text_Trainer6Defeat
	msgbox Route208_Text_Trainer6Post, MSGBOX_AUTOCLOSE
	end

Route208_Text_Trainer6Intro:
	.string "Oh, you want to have a battle?\pI was meaning to enter a Contest,\n"
	.string "but beating you won't take long...$"

Route208_Text_Trainer6Defeat:
	.string "Oh, you have us beaten.$"

Route208_Text_Trainer6Post:
	.string "You and your Pokémon have so much\n"
	.string "energy.\pI think you would do well in\n"
	.string "Contests, too.$"

Route208_EventScript_Trainer7::
	trainerbattle_single TRAINER_SINNOH_ARTIST_WILLIAM, Route208_Text_Trainer7Intro, Route208_Text_Trainer7Defeat
	msgbox Route208_Text_Trainer7Post, MSGBOX_AUTOCLOSE
	end

Route208_Text_Trainer7Intro:
	.string "You and I!\pLet us create a scene!\n"
	.string "A fantastic tableau of battle!$"

Route208_Text_Trainer7Defeat:
	.string "Magnificent!\n"
	.string "I am aglow with inspiration!$"

Route208_Text_Trainer7Post:
	.string "That battle will surely become a\n"
	.string "stupendous masterpiece painting!\pI shall title it...\p“My Pokémon Is Fight”!$"
