@ NacreneOutskirtEast do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_NacreneOutskirtEast_MapScripts::
	.byte 0

Unova_NacreneOutskirtEast_EventScript_Lider0::
	trainerbattle_single TRAINER_UNOVA_BLACKBELT_NACRENE_OUTSKIRT, Unova_NacreneOutskirtEast_Text_BlackbeltNacreneSeenText, Unova_NacreneOutskirtEast_Text_BlackbeltNacreneBeatenText
	end

Unova_NacreneOutskirtEast_EventScript_Lider1::
	trainerbattle_single TRAINER_UNOVA_BATTLE_GIRL_NACRENE_OUTSKIRT, Unova_NacreneOutskirtEast_Text_BattleGirlNacreneSeenText, Unova_NacreneOutskirtEast_Text_BattleGirlNacreneBeatenText
	end


Unova_NacreneOutskirtEast_Text_BlackbeltNacreneSeenText::
	.string "I will read your"
	.string "\nmind and predict"
	.string "\lyour every move!$"

Unova_NacreneOutskirtEast_Text_BlackbeltNacreneBeatenText::
	.string "Your moves… They"
	.string "\nare entirely"
	.string "\lunpredictable!$"

Unova_NacreneOutskirtEast_Text_BattleGirlNacreneSeenText::
	.string "Heh, I wonder what"
	.string "\nwould happen if I"
	.string "\phad all my POKéMON"
	.string "\nattack at once?$"

Unova_NacreneOutskirtEast_Text_BattleGirlNacreneBeatenText::
	.string "I couldn't focus"
	.string "\non the target!$"
