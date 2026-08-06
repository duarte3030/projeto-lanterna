@ Rt20 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt20_MapScripts::
	.byte 0

Unova_Rt20_EventScript_Lider4::
	trainerbattle_single TRAINER_UNOVA_SCHOOL_KIDM_R20_1, Unova_Rt20_Text_SchoolKidM1R20SeenText, Unova_Rt20_Text_SchoolKidM1R20BeatenText
	end

Unova_Rt20_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_SCHOOL_KIDM_R20_2, Unova_Rt20_Text_SchoolKidM2R20SeenText, Unova_Rt20_Text_SchoolKidM2R20BeatenText
	end

Unova_Rt20_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_SCHOOL_KIDM_R20_3, Unova_Rt20_Text_SchoolKidM3R20SeenText, Unova_Rt20_Text_SchoolKidM3R20BeatenText
	end

Unova_Rt20_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_TWINS_R20, Unova_Rt20_Text_TwinsR20SeenText, Unova_Rt20_Text_TwinsR20BeatenText
	end

Unova_Rt20_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_TWINS_R20, Unova_Rt20_Text_TwinsR20SeenText, Unova_Rt20_Text_TwinsR20BeatenText
	end

Unova_Rt20_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_SCHOOL_KIDF_R20_1, Unova_Rt20_Text_SchoolKidF1R20SeenText, Unova_Rt20_Text_SchoolKidF1R20BeatenText
	end

Unova_Rt20_EventScript_Lider10::
	trainerbattle_single TRAINER_UNOVA_SCHOOL_KIDF_R20_2, Unova_Rt20_Text_SchoolKidF2R20SeenText, Unova_Rt20_Text_SchoolKidF2R20BeatenText
	end

Unova_Rt20_EventScript_Lider11::
	trainerbattle_single TRAINER_UNOVA_SCHOOL_KIDF_R20_3, Unova_Rt20_Text_SchoolKidF3R20SeenText, Unova_Rt20_Text_SchoolKidF3R20BeatenText
	end

Unova_Rt20_EventScript_Lider12::
	trainerbattle_single TRAINER_UNOVA_NURSERY_AIDE_R20, Unova_Rt20_Text_NurseryAideR20SeenText, Unova_Rt20_Text_NurseryAideR20BeatenText
	end


Unova_Rt20_Text_SchoolKidM1R20SeenText::
	.string "To me, the battle-"
	.string "\nfield is a place"
	.string "\lfor learning!$"

Unova_Rt20_Text_SchoolKidM1R20BeatenText::
	.string "W-wait! I've got"
	.string "\nto analyze this"
	.string "\ldefeat!$"

Unova_Rt20_Text_SchoolKidM2R20SeenText::
	.string "Hey, you! You're"
	.string "\ngonna lose and"
	.string "\lcry!$"

Unova_Rt20_Text_SchoolKidM2R20BeatenText::
	.string "…Grrr!$"

Unova_Rt20_Text_SchoolKidM3R20SeenText::
	.string "You look tough!"
	.string "\pAll right! My"
	.string "\nPOKéMON are burn-"
	.string "\ling for a fight"
	.string "\pagainst a tough"
	.string "\nopponent!$"

Unova_Rt20_Text_SchoolKidM3R20BeatenText::
	.string "Arg! I wasn't able"
	.string "\nto give good"
	.string "\lorders!$"

Unova_Rt20_Text_TwinsR20SeenText::
	.string "The two of us make"
	.string "\nan amazing"
	.string "\lcombination!"
	.string "\pLet's battle!$"

Unova_Rt20_Text_TwinsR20BeatenText::
	.string "Our amazing"
	.string "\ncombination…$"

Unova_Rt20_Text_SchoolKidF1R20SeenText::
	.string "Is that a POKéDEX?"
	.string "\pI'd love it if you"
	.string "\nwould show me lots"
	.string "\pof different kinds"
	.string "\nof POKéMON!$"

Unova_Rt20_Text_SchoolKidF1R20BeatenText::
	.string "I've never seen a"
	.string "\nPOKéMON like that!$"

Unova_Rt20_Text_SchoolKidF2R20SeenText::
	.string "Hi, hi! Trainer!"
	.string "\nPlease show me"
	.string "\pwhat kinds of"
	.string "\nPOKéMON you are"
	.string "\ltraining!$"

Unova_Rt20_Text_SchoolKidF2R20BeatenText::
	.string "Great, great! I"
	.string "\ndidn't know that"
	.string "\pway to raise POKé-"
	.string "\nMON!$"

Unova_Rt20_Text_SchoolKidF3R20SeenText::
	.string "Ta-da! Here's my"
	.string "\ncute POKéMON!$"

Unova_Rt20_Text_SchoolKidF3R20BeatenText::
	.string "Oh maaaan!$"

Unova_Rt20_Text_NurseryAideR20SeenText::
	.string "I always give it"
	.string "\nmy best when I'm"
	.string "\paround kids and"
	.string "\nPOKéMON!$"

Unova_Rt20_Text_NurseryAideR20BeatenText::
	.string "Oh no! I'm not"
	.string "\nbeing a very good"
	.string "\pexample to the"
	.string "\nkids, am I?$"

@ NPCs ligados a partir do BW3G por dev_scripts/importa_npcs_unova.py

@ FRUITTREE_R_20 do BW3G. ponytail: no gen 2 a arvore reenche;
@ aqui a fruta sai uma vez, porque replantio e outra mecanica.
Unova_Rt20_EventScript_Arvore::
	lock
	goto_if_set FLAG_UNOVA_ARVORE_R_20, Unova_EventScript_GrutaVazia
	giveitem ITEM_PECHA_BERRY
	setflag FLAG_UNOVA_ARVORE_R_20
	release
	end
