@ Rt5 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt5_MapScripts::
	.byte 0

Unova_Rt5_EventScript_Placa0::
	msgbox Unova_Rt5_Text_R5BridgeSignText, MSGBOX_SIGN
	end

Unova_Rt5_EventScript_Placa1::
	msgbox Unova_Rt5_Text_R5NimbasaSignText, MSGBOX_SIGN
	end

Unova_Rt5_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_DANCER_R5_1, Unova_Rt5_Text_Dancer1R5SeenText, Unova_Rt5_Text_Dancer1R5BeatenText
	end

Unova_Rt5_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_DANCER_R5_2, Unova_Rt5_Text_Dancer2R5SeenText, Unova_Rt5_Text_Dancer2R5BeatenText
	end

Unova_Rt5_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_LINEBACKER_R5, Unova_Rt5_Text_LinebackerR5SeenText, Unova_Rt5_Text_LinebackerR5BeatenText
	end

Unova_Rt5_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_BAKER_R5, Unova_Rt5_Text_BakerR5SeenText, Unova_Rt5_Text_BakerR5BeatenText
	end

Unova_Rt5_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_ARTIST_R5, Unova_Rt5_Text_ArtistR5SeenText, Unova_Rt5_Text_ArtistR5BeatenText
	end

Unova_Rt5_EventScript_Lider10::
	trainerbattle_single TRAINER_UNOVA_BACKERSF_R5, Unova_Rt5_Text_BackersFR5SeenText, Unova_Rt5_Text_BackersFR5BeatenText
	end

Unova_Rt5_EventScript_Lider11::
	trainerbattle_single TRAINER_UNOVA_BACKERSF_R5, Unova_Rt5_Text_BackersFR5SeenText, Unova_Rt5_Text_BackersFR5BeatenText
	end

Unova_Rt5_EventScript_Npc12::
	msgbox Unova_Rt5_Text_R5CharlesSeenText, MSGBOX_NPC
	end


Unova_Rt5_Text_R5BridgeSignText::
	.string "DRIFTVEIL"
	.string "\nDRAWBRIDGE."
	.string "\pInquire inside"
	.string "\nfor bridge access.$"

Unova_Rt5_Text_R5NimbasaSignText::
	.string "NIMBASA CITY"
	.string "\nahead.$"

Unova_Rt5_Text_Dancer1R5SeenText::
	.string "Turn around, and"
	.string "\nit's my turn. Turn"
	.string "\paround, and it's"
	.string "\nyour turn!$"

Unova_Rt5_Text_Dancer1R5BeatenText::
	.string "Turn around, turn"
	.string "\naround… and turn"
	.string "\laround some more!$"

Unova_Rt5_Text_Dancer2R5SeenText::
	.string "I can feel it in"
	.string "\nthe air… This"
	.string "\pbattle will be"
	.string "\nelectrifying!$"

Unova_Rt5_Text_Dancer2R5BeatenText::
	.string "What electrifying"
	.string "\nstrength! You"
	.string "\lshocked me good!$"

Unova_Rt5_Text_LinebackerR5SeenText::
	.string "Heheh! Nobody can"
	.string "\nbeat my speed and"
	.string "\lfury!$"

Unova_Rt5_Text_LinebackerR5BeatenText::
	.string "I have lost! I am"
	.string "\nsuch a loser!$"

Unova_Rt5_Text_BakerR5SeenText::
	.string "These POKéMON"
	.string "\nusually help me"
	.string "\pbake. But today,"
	.string "\nthey'll help me"
	.string "\lbattle you!$"

Unova_Rt5_Text_BakerR5BeatenText::
	.string "Battling is much"
	.string "\nmore difficult"
	.string "\lthan baking!$"

Unova_Rt5_Text_ArtistR5SeenText::
	.string "Art is explosions!"
	.string "\nLife forces colli-"
	.string "\lding together!$"

Unova_Rt5_Text_ArtistR5BeatenText::
	.string "Oh, I just got"
	.string "\nwhitewashed!$"

Unova_Rt5_Text_BackersFR5SeenText::
	.string "After watching a"
	.string "\nfootball game, we"
	.string "\pwant to get rowdy"
	.string "\nourselves!$"

Unova_Rt5_Text_BackersFR5BeatenText::
	.string "Too rowdy!$"

Unova_Rt5_Text_R5CharlesSeenText::
	.string "I'm a heart-"
	.string "\nbreaker… My name…"
	.string "\lCHARLES…"
	.string "\pYou… You wish to"
	.string "\nchallenge me…?"
	.string "\pPrepare… to be…"
	.string "\nheartbroken…$"

@ Placas trazidas do BW3G por dev_scripts/importa_placas_unova.py

@ Gruta escondida do BW3G (tier 1). ponytail: la ela reenche
@ todo dia; aqui e uma flag e o item sai uma vez so.
Unova_Rt5_EventScript_Gruta4B9::
	goto_if_set FLAG_UNOVA_GRUTA_R5, Unova_EventScript_GrutaVazia
	setflag FLAG_UNOVA_GRUTA_R5
	goto Unova_EventScript_GrutaTier1
