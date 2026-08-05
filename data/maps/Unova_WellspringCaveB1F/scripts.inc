@ WellspringCaveB1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_WellspringCaveB1F_MapScripts::
	.byte 0

Unova_WellspringCaveB1F_EventScript_Lider3::
	trainerbattle_single TRAINER_UNOVA_BLACKBELT_WELLSPRING_2, Unova_WellspringCaveB1F_Text_BlackbeltWellspringB1FSeenText, Unova_WellspringCaveB1F_Text_BlackbeltWellspringB1FBeatenText
	end

Unova_WellspringCaveB1F_EventScript_Lider4::
	trainerbattle_single TRAINER_UNOVA_BATTLE_GIRL_WELLSPRING, Unova_WellspringCaveB1F_Text_BattleGirlWellspringB1FSeenText, Unova_WellspringCaveB1F_Text_BattleGirlWellspringB1FBeatenText
	end

Unova_WellspringCaveB1F_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_HIKER_WELLSPRING, Unova_WellspringCaveB1F_Text_HikerWellspringB1FSeenText, Unova_WellspringCaveB1F_Text_HikerWellspringB1FBeatenText
	end


Unova_WellspringCaveB1F_Text_BlackbeltWellspringB1FSeenText::
	.string "Here in the dark-"
	.string "\nness… I feel my"
	.string "\pway through thanks"
	.string "\nto my POKéMON!"
	.string "\pI'll show you the"
	.string "\npower of our bond!$"

Unova_WellspringCaveB1F_Text_BlackbeltWellspringB1FBeatenText::
	.string "Our power went"
	.string "\ndark!$"

Unova_WellspringCaveB1F_Text_BattleGirlWellspringB1FSeenText::
	.string "You gotta have"
	.string "\nstamina! Burn the"
	.string "\pflames of life,"
	.string "\nand never stop"
	.string "\lmoving forward!$"

Unova_WellspringCaveB1F_Text_BattleGirlWellspringB1FBeatenText::
	.string "I'm out of"
	.string "\nstamina!$"

Unova_WellspringCaveB1F_Text_HikerWellspringB1FSeenText::
	.string "A lake that"
	.string "\nspreads beneath"
	.string "\pthe earth… And the"
	.string "\nHIKER who waits"
	.string "\lbeside it!$"

Unova_WellspringCaveB1F_Text_HikerWellspringB1FBeatenText::
	.string "You seized victory"
	.string "\nwith ease, young"
	.string "\ltrainer…$"
