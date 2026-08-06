VeilstoneStoreB1F_MapScripts::
	.byte 0

VeilstoneStoreB1F_EventScript_Caixa::
	lock
	faceplayer
	msgbox VeilstoneStoreB1F_Text_Caixa, MSGBOX_DEFAULT
	pokemart VeilstoneStoreB1F_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
VeilstoneStoreB1F_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

VeilstoneStoreB1F_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

VeilstoneStoreB1F_EventScript_Npc1::
	msgbox VeilstoneStoreB1F_Text_Npc1, MSGBOX_NPC
	end

VeilstoneStoreB1F_Text_Npc1:
	.string "Hello, there.\pWould you like some Lava Cookies?\nThey're $200 each.$"

VeilstoneStoreB1F_EventScript_Npc2::
	msgbox VeilstoneStoreB1F_Text_Npc2, MSGBOX_NPC
	end

VeilstoneStoreB1F_Text_Npc2:
	.string "Hello!\nI sell Poffins.\pThe ones I sell go for $6,400 each.\nWould you like one?$"
