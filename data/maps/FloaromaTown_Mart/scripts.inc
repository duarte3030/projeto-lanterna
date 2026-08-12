FloaromaTown_Mart_MapScripts::
	.byte 0

FloaromaTown_Mart_EventScript_Cashier::
	lock
	faceplayer
	msgbox FloaromaTown_Mart_Text_Cashier, MSGBOX_DEFAULT
	pokemart FloaromaTown_Mart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
FloaromaTown_Mart_Pokemart:
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_REVIVE
	.2byte ITEM_ESCAPE_ROPE
	pokemartlistend

FloaromaTown_Mart_Text_Cashier:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

FloaromaTown_Mart_EventScript_Npc1::
	msgbox FloaromaTown_Mart_Text_Npc1, MSGBOX_NPC
	end

FloaromaTown_Mart_Text_Npc1:
	.string "I'm going to dress up my Pokémon with\ncute Accessories and take it to the\pTV station in Jubilife City.\pThat way, everyone in the region\nwill be able to see my Pokémon!$"

FloaromaTown_Mart_EventScript_Npc2::
	msgbox FloaromaTown_Mart_Text_Npc2, MSGBOX_NPC
	end

FloaromaTown_Mart_Text_Npc2:
	.string "You can't buy Berries or Accessories\nat Poké Marts.\pIt's better for me that way.\nI won't waste money impulse shopping.$"

@ Lojas de Sinnoh portadas do pokeplatinum (dev_scripts/mudos_sinnoh.py --lojas-aplica)

@ loja_especial do Platinum (MART_SPECIALTIES_ID_FLOAROMA), tabela de include/data/mart_items.h
FloaromaTown_Mart_EventScript_Loja1::
	lock
	faceplayer
	msgbox FloaromaTown_Mart_Text_Cashier, MSGBOX_DEFAULT
	pokemart FloaromaTown_Mart_Pokemart_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
FloaromaTown_Mart_Pokemart_Loja1:
	.2byte ITEM_HEAL_BALL
	.2byte ITEM_NET_BALL
	pokemartlistend
