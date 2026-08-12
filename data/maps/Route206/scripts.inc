Route206_MapScripts::
	.byte 0

Route206_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_CYCLIST_AXEL, Route206_Text_Trainer1Intro, Route206_Text_Trainer1Defeat
	msgbox Route206_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route206_Text_Trainer1Intro:
	.string "Yo! Cycling and Pokémon!\n"
	.string "Which do you prefer?$"

Route206_Text_Trainer1Defeat:
	.string "Hey, not bad, you!$"

Route206_Text_Trainer1Post:
	.string "This Cycling Road is one fine place--\n"
	.string "great bikes, superb Pokémon,\pand awesome Trainers all around!$"

Route206_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_CYCLIST_MEGAN, Route206_Text_Trainer2Intro, Route206_Text_Trainer2Defeat
	msgbox Route206_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route206_Text_Trainer2Intro:
	.string "Cycling feels great!\pIt will feel even better when I beat\n"
	.string "you in a battle!$"

Route206_Text_Trainer2Defeat:
	.string "Whew!\n"
	.string "You worked us over.$"

Route206_Text_Trainer2Post:
	.string "I like spinning the pedals backward\n"
	.string "while sailing downhill.$"

Route206_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_CYCLIST_JAMES, Route206_Text_Trainer3Intro, Route206_Text_Trainer3Defeat
	msgbox Route206_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route206_Text_Trainer3Intro:
	.string "Ding-ding! Watch out, you!\n"
	.string "Or, did you want to battle?$"

Route206_Text_Trainer3Defeat:
	.string "Despite all the effort, I'm just spinning\n"
	.string "my wheels...\pIt's always that way with me!$"

Route206_Text_Trainer3Post:
	.string "I might try racing through Cycling\n"
	.string "Road in one long shot.$"

Route206_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_CYCLIST_NICOLE, Route206_Text_Trainer4Intro, Route206_Text_Trainer4Defeat
	msgbox Route206_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route206_Text_Trainer4Intro:
	.string "The both of us are on Bikes, and we\n"
	.string "both have Pokémon!\pI can't let you get the better of me!$"

Route206_Text_Trainer4Defeat:
	.string "Oh, geez...\n"
	.string "I seem to have fallen off my Bike.$"

Route206_Text_Trainer4Post:
	.string "I should have challenged you to a race,\n"
	.string "not a battle!$"

Route206_EventScript_Trainer5::
	trainerbattle_single TRAINER_SINNOH_CYCLIST_JOHN, Route206_Text_Trainer5Intro, Route206_Text_Trainer5Defeat
	msgbox Route206_Text_Trainer5Post, MSGBOX_AUTOCLOSE
	end

Route206_Text_Trainer5Intro:
	.string "That Bike you've got there...it's the\n"
	.string "type that can change gears!\pYou gotta love that!\n"
	.string "Sure, I'll give you a battle!$"

Route206_Text_Trainer5Defeat:
	.string "Crash! Tinkle...$"

Route206_Text_Trainer5Post:
	.string "The 3-speed makes for easy turning,\n"
	.string "and the 4-speed's for going fast.\pI love them both!$"

Route206_EventScript_Trainer6::
	trainerbattle_single TRAINER_SINNOH_CYCLIST_KAYLA, Route206_Text_Trainer6Intro, Route206_Text_Trainer6Defeat
	msgbox Route206_Text_Trainer6Post, MSGBOX_AUTOCLOSE
	end

Route206_Text_Trainer6Intro:
	.string "If you beat me, you can count on\n"
	.string "something rotten coming your way!$"

Route206_Text_Trainer6Defeat:
	.string "Kerrrash!$"

Route206_Text_Trainer6Post:
	.string "Aww!\n"
	.string "Why did you beat me?!\pI hope you get so lost in Wayward Cave\n"
	.string "you cry! Boo-hoo-hoo!$"

Route206_EventScript_Trainer7::
	trainerbattle_single TRAINER_SINNOH_CYCLIST_RYAN, Route206_Text_Trainer7Intro, Route206_Text_Trainer7Defeat
	msgbox Route206_Text_Trainer7Post, MSGBOX_AUTOCLOSE
	end

Route206_Text_Trainer7Intro:
	.string "A bike will carry you a long way.\pThe only thing that limits you is your\n"
	.string "own endurance!$"

Route206_Text_Trainer7Defeat:
	.string "Gasp... Gasp... Gasp...$"

Route206_Text_Trainer7Post:
	.string "My Pokémon and I are plumb worn out.\n"
	.string "We should be getting home to rest...$"

Route206_EventScript_Trainer8::
	trainerbattle_single TRAINER_SINNOH_CYCLIST_RACHEL, Route206_Text_Trainer8Intro, Route206_Text_Trainer8Defeat
	msgbox Route206_Text_Trainer8Post, MSGBOX_AUTOCLOSE
	end

Route206_Text_Trainer8Intro:
	.string "Some people compete over speed, and\n"
	.string "some compete over technique.\pWhich kind are you?$"

Route206_Text_Trainer8Defeat:
	.string "You're a speedy technician!$"

Route206_Text_Trainer8Post:
	.string "I enjoy the scenery.\pDon't you think the area below\n"
	.string "Cycling Road looks nice?$"

Route206_EventScript_Trainer9::
	trainerbattle_single TRAINER_SINNOH_HIKER_THEODORE, Route206_Text_Trainer9Intro, Route206_Text_Trainer9Defeat
	msgbox Route206_Text_Trainer9Post, MSGBOX_AUTOCLOSE
	end

Route206_Text_Trainer9Intro:
	.string "Whoa! You startled me!\n"
	.string "Well, we may as well battle!$"

Route206_Text_Trainer9Defeat:
	.string "Your power startles me!$"

Route206_Text_Trainer9Post:
	.string "We Hikers are bighearted guys!\n"
	.string "Losing doesn't bother us!$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route206_EventScript_Placa1::
	msgbox Route206_Text_Placa1, MSGBOX_SIGN
	end

Route206_Text_Placa1:
	.string "Rt. 206\nOreburgh City$"

Route206_EventScript_Placa2::
	msgbox Route206_Text_Placa2, MSGBOX_SIGN
	end

Route206_Text_Placa2:
	.string "Rt. 206\nEterna City$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route206_EventScript_Npc1::
	msgbox Route206_Text_Npc1, MSGBOX_NPC
	end

Route206_Text_Npc1:
	.string "This is odd... I heard there were two\ncaves on Route 206.\pBut I can only find one entrance.$"
