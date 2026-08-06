VeilstoneStore2F_MapScripts::
	.byte 0

VeilstoneStore2F_EventScript_Caixa::
	lock
	faceplayer
	msgbox VeilstoneStore2F_Text_Caixa, MSGBOX_DEFAULT
	pokemart VeilstoneStore2F_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
VeilstoneStore2F_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

VeilstoneStore2F_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

VeilstoneStore2F_EventScript_Npc1::
	msgbox VeilstoneStore2F_Text_Npc1, MSGBOX_NPC
	end

VeilstoneStore2F_Text_Npc1:
	.string "We're giving away a Pokétch app for\nfree as a promotion.\pI can give you the Counter app\nover the counter. Would you like it?$"

VeilstoneStore2F_EventScript_Npc2::
	msgbox VeilstoneStore2F_Text_Npc2, MSGBOX_NPC
	end

VeilstoneStore2F_Text_Npc2:
	.string "Hello.\nMay I help you with anything?$"
