@ ReversalMountainB1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_ReversalMountainB1F_MapScripts::
	.byte 0

Unova_ReversalMountainB1F_EventScript_Lider3::
	trainerbattle_single TRAINER_UNOVA_HIKER_REVERSAL_1, Unova_ReversalMountainB1F_Text_Hiker1ReversalSeenText, Unova_ReversalMountainB1F_Text_Hiker1ReversalBeatenText
	end

Unova_ReversalMountainB1F_EventScript_Lider4::
	trainerbattle_single TRAINER_UNOVA_BATTLE_GIRL_REVERSAL, Unova_ReversalMountainB1F_Text_BattleGirlReversalSeenText, Unova_ReversalMountainB1F_Text_BattleGirlReversalBeatenText
	end


Unova_ReversalMountainB1F_Text_Hiker1ReversalSeenText::
	.string "Me and my POKéMON"
	.string "\nare professional"
	.string "\ptunnellers! We"
	.string "\nhave no rival!$"

Unova_ReversalMountainB1F_Text_Hiker1ReversalBeatenText::
	.string "To hit a wall like"
	.string "\nthis…$"

Unova_ReversalMountainB1F_Text_BattleGirlReversalSeenText::
	.string "I can feel the"
	.string "\nenergy that over-"
	.string "\pflows from the"
	.string "\nearth!$"

Unova_ReversalMountainB1F_Text_BattleGirlReversalBeatenText::
	.string "I felt the energy"
	.string "\nthat overflowed"
	.string "\lfrom your POKéMON!$"
