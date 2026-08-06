@ Rt2 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt2_MapScripts::
	.byte 0

Unova_Rt2_EventScript_Placa0::
	msgbox Unova_Rt2_Text_R2SignText, MSGBOX_SIGN
	end

Unova_Rt2_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_YOUNGSTER_R2, Unova_Rt2_Text_YoungsterR2SeenText, Unova_Rt2_Text_YoungsterR2BeatenText
	end

Unova_Rt2_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_LASS_R2, Unova_Rt2_Text_LassR2SeenText, Unova_Rt2_Text_LassR2BeatenText
	end

Unova_Rt2_EventScript_Lider10::
	trainerbattle_single TRAINER_UNOVA_SOCIALITE_R2, Unova_Rt2_Text_SocialiteR2SeenText, Unova_Rt2_Text_SocialiteR2BeatenText
	end

Unova_Rt2_EventScript_Lider11::
	trainerbattle_single TRAINER_UNOVA_GENTLEMAN_R2, Unova_Rt2_Text_GentlemanR2SeenText, Unova_Rt2_Text_GentlemanR2BeatenText
	end

Unova_Rt2_EventScript_Lider12::
	trainerbattle_single TRAINER_UNOVA_BACKPACKERM_R2, Unova_Rt2_Text_BackpackerMR2SeenText, Unova_Rt2_Text_BackpackerMR2BeatenText
	end

Unova_Rt2_EventScript_Lider13::
	trainerbattle_single TRAINER_UNOVA_BACKPACKERF_R2, Unova_Rt2_Text_BackpackerFR2SeenText, Unova_Rt2_Text_BackpackerFR2BeatenText
	end

Unova_Rt2_EventScript_Lider14::
	trainerbattle_single TRAINER_UNOVA_POLICEMAN_R2, Unova_Rt2_Text_PolicemanR2SeenText, Unova_Rt2_Text_PolicemanR2BeatenText
	end

Unova_Rt2_EventScript_Lider15::
	trainerbattle_single TRAINER_UNOVA_TWINS_R2, Unova_Rt2_Text_TwinsR2SeenText, Unova_Rt2_Text_TwinsR2BeatenText
	end

Unova_Rt2_EventScript_Lider16::
	trainerbattle_single TRAINER_UNOVA_TWINS_R2, Unova_Rt2_Text_TwinsR2SeenText, Unova_Rt2_Text_TwinsR2BeatenText
	end


Unova_Rt2_Text_R2SignText::
	.string "ROUTE 2."
	.string "\pSouth to ACCUMULA"
	.string "\nTOWN.$"

Unova_Rt2_Text_YoungsterR2SeenText::
	.string "My POKéMON are"
	.string "\ngonna steam you"
	.string "\lout!$"

Unova_Rt2_Text_YoungsterR2BeatenText::
	.string "We haven't lost in"
	.string "\nterms of coolness!"
	.string "\pI'll just keep"
	.string "\nthinking that…$"

Unova_Rt2_Text_LassR2SeenText::
	.string "Hi, hi! Trainer!"
	.string "\nI will let you see"
	.string "\pwhat kind of POKé-"
	.string "\nMON I have!$"

Unova_Rt2_Text_LassR2BeatenText::
	.string "Oooh, quit bugging"
	.string "\nme!$"

Unova_Rt2_Text_SocialiteR2SeenText::
	.string "Hello there, young"
	.string "\ntrainer. Please,"
	.string "\pbattle with me for"
	.string "\na spell.$"

Unova_Rt2_Text_SocialiteR2BeatenText::
	.string "My, oh my. Looks"
	.string "\nlike I lost!$"

Unova_Rt2_Text_GentlemanR2SeenText::
	.string "I've asked myself"
	.string "\nif it really is"
	.string "\pnatural for POKé-"
	.string "\nMON to live with"
	.string "\lpeople."
	.string "\pI still haven't"
	.string "\ncome up with an"
	.string "\lanswer.$"

Unova_Rt2_Text_GentlemanR2BeatenText::
	.string "All sorts of feel-"
	.string "\nings are stirred"
	.string "\lup by battling.$"

Unova_Rt2_Text_BackpackerMR2SeenText::
	.string "It's 'The Waving"
	.string "\nWeaving Walk'-"
	.string "\pWawalk for short!"
	.string "\pI wonder what kind"
	.string "\nof POKéMON we'll"
	.string "\lmeet today?$"

Unova_Rt2_Text_BackpackerMR2BeatenText::
	.string "Your POKéMON have"
	.string "\nstrong abilities,"
	.string "\ldon't they?$"

Unova_Rt2_Text_BackpackerFR2SeenText::
	.string "Let's see who has"
	.string "\nthe most admirable"
	.string "\lPOKéMON!$"

Unova_Rt2_Text_BackpackerFR2BeatenText::
	.string "Even though we"
	.string "\nlost, my POKéMON"
	.string "\pare still pretty"
	.string "\nadmirable.$"

Unova_Rt2_Text_PolicemanR2SeenText::
	.string "Hey, you! Stop"
	.string "\nright there!$"

Unova_Rt2_Text_PolicemanR2BeatenText::
	.string "There's no one"
	.string "\nstopping you!"
	.string "\pYou're what could"
	.string "\nbe called"
	.string "\lunstoppable!$"

Unova_Rt2_Text_TwinsR2SeenText::
	.string "Two POKéMON!"
	.string "\pStrong and strong"
	.string "\ncome together to"
	.string "\pbecome…"
	.string "\nvery strong!$"

Unova_Rt2_Text_TwinsR2BeatenText::
	.string "Uh oh… My POKéMON"
	.string "\nisn't looking so"
	.string "\lwell…$"

@ Placas trazidas do BW3G por dev_scripts/importa_placas_unova.py

@ Gruta escondida do BW3G (tier 2). ponytail: la ela reenche
@ todo dia; aqui e uma flag e o item sai uma vez so.
Unova_Rt2_EventScript_Gruta4BD::
	goto_if_set FLAG_UNOVA_GRUTA_R2, Unova_EventScript_GrutaVazia
	setflag FLAG_UNOVA_GRUTA_R2
	goto Unova_EventScript_GrutaTier2

@ NPCs ligados a partir do BW3G por dev_scripts/importa_npcs_unova.py

@ FRUITTREE_R_2 do BW3G. ponytail: no gen 2 a arvore reenche;
@ aqui a fruta sai uma vez, porque replantio e outra mecanica.
Unova_Rt2_EventScript_Arvore::
	lock
	goto_if_set FLAG_UNOVA_ARVORE_R_2, Unova_EventScript_GrutaVazia
	giveitem ITEM_RAWST_BERRY
	setflag FLAG_UNOVA_ARVORE_R_2
	release
	end
