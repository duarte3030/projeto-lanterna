VeilstoneStore5F_MapScripts::
	.byte 0

VeilstoneStore5F_EventScript_Caixa::
	lock
	faceplayer
	msgbox VeilstoneStore5F_Text_Caixa, MSGBOX_DEFAULT
	pokemart VeilstoneStore5F_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
VeilstoneStore5F_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

VeilstoneStore5F_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

VeilstoneStore5F_EventScript_Npc1::
	msgbox VeilstoneStore5F_Text_Npc1, MSGBOX_NPC
	end

VeilstoneStore5F_Text_Npc1:
	.string "Ah, young Pokémon Trainer...\pAs your senior in life, let me make\na gift of this Sticky Barb!$"

VeilstoneStore5F_EventScript_Placa1::
	msgbox VeilstoneStore5F_Text_Placa1, MSGBOX_SIGN
	end

VeilstoneStore5F_Text_Placa1:
	.string "It's a Vending Machine.\nWhich drink would you like?$"

VeilstoneStore5F_EventScript_Placa2::
	msgbox VeilstoneStore5F_Text_Placa2, MSGBOX_SIGN
	end

VeilstoneStore5F_Text_Placa2:
	.string "It's a Vending Machine.\nWhich drink would you like?$"
