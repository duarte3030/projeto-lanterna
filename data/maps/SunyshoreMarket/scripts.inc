SunyshoreMarket_MapScripts::
	.byte 0

SunyshoreMarket_EventScript_Caixa::
	lock
	faceplayer
	msgbox SunyshoreMarket_Text_Caixa, MSGBOX_DEFAULT
	pokemart SunyshoreMarket_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
SunyshoreMarket_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

SunyshoreMarket_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

SunyshoreMarket_EventScript_Npc1::
	msgbox SunyshoreMarket_Text_Npc1, MSGBOX_NPC
	end

SunyshoreMarket_Text_Npc1:
	.string "See the Seal Merchant there?$"

SunyshoreMarket_EventScript_Npc2::
	msgbox SunyshoreMarket_Text_Npc2, MSGBOX_NPC
	end

SunyshoreMarket_Text_Npc2:
	.string "Ah, please, allow me a little of your\ntime, if you will. You won't regret it.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SunyshoreMarket_EventScript_Npc1::
	msgbox SunyshoreMarket_Text_Npc1, MSGBOX_NPC
	end

SunyshoreMarket_Text_Npc1:
	.string "Sunyshore Market is best known for\nits big selection of Seals.$"

SunyshoreMarket_EventScript_Npc2::
	msgbox SunyshoreMarket_Text_Npc2, MSGBOX_NPC
	end

SunyshoreMarket_Text_Npc2:
	.string "I love Tap Toys!\nPlaza Games are great, too!\pI'm a huge fan of the Wi-Fi Plaza, so\nI'm promoting it on my own.$"
