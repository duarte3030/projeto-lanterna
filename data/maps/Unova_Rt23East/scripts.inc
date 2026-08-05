@ Rt23East do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt23East_MapScripts::
	.byte 0

Unova_Rt23East_EventScript_Npc0::
	msgbox Unova_Rt23East_Text_R23Officer1StopText, MSGBOX_NPC
	end

Unova_Rt23East_EventScript_Npc1::
	msgbox Unova_Rt23East_Text_R23Officer2StopText, MSGBOX_NPC
	end

Unova_Rt23East_EventScript_Npc2::
	msgbox Unova_Rt23East_Text_R23Officer3HaveBadgeText, MSGBOX_NPC
	end

Unova_Rt23East_EventScript_Npc3::
	msgbox Unova_Rt23East_Text_R23Officer4HaveBadgeText, MSGBOX_NPC
	end

Unova_Rt23East_EventScript_Npc4::
	msgbox Unova_Rt23East_Text_R23Officer5HaveBadgeText, MSGBOX_NPC
	end

Unova_Rt23East_EventScript_Npc5::
	msgbox Unova_Rt23East_Text_R23Officer6StopText, MSGBOX_NPC
	end

Unova_Rt23East_EventScript_Lider12::
	trainerbattle_single TRAINER_UNOVA_ACE_TRAINERM_R23_1, Unova_Rt23East_Text_AceTrainerM1R23SeenText, Unova_Rt23East_Text_AceTrainerM1R23BeatenText
	end

Unova_Rt23East_EventScript_Lider13::
	trainerbattle_single TRAINER_UNOVA_ACE_TRAINERF_R23_1, Unova_Rt23East_Text_AceTrainerF1R23SeenText, Unova_Rt23East_Text_AceTrainerF1R23BeatenText
	end


Unova_Rt23East_Text_R23Officer1StopText::
	.string "Stop! Ahead lies"
	.string "\nthe path to the"
	.string "\lPOKéMON LEAGUE."
	.string "\pOnly those who"
	.string "\nhave collected"
	.string "\pall 8 POKéMON"
	.string "\nLEAGUE GYM BADGES"
	.string "\lmay enter."
	.string "\pYou cannot pass"
	.string "\nhere unless you"
	.string "\phave the"
	.string "\nSPOOKYBADGE.$"

Unova_Rt23East_Text_R23Officer2StopText::
	.string "Stop! Ahead lies"
	.string "\nthe path to the"
	.string "\lPOKéMON LEAGUE."
	.string "\pOnly those who"
	.string "\nhave collected"
	.string "\pall 8 POKéMON"
	.string "\nLEAGUE GYM BADGES"
	.string "\lmay enter."
	.string "\pYou cannot pass"
	.string "\nhere unless you"
	.string "\phave the"
	.string "\nINSECTBADGE.$"

Unova_Rt23East_Text_R23Officer3HaveBadgeText::
	.string "Oh, that is the"
	.string "\nTOXICBADGE!"
	.string "\pYou may pass.$"

Unova_Rt23East_Text_R23Officer4HaveBadgeText::
	.string "Oh, that is the"
	.string "\nBASICBADGE!"
	.string "\pYou may pass.$"

Unova_Rt23East_Text_R23Officer5HaveBadgeText::
	.string "Oh, that is the"
	.string "\nGARNISHBADGE!"
	.string "\pYou may pass.$"

Unova_Rt23East_Text_R23Officer6StopText::
	.string "Stop! Ahead lies"
	.string "\nthe path to the"
	.string "\lPOKéMON LEAGUE."
	.string "\pOnly those who"
	.string "\nhave collected"
	.string "\pall 8 POKéMON"
	.string "\nLEAGUE GYM BADGES"
	.string "\lmay enter."
	.string "\pYou cannot pass"
	.string "\nhere unless you"
	.string "\phave the"
	.string "\nJETBADGE.$"

Unova_Rt23East_Text_AceTrainerM1R23SeenText::
	.string "Our battle will"
	.string "\nsurely be worth a"
	.string "\ppage in the book"
	.string "\nof your journey!$"

Unova_Rt23East_Text_AceTrainerM1R23BeatenText::
	.string "If only I could've"
	.string "\nwon, I would have"
	.string "\pmade an impression"
	.string "\non you.$"

Unova_Rt23East_Text_AceTrainerF1R23SeenText::
	.string "I can see the plea"
	.string "\nin my POKéMON's"
	.string "\peyes. To fight!"
	.string "\nAnd to win!$"

Unova_Rt23East_Text_AceTrainerF1R23BeatenText::
	.string "The eyes of your"
	.string "\nPOKéMON are"
	.string "\pglimmering with"
	.string "\nstrength!$"

@ Placas trazidas do BW3G por dev_scripts/importa_placas_unova.py

@ Gruta escondida do BW3G (tier 3). ponytail: la ela reenche
@ todo dia; aqui e uma flag e o item sai uma vez so.
Unova_Rt23East_EventScript_Gruta4C2::
	goto_if_set FLAG_UNOVA_GRUTA_R23, Unova_EventScript_GrutaVazia
	setflag FLAG_UNOVA_GRUTA_R23
	goto Unova_EventScript_GrutaTier3
