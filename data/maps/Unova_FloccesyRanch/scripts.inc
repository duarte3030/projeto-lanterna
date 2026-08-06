@ FloccesyRanch do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_FloccesyRanch_MapScripts::
	.byte 0

Unova_FloccesyRanch_EventScript_Placa0::
	msgbox Unova_FloccesyRanch_Text_FloccesyRanchSignText, MSGBOX_SIGN
	end


Unova_FloccesyRanch_Text_FloccesyRanchSignText::
	.string "FLOCCESY RANCH"
	.string "\pTry our MOOMOO"
	.string "\nMILK today!$"

@ Placas trazidas do BW3G por dev_scripts/importa_placas_unova.py

@ Gruta escondida do BW3G (tier 2). ponytail: la ela reenche
@ todo dia; aqui e uma flag e o item sai uma vez so.
Unova_FloccesyRanch_EventScript_Gruta4BB::
	goto_if_set FLAG_UNOVA_GRUTA_FLOCCESYRANCH, Unova_EventScript_GrutaVazia
	setflag FLAG_UNOVA_GRUTA_FLOCCESYRANCH
	goto Unova_EventScript_GrutaTier2

@ NPCs ligados a partir do BW3G por dev_scripts/importa_npcs_unova.py

@ FRUITTREE_FLOCCESY_RANCH do BW3G. ponytail: no gen 2 a arvore reenche;
@ aqui a fruta sai uma vez, porque replantio e outra mecanica.
Unova_FloccesyRanch_EventScript_Arvore::
	lock
	goto_if_set FLAG_UNOVA_ARVORE_FLOCCESY_RANCH, Unova_EventScript_GrutaVazia
	giveitem ITEM_ORAN_BERRY
	setflag FLAG_UNOVA_ARVORE_FLOCCESY_RANCH
	release
	end
