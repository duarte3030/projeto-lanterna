IronIslandB2FLeftRoom_MapScripts::
	.byte 0

@ Treinador do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_masmorra_sinnoh.py)

IronIslandB2FLeftRoom_EventScript_HikerDamon::
	trainerbattle_single TRAINER_SINNOH_HIKER_DAMON, IronIslandB2FLeftRoom_Text_HikerDamonIntro, IronIslandB2FLeftRoom_Text_HikerDamonDefeat
	msgbox IronIslandB2FLeftRoom_Text_HikerDamonPost, MSGBOX_AUTOCLOSE
	end

IronIslandB2FLeftRoom_Text_HikerDamonIntro:
	.string "Every good Hiker gets a boost of\nenergy when surrounded by boulders!\pWrooooar! Coming at you!\nLet me blow off some steam!$"

IronIslandB2FLeftRoom_Text_HikerDamonDefeat:
	.string "Whew... Crazy, delicious sugar!\nI think I've calmed down now...$"

IronIslandB2FLeftRoom_Text_HikerDamonPost:
	.string "If it's called a mountain, you can\nbe sure I'll be climbing it.\pEven if it's a mountain of food, I'll\nstill be stickin' my flag on top!$"

IronIslandB2FLeftRoom_EventScript_HikerMaurice::
	trainerbattle_single TRAINER_SINNOH_HIKER_MAURICE, IronIslandB2FLeftRoom_Text_HikerMauriceIntro, IronIslandB2FLeftRoom_Text_HikerMauriceDefeat
	msgbox IronIslandB2FLeftRoom_Text_HikerMauricePost, MSGBOX_AUTOCLOSE
	end

IronIslandB2FLeftRoom_Text_HikerMauriceIntro:
	.string "When you're up in the mountains,\na battle'd do for a proper greeting!$"

IronIslandB2FLeftRoom_Text_HikerMauriceDefeat:
	.string "Yahoo!$"

IronIslandB2FLeftRoom_Text_HikerMauricePost:
	.string "Actually, when you're up in the\nmountains, a simple hi'd do if\pyou walk past someone.\pOh, and this isn't the mountains.$"

IronIslandB2FLeftRoom_EventScript_BlackBeltKendal::
	trainerbattle_single TRAINER_SINNOH_BLACK_BELT_KENDAL, IronIslandB2FLeftRoom_Text_BlackBeltKendalIntro, IronIslandB2FLeftRoom_Text_BlackBeltKendalDefeat
	msgbox IronIslandB2FLeftRoom_Text_BlackBeltKendalPost, MSGBOX_AUTOCLOSE
	end

IronIslandB2FLeftRoom_Text_BlackBeltKendalIntro:
	.string "I'll pound the fear of my fists into\nyou all karate style, punk!$"

IronIslandB2FLeftRoom_Text_BlackBeltKendalDefeat:
	.string "I'm so sorry...\nI got a bit mouthy there, didn't I?$"

IronIslandB2FLeftRoom_Text_BlackBeltKendalPost:
	.string "So, I'm gonna try and shatter steel!\pI wonder how many more years it\nwould take for me to do that?$"

IronIslandB2FLeftRoom_EventScript_BattleGirlTyler::
	trainerbattle_single TRAINER_SINNOH_BATTLE_GIRL_TYLER, IronIslandB2FLeftRoom_Text_BattleGirlTylerIntro, IronIslandB2FLeftRoom_Text_BattleGirlTylerDefeat
	msgbox IronIslandB2FLeftRoom_Text_BattleGirlTylerPost, MSGBOX_AUTOCLOSE
	end

IronIslandB2FLeftRoom_Text_BattleGirlTylerIntro:
	.string "Beating you would be my 100th\nstraight win! Here's to a fun battle!$"

IronIslandB2FLeftRoom_Text_BattleGirlTylerDefeat:
	.string "How could I lose now?!\nThis is beyond aggravating!$"

