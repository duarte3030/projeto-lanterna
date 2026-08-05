@ Rt7North do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt7North_MapScripts::
	.byte 0

Unova_Rt7North_EventScript_Placa0::
	msgbox Unova_Rt7North_Text_R7NorthSignText, MSGBOX_SIGN
	end

Unova_Rt7North_EventScript_Lider4::
	trainerbattle_single TRAINER_UNOVA_BACKPACKERM_R7, Unova_Rt7North_Text_BackpackerMR7NorthSeenText, Unova_Rt7North_Text_BackpackerMR7NorthBeatenText
	end

Unova_Rt7North_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_BACKPACKERF_R7, Unova_Rt7North_Text_BackpackerFR7NorthSeenText, Unova_Rt7North_Text_BackpackerFR7NorthBeatenText
	end

Unova_Rt7North_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_HARLEQUIN_R7, Unova_Rt7North_Text_HarlequinR7NorthSeenText, Unova_Rt7North_Text_HarlequinR7NorthBeatenText
	end

Unova_Rt7North_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_TWINS_R7, Unova_Rt7North_Text_TwinsR7NorthSeenText, Unova_Rt7North_Text_TwinsR7NorthBeatenText
	end

Unova_Rt7North_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_TWINS_R7, Unova_Rt7North_Text_TwinsR7NorthSeenText, Unova_Rt7North_Text_TwinsR7NorthBeatenText
	end


Unova_Rt7North_Text_R7NorthSignText::
	.string "TWIST MOUNTAIN"
	.string "\nahead.$"

Unova_Rt7North_Text_BackpackerMR7NorthSeenText::
	.string "I travel the world"
	.string "\nbecause I'm look-"
	.string "\ling for danger!"
	.string "\pAre you dangerous?$"

Unova_Rt7North_Text_BackpackerMR7NorthBeatenText::
	.string "You're so danger-"
	.string "\nous, I was in"
	.string "\pdanger of giving"
	.string "\nup the match!$"

Unova_Rt7North_Text_BackpackerFR7NorthSeenText::
	.string "Oh my! My POKéMON"
	.string "\nreally seem raring"
	.string "\lto go today!$"

Unova_Rt7North_Text_BackpackerFR7NorthBeatenText::
	.string "It seems my POKé-"
	.string "\nMON weren't as"
	.string "\pready as I had"
	.string "\nthought!$"

Unova_Rt7North_Text_HarlequinR7NorthSeenText::
	.string "POKéMON battles"
	.string "\nare no joking"
	.string "\lmatter!$"

Unova_Rt7North_Text_HarlequinR7NorthBeatenText::
	.string "You weren't"
	.string "\nclowining around!$"

Unova_Rt7North_Text_TwinsR7NorthSeenText::
	.string "The teamwork of"
	.string "\ntwins… A true"
	.string "\pexample of"
	.string "\nperfection!$"

Unova_Rt7North_Text_TwinsR7NorthBeatenText::
	.string "I can't believe"
	.string "\nit! We should have"
	.string "\pbeen perfect, but"
	.string "\nwe lost!$"
