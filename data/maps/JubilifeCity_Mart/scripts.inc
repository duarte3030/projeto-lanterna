JubilifeCity_Mart_MapScripts::
	.byte 0

JubilifeCity_Mart_EventScript_Cashier::
	lock
	faceplayer
	msgbox JubilifeCity_Mart_Text_Cashier, MSGBOX_DEFAULT
	pokemart JubilifeCity_Mart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
JubilifeCity_Mart_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	pokemartlistend

JubilifeCity_Mart_Text_Cashier:
	.string "Welcome to the POKéMON MART!\p"
	.string "Sorry, we're not able to sell\n"
	.string "anything just yet.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

JubilifeCity_Mart_EventScript_Npc1::
	msgbox JubilifeCity_Mart_Text_Npc1, MSGBOX_NPC
	end

JubilifeCity_Mart_Text_Npc1:
	.string "Aww, man.\nI wasted money on some Poké Balls.\pI should've lowered the HP of wild\nPokémon more before throwing them.$"

JubilifeCity_Mart_EventScript_Npc2::
	msgbox JubilifeCity_Mart_Text_Npc2, MSGBOX_NPC
	end

JubilifeCity_Mart_Text_Npc2:
	.string "The one thing you must remember is to\npack some Potions.\pIf all your Pokémon faint, it'll be\nlights out for you, too!$"

JubilifeCity_Mart_EventScript_Npc3::
	msgbox JubilifeCity_Mart_Text_Npc3, MSGBOX_NPC
	end

JubilifeCity_Mart_Text_Npc3:
	.string "Potions are important, but sometimes,\nit's better to simply avoid battles.\pIf you want to avoid wild Pokémon for a\nwhile, just use a Repel.\pAfter all, if you don't battle, your\nPokémon can't lose HP.$"

@ Lojas de Sinnoh portadas do pokeplatinum (dev_scripts/mudos_sinnoh.py --lojas-aplica)

@ loja_especial do Platinum (MART_SPECIALTIES_ID_JUBILIFE), tabela de include/data/mart_items.h
JubilifeCity_Mart_EventScript_Loja1::
	lock
	faceplayer
	msgbox JubilifeCity_Mart_Text_Cashier, MSGBOX_DEFAULT
	pokemart JubilifeCity_Mart_Pokemart_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
JubilifeCity_Mart_Pokemart_Loja1:
	.2byte ITEM_HEAL_BALL
	pokemartlistend
