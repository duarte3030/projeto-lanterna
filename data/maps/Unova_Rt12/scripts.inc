@ Rt12 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt12_MapScripts::
	.byte 0

Unova_Rt12_EventScript_Placa0::
	msgbox Unova_Rt12_Text_R12SignText, MSGBOX_SIGN
	end

Unova_Rt12_EventScript_Placa1::
	msgbox Unova_Rt12_Text_R12BridgeSignText, MSGBOX_SIGN
	end

Unova_Rt12_EventScript_Npc2::
	msgbox Unova_Rt12_Text_R12YoungsterText, MSGBOX_NPC
	end

Unova_Rt12_EventScript_Npc3::
	msgbox Unova_Rt12_Text_R12LassText, MSGBOX_NPC
	end

Unova_Rt12_EventScript_Npc4::
	msgbox Unova_Rt12_Text_R12PokefanFText, MSGBOX_NPC
	end


Unova_Rt12_Text_R12SignText::
	.string "ROUTE 12"
	.string "\pWest to VILLAGE"
	.string "\nBRIDGE.$"

Unova_Rt12_Text_R12BridgeSignText::
	.string "VILLAGE BRIDGE"
	.string "\pPassage to"
	.string "\nOPELUCID CITY.$"

Unova_Rt12_Text_R12YoungsterText::
	.string "POKéMON battles"
	.string "\nbegin when eyes"
	.string "\lmeet!"
	.string "\pIf I were a POKé-"
	.string "\nMON trainer, you"
	.string "\pand I would be"
	.string "\nbattling now!"
	.string "\p…But I don't have"
	.string "\nany POKéMON yet…$"

Unova_Rt12_Text_R12LassText::
	.string "ROUTE 12 is a good"
	.string "\nplace to find"
	.string "\lwild POKéMON!"
	.string "\pI'm looking for"
	.string "\na SHROOMISH, or"
	.string "\lmaybe a RALTS!$"

Unova_Rt12_Text_R12PokefanFText::
	.string "This ROUTE is so"
	.string "\nnice! It's close"
	.string "\pto town, so I"
	.string "\ndon't have to"
	.string "\pworry about my"
	.string "\nPOKéMON fainting.$"

@ NPCs ligados a partir do BW3G por dev_scripts/importa_npcs_unova.py

@ FRUITTREE_R_12 do BW3G. ponytail: no gen 2 a arvore reenche;
@ aqui a fruta sai uma vez, porque replantio e outra mecanica.
Unova_Rt12_EventScript_Arvore::
	lock
	goto_if_set FLAG_UNOVA_ARVORE_R_12, Unova_EventScript_GrutaVazia
	giveitem ITEM_ORAN_BERRY
	setflag FLAG_UNOVA_ARVORE_R_12
	release
	end
