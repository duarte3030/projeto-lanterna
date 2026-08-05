@ Rt6 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt6_MapScripts::
	.byte 0

Unova_Rt6_EventScript_Placa0::
	msgbox Unova_Rt6_Text_R6SignText, MSGBOX_SIGN
	end

Unova_Rt6_EventScript_Placa1::
	msgbox Unova_Rt6_Text_R6LabText, MSGBOX_SIGN
	end

Unova_Rt6_EventScript_Placa2::
	msgbox Unova_Rt6_Text_R6ChargestoneText, MSGBOX_SIGN
	end

Unova_Rt6_EventScript_Npc6::
	msgbox Unova_Rt6_Text_AmoongussText, MSGBOX_NPC
	end

Unova_Rt6_EventScript_Npc7::
	msgbox Unova_Rt6_Text_AmoongussText, MSGBOX_NPC
	end

Unova_Rt6_EventScript_Npc8::
	msgbox Unova_Rt6_Text_AmoongussText, MSGBOX_NPC
	end

Unova_Rt6_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_PARASOL_LADY_R6_1, Unova_Rt6_Text_ParasolLady1R6SeenText, Unova_Rt6_Text_ParasolLady1R6BeatenText
	end

Unova_Rt6_EventScript_Lider10::
	trainerbattle_single TRAINER_UNOVA_PARASOL_LADY_R6_2, Unova_Rt6_Text_ParasolLady2R6SeenText, Unova_Rt6_Text_ParasolLady2R6BeatenText
	end

Unova_Rt6_EventScript_Lider11::
	trainerbattle_single TRAINER_UNOVA_PKMN_RANGERM_R6, Unova_Rt6_Text_PkmnRangerMR6SeenText, Unova_Rt6_Text_PkmnRangerMR6BeatenText
	end

Unova_Rt6_EventScript_Lider12::
	trainerbattle_single TRAINER_UNOVA_PKMN_RANGERF_R6, Unova_Rt6_Text_PkmnRangerFR6SeenText, Unova_Rt6_Text_PkmnRangerFR6BeatenText
	end

Unova_Rt6_EventScript_Lider13::
	trainerbattle_single TRAINER_UNOVA_PKMN_BREEDERF_R6, Unova_Rt6_Text_PkmnBreederFR6SeenText, Unova_Rt6_Text_PkmnBreederFR6BeatenText
	end

Unova_Rt6_EventScript_Lider14::
	trainerbattle_single TRAINER_UNOVA_PKMN_BREEDERM_R6, Unova_Rt6_Text_PkmnBreederMR6SeenText, Unova_Rt6_Text_PkmnBreederMR6BeatenText
	end

Unova_Rt6_EventScript_Lider15::
	trainerbattle_single TRAINER_UNOVA_SCIENTISTM_R6, Unova_Rt6_Text_ScientistMR6SeenText, Unova_Rt6_Text_ScientistMR6BeatenText
	end

Unova_Rt6_EventScript_Lider16::
	trainerbattle_single TRAINER_UNOVA_SCIENTISTF_R6, Unova_Rt6_Text_ScientistFR6SeenText, Unova_Rt6_Text_ScientistFR6BeatenText
	end


Unova_Rt6_Text_R6SignText::
	.string "ROUTE 6."
	.string "\nWest to CHARGE-"
	.string "\lSTONE CAVE.$"

Unova_Rt6_Text_R6LabText::
	.string "ROUTE 6"
	.string "\nWeather Lab.$"

Unova_Rt6_Text_R6ChargestoneText::
	.string "CHARGESTONE CAVE"
	.string "\nahead."
	.string "\pPassage to"
	.string "\nMISTRALTON CITY.$"

Unova_Rt6_Text_AmoongussText::
	.string "Ooong!$"

Unova_Rt6_Text_ParasolLady1R6SeenText::
	.string "Pouring rain…"
	.string "\nFighting POKéMON…$"

Unova_Rt6_Text_ParasolLady1R6BeatenText::
	.string "Ah, the sad melody"
	.string "\nof a total defeat…$"

Unova_Rt6_Text_ParasolLady2R6SeenText::
	.string "Water fun with"
	.string "\nPOKéMON! Do you"
	.string "\pwant to play with"
	.string "\nus?$"

Unova_Rt6_Text_ParasolLady2R6BeatenText::
	.string "My oh my… I lost.$"

Unova_Rt6_Text_PkmnRangerMR6SeenText::
	.string "Nature!$"

Unova_Rt6_Text_PkmnRangerMR6BeatenText::
	.string "Natuuure!$"

Unova_Rt6_Text_PkmnRangerFR6SeenText::
	.string "There are some"
	.string "\nPOKéMON that can"
	.string "\pdisguise them-"
	.string "\nselves!$"

Unova_Rt6_Text_PkmnRangerFR6BeatenText::
	.string "I lost…$"

Unova_Rt6_Text_PkmnBreederFR6SeenText::
	.string "Going through"
	.string "\ntrials is the best"
	.string "\pfor growing"
	.string "\nstronger!$"

Unova_Rt6_Text_PkmnBreederFR6BeatenText::
	.string "You were the"
	.string "\nperfect trial!$"

Unova_Rt6_Text_PkmnBreederMR6SeenText::
	.string "We've just got to"
	.string "\ndo what we can!$"

Unova_Rt6_Text_PkmnBreederMR6BeatenText::
	.string "I feel like I"
	.string "\nunderstood what I"
	.string "\pcould and couldn't"
	.string "\ndo…$"

Unova_Rt6_Text_ScientistMR6SeenText::
	.string "Testing out one's"
	.string "\ntheory is all a"
	.string "\lpart of science!$"

Unova_Rt6_Text_ScientistMR6BeatenText::
	.string "Analyzing the"
	.string "\ncurrent situation"
	.string "\pis also a part of"
	.string "\nscience!$"

Unova_Rt6_Text_ScientistFR6SeenText::
	.string "I shall uncover"
	.string "\nthe mechanism"
	.string "\pbehind trainer and"
	.string "\nPOKéMON relation-"
	.string "\lships!$"

Unova_Rt6_Text_ScientistFR6BeatenText::
	.string "Why are POKéMON"
	.string "\nable to understand"
	.string "\ptheir trainers'"
	.string "\norders?$"
