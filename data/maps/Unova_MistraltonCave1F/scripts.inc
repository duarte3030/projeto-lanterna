@ MistraltonCave1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_MistraltonCave1F_MapScripts::
	.byte 0

Unova_MistraltonCave1F_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_HIKER_MISTRALTON_CAVE_1, Unova_MistraltonCave1F_Text_Hiker1MistraltonCaveSeenText, Unova_MistraltonCave1F_Text_Hiker1MistraltonCaveBeatenText
	end

Unova_MistraltonCave1F_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_HIKER_MISTRALTON_CAVE_2, Unova_MistraltonCave1F_Text_Hiker2MistraltonCaveSeenText, Unova_MistraltonCave1F_Text_Hiker2MistraltonCaveBeatenText
	end


Unova_MistraltonCave1F_Text_Hiker1MistraltonCaveSeenText::
	.string "Whooo! Mountain!!$"

Unova_MistraltonCave1F_Text_Hiker1MistraltonCaveBeatenText::
	.string "Let the scales"
	.string "\nfall from your"
	.string "\leyes!$"

Unova_MistraltonCave1F_Text_Hiker2MistraltonCaveSeenText::
	.string "I'll knock you"
	.string "\ndown with mountain"
	.string "\lpower!$"

Unova_MistraltonCave1F_Text_Hiker2MistraltonCaveBeatenText::
	.string "Your power is off"
	.string "\nthe charts!$"
