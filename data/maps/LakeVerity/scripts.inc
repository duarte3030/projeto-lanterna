LakeVerity_MapScripts::
	.byte 0

LakeVerity_EventScript_Fisherman::
	msgbox LakeVerity_Text_Fisherman, MSGBOX_NPC
	end

LakeVerity_EventScript_Hiker::
	msgbox LakeVerity_Text_Hiker, MSGBOX_NPC
	end

LakeVerity_Text_Fisherman:
	.string "This lake is calm today...\n"
	.string "Good a spot as any to cast a line.$"

LakeVerity_Text_Hiker:
	.string "They say Lake Verity never freezes,\n"
	.string "no matter how cold the winter gets.$"

LakeVerity_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_LAKE_VERITY_1, LakeVerity_Text_Trainer1Intro, LakeVerity_Text_Trainer1Defeat
	msgbox LakeVerity_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

LakeVerity_Text_Trainer1Intro:
	.string "It is our mission to stall you.\n"
	.string "Sorry, but we gotta do our job.$"

LakeVerity_Text_Trainer1Defeat:
	.string "Losing was a part of my job, too.\n"
	.string "...I feel better by saying that.$"

LakeVerity_Text_Trainer1Post:
	.string "From three lakes, we must secure three\n"
	.string "Pokémon.\pYou simply mustn't interfere!$"

LakeVerity_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_LAKE_VERITY_3, LakeVerity_Text_Trainer2Intro, LakeVerity_Text_Trainer2Defeat
	msgbox LakeVerity_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

LakeVerity_Text_Trainer2Intro:
	.string "I'll knock your Pokémon into orbit!$"

LakeVerity_Text_Trainer2Defeat:
	.string "My mind is going orbital!$"

LakeVerity_Text_Trainer2Post:
	.string "The Pokémon here has already been\n"
	.string "taken to our HQ in Veilstone.\pSo, you see?\n"
	.string "A child like you can't touch us!$"

LakeVerity_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_LAKE_VERITY_2, LakeVerity_Text_Trainer3Intro, LakeVerity_Text_Trainer3Defeat
	msgbox LakeVerity_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

LakeVerity_Text_Trainer3Intro:
	.string "In order for us to bring peace to\n"
	.string "the world, we must control it!$"

LakeVerity_Text_Trainer3Defeat:
	.string "You're too young to understand.$"

LakeVerity_Text_Trainer3Post:
	.string "Our boss always had plans for\n"
	.string "the three lakes...\pWhile you were blissfully ignorant,\n"
	.string "our work went ahead...$"

LakeVerity_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_LAKE_VERITY_4, LakeVerity_Text_Trainer4Intro, LakeVerity_Text_Trainer4Defeat
	msgbox LakeVerity_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

LakeVerity_Text_Trainer4Intro:
	.string "If this mission is successful, we\n"
	.string "will get a nice bonus.$"

LakeVerity_Text_Trainer4Defeat:
	.string "There goes our bonus...\n"
	.string "This is an epic tragedy...$"

LakeVerity_Text_Trainer4Post:
	.string "I want Team Galactic to become\n"
	.string "powerful. That is all I want.$"
