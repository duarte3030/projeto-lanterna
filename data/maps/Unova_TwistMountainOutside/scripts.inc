@ TwistMountainOutside do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_TwistMountainOutside_MapScripts::
	.byte 0

Unova_TwistMountainOutside_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_NURSE_TWIST_MOUNTAIN, Unova_TwistMountainOutside_Text_NurseTwistMountainOutsideIntroText, Unova_TwistMountainOutside_Text_NurseTwistMountainOutsideWinText
	end

Unova_TwistMountainOutside_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_WORKER_TWIST_MOUNTAIN_1, Unova_TwistMountainOutside_Text_WorkerTwistMountainOutsideSeenText, Unova_TwistMountainOutside_Text_WorkerTwistMountainOutsideBeatenText
	end

Unova_TwistMountainOutside_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_HIKER_TWIST_MOUNTAIN_2, Unova_TwistMountainOutside_Text_HikerTwistMountainOutsideSeenText, Unova_TwistMountainOutside_Text_HikerTwistMountainOutsideBeatenText
	end

Unova_TwistMountainOutside_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_VETERANM_TWIST_MOUNTAIN_1, Unova_TwistMountainOutside_Text_VeteranMTwistMountainOutsideSeenText, Unova_TwistMountainOutside_Text_VeteranMTwistMountainOutsideBeatenText
	end


Unova_TwistMountainOutside_Text_NurseTwistMountainOutsideIntroText::
	.string "I'm a nurse, but"
	.string "\nI'm also a POKé-"
	.string "\lMON trainer."
	.string "\pIf you can defeat"
	.string "\nme in a battle,"
	.string "\lI'll heal your"
	.string "\lPOKéMON.$"

Unova_TwistMountainOutside_Text_NurseTwistMountainOutsideWinText::
	.string "Ah, I see.$"

Unova_TwistMountainOutside_Text_WorkerTwistMountainOutsideSeenText::
	.string "I've found a"
	.string "\nstrong looking"
	.string "\ptrainer during my"
	.string "\npatrol! Go, my"
	.string "\lPOKéMON!$"

Unova_TwistMountainOutside_Text_WorkerTwistMountainOutsideBeatenText::
	.string "It's just as I"
	.string "\nthought! A"
	.string "\pmonstrously strong"
	.string "\ntrainer!$"

Unova_TwistMountainOutside_Text_HikerTwistMountainOutsideSeenText::
	.string "Why do I dig? Why"
	.string "\ndo you fight?$"

Unova_TwistMountainOutside_Text_HikerTwistMountainOutsideBeatenText::
	.string "Your past"
	.string "\nexperience…"
	.string "\pIs that the source"
	.string "\nof your strength?$"

Unova_TwistMountainOutside_Text_VeteranMTwistMountainOutsideSeenText::
	.string "OK! I will show"
	.string "\nyou the results of"
	.string "\lmy daily workouts!$"

Unova_TwistMountainOutside_Text_VeteranMTwistMountainOutsideBeatenText::
	.string "Was my training"
	.string "\ntoo unbalanced?$"
