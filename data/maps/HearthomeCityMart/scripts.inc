HearthomeCityMart_MapScripts::
	.byte 0

HearthomeCityMart_EventScript_Caixa::
	lock
	faceplayer
	msgbox HearthomeCityMart_Text_Caixa, MSGBOX_DEFAULT
	pokemart HearthomeCityMart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
HearthomeCityMart_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

HearthomeCityMart_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

HearthomeCityMart_EventScript_Npc1::
	msgbox HearthomeCityMart_Text_Npc1, MSGBOX_NPC
	end

HearthomeCityMart_Text_Npc1:
	.string "The item Revive is something I could\nuse now.\pBut I've only got two Gym Badges, so\nI can't buy any yet...$"

HearthomeCityMart_EventScript_Npc2::
	msgbox HearthomeCityMart_Text_Npc2, MSGBOX_NPC
	end

HearthomeCityMart_Text_Npc2:
	.string "Do you know Amity Square?\nIt's a happy and cheerful place.\pYou can find Accessories there you\ncan't buy in Poké Marts.$"
