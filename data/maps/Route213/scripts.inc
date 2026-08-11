Route213_MapScripts::
	.byte 0

Route213_EventScript_Fisherman::
	msgbox Route213_Text_Fisherman, MSGBOX_NPC
	end

Route213_EventScript_Beauty::
	msgbox Route213_Text_Beauty, MSGBOX_NPC
	end

Route213_EventScript_Collector::
	msgbox Route213_Text_Collector, MSGBOX_NPC
	end

Route213_EventScript_Sailor::
	msgbox Route213_Text_Sailor, MSGBOX_NPC
	end

Route213_EventScript_HotelSign::
	msgbox Route213_Text_HotelSign, MSGBOX_SIGN
	end

Route213_Text_Fisherman:
	.string "This route runs right along LAKE\n"
	.string "VALOR. The fishing here is some of\l"
	.string "the best in SINNOH.$"

Route213_Text_Beauty:
	.string "I came all this way just to see the\n"
	.string "sun rise over the lake. Wasn't it\l"
	.string "worth it?$"

Route213_Text_Collector:
	.string "Grand Lake gives me the perfect\n"
	.string "excuse to walk in circles all day\l"
	.string "looking for treasure.$"

Route213_Text_Sailor:
	.string "The waters around here look calm,\n"
	.string "but don't let that fool you. Always\l"
	.string "respect the lake.$"

Route213_Text_HotelSign:
	.string "HOTEL GRAND LAKE\n"
	.string "Rest and relax with a view of\l"
	.string "LAKE VALOR.$"

Route213_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_SHELTIN, Route213_Text_Trainer1Intro, Route213_Text_Trainer1Defeat
	msgbox Route213_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route213_Text_Trainer1Intro:
	.string "I swim the whole year round.\nI'm not losing a battle at sea!\p$"

Route213_Text_Trainer1Defeat:
	.string "I lost at sea! But I swim here the\nwhole year round!\n$"

Route213_Text_Trainer1Post:
	.string "When you're out at sea, Water-type\nPokémon look more lively.\n$"

Route213_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_EVAN, Route213_Text_Trainer2Intro, Route213_Text_Trainer2Defeat
	msgbox Route213_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route213_Text_Trainer2Intro:
	.string "Brr... I'm starting to get chilly.\nI could use a win to get warmed up.\p$"

Route213_Text_Trainer2Defeat:
	.string "The chill of the sea, and the\ncoldness of defeat...\pIt's a double whammy.\n$"

Route213_Text_Trainer2Post:
	.string "Look at my lips...\nThey're the color of prunes!\n$"

Route213_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_MARY, Route213_Text_Trainer3Intro, Route213_Text_Trainer3Defeat
	msgbox Route213_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route213_Text_Trainer3Intro:
	.string "Hello, there!\nAren't you going to swim?\p$"

Route213_Text_Trainer3Defeat:
	.string "What's saltier?\nMy tears or the sea...\n$"

Route213_Text_Trainer3Post:
	.string "There aren't many sea routes that\nyou can swim in Sinnoh.\pIt makes me want to take a vacation\nin the Hoenn region.\n$"

Route213_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_HALEY, Route213_Text_Trainer4Intro, Route213_Text_Trainer4Defeat
	msgbox Route213_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route213_Text_Trainer4Intro:
	.string "Hi, wave-riding Trainer!\nHow about a battle on the sea?\p$"

Route213_Text_Trainer4Defeat:
	.string "You sure schooled me there.\n$"

Route213_Text_Trainer4Post:
	.string "Maybe I should switch to surfing,\ntoo...\n$"

Route213_EventScript_Trainer5::
	trainerbattle_single TRAINER_SINNOH_TUBER_JARED, Route213_Text_Trainer5Intro, Route213_Text_Trainer5Defeat
	msgbox Route213_Text_Trainer5Post, MSGBOX_AUTOCLOSE
	end

Route213_Text_Trainer5Intro:
	.string "Isn't this nice?\nI love my inflatable tube!\p$"

Route213_Text_Trainer5Defeat:
	.string "It's not easy trying to move holding\non to this inflatable tube.\n$"

Route213_Text_Trainer5Post:
	.string "Mom blew up my inflatable tube for me.\nI ran out of breath just opening it!\n$"

