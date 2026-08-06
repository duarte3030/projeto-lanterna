VeilstoneStore4F_MapScripts::
	.byte 0

VeilstoneStore4F_EventScript_Caixa::
	lock
	faceplayer
	msgbox VeilstoneStore4F_Text_Caixa, MSGBOX_DEFAULT
	pokemart VeilstoneStore4F_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
VeilstoneStore4F_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

VeilstoneStore4F_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

VeilstoneStore4F_EventScript_Npc1::
	msgbox VeilstoneStore4F_Text_Npc1, MSGBOX_NPC
	end

VeilstoneStore4F_Text_Npc1:
	.string "Hello.\nMay I help you with anything?$"
