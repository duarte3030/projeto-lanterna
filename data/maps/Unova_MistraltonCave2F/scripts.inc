@ MistraltonCave2F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_MistraltonCave2F_MapScripts::
	.byte 0

Unova_MistraltonCave2F_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_ACE_TRAINERM_MISTRALTON_CAVE, Unova_MistraltonCave2F_Text_AceTrainerMMistraltonCaveSeenText, Unova_MistraltonCave2F_Text_AceTrainerMMistraltonCaveBeatenText
	end

Unova_MistraltonCave2F_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_ACE_TRAINERF_MISTRALTON_CAVE, Unova_MistraltonCave2F_Text_AceTrainerFMistraltonCaveSeenText, Unova_MistraltonCave2F_Text_AceTrainerFMistraltonCaveBeatenText
	end


Unova_MistraltonCave2F_Text_AceTrainerMMistraltonCaveSeenText::
	.string "Behold my"
	.string "\nimpressive"
	.string "\pphysique. It's"
	.string "\nfitting of an ACE"
	.string "\lTRAINER!$"

Unova_MistraltonCave2F_Text_AceTrainerMMistraltonCaveBeatenText::
	.string "My POKéMON didn't"
	.string "\ndo my physique"
	.string "\ljustice!$"

Unova_MistraltonCave2F_Text_AceTrainerFMistraltonCaveSeenText::
	.string "Why don't you prove"
	.string "\nto me how much you"
	.string "\pand your POKéMON"
	.string "\nare capable of!$"

Unova_MistraltonCave2F_Text_AceTrainerFMistraltonCaveBeatenText::
	.string "You are capable of"
	.string "\nfar more than we"
	.string "\lare!$"
