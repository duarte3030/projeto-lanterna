Route213_MapScripts::
	.byte 0

Route213_EventScript_HotelSign::
	msgbox Route213_Text_HotelSign, MSGBOX_SIGN
	end

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
	.string "I lost at sea! But I swim here the\n"
	.string "whole year round!$"

Route213_Text_Trainer1Post:
	.string "When you're out at sea, Water-type\n"
	.string "Pokémon look more lively.$"

Route213_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_EVAN, Route213_Text_Trainer2Intro, Route213_Text_Trainer2Defeat
	msgbox Route213_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route213_Text_Trainer2Intro:
	.string "Brr... I'm starting to get chilly.\nI could use a win to get warmed up.\p$"

Route213_Text_Trainer2Defeat:
	.string "The chill of the sea, and the\n"
	.string "coldness of defeat...\p"
	.string "It's a double whammy.$"

Route213_Text_Trainer2Post:
	.string "Look at my lips...\n"
	.string "They're the color of prunes!$"

Route213_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_MARY, Route213_Text_Trainer3Intro, Route213_Text_Trainer3Defeat
	msgbox Route213_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route213_Text_Trainer3Intro:
	.string "Hello, there!\nAren't you going to swim?\p$"

Route213_Text_Trainer3Defeat:
	.string "What's saltier?\n"
	.string "My tears or the sea...$"

Route213_Text_Trainer3Post:
	.string "There aren't many sea routes that\n"
	.string "you can swim in Sinnoh.\p"
	.string "It makes me want to take a vacation\n"
	.string "in the Hoenn region.$"

Route213_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_HALEY, Route213_Text_Trainer4Intro, Route213_Text_Trainer4Defeat
	msgbox Route213_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route213_Text_Trainer4Intro:
	.string "Hi, wave-riding Trainer!\nHow about a battle on the sea?\p$"

Route213_Text_Trainer4Defeat:
	.string "You sure schooled me there.$"

Route213_Text_Trainer4Post:
	.string "Maybe I should switch to surfing,\n"
	.string "too...$"

Route213_EventScript_Trainer5::
	trainerbattle_single TRAINER_SINNOH_TUBER_JARED, Route213_Text_Trainer5Intro, Route213_Text_Trainer5Defeat
	msgbox Route213_Text_Trainer5Post, MSGBOX_AUTOCLOSE
	end

Route213_Text_Trainer5Intro:
	.string "Isn't this nice?\nI love my inflatable tube!\p$"

Route213_Text_Trainer5Defeat:
	.string "It's not easy trying to move holding\n"
	.string "on to this inflatable tube.$"

Route213_Text_Trainer5Post:
	.string "Mom blew up my inflatable tube for me.\n"
	.string "I ran out of breath just opening it!$"

Route213_EventScript_Trainer6::
	trainerbattle_single TRAINER_SINNOH_TUBER_CHELSEA, Route213_Text_Trainer6Intro, Route213_Text_Trainer6Defeat
	msgbox Route213_Text_Trainer6Post, MSGBOX_AUTOCLOSE
	end

Route213_Text_Trainer6Intro:
	.string "Ehehe...\nI can battle, too!\p$"

Route213_Text_Trainer6Defeat:
	.string "Losing made me all hungry now.$"

Route213_Text_Trainer6Post:
	.string "That cloud looks like giant ice cream!\n"
	.string "I bet it tastes yummy!$"

Route213_EventScript_Trainer7::
	trainerbattle_single TRAINER_SINNOH_BEAUTY_CYNDY, Route213_Text_Trainer7Intro, Route213_Text_Trainer7Defeat
	msgbox Route213_Text_Trainer7Post, MSGBOX_AUTOCLOSE
	end

Route213_Text_Trainer7Intro:
	.string "Let me demonstrate my technique.\nIt's how this grown-up battles.\p$"

Route213_Text_Trainer7Defeat:
	.string "Oh, my gosh!\n"
	.string "You attack that savagely?$"

Route213_Text_Trainer7Post:
	.string "You're so much more of a Trainer\n"
	.string "than you look!$"

Route213_EventScript_Trainer8::
	trainerbattle_single TRAINER_SINNOH_FISHERMAN_KENNETH, Route213_Text_Trainer8Intro, Route213_Text_Trainer8Defeat
	msgbox Route213_Text_Trainer8Post, MSGBOX_AUTOCLOSE
	end

Route213_Text_Trainer8Intro:
	.string "Waah! Now! Just now!\nI was just about to reel it in!\p$"

Route213_Text_Trainer8Defeat:
	.string "You need to have more respect for\n"
	.string "a grown-up...$"

Route213_Text_Trainer8Post:
	.string "Go on. Don't be shy about going up to\n"
	.string "people to hear what they have to say...\p"
	.string "Just don't you talk to me.$"

Route213_EventScript_Trainer9::
	trainerbattle_single TRAINER_SINNOH_SAILOR_PAUL, Route213_Text_Trainer9Intro, Route213_Text_Trainer9Defeat
	msgbox Route213_Text_Trainer9Post, MSGBOX_AUTOCLOSE
	end

Route213_Text_Trainer9Intro:
	.string "Traveling alone, are you? That's\nimpressive! How about we battle?\p$"

Route213_Text_Trainer9Defeat:
	.string "You're good, pip-squeak!$"

Route213_Text_Trainer9Post:
	.string "Maybe I'll go work out down at the\n"
	.string "restaurant again.\p"
	.string "That place gets different people in\n"
	.string "every day, and they all like battles.$"


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
