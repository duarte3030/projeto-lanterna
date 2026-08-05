LakeValor_MapScripts::
	.byte 0

LakeValor_EventScript_Fisherman::
	msgbox LakeValor_Text_Fisherman, MSGBOX_NPC
	end

LakeValor_EventScript_Hiker::
	msgbox LakeValor_Text_Hiker, MSGBOX_NPC
	end

LakeValor_Text_Fisherman:
	.string "The water's deep out there.\n"
	.string "I've heard strange stories about\n"
	.string "this lake.$"

LakeValor_Text_Hiker:
	.string "Lake Valor sure is quiet this\n"
	.string "time of day.$"

@ Historia: o Lago Valor tomado, e o Comandante Saturn.
@ Texto de pret/pokeplatinum, res/text/lake_valor.json e acuity_lakefront.json.
@ A caverna do lago (valor_cavern) NAO existe neste hack: Saturn fica na margem.

LakeValor_EventScript_GalacticGrunt1::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_LAKE_VALOR_1, LakeValor_Text_Grunt1Intro, LakeValor_Text_Grunt1Defeat
	msgbox LakeValor_Text_Grunt1PostBattle, MSGBOX_AUTOCLOSE
	end

LakeValor_EventScript_GalacticGrunt2::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_LAKE_VALOR_2, LakeValor_Text_Grunt2Intro, LakeValor_Text_Grunt2Defeat
	msgbox LakeValor_Text_Grunt2PostBattle, MSGBOX_AUTOCLOSE
	end

LakeValor_EventScript_Saturn::
	trainerbattle_single TRAINER_SINNOH_COMMANDER_SATURN_VALOR_CAVERN, LakeValor_Text_SaturnIntro, LakeValor_Text_SaturnDefeat
	msgbox LakeValor_Text_SaturnPostBattle, MSGBOX_AUTOCLOSE
	end

LakeValor_Text_Grunt1Intro:
	.string "The mission is proceeding without\n"
	.string "a hitch. The boss should be pleased.\p"
	.string "Everything is for everyone, and\n"
	.string "for the good of Team Galactic!$"

LakeValor_Text_Grunt1Defeat:
	.string "The mission... it had a hitch\n"
	.string "after all...$"

LakeValor_Text_Grunt1PostBattle:
	.string "The Pokémon of the three lakes\n"
	.string "appear to be connected somehow.$"

LakeValor_Text_Grunt2Intro:
	.string "Standing guard is a very important\n"
	.string "assignment!\p"
	.string "I'll make this a success and earn\n"
	.string "myself a Clefairy!$"

LakeValor_Text_Grunt2Defeat:
	.string "There goes my Clefairy...$"

LakeValor_Text_Grunt2PostBattle:
	.string "A Magikarp is weakly flopping\n"
	.string "about at the water's edge...$"

LakeValor_Text_SaturnIntro:
	.string "I recognize your face!\p"
	.string "You're the child who raided the\n"
	.string "Team Galactic building in Eterna!\p"
	.string "Humph! Mars should be ashamed of\n"
	.string "herself, being beaten by a child.\p"
	.string "But anything and anyone that\n"
	.string "opposes Team Galactic must be\l"
	.string "crushed!\p"
	.string "Even the very thought of\n"
	.string "opposition will not be tolerated!$"

LakeValor_Text_SaturnDefeat:
	.string "Gah! Even I, a Commander, only\n"
	.string "managed to buy us time?$"

LakeValor_Text_SaturnPostBattle:
	.string "A child like you will never be able\n"
	.string "to stem the flow of time!\p"
	.string "Team Galactic will get the three\n"
	.string "legendary Pokémon of the lakes!\p"
	.string "With their power, we will create an\n"
	.string "entirely new universe!\p"
	.string "You will bear witness, as you are\n"
	.string "helpless to stop us!$"
