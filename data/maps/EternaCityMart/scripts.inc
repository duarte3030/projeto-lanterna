EternaCityMart_MapScripts::
	.byte 0

EternaCityMart_EventScript_Caixa::
	lock
	faceplayer
	msgbox EternaCityMart_Text_Caixa, MSGBOX_DEFAULT
	pokemart EternaCityMart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
EternaCityMart_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

EternaCityMart_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

EternaCityMart_EventScript_Npc1::
	msgbox EternaCityMart_Text_Npc1, MSGBOX_NPC
	end

EternaCityMart_Text_Npc1:
	.string "The more Gym Badges you have, the\nbetter they treat you at Poké Marts.\pYou get to buy a better selection of\nmerchandise, you see.\pBut I don't have a single Gym Badge.\nIt's because Gardenia's too much!\pArgh! I don't want to see another\ngrass Pokémon ever again!\pIf only I had Flying-type Pokémon...\nThen my losing streak would end!$"

EternaCityMart_EventScript_Npc2::
	msgbox EternaCityMart_Text_Npc2, MSGBOX_NPC
	end

EternaCityMart_Text_Npc2:
	.string "An Escape Rope is indispensable!\pI wish I'd had one when I got into a \ntough spot in the Eterna Forest.\pI would've been able to warp to the\nentrance instantly!$"

@ Lojas de Sinnoh portadas do pokeplatinum (dev_scripts/mudos_sinnoh.py --lojas-aplica)

@ loja_especial do Platinum (MART_SPECIALTIES_ID_ETERNA_MART), tabela de include/data/mart_items.h
EternaCityMart_EventScript_Loja1::
	lock
	faceplayer
	msgbox EternaCityMart_Text_Caixa, MSGBOX_DEFAULT
	pokemart EternaCityMart_Pokemart_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
EternaCityMart_Pokemart_Loja1:
	.2byte ITEM_HEAL_BALL
	.2byte ITEM_NET_BALL
	.2byte ITEM_NEST_BALL
	pokemartlistend