IronIslandB2FLeftRoom_Text_BattleGirlTylerPost:
	.string "I wish I could beat Maylene in\nVeilstone City one day...$"

IronIslandB2FLeftRoom_EventScript_WorkerBrendon::
	trainerbattle_single TRAINER_SINNOH_WORKER_BRENDON, IronIslandB2FLeftRoom_Text_WorkerBrendonIntro, IronIslandB2FLeftRoom_Text_WorkerBrendonDefeat
	msgbox IronIslandB2FLeftRoom_Text_WorkerBrendonPost, MSGBOX_AUTOCLOSE
	end

IronIslandB2FLeftRoom_Text_WorkerBrendonIntro:
	.string "Hey! This is no playground!\nIf you're gonna play, battle me!$"

IronIslandB2FLeftRoom_Text_WorkerBrendonDefeat:
	.string "You played me like an amateur!$"

IronIslandB2FLeftRoom_Text_WorkerBrendonPost:
	.string "They were going to close this place\nup so no one could get in.\pBut, they left it open so people and\nPokémon can get together here.$"

IronIslandB2FLeftRoom_EventScript_WorkerQuentin::
	trainerbattle_single TRAINER_SINNOH_WORKER_QUENTIN, IronIslandB2FLeftRoom_Text_WorkerQuentinIntro, IronIslandB2FLeftRoom_Text_WorkerQuentinDefeat
	msgbox IronIslandB2FLeftRoom_Text_WorkerQuentinPost, MSGBOX_AUTOCLOSE
	end

IronIslandB2FLeftRoom_Text_WorkerQuentinIntro:
	.string "The Canalave Gym folks use this place\nas their training grounds.$"

IronIslandB2FLeftRoom_Text_WorkerQuentinDefeat:
	.string "Maybe I should head to the Gym and\nwork out there...$"

IronIslandB2FLeftRoom_Text_WorkerQuentinPost:
	.string "Roark spent his childhood playing\nhere, I think...$"

IronIslandB2FLeftRoom_EventScript_AceTrainerJonah::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_JONAH, IronIslandB2FLeftRoom_Text_AceTrainerJonahIntro, IronIslandB2FLeftRoom_Text_AceTrainerJonahDefeat
	msgbox IronIslandB2FLeftRoom_Text_AceTrainerJonahPost, MSGBOX_AUTOCLOSE
	end

IronIslandB2FLeftRoom_Text_AceTrainerJonahIntro:
	.string "If we were to battle, your Pokémon \nwould become tougher.\pLikewise, my Pokémon would also\nbecome tougher.\pIt's all good.\nThis calls for a battle!$"

IronIslandB2FLeftRoom_Text_AceTrainerJonahDefeat:
	.string "You know, I would have really enjoyed\na win there. Would've been real nice.$"

IronIslandB2FLeftRoom_Text_AceTrainerJonahPost:
	.string "This mine's been abandoned, but\nnow it's home to many Pokémon.\pI guess everything finds a place\nto call home someday...$"

IronIslandB2FLeftRoom_EventScript_AceTrainerBrenda::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_BRENDA, IronIslandB2FLeftRoom_Text_AceTrainerBrendaIntro, IronIslandB2FLeftRoom_Text_AceTrainerBrendaDefeat
	msgbox IronIslandB2FLeftRoom_Text_AceTrainerBrendaPost, MSGBOX_AUTOCLOSE
	end

IronIslandB2FLeftRoom_Text_AceTrainerBrendaIntro:
	.string "Tough Pokémon...\nTough Trainers...\pYou tell me, where else can I find\na place as good as this to train?$"

IronIslandB2FLeftRoom_Text_AceTrainerBrendaDefeat:
	.string "That was good.\nYou've bonded well with your Pokémon.$"

IronIslandB2FLeftRoom_Text_AceTrainerBrendaPost:
	.string "Tough Pokémon...\nTough Trainers...\pTheir strength comes from their bond.\nAnd that's something that can be\pmade stronger anywhere.$"
