SolaceonTownMart_MapScripts::
	.byte 0

SolaceonTownMart_EventScript_Caixa::
	lock
	faceplayer
	msgbox SolaceonTownMart_Text_Caixa, MSGBOX_DEFAULT
	pokemart SolaceonTownMart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
SolaceonTownMart_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

SolaceonTownMart_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SolaceonTownMart_EventScript_Npc1::
	msgbox SolaceonTownMart_Text_Npc1, MSGBOX_NPC
	end

SolaceonTownMart_Text_Npc1:
	.string "Someone gave me a Seal Case.\nNow, I'm off to a Pokémon Center.\pYou see, you need to use a PC to put\nSeals on your Poké Balls.$"

SolaceonTownMart_EventScript_Npc2::
	msgbox SolaceonTownMart_Text_Npc2, MSGBOX_NPC
	end

SolaceonTownMart_Text_Npc2:
	.string "If you're not totally happy with Repel,\nconsider moving up to a Super Repel.$"
