OreburghCity_Mart_MapScripts::
	.byte 0

OreburghCity_Mart_EventScript_Cashier::
	lock
	faceplayer
	msgbox OreburghCity_Mart_Text_Cashier, MSGBOX_DEFAULT
	pokemart OreburghCity_Mart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
OreburghCity_Mart_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

OreburghCity_Mart_EventScript_Hiker::
	msgbox OreburghCity_Mart_Text_Hiker, MSGBOX_NPC
	end

OreburghCity_Mart_EventScript_Collector::
	msgbox OreburghCity_Mart_Text_Collector, MSGBOX_NPC
	end

OreburghCity_Mart_Text_Cashier:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

OreburghCity_Mart_Text_Hiker:
	.string "The OREBURGH MINE is right nearby.\n"
	.string "I always stock up here before I go in.$"

OreburghCity_Mart_Text_Collector:
	.string "I collect rare items from all over\n"
	.string "SINNOH. This MART always has something\l"
	.string "new for my collection.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

OreburghCity_Mart_EventScript_Npc1::
	msgbox OreburghCity_Mart_Text_Npc1, MSGBOX_NPC
	end

OreburghCity_Mart_Text_Npc1:
	.string "The Badges that Pokémon Gyms give you\nare a measure of a Trainer's worth.\pBy getting more Badges, you get to\nbuy more items in Poké Marts.$"

OreburghCity_Mart_EventScript_Npc2::
	msgbox OreburghCity_Mart_Text_Npc2, MSGBOX_NPC
	end

OreburghCity_Mart_Text_Npc2:
	.string "The Poké Mart is staffed by a lady and\na young fellow.\pThey offer different kinds of\nmerchandise. Did you know?$"
