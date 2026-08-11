SnowpointCityMart_MapScripts::
	.byte 0

SnowpointCityMart_EventScript_Caixa::
	lock
	faceplayer
	msgbox SnowpointCityMart_Text_Caixa, MSGBOX_DEFAULT
	pokemart SnowpointCityMart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
SnowpointCityMart_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

SnowpointCityMart_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SnowpointCityMart_EventScript_Npc1::
	msgbox SnowpointCityMart_Text_Npc1, MSGBOX_NPC
	end

SnowpointCityMart_Text_Npc1:
	.string "I'm using Technical Machines to teach\nmoves to my Pokémon.\pI'm trying for different mixes of\nmoves in different types.\pIt's for when I go up against the Elite\nFour of the Pokémon League.\pThey say the Elite Four are tougher\nthan any Gym Leader by far.$"

SnowpointCityMart_EventScript_Npc2::
	msgbox SnowpointCityMart_Text_Npc2, MSGBOX_NPC
	end

SnowpointCityMart_Text_Npc2:
	.string "If your Pokémon gets frozen, it will\nthaw out after a while.\pBut if I were you, I'd keep some\nIce Heals around.$"
