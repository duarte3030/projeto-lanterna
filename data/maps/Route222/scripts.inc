Route222_MapScripts::
	.byte 0

Route222_EventScript_SignPikachuFanClub::
	msgbox Route222_Text_SignPikachuFanClub, MSGBOX_SIGN
	end

Route222_EventScript_SignSizeContest::
	msgbox Route222_Text_SignSizeContest, MSGBOX_SIGN
	end

Route222_Text_SignPikachuFanClub:
	.string "PIKACHU FAN CLUB\n"
	.string "Members only, this way.$"

Route222_Text_SignSizeContest:
	.string "POKéMON SIZE CONTEST\n"
	.string "Bring your biggest and best!$"

Route222_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_FISHERMAN_BRETT, Route222_Text_Trainer1Intro, Route222_Text_Trainer1Defeat
	msgbox Route222_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route222_Text_Trainer1Intro:
	.string "Well, I am fishing, but...\pVery well!\nI accept your challenge!\p$"

Route222_Text_Trainer1Defeat:
	.string "A bittersweet smile is on my lips.$"

Route222_Text_Trainer1Post:
	.string "I've gone down in defeat.\n"
	.string "Whatever more is there to say?$"

Route222_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_FISHERMAN_ALEC, Route222_Text_Trainer2Intro, Route222_Text_Trainer2Defeat
	msgbox Route222_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route222_Text_Trainer2Intro:
	.string "Hi, traveler!\nHow would you like to battle?\p$"

Route222_Text_Trainer2Defeat:
	.string "You've bested this fisherman traveler.$"

Route222_Text_Trainer2Post:
	.string "I like to fish.\n"
	.string "You're a traveler.\p"
	.string "Farewell, until we meet again!$"

Route222_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_FISHERMAN_GEORGE, Route222_Text_Trainer3Intro, Route222_Text_Trainer3Defeat
	msgbox Route222_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route222_Text_Trainer3Intro:
	.string "I'm getting bored of fishing.\nLet's have a quick battle!\p$"

Route222_Text_Trainer3Defeat:
	.string "I've been done in...$"

Route222_Text_Trainer3Post:
	.string "Thanks for that!\n"
	.string "It was a good change of pace for me.$"

Route222_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_FISHERMAN_COLE, Route222_Text_Trainer4Intro, Route222_Text_Trainer4Defeat
	msgbox Route222_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route222_Text_Trainer4Intro:
	.string "If I stare at the water's surface\nfor too long, I begin to forget what\pI was doing in the first place.\p$"

Route222_Text_Trainer4Defeat:
	.string "I don't know how, but I lost!$"

Route222_Text_Trainer4Post:
	.string "Oh, right...\n"
	.string "I was fishing, wasn't I?$"

Route222_EventScript_Trainer5::
	trainerbattle_single TRAINER_SINNOH_BEAUTY_NICOLA, Route222_Text_Trainer5Intro, Route222_Text_Trainer5Defeat
	msgbox Route222_Text_Trainer5Post, MSGBOX_AUTOCLOSE
	end

Route222_Text_Trainer5Intro:
	.string "After enjoying a meal at the hotel\nrestaurant, one has a battle.\pThat's the social etiquette.\p$"

Route222_Text_Trainer5Defeat:
	.string "Enchanting.$"

Route222_Text_Trainer5Post:
	.string "Personally, I would much rather pamper\n"
	.string "Pokémon than make them battle.$"

Route222_EventScript_Trainer6::
	trainerbattle_single TRAINER_SINNOH_TUBER_CONNER, Route222_Text_Trainer6Intro, Route222_Text_Trainer6Defeat
	msgbox Route222_Text_Trainer6Post, MSGBOX_AUTOCLOSE
	end

Route222_Text_Trainer6Intro:
	.string "Look, look! Look at my Pokémon!\nIt's really cool!\p$"

Route222_Text_Trainer6Defeat:
	.string "Wowee! I had to hold on tight to\n"
	.string "my inflatable tube!$"

Route222_Text_Trainer6Post:
	.string "Pools are OK, but I like the sea\n"
	.string "because Pokémon live there.$"

Route222_EventScript_Trainer7::
	trainerbattle_single TRAINER_SINNOH_RICH_BOY_TREY, Route222_Text_Trainer7Intro, Route222_Text_Trainer7Defeat
	msgbox Route222_Text_Trainer7Post, MSGBOX_AUTOCLOSE
	end

Route222_Text_Trainer7Intro:
	.string "I need to escape these doldrums...\nYou can keep me company.\p$"

Route222_Text_Trainer7Defeat:
	.string "That did liberate me from the doldrums,\n"
	.string "but at what price...$"

Route222_Text_Trainer7Post:
	.string "I'm going back to the hotel to rest!\n"
	.string "I find you exceedingly tiresome!$"

Route222_EventScript_Trainer8::
	trainerbattle_single TRAINER_SINNOH_SAILOR_LUTHER, Route222_Text_Trainer8Intro, Route222_Text_Trainer8Defeat
	msgbox Route222_Text_Trainer8Post, MSGBOX_AUTOCLOSE
	end

Route222_Text_Trainer8Intro:
	.string "My dream's a big one!\pI want to battle every kind of Pokémon\nfrom around the world!\p$"

Route222_Text_Trainer8Defeat:
	.string "I lost, but I am one step closer to\n"
	.string "realizing my dream!$"

Route222_Text_Trainer8Post:
	.string "Listen, you! Whatever happens, never\n"
	.string "lose sight of your dream!$"

Route222_EventScript_Trainer9::
	trainerbattle_single TRAINER_SINNOH_POLICEMAN_THOMAS, Route222_Text_Trainer9Intro, Route222_Text_Trainer9Defeat
	msgbox Route222_Text_Trainer9Post, MSGBOX_AUTOCLOSE
	end

Route222_Text_Trainer9Intro:
	.string "Who's there?!\nWhat do you think you're doing?!\p$"

Route222_Text_Trainer9Defeat:
	.string "I happen to be rather jumpy, so\n"
	.string "everyone looks suspicious to me.$"

Route222_Text_Trainer9Post:
	.string "I'm easy to scare, and yet here I am\n"
	.string "on patrol. Funny how things go.$"

Route222_EventScript_Trainer10::
	trainerbattle_single TRAINER_SINNOH_TUBER_HOLLY, Route222_Text_Trainer10Intro, Route222_Text_Trainer10Defeat
	msgbox Route222_Text_Trainer10Post, MSGBOX_AUTOCLOSE
	end

Route222_Text_Trainer10Intro:
	.string "Listen, listen! Can you tell me what\nkind of Pokémon you have?\p$"

Route222_Text_Trainer10Defeat:
	.string "You're so tough. I'm stunned...$"

Route222_Text_Trainer10Post:
	.string "I want to hang on to a BUIZEL and\n"
	.string "just bob around.$"

Route222_EventScript_Trainer11::
	trainerbattle_single TRAINER_SINNOH_SAILOR_MARC, Route222_Text_Trainer11Intro, Route222_Text_Trainer11Defeat
	msgbox Route222_Text_Trainer11Post, MSGBOX_AUTOCLOSE
	end

Route222_Text_Trainer11Intro:
	.string "Oh, we'll ride upon the sea,\nin a boat, just you and me!\pThat's the way of the Sailor!\nWay of the Sailor. Sing it!\p$"

Route222_Text_Trainer11Defeat:
	.string "Your Pokémon...\n"
	.string "They're looking good!$"

Route222_Text_Trainer11Post:
	.string "You ought to think about becoming\n"
	.string "a Sailor yourself.\p"
	.string "It's been great to be able to visit\n"
	.string "different places around the world.$"


@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route222_EventScript_Npc1::
	msgbox Route222_Text_Npc1, MSGBOX_NPC
	end

Route222_Text_Npc1:
	.string "When I first started fishing, catching\nanything made me happy.\pBut those days are long gone now...\pNow I get annoyed if I can't beat my\nrecord by even an inch...$"

Route222_EventScript_Npc2::
	msgbox Route222_Text_Npc2, MSGBOX_NPC
	end

Route222_Text_Npc2:
	.string "The only items you ever throw are\nPoké Balls!\pBut is that true?!\nI want people to think about that.\pThat's why I give away the Technical\nMachine Fling.$"

Route222_EventScript_PolicemanThomasNoBattle::
	msgbox Route222_Text_PolicemanThomasNoBattle, MSGBOX_NPC
	end

Route222_Text_PolicemanThomasNoBattle:
	.string "I can't explain it.\nI get more easily agitated at night.$"
