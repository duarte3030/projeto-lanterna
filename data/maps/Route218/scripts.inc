Route218_MapScripts::
	.byte 0

Route218_EventScript_Guitarist::
	msgbox Route218_Text_Guitarist, MSGBOX_NPC
	end

Route218_EventScript_FishermanWest::
	msgbox Route218_Text_FishermanWest, MSGBOX_NPC
	end

Route218_EventScript_Sailor::
	msgbox Route218_Text_Sailor, MSGBOX_NPC
	end

Route218_EventScript_FishermanEast::
	msgbox Route218_Text_FishermanEast, MSGBOX_NPC
	end

Route218_EventScript_JubilifeSign::
	msgbox Route218_Text_JubilifeSign, MSGBOX_SIGN
	end

Route218_Text_Guitarist:
	.string "I write my best songs sitting by\n"
	.string "the water out here.$"

Route218_Text_FishermanWest:
	.string "CANALAVE's just down the road.\n"
	.string "Good POKéMON in these waters,\l"
	.string "though.$"

Route218_Text_Sailor:
	.string "This channel links JUBILIFE and\n"
	.string "CANALAVE. Ships pass through here\l"
	.string "all the time.$"

Route218_Text_FishermanEast:
	.string "Cast a line off that bridge sometime.\n"
	.string "You might be surprised what bites.$"

Route218_Text_JubilifeSign:
	.string "JUBILIFE CITY\n"
	.string "This way.$"

Route218_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_SAILOR_SKYLER, Route218_Text_Trainer1Intro, Route218_Text_Trainer1Defeat
	msgbox Route218_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route218_Text_Trainer1Intro:
	.string "A man of the sea is also a man of\nPokémon!\p$"

Route218_Text_Trainer1Defeat:
	.string "Anchors away!\n$"

Route218_Text_Trainer1Post:
	.string "You've got what it takes to be\na Trainer among Trainers!\n$"

Route218_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_FISHERMAN_MIGUEL, Route218_Text_Trainer2Intro, Route218_Text_Trainer2Defeat
	msgbox Route218_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route218_Text_Trainer2Intro:
	.string "Outdoor fishing for the win!\pShouting doesn't help my fishing any,\nbut shout I must!\p$"

Route218_Text_Trainer2Defeat:
	.string "Gwaaah!\nThis is hurting!\n$"

Route218_Text_Trainer2Post:
	.string "Oh, right... My shouting is scaring\naway the Pokémon.\n$"

Route218_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_FISHERMAN_LUC, Route218_Text_Trainer3Intro, Route218_Text_Trainer3Defeat
	msgbox Route218_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route218_Text_Trainer3Intro:
	.string "Yeah, yeah...\nNothing's biting!\p$"

Route218_Text_Trainer3Defeat:
	.string "Can't catch a fish!\nCan't catch a break!\n$"

Route218_Text_Trainer3Post:
	.string "I was counting on strength in numbers,\nbut...\pPacking it in and going home sounds good\nat a time like this...\n$"


Route218_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_GUITARIST_TONY, Route218_Text_Trainer4Intro, Route218_Text_Trainer4Defeat
	msgbox Route218_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route218_Text_Trainer4Intro:
	.string "Let it rock!\nIt's the rhythm of battle!\p$"

Route218_Text_Trainer4Defeat:
	.string "Can you hear it?\nThat's my guitar weeping...\n$"

Route218_Text_Trainer4Post:
	.string "I'm too torn up to sing anymore...\nI am so cool that way...\n$"


@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route218_EventScript_Placa1::
	msgbox Route218_Text_Placa1, MSGBOX_SIGN
	end

Route218_Text_Placa1:
	.string "Rt. 218\nJubilife City$"

Route218_EventScript_Placa2::
	msgbox Route218_Text_Placa2, MSGBOX_SIGN
	end

Route218_Text_Placa2:
	.string "Rt. 218\nCanalave City$"
