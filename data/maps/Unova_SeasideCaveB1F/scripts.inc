@ SeasideCaveB1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_SeasideCaveB1F_MapScripts::
	.byte 0

Unova_SeasideCaveB1F_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_BLACKBELT_SEASIDE_CAVE_2, Unova_SeasideCaveB1F_Text_BlackbeltSeasideCaveB1FSeenText, Unova_SeasideCaveB1F_Text_BlackbeltSeasideCaveB1FBeatenText
	end

Unova_SeasideCaveB1F_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_BATTLE_GIRL_SEASIDE_CAVE_2, Unova_SeasideCaveB1F_Text_BattleGirlSeasideCaveB1FSeenText, Unova_SeasideCaveB1F_Text_BattleGirlSeasideCaveB1FBeatenText
	end


Unova_SeasideCaveB1F_Text_BlackbeltSeasideCaveB1FSeenText::
	.string "I will never turn"
	.string "\nmy back and run!$"

Unova_SeasideCaveB1F_Text_BlackbeltSeasideCaveB1FBeatenText::
	.string "Ugh… Sometimes you"
	.string "\nmust retreat to"
	.string "\lwin.$"

Unova_SeasideCaveB1F_Text_BattleGirlSeasideCaveB1FSeenText::
	.string "My training will"
	.string "\nnever betray me."
	.string "\pAfter training"
	.string "\nthis much, I am"
	.string "\lcertain to win!$"

Unova_SeasideCaveB1F_Text_BattleGirlSeasideCaveB1FBeatenText::
	.string "…how can that be?"
	.string "\neven after I"
	.string "\ltrained so much?$"
