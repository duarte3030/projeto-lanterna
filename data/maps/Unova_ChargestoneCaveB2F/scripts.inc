@ ChargestoneCaveB2F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_ChargestoneCaveB2F_MapScripts::
	.byte 0

Unova_ChargestoneCaveB2F_EventScript_Lider3::
	trainerbattle_single TRAINER_UNOVA_GUITARIST_CHARGESTONE_2, Unova_ChargestoneCaveB2F_Text_Guitarist2ChargestoneSeenText, Unova_ChargestoneCaveB2F_Text_Guitarist2ChargestoneBeatenText
	end

Unova_ChargestoneCaveB2F_EventScript_Lider4::
	trainerbattle_single TRAINER_UNOVA_HIKER_CHARGESTONE_3, Unova_ChargestoneCaveB2F_Text_Hiker3ChargestoneSeenText, Unova_ChargestoneCaveB2F_Text_Hiker3ChargestoneBeatenText
	end

Unova_ChargestoneCaveB2F_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_ACE_TRAINERM_CHARGESTONE_2, Unova_ChargestoneCaveB2F_Text_AceTrainerM2ChargestoneSeenText, Unova_ChargestoneCaveB2F_Text_AceTrainerM2ChargestoneBeatenText
	end


Unova_ChargestoneCaveB2F_Text_Guitarist2ChargestoneSeenText::
	.string "Here I go!$"

Unova_ChargestoneCaveB2F_Text_Guitarist2ChargestoneBeatenText::
	.string "Your style is"
	.string "\nelectrifying!$"

Unova_ChargestoneCaveB2F_Text_Hiker3ChargestoneSeenText::
	.string "It is the way of"
	.string "\ngreeting high in"
	.string "\pthe mountains and"
	.string "\ndown in the caves."
	.string "\pThat's right! We"
	.string "\neach get our POKé-"
	.string "\lMON, and begin!$"

Unova_ChargestoneCaveB2F_Text_Hiker3ChargestoneBeatenText::
	.string "Farewell…"
	.string "\nFarewell, my"
	.string "\lvictory…$"

Unova_ChargestoneCaveB2F_Text_AceTrainerM2ChargestoneSeenText::
	.string "I researched on"
	.string "\nthe PC the best"
	.string "\pway to battle, and"
	.string "\nnow I'm sure to"
	.string "\lwin!$"

Unova_ChargestoneCaveB2F_Text_AceTrainerM2ChargestoneBeatenText::
	.string "Seriously?$"
