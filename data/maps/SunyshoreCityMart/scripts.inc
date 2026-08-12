SunyshoreCityMart_MapScripts::
	.byte 0

SunyshoreCityMart_EventScript_Caixa::
	lock
	faceplayer
	msgbox SunyshoreCityMart_Text_Caixa, MSGBOX_DEFAULT
	pokemart SunyshoreCityMart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
SunyshoreCityMart_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

SunyshoreCityMart_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SunyshoreCityMart_EventScript_Npc1::
	msgbox SunyshoreCityMart_Text_Npc1, MSGBOX_NPC
	end

SunyshoreCityMart_Text_Npc1:
	.string "I've heard about Victory Road, which\nleads to the Pokémon League.\pThe word is the road is harsh and\nharrowing.\pI'd better load up on as many items\nand as much medicine as I can carry...$"

SunyshoreCityMart_EventScript_Npc2::
	msgbox SunyshoreCityMart_Text_Npc2, MSGBOX_NPC
	end

SunyshoreCityMart_Text_Npc2:
	.string "I shall buy Seals for decorating Poké\nBalls at the Sunyshore Market.\pUsing those Seals in a cool way will be\nsure to impress my Pokémon!$"

@ Lojas de Sinnoh portadas do pokeplatinum (dev_scripts/mudos_sinnoh.py --lojas-aplica)

@ loja_especial do Platinum (MART_SPECIALTIES_ID_SUNYSHORE), tabela de include/data/mart_items.h
SunyshoreCityMart_EventScript_Loja1::
	lock
	faceplayer
	msgbox SunyshoreCityMart_Text_Caixa, MSGBOX_DEFAULT
	pokemart SunyshoreCityMart_Pokemart_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
SunyshoreCityMart_Pokemart_Loja1:
	.2byte ITEM_LUXURY_BALL
	pokemartlistend
