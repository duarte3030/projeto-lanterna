CycleShop_MapScripts::
	.byte 0

CycleShop_EventScript_Caixa::
	lock
	faceplayer
	msgbox CycleShop_Text_Caixa, MSGBOX_DEFAULT
	pokemart CycleShop_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
CycleShop_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

CycleShop_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

CycleShop_EventScript_Npc1::
	msgbox CycleShop_Text_Npc1, MSGBOX_NPC
	end

CycleShop_Text_Npc1:
	.string "The manager's gone off to the Team\nGalactic building and hasn't returned.\pI wonder what's holding him up?$"
