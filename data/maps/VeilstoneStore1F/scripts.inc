VeilstoneStore1F_MapScripts::
	.byte 0

VeilstoneStore1F_EventScript_Caixa::
	lock
	faceplayer
	msgbox VeilstoneStore1F_Text_Caixa, MSGBOX_DEFAULT
	pokemart VeilstoneStore1F_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
VeilstoneStore1F_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

VeilstoneStore1F_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

VeilstoneStore1F_EventScript_Npc1::
	msgbox VeilstoneStore1F_Text_Npc1, MSGBOX_NPC
	end

VeilstoneStore1F_Text_Npc1:
	.string "I made an Accessory modeled after\nthe Pokémon of a Trainer I met.\pWould you like one?$"
