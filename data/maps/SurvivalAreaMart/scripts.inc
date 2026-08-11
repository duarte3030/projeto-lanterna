SurvivalAreaMart_MapScripts::
	.byte 0

SurvivalAreaMart_EventScript_Caixa::
	lock
	faceplayer
	msgbox SurvivalAreaMart_Text_Caixa, MSGBOX_DEFAULT
	pokemart SurvivalAreaMart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
SurvivalAreaMart_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

SurvivalAreaMart_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SurvivalAreaMart_EventScript_Npc1::
	msgbox SurvivalAreaMart_Text_Npc1, MSGBOX_NPC
	end

SurvivalAreaMart_Text_Npc1:
	.string "I was on a 54-win streak...\nIf only I used that move when...$"

SurvivalAreaMart_EventScript_Npc2::
	msgbox SurvivalAreaMart_Text_Npc2, MSGBOX_NPC
	end

SurvivalAreaMart_Text_Npc2:
	.string "A word of advice from a grizzled\nmountain man!\pStark Mountain is a harsh, harsh place\nthat's rife with Fire-type Pokémon.\pWater-type Pokémon and moves should\ntake the edge off.\pThat's my advice.\nYou'd best heed it, no joke!$"
