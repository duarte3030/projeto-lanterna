PastoriaCityMart_MapScripts::
	.byte 0

PastoriaCityMart_EventScript_Caixa::
	lock
	faceplayer
	msgbox PastoriaCityMart_Text_Caixa, MSGBOX_DEFAULT
	pokemart PastoriaCityMart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
PastoriaCityMart_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

PastoriaCityMart_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

PastoriaCityMart_EventScript_Npc1::
	msgbox PastoriaCityMart_Text_Npc1, MSGBOX_NPC
	end

PastoriaCityMart_Text_Npc1:
	.string "The Pokémon CROAGUNK is the city's\nofficial mascot.\pCROAGUNK sure is purdy--we're hopin'\nit'll get popular 'round the world.$"

PastoriaCityMart_EventScript_Npc2::
	msgbox PastoriaCityMart_Text_Npc2, MSGBOX_NPC
	end

PastoriaCityMart_Text_Npc2:
	.string "Put Seals on the Capsule, then put\nit on a Poké Ball...\pAnd done! Another Poké Ball made by\nme! It's one of a kind!\pGiggle...\nAre you using Ball Capsules?$"

PastoriaCityMart_EventScript_Placa3::
	msgbox PastoriaCityMart_Text_Placa3, MSGBOX_SIGN
	end

PastoriaCityMart_Text_Placa3:
	.string "It's a wood carving of the Pokémon\nCROAGUNK.\pEven though it's made of wood, it\nlooks like it's seeping poison...$"
