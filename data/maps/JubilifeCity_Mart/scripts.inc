JubilifeCity_Mart_MapScripts::
	.byte 0

JubilifeCity_Mart_EventScript_Cashier::
	lock
	faceplayer
	msgbox JubilifeCity_Mart_Text_Cashier, MSGBOX_DEFAULT
	pokemart JubilifeCity_Mart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
JubilifeCity_Mart_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	pokemartlistend

JubilifeCity_Mart_EventScript_Guitarist::
	msgbox JubilifeCity_Mart_Text_Guitarist, MSGBOX_NPC
	end

JubilifeCity_Mart_EventScript_Pokefan::
	msgbox JubilifeCity_Mart_Text_Pokefan, MSGBOX_NPC
	end

JubilifeCity_Mart_Text_Cashier:
	.string "Welcome to the POKéMON MART!\p"
	.string "Sorry, we're not able to sell\n"
	.string "anything just yet.$"

JubilifeCity_Mart_Text_Guitarist:
	.string "I stop by here every day just to\n"
	.string "look at the new items.$"

JubilifeCity_Mart_Text_Pokefan:
	.string "This MART always has the freshest\n"
	.string "stock in all of JUBILIFE CITY.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

JubilifeCity_Mart_EventScript_Npc1::
	msgbox JubilifeCity_Mart_Text_Npc1, MSGBOX_NPC
	end

JubilifeCity_Mart_Text_Npc1:
	.string "Aww, man.\nI wasted money on some Poké Balls.\pI should've lowered the HP of wild\nPokémon more before throwing them.$"

JubilifeCity_Mart_EventScript_Npc2::
	msgbox JubilifeCity_Mart_Text_Npc2, MSGBOX_NPC
	end

JubilifeCity_Mart_Text_Npc2:
	.string "The one thing you must remember is to\npack some Potions.\pIf all your Pokémon faint, it'll be\nlights out for you, too!$"

JubilifeCity_Mart_EventScript_Npc3::
	msgbox JubilifeCity_Mart_Text_Npc3, MSGBOX_NPC
	end

JubilifeCity_Mart_Text_Npc3:
	.string "Potions are important, but sometimes,\nit's better to simply avoid battles.\pIf you want to avoid wild Pokémon for a\nwhile, just use a Repel.\pAfter all, if you don't battle, your\nPokémon can't lose HP.$"
