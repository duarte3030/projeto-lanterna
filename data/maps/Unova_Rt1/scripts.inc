@ Rt1 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt1_MapScripts::
	.byte 0

Unova_Rt1_EventScript_Placa0::
	msgbox Unova_Rt1_Text_R1SignText, MSGBOX_SIGN
	end

Unova_Rt1_EventScript_Lider3::
	trainerbattle_single TRAINER_UNOVA_PKMN_RANGERM_R1, Unova_Rt1_Text_PkmnRangerMR1SeenText, Unova_Rt1_Text_PkmnRangerMR1BeatenText
	end

Unova_Rt1_EventScript_Lider4::
	trainerbattle_single TRAINER_UNOVA_PKMN_RANGERF_R1, Unova_Rt1_Text_PkmnRangerFR1SeenText, Unova_Rt1_Text_PkmnRangerFR1BeatenText
	end

Unova_Rt1_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_MAID_R1, Unova_Rt1_Text_MaidR1SeenText, Unova_Rt1_Text_MaidR1BeatenText
	end

Unova_Rt1_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_BLACKBELT_R1, Unova_Rt1_Text_BlackbeltR1SeenText, Unova_Rt1_Text_BlackbeltR1BeatenText
	end

Unova_Rt1_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_BATTLE_GIRL_R1, Unova_Rt1_Text_BattleGirlR1SeenText, Unova_Rt1_Text_BattleGirlR1BeatenText
	end

Unova_Rt1_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_TWINS_R1, Unova_Rt1_Text_TwinsR1SeenText, Unova_Rt1_Text_TwinsR1BeatenText
	end

Unova_Rt1_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_TWINS_R1, Unova_Rt1_Text_TwinsR1SeenText, Unova_Rt1_Text_TwinsR1BeatenText
	end


Unova_Rt1_Text_R1SignText::
	.string "ROUTE 1."
	.string "\pNorth to ACCUMULA"
	.string "\nTOWN, south to"
	.string "\lNUVEMA TOWN.$"

Unova_Rt1_Text_PkmnRangerMR1SeenText::
	.string "I choose a move,"
	.string "\nand my POKéMON"
	.string "\lwill do the move."
	.string "\pIn a moment, that"
	.string "\nmove will reach"
	.string "\lyour POKéMON!$"

Unova_Rt1_Text_PkmnRangerMR1BeatenText::
	.string "I lost, but during"
	.string "\nthe battle, we"
	.string "\pwere connected,"
	.string "\nright?$"

Unova_Rt1_Text_PkmnRangerFR1SeenText::
	.string "Hm? You're headed"
	.string "\nfor the JUNIPER"
	.string "\pPOKéMON LAB, aren't"
	.string "\nyou? Didn't you"
	.string "\pknow? There's a new"
	.string "\nPROF. there now!$"

Unova_Rt1_Text_PkmnRangerFR1BeatenText::
	.string "You're not an"
	.string "\nopponent one could"
	.string "\pdefeat without"
	.string "\ntrying!$"

Unova_Rt1_Text_MaidR1SeenText::
	.string "What? A battle at"
	.string "\na place like this?"
	.string "\pEveryone is"
	.string "\nwatching us!$"

Unova_Rt1_Text_MaidR1BeatenText::
	.string "Well, thanks to"
	.string "\nyou, I've overcome"
	.string "\pmy performance"
	.string "\nanxiety.$"

Unova_Rt1_Text_BlackbeltR1SeenText::
	.string "This is my path!$"

Unova_Rt1_Text_BlackbeltR1BeatenText::
	.string "This is everyone's"
	.string "\npath!$"

Unova_Rt1_Text_BattleGirlR1SeenText::
	.string "Let me test what"
	.string "\nfighting style is"
	.string "\lmore effective!$"

Unova_Rt1_Text_BattleGirlR1BeatenText::
	.string "By any chance, are"
	.string "\nyou a battle"
	.string "\lgenius?$"

Unova_Rt1_Text_TwinsR1SeenText::
	.string "My sister and I"
	.string "\nare of one mind!$"

Unova_Rt1_Text_TwinsR1BeatenText::
	.string "Wow! We lost!$"
