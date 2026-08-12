CelesticTownNorthwestHouse_MapScripts::
	.byte 0

CelesticTownNorthwestHouse_EventScript_Npc1::
	msgbox CelesticTownNorthwestHouse_Text_Npc1, MSGBOX_NPC
	end

CelesticTownNorthwestHouse_Text_Npc1:
	.string "Putting on a pair of glasses changes\nhow the world looks.\pTaking off a pair of glasses changes\nhow the world looks, too. Deep, man.$"

@ Lojas de Sinnoh portadas do pokeplatinum (dev_scripts/mudos_sinnoh.py --lojas-aplica)

CelesticTownNorthwestHouse_Text_LojaSaudacao:
	.string "Welcome! Take a look around, we've\ngot everything a TRAINER needs.$"

@ loja_especial do Platinum (MART_SPECIALTIES_ID_CELESTIC), tabela de include/data/mart_items.h
CelesticTownNorthwestHouse_EventScript_Loja1::
	lock
	faceplayer
	msgbox CelesticTownNorthwestHouse_Text_LojaSaudacao, MSGBOX_DEFAULT
	pokemart CelesticTownNorthwestHouse_Pokemart_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
CelesticTownNorthwestHouse_Pokemart_Loja1:
	.2byte ITEM_DUSK_BALL
	.2byte ITEM_QUICK_BALL
	.2byte ITEM_TIMER_BALL
	pokemartlistend

@ loja_comum do Platinum (lista comum), tabela de include/data/mart_items.h
CelesticTownNorthwestHouse_EventScript_Loja2::
	lock
	faceplayer
	msgbox CelesticTownNorthwestHouse_Text_LojaSaudacao, MSGBOX_DEFAULT
	pokemart CelesticTownNorthwestHouse_Pokemart_Loja2
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
CelesticTownNorthwestHouse_Pokemart_Loja2:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend
