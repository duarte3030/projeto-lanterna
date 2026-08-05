@ Rt3 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt3_MapScripts::
	.byte 0

Unova_Rt3_EventScript_Placa0::
	msgbox Unova_Rt3_Text_R3WellspringSignText, MSGBOX_SIGN
	end

Unova_Rt3_EventScript_Placa1::
	msgbox Unova_Rt3_Text_R3DayCareSignText, MSGBOX_SIGN
	end

Unova_Rt3_EventScript_Lider4::
	trainerbattle_single TRAINER_UNOVA_PKMN_RANGERM_R3, Unova_Rt3_Text_PkmnRangerMR3SeenText, Unova_Rt3_Text_PkmnRangerMR3BeatenText
	end

Unova_Rt3_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_PKMN_RANGERF_R3, Unova_Rt3_Text_PkmnRangerFR3SeenText, Unova_Rt3_Text_PkmnRangerFR3BeatenText
	end

Unova_Rt3_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_SOCIALITE_R3, Unova_Rt3_Text_SocialiteR3SeenText, Unova_Rt3_Text_SocialiteR3BeatenText
	end

Unova_Rt3_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_FISHER_R3_1, Unova_Rt3_Text_Fisher1R3SeenText, Unova_Rt3_Text_Fisher1R3BeatenText
	end

Unova_Rt3_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_FISHER_R3_2, Unova_Rt3_Text_Fisher2R3SeenText, Unova_Rt3_Text_Fisher2R3BeatenText
	end

Unova_Rt3_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_ARTIST_R3, Unova_Rt3_Text_ArtistR3SeenText, Unova_Rt3_Text_ArtistR3BeatenText
	end

Unova_Rt3_EventScript_Lider10::
	trainerbattle_single TRAINER_UNOVA_GENTLEMAN_R3, Unova_Rt3_Text_GentlemanR3SeenText, Unova_Rt3_Text_GentlemanR3BeatenText
	end


Unova_Rt3_Text_R3WellspringSignText::
	.string "WELLSPRING CAVE."
	.string "\pBeware of wild"
	.string "\nPOKéMON!$"

Unova_Rt3_Text_R3DayCareSignText::
	.string "DAY CARE."
	.string "\pLet your POKéMON"
	.string "\nplay with us!$"

Unova_Rt3_Text_PkmnRangerMR3SeenText::
	.string "Forming a team of"
	.string "\nPOKéMON that can"
	.string "\pwork well together"
	.string "\nis key in battle!"
	.string "\lLet's begin!$"

Unova_Rt3_Text_PkmnRangerMR3BeatenText::
	.string "Oh no! The way I"
	.string "\npositioned my"
	.string "\pPOKéMON was"
	.string "\nterrible!$"

Unova_Rt3_Text_PkmnRangerFR3SeenText::
	.string "Melding into the"
	.string "\nwild landscape…"
	.string "\pThat's what a POKé-"
	.string "\nMON RANGER does!$"

Unova_Rt3_Text_PkmnRangerFR3BeatenText::
	.string "I am such a weak-"
	.string "\nling! I will dis-"
	.string "\lappear back into"
	.string "\lthe wilderness!$"

Unova_Rt3_Text_SocialiteR3SeenText::
	.string "Two years ago, I"
	.string "\nparted ways with"
	.string "\lmy POKéMON…"
	.string "\pYet in my heart,"
	.string "\nI've never stopped"
	.string "\pbeing a POKéMON"
	.string "\ntrainer!$"

Unova_Rt3_Text_SocialiteR3BeatenText::
	.string "This is the type"
	.string "\nof defeat that"
	.string "\ponly a POKéMON"
	.string "\ntrainer can"
	.string "\lexperience.$"

Unova_Rt3_Text_Fisher1R3SeenText::
	.string "I am a wonderful"
	.string "\nfisherman who"
	.string "\lloves everything!$"

Unova_Rt3_Text_Fisher1R3BeatenText::
	.string "I even love a"
	.string "\ndisappointing"
	.string "\lresult!$"

Unova_Rt3_Text_Fisher2R3SeenText::
	.string "Hey! What kinds of"
	.string "\ngreat POKéMON have"
	.string "\lyou caught?$"

Unova_Rt3_Text_Fisher2R3BeatenText::
	.string "Ho ho! These are"
	.string "\nsome impressive"
	.string "\lPOKéMON!$"

Unova_Rt3_Text_ArtistR3SeenText::
	.string "A high level"
	.string "\nbattling technique"
	.string "\pis art in its own"
	.string "\nway!$"

Unova_Rt3_Text_ArtistR3BeatenText::
	.string "Your strength can't"
	.string "\nbe put into words!$"

Unova_Rt3_Text_GentlemanR3SeenText::
	.string "I came here"
	.string "\nbecause this place"
	.string "\pfeels quite"
	.string "\nnostalgic to me…"
	.string "\pBut I'd rather"
	.string "\nbattle than stroll"
	.string "\ldown memory lane!$"

Unova_Rt3_Text_GentlemanR3BeatenText::
	.string "I see… So that's"
	.string "\nit. I sed to also"
	.string "\pbe that focused"
	.string "\nlong ago.$"

@ Placas trazidas do BW3G por dev_scripts/importa_placas_unova.py

@ Gruta escondida do BW3G (tier 2). ponytail: la ela reenche
@ todo dia; aqui e uma flag e o item sai uma vez so.
Unova_Rt3_EventScript_Gruta4BC::
	goto_if_set FLAG_UNOVA_GRUTA_R3, Unova_EventScript_GrutaVazia
	setflag FLAG_UNOVA_GRUTA_R3
	goto Unova_EventScript_GrutaTier2
