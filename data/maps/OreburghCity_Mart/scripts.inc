OreburghCity_Mart_MapScripts::
	.byte 0

OreburghCity_Mart_EventScript_Cashier::
	lock
	faceplayer
	msgbox OreburghCity_Mart_Text_Cashier, MSGBOX_DEFAULT
	pokemart OreburghCity_Mart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
OreburghCity_Mart_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

OreburghCity_Mart_Text_Cashier:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

OreburghCity_Mart_EventScript_Npc1::
	msgbox OreburghCity_Mart_Text_Npc1, MSGBOX_NPC
	end

OreburghCity_Mart_Text_Npc1:
	.string "The Badges that Pokémon Gyms give you\nare a measure of a Trainer's worth.\pBy getting more Badges, you get to\nbuy more items in Poké Marts.$"

OreburghCity_Mart_EventScript_Npc2::
	msgbox OreburghCity_Mart_Text_Npc2, MSGBOX_NPC
	end

OreburghCity_Mart_Text_Npc2:
	.string "The Poké Mart is staffed by a lady and\na young fellow.\pThey offer different kinds of\nmerchandise. Did you know?$"

@ Lojas de Sinnoh portadas do pokeplatinum (dev_scripts/mudos_sinnoh.py --lojas-aplica)

@ loja_especial do Platinum (MART_SPECIALTIES_ID_OREBURGH), tabela de include/data/mart_items.h
OreburghCity_Mart_EventScript_Loja1::
	lock
	faceplayer
	msgbox OreburghCity_Mart_Text_Cashier, MSGBOX_DEFAULT
	pokemart OreburghCity_Mart_Pokemart_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
OreburghCity_Mart_Pokemart_Loja1:
	.2byte ITEM_HEAL_BALL
	.2byte ITEM_NET_BALL
	pokemartlistend
