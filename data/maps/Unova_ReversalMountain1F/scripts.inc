@ ReversalMountain1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_ReversalMountain1F_MapScripts::
	.byte 0

Unova_ReversalMountain1F_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_SCHOOL_KIDF_REVERSAL, Unova_ReversalMountain1F_Text_SchoolKidFReversalSeenText, Unova_ReversalMountain1F_Text_SchoolKidFReversalBeatenText
	end

Unova_ReversalMountain1F_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_HIKER_REVERSAL_2, Unova_ReversalMountain1F_Text_Hiker2ReversalSeenText, Unova_ReversalMountain1F_Text_Hiker2ReversalBeatenText
	end

Unova_ReversalMountain1F_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_BACKPACKERF_REVERSAL, Unova_ReversalMountain1F_Text_BackpackerFReversalSeenText, Unova_ReversalMountain1F_Text_BackpackerFReversalBeatenText
	end

Unova_ReversalMountain1F_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_BACKPACKERM_REVERSAL, Unova_ReversalMountain1F_Text_BackpackerMReversalSeenText, Unova_ReversalMountain1F_Text_BackpackerMReversalBeatenText
	end

Unova_ReversalMountain1F_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_BLACKBELT_REVERSAL, Unova_ReversalMountain1F_Text_BlackbeltReversalSeenText, Unova_ReversalMountain1F_Text_BlackbeltReversalBeatenText
	end

Unova_ReversalMountain1F_EventScript_Lider10::
	trainerbattle_single TRAINER_UNOVA_LASS_REVERSAL, Unova_ReversalMountain1F_Text_LassReversalSeenText, Unova_ReversalMountain1F_Text_LassReversalBeatenText
	end

Unova_ReversalMountain1F_EventScript_Npc11::
	msgbox Unova_ReversalMountain1F_Text_ReversalGruntIntroText, MSGBOX_NPC
	end


Unova_ReversalMountain1F_Text_SchoolKidFReversalSeenText::
	.string "Hi there! Look at"
	.string "\nmy awesome POKé-"
	.string "\lMON!$"

Unova_ReversalMountain1F_Text_SchoolKidFReversalBeatenText::
	.string "I… I'm not mad!$"

Unova_ReversalMountain1F_Text_Hiker2ReversalSeenText::
	.string "My POKéMON dig"
	.string "\ncause they believe"
	.string "\pthey're gonna find"
	.string "\nsomething, and"
	.string "\pthey battle cause"
	.string "\nthey believe"
	.string "\lthey're gonna win!$"

Unova_ReversalMountain1F_Text_Hiker2ReversalBeatenText::
	.string "I may have lost,"
	.string "\nbut I still"
	.string "\pbelieve in my"
	.string "\nPOKéMON!$"

Unova_ReversalMountain1F_Text_BackpackerFReversalSeenText::
	.string "Hello, lo, lo!$"

Unova_ReversalMountain1F_Text_BackpackerFReversalBeatenText::
	.string "I, I, I…"
	.string "\nLost, lost, lost!$"

Unova_ReversalMountain1F_Text_BackpackerMReversalSeenText::
	.string "You sure are"
	.string "\nunlucky to have"
	.string "\prun into someone"
	.string "\nas strong as me!$"

Unova_ReversalMountain1F_Text_BackpackerMReversalBeatenText::
	.string "I guess it was I"
	.string "\nwho was unlucky to"
	.string "\lrun into you!$"

Unova_ReversalMountain1F_Text_BlackbeltReversalSeenText::
	.string "Oh! I haven't seen"
	.string "\nyou before! Would"
	.string "\pyou mind sparring"
	.string "\nwith me?$"

Unova_ReversalMountain1F_Text_BlackbeltReversalBeatenText::
	.string "Wow, impressive!"
	.string "\pFor one so young,"
	.string "\nyou're quite good!$"

Unova_ReversalMountain1F_Text_LassReversalSeenText::
	.string "Sure, I'll be your"
	.string "\nopponent, right"
	.string "\palongside my"
	.string "\ntrusty MUNNA!$"

Unova_ReversalMountain1F_Text_LassReversalBeatenText::
	.string "You're strong!$"

Unova_ReversalMountain1F_Text_ReversalGruntIntroText::
	.string "…"
	.string "\pI think this is"
	.string "\nthe way out…?$"
