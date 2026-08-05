@ DreamyardB1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_DreamyardB1F_MapScripts::
	.byte 0

Unova_DreamyardB1F_EventScript_Lider4::
	trainerbattle_single TRAINER_UNOVA_SCIENTISTM_DREAMYARD, Unova_DreamyardB1F_Text_ScientistMDreamyardSeenText, Unova_DreamyardB1F_Text_ScientistMDreamyardBeatenText
	end

Unova_DreamyardB1F_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_SCIENTISTF_DREAMYARD, Unova_DreamyardB1F_Text_ScientistFDreamyardSeenText, Unova_DreamyardB1F_Text_ScientistFDreamyardBeatenText
	end

Unova_DreamyardB1F_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_PSYCHICM_DREAMYARD, Unova_DreamyardB1F_Text_PsychicMDreamyardSeenText, Unova_DreamyardB1F_Text_PsychicMDreamyardBeatenText
	end

Unova_DreamyardB1F_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_PSYCHICF_DREAMYARD, Unova_DreamyardB1F_Text_PsychicFDreamyardSeenText, Unova_DreamyardB1F_Text_PsychicFDreamyardBeatenText
	end


Unova_DreamyardB1F_Text_ScientistMDreamyardSeenText::
	.string "Let us conduct"
	.string "\nsome POKéMON"
	.string "\presearch. Yes, let"
	.string "\nus show each"
	.string "\lother our POKéMON.$"

Unova_DreamyardB1F_Text_ScientistMDreamyardBeatenText::
	.string "A new discovery…"
	.string "\nAnd an ever deep-"
	.string "\lening mystery!$"

Unova_DreamyardB1F_Text_ScientistFDreamyardSeenText::
	.string "The mysterious"
	.string "\npsychic power! You"
	.string "\pcannot see it, yet"
	.string "\nit is definitely"
	.string "\lthere!$"

Unova_DreamyardB1F_Text_ScientistFDreamyardBeatenText::
	.string "Argh! I cannot see"
	.string "\nwhat really"
	.string "\lmatters!$"

Unova_DreamyardB1F_Text_PsychicMDreamyardSeenText::
	.string "Heheh…"
	.string "\pI always know who"
	.string "\nwins in every"
	.string "\lbattle!$"

Unova_DreamyardB1F_Text_PsychicMDreamyardBeatenText::
	.string "What…? Was every-"
	.string "\nthing up until now"
	.string "\la coincidence…?$"

Unova_DreamyardB1F_Text_PsychicFDreamyardSeenText::
	.string "I foresaw your"
	.string "\nmove… Should I run"
	.string "\laway from you?$"

Unova_DreamyardB1F_Text_PsychicFDreamyardBeatenText::
	.string "Eek! I foresaw"
	.string "\nyour thoughts, but"
	.string "\lI lost!$"
