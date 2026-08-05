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
