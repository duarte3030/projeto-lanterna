@ DriftveilCity do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_DriftveilCity_MapScripts::
	.byte 0

Unova_DriftveilCity_EventScript_Placa0::
	msgbox Unova_DriftveilCity_Text_DriftveilSignText, MSGBOX_SIGN
	end

Unova_DriftveilCity_EventScript_Placa1::
	msgbox Unova_DriftveilCity_Text_DriftveilShelterText, MSGBOX_SIGN
	end

Unova_DriftveilCity_EventScript_Npc0::
	msgbox Unova_DriftveilCity_Text_DriftveilGuardText, MSGBOX_NPC
	end

Unova_DriftveilCity_EventScript_Npc1::
	msgbox Unova_DriftveilCity_Text_DriftveilGuardText, MSGBOX_NPC
	end

Unova_DriftveilCity_EventScript_Npc2::
	msgbox Unova_DriftveilCity_Text_DriftveilGuardText, MSGBOX_NPC
	end

Unova_DriftveilCity_EventScript_Npc3::
	msgbox Unova_DriftveilCity_Text_DriftveilGruntText, MSGBOX_NPC
	end

Unova_DriftveilCity_EventScript_Npc4::
	msgbox Unova_DriftveilCity_Text_DriftveilGruntText, MSGBOX_NPC
	end

Unova_DriftveilCity_EventScript_Npc7::
	msgbox Unova_DriftveilCity_Text_DriftveilMerchantEmptyText, MSGBOX_NPC
	end

Unova_DriftveilCity_EventScript_Npc8::
	msgbox Unova_DriftveilCity_Text_DriftveilLassText, MSGBOX_NPC
	end

Unova_DriftveilCity_EventScript_Npc9::
	msgbox Unova_DriftveilCity_Text_DriftveilYoungsterText, MSGBOX_NPC
	end

Unova_DriftveilCity_EventScript_Npc10::
	msgbox Unova_DriftveilCity_Text_DriftveilGrampsText, MSGBOX_NPC
	end

Unova_DriftveilCity_EventScript_Npc11::
	msgbox Unova_DriftveilCity_Text_DriftveilLass2Text, MSGBOX_NPC
	end


Unova_DriftveilCity_Text_DriftveilSignText::
	.string "DRIFTVEIL CITY."
	.string "\pA city of"
	.string "\nbillowing sails.$"

Unova_DriftveilCity_Text_DriftveilShelterText::
	.string "DRIFTVEIL CITY"
	.string "\nPOKéMON shelter.$"

Unova_DriftveilCity_Text_DriftveilGuardText::
	.string "Sorry, we're not"
	.string "\nletting anyone"
	.string "\lpast here."
	.string "\pThere's currently"
	.string "\nan investigation"
	.string "\lin progress.$"

Unova_DriftveilCity_Text_DriftveilGruntText::
	.string "Scram, kid! Can't"
	.string "\nyou see we're"
	.string "\lbusy?$"

Unova_DriftveilCity_Text_DriftveilMerchantEmptyText::
	.string "Sorry kid, you"
	.string "\nbought me out!$"

Unova_DriftveilCity_Text_DriftveilLassText::
	.string "I want to level up"
	.string "\nmy dear POKéMON so"
	.string "\pthey never have to"
	.string "\nfeel the sting of"
	.string "\ldefeat!$"

Unova_DriftveilCity_Text_DriftveilYoungsterText::
	.string "I wanted to cross"
	.string "\nthe DRAWBRIDGE"
	.string "\pto get to NIMBASA"
	.string "\nCITY, but some"
	.string "\psuspicious guys"
	.string "\nwon't let me"
	.string "\lthrough!$"

Unova_DriftveilCity_Text_DriftveilGrampsText::
	.string "The police are"
	.string "\nout and about…"
	.string "\pSomething strange"
	.string "\nis going on here…$"

Unova_DriftveilCity_Text_DriftveilLass2Text::
	.string "The people in the"
	.string "\nSTONE EMPORIUM are"
	.string "\lcrazy for gems!$"

@ NPCs ligados a partir do BW3G por dev_scripts/importa_npcs_unova.py

@ MART_MERCHANT_1 do BW3G (data/items/marts.asm)
Unova_DriftveilCity_EventScript_Loja0::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_DriftveilCity_EventScript_Loja0_Itens
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_DriftveilCity_EventScript_Loja0_Itens:
	.2byte ITEM_SILK_SCARF
	.2byte ITEM_MIRACLE_SEED
	.2byte ITEM_CHARCOAL
	.2byte ITEM_MYSTIC_WATER
	pokemartlistend

@ MART_MERCHANT_2 do BW3G (data/items/marts.asm)
Unova_DriftveilCity_EventScript_Loja1::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_DriftveilCity_EventScript_Loja1_Itens
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_DriftveilCity_EventScript_Loja1_Itens:
	.2byte ITEM_X_ATTACK
	.2byte ITEM_X_DEFEND
	.2byte ITEM_X_SPEED
	.2byte ITEM_X_SPECIAL
	.2byte ITEM_X_SP_DEF
	.2byte ITEM_X_ACCURACY
	.2byte ITEM_DIRE_HIT
	.2byte ITEM_GUARD_SPEC
	pokemartlistend
