VeilstoneCityPrizeExchange_MapScripts::
	.byte 0

VeilstoneCityPrizeExchange_EventScript_Caixa::
	lock
	faceplayer
	msgbox VeilstoneCityPrizeExchange_Text_Caixa, MSGBOX_DEFAULT
	pokemart VeilstoneCityPrizeExchange_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
VeilstoneCityPrizeExchange_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

VeilstoneCityPrizeExchange_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

VeilstoneCityPrizeExchange_EventScript_Npc1::
	msgbox VeilstoneCityPrizeExchange_Text_Npc1, MSGBOX_NPC
	end

VeilstoneCityPrizeExchange_Text_Npc1:
	.string "Welcome!\pYou may exchange your Coins for\nfabulous prizes here!$"

VeilstoneCityPrizeExchange_EventScript_Npc2::
	msgbox VeilstoneCityPrizeExchange_Text_Npc2, MSGBOX_NPC
	end

VeilstoneCityPrizeExchange_Text_Npc2:
	.string "I woke up and realized my potential!\pSo, what potential was woken in me?\nWhat's my hidden power, you ask?\pIt's a power that lets me see the\nHidden Power of a Pokémon.\pWhen they learn that move, I can tell\nwhat type the move will be.\pSo, want me to use my hidden power?\pI'll tell you what type your Pokémon's\nHidden Power will be.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

VeilstoneCityPrizeExchange_EventScript_Npc3::
	msgbox VeilstoneCityPrizeExchange_Text_Npc3, MSGBOX_NPC
	end

VeilstoneCityPrizeExchange_Text_Npc3:
	.string "They have prizes I really want.\nBut Coins, I have none!$"
