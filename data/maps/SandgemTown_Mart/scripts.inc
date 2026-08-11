SandgemTown_Mart_MapScripts::
	.byte 0

SandgemTown_Mart_EventScript_Clerk::
	lock
	faceplayer
	msgbox SandgemTown_Mart_Text_Clerk, MSGBOX_DEFAULT
	pokemart SandgemTown_Mart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
SandgemTown_Mart_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_ANTIDOTE
	pokemartlistend

SandgemTown_Mart_EventScript_SchoolKid::
	msgbox SandgemTown_Mart_Text_SchoolKid, MSGBOX_NPC
	end

SandgemTown_Mart_EventScript_Breeder::
	msgbox SandgemTown_Mart_Text_Breeder, MSGBOX_NPC
	end

SandgemTown_Mart_Text_Clerk:
	.string "Welcome to the SANDGEM TOWN MART!\p"
	.string "Take a look at our selection whenever\n"
	.string "you're ready.$"

SandgemTown_Mart_Text_SchoolKid:
	.string "I'm saving up my allowance for a new\n"
	.string "POKé BALL.$"

SandgemTown_Mart_Text_Breeder:
	.string "Stocking up on supplies before I head\n"
	.string "back out to the ROUTES.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SandgemTown_Mart_EventScript_Npc1::
	msgbox SandgemTown_Mart_Text_Npc1, MSGBOX_NPC
	end

SandgemTown_Mart_Text_Npc1:
	.string "If you come across a Pokémon you've\njust gotta have, toss a Poké Ball!\pNever leave home without one!$"

SandgemTown_Mart_EventScript_Npc2::
	msgbox SandgemTown_Mart_Text_Npc2, MSGBOX_NPC
	end

SandgemTown_Mart_Text_Npc2:
	.string "If a Pokémon loses all its HP,\nit can't battle anymore.\pI'm buying lots of Potions to avoid\nhaving that happen!$"
