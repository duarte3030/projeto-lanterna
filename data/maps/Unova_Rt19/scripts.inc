@ Rt19 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt19_MapScripts::
	.byte 0

Unova_Rt19_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_PKMN_BREEDERF_R19, Unova_Rt19_Text_PkmnBreederFR19SeenText, Unova_Rt19_Text_PkmnBreederFR19BeatenText
	end

Unova_Rt19_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_PKMN_BREEDERM_R19, Unova_Rt19_Text_PkmnBreederMR19SeenText, Unova_Rt19_Text_PkmnBreederMR19BeatenText
	end

Unova_Rt19_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_LADY_R19, Unova_Rt19_Text_LadyR19SeenText, Unova_Rt19_Text_LadyR19BeatenText
	end

Unova_Rt19_EventScript_Lider10::
	trainerbattle_single TRAINER_UNOVA_DEPOT_AGENT_R19_1, Unova_Rt19_Text_DepotAgent1R19SeenText, Unova_Rt19_Text_DepotAgent1R19BeatenText
	end

Unova_Rt19_EventScript_Lider11::
	trainerbattle_single TRAINER_UNOVA_DEPOT_AGENT_R19_2, Unova_Rt19_Text_DepotAgent2R19SeenText, Unova_Rt19_Text_DepotAgent2R19BeatenText
	end

Unova_Rt19_EventScript_Lider12::
	trainerbattle_single TRAINER_UNOVA_MAID_R19, Unova_Rt19_Text_MaidR19SeenText, Unova_Rt19_Text_MaidR19BeatenText
	end

Unova_Rt19_EventScript_Lider13::
	trainerbattle_single TRAINER_UNOVA_BAKER_R19, Unova_Rt19_Text_BakerR19SeenText, Unova_Rt19_Text_BakerR19BeatenText
	end


Unova_Rt19_Text_PkmnBreederFR19SeenText::
	.string "We are totally in"
	.string "\nsync! I will teach"
	.string "\pyou all about"
	.string "\nPOKéMON breeders!$"

Unova_Rt19_Text_PkmnBreederFR19BeatenText::
	.string "In fact, we"
	.string "\nlearned all about"
	.string "\lyou!$"

Unova_Rt19_Text_PkmnBreederMR19SeenText::
	.string "I'm always"
	.string "\npatrolling this"
	.string "\larea!$"

Unova_Rt19_Text_PkmnBreederMR19BeatenText::
	.string "I couldn't take"
	.string "\nadvantage of the"
	.string "\lterrain!$"

Unova_Rt19_Text_LadyR19SeenText::
	.string "Are you beautiful"
	.string "\nas a trainer?"
	.string "\lSurprise me!$"

Unova_Rt19_Text_LadyR19BeatenText::
	.string "…Strong and"
	.string "\nbeautiful! You"
	.string "\lcaptivated me!$"

Unova_Rt19_Text_DepotAgent1R19SeenText::
	.string "This is the battle"
	.string "\ntrain! All aboard!$"

Unova_Rt19_Text_DepotAgent1R19BeatenText::
	.string "You're the non-"
	.string "\nstop express line!$"

Unova_Rt19_Text_DepotAgent2R19SeenText::
	.string "I want you to tell"
	.string "\nme something!$"

Unova_Rt19_Text_DepotAgent2R19BeatenText::
	.string "You showed me your"
	.string "\nfull strength!$"

Unova_Rt19_Text_MaidR19SeenText::
	.string "You! Are you a fan"
	.string "\nof that person?"
	.string "\pBut that person is"
	.string "\nmine!$"

Unova_Rt19_Text_MaidR19BeatenText::
	.string "Oh no, oh why?"
	.string "\nI'm sorry…$"

Unova_Rt19_Text_BakerR19SeenText::
	.string "I'm not satisfied"
	.string "\nwith my baking."
	.string "\pAre you satisfied"
	.string "\nwith your POKéMON"
	.string "\ltraining?$"

Unova_Rt19_Text_BakerR19BeatenText::
	.string "Are you pleased"
	.string "\nwith your victory?"
	.string "\pOr are you"
	.string "\nunsatisfied?$"

@ Placas trazidas do BW3G por dev_scripts/importa_placas_unova.py

@ Gruta escondida do BW3G (tier 2). ponytail: la ela reenche
@ todo dia; aqui e uma flag e o item sai uma vez so.
Unova_Rt19_EventScript_Gruta4BA::
	goto_if_set FLAG_UNOVA_GRUTA_R19, Unova_EventScript_GrutaVazia
	setflag FLAG_UNOVA_GRUTA_R19
	goto Unova_EventScript_GrutaTier2

@ NPCs ligados a partir do BW3G por dev_scripts/importa_npcs_unova.py

@ FRUITTREE_R_19 do BW3G. ponytail: no gen 2 a arvore reenche;
@ aqui a fruta sai uma vez, porque replantio e outra mecanica.
Unova_Rt19_EventScript_Arvore::
	lock
	goto_if_set FLAG_UNOVA_ARVORE_R_19, Unova_EventScript_GrutaVazia
	giveitem ITEM_CHESTO_BERRY
	setflag FLAG_UNOVA_ARVORE_R_19
	release
	end
