EternaCityHerbShop_MapScripts::
	.byte 0

EternaCityHerbShop_EventScript_Caixa::
	lock
	faceplayer
	msgbox EternaCityHerbShop_Text_Caixa, MSGBOX_DEFAULT
	pokemart EternaCityHerbShop_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
EternaCityHerbShop_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

EternaCityHerbShop_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

EternaCityHerbShop_EventScript_Npc1::
	msgbox EternaCityHerbShop_Text_Npc1, MSGBOX_NPC
	end

EternaCityHerbShop_Text_Npc1:
	.string "Welcome to the Herb Shop, home of\neffective yet inexpensive medicine.$"
