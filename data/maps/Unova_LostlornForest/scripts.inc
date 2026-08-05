@ LostlornForest do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_LostlornForest_MapScripts::
	.byte 0

Unova_LostlornForest_EventScript_Placa0::
	msgbox Unova_LostlornForest_Text_LostlornForestSignText, MSGBOX_SIGN
	end

Unova_LostlornForest_EventScript_Placa1::
	msgbox Unova_LostlornForest_Text_LostlornR16SignText, MSGBOX_SIGN
	end

Unova_LostlornForest_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_SCHOOL_KIDF_LOSTLORN, Unova_LostlornForest_Text_SchoolKidFLostlornSeenText, Unova_LostlornForest_Text_SchoolKidFLostlornBeatenText
	end

Unova_LostlornForest_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_SCHOOL_KIDM_LOSTLORN, Unova_LostlornForest_Text_SchoolKidMLostlornSeenText, Unova_LostlornForest_Text_SchoolKidMLostlornBeatenText
	end

Unova_LostlornForest_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_PKMN_BREEDERM_LOSTLORN, Unova_LostlornForest_Text_PkmnBreederMLostlornSeenText, Unova_LostlornForest_Text_PkmnBreederMLostlornBeatenText
	end

Unova_LostlornForest_EventScript_Lider10::
	trainerbattle_single TRAINER_UNOVA_PKMN_BREEDERF_LOSTLORN, Unova_LostlornForest_Text_PkmnBreederFLostlornSeenText, Unova_LostlornForest_Text_PkmnBreederFLostlornBeatenText
	end

Unova_LostlornForest_EventScript_Lider11::
	trainerbattle_single TRAINER_UNOVA_YOUNGSTER_LOSTLORN, Unova_LostlornForest_Text_YoungsterLostlornSeenText, Unova_LostlornForest_Text_YoungsterLostlornBeatenText
	end

Unova_LostlornForest_EventScript_Lider12::
	trainerbattle_single TRAINER_UNOVA_LASS_LOSTLORN, Unova_LostlornForest_Text_LassLostlornSeenText, Unova_LostlornForest_Text_LassLostlornBeatenText
	end


Unova_LostlornForest_Text_LostlornForestSignText::
	.string "LOSTLORN FOREST"
	.string "\pTake caution not"
	.string "\nto become lost.$"

Unova_LostlornForest_Text_LostlornR16SignText::
	.string "ROUTE 16 ahead."
	.string "\pPassage to"
	.string "\nNIMBASA CITY.$"

Unova_LostlornForest_Text_SchoolKidFLostlornSeenText::
	.string "I need to research"
	.string "\nthe EXP points of"
	.string "\pPOKéMON for my"
	.string "\nhomework!$"

Unova_LostlornForest_Text_SchoolKidFLostlornBeatenText::
	.string "It's not fair to"
	.string "\nuse moves I wasn't"
	.string "\lexpecting!$"

Unova_LostlornForest_Text_SchoolKidMLostlornSeenText::
	.string "I have a riddle"
	.string "\nfor you! Do you"
	.string "\pknow what is"
	.string "\ndistant but close?$"

Unova_LostlornForest_Text_SchoolKidMLostlornBeatenText::
	.string "The difference"
	.string "\nbetween winning"
	.string "\land losing!$"

Unova_LostlornForest_Text_PkmnBreederMLostlornSeenText::
	.string "Having lots of"
	.string "\nbattles is the"
	.string "\pbest way to raise"
	.string "\nPOKéMON quickly.$"

Unova_LostlornForest_Text_PkmnBreederMLostlornBeatenText::
	.string "Your training"
	.string "\nmethod is great,"
	.string "\pI'm going to copy"
	.string "\nit!$"

Unova_LostlornForest_Text_PkmnBreederFLostlornSeenText::
	.string "I need to practice"
	.string "\nmore as a POKéMON"
	.string "\lbreeder."
	.string "\pPlease, be my"
	.string "\nopponent!$"

Unova_LostlornForest_Text_PkmnBreederFLostlornBeatenText::
	.string "I've still got a"
	.string "\nlong way to go…"
	.string "\pI'll keep raising"
	.string "\nmy POKéMON!$"

Unova_LostlornForest_Text_YoungsterLostlornSeenText::
	.string "I might be lost"
	.string "\nright now, but"
	.string "\pI'll battle you"
	.string "\nanyway!$"

Unova_LostlornForest_Text_YoungsterLostlornBeatenText::
	.string "I don't stand a"
	.string "\nchance if I fight"
	.string "\lwhen I'm lost!$"

Unova_LostlornForest_Text_LassLostlornSeenText::
	.string "Are you ready? I"
	.string "\nam! Let's go!$"

Unova_LostlornForest_Text_LassLostlornBeatenText::
	.string "What? I never even"
	.string "\nconsidered losing"
	.string "\pbefore going into"
	.string "\nbattle!$"
