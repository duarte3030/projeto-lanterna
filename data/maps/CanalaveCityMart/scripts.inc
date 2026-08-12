CanalaveCityMart_MapScripts::
	.byte 0

CanalaveCityMart_EventScript_Caixa::
	lock
	faceplayer
	msgbox CanalaveCityMart_Text_Caixa, MSGBOX_DEFAULT
	pokemart CanalaveCityMart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
CanalaveCityMart_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

CanalaveCityMart_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

CanalaveCityMart_EventScript_Npc1::
	msgbox CanalaveCityMart_Text_Npc1, MSGBOX_NPC
	end

CanalaveCityMart_Text_Npc1:
	.string "A Poké Ball that makes it easy to\ncatch the same kinds of Pokémon...\pWell, that's the Repeat Ball!$"

CanalaveCityMart_EventScript_Npc2::
	msgbox CanalaveCityMart_Text_Npc2, MSGBOX_NPC
	end

CanalaveCityMart_Text_Npc2:
	.string "I should take a Revive out to\neveryone training on Iron Island.\pI'm sure they'd appreciate it.\pIt can be rough out there, especially\nsince there's no Pokémon Center.$"

@ Lojas de Sinnoh portadas do pokeplatinum (dev_scripts/mudos_sinnoh.py --lojas-aplica)

@ loja_especial do Platinum (MART_SPECIALTIES_ID_CANALAVE), tabela de include/data/mart_items.h
CanalaveCityMart_EventScript_Loja1::
	lock
	faceplayer
	msgbox CanalaveCityMart_Text_Caixa, MSGBOX_DEFAULT
	pokemart CanalaveCityMart_Pokemart_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
CanalaveCityMart_Pokemart_Loja1:
	.2byte ITEM_QUICK_BALL
	.2byte ITEM_TIMER_BALL
	.2byte ITEM_REPEAT_BALL
	pokemartlistend
