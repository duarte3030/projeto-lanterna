SolaceonTownMart_MapScripts::
	.byte 0

SolaceonTownMart_EventScript_Caixa::
	lock
	faceplayer
	msgbox SolaceonTownMart_Text_Caixa, MSGBOX_DEFAULT
	pokemart SolaceonTownMart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
SolaceonTownMart_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

SolaceonTownMart_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"