Route213_EventScript_Trainer6::
	trainerbattle_single TRAINER_SINNOH_TUBER_CHELSEA, Route213_Text_Trainer6Intro, Route213_Text_Trainer6Defeat
	msgbox Route213_Text_Trainer6Post, MSGBOX_AUTOCLOSE
	end

Route213_Text_Trainer6Intro:
	.string "Ehehe...\nI can battle, too!\p$"

Route213_Text_Trainer6Defeat:
	.string "Losing made me all hungry now.\n$"

Route213_Text_Trainer6Post:
	.string "That cloud looks like giant ice cream!\nI bet it tastes yummy!\n$"

Route213_EventScript_Trainer7::
	trainerbattle_single TRAINER_SINNOH_BEAUTY_CYNDY, Route213_Text_Trainer7Intro, Route213_Text_Trainer7Defeat
	msgbox Route213_Text_Trainer7Post, MSGBOX_AUTOCLOSE
	end

Route213_Text_Trainer7Intro:
	.string "Let me demonstrate my technique.\nIt's how this grown-up battles.\p$"

Route213_Text_Trainer7Defeat:
	.string "Oh, my gosh!\nYou attack that savagely?\n$"

Route213_Text_Trainer7Post:
	.string "You're so much more of a Trainer\nthan you look!\n$"

Route213_EventScript_Trainer8::
	trainerbattle_single TRAINER_SINNOH_FISHERMAN_KENNETH, Route213_Text_Trainer8Intro, Route213_Text_Trainer8Defeat
	msgbox Route213_Text_Trainer8Post, MSGBOX_AUTOCLOSE
	end

Route213_Text_Trainer8Intro:
	.string "Waah! Now! Just now!\nI was just about to reel it in!\p$"

Route213_Text_Trainer8Defeat:
	.string "You need to have more respect for\na grown-up...\n$"

Route213_Text_Trainer8Post:
	.string "Go on. Don't be shy about going up to\npeople to hear what they have to say...\pJust don't you talk to me.\n$"

Route213_EventScript_Trainer9::
	trainerbattle_single TRAINER_SINNOH_SAILOR_PAUL, Route213_Text_Trainer9Intro, Route213_Text_Trainer9Defeat
	msgbox Route213_Text_Trainer9Post, MSGBOX_AUTOCLOSE
	end

Route213_Text_Trainer9Intro:
	.string "Traveling alone, are you? That's\nimpressive! How about we battle?\p$"

Route213_Text_Trainer9Defeat:
	.string "You're good, pip-squeak!\n$"

Route213_Text_Trainer9Post:
	.string "Maybe I'll go work out down at the\nrestaurant again.\pThat place gets different people in\nevery day, and they all like battles.\n$"


@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route213_EventScript_Placa1::
	msgbox Route213_Text_Placa1, MSGBOX_SIGN
	end

Route213_Text_Placa1:
	.string "Rt. 213\nPastoria City$"

Route213_EventScript_Placa2::
	msgbox Route213_Text_Placa2, MSGBOX_SIGN
	end

Route213_Text_Placa2:
	.string "Dr. Footstep's House\nFootprints Reveal All$"

Route213_EventScript_Placa3::
	msgbox Route213_Text_Placa3, MSGBOX_SIGN
	end

Route213_Text_Placa3:
	.string "Hotel Grand Lake\nAnother World on Lake Valor$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route213_EventScript_Npc1::
	msgbox Route213_Text_Npc1, MSGBOX_NPC
	end

Route213_Text_Npc1:
	.string "There's a fancy hotel in a fancy\nplace with a fancy restaurant.\pThe fancy restaurant's filled with\nfancy people who think of themselves\pas being too fancy to battle alone.$"

Route213_EventScript_Npc2::
	msgbox Route213_Text_Npc2, MSGBOX_NPC
	end

Route213_Text_Npc2:
	.string "I'd rather be in a pool than the sea.\pThe salty tang of the sea tastes like\nmy tears after a hard day at work...$"

Route213_EventScript_Npc3::
	msgbox Route213_Text_Npc3, MSGBOX_NPC
	end

Route213_Text_Npc3:
	.string "There's something on top of this\nbig cliff here!\pMy instincts tell me that, but how\nam I supposed to climb up?$"
