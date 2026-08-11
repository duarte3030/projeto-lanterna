FightAreaMart_MapScripts::
	.byte 0

FightAreaMart_EventScript_Caixa::
	lock
	faceplayer
	msgbox FightAreaMart_Text_Caixa, MSGBOX_DEFAULT
	pokemart FightAreaMart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
FightAreaMart_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

FightAreaMart_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

FightAreaMart_EventScript_Npc1::
	msgbox FightAreaMart_Text_Npc1, MSGBOX_NPC
	end

FightAreaMart_Text_Npc1:
	.string "What items should Pokémon hold?\nIt's an important question.\pHere's something else to think about.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

FightAreaMart_EventScript_Npc2::
	msgbox FightAreaMart_Text_Npc2, MSGBOX_NPC
	end

FightAreaMart_Text_Npc2:
	.string "An item that guarantees you won't\never lose a battle...\pThey don't sell anything like that.$"
