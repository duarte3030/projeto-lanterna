@ IcirrusBoutique do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_IcirrusBoutique_MapScripts::
	.byte 0

Unova_IcirrusBoutique_EventScript_Npc1::
	msgbox Unova_IcirrusBoutique_Text_IcirrusBoutiqueCooltrainerFText, MSGBOX_NPC
	end

Unova_IcirrusBoutique_EventScript_Npc2::
	msgbox Unova_IcirrusBoutique_Text_IcirrusBoutiqueBuenaText, MSGBOX_NPC
	end


Unova_IcirrusBoutique_Text_IcirrusBoutiqueCooltrainerFText::
	.string "The BOUTIQUE sells"
	.string "\nfashion for POKé-"
	.string "\lMON."
	.string "\pSome of the pieces"
	.string "\nhave useful"
	.string "\leffects in battle!$"

Unova_IcirrusBoutique_Text_IcirrusBoutiqueBuenaText::
	.string "I just love seeing"
	.string "\nthe selections!"
	.string "\pOh? You're not"
	.string "\ninterested in"
	.string "\lfashion?"
	.string "\pYou should pick"
	.string "\nout some cute"
	.string "\pthings for your"
	.string "\nPOKéMON instead!$"

@ NPCs ligados a partir do BW3G por dev_scripts/importa_npcs_unova.py

@ MART_BOUTIQUE do BW3G (data/items/marts.asm)
Unova_IcirrusBoutique_EventScript_Loja0::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_IcirrusBoutique_EventScript_Loja0_Itens
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_IcirrusBoutique_EventScript_Loja0_Itens:
	.2byte ITEM_BLACK_GLASSES
	.2byte ITEM_BLACK_BELT
	.2byte ITEM_MUSCLE_BAND
	.2byte ITEM_WISE_GLASSES
	.2byte ITEM_FOCUS_BAND
	pokemartlistend
