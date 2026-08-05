@ Dreamyard do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Dreamyard_MapScripts::
	.byte 0

Unova_Dreamyard_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_YOUNGSTER_DREAMYARD, Unova_Dreamyard_Text_YoungsterDreamyardSeenText, Unova_Dreamyard_Text_YoungsterDreamyardBeatenText
	end

Unova_Dreamyard_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_SCHOOL_KIDM_DREAMYARD, Unova_Dreamyard_Text_SchoolKidMDreamyardSeenText, Unova_Dreamyard_Text_SchoolKidMDreamyardBeatenText
	end

Unova_Dreamyard_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_SCHOOL_KIDF_DREAMYARD, Unova_Dreamyard_Text_SchoolKidFDreamyardSeenText, Unova_Dreamyard_Text_SchoolKidFDreamyardBeatenText
	end


Unova_Dreamyard_Text_YoungsterDreamyardSeenText::
	.string "Shorts and POKé-"
	.string "\nMON! This is the"
	.string "\pultimate"
	.string "\ncombination!$"

Unova_Dreamyard_Text_YoungsterDreamyardBeatenText::
	.string "It's not my POKé-"
	.string "\nMON's fault! It's"
	.string "\pnot my shorts'"
	.string "\nfault either!$"

Unova_Dreamyard_Text_SchoolKidMDreamyardSeenText::
	.string "My POKéMON's"
	.string "\nstrong points!"
	.string "\pYou'll see them if"
	.string "\nyou fight!$"

Unova_Dreamyard_Text_SchoolKidMDreamyardBeatenText::
	.string "Hey! Did you see"
	.string "\nmy POKéMON's strong"
	.string "\lpoints?$"

Unova_Dreamyard_Text_SchoolKidFDreamyardSeenText::
	.string "See my extra-"
	.string "\nordinarily pretty"
	.string "\lPOKéMON!$"

Unova_Dreamyard_Text_SchoolKidFDreamyardBeatenText::
	.string "Ah! Its beauty has"
	.string "\nbeen weakened!$"
