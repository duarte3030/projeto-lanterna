@ NimbasaBallMart do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_NimbasaBallMart_MapScripts::
	.byte 0

Unova_NimbasaBallMart_EventScript_Npc1::
	msgbox Unova_NimbasaBallMart_Text_NimbasaBallMartRangerMText, MSGBOX_NPC
	end

Unova_NimbasaBallMart_EventScript_Npc2::
	msgbox Unova_NimbasaBallMart_Text_NimbasaBallMartLassText, MSGBOX_NPC
	end


Unova_NimbasaBallMart_Text_NimbasaBallMartRangerMText::
	.string "Different kinds of"
	.string "\nPOKéBALLS are good"
	.string "\pfor different"
	.string "\nsituations. Use"
	.string "\pthe best BALL for"
	.string "\nthe job!$"

Unova_NimbasaBallMart_Text_NimbasaBallMartLassText::
	.string "NET BALLS are good"
	.string "\nfor catching bug"
	.string "\land water type"
	.string "\lPOKéMON.$"

@ NPCs ligados a partir do BW3G por dev_scripts/importa_npcs_unova.py

@ MART_NIMBASA_BALL do BW3G (data/items/marts.asm)
Unova_NimbasaBallMart_EventScript_Loja0::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_NimbasaBallMart_EventScript_Loja0_Itens
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_NimbasaBallMart_EventScript_Loja0_Itens:
	.2byte ITEM_FRIEND_BALL
	.2byte ITEM_HEAVY_BALL
	.2byte ITEM_LURE_BALL
	.2byte ITEM_QUICK_BALL
	.2byte ITEM_TIMER_BALL
	.2byte ITEM_NET_BALL
	.2byte ITEM_DUSK_BALL
	.2byte ITEM_REPEAT_BALL
	.2byte ITEM_DIVE_BALL
	.2byte ITEM_LEVEL_BALL
	.2byte ITEM_LOVE_BALL
	pokemartlistend
